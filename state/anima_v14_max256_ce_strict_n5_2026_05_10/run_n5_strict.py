"""BG-V14-MAX256-CE-STRICT-N5 — C + E n=5 strict upgrade at max_cells=256.

§51 BG-V14-MAX256-CAP-FREE-MULTI delivered ★★★★★ PARTIAL:
  - A_phase2_cotrain: 5/5 V14_PASS (full)
  - C_cells64_aware:  2/2 V14_PASS (n=2 partial, sign-p=0.5)
  - E_convo5k_ft:     2/2 V14_PASS (n=2 partial, sign-p=0.5, mirrors reused from C)

This BG closes the n=5 gap for C and E by running the 3 missing mirror
seeds [271, 314, 1729] at max_cells=256, n_turns=100.

Critical efficiency: v2 path mirrors are ckpt-independent (init_engine_random
+ make_prompt_stream are deterministic with cfg+seed only). Therefore mirror
seeds can be run ONCE and reused across both substrates C and E, identical
to §51's pattern (which empirically verified E-s42 trajectory == C-s42).

Plan:
  1. Run TRAINED for C at max=256 n_turns=100 (re-baseline; deterministic)
  2. Run TRAINED for E at max=256 n_turns=100 (re-baseline; deterministic)
  3. Run mirrors s271, s314, s1729 ONCE (shared between C and E)
  4. Combine with §51 cached s42, s137 results from result_C/E.json
  5. Compute n=5 strict sign-test verdict

Total: 5 v2 trajectories × ~13 min cap-bound = ~65 min budget.

Output:
  - state/anima_v14_max256_ce_strict_n5_2026_05_10/spec.md
  - state/anima_v14_max256_ce_strict_n5_2026_05_10/result.json
  - state/anima_v14_max256_ce_strict_n5_2026_05_10/verdict.md
  - state/anima_v14_max256_ce_strict_n5_2026_05_10/run_n5.log

raw#9 / raw#15 / own 14 / own 16 / own 22 / own 38 honored.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

ANIMA_ROOT = Path("/Users/ghost/core/anima")
THIS_DIR = ANIMA_ROOT / "state" / "anima_v14_max256_ce_strict_n5_2026_05_10"
PRIOR_DIR = ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"
THIS_DIR.mkdir(parents=True, exist_ok=True)

# upstream module imports (additive, raw#15)
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_clm_v5_iit_phi_remetric_2026_05_10"))

from training.mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402
from training.v5mitosis_d384_v14_mirror import (  # noqa: E402
    init_engine_from_v2,
    init_engine_random,
    make_prompt_stream,
)


# ─── Config (matches §51 exactly except seed-set is differential)
MAX_CELLS = 256
N_TURNS = 100
SNAP_EVERY = 25
PROMPT_SEED = 2026

V4_SEEDS_FULL = [42, 137, 271, 314, 1729]
SEEDS_NEW = [271, 314, 1729]  # the 3 missing seeds
SEEDS_CACHED = [42, 137]      # already completed in §51

SUBSTRATES = {
    "C_cells64_aware": {
        "ckpt": str(ANIMA_ROOT / "state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt"),
        "schema": "v2_d384",
        "arch": "v2 6L transformer d=384 heads=6",
        "paradigm": "aware_max_cells_64",
        "cached_result": str(PRIOR_DIR / "result_C_cells64_aware.json"),
    },
    "E_convo5k_ft": {
        "ckpt": str(ANIMA_ROOT / "state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt"),
        "schema": "v2_d384",
        "arch": "v2-derived 6L d=384 byte-level (FT)",
        "paradigm": "naive_ft_no_mitosis",
        "cached_result": str(PRIOR_DIR / "result_E_convo5k_ft.json"),
    },
}


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _binom_coef(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    for i in range(k):
        num = num * (n - i) // (i + 1)
    return num


def sign_test_p_value(n_beats: int, n: int) -> float:
    if n <= 0:
        return float("nan")
    k = max(n_beats, n - n_beats)
    tail = sum(_binom_coef(n, j) for j in range(k, n + 1))
    p = 2.0 * tail / (2.0 ** n)
    return min(1.0, p)


def alpha_v2(traj):
    xs, ys = [], []
    for entry in traj:
        # entry is (turn, n_cells, phi, phi_per_cell)
        if len(entry) < 4:
            continue
        nc = entry[1]
        phi_pc = entry[3]
        if nc < 2 or phi_pc <= 0:
            continue
        xs.append(math.log(nc))
        ys.append(math.log(phi_pc + 1.0))
    if len(xs) < 5:
        return None
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den < 1e-12:
        return None
    return num / den


def run_v2_trajectory(eng, prompts, n_turns, label, log_fn, max_cells):
    eng.eval()
    cell_counts = []
    phi_traj = []
    cap_bound_turns = 0
    first_cap_turn = None
    t0 = time.time()
    last_print = 0.0
    with torch.no_grad():
        for t in range(n_turns):
            prompt = prompts[t][:, : eng.max_seq]
            try:
                logits, info = eng(prompt)
                eng.mitosis_step(info)
            except Exception:
                phi_traj.append((t, eng.n_cells, -1.0, -1.0))
                continue
            cell_counts.append(eng.n_cells)
            if eng.n_cells >= max_cells:
                cap_bound_turns += 1
                if first_cap_turn is None:
                    first_cap_turn = t
            if (t % SNAP_EVERY) == 0 or t == n_turns - 1:
                phi_traj.append((t, eng.n_cells, eng.phi, eng.phi_per_cell))
                if time.time() - last_print > 8:
                    el = time.time() - t0
                    log_fn(
                        f"  [{label}] turn {t:>4d} n_cells={eng.n_cells} "
                        f"phi={eng.phi:.3f} ({el:.1f}s)"
                    )
                    last_print = time.time()
    el_total = time.time() - t0
    status = eng.status()
    return {
        "label": label,
        "n_turns": n_turns,
        "elapsed_s": el_total,
        "final_n_cells": eng.n_cells,
        "max_n_cells_observed": max(cell_counts) if cell_counts else eng.n_cells,
        "splits": status["splits"],
        "splits_by_dispersion": status.get("splits_by_dispersion", 0),
        "merges": status["merges"],
        "ratchets": status["ratchets"],
        "phi_final": eng.phi,
        "phi_per_cell_final": eng.phi_per_cell,
        "phi_best": eng._phi_best,
        "phi_per_cell_best": eng._phi_per_cell_best,
        "cap_bound_turns": cap_bound_turns,
        "first_cap_turn": first_cap_turn,
        "phi_trajectory": phi_traj,
    }


def make_cfg() -> MitosisModelConfig:
    return MitosisModelConfig(
        vocab_size=256, d_model=384, n_head=6, ffn_dim=1536,
        max_seq=256, initial_cells=8, max_cells=MAX_CELLS,
        dispersion_trigger_enabled=True,
        per_cell_threshold_enabled=True,
        lorenz_auto_calibrate=True,
        readout_mode="a_minus_g",
        attention_sharing="auto",
        weight_tied_lm_head=True,
    )


def run_trained(sub_id, sub, log_fn):
    log_fn(f"\n{'='*72}\n[{sub_id}] TRAINED — max_cells={MAX_CELLS} n_turns={N_TURNS}\n{'='*72}")
    log_fn(f"ckpt: {sub['ckpt']}")
    sha = sha256_of(sub["ckpt"])
    log_fn(f"sha256: {sha}")
    ck = torch.load(sub["ckpt"], map_location="cpu", weights_only=False)
    sd = ck["model_state"]
    n_params = sum(v.numel() for v in sd.values() if hasattr(v, "numel"))
    log_fn(f"trained: params={n_params/1e6:.2f}M step={ck.get('step')}")

    cfg = make_cfg()
    prompts = make_prompt_stream(seed=PROMPT_SEED, n_turns=N_TURNS, vocab=256, max_seq=256)
    torch.manual_seed(0)
    eng_t, diag = init_engine_from_v2(cfg, sd)
    log_fn(f"  v2 blocks loaded={diag['v2_blocks_loaded']} random_cells={diag['random_cells']}")
    out = run_v2_trajectory(
        eng_t, prompts, N_TURNS, label=f"{sub_id}_trained",
        log_fn=log_fn, max_cells=MAX_CELLS,
    )
    out["alpha_v2"] = alpha_v2(out["phi_trajectory"])
    log_fn(
        f"  [{sub_id}] TRAINED: cells={out['final_n_cells']} splits={out['splits']} "
        f"phi={out['phi_final']:.3f} phi/c={out['phi_per_cell_final']:.3f} "
        f"alpha={out['alpha_v2']} cap_bound={out['cap_bound_turns']}/{N_TURNS} "
        f"first_cap={out['first_cap_turn']} elapsed={out['elapsed_s']:.1f}s"
    )
    return out, sha, n_params


def run_mirror(seed, log_fn):
    log_fn(f"\n--- mirror seed={seed} (shared C+E) ---")
    cfg = make_cfg()
    prompts = make_prompt_stream(seed=PROMPT_SEED, n_turns=N_TURNS, vocab=256, max_seq=256)
    eng_r = init_engine_random(cfg, seed)
    out = run_v2_trajectory(
        eng_r, prompts, N_TURNS, label=f"shared_s{seed}",
        log_fn=log_fn, max_cells=MAX_CELLS,
    )
    out["seed"] = seed
    out["alpha_v2"] = alpha_v2(out["phi_trajectory"])
    log_fn(
        f"  s={seed}: cells={out['final_n_cells']} splits={out['splits']} "
        f"phi={out['phi_final']:.3f} phi/c={out['phi_per_cell_final']:.3f} "
        f"alpha={out['alpha_v2']} cap_bound={out['cap_bound_turns']}/{N_TURNS} "
        f"first_cap={out['first_cap_turn']} elapsed={out['elapsed_s']:.1f}s"
    )
    return out


def load_cached_mirrors(sub_id, sub) -> list:
    """Pull cached s42, s137 mirror runs from §51 result.json."""
    p = Path(sub["cached_result"])
    j = json.loads(p.read_text())
    return j.get("mirror_runs", [])


def assemble_verdict(sub_id, sub, sha, n_params, trained, all_mirrors):
    rand_phi = [m["phi_final"] for m in all_mirrors]
    rand_phi_pc = [m["phi_per_cell_final"] for m in all_mirrors]
    rand_cells = [m["final_n_cells"] for m in all_mirrors]
    rand_first_cap = [m["first_cap_turn"] for m in all_mirrors]
    rand_cap_bound = [m["cap_bound_turns"] for m in all_mirrors]
    n = len(rand_phi)
    n_beats = sum(1 for r in rand_phi if trained["phi_final"] > r)
    n_beats_pc = sum(1 for r in rand_phi_pc if trained["phi_per_cell_final"] > r)
    p_sign = sign_test_p_value(n_beats, n)
    p_sign_pc = sign_test_p_value(n_beats_pc, n)
    if n_beats == n and n_beats_pc == n:
        verdict = "V14_STRICT_PASS"
    elif n_beats >= n - 1 and n_beats_pc >= n - 1:
        verdict = "V14_NEAR_PASS"
    elif n_beats == n or n_beats_pc == n:
        verdict = "V14_PARTIAL"
    elif n_beats <= 1 and n_beats_pc <= 1:
        verdict = "V14_VIOLATED"
    else:
        verdict = "V14_AMBIGUOUS"
    return {
        "substrate_id": sub_id,
        "schema": sub["schema"],
        "arch": sub["arch"],
        "paradigm": sub["paradigm"],
        "ckpt": sub["ckpt"],
        "ckpt_sha256": sha,
        "n_params": n_params,
        "n_turns": N_TURNS,
        "max_cells_setting": MAX_CELLS,
        "metric_primary": "phi_final + phi_per_cell_final",
        "trained_phi": trained["phi_final"],
        "trained_phi_per_cell": trained["phi_per_cell_final"],
        "trained_alpha_v2": trained["alpha_v2"],
        "trained_n_cells": trained["final_n_cells"],
        "trained_splits": trained["splits"],
        "trained_cap_bound_turns": trained["cap_bound_turns"],
        "trained_first_cap_turn": trained["first_cap_turn"],
        "trained_max_n_cells_observed": trained["max_n_cells_observed"],
        "random_seeds": [m.get("seed") for m in all_mirrors],
        "random_phi": rand_phi,
        "random_phi_per_cell": rand_phi_pc,
        "random_n_cells": rand_cells,
        "random_first_cap_turn": rand_first_cap,
        "random_cap_bound_turns": rand_cap_bound,
        "n_random_beats_phi": n_beats,
        "n_random_beats_phi_per_cell": n_beats_pc,
        "n_random_total": n,
        "sign_test_p_phi": p_sign,
        "sign_test_p_phi_per_cell": p_sign_pc,
        "verdict": verdict,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mirrors-only", action="store_true",
                    help="Run only the 3 new mirrors (skip TRAINED reruns; reuse §51 trained values)")
    ap.add_argument("--reuse-cached-trained", action="store_true",
                    help="Reuse §51's cached trained_phi values; skip C/E TRAINED runs")
    args = ap.parse_args()

    log_path = THIS_DIR / "run_n5.log"
    log_f = open(log_path, "a")

    def log(msg, _f=log_f):
        print(msg, flush=True)
        _f.write(msg + "\n")
        _f.flush()

    log(f"\n=== BG-V14-MAX256-CE-STRICT-N5 — {datetime.now(timezone.utc).isoformat()} ===")
    log(f"V4_SEEDS_FULL={V4_SEEDS_FULL}  SEEDS_NEW={SEEDS_NEW}  SEEDS_CACHED={SEEDS_CACHED}")
    log(f"max_cells={MAX_CELLS} n_turns={N_TURNS} prompt_seed={PROMPT_SEED}")

    # ── Step 1: Run 3 NEW shared mirrors (deterministic, ckpt-independent)
    log("\n[Step 1] Running 3 NEW mirror seeds (shared C+E, deterministic)")
    new_mirrors = []
    for s in SEEDS_NEW:
        m = run_mirror(s, log)
        new_mirrors.append(m)
    log(f"\n[Step 1 done] {len(new_mirrors)} new mirrors complete")

    aggregate = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "config": {
            "max_cells": MAX_CELLS,
            "n_turns": N_TURNS,
            "snap_every": SNAP_EVERY,
            "v4_seeds_full": V4_SEEDS_FULL,
            "seeds_new": SEEDS_NEW,
            "seeds_cached": SEEDS_CACHED,
            "prompt_seed": PROMPT_SEED,
        },
        "shared_new_mirrors": [
            {
                "seed": m["seed"],
                "elapsed_s": m["elapsed_s"],
                "final_n_cells": m["final_n_cells"],
                "max_n_cells_observed": m["max_n_cells_observed"],
                "splits": m["splits"],
                "phi_final": m["phi_final"],
                "phi_per_cell_final": m["phi_per_cell_final"],
                "alpha_v2": m["alpha_v2"],
                "cap_bound_turns": m["cap_bound_turns"],
                "first_cap_turn": m["first_cap_turn"],
                "phi_trajectory": m["phi_trajectory"],
            }
            for m in new_mirrors
        ],
        "substrates": {},
    }

    # ── Step 2: For each substrate (C, E), assemble n=5 verdict
    for sub_id, sub in SUBSTRATES.items():
        log(f"\n{'='*72}\n[Step 2] Assemble n=5 verdict for {sub_id}\n{'='*72}")

        if args.reuse_cached_trained:
            cache = json.loads(Path(sub["cached_result"]).read_text())
            log(f"  reusing §51 cached TRAINED: phi={cache['trained_phi']} "
                f"phi/c={cache['trained_phi_per_cell']}")
            trained = {
                "phi_final": cache["trained_phi"],
                "phi_per_cell_final": cache["trained_phi_per_cell"],
                "alpha_v2": cache["trained_alpha_v2"],
                "final_n_cells": cache["trained_n_cells"],
                "splits": cache["trained_splits"],
                "cap_bound_turns": cache["trained_cap_bound_turns"],
                "first_cap_turn": cache["trained_first_cap_turn"],
                "max_n_cells_observed": cache["trained_max_n_cells_observed"],
            }
            sha = cache["ckpt_sha256"]
            n_params = cache["n_params"]
        else:
            trained, sha, n_params = run_trained(sub_id, sub, log)

        # Cached mirrors from §51 (s42, s137)
        cached_mirrors = load_cached_mirrors(sub_id, sub)
        log(f"  cached mirrors from §51: {[m['seed'] for m in cached_mirrors]}")

        # Combine: cached (s42, s137) + new (s271, s314, s1729)
        all_mirrors = list(cached_mirrors) + [
            {
                "seed": m["seed"],
                "elapsed_s": m["elapsed_s"],
                "final_n_cells": m["final_n_cells"],
                "max_n_cells_observed": m["max_n_cells_observed"],
                "splits": m["splits"],
                "phi_final": m["phi_final"],
                "phi_per_cell_final": m["phi_per_cell_final"],
                "alpha_v2": m["alpha_v2"],
                "cap_bound_turns": m["cap_bound_turns"],
                "first_cap_turn": m["first_cap_turn"],
            }
            for m in new_mirrors
        ]

        assert [m["seed"] for m in all_mirrors] == V4_SEEDS_FULL, \
            f"seed-order mismatch: got {[m['seed'] for m in all_mirrors]}"

        verdict = assemble_verdict(sub_id, sub, sha, n_params, trained, all_mirrors)
        verdict["all_mirrors_n5"] = all_mirrors
        verdict["trained_summary"] = {
            "phi_final": trained.get("phi_final"),
            "phi_per_cell_final": trained.get("phi_per_cell_final"),
            "alpha_v2": trained.get("alpha_v2"),
            "final_n_cells": trained.get("final_n_cells"),
            "splits": trained.get("splits"),
            "cap_bound_turns": trained.get("cap_bound_turns"),
            "first_cap_turn": trained.get("first_cap_turn"),
        }
        log(
            f"\n[{sub_id} n=5 verdict] {verdict['verdict']}  "
            f"n_beats_phi={verdict['n_random_beats_phi']}/{verdict['n_random_total']} "
            f"sign_p={verdict['sign_test_p_phi']:.4f}  "
            f"n_beats_phi_per_cell={verdict['n_random_beats_phi_per_cell']}/{verdict['n_random_total']} "
            f"sign_p_pc={verdict['sign_test_p_phi_per_cell']:.4f}"
        )
        aggregate["substrates"][sub_id] = verdict

    # ── Save
    res_path = THIS_DIR / "result.json"
    with res_path.open("w") as f:
        json.dump(aggregate, f, indent=2, default=str)
    log(f"\n[saved] {res_path}")

    log_f.close()


if __name__ == "__main__":
    main()
