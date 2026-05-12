#!/usr/bin/env python3
"""F1 cycle 1 XMETA3 N=3 seed CPU dispatch wrapper.

Runs ready/bench/bench_phi_hypotheses_LEGACY.py:run_XMETA3_omega4_plus_metacog()
with 3 distinct seeds (42, 1337, 2718) on CPU. Persists per-seed Phi + wallclock.

raw 86 cost: $0 vendor=local-cpu (Mac).
"""
import os
import sys
import json
import time

# Force CPU-only (defensive; CUDA not available on this Mac anyway)
os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Add bench module path + LEGACY bench file path
WORKTREE_SRC = "/Users/ghost/core/anima/ready/.claude/worktrees/agent-abb59ac1/anima/src"
BENCH_DIR = "/Users/ghost/core/anima/ready/bench"
sys.path.insert(0, WORKTREE_SRC)
sys.path.insert(0, BENCH_DIR)

import torch
import numpy as np

# Import target hypothesis fn from LEGACY bench
import importlib.util
spec = importlib.util.spec_from_file_location(
    "bench_phi_hypotheses_LEGACY",
    os.path.join(BENCH_DIR, "bench_phi_hypotheses_LEGACY.py"),
)
bench_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bench_mod)

run_XMETA3 = bench_mod.run_XMETA3_omega4_plus_metacog

SEEDS = [42, 1337, 2718]
STEPS = 100  # default per LEGACY bench

results = []
device_str = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[xmeta3_n3] device={device_str} seeds={SEEDS} steps={STEPS}", flush=True)

for seed in SEEDS:
    torch.manual_seed(seed)
    np.random.seed(seed)
    print(f"[xmeta3_n3] starting seed={seed} t={time.strftime('%H:%M:%S')}", flush=True)
    t0 = time.time()
    res = run_XMETA3(steps=STEPS, dim=64, hidden=128)
    elapsed = time.time() - t0
    rec = {
        "seed": seed,
        "hypothesis": res.hypothesis,
        "name": res.name,
        "phi_final": float(res.phi),
        "total_mi": float(res.total_mi),
        "min_partition_mi": float(res.min_partition_mi),
        "integration": float(res.integration),
        "complexity": float(res.complexity),
        "elapsed_sec_internal": float(res.elapsed_sec),
        "wallclock_sec": elapsed,
        "final_cells": res.extra.get("final_cells") if res.extra else None,
    }
    results.append(rec)
    print(f"[xmeta3_n3] seed={seed} phi={res.phi:.4f} cells={rec['final_cells']} wall={elapsed:.2f}s", flush=True)

out = {
    "task": "F1_cycle1_xmeta3_n3",
    "device": device_str,
    "seeds": SEEDS,
    "steps": STEPS,
    "results": results,
    "phi_min": min(r["phi_final"] for r in results),
    "phi_max": max(r["phi_final"] for r in results),
    "phi_mean": sum(r["phi_final"] for r in results) / len(results),
    "vendor": "local-cpu",
    "cost_usd": 0.0,
}

out_path = "/Users/ghost/core/anima/state/f1_cycle1_xmeta3_n3/results.json"
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print(f"[xmeta3_n3] OK wrote {out_path}")
print(f"[xmeta3_n3] phi range: [{out['phi_min']:.4f}, {out['phi_max']:.4f}] mean={out['phi_mean']:.4f}")
