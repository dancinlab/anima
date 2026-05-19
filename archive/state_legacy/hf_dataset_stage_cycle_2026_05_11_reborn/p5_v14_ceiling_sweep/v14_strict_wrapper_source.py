"""P5 V14-strict ceiling-variant — eval-time ceiling=20 vs §69 baseline ceiling=10.

Monkey-patches mitosis_v5_port.MitosisV5Engine._inject_lorenz to use clamp(max=20.0)
instead of clamp(max=10.0). Otherwise IDENTICAL to run_b.py — same substrate, same
seeds, same N_TURNS, same MAX_CELLS. Compares V14 strict verdict on BG-LA pretrain
ckpt with relaxed ceiling.
"""
from __future__ import annotations
import os, sys, json, math, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_b_no_cotrain_2026_05_10"))

# ── PATCH mitosis_v5_port BEFORE run_b imports it ───────────────────
import mitosis_v5_port as mvp
import torch

CEILING = float(os.environ.get("CEILING", "20.0"))
print(f"[P5 ceiling-variant patch] ceiling clamp(max=10.0) → clamp(max={CEILING})", flush=True)

_orig_inject_lorenz = mvp.MitosisV5Engine._inject_lorenz

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
    # PATCHED: ceiling = CEILING (env-configurable) instead of 10.0
    norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    scale_back = (norms / norms.clamp(max=CEILING))
    out = out / scale_back
    return out

mvp.MitosisV5Engine._inject_lorenz = _patched_inject_lorenz

# Output dir
OUT_DIR = ANIMA_ROOT / "state" / f"anima_p5_v14_ceiling{int(CEILING)}_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Import run_b WITH patched mitosis_v5_port
import run_b
# Redirect output dir
run_b.THIS_DIR = OUT_DIR

# Run
print(f"[P5 ceiling={CEILING}] firing V14 strict on BG-LA substrate (output: {OUT_DIR})", flush=True)
t0 = time.time()
try:
    run_b.main()
    print(f"[P5 ceiling={CEILING}] DONE elapsed={(time.time()-t0)/60:.1f}min", flush=True)
except Exception as e:
    print(f"[P5 ceiling={CEILING}] FAILED: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
