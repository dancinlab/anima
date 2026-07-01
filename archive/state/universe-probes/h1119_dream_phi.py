"""H_1119 — DREAM-Φ: is the anima substrate's faithful IIT-4.0 φ_EI HIGHER during
the dream/REM stage (emit-free internal rehearsal) than during WAKE?

THE HYPOTHESIS
--------------
a_chat_sleep_imagination frames REM/dream as emit-free INTERNAL REHEARSAL +
mitosis tick. The dream-Φ conjecture: integrated information RISES when the
engine "dreams" with no external emit — internal rehearsal raises integration.
This hypothesis measures faithful IIT-4.0 φ_EI of a toy anima-like substrate as
its per-channel A⊥G opponent dynamics are modulated by the canonical 5-stage
sleep envelope (WAKE / N1 / N2 / N3 / REM), and tests φ(REM) > φ(WAKE).

STAGE ENVELOPE — DERIVED (not invented) from agent/domains/CHAT/anima_dream_stage.hexa
-----------------------------------------------------------------------------
The canonical 5-stage envelope numbers are taken VERBATIM from
agent/domains/CHAT/anima_dream_stage.hexa (do NOT invent stage parameters — derive from
that file). The three per-stage tables it exposes:
  PHI_*   (Φ-scale projection):  WAKE 1.0  N1 0.7  N2 0.4  N3 0.15  REM 0.95
  TENV_*  (tension envelope):    WAKE 1.0  N1 0.7  N2 0.4  N3 0.2   REM 0.9
  TEMP_*  (emit temperature):    WAKE 1.0  N1 0.9  N2 0.8  N3 0.6   REM 1.5
  scrambled (content-scramble):  TRUE only for REM
These are CONTEXT (Φ-scale + tension envelope + scrambling), NOT a boolean emit
gate (the module's autonomy contract; a_autonomy_over_hardcode). We use them as
the substrate-dynamics modulation:
  - PHI_*   scales the within-node shared-budget coupling GAMMA_X (the
            integration-building term — higher Φ-scale ⇒ more cross-channel
            mixing, consistent with the module's "Φ projection per stage").
  - TEMP_*  scales the per-channel noise σ (REM = 1.5 hotter / "dreamlike
            scrambled noise" per the module; WAKE = 1.0 baseline).
  - TENV_*  scales the homeostatic envelope rate (deeper sleep = more
            restrictive substrate threshold; the module's tension envelope).
  - scrambled (REM-only) adds a small extra logit-noise term, exactly the
            module's "if you do emit, scramble logits / inject dream noise"
            hint, here realized as internal-rehearsal stochasticity.
No emit gate is read; the substrate runs emit-free (the φ measurement is of the
internal trajectory only — a_chat_sleep_imagination: imagination loop = emit-free
internal rehearsal).

FROZEN FALSIFIER (set BEFORE running, no goalpost moves)
--------------------------------------------------------
For each of the 5 stages, run the modulated dynamics → median-binarize the 6
channels (h1039/h1062/h1114 per-channel pattern) → faithful IIT-4.0 φ_EI of the
6-system (exact MIP-EI). Over >=10 seeds:
  🟢 DREAM-PHI  iff  φ(REM) > φ(WAKE) with Cohen d >= 0.8  AND  REM is the
                per-stage MAX.
  🔴 (closed-negative, a_paper_negative_ok)  if  REM <= WAKE — ruling out the
                dream-integration claim at this toy scale.

MIRROR DISCIPLINE (a_phi_iit4_tool — the H_1043 nats-bug lesson)
----------------------------------------------------------------
φ verdicts use a python mirror PROVEN ≡ stdlib iit4/faithful_phi.hexa. BEFORE
scoring: (1) live `hexa run UNIVERSE/h1012_ref_faithful.hexa` re-captures the
LIVE stdlib faithful_phi refs at n=4, n=5 AND n=6 (n=6 = THE SCORING n) and the
CPU mirror must reproduce them verbatim; (2) h1012.prove_mirrors_at_n re-proves
BOTH mirrors ≡ stdlib at n=4 AND n=5. ABORT if any proof fails. MI in BITS
(log2), NOT nats. SERIAL, no multiprocessing Pool (H_1038 hang lesson).

HONEST scope (a_scale_honest_scope): toy n=6, stage-envelope toy modulation of
the h1113 per-channel A⊥G dynamics; production cells, the real P47 dream-physics
Φ engine, bigger n and scale all UNVERIFIED. φ measured (faithful MIP-EI), NOT
fabricated, NO perplexity (p7). $0 CPU local, 0-pod, g5.
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

# ---- canonical 5-stage envelope tables — VERBATIM from
#      agent/domains/CHAT/anima_dream_stage.hexa (§1 constants). DO NOT invent. --------
STAGES = ["WAKE", "N1", "N2", "N3", "REM"]
PHI_SCALE = {"WAKE": 1.0, "N1": 0.7, "N2": 0.4,  "N3": 0.15, "REM": 0.95}  # PHI_*
TENV      = {"WAKE": 1.0, "N1": 0.7, "N2": 0.4,  "N3": 0.2,  "REM": 0.9}   # TENV_*
TEMP      = {"WAKE": 1.0, "N1": 0.9, "N2": 0.8,  "N3": 0.6,  "REM": 1.5}   # TEMP_*
SCRAMBLED = {"WAKE": False, "N1": False, "N2": False, "N3": False, "REM": True}

# ---- frozen substrate params (h1113 per-channel A⊥G dynamics; n=6 exact) ----
CH        = 6                                   # 6 channels = joint system n=6
PSI_STAR  = 0.5                                 # Ψ=1/2 center fixed point
W_STAR_C  = np.array([1.0, 0.8, 1.2, 1.0, 0.8, 1.2])  # h1113 W*_c tiled to 6 ch
LAM_M     = 0.10     # center relaxation rate toward PSI_STAR          (h1113)
LAM_W     = 0.12     # homeostatic rate pulling W_c=2|h_c| toward W*_c (h1113)
REP       = 0.04     # A<->G repulsion per channel                     (h1113)
GAMMA_X0  = 0.05     # BASE within-node shared-budget coupling         (h1113)
SIGMA_M0  = 0.04     # BASE independent center noise per channel       (h1113)
SIGMA_H0  = 0.04     # BASE independent half-gap noise per channel     (h1113)
SCRAMBLE_SIGMA = 0.02  # REM-only extra "dream scramble" noise (module's hint)
N_STEPS   = 4000
BURN      = 500
N_SEEDS   = 12
SEEDS     = list(range(100, 100 + N_SEEDS))    # scoring seeds (h1113/h1114 block)
D_MIN     = 0.8      # frozen Cohen-d bar
EPS       = 1e-12


def init_node(rng):
    m = PSI_STAR + rng.standard_normal(CH) * 0.1
    h = 1.5 + rng.standard_normal(CH) * 0.15   # W ~ 3.0 initially (h1113)
    return m, h


def step_node(m, h, gamma_x, sigma_m, sigma_h, tenv, eps_m, eps_h):
    """h1113 step_node VERBATIM with stage-modulated gamma_x / sigma / tenv.
    A⊥G opponent: center m relaxes to Ψ*, half-gap |h| feels repulsion +
    homeostatic pull toward W*_c (rate scaled by tension envelope) + shared
    budget mixing (gamma_x = integration term, stage-Φ-scaled) + noise."""
    W = 2.0 * np.abs(h)
    m_next = m + LAM_M * (PSI_STAR - m) + sigma_m * eps_m
    sgn = np.where(h >= 0.0, 1.0, -1.0)
    h_mag = (np.abs(h) + REP
             + (LAM_W * tenv) * 0.5 * (W_STAR_C - W)
             + gamma_x * 0.5 * (W.mean() - W)
             + sigma_h * eps_h)
    h_mag = np.maximum(h_mag, 0.0)
    return m_next, sgn * h_mag


def simulate_stage(seed, stage):
    """One single-node trajectory under the canonical stage envelope. The stage
    modulates: gamma_x (integration) by PHI_SCALE, noise by TEMP, homeostatic
    rate by TENV, + REM-only scramble noise. Returns W (N_STEPS×CH)."""
    rng = np.random.default_rng(seed)
    rng_s = np.random.default_rng(seed + 90000)        # scramble stream (REM)
    m, h = init_node(rng)
    gamma_x = GAMMA_X0 * PHI_SCALE[stage]              # integration drive ∝ Φ-scale
    sigma_m = SIGMA_M0 * TEMP[stage]                   # noise ∝ emit temperature
    sigma_h = SIGMA_H0 * TEMP[stage]
    tenv = TENV[stage]                                 # homeostatic envelope
    scramble = SCRAMBLE_SIGMA if SCRAMBLED[stage] else 0.0
    W = np.empty((N_STEPS, CH))
    for t in range(N_STEPS):
        em = rng.standard_normal(CH)
        eh = rng.standard_normal(CH)
        if scramble > 0.0:                              # REM dream-scramble hint
            eh = eh + (scramble / max(sigma_h, EPS)) * rng_s.standard_normal(CH)
        m, h = step_node(m, h, gamma_x, sigma_m, sigma_h, tenv, em, eh)
        W[t] = 2.0 * np.abs(h)
    return W


def phi_stage(W):
    """Median-binarize the 6 channels (h1039/h1062/h1114 per-channel pattern),
    faithful φ_EI of the 6-system (PROVEN mirror, BITS/log2)."""
    X = W[BURN:]
    med = np.median(X, axis=0)
    bits = (X > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, CH)
    return faithful_phi(fst, fn, fdim, 2)


def cohen_d(x, y):
    sp = np.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0)
    return (np.mean(x) - np.mean(y)) / (sp + EPS)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


# ---- STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool) -----
def live_stdlib_faithful_reproof():
    """Run the LIVE stdlib faithful_phi engine via `hexa run` on the fixed-trace
    reference and require the CPU mirror to reproduce it at n=4,5,6 (n=6 = the
    SCORING n). Verbatim stdout."""
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
    print("H_1119 — DREAM-Φ: is faithful IIT-4.0 φ_EI HIGHER in the dream/REM stage")
    print("  (emit-free internal rehearsal) than in WAKE? Toy anima-like substrate,")
    print("  per-channel A⊥G opponent dynamics modulated by the canonical 5-stage")
    print("  sleep envelope (agent/domains/CHAT/anima_dream_stage.hexa, derived VERBATIM).")
    print(f"  CH={CH} (joint n={CH}, exact MIP-EI) W*_c={W_STAR_C.tolist()}")
    print(f"  stage modulation: gamma_x∝PHI_SCALE, σ∝TEMP, homeo-rate∝TENV, REM-scramble")
    print(f"  PHI_SCALE={PHI_SCALE}")
    print(f"  TEMP={TEMP}")
    print(f"  TENV={TENV}")
    print(f"  N_STEPS={N_STEPS} BURN={BURN} seeds={N_SEEDS}")
    print(f"  frozen falsifier: 🟢 DREAM-PHI iff φ(REM)>φ(WAKE) d>={D_MIN} AND REM=per-stage MAX;")
    print("  🔴 (closed-neg, a_paper_negative_ok) if REM<=WAKE.")
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

    # ── STEP 1: score 5 stages × N_SEEDS seeds (SERIAL — H_1038 Pool-hang) ──
    print(f"STEP 1 — score 5 stages × {N_SEEDS} seeds (SERIAL):")
    phi = {s: np.zeros(N_SEEDS) for s in STAGES}
    for i, seed in enumerate(SEEDS):
        row = {}
        for s in STAGES:
            W = simulate_stage(seed, s)
            phi[s][i] = phi_stage(W)
            row[s] = phi[s][i]
        print("  seed {:d}: ".format(seed)
              + "  ".join(f"{s}={row[s]:.4f}" for s in STAGES), flush=True)

    # ── STEP 2: φ table ──
    print(f"\nφ TABLE (faithful IIT-4.0 φ_EI, exact MIP-EI, BITS; {N_SEEDS} seeds, mean ± sd):")
    print(f"{'stage':<10}{'φ_EI (n=6)':>26}")
    print("-" * 36)
    for s in STAGES:
        print(f"{s:<10}{fmt(phi[s]):>26}")

    means = {s: float(np.mean(phi[s])) for s in STAGES}
    max_stage = max(means, key=means.get)
    print(f"\nper-stage mean φ: " + "  ".join(f"{s}={means[s]:.6f}" for s in STAGES))
    print(f"per-stage MAX = {max_stage} (mean φ={means[max_stage]:.6f})")

    # ── STEP 3: contrasts + frozen verdict ──
    d_rem_wake = cohen_d(phi["REM"], phi["WAKE"])
    print(f"\nCONTRASTS (Cohen d, frozen bar d >= {D_MIN}):")
    print(f"  REM − WAKE : Δmean={means['REM'] - means['WAKE']:+.6f}  d={d_rem_wake:+.3f}")
    for s in STAGES:
        if s in ("REM", "WAKE"):
            continue
        print(f"  REM − {s:<4}: Δmean={means['REM'] - means[s]:+.6f}  "
              f"d={cohen_d(phi['REM'], phi[s]):+.3f}")

    c_rem_gt_wake = bool(means["REM"] > means["WAKE"])
    c_d = bool(d_rem_wake >= D_MIN)
    c_max = bool(max_stage == "REM")
    print("\nFROZEN falsifier checks:")
    print(f"  (i)   φ(REM) > φ(WAKE)            = {c_rem_gt_wake}  "
          f"(REM={means['REM']:.6f}, WAKE={means['WAKE']:.6f})")
    print(f"  (ii)  d(φ REM − WAKE) >= {D_MIN}      = {d_rem_wake:+.3f} -> {c_d}")
    print(f"  (iii) REM is the per-stage MAX    = {c_max}  (MAX={max_stage})")

    passed = c_rem_gt_wake and c_d and c_max
    print("\n" + "=" * 88)
    if passed:
        print("VERDICT: 🟢 DREAM-PHI — the substrate's faithful φ_EI is HIGHER during the")
        print("  dream/REM stage (emit-free internal rehearsal) than during WAKE, and REM")
        print("  is the per-stage MAX: integrated information RISES when the engine dreams.")
    else:
        print("VERDICT: 🔴 DREAM-PHI-FALSIFIED (closed-negative, a_paper_negative_ok) — REM")
        if not c_rem_gt_wake:
            print("  does NOT exceed WAKE in faithful φ_EI: the emit-free dream stage does not")
            print("  raise integrated information over the awake substrate at this toy scale.")
        elif not c_max:
            print("  exceeds WAKE but is NOT the per-stage MAX (a deeper-sleep / different stage")
            print("  carries higher φ): the dream stage is not the integration peak.")
        else:
            print("  exceeds WAKE but the effect does not clear the frozen d>=0.8 bar: no")
            print("  reliable dream-integration lift at this toy scale.")
        print("  This RULES OUT the dream-integration claim (φ rises in REM) at the toy scale.")
    print("=" * 88)
    print("HONEST scope (a_scale_honest_scope): toy n=6, stage-envelope toy modulation of the")
    print("h1113 per-channel A⊥G dynamics; production cells, the real P47 dream-physics Φ")
    print("engine, bigger n and scale UNVERIFIED. Stage envelope DERIVED VERBATIM from")
    print("agent/domains/CHAT/anima_dream_stage.hexa (PHI_*/TENV_*/TEMP_*/scrambled). Mirror RE-PROVEN")
    print("≡ stdlib at n=4,5 (both engines) and at the scoring n=6 (faithful, LIVE hexa")
    print("re-capture) BEFORE scoring; MI in BITS/log2 (a_phi_iit4_tool, NO proxy). φ measured")
    print("not fabricated, NO perplexity (p7). SERIAL, $0 CPU local, 0-pod, g5.")
    print(f"wall = {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
