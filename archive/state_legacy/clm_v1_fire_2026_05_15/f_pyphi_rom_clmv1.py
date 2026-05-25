"""F-PYPHI-Φ-FORMAL n=3-6 RoM on .clm v1 recovered ckpt (cycle 90).

Adapt of state/verify_d_2026_05_15/pyphi_rom_cycle.py for ClmV1Model cell structure
(cells.{i}.ln/fc1/fc2 vs v5-mitosis cells.{i}.ln1/ln2).

Spec (spec_frozen falsifier #6 F-PYPHI-Φ-FORMAL):
  ≥1 (n, seed) Φ ≥ 0.5 strict on n=3-6 RoM → 🔵 SUPPORTED-FORMAL unlock (g_verdict_tier_blue)

n=3,4 fast (~2hr), n=5 (~5hr), n=6 (~13hr) — full ~20hr. Run n=3,4,5 foreground;
n=6 separate background if n=3-5 inconclusive.

Honest C3:
  - PyPhi 1.2.0 small-N limit (full 64-cell formal IIT impossible)
  - RoM = lossy top-correlated projection
  - synthetic perturbation dynamics, not real chat
  - state-space ergodicity issue carry (V8 B-bio Lorenz-only unlock)
"""
import os
import sys
import json
import time
from collections import Counter

import numpy as np
import torch

os.environ["PYPHI_WELCOME_OFF"] = "yes"
import pyphi

pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1

CKPT = "/Users/ghost/core/anima/state/clm_v1_fire_2026_05_15/ckpts/ckpt_clm_v1_fire_final.pt"
OUT = "/Users/ghost/core/anima/state/clm_v1_fire_2026_05_15/f_pyphi_rom_result.json"


def load_cell_signatures(ckpt_path):
    """ClmV1Model per-cell composite signature from ln+fc1+fc2 weights."""
    ck = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    sd = ck.get("model_state_dict", ck)
    cell_idx = 0
    sigs = []
    while True:
        keys = [
            f"cells.{cell_idx}.ln.weight",
            f"cells.{cell_idx}.fc1.weight",
            f"cells.{cell_idx}.fc2.weight",
        ]
        if not all(k in sd for k in keys):
            break
        # composite: ln.weight (768) + fc1.weight row-mean (1024) + fc2.weight col-mean (768)
        ln = sd[keys[0]].float().flatten()
        fc1 = sd[keys[1]].float().mean(dim=1)  # (1024,)
        fc2 = sd[keys[2]].float().mean(dim=0)  # (768,)
        sig = torch.cat([ln, fc1, fc2])
        sigs.append(sig)
        cell_idx += 1
    if not sigs:
        return None
    return torch.stack(sigs)


def select_top_correlated(sigs, n_select=3):
    sn = sigs / (sigs.norm(dim=1, keepdim=True) + 1e-9)
    cm = sn @ sn.t()
    cm.fill_diagonal_(0)
    flat = cm.flatten().argmax().item()
    i, j = flat // cm.shape[0], flat % cm.shape[0]
    sel = [int(i), int(j)]
    while len(sel) < n_select:
        sc = cm[sel].sum(dim=0)
        for s in sel:
            sc[s] = -1
        sel.append(int(sc.argmax().item()))
    return sel


def sample_cell_dynamics(sigs, selected, n_samples=500, seed=42):
    torch.manual_seed(seed)
    sub = sigs[selected]
    N, D = sub.shape
    states = []
    for _ in range(n_samples):
        x = torch.randn(D)
        tens = (sub @ x) / (sub.norm(dim=1) * x.norm() + 1e-9)
        thr = tens.median()
        states.append(tuple((tens > thr).int().tolist()))
    return states


def states_to_tpm(states, n):
    ns = 2 ** n
    tc = np.zeros((ns, ns))
    for i in range(len(states) - 1):
        si = sum(b << k for k, b in enumerate(states[i]))
        ni = sum(b << k for k, b in enumerate(states[i + 1]))
        tc[si, ni] += 1
    tpm = np.zeros((ns, n))
    for si in range(ns):
        rt = tc[si].sum()
        if rt == 0:
            for i in range(n):
                tpm[si, i] = (si >> i) & 1
            continue
        for i in range(n):
            c1 = sum(tc[si, nidx] for nidx in range(ns) if (nidx >> i) & 1)
            tpm[si, i] = c1 / rt
    return tpm, tc


def measure_phi(tpm, state):
    N = tpm.shape[1]
    cm = (np.ones((N, N)) - np.eye(N)).astype(int)
    labels = tuple(f"C{i}" for i in range(N))
    try:
        net = pyphi.Network(tpm, cm=cm, node_labels=labels)
        sub = pyphi.Subsystem(net, tuple(state), range(N))
        sia = pyphi.compute.sia(sub)
        return float(sia.phi), "OK"
    except Exception as e:
        return None, f"ERROR: {type(e).__name__}: {str(e)[:200]}"


def main():
    t0 = time.time()
    print("=== F-PYPHI-Φ-FORMAL RoM on .clm v1 recovered ckpt ===")
    sigs = load_cell_signatures(CKPT)
    if sigs is None:
        print("FATAL: no cell signatures")
        sys.exit(1)
    print(f"  {sigs.shape[0]} cells, sig dim {sigs.shape[1]}")

    n_list = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [3, 4, 5]
    seeds = [42, 1234, 5678]
    result = {
        "falsifier": "F-PYPHI-Φ-FORMAL",
        "cycle": "90 (2026-05-15)",
        "pyphi_version": pyphi.__version__,
        "ckpt": "ckpt_clm_v1_fire_final.pt (64 cells)",
        "spec": "≥1 (n,seed) Φ ≥ 0.5 strict → 🔵 SUPPORTED-FORMAL unlock",
        "n_list": n_list,
        "seeds": seeds,
        "measurements": [],
    }
    best_phi = -1.0
    best_cfg = None
    for n in n_list:
        sel = select_top_correlated(sigs, n_select=n)
        for seed in seeds:
            ts = time.time()
            states = sample_cell_dynamics(sigs, sel, n_samples=500, seed=seed)
            uniq = len(set(states))
            tpm, tc = states_to_tpm(states, n)
            top = Counter(states).most_common(1)[0][0]
            phi, status = measure_phi(tpm, top)
            wall = time.time() - ts
            m = {
                "n": n, "seed": seed, "selected_cells": sel,
                "unique_states": uniq, "total_states": 2 ** n,
                "top_state": list(top), "phi": phi, "status": status,
                "wall_sec": round(wall, 1),
            }
            result["measurements"].append(m)
            print(f"  n={n} seed={seed}: Φ={phi} uniq={uniq}/{2**n} ({wall:.1f}s) {status}")
            if phi is not None and phi > best_phi:
                best_phi = phi
                best_cfg = {"n": n, "seed": seed}
            # Save incrementally
            with open(OUT, "w") as f:
                json.dump(result, f, indent=2, default=str)

    pass_strict = best_phi >= 0.5
    result["best_phi"] = best_phi
    result["best_cfg"] = best_cfg
    result["verdict"] = "PASS" if pass_strict else "FAIL"
    result["verdict_note"] = (
        f"best Φ={best_phi:.4f} {'≥' if pass_strict else '<'} 0.5 strict → "
        f"{'🔵 SUPPORTED-FORMAL unlock' if pass_strict else 'AT-RISK (state-space ergodicity issue carry, V8 B-bio Lorenz-only pattern)'}"
    )
    result["wall_total_sec"] = round(time.time() - t0, 1)
    result["honest_c3"] = [
        "1. PyPhi 1.2.0 small-N (full 64-cell formal IIT computationally impossible) — RoM top-correlated projection lossy",
        "2. synthetic random perturbation dynamics, not real chat token-stream",
        "3. state-space ergodicity issue carry — V8 B-bio Phase 3 showed only Lorenz-class chaotic dynamics unlock Φ≥0.5; static cell weights may saturate near 0",
        "4. anima Φ★ proxy = 4.34 (mean pairwise + log(N+1)) is a DIFFERENT phenomenon from formal IIT Φ — not directly comparable",
        f"5. FAIL here does NOT negate 7/7 measured battery — F-PYPHI is the formal-tier gate (🔵), 7/7 = 🟢 SUPPORTED-STRONG empirical stands",
    ]
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n=== F-PYPHI verdict: {result['verdict']} (best Φ={best_phi:.4f}) ===")
    print(result["verdict_note"])
    print(f"saved {OUT} (wall {result['wall_total_sec']}s)")


if __name__ == "__main__":
    main()
