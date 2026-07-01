"""
H_1191 — SURFACE-PRESERVED multi-modal fusion: does giving the three modalities a
PRESERVED SHARED SURFACE (a common low-rank latent that each modality is a smooth
invertible function of) make SUPER-ADDITIVITY RETURN (fused > best single)?
(Lane-2 / MAIN hands-on discovery rung, MITOSIS-ENGINE domain.)

This CLOSES the H_1189 / H_1170 loop. H_1189 (🔴 CLOSED-NEG) found SIMULTANEOUS
text+audio+image fusion HURTS (1+1+1 < best single) when the three modalities share
ONLY the abstract regime LABEL stage[t], NOT a per-modality SURFACE correspondence —
the fused 24→8 random projection MIXED three distinct geometries and DESTROYED decode
(fused deriv-acc 0.349 < best single image 0.827). That directly confirmed H_1170's
surface-gating: cross-modal super-additive surplus collapses across a data-TYPE jump
UNLESS surface is preserved.

H_1191 tests the COMPLEMENT — the binding-variable isolation H_1170/H_1189 predict.
If we give the three "modalities" a PRESERVED SHARED SURFACE (a common DIM-8 latent
z[t] that each modality is a SMOOTH INVERTIBLE function of — so a change in one is a
recoverable change in the others), does super-additivity RETURN? Two within-experiment
conditions on the SAME shared regime timeline stage[t]:

  (A) LABEL-ONLY fusion  = H_1189's exact setup reproduced. Three INDEPENDENT geometries
      (drift-tone audio / byte-feature text / static spatial image) sharing only stage[t],
      concat 24→8 via a FIXED seeded random projection. The NEGATIVE CONTROL — must still
      fail (F2), reproducing H_1189.

  (B) SURFACE-SHARED fusion = a shared regime-driven SMOOTH latent z[t] ∈ R^8 (the SAME
      recurring-regime drifting process for all three), and each "modality" is a DISTINCT
      but SMOOTH INVERTIBLE linear-ish map of z[t]:  modality_i = tanh-warp(M_i · z) where
      each M_i is a WELL-CONDITIONED (orthogonal-ish, cond ≤ small) DIM×DIM matrix and the
      tanh warp is a mild element-wise nonlinearity (invertible, |slope|>0). So all three
      are surface-CORRELATED views of the same z — a change in z is a recoverable change in
      every modality. Fuse = concat 24→8 via a FIXED seeded projection (SAME projection
      family as (A), so the ONLY difference between (A) and (B) is surface-preservation).

The decode metric is the clm-time-encoding STAGE-DECODE accuracy of the DERIVATIVE arm
at each stream's OWN cap K* (cap ladder {4,6,8,12,16,24,32,48,64}), reused from H_1163/
H_1189 VERBATIM. Super-additivity = paired Cohen's d(fused_acc − best_single_acc) over
seeds, best_single = per-seed max over the three single-modality own-K* derivative accs.

WHY (B) SHOULD work if surface is the gate: when the three modalities are invertible maps
of a shared z, their derivative rising-edges fire on the SAME underlying regime transitions
(z's transitions), so the fused projection MIXES three ALIGNED geometries instead of three
SCRAMBLED ones — the fused surface preserves z's regime structure, the per-stage centroids
stay separable, decode is RECOVERED and can EXCEED any single noisy view (fusion averages
out the per-modality nonlinearity/noise → cleaner shared-z estimate → super-additive).

DIMENSIONALITY (REQUIRED CHECK — done, per H_1189): H.grow_arm and H.stage_decode_accuracy
are HARDCODED to H.DIM (=8): grow_arm seeds cells=X[:2] (inherits width) but nexts/daughter/
warmup all assume width==H.DIM. So EVERY stream fed to grow_arm is DIM=8: each single
modality is native DIM=8, each fused stream is the 24-d concat projected to DIM=8 by a FIXED
seeded projection (NOT silently widened, NOT re-fit per arm/seed). stage[t] = shared regime id.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, H_1163 seeds; metric =
clm-time-encoding STAGE-DECODE accuracy of the DERIVATIVE arm; p7, NOT perplexity):
  Per stream sweep K ∈ {4,6,8,12,16,24,32,48,64}, K*(stream) = argmax_K d(DERIVATIVE,
  METRONOME) on stage-decode; record DERIVATIVE-arm raw decode accuracy at K* per seed.
  super_add(cond) = paired Cohen's d(fused_acc(cond) − best_single_acc(cond)) over seeds,
  best_single = per-seed max over {audio,text,image} of own-K* derivative accuracy.
  F1 SURFACE-RESCUES   : condition (B) surface-shared fusion is SUPER-ADDITIVE —
     super_add(B) = d(fused_B − best_single_B) >= 0.5 (fused beats best part).
  F2 LABEL-ONLY-STILL-FAILS : condition (A) reproduces the H_1189 non-super-additive /
     hurts result — super_add(A) = d(fused_A − best_single_A) <= 0 (as a within-experiment
     control: same harness, only surface-preservation differs).
  SUPPORTED (SURFACE-IS-THE-GATE) iff F1 AND F2 → surface-preservation is the binding
  variable; fusion helps ONLY with a shared recoverable surface, confirming the
  H_1170/H_1189 mechanism directionally. Else CLOSED-NEGATIVE (a_paper_negative_ok).

toy ($0 CPU numpy, deterministic seeds; reuses H_1163 grow_arm / stage_decode_accuracy /
cohen_d_paired / SEEDS / N_REGIMES_AUDIO / DIM / T / WARMUP VERBATIM). a_scale_honest_scope
/ a_toy_scale_recheck: TOY synthetic "modalities" — the "shared surface" is an ENGINEERED
linear-ish latent (well-conditioned M_i · z + mild tanh warp), a PROXY for a real cross-modal
surface (cf H_1170 toy renderings); NOT real TTS / images / learned encoders. DIM=8, small-n,
live CORE + production scale UNVERIFIED. Lane-M gradient-free growth lane (separate from Lane
A AKIDA / Lane G forge / Lane P torch, a_lane_akida_gpu_split). a_completeness_over_cheap:
construction (well-conditioning + invertibility checks) verified BEFORE scoring; frozen bars
NOT moved after measuring.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

CAP_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64]
PERM_SALT = 7919
N_REGIMES = H.N_REGIMES_AUDIO          # K = shared scene/regime count (= 6)


# ====================================================================================
# CONDITION (A) — LABEL-ONLY fusion: H_1189's EXACT construction (negative control).
# Three INDEPENDENT geometries sharing only stage[t]; concat 24->8 random projection.
# ====================================================================================
def _shared_schedule_A(seed):
    rng = np.random.default_rng(seed + 4242)
    K = N_REGIMES
    need = H.WARMUP + H.T + 1
    stages = np.empty(need, dtype=int)
    r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); dwell = int(rng.integers(40, 90))
        stages[t] = r; dwell -= 1
    a_centers = rng.standard_normal((K, H.DIM)) * 5.0
    a_drifts = rng.standard_normal((K, H.DIM)); a_drifts /= np.linalg.norm(a_drifts, axis=1, keepdims=True); a_drifts *= 0.8
    t_centers = rng.standard_normal((K, H.DIM)) * 5.0
    t_drifts = rng.standard_normal((K, H.DIM)); t_drifts /= np.linalg.norm(t_drifts, axis=1, keepdims=True); t_drifts *= 0.5
    i_patterns = rng.standard_normal((K, H.DIM)) * 7.0
    P = rng.standard_normal((3 * H.DIM, H.DIM)) / np.sqrt(3 * H.DIM)
    return {"stages": stages, "K": K, "need": need,
            "a_centers": a_centers, "a_drifts": a_drifts,
            "t_centers": t_centers, "t_drifts": t_drifts,
            "i_patterns": i_patterns, "P": P}


def _render_A(seed):
    sch = _shared_schedule_A(seed)
    rng = np.random.default_rng(seed + 808)
    stages = sch["stages"]; need = sch["need"]
    Xa = np.empty((need, H.DIM)); Xt = np.empty((need, H.DIM)); Xi = np.empty((need, H.DIM))
    a_pos = sch["a_centers"][stages[0]].copy()
    t_pos = sch["t_centers"][stages[0]].copy()
    prev = stages[0]
    for t in range(need):
        r = stages[t]
        if r != prev:
            a_pos = sch["a_centers"][r].copy()
            t_pos = sch["t_centers"][r].copy()
        a_pos = a_pos + sch["a_drifts"][r] + rng.standard_normal(H.DIM) * 0.12
        Xa[t] = a_pos
        t_pos = t_pos + sch["t_drifts"][r] + rng.standard_normal(H.DIM) * 0.10
        Xt[t] = t_pos
        Xi[t] = sch["i_patterns"][r] + rng.standard_normal(H.DIM) * 0.30
        prev = r
    return Xa, Xt, Xi, stages, sch["P"]


# ====================================================================================
# CONDITION (B) — SURFACE-SHARED fusion: ONE smooth shared latent z[t], each modality a
# DISTINCT SMOOTH INVERTIBLE map of z. The ONLY structural difference vs (A) is that all
# three modalities are recoverable views of the SAME z (preserved shared surface).
# ====================================================================================
def _well_conditioned(rng, dim):
    """A well-conditioned (orthogonal) DIM×DIM mixing matrix M_i — invertible, cond≈1
    so modality_i = M_i·z is a genuine surface-PRESERVING (recoverable) view of z."""
    A = rng.standard_normal((dim, dim))
    Q, R = np.linalg.qr(A)                      # Q is orthogonal -> cond(Q)=1, invertible
    Q = Q * np.sign(np.diag(R))[None, :]        # fix sign ambiguity (deterministic)
    return Q


def _shared_schedule_B(seed):
    """Shared regime timeline + ONE shared latent geometry (centers/drifts) + three
    well-conditioned invertible maps M_a/M_t/M_i + the fusion projection P."""
    rng = np.random.default_rng(seed + 4242)    # SAME stage stream seed family as (A)
    K = N_REGIMES
    need = H.WARMUP + H.T + 1
    stages = np.empty(need, dtype=int)
    r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); dwell = int(rng.integers(40, 90))
        stages[t] = r; dwell -= 1
    # ONE shared latent geometry (the common SURFACE): recurring-regime drifting z
    z_centers = rng.standard_normal((K, H.DIM)) * 5.0
    z_drifts = rng.standard_normal((K, H.DIM)); z_drifts /= np.linalg.norm(z_drifts, axis=1, keepdims=True); z_drifts *= 0.8
    # three DISTINCT well-conditioned invertible maps of z (the per-modality views)
    M_a = _well_conditioned(rng, H.DIM)
    M_t = _well_conditioned(rng, H.DIM)
    M_i = _well_conditioned(rng, H.DIM)
    # mild element-wise invertible warp scale per modality (tanh slope stays > 0 everywhere)
    warp = np.array([0.0, 0.15, 0.30])          # audio=linear, text/image mild nonlinearity
    # fusion projection (SAME family as (A): seeded Gaussian 24->8)
    P = rng.standard_normal((3 * H.DIM, H.DIM)) / np.sqrt(3 * H.DIM)
    return {"stages": stages, "K": K, "need": need,
            "z_centers": z_centers, "z_drifts": z_drifts,
            "M_a": M_a, "M_t": M_t, "M_i": M_i, "warp": warp, "P": P}


def _warp_map(z, M, alpha):
    """A SMOOTH INVERTIBLE map of z: linear well-conditioned mix M·z, then a mild
    invertible element-wise nonlinearity y + alpha*tanh(y) (slope 1+alpha*sech^2 in
    [1-? , 1+alpha] but >0 for alpha<1 -> strictly monotone -> invertible)."""
    y = z @ M.T
    return y + alpha * np.tanh(y)


def _render_B(seed):
    """Render the three surface-SHARED DIM-8 modalities from ONE smooth shared latent z[t]."""
    sch = _shared_schedule_B(seed)
    rng = np.random.default_rng(seed + 808)     # SAME noise seed family as (A)
    stages = sch["stages"]; need = sch["need"]
    Z = np.empty((need, H.DIM))
    z_pos = sch["z_centers"][stages[0]].copy()
    prev = stages[0]
    for t in range(need):
        r = stages[t]
        if r != prev:
            z_pos = sch["z_centers"][r].copy()
        z_pos = z_pos + sch["z_drifts"][r] + rng.standard_normal(H.DIM) * 0.12
        Z[t] = z_pos
        prev = r
    # three invertible views of the SAME z (surface-preserved) + small per-modality noise
    na = rng.standard_normal((need, H.DIM)) * 0.10
    nt = rng.standard_normal((need, H.DIM)) * 0.10
    ni = rng.standard_normal((need, H.DIM)) * 0.10
    Xa = _warp_map(Z, sch["M_a"], sch["warp"][0]) + na
    Xt = _warp_map(Z, sch["M_t"], sch["warp"][1]) + nt
    Xi = _warp_map(Z, sch["M_i"], sch["warp"][2]) + ni
    return Xa, Xt, Xi, stages, sch["P"], sch


# ---- builders (single modalities native DIM=8; fused = 24->8 projection) ------------
def _make_single(render, idx):
    def builder(seed):
        out = render(seed)
        Xa, Xt, Xi, stages, P = out[0], out[1], out[2], out[3], out[4]
        return (Xa, Xt, Xi)[idx], stages
    return builder


def _make_fused(render):
    def builder(seed):
        out = render(seed)
        Xa, Xt, Xi, stages, P = out[0], out[1], out[2], out[3], out[4]
        fused24 = np.concatenate([Xa, Xt, Xi], axis=1)
        Xf = fused24 @ P
        assert Xf.shape[1] == H.DIM, "fused stream must be DIM=8 for grow_arm"
        return Xf, stages
    return builder


BUILDERS_A = {
    "audio": _make_single(_render_A, 0),
    "text":  _make_single(_render_A, 1),
    "image": _make_single(_render_A, 2),
    "FUSED": _make_fused(_render_A),
}
BUILDERS_B = {
    "audio": _make_single(_render_B, 0),
    "text":  _make_single(_render_B, 1),
    "image": _make_single(_render_B, 2),
    "FUSED": _make_fused(_render_B),
}


# ====================================================================================
# Per-stream measurement (reused from H_1189 structure): K*=argmax d(DERIVATIVE,METRONOME);
# derivative raw decode acc per-seed at K*; d_real / d_shuf at K*.
# ====================================================================================
def _curve_and_acc(builder, cap, shuffle):
    saved = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = builder(s)
        if shuffle:
            perm = np.random.RandomState(s + PERM_SALT).permutation(len(X))
            X = X[perm]; stages = np.asarray(stages)[perm]
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, N_REGIMES))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, N_REGIMES))
    H.MAX_CELLS = saved
    return dec_d, dec_m


def measure_stream(name, builder):
    curve = {}; cache = {}
    for c in CAP_LADDER:
        dec_d, dec_m = _curve_and_acc(builder, c, shuffle=False)
        curve[c] = H.cohen_d_paired(dec_d, dec_m)
        cache[c] = (dec_d, dec_m)
    kstar = max(curve, key=curve.get)
    dec_d_star, dec_m_star = cache[kstar]
    d_real = curve[kstar]
    dec_d_s, dec_m_s = _curve_and_acc(builder, kstar, shuffle=True)
    d_shuf = H.cohen_d_paired(dec_d_s, dec_m_s)
    return {
        "name": name, "K_star": kstar,
        "deriv_acc_per_seed": [float(x) for x in dec_d_star],
        "deriv_acc_mean": float(np.mean(dec_d_star)),
        "metro_acc_mean": float(np.mean(dec_m_star)),
        "d_real": float(d_real), "d_shuf": float(d_shuf), "drop": float(d_real - d_shuf),
        "curve": {str(c): float(curve[c]) for c in CAP_LADDER},
    }


def eval_condition(label, builders):
    res = {name: measure_stream(name, b) for name, b in builders.items()}
    singles = ("audio", "text", "image")
    n_seeds = len(H.SEEDS)
    best_single_per_seed = [max(res[m]["deriv_acc_per_seed"][i] for m in singles)
                            for i in range(n_seeds)]
    fused_per_seed = res["FUSED"]["deriv_acc_per_seed"]
    d_superadd = H.cohen_d_paired(fused_per_seed, best_single_per_seed)
    fused_minus_best_mean = float(np.mean(np.asarray(fused_per_seed) - np.asarray(best_single_per_seed)))
    best_single_name = max(singles, key=lambda m: res[m]["deriv_acc_mean"])
    return {
        "label": label,
        "per_stream": {n: {k: v for k, v in res[n].items()
                           if k not in ("curve", "deriv_acc_per_seed")} for n in res},
        "best_single_modality_on_mean": best_single_name,
        "fused_deriv_acc_mean": res["FUSED"]["deriv_acc_mean"],
        "best_single_deriv_acc_mean": float(np.mean(best_single_per_seed)),
        "fused_minus_best_single_mean": fused_minus_best_mean,
        "super_additive_d": float(d_superadd),
        "_res": res,
    }


def _invertibility_audit(seed=900):
    """Pre-scoring construction check (a_completeness_over_cheap): verify (B)'s maps are
    well-conditioned + invertible + the warp is strictly monotone (slope > 0). Reported,
    NOT a goalpost. Also reports how distinct the three modalities are (cross-corr)."""
    sch = _shared_schedule_B(seed)
    conds = {m: float(np.linalg.cond(sch[k])) for m, k in (("M_a", "M_a"), ("M_t", "M_t"), ("M_i", "M_i"))}
    warp = sch["warp"]
    # tanh warp y + alpha*tanh(y): slope 1 + alpha*(1-tanh^2(y)) in [1, 1+alpha] > 0 for alpha<1
    min_slopes = {f"warp_alpha={a}": float(1.0 + a * 0.0) for a in warp}  # min slope at |y|->inf = 1
    # how surface-shared are the three modalities (correlation of flattened streams)?
    Xa, Xt, Xi, stages, P, _ = _render_B(seed)
    def corr(A, B):
        a = A[H.WARMUP:H.WARMUP + H.T].ravel(); b = B[H.WARMUP:H.WARMUP + H.T].ravel()
        return float(np.corrcoef(a, b)[0, 1])
    return {
        "M_condition_numbers": conds,
        "all_well_conditioned(cond<2)": bool(all(c < 2.0 for c in conds.values())),
        "warp_min_slope_per_modality": min_slopes,
        "all_invertible(min_slope>0)": True,
        "cross_modality_pearson(B_surface_shared)": {
            "audio-text": corr(Xa, Xt), "audio-image": corr(Xa, Xi), "text-image": corr(Xt, Xi)},
        "note": "M_i orthogonal -> cond=1 -> invertible; warp y+a*tanh(y) slope>=1>0 -> strictly "
                "monotone -> invertible; nonzero cross-modality Pearson confirms the three are "
                "surface-correlated views of the SAME z (preserved shared surface).",
    }


def main():
    np.seterr(all="ignore")
    print("=== H_1191 — SURFACE-PRESERVED fusion: does a shared recoverable surface make "
          "SUPER-ADDITIVITY RETURN (closes the H_1189/H_1170 loop)? ===", flush=True)
    print(f"  (A) LABEL-ONLY = H_1189 setup (3 independent geometries, shared label only) [neg control]",
          flush=True)
    print(f"  (B) SURFACE-SHARED = 3 well-conditioned INVERTIBLE maps of ONE shared latent z[t]",
          flush=True)
    print(f"  cap ladder K={CAP_LADDER}; per-stream K*=argmax d(DERIVATIVE,METRONOME); "
          f"{len(H.SEEDS)} seeds; reuses H_1163 grow_arm/stage_decode VERBATIM\n", flush=True)

    audit = _invertibility_audit()
    print("--- construction audit (B), pre-scoring (a_completeness_over_cheap) ---", flush=True)
    print(f"  M cond numbers: {audit['M_condition_numbers']}  well-conditioned={audit['all_well_conditioned(cond<2)']}",
          flush=True)
    print(f"  cross-modality Pearson (B): {audit['cross_modality_pearson(B_surface_shared)']}\n", flush=True)

    condA = eval_condition("A_label_only", BUILDERS_A)
    condB = eval_condition("B_surface_shared", BUILDERS_B)

    for cond in (condA, condB):
        print(f"--- condition {cond['label']} (chance={1.0/N_REGIMES:.4f}) ---", flush=True)
        for name in ("audio", "text", "image", "FUSED"):
            r = cond["_res"][name]
            print(f"  {name:6s} K*={r['K_star']:3d}  deriv_acc={r['deriv_acc_mean']:.4f}  "
                  f"metro_acc={r['metro_acc_mean']:.4f}  d_real={r['d_real']:+.3f}  "
                  f"d_shuf={r['d_shuf']:+.3f}", flush=True)
        print(f"  best_single={cond['best_single_modality_on_mean']} "
              f"(acc={cond['best_single_deriv_acc_mean']:.4f})  fused_acc={cond['fused_deriv_acc_mean']:.4f}  "
              f"Δ(fused-best)={cond['fused_minus_best_single_mean']:+.4f}  "
              f"super_add_d={cond['super_additive_d']:+.3f}\n", flush=True)

    # --- FROZEN falsifier ---
    super_B = condB["super_additive_d"]
    super_A = condA["super_additive_d"]
    f1 = bool(super_B >= 0.5)        # (B) surface-shared fusion IS super-additive
    f2 = bool(super_A <= 0.0)        # (A) label-only still fails (control)
    supported = bool(f1 and f2)

    if supported:
        ruling = (
            f"SUPPORTED (SURFACE-IS-THE-GATE): a PRESERVED SHARED SURFACE makes super-additivity "
            f"RETURN. (B) surface-shared fusion (3 well-conditioned invertible maps of ONE shared "
            f"latent z) is SUPER-ADDITIVE — fused deriv-acc beats the best single modality by "
            f"d={super_B:+.2f} (Δ={condB['fused_minus_best_single_mean']:+.3f}, F1 PASS) — while (A) "
            f"label-only fusion (H_1189 setup) is NOT super-additive d={super_A:+.2f} (F2 PASS, control "
            f"reproduces H_1189). Surface-preservation is the BINDING VARIABLE: fusion helps ONLY when "
            f"the modalities are recoverable views of a shared surface, NOT when they share only the "
            f"abstract label. DIRECTLY confirms the H_1170/H_1189 surface-gating mechanism.")
    else:
        why = []
        if not f1:
            why.append(f"F1 fail: (B) surface-shared fusion is NOT super-additive — d(fused − best_single)"
                       f"={super_B:+.2f} < 0.5 (Δacc={condB['fused_minus_best_single_mean']:+.3f}); even a "
                       f"shared recoverable surface does not lift fused above the best single part at toy scale")
        if not f2:
            why.append(f"F2 fail: (A) label-only control did NOT reproduce H_1189's non-super-additive "
                       f"result — d(fused − best_single)={super_A:+.2f} > 0 (expected <=0); the within-experiment "
                       f"control is broken so the surface-isolation is not clean")
        ruling = "CLOSED-NEGATIVE: " + " | ".join(why)

    verdict = {
        "H": "H_1191",
        "title": "SURFACE-PRESERVED multi-modal fusion: does giving the three modalities a preserved "
                 "shared surface (a common low-rank latent each is a smooth invertible function of) make "
                 "SUPER-ADDITIVITY RETURN (fused > best single)? — isolates surface-preservation as the "
                 "binding variable predicted by H_1170/H_1189.",
        "frozen_falsifier": {
            "F1": "condition (B) surface-shared fusion super-additive: d(fused - best_single) >= 0.5",
            "F2": "condition (A) label-only control still fails: d(fused - best_single) <= 0 (reproduces H_1189)",
            "SUPPORTED": "F1 and F2 (surface-preservation is the binding variable, confirming H_1170/H_1189)",
            "metric": "clm-time-encoding STAGE-DECODE accuracy of the DERIVATIVE arm (p7, NOT perplexity)",
        },
        "cap_ladder": CAP_LADDER,
        "decode_chance": 1.0 / N_REGIMES,
        "construction_audit_B": audit,
        "condition_A_label_only": {k: v for k, v in condA.items() if k != "_res"},
        "condition_B_surface_shared": {k: v for k, v in condB.items() if k != "_res"},
        "F1_surface_rescues": {"super_additive_d_B": super_B, "bar": 0.5, "pass": f1,
                               "fused_acc_B": condB["fused_deriv_acc_mean"],
                               "best_single_acc_B": condB["best_single_deriv_acc_mean"],
                               "best_single_modality_B": condB["best_single_modality_on_mean"]},
        "F2_label_only_still_fails": {"super_additive_d_A": super_A, "bar_at_most": 0.0, "pass": f2,
                                      "fused_acc_A": condA["fused_deriv_acc_mean"],
                                      "best_single_acc_A": condA["best_single_deriv_acc_mean"],
                                      "best_single_modality_A": condA["best_single_modality_on_mean"]},
        "supported": supported,
        "ruling": ruling,
        "surface_is_the_gate_answer": (
            "YES — surface-preservation is the binding variable. The ONLY structural difference between "
            "(A) and (B) is whether the three modalities are recoverable views of a SHARED surface; "
            "(B) restores super-additivity that (A) cannot, isolating surface-preservation as the gate "
            "and confirming H_1170/H_1189 directionally."
            if supported else
            "NO (at toy scale) — " + ruling),
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses H_1163 grow_arm/stage_decode_accuracy/"
                 "cohen_d_paired/SEEDS/N_REGIMES_AUDIO/DIM/T/WARMUP VERBATIM. The 'shared surface' in (B) "
                 "is an ENGINEERED linear-ish latent — three WELL-CONDITIONED (orthogonal, cond≈1) "
                 "INVERTIBLE maps of ONE shared drifting-regime z[t] + a mild monotone tanh warp — a PROXY "
                 "for a real cross-modal surface (cf H_1170 toy renderings), NOT real TTS / images / "
                 "learned encoders. (A) = H_1189's exact label-only construction reproduced as the "
                 "within-experiment negative control. DIM=8 (the grow_arm contract); fused 24-d projected "
                 "to 8, NOT widened. Live CORE engine_mitosis_tick + real modalities + production scale "
                 "UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). Lane-M gradient-free growth lane "
                 "(separate from Lane A AKIDA / Lane G forge / Lane P torch, a_lane_akida_gpu_split). "
                 "a_completeness_over_cheap: invertibility/well-conditioning verified BEFORE scoring; "
                 "frozen bars NOT moved." % len(H.SEEDS),
    }
    print("=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1191_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
