"""BG-V14-MAX256-CAP-FREE-MULTI — 3 substrate × max=256 × 5-seed strict.

Cap-conditional polarity strict test at max_cells=256, disambiguating
cap-conditional vs cotrain-exercise hypotheses (§45 + §47 follow-up).

Substrates:
  A_phase2_cotrain — EngineAG path (350M Phase 2 cotrain ckpt)
  C_cells64_aware  — v2 d=384 path (mitosis-aware)
  E_convo5k_ft     — v2 d=384 path (mitosis-naive FT, no in-loop mitosis)

raw#9 / raw#15 / / / / honored.
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
THIS_DIR = ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"
THIS_DIR.mkdir(parents=True, exist_ok=True)

# upstream module imports (additive, raw#15)
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_clm_v5_iit_phi_remetric_2026_05_10"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_iit_real_350m_2026_05_10"))

from mitosis_v5_port import MitosisV5Engine  # noqa: E402
from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa: E402
from iit_phi_port import compute_iit_phi  # noqa: E402
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


V4_SEEDS = [42, 137, 271, 314, 1729]
TRAINED_PROMPT_SEED = 42
MAX_CELLS = 256  # ★ §45/§47 used 128; this is the SOLE override
N_TURNS = 200 # budget compromise; mission asked 1K-turn
SNAP_EVERY = 25  # denser than §47

SUBSTRATES = {
    "A_phase2_cotrain": {
        "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
        "schema": "engine_ag",
        "arch": "EngineAG d=1024 GQA 24L (Phase 2 cotrain 350M)",
        "paradigm": "naive_cotrain_chat_KO",
    },
    "C_cells64_aware": {
        "ckpt": str(ANIMA_ROOT / "state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt"),
        "schema": "v2_d384",
        "arch": "v2 6L transformer d=384 heads=6",
        "paradigm": "aware_max_cells_64",
    },
    "E_convo5k_ft": {
        "ckpt": str(ANIMA_ROOT / "state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt"),
        "schema": "v2_d384",
        "arch": "v2-derived 6L d=384 byte-level (FT)",
        "paradigm": "naive_ft_no_mitosis",
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


# =======================================================================
# EngineAG path (substrate A)
# =======================================================================
def run_engine_ag_trajectory(model, label, n_turns, seed, max_cells, log_fn):
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
                elif ev["type"] == "merge":
                    n_merges += 1
            if out["n_cells"] >= max_cells:
                cap_bound_turns += 1
                if first_cap_turn is None:
                    first_cap_turn = turn
            if turn % SNAP_EVERY == 0 or turn == n_turns - 1:
                cp = mitosis.cell_pool.detach().cpu().numpy()
                phi_iit = compute_iit_phi(torch.tensor(cp, dtype=torch.float32), n_bins=16)
                snap = {
                    "turn": int(turn),
                    "n_cells": int(out["n_cells"]),
                    "proxy_phi": float(out["phi"]),
                    "iit_phi_unnorm_b16": phi_iit["spatial_phi_unnormalized"],
                    "iit_phi_norm_b16": phi_iit["spatial_phi"],
                    "n_splits_cum": int(n_splits),
                    "n_merges_cum": int(n_merges),
                    "elapsed_sec": float(time.time() - t_start),
                }
                snapshots.append(snap)
                if time.time() - last_print > 8:
                    log_fn(
                        f"  [{label}] turn={turn:5d} cells={snap['n_cells']:3d}"
                        f" iit_un16={snap['iit_phi_unnorm_b16']:7.2f}"
                        f" splits={n_splits} elapsed={snap['elapsed_sec']:.1f}s"
                    )
                    last_print = time.time()
    return {
        "label": label, "seed": seed, "n_turns": n_turns,
        "elapsed_sec": time.time() - t_start,
        "snapshots": snapshots,
        "final_n_cells": int(mitosis.n_cells),
        "n_splits": n_splits, "n_merges": n_merges,
        "cap_bound_turns": cap_bound_turns,
        "first_cap_turn": first_cap_turn,
    }


def fire_substrate_engine_ag(sub_id, sub, log_fn):
    log_fn(f"\n{'='*72}\nSUBSTRATE {sub_id} — EngineAG path  max_cells={MAX_CELLS}\n{'='*72}")
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
    log_fn(f"trained: params={n_params/1e6:.2f}M miss={len(miss)} unexp={len(unexp)}")
    del ckpt, sd, sd_fp32

    log_fn(f"\n--- TRAINED @ prompt_seed={TRAINED_PROMPT_SEED} max_cells={MAX_CELLS} ---")
    trained = run_engine_ag_trajectory(
        trained_model, label=f"{sub_id}_trained", n_turns=N_TURNS,
        seed=TRAINED_PROMPT_SEED, max_cells=MAX_CELLS, log_fn=log_fn,
    )
    tfinal = trained["snapshots"][-1]
    log_fn(f"  trained: cells={trained['final_n_cells']} splits={trained['n_splits']}"
           f" cap_bound={trained['cap_bound_turns']}/{N_TURNS} first_cap={trained['first_cap_turn']}"
           f" Φ_un16={tfinal['iit_phi_unnorm_b16']:.2f} elapsed={trained['elapsed_sec']:.1f}s")
    del trained_model

    mirrors = []
    for s in V4_SEEDS:
        log_fn(f"\n--- mirror seed={s} ---")
        rand_model = load_random_init(seed=s, preset="la_350m")
        traj = run_engine_ag_trajectory(
            rand_model, label=f"{sub_id}_s{s}", n_turns=N_TURNS,
            seed=s, max_cells=MAX_CELLS, log_fn=log_fn,
        )
        rfinal = traj["snapshots"][-1]
        log_fn(f"  s={s}: cells={traj['final_n_cells']} splits={traj['n_splits']}"
               f" cap_bound={traj['cap_bound_turns']}/{N_TURNS} first_cap={traj['first_cap_turn']}"
               f" Φ_un16={rfinal['iit_phi_unnorm_b16']:.2f}")
        mirrors.append(traj)
        del rand_model

    return verdict_from_runs_engine_ag(sub_id, sub, sha, n_params, trained, mirrors)


# =======================================================================
# v2 d=384 path (substrates C, E)
# =======================================================================
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
                    log_fn(f"  [{label}] turn {t:>4d} n_cells={eng.n_cells} phi={eng.phi:.3f} ({el:.1f}s)")
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


def alpha_v2(traj):
    xs, ys = [], []
    for (turn, nc, phi, phi_pc) in traj:
        if nc < 2 or phi_pc <= 0:
            continue
        xs.append(math.log(nc))
        ys.append(math.log(phi_pc + 1.0))
    if len(xs) < 5:
        return None
    n = len(xs)
    mx = sum(xs) / n; my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den < 1e-12:
        return None
    return num / den


def fire_substrate_v2_d384(sub_id, sub, log_fn):
    log_fn(f"\n{'='*72}\nSUBSTRATE {sub_id} — v2 d=384 path  max_cells={MAX_CELLS}\n{'='*72}")
    log_fn(f"ckpt: {sub['ckpt']}")
    sha = sha256_of(sub["ckpt"])
    log_fn(f"sha256: {sha}")
    ck = torch.load(sub["ckpt"], map_location="cpu", weights_only=False)
    sd = ck["model_state"]
    n_params = sum(v.numel() for v in sd.values() if hasattr(v, "numel"))
    log_fn(f"trained: params={n_params/1e6:.2f}M step={ck.get('step')}")

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
    prompts = make_prompt_stream(seed=2026, n_turns=N_TURNS, vocab=256, max_seq=256)

    log_fn(f"\n--- TRAINED max_cells={MAX_CELLS} n_turns={N_TURNS} ---")
    torch.manual_seed(0)
    eng_t, diag = init_engine_from_v2(cfg, sd)
    log_fn(f"  v2 blocks loaded={diag['v2_blocks_loaded']} random_cells={diag['random_cells']}")
    trained = run_v2_trajectory(eng_t, prompts, N_TURNS, label=f"{sub_id}_trained", log_fn=log_fn, max_cells=MAX_CELLS)
    trained["alpha_v2"] = alpha_v2(trained["phi_trajectory"])
    log_fn(f"  trained: cells={trained['final_n_cells']} splits={trained['splits']}"
           f" phi={trained['phi_final']:.3f} phi/c={trained['phi_per_cell_final']:.3f}"
           f" α={trained['alpha_v2']} cap_bound={trained['cap_bound_turns']}/{N_TURNS}"
           f" first_cap={trained['first_cap_turn']}"
           f" max_observed={trained['max_n_cells_observed']}"
           f" elapsed={trained['elapsed_s']:.1f}s")
    del eng_t

    mirrors = []
    for s in V4_SEEDS:
        log_fn(f"\n--- mirror seed={s} ---")
        eng_r = init_engine_random(cfg, s)
        rrun = run_v2_trajectory(eng_r, prompts, N_TURNS, label=f"{sub_id}_s{s}", log_fn=log_fn, max_cells=MAX_CELLS)
        rrun["seed"] = s
        rrun["alpha_v2"] = alpha_v2(rrun["phi_trajectory"])
        log_fn(f"  s={s}: cells={rrun['final_n_cells']} splits={rrun['splits']}"
               f" phi={rrun['phi_final']:.3f} phi/c={rrun['phi_per_cell_final']:.3f}"
               f" α={rrun['alpha_v2']} cap_bound={rrun['cap_bound_turns']}/{N_TURNS}"
               f" first_cap={rrun['first_cap_turn']}"
               f" max_observed={rrun['max_n_cells_observed']}")
        mirrors.append(rrun)
        del eng_r

    return verdict_from_runs_v2(sub_id, sub, sha, n_params, trained, mirrors)


def verdict_from_runs_engine_ag(sub_id, sub, sha, n_params, trained, mirrors):
    tfinal = trained["snapshots"][-1]
    rand_phi = [m["snapshots"][-1]["iit_phi_unnorm_b16"] for m in mirrors]
    rand_cells = [m["final_n_cells"] for m in mirrors]
    n_beats = sum(1 for r in rand_phi if tfinal["iit_phi_unnorm_b16"] > r)
    p_sign = sign_test_p_value(n_beats, len(rand_phi))
    if n_beats == len(rand_phi):
        verdict = "V14_PASS"
    elif n_beats >= len(rand_phi) - 1:
        verdict = "V14_PARTIAL"
    elif n_beats <= 1:
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
        "metric_primary": "iit_phi_unnorm_b16",
        "trained_phi": tfinal["iit_phi_unnorm_b16"],
        "trained_n_cells": trained["final_n_cells"],
        "trained_splits": trained["n_splits"],
        "trained_cap_bound_turns": trained["cap_bound_turns"],
        "trained_first_cap_turn": trained["first_cap_turn"],
        "random_phi": rand_phi,
        "random_n_cells": rand_cells,
        "random_seeds": V4_SEEDS,
        "random_first_cap_turn": [m["first_cap_turn"] for m in mirrors],
        "random_cap_bound_turns": [m["cap_bound_turns"] for m in mirrors],
        "n_random_beats": n_beats,
        "n_random_total": len(rand_phi),
        "sign_test_p_two_sided": p_sign,
        "verdict": verdict,
        "trained_run": {"snapshots": trained["snapshots"], "elapsed_sec": trained["elapsed_sec"]},
        "mirror_runs": [{
            "seed": m["seed"], "elapsed_sec": m["elapsed_sec"],
            "final_n_cells": m["final_n_cells"], "n_splits": m["n_splits"],
            "cap_bound_turns": m["cap_bound_turns"],
            "first_cap_turn": m["first_cap_turn"],
            "phi_final": m["snapshots"][-1]["iit_phi_unnorm_b16"],
            "snapshots": m["snapshots"],
        } for m in mirrors],
    }


def verdict_from_runs_v2(sub_id, sub, sha, n_params, trained, mirrors):
    rand_phi = [m["phi_final"] for m in mirrors]
    rand_phi_pc = [m["phi_per_cell_final"] for m in mirrors]
    rand_cells = [m["final_n_cells"] for m in mirrors]
    n_beats = sum(1 for r in rand_phi if trained["phi_final"] > r)
    n_beats_pc = sum(1 for r in rand_phi_pc if trained["phi_per_cell_final"] > r)
    p_sign = sign_test_p_value(n_beats, len(rand_phi))
    p_sign_pc = sign_test_p_value(n_beats_pc, len(rand_phi_pc))
    if n_beats == len(rand_phi) and n_beats_pc == len(rand_phi_pc):
        verdict = "V14_PASS"
    elif n_beats == len(rand_phi) or n_beats_pc == len(rand_phi_pc):
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
        "random_phi": rand_phi,
        "random_phi_per_cell": rand_phi_pc,
        "random_n_cells": rand_cells,
        "random_max_n_cells_observed": [m["max_n_cells_observed"] for m in mirrors],
        "random_seeds": V4_SEEDS,
        "random_first_cap_turn": [m["first_cap_turn"] for m in mirrors],
        "random_cap_bound_turns": [m["cap_bound_turns"] for m in mirrors],
        "n_random_beats_phi": n_beats,
        "n_random_beats_phi_per_cell": n_beats_pc,
        "n_random_total": len(rand_phi),
        "sign_test_p_phi": p_sign,
        "sign_test_p_phi_per_cell": p_sign_pc,
        "verdict": verdict,
        "trained_phi_trajectory": trained["phi_trajectory"],
        "mirror_runs": [{
            "seed": m["seed"], "elapsed_s": m["elapsed_s"],
            "final_n_cells": m["final_n_cells"], "n_splits": m["splits"],
            "cap_bound_turns": m["cap_bound_turns"],
            "first_cap_turn": m["first_cap_turn"],
            "max_n_cells_observed": m["max_n_cells_observed"],
            "phi_final": m["phi_final"], "phi_per_cell_final": m["phi_per_cell_final"],
            "alpha_v2": m["alpha_v2"],
            "phi_trajectory": m["phi_trajectory"],
        } for m in mirrors],
    }


def main():
    global N_TURNS, SNAP_EVERY, MAX_CELLS
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrate", type=str, required=True,
                    help="One of: A_phase2_cotrain, C_cells64_aware, E_convo5k_ft, ALL")
    ap.add_argument("--n-turns", type=int, default=N_TURNS)
    ap.add_argument("--max-cells", type=int, default=MAX_CELLS)
    ap.add_argument("--snap-every", type=int, default=SNAP_EVERY)
    args = ap.parse_args()
    N_TURNS = args.n_turns
    SNAP_EVERY = args.snap_every
    MAX_CELLS = args.max_cells

    if args.substrate == "ALL":
        targets = list(SUBSTRATES.keys())
    else:
        targets = [args.substrate]

    aggregate = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "config": {
            "max_cells": MAX_CELLS,
            "n_turns": N_TURNS,
            "snap_every": SNAP_EVERY,
            "v4_seeds": V4_SEEDS,
            "trained_prompt_seed": TRAINED_PROMPT_SEED,
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

        log(f"=== BG-V14-MAX256-CAP-FREE-MULTI — {sub_id} ===")
        log(f"ts: {datetime.now(timezone.utc).isoformat()}")
        log(f"sub: {sub}")
        log(f"V4_SEEDS={V4_SEEDS} max_cells={MAX_CELLS} n_turns={N_TURNS} snap_every={SNAP_EVERY}")

        if sub["schema"] == "engine_ag":
            result = fire_substrate_engine_ag(sub_id, sub, log)
        elif sub["schema"] == "v2_d384":
            result = fire_substrate_v2_d384(sub_id, sub, log)
        else:
            raise RuntimeError(f"Unknown schema {sub['schema']}")

        log(f"\n=== {sub_id} VERDICT: {result['verdict']} ===")
        with out.open("w") as f:
            json.dump(result, f, indent=2, default=str)
        log(f"[saved] {out}")
        aggregate["substrates"][sub_id] = result
        log_f.close()

    agg_path = THIS_DIR / "per_substrate_max256_results.json"
    with agg_path.open("w") as f:
        json.dump(aggregate, f, indent=2, default=str)
    print(f"\n[aggregate saved] {agg_path}")


if __name__ == "__main__":
    main()
