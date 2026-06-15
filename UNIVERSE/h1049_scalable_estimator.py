"""H_1049 — Scalable validated Phi estimator: does an information-bottleneck (IB)
coarse-grain stay within epsilon of EXACT Phi on a validation ladder n=4..8?

CONSTRUCTIVE hypothesis. Exact IIT-4.0 is feasible only at small n (big-Phi super-exp,
cap n<=6; faithful phi_EI MIP exact only n<=8). A PRINCIPLED coarse-graining (information-
bottleneck macro-map: pick the m<=6 macro-units preserving the most predictive info about
the system's future) should give a Phi ESTIMATE within a fixed epsilon of the EXACT Phi
on a validation ladder N=4..8, and is the scalable ruler's measurement core.

GROUND TRUTH = stdlib faithful_phi (exact phi_EI, exact n<=8) on the FULL N-unit system.
ESTIMATE    = faithful_phi on the m=4 macro-unit coarse-grain (IB / top-var / random).

REUSES (a_phi_iit4_tool, no proxy):
  - H_1004 engines (faithful_phi) + planning_trajectories harness (VERBATIM)
  - H_1012 prove_mirrors_at_n (re-prove mirror == stdlib at n=4 AND n=5 BEFORE scoring)
  - H_1037/H_1038 majority-vote macro coarse-grain (here with an IB group-selection rule)

PRE-REGISTERED FALSIFIER (frozen in UNIVERSE/cards/H_1049_scalable_estimator.md, TEXT tokens):
  epsilon = 0.15. H1 PASS = IB relative error <= 0.15 at EVERY genuine rung N in {5,6,7,8}
  AND IB strictly beats random control at every such rung AND IB error does NOT grow with N
  (N=8 error not the largest) -> a validated scalable estimator exists. H1 FAIL otherwise
  (publishable closed-negative; report smallest satisfied epsilon + whether IB beats random).

g5 CODE-measured (no LLM self-judge, p7). a_scale_honest_scope: validated n<=8 only;
real-model fidelity UNVERIFIED (gates H_1038/H_1042). $0 CPU-local. NOT a forge binary.
"""
import sys, os, math, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
sys.path.insert(0, HERE)

# Import the REAL module by its REAL name (a_phi_iit4_tool; no importlib custom-name).
import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402

faithful_phi = h1004.faithful_phi
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ── PRE-FROZEN parameters ──────────────────────────────────────────────────
N_SEEDS = 30
PLAN_DEPTH = 8
MACRO = 4                 # FIXED macro-unit count (estimator output dim held constant)
LADDER = [4, 5, 6, 7, 8]  # GROUND-TRUTH full-system sizes (exact faithful phi_EI, n<=8)
EPSILON = 0.15            # pre-registered tolerance |Delta|/Phi
N_RANDOM_PARTITIONS = 8   # control: average over this many random partitions
RANDOM_SEED0 = 20260608


# ═══════════════════════════════════════════════════════════════════════════
# Full micro-system bits at size N: top-N variance channels, binarized at median.
# (H_1004/H_1002/H_1012 latent_to_binary_seq_n path VERBATIM.)
# ═══════════════════════════════════════════════════════════════════════════
def full_bits(H, N):
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:N])
    chans = H[:, idx]
    med = np.median(chans, axis=0)
    bits = (chans > med).astype(int)   # (T x N)
    return bits


def phi_of_bits(bits):
    """Exact faithful phi_EI over the (T x n) binary units (n_bins=2)."""
    n = bits.shape[1]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    return faithful_phi(fstate, fn, fdim, 2)


# ═══════════════════════════════════════════════════════════════════════════
# MACRO COARSE-GRAIN — majority-vote grain (H_1037/H_1038), ties -> 0.
# A macro-map = a list `groups` of m disjoint non-empty index-lists partitioning {0..N-1}.
# macro_bits[:, g] = majority bit of the micro-units in group g at each step.
# ═══════════════════════════════════════════════════════════════════════════
def apply_macro_map(bits, groups):
    T = bits.shape[0]
    m = len(groups)
    macro = np.zeros((T, m), dtype=int)
    for g, members in enumerate(groups):
        sub = bits[:, members]              # (T x |group|)
        s = sub.sum(axis=1)
        thr = len(members) / 2.0
        macro[:, g] = (s > thr).astype(int)  # strict majority; tie -> 0
    return macro


# ── predictive-info surrogate I_pred(unit_trace_t ; full micro_{t+1}) ───────
def _mi_pair_binary(a, b):
    """MI (bits, n_bins=2) between two binary traces a,b of equal length (uses the
    H_1004 _mi_pair which bins at n_bins=2; binary data => exact contingency MI)."""
    return h1004._mi_pair(np.asarray(a, float), np.asarray(b, float), 2)


def _pred_info_of_trace(trace_t, future_bits):
    """I_pred surrogate: summed MI between a macro/group trace at t and EVERY micro
    unit's bit at t+1. trace_t = (T,), future_bits = (T x N). Aligns t with t+1."""
    a = trace_t[:-1]
    fut = future_bits[1:, :]
    tot = 0.0
    for u in range(fut.shape[1]):
        tot += _mi_pair_binary(a, fut[:, u])
    return tot


def _group_trace(bits, members):
    """majority-vote binary trace of a group of micro-units."""
    sub = bits[:, members]
    s = sub.sum(axis=1)
    thr = len(members) / 2.0
    return (s > thr).astype(int)


# ═══════════════════════════════════════════════════════════════════════════
# MACRO-MAP 1 — IB: greedy agglomerative merge LOSING THE LEAST predictive info.
# Start from N singletons; repeatedly merge the pair whose MERGED group RETAINS the
# most predictive info (max I_pred of the merged trace) until MACRO groups remain.
# ═══════════════════════════════════════════════════════════════════════════
def ib_macro_map(bits, m):
    N = bits.shape[1]
    future_bits = bits
    groups = [[i] for i in range(N)]
    if N <= m:
        return groups
    while len(groups) > m:
        best_gain = -1.0e308
        best_pair = (0, 1)
        ng = len(groups)
        for i in range(ng):
            for j in range(i + 1, ng):
                merged = groups[i] + groups[j]
                tr = _group_trace(bits, merged)
                ipred = _pred_info_of_trace(tr, future_bits)
                # merge that keeps the most predictive info in the merged macro-unit
                if ipred > best_gain:
                    best_gain = ipred
                    best_pair = (i, j)
        i, j = best_pair
        merged = groups[i] + groups[j]
        groups = [groups[k] for k in range(ng) if k not in (i, j)]
        groups.append(merged)
    return groups


# ═══════════════════════════════════════════════════════════════════════════
# MACRO-MAP 2 — top-var: the m highest-variance micro-units seed the m macro-units;
# each remaining unit folds into the variance-nearest seed.
# ═══════════════════════════════════════════════════════════════════════════
def topvar_macro_map(bits, m):
    N = bits.shape[1]
    if N <= m:
        return [[i] for i in range(N)]
    var = bits.astype(float).var(axis=0)
    order = np.argsort(var)[::-1]
    seeds = list(order[:m])
    groups = [[int(s)] for s in seeds]
    seed_var = np.array([var[s] for s in seeds])
    for u in order[m:]:
        d = np.abs(seed_var - var[u])
        g = int(np.argmin(d))
        groups[g].append(int(u))
    return groups


# ═══════════════════════════════════════════════════════════════════════════
# MACRO-MAP 3 — random CONTROL: uniformly random partition of N units into m
# non-empty groups (seeded). Returns ONE partition; caller averages over many.
# ═══════════════════════════════════════════════════════════════════════════
def random_macro_map(N, m, rng):
    if N <= m:
        return [[i] for i in range(N)]
    while True:
        assign = rng.integers(0, m, size=N)
        # ensure every group non-empty
        if len(set(assign.tolist())) == m:
            break
    groups = [[] for _ in range(m)]
    for u in range(N):
        groups[int(assign[u])].append(u)
    return groups


# ═══════════════════════════════════════════════════════════════════════════
# Per-seed Phi triples at one ladder rung N.
# ═══════════════════════════════════════════════════════════════════════════
def measure_rung(N, seeds=N_SEEDS):
    ground, est_ib, est_tv, est_rand = [], [], [], []
    for s in range(seeds):
        _Hg, Hp = planning_trajectories(s, PLAN_DEPTH)
        bits = full_bits(Hp, N)                      # (T x N) micro-system
        phi_g = phi_of_bits(bits)                    # EXACT ground truth
        # IB estimate
        g_ib = ib_macro_map(bits, MACRO)
        phi_ib = phi_of_bits(apply_macro_map(bits, g_ib))
        # top-var estimate
        g_tv = topvar_macro_map(bits, MACRO)
        phi_tv = phi_of_bits(apply_macro_map(bits, g_tv))
        # random control: average Phi over N_RANDOM_PARTITIONS partitions
        rng = np.random.default_rng(RANDOM_SEED0 + s * 131 + N)
        rphis = []
        for _ in range(N_RANDOM_PARTITIONS):
            g_r = random_macro_map(N, MACRO, rng)
            rphis.append(phi_of_bits(apply_macro_map(bits, g_r)))
        phi_r = float(np.mean(rphis))
        ground.append(phi_g); est_ib.append(phi_ib); est_tv.append(phi_tv); est_rand.append(phi_r)
    return (np.array(ground), np.array(est_ib), np.array(est_tv), np.array(est_rand))


def rel_err(est_mean, ground_mean):
    if abs(ground_mean) < 1e-12:
        return float("nan")
    return abs(est_mean - ground_mean) / abs(ground_mean)


def main():
    print("=" * 90)
    print("H_1049 — Scalable validated Phi estimator: IB coarse-grain within epsilon of EXACT?")
    print("substrate=CPU-mirror (numpy) — H_1004 faithful_phi engine + H_1012 mirror proof")
    print("faithful_phi (GROUND TRUTH, exact phi_EI n<=8): "
          "hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa")
    print(f"ladder N in {LADDER} (exact ground truth) | macro m={MACRO} fixed | seeds={N_SEEDS} "
          f"| plan depth={PLAN_DEPTH}")
    print(f"PRE-REG epsilon = {EPSILON} | macro-maps: IB (info-bottleneck) / top-var / random(control)")
    print("PASS = IB rel-err <= eps at every genuine rung N in {5,6,7,8} AND IB < random AND error not")
    print("       growing with N. FAIL otherwise (a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("=" * 90, flush=True)
    print()
    t0 = time.time()

    # ── STEP 0: RE-PROVE faithful_phi mirror == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE faithful_phi CPU mirror == stdlib (a_phi_iit4_tool) at n=4 AND n=5")
    print("         BEFORE scoring (H_1012 prove_mirrors_at_n discipline; LIVE stdlib refs):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # ── STEP 0b: coarse-grain read determinism guard (pure fn of micro-bits) ──
    print("STEP 0b — macro coarse-grain read determinism guard (pure fn of bits):", flush=True)
    _Hg, Hp = planning_trajectories(0, PLAN_DEPTH)
    b6 = full_bits(Hp, 6)
    g_ib = ib_macro_map(b6, MACRO)
    pa = phi_of_bits(apply_macro_map(b6, g_ib))
    pb = phi_of_bits(apply_macro_map(b6, ib_macro_map(b6, MACRO)))
    det_ok = abs(pa - pb) < 1e-12
    print(f"  IB macro re-run deterministic at N=6: {det_ok} (phi={pa:.9f}=={pb:.9f}, "
          f"|Delta|={abs(pa-pb):.2e})", flush=True)
    if not det_ok:
        print("  ABORT — coarse-grain read non-deterministic.")
        raise SystemExit(1)
    print()

    # ── STEP 1: score the ladder ──
    print(f"STEP 1 — score the validation ladder N in {LADDER} (exact ground truth, {N_SEEDS} seeds)")
    print(f"         {'N':>2s} | {'Phi_ground':>10s} | {'Phi_IB':>8s} | {'Phi_topvar':>10s} | "
          f"{'Phi_rand':>8s} | {'errIB':>7s} | {'errTV':>7s} | {'errRand':>7s}", flush=True)
    rows = []
    for N in LADDER:
        ground, ib, tv, rand = measure_rung(N)
        gm, im, tm, rm = ground.mean(), ib.mean(), tv.mean(), rand.mean()
        eib = rel_err(im, gm); etv = rel_err(tm, gm); erd = rel_err(rm, gm)
        # per-seed paired mean relative error (auxiliary)
        denom = np.where(np.abs(ground) < 1e-9, np.nan, np.abs(ground))
        eib_paired = float(np.nanmean(np.abs(ib - ground) / denom))
        erd_paired = float(np.nanmean(np.abs(rand - ground) / denom))
        genuine = (N > MACRO)
        rows.append(dict(N=int(N), genuine=bool(genuine),
                         phi_ground=float(gm), phi_ib=float(im), phi_topvar=float(tm),
                         phi_rand=float(rm), err_ib=float(eib), err_topvar=float(etv),
                         err_rand=float(erd), err_ib_paired=eib_paired, err_rand_paired=erd_paired))
        tag = "" if genuine else "  (identity rung; m==N)"
        print(f"         {N:>2d} | {gm:>10.5f} | {im:>8.5f} | {tm:>10.5f} | {rm:>8.5f} | "
              f"{eib:>7.4f} | {etv:>7.4f} | {erd:>7.4f}{tag}", flush=True)
    print()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER scoring (frozen; TEXT tokens only)
    # ═══════════════════════════════════════════════════════════════════════
    genuine_rows = [r for r in rows if r["genuine"]]
    ib_errs = [r["err_ib"] for r in genuine_rows]
    rand_errs = [r["err_rand"] for r in genuine_rows]
    Ns = [r["N"] for r in genuine_rows]

    within_eps = all(e <= EPSILON for e in ib_errs)
    beats_random = all(r["err_ib"] < r["err_rand"] for r in genuine_rows)
    # error not growing with N: the largest-N rung's error is not strictly the max
    max_err = max(ib_errs)
    err_at_maxN = ib_errs[Ns.index(max(Ns))]
    not_growing = (err_at_maxN <= max_err) and (err_at_maxN < max_err + 1e-12) and \
                  (err_at_maxN <= ib_errs[0] + 1e-9 or err_at_maxN != max_err)
    # simpler honest definition: N=8 error is NOT the unique largest across the ladder
    not_growing = (err_at_maxN < max_err - 1e-12) or (ib_errs.count(max_err) > 1) or \
                  (err_at_maxN <= np.median(ib_errs) + 1e-12)

    print("=" * 90)
    print(f"FALSIFIER (pre-registered, epsilon={EPSILON}):")
    print(f"  genuine-compression rungs N in {Ns} (m={MACRO} < N)")
    print(f"  IB rel-errs:     {[f'{e:.4f}' for e in ib_errs]}")
    print(f"  random rel-errs: {[f'{e:.4f}' for e in rand_errs]}")
    print(f"  [1] IB within epsilon at every genuine rung: {within_eps}")
    print(f"  [2] IB strictly beats random control at every genuine rung: {beats_random}")
    print(f"  [3] IB error not growing with N (N={max(Ns)} err={err_at_maxN:.4f} not the unique max "
          f"{max_err:.4f}): {not_growing}")
    PASS = bool(within_eps and beats_random and not_growing)
    print()
    if PASS:
        print("OVERALL: VALIDATED-SCALABLE-ESTIMATOR-EXISTS — the IB coarse-grain Phi estimate stays")
        print(f"  within epsilon={EPSILON} of the EXACT faithful phi_EI at every genuine rung N in {Ns},")
        print("  strictly beats the random-macro-map control, and its error does NOT grow with N. The")
        print("  IB (information-bottleneck) coarse-grain is a VALIDATED measurement core for a scalable")
        print("  consciousness ruler (validated to n<=8; real-model fidelity gates H_1038/H_1042).")
        print("  VERDICT-TOKEN: VALIDATED-SCALABLE-ESTIMATOR-EXISTS")
    else:
        # smallest epsilon the IB map DOES satisfy at every genuine rung
        eps_satisfied = max(ib_errs)
        print("OVERALL: NO-VALIDATED-ESTIMATOR (CLOSED-NEGATIVE) — the IB coarse-grain does NOT meet the")
        print(f"  pre-registered fidelity: within_eps={within_eps}, beats_random={beats_random}, "
              f"not_growing={not_growing}.")
        print(f"  Smallest epsilon the IB map satisfies at EVERY genuine rung: {eps_satisfied:.4f} "
              f"(vs pre-reg {EPSILON}).")
        print(f"  IB beats random at all genuine rungs: {beats_random} (a weaker honest partial result).")
        print("  The ruler cannot honestly extend past n<=8 at this fidelity yet (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: NO-VALIDATED-ESTIMATOR")
    print("=" * 90)
    print("HONEST scope (a_scale_honest_scope): validated to n<=8 ONLY (exact faithful phi_EI is the")
    print("ground truth, exact only n<=8 — no exact reference exists beyond N=8). Real-model fidelity")
    print("UNVERIFIED (gates H_1038/H_1042 macro-IIT honesty). TOY WM latent; production transfer")
    print("UNVERIFIED. faithful_phi mirror RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring")
    print("(a_phi_iit4_tool; no proxy). Coarse-grain read deterministic (pure fn of bits). g5")
    print("CODE-measured (no LLM self-judge, p7). NOT a forge binary; $0 CPU-local.")

    out = dict(ladder=LADDER, macro=MACRO, n_seeds=N_SEEDS, plan_depth=PLAN_DEPTH,
               epsilon=EPSILON, mirror_proven={int(k): bool(v) for k, v in proven.items()},
               det_ok=bool(det_ok), rows=rows,
               within_eps=bool(within_eps), beats_random=bool(beats_random),
               not_growing=bool(not_growing), PASS=PASS,
               verdict_token=("VALIDATED-SCALABLE-ESTIMATOR-EXISTS" if PASS else "NO-VALIDATED-ESTIMATOR"),
               total_wall_sec=time.time() - t0)
    outp = os.path.join(HERE, "h1049_scalable_estimator_result.json")
    with open(outp, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {outp}", flush=True)
    print(f"total wall {time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
