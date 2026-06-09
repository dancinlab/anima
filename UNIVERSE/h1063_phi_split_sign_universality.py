"""H_1063 — phi-split-sign-universality: is the faithful-phi-UP / big-Phi-DOWN sign SPLIT
a UNIVERSAL measure-theoretic property of within-block correlation, removability-INDEPENDENT?
(synthesis resolving the H_1062 puzzle: WHY does the split DIRECTION generalize when the
cleanly-removable-redundancy MECHANISM (H_1039) does not?)

PRE-REG: UNIVERSE/H_1063_phi_split_sign_universality.md.

PRIORS:
  H_1039 (REDUNDANCY-CAUSAL): WB redundancy CAUSALLY drives the *planning* Phi sign-split;
    de-redundify (ZCA/GS) collapses it on planning (control faith +2.33 / big -4.01).
  H_1062 (SPLIT-IS-PLANNING-SPECIFIC): the CAUSAL mechanism (clean ZCA-removable redundancy)
    is planning-specific; de-redundify collapses the split ONLY for planning. YET the split
    DIRECTION still rank-generalized across non-planning interventions (cross-IV Spearman +0.80).

SYNTHESIS HYPOTHESIS: the SIGN of the split is a UNIVERSAL measure-theoretic property —
  faithful phi_EI and big-Phi have OPPOSITE monotone responses to ANY increase in within-block
  correlation, independent of whether that correlation forms a surgically-removable block. Only
  the MAGNITUDE/causality (clean ZCA-removable redundancy) is substrate-specific. Unifies
  H_1039 (causal, planning) + H_1062 (direction generalizes).

DESIGN (parametric — decouple SIGN from removability): a GRADED within-block correlation
  sweep on the EXACT H_1039/H_1062 channel substrate (_top_variance_channels(H_greedy,4),
  40x4 continuous, GREEDY baseline). A single tunable knob rho_corr in {0.0..0.9} step 0.1
  raises within-block channel correlation in a CONTROLLED way via SHARED-LATENT / Gaussian-copula
  mixing (NOT a planning intervention, NOT a clean block):
      Xz   = zscore(X)                          # per-channel z-score (T x k)
      z    = mean over channels of Xz           # diffuse common-mode shared latent (T,)
      Xr_j = sqrt(1-rho)*Xz_j + sqrt(rho)*z      # convex-in-variance loading
      Xr_j <- Xr_j*sigma_orig_j + mu_orig_j      # restore per-channel scale (signal preserved)
  The induced redundancy is DIFFUSE (rank-1 shared common mode spread across all channels) — it
  need NOT be cleanly ZCA-removable, which is the removability-resistant regime under test.

TESTS:
  (a) opposite-monotone SIGN over the FULL sweep: faithful rises monotone (Spearman >= +0.9) while
      big-Phi falls monotone (Spearman <= -0.9), opposite signs.
  (b) removability-resistant check: does the high-rho faith-UP/big-DOWN SIGN SURVIVE ZCA
      de-redundify (ZCA does NOT collapse the sign even though it cuts the diffuse redundancy)?
  (c) saturation/reversal bound: per-step monotone direction table for both measures.

ENGINES — BOTH stdlib IIT-4.0 CPU mirrors (h1004), RE-PROVEN == stdlib at n=4 AND n=5 BEFORE
scoring (h1012.prove_mirrors_at_n; a_phi_iit4_tool, NO proxy). PID = Williams-Beer (2010) I_min,
exact pure-numpy (h1039.pid_system VERBATIM; validation variable, NOT a Phi proxy). MI in BITS
(log2; H_1043 nats-bug lesson). IMPORTS by REAL MODULE NAME. SERIAL only; NO multiprocessing.Pool.
$0 CPU-local, no GPU.

FROZEN thresholds (locked in pre-reg .md BEFORE scoring; NO goalpost move):
  SIGN_EPS=1e-3; MONO_BAR=0.9 (Spearman |rho| over sweep); N_SEEDS=30; rho grid {0.0..0.9} step 0.1;
  RED_REDUCTION_THRESHOLD=0.20 (>=80% cut, labels removability of induced redundancy at high rho).
PASS = H1-SIGN-UNIVERSAL: faith Spearman(rho_corr) >= +0.9 AND big Spearman(rho_corr) <= -0.9
  (opposite, both |rho_s|>=0.9) AND the high-rho faith-UP/big-DOWN SIGN SURVIVES ZCA de-redundify.
FAIL = SIGN-NOT-CLEAN-UNIVERSAL (closed-negative, a_paper_negative_ok).

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT scored (big-Phi super-
exponential), n=5 mirror-proven; production scale UNVERIFIED. g5 CODE-measured (p7).
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# Import the prior chain by REAL MODULE NAMES (no importlib custom-name).
import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402
import h1039_redundancy_causal as h1039              # noqa: E402

# REUSE H_1039 machinery UNMODIFIED -----------------------------------------------------------
big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
cohens_d = h1004.cohens_d
welch_t = h1004.welch_t
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

pid_system = h1039.pid_system                       # WB I_min PID (validation variable)
_top_variance_channels = h1039._top_variance_channels  # EXACT channel selection
_zca_whiten = h1039._zca_whiten                     # de-redundify PRIMARY (UNMODIFIED)
_binarize_median = h1039._binarize_median           # h1004 downstream binarization

N_UNITS = h1039.N_UNITS                  # 4
N_SEEDS = h1039.N_SEEDS                  # 30
PLAN_DEPTH = h1039.PLAN_DEPTH            # 8 (reproduce-H_1039 check only)
SIGN_EPS = h1039.SIGN_EPS                # 1e-3
RED_REDUCTION_THRESHOLD = h1039.RED_REDUCTION_THRESHOLD   # 0.20 (>=80% cut)

# FROZEN (pre-reg .md) ------------------------------------------------------------------------
MONO_BAR = 0.9                                       # Spearman |rho| over the sweep
RHO_GRID = [round(0.1 * i, 1) for i in range(10)]    # {0.0, 0.1, ..., 0.9}

# ═══════════════════════════════════════════════════════════════════════════
# GRADED within-block correlation knob: shared-latent / Gaussian-copula mixing.
# rho_corr in [0,1) raises pairwise within-block channel correlation monotonically.
# DIFFUSE common-mode (rank-1 over ALL channels) — NOT a clean removable block.
# Per-channel signal magnitude preserved (restore original mean+std).
# ═══════════════════════════════════════════════════════════════════════════
def correlate_channels(X, rho):
    """Raise within-block channel correlation to level rho via a shared common-mode latent.
       rho=0 returns X unchanged (identity baseline)."""
    X = np.asarray(X, float)
    mu = X.mean(axis=0, keepdims=True)
    sd = X.std(axis=0, keepdims=True)
    sd_safe = np.where(sd > 1e-12, sd, 1.0)
    Xz = (X - mu) / sd_safe                          # per-channel z-score (T x k)
    z = Xz.mean(axis=1, keepdims=True)               # diffuse common-mode shared latent (T x 1)
    # convex-in-variance loading: var-preserving when channels were unit-variance & z unit-var.
    Xr = math.sqrt(1.0 - rho) * Xz + math.sqrt(rho) * z
    # restore the ORIGINAL per-channel scale so per-channel signal magnitude is preserved
    return Xr * sd_safe + mu

# ═══════════════════════════════════════════════════════════════════════════
# substrate read on the CONTINUOUS channel matrix `chans` -> BOTH engines + PID.
# (mirrors h1039.substrate_reads but on continuous channels so we can apply the
#  correlation knob and/or ZCA de-redundify before median-binarization.)
# ═══════════════════════════════════════════════════════════════════════════
def _reads_from_channels(chans, n):
    bits = _binarize_median(chans)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    p = pid_system(bits)
    return dict(big=bphi, faith=fphi, red=p["red_total"], syn=p["syn_total"],
                on_frac=float(bits.mean()))

def reads_for(H, n, rho=0.0, dered=None):
    """top-variance channels of H -> correlation knob @ rho -> optional ZCA de-redundify -> reads."""
    chans = _top_variance_channels(H, n)
    if rho > 0.0:
        chans = correlate_channels(chans, rho)
    if dered == "zca":
        chans = _zca_whiten(chans)
    elif dered is not None:
        raise ValueError(dered)
    return _reads_from_channels(chans, n)

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(A, B, k):
    c = A[k].mean() - B[k].mean()
    try:
        d = cohens_d(A[k], B[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(A[k], B[k])
    except Exception:
        p = float("nan")
    return dict(contrast=float(c), d=float(d), p=float(p),
                a=float(A[k].mean()), b=float(B[k].mean()))

def faith_sign(c):
    return "UP" if c > SIGN_EPS else ("DOWN" if c < -SIGN_EPS else "NULL")

def big_sign(c):
    return "DOWN" if c < -SIGN_EPS else ("UP" if c > SIGN_EPS else "NULL")

def split_present(faith_c, big_c):
    return (faith_sign(faith_c) == "UP") and (big_sign(big_c) == "DOWN")

# ─── Spearman rho (exact pure-numpy; tie-aware average ranks) — h1062 VERBATIM ───
def _rankdata(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks

def spearman(x, y):
    rx = _rankdata(x); ry = _rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    denom = math.sqrt((rx @ rx) * (ry @ ry))
    if denom < 1e-12:
        return float("nan")
    return float((rx @ ry) / denom)

# ─── mean within-block channel correlation (knob-validation; NOT a Phi proxy) ───
def _mean_offdiag_corr(X):
    X = np.asarray(X, float)
    C = np.corrcoef(X, rowvar=False)
    C = np.atleast_2d(C)
    k = C.shape[0]
    off = C[~np.eye(k, dtype=bool)]
    return float(np.nanmean(np.abs(off)))

# ─── reproduce-H_1039 check (planning split control + ZCA collapse), via h1039.score_arm ───
def reproduce_h1039(n, t0):
    print("REPRODUCE-H_1039 — planning(depth-8) vs GREEDY split control + ZCA collapse")
    ctrl = h1039.score_arm("control", n, t0)
    zca = h1039.score_arm("dered_zca", n, t0)
    cfc = ctrl["faith"]["contrast"]; cbc = ctrl["big"]["contrast"]
    zfc = zca["faith"]["contrast"]; zbc = zca["big"]["contrast"]
    ctrl_split = split_present(cfc, cbc)
    zca_split = split_present(zfc, zbc)
    cdr = abs(ctrl["red"]["contrast"]); zdr = abs(zca["red"]["contrast"])
    red_removed = (zdr <= RED_REDUCTION_THRESHOLD * cdr) if cdr > 1e-9 else (zdr < 1e-3)
    cut = (1.0 - zdr / cdr) * 100 if cdr > 1e-9 else float("nan")
    print(f"  control:    faith={cfc:+.4f}({faith_sign(cfc)}) big={cbc:+.4f}({big_sign(cbc)}) "
          f"Dred={ctrl['red']['contrast']:+.4f}  SPLIT={ctrl_split}")
    print(f"  dered_zca:  faith={zfc:+.4f}({faith_sign(zfc)}) big={zbc:+.4f}({big_sign(zbc)}) "
          f"Dred={zca['red']['contrast']:+.4f}  SPLIT={zca_split}")
    print(f"  Dred cut by ZCA = {cut:5.1f}%  (>=80% removed = {red_removed})")
    ok = ctrl_split and (not zca_split) and red_removed
    print(f"  reproduce-H_1039 confirmed (control split HELD + ZCA collapsed + Dred removed): {ok}")
    print(f"  [ref H_1039: control faith +2.33-region / big-Phi ~ -4.01; ZCA collapses split]")
    return dict(ok=bool(ok), ctrl_faith=cfc, ctrl_big=cbc, ctrl_split=bool(ctrl_split),
                zca_faith=zfc, zca_big=zbc, zca_split=bool(zca_split),
                red_cut_pct=float(cut), red_removed=bool(red_removed))

# ─── score one rho_corr level: correlated arm vs rho=0 baseline (paired by seed), dered mode ───
def score_rho(rho, n, t0, dered=None):
    base_rows, cor_rows = [], []
    for s in range(N_SEEDS):
        Hg, _Hp = planning_trajectories(s, PLAN_DEPTH)   # GREEDY baseline (non-planning)
        base_rows.append(reads_for(Hg, n, rho=0.0, dered=dered))
        cor_rows.append(reads_for(Hg, n, rho=rho, dered=dered))
    A = _agg(cor_rows); B = _agg(base_rows)
    out = {k: _contrast(A, B, k) for k in ("big", "faith", "red", "syn", "on_frac")}
    # knob-validation: mean within-block |corr| of the correlated channels (seed-0 representative)
    Hg0, _ = planning_trajectories(0, PLAN_DEPTH)
    ch0 = _top_variance_channels(Hg0, n)
    ch0c = correlate_channels(ch0, rho) if rho > 0 else ch0
    out["_meancorr"] = _mean_offdiag_corr(ch0c)
    return out

def main():
    print("=" * 96)
    print("H_1063 — phi-split-sign-universality: is the faithful-UP / big-Phi-DOWN SIGN-split a")
    print("         UNIVERSAL measure-property of within-block correlation, removability-INDEPENDENT?")
    print("         (synthesis resolving the H_1062 puzzle: direction generalizes, mechanism does not)")
    print("substrate=CPU-mirror (numpy) — h1004 engines + h1012 proof, RE-PROVEN == stdlib n=4,5")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min, EXACT pure-numpy (h1039.pid_system VERBATIM;")
    print("      knob/removability-validation variable, NOT a Phi proxy). a_phi_iit4_tool — no proxy.")
    print("KNOB: graded within-block correlation rho_corr via shared-latent (diffuse common-mode)")
    print(f"  mixing on the EXACT top-variance channels (GREEDY baseline Hg); rho grid = {RHO_GRID}")
    print("de-redundify = ZCA (H_1039 operator UNMODIFIED) — removability-resistant check at high rho.")
    print(f"FROZEN: SIGN_EPS={SIGN_EPS}; MONO_BAR={MONO_BAR} (Spearman |rho| over sweep); N_SEEDS={N_SEEDS};")
    print(f"  RED_REDUCTION_THRESHOLD={RED_REDUCTION_THRESHOLD} (>=80% cut labels removability).")
    print("PASS = SIGN-UNIVERSAL: faith Spearman(rho)>=+0.9 AND big Spearman(rho)<=-0.9 (opposite,")
    print("  both |rho_s|>=0.9) AND high-rho faith-UP/big-DOWN SIGN SURVIVES ZCA de-redundify.")
    print("FAIL = SIGN-NOT-CLEAN-UNIVERSAL (closed-negative, a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope | SERIAL CPU $0, no GPU/pod")
    print("=" * 96, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5")
    print("         BEFORE scoring (h1012.prove_mirrors_at_n discipline; LIVE stdlib refs):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    n = N_UNITS
    t0 = time.time()

    # ── STEP 1: reproduce-H_1039 (planning split control + ZCA collapse) BEFORE the sweep ──
    print(f"STEP 1 — reproduce-H_1039 at n={n} EXACT, {N_SEEDS} seeds (confirm harness fidelity)")
    repro = reproduce_h1039(n, t0)
    print()
    if not repro["ok"]:
        print("  WARNING — reproduce-H_1039 did NOT confirm; sweep results are still reported")
        print("  but the planning-baseline fidelity is not established. (recorded in JSON)")
        print()

    # ── STEP 2: GRADED rho_corr sweep (correlated arm vs rho=0 baseline), CONTROL (no dered) ──
    print(f"STEP 2 — GRADED rho_corr sweep at n={n} EXACT, {N_SEEDS} seeds SERIAL (CONTROL, no dered)")
    sweep = {}
    for rho in RHO_GRID:
        r = score_rho(rho, n, t0, dered=None)
        fc = r["faith"]["contrast"]; bc = r["big"]["contrast"]; dr = r["red"]["contrast"]
        sweep[rho] = dict(faith=fc, big=bc, red=dr, syn=r["syn"]["contrast"],
                          on_frac=r["on_frac"]["a"], meancorr=r["_meancorr"],
                          faith_d=r["faith"]["d"], big_d=r["big"]["d"], split=split_present(fc, bc))
        print(f"  rho={rho:.1f}  meancorr={r['_meancorr']:.3f} | "
              f"faith={fc:+.4f}({faith_sign(fc)}) d={r['faith']['d']:+.2f} | "
              f"big-Phi={bc:+.4f}({big_sign(bc)}) d={r['big']['d']:+.2f} | "
              f"Dred={dr:+.4f} | SPLIT={split_present(fc,bc)}", flush=True)
    print()

    # ── STEP 3: removability-resistant check — ZCA-deredundified sweep arm ──
    print(f"STEP 3 — removability-resistant check: ZCA de-redundify on the correlated channels")
    print("         (does the high-rho faith-UP/big-DOWN SIGN SURVIVE ZCA? sign indep of removability?)")
    sweep_zca = {}
    for rho in RHO_GRID:
        r = score_rho(rho, n, t0, dered="zca")
        fc = r["faith"]["contrast"]; bc = r["big"]["contrast"]; dr = r["red"]["contrast"]
        sweep_zca[rho] = dict(faith=fc, big=bc, red=dr, split=split_present(fc, bc))
        print(f"  rho={rho:.1f} ZCA | faith={fc:+.4f}({faith_sign(fc)}) | "
              f"big-Phi={bc:+.4f}({big_sign(bc)}) | Dred={dr:+.4f} | SPLIT={split_present(fc,bc)}", flush=True)
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER tables
    # ═══════════════════════════════════════════════════════════════════════
    rho_arr = np.array(RHO_GRID, float)
    faith_arr = np.array([sweep[r]["faith"] for r in RHO_GRID], float)
    big_arr = np.array([sweep[r]["big"] for r in RHO_GRID], float)
    corr_arr = np.array([sweep[r]["meancorr"] for r in RHO_GRID], float)
    red_arr = np.array([sweep[r]["red"] for r in RHO_GRID], float)

    print("=" * 96)
    print("SWEEP TABLE — (faithful, big-Phi) contrast vs rho_corr @ n=4 EXACT, 30 seeds (CONTROL arm)")
    print("=" * 96)
    print(f"  {'rho':>4s} | {'meancorr':>8s} | {'faith Dc':>9s} | {'big Dc':>9s} | "
          f"{'Dred':>8s} | {'SPLIT':>5s} | {'faith_sign':>10s} | {'big_sign':>8s}")
    for rho in RHO_GRID:
        s = sweep[rho]
        print(f"  {rho:4.1f} | {s['meancorr']:8.3f} | {s['faith']:+9.4f} | {s['big']:+9.4f} | "
              f"{s['red']:+8.4f} | {str(s['split']):>5s} | {faith_sign(s['faith']):>10s} | "
              f"{big_sign(s['big']):>8s}")
    print()

    # (a) opposite-monotone Spearman over the FULL sweep
    faith_spear = spearman(rho_arr, faith_arr)
    big_spear = spearman(rho_arr, big_arr)
    corr_spear = spearman(rho_arr, corr_arr)
    print("MONOTONE Spearman over the rho_corr sweep (FROZEN bar |rho_s| >= 0.9, opposite signs):")
    print(f"  knob-validation : Spearman(rho_corr, mean within-block |corr|) = {corr_spear:+.4f}  "
          f"(monotone-up knob check)")
    print(f"  faithful phi_EI : Spearman(rho_corr, faith_contrast) = {faith_spear:+.4f}  "
          f"(want >= +{MONO_BAR})")
    print(f"  big-Phi         : Spearman(rho_corr, big_contrast)   = {big_spear:+.4f}  "
          f"(want <= -{MONO_BAR})")
    print()

    # (c) saturation/reversal bound — per-step direction
    print("PER-STEP direction (saturation/reversal bound) — d(measure)/d(rho) sign per step:")
    print(f"  {'rho step':>11s} | {'d_faith':>9s} | {'dir':>5s} | {'d_big':>9s} | {'dir':>5s}")
    faith_steps_up = 0; big_steps_dn = 0; nsteps = len(RHO_GRID) - 1
    for i in range(nsteps):
        df = faith_arr[i + 1] - faith_arr[i]
        db = big_arr[i + 1] - big_arr[i]
        fdir = "UP" if df > 0 else ("DOWN" if df < 0 else "FLAT")
        bdir = "UP" if db > 0 else ("DOWN" if db < 0 else "FLAT")
        if df > 0: faith_steps_up += 1
        if db < 0: big_steps_dn += 1
        print(f"  {RHO_GRID[i]:.1f}->{RHO_GRID[i+1]:.1f} | {df:+9.4f} | {fdir:>5s} | "
              f"{db:+9.4f} | {bdir:>5s}")
    print(f"  faith steps increasing: {faith_steps_up}/{nsteps}   "
          f"big-Phi steps decreasing: {big_steps_dn}/{nsteps}")
    print()

    # (b) removability-resistant check at the highest rho
    rho_hi = RHO_GRID[-1]
    ctl_hi = sweep[rho_hi]; zca_hi = sweep_zca[rho_hi]
    ctl_split_hi = ctl_hi["split"]
    zca_split_hi = zca_hi["split"]
    red_ctl_hi = abs(ctl_hi["red"]); red_zca_hi = abs(zca_hi["red"])
    red_removed_hi = (red_zca_hi <= RED_REDUCTION_THRESHOLD * red_ctl_hi) if red_ctl_hi > 1e-9 else (red_zca_hi < 1e-3)
    cut_hi = (1.0 - red_zca_hi / red_ctl_hi) * 100 if red_ctl_hi > 1e-9 else float("nan")
    # SIGN survives ZCA iff the split SIGN is still present after de-redundify
    sign_survives_zca = zca_split_hi
    print("REMOVABILITY-RESISTANT check at highest rho (sign INDEPENDENT of removability?):")
    print(f"  rho={rho_hi:.1f} CONTROL : faith={ctl_hi['faith']:+.4f}({faith_sign(ctl_hi['faith'])}) "
          f"big={ctl_hi['big']:+.4f}({big_sign(ctl_hi['big'])}) SPLIT={ctl_split_hi} Dred={ctl_hi['red']:+.4f}")
    print(f"  rho={rho_hi:.1f} ZCA     : faith={zca_hi['faith']:+.4f}({faith_sign(zca_hi['faith'])}) "
          f"big={zca_hi['big']:+.4f}({big_sign(zca_hi['big'])}) SPLIT={zca_split_hi} Dred={zca_hi['red']:+.4f}")
    print(f"  ZCA Dred cut at high rho = {cut_hi:5.1f}% (>=80% removed = {red_removed_hi}); "
          f"redundancy diffuse/non-removable iff cut < 80%")
    print(f"  SIGN survives ZCA (faith-UP/big-DOWN split STILL present after de-redundify): {sign_survives_zca}")
    print()

    # ── FALSIFIER ──
    cond_faith = (not math.isnan(faith_spear)) and (faith_spear >= MONO_BAR)
    cond_big = (not math.isnan(big_spear)) and (big_spear <= -MONO_BAR)
    cond_opposite = cond_faith and cond_big
    cond_resistant = bool(sign_survives_zca)
    universal = cond_opposite and cond_resistant

    print("=" * 96)
    print("FALSIFIER (FROZEN; NO goalpost move)")
    print(f"  cond_faith  faithful Spearman >= +{MONO_BAR}:        {cond_faith}  (rho_s={faith_spear:+.4f})")
    print(f"  cond_big    big-Phi  Spearman <= -{MONO_BAR}:        {cond_big}  (rho_s={big_spear:+.4f})")
    print(f"  cond_opposite (both, opposite signs):        {cond_opposite}")
    print(f"  cond_resistant high-rho SIGN survives ZCA:   {cond_resistant}  (zca_split@rho={rho_hi:.1f}={zca_split_hi})")
    print()
    if universal:
        verdict_token = "SIGN-UNIVERSAL"
        print("OVERALL: SIGN-UNIVERSAL — the faithful-UP/big-Phi-DOWN sign-split is a UNIVERSAL")
        print("  measure-property of within-block correlation: faithful phi_EI rises monotone AND")
        print("  big-Phi falls monotone in rho_corr (opposite signs, |Spearman|>=0.9), AND the SIGN")
        print("  SURVIVES ZCA de-redundify at high rho (holds even where the redundancy is diffuse /")
        print("  not cleanly removable). The split SIGN is removability-INDEPENDENT — unifying")
        print("  H_1039 (causal MAGNITUDE, planning) with H_1062 (direction generalizes): the two")
        print("  measures simply respond with OPPOSITE monotonicity to ANY within-block correlation.")
    else:
        verdict_token = "SIGN-NOT-CLEAN-UNIVERSAL"
        print("OVERALL: SIGN-NOT-CLEAN-UNIVERSAL (CLOSED-NEGATIVE, a_paper_negative_ok) — at least one")
        print("  falsifier condition FAILED: the faithful-UP/big-Phi-DOWN opposite-monotone response")
        print("  is NOT a clean universal measure-property over the graded within-block correlation")
        print("  sweep (same-sign / non-monotone / |Spearman|<0.9 for a measure, OR the high-rho sign")
        print("  does NOT survive ZCA de-redundify). The unification is BOUNDED accordingly.")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 96)
    print(f"reproduce-H_1039 confirmed: {repro['ok']}  (control split held + ZCA collapse + Dred>=80% cut)")
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT (both engines exact;")
    print("big-Phi super-exponential -> n=4 rung for the full sweep x 30 seeds; n=5 mirror-proven). BOTH")
    print("CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring")
    print("(a_phi_iit4_tool; NO proxy). H_1039 ZCA de-redundify operator reused UNMODIFIED; the WB PID")
    print("is the knob/removability-validation variable (NOT a Phi proxy). SERIAL CPU $0, no GPU/pod.")
    print("Production scale UNVERIFIED. g5 (p7).")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH),
        sign_eps=SIGN_EPS, mono_bar=MONO_BAR, rho_grid=RHO_GRID,
        red_reduction_threshold=RED_REDUCTION_THRESHOLD,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        reproduce_h1039=repro,
        sweep={str(r): {k: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v))
                        for k, v in sweep[r].items()} for r in RHO_GRID},
        sweep_zca={str(r): {k: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v))
                            for k, v in sweep_zca[r].items()} for r in RHO_GRID},
        faith_spearman=float(faith_spear), big_spearman=float(big_spear),
        corr_spearman=float(corr_spear),
        faith_steps_up=int(faith_steps_up), big_steps_dn=int(big_steps_dn), nsteps=int(nsteps),
        high_rho=float(rho_hi), high_rho_control_split=bool(ctl_split_hi),
        high_rho_zca_split=bool(zca_split_hi), high_rho_red_cut_pct=float(cut_hi),
        high_rho_red_removed=bool(red_removed_hi), sign_survives_zca=bool(sign_survives_zca),
        cond_faith=bool(cond_faith), cond_big=bool(cond_big),
        cond_opposite=bool(cond_opposite), cond_resistant=bool(cond_resistant),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1063_phi_split_sign_universality_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
