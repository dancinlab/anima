"""H_1037 — does the planning Phi sign-split DISCRETIZATION-INVARIANCE (H_1024 🟢) ALSO
hold at n=6 EXACT (the largest exactly-computable system size), or was the n<=5 binning
invariance a small-n artifact?

FOLLOW-UP OF (both 🟢):
  H_1024  SIGN-DISCRETIZATION-INVARIANT — the planning faithful_phi-UP / big-Phi-DOWN
          sign-split holds for EVERY binning in a pre-frozen grid (nb in {2,3,4} x
          {equal_width, quantile} = 6 binnings), SCORED at n=4 (n=5 was the HONEST CAP:
          mirrors proven exact but the full grid INFEASIBLE @ $0 CPU on one Mac core).
  H_1022  SPLIT-PERSISTS-N6+ — the sign-split STRENGTHENS through n=6 EXACT (Cohen d
          -1.83 -> -2.28 -> -3.60) on a 96-core pod (n=6 EXACT = 150 evals in 3.16h).

RESIDUAL QUESTION (this rung):
  H_1024 only had the discretization grid at n<=5. Does the 6-binning sign-invariance
  ALSO hold at the n=6 EXACT scale? i.e. re-run the H_1024 6-binning robustness sweep at
  the n=6 EXACT scale (where big-Phi was the cap on a single Mac core, so it needs a
  many-core pod, exactly as H_1022 did for n=6).

WHAT VARIES (the ONLY thing): the DISCRETIZATION — VERBATIM the H_1024 pre-frozen grid.
WHAT CHANGES vs H_1024: scored at n=6 EXACT (not n=4), the full grid fanned out over a
many-core pool (route(a) EXACT many-core, exactly the H_1022 n=6 machinery).

ENGINES — BOTH stdlib IIT-4.0 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 (AND a
ring/standalone n=6 proof) BEFORE scoring via the H_1012 prove_mirrors_at_n discipline
(a_phi_iit4_tool — real engines, no proxy). big-Phi distinctions+relations are EXACT and
the MIP bipartition search is FULLY ENUMERATED at n=6 (route a, no sampling).

PRE-REGISTERED FALSIFIER (frozen; TEXT tokens only — PASS/FAIL, NO emoji in pre-reg)
-----------------------------------------------------------------------------------
At n=6 EXACT, score the planning(depth-8) - GREEDY contrast SIGN of BOTH measures for
EACH of the 6 binnings (nb in {2,3,4} x {equal_width, quantile}). Per-scheme sign-
criterion (stated BEFORE running):
  faith_sign  = UP   iff faithful_phi contrast > +1e-3
  big_sign    = DOWN iff big-Phi      contrast < -1e-3
  scheme PRESERVES the split iff (faith_sign == UP) AND (big_sign == DOWN).
- PASS = discretization-invariance CONFIRMED at scale : ALL 6/6 schemes PRESERVE the
  split at n=6 EXACT (faithful RAISES, big-Phi LOWERS; magnitudes may vary).
- FAIL = the n<=5 invariance was a small-n artifact : ANY scheme flips the sign at n=6
  (faith not UP, or big-Phi not DOWN) -> a publishable closed-negative (a_paper_negative_ok).

HONEST scope (a_scale_honest_scope): n=6 is the largest EXACT size. n=7 EXACT is
INFEASIBLE-CAP (big-Phi super-exponential). Verdict scoped to n<=6 EXACT; the H_1022 MC
estimator validated |Delta|=0.0000 at n<=5 but n>=7 is UNVERIFIED. Both engines EXACT at
n=6 (distinctions+relations exact, MIP fully enumerated). g5 CODE-measured (no LLM self-
judge, p7). NOT a forge binary; pure-CPU EXACT many-core.
"""
import sys, os, math, time, json, argparse
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
sys.path.insert(0, HERE)

# Import H_1004 (engines) + H_1012 (per-n equivalence proof) by their REAL MODULE NAMES
# so forked multiprocessing workers can re-import + unpickle without PicklingError
# (H_1022 lesson: importlib custom-name modules break on forked workers).
import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402

# real stdlib-mirror engines + substrate plumbing
big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
cohens_d = h1004.cohens_d
welch_t = h1004.welch_t
planning_trajectories = h1004.planning_trajectories
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ── PRE-FROZEN DISCRETIZATION GRID — VERBATIM from H_1024 (the ONLY thing that varies) ──
NB_GRID = [2, 3, 4]
SCHEME_GRID = ["equal_width", "quantile"]
F32_EPS = 1.19209290e-7
N_SEEDS = 30
PLAN_DEPTH = 8


def _discretize_channel_levels(v, nb, scheme):
    """VERBATIM H_1024. Continuous channel -> integer levels {0..nb-1}.
    equal_width = nb equal-width bins between min,max; quantile = nb equal-mass bins."""
    v = np.asarray(v, float)
    mn = v.min(); mx = v.max(); rng = mx - mn
    if rng < F32_EPS:
        return np.zeros(len(v), dtype=int)
    if scheme == "equal_width":
        edges = mn + rng * (np.arange(1, nb) / nb)
    elif scheme == "quantile":
        edges = np.quantile(v, np.arange(1, nb) / nb)
    else:
        raise ValueError(f"unknown scheme {scheme}")
    return np.searchsorted(edges, v, side="right").astype(int)


def latent_to_binary_seq_disc(H, n_units, nb, scheme):
    """VERBATIM H_1024. (n_steps x latent) -> (n_steps x n_units) BINARY via (nb,scheme).
    Top-variance channels, each -> nb levels, then bit = (level >= ceil(nb/2)).
    nb=2/quantile == the H_1012 median baseline."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    chans = H[:, idx]
    thr = math.ceil(nb / 2)
    bits = np.zeros_like(chans, dtype=int)
    for c in range(chans.shape[1]):
        levels = _discretize_channel_levels(chans[:, c], nb, scheme)
        bits[:, c] = (levels >= thr).astype(int)
    return bits, n_units


def both_phi_disc(H, n_units, nb, scheme):
    """VERBATIM H_1024. ONE (nb,scheme) discretization at size n_units, BOTH engines.
    big-Phi EXACT (distinctions+relations exact, MIP fully enumerated). Returns (big, faith)."""
    bits, n = latent_to_binary_seq_disc(H, n_units, nb, scheme)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return bphi, fphi


# ═══════════════════════════════════════════════════════════════════════════
# PARALLEL WORKER — ONE (seed, depth, which, nb, scheme) EXACT eval. Top-level so
# forked workers can pickle it (H_1022 lesson). Returns the exact (big, faith).
# ═══════════════════════════════════════════════════════════════════════════
def _eval_disc(args):
    n, seed, depth, which, nb, scheme = args
    Hg, Hp = planning_trajectories(seed, depth)
    H = Hp if which == "plan" else Hg
    b, f = both_phi_disc(H, n, nb, scheme)
    return (seed, nb, scheme, which, b, f)


def build_jobs(n, nb, scheme):
    """For one binning: 30 plan(depth-8) + 30 greedy = 60 EXACT evals."""
    jobs = []
    for s in range(N_SEEDS):
        jobs.append((n, s, PLAN_DEPTH, "plan", nb, scheme))
        jobs.append((n, s, PLAN_DEPTH, "greedy", nb, scheme))
    return jobs


def signword(x, eps=1e-3):
    return "UP" if x > eps else ("DOWN" if x < -eps else "NULL")


def contrast(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    c = a.mean() - b.mean()
    try:
        d = cohens_d(a, b)
    except Exception:
        d = float("nan")
    try:
        _, p = welch_t(a, b)
    except Exception:
        p = float("nan")
    return dict(contrast=c, d=d, p=p)


def score_binning_parallel(n, nb, scheme, pool, t0):
    jobs = build_jobs(n, nb, scheme)
    print(f"------ SCORE binning nb={nb} scheme={scheme}: dispatching {len(jobs)} EXACT "
          f"evals over {pool._processes} workers (elapsed {time.time()-t0:.1f}s) ------", flush=True)
    tb = time.time()
    results = pool.map(_eval_disc, jobs)
    el = time.time() - tb
    big_plan, big_greedy, faith_plan, faith_greedy = [], [], [], []
    for (seed, _nb, _sc, which, b, f) in results:
        if which == "plan":
            big_plan.append(b); faith_plan.append(f)
        else:
            big_greedy.append(b); faith_greedy.append(f)
    on_frac = float(latent_to_binary_seq_disc(
        planning_trajectories(0, PLAN_DEPTH)[1], n, nb, scheme)[0].mean())
    bC = contrast(big_plan, big_greedy)
    fC = contrast(faith_plan, faith_greedy)
    print(f"   binning nb={nb} {scheme}: {len(jobs)} evals DONE in {el:.1f}s wall "
          f"({el/len(jobs):.1f}s/eval amortized)", flush=True)
    return dict(big=bC, faith=fC, on_frac=on_frac, elapsed=el)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 1))
    ap.add_argument("--n", type=int, default=6, help="EXACT system size to score the grid at")
    ap.add_argument("--out", type=str, default=os.path.join(HERE, "h1037_n6_discretization_result.json"))
    args = ap.parse_args()

    print("=" * 88)
    print("H_1037 — is the planning faithful-UP / big-Phi-DOWN sign-split DISCRETIZATION-INVARIANT")
    print(f"         at n={args.n} EXACT (the largest exactly-computable size)?  Follow-up of H_1024 + H_1022.")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof, RE-PROVEN == stdlib per n")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s, MIP fully enumerated)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("VARY ONLY the discretization (binning) — VERBATIM the H_1024 pre-frozen grid, at n=6 EXACT.")
    print(f"PRE-FROZEN GRID: nb in {NB_GRID} x scheme in {SCHEME_GRID} = "
          f"{len(NB_GRID)*len(SCHEME_GRID)} binnings (NO post-hoc selection).")
    print("per-scheme sign-criterion (frozen): faith UP iff Δ>+1e-3 ; big-Phi DOWN iff Δ<-1e-3 ;")
    print("  scheme PRESERVES split iff (faith==UP AND big-Phi==DOWN).")
    print("PASS = discretization-invariance CONFIRMED at scale (ALL 6/6 preserve at n=6 EXACT).")
    print("FAIL = the n<=5 invariance was a small-n artifact (ANY scheme flips at n=6; a_paper_negative_ok).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print(f"workers={args.workers}  cpu_count={mp.cpu_count()}")
    print("=" * 88, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 (AND ring/standalone n=6) ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4, n=5, and n=6")
    print("         BEFORE scoring (H_1012 prove_mirrors_at_n discipline; LIVE stdlib refs):")
    proven = {}
    for n in (4, 5, 6):
        proven[n] = prove_mirrors_at_n(n)
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # ── STEP 0b: discretization-read determinism guard — PARALLEL (the scoring pool also
    #    re-runs these reads as a pure fn of the bits, so determinism is verified WITHIN the
    #    scored grid; here we confirm it on ONE representative binning per nb without burning a
    #    long SERIAL chain of dense n=6 big-Φ evals — a_wall_first). The bits->TPM->big-Φ path
    #    is identical across binnings (only the bit pattern differs), so two re-runs of the
    #    median-baseline binning suffice to assert read-determinism; the full-grid scores below
    #    further re-confirm it implicitly (deterministic engines). The guard runs ON THE POOL.
    print("STEP 0b — discretization-read determinism guard (pure fn of bits; PARALLEL, pool):", flush=True)
    pool = mp.Pool(processes=args.workers)
    all_rows = []
    t0 = time.time()
    try:
        guard_jobs = [(args.n, 0, PLAN_DEPTH, "plan", 2, "quantile"),   # median baseline, run A
                      (args.n, 0, PLAN_DEPTH, "plan", 2, "quantile")]   # median baseline, run B
        gA, gB = pool.map(_eval_disc, guard_jobs)
        det_ok = bool(abs(gA[4] - gB[4]) < 1e-12 and abs(gA[5] - gB[5]) < 1e-12)
        print(f"  median-baseline (nb=2 quantile) read deterministic at n={args.n}: {det_ok} "
              f"(big={gA[4]:.6f}=={gB[4]:.6f}, faith={gA[5]:.6f}=={gB[5]:.6f})", flush=True)
        if not det_ok:
            print("  ABORT — discretization read non-deterministic.")
            raise SystemExit(1)
        print()

        # ── STEP 1: score the full pre-frozen grid at n EXACT, many-core ──
        print(f"STEP 1 — route(a) EXACT many-core: score the 6-binning grid at n={args.n} EXACT", flush=True)
        for nb in NB_GRID:
            for scheme in SCHEME_GRID:
                tag = "median-baseline (== H_1012/H_1017/H_1024)" if (nb == 2 and scheme == "quantile") else ""
                r = score_binning_parallel(args.n, nb, scheme, pool, t0)
                bc = r["big"]["contrast"]; fc = r["faith"]["contrast"]
                bs = signword(bc); fs = signword(fc)
                preserves = (fs == "UP" and bs == "DOWN")
                print(f"   big-Phi      contrast={bc:+.4f} d={r['big']['d']:+.3f} p={r['big']['p']:.3e} -> {bs}")
                print(f"   faithful_phi contrast={fc:+.4f} d={r['faith']['d']:+.3f} p={r['faith']['p']:.3e} -> {fs}")
                print(f"   on-fraction(seed0 plan)={r['on_frac']:.3f}  {tag}")
                print(f"   PRESERVES split (faith-UP & big-DOWN): {preserves}", flush=True)
                print()
                all_rows.append(dict(n=int(args.n), nb=int(nb), scheme=scheme,
                                     bc=float(bc), fc=float(fc),
                                     bd=float(r["big"]["d"]), fd=float(r["faith"]["d"]),
                                     bp=float(r["big"]["p"]), fp=float(r["faith"]["p"]),
                                     bs=bs, fs=fs, on_frac=float(r["on_frac"]),
                                     preserves=bool(preserves), elapsed=float(r["elapsed"])))
    finally:
        pool.close()
        pool.join()

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER — per-binning SIGN table at n EXACT
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 88)
    print(f"PER-BINNING SIGN TABLE at n={args.n} EXACT — planning(depth-8) - GREEDY contrast SIGN")
    print("=" * 88)
    print(f"  {'n':>2s} | {'nb':>2s} | {'scheme':11s} | {'on_frac':>7s} | "
          f"{'faith Δ':>9s} | {'faith':>5s} | {'big-Phi Δ':>10s} | {'big-Phi':>7s} | {'PRESERVES':>9s}")
    invariant = True
    n_ok = 0
    for r in all_rows:
        ok_b = r["preserves"]
        if ok_b:
            n_ok += 1
        else:
            invariant = False
        print(f"  {r['n']:>2d} | {r['nb']:>2d} | {r['scheme']:11s} | {r['on_frac']:>7.3f} | "
              f"{r['fc']:+9.4f} | {r['fs']:>5s} | {r['bc']:+10.4f} | {r['bs']:>7s} | {str(ok_b):>9s}")
    print()
    n_total = len(all_rows)
    print(f"binnings PRESERVING faith-UP & big-Phi-DOWN at n={args.n} EXACT: {n_ok}/{n_total}")
    print()

    print("=" * 88)
    if invariant and n_total == len(NB_GRID) * len(SCHEME_GRID):
        print(f"OVERALL: DISCRETIZATION-INVARIANT-AT-SCALE — the planning faithful_phi-UP / big-Phi-DOWN")
        print(f"  sign-split holds for EVERY binning in the pre-frozen grid at n={args.n} EXACT")
        print(f"  (all nb in {NB_GRID} x {SCHEME_GRID}). The discretization-invariance established at")
        print(f"  n<=5 (H_1024) is CONFIRMED at the largest exactly-computable size; it was NOT a")
        print(f"  small-n artifact. Only the magnitudes vary; the sign never flips.")
        print(f"  VERDICT-TOKEN: DISCRETIZATION-INVARIANT-AT-SCALE")
    else:
        print(f"OVERALL: SIGN-FLIPS-AT-N6 (CLOSED-NEGATIVE) — the planning sign-split FLIPS for >=1")
        print(f"  valid binning at n={args.n} EXACT: faith-UP / big-Phi-DOWN does NOT hold for every")
        print(f"  discretization at scale. The n<=5 (H_1024) invariance was a small-n artifact; the")
        print(f"  paper's discretization-invariance claim must be scoped to n<=5 (a_paper_negative_ok).")
        print(f"  VERDICT-TOKEN: SIGN-FLIPS-AT-N6")
    print("=" * 88)
    print(f"HONEST scope (a_scale_honest_scope): n={args.n} is the largest EXACT size; n=7 EXACT is")
    print("INFEASIBLE-CAP (big-Phi super-exponential). Verdict scoped to n<=6 EXACT. The H_1022 MC")
    print("estimator validated |Δ|=0.0000 at n<=5; n>=7 is UNVERIFIED. Both engines EXACT at n=6")
    print("(distinctions+relations exact, MIP fully enumerated — no sampling). BOTH CPU mirrors")
    print("RE-PROVEN == stdlib at n=4 AND n=5 (+ ring/standalone n=6) BEFORE scoring (a_phi_iit4_tool;")
    print("no proxy). The discretization grid is PRE-FROZEN (no post-hoc selection); each read is a")
    print("deterministic pure function of the bits. g5 CODE-measured (no LLM self-judge, p7). NOT a")
    print("forge binary; pure-CPU EXACT many-core. TOY n-ladder.")

    # persist machine-readable result
    out = dict(n=int(args.n), workers=int(args.workers),
               mirror_proven={int(k): bool(v) for k, v in proven.items()},
               det_ok=bool(det_ok),
               n_ok=int(n_ok), n_total=int(n_total), invariant=bool(invariant),
               verdict_token=("DISCRETIZATION-INVARIANT-AT-SCALE" if (invariant and n_total == 6)
                              else "SIGN-FLIPS-AT-N6"),
               rows=all_rows, total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
