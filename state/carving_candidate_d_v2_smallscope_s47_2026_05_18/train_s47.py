#!/usr/bin/env python3
"""§47 trainer — §16 trainer BYTE-EQUIVALENT, only `--steps` smaller.

RESEARCH.md §47. The trainer is the §16 `train_carving_s16.py` (Dir-I
lever — Ψ-anchored CTL + tension-supervised routing + §12.1 Q1-c
curriculum) byte-equivalent. §47 simply imports it and invokes with
smaller --steps (default 3000 = 0.25× §16's 12000) for small-scope
per §47 task mandate.

NO trainer modification. Only step budget shrinks. All §16 connection-
point closures (B-S16-5 overlay-OFF / B-S16-6 curriculum-OFF) inherit.
"""
import os
import sys

_S16_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "carving_dataregime_s16_2026_05_18")
sys.path.insert(0, _S16_DIR)

# Import the §16 trainer module (byte-identical from disk).
# Then re-emit its argparse main with the §47 default `--steps 3000`.
import argparse
import corpus_carving_s16_generator  # noqa: F401 (s16 trainer imports it)
import train_carving_s16 as s16_trainer  # noqa: E402

# The §16 trainer's CLI uses default --steps 12000. §47 wants 3000.
# We re-parse args here and forward to s16_trainer.run() with cfg.
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000,
                    help="§47 default 3000 (§16/§34 use 12000) — "
                         "0.25× per §47 small-scope mandate")
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--blend-frac", type=float, default=0.15)
    ap.add_argument("--no-curriculum", action="store_true")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps,
                   warmup=max(20, args.steps // 20),
                   seed=args.seed,
                   log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route,
                   blend_frac=args.blend_frac,
                   curriculum=(not args.no_curriculum))
        s16_trainer.run(cfg)
    else:
        # No sanity branch exposed in §47.
        sys.exit("§47 trainer: --mode sanity not supported "
                 "(use s16 trainer directly for sanity)")
