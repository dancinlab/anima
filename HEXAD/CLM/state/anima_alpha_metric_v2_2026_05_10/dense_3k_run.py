#!/usr/bin/env python3
"""Dense 3K toy run for V2 metric application — snapshot_every=1.

Re-uses TinyV5Substrate + ALL_PROMPTS + encode_prompt_to_hidden from the
existing 3K trajectory run.py (raw#15 additive — imports, no mutation).

Output: dense_3k_history.json — per-step records
    {step, cell_count, phi_unnorm, n_splits_cum, n_merges_cum}
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import torch

# Re-use upstream substrate + prompts + encoder
sys.path.insert(0, "/Users/ghost/core/anima/training")
sys.path.insert(0, "/Users/ghost/core/anima/state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10")

from mitosis_v5_port import MitosisV5Engine  # noqa: E402

# Import the upstream module by file path (its directory has unsafe name chars)
import importlib.util as _ilu  # noqa: E402

_RUN_PATH = "/Users/ghost/core/anima/state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/run.py"
_spec = _ilu.spec_from_file_location("upstream_run", _RUN_PATH)
_upstream = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_upstream)

TinyV5Substrate = _upstream.TinyV5Substrate
ALL_PROMPTS = _upstream.ALL_PROMPTS
encode_prompt_to_hidden = _upstream.encode_prompt_to_hidden


def main(n_turns: int = 3000, seed: int = 42) -> None:
    torch.manual_seed(seed)
    sub = TinyV5Substrate(n_cells=8, c_dim=12, d_model=32)
    mitosis = MitosisV5Engine(
        cell_pool=sub.cell_pool_init.detach().clone(),
        c_to_h=sub.c_to_h,
        initial_cells=8,
        max_cells=64,
        split_patience=3,
        split_noise=0.10,
        merge_threshold=0.005,
        merge_patience=30,
        min_cells=2,
        lorenz_scale=0.05,
    )
    n_splits = 0
    n_merges = 0
    history: list[dict] = []
    t0 = time.time()
    B, T, D = 2, 4, 32
    last_log = 0.0
    for turn in range(n_turns):
        _, prompt = ALL_PROMPTS[turn % len(ALL_PROMPTS)]
        x = encode_prompt_to_hidden(prompt, B=B, T=T, D=D)
        h_mean = sub.hidden_mean(x)
        out = mitosis.process(h_mean)
        for ev in out["events"]:
            if ev["type"] == "split":
                n_splits += 1
            elif ev["type"] == "merge":
                n_merges += 1
        # dense per-step record (snapshot_every=1 equivalent)
        history.append({
            "step": turn,
            "cell_count": int(out["n_cells"]),
            "phi_unnorm": float(out["phi"]),
            "n_splits_cum": n_splits,
            "n_merges_cum": n_merges,
        })
        if time.time() - last_log > 5:
            print(
                f"  step={turn:5d} cells={out['n_cells']:3d} Φ={out['phi']:.4f} "
                f"splits={n_splits} merges={n_merges} "
                f"elapsed={time.time()-t0:.1f}s"
            )
            last_log = time.time()
    elapsed = time.time() - t0
    print(f"DONE n_turns={n_turns} elapsed={elapsed:.1f}s splits={n_splits} merges={n_merges}")
    out_dir = Path("/Users/ghost/core/anima/state/anima_alpha_metric_v2_2026_05_10")
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = f"dense_{n_turns}_history.json"
    with open(out_dir / fname, "w") as fp:
        json.dump({
            "ts": "2026-05-10",
            "n_turns": n_turns,
            "seed": seed,
            "snapshot_every": 1,
            "elapsed_sec": elapsed,
            "final": {
                "n_cells": int(mitosis.n_cells),
                "phi": history[-1]["phi_unnorm"],
                "n_splits": n_splits,
                "n_merges": n_merges,
            },
            "history": history,
        }, fp)
    print(f"wrote {out_dir / fname}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    main(n_turns=n)
