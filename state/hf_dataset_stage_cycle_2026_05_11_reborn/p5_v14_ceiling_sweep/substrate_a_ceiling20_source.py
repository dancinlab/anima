"""§68 robustness test — substrate A (cotrain) × ceiling=20 V14 strict.
If V14_PASS holds, §68 ★★★★★ is ceiling-robust; if V14_VIOLATED, ceiling-sensitive."""
from __future__ import annotations
import os, sys, json, math, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import mitosis_v5_port as mvp
import torch

CEILING = float(os.environ.get("CEILING", "20.0"))
print(f"[substrate A patch] ceiling clamp(max=10.0) → clamp(max={CEILING})", flush=True)

def _patched_inject_lorenz(self, cells: torch.Tensor) -> torch.Tensor:
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
    norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    scale_back = (norms / norms.clamp(max=CEILING))
    out = out / scale_back
    return out

mvp.MitosisV5Engine._inject_lorenz = _patched_inject_lorenz

OUT_DIR = ANIMA_ROOT / "state" / f"anima_p5_v14_sub_a_ceiling{int(CEILING)}_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Import run_max256, fire substrate A only
import run_max256 as M

log_path = OUT_DIR / "run_a.log"
log_f = open(log_path, "w")
def log(msg, _f=log_f):
    print(msg, flush=True); _f.write(msg + "\n"); _f.flush()

t0 = time.time()
sub_id = "A_phase2_cotrain"
log(f"=== §68 ROBUSTNESS — substrate A × ceiling={CEILING} === ts: {datetime.now(timezone.utc).isoformat()}")
log(f"V4_SEEDS={M.V4_SEEDS} max_cells={M.MAX_CELLS} n_turns={M.N_TURNS}")

result = M.fire_substrate_engine_ag(sub_id, M.SUBSTRATES[sub_id], log)
result["ts_complete"] = datetime.now(timezone.utc).isoformat()
result["total_elapsed_sec"] = time.time() - t0
result["ceiling_variant"] = CEILING

log(f"\n=== {sub_id} (ceiling={CEILING}) VERDICT: {result['verdict']} ===")
log(f"trained_phi: {result['trained_phi']:.2f}")
log(f"random_phi: {[f'{x:.2f}' for x in result['random_phi']]}")
log(f"n_random_beats: {result['n_random_beats']}/{result['n_random_total']}")
log(f"sign_test_p: {result['sign_test_p_two_sided']:.4f}")
log(f"total elapsed: {result['total_elapsed_sec']:.1f}s")

with (OUT_DIR / "result.json").open("w") as f:
    json.dump(result, f, indent=2, default=str)
log(f"[saved] {OUT_DIR / 'result.json'}")
log_f.close()
