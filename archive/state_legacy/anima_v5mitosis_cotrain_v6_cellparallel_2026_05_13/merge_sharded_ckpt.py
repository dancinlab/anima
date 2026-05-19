"""state/anima_v5mitosis_cotrain_v6_cellparallel_2026_05_13/merge_sharded_ckpt.py

Merge sharded v6 cell-parallel ckpts (ckpt_final_rank{r}.pt) into a single-GPU
ckpt compatible with mitosis_model_v5.MitosisModelEngine (the v4 single-GPU API).

Usage:
    python3 merge_sharded_ckpt.py --shards 4 --input-dir ckpts/ --output ckpts/ckpt_merged.pt

Produces a ckpt with:
    model_state_dict: keys compatible with MitosisModelEngine (single-GPU)
        tok_emb.weight / pos_emb.weight / final_ln.* / lm_head.weight
        cells.0.* ... cells.{N_total-1}.* (concatenated across shards in rank order)
    router_state_dict: router weights from rank 0
    config: arch config
    n_cells: total cells
    cell_metadata: list of cell meta dicts in rank-then-local order

This is a POST-TRAINING utility; the training process itself writes sharded
artifacts. Downstream measurement (v4-style F-PERSONA-4a/4b, V5.8 4-mode eval,
HF push) loads the merged ckpt into MitosisModelEngine.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import torch


def merge_shards(shard_paths: List[Path], output_path: Path) -> Dict[str, Any]:
    shards = []
    for p in shard_paths:
        sd = torch.load(p, map_location="cpu", weights_only=False)
        shards.append(sd)
        print(f"[load] {p.name} rank={sd['rank']} n_local_cells={sd['n_local_cells']} "
              f"n_cells_global={sd['n_cells_global']} step={sd['step_count']}")

    shards.sort(key=lambda s: s["rank"])
    rank0 = shards[0]
    assert rank0["rank"] == 0, "rank 0 ckpt required (carries shared state)"
    assert rank0["shared_state"] is not None, "rank 0 must include shared_state"

    cfg = rank0["config"]
    world_size = rank0["world_size"]
    assert len(shards) == world_size, f"expected {world_size} shards, got {len(shards)}"

    # Build the single-GPU compatible state_dict
    merged_model_state: Dict[str, torch.Tensor] = {}

    # Shared modules: copy from rank 0
    for k, v in rank0["shared_state"].items():
        merged_model_state[k] = v.detach().cpu()

    # Cells: concatenate across shards in rank order
    total_local_idx = 0
    cell_meta_merged: List[Dict[str, Any]] = []
    for shard in shards:
        cells_state = shard["cells_state"]
        cell_meta = shard["cell_meta"]
        # Group keys by local cell index
        # cells_state keys look like "cells.{local_idx}.{...}"
        per_local: Dict[int, Dict[str, torch.Tensor]] = {}
        for key, val in cells_state.items():
            parts = key.split(".", 2)  # ["cells", "{local_idx}", "{rest}"]
            assert parts[0] == "cells", f"unexpected key: {key}"
            local_idx = int(parts[1])
            rest = parts[2]
            per_local.setdefault(local_idx, {})[rest] = val
        # Emit in local_idx order under new global index
        for local_idx in sorted(per_local.keys()):
            for rest, val in per_local[local_idx].items():
                merged_model_state[f"cells.{total_local_idx}.{rest}"] = val.detach().cpu()
            # carry meta
            this_meta = next((m for m in cell_meta if m["local_idx"] == local_idx), None)
            if this_meta is None:
                this_meta = {"local_idx": local_idx, "cell_id": -1}
            this_meta["new_global_idx"] = total_local_idx
            this_meta["original_rank"] = shard["rank"]
            cell_meta_merged.append(this_meta)
            total_local_idx += 1

    # Sanity: global n_cells should match across shards
    n_cells_claimed = rank0["n_cells_global"]
    if total_local_idx != n_cells_claimed:
        print(f"[WARN] merged n_cells={total_local_idx} != claimed n_cells_global={n_cells_claimed}")

    out_ckpt = {
        "model_state_dict": merged_model_state,
        "router_state_dict": rank0["router_state"],
        "router_top_k": rank0["router_top_k"],
        "config": cfg,
        "n_cells": total_local_idx,
        "step_count": rank0["step_count"],
        "cell_metadata": cell_meta_merged,
        "lorenz_state_rank0": rank0["lorenz_state"],
        "phi_rank0": rank0["phi"],
        "phi_best_rank0": rank0["phi_best"],
        "split_threshold_rank0": rank0["split_threshold"],
        "trainer": rank0["trainer"] + " [MERGED from {} shards]".format(world_size),
        "merged_at": rank0["saved_ts"],
        "world_size_at_train": world_size,
    }
    torch.save(out_ckpt, output_path)
    print(f"[merge] wrote {output_path} (n_cells={total_local_idx} from {world_size} shards)")
    return out_ckpt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, help="dir containing ckpt_final_rank{r}.pt")
    ap.add_argument("--shards", type=int, required=True, help="number of shards (world_size)")
    ap.add_argument("--output", required=True, help="merged ckpt output path")
    ap.add_argument("--prefix", default="ckpt_final_rank")
    args = ap.parse_args()

    inp = Path(args.input_dir)
    shard_paths = []
    for r in range(args.shards):
        p = inp / f"{args.prefix}{r}.pt"
        if not p.exists():
            raise FileNotFoundError(f"missing shard: {p}")
        shard_paths.append(p)

    merge_shards(shard_paths, Path(args.output))


if __name__ == "__main__":
    main()
