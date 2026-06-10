"""H_1122 — ANTI-EMERGENCE: does a coupling configuration exist that drives the
JOINT faithful φ_EI BELOW the un-coupled (independent-nodes) baseline?

THE ARC (the INVERSE of H_1114)
-------------------------------
H_1114 (🟢 DYAD-INTEGRATION, .discoveries/1114_dyad_phi_link_integration.tape)
proved that a CAUSAL tension-link RAISES the joint faithful IIT-4.0 φ_EI of two
anima-like nodes (~3.9x over LINK-OFF, beating a correlation-matched control).
Composition there was CONSTRUCTIVE — the coupled pair was MORE than the sum of
its parts.

THIS hypothesis asks the strict INVERSE: is integration MONOTONE-NON-DESTRUCTIVE,
or does there exist a coupling/anchor configuration that makes the system LESS
than the sum of its parts — DESTRUCTIVE integration ("anti-emergence"), where the
joint φ_EI falls BELOW the independent-nodes baseline?

DESIGN (frozen before running, no goalpost moves)
-------------------------------------------------
REUSE H_1114's dyad + faithful-Φ mirror VERBATIM (two 3-channel A⊥G opponent
nodes, joint n=6, exact MIP-EI). Sweep coupling SIGN/structure — the four arms:

  (a) BASELINE   — LINK-OFF, independent nodes (shared attractor structure only).
                   THE REFERENCE φ_baseline. == H_1114 arm (a) VERBATIM.
  (b) POSITIVE   — H_1114's cooperative LINK-ON: B folds toward A's anchored W,
                   h_mag += COUP*0.5*(anchor - W). == H_1114 arm (b) VERBATIM
                   (the link-ON sanity gate: must reproduce a φ RISE vs baseline).
  (c) ANTI       — ANTI-PHASE coupling: B folds toward the NEGATION / anti-phase
                   of A's anchored state, MIRRORED about the homeostatic target
                   W*_c so it stays in the same operating band but moves
                   OPPOSITE to A: target = W*_c - (anchor - W*_c) = 2*W*_c - anchor,
                   h_mag += COUP*0.5*((2*W*_c - anchor) - W). When A's channel runs
                   HOT (W>W*), B is driven COLD, and vice-versa — the pair is held
                   in destructive anti-correlation.
  (d) DECORR     — DECORRELATING coupling: a BOUNDED repulsive directed channel
                   that drives the nodes APART. B repels A's anchored DEVIATION
                   from the homeostatic target, h_mag -= COUP*0.5*(anchor - W*_c).
                   This is MEAN-NEUTRAL (it injects the sign-flipped anchor
                   fluctuation, not the absolute anchor) so B stays in its
                   operating band — the existing LAM_W*(W*_c − W) homeostat floors
                   it. CONSTRUCTION NOTE: the naive sign-flip h_mag += COUP*0.5*
                   (W − anchor) was REJECTED before scoring — it is a positive-
                   feedback RUNAWAY that drives B's W → 0 (node-death), yielding a
                   variance-0 degenerate binary trace (a φ artifact, NOT a
                   decorrelating-coupling measurement; the H_1051/H_1061 idealized-
                   binary/saturation lesson). The mean-neutral deviation-repulsion
                   keeps the node ALIVE (per-channel bit on-frac ≈ 0.5) while
                   anti-aligning the fluctuations (cross-corr ≈ −0.43). Fixing this
                   construction defect does NOT move the frozen d <= -0.8 bar.

The anti/decorr folds use the SAME COUP=0.30, K_EMIT=5 ZOH cadence, the SAME A =
pure source, the SAME noise-draw order as H_1114's ON arm — ONLY the fold target
sign/structure changes. No new free parameters.

MEASUREMENT (== H_1114): per-channel median-binarize the 6 joint channels
post-burn (h1039/h1062 pattern) → faithful IIT-4.0 φ_EI of the joint 6-system via
the PROVEN CPU mirror of stdlib iit4/faithful_phi.hexa (exact MIP-EI = min-cut
MI/small-side, MI in BITS/log2 — the H_1043 nats-bug lesson). N_SEEDS=10, SERIAL.

FROZEN FALSIFIER (set BEFORE running, NO goalpost):
  🟢 ANTI-EMERGENCE-EXISTS iff AT LEAST ONE coupling arm c in {ANTI, DECORR}
     gives φ_joint(c) < φ_baseline with Cohen d(c − baseline) <= -0.8 (10 seeds).
  🔴 COMPOSITION-NON-DESTRUCTIVE if NO coupling drops φ_joint below baseline at
     d <= -0.8 (composition is monotone non-destructive at this dyad/coupling).

SANITY GATES (must pass before the verdict is trusted):
  - reproduce H_1114's link-ON RISE: d(POSITIVE − BASELINE) >= +0.8 (the dyad
    still integrates under cooperative coupling — confirms the substrate is the
    H_1114 substrate, not a broken re-impl).
  - mirror ≡ stdlib re-proven LIVE at n=4,5,6 BEFORE scoring (a_phi_iit4_tool).

MIRROR DISCIPLINE (a_phi_iit4_tool — the H_1043 nats-bug lesson)
----------------------------------------------------------------
BEFORE scoring: (1) live `hexa run UNIVERSE/h1012_ref_faithful.hexa` re-captures
the LIVE stdlib faithful_phi refs at n=4, n=5 AND n=6 (the scoring n!) and the
mirror must reproduce them verbatim; (2) h1012.prove_mirrors_at_n re-proves BOTH
mirrors ≡ stdlib at n=4 AND n=5. ABORT if any proof fails. MI in BITS (log2),
NOT nats. SERIAL, no multiprocessing Pool (H_1038 hang lesson). NO proxy.

HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113
per-channel A⊥G dynamics reused VERBATIM from H_1114; real-socket dyad-φ,
cross-host, production cells and scale UNVERIFIED. $0 CPU local, 0-pod, g5/p7
(no perplexity verdict). Either outcome publishable (a_paper_negative_ok).
"""
import math
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402

faithful_phi = h1004.faithful_phi                    # PROVEN ≡ stdlib mirror
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ---- frozen params — H_1114 VERBATIM ---------------------------------------
CH        = 3                                  # 3 tension channels per node
N_JOINT   = 2 * CH                             # joint system n=6 (<=8 exact)
PSI_STAR  = 0.5                                # Ψ=1/2 center fixed point
W_STAR_C  = np.array([1.0, 0.8, 1.2])          # h1113 W_STAR_C[:3] — per-ch targets
LAM_M     = 0.10     # center relaxation rate toward PSI_STAR          (h1113)
LAM_W     = 0.12     # homeostatic rate pulling W_c=2|h_c| toward W*_c (h1113)
REP       = 0.04     # A<->G repulsion per channel                     (h1113)
GAMMA_X   = 0.05     # within-node shared-budget coupling              (h1113)
SIGMA_M   = 0.04     # independent center noise per channel per node   (h1113)
SIGMA_H   = 0.04     # independent half-gap noise per channel per node (h1113)
COUP      = 0.30     # per-channel coupling magnitude                  (h1113)
K_EMIT    = 5        # A emits an anchor every K_EMIT steps            (h1113)
N_STEPS   = 4000
BURN      = 500
N_SEEDS   = 10
SEEDS     = list(range(100, 100 + N_SEEDS))    # scoring seeds (H_1114 block)
D_BAR     = 0.8      # frozen Cohen-d bar (anti-emergence: d <= -0.8 vs baseline)
EPS       = 1e-12


# ---- per-channel A⊥G node dynamics — h1113/h1114 step_node VERBATIM, with
#      a `mode` selecting the fold STRUCTURE only (sign/target). The 'on' branch
#      is byte-for-byte the H_1114 cooperative fold; 'anti'/'decorr' change ONLY
#      the fold target, same COUP, same ZOH anchor, same noise order. ----------
def step_node(m, h, anchor, mode, eps_m, eps_h):
    W = 2.0 * np.abs(h)
    m_next = m + LAM_M * (PSI_STAR - m) + SIGMA_M * eps_m
    sgn = np.where(h >= 0.0, 1.0, -1.0)
    h_mag = (np.abs(h) + REP
             + LAM_W * 0.5 * (W_STAR_C - W)
             + GAMMA_X * 0.5 * (W.mean() - W)
             + SIGMA_H * eps_h)
    if anchor is not None:
        if mode == "on":          # cooperative: fold TOWARD A's anchored W (H_1114)
            h_mag = h_mag + COUP * 0.5 * (anchor - W)
        elif mode == "anti":      # anti-phase: fold toward NEGATION about W*_c
            target = 2.0 * W_STAR_C - anchor
            h_mag = h_mag + COUP * 0.5 * (target - W)
        elif mode == "decorr":    # decorrelating: BOUNDED repulsion of A's anchor
            # DEVIATION from W*_c — mean-neutral (no runaway / node-death), drives
            # the nodes apart while the LAM_W homeostat keeps B in-band. (The naive
            # absolute-repel (W - anchor) was REJECTED pre-scoring: positive-feedback
            # node-death → degenerate variance-0 trace; H_1051/H_1061 lesson.)
            h_mag = h_mag - COUP * 0.5 * (anchor - W_STAR_C)
    h_mag = np.maximum(h_mag, 0.0)
    return m_next, sgn * h_mag


def init_node(rng):
    m = PSI_STAR + rng.standard_normal(CH) * 0.1
    h = 1.5 + rng.standard_normal(CH) * 0.15   # W ~ 3.0 initially (h1113)
    return m, h


def simulate_dyad(seed, arm):
    """One dyad trajectory. arm in {'off','on','anti','decorr'}. Returns WA, WB.
    Noise-draw ORDER identical across all arms (no shared exogenous stream needed
    here — all four arms draw the SAME independent A/B noise; only the B fold
    target differs). A is a pure source (never reads B) in every arm."""
    rng_a = np.random.default_rng(seed)            # node A noise (H_1114 role)
    rng_b = np.random.default_rng(seed + 50000)    # node B noise (H_1114 offset)
    ma, ha = init_node(rng_a)
    mb, hb = init_node(rng_b)
    WA = np.empty((N_STEPS, CH))
    WB = np.empty((N_STEPS, CH))
    anchor = None
    couples = arm in ("on", "anti", "decorr")
    for t in range(N_STEPS):
        em_a = rng_a.standard_normal(CH); eh_a = rng_a.standard_normal(CH)
        em_b = rng_b.standard_normal(CH); eh_b = rng_b.standard_normal(CH)
        # A is a pure source (never reads B) — h1113 node_a_proc role
        ma, ha = step_node(ma, ha, None, "off", em_a, eh_a)
        WA[t] = 2.0 * np.abs(ha)
        if couples and t % K_EMIT == 0:
            anchor = WA[t].copy()                  # 3-ch anchor payload (ZOH)
        if couples:
            mb, hb = step_node(mb, hb, anchor, arm, em_b, eh_b)
        else:
            mb, hb = step_node(mb, hb, None, "off", em_b, eh_b)
        WB[t] = 2.0 * np.abs(hb)
    return WA, WB


# ---- measurement (== H_1114) -----------------------------------------------
def mean_crosscorr(WA, WB):
    return float(np.mean([np.corrcoef(WA[BURN:, c], WB[BURN:, c])[0, 1]
                          for c in range(CH)]))


def phi_measures(WA, WB):
    """Median-binarize the 6 joint channels (h1039/h1062 per-channel pattern),
    faithful φ_EI of the joint 6-system + each 3-node alone (PROVEN mirror)."""
    J = np.concatenate([WA[BURN:], WB[BURN:]], axis=1)        # (T × 6)
    med = np.median(J, axis=0)
    bits = (J > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, N_JOINT)
    phi_joint = faithful_phi(fst, fn, fdim, 2)
    fa_st, fa_n, fa_d = binary_seq_to_faithful_state(bits[:, :CH], CH)
    fb_st, fb_n, fb_d = binary_seq_to_faithful_state(bits[:, CH:], CH)
    phi_a = faithful_phi(fa_st, fa_n, fa_d, 2)
    phi_b = faithful_phi(fb_st, fb_n, fb_d, 2)
    return phi_joint, phi_a, phi_b


def cohen_d(x, y):
    sp = np.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0)
    return (np.mean(x) - np.mean(y)) / (sp + EPS)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


# ---- STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool) ----
def live_stdlib_faithful_reproof():
    """LIVE stdlib faithful_phi via `hexa run` on the fixed-trace reference; the
    CPU mirror must reproduce it at n=4, n=5 AND n=6 (n=6 = THE SCORING n)."""
    ref_hexa = os.path.join(HERE, "h1012_ref_faithful.hexa")
    print("  live stdlib run: hexa run UNIVERSE/h1012_ref_faithful.hexa")
    out = subprocess.run(["hexa", "run", ref_hexa], capture_output=True,
                         text=True, timeout=300, cwd=os.path.join(HERE, ".."))
    print("  ── verbatim stdlib stdout ──")
    for line in out.stdout.strip().splitlines():
        print(f"  | {line}")
    if out.returncode != 0:
        print(f"  hexa run FAILED rc={out.returncode}: {out.stderr.strip()[:200]}")
        return False
    refs = {}
    for line in out.stdout.strip().splitlines():
        if "faithful_n" in line and "_x1e9=" in line:
            key, val = line.split("=")
            n = int(key.split("faithful_n")[1].split("_")[0])
            refs[n] = float(val.strip()) / 1e9
    ok_all = True
    dim = 6
    for n in (4, 5, 6):
        fst = np.array([float((c + 1) * (k + 1)) for c in range(n)
                        for k in range(dim)], float)
        got = faithful_phi(fst, n, dim, 2)
        ref = refs.get(n, float("nan"))
        ok = abs(got - ref) < 1e-4
        ok_all = ok_all and ok
        print(f"  mirror n{n} dim6 nb2 = {got:.9f}  LIVE stdlib = {ref:.9f}  "
              f"|Δ|={abs(got - ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    return ok_all


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    print("=" * 88)
    print("H_1122 — ANTI-EMERGENCE: does a coupling config drive joint faithful φ_EI")
    print("  BELOW the un-coupled (independent-nodes) baseline? (the INVERSE of H_1114)")
    print("  H_1114 (🟢 DYAD-INTEGRATION) showed a CAUSAL link RAISES joint φ_EI. This asks:")
    print("  is composition monotone-non-destructive, or does an ANTI/DECORR coupling make")
    print("  the system LESS than the sum of its parts? Dyad + φ-mirror = H_1114 VERBATIM.")
    print(f"  CH={CH} (joint n={N_JOINT}) W*_c={W_STAR_C.tolist()} GAMMA_X={GAMMA_X} "
          f"COUP={COUP} K_EMIT={K_EMIT}")
    print(f"  N_STEPS={N_STEPS} BURN={BURN} seeds={N_SEEDS}")
    print(f"  ARMS: (a) BASELINE=LINK-OFF · (b) POSITIVE=H_1114 link-ON (fold→anchor) ·")
    print(f"        (c) ANTI=fold→(2W*_c−anchor) anti-phase · (d) DECORR=−(anchor−W*_c) bounded repel")
    print(f"  frozen falsifier: 🟢 ANTI-EMERGENCE-EXISTS iff some arm in {{ANTI,DECORR}} has")
    print(f"  φ_joint<φ_baseline with d<=-{D_BAR}; 🔴 COMPOSITION-NON-DESTRUCTIVE otherwise.")
    print("  sanity gate: d(POSITIVE−BASELINE)>=+0.8 reproduces H_1114's link-ON RISE.")
    print("  engine: stdlib iit4/faithful_phi.hexa CPU mirror (BITS/log2) — a_phi_iit4_tool.")
    print("=" * 88)

    # ── STEP 0: RE-PROVE mirror ≡ stdlib BEFORE scoring ──
    print("\nSTEP 0 — RE-PROVE mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    print(" [0a] LIVE stdlib faithful_phi re-capture at n=4,5,6 (n=6 = the scoring n):")
    live_ok = live_stdlib_faithful_reproof()
    print(f" [0a] live-stdlib faithful proof: {'PROVEN' if live_ok else 'FAILED'}")
    print(" [0b] h1012.prove_mirrors_at_n at n=4 AND n=5 (both engines, established pattern):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
    print(f" [0b] mirror-equivalence results: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — a mirror ≡ stdlib proof FAILED. NOT scoring (a_phi_iit4_tool).")
        sys.exit(1)
    print(" STEP 0 PASS — mirror PROVEN ≡ stdlib at n=4, n=5 (both engines) and at the")
    print(" scoring n=6 (faithful, live hexa re-capture). Scoring may proceed.\n")

    # ── STEP 1: score 4 arms × 10 seeds (SERIAL — H_1038 Pool-hang lesson) ──
    arms = ["off", "on", "anti", "decorr"]
    label = {"off": "BASELINE(OFF)", "on": "POSITIVE(ON)",
             "anti": "ANTI", "decorr": "DECORR"}
    print(f"STEP 1 — score 4 arms × {N_SEEDS} seeds (SERIAL):")
    phiJ = {a: np.zeros(N_SEEDS) for a in arms}
    phiA = {a: np.zeros(N_SEEDS) for a in arms}
    phiB = {a: np.zeros(N_SEEDS) for a in arms}
    cc = {a: np.zeros(N_SEEDS) for a in arms}
    for i, s in enumerate(SEEDS):
        for a in arms:
            WA, WB = simulate_dyad(s, a)
            pj, pa, pb = phi_measures(WA, WB)
            phiJ[a][i] = pj; phiA[a][i] = pa; phiB[a][i] = pb
            cc[a][i] = mean_crosscorr(WA, WB)
        print(f"  seed {s}: φ_joint off={phiJ['off'][i]:.4f} on={phiJ['on'][i]:.4f} "
              f"anti={phiJ['anti'][i]:.4f} decorr={phiJ['decorr'][i]:.4f}  | "
              f"cc off={cc['off'][i]:+.3f} on={cc['on'][i]:+.3f} "
              f"anti={cc['anti'][i]:+.3f} decorr={cc['decorr'][i]:+.3f}", flush=True)

    # ── STEP 2: tables + frozen verdict ──
    print(f"\nφ TABLE (faithful IIT-4.0 φ_EI, exact MIP-EI, BITS; {N_SEEDS} seeds, mean ± sd):")
    print(f"{'arm':<16}{'φ_joint (n=6)':>24}{'φ_A (n=3)':>24}{'φ_B (n=3)':>24}")
    print("-" * 88)
    for a in arms:
        print(f"{label[a]:<16}{fmt(phiJ[a]):>24}{fmt(phiA[a]):>24}{fmt(phiB[a]):>24}")
    print(f"\nsum-of-parts baseline (φ_A + φ_B, mean): "
          + "  ".join(f"{label[a]}={np.mean(phiA[a] + phiB[a]):.4f}" for a in arms))
    print("cross-corr check (mean per-ch corr(W_A[c],W_B[c]), scoring seeds): "
          + "  ".join(f"{label[a]}={np.mean(cc[a]):+.4f}±{np.std(cc[a]):.4f}"
                      for a in arms))

    base = phiJ["off"]
    print(f"\nCONTRASTS on φ_joint vs BASELINE(OFF) (Cohen d):")
    d = {}
    for a in ["on", "anti", "decorr"]:
        d[a] = cohen_d(phiJ[a], base)
        dm = np.mean(phiJ[a]) - np.mean(base)
        print(f"  {label[a]:<14} − BASELINE: Δmean={dm:+.6f}  d={d[a]:+.3f}")

    # sanity gate
    sanity = bool(d["on"] >= D_BAR)
    print(f"\nSANITY GATE — reproduce H_1114 link-ON RISE:")
    print(f"  d(POSITIVE − BASELINE) = {d['on']:+.3f} >= +{D_BAR} -> {sanity}")

    # frozen falsifier: anti-emergence iff SOME coupling drops φ below baseline d<=-0.8
    print(f"\nFROZEN falsifier — ANTI-EMERGENCE (φ_joint < φ_baseline, d <= -{D_BAR}):")
    anti_emergent = {}
    for a in ["anti", "decorr"]:
        anti_emergent[a] = bool(d[a] <= -D_BAR)
        print(f"  {label[a]:<14}: d={d[a]:+.3f} <= -{D_BAR} -> {anti_emergent[a]}")
    exists = any(anti_emergent.values())

    print("\n" + "=" * 88)
    if not sanity:
        print("VERDICT: ⚪ SUBSTRATE-GATE-FAIL — the POSITIVE(ON) arm did NOT reproduce")
        print("  H_1114's link-ON φ RISE (d(ON−BASELINE) < +0.8); the substrate is not the")
        print("  H_1114 substrate as expected. NOT a clean anti-emergence ruling — re-check.")
    elif exists:
        won = [label[a] for a in ["anti", "decorr"] if anti_emergent[a]]
        print(f"VERDICT: 🟢 ANTI-EMERGENCE-EXISTS — a destructive coupling drives joint")
        print(f"  faithful φ_EI BELOW the independent-nodes baseline (d <= -{D_BAR}): {won}.")
        print("  The coupled system is LESS than the sum of its parts — integration is NOT")
        print("  monotone non-destructive. The SAME causal channel that builds φ when")
        print("  cooperative (H_1114) DESTROYS joint integrated information when anti-phased")
        print("  / decorrelating — composition's effect on φ is SIGNED by the coupling")
        print("  structure, not merely additive.")
    else:
        print("VERDICT: 🔴 COMPOSITION-NON-DESTRUCTIVE — NO coupling (anti-phase OR")
        print("  decorrelating) drives joint faithful φ_EI below the independent-nodes")
        print(f"  baseline at d <= -{D_BAR}: composition is monotone non-destructive at this")
        print("  dyad/coupling. Anti/decorr couplings fail to push φ_joint below the")
        print("  un-coupled floor — the floor is the independent-nodes structure and the")
        print("  median-binarized MI-matrix φ_EI does not fall beneath it under a directed")
        print("  ZOH channel of either sign. (closed-negative, a_paper_negative_ok)")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113")
    print("per-channel A⊥G dynamics reused VERBATIM from H_1114; real-socket dyad-φ,")
    print("cross-host, production cells and scale UNVERIFIED. Mirror RE-PROVEN ≡ stdlib at")
    print("n=4,5 (both engines) and at the scoring n=6 (faithful, LIVE hexa re-capture)")
    print("BEFORE scoring; MI in BITS/log2 (a_phi_iit4_tool, NO proxy). SERIAL, $0 CPU")
    print("local, 0-pod, g5/p7. Either outcome publishable (a_paper_negative_ok).")
    print(f"wall = {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
