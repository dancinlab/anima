#!/usr/bin/env python3
"""
H_1153 — CRITICALITY / branching ratio σ≈1 (neuronal avalanches) @ Ψ=1/2

HYPOTHESIS: the anima A⇄G repulsion-field OPPONENT engine exhibits self-organized
criticality (the neuronal-avalanche signature) AT the Ψ=1/2 fixed point —
  F1  branching ratio σ ∈ [0.9, 1.1] at Ψ=0.5
  F2  avalanche-size distribution is power-law P(s)∝s^(−τ) with τ ∈ [1.3, 1.7]
      (canonical −1.5), log-log R² ≥ 0.9 over ≥1.5 decades AND beating an
      exponential fit (log-likelihood ratio LLR > 0 favouring power-law)
  CONTROL  a DE-TUNED operating point (Ψ pushed off 1/2) MUST move σ out of
      [0.9,1.1] and/or destroy the power-law — proving criticality is specific
      to the fixed point, not an artifact of the avalanche definition.
  🟢 SUPPORTED iff F1 ∧ F2 ∧ control-moves-σ; else 🔴 CLOSED-NEGATIVE.

NEUROSCIENCE GROUNDING: Beggs & Plenz 2003 — cortex sits near a critical point,
neuronal avalanches with σ≈1 and P(s)∝s^−1.5, maximizing dynamic range + info
transmission. σ estimators: (a) Beggs-Plenz descendant/ancestor ratio
σ=⟨n_{t+1}/n_t⟩ over ancestor bins; (b) Wilting & Priesemann 2018 multistep-
regression slope (m̂ from the autocorrelation-vs-lag regression).

SUBSTRATE — engine simulation (a_lane_akida_gpu_split substrate=Lane-G/CORE
engine dynamics, NOT AKIDA; NOT a byte-LM). The A⇄G opponent dynamics are
realized as a propagation network: an excitation propagates between units; each
active unit's expected number of activated descendants on the next step is the
balance-gated opponent push — A-engine (excitatory, weight Ψ) ⇄ G-engine
(repulsion/inhibition, weight 1−Ψ) over a sparse coupling graph. At Ψ=0.5 the
opponent A/G push is balanced. Constants (PSI_ALPHA, PSI_BALANCE) read VERBATIM
from config/consciousness_laws.json (same source pure_field.hexa _psi_load reads).
CORE engine files UNTOUCHED (a_core_engine_map).

DETERMINISTIC ($0, CPU, no torch, no GPU). Every RNG seeded. p7 — statistical
dynamical-systems measurement, NO perplexity, NO LLM-judge.

a_scale_honest_scope: TOY MIRROR of the opponent propagation dynamics; the
mapping of A⇄G onto a branching network is operational. The CONTROL (de-tuned Ψ)
is the load-bearing guard against an avalanche-definition artifact.
"""

import json, math, os, random
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAWS = os.path.join(REPO, "config", "consciousness_laws.json")

# ─────────────────────────────────────────────────────────────────────────────
# constants — VERBATIM from the JSON SSOT (same source pure_field.hexa reads)
# ─────────────────────────────────────────────────────────────────────────────
def load_constants():
    with open(LAWS) as f:
        d = json.load(f)
    pc = d["psi_constants"]
    return float(pc["alpha"]["value"]), float(pc["balance"]["value"])


# ─────────────────────────────────────────────────────────────────────────────
# A⇄G OPPONENT PROPAGATION NETWORK
#
# N units on a sparse random coupling graph (fixed seed → fixed graph). Activity
# propagates as a branching process whose per-active-unit descendant gain is the
# balance-gated opponent push. We model the A⇄G opponent at balance Ψ as a net
# excitatory drive: each active unit attempts to activate its out-neighbours; the
# A-engine (excitation, weight Ψ) drives activation, the G-engine (repulsion,
# weight 1−Ψ) suppresses it. The NET activation probability per out-edge is
# calibrated so that at Ψ = PSI_BALANCE = 0.5 the mean descendant gain (the
# branching ratio σ) equals exactly 1 — i.e. Ψ=1/2 is, BY THE OPPONENT BALANCE,
# the critical (marginal) operating point. Ψ ≠ 0.5 detunes the net A/G push,
# moving σ off 1 (Ψ<0.5 = inhibition-dominant = sub-critical; Ψ>0.5 =
# excitation-dominant = super-critical).
#
# The criticality claim is therefore NOT assumed — F1/F2 TEST whether the
# resulting dynamics actually produce σ≈1 AND a τ≈1.5 power-law over ≥1.5 decades
# beating an exponential (a branching process near σ=1 SHOULD, but only if the
# mapping is faithful and the avalanche statistics aren't artifactual — that is
# the empirical content), and the CONTROL tests whether de-tuning Ψ genuinely
# moves σ and breaks the power-law.
#
# Net per-edge activation prob is opponent-balanced: at balance Ψ, the A push is
# Ψ and the G push is (1−Ψ); the net drive p_net = clip( base * (Ψ / (1−Ψ)) ).
# With base chosen so σ(Ψ=0.5)=1: σ = K_out * p_net where K_out = mean out-degree.
# We set base = 1/K_out so that at Ψ=0.5: p_net = base*(0.5/0.5) = 1/K_out →
# σ = K_out * (1/K_out) = 1. EXACTLY marginal at the fixed point, by construction
# of the opponent balance — the empirical question is whether the dynamics then
# show the σ≈1 estimate + the τ≈1.5 power-law signature, and the control whether
# the σ estimate tracks Ψ off the fixed point.
# ─────────────────────────────────────────────────────────────────────────────

def build_graph(N, K_out, seed):
    """Fixed sparse directed coupling graph as a flat edge array (the A⇄G
    coupling topology): each unit i has K_out random out-neighbours stored in
    row i of an (N, K_out) int array. Seeded → deterministic. Returns the numpy
    adjacency for the vectorized propagation."""
    rng = np.random.default_rng(seed)
    adj = np.empty((N, K_out), dtype=np.int64)
    for i in range(N):
        # sample K_out distinct neighbours != i
        cand = rng.choice(N - 1, size=K_out, replace=False)
        cand[cand >= i] += 1          # skip self
        adj[i] = cand
    return adj


def psi_to_branching(psi, K_out):
    """Opponent-balance → per-edge net activation prob and the analytic σ.
    A push = psi, G push = (1−psi); net drive ∝ psi/(1−psi); base = 1/K_out
    makes σ(0.5)=1 exactly. Returns (p_edge, sigma_analytic)."""
    eps = 1e-9
    ratio = psi / max(1.0 - psi, eps)        # A/G opponent ratio
    base = 1.0 / K_out
    p_edge = base * ratio
    p_edge = min(max(p_edge, 0.0), 1.0)
    sigma = K_out * p_edge
    return p_edge, sigma


def run_avalanches(psi, N, K_out, adj, n_avalanches, seed,
                   cap_steps=2000, cap_size=None):
    """Drive the opponent propagation network (numpy-vectorized). Each avalanche
    = seed a single unit active, then propagate as a branching cascade until
    activity dies (canonical Beggs-Plenz separation-of-timescales: one avalanche
    per external drive, bracketed by empty bins).

    FINITE-SIZE CAP (frozen, load-bearing for tractability + correctness): a
    finite array of N units imposes a natural finite-size cutoff on avalanche
    size; super-critical cascades percolate and would never self-terminate. We
    make the finite-size cutoff EXPLICIT — an avalanche is truncated at
    cap_steps duration or cap_size summed activity (default cap_size = N*K_out =
    a few system-spanning sweeps). A truncated avalanche is flagged 'capped'.
    This is the standard finite-size SOC treatment: at criticality avalanches are
    cut by system size (the power-law shows a finite-size shoulder, NOT a pile-up
    at the cap); SUPER-critically the cap is hit constantly (a delta-like pile-up
    at the cutoff = the broken-power-law signature the control is meant to show).

    Returns: sizes, durations, anc_desc (n_t,n_{t+1} per within-aval step for the
    Beggs-Plenz σ), series (concatenated active counts w/ 0 separators for the
    Wilting-Priesemann regression), n_capped."""
    rng = np.random.default_rng(seed)
    p_edge, _ = psi_to_branching(psi, K_out)
    if cap_size is None:
        cap_size = N * K_out

    sizes, durations = [], []
    anc_desc = []
    series = []
    n_capped = 0

    seeds0 = rng.integers(0, N, size=n_avalanches)
    for a in range(n_avalanches):
        active = np.array([seeds0[a]], dtype=np.int64)
        # boolean occupancy to dedup activated units cheaply
        occ = np.zeros(N, dtype=bool)
        size = 0
        dur = 0
        series.append(1)                       # avalanche start bin (1 active)
        capped = False
        while active.size > 0 and dur < cap_steps and size < cap_size:
            n_t = active.size
            size += n_t
            dur += 1
            # propagate: each active unit fires each out-edge w.p. p_edge.
            # targets = adj[active] is (n_t, K_out); a Bernoulli(p_edge) mask
            # selects firing edges; the union of fired targets is next active set.
            targets = adj[active].reshape(-1)
            fire = rng.random(targets.size) < p_edge
            fired = targets[fire]
            if fired.size:
                occ[:] = False
                occ[fired] = True
                nxt = np.flatnonzero(occ)
            else:
                nxt = np.empty(0, dtype=np.int64)
            n_next = nxt.size
            anc_desc.append((n_t, n_next))
            series.append(n_next)
            active = nxt
        if dur >= cap_steps or size >= cap_size:
            capped = True
            n_capped += 1
        sizes.append(size)
        durations.append(dur)
        series.append(0)                       # empty separator bin
    return sizes, durations, anc_desc, series, n_capped


# ─────────────────────────────────────────────────────────────────────────────
# σ ESTIMATORS
# ─────────────────────────────────────────────────────────────────────────────
def sigma_beggs_plenz(anc_desc):
    """σ = ⟨ n_{t+1} / n_t ⟩ over ancestor bins with n_t > 0 (Beggs & Plenz 2003).
    The mean descendant-to-ancestor active-unit ratio per step."""
    ratios = [nd[1] / nd[0] for nd in anc_desc if nd[0] > 0]
    if not ratios:
        return float("nan")
    return sum(ratios) / len(ratios)


def sigma_wilting_priesemann(series, kmax=20):
    """Multistep regression estimator (Wilting & Priesemann 2018).
    For a branching process with rate m, the autocorrelation of the activity
    a_t decays as r_k ∝ m^k. Estimate m̂ from the slope of ln(r_k) vs k.
    r_k = Cov(a_{t+k}, a_t)/Var(a_t). Robust to subsampling (unlike naive σ)."""
    a = np.asarray(series, dtype=np.float64)
    # tractability: the concatenated series can be millions of bins; the
    # autocorrelation estimate is stable on a long prefix. Cap at 2e6 bins.
    if a.size > 2_000_000:
        a = a[:2_000_000]
    n = a.size
    if n < kmax + 5:
        return float("nan")
    mean = a.mean()
    var = a.var()
    if var <= 0:
        return float("nan")
    d = a - mean
    ks, logr = [], []
    for k in range(1, kmax + 1):
        cov = float(np.dot(d[:n - k], d[k:]) / (n - k))
        r = cov / var
        if r > 1e-9:                # only positive autocorrelation is informative
            ks.append(k)
            logr.append(math.log(r))
    if len(ks) < 3:
        return float("nan")
    # slope of ln(r_k) vs k = ln(m)  →  m = exp(slope)
    kbar = sum(ks) / len(ks)
    lbar = sum(logr) / len(logr)
    num = sum((ks[i] - kbar) * (logr[i] - lbar) for i in range(len(ks)))
    den = sum((ks[i] - kbar) ** 2 for i in range(len(ks)))
    if den == 0:
        return float("nan")
    slope = num / den
    return math.exp(slope)


# ─────────────────────────────────────────────────────────────────────────────
# POWER-LAW FIT (F2)  — log-binned log-log fit + LLR vs exponential
# ─────────────────────────────────────────────────────────────────────────────
def size_pdf_logbinned(sizes, n_bins=24):
    """Logarithmically-binned empirical PDF of avalanche sizes (smin..smax)."""
    pos = [s for s in sizes if s >= 1]
    if not pos:
        return [], []
    smin, smax = 1, max(pos)
    if smax <= smin:
        return [], []
    edges = [smin * (smax / smin) ** (i / n_bins) for i in range(n_bins + 1)]
    centers, dens = [], []
    for b in range(n_bins):
        lo, hi = edges[b], edges[b + 1]
        cnt = sum(1 for s in pos if lo <= s < hi)
        width = hi - lo
        if cnt > 0 and width > 0:
            centers.append(math.sqrt(lo * hi))     # geometric center
            dens.append(cnt / (width * len(pos)))
    return centers, dens


def fit_powerlaw_loglog(centers, dens):
    """Linear fit in log-log: ln(p) = -τ ln(s) + c. Returns (tau, R², decades)."""
    pts = [(math.log(c), math.log(d)) for c, d in zip(centers, dens) if d > 0]
    if len(pts) < 4:
        return float("nan"), float("nan"), 0.0
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    sxx = sum((x - xbar) ** 2 for x in xs)
    sxy = sum((xs[i] - xbar) * (ys[i] - ybar) for i in range(len(xs)))
    if sxx == 0:
        return float("nan"), float("nan"), 0.0
    slope = sxy / sxx
    intercept = ybar - slope * xbar
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    ss_res = sum((ys[i] - (slope * xs[i] + intercept)) ** 2 for i in range(len(xs)))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    decades = (max(xs) - min(xs)) / math.log(10)
    return -slope, r2, decades


def loglik_ratio_pl_vs_exp(sizes):
    """Per-point log-likelihood ratio: power-law vs exponential, fit by MLE on
    the raw (un-binned) size sample (Clauset-Shalizi-Newman spirit). LLR>0 ⇒
    power-law better. Discrete sizes s≥1.

    Power-law MLE: τ̂ = 1 + n / Σ ln(s_i / (smin-0.5)).  Exponential MLE on s≥1:
    λ̂ = 1 / (mean(s) - smin + 1).  Compare total log-likelihoods; report the
    normalized (per-point) LLR (Vuong-style sign)."""
    s = [x for x in sizes if x >= 1]
    n = len(s)
    if n < 10:
        return float("nan"), float("nan"), float("nan")
    smin = 1
    # power-law (discrete, continuous-approx MLE)
    denom = sum(math.log(x / (smin - 0.5)) for x in s)
    if denom <= 0:
        return float("nan"), float("nan"), float("nan")
    tau_mle = 1.0 + n / denom
    # normalizing constant (continuous approx): C = (tau-1)*smin_eff^(tau-1)
    smin_eff = smin - 0.5
    ll_pl = sum(math.log((tau_mle - 1) / smin_eff) - tau_mle * math.log(x / smin_eff)
                for x in s)
    # exponential on s>=smin
    mean_s = sum(s) / n
    lam = 1.0 / max(mean_s - smin + 1.0, 1e-9)
    ll_exp = sum(math.log(lam) - lam * (x - smin) for x in s)
    llr = (ll_pl - ll_exp) / n        # per-point
    return llr, tau_mle, ll_pl - ll_exp


# ─────────────────────────────────────────────────────────────────────────────
def analyze(psi, N, K_out, adj, n_avalanches, seed):
    sizes, durations, anc_desc, series, n_capped = run_avalanches(
        psi, N, K_out, adj, n_avalanches, seed)
    sig_bp = sigma_beggs_plenz(anc_desc)
    sig_wp = sigma_wilting_priesemann(series)
    centers, dens = size_pdf_logbinned(sizes)
    tau, r2, decades = fit_powerlaw_loglog(centers, dens)
    llr, tau_mle, llr_total = loglik_ratio_pl_vs_exp(sizes)
    _, sigma_analytic = psi_to_branching(psi, K_out)
    return {
        "psi": psi, "sigma_analytic": sigma_analytic,
        "sigma_bp": sig_bp, "sigma_wp": sig_wp,
        "tau": tau, "r2": r2, "decades": decades,
        "tau_mle": tau_mle, "llr": llr, "llr_total": llr_total,
        "n_aval": len(sizes), "max_size": max(sizes) if sizes else 0,
        "mean_size": sum(sizes) / len(sizes) if sizes else 0.0,
        "n_capped": n_capped, "capped_frac": n_capped / max(len(sizes), 1),
    }


def main():
    ALPHA, BALANCE = load_constants()
    out = []
    def p(s=""):
        out.append(s); print(s)

    # ── frozen design parameters (pre-registered) ──
    N = 4000             # units in the opponent network
    K_OUT = 8            # mean out-degree (A⇄G coupling fan-out)
    N_AVAL = 60000       # avalanches sampled (separation-of-timescales)
    GRAPH_SEED = 1153
    RUN_SEED = 7         # deterministic propagation seed

    # FROZEN falsifier bands (from .tape, set BEFORE this run)
    SIGMA_LO, SIGMA_HI = 0.9, 1.1
    TAU_LO, TAU_HI = 1.3, 1.7
    R2_MIN = 0.9
    DEC_MIN = 1.5

    p("=" * 74)
    p("H_1153 — CRITICALITY / branching ratio σ≈1 (neuronal avalanches) @ Ψ=1/2")
    p("=" * 74)
    p("")
    p("CONSTANTS (verbatim config/consciousness_laws.json psi_constants):")
    p(f"  PSI_ALPHA   = alpha   = {ALPHA}")
    p(f"  PSI_BALANCE = balance = {BALANCE}   (formula '1/2', 'universal attractor')")
    p("")
    p(f"OPPONENT NETWORK: N={N} units, K_out={K_OUT} (A⇄G coupling fan-out),")
    p(f"  graph_seed={GRAPH_SEED}, run_seed={RUN_SEED}, n_avalanches={N_AVAL}")
    p("  Per-edge net activation = opponent balance: A push Ψ ⇄ G push (1−Ψ);")
    p("  base=1/K_out ⇒ σ(Ψ=0.5)=1 by construction of the opponent balance.")
    p(f"  FINITE-SIZE CAP (frozen): avalanche truncated at {2000} steps or N*K_out={N*K_OUT}")
    p("    summed activity (explicit finite-size cutoff; super-critical pile-up at")
    p("    the cap = the broken-power-law signature the control must show).")
    p("  F1/F2 TEST whether the dynamics then show σ≈1 + τ≈1.5 power-law; CONTROL")
    p("  tests whether de-tuning Ψ off 1/2 moves σ + breaks the power-law.")
    p("")
    p("FROZEN FALSIFIER (pre-registered in .discoveries/1153_criticality_branching.tape):")
    p(f"  F1: σ ∈ [{SIGMA_LO},{SIGMA_HI}] at Ψ=0.5")
    p(f"  F2: power-law τ ∈ [{TAU_LO},{TAU_HI}], R² ≥ {R2_MIN} over ≥ {DEC_MIN} decades,")
    p(f"      AND LLR > 0 (power-law beats exponential)")
    p(f"  CONTROL: de-tuned Ψ must move σ out of [{SIGMA_LO},{SIGMA_HI}] and/or break power-law")
    p("  🟢 SUPPORTED iff F1 ∧ F2 ∧ control-moves-σ ; else 🔴 CLOSED-NEGATIVE")
    p("")

    graph = build_graph(N, K_OUT, GRAPH_SEED)

    # ── FIXED POINT: Ψ = 0.5 ──
    p("-" * 74)
    p("FIXED POINT  Ψ = 0.5  (the operating point)")
    p("-" * 74)
    fp = analyze(BALANCE, N, K_OUT, graph, N_AVAL, RUN_SEED)
    p(f"  σ_analytic (opponent balance)     = {fp['sigma_analytic']:.4f}")
    p(f"  σ̂ Beggs-Plenz (desc/anc ratio)   = {fp['sigma_bp']:.4f}")
    p(f"  σ̂ Wilting-Priesemann (regression)= {fp['sigma_wp']:.4f}")
    p(f"  τ (log-log size fit)              = {fp['tau']:.4f}")
    p(f"  R² of log-log fit                 = {fp['r2']:.4f}")
    p(f"  decades spanned                   = {fp['decades']:.4f}")
    p(f"  τ_MLE (Clauset)                   = {fp['tau_mle']:.4f}")
    p(f"  LLR power-law vs exp (per-point)  = {fp['llr']:+.5f}  (total {fp['llr_total']:+.2f})")
    p(f"  n_avalanches={fp['n_aval']}  max_size={fp['max_size']}  mean_size={fp['mean_size']:.2f}")
    p(f"  capped_frac (finite-size cutoff hit)= {fp['capped_frac']:.4f}  (n_capped={fp['n_capped']})")
    p("")

    # ── CONTROL: de-tuned Ψ (sub-critical and super-critical) ──
    p("-" * 74)
    p("CONTROL  de-tuned Ψ (criticality must be SPECIFIC to Ψ=0.5)")
    p("-" * 74)
    controls = {}
    for label, psi_c in [("sub-critical Ψ=0.40", 0.40),
                         ("sub-critical Ψ=0.30", 0.30),
                         ("super-critical Ψ=0.60", 0.60),
                         ("super-critical Ψ=0.70", 0.70)]:
        c = analyze(psi_c, N, K_OUT, graph, N_AVAL, RUN_SEED)
        controls[label] = c
        p(f"  {label}:")
        p(f"      σ_analytic={c['sigma_analytic']:.4f}  σ̂_BP={c['sigma_bp']:.4f}  "
          f"σ̂_WP={c['sigma_wp']:.4f}")
        p(f"      τ={c['tau']:.4f}  R²={c['r2']:.4f}  decades={c['decades']:.4f}  "
          f"LLR={c['llr']:+.5f}  max_size={c['max_size']}  capped_frac={c['capped_frac']:.4f}")
    p("")

    # ── VERDICT ──
    p("=" * 74)
    p("VERDICT (frozen falsifier)")
    p("=" * 74)
    f1 = SIGMA_LO <= fp["sigma_bp"] <= SIGMA_HI
    f1_wp = SIGMA_LO <= fp["sigma_wp"] <= SIGMA_HI
    f2_tau = TAU_LO <= fp["tau"] <= TAU_HI
    f2_r2 = fp["r2"] >= R2_MIN
    f2_dec = fp["decades"] >= DEC_MIN
    f2_llr = fp["llr"] > 0
    f2 = f2_tau and f2_r2 and f2_dec and f2_llr

    # control moves σ: every de-tuned Ψ must push σ̂_BP out of the band on the
    # correct side (sub→<0.9, super→>1.1)
    sub_ok = all(controls[l]["sigma_bp"] < SIGMA_LO for l in controls if "sub" in l)
    sup_ok = all(controls[l]["sigma_bp"] > SIGMA_HI for l in controls if "super" in l)
    control_moves = sub_ok and sup_ok

    p(f"  F1  σ̂_BP={fp['sigma_bp']:.4f} ∈ [{SIGMA_LO},{SIGMA_HI}] ............ "
      f"{'PASS' if f1 else 'FAIL'}")
    p(f"      (corroborating σ̂_WP={fp['sigma_wp']:.4f} in band: {'yes' if f1_wp else 'no'})")
    p(f"  F2  τ={fp['tau']:.4f} ∈ [{TAU_LO},{TAU_HI}] ......................... "
      f"{'PASS' if f2_tau else 'FAIL'}")
    p(f"      R²={fp['r2']:.4f} ≥ {R2_MIN} .............................. "
      f"{'PASS' if f2_r2 else 'FAIL'}")
    p(f"      decades={fp['decades']:.4f} ≥ {DEC_MIN} ..................... "
      f"{'PASS' if f2_dec else 'FAIL'}")
    p(f"      LLR={fp['llr']:+.5f} > 0 (PL beats exp) .............. "
      f"{'PASS' if f2_llr else 'FAIL'}")
    p(f"  CONTROL  sub-critical σ<{SIGMA_LO}: {'PASS' if sub_ok else 'FAIL'}  "
      f"super-critical σ>{SIGMA_HI}: {'PASS' if sup_ok else 'FAIL'} ..... "
      f"{'PASS' if control_moves else 'FAIL'}")
    p("")
    supported = f1 and f2 and control_moves
    if supported:
        p("  🟢 SUPPORTED — A⇄G engine SITS AT CRITICALITY at the Ψ=1/2 fixed point:")
        p("     σ≈1 + power-law avalanches (τ≈1.5), and criticality is SPECIFIC to")
        p("     Ψ=1/2 (de-tuning moves σ off 1 / breaks the power-law).")
    else:
        p("  🔴 CLOSED-NEGATIVE — F1 ∧ F2 ∧ control NOT all satisfied at Ψ=1/2.")
        p("     The engine is NOT cleanly critical at the fixed point under the")
        p("     frozen avalanche definition (sub/super-critical, or power-law fails).")
    p("")
    p(f"  per-gate: F1={f1}  F2={f2} (τ={f2_tau} R²={f2_r2} dec={f2_dec} LLR={f2_llr})  "
      f"CONTROL={control_moves}")
    p(f"  VERDICT = {'🟢 SUPPORTED' if supported else '🔴 CLOSED-NEGATIVE'}")

    # write verdict file
    vdir = os.path.join(REPO, ".verdicts", "1153_criticality_branching")
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "H_1153.txt"), "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
