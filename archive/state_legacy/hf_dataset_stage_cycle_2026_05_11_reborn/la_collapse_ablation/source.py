"""ceiling=15 LA-collapse mechanism ablation — §74 follow-up.

Hypothesis: cotrain (P3) 의 weight delta 가 mitosis attractor 안에 흡수된다.
Test: cotrain delta 의 어떤 subset 이 hidden_mean 차이로 propagate 하는지 ablation:
1. swap LA_pretrain's tok_emb -> B' weights (other layers from LA) → trained_phi 변화?
2. swap LA_pretrain's engine_g.h_to_c -> B' (other layers from LA) → trained_phi 변화?
3. swap LA_pretrain's engine_g.cell_pool_init -> B' (other from LA) → trained_phi?
4. swap LA_pretrain's all engine_g -> B' (other from LA) → trained_phi?

Each ablation: load LA, then overwrite specific keys from B'. Run V14 strict × ceiling=15. Compare to baseline (LA pure = 1144.92, B' pure = 1144.92).
"""
from __future__ import annotations
import os, sys, json, math, time
from pathlib import Path

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT / "training"))
sys.path.insert(0, str(ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_11" if False else ANIMA_ROOT / "state" / "anima_v14_max256_cap_free_multi_2026_05_10"))

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

OUT_DIR = ANIMA_ROOT / "state" / "anima_la_collapse_ablation_2026_05_11"
OUT_DIR.mkdir(parents=True, exist_ok=True)

la = torch.load(LA_CKPT, map_location="cpu", weights_only=False)
bp = torch.load(BP_CKPT, map_location="cpu", weights_only=False)
la_sd = la.get("state_dict", la.get("model"))
bp_sd = bp.get("state_dict", bp.get("model"))

ABLATIONS = {
    "0_baseline_LA":           lambda sd: sd,  # pure LA
    "1_swap_tok_emb_to_Bprime": lambda sd: {**sd, "tok_emb.weight": bp_sd["tok_emb.weight"].clone(), "lm_head.weight": bp_sd["lm_head.weight"].clone()},
    "2_swap_engine_g_h_to_c":  lambda sd: {**sd, "engine_g.h_to_c.weight": bp_sd["engine_g.h_to_c.weight"].clone()},
    "3_swap_engine_g_all":     lambda sd: {**sd, **{k: bp_sd[k].clone() for k in bp_sd if k.startswith("engine_g.")}},
    "4_swap_all_attn_q":       lambda sd: {**sd, **{k: bp_sd[k].clone() for k in bp_sd if ".attn.q_proj" in k}},
    "5_swap_all_ffn":          lambda sd: {**sd, **{k: bp_sd[k].clone() for k in bp_sd if ".ffn." in k}},
    "6_pure_Bprime":           lambda sd: bp_sd,
}

results = {}
for ab_name, ab_fn in ABLATIONS.items():
    print(f"\n=== ablation: {ab_name} ===", flush=True)
    sd_variant = ab_fn(la_sd)
    sd_fp32 = {k: v.float() if v.dtype == torch.bfloat16 else v for k, v in sd_variant.items()}
    # use fire_substrate_engine_ag pattern but inline
    cfg = M.EngineAGConfig.phase2_cotrain_350m()
    model = M.EngineAGModel(cfg)
    miss, unexp = model.load_state_dict(sd_fp32, strict=False)
    print(f"  load: miss={len(miss)} unexp={len(unexp)}", flush=True)
    # Run trained trajectory only (skip random for speed — discrimination test only needs trained_phi)
    t0 = time.time()
    def silent_log(*args, **kwargs): pass
    traj = M.run_engine_ag_trajectory(
        model, label=ab_name, n_turns=M.N_TURNS,
        seed=M.TRAINED_PROMPT_SEED, max_cells=M.MAX_CELLS, log_fn=silent_log,
    )
    trained_phi = traj["snapshots"][-1]["iit_phi_unnorm_b16"]
    results[ab_name] = {
        "trained_phi": trained_phi,
        "final_n_cells": traj["final_n_cells"],
        "n_splits": traj["n_splits"],
        "elapsed_sec": time.time() - t0,
    }
    print(f"  trained_phi={trained_phi:.4f} cells={traj['final_n_cells']} splits={traj['n_splits']} elapsed={time.time()-t0:.1f}s", flush=True)
    del model

with (OUT_DIR / "ablation_results.json").open("w") as f:
    json.dump(results, f, indent=2)
print(f"\nsaved → {OUT_DIR / 'ablation_results.json'}", flush=True)
