"""H_1040 — which BASELINE REGIME predicts the big-Phi-DOWN half? (H_1033 residual)

RESIDUAL OF H_1033 (⚪ INCONCLUSIVE-DEGENERATE-FAMILY)
----------------------------------------------------
H_1033 held the BASELINE fixed (the H_1023 independent-noisy-bits baseline) and swept the TASK
across a frozen family of 5 n=4 substrates. EVERY task came out big-Phi-NOT-DOWN (the bigΦ-DOWN
class was empty) — so the bigΦ-DOWN half of the planning split does NOT reproduce on ANY matched
independent-bits baseline. Its deferred next step (verbatim): the SIGN is dominated by the
BASELINE CONTRAST, not the intervention's task structure. So HOLD the planning intervention
FIXED and SWEEP the BASELINE REGIME; find which baseline makes big-Phi go DOWN.

THE H_1040 PRE-REGISTERED TEST (frozen in H_1040_split_baseline_regime.md, merged #1939)
----------------------------------------------------------------------------------------
FIXED intervention = the canonical PLANNING rollout that produced the original H_973/H_1004 split
(planning_trajectories(seed, depth=8) -> H_plan -> latent_to_binary_seq). Imported VERBATIM from
h1004 (the same LatentWorldModel + planning depth-8 deliberation H_973 used). For each seed the
SAME planning bits feed BOTH Phi engines.

FROZEN sweep of 4 BASELINE REGIMES, each contrasted planning-vs-baseline (planning − baseline),
30 seeds, Cohen d, sign:
  (a) independent-bits        : H_1033/H_1023 run_base — independent noisy coin bits (no structure)
  (b) pre-rollout latent      : the A-PRIORI PICK — H_greedy = H0 = the model's OWN latent state
                                BEFORE the planning rollout (this IS the original H_973 GREEDY
                                baseline). latent_to_binary_seq(H_greedy).
  (c) shuffled-time           : the planning bits with the TIME axis shuffled per seed (frozen
                                shuffle RNG) — same marginals, temporal/TPM structure destroyed.
  (d) matched-marginal corr   : per-step independent draws matching the planning arm's per-unit
                                ON-marginals (frozen draw RNG) — marginals matched, cross-unit +
                                temporal correlation broken.

FROZEN sign rule: a baseline labels the planning contrast bigΦ-DOWN iff big-Phi contrast d <= -0.8
(the pre-registered d threshold) AND big-Phi mean contrast < 0.

PRE-REGISTERED FALSIFIER (frozen BEFORE measuring):
  PASS = BASELINE-REGIME-SPECIFIC : the A-PRIORI pre-rollout-latent baseline (b) makes big-Phi go
    DOWN (d <= -0.8) AND faithful go UP (faithful contrast > 0), AND at least one OTHER baseline
    does NOT make big-Phi go DOWN -> the bigΦ-DOWN half is a planning-vs-(pre-rollout-latent)
    property, pinning the H_1033 residual.
  FAIL = NOT-BASELINE-SPECIFIC : big-Phi-DOWN appears under NO baseline regime, or under ALL of
    them -> the DOWN half is either non-existent or regime-independent (H_1033's degeneracy is
    structural, not a baseline choice; publishable closed-negative, a_paper_negative_ok).

REUSE (a_phi_iit4_tool): the two stdlib IIT-4.0 engine CPU mirrors + matched discretization reads
+ H_1012 prove_mirrors_at_n equivalence proof + run_base — ALL imported VERBATIM via the H_1033
module (which chains h1023->h1017->h1014->h1004). The planning intervention + latent->bits reads
are imported VERBATIM from h1004. This file adds ONLY the 4 frozen baseline-regime generators +
the frozen sign rule + the falsifier. Phi from the stdlib mirrors ONLY — NEVER a proxy.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT; big-Phi
super-exponential so n=4 is the rung for 4 baselines x 30 seeds. CPU mirrors RE-PROVEN == stdlib
at n=4 AND n=5 (H_1012) BEFORE scoring. SERIAL only (no Pool — H_1038 hang lesson). Scale-transfer
UNVERIFIED. NOT a forge binary; $0 CPU-local, no GPU. g5 CODE-measured (no LLM self-judge, p7).
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Import the H_1033 module VERBATIM: it re-exports (via its h1023->h1017->h1014->h1004 chain)
#    BOTH engine mirrors, matched discretization reads, the H_1012 equivalence proof, run_base,
#    AND reads_from_bits (big-Phi + faithful + PID, all on the SAME mirror-built MI matrix). ──
import importlib.util as _ilu
_h1033_path = os.path.join(HERE, "h1033_split_task_property.py")
_spec = _ilu.spec_from_file_location("h1033", _h1033_path)
_h1033 = _ilu.module_from_spec(_spec)
_src = open(_h1033_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1033_path, "exec"), _h1033.__dict__)

prove_mirrors_at_n = _h1033.prove_mirrors_at_n
big_phi = _h1033.big_phi
faithful_phi = _h1033.faithful_phi
build_mi_matrix = _h1033.build_mi_matrix
faithful_phi_from_mi = _h1033.faithful_phi_from_mi
binary_seq_to_tpm = _h1033.binary_seq_to_tpm
modal_state = _h1033.modal_state
binary_seq_to_faithful_state = _h1033.binary_seq_to_faithful_state
cohens_d = _h1033.cohens_d
welch_t = _h1033.welch_t
run_base = _h1033.run_base          # H_1033/H_1023 independent-noisy-bits baseline
reads_from_bits = _h1033.reads_from_bits

N_UNITS = _h1033.N_UNITS            # 4
N_SEEDS = _h1033.N_SEEDS            # 30
assert N_UNITS == 4, "frozen n=4 family"

# ── Import the CANONICAL PLANNING intervention VERBATIM from h1004 (the SAME LatentWorldModel +
#    planning depth-8 deliberation that produced the original H_973 big-Phi-DOWN / faithful-UP
#    split, and the SAME latent_to_binary_seq discretization). ──
_h1004_path = os.path.join(HERE, "h1004_bigphi_faithful_clean.py")
_spec4 = _ilu.spec_from_file_location("h1004", _h1004_path)
_h1004 = _ilu.module_from_spec(_spec4)
_src4 = open(_h1004_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src4, _h1004_path, "exec"), _h1004.__dict__)

planning_trajectories = _h1004.planning_trajectories
latent_to_binary_seq = _h1004.latent_to_binary_seq

PLAN_DEPTH = 8   # FROZEN — the deepest depth H_973/H_1004 used (where the split was largest)

# ═══════════════════════════════════════════════════════════════════════════
# FIXED INTERVENTION + the 4 FROZEN BASELINE REGIMES.
# Every generator returns an (n_steps × N_UNITS) binary bits array for one seed.
# ═══════════════════════════════════════════════════════════════════════════
def gen_planning(seed):
    """FIXED intervention: canonical planning rollout (depth-8 deliberation), the SAME H_973
    intervention that produced the original big-Phi-DOWN / faithful-UP split. bits = top-variance
    binarized latent of the deliberation trajectory H_plan."""
    _Hg, Hp = planning_trajectories(seed, PLAN_DEPTH)
    bits, _n = latent_to_binary_seq(Hp)
    return bits

def base_independent_bits(seed):
    """(a) independent-bits — the H_1033/H_1023 baseline: independent noisy coin bits, no structure."""
    return run_base(seed)

def base_pre_rollout_latent(seed):
    """(b) pre-rollout latent — the A-PRIORI PICK: the model's OWN latent state BEFORE the planning
    rollout. H_greedy = H0 = the encoded start trajectory, the original H_973 GREEDY baseline.
    bits = top-variance binarized latent of H_greedy."""
    Hg, _Hp = planning_trajectories(seed, PLAN_DEPTH)
    bits, _n = latent_to_binary_seq(Hg)
    return bits

def base_shuffled_time(seed):
    """(c) shuffled-time — the planning bits with the TIME axis permuted (frozen shuffle RNG).
    Per-unit marginals identical to the planning arm; temporal / TPM structure destroyed."""
    bits = gen_planning(seed)
    rng = np.random.default_rng(60_000 + seed)
    perm = rng.permutation(bits.shape[0])
    return bits[perm].copy()

def base_matched_marginal(seed):
    """(d) matched-marginal correlated — per-step INDEPENDENT draws matching the planning arm's
    per-unit ON-marginals (frozen draw RNG). Marginals matched; cross-unit + temporal correlation
    broken. (Named 'correlated' in the .md as the marginal-preserving control vs (a)'s 0.5 coins.)"""
    bits = gen_planning(seed)
    p_on = bits.mean(axis=0)            # per-unit ON-probability of the planning arm
    rng = np.random.default_rng(70_000 + seed)
    T = bits.shape[0]
    out = (rng.random((T, N_UNITS)) < p_on[None, :]).astype(int)
    return out

# ═══════════════════════════════════════════════════════════════════════════
# CONTRAST machinery (planning − baseline), matched per seed.
# ═══════════════════════════════════════════════════════════════════════════
def _agg(rows):
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}

def _contrast(I, B, k):
    c = I[k].mean() - B[k].mean()
    try:
        d = cohens_d(I[k], B[k])
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(I[k], B[k])
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p, base=B[k].mean(), intv=I[k].mean())

def score_baseline(name, base_gen, plan_rows, t0):
    """plan_rows = the (already-computed) reads of the FIXED planning arm over seeds.
    Score the matched contrast planning − base_gen(seed)."""
    base_rows = []
    for s in range(N_SEEDS):
        base_rows.append(reads_from_bits(base_gen(s)))
        print(f"    [{name} seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    B = _agg(base_rows); I = _agg(plan_rows)
    return {k: _contrast(I, B, k) for k in ("big", "faith", "dec", "red_total", "syn_total")}

D_DOWN = -0.8   # FROZEN pre-registered Cohen-d threshold for "big-Phi goes DOWN"

def is_big_down(r):
    """frozen sign rule: big-Phi goes DOWN iff its contrast d <= -0.8 AND mean contrast < 0."""
    return (r["big"]["d"] <= D_DOWN) and (r["big"]["contrast"] < 0.0)

def is_faith_up(r):
    return r["faith"]["contrast"] > 0.0

def signword(x, eps=1e-3):
    return "RAISES" if x > eps else ("LOWERS" if x < -eps else "NULL")

def main():
    print("=" * 88)
    print("H_1040 — which BASELINE REGIME predicts the big-Phi-DOWN (split-enabling) half?")
    print("RESIDUAL of H_1033 (⚪ degenerate: bigΦ-DOWN empty on a FIXED independent-bits baseline).")
    print("HOLD the canonical PLANNING intervention FIXED (planning_trajectories depth=8, H_973/H_1004);")
    print("SWEEP 4 baseline regimes: (a) independent-bits (b) pre-rollout-latent [A-PRIORI PICK]")
    print("  (c) shuffled-time (d) matched-marginal correlated. Contrast = planning − baseline, 30 seeds.")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("engine reads=CPU mirror (numpy), H_1004 engines RE-PROVEN == stdlib at n=4 AND n=5 (H_1012)")
    print("  BEFORE scoring. SERIAL only (no Pool — H_1038 hang lesson). Phi from mirrors ONLY (no proxy).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print(f"FROZEN d threshold = {D_DOWN} (big-Phi DOWN iff contrast d <= {D_DOWN} AND mean contrast < 0).")
    print("PASS = BASELINE-REGIME-SPECIFIC: pre-rollout-latent (b) makes bigΦ DOWN (d<=-0.8) AND faithful")
    print("  UP, AND >=1 OTHER baseline does NOT make bigΦ DOWN.")
    print("FAIL = NOT-BASELINE-SPECIFIC: bigΦ-DOWN under NO baseline, or under ALL (closed-negative).")
    print("=" * 88)
    print()

    # ── STEP 0 — equivalence proof BEFORE scoring (H_1012), n=4 + n=5. ──
    print("EQUIVALENCE PROOF (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    ok = ok and ok5

    # engine determinism on a fixed sample of THIS probe's bits (the planning arm).
    b_fixed = gen_planning(0)
    r1 = reads_from_bits(b_fixed); r2 = reads_from_bits(b_fixed)
    eng_det = (abs(r1["big"] - r2["big"]) < 1e-12 and abs(r1["faith"] - r2["faith"]) < 1e-12)
    print(f"  planning-arm engine deterministic re-run: {eng_det}  "
          f"big={r1['big']:.4f} faith={r1['faith']:.6f}  (plan bits shape={b_fixed.shape})")

    # baseline-generator determinism (frozen RNGs -> identical bits on re-call).
    det_base = all(np.array_equal(g(0), g(0)) for g in
                   (base_independent_bits, base_pre_rollout_latent, base_shuffled_time, base_matched_marginal))
    print(f"  baseline generators deterministic re-call: {det_base}")

    # marginal-match sanity for (c)/(d): they must reproduce the planning arm's per-unit marginals.
    pb = gen_planning(0)
    mc = base_shuffled_time(0); md = base_matched_marginal(0)
    shuf_marg_ok = np.allclose(np.sort(pb.mean(0)), np.sort(mc.mean(0)))  # shuffle preserves marginals exactly
    print(f"  shuffled-time preserves planning marginals: {shuf_marg_ok}  "
          f"(plan ON={np.round(pb.mean(0),3)} shuf ON={np.round(mc.mean(0),3)} matched-marg ON={np.round(md.mean(0),3)})")
    ok = ok and eng_det and det_base and shuf_marg_ok
    print(f"  EQUIVALENCE + GENERATOR-VALIDITY PROOF: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/generator proof failed — aborting")
    print()

    # ── score the FIXED planning arm ONCE (same seeds reused for every baseline contrast). ──
    print("################ FIXED INTERVENTION = planning (depth-8 deliberation) ################")
    t0 = time.time()
    plan_rows = []
    for s in range(N_SEEDS):
        plan_rows.append(reads_from_bits(gen_planning(s)))
        print(f"    [planning seed {s+1}/{N_SEEDS}] elapsed={time.time()-t0:6.1f}s", flush=True)
    PI = _agg(plan_rows)
    print(f"  planning arm: big-Phi mean={PI['big'].mean():.4f}±{PI['big'].std():.4f}  "
          f"faithful mean={PI['faith'].mean():.6f}±{PI['faith'].std():.6f}")
    print()

    BASELINES = [
        ("independent-bits",       base_independent_bits,   "H_1033/H_1023 indep noisy coins (no structure)"),
        ("pre-rollout-latent",     base_pre_rollout_latent, "A-PRIORI PICK: model's own state BEFORE rollout (GREEDY)"),
        ("shuffled-time",          base_shuffled_time,      "planning bits, time axis permuted (marginals kept)"),
        ("matched-marginal-corr",  base_matched_marginal,   "per-step indep draws matching planning marginals"),
    ]
    results = {}
    for name, gen, note in BASELINES:
        print(f"################ BASELINE = {name}  [{note}] ################")
        r = score_baseline(name, gen, plan_rows, t0)
        results[name] = r
        bs = signword(r["big"]["contrast"]); fs = signword(r["faith"]["contrast"])
        down = is_big_down(r); fup = is_faith_up(r)
        print(f"  --- planning − {name} (matched n=4, 30 seeds) ---")
        print(f"     big-Phi      contrast={r['big']['contrast']:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {bs}")
        print(f"     faithful_phi contrast={r['faith']['contrast']:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {fs}")
        print(f"     bigΦ-DOWN? (d<={D_DOWN} AND mean<0): {down}   faithful-UP? (mean>0): {fup}")
        print(f"     [base big-Phi={r['big']['base']:.4f} faithful={r['faith']['base']:.6f}]")
        print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER TEST
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 88)
    print("BASELINE-REGIME CONTRAST MATRIX — planning − baseline (FIXED planning intervention)")
    print("=" * 88)
    print(f"  {'baseline':24s} | {'bigΦ d':>8s} | {'bigΦ ctr':>9s} | {'DOWN?':>6s} | {'faith d':>8s} | {'faith ctr':>10s} | {'fUP?':>5s}")
    for name, gen, note in BASELINES:
        r = results[name]
        print(f"  {name:24s} | {r['big']['d']:+8.3f} | {r['big']['contrast']:+9.4f} | "
              f"{str(is_big_down(r)):>6s} | {r['faith']['d']:+8.3f} | {r['faith']['contrast']:+10.4f} | "
              f"{str(is_faith_up(r)):>5s}")
    print()

    pre = results["pre-rollout-latent"]
    pre_down = is_big_down(pre)
    pre_fup = is_faith_up(pre)
    other_names = [n for (n, _, _) in BASELINES if n != "pre-rollout-latent"]
    other_not_down = [n for n in other_names if not is_big_down(results[n])]
    all_down = all(is_big_down(results[n]) for (n, _, _) in BASELINES)
    any_down = any(is_big_down(results[n]) for (n, _, _) in BASELINES)

    print(f"  A-PRIORI baseline = pre-rollout-latent: bigΦ-DOWN={pre_down} (d={pre['big']['d']:+.3f}), "
          f"faithful-UP={pre_fup} (contrast={pre['faith']['contrast']:+.4f})")
    print(f"  OTHER baselines NOT making bigΦ-DOWN: {other_not_down}")
    print(f"  bigΦ-DOWN under ANY baseline: {any_down} | under ALL baselines: {all_down}")
    print()

    pass_cond = pre_down and pre_fup and (len(other_not_down) >= 1)

    print("=" * 88)
    if pass_cond:
        print("OVERALL: 🟢 BASELINE-REGIME-SPECIFIC — the A-PRIORI pre-rollout-latent baseline makes")
        print("  big-Phi go DOWN (d<=-0.8) AND faithful go UP under the FIXED planning intervention,")
        print("  while at least one OTHER baseline regime does NOT make big-Phi go DOWN. The split's")
        print("  big-Phi-DOWN half is a planning-vs-(pre-rollout-latent) property — the H_1033 residual")
        print("  is pinned: the SIGN is dominated by the BASELINE CONTRAST (the model's own prior state),")
        print("  not by generic task decomposability. NOT regime-independent.")
        print("  VERDICT-TOKEN: BASELINE-REGIME-SPECIFIC")
    else:
        if not any_down:
            why = ("big-Phi-DOWN appears under NO baseline regime (incl. the a-priori pre-rollout-latent) "
                   "-> the DOWN half does not reproduce against the fixed planning arm at this rung")
        elif all_down:
            why = ("big-Phi-DOWN appears under ALL baseline regimes -> the DOWN half is regime-INDEPENDENT, "
                   "not specific to the pre-rollout-latent contrast")
        elif not pre_down:
            why = ("the a-priori pre-rollout-latent baseline does NOT make big-Phi go DOWN (d>%.1f or mean>=0) "
                   "-> the pre-registered a-priori pick fails its own falsifier" % D_DOWN)
        elif not pre_fup:
            why = ("the a-priori pre-rollout-latent baseline makes big-Phi DOWN but faithful does NOT go UP "
                   "-> the split (opposite-sign) requirement is not met")
        else:
            why = "no OTHER baseline differs from the pre-rollout-latent pattern -> not baseline-specific"
        print("OVERALL: 🔴 NOT-BASELINE-SPECIFIC (CLOSED-NEGATIVE) —", why + ".")
        print("  H_1033's degeneracy is structural, not a baseline choice (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: NOT-BASELINE-SPECIFIC")
    print("=" * 88)
    _scope()

def _scope():
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for 4 baselines x 30 seeds. Both CPU mirrors")
    print("RE-PROVEN == stdlib at n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring; SERIAL only")
    print("(no Pool — H_1038 hang). The planning intervention + latent->bits discretization are the")
    print("VERBATIM H_973/H_1004 ones; Phi from the stdlib mirrors ONLY (NOT a proxy, a_phi_iit4_tool).")
    print("Scale-transfer UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7). NOT a forge binary;")
    print("$0 CPU-local, no GPU.")

if __name__ == "__main__":
    main()
