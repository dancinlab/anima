#!/usr/bin/env python3
"""Inspect the non-state-dict metadata in cells64/cells128 .pt files."""
import sys
import json
import torch

path = sys.argv[1]
obj = torch.load(path, map_location="cpu", weights_only=False)
print(f"=== {path} ===")
print(f"top-level keys: {list(obj.keys())}")
print()

for k in ("step", "phase", "config", "mitosis_status", "phi_history"):
    if k not in obj:
        continue
    v = obj[k]
    print(f"--- {k} ---")
    if isinstance(v, list):
        if len(v) > 20:
            print(f"  list[{len(v)}], first 5 = {v[:5]}, last 5 = {v[-5:]}")
            if all(isinstance(x, (int, float)) for x in v[:10]):
                arr = torch.tensor(v, dtype=torch.float32)
                print(f"  stats: min={arr.min().item():.4f} max={arr.max().item():.4f} mean={arr.mean().item():.4f}")
        else:
            print(f"  {v}")
    elif isinstance(v, dict):
        for kk, vv in v.items():
            tag = ""
            if isinstance(vv, torch.Tensor):
                tag = f"<tensor {list(vv.shape)} {vv.dtype}>"
            elif isinstance(vv, list):
                tag = f"<list len={len(vv)}, sample={vv[:3]}>"
            else:
                try:
                    json.dumps(vv)
                    tag = repr(vv)[:200]
                except Exception:
                    tag = f"<{type(vv).__name__}>"
            print(f"  {kk}: {tag}")
    else:
        print(f"  {v!r}"[:300])
    print()

# Check optimizer keys (just count)
if "optimizer_state" in obj:
    opt = obj["optimizer_state"]
    if isinstance(opt, dict):
        print(f"--- optimizer_state ---")
        print(f"  keys: {list(opt.keys())}")
        if "state" in opt:
            print(f"  state-param-count: {len(opt['state'])}")
        if "param_groups" in opt:
            print(f"  param_groups: {len(opt['param_groups'])}")

# loss_ensemble_state
if "loss_ensemble_state" in obj:
    le = obj["loss_ensemble_state"]
    print(f"--- loss_ensemble_state ---")
    if isinstance(le, dict):
        for kk, vv in le.items():
            tag = repr(vv)[:120] if not isinstance(vv, torch.Tensor) else f"<tensor {list(vv.shape)}>"
            print(f"  {kk}: {tag}")
    else:
        print(f"  {repr(le)[:200]}")
