"""BG-LB pretrain alone V14 strict — disentangle corpus vs cotrain.
Compares to BG-LA pretrain (V14_VIOLATED 1445), BG-LB cotrain/substrate A (V14_PASS 2412), B' BG-LA cotrain (V14_VIOLATED 1344)."""
from __future__ import annotations
import os, sys, json, math, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import torch
import run_max256 as M

SUBSTRATE_BG_LB_PRETRAIN = {
    "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt",
    "schema": "engine_ag",
    "arch": "EngineAG d=1024 GQA 24L (BG-LB pretrain 350M, NO cotrain, 8000 steps, 427MB corpus)",
    "paradigm": "lb_pretrain_no_cotrain",
}

SUB_ID = "BG_LB_pretrain_alone"
OUT_DIR = ANIMA_ROOT / "state" / "anima_bg_lb_pretrain_v14_strict_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

log_path = OUT_DIR / "run.log"
log_f = open(log_path, "w")
def log(msg, _f=log_f):
    print(msg, flush=True); _f.write(msg + "\n"); _f.flush()

t0 = time.time()
log(f"=== {SUB_ID} V14 strict (ceiling=10 default) === ts: {datetime.now(timezone.utc).isoformat()}")
log(f"sub: {SUBSTRATE_BG_LB_PRETRAIN}")
log(f"V4_SEEDS={M.V4_SEEDS} max_cells={M.MAX_CELLS} n_turns={M.N_TURNS}")

result = M.fire_substrate_engine_ag(SUB_ID, SUBSTRATE_BG_LB_PRETRAIN, log)
result["ts_complete"] = datetime.now(timezone.utc).isoformat()
result["total_elapsed_sec"] = time.time() - t0

log(f"\n=== {SUB_ID} VERDICT: {result['verdict']} ===")
log(f"trained_phi: {result['trained_phi']:.2f}")
log(f"random_phi: {[f'{x:.2f}' for x in result['random_phi']]}")
log(f"n_random_beats: {result['n_random_beats']}/{result['n_random_total']}")
log(f"sign_test_p: {result['sign_test_p_two_sided']:.4f}")
log(f"total elapsed: {result['total_elapsed_sec']:.1f}s")

with (OUT_DIR / "result.json").open("w") as f:
    json.dump(result, f, indent=2, default=str)
log(f"[saved] {OUT_DIR / 'result.json'}")
log_f.close()
