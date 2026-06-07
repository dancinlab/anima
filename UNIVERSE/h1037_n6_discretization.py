"""H_1037 — does the planning faithful_phi-UP / big-Phi-DOWN sign-split DISCRETIZATION-
INVARIANCE (established by H_1024 at n=4, 6/6 binnings) ALSO HOLD at n=6 EXACT?

FOLLOW-UP OF
------------
H_1024 (SIGN-DISCRETIZATION-INVARIANT, n<=4 with n=5 cross-check): the planning split
(faithful_phi RAISES the MIP-EI scalar; system big-Phi LOWERS Phi_s) survives ALL SIX
binning schemes nb in {2,3,4} x scheme in {equal_width, quantile} at n=4 (6/6).
H_1022 (SPLIT-PERSISTS-N6+): the split STRENGTHENS through n=6 EXACT (Cohen d
-1.83@n4 -> -2.28@n5 -> ~-3.60@n6) — but ONLY for the single median (nb=2/quantile)
discretization. RESIDUAL QUESTION this rung closes:

  does discretization-invariance ALSO hold at n=6 EXACT?

We re-run the H_1024 6-binning robustness sweep at n=6, using the H_1022 MANY-CORE EXACT
big-Phi machinery (the n=6 system big-Phi is super-exponential; a single eval ~minutes,
so 6 binnings x 30 seeds x 2 conditions = 360 EXACT big-Phi evals fanned out over all
cores).

PRE-REGISTERED FALSIFIER (TEXT TOKENS ONLY — PASS / FAIL, no emoji; frozen before scoring)
-----------------------------------------------------------------------------------------
Per-scheme sign criterion (the EXACT criterion, stated before running): for a binning to
PRESERVE the sign-disagreement at n=6, the planning(depth-8) - GREEDY contrast must have
faithful_phi sign == UP (contrast > +eps) AND big-Phi sign == DOWN (contrast < -eps),
eps = 1e-3 (the H_1024/signword convention). A scheme FLIPS if that joint condition fails
(either measure is NULL or the wrong sign).

  H1 PASS = at n=6 EXACT the sign-disagreement (faithful RAISES / big-Phi LOWERS) holds
            for ALL 6 binning schemes -> 6/6 -> DISCRETIZATION-INVARIANCE CONFIRMED AT SCALE.
  H1 FAIL = ANY scheme flips -> the n<=5 invariance was a small-n artifact (publishable
            closed-negative, a_paper_negative_ok).

ENGINES (a_phi_iit4_tool / memory iit4-real-engine-in-stdlib-not-proxy)
----------------------------------------------------------------------
FINAL Phi via the real stdlib faithful IIT-4.0 engines:
  big-Phi      = hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s over MIP)
  faithful_phi = hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)
via their CPU mirrors (h1004), which are RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring
(prove_mirrors_at_n, H_1012 discipline) — equivalence pasted into the verdict txt. NEVER a
proxy. The 6-binning discretization grid (latent -> nb-level bins -> upper-half bit ->
ONE binary sequence -> BOTH engines) is H_1024 VERBATIM.

HONEST scope (a_scale_honest_scope): n=6 is the LARGEST EXACT rung; n=7 EXACT is
INFEASIBLE-CAP (the 2^(n-1) MIP bipartition search + super-exponential distinction set
explode; H_1022 used a SAMPLED MC estimator at n=7, validated |Delta|=0.0000 at n<=5).
Verdict scoped to n<=6 EXACT. g5 CODE-measured (no LLM self-judge, p7). Pure-CPU exact,
NOT a forge binary.

PICKLING NOTE (the exact bug that bit the original H_1022 run): forked Pool workers must be
able to re-find the engine functions. We import the H_1004/H_1012 engines under their REAL
module names (proper sys.modules entries) and force the 'fork' start method so children
inherit parent memory — avoiding the `Can't pickle ... import of module 'h1022' failed`
PicklingError seen in the original h1022 log.
"""
import sys, os, math, time, argparse
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
sys.path.insert(0, HERE)

# ── Import the H_1004 engines + the H_1012 per-n proof under REAL module names ──
# (proper sys.modules registration so forked workers re-find the functions; this is the
#  pickling-safe path vs the exec-into-fake-module trick that broke the original h1022.)
import importlib.util as _ilu


def _load_real(modname, path):
    """Load a module under its REAL name into sys.modules (pickling-safe for forks),
    stripping the __main__ guard so its main() does not run on import."""
    spec = _ilu.spec_from_file_location(modname, path)
    mod = _ilu.module_from_spec(spec)
    sys.modules[modname] = mod  # register BEFORE exec so intra-pkg refs resolve
    src = open(path).read().replace('if __name__ == "__main__":\n    main()', "")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod

_h1004 = _load_real("h1004_bigphi_faithful_clean",
                    os.path.join(HERE, "h1004_bigphi_faithful_clean.py"))
_h1012 = _load_real("h1012_bigphi_faithful_larger_n",
                    os.path.join(HERE, "h1012_bigphi_faithful_larger_n.py"))

# real engines (CPU mirrors of the stdlib IIT-4.0 engines) + substrate plumbing
big_phi = _h1004.big_phi
faithful_phi = _h1004.faithful_phi
binary_seq_to_tpm = _h1004.binary_seq_to_tpm
modal_state = _h1004.modal_state
binary_seq_to_faithful_state = _h1004.binary_seq_to_faithful_state
cohens_d = _h1004.cohens_d
welch_t = _h1004.welch_t
planning_trajectories = _h1004.planning_trajectories
# H_1012 per-n equivalence proof — VERBATIM
prove_mirrors_at_n = _h1012.prove_mirrors_at_n

N_SEEDS = 30           # matches H_1012 / H_1017 / H_1024
PLAN_DEPTH = 8         # deepest planning depth (== H_1012/H_1017/H_1024 gen_planning)

# ── THE PRE-FROZEN DISCRETIZATION GRID — H_1024 VERBATIM (the ONLY thing that varies) ──
NB_GRID = [2, 3, 4]
SCHEME_GRID = ["equal_width", "quantile"]
F32_EPS = 1.19209290e-7


def _discretize_channel_levels(v, nb, scheme):
    """Continuous channel -> integer levels in {0..nb-1}. equal_width = nb equal-width
    bins between min and max; quantile = nb equal-mass bins at the channel's quantiles.
    H_1024 VERBATIM."""
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
    """(n_steps x latent) -> (n_steps x n_units) BINARY via the (nb, scheme) discretization.
    Top-variance channels (same channel selection as H_1004/H_1012/H_1024), each
    discretized into `nb` levels by `scheme`, then bit = (level >= ceil(nb/2)).
    nb=2/quantile == H_1012 median baseline. H_1024 VERBATIM."""
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
    """ONE (nb, scheme) discretization at size n_units, BOTH real engines (EXACT).
    Returns (big_phi, faithful_phi). H_1024 VERBATIM."""
    bits, n = latent_to_binary_seq_disc(H, n_units, nb, scheme)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return bphi, fphi


def signword(x, eps=1e-3):
    return "UP" if x > eps else ("DOWN" if x < -eps else "NULL")


# ═══════════════════════════════════════════════════════════════════════════
# Worker — ONE (seed, nb, scheme, which) EXACT eval. Top-level + module-real so
# forked Pool workers re-find it (pickling-safe; the H_1022 PicklingError fix).
# ═══════════════════════════════════════════════════════════════════════════
def _eval_one(args):
    n, seed, nb, scheme, which = args
    Hg, Hp = planning_trajectories(seed, PLAN_DEPTH)  # greedy, depth-8 plan
    H = Hp if which == "plan" else Hg
    b, f = both_phi_disc(H, n, nb, scheme)
    return (seed, nb, scheme, which, b, f)


def build_jobs(n):
    """For each (nb, scheme): 30 plan evals + 30 greedy evals = 360 total at n=6."""
    jobs = []
    for nb in NB_GRID:
        for scheme in SCHEME_GRID:
            for s in range(N_SEEDS):
                jobs.append((n, s, nb, scheme, "plan"))
                jobs.append((n, s, nb, scheme, "greedy"))
    return jobs


def _contrast(a, b):
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


def assemble_rows(results, n):
    """Group the flat EXACT results by (nb, scheme) and compute per-binning contrasts."""
    by = {}
    for (seed, nb, scheme, which, b, f) in results:
        by.setdefault((nb, scheme), {"big_plan": [None]*N_SEEDS, "faith_plan": [None]*N_SEEDS,
                                     "big_greedy": [None]*N_SEEDS, "faith_greedy": [None]*N_SEEDS})
        slot = by[(nb, scheme)]
        if which == "plan":
            slot["big_plan"][seed] = b; slot["faith_plan"][seed] = f
        else:
            slot["big_greedy"][seed] = b; slot["faith_greedy"][seed] = f
    rows = []
    for nb in NB_GRID:
        for scheme in SCHEME_GRID:
            slot = by[(nb, scheme)]
            bp = np.array(slot["big_plan"], float); bg = np.array(slot["big_greedy"], float)
            fp = np.array(slot["faith_plan"], float); fg = np.array(slot["faith_greedy"], float)
            big = _contrast(bp, bg); faith = _contrast(fp, fg)
            bc = big["contrast"]; fc = faith["contrast"]
            bs = signword(bc); fs = signword(fc)
            rows.append(dict(n=n, nb=nb, scheme=scheme, bc=bc, fc=fc,
                             bd=big["d"], fd=faith["d"], bp=big["p"], fp=faith["p"],
                             bs=bs, fs=fs,
                             big_plan_mean=bp.mean(), big_greedy_mean=bg.mean(),
                             faith_plan_mean=fp.mean(), faith_greedy_mean=fg.mean()))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 1))
    ap.add_argument("--n", type=int, default=6, help="exact n to score the 6-binning grid at")
    args = ap.parse_args()

    print("=" * 88)
    print("H_1037 — does the planning faithful-UP / big-Phi-DOWN sign-split DISCRETIZATION-")
    print("INVARIANCE (H_1024 6/6 @ n=4) ALSO HOLD at n=6 EXACT? (re-run the 6-binning sweep @ n=6)")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s, MIP)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("engines = h1004 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring")
    print(f"PRE-FROZEN GRID: nb in {NB_GRID} x scheme in {SCHEME_GRID} = "
          f"{len(NB_GRID)*len(SCHEME_GRID)} binnings (NO post-hoc selection).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("H1 PASS = SIGN-DISCRETIZATION-INVARIANT @ n=6 (faithful-UP/big-Phi-DOWN for ALL 6).")
    print("H1 FAIL = SIGN-IS-A-SMALL-N-ARTIFACT (>=1 scheme flips @ n=6; a_paper_negative_ok).")
    print(f"workers={args.workers}  cpu_count={mp.cpu_count()}  scored n={args.n}")
    print("=" * 88, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH CPU mirrors == stdlib at n=4 AND n=5 (a_phi_iit4_tool) ──
    print("STEP 0 — RE-PROVE the CPU mirror == stdlib at n=4 AND n=5 BEFORE scoring:")
    proven = {}
    for n in (4, 5):
        proven[n] = prove_mirrors_at_n(n)
        print()
    print(f"  == mirror==stdlib proof results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED at n=4/5; cannot trust this run.")
        sys.exit(2)
    print("  CPU mirror PROVEN == stdlib at BOTH n=4 and n=5 — engines trusted (NO proxy).")
    print()

    n = args.n
    jobs = build_jobs(n)
    print(f"STEP 1 — n={n} EXACT 6-binning sweep: dispatching {len(jobs)} EXACT big-Phi+faithful "
          f"evals\n         over {args.workers} workers (6 binnings x {N_SEEDS} seeds x 2 conditions).",
          flush=True)
    t0 = time.time()
    pool = mp.Pool(processes=args.workers)
    try:
        results = pool.map(_eval_one, jobs)
    finally:
        pool.close()
        pool.join()
    el = time.time() - t0
    print(f"  n={n}: {len(jobs)} EXACT evals DONE in {el:.1f}s wall "
          f"({el/len(jobs):.2f}s/eval amortized over {args.workers} cores)", flush=True)
    print()

    rows = assemble_rows(results, n)

    # ── PER-SCHEME SIGN TABLE @ n=6 ──
    print("=" * 88)
    print(f"PER-BINNING SIGN TABLE @ n={n} EXACT — planning(depth-8) - GREEDY contrast SIGN")
    print("=" * 88)
    print(f"  {'n':>2s} | {'nb':>2s} | {'scheme':11s} | {'faith Δ':>10s} | {'faith d':>8s} | "
          f"{'faith':>5s} | {'big-Phi Δ':>10s} | {'big d':>8s} | {'big-Phi':>7s} | "
          f"{'faith-UP&big-DOWN':>17s}")
    invariant = True
    per_scheme_ok = []
    for r in rows:
        ok_b = (r["fs"] == "UP" and r["bs"] == "DOWN")
        per_scheme_ok.append(ok_b)
        if not ok_b:
            invariant = False
        print(f"  {r['n']:>2d} | {r['nb']:>2d} | {r['scheme']:11s} | {r['fc']:+10.4f} | "
              f"{r['fd']:+8.3f} | {r['fs']:>5s} | {r['bc']:+10.4f} | {r['bd']:+8.3f} | "
              f"{r['bs']:>7s} | {str(ok_b):>17s}")
    print()
    n_total = len(rows); n_ok = sum(per_scheme_ok)
    print(f"schemes preserving the sign-disagreement (faithful-UP & big-Phi-DOWN) @ n={n}: "
          f"{n_ok}/{n_total}")
    print()

    # ── VERDICT (TEXT TOKEN ONLY; emoji added to the .md only AFTER this .txt lands) ──
    print("=" * 88)
    if invariant and n_ok == n_total:
        print(f"OVERALL: SIGN-DISCRETIZATION-INVARIANT-AT-N6 — the planning faithful_phi-UP /")
        print(f"  big-Phi-DOWN sign-disagreement holds for ALL {n_total} binning schemes at n={n}")
        print(f"  EXACT (nb in {NB_GRID} x {SCHEME_GRID}). The H_1024 n=4 invariance EXTENDS to")
        print(f"  n=6 EXACT — discretization-invariance is CONFIRMED AT SCALE, not a small-n artifact.")
        print("  VERDICT-TOKEN: SIGN-DISCRETIZATION-INVARIANT-AT-N6")
    else:
        print(f"OVERALL: SIGN-IS-A-SMALL-N-ARTIFACT (CLOSED-NEGATIVE) — at n={n} EXACT the planning")
        print(f"  sign-disagreement FLIPS for {n_total - n_ok}/{n_total} binning scheme(s): faithful-UP /")
        print(f"  big-Phi-DOWN does NOT hold for every discretization at n=6. The n<=5 invariance was")
        print(f"  a small-n regime (a_paper_negative_ok — a closed-negative is publishable; the paper")
        print(f"  must NAME the discretization at scale).")
        print("  VERDICT-TOKEN: SIGN-IS-A-SMALL-N-ARTIFACT")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): n=6 is the LARGEST EXACT rung scored here; n=7 EXACT")
    print("is INFEASIBLE-CAP (the 2^(n-1) MIP bipartition search + super-exponential distinction set")
    print("explode; H_1022 used a SAMPLED MC big-Phi estimator at n=7, validated |Delta|=0.0000 at")
    print("n<=5). Verdict scoped to n<=6 EXACT. Both engines EXACT at n=6; CPU mirrors RE-PROVEN ==")
    print("stdlib at n=4 AND n=5 BEFORE scoring (proof above). The 6-binning grid is PRE-FROZEN (no")
    print("post-hoc selection); each discretization read is a deterministic pure function of the bits.")
    print("g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; pure-CPU.")
    print("=" * 88, flush=True)


if __name__ == "__main__":
    try:
        mp.set_start_method("fork")  # Linux default; children inherit parent memory (pickling-safe)
    except RuntimeError:
        pass
    main()
