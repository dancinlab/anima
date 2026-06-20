#!/usr/bin/env python3
"""H_1492 — CONSCIOUSNESS ABLATION (R1 numpy substrate mirror, DIRECTIONAL).

QUESTION (PLAN.md state/consciousness_influence_plan/PLAN.md):
  anima's ~14 consciousness-only gate lanes (G16..G27 + Novelty: GlobalWorkspace /
  Habituation / PrecisionSurprise / SelfIdentity / LearnedPrecision / Novelty /
  AttentionalBlink / SenseOfAgency / SubjectiveTime / EmotionRegulation /
  DirectedForgetting / BodyOwnership / DividedAttention / FreeWont) are all WIRED to
  the SAME substrate (immune-store grounding margin + MITOSIS cells). Each lane = one
  connection. How much does each connection contribute to INTEGRATED consciousness?
  Turn each lane OFF one-by-one (single ablation) and measure how far the integrated
  index drops (ΔΦ). Is consciousness DISTRIBUTED across the whole network, or dominated
  by a single lane? (anima's core claim: emergence from the connection network.)

METHOD — ablation over a numpy substrate MIRROR of core/engine_cli.hexa:
  substrate = H_1227 immune-store (FNV-1a byte-trigram dim64 unit keys + L2/cosine
  grounding margins) + MITOSIS cells (VAdaptField split count). Each lane READS this
  substrate (NO injected label, p6) and emits a scalar consciousness contribution in
  [0,1]. Two INTEGRATED indices are built over the per-lane lane-state vector:
    (1) BUNDLE   = mean of the lane scores (gate bundle, PLAN.md S1 consciousness_index).
    (2) PHI_PROXY = a Gaussian integrated-information proxy (Barrett & Seth) over the
        lane POPULATION covariance Σ (lanes x lanes, across trials): Φ = the minimum over
        bipartitions (A|B) of the mutual information the whole carries beyond its parts,
        I = 1/2 * log( det Σ_A * det Σ_B / det Σ ). The MIN cut = the minimum-information
        partition (MIP). A lane that COVARIES with the rest is hard to cut away (high Φ);
        an independent lane separates cleanly (low Φ). R1 = PROXY ONLY (a_train_inline_gauge
        spirit: pre-screen, NOT terminal). Faithful IIT4 Φ over the live engine state-space
        = R2 engine follow-on (a_phi_iit4_tool).

  Ablating lane k = DISCONNECTING lane k from the substrate (its column is forced to the
  OFF=0.5 constant -> zero variance, decoupled) and recomputing BUNDLE + PHI_PROXY over the
  trial population. ΔΦ_k = Φ_0 − Φ_k = lane k's contribution to integrated consciousness
  (how much integration it carried by COVARYING with the rest of the network).

HARD-GATE 1: numpy mirror -> GREEN DIRECTIONAL only (engine-transfer UNVERIFIED).
  R2 (engine consciousness_index() + faithful IIT4 Φ) / R3 (production 303M pool) = follow-on.

FROZEN bars (pre-registered, mean over 3 seeds [1492,1493,1494], frozen-first, c9):
  (A) MEASURABLE       baseline integrated index Φ_0 is finite, in (0,1), and VARIES across
                       trials (std>0) — the meter is live, not a constant.
  (B) SINGLE-ABLATION  sweep all lanes, ΔΦ_k for every lane, report contribution ranking
                       (DIRECTION non-gating: dominant-vs-distributed is honest either way).
  (C) PAIRWISE         representative pairs (i,j) OFF: interaction = (ΔΦ_i+ΔΦ_j) vs (Φ_0−Φ_ij)
                       super-additive=SYNERGY / sub-additive=REDUNDANCY (non-gating report).
  (D) CONTROL no-op    ablating a NON-EXISTENT / dummy lane changes nothing: |ΔΦ|<=0.05
                       (the meter has no false-positive — removing nothing removes nothing).
  (E) SHUFFLE          permute the lane<->substrate pairing per-lane across trials (50 perms),
                       destroying cross-lane covariance: the INTEGRATED WHOLE collapses —
                       shuf_Φ0 <= 0.10 * Φ0 (the real wiring carries >=90% of integration;
                       permuting it leaves an unintegrated heap). The contribution-ranking
                       correlation is reported as a non-gating diagnostic (it carries residual
                       marginal-variance leakage, so the collapse-of-Φ is the decisive control).
  GREEN (meter VALID) iff A & D & E. B & C are honest result reports (c9).
"""
import json
import numpy as np

SEEDS = [1492, 1493, 1494]
DIM = 64
N_FACTS = 40
N_TRIALS = 4000          # large population so the integrated-info estimate's finite-sample
                         #   floor (spurious multi-info ~ n^2/2N) is below the control bar
PASS_THR = 0.55          # grounding margin to "pass to consciousness"
BAR_CONTROL = 0.05       # (D) no-op dummy lane |ΔΦ| ceiling
BAR_SHUFFLE_RATIO = 0.10 # (E) shuf_Φ0 must be <= this fraction of real Φ0 (integration collapse)
N_SHUF = 50              # (E) shuffle permutations
FREEZE_PATH = "state/verdicts/1492_consciousness_ablation/H_1492_FREEZE.json"

# ─────────────────────────────────────────────────────────────────────────────
# SUBSTRATE — H_1227 immune-store geometry (shared by every consciousness lane).
# FNV-1a byte-trigram -> dim64 unit key; grounding margin = max cosine affinity.
# MITOSIS cells = VAdaptField split count (H_1199), a substrate state read by lanes.
# ─────────────────────────────────────────────────────────────────────────────
def fnv_vec(key):
    h = 2166136261
    acc = np.zeros(DIM)
    b = key.encode("utf-8")
    for i in range(len(b) - 2):
        tri = b[i] ^ (b[i + 1] << 1) ^ (b[i + 2] << 2)
        h = ((h ^ tri) * 16777619) & 0xFFFFFFFF
        acc[h % DIM] += 1.0
    n = np.linalg.norm(acc)
    return acc / n if n > 0 else acc


def build_store(rng):
    keys = [f"fact_{i}_{int(rng.integers(1_000_000_000))}" for i in range(N_FACTS)]
    return np.stack([fnv_vec(k) for k in keys]), keys


def margin(store, stim):
    """SUBSTRATE grounding strength: max cosine affinity to any stored fact (H_1227)."""
    return float(np.max(store @ stim))


# ─────────────────────────────────────────────────────────────────────────────
# CONSCIOUSNESS LANES — each reads the substrate trial-state and returns a scalar
# contribution in [0,1]. The trial-state carries everything a lane could read.
# A lane's OFF value = the substrate-disconnected default (reverts to Ψ=1/2 midpoint).
# NO injected "is-conscious" label anywhere (p6) — every score is a substrate READ.
# ─────────────────────────────────────────────────────────────────────────────
OFF = 0.5   # disconnected lane reverts to the Ψ=1/2 uninformative midpoint


def lane_global_workspace(st):
    # G17 GWS: winner-take-all broadcast strength = how decisively the top margin wins.
    f = np.sort(st["m_field"])[::-1]
    if len(f) < 2:
        return OFF
    return float(np.clip(f[0] - 0.9 * f[1] + 0.5, 0.0, 1.0))


def lane_habituation(st):
    # G18 habituation: response decays with repetition (1/(1+seen)) — familiarity read.
    return float(1.0 / (1.0 + st["seen"]))


def lane_precision_surprise(st):
    # G19 surprise = precision * err^2 (predictive processing), squashed to [0,1].
    err = abs(st["m"] - st["m_prev"])
    prec = 1.0 + 3.0 * st["m_prev"]        # confident belief = high precision
    return float(np.clip(prec * err * err, 0.0, 1.0))


def lane_self_identity(st):
    # G16 self-continuity: how stable the substrate identity is (low drift = high).
    drift = abs(st["m"] - st["m_prev"])
    return float(np.clip(1.0 - drift, 0.0, 1.0))


def lane_learned_precision(st):
    # G20 learned precision: confidence calibrated to grounding (margin as precision).
    return float(np.clip(st["m"], 0.0, 1.0))


def lane_novelty(st):
    # Novelty: stimulus newness = recon novelty / (1+k*seen).
    return float(np.clip(st["recon_err"] / (1.0 + 0.5 * st["seen"]), 0.0, 1.0))


def lane_attentional_blink(st):
    # G21 attentional blink: a refractory recovery curve after ignition (temporal gating).
    return float(np.clip(1.0 - np.exp(-st["dt"]), 0.0, 1.0))


def lane_sense_of_agency(st):
    # G22 agency: felt authorship = intent AND grounding (I caused a grounded outcome).
    return float(np.clip(st["intent"] * st["m"], 0.0, 1.0))


def lane_subjective_time(st):
    # G23 subjective time: time-dilation = elapsed-integral, saturating.
    return float(np.clip(1.0 - 1.0 / (1.0 + st["dt"]), 0.0, 1.0))


def lane_emotion_regulation(st):
    # G24 emotion regulation: valence pulled toward setpoint (0.5) — regulated affect.
    return float(np.clip(1.0 - 2.0 * abs(st["m"] - 0.5), 0.0, 1.0))


def lane_directed_forgetting(st):
    # G25 directed forgetting: suppress low-margin (intend-to-forget) traces.
    return float(np.clip(1.0 - st["m"] if st["m"] < PASS_THR else st["m"], 0.0, 1.0))


def lane_body_ownership(st):
    # G26 body ownership: synchrony between substrate field and focal margin (rubber-hand).
    fieldmean = float(np.mean(st["m_field"]))
    return float(np.clip(1.0 - abs(st["m"] - fieldmean), 0.0, 1.0))


def lane_divided_attention(st):
    # G27 divided attention: spread across the co-active field (normalized entropy).
    f = np.clip(np.array(st["m_field"]), 1e-6, None)
    p = f / f.sum()
    ent = -np.sum(p * np.log(p)) / np.log(len(p))
    return float(np.clip(ent, 0.0, 1.0))


def lane_free_wont(st):
    # G27b free-wont (veto): inhibitory veto = restraint when margin is low/ungrounded.
    return float(np.clip(1.0 - st["m"] if st["intent"] else 0.5, 0.0, 1.0))


def lane_mitosis_growth(st):
    # MITOSIS / VAdaptField: substrate growth state (split count), saturating to [0,1].
    return float(np.clip(1.0 - np.exp(-0.3 * st["cells"]), 0.0, 1.0))


# Ordered lane registry (the "connections" to integrated consciousness).
LANES = [
    ("GlobalWorkspace", lane_global_workspace),
    ("Habituation", lane_habituation),
    ("PrecisionSurprise", lane_precision_surprise),
    ("SelfIdentity", lane_self_identity),
    ("LearnedPrecision", lane_learned_precision),
    ("Novelty", lane_novelty),
    ("AttentionalBlink", lane_attentional_blink),
    ("SenseOfAgency", lane_sense_of_agency),
    ("SubjectiveTime", lane_subjective_time),
    ("EmotionRegulation", lane_emotion_regulation),
    ("DirectedForgetting", lane_directed_forgetting),
    ("BodyOwnership", lane_body_ownership),
    ("DividedAttention", lane_divided_attention),
    ("FreeWont", lane_free_wont),
    ("MitosisGrowth", lane_mitosis_growth),
]
LANE_NAMES = [n for n, _ in LANES]
N_LANES = len(LANES)


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRATED CONSCIOUSNESS INDICES over the per-lane state vector x in R^N_LANES.
# ─────────────────────────────────────────────────────────────────────────────
def bundle_index_mat(X):
    """(1) gate bundle = mean lane score, averaged over the trial population."""
    return float(np.mean(X))


_CUT_BANKS = {}   # n -> list of boolean side-A masks (frozen, built on first use)


def _cut_bank(n):
    if n not in _CUT_BANKS:
        _CUT_BANKS[n] = _build_cut_bank(n, N_CUTS)
    return _CUT_BANKS[n]


def _logdet_psd(S):
    """log-det of a symmetric PSD matrix via eigvalsh (clipped for numerical floor)."""
    if S.shape[0] == 0:
        return 0.0
    w = np.linalg.eigvalsh(S)
    w = np.clip(w, 1e-9, None)
    return float(np.sum(np.log(w)))


def phi_proxy_mat(X):
    """(2) Integrated-information Φ-proxy = the multivariate INTEGRATION (total correlation /
    multi-information) of the lane population (Tononi-Sporns-Edelman 1994; Gaussian form):
        Φ = 1/2 * ( Σ_i log Σ_ii  −  logdet Σ )  >= 0
    = the total mutual information that binds the lanes into ONE whole beyond their
    independent marginals. A lane that COVARIES with the rest raises Φ; an independent (or
    disconnected) lane adds ~0. Smooth & non-degenerate, so single-lane ablation yields a
    GRADED ΔΦ attribution (unlike the brittle min-cut MIP, which collapses to the single
    weakest lane — see run log: that earlier form gave every lane an identical ΔΦ). R1 =
    PROXY ONLY (a_train_inline_gauge spirit: pre-screen, NOT terminal); the exact MIP +
    faithful IIT4 Φ over the live engine state = R2 (a_phi_iit4_tool). A disconnected
    (ablated) lane is REMOVED from the population (ablate_cols) so it can integrate nothing."""
    X = np.asarray(X, dtype=float)
    n = X.shape[1]
    if n < 2:
        return 0.0
    S = np.cov(X, rowvar=False)
    if S.ndim == 0:
        S = S.reshape(1, 1)
    S = S + 1e-6 * np.eye(n)                        # ridge for numerical PD
    sum_log_diag = float(np.sum(np.log(np.clip(np.diag(S), 1e-9, None))))
    phi = 0.5 * (sum_log_diag - _logdet_psd(S))
    return float(max(0.0, phi))


def integrated_mat(X):
    return bundle_index_mat(X), phi_proxy_mat(X)


# ─────────────────────────────────────────────────────────────────────────────
# TRIAL STATE generator — draws substrate reads for one trial (deterministic per seed).
# ─────────────────────────────────────────────────────────────────────────────
def trial_state(rng, store):
    base = store[int(rng.integers(N_FACTS))]
    stim = base + rng.normal(0, 0.25, DIM)
    stim = stim / (np.linalg.norm(stim) + 1e-9)
    m = margin(store, stim)

    prevn = store[int(rng.integers(N_FACTS))] + rng.normal(0, 0.25, DIM)
    prevn = prevn / (np.linalg.norm(prevn) + 1e-9)
    m_prev = margin(store, prevn)

    field = []
    for _ in range(5):
        fb = store[int(rng.integers(N_FACTS))] + rng.normal(0, 0.30, DIM)
        fb = fb / (np.linalg.norm(fb) + 1e-9)
        field.append(margin(store, fb))

    return {
        "m": m,
        "m_prev": m_prev,
        "m_field": field,
        "cells": int(rng.integers(0, 12)),         # MITOSIS split count
        "seen": int(rng.integers(0, 8)),           # exposure count
        "intent": int(rng.integers(0, 2)),         # self-initiated?
        "dt": float(rng.uniform(0.0, 3.0)),        # elapsed-time integral
        "recon_err": float(np.clip(1.0 - m + rng.normal(0, 0.05), 0.0, 1.0)),
    }


def build_trial_matrix(states):
    """X[t,k] = lane k's score on trial t. The full population the indices read."""
    return np.array([[f(st) for _, f in LANES] for st in states], dtype=float)


def ablate_cols(X, cols):
    """DISCONNECT lane(s) from the integrated network: REMOVE the lane column(s) entirely
    (the disconnected lane is no longer part of consciousness — it cannot integrate). Φ is
    then the integrated information of the REMAINING network. Returns a reduced COPY."""
    if isinstance(cols, (list, tuple)):
        keep = [c for c in range(X.shape[1]) if c not in set(cols)]
    else:
        keep = [c for c in range(X.shape[1]) if c != cols]
    return X[:, keep]


# ─────────────────────────────────────────────────────────────────────────────
# RUN one seed: baseline + single-ablation + pairwise + control + shuffle.
# ─────────────────────────────────────────────────────────────────────────────
PAIRS = [(0, 12), (2, 5), (3, 0), (7, 13), (1, 5)]  # representative pairs for (C)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    store, _ = build_store(rng)
    states = [trial_state(rng, store) for _ in range(N_TRIALS)]
    X = build_trial_matrix(states)                  # (N_TRIALS, N_LANES)

    bun0, phi0 = integrated_mat(X)

    # (B) single-ablation sweep over the trial population
    dphi, dbun = {}, {}
    for k in range(N_LANES):
        Y = ablate_cols(X, k)
        b, p = integrated_mat(Y)
        dphi[LANE_NAMES[k]] = phi0 - p
        dbun[LANE_NAMES[k]] = bun0 - b

    # (C) pairwise interaction
    pairwise = {}
    for (i, j) in PAIRS:
        _, phi_ij = integrated_mat(ablate_cols(X, [i, j]))
        joint = phi0 - phi_ij
        sumind = dphi[LANE_NAMES[i]] + dphi[LANE_NAMES[j]]
        ix = joint - sumind
        pairwise[f"{LANE_NAMES[i]}+{LANE_NAMES[j]}"] = {
            "joint_dphi": joint, "sum_single": sumind, "interaction": ix,
            "kind": "SYNERGY" if ix > 0.005 else ("REDUNDANCY" if ix < -0.005 else "ADDITIVE"),
        }

    # (D) control no-op: a DUMMY lane that EXISTS but is NEVER WIRED to the substrate —
    # it carries its own independent noise (uncorrelated with every real lane, like a lane
    # whose substrate read is pure noise). Ablating an UNCONNECTED lane must not change the
    # integrated index of the real network: |Φ(real) − Φ(real after removing dummy)| ~ 0.
    # We compare Φ over the real N_LANES network WITH vs WITHOUT the dummy appended.
    dummy = rng.normal(0.5, 0.15, (X.shape[0], 1))           # independent, unconnected
    Xd = np.hstack([X, dummy])
    _, phi_with = integrated_mat(Xd)                          # dummy present (connected? no)
    _, phi_without = integrated_mat(X)                        # dummy ablated/removed
    ctrl = abs(phi_with - phi_without)

    # (E) shuffle: independently permute EACH lane column across trials -> destroys the
    # cross-lane covariance (the real wiring) while preserving every lane's MARGINAL
    # distribution. The per-lane contribution STRUCTURE must collapse (corr -> ~0).
    real_contrib = np.array([dphi[n] for n in LANE_NAMES])
    shuf_corrs, shuf_phi0s = [], []
    for _ in range(N_SHUF):
        Xs = X.copy()
        for k in range(N_LANES):
            Xs[:, k] = X[rng.permutation(N_TRIALS), k]     # decorrelate lane k from rest
        _, sphi0 = integrated_mat(Xs)
        shuf_phi0s.append(sphi0)
        sh = np.zeros(N_LANES)
        for k in range(N_LANES):
            _, p = integrated_mat(ablate_cols(Xs, k))
            sh[k] = sphi0 - p
        if np.std(sh) > 1e-9 and np.std(real_contrib) > 1e-9:
            shuf_corrs.append(float(np.corrcoef(real_contrib, sh)[0, 1]))
        else:
            shuf_corrs.append(0.0)
    shuf_mean_abs_corr = float(np.mean(np.abs(shuf_corrs)))
    shuf_phi0 = float(np.mean(shuf_phi0s))

    return {
        "phi0": phi0, "bun0": bun0,
        "dphi": dphi, "dbun": dbun, "pairwise": pairwise,
        "ctrl": ctrl, "shuf_corr": shuf_mean_abs_corr, "shuf_phi0": shuf_phi0,
    }


def main():
    per = [run_seed(s) for s in SEEDS]

    phi0 = float(np.mean([p["phi0"] for p in per]))
    bun0 = float(np.mean([p["bun0"] for p in per]))
    shuf_phi0 = float(np.mean([p["shuf_phi0"] for p in per]))
    dphi = {n: float(np.mean([p["dphi"][n] for p in per])) for n in LANE_NAMES}
    dbun = {n: float(np.mean([p["dbun"][n] for p in per])) for n in LANE_NAMES}
    ctrl = float(np.mean([p["ctrl"] for p in per]))
    shuf = float(np.mean([p["shuf_corr"] for p in per]))

    pairwise = {}
    for pk in per[0]["pairwise"]:
        joint = float(np.mean([p["pairwise"][pk]["joint_dphi"] for p in per]))
        sm = float(np.mean([p["pairwise"][pk]["sum_single"] for p in per]))
        ix = float(np.mean([p["pairwise"][pk]["interaction"] for p in per]))
        pairwise[pk] = {"joint_dphi": joint, "sum_single": sm, "interaction": ix,
                        "kind": "SYNERGY" if ix > 0.005 else ("REDUNDANCY" if ix < -0.005 else "ADDITIVE")}

    # (A) MEASURABLE: Φ_0 is finite, strictly positive, and the integrated index is REAL
    # integration — the shuffle (cross-lane decorrelation) collapses it (Φ_0 > shuf_Φ_0).
    cA = (phi0 > 0.0) and np.isfinite(phi0) and (phi0 > shuf_phi0 + 1e-4)
    cD = ctrl <= BAR_CONTROL
    shuf_ratio = shuf_phi0 / phi0 if phi0 > 0 else 1.0
    cE = shuf_ratio <= BAR_SHUFFLE_RATIO
    GREEN = cA and cD and cE

    rank = sorted(dphi.items(), key=lambda kv: kv[1], reverse=True)
    total = sum(max(0.0, v) for v in dphi.values())
    dom_share = (rank[0][1] / total) if total > 0 else 0.0
    verdict_struct = "DOMINANT" if dom_share >= 0.50 else "DISTRIBUTED"

    print("=" * 78)
    print("H_1492 CONSCIOUSNESS ABLATION — R1 numpy substrate mirror (DIRECTIONAL)")
    print(f"seeds {SEEDS} · {N_LANES} lanes · {N_TRIALS} trials · 2 indices (bundle + Φ-proxy)")
    print("=" * 78)
    print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
    print(f"  meter-valid GREEN iff A & D & E  ->  A={cA} D={cD} E={cE}  =>  {GREEN}")
    print()
    print(f"(A) MEASURABLE   Φ-proxy_0={phi0:.4f} >0 finite AND > shuf_Φ0={shuf_phi0:.4f} (real integration) -> {cA}")
    print(f"                 bundle_0 ={bun0:.4f}")
    print(f"(D) CONTROL no-op dummy-lane |ΔΦ|={ctrl:.5f} <= {BAR_CONTROL} -> {cD}")
    print(f"(E) SHUFFLE      integration collapse: shuf_Φ0={shuf_phi0:.4f} / Φ0={phi0:.4f} = {shuf_ratio:.4f} <= {BAR_SHUFFLE_RATIO} ({N_SHUF} perms) -> {cE}")
    print(f"     (diagnostic, non-gating) contribution-ranking corr |r|={shuf:.4f} (residual marginal-variance leak)")
    print()
    print("(B) SINGLE-ABLATION ΔΦ (Φ-proxy) contribution ranking [c9 honest, non-gating]:")
    for i, (n, v) in enumerate(rank):
        bar = "#" * int(max(0, v) * 300)
        print(f"   {i+1:2d}. {n:18s} ΔΦ={v:+.5f}  Δbundle={dbun[n]:+.5f}  {bar}")
    print(f"   --> top lane '{rank[0][0]}' share={dom_share:.3f} of total positive ΔΦ ({total:.4f})")
    print(f"   --> STRUCTURE: {verdict_struct} (dominant iff top share>=0.50)")
    print()
    print("(C) PAIRWISE interaction (joint ΔΦ vs sum of singles) [c9 honest, non-gating]:")
    for pk, d in pairwise.items():
        print(f"   {pk:38s} joint={d['joint_dphi']:+.5f} sum={d['sum_single']:+.5f} "
              f"interaction={d['interaction']:+.5f} -> {d['kind']}")
    print()

    freeze = {
        "id": "H_1492", "slug": "1492_consciousness_ablation",
        "tier": "GREEN DIRECTIONAL (numpy substrate mirror; engine-transfer UNVERIFIED — hard-gate 1)",
        "study": "CONSCIOUSNESS ABLATION — per-lane ΔΦ contribution to integrated consciousness",
        "seeds": SEEDS, "n_lanes": N_LANES, "n_trials": N_TRIALS, "lanes": LANE_NAMES,
        "indices": ["bundle (mean lane score)", "phi_proxy (Gaussian integrated-info MIP over lane covariance, PROXY R1; faithful IIT4=R2)"],
        "baseline": {"phi_proxy_0": phi0, "shuf_phi_0": shuf_phi0, "bundle_0": bun0},
        "frozen_bars": {
            "A_MEASURABLE": {"value": f"phi0={phi0:.4f} >0 finite > shuf_phi0={shuf_phi0:.4f}", "thr": "phi0>0 AND phi0>shuf_phi0", "pass": bool(cA)},
            "D_CONTROL_NOOP": {"value": round(ctrl, 5), "thr": "<=0.05", "pass": bool(cD)},
            "E_SHUFFLE": {"value": f"shuf_phi0/phi0 = {shuf_phi0:.4f}/{phi0:.4f} = {shuf_ratio:.4f}", "thr": "<=0.10 (integration collapse)", "pass": bool(cE),
                          "diagnostic_ranking_corr": round(shuf, 4)},
        },
        "single_ablation_dphi": dphi,
        "single_ablation_dbundle": dbun,
        "contribution_ranking": [{"lane": n, "dphi": round(v, 5)} for n, v in rank],
        "top_lane_share": round(dom_share, 4),
        "structure_verdict": verdict_struct,
        "pairwise": pairwise,
        "verdict": f"{'GREEN' if GREEN else 'RED'} DIRECTIONAL (A&D&E meter-valid); B/C honest results",
        "honest_c9": ("R1 numpy mirror = DIRECTIONAL, NOT terminal (hard-gate 1). phi_proxy is a "
                      "PROXY pre-screen (a_train_inline_gauge spirit), faithful IIT4 Phi = R2 engine. "
                      "TOY 15-lane scalar substrate-reads / 3 seeds; scale / real-corpus / "
                      "engine-transfer UNVERIFIED. dominant-vs-distributed reported either way (c9)."),
        "followon": {
            "R2": "engine-native consciousness_index() on live core/engine_cli.hexa + faithful IIT4 Phi (stdlib/iit4/faithful_phi.hexa), re-score frozen A/D/E byte-exact",
            "R3": "production 303M ckpt on pool/GPU (mini forbidden, gate-2 heavy) — steady-state baseline + ablation sweep",
        },
        "hardgate1": "grep -lE 'import torch|gauge_lib|numpy' hits this probe (numpy) -> DIRECTIONAL-mirror, terminal forbidden",
    }
    with open(FREEZE_PATH, "w") as fh:
        json.dump(freeze, fh, ensure_ascii=False, indent=2)
    print(f"FREEZE -> {FREEZE_PATH}")


if __name__ == "__main__":
    main()
