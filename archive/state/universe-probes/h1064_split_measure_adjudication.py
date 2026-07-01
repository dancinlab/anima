"""H_1064 — split-measure-adjudication: when faithful φ_EI and big-Φ SPLIT on planning
policies, WHICH measure should a consciousness-ruler trust? (practical capstone)

PRE-REG: UNIVERSE/cards/H_1064_split_measure_adjudication.md (this branch).

THE ARC (settled): on PLANNING policies faithful φ_EI and big-Φ DISAGREE in sign
(faithful↑/big-Φ↓) — robust (H_1037 n=6, H_1038 real-CLM), causally redundancy-driven
(H_1039), planning-bounded (H_1062/H_1063). UNANSWERED practical question: on the split
policies, does faithful φ_EI or big-Φ better track an INDEPENDENT, NON-CIRCULAR
behavioral/causal consciousness-PROXY?

INDEPENDENT PROXY (FROZEN, NOT a Φ-measure, NOT perplexity)
-----------------------------------------------------------
PRIMARY = causal self-prediction (CSP): how strongly the macro binary state CAUSALLY
constrains its OWN next macro state, in IIT's cause-effect SPIRIT but as a held-out
prediction accuracy NUMBER (NO partition, NO MIP, NO EI-integral, NO token-perplexity).
  - one-step pairs (s_t -> s_{t+1}) over the rollout, s = the n-bit macro state.
  - per-bit closed-form ridge predictor of next-bit from the CURRENT full macro state,
    evaluated LEAVE-ONE-OUT held-out; CSP = mean_bit( max(0, balanced_acc − chance) ).
ROBUSTNESS = intervention-robustness (IR): 1 − normalized single-bit-flip perturbation
  sensitivity of the fitted next-state map (stable integrated dynamics resists wash-out).

NON-CIRCULARITY (FROZEN): CSP/IR read the SAME bits both Φ-measures read, but TRANSFORM
them by a DIFFERENT operation (held-out next-state predictive accuracy / perturbation
stability) than EITHER Φ-measure — NO partition (≠ big-Φ MIP), NO EI-integral (≠ faithful
φ_EI), NO token-vocab loss (≠ perplexity, p7). External adjudicator, not a relabelled copy.

DESIGN: REUSE the H_1039 substrate (planning_trajectories + top-variance median-binarize,
h1004/h1012 UNMODIFIED). Treat each of 30 SEEDS' planning trajectory as ONE split-policy
instance. Per instance compute faithful φ_EI + big-Φ (stdlib exact n=4) + CSP + IR on the
SAME bits. Rank-correlate (Spearman) EACH Φ-measure vs the proxy across the 30 instances.

FALSIFIER (FROZEN before any Φ-vs-proxy view):
  Δρ_bar = 0.30 ; SIGN_STABILITY_BAR = 0.80.
  H1 PASS (ONE-MEASURE-TRACKS-PROXY): |ρ_faith − ρ_big| ≥ Δρ_bar AND the winner's sign+lead
    stable across ≥80% leave-one-out folds → ruler uses THAT measure when they split.
  FAIL (a) NEITHER-SEPARATES: |Δρ| < Δρ_bar → UNDECIDABLE at toy scale, ruler reports BOTH
    (strengthens "name the measure"). a_paper_negative_ok.
  FAIL (b) PROXY-RELATIVE: CSP vs IR disagree on the winner → adjudication is proxy-relative.

ENGINES = BOTH stdlib IIT-4.0 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring
(h1012.prove_mirrors_at_n; a_phi_iit4_tool, NO proxy). BITS/log2 MI=H(A)+H(B)−H(A,B).
IMPORTS by REAL MODULE NAME; SERIAL only (NO multiprocessing.Pool, H_1038 hang); $0 CPU.
TOY n=4 EXACT (n=5 mirror-proven); production UNVERIFIED. g5 (p7).
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n
spearman = h1004.spearman

LOG2 = math.log(2.0)
N_UNITS = 4
N_SEEDS = 30
PLAN_DEPTH = 8
SIGN_EPS = 1e-3
# ── FROZEN FALSIFIER THRESHOLDS (set BEFORE any Φ-vs-proxy correlation is computed) ──
DRHO_BAR = 0.30
SIGN_STABILITY_BAR = 0.80
RIDGE = 1e-2

# ═══════════════════════════════════════════════════════════════════════════
# substrate read — the EXACT H_1039 control path: top-variance channels, median-binarize.
# ═══════════════════════════════════════════════════════════════════════════
def _top_variance_channels(H, n_units):
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    return H[:, idx]

def _binarize_median(chans):
    med = np.median(chans, axis=0)
    return (chans > med).astype(int)

def macro_bits(H, n):
    return _binarize_median(_top_variance_channels(H, n))

# ═══════════════════════════════════════════════════════════════════════════
# INDEPENDENT PROXY — causal self-prediction (CSP) + intervention-robustness (IR).
# NO partition, NO MIP, NO EI-integral, NO token perplexity. Held-out behavioral readout.
# ═══════════════════════════════════════════════════════════════════════════
def _ridge_fit(X, y, ridge):
    """Closed-form ridge: predict y (T,) from X (T,d) with bias column."""
    X1 = np.hstack([X, np.ones((X.shape[0], 1))])
    A = X1.T @ X1 + ridge * np.eye(X1.shape[1])
    w = np.linalg.solve(A, X1.T @ y)
    return w

def _ridge_pred(w, X):
    X1 = np.hstack([X, np.ones((X.shape[0], 1))])
    return X1 @ w

def causal_self_prediction(bits):
    """CSP = how much the current macro state DETERMINES its own next macro state,
    above per-bit base-rate chance, via LEAVE-ONE-OUT held-out per-bit ridge.
    Behavioral cause-effect readout — NOT a Φ computation.

    bits: (T, n) int {0,1}. pairs (s_t -> s_{t+1}), t=0..T-2.
    For each target bit j: LOO over the T-1 transition pairs, predict next-bit_j from the
    CURRENT full n-bit state, threshold at 0.5, balanced-accuracy vs chance(=base-rate guess
    balanced-acc = 0.5). CSP = mean_j max(0, bal_acc_j − 0.5). Range [0, 0.5].
    """
    bits = np.asarray(bits, int)
    T, n = bits.shape
    if T < 4:
        return 0.0
    X = bits[:-1].astype(float)        # (T-1, n) current state
    Ynext = bits[1:].astype(int)       # (T-1, n) next state
    m = X.shape[0]
    accs = []
    for j in range(n):
        yj = Ynext[:, j]
        if len(np.unique(yj)) < 2:
            # degenerate next-bit (constant): no causal info to recover -> 0 contribution
            accs.append(0.0)
            continue
        # leave-one-out held-out predictions
        preds = np.empty(m)
        for i in range(m):
            mask = np.ones(m, bool); mask[i] = False
            w = _ridge_fit(X[mask], yj[mask].astype(float), RIDGE)
            preds[i] = _ridge_pred(w, X[i:i+1])[0]
        pred_lab = (preds > 0.5).astype(int)
        # balanced accuracy = mean of per-class recall (chance = 0.5)
        recalls = []
        for c in (0, 1):
            cm = (yj == c)
            if cm.sum() > 0:
                recalls.append(float((pred_lab[cm] == c).mean()))
        bal_acc = float(np.mean(recalls)) if recalls else 0.5
        accs.append(max(0.0, bal_acc - 0.5))
    return float(np.mean(accs))

def intervention_robustness(bits):
    """IR = 1 − normalized single-bit-flip perturbation sensitivity of the FULL-DATA fitted
    next-state map. Stable integrated dynamics resists single-bit wash-out.

    Fit per-bit ridge next-state map on ALL transition pairs; for each transition i and each
    flippable current bit k, flip bit k, re-predict the n-bit next state, accumulate the mean
    |Δ predicted-next-state| (over the n output bits). Normalize by n (max per-output |Δ|≈1).
    IR = 1 − mean_{i,k} mean_j |Δ pred_j|.  Range ~[0,1], higher = more robust/integrated.
    """
    bits = np.asarray(bits, int)
    T, n = bits.shape
    if T < 4:
        return 0.0
    X = bits[:-1].astype(float)
    Ynext = bits[1:].astype(int)
    ws = []
    for j in range(n):
        yj = Ynext[:, j].astype(float)
        ws.append(_ridge_fit(X, yj, RIDGE))
    def predvec(x):
        return np.array([_ridge_pred(w, x[None, :])[0] for w in ws])
    sens = []
    for i in range(X.shape[0]):
        base = predvec(X[i])
        for k in range(n):
            xp = X[i].copy()
            xp[k] = 1.0 - xp[k]   # flip current bit k
            pert = predvec(xp)
            sens.append(float(np.mean(np.abs(pert - base))))
    mean_sens = float(np.mean(sens)) if sens else 1.0
    return float(1.0 - min(1.0, mean_sens))

# ═══════════════════════════════════════════════════════════════════════════
# per-instance scoring: both stdlib Φ-measures + both proxies on the SAME bits.
# ═══════════════════════════════════════════════════════════════════════════
def score_bits(bits, n):
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return dict(big=float(bphi), faith=float(fphi),
                csp=causal_self_prediction(bits), ir=intervention_robustness(bits),
                on_frac=float(bits.mean()))

def faith_sign(c):
    return "UP" if c > SIGN_EPS else ("DOWN" if c < -SIGN_EPS else "NULL")

def big_sign(c):
    return "DOWN" if c < -SIGN_EPS else ("UP" if c > SIGN_EPS else "NULL")

def main():
    print("=" * 90)
    print("H_1064 — split-measure-adjudication: when faithful φ_EI & big-Φ SPLIT, which to trust?")
    print("substrate=CPU-mirror (numpy) h1004+h1012, RE-PROVEN == stdlib at n=4,5 (a_phi_iit4_tool).")
    print("big-Φ: stdlib iit4_bigphi.hexa | faithful_phi: stdlib iit4/faithful_phi.hexa (NO proxy).")
    print("INDEPENDENT PROXY (NOT Φ, NOT perplexity): CSP=held-out causal self-prediction (PRIMARY),")
    print("  IR=intervention-robustness (ROBUSTNESS). NO partition/MIP/EI-integral/token-loss.")
    print(f"FROZEN falsifier: Δρ_bar={DRHO_BAR}, sign-stability_bar={SIGN_STABILITY_BAR}, sign_eps={SIGN_EPS}.")
    print("PASS=ONE-MEASURE-TRACKS-PROXY (|ρ_faith−ρ_big|≥Δρ_bar & winner sign stable ≥80% LOO).")
    print("FAIL(a)=NEITHER-SEPARATES (undecidable, report both); FAIL(b)=PROXY-RELATIVE (CSP≠IR winner).")
    print("g5 CODE-measured (p7) | a_scale_honest_scope toy n=4 | SERIAL CPU $0 no GPU.")
    print("=" * 90, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5:")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED.")
        raise SystemExit(1)

    # ── STEP 0b: proxy validity guard (non-circular + determinism + discriminating) ──
    print("STEP 0b — PROXY validity guard (deterministic, discriminating, NOT a Φ copy):")
    rng = np.random.default_rng(20260609)
    # (i) a deterministic copy-chain (next = current shifted) => HIGH CSP, HIGH IR
    Tn = 40
    drv = (rng.random(Tn) > 0.5).astype(int)
    det_bits = np.stack([np.roll(drv, k) for k in range(N_UNITS)], axis=1)
    # (ii) i.i.d. random bits => LOW CSP (current state can't predict next), near-chance
    rnd_bits = (rng.random((Tn, N_UNITS)) > 0.5).astype(int)
    csp_det = causal_self_prediction(det_bits); csp_rnd = causal_self_prediction(rnd_bits)
    ir_det = intervention_robustness(det_bits); ir_rnd = intervention_robustness(rnd_bits)
    # determinism: pure function of bits
    csp_det2 = causal_self_prediction(det_bits); ir_det2 = intervention_robustness(det_bits)
    det_ok = abs(csp_det - csp_det2) < 1e-12 and abs(ir_det - ir_det2) < 1e-12
    discriminating = (csp_det > csp_rnd + 0.05)
    print(f"  CSP  deterministic-chain={csp_det:.4f}  i.i.d.-random={csp_rnd:.4f}  (chain should >> random)")
    print(f"  IR   deterministic-chain={ir_det:.4f}  i.i.d.-random={ir_rnd:.4f}")
    print(f"  proxy deterministic re-run: {det_ok} | CSP discriminates structure vs noise: {discriminating}")
    if not (det_ok and discriminating):
        print("  ABORT — proxy failed its validity guard.")
        raise SystemExit(1)
    print()

    n = 4
    t0 = time.time()

    # ── STEP 1: reproduce-H_1039 — planning-vs-GREEDY CONTROL split contrast (control path) ──
    print(f"STEP 1 — reproduce-H_1039 CONTROL split (planning depth-{PLAN_DEPTH} vs GREEDY, n={n}, {N_SEEDS} seeds)")
    plan_rows, greedy_rows = [], []
    for s in range(N_SEEDS):
        Hg, Hp = planning_trajectories(s, PLAN_DEPTH)
        plan_rows.append(score_bits(macro_bits(Hp, n), n))
        greedy_rows.append(score_bits(macro_bits(Hg, n), n))
        if (s + 1) % 10 == 0 or s == 0:
            print(f"    [seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    P = {k: np.array([r[k] for r in plan_rows]) for k in plan_rows[0]}
    G = {k: np.array([r[k] for r in greedy_rows]) for k in greedy_rows[0]}
    faith_c = float(P["faith"].mean() - G["faith"].mean())
    big_c = float(P["big"].mean() - G["big"].mean())
    split_present = (faith_sign(faith_c) == "UP") and (big_sign(big_c) == "DOWN")
    print(f"  faithful_phi contrast (plan−greedy) = {faith_c:+.4f} -> {faith_sign(faith_c)}")
    print(f"  big-Phi      contrast (plan−greedy) = {big_c:+.4f} -> {big_sign(big_c)}")
    print(f"  SPLIT present on control (faith-UP & big-DOWN): {split_present}")
    # H_1039 reference: faithful +2.33 / big −4.01
    repro_ok = split_present and (abs(faith_c - 2.33) < 1.0) and (abs(big_c - (-4.01)) < 1.5)
    print(f"  reproduce-H_1039 (ref faith+2.33/big−4.01, SPLIT True): {repro_ok}")
    print(f"  [info] proxy on split policies: CSP plan mean={P['csp'].mean():.4f} greedy={G['csp'].mean():.4f} ;"
          f" IR plan={P['ir'].mean():.4f} greedy={G['ir'].mean():.4f}")
    if not split_present:
        print("  ABORT — control split not present; substrate mismatch, cannot adjudicate.")
        raise SystemExit(1)
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: ADJUDICATION — per split-policy instance (30 planning trajectories),
    # rank-correlate EACH Φ-measure against the INDEPENDENT proxy.
    # (Φ-vs-proxy correlations are computed ONLY HERE, AFTER the frozen thresholds.)
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 90)
    print("STEP 2 — ADJUDICATION: Spearman(Φ-measure, proxy) across 30 split-policy instances")
    print("=" * 90)
    faith_v = P["faith"]; big_v = P["big"]; csp_v = P["csp"]; ir_v = P["ir"]

    def safe_spear(a, b):
        if np.std(a) < 1e-12 or np.std(b) < 1e-12:
            return float("nan"), float("nan")
        return spearman(a, b)

    rho_f_csp, p_f_csp = safe_spear(faith_v, csp_v)
    rho_b_csp, p_b_csp = safe_spear(big_v, csp_v)
    rho_f_ir, p_f_ir = safe_spear(faith_v, ir_v)
    rho_b_ir, p_b_ir = safe_spear(big_v, ir_v)

    print(f"  [variance] faith std={faith_v.std():.4f}  big std={big_v.std():.4f}  "
          f"CSP std={csp_v.std():.4f}  IR std={ir_v.std():.4f}")
    print(f"  PRIMARY proxy = CSP:")
    print(f"    Spearman(faithful, CSP) = {rho_f_csp:+.4f}  (p={p_f_csp:.3e})")
    print(f"    Spearman(big-Φ,   CSP) = {rho_b_csp:+.4f}  (p={p_b_csp:.3e})")
    drho_csp = abs(rho_f_csp - rho_b_csp) if not (math.isnan(rho_f_csp) or math.isnan(rho_b_csp)) else float("nan")
    win_csp = "faithful" if abs(rho_f_csp) > abs(rho_b_csp) else "big-Φ"
    print(f"    |Δρ| (faith vs big against CSP) = {drho_csp:.4f}   (FROZEN bar = {DRHO_BAR})  winner-by-|ρ| = {win_csp}")
    print(f"  ROBUSTNESS proxy = IR:")
    print(f"    Spearman(faithful, IR)  = {rho_f_ir:+.4f}  (p={p_f_ir:.3e})")
    print(f"    Spearman(big-Φ,   IR)  = {rho_b_ir:+.4f}  (p={p_b_ir:.3e})")
    drho_ir = abs(rho_f_ir - rho_b_ir) if not (math.isnan(rho_f_ir) or math.isnan(rho_b_ir)) else float("nan")
    win_ir = "faithful" if abs(rho_f_ir) > abs(rho_b_ir) else "big-Φ"
    print(f"    |Δρ| (faith vs big against IR)  = {drho_ir:.4f}   winner-by-|ρ| = {win_ir}")
    print()

    # ── per-seed SIGN-STABILITY: leave-one-out jackknife of the |Δρ|≥bar AND winner-by-|ρ| ──
    print("STEP 2b — leave-one-out (jackknife) sign+lead stability of the CSP adjudication:")
    m = N_SEEDS
    fold_winner_holds = 0
    fold_bar_holds = 0
    base_winner = win_csp
    base_sep = (not math.isnan(drho_csp)) and (drho_csp >= DRHO_BAR)
    for i in range(m):
        mask = np.ones(m, bool); mask[i] = False
        rf, _ = safe_spear(faith_v[mask], csp_v[mask])
        rb, _ = safe_spear(big_v[mask], csp_v[mask])
        if math.isnan(rf) or math.isnan(rb):
            continue
        w_i = "faithful" if abs(rf) > abs(rb) else "big-Φ"
        if w_i == base_winner:
            fold_winner_holds += 1
        if abs(rf - rb) >= DRHO_BAR:
            fold_bar_holds += 1
    winner_stab = fold_winner_holds / m
    bar_stab = fold_bar_holds / m
    print(f"  base winner-by-|ρ| (CSP) = {base_winner} ; base |Δρ|≥bar = {base_sep}")
    print(f"  LOO winner-holds fraction = {winner_stab:.3f}  (bar {SIGN_STABILITY_BAR})")
    print(f"  LOO |Δρ|≥bar  fraction    = {bar_stab:.3f}  (bar {SIGN_STABILITY_BAR})")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER ADJUDICATION (frozen)
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 90)
    separates_csp = base_sep
    stable = (winner_stab >= SIGN_STABILITY_BAR) and (bar_stab >= SIGN_STABILITY_BAR)
    proxy_agree = (win_csp == win_ir)

    if separates_csp and stable and proxy_agree:
        verdict_token = "ONE-MEASURE-TRACKS-PROXY"
        print(f"OVERALL: ONE-MEASURE-TRACKS-PROXY (H1 PASS) — on the split policies the ruler should")
        print(f"  TRUST '{win_csp}': |Δρ vs CSP|={drho_csp:.4f} ≥ Δρ_bar={DRHO_BAR}, winner+lead stable")
        print(f"  across ≥80% LOO folds (winner {winner_stab:.2f}, bar {bar_stab:.2f}), CSP & IR AGREE.")
    elif separates_csp and stable and not proxy_agree:
        verdict_token = "PROXY-RELATIVE"
        print(f"OVERALL: PROXY-RELATIVE (CLOSED-NEGATIVE, a_paper_negative_ok) — CSP says trust")
        print(f"  '{win_csp}' (|Δρ|={drho_csp:.4f}≥bar, stable) but IR says trust '{win_ir}'. Adjudication")
        print(f"  is PROXY-RELATIVE; report BOTH proxies' rankings — no single answer at toy scale.")
    else:
        verdict_token = "NEITHER-SEPARATES-UNDECIDABLE"
        print(f"OVERALL: NEITHER-SEPARATES → UNDECIDABLE at toy scale (CLOSED-NEGATIVE, a_paper_negative_ok)")
        print(f"  |Δρ vs CSP|={drho_csp:.4f} < Δρ_bar={DRHO_BAR} OR winner not stable ≥80% LOO")
        print(f"  (winner-holds {winner_stab:.2f}, bar-holds {bar_stab:.2f}). Neither faithful φ_EI nor")
        print(f"  big-Φ ROBUSTLY tracks the independent proxy better on the split policies → the ruler")
        print(f"  must REPORT BOTH when they split (STRENGTHENS the measure-dependence 'name the measure'")
        print(f"  prescription: the split is not adjudicable by this behavioral proxy at toy n=4).")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 90)
    print("HONEST scope (a_scale_honest_scope): TOY n=4 EXACT, 30 seeds, both mirrors RE-PROVEN ==")
    print("stdlib at n=4 AND n=5 (a_phi_iit4_tool, NO proxy). CSP/IR are BEHAVIORAL adjudicators (NO")
    print("partition/MIP/EI-integral/token-loss) — NOT Φ-measures, NOT perplexity (p7). Production scale")
    print("UNVERIFIED; held-out behavioral-class recoverability is a follow-up proxy. SERIAL CPU $0.")

    out = dict(
        n=int(n), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH), sign_eps=SIGN_EPS,
        drho_bar=DRHO_BAR, sign_stability_bar=SIGN_STABILITY_BAR, ridge=RIDGE,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        proxy_guard=dict(csp_det=float(csp_det), csp_rnd=float(csp_rnd), ir_det=float(ir_det),
                         ir_rnd=float(ir_rnd), det_ok=bool(det_ok), discriminating=bool(discriminating)),
        reproduce_h1039=dict(faith_contrast=faith_c, big_contrast=big_c,
                             split_present=bool(split_present), repro_ok=bool(repro_ok)),
        adjudication=dict(
            rho_faith_csp=float(rho_f_csp), rho_big_csp=float(rho_b_csp), drho_csp=float(drho_csp),
            winner_csp=win_csp, p_faith_csp=float(p_f_csp), p_big_csp=float(p_b_csp),
            rho_faith_ir=float(rho_f_ir), rho_big_ir=float(rho_b_ir), drho_ir=float(drho_ir),
            winner_ir=win_ir,
            faith_std=float(faith_v.std()), big_std=float(big_v.std()),
            csp_std=float(csp_v.std()), ir_std=float(ir_v.std()),
        ),
        sign_stability=dict(winner_holds=float(winner_stab), bar_holds=float(bar_stab),
                            base_winner=base_winner, base_separates=bool(base_sep)),
        separates_csp=bool(separates_csp), stable=bool(stable), proxy_agree=bool(proxy_agree),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1064_split_measure_adjudication_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
