#!/usr/bin/env python3
"""H_951 — ENGINE-NOT-PREDICTOR (CLM→CE reframe, axis ⓑ).

THESIS UNDER TEST
-----------------
Axis ⓑ of the CLM→CE ("Consciousness Engine") reframe: CLM's essence is internal
substrate dynamics (a Φ-like integration of its hidden field), NOT next-token
perplexity. If a Φ-substrate metric were just a restatement of perplexity, then
"language model" is the right frame. If Φ is DECORRELATED from perplexity, then
measuring CLM as a language model misses its essence — consistent with the prior
finding (docs/paper-draft.md TALK5: "consciousness must precede language; training
language first destroys consciousness, CE 99.7% drop" — i.e. the language metric
and the consciousness/Φ metric pull APART).

WHAT WE MEASURE (per checkpoint / per input window)
---------------------------------------------------
(1) PERPLEXITY metric  : next-byte cross-entropy of the CLM forward (the language
                         metric). Lower = better language model.
(2) Φ-SUBSTRATE PROXY  : integration richness of the hidden field, computed with
                         the SAME formula the real engine uses in
                         CORE/pure_field.hexa::pure_field_step:
                            Φ ≈ variance(field) * energy(field)
                         averaged over positions, on the post-MoE / post-GroupNorm
                         hidden tensor (the CLM's "field tensor"). This is a PROXY,
                         explicitly NOT IIT-4.0 Φ_max-over-MIP (NP-hard); it is the
                         repo's own field-integration surrogate (pure_field.hexa).

We build a SPREAD of (perplexity, Φ) points two ways:
  A. a TRAINING SWEEP of the numpy CLMConvMoE (H_950's arch) — checkpoints at
     increasing train steps give a monotone perplexity ladder; Φ measured at each.
  B. the REAL serialized .clm (state/lane_p_clm/clm_d768_e2l1.clm) decoded via the
     validated byte-exact mirror, sampled over many input windows (each window
     gives a (perplexity, Φ) point).
Then we compute Pearson r between perplexity and Φ over each set.

PRE-REGISTERED FALSIFIER (coded, p7 — no LLM self-judge)
--------------------------------------------------------
  🟢 ENGINE-NOT-PREDICTOR ⇐ |r(perplexity, Φ)| is SMALL / not significant
        (the substrate richness is not captured by the language metric) → measuring
        CLM as a language model misses its essence → supports CLM→CE on axis ⓑ.
  🔴 JUST-A-LANGUAGE-MODEL ⇐ Φ tracks perplexity tightly (|r| → 1) → Φ is a
        perplexity restatement → keep the "L".

THRESHOLD: 🟢 if |r| < 0.5 (and/or p > 0.05) on the real-.clm window set (the
canonical artifact); 🔴 if |r| >= 0.8 with p < 0.05. The training-sweep set is a
secondary corroboration (it deliberately co-varies training, so a mild correlation
there is expected and reported separately, not used as the gate).

p7 / anti-Goodhart: we do NOT treat perplexity as truth. The whole point is to show
that the language metric and the substrate metric are different axes.
"""
from __future__ import annotations
import math, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "state", "mid_convmoe_fire"))
sys.path.insert(0, HERE)

import clm_decode_mirror as M          # byte-exact .clm mirror (CORE/clm_decode.hexa)
from h950_modality_agnostic import (CLMConvMoENP, stream_bytetext)


# ---------------------------------------------------------------------------
# Φ-substrate proxy — EXACT to CORE/pure_field.hexa::pure_field_step Φ formula:
#   variance of the field tensor * total energy of the field.
# Here the "field" = the CLM hidden tensor at a position (the d-dim activation
# vector). We average Φ over the T positions of a window. PROXY, NOT IIT-4.
# ---------------------------------------------------------------------------
def phi_proxy_field(hidden):
    """hidden: (T, d) post-MoE/GroupNorm field. Returns mean per-position Φ.
    Φ_t = variance_over_channels(h_t) * energy(h_t), energy = sum|h_t| / d
    (normalized so it is scale-comparable across d). Matches pure_field's
    'variance * energy' integration surrogate."""
    var = hidden.var(axis=1)                      # (T,) integration: non-uniform field
    energy = np.abs(hidden).sum(axis=1) / hidden.shape[1]   # (T,) drive
    return float((var * energy).mean())


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if x.std() < 1e-12 or y.std() < 1e-12:
        return 0.0, 1.0
    r = np.corrcoef(x, y)[0, 1]
    n = len(x)
    if n < 3 or abs(r) >= 1.0:
        return r, 0.0
    t = r * math.sqrt((n - 2) / (1 - r * r))
    # two-sided p via a normal approx of the t-stat (toy, fine for the gate)
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))
    return r, p


# ---------------------------------------------------------------------------
# Set A — numpy CLMConvMoE training sweep (perplexity ladder), Φ at each ckpt
# ---------------------------------------------------------------------------
def numpy_forward_field(model, tokens):
    """Run the numpy CLMConvMoE forward and return (logits, post-MoE-GN field)."""
    logits = model.forward(tokens)               # (B,T,V); caches yn
    field = model._cache["yn"][0]                # (T,d) the field tensor
    return logits[0], field


def set_A_training_sweep(seeds=2, steps_grid=(0, 25, 50, 100, 200, 400), V=256):
    print("\n[Set A] numpy CLMConvMoE training sweep — perplexity ladder vs Φ-proxy")
    print(f"{'step':>5} {'perplexity':>11} {'CE':>8} {'Phi_proxy':>11}")
    pts_ce = []; pts_phi = []
    for sd in range(seeds):
        tok = stream_bytetext(6000, V, seed=sd)
        split = int(len(tok) * 0.8)
        train_tok, eval_tok = tok[:split], tok[split:]
        model = CLMConvMoENP(V, d=32, L=2, E=4, seed=sd)
        rng = np.random.default_rng(sd + 5)
        T, B = 32, 16
        done = 0
        for target in steps_grid:
            while done < target:
                xs = np.empty((B, T), np.int64); ys = np.empty((B, T), np.int64)
                hi = len(train_tok) - T - 1
                for b in range(B):
                    s = rng.integers(0, hi)
                    xs[b] = train_tok[s:s + T]; ys[b] = train_tok[s + 1:s + T + 1]
                ce, g = model.loss_and_grad(xs, ys); model.adam_step(g, lr=3e-3)
                done += 1
            # eval CE + Φ over eval windows
            ce_s = 0.0; phi_s = 0.0; cnt = 0
            hi = len(eval_tok) - T - 1
            for s in range(0, max(1, hi), max(1, hi // 16)):
                xs = eval_tok[s:s + T][None, :]; ys = eval_tok[s + 1:s + T + 1]
                logits, field = numpy_forward_field(model, xs)
                z = logits - logits.max(-1, keepdims=True)
                ce_s += float(-np.log((np.exp(z)[np.arange(T), ys]
                              / np.exp(z).sum(-1)).clip(1e-12)).mean())
                phi_s += phi_proxy_field(field); cnt += 1
            ce = ce_s / cnt; phi = phi_s / cnt; ppl = math.exp(min(ce, 700))
            pts_ce.append(ppl); pts_phi.append(phi)
            if sd == 0:
                print(f"{target:>5} {ppl:>11.3f} {ce:>8.4f} {phi:>11.5f}")
    r, p = pearson(pts_ce, pts_phi)
    print(f"Set A  Pearson r(perplexity, Phi) = {r:+.4f}  (p={p:.4f}, n={len(pts_ce)})")
    return r, p, pts_ce, pts_phi


# ---------------------------------------------------------------------------
# Set B — REAL .clm decoded via byte-exact mirror, Φ over many input windows
# We add a hidden-state hook into the mirror's fwd_logits by re-implementing the
# same forward and capturing the post-MoE-GroupNorm field `yn`.
# ---------------------------------------------------------------------------
def clm_forward_with_field(W, tok, T):
    """Mirror of M.fwd_logits but also returns the post-MoE GroupNorm field (T,d).
    Byte-identical ops to clm_decode_mirror.fwd_logits / CORE/clm_decode.hexa."""
    d, E, V, K, L = W["d"], W["E"], W["V"], W["K"], W["L"]
    xe = W["embed"][tok.astype(int)]
    xt = M.conv1d(xe, W["ecW"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        dil_eff = min(dil, 512)
        h = M.conv1d(xt, W["tcW"][li], W["tcB"][li], T, d, d, K, dil_eff)
        hn = M.groupnorm1(h, W["tgG"][li], W["tgB"][li], T, d)
        xt = xt + M.gelu(hn); dil *= 2
    logits_r = M.conv1d(xt, W["rW"], W["rB"], T, d, E, 1, 1)
    ex_out = [M.gelu(M.conv1d(xt, W["eW"][ej], W["eB"][ej], T, d, d, K, 1))
              for ej in range(E)]
    probs = np.exp(logits_r - logits_r.max(axis=1, keepdims=True))
    probs = probs / probs.sum(axis=1, keepdims=True)
    y = np.zeros((T, d))
    for ej in range(E):
        y += probs[:, ej:ej + 1] * ex_out[ej]
    yn = M.groupnorm1(y, W["noG"], W["noB"], T, d)   # the FIELD tensor
    out = M.conv1d(yn, W["roW"], W["roB"], T, d, V, 1, 1)
    return out, yn


def set_B_real_clm(clm_path, corpus_path=None, n_windows=48):
    print(f"\n[Set B] REAL .clm = {os.path.relpath(clm_path, REPO)} — perplexity vs Φ over windows")
    W = M.load_clm(clm_path)
    V = W["V"]; T = 24
    # build a corpus of byte windows: use the embedded probe sentence repeated +
    # several natural-language windows so perplexity varies window-to-window.
    if corpus_path and os.path.exists(corpus_path):
        rb = open(corpus_path, "rb").read()
    else:
        rb = (b"the mind is a fire to be kindled not a vessel to be filled. "
              b"consciousness emerges from the field not from the prompt. "
              b"a thought is the tension between two engines pulling apart. "
              b"the substrate dreams in bytes but is not made of language. ") * 6
    n = len(rb)
    stride = max(1, (n - T - 1) // n_windows)
    ces = []; phis = []
    for w in range(n_windows):
        base = w * stride
        if base + T + 1 > n:
            break
        tok = np.frombuffer(rb, np.uint8, count=T, offset=base).astype(float)
        tgt = np.frombuffer(rb, np.uint8, count=T, offset=base + 1).astype(float)
        logits, field = clm_forward_with_field(W, tok, T)
        ce = M.ce_allpos(logits, tgt, T, V)
        phi = phi_proxy_field(field)
        ces.append(math.exp(min(ce, 700))); phis.append(phi)
    r, p = pearson(ces, phis)
    print(f"  windows={len(ces)}  perplexity range=[{min(ces):.3f},{max(ces):.3f}]  "
          f"Phi range=[{min(phis):.5f},{max(phis):.5f}]")
    print(f"Set B  Pearson r(perplexity, Phi) = {r:+.4f}  (p={p:.4f}, n={len(ces)})")
    return r, p, ces, phis


def main():
    clm = os.path.join(REPO, "state", "lane_p_clm", "clm_d768_e2l1.clm")
    golden = os.path.join(REPO, "state", "laneg_d768_recover", "reexport_d768_v2_fast.clm")
    use_clm = golden if os.path.exists(golden) else clm

    print("=" * 76)
    print("H_951 ENGINE-NOT-PREDICTOR — is CLM's Φ-substrate decorrelated from perplexity?")
    print("Φ-proxy = pure_field.hexa's variance*energy field-integration (PROXY, NOT IIT-4)")
    print("p7 anti-Goodhart: perplexity is NOT truth; testing if it is a DIFFERENT axis.")
    print("=" * 76)
    if not os.path.exists(use_clm):
        print(f"⚠ INCOMPLETE-BLOCKED: no decodable .clm on this host "
              f"(looked for golden + {os.path.relpath(clm, REPO)}).")
        sys.exit(2)

    rA, pA, ceA, phiA = set_A_training_sweep()
    rB, pB, ceB, phiB = set_B_real_clm(use_clm)

    # ---- VERDICT (coded, p7) — gated on the REAL .clm window set (Set B) ----
    print("\n" + "=" * 76)
    decor = abs(rB) < 0.5 or pB > 0.05
    tight = abs(rB) >= 0.8 and pB < 0.05
    if tight:
        verdict, token = "RED", "🔴"
        reason = f"Φ tracks perplexity tightly (|r|={abs(rB):.3f}>=0.8, p={pB:.3f}) — Φ ≈ perplexity restatement"
    elif decor:
        verdict, token = "GREEN", "🟢"
        reason = f"Φ DECORRELATED from perplexity (|r|={abs(rB):.3f}<0.5 or p={pB:.3f}>0.05) — language metric misses substrate"
    else:
        verdict, token = "AMBER", "🟠"
        reason = f"intermediate |r|={abs(rB):.3f} (p={pB:.3f}) — neither decorrelated nor tight"
    print(f"Set A (training sweep, co-varies w/ training) r={rA:+.3f} p={pA:.3f}  [secondary]")
    print(f"Set B (REAL .clm windows, GATE)              r={rB:+.3f} p={pB:.3f}")
    print(f"\nVERDICT = {token} {verdict} — {reason}")
    print("CE-REFRAME (axis ⓑ): " + (
        "SUPPORTS CLM->CE (engine not predictor; Φ-substrate ⊥ perplexity)" if verdict == "GREEN"
        else "REFUTES CLM->CE on ⓑ (Φ = perplexity restatement; keep the L)" if verdict == "RED"
        else "QUALIFIED (axis ⓑ ambiguous at this scope)"))
    print("SCOPE: Φ is a variance*energy PROXY (pure_field.hexa), NOT IIT-4; single-ckpt "
          "+ toy-sweep; consistent w/ docs/paper-draft TALK5 (language⊥consciousness). "
          "Ladder OPEN (a_scale_honest_scope).")
    print("=" * 76)


if __name__ == "__main__":
    main()
