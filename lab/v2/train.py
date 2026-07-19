"""v2/train.py — arm runner.

Arms (bars.json):
    COTRAIN  trunk+bridge co-trained, per-example store rotation   [the hypothesis]
    BOLT     trunk FROZEN (loaded from NOSTORE), bridge trained    [== H_9392 BRIDGE-BOLT]
    NOSTORE  no store at all, same budget                          [memorisation ceiling]
    SLOWROT  COTRAIN but rotation every 500 steps                  [isolates rotation]

Only the trunk is frozen in BOLT — lam/W_q/W_out/W_k/val still train. That isolates the
COTRAIN-BOLT difference down to ONE thing: trunk co-adaptation. And BOLT gets its honest
best lr from the frozen grid, picked on TRAIN LOSS (never on eval DV — picking on DV would
be tune-to-green). An arm that dies must die having been given its best shot.
"""

import argparse
import json
import os
import pickle
import time

import numpy as np

import gen
import model as M
from loss import forward_loss

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/v2"    # mix (V2_1); logit (V2_2) -> /tmp/v2-logit


def load_bars():
    return json.load(open(os.path.join(HERE, "bars.json")))


def encode_batch(examples, cfg):
    """Pack examples into (ids, targets, loss_mask, store_ids, val_idx, qpos, ans_pos)."""
    B = len(examples)
    T = cfg["max_seq"]
    nl = 5
    ids = np.zeros((B, T), dtype=np.int64)
    targets = np.zeros((B, T), dtype=np.int64)
    mask = np.zeros((B, T))
    S = len(examples[0]["store_names"])
    store_ids = np.zeros((B, S, nl), dtype=np.int64)
    val_idx = np.zeros((B, S), dtype=np.int64)
    qpos = np.zeros(B, dtype=np.int64)
    ans_pos = np.zeros(B, dtype=np.int64)

    for i, ex in enumerate(examples):
        seq = ex["prompt"] + ex["answer"] + b"\n"
        if len(seq) > T:
            raise ValueError(f"seq {len(seq)} > max_seq {T}")
        arr = np.frombuffer(seq, dtype=np.uint8).astype(np.int64)
        ids[i, : len(arr)] = arr
        # next-byte targets; CE counted on the answer bytes only
        targets[i, : len(arr) - 1] = arr[1:]
        p_len = len(ex["prompt"])
        mask[i, p_len - 1 : len(arr) - 1] = 1.0
        qpos[i] = p_len - 1          # last prompt byte: its hidden predicts answer byte 0
        ans_pos[i] = p_len - 1
        for s, nm in enumerate(ex["store_names"]):
            store_ids[i, s] = np.frombuffer(nm.encode(), dtype=np.uint8).astype(np.int64)
        val_idx[i] = ex["store_pols"]
    return ids, targets, mask, store_ids, val_idx, qpos, ans_pos


class Adam:
    def __init__(self, params, lr, frozen=()):
        self.lr = lr
        self.frozen = set(frozen)
        self.m = {k: np.zeros_like(v) for k, v in params.items()}
        self.v = {k: np.zeros_like(v) for k, v in params.items()}
        self.t = 0

    def step(self, params, grads, lr_scale=1.0):
        self.t += 1
        b1, b2, eps = 0.9, 0.999, 1e-8
        for k in params:
            if k in self.frozen:
                continue
            g = grads.get(k)
            if g is None:
                continue
            self.m[k] = b1 * self.m[k] + (1 - b1) * g
            self.v[k] = b2 * self.v[k] + (1 - b2) * (g * g)
            mh = self.m[k] / (1 - b1**self.t)
            vh = self.v[k] / (1 - b2**self.t)
            params[k] -= self.lr * lr_scale * mh / (np.sqrt(vh) + eps)


def out_dir(gate, readout="linear", tag=""):
    t = gate + ("-mlp" if readout == "mlp" else "") + tag
    return f"/tmp/v2-{t}"


def train_arm(arm, seed, bars, lr=None, steps=None, quiet=False, gate="mix", readout="linear", tag="", fixed_key=False):
    cfg = dict(bars["model"])
    cfg["max_seq"] = bars["task"]["max_seq"]
    cfg["gate"] = gate
    cfg["readout"] = readout
    cfg["fixed_key"] = fixed_key
    t = bars["task"]
    b = bars["budget"]
    steps = steps or b["steps"]
    lr = lr or b["lr"]

    use_store = arm != "NOSTORE"
    rotate = 500 if arm == "SLOWROT" else 1
    oracle = arm == "ORACLE"   # C0-e positive control: retrieval handed over for free

    train_ent, _ = gen.split_pool(t["entity_pool"], t["entity_train"], t["entity_eval"])
    stream = gen.Stream(seed, train_ent, t["store_slots"], rotate_every=rotate)

    rng = np.random.default_rng(seed)
    p = M.init_params(cfg, rng, with_store=use_store)

    frozen = ()
    if arm == "BOLT":
        src = os.path.join(out_dir(gate, readout, tag), f"NOSTORE_seed{seed}.pkl")
        if not os.path.exists(src):
            raise SystemExit(f"BOLT needs the NOSTORE trunk first: {src} missing")
        trunk = pickle.load(open(src, "rb"))["params"]
        for k, v in trunk.items():
            if not M.is_bridge(k):
                p[k] = v.copy()
        frozen = tuple(k for k in p if not M.is_bridge(k))  # trunk frozen; bridge trains

    opt = Adam(p, lr, frozen=frozen)
    t0 = time.time()
    losses = []
    for step in range(steps):
        exs = stream.batch(b["batch"])
        ids, tg, mask, sids, vidx, qp, ap = encode_batch(exs, cfg)
        oslot = np.array([e["slot"] for e in exs]) if oracle else None
        loss, grads = forward_loss(p, cfg, ids, tg, mask, sids, vidx, qp, ap,
                                   use_store=use_store, backward=True, oracle_slot=oslot,
                                   gate=gate)
        scale = min(1.0, (step + 1) / b["warmup"])
        opt.step(p, grads, lr_scale=scale)
        losses.append(loss)
        if not quiet and (step % 400 == 0 or step == steps - 1):
            lam = float(M.sigmoid(p["lam_raw"][0])) if use_store else float("nan")
            print(f"  [{arm} s{seed}] step {step:5d}  loss {np.mean(losses[-100:]):.4f}  "
                  f"lam {lam:.3f}  ({time.time()-t0:.0f}s)")
    od = out_dir(gate, readout, tag)
    os.makedirs(od, exist_ok=True)
    path = os.path.join(od, f"{arm}_seed{seed}.pkl")
    pickle.dump({"params": p, "cfg": cfg, "arm": arm, "seed": seed, "gate": gate,
                 "final_loss": float(np.mean(losses[-100:])), "lr": lr}, open(path, "wb"))
    return path, float(np.mean(losses[-100:]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True,
                    choices=["COTRAIN", "BOLT", "NOSTORE", "SLOWROT", "ORACLE"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--gate", choices=["mix", "logit", "store_only"], default="mix")
    ap.add_argument("--readout", choices=["linear", "mlp"], default="linear")
    ap.add_argument("--tag", default="")
    ap.add_argument("--fixed-key", action="store_true", dest="fixed_key")
    args = ap.parse_args()

    bars = load_bars()
    if args.arm == "BOLT":
        # frozen lr grid, selected on TRAIN LOSS only (bars.json bolt_lr_selected_by)
        best = None
        for lr in bars["budget"]["bolt_lr_grid"]:
            _, fl = train_arm("BOLT", args.seed, bars, lr=lr, steps=args.steps, quiet=True, gate=args.gate, readout=args.readout, tag=args.tag, fixed_key=args.fixed_key)
            print(f"  [BOLT s{args.seed}] lr={lr} -> train_loss {fl:.4f}")
            if best is None or fl < best[1]:
                best = (lr, fl)
        print(f"  [BOLT s{args.seed}] selected lr={best[0]} (train_loss {best[1]:.4f})")
        path, fl = train_arm("BOLT", args.seed, bars, lr=best[0], steps=args.steps, gate=args.gate, readout=args.readout, tag=args.tag, fixed_key=args.fixed_key)
    else:
        path, fl = train_arm(args.arm, args.seed, bars, steps=args.steps, gate=args.gate, readout=args.readout, tag=args.tag, fixed_key=args.fixed_key)
    print(f"{args.arm} seed{args.seed}: final_loss={fl:.4f} -> {path}")


if __name__ == "__main__":
    main()
