"""Substrate C and E full n=5 V14 strict — re-measure."""
from __future__ import annotations
import os, sys, json, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import torch
import run_max256 as M

# Fire C then E sequentially
TARGETS = ["C_cells64_aware", "E_convo5k_ft"]
OUT_DIR = ANIMA_ROOT / "state" / "anima_substrate_ce_full_v14_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

for sub_id in TARGETS:
    sub = M.SUBSTRATES[sub_id]
    log_path = OUT_DIR / f"run_{sub_id}.log"
    log_f = open(log_path, "w")
    def log(msg, _f=log_f):
        print(msg, flush=True); _f.write(msg + "\n"); _f.flush()
    t0 = time.time()
    log(f"=== {sub_id} n=5 full V14 strict === ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"V4_SEEDS={M.V4_SEEDS} max_cells={M.MAX_CELLS} n_turns={M.N_TURNS}")
    try:
        result = M.fire_substrate_v2_d384(sub_id, sub, log)
        result["ts_complete"] = datetime.now(timezone.utc).isoformat()
        result["total_elapsed_sec"] = time.time() - t0
        log(f"\n=== {sub_id} VERDICT: {result['verdict']} ===")
        log(f"trained_phi: {result.get('trained_phi', 'N/A')}")
        log(f"random_phi: {result.get('random_phi', 'N/A')}")
        log(f"n_random_beats: {result.get('n_random_beats', result.get('n_random_beats_phi', 'N/A'))}")
        log(f"sign_test_p: {result.get('sign_test_p_two_sided', 'N/A')}")
        log(f"total elapsed: {result['total_elapsed_sec']:.1f}s")
        with (OUT_DIR / f"result_{sub_id}.json").open("w") as f:
            json.dump(result, f, indent=2, default=str)
        log(f"[saved] {OUT_DIR / f'result_{sub_id}.json'}")
    except Exception as e:
        import traceback
        log(f"FAILED: {e}\n{traceback.format_exc()}")
    log_f.close()
