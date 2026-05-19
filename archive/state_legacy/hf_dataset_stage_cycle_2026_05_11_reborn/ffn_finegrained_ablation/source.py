"""§77 follow-up — fine-grained FFN ablation.
§77 found: FFN-only swap LA→B' splits trajectory (A1=1145 → A2=1491).
This script narrows: which FFN projection (gate/up/down) + which layers contribute most?
"""
from __future__ import annotations
import os, sys, json, math, time
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import torch
import mitosis_v5_port as mvp

CEILING = 15.0
def make_patched(C):
    def _p(self, cells):
        dx, dy, dz = self._lorenz_step()
        lorenz_vec = torch.tensor([dx, dy, dz], dtype=cells.dtype, device=cells.device)
        N, C_ = cells.shape
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
            noise = torch.randn(C_, dtype=cells.dtype, device=cells.device) * scale
            inject = min(3, C_)
            noise[:inject] = noise[:inject] + lorenz_vec[:inject] * 0.2
            out[i] = out[i] + noise
        norms = out.norm(dim=-1, keepdim=True).clamp(min=1e-8)
        scale_back = (norms / norms.clamp(max=C))
        out = out / scale_back
        return out
    return _p
mvp.MitosisV5Engine._inject_lorenz = make_patched(CEILING)

import run_max256 as M

LA_CKPT = "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt"
BP_CKPT = "/Users/ghost/core/anima/state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt"

OUT_DIR = ANIMA_ROOT / "state" / "anima_ffn_finegrained_ablation_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

la = torch.load(LA_CKPT, map_location="cpu", weights_only=False)
bp = torch.load(BP_CKPT, map_location="cpu", weights_only=False)
la_sd = la.get("state_dict", la.get("model"))
bp_sd = bp.get("state_dict", bp.get("model"))

def swap_keys(la_base, bp_keys_pred):
    """Make a state dict starting from la_base, overriding keys matching pred from bp_sd."""
    sd = dict(la_base)
    for k in bp_sd:
        if bp_keys_pred(k):
            sd[k] = bp_sd[k].clone()
    return sd

ABLATIONS = {
    "0_baseline_LA": lambda: dict(la_sd),
    "1_ffn_gate_only": lambda: swap_keys(la_sd, lambda k: ".ffn.gate" in k),
    "2_ffn_up_only": lambda: swap_keys(la_sd, lambda k: ".ffn.up" in k),
    "3_ffn_down_only": lambda: swap_keys(la_sd, lambda k: ".ffn.down" in k),
    "4_ffn_layer_0_only": lambda: swap_keys(la_sd, lambda k: k.startswith("layers.0.ffn")),
    "5_ffn_layer_12_only": lambda: swap_keys(la_sd, lambda k: k.startswith("layers.12.ffn")),
    "6_ffn_layer_23_only": lambda: swap_keys(la_sd, lambda k: k.startswith("layers.23.ffn")),
    "7_ffn_early_half": lambda: swap_keys(la_sd, lambda k: any(k.startswith(f"layers.{i}.ffn") for i in range(12))),
    "8_ffn_late_half": lambda: swap_keys(la_sd, lambda k: any(k.startswith(f"layers.{i}.ffn") for i in range(12, 24))),
}

results = {}
for ab_name, sd_factory in ABLATIONS.items():
    print(f"\n=== {ab_name} ===", flush=True)
    sd_variant = sd_factory()
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd_variant.items()}
    cfg = M.EngineAGConfig.phase2_cotrain_350m()
    model = M.EngineAGModel(cfg)
    miss, unexp = model.load_state_dict(sd_fp32, strict=False)
    print(f"  load: miss={len(miss)} unexp={len(unexp)}", flush=True)
    t0 = time.time()
    def silent_log(*args, **kwargs): pass
    traj = M.run_engine_ag_trajectory(
        model, label=ab_name, n_turns=M.N_TURNS,
        seed=M.TRAINED_PROMPT_SEED, max_cells=M.MAX_CELLS, log_fn=silent_log,
    )
    trained_phi = traj["snapshots"][-1]["iit_phi_unnorm_b16"]
    elapsed = time.time() - t0
    results[ab_name] = {
        "trained_phi": trained_phi,
        "final_n_cells": traj["final_n_cells"],
        "n_splits": traj["n_splits"],
        "elapsed_sec": elapsed,
    }
    attractor = "A1" if abs(trained_phi - 1144.92) < 1.0 else "A2" if abs(trained_phi - 1491.53) < 1.0 else "A_other"
    print(f"  trained_phi={trained_phi:.4f} cells={traj['final_n_cells']} splits={traj['n_splits']} elapsed={elapsed:.1f}s attractor={attractor}", flush=True)
    del model

with (OUT_DIR / "ffn_finegrained_results.json").open("w") as f:
    json.dump(results, f, indent=2)
print(f"\nsaved → {OUT_DIR / 'ffn_finegrained_results.json'}", flush=True)
