"""V14 strict on FFN.gate cotrain output (B'') — §78 prediction direct test.
Compare against:
  BG-LA pretrain (B): trained_phi=1445 (V14_VIOLATED)
  B' P3 cotrain: trained_phi=1344 (V14_VIOLATED, regress)
  Substrate A (BG-LB cotrain): trained_phi=2412 (V14_PASS 5/5)
"""
from __future__ import annotations
import os, sys, json, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import run_max256 as M

SUBSTRATE = {
    "ckpt": str(ANIMA_ROOT / "state/anima_ffn_gate_cotrain_2026_05_11/ckpts/ckpt_final.pt"),
    "schema": "engine_ag",
    "arch": "EngineAG d=1024 GQA 24L (BG-LA + FFN.gate-only cotrain 6000 steps, §78 falsifiable test)",
    "paradigm": "ffn_gate_only_cotrain",
}

SUB_ID = "Bpp_ffn_gate_cotrain"
OUT_DIR = ANIMA_ROOT / "state" / "anima_ffn_gate_cotrain_2026_05_11"

log_path = OUT_DIR / "v14_strict_ceiling10.log"
log_f = open(log_path, "w")
def log(msg, _f=log_f):
    print(msg, flush=True); _f.write(msg + "\n"); _f.flush()

t0 = time.time()
log(f"=== {SUB_ID} V14 strict (ceiling=10) === ts: {datetime.now(timezone.utc).isoformat()}")
log(f"sub: {SUBSTRATE}")
log(f"V4_SEEDS={M.V4_SEEDS} max_cells={M.MAX_CELLS} n_turns={M.N_TURNS}")

result = M.fire_substrate_engine_ag(SUB_ID, SUBSTRATE, log)
result["ts_complete"] = datetime.now(timezone.utc).isoformat()
result["total_elapsed_sec"] = time.time() - t0

log(f"\n=== {SUB_ID} VERDICT: {result['verdict']} ===")
log(f"trained_phi: {result['trained_phi']:.2f}")
log(f"random_phi: {[f'{x:.2f}' for x in result['random_phi']]}")
log(f"n_random_beats: {result['n_random_beats']}/{result['n_random_total']}")
log(f"sign_test_p: {result['sign_test_p_two_sided']:.4f}")

with (OUT_DIR / "v14_strict_ceiling10_result.json").open("w") as f:
    json.dump(result, f, indent=2, default=str)
log(f"[saved] {OUT_DIR / 'v14_strict_ceiling10_result.json'}")
log_f.close()
