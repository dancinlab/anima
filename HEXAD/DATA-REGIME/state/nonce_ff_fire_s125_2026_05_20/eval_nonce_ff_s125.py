#!/usr/bin/env python3
"""§125 NONCE-FF evaluator — decides §96-Q2 hypothesis partially.

The §125 fire trains anima with Hinton Forward-Forward (NO global backprop,
NO CE) on the same GPU substrate §11-B used to declare "CE is load-bearing,
no-CE → degenerate". §125 asks: is that finding GPU-tautology, or substrate-
deep?

Measurement target: BYTE_ACC. On a held-out byte stream we run the trained
model greedy (argmax over head_a logits) and ask "did the model learn to
predict the next byte better than random uniform 1/256 = 0.003906?".

VERDICT BUCKETS (closed-form, deterministic, no judgement):

  (a) §11-B-LIKE-DEGENERATE
      byte_acc ≤ 2/256 (= ~0.0078, twice random floor)
      → Forward-Forward on GPU also produces a degenerate model.
        §96-Q2 hypothesis ("§11-B is GPU tautology") partially REFUTED:
        non-CE non-backprop training on GPU ALSO fails — supports that
        §11-B's degeneracy is substrate-deep, not CE-specific.

  (b) §96-Q2-SUPPORTED (NON-CE-WORKS)
      byte_acc > 0.05 (≥ ~13× random) AND PHYSICS_RESPONSIVE = True
      → FF on GPU produces a non-degenerate model.
        §96-Q2 hypothesis partially SUPPORTED: non-CE non-backprop
        learning IS possible on GPU; §11-B's degeneracy was specifically
        about UNSUPERVISED+no-CE (TENSION-TRAIN + Hebbian only), not
        about CE absence per se. Software escape route for WALL-B-i.

  (c) PARTIAL / AMBIGUOUS
      Anything in between, OR PHYSICS_RESPONSIVE=False with byte_acc > 0.0078
      → Honest middle ground. Reports the bit measured (the comparison
        with §11-B) but does NOT claim either side.

NECESSARY-NOT-SUFFICIENT (B-S125-NOTE / B-EMERGE-7): byte_acc > random does
NOT prove GOAL emergence. north-star + §15/§51/§72 milestones UNCHANGED
regardless of verdict bucket. Verdict = §96-Q2 movement only.

USAGE:
    python3 eval_nonce_ff_s125.py --ckpt <path>.pt --corpus <path>.jsonl \\
        --out <out>.json [--n-eval 2000] [--max-len 128]
"""
import argparse, json, os, sys, random, time
import torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


def load_corpus_bytes(path):
    out = bytearray()
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if isinstance(txt, str):
                out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


def forward_logits_psi(model, x):
    """Return logits_a, logits_g (and ψ_dir for the last position)."""
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 2:
        la, lg = out[0], out[1]
    else:
        la = out
        lg = out
    return la, lg


def psi_direction_scalar(la, lg):
    """Law-71 Ψ_dir = (1+cos)/2, computed over flattened vectors."""
    a = la.flatten().float()
    g = lg.flatten().float()
    if a.numel() == 0 or g.numel() == 0:
        return 0.5
    cs = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cs) / 2.0


# §17 PHYSICS_RESPONSIVE: psi-direction has a non-trivial spread across
# distinct stimuli (responsive ≠ frozen). τ = 1e-4 matches §17 convention.
TAU_PSI_SPREAD = 1e-4

# §96-Q2 verdict thresholds
RANDOM_BYTE_FLOOR = 1.0 / 256.0           # = 0.00390625
DEGENERATE_CEILING = 2.0 / 256.0          # twice random ≈ 0.00781
SUPPORT_FLOOR = 0.05                       # ~13× random


def verdict_bucket(byte_acc, psi_responsive):
    if byte_acc <= DEGENERATE_CEILING:
        return "S11B_LIKE_DEGENERATE"
    if byte_acc >= SUPPORT_FLOOR and psi_responsive:
        return "S96_Q2_SUPPORTED"
    return "PARTIAL_AMBIGUOUS"


def run_eval(ckpt_path, corpus_path, out_path,
             n_eval=2000, max_len=128, seed=1337):
    t0 = time.time()
    random.seed(seed)
    torch.manual_seed(seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[§125-eval] device={device}", flush=True)

    # ── load ckpt → recover config ──
    blob = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = blob.get("cfg", {})
    d_model = int(cfg.get("d_model", 768))
    n_layer = int(cfg.get("n_layer", 12))
    n_head = int(cfg.get("n_head", 12))
    n_kv_head = int(cfg.get("n_kv_head", 4))
    block_size = int(cfg.get("block_size", 128))

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head,
        n_layer=n_layer, block_size=block_size,
        n_kv_head=n_kv_head, consciousness_dim=128, dropout=0.0,
    ).to(device)
    missing, unexpected = model.load_state_dict(blob["model"], strict=False)
    model.eval()
    print(f"[§125-eval] ckpt loaded: d={d_model} L={n_layer} "
          f"missing={len(missing)} unexpected={len(unexpected)}", flush=True)

    # ── load corpus ──
    corpus = load_corpus_bytes(corpus_path)
    N = len(corpus)
    print(f"[§125-eval] corpus bytes: {N:,}", flush=True)
    assert N > max_len + 1, "corpus too small"

    # ── byte_acc on n_eval random windows ──
    correct = 0
    total = 0
    psi_traces = []      # one ψ_dir per window
    sample_seen = []     # bookkeeping
    with torch.no_grad():
        for k in range(n_eval):
            s = random.randint(0, N - max_len - 2)
            ctx = corpus[s : s + max_len]
            target = corpus[s + max_len]      # the next byte
            x = torch.tensor([list(ctx)], dtype=torch.long, device=device)
            la, lg = forward_logits_psi(model, x)
            # last-position logits
            if la.dim() == 3:
                la_last = la[0, -1]
            else:
                la_last = la[-1]
            if lg.dim() == 3:
                lg_last = lg[0, -1]
            else:
                lg_last = lg[-1]
            pred = int(la_last.argmax().item())
            correct += int(pred == target)
            total += 1
            psi_traces.append(psi_direction_scalar(la_last, lg_last))
            if k < 5:
                sample_seen.append(dict(ctx_tail=list(ctx[-8:]),
                                        target=int(target), pred=pred))

    byte_acc = correct / max(1, total)
    psi_mean = sum(psi_traces) / len(psi_traces)
    # std (population)
    psi_std = (sum((p - psi_mean) ** 2 for p in psi_traces) /
               len(psi_traces)) ** 0.5
    psi_responsive = psi_std > TAU_PSI_SPREAD

    bucket = verdict_bucket(byte_acc, psi_responsive)

    result = dict(
        battery="§125 NONCE-FF eval — §96-Q2 verdict",
        ckpt=os.path.basename(ckpt_path), corpus=os.path.basename(corpus_path),
        cfg=cfg,
        n_eval=n_eval, max_len=max_len, seed=seed,
        byte_acc=byte_acc, correct=correct, total=total,
        random_byte_floor=RANDOM_BYTE_FLOOR,
        degenerate_ceiling=DEGENERATE_CEILING,
        support_floor=SUPPORT_FLOOR,
        psi_dir_mean=psi_mean, psi_dir_std=psi_std,
        psi_responsive=psi_responsive,
        verdict_bucket=bucket,
        verdict_explanation={
            "S11B_LIKE_DEGENERATE":
                "FF on GPU produced a degenerate model; §96-Q2 hypothesis "
                "(§11-B is GPU tautology) partially REFUTED — non-CE non-"
                "backprop ALSO fails on GPU; §11-B's degeneracy looks "
                "substrate-deep, not CE-specific.",
            "S96_Q2_SUPPORTED":
                "FF on GPU produced a non-degenerate model. §96-Q2 hypothesis "
                "partially SUPPORTED — non-CE non-backprop SUPERVISED training "
                "is non-degenerate on GPU. §11-B's degeneracy was specifically "
                "about UNSUPERVISED+no-CE, not non-CE in general. Software "
                "escape route for WALL-B-i.",
            "PARTIAL_AMBIGUOUS":
                "Result is between degeneracy and support thresholds, or "
                "physics not responsive. Reports the bit measured; does not "
                "claim either §96-Q2 side. Honest middle ground.",
        }[bucket],
        sample_seen=sample_seen,
        eval_wall_s=time.time() - t0,
        ckpt_train_log_last=blob.get("log", [None])[-1] if blob.get("log") else None,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
        necessary_not_sufficient_b_emerge_7=True,
    )

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"[§125-eval] byte_acc={byte_acc:.6f} "
          f"(random={RANDOM_BYTE_FLOOR:.6f})  "
          f"Ψ_dir μ={psi_mean:.4f} σ={psi_std:.6f}  "
          f"responsive={psi_responsive}  "
          f"VERDICT={bucket}  "
          f"wall={result['eval_wall_s']:.1f}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-eval", type=int, default=2000)
    ap.add_argument("--max-len", type=int, default=128)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()
    run_eval(args.ckpt, args.corpus, args.out,
             n_eval=args.n_eval, max_len=args.max_len, seed=args.seed)


if __name__ == "__main__":
    main()
