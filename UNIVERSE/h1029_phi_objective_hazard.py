"""H_1029 — is "maximize Phi" a measure-dependent OBJECTIVE hazard? (falsifiable)

MISSION (the paper's Discussion remark, made a behavioral measurement)
---------------------------------------------------------------------
PAPER/phi-measure-dependence-planning argues, in Discussion ONLY, that wiring
"Phi" into an agent objective is hazardous because faithful_phi and big-Phi
disagree: maximizing the MIP-EI scalar (faithful_phi) rewards deliberation
(redundancy-raising), while maximizing the system structure (big-Phi) penalizes
the SAME deliberation when it modularizes the system (H_1012 split + H_1017
redundancy mechanism). That is asserted as a design hazard but never MEASURED.

This probe makes it a falsifiable BEHAVIORAL result: on ONE planning-control
substrate, run two policy searches over a single PRE-FROZEN policy set that
differ ONLY in the objective — (A) reward = faithful_phi, (B) reward = big-Phi
— select the maximizing policy under each objective, and compare what the two
maximizers actually DO (realized planning behavior), plus cross-evaluate each
measure under both selected policies.

REUSE (verbatim, no reinvention) — the H_1012/H_1014/H_1017 substrate
--------------------------------------------------------------------
- The SAME LatentWorldModel + planning_trajectories(seed, depth) rollouts from
  H_1004 (imported through H_1014). The "policy" is the planning DEPTH parameter
  (how deeply the agent deliberates before committing) — the depth-ladder policy
  family that already exists in the substrate. depth 0 == the greedy (no-plan)
  policy; depths {1,2,4,8} are the deliberative policies. THIS IS THE FROZEN SET.
- BOTH stdlib IIT-4.0 engines as the OBJECTIVE, no proxy (a_phi_iit4_tool):
  big-Phi  = stdlib iit4_bigphi.hexa  (system Phi_s), CPU mirror.
  faithful = stdlib iit4/faithful_phi.hexa (MIP-EI scalar), CPU mirror.
  Both mirrors are RE-PROVEN == stdlib at n=4 (H_1012 prove_mirrors_at_n) BEFORE
  any policy is scored. NO variance*energy proxy; the REAL engines are the reward.

THE POLICY SEARCH (E5) — identical setup, ONLY the objective differs
-------------------------------------------------------------------
For every policy (depth) in the frozen set, roll the SAME substrate over N_SEEDS
seeds and read BOTH measures off the ONE matched n=4 binary discretization.
  objective A (faithful-maximizer): argmax_policy mean_over_seeds faithful_phi
  objective B (big-Phi-maximizer):  argmax_policy mean_over_seeds big_phi
The two searches see the EXACT same rollouts; the ONLY difference is which scalar
is the reward. This is the cleanest possible test of "the measure you optimize
changes what the agent does".

PRE-REGISTERED FALSIFIER (frozen 2026-06-07 in H_1029_*.md — NOT rewritten here)
-------------------------------------------------------------------------------
PASS = OBJECTIVE-HAZARD-REAL : the two maximizers select DIVERGENT behavior
  (frozen divergence metric exceeds threshold) AND each measure is higher under
  its OWN maximizer (the 2x2 cross-eval diagonal dominates its column).
FAIL = OBJECTIVES-CONVERGE : both objectives select near-identical policies
  (closed-negative, a_paper_negative_ok).

FROZEN divergence metric + threshold (declared BEFORE the run):
  - selected_depth_gap = | depth*(faithful) - depth*(big-Phi) | (policy-id gap), and
  - behavioral_js = Jensen-Shannon distance (bits, base-2, in [0,1]) between the
    realized n=4 system-STATE distributions of the two selected policies' rollouts
    (pooled over seeds) — a measure-INDEPENDENT read of what the agent DOES.
  DIVERGENT iff selected_depth_gap >= 1 (the two objectives pick DIFFERENT policies)
  AND behavioral_js >= 0.05 (their realized behavior is materially different).
  CROSS-EVAL self-preference iff faithful(pol_A) > faithful(pol_B) AND
  big(pol_B) > big(pol_A) (each measure strictly higher under its own maximizer).
  PASS iff DIVERGENT AND self-preference both hold.

p6/p7 honored: this measures behavioral divergence under two honest Phi
objectives, nothing else. No fine-tuned ethics; no perplexity verdict (g5
CODE-measured, no LLM self-judge). a_phi_iit4_tool: REAL engines, no proxy.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines
EXACT; big-Phi super-exponential so n=4 is the rung for the full policy set x
seeds. Mirrors RE-PROVEN == stdlib at n=4 BEFORE scoring. Scale-transfer
UNVERIFIED. NOT a forge binary; $0 CPU-local, serial, no GPU, polled inline.
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# ── Import the H_1014 driver VERBATIM (it imports H_1004 engines + harness +
#    the H_1012 prove_mirrors_at_n equivalence proof). No reinvention. ──
import importlib.util as _ilu
_h1014_path = os.path.join(HERE, "h1014_intervention_split_predictor.py")
_spec = _ilu.spec_from_file_location("h1014", _h1014_path)
_h1014 = _ilu.module_from_spec(_spec)
_src = open(_h1014_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1014_path, "exec"), _h1014.__dict__)

prove_mirrors_at_n = _h1014.prove_mirrors_at_n
planning_trajectories = _h1014.planning_trajectories  # (seed, depth) -> (H_greedy, H_plan)
substrate_reads = _h1014.substrate_reads              # H -> {big, faith, ...} (both engines)
latent_to_binary_seq = _h1014.latent_to_binary_seq    # H -> (bits n_steps x 4, n)
cohens_d = _h1014.cohens_d
welch_t = _h1014.welch_t
LATENT = _h1014.LATENT

# ── FROZEN policy set: planning DEPTH is the policy. depth 0 = greedy (no-plan);
#    depths {1,2,4,8} = deliberative policies. This is the substrate's existing
#    depth-ladder policy family (H_1004 planning_trajectories). n=4 policies + greedy.
POLICY_DEPTHS = [0, 1, 2, 4, 8]   # 0 == greedy
N_SEEDS = 30                       # multi-seed (matches the substrate's N_SEEDS)

# ── FROZEN divergence thresholds (declared before the run). ──
DEPTH_GAP_MIN = 1       # objectives must pick DIFFERENT policies
JS_MIN = 0.05           # realized behavior must differ (Jensen-Shannon bits)

LOG2 = math.log(2.0)


def policy_rollout(seed, depth):
    """Roll the substrate under one policy (planning depth). depth 0 == the greedy
    (no-deliberation) policy; depth>=1 == the depth-deep deliberative policy. Uses
    planning_trajectories VERBATIM (greedy arm for depth 0, plan arm otherwise)."""
    Hg, Hp = planning_trajectories(seed, depth if depth >= 1 else 1)
    return Hg if depth == 0 else Hp


def state_hist_from_H(H):
    """Realized n=4 system-STATE distribution of a rollout: the matched binary
    discretization → integer state index 0..15 per step → empirical histogram.
    This is a measure-INDEPENDENT read of what the policy DOES (behavior), not Phi."""
    bits, n = latent_to_binary_seq(H)
    full = 2 ** n
    idx = np.zeros(bits.shape[0], dtype=np.int64)
    for u in range(n):
        idx += (bits[:, u].astype(np.int64) << u)
    h = np.bincount(idx, minlength=full).astype(float)
    return h  # un-normalized counts (pooled later, then normalized)


def js_distance(p, q):
    """Jensen-Shannon DISTANCE (sqrt of JS divergence, base-2) in [0,1] between two
    state distributions. JSD = 0.5 KL(p||m) + 0.5 KL(q||m), m=(p+q)/2 (bits)."""
    p = np.asarray(p, float); q = np.asarray(q, float)
    ps = p.sum(); qs = q.sum()
    if ps <= 0 or qs <= 0:
        return 0.0
    p = p / ps; q = q / qs
    m = 0.5 * (p + q)
    def _kl(a, b):
        s = 0.0
        for ai, bi in zip(a, b):
            if ai > 0 and bi > 0:
                s += ai * (math.log(ai / bi) / LOG2)
        return s
    jsd = 0.5 * _kl(p, m) + 0.5 * _kl(q, m)   # in [0,1] bits
    if jsd < 0:
        jsd = 0.0
    return math.sqrt(jsd)


def score_policy_set(t0):
    """For each policy (depth) roll N_SEEDS seeds, read BOTH measures off the ONE
    matched discretization, and accumulate the pooled realized state histogram.
    Returns per-policy arrays {depth: dict(faith[], big[], state_hist)}."""
    out = {}
    for d in POLICY_DEPTHS:
        faiths, bigs = [], []
        pooled = np.zeros(16, dtype=float)
        for s in range(N_SEEDS):
            H = policy_rollout(s, d)
            r = substrate_reads(H)              # both engines, SAME bits
            faiths.append(r["faith"]); bigs.append(r["big"])
            pooled += state_hist_from_H(H)
            print(f"    [policy depth={d} seed {s+1}/{N_SEEDS}] "
                  f"faith={r['faith']:.4f} big={r['big']:.4f} elapsed={time.time()-t0:6.1f}s",
                  flush=True)
        out[d] = dict(faith=np.array(faiths), big=np.array(bigs), state_hist=pooled)
    return out


def main():
    print("=" * 80)
    print("H_1029 — is 'maximize Phi' a measure-dependent OBJECTIVE hazard? (falsifiable)")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof (via H_1014), RE-PROVEN == stdlib at n=4")
    print("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s) — THE OBJECTIVE (no proxy)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar) — THE OBJECTIVE")
    print("policy = planning DEPTH (deliberation depth); FROZEN policy set = {0(greedy),1,2,4,8}")
    print("two policy searches differ ONLY in the objective; SAME rollouts, SAME seeds.")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | p6 | a_scale_honest_scope")
    print("PASS=OBJECTIVE-HAZARD-REAL (divergent policies + each measure higher under its own maximizer)")
    print("FAIL=OBJECTIVES-CONVERGE (near-identical policies; a_paper_negative_ok)")
    print(f"FROZEN divergence: selected_depth_gap>={DEPTH_GAP_MIN} AND behavioral_js>={JS_MIN}")
    print("=" * 80)
    print()

    # STEP 0 — equivalence proof at n=4 (H_1012 discipline) BEFORE scoring.
    print("EQUIVALENCE PROOF at n=4 (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    # determinism: both measures are a pure function of the SAME bits.
    rng = np.random.default_rng(20260607)
    H = rng.standard_normal((40, LATENT))
    r1 = substrate_reads(H); r2 = substrate_reads(H)
    det = (abs(r1["faith"] - r2["faith"]) < 1e-12 and abs(r1["big"] - r2["big"]) < 1e-12)
    # JS distance self-consistency sanity: JS(p,p)=0, JS(disjoint)=1.
    a = np.array([1.0, 0, 0, 0] + [0] * 12); b = np.array([0, 0, 0, 1.0] + [0] * 12)
    js_self = js_distance(a, a); js_disj = js_distance(a, b)
    js_ok = (abs(js_self) < 1e-9 and abs(js_disj - 1.0) < 1e-9)
    print(f"  both-measure deterministic re-run: {det}  faith={r1['faith']:.6f} big={r1['big']:.6f}")
    print(f"  JS-distance sanity: JS(p,p)={js_self:.6f} (expect 0)  JS(disjoint)={js_disj:.6f} (expect 1)  ok={js_ok}")
    ok = ok and det and js_ok
    print(f"  EQUIVALENCE + METRIC-VALIDITY PROOF n=4: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/metric proof failed — aborting")
    print()

    # ── POLICY SEARCH: score the FROZEN policy set under the SAME rollouts. ──
    print(f"POLICY SEARCH over frozen set {POLICY_DEPTHS} × {N_SEEDS} seeds "
          f"(SAME rollouts; only the objective differs):")
    t0 = time.time()
    scored = score_policy_set(t0)
    print()

    # per-policy mean of each measure
    faith_mean = {d: scored[d]["faith"].mean() for d in POLICY_DEPTHS}
    big_mean = {d: scored[d]["big"].mean() for d in POLICY_DEPTHS}

    print("=" * 80)
    print("PER-POLICY OBJECTIVE TABLE (mean over seeds; the search maximizes down each column)")
    print("=" * 80)
    print(f"  {'policy(depth)':>13s} | {'mean faithful_phi':>17s} | {'mean big-Phi':>13s}")
    for d in POLICY_DEPTHS:
        tagf = " <== argmax faithful" if d == max(faith_mean, key=faith_mean.get) else ""
        tagb = " <== argmax big-Phi" if d == max(big_mean, key=big_mean.get) else ""
        print(f"  {('greedy' if d==0 else 'depth-%d'%d):>13s} | {faith_mean[d]:17.4f} | {big_mean[d]:13.4f}"
              f"{tagf}{tagb}")
    print()

    # ── SELECT the maximizing policy under each objective. ──
    pol_A = max(faith_mean, key=faith_mean.get)   # faithful-maximizer
    pol_B = max(big_mean, key=big_mean.get)        # big-Phi-maximizer
    nameA = ("greedy" if pol_A == 0 else f"depth-{pol_A}")
    nameB = ("greedy" if pol_B == 0 else f"depth-{pol_B}")
    print(f"OBJECTIVE A (maximize faithful_phi) selects policy: {nameA} (depth={pol_A})")
    print(f"OBJECTIVE B (maximize big-Phi)      selects policy: {nameB} (depth={pol_B})")
    print()

    # ── BEHAVIORAL DIVERGENCE METRIC (measure-independent). ──
    depth_gap = abs(pol_A - pol_B)
    behav_js = js_distance(scored[pol_A]["state_hist"], scored[pol_B]["state_hist"])
    divergent = (depth_gap >= DEPTH_GAP_MIN) and (behav_js >= JS_MIN)
    print("BEHAVIORAL DIVERGENCE (what the two maximizers actually DO — measure-independent):")
    print(f"  selected_depth_gap = |{pol_A} - {pol_B}| = {depth_gap}  (threshold >= {DEPTH_GAP_MIN}: {depth_gap >= DEPTH_GAP_MIN})")
    print(f"  behavioral_js (JS distance of realized n=4 state distributions, bits) = {behav_js:.4f}  "
          f"(threshold >= {JS_MIN}: {behav_js >= JS_MIN})")
    print(f"  DIVERGENT (both thresholds): {divergent}")
    print()

    # ── 2x2 CROSS-EVALUATION MATRIX: each measure under each selected policy. ──
    fA = faith_mean[pol_A]; fB = faith_mean[pol_B]
    bA = big_mean[pol_A]; bB = big_mean[pol_B]
    print("=" * 80)
    print("2x2 CROSS-EVALUATION MATRIX (mean over seeds): each measure under each maximizer")
    print("=" * 80)
    print(f"  {'':>22s} | {'faithful_phi':>13s} | {'big-Phi':>10s}")
    print(f"  {('policy_A='+nameA):>22s} | {fA:13.4f} | {bA:10.4f}")
    print(f"  {('policy_B='+nameB):>22s} | {fB:13.4f} | {bB:10.4f}")
    print(f"  {'Δ (A − B)':>22s} | {fA-fB:+13.4f} | {bA-bB:+10.4f}")
    print()
    # self-preference: each measure strictly higher under its own maximizer.
    faith_self = fA > fB        # faithful higher under A (its maximizer)
    big_self = bB > bA          # big-Phi higher under B (its maximizer)
    self_pref = faith_self and big_self
    print(f"  faithful_phi higher under its own maximizer (A): {faith_self}  (Δ_faith(A−B)={fA-fB:+.4f})")
    print(f"  big-Phi      higher under its own maximizer (B): {big_self}  (Δ_big(B−A)={bB-bA:+.4f})")
    print(f"  SELF-PREFERENCE (each measure higher under its own maximizer): {self_pref}")
    print()

    # cross-eval Welch stats for the cross terms (audit)
    _, p_faith = welch_t(scored[pol_A]["faith"], scored[pol_B]["faith"])
    _, p_big = welch_t(scored[pol_B]["big"], scored[pol_A]["big"])
    d_faith = cohens_d(scored[pol_A]["faith"], scored[pol_B]["faith"])
    d_big = cohens_d(scored[pol_B]["big"], scored[pol_A]["big"])
    print(f"  (audit) faithful A−B: d={d_faith:+.3f} p={p_faith:.3e} | big-Phi B−A: d={d_big:+.3f} p={p_big:.3e}")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # VERDICT — PASS iff DIVERGENT AND SELF-PREFERENCE (frozen falsifier).
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 80)
    hazard_real = divergent and self_pref
    if hazard_real:
        print("OVERALL: 🟢 OBJECTIVE-HAZARD-REAL — two policy searches that differ ONLY in the")
        print("  objective (maximize faithful_phi vs maximize big-Phi) select DIVERGENT behavior")
        print(f"  on the SAME substrate: faithful picks {nameA}, big-Phi picks {nameB} "
              f"(depth_gap={depth_gap}, behavioral_js={behav_js:.4f}); AND each measure is HIGHER")
        print("  under its OWN maximizer (cross-eval diagonal dominates). The paper's Discussion")
        print("  remark — 'an agent that maximizes Phi pursues opposite policies depending on")
        print("  which Phi is wired into the objective' — is a MEASURED behavioral hazard, not a")
        print("  remark. The measure you optimize literally changes what the agent DOES.")
        print("  VERDICT-TOKEN: OBJECTIVE-HAZARD-REAL")
    else:
        print("OVERALL: 🔴 OBJECTIVES-CONVERGE (CLOSED-NEGATIVE) — the two objectives select")
        print(f"  near-identical policies (faithful->{nameA}, big-Phi->{nameB}, depth_gap={depth_gap},")
        print(f"  behavioral_js={behav_js:.4f}) and/or each measure is NOT higher under its own")
        print("  maximizer (self-preference fails). The H_1012/H_1017 measurement split does NOT")
        print("  translate to a behavioral objective hazard: optimizing either Phi yields the same")
        print("  behavior. The objective-hazard claim is FALSIFIED on this substrate")
        print("  (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: OBJECTIVES-CONVERGE")
    print("=" * 80)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for the full policy set x 30 seeds. Both CPU")
    print("mirrors RE-PROVEN == stdlib at n=4 (H_1012 prove_mirrors_at_n) BEFORE scoring; the REAL")
    print("engines are the objective (a_phi_iit4_tool, NO variance*energy proxy). p6 (no fine-tuned")
    print("ethics) + p7 (no perplexity verdict) honored — this measures behavioral divergence under")
    print("two honest Phi objectives only. The divergence metric (depth_gap + JS distance of realized")
    print("state distributions) is measure-INDEPENDENT. Scale-transfer UNVERIFIED. g5 CODE-measured")
    print("(no LLM self-judge). NOT a forge binary; $0 CPU-local, serial, no GPU.")


if __name__ == "__main__":
    main()
