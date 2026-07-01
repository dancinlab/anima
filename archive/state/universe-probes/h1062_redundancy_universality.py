"""H_1062 — is the faithful-phi-UP / big-Phi-DOWN sign-split UNIVERSALLY redundancy-driven,
or PLANNING-SPECIFIC? (generality test of H_1039's causal mechanism)

PRE-REG: UNIVERSE/cards/H_1062_redundancy_universality.md.

PRIOR (H_1039 GREEN, REDUNDANCY-CAUSAL): Williams-Beer redundancy CAUSALLY drives the
*planning* Phi sign-split -- de-redundifying (ZCA/Gram-Schmidt) the planning channels
COLLAPSES the split while it HOLDS on the matched control (>=97% Dred cut). That was shown
for PLANNING interventions ONLY. This hypothesis tests GENERALITY: do OTHER, NON-planning
interventions that act on the same toy channel substrate ALSO produce a redundancy-gated
sign-split, and does redundancy rank-predict split magnitude ACROSS interventions?

SUBSTRATE: the GREEDY baseline latent matrix Hg from h1004.planning_trajectories(seed,depth)
(the NON-planning rollout). The planning ladder Hp is reused ONLY for the reproduce-H_1039
check, never as a phi-intervention here. Each NON-planning intervention transforms the
CONTINUOUS top-variance channel matrix (the EXACT channels _top_variance_channels selects)
BEFORE median-binarization; contrast = (intervened reads) - (un-intervened baseline reads),
SAME-seed paired, 30 seeds.

FOUR NON-planning phi-raising interventions on the continuous channel matrix X (T x n_units):
  (i)  ema     -- temporal smoothing / recurrence:  X[t] <- a*X[t] + (1-a)*X[t-1], a=0.5
  (ii) gain    -- logit-temperature / sharpening:   X <- tanh(g*zscore(X)),        g=2.5
  (iii)pool    -- attention-style channel pooling:  X <- (1-b)*X + b*mean_chan(X),  b=0.5
  (iv) lowrank -- low-rank mixing:                  X <- X @ ((1-c)I + c*11^T/k),  c=0.6

For EACH intervention vs its matched baseline, measure on the SAME-seed paired arms:
  (a) sign-split: faithful contrast (UP iff > +SIGN_EPS) vs big-Phi contrast (DOWN iff < -SIGN_EPS);
      SPLIT present iff (faith UP AND big DOWN).
  (b) WB I_min Dred it induces (intervention-VALIDATION variable, NOT a Phi proxy; H_1039 lesson).
  (c) de-redundify (ZCA primary + Gram-Schmidt robustness, H_1039 operators UNMODIFIED) applied
      to the INTERVENED channels -> does the split COLLAPSE (SPLIT->False)?
  cross-intervention: does Dred RANK-PREDICT split magnitude across ALL interventions
      (Spearman rho)? split-magnitude = faith_contrast - big_contrast (signed split size).

ENGINES -- BOTH stdlib IIT-4.0 CPU mirrors (h1004), RE-PROVEN == stdlib at n=4 AND n=5 BEFORE
scoring (h1012.prove_mirrors_at_n; a_phi_iit4_tool, NO proxy). PID = Williams-Beer (2010) I_min,
exact pure-numpy (h1039.pid_system VERBATIM; intervention-validation, NOT a Phi proxy). MI in
BITS (log2; H_1043 nats-bug lesson). IMPORTS by REAL MODULE NAME (no importlib custom-name;
H_1038 fork-unpickle lesson). SERIAL only; NO multiprocessing.Pool. $0 CPU-local, no GPU.

FROZEN thresholds (locked in the pre-reg .md BEFORE scoring; NO goalpost move):
  SIGN_EPS=1e-3; split-def = (faith>+eps AND big<-eps); RED_REDUCTION_THRESHOLD=0.20 (>=80% cut);
  SPEARMAN_BAR=0.7; N_SEEDS=30.
PASS = REDUNDANCY-UNIVERSAL: split in >=2 non-planning interventions AND de-redundify collapses
  each AND cross-intervention Spearman rho >= 0.7.
FAIL = SPLIT-IS-PLANNING-SPECIFIC (closed-negative, a_paper_negative_ok).

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT scored (big-Phi
super-exponential), n=5 mirror-proven; production scale UNVERIFIED. g5 CODE-measured (p7).
"""
import sys, os, math, time, json, itertools
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

pid_system = h1039.pid_system                       # WB I_min PID (intervention-validation)
_top_variance_channels = h1039._top_variance_channels  # EXACT channel selection
_zca_whiten = h1039._zca_whiten                     # de-redundify PRIMARY (UNMODIFIED)
_gram_schmidt = h1039._gram_schmidt                 # de-redundify ROBUSTNESS (UNMODIFIED)
_binarize_median = h1039._binarize_median           # h1004 downstream binarization

N_UNITS = h1039.N_UNITS                  # 4
N_SEEDS = h1039.N_SEEDS                  # 30
PLAN_DEPTH = h1039.PLAN_DEPTH            # 8 (reproduce-H_1039 check only)
SIGN_EPS = h1039.SIGN_EPS                # 1e-3
RED_REDUCTION_THRESHOLD = h1039.RED_REDUCTION_THRESHOLD   # 0.20 (>=80% cut)
SPEARMAN_BAR = 0.7                       # cross-intervention rank-predict bar (FROZEN)

# ═══════════════════════════════════════════════════════════════════════════
# NON-planning phi-raising interventions on the CONTINUOUS channel matrix X (T x k).
# Each returns a transformed (T x k) matrix; binarization happens downstream (h1004 path).
# ═══════════════════════════════════════════════════════════════════════════
EMA_ALPHA = 0.5
GAIN_G = 2.5
POOL_BETA = 0.5
LOWRANK_GAMMA = 0.6

def _iv_ema(X):
    """temporal smoothing / recurrence -- induces temporal redundancy."""
    Y = X.astype(float).copy()
    for t in range(1, Y.shape[0]):
        Y[t] = EMA_ALPHA * Y[t] + (1.0 - EMA_ALPHA) * Y[t - 1]
    return Y

def _iv_gain(X):
    """logit-temperature / sharpening -- per-channel z-score then tanh gain."""
    Xc = X.astype(float)
    mu = Xc.mean(axis=0, keepdims=True)
    sd = Xc.std(axis=0, keepdims=True)
    sd = np.where(sd > 1e-12, sd, 1.0)
    return np.tanh(GAIN_G * (Xc - mu) / sd)

def _iv_pool(X):
    """attention-style channel pooling -- mix each channel toward the channel mean."""
    Xc = X.astype(float)
    chan_mean = Xc.mean(axis=1, keepdims=True)      # (T x 1) row-wise mean over channels
    return (1.0 - POOL_BETA) * Xc + POOL_BETA * chan_mean

def _iv_lowrank(X):
    """low-rank mixing -- shared rank-1 component across channels via M=(1-c)I + c 11^T/k."""
    Xc = X.astype(float)
    k = Xc.shape[1]
    M = (1.0 - LOWRANK_GAMMA) * np.eye(k) + LOWRANK_GAMMA * (np.ones((k, k)) / k)
    return Xc @ M

INTERVENTIONS = {
    "ema":     _iv_ema,
    "gain":    _iv_gain,
    "pool":    _iv_pool,
    "lowrank": _iv_lowrank,
}

# ═══════════════════════════════════════════════════════════════════════════
# substrate read on the CONTINUOUS channel matrix `chans` -> BOTH engines + PID.
# (mirrors h1039.substrate_reads but takes the continuous channels directly so we can
#  apply an intervention and/or a de-redundify operator before median-binarization.)
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

def _channels(H, n):
    return _top_variance_channels(H, n)

def reads_for(H, n, iv=None, dered=None):
    """top-variance channels of H -> optional intervention -> optional de-redundify -> reads."""
    chans = _channels(H, n)
    if iv is not None:
        chans = INTERVENTIONS[iv](chans)
    if dered == "zca":
        chans = _zca_whiten(chans)
    elif dered == "gs":
        chans = _gram_schmidt(chans)
    elif dered is not None:
        raise ValueError(dered)
    return _reads_from_channels(chans, n)

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(A, B, k):
    """contrast = mean(A) - mean(B); paired-by-seed arrays."""
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

# ─────────────────────────────────────────────────────────────────────────────
# Spearman rho (exact pure-numpy; tie-aware average ranks). NOT a Phi proxy.
# ─────────────────────────────────────────────────────────────────────────────
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
        avg = (i + j) / 2.0 + 1.0  # 1-based average rank
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

# ─────────────────────────────────────────────────────────────────────────────
# scoring: one intervention vs baseline (paired by seed), on a chosen dered mode.
# ─────────────────────────────────────────────────────────────────────────────
def score_intervention(iv, n, t0, dered=None):
    base_rows, iv_rows = [], []
    for s in range(N_SEEDS):
        Hg, _Hp = planning_trajectories(s, PLAN_DEPTH)   # GREEDY baseline (non-planning)
        base_rows.append(reads_for(Hg, n, iv=None, dered=dered))
        iv_rows.append(reads_for(Hg, n, iv=iv, dered=dered))
        if (s + 1) % 10 == 0 or s == 0:
            tag = iv if dered is None else f"{iv}+{dered}"
            print(f"    [{tag} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    A = _agg(iv_rows); B = _agg(base_rows)
    return {k: _contrast(A, B, k) for k in ("big", "faith", "red", "syn", "on_frac")}

# ─────────────────────────────────────────────────────────────────────────────
# reproduce-H_1039 check (planning split control + ZCA collapse), via h1039.score_arm.
# ─────────────────────────────────────────────────────────────────────────────
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

def main():
    print("=" * 92)
    print("H_1062 — is the faithful-phi-UP / big-Phi-DOWN sign-split UNIVERSALLY redundancy-driven")
    print("         or PLANNING-SPECIFIC? (generality test of H_1039's causal mechanism)")
    print("substrate=CPU-mirror (numpy) — h1004 engines + h1012 proof, RE-PROVEN == stdlib n=4,5")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min, EXACT pure-numpy (h1039.pid_system VERBATIM;")
    print("      intervention-validation variable, NOT a Phi proxy). a_phi_iit4_tool — no proxy.")
    print("4 NON-planning phi-interventions on the continuous top-variance channels (GREEDY baseline Hg):")
    print(f"  ema(a={EMA_ALPHA}) gain(g={GAIN_G}) pool(b={POOL_BETA}) lowrank(c={LOWRANK_GAMMA})")
    print("de-redundify = ZCA (primary) + Gram-Schmidt (robustness), H_1039 operators UNMODIFIED.")
    print(f"FROZEN: SIGN_EPS={SIGN_EPS}; split=(faith>+eps & big<-eps); redundancy removed iff")
    print(f"  |Dred_dered| <= {RED_REDUCTION_THRESHOLD}*|Dred_intervention| (>=80% cut);")
    print(f"  cross-intervention Spearman rho >= {SPEARMAN_BAR}.")
    print("PASS = REDUNDANCY-UNIVERSAL: split in >=2 non-planning IVs AND de-redundify collapses each")
    print("       AND cross-IV Spearman rho >= 0.7. FAIL = SPLIT-IS-PLANNING-SPECIFIC (a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope | SERIAL CPU $0, no GPU/pod")
    print("=" * 92, flush=True)
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

    # ── STEP 1: reproduce-H_1039 (planning split control + ZCA collapse) BEFORE new IVs ──
    print(f"STEP 1 — reproduce-H_1039 at n={n} EXACT, {N_SEEDS} seeds (confirm harness fidelity)")
    repro = reproduce_h1039(n, t0)
    print()
    if not repro["ok"]:
        print("  WARNING — reproduce-H_1039 did NOT confirm; the new-IV results are still reported")
        print("  but the planning-baseline fidelity is not established. (recorded in JSON)")
        print()

    # ── STEP 2: score the 4 NON-planning interventions (intervention vs baseline) ──
    print(f"STEP 2 — score 4 NON-planning interventions vs baseline at n={n} EXACT, {N_SEEDS} seeds SERIAL")
    iv_results = {}
    for iv in INTERVENTIONS:
        print(f"################ INTERVENTION = {iv} (vs un-intervened baseline) ################", flush=True)
        base = score_intervention(iv, n, t0, dered=None)
        zca = score_intervention(iv, n, t0, dered="zca")
        gs = score_intervention(iv, n, t0, dered="gs")
        fc = base["faith"]["contrast"]; bc = base["big"]["contrast"]; dred = base["red"]["contrast"]
        sp = split_present(fc, bc)
        zfc = zca["faith"]["contrast"]; zbc = zca["big"]["contrast"]
        gfc = gs["faith"]["contrast"]; gbc = gs["big"]["contrast"]
        zsp = split_present(zfc, zbc); gsp = split_present(gfc, gbc)
        red_mag = abs(dred)
        zdr = abs(zca["red"]["contrast"]); gdr = abs(gs["red"]["contrast"])
        red_removed_zca = (zdr <= RED_REDUCTION_THRESHOLD * red_mag) if red_mag > 1e-9 else (zdr < 1e-3)
        red_removed_gs = (gdr <= RED_REDUCTION_THRESHOLD * red_mag) if red_mag > 1e-9 else (gdr < 1e-3)
        cut_zca = (1.0 - zdr / red_mag) * 100 if red_mag > 1e-9 else float("nan")
        cut_gs = (1.0 - gdr / red_mag) * 100 if red_mag > 1e-9 else float("nan")
        # de-redundify collapses iff: split was present, redundancy removed, and split now False
        collapse_zca = (sp and red_removed_zca and (not zsp))
        collapse_gs = (sp and red_removed_gs and (not gsp))
        split_mag = fc - bc          # signed split magnitude (faith UP & big DOWN -> large +)
        iv_results[iv] = dict(
            faith_c=fc, big_c=bc, dred=dred, split=sp, split_mag=split_mag,
            zca_faith=zfc, zca_big=zbc, zca_split=zsp, gs_faith=gfc, gs_big=gbc, gs_split=gsp,
            red_mag=red_mag, cut_zca=cut_zca, cut_gs=cut_gs,
            red_removed_zca=red_removed_zca, red_removed_gs=red_removed_gs,
            collapse_zca=collapse_zca, collapse_gs=collapse_gs,
            faith_d=base["faith"]["d"], big_d=base["big"]["d"], red_d=base["red"]["d"],
            on_frac=base["on_frac"]["a"],
        )
        print(f"   baseline-vs-IV : faith={fc:+.4f}({faith_sign(fc)}) d={base['faith']['d']:+.2f}  "
              f"big-Phi={bc:+.4f}({big_sign(bc)}) d={base['big']['d']:+.2f}  Dred={dred:+.4f} d={base['red']['d']:+.2f}")
        print(f"   SPLIT present (faith-UP & big-DOWN): {sp}   split_mag(faith-big)={split_mag:+.4f}")
        print(f"   ZCA arm : faith={zfc:+.4f}({faith_sign(zfc)}) big={zbc:+.4f}({big_sign(zbc)}) "
              f"SPLIT={zsp}  Dred-cut={cut_zca:5.1f}% removed={red_removed_zca} collapse={collapse_zca}")
        print(f"   GS  arm : faith={gfc:+.4f}({faith_sign(gfc)}) big={gbc:+.4f}({big_sign(gbc)}) "
              f"SPLIT={gsp}  Dred-cut={cut_gs:5.1f}% removed={red_removed_gs} collapse={collapse_gs}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER tables
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 92)
    print("PER-INTERVENTION TABLE (intervention - baseline @ n=4 EXACT, 30 seeds)")
    print("=" * 92)
    print(f"  {'IV':9s} | {'faith Dc':>9s} | {'big Dc':>9s} | {'Dred':>8s} | {'SPLIT':>5s} | "
          f"{'ZCA-collapse':>12s} | {'GS-collapse':>11s} | {'Dred-cut(ZCA)':>13s}")
    for iv, r in iv_results.items():
        print(f"  {iv:9s} | {r['faith_c']:+9.4f} | {r['big_c']:+9.4f} | {r['dred']:+8.4f} | "
              f"{str(r['split']):>5s} | {str(r['collapse_zca']):>12s} | {str(r['collapse_gs']):>11s} | "
              f"{r['cut_zca']:12.1f}%")
    print()

    # cross-intervention: does Dred RANK-PREDICT split magnitude across interventions?
    ivs = list(iv_results.keys())
    dred_vec = np.array([abs(iv_results[i]["dred"]) for i in ivs])
    splitmag_vec = np.array([iv_results[i]["split_mag"] for i in ivs])
    rho = spearman(dred_vec, splitmag_vec)
    print("CROSS-INTERVENTION redundancy -> split-magnitude (Spearman rank; FROZEN bar >= 0.7)")
    for i in ivs:
        print(f"  {i:9s}  |Dred|={abs(iv_results[i]['dred']):.4f}   split_mag(faith-big)={iv_results[i]['split_mag']:+.4f}")
    print(f"  Spearman rho(|Dred|, split_mag) over {len(ivs)} interventions = {rho:+.4f}  (bar {SPEARMAN_BAR})")
    print()

    # ── FALSIFIER ──
    n_split = sum(1 for r in iv_results.values() if r["split"])
    split_ivs = [i for i, r in iv_results.items() if r["split"]]
    # every split-bearing IV must collapse on ZCA (primary), GS consistent for robustness
    all_collapse_zca = all(iv_results[i]["collapse_zca"] for i in split_ivs) if split_ivs else False
    all_collapse_gs = all(iv_results[i]["collapse_gs"] for i in split_ivs) if split_ivs else False
    cond1 = (n_split >= 2)
    cond2 = (len(split_ivs) > 0 and all_collapse_zca and all_collapse_gs)
    cond3 = (not math.isnan(rho)) and (rho >= SPEARMAN_BAR)
    universal = cond1 and cond2 and cond3

    print("=" * 92)
    print("FALSIFIER (FROZEN; NO goalpost move)")
    print(f"  cond1 split in >=2 non-planning IVs:        {cond1}  (n_split={n_split}, split_IVs={split_ivs})")
    print(f"  cond2 de-redundify collapses EACH split IV: {cond2}  (ZCA-all={all_collapse_zca}, GS-all={all_collapse_gs})")
    print(f"  cond3 cross-IV Spearman rho >= {SPEARMAN_BAR}:       {cond3}  (rho={rho:+.4f})")
    print()
    if universal:
        verdict_token = "REDUNDANCY-UNIVERSAL"
        print("OVERALL: REDUNDANCY-UNIVERSAL — the faithful-UP/big-Phi-DOWN sign-split is NOT")
        print("  planning-specific: it appears in >=2 NON-planning interventions, de-redundifying")
        print("  COLLAPSES it in each, AND the WB redundancy-margin rank-predicts split magnitude")
        print("  ACROSS interventions (Spearman >= 0.7). Redundancy is the UNIVERSAL split driver;")
        print("  H_1039's causal mechanism GENERALIZES beyond planning.")
    else:
        verdict_token = "SPLIT-IS-PLANNING-SPECIFIC"
        print("OVERALL: SPLIT-IS-PLANNING-SPECIFIC (CLOSED-NEGATIVE, a_paper_negative_ok) — at least")
        print("  one falsifier condition FAILED: the redundancy-gated faithful-UP/big-Phi-DOWN split")
        print("  does NOT universally arise from non-planning phi-raising interventions on this")
        print("  substrate (split absent in <2 IVs, OR de-redundify does not collapse it, OR the")
        print("  redundancy-margin does not rank-predict split across interventions). H_1039's")
        print("  redundancy-causal claim is BOUNDED to planning — the split is planning-specific.")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 92)
    print(f"reproduce-H_1039 confirmed: {repro['ok']}  (control split held + ZCA collapse + Dred>=80% cut)")
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT (both engines exact;")
    print("big-Phi super-exponential -> n=4 rung for the full SET x 30 seeds; n=5 mirror-proven). BOTH")
    print("CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring")
    print("(a_phi_iit4_tool; NO proxy). H_1039 de-redundify operators (ZCA/GS) reused UNMODIFIED; the")
    print("PID is the intervention-validation variable (NOT a Phi proxy). SERIAL CPU $0, no GPU/pod.")
    print("Production scale UNVERIFIED. g5 (p7).")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH),
        sign_eps=SIGN_EPS, red_reduction_threshold=RED_REDUCTION_THRESHOLD,
        spearman_bar=SPEARMAN_BAR,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        interventions={k: dict(alpha=EMA_ALPHA, g=GAIN_G, beta=POOL_BETA, gamma=LOWRANK_GAMMA)
                       for k in INTERVENTIONS},
        reproduce_h1039=repro,
        iv_results={i: {k: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v))
                        for k, v in iv_results[i].items()} for i in iv_results},
        n_split=int(n_split), split_ivs=split_ivs,
        all_collapse_zca=bool(all_collapse_zca), all_collapse_gs=bool(all_collapse_gs),
        cross_iv_spearman=float(rho),
        cond1=bool(cond1), cond2=bool(cond2), cond3=bool(cond3),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1062_redundancy_universality_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
