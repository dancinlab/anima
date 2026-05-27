#!/usr/bin/env python3
"""Inspect a torch .pt file: state_dict keys, shapes, and architecture inference.

Usage: inspect_pt.py <path>
Output: JSON dict on stdout, human summary on stderr.
"""
import sys
import json
import hashlib
import os
import torch


def sha256_file(path: str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def categorize(obj):
    if isinstance(obj, torch.Tensor):
        return {"_kind": "tensor", "shape": list(obj.shape), "dtype": str(obj.dtype)}
    if isinstance(obj, dict):
        return {k: categorize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [categorize(x) for x in obj]
    return repr(obj)[:200]


def flatten_state_dict(d, prefix=""):
    """Yield (full_key, tensor) for tensors in nested dict."""
    if isinstance(d, torch.Tensor):
        yield prefix, d
        return
    if isinstance(d, dict):
        for k, v in d.items():
            sub = f"{prefix}.{k}" if prefix else str(k)
            yield from flatten_state_dict(v, sub)


def main():
    path = sys.argv[1]
    size = os.path.getsize(path)
    sha = sha256_file(path)
    print(f"[inspect] path={path} size={size} sha256={sha}", file=sys.stderr)

    out = {
        "path": path,
        "size_bytes": size,
        "sha256": sha,
    }

    # Try torch.load
    try:
        obj = torch.load(path, map_location="cpu", weights_only=False)
        out["torch_load_pass"] = True
        out["top_level_kind"] = type(obj).__name__
    except Exception as e:
        out["torch_load_pass"] = False
        out["torch_load_error"] = f"{type(e).__name__}: {e}"
        print(json.dumps(out, indent=2))
        return

    # Top-level summary
    top_keys = []
    if isinstance(obj, dict):
        top_keys = list(obj.keys())
        out["top_level_keys"] = [str(k) for k in top_keys][:30]
        # Find state_dict-shaped sub-dict
        if "model_state" in obj:
            sd_root = obj["model_state"]
            out["state_dict_path"] = "model_state"
        elif "state_dict" in obj:
            sd_root = obj["state_dict"]
            out["state_dict_path"] = "state_dict"
        elif "model" in obj:
            sd_root = obj["model"]
            out["state_dict_path"] = "model"
        else:
            sd_root = obj
            out["state_dict_path"] = "<root>"
        # Step / metadata if present
        for k in ("step", "epoch", "iter", "config", "n_cells", "cells", "phi"):
            if k in obj and k not in (sd_root if isinstance(sd_root, dict) else {}):
                v = obj[k]
                if isinstance(v, torch.Tensor):
                    out[k] = v.tolist() if v.numel() < 10 else f"<tensor {list(v.shape)}>"
                else:
                    try:
                        json.dumps(v)
                        out[k] = v
                    except Exception:
                        out[k] = repr(v)[:200]
    else:
        sd_root = obj
        out["state_dict_path"] = "<root>"

    # Flatten and collect tensor info
    tensors = list(flatten_state_dict(sd_root))
    out["state_dict_keys_count"] = len(tensors)
    keys_with_shape = [(k, list(t.shape), str(t.dtype), t.numel()) for k, t in tensors]
    out["first_30_keys"] = keys_with_shape[:30]
    out["last_10_keys"] = keys_with_shape[-10:]

    total_params = sum(t.numel() for _, t in tensors)
    out["total_params"] = total_params
    out["total_params_M"] = round(total_params / 1e6, 3)

    # Architecture detection
    arch = {}
    keys = [k for k, _ in tensors]

    # tok_emb
    for k, t in tensors:
        if "tok_emb" in k or k.endswith(".weight") and "tok" in k.lower():
            arch["tok_emb_shape"] = list(t.shape)
            if len(t.shape) == 2:
                arch["vocab_inferred"] = t.shape[0]
                arch["d_model_inferred"] = t.shape[1]
            break

    # engine_a / engine_g presence
    arch["engine_a_present"] = any("engine_a" in k for k in keys)
    arch["engine_g_present"] = any("engine_g" in k for k in keys)
    arch["head_a_present"] = any("head_a" in k for k in keys)
    arch["head_g_present"] = any("head_g" in k for k in keys)
    arch["memory_gru_present"] = any("memory" in k and ("weight_ih" in k or "weight_hh" in k) for k in keys)
    arch["c_attn_present"] = any("c_attn" in k for k in keys)
    arch["mlp_present"] = any(".mlp." in k for k in keys)
    arch["ln_f_present"] = any(k.endswith("ln_f.weight") or "ln_f" in k for k in keys)

    # Cell-style prefix detection
    cell_prefixes = set()
    for k in keys:
        # Patterns like cells.0.mind.engine_a... or cell_0.mind...
        parts = k.split(".")
        if parts and parts[0] in ("cells", "cell_list"):
            if len(parts) > 1 and parts[1].isdigit():
                cell_prefixes.add(parts[1])
        if parts and parts[0].startswith("cell_") and parts[0][5:].isdigit():
            cell_prefixes.add(parts[0])
    arch["cell_prefix_count"] = len(cell_prefixes)
    arch["cell_prefix_sample"] = sorted(cell_prefixes, key=lambda x: int(x) if x.isdigit() else int(x.split("_")[1]))[:5]

    # n_layers — count blocks
    block_ids = set()
    for k in keys:
        parts = k.split(".")
        for i, p in enumerate(parts):
            if p == "blocks" or p == "h" or p == "layers":
                if i + 1 < len(parts) and parts[i + 1].isdigit():
                    block_ids.add(int(parts[i + 1]))
    arch["n_blocks_inferred"] = max(block_ids) + 1 if block_ids else None

    out["architecture"] = arch

    # Print JSON summary
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
