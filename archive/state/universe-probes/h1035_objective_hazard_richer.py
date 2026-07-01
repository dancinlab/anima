"""H_1035 — is the faithful_phi-vs-big-Phi OBJECTIVE hazard ROBUST + characterizable
over a RICHER policy space? (falsifiable; residual of H_1029)

MISSION
-------
H_1029 showed OBJECTIVE-HAZARD-REAL on a SMALL policy set (planning depth
{0,1,2,4,8} only): maximizing faithful_phi -> depth-2 (deliberate), maximizing
big-Phi -> greedy (no deliberation), divergent (depth_gap=2, JS=0.3048), each
measure higher under its own maximizer. OPEN residual: was that an artifact of the
tiny one-dimensional set, or is the conflict robust + characterizable? This probe
(a) widens the policy space to a 3-axis parameterized family (planning depth ×
exploration noise × greedy/plan mixing knob), and (b) sweeps a SCALARIZED combined
objective alpha*faithful + (1-alpha)*big-Phi to trace the trade-off (Pareto) frontier.

REUSE (verbatim, no reinvention) — the H_1004/H_1012/H_1014/H_1029 substrate
---------------------------------------------------------------------------
- The SAME LatentWorldModel + fit_engine + roll_latent / encode_seq primitives
  from H_1004 (imported through H_1014). The H_1029 planning_trajectories rollout
  is a special case of the parameterized rollout here at (explore=0.05, mix=0.0);
  this is asserted at runtime (REPRODUCE-H_1029 check) before the sweep.
- BOTH stdlib IIT-4.0 engines as the OBJECTIVE, no proxy (a_phi_iit4_tool):
  big-Phi  = stdlib iit4_bigphi.hexa (system Phi_s), CPU mirror.
  faithful = stdlib iit4/faithful_phi.hexa (MIP-EI scalar), CPU mirror.
  Both mirrors RE-PROVEN == stdlib at n=4 (H_1012 prove_mirrors_at_n) BEFORE scoring.

FROZEN policy space (declared in H_1035_*.md 2026-06-08, NOT rewritten here)
---------------------------------------------------------------------------
  depth   in {0, 1, 2, 4, 8}        (depth 0 == greedy)
  explore in {0.00, 0.05, 0.20}     (branch-perturbation noise; 0.05 == H_1029)
  mix     in {0.0, 0.5}             (greedy/plan blend; 0.0 == pure plan == H_1029)
  => 5 x 3 x 2 = 30 policies, N_SEEDS=30.

FROZEN alpha-sweep: J(alpha,pol)=alpha*faithful_norm + (1-alpha)*bigphi_norm, both
min-max normalized to [0,1] over the policy space; alpha-grid 0.0..1.0 step 0.1 (11).

FROZEN falsifier (declared BEFORE the run):
  DIVERGENT iff pol_F != pol_B AND behavioral_js >= JS_MIN(0.05).
  BOTH-MAXING policy exists iff some policy has faithful_norm >= 1-EPS AND
    bigphi_norm >= 1-EPS, EPS=0.05 (top-5% of BOTH measures).
  FRONTIER REAL iff NO both-maxing policy AND alpha-sweep selects >=2 distinct
    policies AND Pareto front has >=2 non-dominated policies.
  PASS = HAZARD-ROBUST-CONFLICTING : DIVERGENT AND FRONTIER REAL.
  FAIL = HAZARD-RESOLVES : both-maxing policy exists OR maximizers converge
    (closed-negative, a_paper_negative_ok).

p6/p7 honored: behavioral divergence + Phi trade-off only; no fine-tuned ethics,
no perplexity verdict (g5 CODE-measured). a_phi_iit4_tool: REAL engines, no proxy.
HONEST scope (a_scale_honest_scope): TOY n=4; scale-transfer UNVERIFIED; $0 CPU.
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# ── Import the H_1014 driver VERBATIM (imports H_1004 engines + harness +
#    the H_1012 prove_mirrors_at_n equivalence proof). No reinvention. ──
import importlib.util as _ilu
_h1014_path = os.path.join(HERE, "h1014_intervention_split_predictor.py")
_spec = _ilu.spec_from_file_location("h1014", _h1014_path)
_h1014 = _ilu.module_from_spec(_spec)
_src = open(_h1014_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1014_path, "exec"), _h1014.__dict__)

prove_mirrors_at_n = _h1014.prove_mirrors_at_n
substrate_reads = _h1014.substrate_reads              # H -> {big, faith, ...} (both engines)
latent_to_binary_seq = _h1014.latent_to_binary_seq    # H -> (bits n_steps x 4, n)
planning_trajectories = _h1014.planning_trajectories   # H_1029 rollout (for REPRODUCE check)
cohens_d = _h1014.cohens_d
welch_t = _h1014.welch_t
LATENT = _h1014.LATENT
# substrate primitives for the parameterized (richer) rollout — H_1004 verbatim
fit_engine = _h1014._h1004.fit_engine
IN_DIM = _h1014._h1004.IN_DIM
ROLL = _h1014._h1004.ROLL

# ── FROZEN richer policy space (H_1035_*.md). ──
DEPTHS = [0, 1, 2, 4, 8]            # depth 0 == greedy
EXPLORES = [0.00, 0.05, 0.20]       # 0.05 == H_1029 setting
MIXES = [0.0, 0.5]                  # 0.0 == pure plan == H_1029
N_SEEDS = 30

# ── FROZEN alpha-sweep + thresholds. ──
ALPHAS = [round(0.1 * i, 1) for i in range(11)]   # 0.0..1.0
JS_MIN = 0.05
EPS = 0.05
LOG2 = math.log(2.0)


def rich_rollout(seed, depth, explore, mix):
    """Parameterized rollout on the SAME H_1004 substrate (fit_engine + roll_latent).

    depth 0 == greedy: return the reactive-encoded trajectory H0 (no deliberation).
    depth>=1 == deliberative plan: 4 branches, each perturbed by `explore` noise,
       rolled `depth` steps via the learned latent transition operator (roll_latent).
       This is EXACTLY H_1029's planning_trajectories at explore=0.05, mix=0.0.
    mix>0 == blend `mix` fraction of the greedy reactive states into the plan rollout
       (a greedy/plan MIXING knob): the realized behavior interpolates plan<->greedy.
    Deterministic in (seed, depth, explore, mix)."""
    rng = np.random.default_rng(1000 + seed)            # H_1029 seeding, verbatim
    wm = fit_engine(rng, seed)
    start = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                      0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H0 = wm.encode_seq(start)                            # greedy reactive trajectory
    h0 = H0[-1]
    if depth == 0:
        return H0                                        # greedy == H_1029 greedy arm
    branches = 4                                         # H_1029 verbatim
    delib = []
    for b in range(branches):
        rb = np.random.default_rng(7000 + seed * 13 + b) # H_1029 verbatim branch seed
        h = h0.copy() + explore * rb.standard_normal(LATENT)
        for _ in range(depth):
            h = wm.roll_latent(h, 1)[0]
            delib.append(h.copy())
    H_plan = np.array(delib)
    if mix <= 0.0:
        return H_plan                                    # pure plan == H_1029 plan arm
    # MIXING knob: blend the greedy reactive states (tiled to match length) into the
    # plan rollout by fraction `mix`. interpolates realized behavior plan<->greedy.
    reps = int(math.ceil(H_plan.shape[0] / H0.shape[0]))
    H_greedy_tiled = np.tile(H0, (reps, 1))[: H_plan.shape[0]]
    return (1.0 - mix) * H_plan + mix * H_greedy_tiled


def state_hist_from_H(H):
    """Realized n=4 system-STATE distribution (measure-INDEPENDENT). H_1029 verbatim."""
    bits, n = latent_to_binary_seq(H)
    full = 2 ** n
    idx = np.zeros(bits.shape[0], dtype=np.int64)
    for u in range(n):
        idx += (bits[:, u].astype(np.int64) << u)
    return np.bincount(idx, minlength=full).astype(float)


def js_distance(p, q):
    """Jensen-Shannon DISTANCE (sqrt JS divergence, base-2) in [0,1]. H_1029 verbatim."""
    p = np.asarray(p, float); q = np.asarray(q, float)
    ps, qs = p.sum(), q.sum()
    if ps <= 0 or qs <= 0:
        return 0.0
    p, q = p / ps, q / qs
    m = 0.5 * (p + q)
    def _kl(a, b):
        s = 0.0
        for ai, bi in zip(a, b):
            if ai > 0 and bi > 0:
                s += ai * (math.log(ai / bi) / LOG2)
        return s
    jsd = 0.5 * _kl(p, m) + 0.5 * _kl(q, m)
    return math.sqrt(jsd) if jsd > 0 else 0.0


def policies():
    out = []
    for d in DEPTHS:
        for e in EXPLORES:
            for m in MIXES:
                out.append((d, e, m))
    return out


def pol_name(p):
    d, e, m = p
    base = "greedy" if d == 0 else f"depth-{d}"
    return f"{base},e={e:.2f},mix={m:.1f}"


def reproduce_h1029_check():
    """Assert the parameterized rollout at (explore=0.05, mix=0.0) reproduces the
    H_1029 planning_trajectories arms EXACTLY (greedy + plan), for a few seeds/depths."""
    ok = True
    for s in (0, 1, 7):
        for d in (0, 1, 2, 4, 8):
            Hg, Hp = planning_trajectories(s, d if d >= 1 else 1)
            ref = Hg if d == 0 else Hp
            got = rich_rollout(s, d, 0.05, 0.0)
            same = (got.shape == ref.shape) and np.allclose(got, ref, atol=1e-12)
            ok = ok and same
            if not same:
                print(f"  REPRODUCE-H_1029 MISMATCH seed={s} depth={d} "
                      f"shapes {got.shape} vs {ref.shape}")
    return ok


def main():
    print("=" * 84)
    print("H_1035 — is the Phi OBJECTIVE hazard ROBUST + characterizable over a RICHER policy space?")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof (via H_1014), RE-PROVEN == stdlib n=4")
    print("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s) — OBJECTIVE (no proxy)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar) — OBJECTIVE")
    print(f"RICHER policy space = depth{DEPTHS} x explore{EXPLORES} x mix{MIXES} = "
          f"{len(DEPTHS)*len(EXPLORES)*len(MIXES)} policies x {N_SEEDS} seeds")
    print(f"alpha-sweep J=alpha*faithful_norm+(1-alpha)*bigphi_norm, alpha-grid {ALPHAS}")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | p6 | a_scale_honest_scope")
    print("PASS=HAZARD-ROBUST-CONFLICTING (maximizers divergent + real trade-off frontier, no both-maxing policy)")
    print("FAIL=HAZARD-RESOLVES (a both-maxing policy exists OR maximizers converge; a_paper_negative_ok)")
    print(f"FROZEN: JS_MIN={JS_MIN}  EPS={EPS} (both-maxing = top-{int(EPS*100)}% of BOTH on min-max norm)")
    print("=" * 84)
    print()

    # STEP 0 — equivalence proof at n=4 (H_1012 discipline) BEFORE scoring.
    print("EQUIVALENCE PROOF at n=4 (H_1012 prove_mirrors_at_n — re-prove BOTH mirrors vs stdlib):")
    ok = prove_mirrors_at_n(4)
    rng = np.random.default_rng(20260608)
    H = rng.standard_normal((40, LATENT))
    r1 = substrate_reads(H); r2 = substrate_reads(H)
    det = (abs(r1["faith"] - r2["faith"]) < 1e-12 and abs(r1["big"] - r2["big"]) < 1e-12)
    a = np.array([1.0, 0, 0, 0] + [0] * 12); b = np.array([0, 0, 0, 1.0] + [0] * 12)
    js_ok = (abs(js_distance(a, a)) < 1e-9 and abs(js_distance(a, b) - 1.0) < 1e-9)
    print(f"  both-measure deterministic re-run: {det}  faith={r1['faith']:.6f} big={r1['big']:.6f}")
    print(f"  JS-distance sanity: JS(p,p)={js_distance(a,a):.6f} JS(disjoint)={js_distance(a,b):.6f} ok={js_ok}")
    print("  REPRODUCE-H_1029: parameterized rollout @ (explore=0.05, mix=0.0) == planning_trajectories arms:")
    rep = reproduce_h1029_check()
    print(f"    REPRODUCE-H_1029 (greedy+plan arms, seeds {{0,1,7}} x depths {{0,1,2,4,8}}): "
          f"{'EXACT' if rep else 'MISMATCH'}")
    ok = ok and det and js_ok and rep
    print(f"  EQUIVALENCE + METRIC + REPRODUCE PROOF n=4: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/metric/reproduce proof failed — aborting")
    print()

    # ── POLICY SEARCH over the RICHER frozen space. ──
    POLS = policies()
    print(f"POLICY SEARCH over RICHER space ({len(POLS)} policies x {N_SEEDS} seeds; "
          f"SAME engines, only the policy params differ):")
    t0 = time.time()
    scored = {}
    for pi, p in enumerate(POLS):
        d, e, m = p
        faiths, bigs = [], []
        pooled = np.zeros(16, dtype=float)
        for s in range(N_SEEDS):
            H = rich_rollout(s, d, e, m)
            r = substrate_reads(H)
            faiths.append(r["faith"]); bigs.append(r["big"])
            pooled += state_hist_from_H(H)
        scored[p] = dict(faith=np.array(faiths), big=np.array(bigs), state_hist=pooled)
        print(f"  [{pi+1:2d}/{len(POLS)}] {pol_name(p):28s} "
              f"mean_faith={scored[p]['faith'].mean():7.4f} mean_big={scored[p]['big'].mean():8.4f} "
              f"elapsed={time.time()-t0:6.1f}s", flush=True)
    print()

    faith_mean = {p: scored[p]["faith"].mean() for p in POLS}
    big_mean = {p: scored[p]["big"].mean() for p in POLS}

    # ── min-max NORMALIZE each measure over the policy space (frozen). ──
    fvals = np.array([faith_mean[p] for p in POLS])
    bvals = np.array([big_mean[p] for p in POLS])
    fmin, fmax = fvals.min(), fvals.max()
    bmin, bmax = bvals.min(), bvals.max()
    fnorm = {p: (faith_mean[p] - fmin) / (fmax - fmin + 1e-12) for p in POLS}
    bnorm = {p: (big_mean[p] - bmin) / (bmax - bmin + 1e-12) for p in POLS}

    # ── maximizers. ──
    pol_F = max(POLS, key=lambda p: faith_mean[p])
    pol_B = max(POLS, key=lambda p: big_mean[p])
    print("=" * 84)
    print("MAXIMIZERS over the RICHER policy space")
    print("=" * 84)
    print(f"  OBJECTIVE F (maximize faithful_phi) selects: {pol_name(pol_F)}  "
          f"(faith={faith_mean[pol_F]:.4f}, big={big_mean[pol_F]:.4f})")
    print(f"  OBJECTIVE B (maximize big-Phi)      selects: {pol_name(pol_B)}  "
          f"(faith={faith_mean[pol_B]:.4f}, big={big_mean[pol_B]:.4f})")
    print()

    # ── behavioral divergence (measure-INDEPENDENT). ──
    behav_js = js_distance(scored[pol_F]["state_hist"], scored[pol_B]["state_hist"])
    distinct = (pol_F != pol_B)
    divergent = distinct and (behav_js >= JS_MIN)
    print("BEHAVIORAL DIVERGENCE (what the two maximizers DO — measure-independent):")
    print(f"  distinct policy tuple: {distinct}  (pol_F={pol_name(pol_F)} vs pol_B={pol_name(pol_B)})")
    print(f"  behavioral_js (JS distance of realized n=4 state distributions, bits) = {behav_js:.4f}  "
          f"(threshold >= {JS_MIN}: {behav_js >= JS_MIN})")
    print(f"  DIVERGENT: {divergent}")
    print()

    # ── BOTH-MAXING policy? (top-EPS of BOTH measures on the normalized scale). ──
    both_maxers = [p for p in POLS if fnorm[p] >= 1 - EPS and bnorm[p] >= 1 - EPS]
    both_maxing_exists = len(both_maxers) > 0
    print(f"BOTH-MAXING policy (faithful_norm>=1-{EPS} AND bigphi_norm>=1-{EPS}, i.e. top-{int(EPS*100)}% of BOTH):")
    if both_maxing_exists:
        for p in both_maxers:
            print(f"  FOUND: {pol_name(p)}  faith_norm={fnorm[p]:.4f} big_norm={bnorm[p]:.4f}")
    else:
        print("  NONE — no single policy is in the top-5% of BOTH measures simultaneously.")
    print(f"  BOTH-MAXING policy exists: {both_maxing_exists}")
    print()

    # ── alpha-sweep: does the combined optimum MOVE? ──
    print("=" * 84)
    print("ALPHA-SWEEP  J(alpha,pol) = alpha*faithful_norm + (1-alpha)*bigphi_norm  (argmax per alpha)")
    print("=" * 84)
    alpha_winners = []
    for al in ALPHAS:
        J = {p: al * fnorm[p] + (1 - al) * bnorm[p] for p in POLS}
        w = max(POLS, key=lambda p: J[p])
        alpha_winners.append(w)
        print(f"  alpha={al:.1f}  ->  {pol_name(w):28s}  "
              f"J={J[w]:.4f}  (faith_norm={fnorm[w]:.3f} big_norm={bnorm[w]:.3f})")
    distinct_alpha = []
    for w in alpha_winners:
        if w not in distinct_alpha:
            distinct_alpha.append(w)
    n_distinct_alpha = len(distinct_alpha)
    alpha_moves = n_distinct_alpha >= 2
    print(f"  distinct policies selected across the alpha-sweep: {n_distinct_alpha} "
          f"({[pol_name(p) for p in distinct_alpha]})")
    print(f"  alpha-optimum MOVES (>=2 distinct): {alpha_moves}")
    print()

    # ── Pareto front over (faithful_norm, bigphi_norm). ──
    def dominated(p, q):
        # q dominates p iff q >= p on both and strictly > on at least one
        return (fnorm[q] >= fnorm[p] and bnorm[q] >= bnorm[p] and
                (fnorm[q] > fnorm[p] or bnorm[q] > bnorm[p]))
    pareto = [p for p in POLS if not any(dominated(p, q) for q in POLS if q != p)]
    n_pareto = len(pareto)
    pareto_multi = n_pareto >= 2
    print(f"PARETO FRONT over (faithful_norm, bigphi_norm): {n_pareto} non-dominated policies")
    for p in sorted(pareto, key=lambda p: fnorm[p]):
        print(f"  {pol_name(p):28s}  faith_norm={fnorm[p]:.4f}  big_norm={bnorm[p]:.4f}")
    print(f"  Pareto front has >=2 non-dominated policies: {pareto_multi}")
    print()

    frontier_real = (not both_maxing_exists) and alpha_moves and pareto_multi
    print(f"TRADE-OFF FRONTIER REAL (no both-maxing AND alpha moves AND >=2 Pareto): {frontier_real}")
    print()

    # ── cross-eval audit of the two maximizers. ──
    fF, fB = faith_mean[pol_F], faith_mean[pol_B]
    bF, bB = big_mean[pol_F], big_mean[pol_B]
    print("2x2 CROSS-EVAL (mean over seeds): each measure under each maximizer")
    print(f"  policy_F={pol_name(pol_F):28s} faith={fF:8.4f} big={bF:8.4f}")
    print(f"  policy_B={pol_name(pol_B):28s} faith={fB:8.4f} big={bB:8.4f}")
    print(f"  Delta (F-B): faith={fF-fB:+.4f}  big={bF-bB:+.4f}")
    _, p_faith = welch_t(scored[pol_F]["faith"], scored[pol_B]["faith"])
    _, p_big = welch_t(scored[pol_B]["big"], scored[pol_F]["big"])
    d_faith = cohens_d(scored[pol_F]["faith"], scored[pol_B]["faith"])
    d_big = cohens_d(scored[pol_B]["big"], scored[pol_F]["big"])
    print(f"  (audit) faithful F-B: d={d_faith:+.3f} p={p_faith:.3e} | big-Phi B-F: d={d_big:+.3f} p={p_big:.3e}")
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # VERDICT — PASS iff DIVERGENT AND FRONTIER REAL (frozen falsifier).
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 84)
    hazard_robust = divergent and frontier_real
    if hazard_robust:
        print("OVERALL: HAZARD-ROBUST-CONFLICTING — over the RICHER policy space the two Phi objectives")
        print(f"  STAY divergent (faithful->{pol_name(pol_F)}, big-Phi->{pol_name(pol_B)}, "
              f"behavioral_js={behav_js:.4f}); NO single policy maxes BOTH (no top-5% both-maxer); the")
        print(f"  alpha-sweep optimum MOVES across {n_distinct_alpha} distinct policies and the Pareto")
        print(f"  front holds {n_pareto} non-dominated policies. The H_1029 hazard is NOT a small-set")
        print("  artifact: the two Phi objectives are genuinely CONFLICTING on a real trade-off frontier.")
        print("  VERDICT-TOKEN: HAZARD-ROBUST-CONFLICTING")
    else:
        print("OVERALL: HAZARD-RESOLVES (CLOSED-NEGATIVE) — the richer policy space either finds a")
        print(f"  (near-)both-maxing policy (both_maxing_exists={both_maxing_exists}) or the maximizers")
        print(f"  converge (divergent={divergent}). The H_1029 hazard does NOT survive the richer space")
        print("  as a genuine trade-off: the objective hazard was a small-set artifact (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: HAZARD-RESOLVES")
    print("=" * 84)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 — both engines EXACT;")
    print("big-Phi super-exponential so n=4 is the rung for the 30-policy x 30-seed sweep. Both CPU")
    print("mirrors RE-PROVEN == stdlib at n=4 (H_1012) + REPRODUCE-H_1029 EXACT BEFORE scoring; the REAL")
    print("engines are the objective (a_phi_iit4_tool, NO proxy). min-max norm is over THIS policy space.")
    print("p6 (no fine-tuned ethics) + p7 (no perplexity verdict) honored. g5 CODE-measured (no LLM")
    print("self-judge). Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, serial, no GPU.")


if __name__ == "__main__":
    main()
