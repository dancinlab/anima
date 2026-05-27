"""§69 robustness check — ceiling-binding finding at varied input magnitude."""
import os, sys, json, math
import torch
sys.path.insert(0, os.path.expanduser('~/core/anima/training'))
import mitosis_v5_port as mvp

stats = {"preclamp_norm_samples": [], "calls": 0, "ceiling_activations": 0, "floor_activations": 0,
         "near_ceiling": 0, "low_norm_zone": 0}

def _patched_inject_lorenz(self, cells):
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
    for v in out.norm(dim=-1).tolist():
        stats["preclamp_norm_samples"].append(v)
        if v > 10.0: stats["ceiling_activations"] += 1
        if v < 1e-8: stats["floor_activations"] += 1
        if 5.0 <= v <= 10.0: stats["near_ceiling"] += 1
        if 1e-6 <= v <= 1e-3: stats["low_norm_zone"] += 1
    norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    scale_back = (norms / norms.clamp(max=10.0))
    out = out / scale_back
    return out

mvp.MitosisV5Engine._inject_lorenz = _patched_inject_lorenz

INITIAL_CELLS, MAX_CELLS, CELL_DIM, HIDDEN_DIM, N_STEPS = 8, 64, 256, 3072, 120
SEEDS = [1042, 1043, 1044, 1045, 1046]
SCALE_VARIANTS = [0.1, 1.0, 10.0]  # § 69 falsifier check
out_results = {"variants": {}}

for hm_scale in SCALE_VARIANTS:
    variant_per_seed = []
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
            hidden_mean = torch.randn(1, CELL_DIM) * hm_scale
            engine.process(hidden_mean)
        n = len(stats["preclamp_norm_samples"])
        variant_per_seed.append({"seed": seed, "n": n,
                                 "ceil_rate": stats["ceiling_activations"]/max(1,n),
                                 "floor_rate": stats["floor_activations"]/max(1,n),
                                 "final_n_cells": engine.n_cells})
    total = sum(v["n"] for v in variant_per_seed)
    overall_ceil = sum(v["ceil_rate"]*v["n"] for v in variant_per_seed) / max(1, total)
    overall_floor = sum(v["floor_rate"]*v["n"] for v in variant_per_seed) / max(1, total)
    out_results["variants"][f"hm_scale_{hm_scale}"] = {
        "per_seed": variant_per_seed,
        "overall_ceiling_rate": overall_ceil,
        "overall_floor_rate": overall_floor,
        "total_samples": total,
    }
    print(f"hm_scale={hm_scale}: overall ceil={overall_ceil:.4%} floor={overall_floor:.4%} n={total}")

print()
print("=== robustness verdict ===")
rates = [out_results["variants"][f"hm_scale_{s}"]["overall_ceiling_rate"] for s in SCALE_VARIANTS]
out_results["robustness_verdict"] = {
    "ceiling_rates_across_scales": dict(zip([str(s) for s in SCALE_VARIANTS], rates)),
    "min_ceiling_rate": min(rates),
    "max_ceiling_rate": max(rates),
    "all_above_50pct": all(r > 0.5 for r in rates),
    "interpretation": ("CEILING_BINDING_ROBUST" if all(r > 0.5 for r in rates) else
                       "CEILING_BINDING_SCALE_DEPENDENT")
}
print(json.dumps(out_results["robustness_verdict"], indent=2))

import os
out_path = os.path.expanduser('~/core/anima/state/anima_p5_norm_clamp_prescreen_2026_05_11/robustness_results.json')
with open(out_path, "w") as f:
    json.dump(out_results, f, indent=2)
print(f"\nsaved → {out_path}")
