"""Expert-count sweep SMOKE for the MITOSIS-ARRAY harness (DISSOLVE · $0 local).

Runs a single forward + dispatch-entropy measurement of CLMArray for each
expert-count E in SWEEP_EXPERT_COUNTS = {4,8,16,32,64}, on random byte input.
Asserts, for every E:
  * forward produces finite logits of shape (B, V, T),
  * dispatch entropy is finite and in [0, ln E],
  * every expert is chip-fit (expert_param_count <= AKD1000_NODE_BUDGET).

This is the harness SMOKE (PR2): it verifies the forward + entropy plumbing
runs for all configs at $0 on a Mac CPU. It is NOT the verdict run -- the
uniform-null z-score sweep + monopoly-escape scaling is run_array_sweep.py (PR3).
Toy != scale (H_666): an untrained random-init forward's dispatch entropy is
intuition only, not a science result.

Run:  python3 CLM/model/array_smoke.py
Set ARRAY_SMOKE_JSON=<path> to dump the result JSON.
"""

from __future__ import annotations

import json
import math
import os
import sys

import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from array_moe import build_array, SWEEP_EXPERT_COUNTS, AKD1000_NODE_BUDGET  # noqa


def smoke_one(n_experts: int, seed: int = 42) -> dict:
    torch.manual_seed(seed)
    model = build_array(n_experts=n_experts)
    B, T = 4, 64
    tokens = torch.randint(0, 256, (B, T))
    targets = torch.randint(0, 256, (B, T))
    out = model(tokens, targets)

    logits = out["logits"]
    H = out["dispatch_entropy_nats"]
    Hmax = math.log(n_experts)
    ok_shape = tuple(logits.shape) == (B, 256, T)
    ok_finite = bool(torch.isfinite(logits).all()) and math.isfinite(H)
    ok_range = (-1e-6 <= H <= Hmax + 1e-6)
    chip_fit = model.expert_chip_fit()
    expert_params = model.moe.expert_param_count()

    return {
        "n_experts": n_experts,
        "params_total": model.num_params(),
        "expert_params": expert_params,
        "chip_fit": chip_fit,
        "akd1000_budget": AKD1000_NODE_BUDGET,
        "dispatch_counts": [int(c) for c in out["dispatch_counts"]],
        "dispatch_entropy_nats": round(H, 5),
        "max_entropy_nats": round(Hmax, 5),
        "norm_entropy": round(out["dispatch_norm_entropy"], 5),
        "n_active_experts": out["n_active_experts"],
        "ce_loss": round(float(out["ce_loss"].detach()), 5),
        "pass": bool(ok_shape and ok_finite and ok_range and chip_fit),
        "checks": {"shape": ok_shape, "finite": ok_finite,
                   "entropy_range": ok_range, "chip_fit": chip_fit},
    }


def main() -> None:
    results = []
    print("MITOSIS-ARRAY harness smoke (DISSOLVE) -- $0 Mac CPU, toy/intuition",
          flush=True)
    print(f"torch={torch.__version__}  AKD1000_budget={AKD1000_NODE_BUDGET}",
          flush=True)
    all_pass = True
    for E in SWEEP_EXPERT_COUNTS:
        r = smoke_one(E)
        results.append(r)
        all_pass = all_pass and r["pass"]
        print(
            f"E={E:>2}: params={r['params_total']:>8} "
            f"expert={r['expert_params']:>6}({'fit' if r['chip_fit'] else 'OVER'}) "
            f"H={r['dispatch_entropy_nats']:.4f}/{r['max_entropy_nats']:.4f} "
            f"(norm {r['norm_entropy']:.3f}) active={r['n_active_experts']}/{E} "
            f"ce={r['ce_loss']:.3f} {'PASS' if r['pass'] else 'FAIL'}",
            flush=True,
        )
    print(f"\nSMOKE {'PASS' if all_pass else 'FAIL'} "
          f"({sum(r['pass'] for r in results)}/{len(results)} configs)",
          flush=True)

    dest = os.environ.get("ARRAY_SMOKE_JSON")
    if dest:
        with open(dest, "w") as f:
            json.dump({"results": results, "all_pass": all_pass,
                       "torch": torch.__version__}, f, indent=2)
        print(f"wrote JSON -> {dest}", flush=True)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
