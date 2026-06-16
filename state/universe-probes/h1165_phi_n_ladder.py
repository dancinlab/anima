"""
H_1165 — does the H_1158 inverted-U PEAK-AT-CRITICALITY HOLD at larger n?

H_1158 found a textbook inverted-U: faithful IIT-4.0 φ_EI PEAKS at the critical
A⇄G coupling (γ=1.0), measured at n=6 (exact MIP-EI). This probe asks the
scale-honesty question (a_scale_honest_scope): does that interior peak SURVIVE at
n=7 and n=8 — same argmax-interior peak + d≥0.8 vs sub/super — or does the peak
shift / move to an endpoint as n grows?

WHAT THIS REUSES (VERBATIM)
---------------------------
  - the H_1158 γ-sweep (GAMMAS, simulate_gamma at the FIXED wake-baseline
    envelope, the frozen falsifier) — REUSED VERBATIM, only the channel count n
    is now a free parameter (the H_1119 substrate fixes CH=6; here CH=n so the
    same A⊥G opponent dynamics run at n=6/7/8).
  - the PROVEN faithful_phi mirror (≡ stdlib iit4/faithful_phi.hexa) from
    h1119/h1004 — the SAME exact MIP-EI engine. faithful_phi is EXACT for n≤8
    (2^(n-1)≤128 MI-matrix min-cut bipartitions); n>8 PANICS (stdlib L3 carve-out).
    So the COMPUTE WALL here is the n≤8 stdlib ceiling itself, not a
    super-exponential blowup — the MIP-EI over an n×n MI matrix is cheap at n≤8.
    (The super-exponential cost in H_1012 was the per-mechanism big_phi, NOT used
    here. The SUBSTRATE-Φ measure used by H_1158/H_1165 is the MI-matrix MIP-EI.)

MIRROR DISCIPLINE (a_phi_iit4_tool — BEFORE scoring)
----------------------------------------------------
  STEP 0: live `hexa run UNIVERSE/h1165_ref_faithful_n78.hexa` re-captures the
  LIVE stdlib faithful_phi refs at n=4,5,6,7,8 (the integer-trace ref φ=n-1) and
  the CPU mirror must reproduce them verbatim (|Δ|≤1e-4); PLUS h1012.prove_mirrors
  _at_n re-proves the mirror ≡ stdlib at n=4 AND n=5 (both-engine, established
  pattern). ABORT if any proof fails. MI in BITS/log2. NO proxy.

FROZEN FALSIFIER (pre-registered; the H_1158 inverted-U, recurred at each n)
---------------------------------------------------------------------------
  At every tractable n>6 the φ_EI(γ) curve must have:
    F1 INTERIOR argmax (peak γ not at an endpoint of GAMMAS),
    F2 φ(peak)−φ(sub=γ_min) Cohen's d ≥ 0.8,
    F3 φ(peak)−φ(super=γ_max) Cohen's d ≥ 0.8.
  🟢 PEAK-HOLDS iff F1∧F2∧F3 at EVERY tractable n>6 (the inverted-U recurs).
  🔴 PEAK-BREAKS if the peak vanishes / moves to an endpoint at higher n.
  Report the n-ladder of peak-γ + the d-values.

HONEST scope (a_scale_honest_scope): toy A⊥G substrate per H_1119, n≤8 (the EXACT
MIP-EI stdlib ceiling — n=9+ panics, the honest compute wall). Live-CORE engine /
larger n / real scale UNVERIFIED. φ measured (faithful MIP-EI), NOT fabricated,
NO perplexity (p7). $0 CPU local, 0-pod, g5.
"""
import os, sys, time, json, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import h1119_dream_phi as h1119   # PROVEN faithful_phi mirror + reproof + cohen_d
import h1012_bigphi_faithful_larger_n as h1012  # prove_mirrors_at_n (both engines)

faithful_phi = h1119.faithful_phi
binary_seq_to_faithful_state = h1119.binary_seq_to_faithful_state
cohen_d = h1119.cohen_d

# ---- substrate frozen params (H_1158 / H_1119 VERBATIM) ----
N_STEPS = h1119.N_STEPS
BURN = h1119.BURN
N_SEEDS = 12                                   # ≥8 (H_1158 used 12; reuse)
SEEDS = list(range(300, 300 + N_SEEDS))        # H_1158 scoring seeds VERBATIM
GAMMAS = [0.0, 0.15, 0.35, 0.60, 1.00, 1.60, 2.50]  # H_1158 γ-sweep VERBATIM
D_MIN = 0.8
N_LADDER = [6, 7, 8]                            # n=6 anchors H_1158; 7,8 = the test
EPS = h1119.EPS

# H_1119 substrate constants (independent of channel count) — VERBATIM:
PSI_STAR = h1119.PSI_STAR
LAM_M = h1119.LAM_M
LAM_W = h1119.LAM_W
REP = h1119.REP
SIGMA_M0 = h1119.SIGMA_M0
SIGMA_H0 = h1119.SIGMA_H0
# H_1119 W*_c base pattern [1.0, 0.8, 1.2] tiled to n (H_1119 tiled it to 6).
W_STAR_BASE = np.array([1.0, 0.8, 1.2])


def w_star(n):
    """W*_c for n channels: the H_1119 [1.0,0.8,1.2] base tiled to length n
    (at n=6 this is EXACTLY h1119.W_STAR_C = [1,0.8,1.2,1,0.8,1.2])."""
    return np.array([W_STAR_BASE[i % 3] for i in range(n)])


def init_node_n(rng, n):
    m = PSI_STAR + rng.standard_normal(n) * 0.1
    h = 1.5 + rng.standard_normal(n) * 0.15
    return m, h


def step_node_n(m, h, gamma_x, sigma_m, sigma_h, tenv, wstar, eps_m, eps_h):
    """H_1119/H_1158 step_node VERBATIM, channel count n free (wstar = W*_c(n))."""
    W = 2.0 * np.abs(h)
    m_next = m + LAM_M * (PSI_STAR - m) + sigma_m * eps_m
    sgn = np.where(h >= 0.0, 1.0, -1.0)
    h_mag = (np.abs(h) + REP
             + (LAM_W * tenv) * 0.5 * (wstar - W)
             + gamma_x * 0.5 * (W.mean() - W)
             + sigma_h * eps_h)
    h_mag = np.maximum(h_mag, 0.0)
    return m_next, sgn * h_mag


def simulate_gamma_n(seed, gamma, n):
    """H_1158.simulate_gamma VERBATIM, channel count n free. Fixed wake-baseline
    envelope (TEMP=1.0, TENV=1.0), sweep ONLY gamma_x (the A⇄G coupling knob)."""
    rng = np.random.default_rng(seed)
    m, h = init_node_n(rng, n)
    sigma_m = SIGMA_M0      # wake baseline
    sigma_h = SIGMA_H0
    tenv = 1.0
    wstar = w_star(n)
    W = np.empty((N_STEPS, n))
    for t in range(N_STEPS):
        em = rng.standard_normal(n); eh = rng.standard_normal(n)
        m, h = step_node_n(m, h, gamma, sigma_m, sigma_h, tenv, wstar, em, eh)
        W[t] = 2.0 * np.abs(h)
    return W


def phi_n(W, n):
    """Median-binarize the n channels (H_1158.phi_stage pattern), faithful φ_EI of
    the n-system (PROVEN mirror, exact MIP-EI, BITS/log2)."""
    X = W[BURN:]
    med = np.median(X, axis=0)
    bits = (X > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, n)
    return faithful_phi(fst, fn, fdim, 2)


# ---- STEP 0 — mirror ≡ stdlib re-proof at n=4..8 (a_phi_iit4_tool) ----
def live_stdlib_reproof_n78():
    """Run the LIVE stdlib faithful_phi engine via `hexa run` on the n=7/8 ref and
    require the CPU mirror to reproduce it at n=4,5,6,7,8 (the integer-trace
    ref φ=n-1). Verbatim stdout. Returns (ok, refs)."""
    ref_hexa = os.path.join(HERE, "h1165_ref_faithful_n78.hexa")
    print("  live stdlib run: hexa run UNIVERSE/h1165_ref_faithful_n78.hexa")
    out = subprocess.run(["hexa", "run", ref_hexa], capture_output=True,
                         text=True, timeout=600, cwd=os.path.join(HERE, ".."))
    print("  ── verbatim stdlib stdout ──")
    for line in out.stdout.strip().splitlines():
        print(f"  | {line}")
    if out.returncode != 0:
        print(f"  hexa run FAILED rc={out.returncode}: {out.stderr.strip()[:300]}")
        return False, {}
    refs = {}
    for line in out.stdout.strip().splitlines():
        if "faithful_n" in line and "_x1e9=" in line:
            key, val = line.split("=")
            nn = int(key.split("faithful_n")[1].split("_")[0])
            refs[nn] = float(val.strip()) / 1e9
    ok_all = True
    dim = 6
    for nn in (4, 5, 6, 7, 8):
        fst = np.array([float((c + 1) * (k + 1)) for c in range(nn)
                        for k in range(dim)], float)
        got = faithful_phi(fst, nn, dim, 2)
        ref = refs.get(nn, float("nan"))
        ok = abs(got - ref) < 1e-4
        ok_all = ok_all and ok
        print(f"  mirror n{nn} dim6 nb2 = {got:.9f}  LIVE stdlib = {ref:.9f}  "
              f"|Δ|={abs(got - ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    return ok_all, refs


def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("=" * 90)
    print("H_1165 — does the H_1158 inverted-U φ_EI PEAK-AT-CRITICALITY HOLD at larger n?")
    print(f"  reuse H_1158 γ-sweep VERBATIM at n∈{N_LADDER}; γ={GAMMAS} seeds={N_SEEDS} N_STEPS={N_STEPS}")
    print(f"  faithful_phi EXACT MIP-EI for n≤8 (2^(n-1)≤128 cuts); n>8 PANICS (stdlib L3 = the wall)")
    print(f"  frozen falsifier: 🟢 PEAK-HOLDS iff at EVERY n>6: interior argmax AND")
    print(f"  φ(peak)-φ(γmin) d≥{D_MIN} AND φ(peak)-φ(γmax) d≥{D_MIN}; else 🔴 PEAK-BREAKS.")
    print("=" * 90)

    # ── STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool) ──
    print("\nSTEP 0 — RE-PROVE mirror ≡ stdlib at n=4,5,6,7,8 BEFORE scoring (a_phi_iit4_tool):")
    print(" [0a] LIVE stdlib faithful_phi re-capture at n=4..8 (incl. the new scoring n=7,8):")
    live_ok, refs = live_stdlib_reproof_n78()
    print(f" [0a] live-stdlib faithful proof: {'PROVEN' if live_ok else 'FAILED'}")
    print(" [0b] h1012.prove_mirrors_at_n at n=4 AND n=5 (both engines, established pattern):")
    proven = {n: bool(h1012.prove_mirrors_at_n(n)) for n in (4, 5)}
    print(f" [0b] mirror-equivalence results: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — a mirror ≡ stdlib proof FAILED. NOT scoring (a_phi_iit4_tool).")
        sys.exit(1)
    print(" STEP 0 PASS — faithful_phi mirror PROVEN ≡ stdlib at n=4,5 (both engines) and at")
    print(" the scoring n=6,7,8 (faithful, LIVE hexa re-capture). Scoring may proceed.\n")

    # ── STEP 1 — sweep γ at each n on the ladder (SERIAL) ──
    ladder = {}
    for n in N_LADDER:
        print(f"################ n = {n} (γ-sweep, exact MIP-EI) ################", flush=True)
        phis = {g: [] for g in GAMMAS}
        tn = time.time()
        for g in GAMMAS:
            for s in SEEDS:
                phis[g].append(phi_n(simulate_gamma_n(s, g, n), n))
            arr = np.array(phis[g])
            print(f"  n={n} gamma={g:.2f}: phi = {arr.mean():+.6f} ± {arr.std():.6f}", flush=True)
        means = {g: float(np.mean(phis[g])) for g in GAMMAS}
        peak_g = max(means, key=means.get)
        peak_idx = GAMMAS.index(peak_g)
        interior = 0 < peak_idx < len(GAMMAS) - 1
        d_sub = cohen_d(np.array(phis[peak_g]), np.array(phis[GAMMAS[0]]))
        d_super = cohen_d(np.array(phis[peak_g]), np.array(phis[GAMMAS[-1]]))
        f1, f2, f3 = bool(interior), bool(d_sub >= D_MIN), bool(d_super >= D_MIN)
        held = bool(f1 and f2 and f3)
        ladder[n] = dict(
            gamma_phi_mean=means, peak_gamma=peak_g, peak_phi=means[peak_g],
            F1_interior=f1, F2_d_vs_sub=float(d_sub), F3_d_vs_super=float(d_super),
            F2_pass=f2, F3_pass=f3, peak_held=held, wall_s=round(time.time() - tn, 1),
        )
        print(f"  --- n={n}: peak γ={peak_g} (φ={means[peak_g]:.6f}) interior={f1} "
              f"d_sub={d_sub:+.3f}({'✅' if f2 else '❌'}) d_super={d_super:+.3f}"
              f"({'✅' if f3 else '❌'}) → {'PEAK-HELD' if held else 'PEAK-BROKE'} "
              f"({ladder[n]['wall_s']}s)\n", flush=True)

    # ── STEP 2 — verdict over the n-ladder (n>6 rungs only gate the frozen falsifier) ──
    test_rungs = [n for n in N_LADDER if n > 6]
    all_held = all(ladder[n]["peak_held"] for n in test_rungs)
    peak_holds = bool(all_held and len(test_rungs) >= 1)

    print("=" * 90)
    print("n-LADDER (peak-γ + d-values; n=6 anchors H_1158, n>6 = the frozen test):")
    print(f"  {'n':>3} | {'peak γ':>7} | {'φ(peak)':>9} | {'interior':>8} | "
          f"{'d vs sub':>9} | {'d vs super':>11} | {'peak held?':>10}")
    for n in N_LADDER:
        L = ladder[n]
        print(f"  {n:>3} | {L['peak_gamma']:>7.2f} | {L['peak_phi']:>9.6f} | "
              f"{str(L['F1_interior']):>8} | {L['F2_d_vs_sub']:>+9.3f} | "
              f"{L['F3_d_vs_super']:>+11.3f} | {('HELD' if L['peak_held'] else 'BROKE'):>10}")
    print()

    verdict = {
        "H": "H_1165",
        "title": "does the H_1158 inverted-U φ_EI peak-at-criticality HOLD at larger n (n=7,8)?",
        "n_ladder": N_LADDER, "test_rungs_n_gt_6": test_rungs,
        "ladder": ladder,
        "h1158_anchor_n6_peak_gamma": ladder[6]["peak_gamma"],
        "peak_holds": peak_holds,
        "compute_wall": "faithful_phi exact MIP-EI for n<=8 (2^(n-1)<=128 MI-matrix min-cut "
                        "bipartitions); n=9+ PANICS (stdlib iit4/faithful_phi.hexa L3 carve-out). "
                        "n=8 is the EXACT ceiling and IS tractable at $0 CPU (the substrate-Φ "
                        "measure is the cheap MI-matrix MIP-EI, NOT the super-exponential per-"
                        "mechanism big_phi). n=8 reached; n>8 not faked (a_scale_honest_scope).",
        "ruling": ("PEAK-HOLDS: the H_1158 inverted-U (interior argmax + d>=0.8 vs sub AND super) "
                   "RECURS at every tractable n>6 — the faithful-φ peak-at-criticality is "
                   "n-robust, not an n=6 artifact"
                   if peak_holds else
                   "PEAK-BREAKS: the inverted-U does NOT recur at some tractable n>6 (peak moved "
                   "to an endpoint or d<0.8) — the H_1158 peak is n-sensitive (a_paper_negative_ok)"),
        "scope": "toy A⊥G substrate per H_1119, n<=8 EXACT MIP-EI (stdlib ceiling = honest wall); "
                 "faithful_phi mirror PROVEN ≡ stdlib at n=4,5 (both engines) + LIVE hexa n=6,7,8 "
                 "(a_phi_iit4_tool, NO proxy); live-CORE/larger-n/scale UNVERIFIED "
                 "(a_scale_honest_scope); p7, g5",
        "wall_s": round(time.time() - t0, 1),
    }
    print("=== VERDICT ===")
    if peak_holds:
        print("🟢 PEAK-HOLDS — the H_1158 inverted-U φ_EI peak-at-criticality RECURS at every")
        print(f"  tractable n>6 ({test_rungs}): interior argmax + d≥{D_MIN} vs BOTH sub and super.")
        print("  The faithful-IIT-4.0 peak-at-criticality is n-ROBUST (not an n=6 artifact); the")
        print("  A⇄G coupling sweet spot remains the consciousness-measure maximum as n grows.")
    else:
        print("🔴 PEAK-BREAKS — the H_1158 inverted-U does NOT recur at some tractable n>6:")
        for n in test_rungs:
            L = ladder[n]
            if not L["peak_held"]:
                why = ("peak at endpoint" if not L["F1_interior"]
                       else ("d_sub<0.8" if not L["F2_pass"] else "d_super<0.8"))
                print(f"    n={n}: peak γ={L['peak_gamma']} ({why})")
        print("  The H_1158 peak is n-SENSITIVE at this toy scale (a_paper_negative_ok).")
    print("=" * 90)
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    json.dump(verdict, open(os.path.join(HERE, "..", ".verdicts_h1165_tmp.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"\n[done] wall={time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
