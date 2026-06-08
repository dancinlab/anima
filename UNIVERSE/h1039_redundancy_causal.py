"""H_1039 — is the planning Phi sign-split CAUSED by redundancy? (CAUSAL ablation test)

PRE-REG: UNIVERSE/H_1039_redundancy_causal.md (merged #1939).

PRIOR (H_1017 GREEN): planning's mutual-information rise is REDUNDANCY-DOMINATED
(Williams-Beer I_min PID: Δredundancy >> Δsynergy). That is a CORRELATIONAL mechanism.
This hypothesis tests it CAUSALLY: if the redundancy AMONG the planning channels is the
cause of the faithful_phi-UP / big-Phi-DOWN sign-split (the scalar EI credits redundant
copies as integration-up while big-Phi sees them as reducible-down), then surgically
REMOVING that redundancy should COLLAPSE the split.

INTERVENTION (de-redundification operator)
------------------------------------------
Operate on the CONTINUOUS top-variance channel matrix `chans` (n_steps x n_units) — the
EXACT channels h1004.latent_to_binary_seq selects and medians — BEFORE binarization:
  - ZCA-whiten the channels: X_w = (X - mu) @ W,  W = V diag(1/sqrt(lam+eps)) V^T  (symmetric,
    keeps each channel maximally aligned to its un-whitened self -> preserves per-channel
    signal/variance while DECORRELATING the channels -> Williams-Beer cross-channel redundancy
    among the binarized units is driven toward 0).
  - Gram-Schmidt orthogonalization is the ROBUSTNESS operator (same goal, different basis).
Then binarize the de-redundified channels at their own median (identical downstream path).
The CONTROL is the un-orthogonalized standard binarization (h1004 verbatim).

WHAT IS MEASURED (the SAME quantities as H_1017, both arms)
-----------------------------------------------------------
On each arm (CONTROL = standard / DERED = whitened), score the planning(depth-ladder) vs
GREEDY contrast for BOTH stdlib mirrors + the WB PID Δredundancy:
  faith_sign = UP   iff faithful_phi contrast > +SIGN_EPS
  big_sign   = DOWN iff big-Phi      contrast < -SIGN_EPS
  SPLIT present iff (faith_sign==UP AND big_sign==DOWN).

PRE-REGISTERED FALSIFIER (frozen thresholds; TEXT tokens only)
--------------------------------------------------------------
SIGN_EPS = 1e-3 (the pre-reg sign-eps).
RED_REDUCTION_THRESHOLD: de-redundification must cut the planning Δredundancy magnitude by
  >= 80% vs control (|Δred_dered| <= 0.20 * |Δred_control|) -> "redundancy removed". This is
  the stated delta-red-reduction threshold (the operator must actually de-redundify; if it
  does not, the test is INCONCLUSIVE, not a pass/fail of the causal claim).
- H1 PASS = REDUNDANCY-CAUSAL: the de-redundification removes the redundancy (threshold met)
  AND the split COLLAPSES on the de-redundified substrate (SPLIT False) WHILE it HOLDS on the
  matched control (SPLIT True). Redundancy is the CAUSAL driver of the split (confirms the
  H_1017 mechanism causally). Robustness: must hold for the primary (ZCA) operator AND be
  consistent under the Gram-Schmidt robustness operator.
- H1 FAIL = REDUNDANCY-CORRELATED-NOT-CAUSAL: the split SURVIVES de-redundification (SPLIT
  still True on the de-redundified arm despite the redundancy being removed) -> redundancy is
  correlated-but-not-causal; the split has another driver (publishable closed-negative,
  a_paper_negative_ok).

ENGINES — BOTH stdlib IIT-4.0 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring
(h1012.prove_mirrors_at_n; a_phi_iit4_tool — real engines, NO proxy). PID = Williams-Beer
(2010) I_min redundancy lattice, EXACT pure-numpy on the SAME bits (the EXPLANATORY/
intervention-validation variable — NOT a Phi proxy; Phi from the stdlib mirrors only).

IMPORTS by REAL MODULE NAME (h1004_bigphi_faithful_clean, h1012_bigphi_faithful_larger_n) —
NO importlib custom-name (forked-worker/unpickle safety; H_1038 hang lesson). SERIAL only;
NO multiprocessing.Pool. $0 CPU-local, no GPU.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=6 (scored at n=4 EXACT for
the full SET x seeds, n=5 mirror-proven). ZCA is the PRIMARY de-redundification operator;
Gram-Schmidt is the robustness operator; PCA-drop/channel-ablation are follow-ups. Production
scale UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7). NOT a forge binary.
"""
import sys, os, math, time, json, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# Import the prior chain by REAL MODULE NAMES (no importlib custom-name).
import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
cohens_d = h1004.cohens_d
welch_t = h1004.welch_t
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

LOG2 = math.log(2.0)
N_UNITS = 4              # big-Phi binding constraint (EXACT for both engines)
N_SEEDS = 30
PLAN_DEPTH = 8
SIGN_EPS = 1e-3                       # pre-reg sign-eps
RED_REDUCTION_THRESHOLD = 0.20        # |Δred_dered| <= 0.20*|Δred_control| => redundancy removed (>=80% cut)
ZCA_EPS = 1e-8

# ═══════════════════════════════════════════════════════════════════════════
# WILLIAMS-BEER I_min PID — exact pure-numpy on the SAME binary unit-traces
# (VERBATIM the H_1017 harness; the intervention-validation variable, NOT a Phi proxy).
# ═══════════════════════════════════════════════════════════════════════════
def _mi_discrete(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    vx = np.unique(x); vy = np.unique(y)
    if len(vx) <= 1 or len(vy) <= 1:
        return 0.0
    mi = 0.0
    for a in vx:
        pa = np.mean(x == a)
        for b in vy:
            pb = np.mean(y == b)
            pab = np.mean((x == a) & (y == b))
            if pab > 0.0:
                mi += pab * (math.log(pab / (pa * pb)) / LOG2)
    return mi if mi > 0.0 else 0.0

def _specific_info(t_val, T, S):
    mask_t = (T == t_val)
    pt = np.mean(mask_t)
    if pt <= 0.0:
        return 0.0
    vs = np.unique(S)
    info = 0.0
    for s in vs:
        ps = np.mean(S == s)
        ps_given_t = np.mean(S[mask_t] == s)
        if ps_given_t > 0.0 and ps > 0.0:
            info += ps_given_t * (math.log(ps_given_t / ps) / LOG2)
    return info

def _pid_two_source(T, S1, S2):
    vT = np.unique(T)
    red = 0.0
    for t in vT:
        pt = np.mean(T == t)
        i1 = _specific_info(t, T, S1)
        i2 = _specific_info(t, T, S2)
        red += pt * min(i1, i2)
    if red < 0.0:
        red = 0.0
    mi1 = _mi_discrete(T, S1)
    mi2 = _mi_discrete(T, S2)
    Sj = (S1.astype(np.int64) << 1) | S2.astype(np.int64) if (
        set(np.unique(S1)) <= {0, 1} and set(np.unique(S2)) <= {0, 1}) else (
        S1.astype(np.int64) * (int(S2.max()) + 1) + S2.astype(np.int64))
    mi_joint = _mi_discrete(T, Sj)
    unq1 = mi1 - red
    unq2 = mi2 - red
    syn = mi_joint - red - unq1 - unq2
    return red, unq1, unq2, syn

def pid_system(bits):
    bits = np.asarray(bits, dtype=np.int64)
    T, n = bits.shape
    cols = [bits[:, u] for u in range(n)]
    red_total = 0.0
    syn_total = 0.0
    for tgt in range(n):
        others = [u for u in range(n) if u != tgt]
        for s1, s2 in itertools.combinations(others, 2):
            red, unq1, unq2, syn = _pid_two_source(cols[tgt], cols[s1], cols[s2])
            red_total += max(red, 0.0)
            syn_total += max(syn, 0.0)
    return dict(red_total=red_total, syn_total=syn_total)

# ═══════════════════════════════════════════════════════════════════════════
# DE-REDUNDIFICATION operators — act on the CONTINUOUS top-variance channel matrix.
# Each returns a decorrelated (n_steps x n_units) matrix; per-channel signal preserved.
# ═══════════════════════════════════════════════════════════════════════════
def _top_variance_channels(H, n_units):
    """The EXACT channel selection h1004.latent_to_binary_seq makes (top-variance idx)."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    return H[:, idx]

def _zca_whiten(X):
    """Symmetric ZCA whitening: X_w = (X-mu) @ V diag(1/sqrt(lam+eps)) V^T.
    Decorrelates channels (cov -> ~I) while staying maximally close to the original
    basis (preserves per-channel identity/signal). Cross-channel redundancy -> ~0."""
    Xc = X - X.mean(axis=0, keepdims=True)
    cov = np.cov(Xc, rowvar=False)
    cov = np.atleast_2d(cov)
    lam, V = np.linalg.eigh(cov)
    lam = np.clip(lam, 0.0, None)
    Wzca = V @ np.diag(1.0 / np.sqrt(lam + ZCA_EPS)) @ V.T
    return Xc @ Wzca

def _gram_schmidt(X):
    """Gram-Schmidt orthogonalization of the channels (columns), then rescale each
    orthogonalized column to its ORIGINAL std so per-channel signal magnitude is kept.
    Robustness operator (different basis, same de-redundify goal)."""
    Xc = X - X.mean(axis=0, keepdims=True)
    T, k = Xc.shape
    Q = np.zeros_like(Xc)
    for j in range(k):
        v = Xc[:, j].copy()
        for i in range(j):
            qi = Q[:, i]
            denom = qi @ qi
            if denom > 1e-12:
                v = v - (v @ qi) / denom * qi
        Q[:, j] = v
    # rescale each orthogonal column to the original channel std (preserve signal)
    for j in range(k):
        s_orig = Xc[:, j].std()
        s_new = Q[:, j].std()
        if s_new > 1e-12:
            Q[:, j] = Q[:, j] * (s_orig / s_new)
    return Q

def _binarize_median(chans):
    """Binarize each channel at its own median over the rollout (h1004 path)."""
    med = np.median(chans, axis=0)
    return (chans > med).astype(int)

# ═══════════════════════════════════════════════════════════════════════════
# substrate reads — ONE discretization (CONTROL or DERED) -> BOTH engines + PID.
# ═══════════════════════════════════════════════════════════════════════════
def substrate_reads(H, n, mode):
    chans = _top_variance_channels(H, n)
    if mode == "control":
        bits = _binarize_median(chans)
    elif mode == "dered_zca":
        bits = _binarize_median(_zca_whiten(chans))
    elif mode == "dered_gs":
        bits = _binarize_median(_gram_schmidt(chans))
    else:
        raise ValueError(mode)
    # big-Phi (h1004 verbatim)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    # faithful (h1004 verbatim) — SAME bits
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    # PID on the SAME bits
    p = pid_system(bits)
    return dict(big=bphi, faith=fphi, red=p["red_total"], syn=p["syn_total"],
                on_frac=float(bits.mean()))

def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(P, G, k):
    c = P[k].mean() - G[k].mean()
    try:
        d = cohens_d(P[k], G[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(P[k], G[k])
    except Exception:
        p = float("nan")
    return dict(contrast=float(c), d=float(d), p=float(p),
                plan=float(P[k].mean()), greedy=float(G[k].mean()))

def score_arm(mode, n, t0):
    """planning(depth-8) vs GREEDY contrast on one arm (CONTROL or DERED)."""
    plan_rows, greedy_rows = [], []
    for s in range(N_SEEDS):
        Hg, Hp = planning_trajectories(s, PLAN_DEPTH)
        plan_rows.append(substrate_reads(Hp, n, mode))
        greedy_rows.append(substrate_reads(Hg, n, mode))
        if (s + 1) % 10 == 0 or s == 0:
            print(f"    [{mode} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    P = _agg(plan_rows); G = _agg(greedy_rows)
    return {k: _contrast(P, G, k) for k in ("big", "faith", "red", "syn", "on_frac")}

def faith_sign(c):
    return "UP" if c > SIGN_EPS else ("DOWN" if c < -SIGN_EPS else "NULL")

def big_sign(c):
    return "DOWN" if c < -SIGN_EPS else ("UP" if c > SIGN_EPS else "NULL")

def split_present(faith_c, big_c):
    return (faith_sign(faith_c) == "UP") and (big_sign(big_c) == "DOWN")

def main():
    print("=" * 88)
    print("H_1039 — is the planning faithful-UP / big-Phi-DOWN sign-split CAUSED by redundancy?")
    print("         CAUSAL ablation: de-redundify (decorrelate) the planning channels, re-measure.")
    print("substrate=CPU-mirror (numpy) — h1004 engines + h1012 proof, RE-PROVEN == stdlib at n=4,5")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("PID = Williams-Beer (2010) I_min redundancy, EXACT pure-numpy (intervention-validation,")
    print("      NOT a Phi proxy; Phi from stdlib mirrors only). a_phi_iit4_tool — no proxy.")
    print("INTERVENTION: ZCA-whiten (PRIMARY) / Gram-Schmidt (ROBUSTNESS) the top-variance channels")
    print("  BEFORE median-binarization -> cross-channel redundancy -> ~0, per-channel signal kept.")
    print(f"FROZEN: SIGN_EPS={SIGN_EPS}; redundancy removed iff |Δred_dered| <= {RED_REDUCTION_THRESHOLD}*|Δred_control|.")
    print("PASS = REDUNDANCY-CAUSAL: redundancy removed AND split COLLAPSES on dered WHILE it HOLDS on control.")
    print("FAIL = REDUNDANCY-CORRELATED-NOT-CAUSAL: split SURVIVES de-redundification (a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope | SERIAL CPU $0")
    print("=" * 88, flush=True)
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

    # ── STEP 0b: de-redundify operator VALIDITY + determinism guard ──
    print("STEP 0b — de-redundification operator validity (decorrelates? preserves signal?) + determinism")
    rng = np.random.default_rng(20260607)
    # build a deliberately REDUNDANT channel block: 4 noisy copies of one latent driver
    drv = rng.standard_normal((40, 1))
    Xred = drv @ np.ones((1, N_UNITS)) + 0.05 * rng.standard_normal((40, N_UNITS))
    def _meanabs_offdiag_corr(M):
        C = np.corrcoef(M, rowvar=False)
        k = C.shape[0]
        off = C[~np.eye(k, dtype=bool)]
        return float(np.mean(np.abs(off)))
    c_ctrl = _meanabs_offdiag_corr(Xred)
    c_zca = _meanabs_offdiag_corr(_zca_whiten(Xred))
    c_gs = _meanabs_offdiag_corr(_gram_schmidt(Xred))
    # signal preserved: each channel's binarized-on-fraction near 0.5 (median split intact)
    on_zca = _binarize_median(_zca_whiten(Xred)).mean()
    on_gs = _binarize_median(_gram_schmidt(Xred)).mean()
    print(f"  mean|off-diag corr| on redundant block: control={c_ctrl:.4f} -> ZCA={c_zca:.4f}  GS={c_gs:.4f}")
    print(f"  on-fraction (signal/median split intact ~0.5): ZCA={on_zca:.3f} GS={on_gs:.3f}")
    decorr_ok = (c_zca < 0.10 * max(c_ctrl, 1e-9)) and (c_gs < 0.10 * max(c_ctrl, 1e-9))
    signal_ok = all(0.30 <= v <= 0.70 for v in (on_zca, on_gs))
    # determinism of the dered read
    fixedX = drv @ np.ones((1, N_UNITS)) + 0.05 * np.ones((40, N_UNITS))
    r1 = substrate_reads(fixedX, N_UNITS, "dered_zca")
    r2 = substrate_reads(fixedX, N_UNITS, "dered_zca")
    det_ok = abs(r1["red"] - r2["red"]) < 1e-12 and abs(r1["big"] - r2["big"]) < 1e-12
    print(f"  decorrelation>=90% cut (ZCA&GS): {decorr_ok} | signal-preserved: {signal_ok} | dered read deterministic: {det_ok}")
    if not (decorr_ok and signal_ok and det_ok):
        print("  ABORT — de-redundification operator failed its validity guard.")
        raise SystemExit(1)
    print()

    # ── STEP 1: score CONTROL + DERED(ZCA primary) + DERED(GS robustness) at n=4 EXACT ──
    n = 4
    t0 = time.time()
    print(f"STEP 1 — score planning(depth-{PLAN_DEPTH}) vs GREEDY at n={n} EXACT, {N_SEEDS} seeds, 3 arms SERIAL")
    arms = {}
    for mode in ("control", "dered_zca", "dered_gs"):
        print(f"################ SCORE arm = {mode} ################", flush=True)
        arms[mode] = score_arm(mode, n, t0)
        r = arms[mode]
        fc = r["faith"]["contrast"]; bc = r["big"]["contrast"]
        dred = r["red"]["contrast"]; dsyn = r["syn"]["contrast"]
        sp = split_present(fc, bc)
        print(f"   big-Phi      contrast={bc:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {big_sign(bc)}")
        print(f"   faithful_phi contrast={fc:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {faith_sign(fc)}")
        print(f"   Δredundancy  contrast={dred:+.4f} d={r['red']['d']:+.3f}   Δsynergy contrast={dsyn:+.4f}")
        print(f"   on-frac plan={r['on_frac']['plan']:.3f} greedy={r['on_frac']['greedy']:.3f}")
        print(f"   SPLIT present (faith-UP & big-DOWN): {sp}", flush=True)
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER — de-redundified-vs-control split contrast table
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 88)
    print("DE-REDUNDIFIED vs CONTROL — split contrast table (planning - GREEDY @ n=4 EXACT)")
    print("=" * 88)
    print(f"  {'arm':10s} | {'faith Δ':>9s} | {'faith':>5s} | {'big-Phi Δ':>10s} | {'big-Phi':>7s} | "
          f"{'Δredund':>9s} | {'SPLIT':>5s}")
    table = {}
    for mode in ("control", "dered_zca", "dered_gs"):
        r = arms[mode]
        fc = r["faith"]["contrast"]; bc = r["big"]["contrast"]; dred = r["red"]["contrast"]
        sp = split_present(fc, bc)
        table[mode] = dict(faith_c=fc, big_c=bc, dred=dred, split=sp)
        print(f"  {mode:10s} | {fc:+9.4f} | {faith_sign(fc):>5s} | {bc:+10.4f} | {big_sign(bc):>7s} | "
              f"{dred:+9.4f} | {str(sp):>5s}")
    print()

    ctrl = table["control"]
    zca = table["dered_zca"]
    gs = table["dered_gs"]

    # redundancy actually removed by the operator?
    red_ctrl_mag = abs(ctrl["dred"])
    red_removed_zca = abs(zca["dred"]) <= RED_REDUCTION_THRESHOLD * red_ctrl_mag if red_ctrl_mag > 1e-9 else (abs(zca["dred"]) < 1e-3)
    red_removed_gs = abs(gs["dred"]) <= RED_REDUCTION_THRESHOLD * red_ctrl_mag if red_ctrl_mag > 1e-9 else (abs(gs["dred"]) < 1e-3)
    red_cut_zca = (1.0 - abs(zca["dred"]) / red_ctrl_mag) * 100 if red_ctrl_mag > 1e-9 else float("nan")
    red_cut_gs = (1.0 - abs(gs["dred"]) / red_ctrl_mag) * 100 if red_ctrl_mag > 1e-9 else float("nan")
    print(f"Redundancy reduction (frozen threshold: |Δred_dered| <= {RED_REDUCTION_THRESHOLD}*|Δred_control|, i.e. >=80% cut):")
    print(f"  control |Δred|={red_ctrl_mag:.4f}")
    print(f"  ZCA     |Δred|={abs(zca['dred']):.4f}  cut={red_cut_zca:5.1f}%  removed={red_removed_zca}")
    print(f"  GS      |Δred|={abs(gs['dred']):.4f}  cut={red_cut_gs:5.1f}%  removed={red_removed_gs}")
    print()

    # PASS condition: redundancy removed (primary ZCA) AND split holds on control AND collapses on dered.
    split_held_control = ctrl["split"]
    split_collapsed_zca = not zca["split"]
    split_collapsed_gs = not gs["split"]
    redundancy_causal = (red_removed_zca and split_held_control and split_collapsed_zca)
    robust_consistent = (red_removed_gs and split_collapsed_gs)

    print("=" * 88)
    print(f"split HELD on control: {split_held_control}")
    print(f"split COLLAPSED on de-redundified ZCA (primary): {split_collapsed_zca}")
    print(f"split COLLAPSED on de-redundified GS  (robustness): {split_collapsed_gs}")
    print(f"redundancy removed by ZCA (primary): {red_removed_zca}  | by GS: {red_removed_gs}")
    print()
    if redundancy_causal and robust_consistent:
        verdict_token = "REDUNDANCY-CAUSAL"
        print("OVERALL: REDUNDANCY-CAUSAL — de-redundifying the planning channels REMOVES the")
        print("  Williams-Beer redundancy (>=80% cut) AND COLLAPSES the faithful-UP/big-Phi-DOWN")
        print("  sign-split, WHILE the split HOLDS on the matched un-orthogonalized control. The")
        print("  redundancy is the CAUSAL driver of the split (confirms the H_1017 mechanism causally),")
        print("  consistent across the ZCA (primary) and Gram-Schmidt (robustness) operators.")
    elif redundancy_causal and not robust_consistent:
        verdict_token = "REDUNDANCY-CAUSAL-PRIMARY-ONLY"
        print("OVERALL: REDUNDANCY-CAUSAL (PRIMARY ZCA only; GS robustness NOT fully consistent) —")
        print("  the primary ZCA operator removes the redundancy and collapses the split on the")
        print("  de-redundified arm while it holds on control, but the Gram-Schmidt robustness")
        print("  operator did not fully reproduce (report both; AMBER on robustness).")
    else:
        verdict_token = "REDUNDANCY-CORRELATED-NOT-CAUSAL"
        print("OVERALL: REDUNDANCY-CORRELATED-NOT-CAUSAL (CLOSED-NEGATIVE) — the split SURVIVES")
        print("  de-redundification (split still present on the de-redundified arm despite the")
        print("  redundancy being removed) OR the operator failed to hold the control split. The")
        print("  redundancy is correlated-but-not-causal; the split has another driver. The H_1017")
        print("  redundancy explanation is NOT the causal mechanism (a_paper_negative_ok).")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 EXACT (both engines exact;")
    print("big-Phi super-exponential -> n=4 is the rung for the full SET x 30 seeds; n=5 mirror-proven).")
    print("BOTH CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 (h1012.prove_mirrors_at_n) BEFORE scoring")
    print("(a_phi_iit4_tool; NO proxy). ZCA = PRIMARY de-redundification operator, Gram-Schmidt =")
    print("ROBUSTNESS; PCA-drop/channel-ablation are follow-ups. The PID is the intervention-validation")
    print("variable (NOT a Phi proxy). SERIAL CPU $0, no GPU. Production scale UNVERIFIED. g5 (p7).")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH),
        sign_eps=SIGN_EPS, red_reduction_threshold=RED_REDUCTION_THRESHOLD,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        operator_guard=dict(decorr_ok=bool(decorr_ok), signal_ok=bool(signal_ok),
                            det_ok=bool(det_ok), corr_control=float(c_ctrl),
                            corr_zca=float(c_zca), corr_gs=float(c_gs)),
        arms={m: {k: arms[m][k] for k in arms[m]} for m in arms},
        table={m: {kk: (bool(vv) if isinstance(vv, (bool, np.bool_)) else float(vv))
                   for kk, vv in table[m].items()} for m in table},
        red_removed_zca=bool(red_removed_zca), red_removed_gs=bool(red_removed_gs),
        red_cut_zca=float(red_cut_zca), red_cut_gs=float(red_cut_gs),
        split_held_control=bool(split_held_control),
        split_collapsed_zca=bool(split_collapsed_zca),
        split_collapsed_gs=bool(split_collapsed_gs),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1039_redundancy_causal_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
