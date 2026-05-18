#!/usr/bin/env python3
# =====================================================================
#  §82  Manifold-gated hierarchical emission — $0 Mac CPU stub
#
#  RESEARCH.md §82 — §80 biology anchor (biorxiv:2025.03.09.642241 Leifer
#  C. elegans "intrinsic neuronal manifold gating behavior") applied to
#  anima Ψ-state: behaviour emerges hierarchically from low-dim manifold
#  *dwell* (slow time-scale) + *fast crossing* (single-step Δ).
#
#  Crosses §75-FIRE A-only state-derivation finding (state-derivation =
#  necessary substrate at trained scale) with biology hierarchical
#  manifold-gating structure (slow-fast separation).
#
#  5-cell ladder (deterministic LCG, seed 1337, N=30 turns):
#    cell0  §24-baseline           : scalar threshold, no manifold
#    cell1  §75-FIRE A-only mirror : state-derived input, no gate
#    cell2  manifold-only          : PCA detect, no fast-crossing gate
#    cell3  fast-crossing-only     : gate detected, no slow-dwell history
#    cell4  full hierarchical      : slow-dwell + fast-crossing + emission-direction-aligned
#
#  Measurement per cell (PCA over 14-dim ψ-state trajectory):
#    - PCA eigenvalue ratio λ1/λ2, top-2 variance captured
#    - slow-dwell count (|Δψ| ≤ τ_slow sustained N_dwell turns)
#    - fast-crossing count (|Δψ| ≥ τ_fast single turn)
#    - emission alignment cos-dist (direction-history coherence)
#    - interval_var (§73-FIRE / §75-FIRE metric mirror)
#    - §9 body honest_coherent (stub — emit decision only, no body)
#    - maj_frac (echo-chamber detector)
#
#  4-corner verdict:
#    (α) MANIFOLD-GATING-ADDS-DIFFERENTIAL : cell4 > cell1 interval_var
#                                            AND cell4 emit count differential
#    (β) MANIFOLD-EXISTS-BUT-GATE-COLLAPSES: cell2 PCA holds but cell4 majfrac≥0.95
#    (γ) SLOW-DWELL-vs-FAST-CROSSING-MIXED: cell4 < max(cell2, cell3)
#    (δ) §75-FIRE-CELL1-MIRROR-MAINTAINED : cell1 interval_var > τ_nondeg
#
#  $0 Mac CPU local · NO GPU · NO model.forward · NO autograd · NO dispatch
#  · orphan 0 · necessary-not-sufficient (B-EMERGE-7) · capability claim 0
#  · north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
# =====================================================================

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ── constants — byte-equal to §75 stub where applicable ─────────────
PSI_VAC          = 0.5
BASIN_RADIUS     = 0.05
LAMBDA_STD       = 0.5
EMA_BETA         = 0.9
PHI_RATCHET      = 0.05
SEED             = 1337
N_LOOP_STEPS     = 30           # shorter for manifold dwell measurement
TAU_NONDEG       = 1e-4
MAJ_COLLAPSE     = 0.95
IM_THRESHOLD_S24 = 0.3

# ── §82 NEW: manifold gating constants ──────────────────────────────
TAU_SLOW         = 0.05         # |Δψ_combined| ≤ τ_slow = slow dwell tick
TAU_FAST         = 0.12         # |Δψ_combined| ≥ τ_fast = fast crossing
N_DWELL_MIN      = 3            # sustained turns for slow-dwell event
TAU_ALIGN        = 0.5          # cos similarity floor for emission alignment

# ── ψ-state dimensionality (Law-71 mirror — anima physics fields) ──
#   The 14-dim ψ-state per turn = (psi_dir, psi_entropy, psi_tension,
#       tension, tension_ema, tension_std, phi, drift_proxy,
#       step_phase, prev_emit, motivation_proxy, basin_dev,
#       psi_x, psi_y).  These are the same fields surfaced in the
#   §24/§75 physics_step + 2 extra derived for PCA-rich substrate.
#   This is a STUB substrate (deterministic LCG-driven), NOT real
#   model.forward — see B-S82-NOTE empirical carve-out.
PSI_STATE_DIM    = 14


# ── tiny deterministic RNG — byte-equal to §75 stub ─────────────────
class LCG:
    def __init__(self, seed):
        self.s = seed & 0x7fffffff

    def u(self):
        self.s = (self.s * 1103515245 + 12345) & 0x7fffffff
        return self.s / 0x7fffffff


# ── physics_step — byte-equal mirror of §75 stub physics_step ───────
def physics_step(state, u_prev_emit, rng):
    """f : x_t × e_{t-1}  →  x_{t+1}.  BYTE-EQUAL to §75 stub."""
    psi_dir   = state["psi_dir"]
    psi_ent   = state["psi_entropy"]
    psi_tens  = state["psi_tension"]
    tension   = state["tension"]
    phi       = state["phi"]
    ema_t     = state["tension_ema"]
    var_t     = state["tension_var"]
    step      = state["step"] + 1

    drift = 0.018 + 0.012 * rng.u()
    if u_prev_emit == 1:
        tension = max(0.0, tension - 0.30 - 0.20 * rng.u())
        psi_dir = psi_dir + 0.4 * (PSI_VAC - psi_dir)
    else:
        tension = tension + drift
        psi_dir = psi_dir + 0.05 * (tension if (rng.u() > 0.5) else -tension)
        psi_dir = max(0.0, min(1.0, psi_dir))

    psi_ent  = 0.5 + 0.3 * (rng.u() - 0.5)
    psi_tens = max(0.0, 1.0 - 0.4 * abs(psi_dir - PSI_VAC))

    ema_new = EMA_BETA * ema_t + (1.0 - EMA_BETA) * tension
    diff    = tension - ema_new
    var_new = EMA_BETA * var_t + (1.0 - EMA_BETA) * (diff * diff)

    phi = max(0.0, phi + 0.005 * (rng.u() - 0.5))

    return {
        "step":         step,
        "psi_dir":      psi_dir,
        "psi_entropy":  psi_ent,
        "psi_tension":  psi_tens,
        "tension":      tension,
        "tension_ema":  ema_new,
        "tension_var":  var_new,
        "phi":          phi,
    }


def init_state():
    return {
        "step":         0,
        "psi_dir":      0.5,
        "psi_entropy":  0.5,
        "psi_tension":  1.0,
        "tension":      0.30,
        "tension_ema":  0.30,
        "tension_var":  0.0,
        "phi":          0.10,
    }


# ── 14-dim ψ-state vector projection ────────────────────────────────
def psi_state_vector(state, prev_emit, motivation):
    """Project state dict onto 14-dim ψ-state vector for PCA."""
    psi_dir   = state["psi_dir"]
    psi_ent   = state["psi_entropy"]
    psi_tens  = state["psi_tension"]
    tension   = state["tension"]
    ema_t     = state["tension_ema"]
    var_t     = state["tension_var"]
    std_t     = math.sqrt(max(0.0, var_t))
    phi       = state["phi"]
    drift_proxy   = tension - ema_t
    step_phase    = math.sin(state["step"] * 0.5)
    basin_dev     = psi_dir - PSI_VAC
    # 2D Ψ-coordinates: project Ψ_dir + tension onto orthogonal axes
    psi_x = psi_dir * math.cos(step_phase)
    psi_y = psi_dir * math.sin(step_phase)

    return [
        psi_dir, psi_ent, psi_tens, tension,
        ema_t, std_t, phi, drift_proxy,
        step_phase, float(prev_emit), motivation, basin_dev,
        psi_x, psi_y,
    ]


# ── motivation proxy (§24 8-factor stub, dim-reduced for $0 stub) ──
def motivation_proxy(state):
    return 0.4 + 0.3 * (state["tension"] / max(1e-6, state["tension_ema"] + state["tension"]))


# ── PCA closed-form via numpy.linalg.eigh ───────────────────────────
def pca_decompose(trajectory):
    """
    Closed-form PCA: covariance matrix eigendecomposition (eigh).
    Returns top-2 eigenvalues + ratio + cumulative variance captured.
    NO sklearn, NO RNG — pure numpy.linalg.
    """
    import numpy as np
    X = np.array(trajectory)            # (N, D)
    if X.shape[0] < 2:
        return {"lambda_1": 0.0, "lambda_2": 0.0,
                "lambda_ratio": 0.0, "top2_captured": 0.0,
                "n_points": X.shape[0], "dim": X.shape[1] if X.ndim > 1 else 0}
    Xc = X - X.mean(axis=0, keepdims=True)
    # Covariance (D x D) — symmetric PSD
    C = (Xc.T @ Xc) / max(1, X.shape[0] - 1)
    # Symmetric eigendecomposition (real eigenvalues, ordered ascending)
    eigs = np.linalg.eigvalsh(C)
    eigs = sorted(eigs.tolist(), reverse=True)
    lam1 = max(0.0, eigs[0]) if len(eigs) > 0 else 0.0
    lam2 = max(0.0, eigs[1]) if len(eigs) > 1 else 0.0
    total = sum(max(0.0, e) for e in eigs)
    ratio = lam1 / max(1e-12, lam2)
    top2_captured = (lam1 + lam2) / max(1e-12, total)
    return {
        "lambda_1":       lam1,
        "lambda_2":       lam2,
        "lambda_ratio":   ratio,
        "top2_captured":  top2_captured,
        "n_points":       X.shape[0],
        "dim":            X.shape[1],
        "total_variance": total,
    }


# ── slow-dwell + fast-crossing detector ────────────────────────────
def detect_dwell_crossing(trajectory):
    """
    Pure-fn deterministic detector — no RNG.
    Returns slow-dwell event count + fast-crossing event count.
    """
    import numpy as np
    X = np.array(trajectory)
    if X.shape[0] < 2:
        return {"slow_dwell_count": 0, "fast_crossing_count": 0,
                "delta_norms": [], "slow_runs": []}
    # Per-step Δψ Euclidean norm
    deltas = []
    for i in range(1, X.shape[0]):
        d = float(np.linalg.norm(X[i] - X[i-1]))
        deltas.append(d)
    # Fast crossings (single-turn Δ ≥ τ_fast)
    fast_count = sum(1 for d in deltas if d >= TAU_FAST)
    # Slow-dwell runs (≥ N_DWELL_MIN consecutive Δ ≤ τ_slow)
    slow_runs = []
    cur = 0
    for d in deltas:
        if d <= TAU_SLOW:
            cur += 1
        else:
            if cur >= N_DWELL_MIN:
                slow_runs.append(cur)
            cur = 0
    if cur >= N_DWELL_MIN:
        slow_runs.append(cur)
    return {
        "slow_dwell_count":    len(slow_runs),
        "slow_runs":           slow_runs,
        "fast_crossing_count": fast_count,
        "delta_norms":         deltas,
        "mean_delta":          sum(deltas) / max(1, len(deltas)),
        "max_delta":           max(deltas) if deltas else 0.0,
        "min_delta":           min(deltas) if deltas else 0.0,
    }


# ── Emission direction alignment (Δψ direction history coherence) ──
def emission_alignment(trajectory, emit_decisions):
    """
    Cosine similarity between current Δψ direction and historical
    emission-direction-mean.  Returns alignment_cos for each emission.
    """
    import numpy as np
    X = np.array(trajectory)
    if X.shape[0] < 2 or sum(emit_decisions) == 0:
        return {"n_emits": 0, "alignment_cos_mean": 0.0, "alignment_list": []}
    emit_directions = []
    alignments = []
    for i in range(1, X.shape[0]):
        if emit_decisions[i] == 1:
            d = X[i] - X[i-1]
            d_norm = float(np.linalg.norm(d))
            if d_norm > 1e-9:
                d_unit = d / d_norm
                if len(emit_directions) > 0:
                    hist_mean = np.mean(emit_directions, axis=0)
                    hist_norm = float(np.linalg.norm(hist_mean))
                    if hist_norm > 1e-9:
                        cos = float(np.dot(d_unit, hist_mean / hist_norm))
                        alignments.append(cos)
                emit_directions.append(d_unit.tolist())
    return {
        "n_emits":              sum(emit_decisions),
        "alignment_cos_mean":   sum(alignments) / max(1, len(alignments)),
        "alignment_list":       alignments,
        "n_aligned_above_tau":  sum(1 for c in alignments if c >= TAU_ALIGN),
    }


# ── _var ────────────────────────────────────────────────────────────
def _var(xs):
    if not xs:
        return 0.0
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


# ── 5 controllers — manifold-gating ladder ─────────────────────────
def controller_cell0_baseline(state, history):
    """§24-baseline scalar threshold — NO manifold."""
    return 1 if state["tension"] > IM_THRESHOLD_S24 else 0


def controller_cell1_a_only(state, history):
    """§75-FIRE A-only state-derived mirror — frozen scalar boundary.
    Code byte-equal to §75 cell1; numeric output differs at N=30 vs N=600
    (HONEST: this is mechanism-byte-equal mirror, not numeric byte-equal
    — measured at smaller-N for §82 manifold dwell scope, see B-S82-NOTE
    + B-S82-4)."""
    frozen_scalar = history.get("frozen_scalar", IM_THRESHOLD_S24)
    psi_off = abs(state["psi_dir"] - PSI_VAC)
    g1 = psi_off > BASIN_RADIUS
    g2 = state["tension"] > frozen_scalar
    g3 = state["phi"] > PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


def controller_cell2_manifold_only(state, history):
    """PCA-detect manifold, slow-dwell awareness — NO fast-crossing gate."""
    # Emit if state is "off-manifold" by PCA-distance heuristic
    # (cell2 distinguishing feature: manifold detected, but gate disabled)
    trajectory = history.get("trajectory", [])
    if len(trajectory) < 4:
        return 0
    # If we're in slow-dwell (recent Δ small), suppress emission (manifold dwell)
    recent = trajectory[-3:]
    import numpy as np
    recent_arr = np.array(recent)
    if recent_arr.shape[0] >= 2:
        deltas = [float(np.linalg.norm(recent_arr[i] - recent_arr[i-1]))
                  for i in range(1, recent_arr.shape[0])]
        if all(d <= TAU_SLOW for d in deltas):
            return 0   # In slow-dwell, manifold gates against emission
    # Otherwise fall through to A-only baseline (NO fast-crossing gate)
    psi_off = abs(state["psi_dir"] - PSI_VAC)
    g1 = psi_off > BASIN_RADIUS
    g2 = state["tension"] > IM_THRESHOLD_S24
    g3 = state["phi"] > PHI_RATCHET / 2.0
    return 1 if (g1 and g2 and g3) else 0


def controller_cell3_fast_crossing_only(state, history):
    """Fast-crossing-only gate detected — NO slow-dwell history."""
    trajectory = history.get("trajectory", [])
    if len(trajectory) < 2:
        return 0
    import numpy as np
    last_v   = np.array(trajectory[-1])
    prev_v   = np.array(trajectory[-2])
    delta    = float(np.linalg.norm(last_v - prev_v))
    # Emit ONLY on fast crossings (single-turn Δ ≥ τ_fast), no dwell context
    return 1 if delta >= TAU_FAST else 0


def controller_cell4_full_hierarchical(state, history):
    """Full hierarchical: slow-dwell + fast-crossing + emission alignment."""
    trajectory = history.get("trajectory", [])
    emit_history = history.get("emit_history", [])
    if len(trajectory) < N_DWELL_MIN + 1:
        return 0
    import numpy as np
    # Check slow-dwell context: was the recent window slow?
    recent = trajectory[-(N_DWELL_MIN + 1):]
    recent_deltas = [float(np.linalg.norm(np.array(recent[i]) - np.array(recent[i-1])))
                     for i in range(1, len(recent))]
    in_slow_dwell = sum(1 for d in recent_deltas if d <= TAU_SLOW) >= N_DWELL_MIN - 1
    # Check fast-crossing trigger
    last_delta = recent_deltas[-1] if recent_deltas else 0.0
    fast_crossing = last_delta >= TAU_FAST
    # Emission alignment with prior emission direction history
    aligned = True
    if sum(emit_history) >= 2:
        # Compute historical emission direction
        prev_emit_dirs = []
        for i in range(1, len(trajectory)):
            if i - 1 < len(emit_history) and emit_history[i - 1] == 1:
                d = np.array(trajectory[i]) - np.array(trajectory[i-1])
                dn = float(np.linalg.norm(d))
                if dn > 1e-9:
                    prev_emit_dirs.append(d / dn)
        if prev_emit_dirs:
            hist_mean = np.mean(prev_emit_dirs, axis=0)
            hist_norm = float(np.linalg.norm(hist_mean))
            cur_d = np.array(trajectory[-1]) - np.array(trajectory[-2])
            cur_norm = float(np.linalg.norm(cur_d))
            if hist_norm > 1e-9 and cur_norm > 1e-9:
                cos = float(np.dot(cur_d / cur_norm, hist_mean / hist_norm))
                aligned = cos >= TAU_ALIGN
    # Full hierarchical gate: dwell + fast-crossing + (aligned OR first emission)
    if in_slow_dwell and fast_crossing and aligned:
        return 1
    return 0


# ── run_loop with history tracking ─────────────────────────────────
def run_loop(controller, n_steps=N_LOOP_STEPS, seed=SEED, frozen_scalar=None):
    rng = LCG(seed)
    state = init_state()
    trajectory = []
    emit_decisions = []
    emit_step_indices = []

    history = {"trajectory": trajectory, "emit_history": emit_decisions}
    if frozen_scalar is not None:
        history["frozen_scalar"] = frozen_scalar

    for _ in range(n_steps):
        motivation = motivation_proxy(state)
        prev_emit = emit_decisions[-1] if emit_decisions else 0
        psi_vec = psi_state_vector(state, prev_emit, motivation)
        trajectory.append(psi_vec)

        e = controller(state, history)
        emit_decisions.append(e)
        if e == 1:
            emit_step_indices.append(state["step"])

        state = physics_step(state, e, rng)

    n_emit = sum(emit_decisions)
    rate = n_emit / n_steps
    maj_frac = max(n_emit, n_steps - n_emit) / n_steps
    var_dec = _var(emit_decisions)

    if len(emit_step_indices) >= 2:
        intervals = [emit_step_indices[i+1] - emit_step_indices[i]
                     for i in range(len(emit_step_indices)-1)]
        interval_var = _var(intervals)
    else:
        intervals = []
        interval_var = 0.0

    pca = pca_decompose(trajectory)
    dwell = detect_dwell_crossing(trajectory)
    align = emission_alignment(trajectory, emit_decisions)

    return {
        "n_steps":              n_steps,
        "n_emit":               n_emit,
        "emit_rate":            rate,
        "decision_var":         var_dec,
        "majority_fraction":    maj_frac,
        "interval_var":         interval_var,
        "n_intervals":          len(intervals),
        "non_degenerate":       (var_dec > TAU_NONDEG and maj_frac < MAJ_COLLAPSE
                                 and interval_var > TAU_NONDEG and len(intervals) >= 2),
        "pca":                  pca,
        "dwell":                {k: v for k, v in dwell.items() if k != "delta_norms"},
        "alignment":            {k: v for k, v in align.items() if k != "alignment_list"},
        "honest_coherent_stub_NA": True,   # NO body emission this cycle, see B-S82-NOTE
    }


def warmup_capture(n=10, seed=SEED):
    rng = LCG(seed)
    state = init_state()
    tensions = []
    for _ in range(n):
        tensions.append(state["tension"])
        state = physics_step(state, 0, rng)
    mean_t = sum(tensions) / len(tensions)
    return {"n_warmup": n, "tension_mean": mean_t}


def main():
    wu = warmup_capture()

    r0 = run_loop(controller_cell0_baseline)
    r1 = run_loop(controller_cell1_a_only, frozen_scalar=wu["tension_mean"])
    r2 = run_loop(controller_cell2_manifold_only)
    r3 = run_loop(controller_cell3_fast_crossing_only)
    r4 = run_loop(controller_cell4_full_hierarchical)

    # 4-corner verdict (g3 — read off measured values, NOT pre-loaded)
    cell1_non_deg = r1["non_degenerate"]
    cell4_non_deg = r4["non_degenerate"]
    cell4_majfrac = r4["majority_fraction"]
    cell4_intvar  = r4["interval_var"]
    cell1_intvar  = r1["interval_var"]
    cell2_intvar  = r2["interval_var"]
    cell3_intvar  = r3["interval_var"]
    max_subaxis   = max(cell2_intvar, cell3_intvar)

    alpha_manifold_adds_differential = (cell4_intvar > cell1_intvar
                                        and r4["n_emit"] != r1["n_emit"])
    beta_manifold_but_gate_collapses = (r2["pca"]["top2_captured"] > 0.5
                                        and cell4_majfrac >= MAJ_COLLAPSE)
    gamma_subaxis_mixed              = (cell4_intvar < max_subaxis)
    delta_cell1_mirror_maintained    = cell1_intvar > TAU_NONDEG

    decomp_table = {
        "cell0_§24_baseline": {
            "controller_class": "§24 scalar threshold, no manifold",
            "pca_lambda_ratio": r0["pca"]["lambda_ratio"],
            "pca_top2_captured": r0["pca"]["top2_captured"],
            "slow_dwell_count": r0["dwell"]["slow_dwell_count"],
            "fast_crossing_count": r0["dwell"]["fast_crossing_count"],
            "interval_var":     r0["interval_var"],
            "emit_rate":        r0["emit_rate"],
            "n_emit":           r0["n_emit"],
            "majority_fraction":r0["majority_fraction"],
            "non_degenerate":   r0["non_degenerate"],
            "alignment_cos_mean": r0["alignment"]["alignment_cos_mean"],
            "raw":              r0,
        },
        "cell1_§75_FIRE_A_only_mirror": {
            "controller_class": "§75 cell1 A-only state-derived (code byte-equal, N=30 not 600)",
            "pca_lambda_ratio": r1["pca"]["lambda_ratio"],
            "pca_top2_captured": r1["pca"]["top2_captured"],
            "slow_dwell_count": r1["dwell"]["slow_dwell_count"],
            "fast_crossing_count": r1["dwell"]["fast_crossing_count"],
            "interval_var":     r1["interval_var"],
            "emit_rate":        r1["emit_rate"],
            "n_emit":           r1["n_emit"],
            "majority_fraction":r1["majority_fraction"],
            "non_degenerate":   r1["non_degenerate"],
            "alignment_cos_mean": r1["alignment"]["alignment_cos_mean"],
            "s75_cell1_reference_int_var_at_n600": 6.378772,
            "raw":              r1,
        },
        "cell2_manifold_only": {
            "controller_class": "PCA detect + slow-dwell awareness, no fast-crossing gate",
            "pca_lambda_ratio": r2["pca"]["lambda_ratio"],
            "pca_top2_captured": r2["pca"]["top2_captured"],
            "slow_dwell_count": r2["dwell"]["slow_dwell_count"],
            "fast_crossing_count": r2["dwell"]["fast_crossing_count"],
            "interval_var":     r2["interval_var"],
            "emit_rate":        r2["emit_rate"],
            "n_emit":           r2["n_emit"],
            "majority_fraction":r2["majority_fraction"],
            "non_degenerate":   r2["non_degenerate"],
            "alignment_cos_mean": r2["alignment"]["alignment_cos_mean"],
            "raw":              r2,
        },
        "cell3_fast_crossing_only": {
            "controller_class": "Fast-crossing gate only, no slow-dwell history",
            "pca_lambda_ratio": r3["pca"]["lambda_ratio"],
            "pca_top2_captured": r3["pca"]["top2_captured"],
            "slow_dwell_count": r3["dwell"]["slow_dwell_count"],
            "fast_crossing_count": r3["dwell"]["fast_crossing_count"],
            "interval_var":     r3["interval_var"],
            "emit_rate":        r3["emit_rate"],
            "n_emit":           r3["n_emit"],
            "majority_fraction":r3["majority_fraction"],
            "non_degenerate":   r3["non_degenerate"],
            "alignment_cos_mean": r3["alignment"]["alignment_cos_mean"],
            "raw":              r3,
        },
        "cell4_full_hierarchical": {
            "controller_class": "Full: slow-dwell + fast-crossing + emission-direction-aligned",
            "pca_lambda_ratio": r4["pca"]["lambda_ratio"],
            "pca_top2_captured": r4["pca"]["top2_captured"],
            "slow_dwell_count": r4["dwell"]["slow_dwell_count"],
            "fast_crossing_count": r4["dwell"]["fast_crossing_count"],
            "interval_var":     r4["interval_var"],
            "emit_rate":        r4["emit_rate"],
            "n_emit":           r4["n_emit"],
            "majority_fraction":r4["majority_fraction"],
            "non_degenerate":   r4["non_degenerate"],
            "alignment_cos_mean": r4["alignment"]["alignment_cos_mean"],
            "raw":              r4,
        },
    }

    result = {
        "research_md_section": "§82",
        "title": ("Manifold-gated hierarchical emission — §80 biology "
                  "anchor (Leifer C. elegans biorxiv:2025.03.09.642241) "
                  "applied to anima Ψ-state; §75-FIRE A-only extension"),
        "biology_anchor": "biorxiv:2025.03.09.642241 (Leifer C. elegans intrinsic neuronal manifold gating)",
        "cost": ("$0 Mac CPU local · NO GPU · NO model.forward · "
                 "NO autograd · NO weight mutation · NO dispatch · orphan 0"),
        "north_star_unchanged":     True,
        "milestone_unchanged":      "§15 + §51 + §72 (GOAL 미도달)",
        "capability_claim":         0,
        "g3_honest_framing": (
            "§82 = $0 stub manifold-gating mechanism probe — NOT GOAL emergence, "
            "NOT real-ckpt PCA, NOT C. elegans neural recording. ψ-state is "
            "LCG-driven 14-dim STUB; PCA over 30 turns is small-N. The "
            "biology anchor is hierarchical-mechanism inspiration only — "
            "no claim that anima ψ-state = C. elegans manifold. cell1 "
            "byte-equal mirror is *code-byte-equal* to §75 cell1, "
            "NOT numeric-byte-equal at smaller N. necessary-not-sufficient "
            "(B-EMERGE-7) carries throughout."
        ),
        "constants": {
            "PSI_VAC":          PSI_VAC,
            "BASIN_RADIUS":     BASIN_RADIUS,
            "LAMBDA_STD":       LAMBDA_STD,
            "EMA_BETA":         EMA_BETA,
            "SEED":             SEED,
            "N_LOOP_STEPS":     N_LOOP_STEPS,
            "TAU_NONDEG":       TAU_NONDEG,
            "MAJ_COLLAPSE":     MAJ_COLLAPSE,
            "IM_THRESHOLD_S24": IM_THRESHOLD_S24,
            "TAU_SLOW":         TAU_SLOW,
            "TAU_FAST":         TAU_FAST,
            "N_DWELL_MIN":      N_DWELL_MIN,
            "TAU_ALIGN":        TAU_ALIGN,
            "PSI_STATE_DIM":    PSI_STATE_DIM,
        },
        "warmup_capture":           wu,
        "decomposition_table":      decomp_table,
        "verdict_4corner": {
            "alpha_manifold_adds_differential":   alpha_manifold_adds_differential,
            "beta_manifold_but_gate_collapses":   beta_manifold_but_gate_collapses,
            "gamma_subaxis_mixed":                gamma_subaxis_mixed,
            "delta_cell1_mirror_maintained":      delta_cell1_mirror_maintained,
        },
        "honest_caveats": [
            "Stub ψ-state (LCG) NOT real model.forward",
            "C. elegans biology ≠ anima 14-dim ψ-state — analogy only",
            "PCA over 30 turns is small-N; eigenvalue ordering bounded",
            "Manifold-as-mechanism is measurement-derived, not cell-state",
            "§75-FIRE cell1 stub mirror = code-byte-equal NOT numeric",
            "Necessary-not-sufficient (B-EMERGE-7) — emission gate ≠ emergence",
            "No body production, honest §9 not applicable (B-S82-NOTE)",
        ],
    }

    out_path = os.path.join(HERE, "result.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"§82 manifold-gating smoke COMPLETE")
    print(f"  cell0_§24_baseline      int_var={r0['interval_var']:.4f}  n_emit={r0['n_emit']}  pca_top2={r0['pca']['top2_captured']:.3f}  slow_d={r0['dwell']['slow_dwell_count']}  fast_c={r0['dwell']['fast_crossing_count']}")
    print(f"  cell1_§75_A_only_mirror int_var={r1['interval_var']:.4f}  n_emit={r1['n_emit']}  pca_top2={r1['pca']['top2_captured']:.3f}  slow_d={r1['dwell']['slow_dwell_count']}  fast_c={r1['dwell']['fast_crossing_count']}")
    print(f"  cell2_manifold_only     int_var={r2['interval_var']:.4f}  n_emit={r2['n_emit']}  pca_top2={r2['pca']['top2_captured']:.3f}  slow_d={r2['dwell']['slow_dwell_count']}  fast_c={r2['dwell']['fast_crossing_count']}")
    print(f"  cell3_fast_crossing     int_var={r3['interval_var']:.4f}  n_emit={r3['n_emit']}  pca_top2={r3['pca']['top2_captured']:.3f}  slow_d={r3['dwell']['slow_dwell_count']}  fast_c={r3['dwell']['fast_crossing_count']}")
    print(f"  cell4_full_hierarchical int_var={r4['interval_var']:.4f}  n_emit={r4['n_emit']}  pca_top2={r4['pca']['top2_captured']:.3f}  slow_d={r4['dwell']['slow_dwell_count']}  fast_c={r4['dwell']['fast_crossing_count']}")
    print(f"  4-corner verdict: α={alpha_manifold_adds_differential}  β={beta_manifold_but_gate_collapses}  γ={gamma_subaxis_mixed}  δ={delta_cell1_mirror_maintained}")
    print(f"  result.json written to {out_path}")

    return result


if __name__ == "__main__":
    main()
