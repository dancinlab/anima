#!/usr/bin/env python3
"""
P-SPK §7.D — NO SPEAK() DESIGN→falsifiable reframe analysis.

REFRAME CLAIM: output token entropy / semantic content is statistically coupled
with internal tension state ||A(t)-G(t)|| — i.e. output is continuous tension
externalization, not a discrete speak() invocation.

NO new fine-tuning. Instrumented forward on existing BG-LB 350M Engine A/G ckpt.

Outputs:
  results_2026_05_12.json
  (verdict_2026_05_12.md written separately after reviewing results)
"""
import os, sys, json, math, time, random
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/aiden/mac_home/core/anima"
CKPT = "/home/aiden/mac_home/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain/ckpts/step_8000_final.pt"
ARCH_DIR = "/home/aiden/mac_home/.cache/anima/clm_v5_remapped/bg_lb_350m_pretrain"
PROBES = os.path.join(HERE, "probe_prompts.jsonl")

sys.path.insert(0, ARCH_DIR)  # engine_a_g_arch.py lives next to the ckpt (the exact training arch)
from engine_a_g_arch import EngineAGModel  # noqa: E402

SEED = 42
N_GEN_STEPS = 30
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.bfloat16 if DEVICE == "cuda" else torch.float32

random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
if DEVICE == "cuda":
    torch.cuda.manual_seed_all(SEED)


def enc(s: str) -> list:
    """Byte-level tokenizer (own 17 anima-native: token id == byte value, vocab mod 32000)."""
    return list(s.encode("utf-8"))


def dec(ids) -> str:
    try:
        return bytes(int(i) & 0xFF for i in ids).decode("utf-8", errors="replace")
    except Exception:
        return "<dec-err>"


def load_model():
    payload = torch.load(CKPT, map_location="cpu")
    from engine_a_g_arch import EngineAGConfig
    cfg = EngineAGConfig(**payload["config"])
    model = EngineAGModel(cfg)
    model.load_state_dict(payload["state_dict"], strict=True)
    model.eval().to(DEVICE).to(DTYPE)
    return model, cfg


@torch.no_grad()
def instrumented_step(model, cfg, input_ids):
    """One forward pass over the prefix. Returns:
       - logits for next token (last position)
       - tension_native: mean over layers of architecture's A/G tension ratio scalar
       - tension_final: architecture's A/G tension at the final (deepest) layer
       - tension_diff: mean over layers of ||hidden_mean_l - project_back(cells_l)||_2
                       (a true ||A-G|| difference after projecting G into A's d_model space)
    Reproduces EngineAGModel.forward internals so we can capture per-layer cells/hidden.
    """
    B, T = input_ids.shape
    x = model.tok_emb(input_ids)
    cells = model.engine_g.fresh_cells(B, x.device, x.dtype)
    tensions = []
    diffs = []
    for li, layer in enumerate(model.layers):
        t = model.engine_g.tension(x, cells)  # (B,) = ||A_h|| / ||G_cells||
        tensions.append(float(t[0].item()))
        # true A-G difference: project G cells into d_model space, compare to hidden mean
        hidden_mean = x.mean(dim=1)                       # (B, d_model) = "A representative"
        g_in_a_space = model.engine_g.project_back(cells) # (B, d_model) = "G projected into A space"
        d = (hidden_mean.float() - g_in_a_space.float()).norm(dim=-1)  # (B,)
        diffs.append(float(d[0].item()))
        x, _ = layer(x, tension=t)
        if (li + 1) % cfg.g_refresh_every == 0 and li + 1 < cfg.n_layers:
            cells = model.engine_g.step(cells, x.mean(dim=1))
            x = x + model.engine_g.project_back(cells).unsqueeze(1)
    x = model.norm_f(x)
    logits = model.lm_head(x)            # (B, T, V)
    next_logits = logits[:, -1, :]       # (B, V)
    return (next_logits,
            float(np.mean(tensions)),
            float(tensions[-1]),
            float(np.mean(diffs)))


def token_entropy(logits_row):
    """Shannon entropy (nats) of next-token distribution."""
    logp = F.log_softmax(logits_row.float(), dim=-1)
    p = logp.exp()
    H = -(p * logp).sum().item()
    return H


@torch.no_grad()
def run_prompt(model, cfg, prompt, mode="free", max_steps=N_GEN_STEPS,
               scripted_template_ids=None, embed_baseline=None):
    """Generate max_steps tokens, recording per-step (tension_native, tension_final,
       tension_diff, entropy, semantic_mag). Returns dict of lists + decoded text.

       mode='free'      : greedy autoregressive (model picks its own next token).
       mode='scripted'  : feed back tokens from scripted_template_ids regardless of
                          model output (output decoupled from tension by construction).
    """
    prompt_ids = enc(prompt)
    # cap prefix to keep ctx within budget (1024); we add up to 30 tokens
    prompt_ids = prompt_ids[: cfg.ctx - max_steps - 2]
    ids = list(prompt_ids)
    recs = {"tension_native": [], "tension_final": [], "tension_diff": [],
            "entropy": [], "semantic_mag": [], "gen_ids": []}
    for step in range(max_steps):
        cur = torch.tensor([ids], dtype=torch.long, device=DEVICE)
        next_logits, t_nat, t_fin, t_diff = instrumented_step(model, cfg, cur)
        H = token_entropy(next_logits[0])
        # choose next token
        if mode == "free":
            nxt = int(next_logits[0].argmax().item()) & 0xFF  # byte-level: keep in 0..255
        elif mode == "scripted":
            nxt = int(scripted_template_ids[step % len(scripted_template_ids)]) & 0xFF
        else:
            raise ValueError(mode)
        # semantic info: magnitude of the emitted token's embedding vs baseline (mean emb)
        emb = model.tok_emb.weight[nxt].float()
        sem = float((emb - embed_baseline).norm().item())
        recs["tension_native"].append(t_nat)
        recs["tension_final"].append(t_fin)
        recs["tension_diff"].append(t_diff)
        recs["entropy"].append(H)
        recs["semantic_mag"].append(sem)
        recs["gen_ids"].append(nxt)
        ids.append(nxt)
    recs["text"] = dec(recs["gen_ids"])
    return recs


def safe_corr(a, b, kind="spearman"):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 3 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return float("nan"), float("nan"), int(len(a))
    if kind == "spearman":
        r, p = stats.spearmanr(a, b)
    else:
        r, p = stats.pearsonr(a, b)
    return float(r), float(p), int(len(a))


def fisher_z_diff_test(r1, n1, r2, n2):
    """Compare two independent correlations via Fisher z. Returns (z, p_two_sided)."""
    if not (np.isfinite(r1) and np.isfinite(r2)) or min(n1, n2) < 4:
        return float("nan"), float("nan")
    r1 = max(min(r1, 0.999999), -0.999999); r2 = max(min(r2, 0.999999), -0.999999)
    z1 = math.atanh(r1); z2 = math.atanh(r2)
    se = math.sqrt(1.0 / (n1 - 3) + 1.0 / (n2 - 3))
    z = (z1 - z2) / se
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return float(z), float(p)


def lead_lag_xcorr(tension_series, output_series, max_lag=5):
    """Cross-correlation of Δtension vs Δoutput across lags -max_lag..+max_lag.
       lag>0 means tension change LEADS output change (tension[t] vs output[t+lag])."""
    dt = np.diff(np.asarray(tension_series, float))
    do = np.diff(np.asarray(output_series, float))
    n = min(len(dt), len(do))
    dt, do = dt[:n], do[:n]
    best_lag, best_r = 0, 0.0
    table = {}
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            x = dt[: n - lag] if lag > 0 else dt
            y = do[lag:] if lag > 0 else do
        else:
            x = dt[-lag:]
            y = do[: n + lag]
        if len(x) < 3 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
            table[lag] = float("nan"); continue
        r = float(np.corrcoef(x, y)[0, 1])
        table[lag] = r
        if np.isfinite(r) and abs(r) > abs(best_r):
            best_r, best_lag = r, lag
    return best_lag, best_r, table


def main():
    t0 = time.time()
    print(f"[{time.time()-t0:.0f}s] loading ckpt {CKPT}", flush=True)
    model, cfg = load_model()
    n_params = sum(p.numel() for p in model.parameters())
    embed_baseline = model.tok_emb.weight.float().mean(dim=0).detach()
    print(f"[{time.time()-t0:.0f}s] model loaded: {n_params:,} params, device={DEVICE} dtype={DTYPE}", flush=True)

    probes = [json.loads(l) for l in open(PROBES) if l.strip()]
    print(f"[{time.time()-t0:.0f}s] {len(probes)} probes", flush=True)

    # scripted template — fixed Korean response seed used for ALL prompts (decoupled from tension)
    SCRIPTED_TEXT = "네, 알겠습니다. 그것은 흥미로운 질문이군요. 제 생각에는 그렇습니다."
    scripted_ids = [b & 0xFF for b in enc(SCRIPTED_TEXT)]

    per_prompt = []
    # pooled accumulators
    pool = {"free": {"tn": [], "tf": [], "td": [], "H": [], "sem": []},
            "scripted": {"tn": [], "tf": [], "td": [], "H": [], "sem": []}}
    cat_pool = {}  # category -> {tn:[],H:[]}
    leadlag_free = []   # per-prompt best lag (free, tension_final vs entropy)

    for i, pr in enumerate(probes):
        cat = pr.get("category", "?")
        for mode in ("free", "scripted"):
            r = run_prompt(model, cfg, pr["prompt"], mode=mode,
                           scripted_template_ids=scripted_ids, embed_baseline=embed_baseline)
            pool[mode]["tn"] += r["tension_native"]
            pool[mode]["tf"] += r["tension_final"]
            pool[mode]["td"] += r["tension_diff"]
            pool[mode]["H"] += r["entropy"]
            pool[mode]["sem"] += r["semantic_mag"]
            if mode == "free":
                cat_pool.setdefault(cat, {"tn": [], "H": []})
                cat_pool[cat]["tn"] += r["tension_native"]
                cat_pool[cat]["H"] += r["entropy"]
                bl, br, _ = lead_lag_xcorr(r["tension_final"], r["entropy"], max_lag=5)
                if np.isfinite(br):
                    leadlag_free.append(bl)
                if i < 5:  # keep first 5 free traces as evidence
                    per_prompt.append({
                        "id": pr["id"], "category": cat, "prompt": pr["prompt"],
                        "text_out": r["text"][:160],
                        "tension_final_trace": [round(v, 4) for v in r["tension_final"]],
                        "entropy_trace": [round(v, 4) for v in r["entropy"]],
                        "semantic_mag_trace": [round(v, 4) for v in r["semantic_mag"]],
                    })
        if (i + 1) % 20 == 0:
            print(f"[{time.time()-t0:.0f}s] {i+1}/{len(probes)} prompts done", flush=True)

    n_steps_free = len(pool["free"]["tn"])
    n_steps_scripted = len(pool["scripted"]["tn"])
    print(f"[{time.time()-t0:.0f}s] free steps={n_steps_free} scripted steps={n_steps_scripted}", flush=True)

    # ── correlations (primary: tension_final vs entropy; report tension_native + tension_diff too) ──
    def block(d):
        out = {}
        for tname, tkey in [("tension_final", "tf"), ("tension_native", "tn"), ("tension_diff", "td")]:
            for oname, okey in [("entropy", "H"), ("semantic_mag", "sem")]:
                rs, ps, ns = safe_corr(d[tkey], d[okey], "spearman")
                rp, pp, _ = safe_corr(d[tkey], d[okey], "pearson")
                out[f"{tname}__{oname}"] = {
                    "spearman_r": round(rs, 4), "spearman_p": ps,
                    "pearson_r": round(rp, 4), "pearson_p": pp, "n": ns}
        return out

    corr_free = block(pool["free"])
    corr_scripted = block(pool["scripted"])

    # primary metric: tension_final vs entropy, Spearman
    rho_real = corr_free["tension_final__entropy"]["spearman_r"]
    n_real = corr_free["tension_final__entropy"]["n"]
    rho_ctrl = corr_scripted["tension_final__entropy"]["spearman_r"]
    n_ctrl = corr_scripted["tension_final__entropy"]["n"]
    fz, fp = fisher_z_diff_test(rho_real, n_real, rho_ctrl, n_ctrl)

    # also Pearson primary for completeness
    rho_real_p = corr_free["tension_final__entropy"]["pearson_r"]
    rho_ctrl_p = corr_scripted["tension_final__entropy"]["pearson_r"]

    # ── shuffle control (sanity): destroy temporal alignment within free pool ──
    rng = np.random.default_rng(SEED)
    Hsh = np.array(pool["free"]["H"], float); rng.shuffle(Hsh)
    rho_shuffle, p_shuffle, _ = safe_corr(pool["free"]["tf"], Hsh, "spearman")

    # ── lead-lag on pooled Δseries (concatenated per-prompt, then global xcorr is noisy;
    #    instead report distribution of per-prompt best lags + a pooled xcorr table) ──
    # pooled xcorr: stitch per-prompt diffs would bleed across boundaries; we already
    # collected per-prompt best lags. Also compute a pooled table by treating the full
    # concatenation (acknowledged: boundary contamination ~3% of pairs).
    pooled_lag, pooled_r, pooled_table = lead_lag_xcorr(pool["free"]["tf"], pool["free"]["H"], max_lag=5)
    leadlag_free = np.array(leadlag_free, float)
    leadlag_summary = {
        "per_prompt_best_lag_mean": round(float(np.nanmean(leadlag_free)), 3) if len(leadlag_free) else None,
        "per_prompt_best_lag_median": float(np.nanmedian(leadlag_free)) if len(leadlag_free) else None,
        "per_prompt_best_lag_mode": int(stats.mode(leadlag_free[np.isfinite(leadlag_free)].astype(int), keepdims=False).mode) if len(leadlag_free) else None,
        "per_prompt_frac_lag_ge_1": round(float(np.mean(leadlag_free >= 1)), 3) if len(leadlag_free) else None,
        "per_prompt_frac_lag_eq_0": round(float(np.mean(leadlag_free == 0)), 3) if len(leadlag_free) else None,
        "per_prompt_frac_lag_le_minus1": round(float(np.mean(leadlag_free <= -1)), 3) if len(leadlag_free) else None,
        "pooled_best_lag": pooled_lag,
        "pooled_best_corr": round(pooled_r, 4),
        "pooled_xcorr_table": {str(k): (round(v, 4) if np.isfinite(v) else None) for k, v in pooled_table.items()},
        "note": "lag>0 => tension change leads output change",
    }

    # ── categorical split ──
    by_cat = {}
    for cat, d in cat_pool.items():
        rs, ps, ns = safe_corr(d["tn"], d["H"], "spearman")
        rsf, _, _ = safe_corr(d["tn"], d["H"], "pearson")
        by_cat[cat] = {"spearman_r": round(rs, 4), "pearson_r": round(rsf, 4),
                       "spearman_p": ps, "n": ns}

    # ── verdict logic per spec falsifier ──
    # EMPIRICAL_UPGRADE: rho_real >= 0.5 AND (rho_real - rho_ctrl) >= 0.3 AND fisher p < 0.01
    # NULL: rho_real < 0.2 OR (rho_real - rho_ctrl) < 0.1
    # MIXED: 0.2 <= rho_real < 0.5
    delta = (rho_real - rho_ctrl) if (np.isfinite(rho_real) and np.isfinite(rho_ctrl)) else float("nan")
    if np.isfinite(rho_real) and rho_real >= 0.5 and np.isfinite(delta) and delta >= 0.3 and np.isfinite(fp) and fp < 0.01:
        verdict = "EMPIRICAL_UPGRADE"
    elif (np.isfinite(rho_real) and rho_real < 0.2) or (np.isfinite(delta) and delta < 0.1):
        verdict = "NULL"
    else:
        verdict = "MIXED"

    results = {
        "bg_id": "P-SPK",
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ckpt": CKPT,
        "ckpt_schema": "engine_a_g_arch/v1 (lineage engine_a_g_dual_350m_v1_lb_pretrain, BG-LB 350M, 8000 steps)",
        "arch": "Engine A (24L/1024d/16h GQA, byte-level vocab32k-mod) + Engine G (16 cells x 64d repulsion-field, A/G tension softmax gate)",
        "n_params": n_params,
        "device": DEVICE, "dtype": str(DTYPE),
        "n_prompts": len(probes),
        "n_gen_steps_per_prompt": N_GEN_STEPS,
        "n_steps_analyzed_free": n_steps_free,
        "n_steps_analyzed_scripted": n_steps_scripted,
        "tension_definitions": {
            "tension_final": "architecture A/G tension ratio ||A_h||/||G_cells|| at deepest layer (the value the model's attention temperature gate actually consumes) — PRIMARY",
            "tension_native": "mean over 24 layers of the A/G tension ratio",
            "tension_diff": "mean over 24 layers of ||hidden_mean_l - project_back(cells_l)||_2 — a true ||A-G|| difference after projecting G cells into A's d_model space",
        },
        "primary_metric": "Spearman rho( tension_final(t), output_token_entropy(t) ) over free-generation steps",
        "rho_real_spearman": rho_real,
        "rho_real_pearson": rho_real_p,
        "rho_control_spearman": rho_ctrl,
        "rho_control_pearson": rho_ctrl_p,
        "rho_real_minus_control": round(delta, 4) if np.isfinite(delta) else None,
        "fisher_z_diff": round(fz, 4) if np.isfinite(fz) else None,
        "fisher_z_p": fp,
        "rho_shuffle_control_spearman": round(rho_shuffle, 4) if np.isfinite(rho_shuffle) else None,
        "correlations_free_all": corr_free,
        "correlations_scripted_all": corr_scripted,
        "lead_lag": leadlag_summary,
        "lead_lag_peak": leadlag_summary["pooled_best_lag"],
        "lead_lag_corr": leadlag_summary["pooled_best_corr"],
        "by_category": {k: v["spearman_r"] for k, v in by_cat.items()},
        "by_category_detail": by_cat,
        "scripted_template_text": SCRIPTED_TEXT,
        "verdict": verdict,
        "falsifier_thresholds": {
            "EMPIRICAL_UPGRADE": "rho_real>=0.5 AND (rho_real-rho_ctrl)>=0.3 AND fisher_p<0.01",
            "NULL": "rho_real<0.2 OR (rho_real-rho_ctrl)<0.1",
            "MIXED": "0.2<=rho_real<0.5 (or fails upgrade gate without hitting NULL)",
        },
        "evidence_traces": per_prompt,
        "wall_seconds": round(time.time() - t0, 1),
        "cost_usd_actual": 0.0,
        "cost_note": "local RTX 5070, $0 marginal compute; analysis-only, no fine-tuning",
        "honest_limits": [
            "Tension is operationalized as the architecture's A/G ratio scalar ||A_h||/||G_cells|| (the quantity the model's softmax-temperature gate actually consumes), NOT a literal ||A-G|| vector difference — A (d_model=1024) and G (cell dim=64) live in different spaces. We additionally report tension_diff (G projected into A space, then ||.||) for triangulation, but the two are not interchangeable; conclusions are about the architecture's own tension signal.",
            "Greedy (argmax) decoding restricted to byte-level vocab (token id & 0xFF) — the BG-LB ckpt was byte-mod-trained, so this is faithful, but greedy collapses output diversity vs nucleus sampling; entropy is the *distribution* entropy (full softmax), not the realized-token surprisal, so it is decode-strategy-robust, but the autoregressive trajectory itself is greedy-specific.",
            "BG-LB is an 8000-step pretrain checkppoint (final loss not converged to a chat-capable regime; sibling §9 work flagged BG-LB chat-cap as not yet emergent). Coupling measured here is a property of this *partially-trained* substrate; a more-converged ckpt could show stronger or weaker coupling.",
            "Scripted-speak control forces a single fixed Korean template for all 100 prompts — it decouples the *emitted* token stream from tension by construction, but the model still computes its own next-token distribution at each step, so the control bounds 'how much of free-gen coupling is an artifact of the prefix/length structure shared by both modes' rather than a perfect placebo.",
            "Lead-lag uses first-difference cross-correlation on 29-step series per prompt — short series, low power; the pooled xcorr table stitches per-prompt diffs (≈3% of adjacent pairs straddle a prompt boundary, mild contamination). Per-prompt best-lag distribution is the more trustworthy lead-lag readout.",
            "n=3000 free steps are NOT independent (29 are autocorrelated within each of 100 prompts) — reported p-values are anticonservative; effect-size (rho) and the control delta are the load-bearing quantities, not significance stars.",
        ],
    }

    out_path = os.path.join(HERE, "results_2026_05_12.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[{time.time()-t0:.0f}s] wrote {out_path}", flush=True)
    print(json.dumps({k: results[k] for k in
        ["verdict", "rho_real_spearman", "rho_real_pearson", "rho_control_spearman",
         "rho_real_minus_control", "fisher_z_p", "lead_lag_peak", "lead_lag_corr",
         "by_category", "n_steps_analyzed_free", "rho_shuffle_control_spearman"]},
        indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
