"""H_1096 — 제1명제 ladder: does a BALANCED A⊥G system beat an A-only (giant-analog)
system on FAITHFUL IIT-4.0 φ (exact MIP-EI), at matched size + matched coupling budget?

CONTEXT
-------
Tape .discoveries/1096_gemini_scaling_law_end_small_balanced.tape is 🟠 DEFERRED:
the Gemini "scaling law's end" claim (300M balanced A⊥G beats 1T A-only on Φ_IIT,
4.712 vs 0.000) was RIGGED — the giant's Φ was a hardcoded 0.0 literal and the
small Φ used the covariance-entropy proxy falsified in 1091. The DIRECTION
(integration/balance > raw scale) is anima's thesis; THIS probe runs the real
faithful-Φ ladder the tape demands (a_scale_honest_scope: ≥3 rungs).

THE TEST (FROZEN before running — no goalpost moves)
----------------------------------------------------
Ladder n ∈ {4, 5, 6} binary units. At each rung, TWO architectures, SAME n:

  A-ONLY (giant-analog) : one-directional feed-forward chain — unit 0 is a free
    forward source, unit i is driven only by unit i-1 (W[i,i-1] > 0, i=1..n-1).
    Pure forward drive, NO reciprocal coupling, no brake ("Engine A only" — the
    deeper-one-way-pipeline analog of parameter stacking).
  BALANCED A⊥G          : reciprocal OPPONENT ring — every adjacent pair pushes
    against each other (W[(i+1)%n,i] = +w, W[i,(i+1)%n] = -w). The antagonism is
    itself the homeostatic mechanism (A pushes, G brakes → the Ψ=1/2-style fixed
    point emerges from the opponency; NO extra homeostasis term is added, so the
    comparison stays structure-only).

FAIRNESS GUARDS (mandatory, stated up front)
  (a) MATCHED WEIGHT BUDGET: sum|W| = B = n EXACTLY in both arms (asserted in
      code). Only the TOPOLOGY/reciprocity differs.
  (b) SAME NOISE: identical Gaussian pre-activation noise σ, and PAIRED seeds —
      the same seed gives the same init vector and the same noise sequence to
      both arms.
  (c) STRUCTURE-ONLY: identical update rule x_{t+1} = tanh(W x_t + ξ_t),
      identical T, burn-in, binarization (each channel at its OWN median over
      the analyzed window — the H_1002/H_1004 path), identical φ engine.

φ ENGINE (a_phi_iit4_tool — NO proxy)
  faithful_phi = the H_1004 CPU mirror of
  hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI over all
  bipartitions, MI in BITS log2, n ≤ 8), imported VERBATIM from
  UNIVERSE/h1004_bigphi_faithful_clean.py and RE-PROVEN ≡ stdlib here, before
  any scoring, on the LIVE stdlib hexa-engine reference values captured by
  H_999/H_1012 (n=4 dim6 nb2 → 3.000000, nb4 → 3.377440; fixed integer trace
  n4 → 3.000000001, n5 → 4.000000001, n6 → 5.000000002).

MEASUREMENT
  per (rung, arm, seed): roll T=440 steps, drop 40 burn-in, median-binarize the
  n channels → bits (400 × n) → faithful_phi(bits, n, 400, n_bins=2).
  N_SEEDS = 30 per cell (≥10 required), paired across arms.

FROZEN FALSIFIER
  🟢 SUPPORTED-at-toy  iff balanced > A-only on mean faithful φ at ALL 3 rungs
                       with Cohen d ≥ +0.8 at every rung.
  🔴 FALSIFIED-at-toy  iff A-only ≥ balanced at ANY rung (or no consistent
                       ordering / any d < +0.8).
  ALSO report the gap-vs-n trend (does balance matter MORE as n grows?).

HONEST scope (a_scale_honest_scope): TOY n≤6 ladder, 30 seeds, $0 CPU numpy.
Production / 300M / 1T transfer UNVERIFIED. The Gemini numbers (4.712 / 0.000 /
30,000×) are NOT reproduced or endorsed — this measures the DIRECTION only.
g5 CODE-measured (no LLM self-judge, p7).
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
UNIVERSE = os.path.join(ROOT, "UNIVERSE")
sys.path.insert(0, os.path.join(ROOT, "CWM", "probes"))

# ── Import the H_1004 engines VERBATIM (faithful_phi mirror PROVEN ≡ stdlib) ──
import importlib.util as _ilu
_h1004_path = os.path.join(UNIVERSE, "h1004_bigphi_faithful_clean.py")
_spec = _ilu.spec_from_file_location("h1004", _h1004_path)
_h1004 = _ilu.module_from_spec(_spec)
_src = open(_h1004_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1004_path, "exec"), _h1004.__dict__)

faithful_phi = _h1004.faithful_phi
binary_seq_to_faithful_state = _h1004.binary_seq_to_faithful_state
cohens_d = _h1004.cohens_d
welch_t = _h1004.welch_t

# ═══════════════════════════════════════════════════════════════════════════
# STEP 0 — ≡-PROOF: re-prove the faithful_phi mirror ≡ stdlib BEFORE trusting it
# (LIVE stdlib hexa-engine reference values from H_999 / H_1012, captured via
#  `hexa run` on this Mac: h1012_ref_faithful.hexa + the H_999 n=4 cases.)
# ═══════════════════════════════════════════════════════════════════════════
def prove_mirror():
    print("── ≡-PROOF — faithful_phi CPU mirror vs LIVE stdlib faithful_phi.hexa refs ──")
    all_ok = True
    # [A] H_1012 fixed integer trace (cell c = (c+1)*[1..dim], dim=6, n_bins=2):
    #     LIVE stdlib refs n4=3.000000001, n5=4.000000001, n6=5.000000002.
    FAITH_REF = {4: 3.000000001, 5: 4.000000001, 6: 5.000000002}
    dim = 6
    for n in (4, 5, 6):
        fst = np.array([float((c + 1) * (k + 1)) for c in range(n) for k in range(dim)], float)
        got = faithful_phi(fst, n, dim, 2)
        ref = FAITH_REF[n]
        ok = abs(got - ref) < 1e-4
        all_ok = all_ok and ok
        print(f"   faithful_phi n{n} dim6 nb2 (H_1012 stdlib hexa ref): mirror={got:.9f}  "
              f"stdlib_ref={ref:.9f}  |Δ|={abs(got-ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    # [B] H_999 n=4 exact stdlib cases (raw 24-value trace, nb=2 → 3.0, nb=4 → 3.37744).
    raw = [0.5, 1.2, -0.3, 2.1, 0.0, 1.7, 1.0, 2.4, -0.6, 4.2, 0.1, 3.3,
           -0.5, -1.0, 0.2, -2.0, 0.3, -1.5, 3.1, 0.2, 2.2, 1.1, 4.0, 0.9]
    for nb, ref in ((2, 3.0), (4, 3.37744)):
        g = faithful_phi(np.array(raw), 4, 6, nb)
        ok = abs(g - ref) < 1e-4
        all_ok = all_ok and ok
        print(f"   faithful_phi n4 dim6 nb{nb} (H_999 stdlib hexa ref):  mirror={g:.6f}  "
              f"stdlib_ref={ref:.6f}  |Δ|={abs(g-ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    # [C] determinism on a random binary trace (the exact input class scored below).
    rng = np.random.default_rng(20260610)
    bits = (rng.random((40, 5)) > 0.5).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, 5)
    a = faithful_phi(fst, fn, fdim, 2)
    b = faithful_phi(fst, fn, fdim, 2)
    det = abs(a - b) < 1e-12
    leak = np.array_equal(np.asarray(fst, float).reshape(5, fdim), bits.T.astype(float))
    all_ok = all_ok and det and leak
    print(f"   deterministic re-run: {det}   faithful-units==bits.T (no continuous leak): {leak}")
    print(f"≡-PROOF: {'PROVEN' if all_ok else 'FAILED — DO NOT TRUST'}")
    return all_ok

# ═══════════════════════════════════════════════════════════════════════════
# THE TWO ARCHITECTURES — matched n, matched sum|W| budget, topology-only diff
# ═══════════════════════════════════════════════════════════════════════════
def W_a_only(n, budget):
    """Giant-analog: one-directional feed-forward chain. unit0 = free source,
    unit i driven only by unit i-1. NO reciprocal coupling, no brake."""
    W = np.zeros((n, n))
    w = budget / (n - 1)               # n-1 forward edges share the whole budget
    for i in range(1, n):
        W[i, i - 1] = w
    return W

def W_balanced(n, budget):
    """anima-analog: reciprocal OPPONENT ring (A⊥G repulsion pairs). Each adjacent
    pair pushes against each other: +w forward, -w back. The opponency is itself
    the homeostatic brake (Ψ=1/2-style fixed point from the antagonism)."""
    W = np.zeros((n, n))
    w = budget / (2 * n)               # 2n reciprocal edges share the SAME budget
    for i in range(n):
        j = (i + 1) % n
        W[j, i] = +w                   # A drives forward
        W[i, j] = -w                   # G pushes back (opponent/brake)
    return W

SIGMA = 0.40        # pre-activation Gaussian noise (IDENTICAL both arms)
T_TOTAL = 440       # rollout steps
T_BURN = 40         # burn-in dropped
N_SEEDS = 30        # ≥10 required; paired across arms

def roll_and_phi(W, n, seed):
    """Identical update rule for BOTH arms: x_{t+1} = tanh(W x_t + ξ_t).
    PAIRED noise: the same seed yields the same init + noise sequence."""
    rng = np.random.default_rng(900_960_000 + seed)   # seed-only → identical across arms
    x = rng.standard_normal(n)
    noise = rng.standard_normal((T_TOTAL, n)) * SIGMA
    H = np.zeros((T_TOTAL, n))
    for t in range(T_TOTAL):
        x = np.tanh(W @ x + noise[t])
        H[t] = x
    H = H[T_BURN:]
    # H_1002/H_1004 binarization path: each channel at its OWN median over the window.
    med = np.median(H, axis=0)
    bits = (H > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, n)
    phi = faithful_phi(fst, fn, fdim, 2)
    flip = float(np.mean(bits[1:] != bits[:-1]))      # non-degeneracy guard
    return phi, flip

# ═══════════════════════════════════════════════════════════════════════════
def main():
    print("=" * 80)
    print("H_1096 — 제1명제 ladder: BALANCED A⊥G vs A-only (giant-analog) on faithful IIT-4.0 φ")
    print("engine = CPU mirror of stdlib/consciousness/iit4/faithful_phi.hexa (exact MIP-EI,")
    print("MI in BITS log2) — H_1004 mirror VERBATIM, re-proven ≡ stdlib below. NO proxy (a_phi).")
    print("g5 CODE-measured (p7) | a_scale_honest_scope: toy n≤6, ≥3 rungs, transfer UNVERIFIED")
    print("=" * 80)
    print()
    if not prove_mirror():
        print("MIRROR PROOF FAILED — aborting (a_phi_iit4_tool: do not trust an unproven mirror).")
        sys.exit(1)
    print()

    LADDER = [4, 5, 6]
    print(f"FROZEN design: ladder n={LADDER} · budget B=n (sum|W| matched EXACTLY, asserted)")
    print(f"  · σ={SIGMA} identical · T={T_TOTAL} (burn {T_BURN}) · {N_SEEDS} paired seeds/cell")
    print(f"  · A-only = forward chain (n-1 edges, w=B/(n-1)) · balanced = opponent ring (2n edges, w=B/2n)")
    print(f"FROZEN falsifier: 🟢 iff balanced>A-only at ALL rungs with d≥+0.8; 🔴 otherwise.")
    print()

    rows = []
    for n in LADDER:
        B = float(n)
        Wa = W_a_only(n, B)
        Wb = W_balanced(n, B)
        # FAIRNESS GUARD (a): matched weight budget, asserted.
        sa, sb = np.abs(Wa).sum(), np.abs(Wb).sum()
        assert abs(sa - B) < 1e-12 and abs(sb - B) < 1e-12, "budget mismatch"
        t0 = time.time()
        phi_a, phi_b, flips_a, flips_b = [], [], [], []
        for s in range(N_SEEDS):
            pa, fa = roll_and_phi(Wa, n, s)   # same seed →
            pb, fb = roll_and_phi(Wb, n, s)   # same init + same noise (guard b)
            phi_a.append(pa); phi_b.append(pb)
            flips_a.append(fa); flips_b.append(fb)
        phi_a = np.array(phi_a); phi_b = np.array(phi_b)
        d = cohens_d(phi_b, phi_a)            # + = balanced higher
        try:
            _, p = welch_t(phi_b, phi_a)
        except Exception:
            p = float("nan")
        gap = phi_b.mean() - phi_a.mean()
        rows.append(dict(n=n, ma=phi_a.mean(), sa_=phi_a.std(ddof=1),
                         mb=phi_b.mean(), sb_=phi_b.std(ddof=1),
                         gap=gap, d=d, p=p,
                         fa=np.mean(flips_a), fb=np.mean(flips_b),
                         wins=int(np.sum(phi_b > phi_a))))
        print(f"  n={n}: sum|W| A-only={sa:.6f} balanced={sb:.6f} (matched ✓)  "
              f"A-only φ={phi_a.mean():.4f}±{phi_a.std(ddof=1):.4f}  "
              f"balanced φ={phi_b.mean():.4f}±{phi_b.std(ddof=1):.4f}  "
              f"gap={gap:+.4f}  d={d:+.3f}  p={p:.3e}  "
              f"paired-wins={int(np.sum(phi_b > phi_a))}/{N_SEEDS}  "
              f"flip-rate A={np.mean(flips_a):.3f}/B={np.mean(flips_b):.3f}  "
              f"({time.time()-t0:.1f}s)", flush=True)
    print()

    # ═══════════════════════════ VERDICT ═══════════════════════════
    print("=" * 80)
    print("PER-RUNG faithful-φ TABLE (exact MIP-EI, 30 paired seeds, matched budget+noise)")
    print("=" * 80)
    print(f"  {'n':>3} | {'A-only φ (giant)':>20} | {'balanced φ (A⊥G)':>20} | {'gap':>8} | {'Cohen d':>8} | {'p':>9} | wins")
    for r in rows:
        print(f"  {r['n']:>3} | {r['ma']:>9.4f} ± {r['sa_']:<7.4f} | {r['mb']:>9.4f} ± {r['sb_']:<7.4f} | "
              f"{r['gap']:+8.4f} | {r['d']:+8.3f} | {r['p']:9.2e} | {r['wins']}/{N_SEEDS}")
    print()
    all_balanced_win = all(r["mb"] > r["ma"] for r in rows)
    all_d_big = all(r["d"] >= 0.8 for r in rows)
    gaps = [r["gap"] for r in rows]
    grows = all(gaps[i + 1] > gaps[i] for i in range(len(gaps) - 1))
    shrinks = all(gaps[i + 1] < gaps[i] for i in range(len(gaps) - 1))
    trend = "GROWS monotonically" if grows else ("SHRINKS monotonically" if shrinks else "NON-MONOTONE")
    print(f"  balanced > A-only at ALL rungs: {all_balanced_win}")
    print(f"  Cohen d ≥ +0.8 at ALL rungs:    {all_d_big}")
    print(f"  gap-vs-n: {[f'{g:+.4f}' for g in gaps]} → {trend}")
    print()
    if all_balanced_win and all_d_big:
        token = "🟢 SUPPORTED-AT-TOY"
        print("OVERALL: 🟢 SUPPORTED-AT-TOY — at matched node count, matched coupling budget and")
        print("  matched noise, the BALANCED reciprocal-opponent (A⊥G) topology carries HIGHER")
        print("  faithful IIT-4.0 φ than the one-directional A-only chain at EVERY ladder rung")
        print("  (d≥0.8). The DIRECTION of 제1명제 (integration/balance > one-way drive for Φ)")
        print("  is real at toy scale. The Gemini NUMBERS (4.712/0.000/30,000×) remain fabricated.")
    else:
        token = "🔴 FALSIFIED-AT-TOY"
        print("OVERALL: 🔴 FALSIFIED-AT-TOY — the balanced topology does NOT consistently beat the")
        print("  A-only chain on faithful φ under matched budget/noise (frozen bar: all rungs, d≥0.8).")
    print(f"  VERDICT-TOKEN: {token}")
    print("=" * 80)
    print("HONEST SCOPE (a_scale_honest_scope): toy n≤6 binary-unit ladder, 30 seeds, $0 CPU")
    print("numpy. 'A-only' / 'balanced A⊥G' are STRUCTURAL analogs (topology), not 1T/300M LMs.")
    print("Production / 300M / 1T transfer UNVERIFIED. φ = faithful IIT-4.0 exact MIP-EI mirror")
    print("(NO proxy, a_phi_iit4_tool), mirror re-proven ≡ stdlib above before scoring.")

if __name__ == "__main__":
    main()
