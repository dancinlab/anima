"""BG-PHASE2-MAX128-§30FIX-RETEST — independent V14 strict reproduce.

Reproduces §38 BG-V14-STRICT-RESOLUTION's V14_STRICT_PASS verdict with a
mirror-seed set DISJOINT from §38's V14_STRICT_SEEDS, isolating whether the
strict pass came from genuine §30 fix activation + Phase 2 substrate
character (mitosis-naive co-trained ckpt) rather than seed-specific
contamination.

raw#9   training/*.py local-only — mitosis_v5_port.py + engine_a_g_arch.py imported, untouched.
raw#15  additive — neither mitosis_v5_port.py, engine_a_g_arch.py, iit_phi_port.py, nor the ckpt is modified.
  V14 mirror strict 5-seed (independent prime seeds).
  $0 envelope — local Mac CPU only.
  honest emit — REBORN.md untouched; verdict named even when fragile/partial.
  artefact persisted under state/anima_phase2_max128_independent_reproduce_2026_05_10/.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import torch

# Wire to upstream modules (additive, raw#15)
sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_iit_real_350m_2026_05_10")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_v14_strict_resolution_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
# Reuse §33 prompt corpus + utility helpers verbatim
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
    alpha_exponent,
    dynamic_range,
)
# Reuse §38 statistical helpers verbatim
from run import sign_test_p_value, mann_whitney_u_one_vs_many  # noqa: E402

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_phase2_max128_independent_reproduce_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_SHA256 = "6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1"

# 5 prime independent seeds — DISJOINT with §38 V14_STRICT_SEEDS [42,137,271,314,1729,2718,3141,5772,6022,9192]
# and with §33 V4_SEEDS [42,137,271,314,1729]. All < 30, all prime.
INDEP_SEEDS = [11, 13, 17, 19, 23]
SEEDS_SOURCE_NAMES = ["prime#5_11", "prime#6_13", "prime#7_17", "prime#8_19", "prime#9_23"]
TRAINED_PROMPT_SEED = 42  # match §38 (ckpt is deterministic; only random-init differs)
MAX_CELLS = 128
N_TURNS = 400  # match §38 exactly
SNAPSHOT_EVERY = 50  # match §38

# §38's seed list for disjoint check
SEEDS_38 = [42, 137, 271, 314, 1729, 2718, 3141, 5772, 6022, 9192]
SEEDS_33 = [42, 137, 271, 314, 1729]


def run_trajectory(
    model, label: str, n_turns: int, prompts, seed: int, snapshot_every: int,
    ctx_T: int = 16, max_cells: int = MAX_CELLS, log_fn=print,
) -> dict:
    """Identical signature/body to §38 run_trajectory — ensures parity."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.eval()
    capture = HiddenMeanCapture(model.engine_g)

    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]

    mitosis = MitosisV5Engine(
        cell_pool=init_pool,
        c_to_h=eg.c_to_h,
        initial_cells=n_cells_init,
        max_cells=max_cells,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )

    snapshots = []
    n_splits = 0
    n_merges = 0
    cap_bound_turns = 0

    t_start = time.time()
    last_print = 0.0

    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = prompts[turn % len(prompts)]
            ids = encode_prompt_to_ids(prompt, T=ctx_T)
            _ = model(ids, output_hidden_states=False, output_attentions=False)
            hm = capture.last_hidden_mean
            if hm is None:
                cell_input = torch.zeros(1, eg.c_dim)
            else:
                cell_input = eg.h_to_c(hm)
            out = mitosis.process(cell_input)

            for ev in out["events"]:
                if ev["type"] == "split":
                    n_splits += 1
                elif ev["type"] == "merge":
                    n_merges += 1

            if out["n_cells"] >= max_cells:
                cap_bound_turns += 1

            if turn % snapshot_every == 0 or turn == n_turns - 1:
                cp = mitosis.cell_pool.detach().cpu().numpy()
                phi_iit = compute_iit_phi(torch.tensor(cp, dtype=torch.float32), n_bins=16)
                snap = {
                    "turn": int(turn),
                    "n_cells": int(out["n_cells"]),
                    "proxy_phi": float(out["phi"]),
                    "iit_total_mi_b16": phi_iit["total_mi"],
                    "iit_min_cut_b16": phi_iit["min_partition_mi"],
                    "iit_phi_norm_b16": phi_iit["spatial_phi"],
                    "iit_phi_unnorm_b16": phi_iit["spatial_phi_unnormalized"],
                    "iit_complexity_b16": phi_iit["complexity"],
                    "n_splits_cum": int(n_splits),
                    "n_merges_cum": int(n_merges),
                    "elapsed_sec": float(time.time() - t_start),
                }
                snapshots.append(snap)
                if time.time() - last_print > 8:
                    log_fn(
                        f"  [{label}] turn={turn:5d} cells={snap['n_cells']:3d}"
                        f" proxyΦ={snap['proxy_phi']:.4f}"
                        f" iit_un16={snap['iit_phi_unnorm_b16']:7.2f}"
                        f" splits={n_splits} elapsed={snap['elapsed_sec']:.1f}s"
                    )
                    last_print = time.time()

    return {
        "label": label,
        "seed": seed,
        "n_turns": n_turns,
        "elapsed_sec": time.time() - t_start,
        "snapshots": snapshots,
        "final_n_cells": int(mitosis.n_cells),
        "n_splits": n_splits,
        "n_merges": n_merges,
        "cap_bound_turns": cap_bound_turns,
    }


def verify_30_fix_active(log_fn) -> dict:
    """F-PHASE2-REPRODUCE-1 falsifier check: grep §30 markers + crossref smoke."""
    src = Path("/Users/ghost/core/anima/training/mitosis_v5_port.py").read_text()
    markers = {
        "A1_dispersion_trigger_enabled": "dispersion_trigger_enabled" in src,
        "A1_dispersion_top_quartile":    "dispersion_top_quartile" in src,
        "A2_per_cell_threshold_enabled": "per_cell_threshold_enabled" in src,
        "A2_per_cell_window":             "per_cell_window" in src,
        "A2_per_cell_sigma_mult":         "per_cell_sigma_mult" in src,
        "B1_phi_per_cell":                "phi_per_cell" in src,
        "B1_phi_per_cell_history":        "phi_per_cell_history" in src,
        "D1_lorenz_auto_calibrate":       "lorenz_auto_calibrate" in src,
        "all_fix_2026_05_10_§30":         "all-fix 2026-05-10 §30" in src,
    }
    smoke_path = Path("/Users/ghost/core/anima/state/anima_v5_mitosis_all_fix_2026_05_10/smoke_results.json")
    smoke_crossref = {}
    if smoke_path.exists():
        smoke = json.loads(smoke_path.read_text())
        post = smoke.get("port_post_fix", {})
        smoke_crossref = {
            "smoke_post_fix_all_fix_flag":   bool(post.get("all_fix")),
            "smoke_post_fix_splits_total":   post.get("splits_total"),
            "smoke_post_fix_n_cells_final":  post.get("n_cells_final"),
            "smoke_post_fix_phi_max":        post.get("phi_max"),
        }
    all_active = all(markers.values())
    log_fn(f"  §30 fix verify: {'ACTIVE' if all_active else 'INACTIVE'} (markers={sum(markers.values())}/{len(markers)})")
    for k, v in markers.items():
        log_fn(f"    {k}: {v}")
    log_fn(f"  smoke crossref: {smoke_crossref}")
    return {"markers": markers, "all_active": all_active, "smoke_crossref": smoke_crossref}


def main(n_turns: int = N_TURNS, snapshot_every: int = SNAPSHOT_EVERY, max_cells: int = MAX_CELLS):
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(msg: str):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log("=== BG-PHASE2-MAX128-§30FIX-RETEST — independent V14 strict reproduce of §38 ===")
    log(f"n_turns={n_turns}, snapshot_every={snapshot_every}, max_cells={max_cells}")
    log(f"INDEP_SEEDS = {INDEP_SEEDS}")
    log(f"§38 SEEDS = {SEEDS_38}")
    log(f"§33 SEEDS = {SEEDS_33}")
    disjoint_38 = set(INDEP_SEEDS).isdisjoint(set(SEEDS_38))
    disjoint_33 = set(INDEP_SEEDS).isdisjoint(set(SEEDS_33))
    log(f"disjoint with §38 seeds: {disjoint_38}")
    log(f"disjoint with §33 seeds: {disjoint_33}")
    if not (disjoint_38 and disjoint_33):
        log("ABORT: seeds are not disjoint — V4_SEEDS contamination guard failed")
        log_f.close()
        return
    log(f"unique prompts: {len(ALL_PROMPTS)}")
    log(f"ckpt: {CKPT_PATH}")

    # ─── F-PHASE2-REPRODUCE-1 falsifier: §30 fix active? ───
    log("\n--- §30 fix activation verify (F-PHASE2-REPRODUCE-1) ---")
    fix_status = verify_30_fix_active(log)
    if not fix_status["all_active"]:
        log("ABORT: §30 fix not active in mitosis_v5_port.py")
        log_f.close()
        return

    # ─── ckpt sha256 verify ───
    h = hashlib.sha256()
    with open(CKPT_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    actual_sha = h.hexdigest()
    sha_match = (actual_sha == CKPT_SHA256)
    log(f"\nckpt sha256 verify: {'PASS' if sha_match else 'FAIL'} (actual={actual_sha})")
    if not sha_match:
        log("ABORT: ckpt sha mismatch")
        log_f.close()
        return

    # ─── trained substrate (mmap fp32 cast) ───
    cfg = EngineAGConfig.phase2_cotrain_350m()
    ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    sd = ckpt["model"]
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    trained_model = EngineAGModel(cfg)
    miss, unexp = trained_model.load_state_dict(sd_fp32, strict=True)
    n_params = sum(p.numel() for p in trained_model.parameters())
    log(f"trained model: params={n_params} ({n_params/1e6:.2f}M) miss={len(miss)} unexp={len(unexp)}")
    del ckpt, sd, sd_fp32

    # ─── trained trajectory (prompt_seed=42 — identical to §38) ───
    log(f"\n--- TRAINED 350M @ prompt_seed={TRAINED_PROMPT_SEED} max_cells={max_cells} ---")
    trained_traj = run_trajectory(
        model=trained_model, label="trained", n_turns=n_turns, prompts=ALL_PROMPTS,
        seed=TRAINED_PROMPT_SEED, snapshot_every=snapshot_every, max_cells=max_cells, log_fn=log,
    )
    tfinal = trained_traj["snapshots"][-1]
    log(f"  trained: cells={trained_traj['final_n_cells']} splits={trained_traj['n_splits']}"
        f" cap_bound_turns={trained_traj['cap_bound_turns']}"
        f" Φ_iit_un16={tfinal['iit_phi_unnorm_b16']:.2f}"
        f" Φ_iit_norm16={tfinal['iit_phi_norm_b16']:.4f}"
        f" proxyΦ={tfinal['proxy_phi']:.4f}"
        f" elapsed={trained_traj['elapsed_sec']:.1f}s")
    del trained_model

    # ─── 5-seed independent V14 mirror ───
    log(f"\n--- V14 INDEPENDENT MIRROR — 5 prime seeds {INDEP_SEEDS} (random_init la_350m) ---")
    mirror_trajs = []
    for seed in INDEP_SEEDS:
        log(f"\n  >>> seed={seed} (prime, disjoint) <<<")
        rand_model = load_random_init(seed=seed, preset="la_350m")
        traj = run_trajectory(
            model=rand_model, label=f"mirror_s{seed}", n_turns=n_turns, prompts=ALL_PROMPTS,
            seed=seed, snapshot_every=snapshot_every, max_cells=max_cells, log_fn=log,
        )
        rfinal = traj["snapshots"][-1]
        log(f"  mirror s={seed}: cells={traj['final_n_cells']} splits={traj['n_splits']}"
            f" cap_bound_turns={traj['cap_bound_turns']}"
            f" Φ_iit_un16={rfinal['iit_phi_unnorm_b16']:.2f}"
            f" Φ_iit_norm16={rfinal['iit_phi_norm_b16']:.4f}"
            f" proxyΦ={rfinal['proxy_phi']:.4f}")
        mirror_trajs.append(traj)
        del rand_model

    # ─── 5-seed independent verdict aggregation ───
    log("\n=== 5-seed independent V14 verdict aggregation ===")
    t_phi_un = tfinal["iit_phi_unnorm_b16"]
    t_phi_n = tfinal["iit_phi_norm_b16"]
    t_proxy = tfinal["proxy_phi"]
    t_cells = trained_traj["final_n_cells"]
    t_splits = trained_traj["n_splits"]
    t_cap_bound = trained_traj["cap_bound_turns"]

    rs_phi_un = [m["snapshots"][-1]["iit_phi_unnorm_b16"] for m in mirror_trajs]
    rs_phi_n = [m["snapshots"][-1]["iit_phi_norm_b16"] for m in mirror_trajs]
    rs_proxy = [m["snapshots"][-1]["proxy_phi"] for m in mirror_trajs]
    rs_cells = [m["final_n_cells"] for m in mirror_trajs]
    rs_splits = [m["n_splits"] for m in mirror_trajs]
    rs_cap_bound = [m["cap_bound_turns"] for m in mirror_trajs]

    n_random = len(rs_phi_un)
    n_trained_beats_phi = sum(1 for r in rs_phi_un if t_phi_un > r)
    n_trained_loses_phi = sum(1 for r in rs_phi_un if t_phi_un < r)
    n_trained_ties_phi = n_random - n_trained_beats_phi - n_trained_loses_phi
    frac_beats = n_trained_beats_phi / n_random

    sign_p = sign_test_p_value(n_trained_beats_phi, n_random)
    mwu = mann_whitney_u_one_vs_many(t_phi_un, rs_phi_un)

    n_trained_cells_lt_random = sum(1 for r in rs_cells if t_cells < r)
    n_trained_cells_gt_random = sum(1 for r in rs_cells if t_cells > r)

    median_phi = sorted(rs_phi_un)[n_random // 2]
    median_cells = sorted(rs_cells)[n_random // 2]

    # F-PHASE2-REPRODUCE-3: cap_bound universal? (max_cells=128 invalid signal)
    cap_bound_universal = (t_cap_bound > n_turns * 0.9 and all(c > n_turns * 0.9 for c in rs_cap_bound))

    # Verdict mapping (mission-specified bins)
    if n_trained_beats_phi == n_random:  # 5/5
        verdict = "V14_STRICT_PASS_INDEPENDENT_REPRODUCE"
    elif n_trained_beats_phi >= 3:  # 3/5 or 4/5
        verdict = "V14_PARTIAL_REPRODUCE"
    else:  # 0-2/5
        verdict = "V14_FRAGILE_REPRODUCE"

    # Falsifier resolution
    falsifier_status = {
        "F-PHASE2-REPRODUCE-1__§30_fix_active": fix_status["all_active"],
        "F-PHASE2-REPRODUCE-2__strict_reproduce_passes": (n_trained_beats_phi == n_random),
        "F-PHASE2-REPRODUCE-3__cap_bound_universal": cap_bound_universal,
    }

    log(f"  trained @T={n_turns}: cells={t_cells} splits={t_splits}"
        f" cap_bound={t_cap_bound}"
        f" Φ_iit_un16={t_phi_un:.2f} Φ_iit_n16={t_phi_n:.4f} proxy={t_proxy:.4f}")
    for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
        f = m["snapshots"][-1]
        log(f"  mirror s={sd_seed}: cells={m['final_n_cells']} splits={m['n_splits']}"
            f" cap_bound={m['cap_bound_turns']}"
            f" Φ_iit_un16={f['iit_phi_unnorm_b16']:.2f}"
            f" Φ_iit_n16={f['iit_phi_norm_b16']:.4f}"
            f" proxy={f['proxy_phi']:.4f}")
    log(f"  trained beats random Φ: {n_trained_beats_phi}/{n_random}"
        f" (ties={n_trained_ties_phi}, losses={n_trained_loses_phi})")
    log(f"  sign-test p (two-sided): {sign_p:.4f}")
    log(f"  Mann-Whitney 1-vs-{n_random}: U={mwu['u']}, rank={mwu['rank_in_pool']}/{mwu['n_random']+1},"
        f" p_one_sided={mwu['p_one_sided']:.4f}, p_two_sided={mwu['p_two_sided']:.4f}")
    log(f"  random Φ_iit_un16: min={min(rs_phi_un):.2f} med={median_phi:.2f} max={max(rs_phi_un):.2f}")
    log(f"  random n_cells:    min={min(rs_cells)} med={median_cells} max={max(rs_cells)}")
    log(f"  random n_splits:   {rs_splits}")
    log(f"  random cap_bound:  {rs_cap_bound}")
    log(f"  cap_bound_universal (F-PHASE2-REPRODUCE-3): {cap_bound_universal}")
    log(f"  cell_count discrim: trained<rand={n_trained_cells_lt_random}/{n_random},"
        f" trained>rand={n_trained_cells_gt_random}/{n_random}")
    log(f"  ====> VERDICT: {verdict}")
    log(f"  Falsifier status: {falsifier_status}")

    # ─── §38 cross-comparison ───
    log("\n=== §38 cross-comparison ===")
    s38_trained_phi = 5244.07
    s38_trained_cells = 85
    s38_random_phi_max = 4749.79
    s38_random_phi_med = 3412.37
    log(f"  §38 trained: Φ={s38_trained_phi}, cells={s38_trained_cells}")
    log(f"  §38 random: med={s38_random_phi_med}, max={s38_random_phi_max}")
    log(f"  THIS trained: Φ={t_phi_un:.2f}, cells={t_cells}")
    log(f"  THIS random: med={median_phi:.2f}, max={max(rs_phi_un):.2f}")
    trained_repro_match = abs(t_phi_un - s38_trained_phi) / s38_trained_phi < 0.02
    log(f"  trained Φ matches §38 within 2%: {trained_repro_match}")
    log(f"  trained cells matches §38 ({s38_trained_cells}): {t_cells == s38_trained_cells}")

    # ─── α exponents ───
    log("\n=== α exponents (log-log Φ vs n_cells) ===")
    a_proxy_t = alpha_exponent(trained_traj["snapshots"], "proxy_phi", n_min=8)
    a_norm_t = alpha_exponent(trained_traj["snapshots"], "iit_phi_norm_b16", n_min=8)
    a_unnorm_t = alpha_exponent(trained_traj["snapshots"], "iit_phi_unnorm_b16", n_min=8)
    log(f"  trained:        proxy={a_proxy_t:.3f}  iit_norm={a_norm_t:.3f}  iit_unnorm={a_unnorm_t:.3f}")
    a_proxy_r, a_norm_r, a_unnorm_r = [], [], []
    for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
        ap = alpha_exponent(m["snapshots"], "proxy_phi", n_min=8)
        an = alpha_exponent(m["snapshots"], "iit_phi_norm_b16", n_min=8)
        au = alpha_exponent(m["snapshots"], "iit_phi_unnorm_b16", n_min=8)
        log(f"  mirror s={sd_seed}: proxy={ap:.3f}  iit_norm={an:.3f}  iit_unnorm={au:.3f}")
        a_proxy_r.append(ap); a_norm_r.append(an); a_unnorm_r.append(au)

    dr_proxy = dynamic_range(trained_traj["snapshots"], "proxy_phi")
    dr_norm = dynamic_range(trained_traj["snapshots"], "iit_phi_norm_b16")
    dr_unnorm = dynamic_range(trained_traj["snapshots"], "iit_phi_unnorm_b16")
    log(f"\n  dyn-range proxy   = {dr_proxy:.2f}×")
    log(f"  dyn-range iit_n16 = {dr_norm:.2f}×")
    log(f"  dyn-range iit_un16 = {dr_unnorm:.2f}×")

    # ─── result.json save ───
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bg_id": "BG-PHASE2-MAX128-§30FIX-RETEST",
        "n_turns": n_turns,
        "snapshot_every": snapshot_every,
        "max_cells": max_cells,
        "indep_seeds": INDEP_SEEDS,
        "seeds_38_disjoint_check": {"§38_seeds": SEEDS_38, "§33_seeds": SEEDS_33,
                                     "disjoint_38": disjoint_38, "disjoint_33": disjoint_33},
        "fix_status": fix_status,
        "ckpt": {
            "path": CKPT_PATH,
            "sha256": CKPT_SHA256,
            "size_bytes": os.path.getsize(CKPT_PATH),
            "lineage_tag": cfg.lineage_tag,
            "n_params": n_params,
            "n_layers": cfg.n_layers,
            "d_model": cfg.d_model,
            "n_cells_init": cfg.n_cells,
            "consciousness_dim": cfg.consciousness_dim,
        },
        "n_unique_prompts": len(ALL_PROMPTS),
        "mitosis_config": {
            "max_cells": max_cells, "split_patience": 3, "split_noise": 0.10,
            "merge_threshold": 0.005, "merge_patience": 30, "min_cells": 2,
            "lorenz_scale": 0.05,
        },
        "trained": {
            "seed": TRAINED_PROMPT_SEED,
            "elapsed_sec": trained_traj["elapsed_sec"],
            "final_n_cells": trained_traj["final_n_cells"],
            "n_splits": trained_traj["n_splits"],
            "n_merges": trained_traj["n_merges"],
            "cap_bound_turns": trained_traj["cap_bound_turns"],
            "snapshots": trained_traj["snapshots"],
            "final_phi_iit_unnorm_b16": t_phi_un,
            "final_phi_iit_norm_b16": t_phi_n,
            "final_proxy_phi": t_proxy,
            "alpha_proxy": a_proxy_t,
            "alpha_iit_norm_b16": a_norm_t,
            "alpha_iit_unnorm_b16": a_unnorm_t,
        },
        "v14_indep_mirror_5seed": [
            {
                "seed": sd_seed,
                "elapsed_sec": m["elapsed_sec"],
                "final_n_cells": m["final_n_cells"],
                "n_splits": m["n_splits"],
                "n_merges": m["n_merges"],
                "cap_bound_turns": m["cap_bound_turns"],
                "snapshots": m["snapshots"],
                "final_phi_iit_unnorm_b16": m["snapshots"][-1]["iit_phi_unnorm_b16"],
                "final_phi_iit_norm_b16": m["snapshots"][-1]["iit_phi_norm_b16"],
                "final_proxy_phi": m["snapshots"][-1]["proxy_phi"],
                "alpha_proxy": ap_, "alpha_iit_norm_b16": an_, "alpha_iit_unnorm_b16": au_,
            }
            for m, sd_seed, ap_, an_, au_ in zip(
                mirror_trajs, INDEP_SEEDS, a_proxy_r, a_norm_r, a_unnorm_r
            )
        ],
        "verdict": {
            "verdict": verdict,
            "n_trained_beats_phi": n_trained_beats_phi,
            "n_trained_loses_phi": n_trained_loses_phi,
            "n_trained_ties_phi": n_trained_ties_phi,
            "frac_beats": frac_beats,
            "sign_test_p_two_sided": sign_p,
            "mann_whitney": mwu,
            "trained": {
                "phi_iit_unnorm_b16": t_phi_un,
                "phi_iit_norm_b16": t_phi_n,
                "n_cells": t_cells,
                "n_splits": t_splits,
                "cap_bound_turns": t_cap_bound,
            },
            "random_phi_iit_unnorm_b16": {
                "min": float(min(rs_phi_un)), "median": float(median_phi),
                "max": float(max(rs_phi_un)), "all": rs_phi_un,
            },
            "random_n_cells": {
                "min": int(min(rs_cells)), "median": int(median_cells),
                "max": int(max(rs_cells)), "all": rs_cells,
            },
            "random_n_splits": rs_splits,
            "random_cap_bound_turns": rs_cap_bound,
            "cap_bound_universal": cap_bound_universal,
            "trained_cells_lt_random": n_trained_cells_lt_random,
            "trained_cells_gt_random": n_trained_cells_gt_random,
            "falsifier_status": falsifier_status,
        },
        "comparison_to_38": {
            "§38_trained_phi": s38_trained_phi,
            "§38_trained_cells": s38_trained_cells,
            "§38_random_max_phi": s38_random_phi_max,
            "§38_random_med_phi": s38_random_phi_med,
            "this_trained_phi": t_phi_un,
            "this_trained_cells": t_cells,
            "this_random_max_phi": max(rs_phi_un),
            "this_random_med_phi": median_phi,
            "trained_phi_match_2pct": trained_repro_match,
            "trained_cells_match_exact": (t_cells == s38_trained_cells),
        },
        "dynamic_range_trained": {
            "proxy": dr_proxy,
            "iit_phi_norm_b16": dr_norm,
            "iit_phi_unnorm_b16": dr_unnorm,
        },
        "honest_c3": [
            "Real Phase 2 350M Engine A/G ckpt (298.76M unique params; GQA-shared K/V — 'nominal 350M' rounded). cell_pool_init starts (16, 64); MitosisV5Engine wraps it with max_cells=128 cap (identical to §38). raw#15 honored: ckpt unmodified (sha256 verified pre-run).",
            "Byte-hash mod 32000 prompt encoding — NOT real BPE tokenizer. Trained and 5 random_init mirror seeds use identical encoding for fairness; absolute Φ values therefore have no semantic claim, only relative comparison (trained vs each random) is valid.",
            "MitosisV5Engine §30 all-fix in force across ALL 6 trajectories (A1 dispersion-trigger top-quartile + A2 per-cell adaptive threshold mean+1.5σ over 100-step window + B1 phi_per_cell ratchet + D1 Lorenz auto-calibration). Verified by source grep + smoke crossref; mtime 2026-05-10 12:02 (post-fix, pre-§38 run).",
            "Trained @ prompt_seed=42 (deterministic ckpt → one shot, identical to §38 trained run). Random mirror runs 5 INDEPENDENT prime seeds [11,13,17,19,23] — set-disjoint with both §33 V4_SEEDS [42,137,271,314,1729] and §38 V14_STRICT_SEEDS [42,137,271,314,1729,2718,3141,5772,6022,9192]. This eliminates V4_SEEDS contamination as a confound for the §38 strict pass.",
            "5-seed sign-test exact p-values: 5/5 → 0.0625 (two-sided); 4/5 → 0.375; 3/5 → 1.000. STRICT_PASS_INDEPENDENT_REPRODUCE thus has p=0.0625 — directional but underpowered relative to §38's 10-seed p=0.002. Read as REPLICATION evidence, not as standalone discovery.",
            "max_cells=128 (identical to §38). cap_bound_turns reported per trajectory — F-PHASE2-REPRODUCE-3 fires only if cap is universally hit (>90% of turns) on every run; otherwise the bound is non-binding and the cell-count discrim is informative.",
            "IIT MIP: spectral Fiedler approximation (NOT canonical PyPhi). 16-bin histogram MI on 64-dim cell vectors is COARSE. Useful for trained-vs-random differentiation only; not for absolute IIT magnitude. Identical to §33+§38 metric stack for parity.",
            "Lorenz autonomous chaos lorenz_scale=0.05 base, D1 auto-calibrated by mean L2-norm of cells, identical scale across all 6 trajectories. RNG resets per seed but injection magnitude is constant. Differential between trained/random flows ONLY through the h_to_c learned projection of hidden_mean → cell_input.",
            "ctx_T=16 tokens per forward (training was T=1024); under-samples substrate's full context-conditioned reactivity. Held constant across trajectories for fairness. Same caveat as §33+§38.",
            "Sign test (binomial) is the primary statistic since the comparison is paired-by-prompt-stream and only random-init differs. Mann-Whitney U with n1=1, n2=5 reduces to rank-of-trained-in-pool — reported as auxiliary; with 6 pooled values the maximum rank is 6 → minimum p_two_sided = 2/6 = 0.333.",
            "Trained run is deterministic given the same ckpt + prompt-stream seed → THIS run's trained Φ should match §38's 5244.07 exactly (within float-roundoff). This is a sanity check for environmental drift, NOT a strict pass criterion. cells should also match §38's 85.",
            "Verdict bins (STRICT_PASS_INDEPENDENT_REPRODUCE / PARTIAL_REPRODUCE / FRAGILE_REPRODUCE) are pre-registered in spec.md before run. The 3-bin mapping is data-driven (count of beats); no post-hoc adjustment.",
        ],
    }
    out_path = THIS_DIR / "result.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    log(f"\nresult.json: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")

    # ─── verdict.md ───
    vmd = THIS_DIR / "verdict.md"
    vmd.write_text(_render_verdict_md(result))
    log(f"verdict.md: {vmd}")

    # ─── plot ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(13, 9))
        ts_t = [s["turn"] for s in trained_traj["snapshots"]]
        cs_t = [s["n_cells"] for s in trained_traj["snapshots"]]
        un_t = [s["iit_phi_unnorm_b16"] for s in trained_traj["snapshots"]]
        pn_t = [s["iit_phi_norm_b16"] for s in trained_traj["snapshots"]]
        px_t = [s["proxy_phi"] for s in trained_traj["snapshots"]]

        ax = axes[0, 0]
        ax.plot(ts_t, cs_t, "b-", linewidth=2, label="trained 350M")
        for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            cs = [s["n_cells"] for s in m["snapshots"]]
            ax.plot(ts, cs, "--", linewidth=1, alpha=0.7, label=f"prime s={sd_seed}")
        ax.set_xlabel("turn"); ax.set_ylabel("n_cells")
        ax.set_title("V14 indep mirror — n_cells")
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        ax.plot(ts_t, un_t, "b-", linewidth=2, label="trained")
        for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            un = [s["iit_phi_unnorm_b16"] for s in m["snapshots"]]
            ax.plot(ts, un, "--", linewidth=1, alpha=0.7, label=f"s={sd_seed}")
        ax.set_xlabel("turn"); ax.set_ylabel("IIT Φ unnorm 16-bin")
        ax.set_title(f"IIT Φ unnorm — verdict={verdict}")
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        ax.plot(ts_t, pn_t, "b-", linewidth=2, label="trained")
        for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            pn = [s["iit_phi_norm_b16"] for s in m["snapshots"]]
            ax.plot(ts, pn, "--", linewidth=1, alpha=0.7, label=f"s={sd_seed}")
        ax.set_xlabel("turn"); ax.set_ylabel("IIT Φ norm 16-bin")
        ax.set_title("IIT Φ normalized")
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        ax = axes[1, 1]
        ax.plot(ts_t, px_t, "b-", linewidth=2, label="trained")
        for m, sd_seed in zip(mirror_trajs, INDEP_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            px = [s["proxy_phi"] for s in m["snapshots"]]
            ax.plot(ts, px, "--", linewidth=1, alpha=0.7, label=f"s={sd_seed}")
        ax.set_xlabel("turn"); ax.set_ylabel("proxy Φ")
        ax.set_title("proxy Φ (cosine·log(n+1))")
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(THIS_DIR / "indep_reproduce_comparison.png", dpi=80)
        plt.close(fig)
        log(f"plot: {THIS_DIR / 'indep_reproduce_comparison.png'}")
    except Exception as e:
        log(f"matplotlib skip: {e}")

    log_f.close()
    return result


def _render_verdict_md(result: dict) -> str:
    v = result["verdict"]
    t = v["trained"]
    seeds = result["indep_seeds"]
    mirrors = result["v14_indep_mirror_5seed"]
    cmp38 = result["comparison_to_38"]
    fix = result["fix_status"]

    lines = []
    lines.append("# BG-PHASE2-MAX128-§30FIX-RETEST — independent V14 strict reproduce")
    lines.append("")
    lines.append(f"**Verdict**: `{v['verdict']}`")
    lines.append("")
    lines.append("## Setup")
    lines.append(f"- Real Phase 2 350M ckpt (298.76M params), {result['n_turns']} turns, max_cells={result['max_cells']}")
    lines.append(f"- Trained: prompt_seed=42 (deterministic given ckpt + prompt stream)")
    lines.append(f"- Independent prime mirror seeds (n=5): {seeds}")
    lines.append(f"- Disjoint with §38 V14_STRICT_SEEDS: {result['seeds_38_disjoint_check']['disjoint_38']}")
    lines.append(f"- Disjoint with §33 V4_SEEDS: {result['seeds_38_disjoint_check']['disjoint_33']}")
    lines.append(f"- Primary metric: IIT Φ unnormalized 16-bin (Fiedler MIP, byte-hash prompts)")
    lines.append("")
    lines.append("## §30 fix activation (F-PHASE2-REPRODUCE-1)")
    lines.append(f"- All-active: **{fix['all_active']}** ({sum(fix['markers'].values())}/{len(fix['markers'])} markers)")
    for k, vv in fix["markers"].items():
        lines.append(f"  - {k}: {vv}")
    if fix.get("smoke_crossref"):
        lines.append(f"- Smoke crossref (post-fix): {fix['smoke_crossref']}")
    lines.append("")
    lines.append("## Final Φ_iit_un16 + n_cells per run")
    lines.append("")
    lines.append("| run | seed | n_cells | n_splits | cap_bound | Φ_iit_un16 | Φ_iit_n16 | proxy |")
    lines.append("|---|---|---|---|---|---|---|---|")
    lines.append(f"| trained | 42 | {t['n_cells']} | {t['n_splits']} | {t['cap_bound_turns']} | "
                 f"{t['phi_iit_unnorm_b16']:.2f} | "
                 f"{result['trained']['final_phi_iit_norm_b16']:.4f} | "
                 f"{result['trained']['final_proxy_phi']:.4f} |")
    for m in mirrors:
        lines.append(f"| mirror | {m['seed']} | {m['final_n_cells']} | {m['n_splits']} | "
                     f"{m['cap_bound_turns']} | "
                     f"{m['final_phi_iit_unnorm_b16']:.2f} | "
                     f"{m['final_phi_iit_norm_b16']:.4f} | "
                     f"{m['final_proxy_phi']:.4f} |")
    lines.append("")
    lines.append("## 5-seed aggregate")
    lines.append(f"- trained beats random Φ: {v['n_trained_beats_phi']}/{result['indep_seeds'].__len__()} "
                 f"(ties={v['n_trained_ties_phi']}, losses={v['n_trained_loses_phi']})")
    lines.append(f"- sign-test p (two-sided): {v['sign_test_p_two_sided']:.4f}")
    lines.append(f"- Mann-Whitney 1-vs-{v['mann_whitney']['n_random']}: U={v['mann_whitney']['u']}, "
                 f"rank={v['mann_whitney']['rank_in_pool']}/{v['mann_whitney']['n_random']+1}, "
                 f"p_one_sided={v['mann_whitney']['p_one_sided']:.4f}, "
                 f"p_two_sided={v['mann_whitney']['p_two_sided']:.4f}")
    lines.append(f"- random Φ_iit_un16: min={v['random_phi_iit_unnorm_b16']['min']:.2f} "
                 f"med={v['random_phi_iit_unnorm_b16']['median']:.2f} "
                 f"max={v['random_phi_iit_unnorm_b16']['max']:.2f}")
    lines.append(f"- random n_cells: min={v['random_n_cells']['min']} "
                 f"med={v['random_n_cells']['median']} "
                 f"max={v['random_n_cells']['max']}")
    lines.append(f"- random n_splits: {v['random_n_splits']}")
    lines.append(f"- random cap_bound_turns: {v['random_cap_bound_turns']}")
    lines.append(f"- cap_bound_universal (F-PHASE2-REPRODUCE-3): {v['cap_bound_universal']}")
    lines.append(f"- cell_count discrim: trained<rand={v['trained_cells_lt_random']}/{result['indep_seeds'].__len__()}, "
                 f"trained>rand={v['trained_cells_gt_random']}/{result['indep_seeds'].__len__()}")
    lines.append("")
    lines.append("## §38 cross-comparison (replication of trained run)")
    lines.append(f"- §38 trained: Φ={cmp38['§38_trained_phi']}, cells={cmp38['§38_trained_cells']}")
    lines.append(f"- THIS trained: Φ={cmp38['this_trained_phi']:.2f}, cells={cmp38['this_trained_cells']}")
    lines.append(f"- trained Φ matches §38 within 2%: **{cmp38['trained_phi_match_2pct']}**")
    lines.append(f"- trained cells matches §38 exact: **{cmp38['trained_cells_match_exact']}**")
    lines.append(f"- §38 random max Φ: {cmp38['§38_random_max_phi']}, this random max Φ: {cmp38['this_random_max_phi']:.2f}")
    lines.append("")
    lines.append("## Falsifier status")
    for k, vv in v["falsifier_status"].items():
        lines.append(f"- {k}: **{vv}**")
    lines.append("")
    lines.append("## Verdict bins (pre-registered)")
    lines.append("- **V14_STRICT_PASS_INDEPENDENT_REPRODUCE**: trained > ALL 5 random Φ → §38 strengthened, ★★★★ pathway")
    lines.append("- **V14_PARTIAL_REPRODUCE**: trained > 3-4/5 random Φ → directional but not strict")
    lines.append("- **V14_FRAGILE_REPRODUCE**: trained > 0-2/5 random Φ → §38 V4_SEEDS contamination plausible")
    lines.append("")
    lines.append("## Honest C3")
    for i, c in enumerate(result["honest_c3"], 1):
        lines.append(f"{i}. {c}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else N_TURNS
    main(n_turns=n_turns)
