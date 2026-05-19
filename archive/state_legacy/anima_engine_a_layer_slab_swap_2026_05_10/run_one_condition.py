"""run_one_condition.py — driver for a single ablation condition.

Invoked as:
    python run_one_condition.py <COND_LABEL> <SLAB_NAME_OR_NONE>

Loads A (Phase 2 cotrain) ckpt, optionally swaps in B's slab tensors,
runs V14 short trajectory (1 trained + 3 mirrors), writes result to
{THIS_DIR}/cond_{COND_LABEL}.json.

Usage:
    run_one_condition.py A0_baseline NONE
    run_one_condition.py A1_slab1_early slab1_early
    run_one_condition.py A2_slab2_middle slab2_middle
    run_one_condition.py A3_slab3_late slab3_late
"""
from __future__ import annotations

import gc
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import torch

ANIMA = "/Users/ghost/core/anima"
sys.path.insert(0, f"{ANIMA}/training")
sys.path.insert(0, f"{ANIMA}/state/anima_iit_real_350m_2026_05_10")
sys.path.insert(0, f"{ANIMA}/state/anima_clm_v5_iit_phi_remetric_2026_05_10")
sys.path.insert(0, f"{ANIMA}/state/anima_engine_a_layer_slab_swap_2026_05_10")

from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init  # noqa
from run import (  # noqa
    _load_engine_ag, _run_v14_short, swap_slab_from_sds_, SLABS,
    CKPT_PHASE2, CKPT_BGLA, V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS,
    THIS_DIR,
)


def main():
    if len(sys.argv) != 3:
        print("usage: run_one_condition.py COND_LABEL SLAB_NAME_OR_NONE", file=sys.stderr)
        sys.exit(2)
    cond_label = sys.argv[1]
    slab_name = sys.argv[2]
    if slab_name == "NONE":
        slab_name = None

    out_path = THIS_DIR / f"cond_{cond_label}.json"
    print(f"[{cond_label}] start ts={datetime.now(timezone.utc).isoformat()}", flush=True)
    t_start = time.time()

    # Load A
    t0 = time.time()
    model_A = _load_engine_ag(CKPT_PHASE2, "phase2_cotrain")
    print(f"[{cond_label}] A loaded: {time.time()-t0:.1f}s", flush=True)

    diag = {"slab": None, "n_tensors_swapped": 0, "n_params_swapped": 0}

    if slab_name is not None:
        # Load B, snapshot relevant slab layers, free B
        t0 = time.time()
        model_B = _load_engine_ag(CKPT_BGLA, "la_350m")
        print(f"[{cond_label}] B loaded: {time.time()-t0:.1f}s", flush=True)
        layer_idxs = SLABS[slab_name]
        B_layer_sds = [None] * model_B.cfg.n_layers
        for li in layer_idxs:
            B_layer_sds[li] = {k: v.detach().clone()
                               for k, v in model_B.layers[li].state_dict().items()}
        del model_B
        gc.collect()
        print(f"[{cond_label}] B freed; {len(layer_idxs)} slab layers retained", flush=True)
        # Apply swap
        diag = swap_slab_from_sds_(model_A, B_layer_sds, slab_name)
        print(f"[{cond_label}] swapped {diag['n_tensors_swapped']} tensors "
              f"({diag['n_params_swapped']:,} params)", flush=True)
        del B_layer_sds
        gc.collect()

    # Run V14 (model_A is the trained substrate; mirrors built fresh per seed)
    print(f"[{cond_label}] V14 short trajectory N_TURNS={N_TURNS_ABL} seeds={V4_SEEDS}...",
          flush=True)
    t0 = time.time()
    res = _run_v14_short(model_A, cond_label,
                         V4_SEEDS, N_TURNS_ABL, SNAPSHOT_EVERY, MAX_CELLS)
    print(f"[{cond_label}] V14 done: {time.time()-t0:.1f}s  verdict={res['verdict']}",
          flush=True)
    res["swap_diag"] = diag
    res["elapsed_total_sec_with_load"] = time.time() - t_start

    out_path.write_text(json.dumps(res, indent=2))
    print(f"[{cond_label}] saved {out_path}", flush=True)
    print(f"[{cond_label}] trained Φ_un16={res['trained_iit_un16']:.2f}"
          f"  mirror_mean={res['mirror_iit_un16_mean']:.2f}"
          f"  beats_un={res['n_beats_iit_un16']}/{res['n_seeds']}"
          f"  beats_proxy={res['n_beats_proxy_phi']}/{res['n_seeds']}"
          f"  trained_cells={res['trained_n_cells']} mirror_cells={res['mirror_n_cells']}",
          flush=True)


if __name__ == "__main__":
    main()
