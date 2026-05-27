#!/usr/bin/env python3
"""§107 trainer — Dir-I lever (§16 byte-equal carry) on §102's CORPUS_S101.

This is `train_carving_s16.py` invoked with §107-specific arguments. The
trainer source is BYTE-IDENTICAL to §16 (G5 single-variable preserve per
§101). The corpus is §102's BUILT CORPUS_S101 (sha256
`39d581da209615468c1c41e07aa8662ef1074bc5be49a666f8f861753dd5810e`,
777,845 records, 603MB, §104-refined I4' = TRUE byte-identical).

5 levers preserved (§101 G5 single-variable):
- §16 routing CARVING corpus  → baseline (Dir-I trainer carries)
- §59-FIRE W-native PTD       → side READ-OUT only, NOT objective (G5 carry)
- §75-FIRE state-derived ctrl → A4 emit-length-indep probe (eval-side)
- §88-F2 neoteny              → AVAILABLE-flag-NOT-ENABLED this cycle (G5)
- §92 L_ap                    → AVAILABLE-flag-NOT-ENABLED this cycle (G5)

corpus is sole variable; trainer is Dir-I/§16 lever exactly.

USAGE:
    python3 train_s107.py --corpus corpus_s101.jsonl --out-dir out_main \\
        --steps 6000 --seed 1337

Internally just imports and reuses `train_carving_s16.py:run` (the canonical
§16 trainer entry point). NOTE: the §16 trainer exposes a single generic
`run(cfg)` — there is no `train_main`/`train_sanity` symbol. The original
§107 dispatch (2026-05-19) crashed at this import in ~2s (ImportError); the
§107-salvage fixed the call to `run(cfg)`. §107-RETRY attempt-4 then crashed
at step 1 (`KeyError: 'log_every'` — the cfg below was missing a key run()
hard-reads). Fix: the cfg dicts are now built BYTE-IDENTICAL to §16's own
`__main__` cfg builder (`train_carving_s16.py:471-491`) — same keys, same
values — so the G5 single-variable "trainer is §16 lever exactly" mandate
holds at the cfg level, not just the source level.
"""
import os, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_carving_s16 import run as _s16_run


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=6000)
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
    ap.add_argument("--no-curriculum", action="store_true",
                    help="overlay-OFF connection point: curriculum-OFF == "
                         "Dir-I shuffled sampling byte-equal (B-S16-6)")
    args = ap.parse_args()

    # cfg dicts mirror train_carving_s16.py:471-491 byte-identically
    # (same keys, same values) — G5 single-variable: trainer == §16 lever.
    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route,
                   curriculum=not args.no_curriculum,
                   blend_frac=args.blend_frac)
        _s16_run(cfg)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route,
                   curriculum=not args.no_curriculum,
                   blend_frac=args.blend_frac)
        _s16_run(cfg)  # §16 sanity cfg (fixed d=32·3L) verbatim


if __name__ == "__main__":
    main()
