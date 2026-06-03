#!/usr/bin/env python3
"""Lane P (GPU-torch) — TRAIN/VAL split generalization test for the d768 E2/L1 CLM.

substrate = GPU-torch (Lane P), distinct from Lane A (AKIDA) / Lane G (forge).
a_lane_akida_gpu_split — torch CE-descent path, NOT forge util.

WHY THIS EXISTS (the honest memorization-vs-generalization test):
  The landed F-CLM-LANEP-TRAIN reached final_eval_ce=0.0986 on the 402KB corpus,
  but its "held-window" eval drew random windows from the SAME stream it trained
  on (train_lane_p.py make_batch/eval_ce share one `stream`), so the eval data
  OVERLAPS the training data. 0.0986 could be MEMORIZATION, not generalization.

  This trainer holds out a CONTIGUOUS 10% block AND a RANDOM-scattered 10% as VAL,
  NEVER samples a training window that touches a held-out byte position, trains on
  the remaining ~80%, and reports train_ce vs (contig-val_ce, rand-val_ce) + the GAP.

  val_ce ~= train_ce  -> GENERALIZES  -> F-CLM-LANEP-GEN=1
  val_ce >> train_ce  -> MEMORIZATION -> honest closed-negative, F-CLM-LANEP-GEN=0

  Same model/cfg/optimizer as the landed run (d768 E2 L1 K3 V256, bf16, AdamW).
  CE numbers are the live optimizer's mean CE per logged window — NO fabrication
  (g63/p7). A memorization finding is a VALID honest result (a_paper_negative_ok);
  this does NOT force a pass.
"""
from __future__ import annotations

import argparse, hashlib, json, os, sys, time

import torch
import torch.nn as nn
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM = os.path.dirname(_HERE)
_MODEL = os.path.join(_CLM, "model")
if _MODEL not in sys.path:
    sys.path.insert(0, _MODEL)

from model import CLMConfig, CLMConvMoE          # noqa: E402
import clm_serialize_v2 as S                      # noqa: E402


def load_byte_stream(path: str):
    with open(path, "rb") as f:
        raw = f.read()
    sha = hashlib.sha256(raw).hexdigest()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8).long(), len(raw), sha


def build_split_segments(n_total, seq_len, val_frac=0.10, seed=42):
    """Partition [0, n_total) into TRAIN / VAL-contig / VAL-rand position sets.

    Returns three lists of (start, end) half-open segments that are MUTUALLY
    DISJOINT in byte-position space. A training window [i, i+seq_len+1) is only
    ever sampled fully inside a TRAIN segment (boundary-crossing windows are
    never produced), so NO training input or target byte ever lands in a held-out
    position. The contiguous-VAL block tests held-out generalization on an unseen
    contiguous region; the random-VAL scatter tests it on positions interleaved
    through the trained region (a harder, distribution-matched held-out probe).
    """
    rng = torch.Generator().manual_seed(seed)
    n_val_contig = int(n_total * val_frac)
    n_val_rand = int(n_total * val_frac)

    # contiguous VAL block: a single chunk placed at 70% through the stream
    c_start = int(n_total * 0.70)
    c_end = c_start + n_val_contig
    contig = [(c_start, c_end)]

    # random VAL scatter: K mini-blocks (each >> seq_len so an interior window
    # fits) drawn from the region OUTSIDE the contiguous block.
    block = max(seq_len * 4, 1024)
    n_blocks = max(1, n_val_rand // block)
    rand_segs = []
    occupied = [(c_start, c_end)]
    tries = 0
    while len(rand_segs) < n_blocks and tries < n_blocks * 50:
        tries += 1
        s = int(torch.randint(0, n_total - block - 1, (1,), generator=rng).item())
        e = s + block
        if any(not (e <= os_ or s >= oe) for (os_, oe) in occupied):
            continue
        rand_segs.append((s, e))
        occupied.append((s, e))
    rand_segs.sort()

    # TRAIN = complement of (contig ∪ rand) over [0, n_total)
    held = sorted(contig + rand_segs)
    train_segs = []
    cur = 0
    for (s, e) in held:
        if s > cur:
            train_segs.append((cur, s))
        cur = max(cur, e)
    if cur < n_total:
        train_segs.append((cur, n_total))

    # keep only segments long enough to host an interior window
    need = seq_len + 1
    train_segs = [(s, e) for (s, e) in train_segs if e - s >= need]
    contig = [(s, e) for (s, e) in contig if e - s >= need]
    rand_segs = [(s, e) for (s, e) in rand_segs if e - s >= need]
    return train_segs, contig, rand_segs


def _seg_weights(segs, seq_len):
    need = seq_len + 1
    w = torch.tensor([max(0, (e - s) - need + 1) for (s, e) in segs], dtype=torch.double)
    return w / w.sum()


def make_batch_from_segs(stream, segs, seg_w, seq_len, batch_size, device, gen):
    """Sample windows ENTIRELY inside the given segments (no boundary cross)."""
    need = seq_len + 1
    seg_idx = torch.multinomial(seg_w, batch_size, replacement=True, generator=gen)
    xs, ys = [], []
    for si in seg_idx.tolist():
        s, e = segs[si]
        hi = (e - need) - s          # inclusive max offset within segment
        off = int(torch.randint(0, hi + 1, (1,), generator=gen).item())
        i = s + off
        xs.append(stream[i:i + seq_len])
        ys.append(stream[i + 1:i + 1 + seq_len])
    x = torch.stack(xs).to(device)
    y = torch.stack(ys).to(device)
    return x, y


@torch.no_grad()
def eval_ce_segs(model, stream, segs, seg_w, seq_len, batch_size, device, gen, iters=40):
    model.eval()
    tot = 0.0
    for _ in range(iters):
        x, y = make_batch_from_segs(stream, segs, seg_w, seq_len, batch_size, device, gen)
        out = model(x, y)
        tot += float(out["ce_loss"])
    model.train()
    return tot / iters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--seq-len", type=int, default=256)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-frac", type=float, default=0.10)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ckpt-out", default=None)
    ap.add_argument("--clm-out", default=None)
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--log-every", type=int, default=200)
    ap.add_argument("--bf16", action="store_true")
    a = ap.parse_args()

    torch.manual_seed(a.seed)
    gen = torch.Generator().manual_seed(a.seed)

    assert torch.cuda.is_available(), "CUDA REQUIRED for Lane P production rung (g63: no silent CPU)"
    device = "cuda"
    cap = torch.cuda.get_device_capability()
    print(f"DEVICE cuda name={torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
          f"torch={torch.__version__}", flush=True)

    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=a.d_model,
                    kernel_size=3, variant="AB")
    model = CLMConvMoE(cfg).to(device)
    n_params = model.num_params()
    print(f"PARAMS n_params={n_params} ({n_params/1e6:.3f}M) "
          f"d={a.d_model} E={cfg.n_experts} L={cfg.n_trunk_layers} K={cfg.kernel_size} V={cfg.vocab_size}",
          flush=True)

    stream, nbytes, sha = load_byte_stream(a.corpus)
    print(f"CORPUS path={a.corpus} bytes={nbytes} sha256={sha}", flush=True)

    train_segs, contig_segs, rand_segs = build_split_segments(
        nbytes, a.seq_len, val_frac=a.val_frac, seed=a.seed)
    tw = _seg_weights(train_segs, a.seq_len)
    cw = _seg_weights(contig_segs, a.seq_len)
    rw = _seg_weights(rand_segs, a.seq_len)
    train_bytes = sum(e - s for s, e in train_segs)
    contig_bytes = sum(e - s for s, e in contig_segs)
    rand_bytes = sum(e - s for s, e in rand_segs)
    print(f"SPLIT train_bytes={train_bytes} ({100*train_bytes/nbytes:.1f}%) "
          f"contig_val_bytes={contig_bytes} ({100*contig_bytes/nbytes:.1f}%) "
          f"rand_val_bytes={rand_bytes} ({100*rand_bytes/nbytes:.1f}%) "
          f"train_segs={len(train_segs)} rand_blocks={len(rand_segs)}", flush=True)
    # leakage assertion: held-out segments disjoint from every train segment
    held_all = contig_segs + rand_segs
    for (hs, he) in held_all:
        for (ts, te) in train_segs:
            assert he <= ts or hs >= te, f"LEAK: held [{hs},{he}) overlaps train [{ts},{te})"
    print("LEAK_CHECK pass (held-out segments disjoint from train segments)", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95),
                            weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min((s + 1) / a.warmup, 1.0) *
                       (0.5 * (1 + torch.cos(torch.tensor(
                           3.14159265 * min(s, a.steps) / a.steps)).item())
                        if s >= a.warmup else 1.0))

    use_bf16 = a.bf16
    model.train()
    t0 = time.time()
    descent = []
    first_ce = None
    for step in range(a.steps):
        x, y = make_batch_from_segs(stream, train_segs, tw, a.seq_len, a.batch_size, device, gen)
        opt.zero_grad(set_to_none=True)
        if use_bf16:
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                loss = out["loss"]
            loss.backward()
        else:
            out = model(x, y)
            loss = out["loss"]
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        ce = float(out["ce_loss"])
        if first_ce is None:
            first_ce = ce
        if step % a.log_every == 0 or step == a.steps - 1:
            descent.append((step, round(ce, 5)))
            print(f"STEP {step:6d} ce={ce:.5f} loss={float(loss):.5f} "
                  f"lr={sched.get_last_lr()[0]:.2e}", flush=True)
    wall = time.time() - t0

    # MEASURE (the verdict) — separate eval generators so each split is sampled fresh
    eg = torch.Generator().manual_seed(a.seed + 1000)
    train_ce = eval_ce_segs(model, stream, train_segs, tw, a.seq_len, a.batch_size, device, eg, iters=40)
    contig_val_ce = eval_ce_segs(model, stream, contig_segs, cw, a.seq_len, a.batch_size, device, eg, iters=40)
    rand_val_ce = eval_ce_segs(model, stream, rand_segs, rw, a.seq_len, a.batch_size, device, eg, iters=40)

    # shuffle baseline: byte-shuffled stream (destroys all structure), eval on a
    # held-out-position window set. uniform = ln(256).
    uniform_ce = float(torch.log(torch.tensor(256.0)))
    perm = torch.randperm(nbytes, generator=torch.Generator().manual_seed(7))
    shuf_stream = stream[perm]
    shuf_segs = [(0, nbytes)]
    sw = _seg_weights(shuf_segs, a.seq_len)
    shuffle_ce = eval_ce_segs(model, shuf_stream, shuf_segs, sw, a.seq_len, a.batch_size, device, eg, iters=40)

    gap_contig = contig_val_ce - train_ce
    gap_rand = rand_val_ce - train_ce
    val_ce = max(contig_val_ce, rand_val_ce)   # worst-case held-out
    gap = val_ce - train_ce

    # GENERALIZES if held-out CE stays close to train CE AND well below baselines.
    # Threshold: val within 2x of train (relative gap) AND val far below uniform.
    rel = gap / max(train_ce, 1e-9)
    generalizes = (val_ce < 0.5 * uniform_ce) and (rel <= 1.0) and (val_ce < shuffle_ce)
    verdict = 1 if generalizes else 0

    print(f"TRAIN_CE {train_ce:.5f}", flush=True)
    print(f"VAL_CE_CONTIG {contig_val_ce:.5f}  GAP_CONTIG {gap_contig:+.5f}", flush=True)
    print(f"VAL_CE_RAND {rand_val_ce:.5f}  GAP_RAND {gap_rand:+.5f}", flush=True)
    print(f"VAL_CE(worst) {val_ce:.5f}  GAP {gap:+.5f}  REL_GAP {rel:.4f}", flush=True)
    print(f"BASELINE uniform_ce={uniform_ce:.5f} shuffle_ce={shuffle_ce:.5f}", flush=True)
    print(f"F-CLM-LANEP-GEN {verdict}  ({'GENERALIZES' if verdict else 'MEMORIZATION'})", flush=True)

    if a.ckpt_out:
        sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
        torch.save(sd, a.ckpt_out)
        print(f"CKPT saved {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)
        if a.clm_out:
            p = S.serialize_v2(sd, cfg, a.clm_out)
            print(f"CLM serialized {p} ({os.path.getsize(p)} bytes)", flush=True)

    result = {
        "substrate": "GPU-torch", "test": "train_val_split_generalization",
        "device": torch.cuda.get_device_name(0), "compute_cap": f"{cap[0]}.{cap[1]}",
        "torch": torch.__version__,
        "d_model": a.d_model, "n_experts": cfg.n_experts,
        "n_trunk_layers": cfg.n_trunk_layers, "kernel_size": cfg.kernel_size,
        "vocab": cfg.vocab_size, "n_params": n_params,
        "steps": a.steps, "seq_len": a.seq_len, "batch_size": a.batch_size,
        "lr": a.lr, "bf16": use_bf16, "wall_s": round(wall, 2),
        "corpus": a.corpus, "corpus_bytes": nbytes, "corpus_sha256": sha,
        "val_frac": a.val_frac,
        "train_bytes": train_bytes, "contig_val_bytes": contig_bytes,
        "rand_val_bytes": rand_bytes,
        "first_ce": round(first_ce, 5),
        "train_ce": round(train_ce, 5),
        "val_ce_contig": round(contig_val_ce, 5),
        "val_ce_rand": round(rand_val_ce, 5),
        "val_ce_worst": round(val_ce, 5),
        "gap_contig": round(gap_contig, 5),
        "gap_rand": round(gap_rand, 5),
        "gap": round(gap, 5), "rel_gap": round(rel, 5),
        "uniform_ce": round(uniform_ce, 5),
        "shuffle_ce": round(shuffle_ce, 5),
        "F_CLM_LANEP_GEN": verdict,
        "verdict_str": "GENERALIZES" if verdict else "MEMORIZATION",
        "descent": descent,
    }
    if a.json_out:
        with open(a.json_out, "w") as f:
            json.dump(result, f, indent=2)
    print("RESULT " + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
