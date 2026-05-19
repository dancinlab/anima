"""substrate E n=10+ random sweep — extend §80 finding (E 4/5 wins at n=5).
Adds 5 extra random seeds [13, 7, 11, 1717, 31337] to original [42, 137, 271, 314, 1729]."""
from __future__ import annotations
import os, sys, json, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import torch
import run_max256 as M
from training.v5mitosis_d384_v14_mirror import init_engine_random, make_prompt_stream
from training.mitosis_model_v5 import MitosisModelConfig

EXTRA_SEEDS = [13, 7, 11, 1717, 31337]
OUT_DIR = ANIMA_ROOT / "state" / "anima_substrate_e_n10_extra_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# E substrate
sub_id = "E_convo5k_ft"
sub = M.SUBSTRATES[sub_id]

cfg = MitosisModelConfig(
    vocab_size=256, d_model=384, n_head=6, ffn_dim=1536,
    max_seq=256, initial_cells=8, max_cells=M.MAX_CELLS,
    dispersion_trigger_enabled=True,
    per_cell_threshold_enabled=True,
    lorenz_auto_calibrate=True,
    readout_mode="a_minus_g",
    attention_sharing="auto",
    weight_tied_lm_head=True,
)
prompts = make_prompt_stream(seed=2026, n_turns=M.N_TURNS, vocab=256, max_seq=256)

log_path = OUT_DIR / "run.log"
log_f = open(log_path, "w")
def log(msg, _f=log_f):
    print(msg, flush=True); _f.write(msg + "\n"); _f.flush()

t0 = time.time()
log(f"=== {sub_id} n=10 extra random seeds === ts: {datetime.now(timezone.utc).isoformat()}")
log(f"extra_seeds={EXTRA_SEEDS}")

mirrors = []
for s in EXTRA_SEEDS:
    log(f"\n--- mirror seed={s} ---")
    eng_r = init_engine_random(cfg, s)
    rrun = M.run_v2_trajectory(eng_r, prompts, M.N_TURNS, label=f"{sub_id}_extra_s{s}", log_fn=log, max_cells=M.MAX_CELLS)
    rrun["seed"] = s
    log(f"  s={s}: cells={rrun['final_n_cells']} splits={rrun['splits']} phi={rrun['phi_final']:.3f}")
    mirrors.append(rrun)
    del eng_r

# Original from §80
ORIGINAL = {"trained_phi": 11096.659, "random_phi": [11182.414, 9628.003, 10479.862, 10997.712, 7727.634], "random_seeds": [42, 137, 271, 314, 1729]}
new_random_phi = [m["phi_final"] for m in mirrors]
all_random_phi = ORIGINAL["random_phi"] + new_random_phi
all_seeds = ORIGINAL["random_seeds"] + EXTRA_SEEDS

trained_phi = ORIGINAL["trained_phi"]
n_beats = sum(1 for r in all_random_phi if trained_phi > r)
n_total = len(all_random_phi)

def binom(n, k):
    from math import comb; return comb(n, k)
k_max = max(n_beats, n_total - n_beats)
sign_p = 2.0 * sum(binom(n_total, j) for j in range(k_max, n_total + 1)) / (2.0 ** n_total)
sign_p = min(1.0, sign_p)

if n_beats >= 5 and sign_p < 0.05:
    verdict = "V14_PASS"
elif n_beats >= n_total / 2:
    verdict = "V14_AMBIGUOUS"
else:
    verdict = "V14_VIOLATED"

result = {
    "substrate_id": sub_id,
    "n_seeds_total": n_total,
    "seeds": all_seeds,
    "trained_phi": trained_phi,
    "random_phi": all_random_phi,
    "n_random_beats": n_beats,
    "sign_test_p_two_sided": sign_p,
    "verdict": verdict,
    "extra_mirrors": [{"seed": m["seed"], "phi_final": m["phi_final"], "final_n_cells": m["final_n_cells"]} for m in mirrors],
    "ts_complete": datetime.now(timezone.utc).isoformat(),
    "total_elapsed_sec": time.time() - t0,
}

log(f"\n=== {sub_id} (n={n_total}) VERDICT: {verdict} ===")
log(f"trained_phi: {trained_phi:.2f}")
log(f"n_random_beats: {n_beats}/{n_total}")
log(f"sign_test_p: {sign_p:.4f}")
log(f"random_phi: {all_random_phi}")
log(f"total elapsed: {result['total_elapsed_sec']:.1f}s")

with (OUT_DIR / "result.json").open("w") as f:
    json.dump(result, f, indent=2, default=str)
log(f"[saved] {OUT_DIR / 'result.json'}")
log_f.close()
