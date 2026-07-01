#!/usr/bin/env python3
"""tool/convert_pt_to_safetensors.py — one-time .pt → .safetensors bridge.

PURPOSE
    HEXA_NATIVE_INFERENCE.md Phase 1 bridge layer. Pure-hexa inference needs
    the EngineAG ckpt in safetensors format (hexa stdlib/safetensors.hexa
    has full parse/load surface, but cannot read PyTorch pickle .pt).

USAGE
    python3 tool/convert_pt_to_safetensors.py <input.pt> <output.safetensors>
    python3 tool/convert_pt_to_safetensors.py --default   # converts Phase 1A.1

OUTPUTS
    - <output.safetensors>           raw weights (222 tensors)
    - <output>.meta.json             arch hyperparams + tensor manifest
                                     (n_layers, d_model, etc. — for hexa to parse)

COMPLIANCE
     mandate: raw output preserved (no transformations).
    raw#9 EXCEPTION: PyTorch pickle deserialization is python-only.
    This is a one-time bridge; the hexa-native inference path reads
    .safetensors directly via stdlib/safetensors.hexa.

WHY pure-hexa cannot read .pt
    .pt uses Python's pickle protocol with custom torch._utils._rebuild_tensor_v2
    callbacks. Re-implementing pickle in hexa is out of scope and would
    introduce a security-sensitive parser. safetensors is the standard
    interchange format (header JSON + raw bytes, simple and safe).
"""

import argparse
import json
import sys
from pathlib import Path

import torch
from safetensors.torch import save_file


ANIMA_ROOT = Path("/Users/ghost/core/anima")
DEFAULT_INPUT = (
    ANIMA_ROOT
    / "state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt"
)
DEFAULT_OUTPUT = (
    ANIMA_ROOT
    / "state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.safetensors"
)


def convert(input_pt: Path, output_st: Path) -> dict:
    """Load .pt, extract state_dict, save as .safetensors. Returns meta dict."""
    print(f"loading: {input_pt}")
    ck = torch.load(input_pt, map_location="cpu", weights_only=False)

    # locate state_dict
    sd_key = None
    for cand in ("model", "model_state", "state_dict", "model_state_dict"):
        if cand in ck:
            sd_key = cand
            break
    sd = ck[sd_key] if sd_key else ck
    print(f"state_dict at ck[{sd_key!r}]" if sd_key else "state_dict at top level")

    # filter: tensors only, contiguous, detach. Skip tied weights (dedupe by data_ptr).
    tensors = {}
    tied_aliases = {}  # alias_key -> primary_key (for hexa loader to re-link)
    seen_ptrs = {}     # data_ptr -> first key
    for k, v in sd.items():
        if not isinstance(v, torch.Tensor):
            print(f"  skip non-tensor: {k} ({type(v).__name__})")
            continue
        t = v.detach().contiguous().cpu()
        ptr = t.data_ptr()
        if ptr in seen_ptrs:
            primary = seen_ptrs[ptr]
            tied_aliases[k] = primary
            print(f"  tied: {k} → alias of {primary} (dedupe)")
            continue
        # safetensors requires standard dtypes; some training ckpts have bf16/fp16
        if t.dtype not in (torch.float32, torch.float16, torch.bfloat16, torch.int32, torch.int64, torch.uint8, torch.bool):
            print(f"  cast {k} {t.dtype} → float32")
            t = t.to(torch.float32)
        tensors[k] = t
        seen_ptrs[ptr] = k

    total_params = sum(t.numel() for t in tensors.values())
    print(f"\ntensors: {len(tensors)} (+{len(tied_aliases)} tied aliases) | total params: {total_params:,}")

    # save
    print(f"writing: {output_st}")
    save_file(tensors, str(output_st))
    size_mb = output_st.stat().st_size / (1024 * 1024)
    print(f"size: {size_mb:.1f}MB")

    # build meta.json (arch hyperparams inferred from shapes)
    meta = _infer_meta(tensors)
    meta["source_pt"] = str(input_pt)
    meta["output_safetensors"] = str(output_st)
    meta["total_params"] = total_params
    meta["n_tensors"] = len(tensors)
    meta["tied_aliases"] = tied_aliases  # hexa loader: re-link these names → primary

    meta_path = output_st.with_suffix(".meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"meta: {meta_path}")
    return meta


def _infer_meta(tensors: dict) -> dict:
    """Infer EngineAG hyperparams from tensor shapes."""
    tok_emb = tensors.get("tok_emb.weight")
    if tok_emb is None:
        return {"error": "tok_emb.weight not found"}
    vocab, d_model = tok_emb.shape

    # count layers (look for max layers.N prefix)
    n_layers = 0
    for k in tensors.keys():
        if k.startswith("layers."):
            idx = int(k.split(".")[1])
            n_layers = max(n_layers, idx + 1)

    # attention dims
    q_w = tensors.get("layers.0.attn.q_proj.weight")
    k_w = tensors.get("layers.0.attn.k_proj.weight")
    ffn_gate = tensors.get("layers.0.ffn.gate.weight")
    cell_pool = tensors.get("engine_g.cell_pool_init")

    return {
        "arch": "EngineAG",
        "vocab_size": vocab,
        "d_model": d_model,
        "n_layers": n_layers,
        "q_proj_out": q_w.shape[0] if q_w is not None else None,
        "kv_proj_out": k_w.shape[0] if k_w is not None else None,
        # n_heads = d_model // d_head; common: d_head=64, so n_heads=d_model/64
        "n_heads_assumed": d_model // 64,
        "n_kv_heads_assumed": (k_w.shape[0] // 64) if k_w is not None else None,
        "d_head_assumed": 64,
        "d_ff": ffn_gate.shape[0] if ffn_gate is not None else None,
        "tied_lm_head": "lm_head.weight" in tensors,
        "rope_theta_assumed": 10000.0,
        "norm_type": "RMSNorm (scale-only)",
        "ffn_type": "SwiGLU (gate + up + down)",
        "engine_g": {
            "present": cell_pool is not None,
            "n_cells": cell_pool.shape[0] if cell_pool is not None else None,
            "consciousness_dim": cell_pool.shape[1] if cell_pool is not None else None,
        },
        "notes": [
            "vocab_size=32000 but anima_chat.py uses ByteTokenizer (effective vocab ~259); "
            "rows 259..32000 of tok_emb are dead space (preserved for own-17 BPE migration).",
        ],
    }


def main():
    p = argparse.ArgumentParser(description="Convert .pt ckpt to .safetensors + meta.json")
    p.add_argument("input", nargs="?", help="input .pt path")
    p.add_argument("output", nargs="?", help="output .safetensors path")
    p.add_argument(
        "--default",
        action="store_true",
        help="convert default Phase 1A.1 ckpt (override input/output)",
    )
    args = p.parse_args()

    if args.default:
        inp, out = DEFAULT_INPUT, DEFAULT_OUTPUT
    else:
        if not args.input or not args.output:
            p.error("input and output paths required (or use --default)")
        inp = Path(args.input)
        out = Path(args.output)

    if not inp.exists():
        print(f"FAIL input not found: {inp}", file=sys.stderr)
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)

    meta = convert(inp, out)
    print(f"\n=== meta summary ===")
    print(json.dumps({k: v for k, v in meta.items() if k != "notes"}, indent=2, default=str))


if __name__ == "__main__":
    main()
