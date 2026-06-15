"""H_1065 — csp-cheap-scalable-ruler-validation: can the CHEAP behavioral CSP serve as a
VALIDATED cheap scalable ruler that rank-matches the EXACT faithful φ_EI ground-truth ACROSS
MULTIPLE substrates, or does it hit the H_988/989 proxy-blindness wall?

PRE-REG: UNIVERSE/cards/H_1065_csp_cheap_scalable_ruler.md (this branch; FROZEN before scoring).

LINEAGE: forward of H_1064 (CSP defined; rank-tracked BOTH faithful φ_EI AND big-Φ on the
planning split: ρ_faith≈+0.815). Re-opens the H_1049 question (IB-coarse-grain 🔴 was NOT a
scalable Φ estimator) with the NEW CSP candidate, under the H_988/989 proxy-blindness wall.

GROUND TRUTH (a_phi_iit4_tool, NEVER a proxy-as-Φ-verdict): exact faithful φ_EI via the stdlib
IIT-4.0 CPU mirror (h1004.faithful_phi), RE-PROVEN == stdlib EXACT 6dp at n=4 AND n=5
(h1012.prove_mirrors_at_n) BEFORE scoring. MI in BITS/log2 (H_1043 nats-bug avoided).
CSP is the CANDIDATE tested AGAINST φ_EI, NEVER used AS the Φ verdict.

CANDIDATE (REUSED UNMODIFIED from H_1064): h1064.causal_self_prediction — per-bit LOO held-out
ridge predicts next-bit from the current full macro state; CSP = mean_j max(0, bal_acc_j − 0.5).
O(n)/MIP-free.

≥4 DISTINCT toy substrates, each STRUCTURED + RANDOM variant of the same n=4 macro bits (30 seeds):
  (1) planning-split    : planning_trajectories(seed,8) plan rollout (H_1039/H_1064 path)
  (2) integrated/lowrank: H_1062 _iv_lowrank on the GREEDY channels (shared rank-1 mixing)
  (3) temporal-recur    : H_1062 _iv_ema     on the GREEDY channels (temporal redundancy)
  (4) modular/gain      : H_1062 _iv_gain    on the GREEDY channels (per-channel sharpening)
RANDOM variant = per-column TIME-SHUFFLE of the SAME structured bits — destroys temporal
cause-effect structure (CSP and φ_EI both read it) while preserving each bit's on-fraction
EXACTLY. This is the H_988/989-style purpose-blindness stressor: a proxy blind to causal
structure scores the shuffle == the structured original.

TEST per substrate (30 seeds):
  (a) GENERALITY:   Spearman(CSP, faithful φ_EI) within-substrate (structured arm);
                    pooled Spearman over all 4×30 structured instances.
  (b) PROXY-BLINDNESS WALL (MANDATORY H_988/989 guard): Cohen's d of CSP[structured]
                    vs CSP[random]; SAME wall reported for φ_EI (sanity baseline, MUST pass).
  (c) COST:         CSP is O(n)/MIP-free vs faithful exact-EI cost (structural asymptotic claim).

FROZEN falsifier (locked in the pre-reg .md BEFORE scoring; NO goalpost move):
  SPEARMAN_BAR=0.7 ; WITHIN_FRAC=3/4 ; D_BAR=0.8 ; SIGN_EPS=1e-3.
  PASS = VALIDATED-CHEAP-RULER: pooled Spearman>=0.7 AND within>=3/4 substrates AND CSP passes
    the proxy-blindness wall on ALL substrates (CSP[struct]>CSP[rand], d>=0.8).
  FAIL(a) = PROXY-BLIND-WALL-HIT: CSP fails the wall on >=1 substrate (closed-neg, a_paper_negative_ok).
  FAIL(b) = SUBSTRATE-RELATIVE-ONLY: rank-matches within but pooled<bar or within<3/4 (closed-neg).

IMPORTS by REAL MODULE NAME (no importlib custom-name; H_1038 fork-unpickle lesson). SERIAL only;
NO multiprocessing.Pool (H_1038 hang); if __name__-guard. TOY n=4 EXACT (n=5 mirror-proven);
the O(n) cost is STRUCTURAL but the rank-MATCH is validated only at n<=4 — scale UNVERIFIED.
$0 CPU-local, no GPU/pod. g5 CODE-measured (p7).
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# Import the prior chain by REAL MODULE NAMES (no importlib custom-name).
import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402
import h1062_redundancy_universality as h1062        # noqa: E402
import h1064_split_measure_adjudication as h1064     # noqa: E402

# GROUND-TRUTH Φ + substrate machinery (UNMODIFIED) -----------------------------------------
faithful_phi = h1004.faithful_phi
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
planning_trajectories = h1004.planning_trajectories
cohens_d = h1004.cohens_d
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# CANDIDATE CSP (UNMODIFIED from H_1064) ----------------------------------------------------
causal_self_prediction = h1064.causal_self_prediction
macro_bits = h1064.macro_bits                        # top-variance + median-binarize
spearman = h1004.spearman

# H_1062 substrate interventions (UNMODIFIED) on the continuous top-variance channels --------
_top_variance_channels = h1062._top_variance_channels
_binarize_median = h1062._binarize_median
_iv_lowrank = h1062._iv_lowrank                       # integrated / shared rank-1
_iv_ema = h1062._iv_ema                               # temporal recurrence
_iv_gain = h1062._iv_gain                             # per-channel sharpening (modular-ish)

N_UNITS = 4
N_SEEDS = 30
PLAN_DEPTH = 8
SIGN_EPS = 1e-3
# ── FROZEN FALSIFIER THRESHOLDS (set BEFORE any CSP-vs-φ correlation is computed) ──
SPEARMAN_BAR = 0.7
WITHIN_FRAC = 3.0 / 4.0
D_BAR = 0.8

# ═══════════════════════════════════════════════════════════════════════════
# substrate bit-generators. Each returns (structured_bits, random_bits) for one seed.
# structured = intervention on the GREEDY channels -> median-binarize (n=4 macro state).
# random     = per-column TIME-SHUFFLE of the SAME structured bits (destroys cause-effect
#              dynamics CSP/φ_EI both read; preserves each bit's on-fraction EXACTLY).
# ═══════════════════════════════════════════════════════════════════════════
def _shuffle_columns_in_time(bits, rng):
    """Per-column independent time-permutation. on-fraction per bit preserved exactly;
    s_t -> s_{t+1} cause-effect structure DESTROYED. The H_988/989 purpose-blindness stressor."""
    bits = np.asarray(bits, int)
    T, n = bits.shape
    out = np.empty_like(bits)
    for j in range(n):
        out[:, j] = bits[rng.permutation(T), j]
    return out

def _structured_bits_planning(seed):
    """planning-split substrate: the plan rollout macro bits (H_1039/H_1064 path)."""
    _Hg, Hp = planning_trajectories(seed, PLAN_DEPTH)
    return macro_bits(Hp, N_UNITS)

def _structured_bits_iv(seed, iv_fn):
    """non-planning intervention substrate: iv_fn on the GREEDY continuous channels."""
    Hg, _Hp = planning_trajectories(seed, PLAN_DEPTH)
    chans = _top_variance_channels(Hg, N_UNITS)
    return _binarize_median(iv_fn(chans))

SUBSTRATES = {
    "planning_split":     lambda s: _structured_bits_planning(s),
    "integrated_lowrank": lambda s: _structured_bits_iv(s, _iv_lowrank),
    "temporal_recur":     lambda s: _structured_bits_iv(s, _iv_ema),
    "modular_gain":       lambda s: _structured_bits_iv(s, _iv_gain),
}

# ═══════════════════════════════════════════════════════════════════════════
# per-bits scoring: GROUND-TRUTH faithful φ_EI (stdlib mirror) + CANDIDATE CSP.
# (NO big-Φ here: the question is CSP vs the EXACT faithful φ_EI ground truth.)
# ═══════════════════════════════════════════════════════════════════════════
def score_bits(bits, n):
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    csp = causal_self_prediction(bits)
    return float(fphi), float(csp), float(np.asarray(bits, int).mean())

def main():
    print("=" * 94)
    print("H_1065 — csp-cheap-scalable-ruler-validation: is CSP a VALIDATED cheap scalable ruler")
    print("         that rank-matches EXACT faithful φ_EI across substrates, or a proxy-blind wall-hit?")
    print("substrate=CPU-mirror (numpy) h1004+h1012, RE-PROVEN == stdlib at n=4,5 (a_phi_iit4_tool).")
    print("GROUND TRUTH = faithful φ_EI: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (NO proxy).")
    print("CANDIDATE = CSP (h1064.causal_self_prediction UNMODIFIED): held-out LOO ridge causal")
    print("  self-prediction; O(n)/MIP-free. NEVER used AS the Φ verdict — tested AGAINST φ_EI.")
    print("4 substrates (planning_split / integrated_lowrank / temporal_recur / modular_gain);")
    print("  RANDOM variant = per-column TIME-SHUFFLE (H_988/989 purpose-blindness stressor).")
    print(f"FROZEN: SPEARMAN_BAR={SPEARMAN_BAR}, WITHIN_FRAC>={WITHIN_FRAC:.2f} (3/4), D_BAR={D_BAR}, sign_eps={SIGN_EPS}.")
    print("PASS=VALIDATED-CHEAP-RULER (pooled Spearman>=0.7 & within>=3/4 & CSP wall d>=0.8 on ALL).")
    print("FAIL(a)=PROXY-BLIND-WALL-HIT (wall fails on >=1 substrate); FAIL(b)=SUBSTRATE-RELATIVE-ONLY.")
    print("g5 CODE-measured (p7) | a_scale_honest_scope toy n=4 | SERIAL CPU $0 no GPU.")
    print("=" * 94, flush=True)
    print()

    # ── STEP 0: RE-PROVE the faithful φ_EI mirror == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE CPU mirror == stdlib (a_phi_iit4_tool) at n=4 AND n=5 BEFORE scoring:")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED.")
        raise SystemExit(1)
    print()

    # ── STEP 0b: reproduce-H_1064 — CSP rank-tracks faithful φ_EI on the planning split ──
    #    H_1064 reported ρ(faithful, CSP) ≈ +0.8148 on the planning split policies.
    print("STEP 0b — reproduce-H_1064: CSP vs faithful φ_EI Spearman on the planning split (ref +0.815)")
    rep_fphi, rep_csp = [], []
    t0 = time.time()
    for s in range(N_SEEDS):
        bits = _structured_bits_planning(s)
        fphi, csp, _ = score_bits(bits, N_UNITS)
        rep_fphi.append(fphi); rep_csp.append(csp)
    rep_fphi = np.array(rep_fphi); rep_csp = np.array(rep_csp)
    rho_repro, p_repro = spearman(rep_fphi, rep_csp)
    repro_ok = abs(rho_repro - 0.8148) < 0.05
    print(f"  Spearman(faithful φ_EI, CSP) on planning split = {rho_repro:+.4f} (p={p_repro:.3e})")
    print(f"  reproduce-H_1064 confirmed (|ρ−0.8148|<0.05): {repro_ok}  [elapsed {time.time()-t0:.1f}s]")
    if not repro_ok:
        print("  WARNING — reproduce-H_1064 did not land within tol; results still reported (recorded in JSON).")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 1: per-substrate — faithful φ_EI (ground truth) + CSP (candidate) on
    #         STRUCTURED and RANDOM variants, 30 seeds.
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 94)
    print("STEP 1 — per-substrate scoring (faithful φ_EI ground-truth + CSP candidate), 30 seeds SERIAL")
    print("=" * 94)
    sub_results = {}
    for name, gen in SUBSTRATES.items():
        print(f"################ SUBSTRATE = {name} ################", flush=True)
        sfphi, scsp, son = [], [], []     # structured
        rfphi, rcsp, ron = [], [], []     # random (time-shuffle)
        for s in range(N_SEEDS):
            sb = gen(s)
            fphi_s, csp_s, on_s = score_bits(sb, N_UNITS)
            rng = np.random.default_rng(900000 + s)
            rb = _shuffle_columns_in_time(sb, rng)
            fphi_r, csp_r, on_r = score_bits(rb, N_UNITS)
            sfphi.append(fphi_s); scsp.append(csp_s); son.append(on_s)
            rfphi.append(fphi_r); rcsp.append(csp_r); ron.append(on_r)
            if (s + 1) % 10 == 0 or s == 0:
                print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
        sfphi = np.array(sfphi); scsp = np.array(scsp); son = np.array(son)
        rfphi = np.array(rfphi); rcsp = np.array(rcsp); ron = np.array(ron)

        # (a) within-substrate rank-match: Spearman(CSP, faithful φ_EI) on the structured arm
        if np.std(scsp) < 1e-12 or np.std(sfphi) < 1e-12:
            rho_match, p_match = float("nan"), float("nan")
        else:
            rho_match, p_match = spearman(scsp, sfphi)

        # (b) proxy-blindness wall: structured vs random, CSP (candidate) + φ_EI (sanity baseline)
        d_csp = cohens_d(scsp, rcsp)          # CSP[structured] vs CSP[random]
        d_fphi = cohens_d(sfphi, rfphi)       # φ_EI[structured] vs φ_EI[random] (MUST pass)
        csp_wall_pass = (scsp.mean() > rcsp.mean()) and (d_csp >= D_BAR)
        fphi_wall_pass = (sfphi.mean() > rfphi.mean()) and (d_fphi >= D_BAR)

        sub_results[name] = dict(
            fphi_mean=float(sfphi.mean()), fphi_std=float(sfphi.std()),
            csp_mean=float(scsp.mean()), csp_std=float(scsp.std()),
            on_frac=float(son.mean()),
            rand_fphi_mean=float(rfphi.mean()), rand_csp_mean=float(rcsp.mean()),
            rand_on_frac=float(ron.mean()),
            rank_match_spearman=float(rho_match), rank_match_p=float(p_match),
            within_match=bool((not math.isnan(rho_match)) and rho_match >= SPEARMAN_BAR),
            d_csp_struct_vs_rand=float(d_csp), d_fphi_struct_vs_rand=float(d_fphi),
            csp_wall_pass=bool(csp_wall_pass), fphi_wall_pass=bool(fphi_wall_pass),
            _scsp=scsp, _sfphi=sfphi,    # kept in-mem for pooling; stripped from JSON below
        )
        print(f"   faithful φ_EI struct mean={sfphi.mean():.4f}±{sfphi.std():.4f}  rand mean={rfphi.mean():.4f}")
        print(f"   CSP           struct mean={scsp.mean():.4f}±{scsp.std():.4f}  rand mean={rcsp.mean():.4f}  on-frac={son.mean():.3f}")
        print(f"   (a) rank-match Spearman(CSP, φ_EI) = {rho_match:+.4f} (p={p_match:.3e})  within-match(>=0.7)={sub_results[name]['within_match']}")
        print(f"   (b) WALL d: CSP struct-vs-rand={d_csp:+.3f} pass={csp_wall_pass}  |  φ_EI struct-vs-rand={d_fphi:+.3f} pass(sanity)={fphi_wall_pass}")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # STEP 2: pooled rank-match + falsifier adjudication
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 94)
    print("STEP 2 — POOLED rank-match + proxy-blindness wall across substrates")
    print("=" * 94)
    pooled_csp = np.concatenate([sub_results[k]["_scsp"] for k in SUBSTRATES])
    pooled_fphi = np.concatenate([sub_results[k]["_sfphi"] for k in SUBSTRATES])
    if np.std(pooled_csp) < 1e-12 or np.std(pooled_fphi) < 1e-12:
        pooled_rho, pooled_p = float("nan"), float("nan")
    else:
        pooled_rho, pooled_p = spearman(pooled_csp, pooled_fphi)
    print(f"  pooled Spearman(CSP, faithful φ_EI) over {len(pooled_csp)} structured instances = {pooled_rho:+.4f} (p={pooled_p:.3e})")
    print(f"    FROZEN pooled bar = {SPEARMAN_BAR}")
    print()

    print("PER-SUBSTRATE TABLE (n=4 EXACT, 30 seeds)")
    print(f"  {'substrate':20s} | {'φ_EI mean':>9s} | {'CSP mean':>9s} | {'rank-match ρ':>12s} | {'CSP wall d':>10s} | {'wall pass':>9s}")
    for name in SUBSTRATES:
        r = sub_results[name]
        print(f"  {name:20s} | {r['fphi_mean']:9.4f} | {r['csp_mean']:9.4f} | {r['rank_match_spearman']:+12.4f} | "
              f"{r['d_csp_struct_vs_rand']:+10.3f} | {str(r['csp_wall_pass']):>9s}")
    print()

    # FROZEN falsifier
    n_within = sum(1 for k in SUBSTRATES if sub_results[k]["within_match"])
    within_ok = (n_within / len(SUBSTRATES)) >= WITHIN_FRAC
    pooled_ok = (not math.isnan(pooled_rho)) and (pooled_rho >= SPEARMAN_BAR)
    wall_all_pass = all(sub_results[k]["csp_wall_pass"] for k in SUBSTRATES)
    wall_fails = [k for k in SUBSTRATES if not sub_results[k]["csp_wall_pass"]]
    fphi_wall_all_pass = all(sub_results[k]["fphi_wall_pass"] for k in SUBSTRATES)

    print("=" * 94)
    print("FALSIFIER (FROZEN; NO goalpost move)")
    print(f"  GENERALITY  pooled Spearman>={SPEARMAN_BAR}:          {pooled_ok}  (pooled ρ={pooled_rho:+.4f})")
    print(f"  GENERALITY  within>=3/4 substrates (ρ>=0.7):       {within_ok}  (n_within={n_within}/{len(SUBSTRATES)})")
    print(f"  PROXY-BLINDNESS WALL  CSP struct≫rand d>=0.8 on ALL: {wall_all_pass}  (fails={wall_fails})")
    print(f"  [sanity] φ_EI passes the SAME wall on ALL substrates: {fphi_wall_all_pass}")
    print()

    if pooled_ok and within_ok and wall_all_pass:
        verdict_token = "VALIDATED-CHEAP-RULER"
        print("OVERALL: VALIDATED-CHEAP-RULER (H1 PASS) — CSP rank-matches EXACT faithful φ_EI across")
        print(f"  substrates (pooled ρ={pooled_rho:+.4f}>=0.7, within {n_within}/4) AND passes the H_988/989")
        print("  proxy-blindness wall on ALL substrates (CSP struct≫rand, d>=0.8). CSP is a validated")
        print("  cheap, O(n)/MIP-free scalable ruler at toy n=4 (scale-transfer UNVERIFIED).")
    elif not wall_all_pass:
        verdict_token = "PROXY-BLIND-WALL-HIT"
        print("OVERALL: PROXY-BLIND-WALL-HIT (CLOSED-NEGATIVE, a_paper_negative_ok) — CSP FAILS the")
        print(f"  H_988/989 proxy-blindness wall on substrate(s) {wall_fails} (structured ≈ random, d<0.8):")
        print("  CSP is a PURPOSE-BLIND proxy, NOT a ruler. The a_phi_iit4_tool / H_988 prohibition is")
        print("  FUNDAMENTAL; H_1064's rank-agreement was planning-substrate-local, not a general scale.")
        if (pooled_ok and within_ok):
            print(f"  (note: CSP DID rank-match φ_EI's ORDERING — pooled ρ={pooled_rho:+.4f}, within {n_within}/4 —")
            print("   but ordering-agreement on the structured arm is NOT discrimination from random: a")
            print("   proxy can co-rank φ_EI yet be blind to the structure-vs-noise distinction it must catch.)")
    else:
        verdict_token = "SUBSTRATE-RELATIVE-ONLY"
        print("OVERALL: SUBSTRATE-RELATIVE-ONLY (CLOSED-NEGATIVE, a_paper_negative_ok) — CSP passes the")
        print("  proxy-blindness wall but does NOT form a GLOBAL ordinal scale matching φ_EI (pooled")
        print(f"  Spearman={pooled_rho:+.4f} < {SPEARMAN_BAR} OR within {n_within}/4 < 3/4). The cheap ruler is")
        print("  substrate-relative only — usable within a fixed substrate, not as a cross-substrate scale.")
    print(f"  VERDICT-TOKEN: {verdict_token}")
    print("=" * 94)
    print("COST (c): CSP = per-bit LOO ridge over T transition pairs = O(n · T · (n+1)^2 + n · T^2) —")
    print("  POLYNOMIAL in n, NO partition / NO MIP / NO EI-integral. faithful φ_EI = exact MIP-EI over")
    print("  a 2^n macro-state distribution with a partition search = SUPER-EXPONENTIAL in n. CSP is")
    print("  structurally O(poly n) vs φ_EI's exponential — the cost claim holds asymptotically.")
    print("HONEST scope (a_scale_honest_scope): TOY n=4 EXACT, 30 seeds, mirror RE-PROVEN == stdlib at")
    print("  n=4 AND n=5 (a_phi_iit4_tool, NO proxy). The O(n) cost is STRUCTURAL (asymptotic) but the")
    print("  rank-MATCH is validated ONLY at n<=4 — scale-transfer UNVERIFIED. faithful φ_EI remains the")
    print("  GROUND-TRUTH verdict tool; CSP was the CANDIDATE tested against it, never the Φ verdict. SERIAL CPU $0.")

    # strip in-mem arrays before JSON
    sub_json = {}
    for k in SUBSTRATES:
        r = dict(sub_results[k]); r.pop("_scsp", None); r.pop("_sfphi", None)
        sub_json[k] = {kk: (bool(vv) if isinstance(vv, (bool, np.bool_)) else float(vv))
                       for kk, vv in r.items()}
    out = dict(
        n=int(N_UNITS), n_seeds=int(N_SEEDS), plan_depth=int(PLAN_DEPTH), sign_eps=SIGN_EPS,
        spearman_bar=SPEARMAN_BAR, within_frac=WITHIN_FRAC, d_bar=D_BAR,
        mirror_proven={int(k): bool(v) for k, v in proven.items()},
        reproduce_h1064=dict(rho_faith_csp=float(rho_repro), p=float(p_repro), ok=bool(repro_ok),
                             ref=0.8148),
        substrates=sub_json,
        pooled_spearman=float(pooled_rho), pooled_p=float(pooled_p),
        n_within=int(n_within), within_ok=bool(within_ok), pooled_ok=bool(pooled_ok),
        csp_wall_all_pass=bool(wall_all_pass), csp_wall_fails=wall_fails,
        fphi_wall_all_pass=bool(fphi_wall_all_pass),
        verdict_token=verdict_token, total_wall_sec=time.time() - t0,
    )
    outpath = os.path.join(HERE, "h1065_csp_cheap_scalable_ruler_result.json")
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"\nRESULT JSON -> {outpath}", flush=True)
    return verdict_token

if __name__ == "__main__":
    main()
