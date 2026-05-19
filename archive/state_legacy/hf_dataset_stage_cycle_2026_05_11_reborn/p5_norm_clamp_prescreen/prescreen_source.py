"""
P5 norm-clamp pre-screen — instrumentation-only, cycle 2026-05-11.
Monkey-patches MitosisV5Engine._inject_lorenz to log pre-clamp per-cell norms.
"""
import os, sys, json, math
import torch

sys.path.insert(0, os.path.expanduser('~/core/anima/training'))
import mitosis_v5_port as mvp

stats = {"preclamp_norm_samples": [], "calls": 0,
         "ceiling_activations": 0, "floor_activations": 0,
         "near_ceiling": 0, "low_norm_zone": 0}

def _patched_inject_lorenz(self, cells: torch.Tensor) -> torch.Tensor:
    stats["calls"] += 1
    dx, dy, dz = self._lorenz_step()
    lorenz_vec = torch.tensor([dx, dy, dz], dtype=cells.dtype, device=cells.device)
    N, C = cells.shape
    if self.lorenz_auto_calibrate and N > 0:
        with torch.no_grad():
            mean_p_norm = float(cells.norm(dim=-1).mean().item())
        base_scale = self.lorenz_scale * max(mean_p_norm, 1e-6) * self.lorenz_calibration_factor
    else:
        base_scale = self.lorenz_scale
    out = cells.clone()
    for i in range(N):
        phase = (i * 2.0 * math.pi) / max(N, 1)
        scale = base_scale * (1.0 + 0.3 * math.sin(phase + self.step_count * 0.1))
        noise = torch.randn(C, dtype=cells.dtype, device=cells.device) * scale
        inject = min(3, C)
        noise[:inject] = noise[:inject] + lorenz_vec[:inject] * 0.2
        out[i] = out[i] + noise
    # LOG pre-clamp per-cell norms
    pc_norms = out.norm(dim=-1).tolist()
    for v in pc_norms:
        stats["preclamp_norm_samples"].append(v)
        if v > 10.0: stats["ceiling_activations"] += 1
        if v < 1e-8: stats["floor_activations"] += 1
        if 5.0 <= v <= 10.0: stats["near_ceiling"] += 1
        if 1e-6 <= v <= 1e-3: stats["low_norm_zone"] += 1
    # original clamp
    norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    scale_back = (norms / norms.clamp(max=10.0))
    out = out / scale_back
    return out

mvp.MitosisV5Engine._inject_lorenz = _patched_inject_lorenz

INITIAL_CELLS, MAX_CELLS, CELL_DIM, HIDDEN_DIM, N_STEPS = 8, 64, 256, 3072, 120
SEEDS = [1042, 1043, 1044, 1045, 1046]
results = {"phase2_lifts_applied": ["v5_port_clamp_activation_prescreen"],
           "n_seeds": len(SEEDS), "seeds": SEEDS, "n_steps_per_seed": N_STEPS, "per_seed": []}

for seed in SEEDS:
    for k in stats:
        if isinstance(stats[k], list): stats[k].clear()
        else: stats[k] = 0
    torch.manual_seed(seed)
    cell_pool = torch.randn(INITIAL_CELLS, CELL_DIM, dtype=torch.float32) * 0.1
    c_to_h = torch.nn.Linear(CELL_DIM, HIDDEN_DIM, bias=False)
    with torch.no_grad():
        c_to_h.weight.data = torch.randn_like(c_to_h.weight) * (1.0 / math.sqrt(CELL_DIM))
    for p in c_to_h.parameters(): p.requires_grad = False
    engine = mvp.MitosisV5Engine(cell_pool=cell_pool, c_to_h=c_to_h,
                                  initial_cells=INITIAL_CELLS, max_cells=MAX_CELLS)
    for p in engine.parameters(): p.requires_grad = False
    engine.eval()
    for step in range(N_STEPS):
        hidden_mean = torch.randn(1, CELL_DIM) * 1.0
        engine.process(hidden_mean)
    norms_sorted = sorted(stats["preclamp_norm_samples"])
    n = len(norms_sorted)
    p50 = norms_sorted[n//2] if n else 0
    p90 = norms_sorted[int(n*0.90)] if n else 0
    p99 = norms_sorted[int(n*0.99)] if n else 0
    nmax = norms_sorted[-1] if n else 0
    nmin = norms_sorted[0] if n else 0
    per_seed = {"seed": seed, "n_calls": stats["calls"], "n_norm_samples": n,
                "ceiling_activations": stats["ceiling_activations"],
                "ceiling_activation_rate": stats["ceiling_activations"]/max(1,n),
                "floor_activations": stats["floor_activations"],
                "floor_activation_rate": stats["floor_activations"]/max(1,n),
                "near_ceiling_5_to_10": stats["near_ceiling"],
                "near_ceiling_rate": stats["near_ceiling"]/max(1,n),
                "low_norm_zone": stats["low_norm_zone"],
                "low_norm_zone_rate": stats["low_norm_zone"]/max(1,n),
                "norm_p50": p50, "norm_p90": p90, "norm_p99": p99,
                "norm_max": nmax, "norm_min": nmin,
                "final_n_cells": engine.n_cells}
    results["per_seed"].append(per_seed)
    print(f"seed={seed} n={n} norm[p50={p50:.4f} p90={p90:.4f} p99={p99:.4f} max={nmax:.4f} min={nmin:.4e}] "
          f"ceil={per_seed['ceiling_activations']}={per_seed['ceiling_activation_rate']:.4%} "
          f"floor={per_seed['floor_activations']}={per_seed['floor_activation_rate']:.4%} "
          f"final_n_cells={engine.n_cells}")

total = sum(s["n_norm_samples"] for s in results["per_seed"])
total_ceil = sum(s["ceiling_activations"] for s in results["per_seed"])
total_floor = sum(s["floor_activations"] for s in results["per_seed"])
total_near = sum(s["near_ceiling_5_to_10"] for s in results["per_seed"])
total_low = sum(s["low_norm_zone"] for s in results["per_seed"])
results["aggregate"] = {
    "total_norm_samples": total,
    "ceiling_activation_rate": total_ceil/max(1,total),
    "floor_activation_rate": total_floor/max(1,total),
    "near_ceiling_rate": total_near/max(1,total),
    "low_norm_zone_rate": total_low/max(1,total),
    "verdict": ("CEILING_BINDING" if total_ceil > 0.01*total else
                "CEILING_NEAR_BUT_NOT_BINDING" if total_near > 0.05*total else
                "BOTH_CLAMPS_INACTIVE_IN_REGIME"),
}
print()
print("=== aggregate verdict ===")
print(json.dumps(results["aggregate"], indent=2))

out_path = os.path.expanduser('~/core/anima/state/anima_p5_norm_clamp_prescreen_2026_05_11/prescreen_results.json')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\nsaved → {out_path}")
