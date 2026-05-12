"""EngineAG 4-substrate × 4-ceiling V14 strict matrix sweep — Mac CPU sequential.
Substrates: BG-LA pretrain, BG-LB pretrain, BG-LA cotrain (B'), BG-LB cotrain (A).
Ceilings: 10, 15, 20, 1000. Already-measured cells skipped.
"""
from __future__ import annotations
import os, sys, json, math, time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

import torch
import mitosis_v5_port as mvp

_orig_inject_lorenz = mvp.MitosisV5Engine._inject_lorenz

def make_patched_inject(CEILING):
    def _patched(self, cells):
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
    return _patched

import run_max256 as M

SUBSTRATES = {
    "BG_LA_pretrain": {
        "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt",
        "schema": "engine_ag",
        "arch": "BG-LA pretrain (12k steps, 243MB corpus)",
        "paradigm": "la_pretrain",
    },
    "BG_LB_pretrain": {
        "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt",
        "schema": "engine_ag",
        "arch": "BG-LB pretrain (8k steps, 427MB corpus)",
        "paradigm": "lb_pretrain",
    },
    "BG_LA_cotrain_Bprime": {
        "ckpt": "/Users/ghost/core/anima/state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt",
        "schema": "engine_ag",
        "arch": "BG-LA cotrain B' (5260 steps from BG-LA, cost-cap halt)",
        "paradigm": "la_cotrain",
    },
    "BG_LB_cotrain_A": {
        "ckpt": "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt",
        "schema": "engine_ag",
        "arch": "BG-LB cotrain (substrate A, 6000 steps from BG-LB)",
        "paradigm": "lb_cotrain",
    },
}

# Already-measured cells from prior § (skip these to save time)
SKIP = {
    ("BG_LA_pretrain", 10.0),     # state/anima_v14_max256_b_no_cotrain_2026_05_10
    ("BG_LA_pretrain", 20.0),     # eval-time ceiling=20 done in §69 ext (B at 20)
    ("BG_LB_pretrain", 10.0),     # §71
    ("BG_LB_pretrain", 20.0),     # §72
    ("BG_LA_cotrain_Bprime", 10.0),  # result_b_prime_ceiling10
    ("BG_LA_cotrain_Bprime", 20.0),  # result_b_prime_ceiling20
    ("BG_LB_cotrain_A", 10.0),    # state/anima_v14_max256_cap_free_multi_2026_05_10/result_A_phase2_cotrain
    ("BG_LB_cotrain_A", 15.0),    # state/anima_p5_v14_sub_a_ceiling15_2026_05_11
    ("BG_LB_cotrain_A", 20.0),    # state/anima_p5_v14_sub_a_ceiling20_2026_05_11
}

CEILINGS = [10.0, 15.0, 20.0, 1000.0]
OUT_DIR = ANIMA_ROOT / "state" / "anima_engine_ag_matrix_sweep_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)
summary = {}

for sub_id, sub in SUBSTRATES.items():
    if not os.path.exists(sub["ckpt"]):
        print(f"[skip {sub_id}] ckpt missing {sub['ckpt']}", flush=True)
        continue
    summary[sub_id] = {}
    for ceiling in CEILINGS:
        cell_key = (sub_id, ceiling)
        if cell_key in SKIP:
            print(f"[skip {sub_id} × {ceiling}] already measured in prior §", flush=True)
            continue
        # patch
        if ceiling == 10.0:
            mvp.MitosisV5Engine._inject_lorenz = _orig_inject_lorenz
        else:
            mvp.MitosisV5Engine._inject_lorenz = make_patched_inject(ceiling)
        # log
        run_log = OUT_DIR / f"{sub_id}_ceiling{int(ceiling)}.log"
        log_f = open(run_log, "w")
        def log(msg, _f=log_f):
            print(msg, flush=True); _f.write(msg + "\n"); _f.flush()
        t0 = time.time()
        log(f"=== {sub_id} × ceiling={ceiling} === ts: {datetime.now(timezone.utc).isoformat()}")
        try:
            result = M.fire_substrate_engine_ag(sub_id, sub, log)
            result["ts_complete"] = datetime.now(timezone.utc).isoformat()
            result["total_elapsed_sec"] = time.time() - t0
            result["ceiling_variant"] = ceiling
            log(f"VERDICT: {result['verdict']} trained_phi={result['trained_phi']:.2f} n_random_beats={result['n_random_beats']}/{result['n_random_total']} sign_p={result['sign_test_p_two_sided']:.4f}")
            with (OUT_DIR / f"{sub_id}_ceiling{int(ceiling)}_result.json").open("w") as f:
                json.dump(result, f, indent=2, default=str)
            summary[sub_id][f"ceiling_{int(ceiling)}"] = {
                "verdict": result["verdict"],
                "trained_phi": result["trained_phi"],
                "n_random_beats": result["n_random_beats"],
                "sign_test_p": result["sign_test_p_two_sided"],
            }
        except Exception as e:
            log(f"ERROR: {e}")
            summary[sub_id][f"ceiling_{int(ceiling)}"] = {"error": str(e)}
        log_f.close()

# Save summary
with (OUT_DIR / "summary.json").open("w") as f:
    json.dump(summary, f, indent=2)

print("\n=== matrix summary ===", flush=True)
print(json.dumps(summary, indent=2), flush=True)
print(f"\nsaved → {OUT_DIR}/summary.json", flush=True)
