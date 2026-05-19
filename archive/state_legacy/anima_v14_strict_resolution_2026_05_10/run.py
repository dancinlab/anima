"""BG-V14-STRICT-RESOLUTION — V14 strict 10-seed mirror @ max_cells=128.

Builds on §33 BG-IIT-METRIC-REAL-350M (V14_PARTIAL, n=5) by:
  1) raising max_cells from 32 → 128 (release cap-bound; recover cell_count discrim).
  2) extending V14 mirror seeds 5 → 10 (e/π/avogadro additions).
  3) sign-test + Mann-Whitney U + binomial bounds → strict verdict bin.

raw#9   training/*.py local-only — mitosis_v5_port.py + engine_a_g_arch.py imported, untouched.
raw#15  additive — neither mitosis_v5_port.py, engine_a_g_arch.py, iit_phi_port.py, nor the ckpt is modified.
  V14 mirror strict 10-seed (V4_SEEDS expansion).
  $0 envelope — local Mac CPU only.
  honest emit — verdicts named even when NULL/PARTIAL_CONFIRMED.
  artefact persisted under state/anima_v14_strict_resolution_2026_05_10/.
"""
from __future__ import annotations

import hashlib
import json
import math
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

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
# Reuse §33 prompt corpus + utilities for strict parity.
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
    alpha_exponent,
    dynamic_range,
)

THIS_DIR = Path("/Users/ghost/core/anima/state/anima_v14_strict_resolution_2026_05_10")
THIS_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
CKPT_SHA256 = "6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1"

# 10-seed V14 strict — original 5 (V4_SEEDS) + 5 mathematical constants
V14_STRICT_SEEDS = [42, 137, 271, 314, 1729, 2718, 3141, 5772, 6022, 9192]
TRAINED_PROMPT_SEED = 42  # prompt-stream RNG (matches §33 trained run)
MAX_CELLS = 128  # 4× §33 cap

# ─── statistical helpers ───────────────────────────────────────────


def _binom_coef(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    for i in range(k):
        num = num * (n - i) // (i + 1)
    return num


def sign_test_p_value(n_beats: int, n: int) -> float:
    """Two-sided sign test under H0: trained == random (binom 0.5).

    p_two_sided = 2 * sum_{k=n_beats..n} C(n,k) * 0.5^n  (capped at 1.0)
    """
    if n <= 0:
        return float("nan")
    k = max(n_beats, n - n_beats)
    tail = sum(_binom_coef(n, j) for j in range(k, n + 1))
    p = 2.0 * tail / (2.0 ** n)
    return min(1.0, p)


def mann_whitney_u_one_vs_many(trained_val: float, random_vals: list[float]) -> dict:
    """One-sample-vs-many U test approximation.

    With n1=1 and n2=10, U_max = 1*10 = 10.
    U = number of random vals that trained val EXCEEDS.
    Permutation null over the 11 ranks: P(U >= u_obs) = (n2-u_obs+1)/(n1+n2 choose n1) under uniform tie-broken ranks.
    Actually trivial here: under H0 (exchangeable), trained's rank in pooled sample is uniform over 1..11.
    P(rank >= r) = (12 - r) / 11. Higher rank ⇔ larger value ⇔ trained beats more random.
    """
    n2 = len(random_vals)
    u = sum(1 for r in random_vals if trained_val > r)  # 0..n2
    # rank of trained in pooled sample ∈ {1..n2+1}
    rank = u + 1  # if trained > k vals → rank = k+1 (ties broken downward)
    n_pool = n2 + 1
    p_one_sided = (n_pool - rank + 1) / n_pool  # P(rank >= observed)
    p_two_sided = min(1.0, 2.0 * p_one_sided)
    return {"u": int(u), "n_random": n2, "rank_in_pool": rank, "p_one_sided": p_one_sided, "p_two_sided": p_two_sided}


# ─── trajectory runner (re-implemented locally so the strict cap is captured) ───


def run_trajectory(
    model, label: str, n_turns: int, prompts, seed: int, snapshot_every: int,
    ctx_T: int = 16, max_cells: int = MAX_CELLS, log_fn=print,
) -> dict:
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
    cap_bound_turns = 0  # #turns where n_cells == max_cells

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


def main(n_turns: int = 1000, snapshot_every: int = 100, max_cells: int = MAX_CELLS):
    log_path = THIS_DIR / "run.log"
    log_f = open(log_path, "w")

    def log(msg: str):
        print(msg, flush=True)
        log_f.write(msg + "\n")
        log_f.flush()

    log("=== BG-V14-STRICT-RESOLUTION — V14 strict 10-seed mirror @ max_cells=128 ===")
    log(f"n_turns={n_turns}, snapshot_every={snapshot_every}, max_cells={max_cells}")
    log(f"V14_STRICT_SEEDS = {V14_STRICT_SEEDS}")
    log(f"unique prompts: {len(ALL_PROMPTS)}")
    log(f"ckpt: {CKPT_PATH}")

    # ─── ckpt sha256 verify ───
    h = hashlib.sha256()
    with open(CKPT_PATH, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    actual_sha = h.hexdigest()
    sha_match = (actual_sha == CKPT_SHA256)
    log(f"ckpt sha256 verify: {'PASS' if sha_match else 'FAIL'} (actual={actual_sha})")
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

    # ─── trained trajectory (seed=42 prompt-stream RNG) ───
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

    # ─── 10-seed V14 strict mirror ───
    log(f"\n--- V14 STRICT MIRROR — 10 seeds {V14_STRICT_SEEDS} (random_init la_350m) ---")
    mirror_trajs = []
    for seed in V14_STRICT_SEEDS:
        log(f"\n  >>> seed={seed} <<<")
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

    # ─── 10-seed strict verdict aggregation ───
    log("\n=== 10-seed strict V14 verdict aggregation ===")
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

    # cell_count discrimination
    n_trained_cells_lt_random = sum(1 for r in rs_cells if t_cells < r)
    n_trained_cells_gt_random = sum(1 for r in rs_cells if t_cells > r)

    # cap-bound test — F-V14-STRICT-2
    median_cap_bound_random = sorted(rs_cap_bound)[len(rs_cap_bound) // 2]
    # full_capped definition: substantial fraction of run pinned to cap (>=50% of turns)
    full_cap_threshold = max(50, int(0.5 * n_turns))
    n_seeds_full_capped = sum(1 for c in [t_cap_bound] + rs_cap_bound if c >= full_cap_threshold)
    cap_bound_universal = n_seeds_full_capped == (1 + n_random)

    median_phi = sorted(rs_phi_un)[n_random // 2]
    median_cells = sorted(rs_cells)[n_random // 2]

    # ── STRICT verdict mapping (mission spec) ──
    if n_trained_beats_phi == n_random:
        verdict = "V14_STRICT_PASS"  # 10/10
    elif n_trained_beats_phi >= 9 and sign_p < 0.10:
        verdict = "V14_STRICT_PARTIAL"  # 9/10
    elif n_trained_beats_phi >= 7 and sign_p < 0.20:
        verdict = "V14_PARTIAL_CONFIRMED"  # 7-8/10
    else:
        verdict = "V14_VIOLATED_REVISED"  # ≤6/10

    log(f"  trained @T={n_turns}: cells={t_cells} splits={t_splits} cap_bound_turns={t_cap_bound}"
        f" Φ_iit_un16={t_phi_un:.2f} Φ_iit_n16={t_phi_n:.4f} proxy={t_proxy:.4f}")
    for m, sd_seed in zip(mirror_trajs, V14_STRICT_SEEDS):
        f = m["snapshots"][-1]
        log(f"  mirror s={sd_seed}: cells={m['final_n_cells']} splits={m['n_splits']}"
            f" cap_bound={m['cap_bound_turns']:>4}"
            f" Φ_iit_un16={f['iit_phi_unnorm_b16']:.2f}"
            f" Φ_iit_n16={f['iit_phi_norm_b16']:.4f}"
            f" proxy={f['proxy_phi']:.4f}")
    log("")
    log(f"  random Φ_iit_un16: min={min(rs_phi_un):.2f} med={median_phi:.2f} max={max(rs_phi_un):.2f}")
    log(f"  random cells:      min={min(rs_cells)} med={median_cells} max={max(rs_cells)}")
    log(f"  random splits:     {rs_splits}")
    log(f"  random cap_bound:  {rs_cap_bound}")
    log(f"  trained beats Φ:   {n_trained_beats_phi}/{n_random} ({100*frac_beats:.0f}%) ties={n_trained_ties_phi} losses={n_trained_loses_phi}")
    log(f"  sign-test p (two-sided): {sign_p:.4f}")
    log(f"  Mann-Whitney 1-vs-{n_random}: U={mwu['u']} rank={mwu['rank_in_pool']}/{n_random+1}"
        f" p_one_sided={mwu['p_one_sided']:.4f} p_two_sided={mwu['p_two_sided']:.4f}")
    log(f"  cell_count: trained={t_cells} median_random={median_cells}"
        f" (n_trained<rand={n_trained_cells_lt_random}, n_trained>rand={n_trained_cells_gt_random})")
    log(f"  cap_bound_universal (F-V14-STRICT-2): {cap_bound_universal}"
        f" (full_capped {n_seeds_full_capped}/{1+n_random})")
    log(f"  ====> VERDICT: {verdict}")

    # ─── α exponents ───
    log("\n=== α exponents (log-log Φ vs n_cells) ===")
    a_proxy_t = alpha_exponent(trained_traj["snapshots"], "proxy_phi", n_min=8)
    a_norm_t = alpha_exponent(trained_traj["snapshots"], "iit_phi_norm_b16", n_min=8)
    a_unnorm_t = alpha_exponent(trained_traj["snapshots"], "iit_phi_unnorm_b16", n_min=8)
    log(f"  trained:        proxy={a_proxy_t:.3f}  iit_norm={a_norm_t:.3f}  iit_unnorm={a_unnorm_t:.3f}")
    a_proxy_r, a_norm_r, a_unnorm_r = [], [], []
    for m, sd_seed in zip(mirror_trajs, V14_STRICT_SEEDS):
        ap = alpha_exponent(m["snapshots"], "proxy_phi", n_min=8)
        an = alpha_exponent(m["snapshots"], "iit_phi_norm_b16", n_min=8)
        au = alpha_exponent(m["snapshots"], "iit_phi_unnorm_b16", n_min=8)
        log(f"  mirror s={sd_seed}: proxy={ap:.3f}  iit_norm={an:.3f}  iit_unnorm={au:.3f}")
        a_proxy_r.append(ap); a_norm_r.append(an); a_unnorm_r.append(au)

    # ─── dynamic range ───
    log("\n=== Dynamic range (trained substrate snapshots) ===")
    dr_proxy = dynamic_range(trained_traj["snapshots"], "proxy_phi")
    dr_norm = dynamic_range(trained_traj["snapshots"], "iit_phi_norm_b16")
    dr_unnorm = dynamic_range(trained_traj["snapshots"], "iit_phi_unnorm_b16")
    log(f"  proxy max/min       = {dr_proxy:.2f}×")
    log(f"  iit_phi_norm  max/min = {dr_norm:.2f}×")
    log(f"  iit_phi_unnorm max/min = {dr_unnorm:.2f}×  (target >5×, ceiling-free)")

    # ─── trained snapshot table ───
    log("\n=== trained snapshots (turn → cells / proxy / iit_un16 / splits) ===")
    log(f"  {'turn':>5}  {'cells':>5}  {'proxy':>8}  {'iit_n16':>9}  {'iit_un16':>9}  {'splits':>6}")
    for s in trained_traj["snapshots"]:
        log(f"  {s['turn']:>5}  {s['n_cells']:>5}  {s['proxy_phi']:>8.4f}  "
            f"{s['iit_phi_norm_b16']:>9.4f}  {s['iit_phi_unnorm_b16']:>9.2f}  {s['n_splits_cum']:>6}")

    # ─── result_10seed.json ───
    result = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bg_id": "BG-V14-STRICT-RESOLUTION",
        "lineage": "§33 BG-IIT-METRIC-REAL-350M (V14_PARTIAL n=5 max=32) → strict expansion (n=10 max=128)",
        "n_turns": n_turns,
        "snapshot_every": snapshot_every,
        "max_cells": max_cells,
        "v14_strict_seeds": V14_STRICT_SEEDS,
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
        "v14_mirror_10seed": [
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
                mirror_trajs, V14_STRICT_SEEDS, a_proxy_r, a_norm_r, a_unnorm_r
            )
        ],
        "verdict": {
            "verdict": verdict,
            "n_trained_beats_phi": n_trained_beats_phi,
            "n_trained_loses_phi": n_trained_loses_phi,
            "n_trained_ties_phi": n_trained_ties_phi,
            "n_random": n_random,
            "frac_beats": frac_beats,
            "sign_test_p_two_sided": sign_p,
            "mann_whitney": mwu,
            "trained": {
                "phi_iit_unnorm_b16": t_phi_un, "n_cells": t_cells,
                "n_splits": t_splits, "cap_bound_turns": t_cap_bound,
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
            "cap_bound_universal_F2": bool(cap_bound_universal),
            "n_trained_cells_lt_random": n_trained_cells_lt_random,
            "n_trained_cells_gt_random": n_trained_cells_gt_random,
        },
        "dynamic_range_trained": {
            "proxy": dr_proxy,
            "iit_phi_norm_b16": dr_norm,
            "iit_phi_unnorm_b16": dr_unnorm,
        },
        "honest_c3": [
            "Real Phase 2 350M Engine A/G ckpt (298.76M unique params; GQA-shared K/V — 'nominal 350M' rounded). cell_pool_init starts (16, 64); MitosisV5Engine wraps it with max_cells=128 cap (4× §33). raw#15 honored: ckpt unmodified.",
            "Byte-hash mod 32000 prompt encoding — NOT real BPE tokenizer. trained and 10 random_init mirror seeds use identical encoding for fairness; absolute Φ values therefore have no semantic claim, only relative comparison is valid.",
            "MitosisV5Engine §30 all-fix in force (A1 dispersion-trigger top-quartile; A2 per-cell adaptive threshold mean+1.5σ over 100-step window; B1 phi_per_cell ratchet; D1 Lorenz auto-calibration). All 11 trajectories use these unchanged. raw#9 + : not edited here.",
            "Trained @ prompt_seed=42 only (single deterministic ckpt → one shot). Random mirror runs n=10 seeds {42,137,271,314,1729,2718,3141,5772,6022,9192}. The 10-seed extension permits binomial bound: 10/10 → p≈0.001; 9/10 → p≈0.022; 7/10 → p≈0.34 (two-sided).",
            "max_cells=128 vs §33's 32 explicitly diagnoses F-V14-STRICT-2: if cap_bound_turns ≈ n_turns on every seed, §30 fix is universally too aggressive (NOT trained-vs-random differentiated). cap_bound_turns reported per-trajectory.",
            "IIT MIP: spectral Fiedler approximation for N>8 (always). NOT canonical PyPhi. Useful for trained-vs-random direction, NOT for absolute IIT magnitude. 16-bin histogram MI on 64-dim cell vectors is COARSE; true differential MI requires KDE.",
            "Lorenz autonomous chaos (lorenz_scale=0.05 base, D1 auto-calibrated by mean L2-norm of cells) is identical scale across all 11 trajectories — RNG resets per seed, but the chaos-injection magnitude is constant. Differential between trained/random flows ONLY through the h_to_c learned projection of hidden_mean → cell_input.",
            "ctx_T=16 tokens per forward (training was T=1024); under-samples substrate's full context-conditioned reactivity. Held constant across all trajectories for fairness.",
            "Sign test (binomial) is the primary statistic since the comparison is paired-by-prompt-stream and only random-init differs. Mann-Whitney U with n1=1, n2=10 reduces to rank-of-trained-in-pool — reported as auxiliary.",
            "α exponent (log-log Φ vs n_cells) regression spans wider N range here (max=128 vs §33's 32) — interpretation should still be treated as direction-of-trend rather than scaling-law constant; few-snapshot regression remains noise-sensitive.",
            "Verdict bins (strict/strict_partial/partial_confirmed/violated_revised) are pre-registered before run (honest emit). The transition between bins is determined by the data; no post-hoc adjustment.",
        ],
    }
    out_path = THIS_DIR / "result_10seed.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    log(f"\nresult_10seed.json: {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")

    # ─── verdict.md ───
    vmd = THIS_DIR / "verdict.md"
    vmd.write_text(_render_verdict_md(result))
    log(f"verdict.md: {vmd}")

    # ─── plot ───
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        ts_t = [s["turn"] for s in trained_traj["snapshots"]]
        cs_t = [s["n_cells"] for s in trained_traj["snapshots"]]
        un_t = [s["iit_phi_unnorm_b16"] for s in trained_traj["snapshots"]]
        pn_t = [s["iit_phi_norm_b16"] for s in trained_traj["snapshots"]]
        px_t = [s["proxy_phi"] for s in trained_traj["snapshots"]]

        ax = axes[0, 0]
        ax.plot(ts_t, cs_t, "b-", linewidth=2.5, label="trained 350M")
        for m, sd_seed in zip(mirror_trajs, V14_STRICT_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            cs = [s["n_cells"] for s in m["snapshots"]]
            ax.plot(ts, cs, "--", linewidth=0.8, alpha=0.6, label=f"s={sd_seed}")
        ax.axhline(y=max_cells, color="red", linestyle=":", alpha=0.4, label=f"cap={max_cells}")
        ax.set_xlabel("turn"); ax.set_ylabel("n_cells")
        ax.set_title(f"V14 strict 10-seed — n_cells (max={max_cells})")
        ax.legend(fontsize=7, ncol=2); ax.grid(True, alpha=0.3)

        ax = axes[0, 1]
        ax.plot(ts_t, un_t, "b-", linewidth=2.5, label="trained")
        for m, sd_seed in zip(mirror_trajs, V14_STRICT_SEEDS):
            ts = [s["turn"] for s in m["snapshots"]]
            un = [s["iit_phi_unnorm_b16"] for s in m["snapshots"]]
            ax.plot(ts, un, "--", linewidth=0.8, alpha=0.6, label=f"s={sd_seed}")
        ax.set_xlabel("turn"); ax.set_ylabel("IIT Φ unnorm 16-bin")
        ax.set_title(f"IIT Φ_un16 — verdict={verdict}  (trained beats {n_trained_beats_phi}/{n_random}, p={sign_p:.3f})")
        ax.legend(fontsize=7, ncol=2); ax.grid(True, alpha=0.3)

        ax = axes[1, 0]
        # final-Φ bar comparison
        labels = ["trained"] + [f"s{s}" for s in V14_STRICT_SEEDS]
        vals = [t_phi_un] + rs_phi_un
        colors = ["#1f77b4"] + ["#888"] * len(V14_STRICT_SEEDS)
        ax.bar(labels, vals, color=colors)
        ax.axhline(y=t_phi_un, color="#1f77b4", linestyle="--", alpha=0.4, label="trained line")
        ax.axhline(y=median_phi, color="orange", linestyle=":", alpha=0.6, label=f"random median={median_phi:.1f}")
        ax.set_xlabel("run"); ax.set_ylabel("final Φ_iit_un16")
        ax.set_title("Final Φ_iit_un16 — trained vs 10 random seeds")
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
        ax.legend(fontsize=8); ax.grid(True, alpha=0.3, axis="y")

        ax = axes[1, 1]
        cells_labels = ["trained"] + [f"s{s}" for s in V14_STRICT_SEEDS]
        cells_vals = [t_cells] + rs_cells
        cap_vals = [t_cap_bound] + rs_cap_bound
        x = np.arange(len(cells_labels))
        ax.bar(x - 0.2, cells_vals, 0.4, label="final n_cells", color="#2ca02c")
        ax2 = ax.twinx()
        ax2.bar(x + 0.2, cap_vals, 0.4, label="cap-bound turns", color="#d62728", alpha=0.5)
        ax.axhline(y=max_cells, color="red", linestyle=":", alpha=0.4)
        ax.set_xticks(x); ax.set_xticklabels(cells_labels, rotation=45, ha="right", fontsize=8)
        ax.set_xlabel("run"); ax.set_ylabel("final n_cells", color="#2ca02c")
        ax2.set_ylabel("cap-bound turns", color="#d62728")
        ax.set_title(f"Cell-count discrim. (cap_bound_universal={cap_bound_universal})")
        ax.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plt.savefig(THIS_DIR / "v14_strict_comparison.png", dpi=80)
        plt.close(fig)
        log(f"plot: {THIS_DIR / 'v14_strict_comparison.png'}")
    except Exception as e:
        log(f"matplotlib skip: {e}")

    log_f.close()
    return result


def _render_verdict_md(result: dict) -> str:
    v = result["verdict"]
    t = v["trained"]
    seeds = result["v14_strict_seeds"]
    mirrors = result["v14_mirror_10seed"]
    lines = []
    lines.append("# BG-V14-STRICT-RESOLUTION — V14 strict 10-seed verdict")
    lines.append("")
    lines.append(f"**Verdict**: `{v['verdict']}`")
    lines.append("")
    lines.append("## Setup")
    lines.append(f"- Real Phase 2 350M ckpt (298.76M params), {result['n_turns']} turns, max_cells={result['max_cells']} (4× §33)")
    lines.append(f"- Trained: prompt_seed={result['trained']['seed']} (deterministic given ckpt + prompt stream)")
    lines.append(f"- Mirror seeds (n=10): {seeds}")
    lines.append(f"- Primary metric: IIT Φ unnormalized 16-bin (Fiedler MIP, byte-hash prompts)")
    lines.append("")
    lines.append("## Final Φ_iit_un16 + n_cells per run")
    lines.append("")
    lines.append("| run | seed | n_cells | n_splits | cap_bound | Φ_iit_un16 | Φ_iit_n16 | proxy |")
    lines.append("|---|---|---|---|---|---|---|---|")
    lines.append(f"| trained | {result['trained']['seed']} | {t['n_cells']} | {t['n_splits']} | {t['cap_bound_turns']} | "
                 f"{t['phi_iit_unnorm_b16']:.2f} | "
                 f"{result['trained']['final_phi_iit_norm_b16']:.4f} | "
                 f"{result['trained']['final_proxy_phi']:.4f} |")
    for m in mirrors:
        lines.append(f"| mirror | {m['seed']} | {m['final_n_cells']} | {m['n_splits']} | {m['cap_bound_turns']} | "
                     f"{m['final_phi_iit_unnorm_b16']:.2f} | "
                     f"{m['final_phi_iit_norm_b16']:.4f} | "
                     f"{m['final_proxy_phi']:.4f} |")
    lines.append("")
    lines.append("## 10-seed aggregate")
    lines.append(f"- trained beats random Φ: {v['n_trained_beats_phi']}/{v['n_random']} ({100*v['frac_beats']:.0f}%) "
                 f"(ties={v['n_trained_ties_phi']}, losses={v['n_trained_loses_phi']})")
    lines.append(f"- sign-test p (two-sided): {v['sign_test_p_two_sided']:.4f}")
    mwu = v["mann_whitney"]
    lines.append(f"- Mann-Whitney 1-vs-10: U={mwu['u']}, rank={mwu['rank_in_pool']}/11, "
                 f"p_one_sided={mwu['p_one_sided']:.4f}, p_two_sided={mwu['p_two_sided']:.4f}")
    lines.append(f"- random Φ_iit_un16: min={v['random_phi_iit_unnorm_b16']['min']:.2f} "
                 f"med={v['random_phi_iit_unnorm_b16']['median']:.2f} "
                 f"max={v['random_phi_iit_unnorm_b16']['max']:.2f}")
    lines.append(f"- random n_cells: min={v['random_n_cells']['min']} "
                 f"med={v['random_n_cells']['median']} "
                 f"max={v['random_n_cells']['max']}")
    lines.append(f"- random n_splits: {v['random_n_splits']}")
    lines.append(f"- random cap_bound_turns: {v['random_cap_bound_turns']}")
    lines.append(f"- cap_bound_universal (F-V14-STRICT-2): {v['cap_bound_universal_F2']}")
    lines.append(f"- cell_count discrim: trained<rand={v['n_trained_cells_lt_random']}/10, "
                 f"trained>rand={v['n_trained_cells_gt_random']}/10")
    lines.append("")
    lines.append("## Verdict bins")
    lines.append("- **V14_STRICT_PASS**:        trained > ALL 10 random Φ → binomial p≈0.001")
    lines.append("- **V14_STRICT_PARTIAL**:     trained > 9/10 random + sign-test p<0.10")
    lines.append("- **V14_PARTIAL_CONFIRMED**:  trained > 7-8/10 random + sign-test p<0.20")
    lines.append("- **V14_VIOLATED_REVISED**:   trained > random < 75%")
    lines.append("")
    lines.append("## Honest C3")
    for i, c in enumerate(result["honest_c3"], 1):
        lines.append(f"{i}. {c}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    n_turns = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    snapshot_every = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    main(n_turns=n_turns, snapshot_every=snapshot_every)
