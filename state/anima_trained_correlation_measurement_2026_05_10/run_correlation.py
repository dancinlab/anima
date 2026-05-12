"""BG-TRAINED-CORRELATION-MEASUREMENT — §51 cap-conditional mechanism explicit measurement.

Hypothesis (§51 ★★★ partial finding): trained cells reach cap LATER than random because
trained cells form more correlated structure → top-quartile dispersion has lower variance
spread → fewer outliers cross sigma_gate → split rate lower near cap.

This BG measures the inter-cell correlation matrix per turn for trained vs random across
3 substrates (A_phase2_cotrain EngineAG, C_cells64_aware v2, E_convo5k_ft v2) at max=256,
snapshotting full cell-pool tensor + dispersion mechanism state.

Lean compute (local CPU $0, own 16): 1 trained + 1 random per substrate (seed=42).
A: 100 turns / snap=10 (cap-free regime, but mechanism still measurable).
C, E: 60 turns / snap=5 (covers pre-cap and at-cap region).

Outputs (own 38):
  spec.md
  correlation_metrics.json   — per substrate × {trained,random} × turn snapshots
  dispersion_trigger_metrics.json — per-turn trigger rate trajectory
  verdict.md

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
from typing import Dict, List

import numpy as np
import torch

ANIMA_ROOT = Path("/Users/ghost/core/anima")
THIS_DIR = ANIMA_ROOT / "state" / "anima_trained_correlation_measurement_2026_05_10"
THIS_DIR.mkdir(parents=True, exist_ok=True)

# Upstream module imports (additive, raw#15)
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_clm_v5_iit_phi_remetric_2026_05_10"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_iit_real_350m_2026_05_10"))

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from _v14_5seed_run import (  # noqa: E402
    ALL_PROMPTS,
    encode_prompt_to_ids,
    HiddenMeanCapture,
)
from training.mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402
from training.v5mitosis_d384_v14_mirror import (  # noqa: E402
    init_engine_from_v2,
    init_engine_random,
    make_prompt_stream,
)


MAX_CELLS = 256
SEED_RANDOM = 42  # single random seed (lean compute)
TRAINED_PROMPT_SEED = 42
PER_CELL_SIGMA_MULT_DEFAULT = 1.0  # used for dispersion sigma_gate inspection

# Per-substrate run config
CFG_A = {"n_turns": 100, "snap_every": 10}
CFG_V2 = {"n_turns": 60, "snap_every": 5}

SUBSTRATES = {
    "A_phase2_cotrain": {
        "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
        "schema": "engine_ag",
        "arch": "EngineAG d=1024 GQA 24L (Phase 2 cotrain 350M)",
        **CFG_A,
    },
    "C_cells64_aware": {
        "ckpt": str(ANIMA_ROOT / "state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt"),
        "schema": "v2_d384",
        "arch": "v2 6L transformer d=384 heads=6",
        **CFG_V2,
    },
    "E_convo5k_ft": {
        "ckpt": str(ANIMA_ROOT / "state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt"),
        "schema": "v2_d384",
        "arch": "v2-derived 6L d=384 byte-level (FT)",
        **CFG_V2,
    },
}


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# =======================================================================
# Correlation / dispersion metrics on a cell-pool snapshot tensor (N, C)
# =======================================================================
def cell_pool_metrics(pool: torch.Tensor, sigma_mult: float = PER_CELL_SIGMA_MULT_DEFAULT) -> Dict:
    """Compute correlation, dispersion, eff_rank metrics from cell-pool tensor (N, C).

    - inter-cell pairwise cosine similarity (N, N) → mean/std/max/min off-diagonal
    - dispersion: pairwise mean L2² distance per row → top-quartile threshold trigger rate
      (matches the actual sigma_gate logic in mitosis_v5_port._dispersion_split_candidates).
    - eff_rank from singular values (sum(σ)² / sum(σ²)).
    - matrix trace of correlation matrix (= N for cosine, but normalized by N gives 1 by
      construction; here we report mean off-diagonal cosine — the canonical "correlation").
    """
    pool = pool.detach().float()
    N, C = pool.shape
    out: Dict = {"n_cells": int(N), "c_dim": int(C)}
    if N < 2:
        return out

    # ── Pairwise cosine similarity ─────────────────────────────────
    norms = pool.norm(dim=-1, keepdim=True).clamp(min=1e-9)
    unit = pool / norms
    cos = unit @ unit.t()  # (N, N) — diag = 1
    off_mask = ~torch.eye(N, dtype=torch.bool)
    off = cos[off_mask]
    out["cos_mean"] = float(off.mean().item())
    out["cos_std"] = float(off.std().item())
    out["cos_max"] = float(off.max().item())
    out["cos_min"] = float(off.min().item())
    # absolute-value version (catches anti-correlation as also "correlated structure")
    out["abs_cos_mean"] = float(off.abs().mean().item())

    # ── Magnitude statistics (norm distribution) ───────────────────
    n_norms = norms.squeeze(-1)
    out["norm_mean"] = float(n_norms.mean().item())
    out["norm_std"] = float(n_norms.std().item()) if N > 1 else 0.0
    out["norm_cv"] = (out["norm_std"] / out["norm_mean"]) if out["norm_mean"] > 1e-9 else 0.0

    # ── Effective rank ─────────────────────────────────────────────
    try:
        s = torch.linalg.svdvals(pool)
        s = s.clamp(min=1e-12)
        eff = float((s.sum() ** 2 / (s ** 2).sum()).item())
    except Exception:
        eff = float("nan")
    out["eff_rank"] = eff
    out["eff_rank_normalized"] = eff / N if N > 0 else float("nan")

    # ── Dispersion: pairwise L2² mean distance per row, sigma_gate ──
    diff = pool.unsqueeze(0) - pool.unsqueeze(1)
    d2 = (diff * diff).mean(dim=-1)  # (N, N)
    mean_dist = d2.sum(dim=-1) / max(N - 1, 1)  # (N,)
    overall_mean = float(mean_dist.mean().item())
    overall_sd = float(mean_dist.std().item()) if N > 1 else 0.0
    sigma_gate = overall_mean + sigma_mult * overall_sd
    k = max(1, int(0.25 * N))
    top_vals, _ = torch.topk(mean_dist, k=min(k, N), largest=True)
    n_above = int((top_vals > sigma_gate).sum().item())
    out["disp_overall_mean"] = overall_mean
    out["disp_overall_std"] = overall_sd
    out["disp_sigma_gate"] = sigma_gate
    out["disp_top_quartile_k"] = k
    out["disp_top_quartile_above_gate"] = n_above
    out["disp_trigger_rate"] = (n_above / k) if k > 0 else 0.0  # 0..1

    # ── Trace of correlation matrix (= sum of diag) — diag is always 1
    # so we report "trace minus diag norm" via mean-off-diagonal-square as
    # "structure energy" beyond identity
    out["cos_off_diag_l2"] = float(off.pow(2).mean().sqrt().item())

    return out


def stack_v2_cell_states(eng) -> torch.Tensor:
    """Stack cell_state (D,) buffers across cells for a v2 d=384 substrate."""
    return torch.stack([c.cell_state for c in eng.cells]).detach().clone()


# =======================================================================
# EngineAG path (substrate A)
# =======================================================================
def run_engine_ag_with_corr(model, label, n_turns, snap_every, seed, max_cells, log_fn):
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.eval()
    capture = HiddenMeanCapture(model.engine_g)
    eg = model.engine_g
    init_pool = eg.cell_pool_init.detach().clone()
    n_cells_init = init_pool.shape[0]
    mitosis = MitosisV5Engine(
        cell_pool=init_pool, c_to_h=eg.c_to_h,
        initial_cells=n_cells_init, max_cells=max_cells,
        split_patience=3, split_noise=0.10,
        merge_threshold=0.005, merge_patience=30,
        min_cells=2, lorenz_scale=0.05,
    )
    snapshots = []
    n_splits = 0
    n_splits_disp_cum = 0
    n_splits_tens_cum = 0
    n_merges = 0
    cap_bound_turns = 0
    first_cap_turn = None
    t_start = time.time()
    last_print = 0.0
    with torch.no_grad():
        for turn in range(n_turns):
            cat, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
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
                    trig = ev.get("trigger", "")
                    if "dispersion" in trig:
                        n_splits_disp_cum += 1
                    if "tension" in trig:
                        n_splits_tens_cum += 1
                elif ev["type"] == "merge":
                    n_merges += 1
            if out["n_cells"] >= max_cells:
                cap_bound_turns += 1
                if first_cap_turn is None:
                    first_cap_turn = turn
            if turn % snap_every == 0 or turn == n_turns - 1:
                cp = mitosis.cell_pool.detach()
                m = cell_pool_metrics(cp)
                m["turn"] = int(turn)
                m["n_splits_cum"] = int(n_splits)
                m["n_splits_dispersion_cum"] = int(n_splits_disp_cum)
                m["n_splits_tension_cum"] = int(n_splits_tens_cum)
                m["n_merges_cum"] = int(n_merges)
                m["elapsed_sec"] = float(time.time() - t_start)
                snapshots.append(m)
                if time.time() - last_print > 8:
                    log_fn(
                        f"  [{label}] turn={turn:4d} cells={m['n_cells']:3d}"
                        f" cos_mean={m['cos_mean']:+.4f}"
                        f" abs_cos={m['abs_cos_mean']:.4f}"
                        f" eff_rank={m['eff_rank']:.2f}"
                        f" disp_trig={m['disp_top_quartile_above_gate']}/{m['disp_top_quartile_k']}"
                        f" splits(d/t)={n_splits_disp_cum}/{n_splits_tens_cum}"
                        f" elapsed={m['elapsed_sec']:.1f}s"
                    )
                    last_print = time.time()
    return {
        "label": label, "seed": seed, "n_turns": n_turns,
        "elapsed_sec": time.time() - t_start,
        "snapshots": snapshots,
        "final_n_cells": int(mitosis.n_cells),
        "n_splits": n_splits,
        "n_splits_dispersion": n_splits_disp_cum,
        "n_splits_tension": n_splits_tens_cum,
        "n_merges": n_merges,
        "cap_bound_turns": cap_bound_turns,
        "first_cap_turn": first_cap_turn,
    }


def fire_substrate_engine_ag(sub_id, sub, log_fn):
    log_fn(f"\n{'='*72}\nSUBSTRATE {sub_id} — EngineAG path\n{'='*72}")
    log_fn(f"ckpt: {sub['ckpt']}")
    sha = sha256_of(sub["ckpt"])
    log_fn(f"sha256: {sha}")
    cfg = EngineAGConfig.phase2_cotrain_350m()
    ckpt = torch.load(sub["ckpt"], map_location="cpu", weights_only=False)
    sd = ckpt.get("state_dict", ckpt.get("model"))
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd.items()}
    trained_model = EngineAGModel(cfg)
    miss, unexp = trained_model.load_state_dict(sd_fp32, strict=False)
    n_params = sum(p.numel() for p in trained_model.parameters())
    log_fn(f"trained params={n_params/1e6:.2f}M miss={len(miss)} unexp={len(unexp)}")
    del ckpt, sd, sd_fp32

    log_fn(f"\n--- TRAINED prompt_seed={TRAINED_PROMPT_SEED} max_cells={MAX_CELLS} n_turns={sub['n_turns']} ---")
    trained = run_engine_ag_with_corr(
        trained_model, label=f"{sub_id}_trained",
        n_turns=sub["n_turns"], snap_every=sub["snap_every"],
        seed=TRAINED_PROMPT_SEED, max_cells=MAX_CELLS, log_fn=log_fn,
    )
    del trained_model

    log_fn(f"\n--- RANDOM seed={SEED_RANDOM} ---")
    rand_model = load_random_init(seed=SEED_RANDOM, preset="la_350m")
    random_run = run_engine_ag_with_corr(
        rand_model, label=f"{sub_id}_s{SEED_RANDOM}",
        n_turns=sub["n_turns"], snap_every=sub["snap_every"],
        seed=SEED_RANDOM, max_cells=MAX_CELLS, log_fn=log_fn,
    )
    del rand_model

    return {
        "substrate_id": sub_id,
        "schema": sub["schema"], "arch": sub["arch"],
        "ckpt": sub["ckpt"], "ckpt_sha256": sha, "n_params": n_params,
        "n_turns": sub["n_turns"], "snap_every": sub["snap_every"],
        "max_cells": MAX_CELLS,
        "trained": trained, "random": random_run,
    }


# =======================================================================
# v2 d=384 path (substrates C, E)
# =======================================================================
def run_v2_with_corr(eng, prompts, n_turns, snap_every, label, log_fn, max_cells):
    eng.eval()
    snapshots = []
    cap_bound_turns = 0
    first_cap_turn = None
    n_splits_disp_cum = 0
    n_splits_tens_cum = 0
    last_status_splits = {"splits": 0, "splits_by_dispersion": 0, "merges": 0, "ratchets": 0}
    t0 = time.time()
    last_print = 0.0
    with torch.no_grad():
        for t in range(n_turns):
            prompt = prompts[t][:, : eng.max_seq]
            try:
                logits, info = eng(prompt)
                eng.mitosis_step(info)
            except Exception as e:
                log_fn(f"  [{label}] turn={t} ERROR: {e}")
                continue
            if eng.n_cells >= max_cells:
                cap_bound_turns += 1
                if first_cap_turn is None:
                    first_cap_turn = t
            stat = eng.status()
            n_splits_disp_cum = stat.get("splits_by_dispersion", 0)
            n_splits_tens_cum = stat["splits"] - n_splits_disp_cum

            if (t % snap_every) == 0 or t == n_turns - 1:
                pool = stack_v2_cell_states(eng)
                m = cell_pool_metrics(pool)
                m["turn"] = int(t)
                m["n_splits_cum"] = int(stat["splits"])
                m["n_splits_dispersion_cum"] = int(n_splits_disp_cum)
                m["n_splits_tension_cum"] = int(n_splits_tens_cum)
                m["n_merges_cum"] = int(stat["merges"])
                m["phi"] = float(eng.phi)
                m["phi_per_cell"] = float(eng.phi_per_cell)
                m["elapsed_sec"] = float(time.time() - t0)
                snapshots.append(m)
                if time.time() - last_print > 8:
                    log_fn(
                        f"  [{label}] turn={t:4d} cells={m['n_cells']:3d}"
                        f" cos_mean={m['cos_mean']:+.4f}"
                        f" abs_cos={m['abs_cos_mean']:.4f}"
                        f" eff_rank={m['eff_rank']:.2f}"
                        f" disp_trig={m['disp_top_quartile_above_gate']}/{m['disp_top_quartile_k']}"
                        f" splits(d/t)={n_splits_disp_cum}/{n_splits_tens_cum}"
                        f" phi={m['phi']:.2f}"
                        f" elapsed={m['elapsed_sec']:.1f}s"
                    )
                    last_print = time.time()
    el_total = time.time() - t0
    status = eng.status()
    return {
        "label": label, "n_turns": n_turns,
        "elapsed_sec": el_total,
        "final_n_cells": eng.n_cells,
        "snapshots": snapshots,
        "n_splits": status["splits"],
        "n_splits_dispersion": status.get("splits_by_dispersion", 0),
        "n_splits_tension": status["splits"] - status.get("splits_by_dispersion", 0),
        "n_merges": status["merges"],
        "cap_bound_turns": cap_bound_turns,
        "first_cap_turn": first_cap_turn,
        "phi_final": eng.phi,
    }


def fire_substrate_v2(sub_id, sub, log_fn):
    log_fn(f"\n{'='*72}\nSUBSTRATE {sub_id} — v2 d=384 path\n{'='*72}")
    log_fn(f"ckpt: {sub['ckpt']}")
    sha = sha256_of(sub["ckpt"])
    log_fn(f"sha256: {sha}")
    ck = torch.load(sub["ckpt"], map_location="cpu", weights_only=False)
    sd = ck["model_state"]
    n_params = sum(v.numel() for v in sd.values() if hasattr(v, "numel"))
    log_fn(f"trained params={n_params/1e6:.2f}M step={ck.get('step')}")

    cfg = MitosisModelConfig(
        vocab_size=256, d_model=384, n_head=6, ffn_dim=1536,
        max_seq=256, initial_cells=8, max_cells=MAX_CELLS,
        dispersion_trigger_enabled=True,
        per_cell_threshold_enabled=True,
        lorenz_auto_calibrate=True,
        readout_mode="a_minus_g",
        attention_sharing="auto",
        weight_tied_lm_head=True,
    )
    prompts = make_prompt_stream(seed=2026, n_turns=sub["n_turns"], vocab=256, max_seq=256)

    log_fn(f"\n--- TRAINED max_cells={MAX_CELLS} n_turns={sub['n_turns']} ---")
    torch.manual_seed(0)
    eng_t, diag = init_engine_from_v2(cfg, sd)
    log_fn(f"  v2 blocks loaded={diag['v2_blocks_loaded']} random_cells={diag['random_cells']}")
    trained = run_v2_with_corr(eng_t, prompts, sub["n_turns"], sub["snap_every"],
                               label=f"{sub_id}_trained", log_fn=log_fn, max_cells=MAX_CELLS)
    del eng_t

    log_fn(f"\n--- RANDOM seed={SEED_RANDOM} ---")
    eng_r = init_engine_random(cfg, SEED_RANDOM)
    random_run = run_v2_with_corr(eng_r, prompts, sub["n_turns"], sub["snap_every"],
                                  label=f"{sub_id}_s{SEED_RANDOM}", log_fn=log_fn, max_cells=MAX_CELLS)
    del eng_r

    return {
        "substrate_id": sub_id,
        "schema": sub["schema"], "arch": sub["arch"],
        "ckpt": sub["ckpt"], "ckpt_sha256": sha, "n_params": n_params,
        "n_turns": sub["n_turns"], "snap_every": sub["snap_every"],
        "max_cells": MAX_CELLS,
        "trained": trained, "random": random_run,
    }


# =======================================================================
# Entry
# =======================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrate", type=str, default="ALL",
                    help="A_phase2_cotrain | C_cells64_aware | E_convo5k_ft | ALL")
    args = ap.parse_args()
    targets = list(SUBSTRATES.keys()) if args.substrate == "ALL" else [args.substrate]

    aggregate = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "config": {
            "max_cells": MAX_CELLS,
            "seed_random": SEED_RANDOM,
            "trained_prompt_seed": TRAINED_PROMPT_SEED,
            "per_substrate_cfg": {k: {"n_turns": v["n_turns"], "snap_every": v["snap_every"]} for k, v in SUBSTRATES.items()},
        },
        "substrates": {},
    }

    for sub_id in targets:
        sub = SUBSTRATES[sub_id]
        out = THIS_DIR / f"result_{sub_id}.json"
        log_path = THIS_DIR / f"run_{sub_id}.log"
        log_f = open(log_path, "w")

        def log(msg, _f=log_f):
            print(msg, flush=True)
            _f.write(msg + "\n")
            _f.flush()

        log(f"=== BG-TRAINED-CORRELATION-MEASUREMENT — {sub_id} ===")
        log(f"ts: {datetime.now(timezone.utc).isoformat()}")
        log(f"sub: {sub}")

        if sub["schema"] == "engine_ag":
            result = fire_substrate_engine_ag(sub_id, sub, log)
        elif sub["schema"] == "v2_d384":
            result = fire_substrate_v2(sub_id, sub, log)
        else:
            raise RuntimeError(f"Unknown schema {sub['schema']}")

        with out.open("w") as f:
            json.dump(result, f, indent=2, default=str)
        log(f"[saved] {out}")
        aggregate["substrates"][sub_id] = result
        log_f.close()

    agg_path = THIS_DIR / "aggregate.json"
    with agg_path.open("w") as f:
        json.dump(aggregate, f, indent=2, default=str)
    print(f"\n[aggregate saved] {agg_path}")


if __name__ == "__main__":
    main()
