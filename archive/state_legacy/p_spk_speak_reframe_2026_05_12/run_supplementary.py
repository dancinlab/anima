#!/usr/bin/env python3
"""
P-SPK §7.D supplementary — diagnose WHY rho_real ~= 0:
  (a) is tension_final essentially a monotone ramp (== seq position proxy)?
  (b) detrended tension (residual after per-prompt linear fit) vs entropy — does any
      coupling survive once the trivial length-ramp is removed?
  (c) within-prompt rho distribution (per-prompt Spearman tension_final vs entropy)
Appends a "supplementary" block to results_2026_05_12.json.
"""
import os, sys, json, time, random
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
CKPT = "/home/aiden/mac_home/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
ARCH_DIR = "/home/aiden/mac_home/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain"
PROBES = os.path.join(HERE, "probe_prompts.jsonl")
sys.path.insert(0, ARCH_DIR)
from engine_a_g_arch import EngineAGModel, EngineAGConfig  # noqa: E402

SEED = 42; N_GEN_STEPS = 30
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if DEVICE == "cuda" else torch.float32
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if DEVICE == "cuda": torch.cuda.manual_seed_all(SEED)

def enc(s): return list(s.encode("utf-8"))
def dec(ids):
    try: return bytes(int(i) & 0xFF for i in ids).decode("utf-8", errors="replace")
    except Exception: return "<dec-err>"

def load_model():
    p = torch.load(CKPT, map_location="cpu")
    cfg = EngineAGConfig(**p["config"]); m = EngineAGModel(cfg)
    m.load_state_dict(p["state_dict"], strict=True); m.eval().to(DEVICE).to(DTYPE)
    return m, cfg

@torch.no_grad()
def instrumented_step(model, cfg, input_ids):
    B, T = input_ids.shape
    x = model.tok_emb(input_ids)
    cells = model.engine_g.fresh_cells(B, x.device, x.dtype)
    tensions = []
    for li, layer in enumerate(model.layers):
        t = model.engine_g.tension(x, cells); tensions.append(float(t[0].item()))
        x, _ = layer(x, tension=t)
        if (li + 1) % cfg.g_refresh_every == 0 and li + 1 < cfg.n_layers:
            cells = model.engine_g.step(cells, x.mean(dim=1))
            x = x + model.engine_g.project_back(cells).unsqueeze(1)
    x = model.norm_f(x); logits = model.lm_head(x)
    return logits[:, -1, :], float(np.mean(tensions)), float(tensions[-1])

def token_entropy(row):
    logp = F.log_softmax(row.float(), dim=-1); p = logp.exp()
    return float(-(p * logp).sum().item())

@torch.no_grad()
def run_prompt(model, cfg, prompt):
    pid = enc(prompt)[: cfg.ctx - N_GEN_STEPS - 2]
    ids = list(pid); tf=[]; tn=[]; H=[]
    for step in range(N_GEN_STEPS):
        cur = torch.tensor([ids], dtype=torch.long, device=DEVICE)
        nl, t_nat, t_fin = instrumented_step(model, cfg, cur)
        H.append(token_entropy(nl[0]))
        tn.append(t_nat); tf.append(t_fin)
        ids.append(int(nl[0].argmax().item()) & 0xFF)
    return np.array(tf), np.array(tn), np.array(H)

def main():
    t0 = time.time()
    model, cfg = load_model()
    probes = [json.loads(l) for l in open(PROBES) if l.strip()]
    print(f"[{time.time()-t0:.0f}s] loaded; {len(probes)} probes", flush=True)

    all_step_idx=[]; all_tf=[]; all_tn=[]; all_H=[]
    all_tf_detr=[]; all_tn_detr=[]; all_H_detr=[]
    per_prompt_rho_tf=[]; per_prompt_rho_tn=[]
    tf_vs_stepidx_rho=[]
    for i, pr in enumerate(probes):
        tf, tn, H = run_prompt(model, cfg, pr["prompt"])
        idx = np.arange(len(tf), dtype=float)
        # per-prompt detrend (remove linear fit in step index) for tf, tn, H
        def detr(y):
            a, b = np.polyfit(idx, y, 1)
            return y - (a*idx + b)
        tf_d, tn_d, H_d = detr(tf), detr(tn), detr(H)
        all_step_idx += list(idx); all_tf += list(tf); all_tn += list(tn); all_H += list(H)
        all_tf_detr += list(tf_d); all_tn_detr += list(tn_d); all_H_detr += list(H_d)
        # per-prompt Spearman
        if np.std(tf) > 1e-9 and np.std(H) > 1e-9:
            r,_ = stats.spearmanr(tf, H); per_prompt_rho_tf.append(float(r))
        if np.std(tn) > 1e-9 and np.std(H) > 1e-9:
            r,_ = stats.spearmanr(tn, H); per_prompt_rho_tn.append(float(r))
        if np.std(tf) > 1e-9:
            r,_ = stats.spearmanr(tf, idx); tf_vs_stepidx_rho.append(float(r))
        if (i+1)%25==0: print(f"[{time.time()-t0:.0f}s] {i+1}", flush=True)

    def sp(a,b):
        a=np.asarray(a,float); b=np.asarray(b,float)
        r,p = stats.spearmanr(a,b); rp,pp = stats.pearsonr(a,b)
        return {"spearman_r":round(float(r),4),"spearman_p":float(p),
                "pearson_r":round(float(rp),4),"pearson_p":float(pp),"n":int(len(a))}

    supp = {
        "purpose": "diagnose near-zero rho_real: is the architecture's A/G tension just a sequence-length ramp?",
        "tension_final_vs_step_index": {
            "pooled": sp(all_step_idx, all_tf),
            "per_prompt_spearman_mean": round(float(np.mean(tf_vs_stepidx_rho)),4),
            "per_prompt_spearman_min": round(float(np.min(tf_vs_stepidx_rho)),4),
            "interpretation": "rho ~= 1 => tension_final is monotone in generation step => it is essentially a length proxy, carrying ~no dynamic 'tension' content within a generation episode",
        },
        "tension_native_vs_step_index": sp(all_step_idx, all_tn),
        "entropy_vs_step_index": sp(all_step_idx, all_H),
        "DETRENDED_correlations (per-prompt linear ramp removed from both series)": {
            "tension_final_detr__entropy_detr": sp(all_tf_detr, all_H_detr),
            "tension_native_detr__entropy_detr": sp(all_tn_detr, all_H_detr),
            "comment": "this is the fairest test of dynamic coupling — strips the trivial shared length trend",
        },
        "per_prompt_rho_distribution": {
            "tension_final__entropy": {
                "mean": round(float(np.mean(per_prompt_rho_tf)),4),
                "median": round(float(np.median(per_prompt_rho_tf)),4),
                "std": round(float(np.std(per_prompt_rho_tf)),4),
                "frac_abs_gt_0.3": round(float(np.mean(np.abs(per_prompt_rho_tf)>0.3)),3),
                "n_prompts": len(per_prompt_rho_tf),
            },
            "tension_native__entropy": {
                "mean": round(float(np.mean(per_prompt_rho_tn)),4),
                "median": round(float(np.median(per_prompt_rho_tn)),4),
                "std": round(float(np.std(per_prompt_rho_tn)),4),
                "frac_abs_gt_0.3": round(float(np.mean(np.abs(per_prompt_rho_tn)>0.3)),3),
                "n_prompts": len(per_prompt_rho_tn),
            },
        },
        "wall_seconds": round(time.time()-t0,1),
    }
    rp = os.path.join(HERE, "results_2026_05_12.json")
    res = json.load(open(rp))
    res["supplementary_detrend_diagnostics"] = supp
    with open(rp, "w") as f: json.dump(res, f, indent=2, ensure_ascii=False)
    print(json.dumps(supp, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
