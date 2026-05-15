"""BG-V14-MAX256-B-NO-COTRAIN — substrate B × max=256 × 5-seed strict.

Cleanest disambiguation of §47 cotrain-exercise hypothesis: same EngineAG arch,
same Phase-1-only pretrain path (NO chat-cotrain), max=256 cap-free.

Reuses §51 BG-V14-MAX256-CAP-FREE-MULTI runner machinery; only swaps substrate
to B (BG-LA pretrain ckpt).

raw#9 / raw#15 / / / / honored.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
THIS_DIR = ANIMA_ROOT / "state" / "anima_v14_max256_b_no_cotrain_2026_05_10"
THIS_DIR.mkdir(parents=True, exist_ok=True)
SIBLING_RUNNER = ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"

# import sibling runner (raw#15 additive — NOT modified)
sys.path.insert(0, str(SIBLING_RUNNER))
import run_max256 as M  # noqa: E402

V4_SEEDS = [42, 137, 271, 314, 1729]
TRAINED_PROMPT_SEED = 42
MAX_CELLS = 256
N_TURNS = 200
SNAP_EVERY = 25

SUBSTRATE_B = {
    "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt",
    "schema": "engine_ag",
    "arch": "EngineAG d=1024 GQA 24L (BG-LA pretrain 350M, NO cotrain)",
    "paradigm": "naive_pretrain_no_cotrain",
}

SUB_ID = "B_bgla_pretrain_no_cotrain"


def main():
    M.V4_SEEDS = V4_SEEDS
    M.TRAINED_PROMPT_SEED = TRAINED_PROMPT_SEED
    M.MAX_CELLS = MAX_CELLS
    M.N_TURNS = N_TURNS
    M.SNAP_EVERY = SNAP_EVERY

    log_path = THIS_DIR / "run_b.log"
    log_f = open(log_path, "w")

    def log(msg, _f=log_f):
        print(msg, flush=True)
        _f.write(msg + "\n")
        _f.flush()

    t_start = time.time()
    log(f"=== BG-V14-MAX256-B-NO-COTRAIN === ts: {datetime.now(timezone.utc).isoformat()}")
    log(f"sub_id: {SUB_ID}")
    log(f"sub: {SUBSTRATE_B}")
    log(f"V4_SEEDS={V4_SEEDS} max_cells={MAX_CELLS} n_turns={N_TURNS} snap_every={SNAP_EVERY}")

    result = M.fire_substrate_engine_ag(SUB_ID, SUBSTRATE_B, log)
    result["ts_complete"] = datetime.now(timezone.utc).isoformat()
    result["total_elapsed_sec"] = time.time() - t_start

    log(f"\n=== {SUB_ID} VERDICT: {result['verdict']} ===")
    log(f"trained_phi: {result['trained_phi']:.2f}")
    log(f"random_phi: {[f'{x:.2f}' for x in result['random_phi']]}")
    log(f"n_random_beats: {result['n_random_beats']}/{result['n_random_total']}")
    log(f"sign_test_p: {result['sign_test_p_two_sided']:.4f}")
    log(f"trained_first_cap_turn: {result['trained_first_cap_turn']}")
    log(f"random_first_cap_turn: {result['random_first_cap_turn']}")
    log(f"trained_cap_bound_turns: {result['trained_cap_bound_turns']}")
    log(f"random_cap_bound_turns: {result['random_cap_bound_turns']}")
    log(f"total elapsed: {result['total_elapsed_sec']:.1f}s")

    out = THIS_DIR / "result.json"
    with out.open("w") as f:
        json.dump(result, f, indent=2, default=str)
    log(f"[saved] {out}")
    log_f.close()


if __name__ == "__main__":
    main()
