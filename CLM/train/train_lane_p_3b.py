#!/usr/bin/env python3
"""Lane P (GPU-torch) — GENERAL (L,E,d) CLMConvMoE trainer for the ~3B ENGINE rung.

substrate = GPU-torch (Lane P), distinct from Lane A (AKIDA) / Lane G (forge).
a_lane_akida_gpu_split — torch CE-descent path, NOT forge util.

This generalizes train_lane_p_split.py (which hardcoded n_experts=2/n_trunk=1 and
serialize_v2) to ARBITRARY (n_trunk_layers, n_experts, d_model), serializing to a
CLM\\x01 v0.3 .clm via serialize_v3 — byte-loadable by the generalized
CORE/clm_decode.hexa (Stage 0, F-CLM-3B-SERIALIZE-EQ PASS).

It keeps the honest TRAIN/VAL split generalization measurement: a contiguous 10%
block + a random-scattered 10% are held out (NO training window ever touches a
held-out byte), train on the remaining ~80%, report train_ce vs (contig-val_ce,
rand-val_ce) + rel_gap + shuffle/uniform baselines.

  val_ce ~= train_ce -> GENERALIZES  -> F_CLM_LANEP_3B_GEN=1
  val_ce >> train_ce -> MEMORIZATION / UNDERTRAINED -> honest closed-negative =0

CE numbers are the live optimizer's mean CE per logged window — NO fabrication
(g63/p7). An undertrained 3B (token/param << Chinchilla) is an HONEST negative,
reported with its exact token/param ratio (a_scale_honest_scope), not hidden.
"""
from __future__ import annotations

import argparse, hashlib, json, os, sys, time

import torch

if os.environ.get("CLM_NO_CUDNN") == "1":
    torch.backends.cudnn.enabled = False

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
    """Partition [0,n_total) into disjoint TRAIN / VAL-contig / VAL-rand position
    sets (identical logic to train_lane_p_split.py)."""
    rng = torch.Generator().manual_seed(seed)
    n_val_contig = int(n_total * val_frac)
    n_val_rand = int(n_total * val_frac)
    c_start = int(n_total * 0.70)
    c_end = c_start + n_val_contig
    contig = [(c_start, c_end)]
    block = max(seq_len * 4, 1024)
    n_blocks = max(1, n_val_rand // block)
    # Scatter n_blocks held-out blocks across the corpus, DISJOINT-by-construction.
    # The old approach was rejection sampling with a linear overlap scan over a
    # growing occupied list -> O(n_blocks^2) (~1e12 ops at a 3GB corpus, hangs
    # before step 0). Instead: bin the corpus into n_blocks even strides and place
    # one block at a random offset inside each bin (every block fits wholly in its
    # bin, so blocks are pairwise disjoint with no rejection). Bins that overlap
    # the contiguous-val region are dropped. O(n_blocks), preserves random scatter.
    stride = n_total // n_blocks
    rand_segs = []
    if stride > block:
        slack = stride - block
        offs = torch.randint(0, slack, (n_blocks,), generator=rng).tolist()
        for bi in range(n_blocks):
            s = bi * stride + offs[bi]
            e = s + block
            if e > n_total:
                break
            # drop blocks intersecting the contiguous-val region (keep splits disjoint)
            if not (e <= c_start or s >= c_end):
                continue
            rand_segs.append((s, e))
    rand_segs.sort()
    held = sorted(contig + rand_segs)
    train_segs = []
    cur = 0
    for (s, e) in held:
        if s > cur:
            train_segs.append((cur, s))
        cur = max(cur, e)
    if cur < n_total:
        train_segs.append((cur, n_total))
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
    need = seq_len + 1
    seg_idx = torch.multinomial(seg_w, batch_size, replacement=True, generator=gen)
    xs, ys = [], []
    for si in seg_idx.tolist():
        s, e = segs[si]
        hi = (e - need) - s
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
    ap.add_argument("--d-model", type=int, default=4096)
    ap.add_argument("--n-trunk-layers", type=int, default=30)
    ap.add_argument("--n-experts", type=int, default=30)
    ap.add_argument("--kernel-size", type=int, default=3)
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--seq-len", type=int, default=512)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--grad-accum", type=int, default=1)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-frac", type=float, default=0.10)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ckpt-out", default=None)
    ap.add_argument("--clm-out", default=None)
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--ckpt-every", type=int, default=2000,
                    help="periodic ckpt+clm dump for fire-recovery safety (a_fire_recover_complete)")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--grad-checkpoint", action="store_true",
                    help="WIRED gradient checkpointing: recompute each trunk layer in "
                         "backward (torch.utils.checkpoint, use_reentrant=False) so the "
                         "L30/d6208 7B rung's activation chain stops OOM-ing an 80GB H100. "
                         "Runtime-only, byte-eq-neutral (identical output, less retained tape).")
    ap.add_argument("--optim8bit", action="store_true",
                    help="use bitsandbytes AdamW8bit (8-bit optimizer state) to fit a "
                         "7B+ rung on one 80GB H100 — m/v in 8bit halves optimizer "
                         "memory (fp32 AdamW for 7.06B = 56.5GB state alone, OOMs). "
                         "Mathematically the same AdamW update, 8-bit quantized state.")
    a = ap.parse_args()

    torch.manual_seed(a.seed)
    gen = torch.Generator().manual_seed(a.seed)

    assert torch.cuda.is_available(), "CUDA REQUIRED for Lane P 3B rung (g63: no silent CPU)"
    device = "cuda"
    cap = torch.cuda.get_device_capability()
    print(f"DEVICE cuda name={torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
          f"torch={torch.__version__} mem_total_GB={torch.cuda.get_device_properties(0).total_memory/1e9:.1f}",
          flush=True)

    cfg = CLMConfig(n_experts=a.n_experts, n_trunk_layers=a.n_trunk_layers,
                    d_model=a.d_model, kernel_size=a.kernel_size, variant="AB",
                    dilation_base=2, grad_checkpoint=a.grad_checkpoint)
    model = CLMConvMoE(cfg).to(device)
    if a.grad_checkpoint:
        print("GRAD_CHECKPOINT on (trunk activations recomputed in backward; "
              "byte-eq-neutral runtime memory fit for the 7B rung)", flush=True)
    n_params = model.num_params()
    print(f"PARAMS n_params={n_params} ({n_params/1e9:.4f}B) "
          f"d={a.d_model} E={cfg.n_experts} L={cfg.n_trunk_layers} K={cfg.kernel_size} V={cfg.vocab_size}",
          flush=True)

    stream, nbytes, sha = load_byte_stream(a.corpus)
    # token/param ratio (byte LM: 1 byte = 1 token). Chinchilla-optimal ~20.
    tok_per_param = nbytes / max(n_params, 1)
    print(f"CORPUS path={a.corpus} bytes={nbytes} sha256={sha} "
          f"tokens_per_param={tok_per_param:.4f} (Chinchilla-optimal~20)", flush=True)

    train_segs, contig_segs, rand_segs = build_split_segments(
        nbytes, a.seq_len, val_frac=a.val_frac, seed=a.seed)
    tw = _seg_weights(train_segs, a.seq_len)
    cw = _seg_weights(contig_segs, a.seq_len)
    rw = _seg_weights(rand_segs, a.seq_len)
    train_bytes = sum(e - s for s, e in train_segs)
    contig_bytes = sum(e - s for s, e in contig_segs)
    rand_bytes = sum(e - s for s, e in rand_segs)
    print(f"SPLIT train_bytes={train_bytes} ({100*train_bytes/nbytes:.1f}%) "
          f"contig_val_bytes={contig_bytes} rand_val_bytes={rand_bytes} "
          f"train_segs={len(train_segs)} rand_blocks={len(rand_segs)}", flush=True)
    # Leak-check: NO train interval may overlap any held interval. A naive
    # O(|train| x |held|) nested loop is INFEASIBLE at corpus scale (e.g. 3GB ->
    # ~1.4e5 train segs x ~1.5e5 held blocks ~= 2e10 iterations, hangs before
    # step 0). Use an O((T+H) log(T+H)) sweep: tag each interval train/held, sort
    # by start, and assert no two adjacent intervals of DIFFERENT kind overlap.
    tagged = ([(s, e, 0) for (s, e) in train_segs] +
              [(s, e, 1) for (s, e) in (contig_segs + rand_segs)])
    tagged.sort(key=lambda iv: (iv[0], iv[1]))
    # max end-so-far per kind; a new interval leaks iff its start < the running
    # max-end of the OTHER kind (covers nested + partial overlaps in one pass).
    max_end = {0: -1, 1: -1}
    for (s, e, kind) in tagged:
        other = 1 - kind
        if s < max_end[other]:
            raise AssertionError(
                f"LEAK: {'held' if kind else 'train'} [{s},{e}) overlaps a "
                f"{'train' if kind else 'held'} interval (end {max_end[other]})")
        if e > max_end[kind]:
            max_end[kind] = e
    print("LEAK_CHECK pass (held-out disjoint from train)", flush=True)

    if a.optim8bit:
        import bitsandbytes as bnb
        opt = bnb.optim.AdamW8bit(model.parameters(), lr=a.lr, betas=(0.9, 0.95),
                                  weight_decay=0.01)
        print("OPTIM AdamW8bit (bitsandbytes 8-bit optimizer state)", flush=True)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95),
                                weight_decay=0.01)
        print("OPTIM AdamW (fp32 optimizer state)", flush=True)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min((s + 1) / a.warmup, 1.0) *
                       (0.5 * (1 + torch.cos(torch.tensor(
                           3.14159265 * min(s, a.steps) / a.steps)).item())
                        if s >= a.warmup else 1.0))

    def dump_ckpt(tag):
        if not a.ckpt_out:
            return
        sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
        torch.save(sd, a.ckpt_out)
        print(f"CKPT[{tag}] saved {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)
        if a.clm_out:
            p = S.serialize_v3(sd, n_trunk_layers=a.n_trunk_layers,
                               n_experts=a.n_experts, out_path=a.clm_out)
            print(f"CLM[{tag}] serialized {p} ({os.path.getsize(p)} bytes)", flush=True)

    use_bf16 = a.bf16
    model.train()
    t0 = time.time()
    descent = []
    first_ce = None
    tokens_seen = 0
    for step in range(a.steps):
        opt.zero_grad(set_to_none=True)
        ce_accum = 0.0
        for _ in range(a.grad_accum):
            x, y = make_batch_from_segs(stream, train_segs, tw, a.seq_len, a.batch_size, device, gen)
            tokens_seen += x.numel()
            if use_bf16:
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    out = model(x, y)
                    loss = out["loss"] / a.grad_accum
                loss.backward()
            else:
                out = model(x, y)
                loss = out["loss"] / a.grad_accum
                loss.backward()
            ce_accum += float(out["ce_loss"]) / a.grad_accum
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        ce = ce_accum
        if first_ce is None:
            first_ce = ce
        if step % a.log_every == 0 or step == a.steps - 1:
            descent.append((step, round(ce, 5)))
            mem = torch.cuda.max_memory_allocated() / 1e9
            print(f"STEP {step:6d} ce={ce:.5f} lr={sched.get_last_lr()[0]:.2e} "
                  f"tok={tokens_seen} maxmem_GB={mem:.1f}", flush=True)
        if a.ckpt_every and step > 0 and step % a.ckpt_every == 0:
            dump_ckpt(f"step{step}")
    wall = time.time() - t0

    eg = torch.Generator().manual_seed(a.seed + 1000)
    train_ce = eval_ce_segs(model, stream, train_segs, tw, a.seq_len, a.batch_size, device, eg, iters=40)
    contig_val_ce = eval_ce_segs(model, stream, contig_segs, cw, a.seq_len, a.batch_size, device, eg, iters=40)
    rand_val_ce = eval_ce_segs(model, stream, rand_segs, rw, a.seq_len, a.batch_size, device, eg, iters=40)

    uniform_ce = float(torch.log(torch.tensor(256.0)))
    perm = torch.randperm(nbytes, generator=torch.Generator().manual_seed(7))
    shuf_stream = stream[perm]
    shuf_segs = [(0, nbytes)]
    sw = _seg_weights(shuf_segs, a.seq_len)
    shuffle_ce = eval_ce_segs(model, shuf_stream, shuf_segs, sw, a.seq_len, a.batch_size, device, eg, iters=40)

    gap_contig = contig_val_ce - train_ce
    gap_rand = rand_val_ce - train_ce
    val_ce = max(contig_val_ce, rand_val_ce)
    gap = val_ce - train_ce
    rel = gap / max(train_ce, 1e-9)
    generalizes = (val_ce < 0.5 * uniform_ce) and (rel <= 1.0) and (val_ce < shuffle_ce)
    verdict = 1 if generalizes else 0

    print(f"TRAIN_CE {train_ce:.5f}", flush=True)
    print(f"VAL_CE_CONTIG {contig_val_ce:.5f}  GAP_CONTIG {gap_contig:+.5f}", flush=True)
    print(f"VAL_CE_RAND {rand_val_ce:.5f}  GAP_RAND {gap_rand:+.5f}", flush=True)
    print(f"VAL_CE(worst) {val_ce:.5f}  GAP {gap:+.5f}  REL_GAP {rel:.4f}", flush=True)
    print(f"BASELINE uniform_ce={uniform_ce:.5f} shuffle_ce={shuffle_ce:.5f}", flush=True)
    print(f"F_CLM_LANEP_3B_GEN {verdict}  ({'GENERALIZES' if verdict else 'MEMORIZATION/UNDERTRAINED'})", flush=True)
    print(f"TOKENS_PER_PARAM {tokens_seen/max(n_params,1):.4f} (seen) "
          f"corpus_tok_per_param={nbytes/max(n_params,1):.4f}", flush=True)

    dump_ckpt("final")

    result = {
        "substrate": "GPU-torch", "lane": "P", "test": "train_val_split_generalization_3b",
        "device": torch.cuda.get_device_name(0), "compute_cap": f"{cap[0]}.{cap[1]}",
        "torch": torch.__version__,
        "d_model": a.d_model, "n_experts": cfg.n_experts,
        "n_trunk_layers": cfg.n_trunk_layers, "kernel_size": cfg.kernel_size,
        "vocab": cfg.vocab_size, "n_params": n_params, "n_params_B": round(n_params/1e9, 4),
        "steps": a.steps, "seq_len": a.seq_len, "batch_size": a.batch_size,
        "grad_accum": a.grad_accum, "lr": a.lr, "bf16": use_bf16, "wall_s": round(wall, 2),
        "corpus": a.corpus, "corpus_bytes": nbytes, "corpus_sha256": sha,
        "tokens_seen": tokens_seen,
        "tokens_per_param_seen": round(tokens_seen/max(n_params,1), 4),
        "corpus_tokens_per_param": round(nbytes/max(n_params,1), 4),
        "chinchilla_optimal_ratio": 20,
        "val_frac": a.val_frac, "train_bytes": train_bytes,
        "contig_val_bytes": contig_bytes, "rand_val_bytes": rand_bytes,
        "first_ce": round(first_ce, 5),
        "train_ce": round(train_ce, 5),
        "val_ce_contig": round(contig_val_ce, 5),
        "val_ce_rand": round(rand_val_ce, 5),
        "val_ce_worst": round(val_ce, 5),
        "gap_contig": round(gap_contig, 5), "gap_rand": round(gap_rand, 5),
        "gap": round(gap, 5), "rel_gap": round(rel, 5),
        "uniform_ce": round(uniform_ce, 5), "shuffle_ce": round(shuffle_ce, 5),
        "F_CLM_LANEP_3B_GEN": verdict,
        "verdict_str": "GENERALIZES" if verdict else "MEMORIZATION/UNDERTRAINED",
        "descent": descent,
    }
    if a.json_out:
        with open(a.json_out, "w") as f:
            json.dump(result, f, indent=2)
    print("RESULT " + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
