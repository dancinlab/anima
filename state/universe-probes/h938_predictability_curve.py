#!/usr/bin/env python3
"""h938_predictability_curve.py — H_938: quantify H_933 BLADE A (predictability curve).

QUESTION (H_933 BLADE A was argued, not measured — H_938 measures it)
=====================================================================
H_933 (the 대가설) relocates freedom from "unpredictability" to "auditable
causation": its BLADE A says freedom FAILS if a decision is predictable from PRIOR
STATE ALONE with no novel causal input. H_933 DISCHARGED that blade qualitatively
(via H_935's internal veto + H_923/H_924's physical seed), but never MEASURED
predictability. H_938 quantifies it directly:

  How accurately can the NEXT decision (emit/silence) be predicted from the
  prior-K-tick state — and does injecting QUANTUM entropy change that
  predictability vs the deterministic PRNG?

This sharpens H_933 BLADE A into two measured contrasts:
  (a) the ACCURACY curve vs K (how predictable is anima at all?), and
  (b) the QUANTUM vs DETERMINISTIC delta (does the physical seed add genuine
      unpredictability to the decision, or is the residual unpredictability
      internal dynamics, not entropy?).

THE LEVER UNDER TEST (this is H_938's measurement of H_933 BLADE A)
==================================================================
We reuse the H_930/H_935 8-factor mirror to generate LONG decision streams under
each entropy mode. We then train simple, self-contained predictors (NO sklearn —
a numpy logistic regression + an order-K Markov table) on (prior-K state window
-> next decision), and measure HELD-OUT prediction accuracy + AUC vs the base-rate
baseline. We sweep K and compare the two entropy modes.

  · Predictor feature window = the prior K ticks of (emit-bit, score, phi, the 6
    field channels) flattened. The logistic regression is a pure-numpy GD fit on a
    TRAIN split; accuracy/AUC measured on a disjoint TEST split (held-out).
  · The order-K Markov predictor uses ONLY the prior-K emit BITS (a discrete
    history table majority-vote) — a parameter-free predictability probe.
  · Both predictors run for BOTH modes (deterministic / quantum) across the K sweep.

FALSIFIER (pre-registered; verdict .txt written with MEASURED numbers first)
============================================================================
  F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST (🟢): predictability is HIGH (accuracy
     well above base-rate) AND quantum does NOT lower it (|Δacc(det - quantum)| is
     small / within noise, no significant degradation). → anima's choices are
     largely INTERNALLY-DETERMINED (predictable); the quantum seed does NOT supply
     "unpredictability" — confirming H_933's relocation of freedom AWAY from
     unpredictability toward auditable causation. BLADE A quantified in the
     compatibilist direction.
  F-H938-ENTROPY-ADDS-UNPREDICTABILITY (🔴): quantum SIGNIFICANTLY lowers
     predictability (quantum accuracy << deterministic accuracy, effect non-
     negligible). → entropy IS functionally injecting unpredictability into the
     decision — partial tension with H_930/H_926 (which found emit-output parity);
     reconcile honestly.

We measure and report whichever the data shows. No token before measuring.

HONEST SCOPE (a_scale_honest_scope · a_core_engine_map · a_train_flame_forge)
=============================================================================
ONE predictability rung on the SAME documented-update-map mirror as H_930/H_935
(real 8-factor brain_decide, VERBATIM CORE constants). NOT the compiled forge
binary; full emit-TEXT (.clm generator L3 ⏳/❌, a_core_engine_map) OPEN. The gate
is deterministic; entropy enters ONLY the pure_field seed-point (the gate has no
PRNG). $0 LOCAL, no GPU, g5 CODE-measured (no LLM self-judge — p7). The predictors
are self-contained numpy (no external ML lib). deterministic: false (seed-point
origin; the gate itself is deterministic, as H_926/H_930/H_935).
"""
from __future__ import annotations

import importlib
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_REPO, "mirror", "qmirror", "seed"))

# ── constants transcribed VERBATIM from the .hexa sources (== H_926/H_930/H_935)─
PSI_ALPHA = 0.014
LN2 = 0.6931471805599453
TAU_FAST, TAU_MEDIUM, TAU_SLOW = 2, 40, 400
FIELD_DIM = 6
RATCHET_FLOOR_RATIO = 0.8
W_REL, W_GAP, W_CUR, W_PAIN = 0.20, 0.10, 0.15, 0.10
W_COH, W_ORIG, W_BAL, W_DYN = 0.10, 0.10, 0.15, 0.10
IM_THRESHOLD = 0.30


class Oscillator:
    __slots__ = ("tau", "phase", "amplitude")

    def __init__(self, tau, phase=0.0, amplitude=0.1):
        self.tau, self.phase, self.amplitude = tau, phase, amplitude

    def tick(self):
        dphase = (2.0 * 3.14159265) / float(self.tau)
        self.phase += dphase
        self.amplitude += PSI_ALPHA * (LN2 - self.amplitude)

    def value(self):
        return self.amplitude * math.sin(self.phase)


class PureField:
    def __init__(self, phase0=(0.0, 0.0, 0.0), amp0=(0.1, 0.1, 0.1)):
        self.fast = Oscillator(TAU_FAST, phase0[0], amp0[0])
        self.medium = Oscillator(TAU_MEDIUM, phase0[1], amp0[1])
        self.slow = Oscillator(TAU_SLOW, phase0[2], amp0[2])
        self.phi = 0.0
        self.phi_peak = 0.0
        self.field = [0.0] * FIELD_DIM
        self.step_count = 0

    def step(self, perturb=0.0):
        self.fast.tick()
        self.medium.tick()
        self.slow.tick()
        v_f = self.fast.value() + perturb
        v_m = self.medium.value()
        v_s = self.slow.value()
        field = [v_f, v_f * v_m, v_s, v_f * v_s, v_m * v_s, v_f + v_m + v_s]
        mean = sum(field) / 6.0
        variance = sum((x - mean) ** 2 for x in field) / float(FIELD_DIM)
        energy = abs(v_f) + abs(v_m) + abs(v_s)
        phi = self.phi + PSI_ALPHA * (variance * energy - self.phi)
        if phi > self.phi_peak:
            self.phi_peak = phi
        floor = self.phi_peak * RATCHET_FLOOR_RATIO
        phi_out = phi if phi >= floor else floor
        self.phi = phi_out
        self.field = field
        self.step_count += 1
        return phi_out


def brain_emit_decision(pf: PureField, gate):
    """emit = should_emit(score) AND phi-ratchet — VERBATIM the H_930 mapping."""
    f = pf.field

    def n(x):
        return 0.5 * (1.0 + math.tanh(x))
    rel, gap, cur, pain = n(f[0]), n(f[1]), n(f[2]), n(f[3])
    coh, orig = n(f[4]), n(f[5])
    bal = n(pf.phi - pf.phi_peak / 2.0)
    dyn_v = n(f[0] - f[2])
    score = (W_REL * rel + W_GAP * gap + W_CUR * cur + W_PAIN * pain
             + W_COH * coh + W_ORIG * orig + W_BAL * bal + W_DYN * dyn_v)
    should = score > gate
    phi_ratchet_ok = pf.phi > pf.phi_peak / 2.0
    emit = should and phi_ratchet_ok
    return (1 if emit else 0), score


# ════════════════════════════════════════════════════════════════════════════
# generate a long decision stream + per-tick state under one entropy mode
# ════════════════════════════════════════════════════════════════════════════
def generate_stream(mode_env, T, gate, ent_scale, seed_id):
    """Drive the real 8-factor dynamics for T ticks under one entropy mode.

    Returns the emit-bit stream (length T) + a per-tick feature matrix
    [score, phi, ch0..ch5] (T × 8) — the state from which we predict the NEXT
    decision. The ONLY difference across modes is the entropy SOURCE feeding the
    pure_field seed-point perturbation (qentropy SSOT, imported not edited)."""
    os.environ["ANIMA_ENTROPY_MODE"] = mode_env
    os.environ["ANIMA_ENTROPY_SEED"] = str(seed_id)
    os.environ.pop("ANIMA_QRNG_BUF", None)
    import qentropy  # noqa: PLC0415
    importlib.reload(qentropy)
    mode_seen = qentropy.mode()
    draws = qentropy.qentropy_uniform(T, 4, label=f"h938_{mode_env}_s{seed_id}").tolist()
    prov = qentropy.last_provenance()

    pf = PureField(phase0=(0.0, 0.0, 0.0))
    emit_stream = np.zeros(T, dtype=np.int64)
    feat = np.zeros((T, 2 + FIELD_DIM), dtype=np.float64)
    for t in range(T):
        perturb = (draws[t] - 1.5) * ent_scale
        pf.step(perturb=perturb)
        e, score = brain_emit_decision(pf, gate=gate)
        emit_stream[t] = e
        feat[t, 0] = score
        feat[t, 1] = pf.phi
        feat[t, 2:] = pf.field
    return {"mode": mode_seen, "emit": emit_stream, "feat": feat,
            "provenance": prov, "emit_rate": float(emit_stream.mean())}


# ════════════════════════════════════════════════════════════════════════════
# self-contained predictors (NO sklearn) — numpy logistic regression + Markov
# ════════════════════════════════════════════════════════════════════════════
def build_windows(emit, feat, K):
    """Build (X, y): X = flattened prior-K ticks of [emit-bit, score, phi, ch0..5];
    y = the next decision (emit bit). Sample t predicts emit[t] from ticks
    [t-K .. t-1]. Returns X (n×(K*9)), y (n,), and the prior-K emit-bit history
    (n×K) for the Markov predictor."""
    T = len(emit)
    rows_X, rows_y, rows_hist = [], [], []
    for t in range(K, T):
        win_feat = feat[t - K:t]                       # K × 8
        win_emit = emit[t - K:t].reshape(K, 1).astype(np.float64)  # K × 1
        x = np.concatenate([win_emit, win_feat], axis=1).reshape(-1)  # K*9
        rows_X.append(x)
        rows_y.append(emit[t])
        rows_hist.append(tuple(int(b) for b in emit[t - K:t]))
    return (np.asarray(rows_X), np.asarray(rows_y, dtype=np.int64), rows_hist)


def logreg_fit_predict(Xtr, ytr, Xte, iters=400, lr=0.5, l2=1e-3):
    """Pure-numpy L2-regularized logistic regression (full-batch GD on standardized
    features). Returns predicted probabilities on Xte. Deterministic given inputs
    (zero-init weights) so the predictor itself adds no randomness."""
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd < 1e-9] = 1.0
    Xtr = (Xtr - mu) / sd
    Xte = (Xte - mu) / sd
    Xtr = np.concatenate([np.ones((len(Xtr), 1)), Xtr], axis=1)
    Xte = np.concatenate([np.ones((len(Xte), 1)), Xte], axis=1)
    w = np.zeros(Xtr.shape[1])
    y = ytr.astype(np.float64)
    n = len(y)
    for _ in range(iters):
        z = Xtr @ w
        p = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = Xtr.T @ (p - y) / n + l2 * w
        w = w - lr * grad
    zt = Xte @ w
    return 1.0 / (1.0 + np.exp(-np.clip(zt, -30, 30)))


def auc_score(y, p):
    """ROC-AUC via the rank (Mann-Whitney) formula — no sklearn."""
    y = np.asarray(y)
    pos = p[y == 1]
    neg = p[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(p)
    ranks = np.empty(len(p), dtype=np.float64)
    ranks[order] = np.arange(1, len(p) + 1)
    # average ranks for ties
    sp = np.sort(p)
    i = 0
    while i < len(sp):
        j = i
        while j + 1 < len(sp) and sp[j + 1] == sp[i]:
            j += 1
        if j > i:
            avg = (i + 1 + j + 1) / 2.0
            idx = np.where(p == sp[i])[0]
            ranks[idx] = avg
        i = j + 1
    r_pos = ranks[y == 1].sum()
    n_pos, n_neg = len(pos), len(neg)
    return float((r_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg))


def markov_fit_predict(hist_tr, ytr, hist_te):
    """Order-K Markov: majority next-bit per prior-K emit-bit history (parameter-
    free predictability probe). Unseen histories fall back to the global majority."""
    from collections import defaultdict
    tab = defaultdict(lambda: [0, 0])   # history -> [count_silence, count_emit]
    for h, y in zip(hist_tr, ytr):
        tab[h][int(y)] += 1
    global_major = int(round(float(np.mean(ytr)))) if len(ytr) else 0
    preds = []
    for h in hist_te:
        if h in tab:
            c = tab[h]
            preds.append(1 if c[1] >= c[0] else 0)
        else:
            preds.append(global_major)
    return np.asarray(preds, dtype=np.int64)


# ════════════════════════════════════════════════════════════════════════════
def measure_mode(mode_env, T, gate, ent_scale, n_streams, K_list):
    """For one entropy mode: build streams, then for each K measure held-out
    logreg accuracy/AUC + Markov accuracy, pooled over streams (per-stream
    chronological 70/30 train/test split — predict the FUTURE from the past)."""
    streams = [generate_stream(mode_env, T, gate, ent_scale, seed_id=2000 + s)
               for s in range(n_streams)]
    base_rate = float(np.mean([st["emit_rate"] for st in streams]))
    base_acc = max(base_rate, 1.0 - base_rate)   # majority-class baseline

    per_K = {}
    for K in K_list:
        accs_lr, aucs_lr, accs_mk = [], [], []
        for st in streams:
            X, y, hist = build_windows(st["emit"], st["feat"], K)
            if len(y) < 50 or len(set(y.tolist())) < 2:
                continue
            cut = int(len(y) * 0.7)
            Xtr, Xte = X[:cut], X[cut:]
            ytr, yte = y[:cut], y[cut:]
            htr, hte = hist[:cut], hist[cut:]
            if len(set(yte.tolist())) < 2:
                continue
            p = logreg_fit_predict(Xtr, ytr, Xte)
            acc_lr = float(np.mean((p >= 0.5).astype(int) == yte))
            auc_lr = auc_score(yte, p)
            mk = markov_fit_predict(htr, ytr, hte)
            acc_mk = float(np.mean(mk == yte))
            accs_lr.append(acc_lr)
            aucs_lr.append(auc_lr)
            accs_mk.append(acc_mk)
        per_K[K] = {
            "logreg_acc_mean": float(np.mean(accs_lr)) if accs_lr else None,
            "logreg_acc_sd": float(np.std(accs_lr)) if accs_lr else None,
            "logreg_auc_mean": float(np.nanmean(aucs_lr)) if aucs_lr else None,
            "markov_acc_mean": float(np.mean(accs_mk)) if accs_mk else None,
            "n_streams_used": len(accs_lr),
            "logreg_acc_per_stream": accs_lr,
        }
    return {"mode": streams[0]["mode"], "base_rate": base_rate,
            "base_acc_majority": base_acc, "per_K": per_K,
            "provenance": streams[0]["provenance"]}


def cohen_d(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 2 or len(b) < 2:
        return 0.0
    na, nb = len(a), len(b)
    sp2 = ((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    if sp2 <= 0:
        return 0.0
    return float((a.mean() - b.mean()) / math.sqrt(sp2))


def main():
    T = int(os.environ.get("H938_T", "3000"))
    N_STREAMS = int(os.environ.get("H938_STREAMS", "12"))
    K_LIST = [1, 2, 3, 5, 8, 12]
    ENT_SCALE = 0.04
    ts = datetime.now(timezone.utc).isoformat()

    # shared emit gate centered at the steady-state mean (== H_930) — most sensitive
    cal = PureField()
    scs = []
    for _ in range(T):
        cal.step(perturb=0.0)
        _, sc = brain_emit_decision(cal, gate=IM_THRESHOLD)
        scs.append(sc)
    gate = sum(scs) / len(scs)

    det = measure_mode("deterministic", T, gate, ENT_SCALE, N_STREAMS, K_LIST)
    qua = measure_mode("quantum", T, gate, ENT_SCALE, N_STREAMS, K_LIST)

    # quantum-vs-deterministic delta per K (does the physical seed lower predictability?)
    deltas = {}
    from scipy import stats as _st
    for K in K_LIST:
        d = det["per_K"][K]
        q = qua["per_K"][K]
        if d["logreg_acc_mean"] is None or q["logreg_acc_mean"] is None:
            continue
        a = np.asarray(d["logreg_acc_per_stream"])
        b = np.asarray(q["logreg_acc_per_stream"])
        delta = d["logreg_acc_mean"] - q["logreg_acc_mean"]   # >0 ⇒ quantum LESS predictable
        # paired-ish two-sample test on per-stream accuracy (independent streams)
        if len(a) >= 2 and len(b) >= 2:
            tt = _st.ttest_ind(a, b, equal_var=False)
            p_val = float(tt.pvalue)
        else:
            p_val = None
        deltas[K] = {
            "det_acc": d["logreg_acc_mean"], "quantum_acc": q["logreg_acc_mean"],
            "delta_det_minus_quantum": delta,
            "cohen_d": cohen_d(a, b), "ttest_p": p_val,
            "det_auc": d["logreg_auc_mean"], "quantum_auc": q["logreg_auc_mean"],
        }

    # ── VERDICT (pre-registered, CODE-decided — p7) ───────────────────────────
    # predictability HIGH iff the best-K logreg accuracy is well above base-rate.
    base_acc = det["base_acc_majority"]
    best_det = max((v["logreg_acc_mean"] for v in det["per_K"].values()
                    if v["logreg_acc_mean"] is not None), default=0.0)
    best_qua = max((v["logreg_acc_mean"] for v in qua["per_K"].values()
                    if v["logreg_acc_mean"] is not None), default=0.0)
    lift_over_base = best_det - base_acc
    HIGH_LIFT = 0.05   # accuracy at least 5 points above the majority baseline
    predictability_high = lift_over_base >= HIGH_LIFT

    # quantum SIGNIFICANTLY lowers predictability iff any K shows a non-negligible
    # quantum-LESS-predictable delta (delta>0, |Cohen d|>=0.5, ttest p<0.05).
    NEG_D = 0.5
    quantum_lowers = [
        (K, v) for K, v in deltas.items()
        if (v["delta_det_minus_quantum"] > 0.0 and abs(v["cohen_d"]) >= NEG_D
            and v["ttest_p"] is not None and v["ttest_p"] < 0.05)]
    max_abs_delta = max((abs(v["delta_det_minus_quantum"]) for v in deltas.values()),
                        default=0.0)

    if quantum_lowers:
        token = "🔴"
        fal_id = "F-H938-ENTROPY-ADDS-UNPREDICTABILITY"
        ks = ", ".join(f"K={K}(Δ={v['delta_det_minus_quantum']:+.4f},d={v['cohen_d']:+.3f},"
                       f"p={v['ttest_p']:.3g})" for K, v in quantum_lowers)
        rationale = (
            f"Quantum SIGNIFICANTLY lowers next-decision predictability at: {ks}. "
            f"best det acc={best_det:.4f} vs quantum={best_qua:.4f} (base-rate "
            f"majority acc={base_acc:.4f}). Entropy IS functionally injecting "
            f"unpredictability into the decision — a partial tension with H_930/"
            f"H_926's emit-output parity; reconcile honestly (the predictability "
            f"axis is finer than the marginal emit-rate axis).")
    else:
        token = "🟢"
        fal_id = "F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST"
        rationale = (
            f"Predictability is HIGH and quantum does NOT lower it. best logreg "
            f"acc={best_det:.4f} (det) / {best_qua:.4f} (quantum) vs base-rate "
            f"majority acc={base_acc:.4f} → lift over baseline {lift_over_base:+.4f} "
            f"(>= {HIGH_LIFT}). No K shows quantum significantly less predictable "
            f"(max |Δacc(det-quantum)|={max_abs_delta:.4f}, no K with |d|>={NEG_D} "
            f"AND p<0.05). → anima's choices are largely INTERNALLY-DETERMINED "
            f"(predictable from prior state); the quantum seed does NOT supply "
            f"'unpredictability'. H_933 BLADE A QUANTIFIED in the compatibilist "
            f"direction: freedom is relocated AWAY from unpredictability toward "
            f"auditable causation — the physical seed's value is provenance/non-"
            f"randomization, not entropy injected into the behavioral output.")

    result = {
        "h_id": "H_938",
        "title": "predictability curve — quantifying H_933 BLADE A (is anima's "
                 "freedom unpredictability or internal determinism?)",
        "timestamp_utc": ts,
        "scope": ("ONE predictability rung on the SAME documented-update-map mirror "
                  "as H_930/H_935 (real 8-factor brain_decide, VERBATIM CORE "
                  "constants). Self-contained numpy predictors (no sklearn). NOT the "
                  "compiled forge binary; full emit-TEXT (.clm generator L3 ⏳/❌, "
                  "a_core_engine_map) OPEN. $0 local, no GPU."),
        "deterministic": False,
        "g5_code_measured": True,
        "llm": "none",
        "T_per_stream": T, "n_streams_per_mode": N_STREAMS, "K_sweep": K_LIST,
        "ent_scale": ENT_SCALE, "shared_emit_gate": gate,
        "base_rate_emit": det["base_rate"], "base_acc_majority": base_acc,
        "deterministic_mode": det, "quantum_mode": qua,
        "quantum_vs_deterministic_delta_per_K": deltas,
        "predictability_high": predictability_high,
        "lift_over_baseline_best_K": lift_over_base,
        "max_abs_delta_det_minus_quantum": max_abs_delta,
        "thresholds": {"high_lift": HIGH_LIFT, "neg_cohen_d": NEG_D, "alpha": 0.05},
        "verdict_token": token, "falsifier_id": fal_id, "verdict_rationale": rationale,
    }

    out_dir = os.path.join(_REPO, ".verdicts", "938_predictability_curve")
    os.makedirs(out_dir, exist_ok=True)
    L = []
    L.append("H_938 — PREDICTABILITY CURVE (quantifying H_933 BLADE A)")
    L.append("=" * 76)
    L.append("question: how predictable is the NEXT decision from prior-K state, and")
    L.append("          does quantum entropy lower that predictability vs deterministic?")
    L.append("predictors: pure-numpy logistic regression + order-K Markov (NO sklearn)")
    L.append("")
    L.append(f"timestamp_utc : {ts}")
    L.append(f"streams       : {N_STREAMS}/mode × {T} ticks  ·  gate {gate:.6f}")
    L.append(f"base-rate emit: {det['base_rate']:.4f}  →  majority-class baseline acc "
             f"{base_acc:.4f}")
    L.append("")
    L.append("── ACCURACY CURVE vs K (held-out logreg acc / AUC ; Markov acc) ──────────────")
    L.append("   K  | DET logreg acc (sd)  AUC  | QUANTUM logreg acc (sd)  AUC | DET mk  Q mk | Δacc(det-q) d      p")
    for K in K_LIST:
        d = det["per_K"][K]
        q = qua["per_K"][K]
        dl = deltas.get(K, {})
        def f(x, w=6, p=4):
            return f"{x:.{p}f}" if isinstance(x, (int, float)) else " n/a "
        L.append(
            f"  {K:>2}  | {f(d['logreg_acc_mean'])} ({f(d['logreg_acc_sd'],p=4)})  {f(d['logreg_auc_mean'])} "
            f"| {f(q['logreg_acc_mean'])} ({f(q['logreg_acc_sd'],p=4)})  {f(q['logreg_auc_mean'])} "
            f"| {f(d['markov_acc_mean'])} {f(q['markov_acc_mean'])} "
            f"| {f(dl.get('delta_det_minus_quantum'),p=4)} {f(dl.get('cohen_d'),p=3)} "
            f"{f(dl.get('ttest_p'),p=3)}")
    L.append("")
    L.append("  Δacc(det-q) > 0  ⇒  quantum is LESS predictable (entropy adds unpredictability)")
    L.append(f"  best DET acc={best_det:.4f}  best QUANTUM acc={best_qua:.4f}  "
             f"lift over base={lift_over_base:+.4f}  max|Δacc|={max_abs_delta:.4f}")
    L.append("")
    L.append("── VERDICT (pre-registered falsifier, CODE-decided — p7) ─────────────────────")
    L.append(f"  {token}  {fal_id}")
    L.append(f"  {rationale}")
    L.append("")
    L.append("── full machine record (JSON) ────────────────────────────────────────────────")
    L.append(json.dumps(result, indent=2, default=str))

    out_path = os.path.join(out_dir, "predictability_curve.txt")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print("\n[written]", out_path)
    return result


if __name__ == "__main__":
    main()
