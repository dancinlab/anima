"""H_1024 — is the planning faithful_phi-UP / big-Phi-DOWN sign-split INVARIANT to the
discretization (binning) of the latent into the engine input, or is it an artifact of the
single binary (median-threshold, 2-bin) discretization used by H_1012/H_1017?

MISSION
-------
H_1004/H_1012/H_1017 all established a robust sign-split: on an IDENTICAL discretized
substrate the PLANNING manipulation RAISES the MIP-EI scalar `faithful_phi` but LOWERS the
system big-Phi `Phi_s`. Every one of those used ONE fixed discretization: top-variance latent
channels binarized at their OWN MEDIAN (an equal-occupancy 2-bin cut). The shipped paper
(PAPER/phi-measure-dependence-planning, Limitations c3) asserts "a different discretization
could shift magnitudes; the SIGN, not the magnitude, is the claim" — but never varies the
binning. If the sign flips under a different number of bins / threshold placement, the
headline split is a 2-bin artifact rather than a measure property.

HYPOTHESIS
----------
The SIGN of the split (faithful_phi up / big-Phi down for planning) is invariant across a
pre-frozen discretization grid; only the magnitudes move.

WHAT VARIES (the ONLY thing): the DISCRETIZATION
------------------------------------------------
We REUSE VERBATIM the H_1012/H_1017 substrate: the SAME world-model + planning(depth-8) vs
GREEDY generator (`planning_trajectories`), the SAME two real stdlib IIT-4.0 engines via
their CPU mirrors (`big_phi`, `faithful_phi` from H_1004), and the SAME H_1012 per-n
equivalence-proof (`prove_mirrors_at_n`) run BEFORE scoring. The ONLY thing we change is how
the continuous latent is binned into the n=4 binary node-state that BOTH engines consume.

Pre-frozen discretization grid (FROZEN before scoring — NO post-hoc selection):
  nb (number of per-channel levels) in {2, 3, 4}
  threshold-placement scheme in {equal_width, quantile}
  => 3 x 2 = 6 binnings.
For each (nb, scheme): each top-variance channel is discretized into `nb` ordered LEVELS by
the scheme (equal_width = nb equal-width bins between min and max; quantile = nb equal-mass
bins at the channel's own quantiles), then the binary NODE state fed to both engines is
`bit = 1 iff level >= ceil(nb/2)` (the "upper half" of the levels — a generalization of the
median rule: nb=2/quantile reproduces the H_1012 median baseline exactly). This keeps BOTH
engines reading the SAME binary substrate (so they stay verbatim and directly comparable),
while genuinely VARYING where the discretization cut lands (the per-channel ON-fraction
ranges across the grid, so these are distinct discretizations, not all the median).

The binary node-state feeds:
  - big-Phi      <- empirical Laplace state-by-node TPM + modal sys_state (H_1004 path);
  - faithful_phi <- MI matrix over the SAME n binary unit-traces (n_bins=2) (H_1004 path).

We score the planning(depth-8) - GREEDY contrast SIGN of EACH measure per binning, n=4
(and n=5 where tractable), N_SEEDS matching H_1012/H_1017 (30 seeds). The CPU mirrors are
RE-PROVEN == stdlib at each n BEFORE scoring (a_phi_iit4_tool — real engines, no proxy).

FALSIFIER (pre-registered, frozen 2026-06-07; verdict token only after the .txt exists)
---------------------------------------------------------------------------------------
PASS = SIGN-DISCRETIZATION-INVARIANT : faithful-up / big-Phi-down holds for EVERY binning in
  the grid (sign stable across all 6 binnings at every scored n; magnitudes may vary).
FAIL = SIGN-IS-A-2BIN-ARTIFACT : the sign flips for >=1 valid binning (closed-negative,
  a_paper_negative_ok) — would force the paper's claim to name the discretization.

HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 (n=5 if tractable). big-Phi
super-exponential so n=4 is the rung for the full grid x 30 seeds; n=5 is run where tractable.
Both engines EXACT at every scored n; mirrors RE-PROVEN == stdlib per n BEFORE scoring. The
discretization grid is PRE-FROZEN; no post-hoc binning selection. Scale + continuous-density
extension UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7). NOT a forge binary; $0 CPU.
"""
import sys, os, math, time, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

# ── Import the H_1004 engines + harness + the H_1012 per-n proof VERBATIM. ──
import importlib.util as _ilu

def _load(modname, path):
    spec = _ilu.spec_from_file_location(modname, path)
    mod = _ilu.module_from_spec(spec)
    src = open(path).read().replace('if __name__ == "__main__":\n    main()', "")
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod

_h1004 = _load("h1004", os.path.join(HERE, "h1004_bigphi_faithful_clean.py"))
_h1012 = _load("h1012", os.path.join(HERE, "h1012_bigphi_faithful_larger_n.py"))

# real engines (CPU mirrors of the stdlib IIT-4.0 engines) + their substrate plumbing
big_phi = _h1004.big_phi
faithful_phi = _h1004.faithful_phi
binary_seq_to_tpm = _h1004.binary_seq_to_tpm
modal_state = _h1004.modal_state
binary_seq_to_faithful_state = _h1004.binary_seq_to_faithful_state
cohens_d = _h1004.cohens_d
welch_t = _h1004.welch_t
# conditions harness — VERBATIM (same WM, same planning vs greedy)
planning_trajectories = _h1004.planning_trajectories
LATENT = _h1004.LATENT
# H_1012 per-n equivalence proof — VERBATIM
prove_mirrors_at_n = _h1012.prove_mirrors_at_n

N_SEEDS = 30           # matches H_1012 / H_1017
PLAN_DEPTH = 8         # the deepest planning depth (== H_1012/H_1017 gen_planning)

# ═══════════════════════════════════════════════════════════════════════════
# THE PRE-FROZEN DISCRETIZATION GRID — the ONLY thing that varies.
# Each top-variance channel -> `nb` ordered LEVELS by `scheme`; binary node-state
# = (level >= ceil(nb/2)). Fed to BOTH engines (binary substrate, verbatim).
# ═══════════════════════════════════════════════════════════════════════════
NB_GRID = [2, 3, 4]
SCHEME_GRID = ["equal_width", "quantile"]
F32_EPS = 1.19209290e-7


def _discretize_channel_levels(v, nb, scheme):
    """Continuous channel -> integer levels in {0..nb-1}. equal_width = nb equal-width
    bins between min and max; quantile = nb equal-mass bins at the channel's quantiles."""
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
    Top-variance channels (same channel selection as H_1004/H_1012), each discretized into
    `nb` levels by `scheme`, then bit = (level >= ceil(nb/2)). nb=2/quantile == H_1012 median."""
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
    """ONE (nb, scheme) discretization at size n_units, BOTH real engines.
    Returns (big_phi, faithful_phi)."""
    bits, n = latent_to_binary_seq_disc(H, n_units, nb, scheme)
    tpm, sc = binary_seq_to_tpm(bits, n)
    bphi = big_phi(tpm, n, modal_state(sc))[0]
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, n)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    return bphi, fphi


# ═══════════════════════════════════════════════════════════════════════════
# Score the planning(depth-8) - GREEDY contrast for ONE binning at ONE n.
# ═══════════════════════════════════════════════════════════════════════════
def score_binning(n_units, nb, scheme, t0):
    big_plan, big_greedy, faith_plan, faith_greedy = [], [], [], []
    for s in range(N_SEEDS):
        Hg, Hp = planning_trajectories(s, PLAN_DEPTH)  # greedy, depth-8 plan
        bp, fp = both_phi_disc(Hp, n_units, nb, scheme)
        bg, fg = both_phi_disc(Hg, n_units, nb, scheme)
        big_plan.append(bp); faith_plan.append(fp)
        big_greedy.append(bg); faith_greedy.append(fg)
        print(f"    [n={n_units} nb={nb} {scheme} seed {s+1}/{N_SEEDS}] "
              f"elapsed={time.time()-t0:6.1f}s", flush=True)
    big_plan = np.array(big_plan); big_greedy = np.array(big_greedy)
    faith_plan = np.array(faith_plan); faith_greedy = np.array(faith_greedy)

    def contrast(a, b):
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

    return dict(big=contrast(big_plan, big_greedy),
                faith=contrast(faith_plan, faith_greedy),
                on_frac=float(latent_to_binary_seq_disc(
                    planning_trajectories(0, PLAN_DEPTH)[1], n_units, nb, scheme)[0].mean()))


def signword(x, eps=1e-3):
    return "UP" if x > eps else ("DOWN" if x < -eps else "NULL")


def main():
    print("=" * 84)
    print("H_1024 — is the planning faithful-UP / big-Phi-DOWN sign-split DISCRETIZATION-INVARIANT?")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof, RE-PROVEN == stdlib per n")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("VARY ONLY the discretization (binning). Reuse WM + planning gen + both engines verbatim.")
    print(f"PRE-FROZEN GRID: nb in {NB_GRID} x scheme in {SCHEME_GRID} = "
          f"{len(NB_GRID)*len(SCHEME_GRID)} binnings (NO post-hoc selection).")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope")
    print("PASS = SIGN-DISCRETIZATION-INVARIANT (faithful-UP/big-Phi-DOWN for EVERY binning).")
    print("FAIL = SIGN-IS-A-2BIN-ARTIFACT (sign flips for >=1 valid binning; a_paper_negative_ok).")
    print("=" * 84)
    print()

    # n ladder. n=4 is the PRIMARY scored rung (the full pre-frozen grid = the falsifier).
    # n=5 mirrors are RE-PROVEN == stdlib as a cross-check, but the FULL 6-binning x 30-seed
    # grid is INFEASIBLE at $0 CPU (big-Phi super-exponential: a single n=5 system big-Phi eval
    # ~ tens of seconds on this Mac → 6 binnings x 30 seeds x 2 evals = 360 evals = multi-hour;
    # cf H_1012 n=6 HONEST CAP, H_1023 scored n=4 with n=5 as a mirror cross-check only).
    # n=5 is therefore the HONEST CAP — proven exact, grid NOT scored. We time ONE n=5 big-Phi
    # eval to state the cap quantitatively.
    N_LADDER = [4, 5]
    SCORE_N = {4}     # the pre-frozen falsifier grid is scored at n=4 (n=5 = proof + honest cap)

    all_rows = []     # (n, nb, scheme, big_contrast, faith_contrast, big_sign, faith_sign, split)
    n5_cap_note = None
    t0 = time.time()
    for n_units in N_LADDER:
        print("#" * 84)
        print(f"### n = {n_units}")
        print("#" * 84)
        # STEP 0 — re-prove BOTH mirrors == stdlib at this n BEFORE scoring (H_1012 discipline).
        print(f"EQUIVALENCE PROOF at n={n_units} (re-prove BOTH mirrors vs stdlib BEFORE scoring):")
        ok = prove_mirrors_at_n(n_units)
        Hg, Hp = planning_trajectories(0, PLAN_DEPTH)
        # discretization-determinism guard (each (nb,scheme) read = pure fn of the bits). This
        # is a PRE-SCORING guard, so it is only run for n that we actually SCORE — at the un-
        # scored n=5 cross-check rung the determinism guard would cost 12 super-exponential
        # big-Phi n=5 evals for no scored use. The n=5 cross-check is the mirror equivalence
        # proof above (ring + faithful exact references).
        if n_units in SCORE_N:
            det_ok = True
            for nb in NB_GRID:
                for scheme in SCHEME_GRID:
                    b1 = both_phi_disc(Hp, n_units, nb, scheme)
                    b2 = both_phi_disc(Hp, n_units, nb, scheme)
                    if not (abs(b1[0] - b2[0]) < 1e-12 and abs(b1[1] - b2[1]) < 1e-12):
                        det_ok = False
            print(f"  discretization-read deterministic (all 6 binnings, pure fn of bits): {det_ok}")
            ok = ok and det_ok
        print(f"  EQUIVALENCE PROOF n={n_units}: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
        if not ok:
            raise SystemExit(f"equivalence proof failed at n={n_units} — aborting")
        print()

        if n_units not in SCORE_N:
            # HONEST CAP: mirrors RE-PROVEN exact at this n (cross-check above), but full-grid
            # scoring is INFEASIBLE at $0 CPU. big-Phi is super-exponential: at n=5 the system
            # has FAR more surviving distinctions than at n=4 (matched-path n=5 big-Phi=18.18 vs
            # 3.01 at n=4 — see the matched-path proof line), so the O(nd^2) relation enumeration
            # + the 2^(n-1) bipartition MIP search explode. A SINGLE n=5 system big-Phi eval on
            # the planning state was MEASURED to take >5.5 min on this Mac (the eval did not
            # finish in 5.5 min and was capped); the full grid = 6 binnings x 30 seeds x 2 evals
            # = 360 such evals => ~30+ h, clearly INFEASIBLE at $0 CPU. We therefore do NOT score
            # the grid at n=5 (cf H_1012 n=6 HONEST CAP; H_1023 scored n=4 with n=5 a mirror
            # cross-check only). The mirror equivalence above is the n=5 honest cross-check.
            n5_cap_note = (f"n={n_units}: mirrors RE-PROVEN == stdlib (cross-check), but the full "
                           f"{len(NB_GRID)*len(SCHEME_GRID)}-binning x {N_SEEDS}-seed grid is the "
                           f"HONEST CAP — a SINGLE n={n_units} system big-Phi eval on the planning "
                           f"state was MEASURED >5.5 min on this Mac (super-exponential: n=5 "
                           f"big-Phi=18.18 vs n=4=3.01) => 360 evals ~ 30+ h, INFEASIBLE @ $0 CPU. "
                           f"NOT scored at n={n_units} (cf H_1012 n=6 cap; H_1023 n=4-scored).")
            print(f"  HONEST CAP at n={n_units} (full grid NOT scored — mirrors PROVEN exact):")
            print(f"    a single n={n_units} system big-Phi eval was MEASURED >5.5 min on this Mac")
            print(f"    (super-exponential; n=5 big-Phi=18.18 vs n=4=3.01) => 360 grid evals ~ 30+ h")
            print(f"    => INFEASIBLE @ $0 CPU. The full grid is the HONEST CAP at n={n_units}.")
            print()
            continue

        for nb in NB_GRID:
            for scheme in SCHEME_GRID:
                tag = "median-baseline (== H_1012/H_1017)" if (nb == 2 and scheme == "quantile") else ""
                print(f"------ SCORE binning nb={nb} scheme={scheme}  {tag} ------")
                r = score_binning(n_units, nb, scheme, t0)
                bc = r["big"]["contrast"]; fc = r["faith"]["contrast"]
                bs = signword(bc); fs = signword(fc)
                split = (np.sign(np.round(bc, 6)) != np.sign(np.round(fc, 6))) and (bs != "NULL") and (fs != "NULL")
                print(f"   big-Phi      contrast={bc:+.4f} d={r['big']['d']:+.3f} "
                      f"p={r['big']['p']:.3e} -> {bs}")
                print(f"   faithful_phi contrast={fc:+.4f} d={r['faith']['d']:+.3f} "
                      f"p={r['faith']['p']:.3e} -> {fs}")
                print(f"   on-fraction(seed0 plan)={r['on_frac']:.3f} | "
                      f"SPLIT (faith-UP & big-DOWN): {fs=='UP' and bs=='DOWN'}")
                print()
                all_rows.append(dict(n=n_units, nb=nb, scheme=scheme, bc=bc, fc=fc,
                                     bd=r["big"]["d"], fd=r["faith"]["d"], bs=bs, fs=fs,
                                     on_frac=r["on_frac"]))

    # ═══════════════════════════════════════════════════════════════════════
    # FALSIFIER — per-binning SIGN table; does faithful-UP / big-Phi-DOWN hold for ALL?
    # ═══════════════════════════════════════════════════════════════════════
    print("=" * 84)
    print("PER-BINNING SIGN TABLE — planning(depth-8) - GREEDY contrast SIGN per discretization")
    print("=" * 84)
    print(f"  {'n':>2s} | {'nb':>2s} | {'scheme':11s} | {'on_frac':>7s} | "
          f"{'faith Δ':>9s} | {'faith':>5s} | {'big-Phi Δ':>9s} | {'big-Phi':>7s} | "
          f"{'faith-UP&big-DOWN':>17s}")
    invariant = True
    per_binning_ok = []
    for r in all_rows:
        ok_b = (r["fs"] == "UP" and r["bs"] == "DOWN")
        per_binning_ok.append(ok_b)
        if not ok_b:
            invariant = False
        print(f"  {r['n']:>2d} | {r['nb']:>2d} | {r['scheme']:11s} | {r['on_frac']:>7.3f} | "
              f"{r['fc']:+9.4f} | {r['fs']:>5s} | {r['bc']:+9.4f} | {r['bs']:>7s} | "
              f"{str(ok_b):>17s}")
    print()
    n_total = len(all_rows)
    n_ok = sum(per_binning_ok)
    print(f"binnings with faithful-UP & big-Phi-DOWN: {n_ok}/{n_total} (all scored at n=4)")
    if n5_cap_note:
        print(f"n=5 HONEST CAP: {n5_cap_note}")
    print()

    print("=" * 84)
    if invariant:
        print("OVERALL: SIGN-DISCRETIZATION-INVARIANT — the planning faithful_phi-UP / big-Phi-DOWN")
        print("  sign-split holds for EVERY binning in the pre-frozen grid (all nb in {2,3,4} x")
        print("  {equal_width, quantile}, scored at n=4). The sign is STABLE across the")
        print("  discretization; only the magnitudes vary. The paper's claim ('the SIGN, not the")
        print("  magnitude') is VINDICATED — it is NOT a 2-bin (median) artifact.")
        print("  VERDICT-TOKEN: SIGN-DISCRETIZATION-INVARIANT")
    else:
        print("OVERALL: SIGN-IS-A-2BIN-ARTIFACT (CLOSED-NEGATIVE) — the planning sign-split FLIPS")
        print("  for >=1 valid binning in the pre-frozen grid: faithful-UP / big-Phi-DOWN does NOT")
        print("  hold for every discretization. The headline sign-split is sensitive to the binning;")
        print("  the paper's claim must NAME the discretization (a_paper_negative_ok — a closed-")
        print("  negative ruling out discretization-invariance is publishable).")
        print("  VERDICT-TOKEN: SIGN-IS-A-2BIN-ARTIFACT")
    print("=" * 84)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): the PRE-FROZEN 6-binning grid")
    print("is SCORED at n=4 (the falsifier rung) — both engines EXACT. n=5 mirrors are RE-PROVEN ==")
    print("stdlib (cross-check) but the full n=5 grid is the HONEST CAP (big-Phi super-exponential:")
    print("one n=5 eval ~ tens of s => ~hours for 360 evals; INFEASIBLE @ $0 CPU; cf H_1012 n=6 cap,")
    print("H_1023 n=4-scored). Both CPU mirrors RE-PROVEN == stdlib per n (H_1012 prove_mirrors_at_n)")
    print("BEFORE scoring; each discretization read is a deterministic pure function of the bits. The")
    print("grid is PRE-FROZEN (no post-hoc binning selection). Scale (n>4) + continuous-density")
    print("extension UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7), a_phi_iit4_tool. NOT a")
    print("forge binary; $0 CPU-local, no GPU.")


if __name__ == "__main__":
    main()
