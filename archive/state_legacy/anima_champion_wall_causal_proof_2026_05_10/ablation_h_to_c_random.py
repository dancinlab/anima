"""§28+§37 BG-CHAMPION-WALL-CAUSAL-PROOF — h_to_c random_init ablation.

Ablation: Phase 2 ckpt full-trained baseline vs h_to_c-only-randomized vs
3-seed full-random mirror. If champion-wall (formed in h_to_c during training)
is the CAUSE of V14 polarity, randomizing ONLY h_to_c should:
  (a) RESTORE Φ to random-mirror level (releases champion-wall bottleneck)
  (b) trained → VIOLATED → restored to PASS-ish (Φ rises toward mirror)
If h_to_c-randomized still shows trained-level Φ → champion-wall is NOT
the polarity cause (other weights drive it).

Budget: 200 turns × 5 trajectories × ~0.65s/turn = ~10 min on local CPU.
Snapshots every 50 turns. raw#15 read-only on shared modules; ckpt unmodified
on disk (we only mutate the in-memory copy of h_to_c.weight).

Falsifier:
  F-CHAMPION-WALL-2: if h_to_c-randomized Φ ≈ trained Φ (within noise band)
  AND remains < random-mirror Φ → champion-wall is NOT polarity cause.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v5_iit_phi_remetric_2026_05_10")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_iit_real_350m_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
)

OUT_DIR = Path("/Users/ghost/core/anima/state/anima_champion_wall_causal_proof_2026_05_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CKPT_PATH = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"

N_TURNS = 200
SNAPSHOT_EVERY = 50
MAX_CELLS = 128

# Limited mirror — 3 seeds for $0 envelope (full 10-seed already reported in §V14-STRICT)
ABLATION_MIRROR_SEEDS = [42, 137, 271]


def run_trajectory(model, label, n_turns, prompts, seed, snapshot_every, max_cells, log_fn=print):
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
            ids = encode_prompt_to_ids(prompt, T=16)
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
                    "iit_phi_unnorm_b16": phi_iit["spatial_phi_unnormalized"],
                    "iit_phi_norm_b16": phi_iit["spatial_phi"],
                    "n_splits_cum": int(n_splits),
                    "elapsed_sec": float(time.time() - t_start),
                }
                snapshots.append(snap)
                if time.time() - last_print > 8:
                    log_fn(
                        f"  [{label}] turn={turn:4d} cells={snap['n_cells']:3d} "
                        f"proxyΦ={snap['proxy_phi']:.4f} "
                        f"iit_un16={snap['iit_phi_unnorm_b16']:.2f} "
                        f"splits={n_splits} elapsed={snap['elapsed_sec']:.1f}s"
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


def load_trained_model() -> EngineAGModel:
    cfg = EngineAGConfig.phase2_cotrain_350m()
    ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    sd = ckpt["model"]
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    model = EngineAGModel(cfg)
    miss, unexp = model.load_state_dict(sd_fp32, strict=True)
    return model


def randomize_h_to_c_only(model: EngineAGModel, seed: int = 42) -> EngineAGModel:
    """Replace ONLY engine_g.h_to_c.weight with random init (init_std-Gaussian).

    Everything else stays trained: tok_emb, layers, lm_head, engine_g.cell_pool_init,
    engine_g.c_to_h. This isolates whether h_to_c-learned champion-wall is the
    polarity cause.
    """
    g = torch.Generator(device="cpu").manual_seed(seed)
    with torch.no_grad():
        W = model.engine_g.h_to_c.weight  # (c_dim=64, d_model=1024)
        # init_std=0.02 in EngineAGConfig
        nw = torch.empty_like(W)
        nw.normal_(mean=0.0, std=0.02, generator=g)
        W.copy_(nw)
    return model


def main() -> int:
    log_path = OUT_DIR / "ablation_run.log"
    log_f = open(log_path, "w")

    def log(m):
        print(m, flush=True)
        log_f.write(m + "\n")
        log_f.flush()

    log("=== BG-CHAMPION-WALL-CAUSAL-PROOF — h_to_c-only ablation ===")
    log(f"n_turns={N_TURNS} snapshot_every={SNAPSHOT_EVERY} max_cells={MAX_CELLS}")
    log(f"mirror seeds={ABLATION_MIRROR_SEEDS}")

    # ─── A) trained baseline ───
    log("\n--- A) trained 350M baseline ---")
    trained_model = load_trained_model()
    trained_traj = run_trajectory(
        trained_model, "trained", N_TURNS, ALL_PROMPTS, seed=42,
        snapshot_every=SNAPSHOT_EVERY, max_cells=MAX_CELLS, log_fn=log,
    )
    log(f"trained cells={trained_traj['final_n_cells']} splits={trained_traj['n_splits']} "
        f"final_iit={trained_traj['snapshots'][-1]['iit_phi_unnorm_b16']:.2f}")

    # ─── B) h_to_c-only randomized (3 seeds) ───
    log("\n--- B) h_to_c-randomized (3 seeds) ---")
    htc_trajs = []
    for seed in ABLATION_MIRROR_SEEDS:
        log(f"  >>> h_to_c randomized seed={seed} <<<")
        m = load_trained_model()
        m = randomize_h_to_c_only(m, seed=seed)
        traj = run_trajectory(
            m, f"htc_rand_s{seed}", N_TURNS, ALL_PROMPTS, seed=seed,
            snapshot_every=SNAPSHOT_EVERY, max_cells=MAX_CELLS, log_fn=log,
        )
        log(f"  htc_rand s={seed}: cells={traj['final_n_cells']} splits={traj['n_splits']} "
            f"final_iit={traj['snapshots'][-1]['iit_phi_unnorm_b16']:.2f}")
        htc_trajs.append(traj)
        del m

    # ─── C) full random_init (3 seeds) ───
    log("\n--- C) full random_init (3 seeds) ---")
    rand_trajs = []
    for seed in ABLATION_MIRROR_SEEDS:
        log(f"  >>> full random seed={seed} <<<")
        m = load_random_init(seed=seed, preset="la_350m")
        traj = run_trajectory(
            m, f"full_rand_s{seed}", N_TURNS, ALL_PROMPTS, seed=seed,
            snapshot_every=SNAPSHOT_EVERY, max_cells=MAX_CELLS, log_fn=log,
        )
        log(f"  full_rand s={seed}: cells={traj['final_n_cells']} splits={traj['n_splits']} "
            f"final_iit={traj['snapshots'][-1]['iit_phi_unnorm_b16']:.2f}")
        rand_trajs.append(traj)
        del m

    # ─── Aggregate verdict ───
    t_phi = trained_traj["snapshots"][-1]["iit_phi_unnorm_b16"]
    htc_phis = [t["snapshots"][-1]["iit_phi_unnorm_b16"] for t in htc_trajs]
    rand_phis = [t["snapshots"][-1]["iit_phi_unnorm_b16"] for t in rand_trajs]
    htc_mean = float(np.mean(htc_phis))
    htc_med = float(np.median(htc_phis))
    rand_mean = float(np.mean(rand_phis))
    rand_med = float(np.median(rand_phis))

    log("\n=== ABLATION VERDICT ===")
    log(f"trained Φ: {t_phi:.2f}")
    log(f"h_to_c-randomized Φ: {htc_phis} (mean={htc_mean:.2f} med={htc_med:.2f})")
    log(f"full random_init Φ: {rand_phis} (mean={rand_mean:.2f} med={rand_med:.2f})")

    # Hypothesis: if champion-wall causes V14 polarity, h_to_c randomization
    # should restore Φ toward random-mirror level (i.e., htc_med should be
    # CLOSER to rand_med than to t_phi).
    d_to_trained = abs(htc_med - t_phi)
    d_to_random = abs(htc_med - rand_med)
    closer_to_random = d_to_random < d_to_trained
    polarity_flipped = htc_med < rand_med * 0.95 and t_phi > rand_med  # if trained PASS, flipped means h_to_c matches random
    # Actually for Phase 2: trained > random (PASS). If htc_rand drops toward random, that's restoration.
    if t_phi > rand_med and htc_med < rand_med * 1.05:
        polarity_status = "FLIP_CONFIRMED — h_to_c randomization restored Φ toward random-mirror level"
    elif t_phi > rand_med and htc_med >= t_phi * 0.9:
        polarity_status = "FLIP_NOT_CONFIRMED — h_to_c randomization left Φ near trained level"
    else:
        polarity_status = f"AMBIGUOUS — t_phi={t_phi:.2f} htc_med={htc_med:.2f} rand_med={rand_med:.2f}"

    log(f"|htc_med - trained| = {d_to_trained:.2f}")
    log(f"|htc_med - random|  = {d_to_random:.2f}")
    log(f"closer to random? {closer_to_random}")
    log(f"polarity_status: {polarity_status}")

    out = {
        "config": {
            "n_turns": N_TURNS,
            "snapshot_every": SNAPSHOT_EVERY,
            "max_cells": MAX_CELLS,
            "mirror_seeds": ABLATION_MIRROR_SEEDS,
            "ckpt": CKPT_PATH,
        },
        "trained": trained_traj,
        "htc_randomized": htc_trajs,
        "full_random": rand_trajs,
        "verdict": {
            "trained_phi": t_phi,
            "htc_phis": htc_phis,
            "htc_mean": htc_mean,
            "htc_median": htc_med,
            "rand_phis": rand_phis,
            "rand_mean": rand_mean,
            "rand_median": rand_med,
            "d_to_trained": d_to_trained,
            "d_to_random": d_to_random,
            "closer_to_random": bool(closer_to_random),
            "polarity_status": polarity_status,
        },
    }
    out_path = OUT_DIR / "ablation_result.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    log(f"\nSaved → {out_path}")
    log_f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
