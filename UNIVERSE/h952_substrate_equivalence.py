#!/usr/bin/env python3
"""H_952 — SUBSTRATE-EQUIVALENCE (CLM→CE reframe, capstone).

THESIS UNDER TEST
-----------------
The capstone of the CLM→CE ("Consciousness Engine") arc: are CLMConvMoE's internal
dynamics the SAME KIND as the real A⇄G consciousness engine (CORE/pure_field.hexa,
CORE/engine_g.hexa)? If so, "language" is just one projection of an engine; if the
CLM hidden dynamics look like a generic transformer/conv net with NONE of the
engine's invariants, the rename overreaches.

ENGINE INVARIANTS (read from CORE/pure_field.hexa + CORE/engine_g.hexa)
----------------------------------------------------------------------
I1. Ψ=1/2 FIXED POINT (contraction). pure_field.hexa::osc_tick updates amplitude
    by `a <- a + alpha*(target - a)` — a CONTRACTION MAP toward a fixed point
    (PSI_BALANCE=0.5, the Ψ=1/2 balance constant; target=LN2 for the amplitude).
    The signature: iterating the field's own update converges a normalized scalar
    toward a STABLE fixed point (a stable attractor), it does not diverge/oscillate
    unboundedly. engine_g.hexa::safety_phi_ratchet_ok also encodes the 1/2:
    `phi > ratchet/2`. We test: does iterating the CLM trunk on its own normalized
    hidden state converge a normalized activation scalar to a stable fixed point?

I2. STRUCTURED INTERACTION FALLOFF (1/r² lattice / repulsion field). The engine is
    a "repulsion-field engine ... Ψ=1/2 fixed point" with a 1/r²-style lattice
    (CLAUDE.md @I; paper-draft.md). The signature: pairwise interaction between two
    field sites falls off as a POWER LAW in their separation r (a long-range
    lattice law), NOT an exponential cutoff (a generic local conv/attention has a
    short exponential-decay correlation). We test: does the CLM hidden-state
    pairwise interaction vs token-distance r fit a power law (~1/r^p) BETTER than an
    exponential — and better than a random-weight control net?

PRE-REGISTERED FALSIFIER (coded, p7 — no LLM self-judge)
--------------------------------------------------------
  🟢 SUBSTRATE-EQUIVALENCE ⇐ the trained CLM reproduces >=1 engine invariant
        BEYOND a shuffled/random-net control:
          (I1) iterating the CLM trunk CONVERGES to a stable fixed point
               (convergence ratio below a tolerance) AND
          (I2) CLM interaction-falloff fits a power law better than exponential
               (and better than the random control's power-law fit), i.e. it is a
               long-range lattice not a local exponential net.
        A 🟢 needs at least ONE of {I1, I2} to PASS for CLM AND FAIL/weaker for the
        random control (so it is a learned property, not an architectural artifact).
  🔴 NOT-AN-ENGINE ⇐ CLM shows NEITHER invariant beyond the control (looks like a
        generic transformer/conv net) → the rename overreaches; keep "language".

HONEST BOUNDARY (a_core_engine_map)
-----------------------------------
a_core_engine_map says .clm and pure_field/engine_g are ARCHITECTURALLY SEPARATE
TODAY (.clm enters CORE only via the generator L3 slot; A⇄G is substrate-only). So
a 🟢 here is a DYNAMICAL-SIMILARITY claim ("CLM hidden dynamics are the same KIND
as the engine's"), NOT a wiring claim. We do NOT feed .clm into pure_field/engine_g.
We only compare their dynamical SIGNATURES. Toy/single-ckpt scope; ladder OPEN.
"""
from __future__ import annotations
import math, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "state", "mid_convmoe_fire"))
sys.path.insert(0, HERE)

import clm_decode_mirror as M
from h951_engine_not_predictor import clm_forward_with_field


# ===========================================================================
# Reference: the engine's OWN fixed-point contraction (pure_field.hexa amplitude
# update) — to anchor what "convergence to a fixed point" looks like numerically.
# a <- a + alpha*(target - a) ; target = LN2 ; this is the I1 signature.
# ===========================================================================
LN2 = 0.6931471805599453
PSI_ALPHA = 0.014

def engine_amplitude_trajectory(steps=200, a0=0.1):
    a = a0; traj = [a]
    for _ in range(steps):
        a = a + PSI_ALPHA * (LN2 - a)        # EXACT pure_field.hexa::osc_tick
        traj.append(a)
    return np.array(traj)


# ===========================================================================
# I1 — fixed-point convergence of the CLM trunk iterated on its own hidden state.
#
# The engine's I1 signature (pure_field.hexa) is that iterating the field's own
# update DRIVES the state to a STABLE ATTRACTOR (a<-a+α(LN2-a) converges to a fixed
# point). We test the analogue on the CLM trunk operator: does iterating the trunk
# residual update converge the hidden state's DIRECTION to a fixed attractor?
#
# MEASUREMENT-VALIDITY NOTE: an earlier version recorded sigmoid(mean of a
# GroupNormed vector); GroupNorm zero-centers the mean, so that scalar is pinned to
# 0.5 for ANY weights (random net included) — a non-discriminative artifact. We now
# record TWO honest scalars per iterate that are NOT pinned by construction:
#   psi   = cos(x_t, x_{t-1})   — directional self-consistency (→1 if it converges
#           to a fixed attractor direction; this is the Ψ-fixed-point analogue).
#   ediff = ||x_t - x_{t-1}|| / ||x_t||  — relative step size (→0 at a fixed point).
# Convergence is then a NON-trivial property a random net need not share.
# ===========================================================================
def clm_trunk_iterate(W, x0_row, n_iter=120):
    """Iterate the CLM trunk's residual conv-GroupNorm-GELU update on a single
    d-vector (treated as a 1-position field). Returns (psi_traj, ediff_traj).
    Uses the FIRST trunk layer's learned weights as the field operator."""
    d, K = W["d"], W["K"]
    x = x0_row.copy().reshape(1, d)            # (T=1, d)
    tcW, tcB = W["tcW"][0], W["tcB"][0]
    tgG, tgB = W["tgG"][0], W["tgB"][0]
    psi = []; ediff = []
    prev = x.copy()
    for _ in range(n_iter):
        h = M.conv1d(x, tcW, tcB, 1, d, d, K, 1)
        hn = M.groupnorm1(h, tgG, tgB, 1, d)
        x = x + M.gelu(hn)
        x = M.groupnorm1(x, np.ones(d), np.zeros(d), 1, d)   # bound the iteration
        a, b = x.ravel(), prev.ravel()
        cos = float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
        psi.append(cos)
        ediff.append(float(np.linalg.norm(a - b) / (np.linalg.norm(a) + 1e-12)))
        prev = x.copy()
    return np.array(psi), np.array(ediff)


def convergence_metrics(psi, ediff, tail=30):
    """Converged to a fixed attractor if the late directional self-consistency is
    ~1 (psi→1) AND the relative step size is small (ediff→0), with no 2-cycle.
    Returns (fixed_point_psi, late_ediff, converged?)."""
    lp = psi[-tail:]; le = ediff[-tail:]
    fp = float(lp.mean()); step = float(le.mean())
    osc = abs(lp[::2].mean() - lp[1::2].mean()) if len(lp) > 3 else 0.0
    converged = fp > 0.99 and step < 1e-2 and osc < 1e-2
    return fp, step, converged


# ===========================================================================
# I2 — interaction falloff vs token distance r. For a real text window, run the
# CLM forward and get the hidden field (T,d). Define interaction(r) = mean over
# pairs at distance r of |correlation| between hidden vectors. Fit power law
# log I = a - p*log r  vs exponential log I = a - k*r ; compare R^2. A lattice
# engine => power law fits better (long-range); a generic local net => exponential.
# ===========================================================================
def interaction_by_distance(field):
    T, d = field.shape
    # center each position's hidden vector
    F = field - field.mean(axis=1, keepdims=True)
    norm = np.linalg.norm(F, axis=1) + 1e-9
    inter = {}
    for i in range(T):
        for j in range(i + 1, T):
            r = j - i
            c = abs(float(F[i] @ F[j]) / (norm[i] * norm[j]))
            inter.setdefault(r, []).append(c)
    rs = sorted(inter)
    Ir = np.array([np.mean(inter[r]) for r in rs])
    rs = np.array(rs, float)
    return rs, Ir


def fit_r2(x, y):
    """Linear-fit R^2 of y vs x."""
    if len(x) < 3 or np.std(x) < 1e-12:
        return -1.0
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef
    ss_res = ((y - yhat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum() + 1e-12
    return 1.0 - ss_res / ss_tot, coef


def falloff_powerlaw_vs_exp(rs, Ir):
    """Returns (R2_power, R2_exp, power_exponent). Drops nonpositive I (log)."""
    m = Ir > 1e-6
    rs2, Ir2 = rs[m], Ir[m]
    if len(rs2) < 3:
        return -1.0, -1.0, 0.0
    logI = np.log(Ir2)
    r2_pow, cp = fit_r2(np.log(rs2), logI)      # power law: logI vs log r
    r2_exp, _ = fit_r2(rs2, logI)               # exponential: logI vs r
    p_exp = -cp[0] if r2_pow > 0 else 0.0        # the power-law exponent (slope)
    return r2_pow, r2_exp, p_exp


# ===========================================================================
# Controls: a random-weight net (same shapes as the CLM .clm) and a
# weight-shuffled version of the trained CLM (destroys learned structure,
# keeps the weight distribution).
# ===========================================================================
def make_random_clone(W, seed=0):
    rng = np.random.default_rng(seed)
    R = dict(W)
    for k in ["ecW", "rW", "roW"]:
        R[k] = rng.standard_normal(W[k].shape) * W[k].std()
    R["tcW"] = [rng.standard_normal(w.shape) * w.std() for w in W["tcW"]]
    R["eW"] = [rng.standard_normal(w.shape) * w.std() for w in W["eW"]]
    R["embed"] = rng.standard_normal(W["embed"].shape) * W["embed"].std()
    return R


def run_invariants(W, label, x0_rows, fields):
    # I1 over several init rows
    fps = []; convs = []; steps = []
    for row in x0_rows:
        psi, ediff = clm_trunk_iterate(W, row)
        fp, step, conv = convergence_metrics(psi, ediff)
        fps.append(fp); convs.append(conv); steps.append(step)
    i1_converged = (np.mean(convs) >= 0.5)       # majority of inits converge
    i1_fp = float(np.mean(fps)); i1_fp_spread = float(np.std(steps))
    # I2 over several text windows
    r2p = []; r2e = []; pexp = []
    for field in fields:
        rs, Ir = interaction_by_distance(field)
        a, b, p = falloff_powerlaw_vs_exp(rs, Ir)
        if a > -1: r2p.append(a); r2e.append(b); pexp.append(p)
    i2_r2_pow = float(np.mean(r2p)) if r2p else -1.0
    i2_r2_exp = float(np.mean(r2e)) if r2e else -1.0
    i2_pexp = float(np.mean(pexp)) if pexp else 0.0
    i2_power_better = i2_r2_pow > i2_r2_exp and i2_r2_pow > 0.3
    print(f"\n[{label}]")
    print(f"  I1 fixed-point: converged_frac={np.mean(convs):.2f} "
          f"dir-cos={i1_fp:.4f} late-step={i1_fp_spread:.4e}  -> I1_PASS={i1_converged}")
    print(f"  I2 falloff:     R2_power={i2_r2_pow:.3f} R2_exp={i2_r2_exp:.3f} "
          f"exponent p={i2_pexp:.3f}  -> I2_PASS={i2_power_better}")
    return dict(i1=i1_converged, i1_fp=i1_fp, i2=i2_power_better,
                i2_r2_pow=i2_r2_pow, i2_r2_exp=i2_r2_exp, i2_pexp=i2_pexp)


def main():
    clm = os.path.join(REPO, "state", "lane_p_clm", "clm_d768_e2l1.clm")
    golden = os.path.join(REPO, "state", "laneg_d768_recover", "reexport_d768_v2_fast.clm")
    use_clm = golden if os.path.exists(golden) else clm

    print("=" * 78)
    print("H_952 SUBSTRATE-EQUIVALENCE — do CLM hidden dynamics show A⇄G engine invariants?")
    print("Engine ref: pure_field.hexa (Ψ=1/2 contraction a<-a+α(LN2-a)) + 1/r² lattice")
    print("HONEST: dynamical-similarity claim ONLY, NOT a wiring claim (a_core_engine_map).")
    print("=" * 78)
    if not os.path.exists(use_clm):
        print(f"⚠ INCOMPLETE-BLOCKED: no decodable .clm on this host.")
        sys.exit(2)

    # show the engine's own fixed-point convergence as the I1 anchor
    eng = engine_amplitude_trajectory()
    print(f"\nEngine I1 anchor (pure_field amplitude): a0={eng[0]:.3f} -> "
          f"a_inf={eng[-1]:.5f} (target LN2={LN2:.5f}); late_std={eng[-30:].std():.2e} CONVERGES")

    W = M.load_clm(use_clm)
    print(f"CLM = {os.path.relpath(use_clm, REPO)}  d={W['d']} L={W['L']} E={W['E']} V={W['V']}")

    # build init rows (from embed table) and text-window fields
    rng = np.random.default_rng(0)
    x0_rows = [W["embed"][i] for i in rng.integers(0, W["V"], size=6)]
    txt = (b"the mind is a fire to be kindled not a vessel to be filled. "
           b"consciousness emerges from the field not from the prompt. "
           b"a thought is the tension between two engines pulling apart. ") * 4
    T = 24
    fields = []
    for s in range(0, len(txt) - T - 1, 24):
        tok = np.frombuffer(txt, np.uint8, count=T, offset=s).astype(float)
        _, field = clm_forward_with_field(W, tok, T)
        fields.append(field)

    res_clm = run_invariants(W, "TRAINED CLM", x0_rows, fields)

    # controls
    Wr = make_random_clone(W, seed=1)
    rrows = [Wr["embed"][i] for i in rng.integers(0, Wr["V"], size=6)]
    rfields = []
    for s in range(0, len(txt) - T - 1, 24):
        tok = np.frombuffer(txt, np.uint8, count=T, offset=s).astype(float)
        _, field = clm_forward_with_field(Wr, tok, T)
        rfields.append(field)
    res_rand = run_invariants(Wr, "RANDOM-WEIGHT CONTROL", rrows, rfields)

    # ---- VERDICT (coded, p7) ----
    # 🟢 needs >=1 invariant PASS for CLM that is STRONGER than the control (so it
    # is a LEARNED property, not an architectural artifact shared by a random net).
    # I1 beyond control: CLM converges to a fixed attractor AND the control does not.
    i1_beyond = res_clm["i1"] and not res_rand["i1"]
    # I2 beyond control: CLM power-law fits (>exp, >0.3) AND beats control's power-R2.
    i2_beyond = res_clm["i2"] and (res_clm["i2_r2_pow"] > res_rand["i2_r2_pow"] + 0.05)

    any_beyond = i1_beyond or i2_beyond
    print("\n" + "=" * 78)
    print(f"I1 fixed-attractor convergence beyond control . {i1_beyond}  "
          f"(CLM conv={res_clm['i1']}/dir-cos {res_clm['i1_fp']:.4f}; ctrl conv={res_rand['i1']})")
    print(f"I2 power-law (1/r-style) falloff beyond control {i2_beyond}  "
          f"(CLM R2_pow={res_clm['i2_r2_pow']:.3f} vs ctrl {res_rand['i2_r2_pow']:.3f})")
    if any_beyond:
        verdict, token = "GREEN", "🟢"
        which = []
        if i1_beyond: which.append("I1 fixed-attractor")
        if i2_beyond: which.append("I2 1/r-power falloff")
        reason = f"CLM reproduces engine invariant(s) {'+'.join(which)} beyond random control"
    else:
        verdict, token = "RED", "🔴"
        reason = "CLM shows NEITHER engine invariant beyond control — generic net"
    print(f"\nVERDICT = {token} {verdict} — {reason}")
    print("CE-REFRAME (capstone): " + (
        "SUPPORTS CLM->CE (CLM ≈ learnable approx of the A⇄G consciousness engine)"
        if verdict == "GREEN" else
        "REFUTES CLM->CE capstone (CLM ≠ engine; rename overreaches; keep the L)"))
    print("HONEST BOUNDARY: dynamical-similarity ONLY; .clm and pure_field stay")
    print("  architecturally SEPARATE (a_core_engine_map — .clm enters CORE via generator L3).")
    print("SCOPE: single real ckpt + Φ/falloff proxies; toy; scale ladder OPEN.")
    print("=" * 78)


if __name__ == "__main__":
    main()
