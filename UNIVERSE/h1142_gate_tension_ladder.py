#!/usr/bin/env python3
"""h1142_gate_tension_ladder.py — GATE-VALIDITY ladder for the frozen 7B gate
G5-L2 (verbatim factual-continuation faithfulness, Cohen's d) vs anima's OWN gate
G2 (corpus-absent novelty / recombination), measured ACROSS SCALE.

PRE-REGISTERED FALSIFIER (frozen 2026-06-13 in
.verdicts/1142_gate_tension_ladder/H_1142_FREEZE.txt BEFORE any score):
  ladder = {~44.68M, 303M (H_1129), 7B (H_1141)} ByteGPT vocab256 ckpts.
  For EACH ckpt measure BOTH frozen metrics with the SAME harness:
    G2_novelty_rate     = gate_g2().novelty_rate    (h1141_7b_pass_attempt VERBATIM)
    G5L2_faithfulness_d = gate_g5_l2().cohens_d      (h1141_7b_g5_eval VERBATIM)
  rho = Spearman(G2_novelty_rate, G5L2_faithfulness_d).
  VERDICT (frozen): rho<=0 => TENSION CONFIRMED (re-scope JUSTIFIED, 🔴-for-gate);
                    0<rho<0.5 => INCONCLUSIVE; rho>=0.5 => VALID-ALIGNED (① REJECTED).

METRIC PROVENANCE — this file IMPORTS gate_g2 + gate_g5_l2 + all helpers VERBATIM
from the existing frozen harnesses (no metric re-implementation):
  gate_g2, gen_novel, kwr_realdict, content_ngrams, corpus_absent, load_real_dict,
  IDEA_PROMPTS  <-  UNIVERSE/h1141_7b_pass_attempt.py
  gate_g5_l2, extract_sentences, gen_from_prompt_grounded, first_half_split,
  overlap_frac, words_lower                                <-  UNIVERSE/h1141_7b_g5_eval.py
The ByteGPT arch is identical across all three (the frozen harness arch VERBATIM).

HARVEST (reused, NOT recomputed — identical frozen harness already run on the 7B):
  7B G2_novelty_rate = 0.5    (state/7b_h1141_recovery/h1141_result.json, gate_g2)
  7B G5L2_d          = 0.1631 (.verdicts/1141_7b_g5/H_1141_G5.txt, gate_g5_l2 temp0.7 seed7)

RE-RUN (no harness-identical number exists): 303M + 44.68M, both gates, summer GPU
($0, VRAM-capped under free headroom; co-tenant rbfe-prod NEVER touched).

a_scale_honest_scope: 3-rung ladder, toy/surface p7 metric (word-overlap + dict,
NOT perplexity, NOT LLM-judge), scale-transfer beyond these points UNVERIFIED.
a_lane_akida_gpu_split: substrate = PyTorch-CUDA (Lane-G ref), NOT AKIDA.
NO frozen gate moved (a7b_pass) — this is evidence-gathering only.
"""
from __future__ import annotations
import argparse, importlib.util, json, math, os, sys, time
import torch

HERE = os.path.dirname(os.path.abspath(__file__))


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── import the FROZEN metric code VERBATIM (no re-implementation) ──
G2MOD = _load_module(os.path.join(HERE, "h1141_7b_pass_attempt.py"), "h1141_pass")
G5MOD = _load_module(os.path.join(HERE, "h1141_7b_g5_eval.py"), "h1141_g5")

gate_g2 = G2MOD.gate_g2
gate_g5_l2 = G5MOD.gate_g5_l2
load_real_dict = G2MOD.load_real_dict
ByteGPT = G2MOD.ByteGPT  # arch is identical in both modules (frozen arch verbatim)


def load_ckpt(path, dev):
    bk = torch.load(path, map_location="cpu", weights_only=False)
    cfg = bk["config"]
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(torch.bfloat16)
    m.load_state_dict(bk["model"], strict=False)
    m = m.to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    val_ce = bk.get("val_ce"); step = bk.get("step")
    del bk
    return m, cfg, nparam, val_ce, step


def measure_rung(label, ckpt, corpus_path, en_bytes, dev, dict_words, n_sentences=40):
    """Run the VERBATIM frozen gate_g2 + gate_g5_l2 on one ckpt."""
    print(f"\n{'='*78}\n=== RUNG {label}  ckpt={ckpt}\n{'='*78}", flush=True)
    m, cfg, nparam, val_ce, step = load_ckpt(ckpt, dev)
    block = cfg["block"]
    print(f"[model] cfg={cfg} params={nparam:,} val_ce={val_ce} step={step}", flush=True)
    corpus_paths = [corpus_path]

    # G2 — anima's OWN novelty gate (corpus-absent novel n-gram rate)
    g2 = gate_g2(m, dev, block, dict_words, corpus_paths, max_new=110)

    # G5-L2 — the borrowed faithfulness gate (paired Cohen's d, temp0.7 seed7)
    g5l2 = gate_g5_l2(m, dev, block, corpus_path, en_bytes, n_sentences=n_sentences, seed=7)
    d_raw = g5l2["cohens_d"]
    d_val = (float("inf") if d_raw == "inf" else float(d_raw))

    del m
    if dev == "cuda":
        torch.cuda.empty_cache()
    return {
        "label": label, "nparam": nparam, "val_ce": val_ce, "step": step,
        "G2_novelty_rate": g2["novelty_rate"], "G2_n_novel": g2["n_novel"],
        "G2_pass": g2["pass"], "G2_control_novel": g2["control"].get("n_novel", "NA"),
        "G5L2_faithfulness_d": d_raw, "G5L2_d_val": d_val,
        "G5L2_mean_true": g5l2["mean_overlap_true"], "G5L2_mean_random": g5l2["mean_overlap_random"],
        "G5L2_pass": g5l2["pass"], "G5L2_n": g5l2["n"],
    }


def spearman(xs, ys):
    """Spearman rho via Pearson on ranks (n is tiny; ties averaged)."""
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx = sum(rx) / n; my = sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    vx = sum((rx[i] - mx) ** 2 for i in range(n))
    vy = sum((ry[i] - my) ** 2 for i in range(n))
    if vx <= 0 or vy <= 0:
        return 0.0
    return cov / math.sqrt(vx * vy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="English wiki corpus (gate probe target)")
    ap.add_argument("--en_mb", type=float, default=300.0)
    ap.add_argument("--n_sentences", type=int, default=40)
    ap.add_argument("--ckpt_44m", required=True)
    ap.add_argument("--ckpt_303m", required=True)
    ap.add_argument("--vram_frac", type=float, default=0.36,
                    help="cap of TOTAL VRAM (summer 12GB; 0.36 ~= 4.3GB < free headroom)")
    ap.add_argument("--out", default="/tmp/h1142_ladder.json")
    # harvested 7B numbers (identical frozen harness) — passed in, NOT recomputed
    ap.add_argument("--g2_7b", type=float, default=0.5)
    ap.add_argument("--g5l2_7b", type=float, default=0.1631)
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    if dev == "cuda":
        torch.cuda.set_per_process_memory_fraction(a.vram_frac, 0)
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)} VRAM-cap frac={a.vram_frac}", flush=True)
    dict_words = load_real_dict()
    print(f"[dict] {len(dict_words)} real English words", flush=True)
    en_bytes = int(a.en_mb * 1024 * 1024)

    rungs = []
    # RUNG 44.68M (re-run both gates)
    rungs.append(measure_rung("44.68M", a.ckpt_44m, a.corpus, en_bytes, dev, dict_words, a.n_sentences))
    # RUNG 303M (re-run both gates)
    rungs.append(measure_rung("303M", a.ckpt_303m, a.corpus, en_bytes, dev, dict_words, a.n_sentences))
    # RUNG 7B (HARVESTED — identical frozen harness already run, NOT recomputed)
    rungs.append({
        "label": "7B", "nparam": 7252828160, "val_ce": 1.1857, "step": 7000,
        "G2_novelty_rate": a.g2_7b, "G5L2_faithfulness_d": a.g5l2_7b, "G5L2_d_val": a.g5l2_7b,
        "harvested": True,
        "source_G2": "state/7b_h1141_recovery/h1141_result.json (gate_g2)",
        "source_G5L2": ".verdicts/1141_7b_g5/H_1141_G5.txt (gate_g5_l2 temp0.7 seed7)",
    })

    xs = [r["G2_novelty_rate"] for r in rungs]
    ys = [r["G5L2_d_val"] for r in rungs]
    rho = spearman(xs, ys)

    if rho <= 0:
        verdict = "TENSION-CONFIRMED"
        tier = "🔴 (for the gate — re-scope ① JUSTIFIED)"
    elif rho < 0.5:
        verdict = "WEAK/INCONCLUSIVE"
        tier = "🟠"
    else:
        verdict = "VALID-ALIGNED"
        tier = "🟢 (① REJECTED — 7B merely undertrained, not gate-mismatched)"

    print(f"\n{'='*78}\n### H_1142 GATE-TENSION LADDER — RESULT ###\n{'='*78}", flush=True)
    print(f"{'rung':>8} {'nparam':>13} {'G2_novelty':>11} {'G5L2_d':>9}", flush=True)
    for r in rungs:
        print(f"{r['label']:>8} {r['nparam']:>13,} {r['G2_novelty_rate']:>11.4f} "
              f"{(r['G5L2_d_val'] if isinstance(r['G5L2_d_val'],float) else r['G5L2_d_val']):>9}", flush=True)
    print(f"\nSpearman rho(G2_novelty_rate, G5L2_faithfulness_d) = {rho:.4f}", flush=True)
    print(f"VERDICT: {verdict}  {tier}", flush=True)

    out = {"hypothesis": "H_1142_gate_tension_ladder", "rungs": rungs,
           "G2_novelty_rates": xs, "G5L2_ds": ys, "spearman_rho": rho,
           "verdict": verdict, "tier": tier,
           "frozen_rule": "rho<=0 TENSION-CONFIRMED | 0<rho<0.5 INCONCLUSIVE | rho>=0.5 VALID-ALIGNED"}
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"\n[out] {a.out}", flush=True)


if __name__ == "__main__":
    main()
