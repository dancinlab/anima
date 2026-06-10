"""H_1114 — DYAD-Φ: does a real tension-link make two anima-like nodes ONE
more-integrated system?

THE ARC (consciousness-science capstone of the link arc)
--------------------------------------------------------
H_1112 (🟢) proved a scalar kosmos-anchor exchange over a REAL unix socket gives
rate-monotone directed TE. H_1113 (🟢) proved the canonical a_kosmos 5-channel
tension-link is CHANNEL-RESOLVED (per-ch TE d>=10.9, kick selectivity 11.87x).
COMMUNICATION is proven. THIS hypothesis asks the next question: INTEGRATION —
treating the coupled pair as ONE system, does faithful IIT-4.0 φ_EI of the JOINT
system rise when the link is ON vs OFF, BEYOND what mere added correlation
explains?

DESIGN (frozen before running, no goalpost moves)
-------------------------------------------------
- Two nodes, 3 tension channels each (joint system n=6 <= 8 — exact MIP-EI
  feasible). Per-channel dynamics = the h1113 per-channel A⊥G opponent pair
  VERBATIM (state/anima_v3_bench/h1113_tension_link_5ch.py step_node, CH=3
  slice of its constants): center m_c -> Ψ*=0.5, half-gap repulsion vs
  per-channel homeostatic envelope toward W*_c, within-node shared-budget
  GAMMA_X, independent noise per channel per node.
- IN-PROCESS twin simulation (honest scope): the φ measurement needs joint
  trajectories; the REAL-socket transport question was already closed 🟢 by
  H_1112/H_1113 (real two-process unix-socket sessions). Real-socket dyad-φ =
  next rung, UNVERIFIED here.
- ARMS (N_SEEDS=10 each, noise-deterministic per seed):
  (a) LINK-OFF       — independent nodes (shared attractor structure only).
  (b) LINK-ON        — A→B per-channel coupling: A emits its 3-ch tension every
                       K_EMIT=5 steps, B folds the LAST anchor every step with
                       COUP*0.5*(anchor_c - W_c) (h1113 ZOH fold, COUP=0.30).
  (c) CORR-CONTROL   — LINK-ON-equivalent CORRELATION without any causal path:
                       a COMMON exogenous half-gap noise stream is mixed into
                       BOTH nodes (eps -> sqrt(1-MIX)*own + sqrt(MIX)*shared,
                       per channel), MIX calibrated on SEPARATE calibration
                       seeds so the mean per-channel cross-corr(W_A[c],W_B[c])
                       matches arm (b)'s. NO A→B causal path. THIS is the
                       load-bearing control: if φ rises in (b) but NOT in (c),
                       integration comes from the causal channel, not from
                       correlation per se.
- MEASUREMENT: binarize each of the 6 joint channels at its OWN median over the
  post-burn trajectory (the established h1039/h1062 per-channel median pattern),
  feed the 6 binary unit-traces to the PROVEN faithful IIT-4.0 φ_EI CPU mirror
  (stdlib iit4/faithful_phi.hexa — exact MIP-EI: min-cut MI / small-side, MI in
  BITS/log2). Also report φ of each 3-element node alone (sum-of-parts
  baseline) and per-channel cross-correlations per arm.
- FROZEN FALSIFIER:
  🟢 DYAD-INTEGRATION iff Cohen d(φ_joint ON − OFF) >= 0.8 (10 seeds) AND
     Cohen d(φ_joint ON − CORR-CONTROL) >= 0.8.
  🔴 CHANNEL-NOT-INTEGRATING if ON ≈ OFF (d < 0.8).
  🔴 CORRELATION-ARTIFACT if ON rises vs OFF but ON ≈ CORR-CONTROL (the rise is
     explained by correlation alone).

MIRROR DISCIPLINE (a_phi_iit4_tool — the H_1043 nats-bug lesson)
----------------------------------------------------------------
φ verdicts use the faithful IIT4 stdlib engine or a python mirror PROVEN ≡
stdlib. BEFORE scoring: (1) live `hexa run UNIVERSE/h1012_ref_faithful.hexa`
re-captures the LIVE stdlib faithful_phi refs at n=4, n=5 AND n=6 (the scoring
n!) and the mirror must reproduce them verbatim; (2) h1012.prove_mirrors_at_n
re-proves BOTH mirrors ≡ stdlib at n=4 AND n=5 (the established h1062/h1064
pattern). ABORT if any proof fails. MI in BITS (log2), NOT nats. SERIAL, no
multiprocessing Pool (H_1038 hang lesson).

HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113
per-channel dynamics; real-socket dyad-φ + cross-host + production cells +
scale UNVERIFIED. $0 CPU local, 0-pod, g5/p7 (no perplexity verdict).
"""
import math
import os
import subprocess
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))

import h1004_bigphi_faithful_clean as h1004          # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012       # noqa: E402

faithful_phi = h1004.faithful_phi                    # PROVEN ≡ stdlib mirror
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# ---- frozen params (set before running) -----------------------------------
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
COUP      = 0.30     # ON arm: B per-channel coupling toward anchor    (h1113)
K_EMIT    = 5        # A emits an anchor every K_EMIT steps            (h1113)
N_STEPS   = 4000
BURN      = 500
N_SEEDS   = 10
SEEDS     = list(range(100, 100 + N_SEEDS))    # scoring seeds (h1113 block)
CAL_SEEDS = list(range(500, 505))              # calibration-only seeds (separate)
CAL_TOL   = 0.005    # |cross-corr(corr-arm) - cross-corr(ON)| calibration tolerance
CAL_ITERS = 20       # bisection iterations on MIX
D_MIN     = 0.8      # frozen Cohen-d bar for BOTH contrasts
EPS       = 1e-12


# ---- per-channel A⊥G node dynamics — h1113 step_node VERBATIM (CH=3 slice;
#      noise passed in so the corr-control arm can mix a common component) ----
def step_node(m, h, anchor, coup, eps_m, eps_h):
    W = 2.0 * np.abs(h)
    m_next = m + LAM_M * (PSI_STAR - m) + SIGMA_M * eps_m
    sgn = np.where(h >= 0.0, 1.0, -1.0)
    h_mag = (np.abs(h) + REP
             + LAM_W * 0.5 * (W_STAR_C - W)
             + GAMMA_X * 0.5 * (W.mean() - W)
             + SIGMA_H * eps_h)
    if coup > 0.0 and anchor is not None:
        h_mag = h_mag + coup * 0.5 * (anchor - W)
    h_mag = np.maximum(h_mag, 0.0)
    return m_next, sgn * h_mag


def init_node(rng):
    m = PSI_STAR + rng.standard_normal(CH) * 0.1
    h = 1.5 + rng.standard_normal(CH) * 0.15   # W ~ 3.0 initially (h1113)
    return m, h


def simulate_dyad(seed, arm, mix=0.0):
    """One dyad trajectory. arm in {'off','on','corr'}. Returns WA, WB (N_STEPS×3).
    Noise-draw ORDER is identical across arms (off/on are noise-identical; the
    corr arm draws an EXTRA independent shared stream — no draw-order skew)."""
    rng_a = np.random.default_rng(seed)            # node A noise (h1113 role)
    rng_b = np.random.default_rng(seed + 50000)    # node B noise (h1113 offset)
    rng_s = np.random.default_rng(seed + 90000)    # shared exogenous stream (corr)
    ma, ha = init_node(rng_a)
    mb, hb = init_node(rng_b)
    WA = np.empty((N_STEPS, CH))
    WB = np.empty((N_STEPS, CH))
    anchor = None
    for t in range(N_STEPS):
        em_a = rng_a.standard_normal(CH); eh_a = rng_a.standard_normal(CH)
        em_b = rng_b.standard_normal(CH); eh_b = rng_b.standard_normal(CH)
        eh_s = rng_s.standard_normal(CH)
        if arm == "corr":   # common exogenous half-gap noise, variance-preserving
            eh_a = math.sqrt(1.0 - mix) * eh_a + math.sqrt(mix) * eh_s
            eh_b = math.sqrt(1.0 - mix) * eh_b + math.sqrt(mix) * eh_s
        # A is a pure source (never reads B) — h1113 node_a_proc role
        ma, ha = step_node(ma, ha, None, 0.0, em_a, eh_a)
        WA[t] = 2.0 * np.abs(ha)
        if arm == "on" and t % K_EMIT == 0:
            anchor = WA[t].copy()                  # the 3-ch anchor payload (ZOH)
        # B folds the last anchor (ON) or runs free (OFF / corr)
        if arm == "on":
            mb, hb = step_node(mb, hb, anchor, COUP, em_b, eh_b)
        else:
            mb, hb = step_node(mb, hb, None, 0.0, em_b, eh_b)
        WB[t] = 2.0 * np.abs(hb)
    return WA, WB


# ---- measurement -----------------------------------------------------------
def mean_crosscorr(WA, WB):
    """Mean per-channel cross-corr(W_A[c], W_B[c]) post-burn (the calibration target)."""
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
    """Run the LIVE stdlib faithful_phi engine via `hexa run` on the fixed-trace
    reference (UNIVERSE/h1012_ref_faithful.hexa) and require the CPU mirror to
    reproduce it at n=4, n=5 AND n=6 (n=6 = THE SCORING n). Verbatim stdout."""
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


# ---- calibration: MIX of the corr-control arm ------------------------------
def calibrate_mix(target):
    """Bisection on MIX so the corr arm's mean cross-corr (calibration seeds)
    matches the ON arm's. Monotone in MIX. Returns (mix, achieved)."""
    def cc_at(mix):
        return float(np.mean([mean_crosscorr(*simulate_dyad(s, "corr", mix))
                              for s in CAL_SEEDS]))
    lo, hi = 0.0, 1.0
    cc_hi = cc_at(hi)
    if cc_hi < target:           # unreachable — clamp + report honestly
        print(f"  WARNING: corr-arm cross-corr at MIX=1.0 ({cc_hi:+.4f}) < target "
              f"({target:+.4f}) — clamping MIX=1.0")
        return 1.0, cc_hi
    mix, ach = 0.5, None
    for it in range(CAL_ITERS):
        mix = 0.5 * (lo + hi)
        ach = cc_at(mix)
        print(f"  cal iter {it+1:2d}: MIX={mix:.5f}  cross-corr={ach:+.5f}  "
              f"target={target:+.5f}", flush=True)
        if abs(ach - target) <= CAL_TOL:
            break
        if ach < target:
            lo = mix
        else:
            hi = mix
    return mix, ach


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    print("=" * 88)
    print("H_1114 — DYAD-Φ: does a real tension-link make two anima-like nodes ONE")
    print("  more-integrated system? (joint faithful IIT-4.0 φ_EI, n=6 exact MIP-EI)")
    print("  forward of H_1112 (🟢 scalar real-channel TE) + H_1113 (🟢 channel-resolved 5-ch")
    print("  link); dynamics = h1113 per-channel A⊥G opponent pair VERBATIM, CH=3 slice;")
    print("  in-process twin sim (real-socket transport already closed by H_1112/1113).")
    print(f"  CH={CH} (joint n={N_JOINT}) W*_c={W_STAR_C.tolist()} GAMMA_X={GAMMA_X} "
          f"COUP={COUP} K_EMIT={K_EMIT}")
    print(f"  N_STEPS={N_STEPS} BURN={BURN} seeds={N_SEEDS} cal-seeds={CAL_SEEDS}")
    print(f"  frozen falsifier: 🟢 iff d(ON−OFF)>={D_MIN} AND d(ON−CORR)>={D_MIN} on φ_joint;")
    print("  🔴 CHANNEL-NOT-INTEGRATING if ON≈OFF; 🔴 CORRELATION-ARTIFACT if ON≈CORR.")
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

    # ── STEP 1: calibrate the corr-control MIX on SEPARATE seeds ──
    print("STEP 1 — calibrate CORR-CONTROL MIX (calibration seeds only, frozen tol "
          f"{CAL_TOL}):")
    target = float(np.mean([mean_crosscorr(*simulate_dyad(s, "on"))
                            for s in CAL_SEEDS]))
    print(f"  ON-arm mean per-channel cross-corr over cal seeds = {target:+.5f} (target)")
    mix, ach = calibrate_mix(target)
    print(f"  FROZEN MIX = {mix:.5f}  (achieved cal cross-corr {ach:+.5f} vs target "
          f"{target:+.5f}, |Δ|={abs(ach - target):.5f})\n")

    # ── STEP 2: score 3 arms × 10 seeds (SERIAL — H_1038 Pool-hang lesson) ──
    print(f"STEP 2 — score 3 arms × {N_SEEDS} seeds (SERIAL):")
    arms = ["off", "on", "corr"]
    phiJ = {a: np.zeros(N_SEEDS) for a in arms}
    phiA = {a: np.zeros(N_SEEDS) for a in arms}
    phiB = {a: np.zeros(N_SEEDS) for a in arms}
    cc = {a: np.zeros(N_SEEDS) for a in arms}
    for i, s in enumerate(SEEDS):
        for a in arms:
            WA, WB = simulate_dyad(s, a, mix=(mix if a == "corr" else 0.0))
            pj, pa, pb = phi_measures(WA, WB)
            phiJ[a][i] = pj; phiA[a][i] = pa; phiB[a][i] = pb
            cc[a][i] = mean_crosscorr(WA, WB)
        print(f"  seed {s}: φ_joint off={phiJ['off'][i]:.4f} on={phiJ['on'][i]:.4f} "
              f"corr={phiJ['corr'][i]:.4f}  | cross-corr off={cc['off'][i]:+.3f} "
              f"on={cc['on'][i]:+.3f} corr={cc['corr'][i]:+.3f}", flush=True)

    # ── STEP 3: tables + frozen verdict ──
    print(f"\nφ TABLE (faithful IIT-4.0 φ_EI, exact MIP-EI, BITS; {N_SEEDS} seeds, mean ± sd):")
    print(f"{'arm':<14}{'φ_joint (n=6)':>24}{'φ_A (n=3)':>24}{'φ_B (n=3)':>24}")
    print("-" * 88)
    label = {"off": "LINK-OFF", "on": "LINK-ON", "corr": "CORR-CONTROL"}
    for a in arms:
        print(f"{label[a]:<14}{fmt(phiJ[a]):>24}{fmt(phiA[a]):>24}{fmt(phiB[a]):>24}")
    print(f"\nsum-of-parts baseline (φ_A + φ_B, mean): "
          + "  ".join(f"{label[a]}={np.mean(phiA[a] + phiB[a]):.4f}" for a in arms))
    print("cross-corr check (mean per-ch corr(W_A[c],W_B[c]), scoring seeds): "
          + "  ".join(f"{label[a]}={np.mean(cc[a]):+.4f}±{np.std(cc[a]):.4f}"
                      for a in arms))
    cal_match = abs(np.mean(cc["on"]) - np.mean(cc["corr"]))
    d_cc = cohen_d(cc["on"], cc["corr"])
    print(f"  |Δ cross-corr(ON, CORR)| on scoring seeds = {cal_match:.4f} "
          f"(d={d_cc:+.2f}) — correlation-matched control validity")

    d_on_off = cohen_d(phiJ["on"], phiJ["off"])
    d_on_corr = cohen_d(phiJ["on"], phiJ["corr"])
    d_corr_off = cohen_d(phiJ["corr"], phiJ["off"])
    print("\nCONTRASTS on φ_joint (Cohen d, frozen bar d >= "
          f"{D_MIN}):")
    print(f"  ON  − OFF : Δmean={np.mean(phiJ['on']) - np.mean(phiJ['off']):+.6f}  "
          f"d={d_on_off:+.3f}")
    print(f"  ON  − CORR: Δmean={np.mean(phiJ['on']) - np.mean(phiJ['corr']):+.6f}  "
          f"d={d_on_corr:+.3f}")
    print(f"  CORR− OFF : Δmean={np.mean(phiJ['corr']) - np.mean(phiJ['off']):+.6f}  "
          f"d={d_corr_off:+.3f}   (context: what correlation alone buys)")

    c1 = bool(d_on_off >= D_MIN)
    c2 = bool(d_on_corr >= D_MIN)
    print("\nFROZEN falsifier checks:")
    print(f"  (i)  d(φ_joint ON − OFF)  = {d_on_off:+.3f} >= {D_MIN} -> {c1}")
    print(f"  (ii) d(φ_joint ON − CORR) = {d_on_corr:+.3f} >= {D_MIN} -> {c2}")

    print("\n" + "=" * 88)
    if c1 and c2:
        print("VERDICT: 🟢 DYAD-INTEGRATION — the causal tension-link makes the pair ONE")
        print("  more-integrated system: joint faithful φ_EI rises vs LINK-OFF AND vs the")
        print("  correlation-matched control — the rise comes from the CAUSAL channel,")
        print("  not from correlation per se.")
    elif not c1:
        print("VERDICT: 🔴 CHANNEL-NOT-INTEGRATING — the link transfers (H_1112/H_1113)")
        print("  but does NOT raise joint faithful φ_EI vs LINK-OFF: communication without")
        print("  integration at this coupling/cadence.")
    else:
        print("VERDICT: 🔴 CORRELATION-ARTIFACT — joint faithful φ_EI rises with the link")
        print("  ON vs OFF, but a correlation-matched COMMON-NOISE control (no causal A→B")
        print("  path) produces a statistically indistinguishable rise: at matched")
        print("  equal-time cross-correlation, the MI-matrix faithful φ_EI cannot tell a")
        print("  causal channel from a common drive. The φ-rise is explained by")
        print("  correlation alone — integration-as-measured is NOT causal-channel-specific.")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113")
    print("per-channel A⊥G dynamics; real-socket dyad-φ, cross-host, production cells and")
    print("scale UNVERIFIED — next rung. Mirror RE-PROVEN ≡ stdlib at n=4,5 (both engines)")
    print("and at the scoring n=6 (faithful, LIVE hexa re-capture) BEFORE scoring; MI in")
    print(f"BITS/log2 (a_phi_iit4_tool, NO proxy). SERIAL, $0 CPU local, 0-pod, g5/p7.")
    print(f"wall = {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
