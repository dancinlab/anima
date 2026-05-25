#!/usr/bin/env python3
"""Try to load each .pt into MitosisEngine from canonical mitosis.py.

MitosisEngine has NO load_state_dict method — it composes N×Cell×ConsciousMind.
Each ConsciousMind has engine_a (Linear seq), engine_g (Linear seq), memory (GRUCell).

The cells64/cells128 .pt model_state contains a single byte-level Transformer:
- tok_emb [256, 384], pos_emb [256, 384], 6 blocks with engine_a/engine_g (FFN, NOT cells), head_a/head_g.
- This is NOT a MitosisEngine state_dict.

We:
1. Confirm MitosisEngine.cells[i].mind.state_dict() vs model_state keys → mismatch evidence.
2. Try forced load anyway: build engine, then load_state_dict on cell[0].mind → measure overlap.
"""
import sys
import json
import os
import importlib.util
import torch
import torch.nn as nn

CANONICAL = "/Users/ghost/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py"
LEGACY = "/Users/ghost/core/anima/ready/anima/models/legacy/mitosis.py"

def import_from(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    pt_path = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "model"

    print(f"=== load test: {pt_path} (label={label}) ===")

    # Load checkpoint
    ckpt = torch.load(pt_path, map_location="cpu", weights_only=False)
    sd = ckpt.get("model_state", ckpt)
    sd_keys = set(sd.keys())
    print(f"checkpoint state_dict keys: {len(sd_keys)}")
    print(f"sample keys: {sorted(sd_keys)[:5]}")

    # Import canonical mitosis.py
    mit = import_from(CANONICAL, "mitosis_canonical")
    print(f"\nMitosis module loaded: {mit.__file__}")
    print(f"  ConsciousMind={mit.ConsciousMind}, MitosisEngine={mit.MitosisEngine}")

    # Build a default MitosisEngine matching default args (input_dim=64, hidden=128, output=64)
    config = ckpt.get("config", {})
    n_cells_meta = ckpt.get("mitosis_status", {}).get("n_cells", 2)
    print(f"\ncheckpoint config: {config}")
    print(f"checkpoint n_cells (mitosis_status): {n_cells_meta}")

    # Get a single ConsciousMind state_dict for comparison
    cm = mit.ConsciousMind(input_dim=64, hidden_dim=128, output_dim=64)
    cm_keys = set(cm.state_dict().keys())
    print(f"\nConsciousMind default state_dict keys ({len(cm_keys)}):")
    for k in sorted(cm_keys):
        sh = list(cm.state_dict()[k].shape)
        print(f"  {k}: {sh}")

    # Try N=2 MitosisEngine
    eng = mit.MitosisEngine(input_dim=64, hidden_dim=128, output_dim=64, initial_cells=2)
    # Reconstruct state_dict from cells
    eng_sd = {}
    for i, cell in enumerate(eng.cells):
        for k, v in cell.mind.state_dict().items():
            eng_sd[f"cells.{i}.mind.{k}"] = v
    eng_keys = set(eng_sd.keys())
    print(f"\nMitosisEngine (n=2) reconstructed state_dict keys ({len(eng_keys)}):")
    for k in sorted(eng_keys)[:10]:
        print(f"  {k}: {list(eng_sd[k].shape)}")

    # Try direct load on the cell[0].mind via load_state_dict on ckpt (will fail)
    print("\n--- attempt 1: load checkpoint sd into ConsciousMind ---")
    try:
        cm.load_state_dict(sd, strict=False)
        miss, unexp = cm.load_state_dict(sd, strict=False)
        print(f"  load result: missing={len(miss)}, unexpected={len(unexp)}")
        print(f"  missing[:5]: {list(miss)[:5]}")
        print(f"  unexpected[:5]: {list(unexp)[:5]}")
    except Exception as e:
        print(f"  EXCEPTION: {type(e).__name__}: {e}")

    print("\n--- attempt 2: load checkpoint sd into MitosisEngine via cells[i].mind iter ---")
    try:
        miss_total = 0
        unexp_total = 0
        for i, cell in enumerate(eng.cells):
            miss, unexp = cell.mind.load_state_dict(sd, strict=False)
            miss_total += len(miss)
            unexp_total += len(unexp)
        print(f"  total missing across {len(eng.cells)} cells: {miss_total}")
        print(f"  total unexpected: {unexp_total}")
    except Exception as e:
        print(f"  EXCEPTION: {type(e).__name__}: {e}")

    # Schema overlap diagnostic
    overlap = sd_keys & cm_keys
    print(f"\nschema overlap: ckpt ∩ ConsciousMind = {len(overlap)} keys")
    if overlap:
        print(f"  overlap: {sorted(overlap)}")

    # Verdict
    print("\n--- archaeological verdict ---")
    if "blocks.0.attn.c_attn.weight" in sd_keys and "tok_emb.weight" in sd_keys:
        print("  ARCH = SINGLE byte-level Transformer decoder (ConsciousLM v2)")
        print("        NOT a MitosisEngine ensemble. mitosis.py CANNOT load this directly.")
        print("        mitosis_status in ckpt = side-channel metadata, NOT model state.")
    elif overlap == cm_keys:
        print("  ARCH = MitosisEngine compatible (full ConsciousMind keys present)")
    else:
        print("  ARCH = unknown / partial match")

    return {
        "ckpt_keys_count": len(sd_keys),
        "consciousmind_keys": sorted(cm_keys),
        "schema_overlap_count": len(overlap),
        "verdict": "single_decoder_ConsciousLM_v2" if "blocks.0.attn.c_attn.weight" in sd_keys else "unknown",
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
