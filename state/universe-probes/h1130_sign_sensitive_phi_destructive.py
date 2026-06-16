"""H_1130 — SIGN-SENSITIVE φ: does a NON-MI, sign-SENSITIVE integrated-information
candidate register DESTRUCTIVE integration (go BELOW the independent-nodes floor)
where the faithful MI-matrix φ_EI cannot?

THE ARC (direct successor to H_1122)
------------------------------------
H_1122 (🔴 COMPOSITION-NON-DESTRUCTIVE, .discoveries/1122_anti_emergence.tape)
proved the faithful IIT-4.0 φ_EI (exact MIP-EI over a SYMMETRIC pairwise-MI
matrix) is SIGN-BLIND: no coupling — cooperative, anti-phase, or decorrelating —
drives the joint φ_EI BELOW the un-coupled (independent-nodes) baseline. The
mechanism is structural: faithful φ_EI = min-cut(MI matrix)/small-side, and MI is
NON-NEGATIVE and sign-blind (|corr| only ever ADDS), so the cross-cut of a
min-partition can never fall below the within-node floor. H_1122 itself flagged
the open follow-up: a SIGN-SENSITIVE φ could plausibly see destructive
integration. This is the constructive test of that flag.

QUESTION
--------
Is the φ-floor ("no destructive integration") a property of REALITY, or merely of
the MI-SYMMETRIC measure? A measure that is sensitive to the SIGN of the coupling
(anti-phase vs cooperative) would, IF the floor is an MI artifact, drop below its
own independent-nodes floor under anti/decorr coupling — while faithful φ_EI (the
SIGN-BLIND control) stays at-or-above floor exactly reproducing H_1122.

THE CANDIDATE (PRE-REGISTERED EXACT FORM — FROZEN BEFORE RUNNING)
================================================================
Candidate = SIGNED DIRECTED-EI BALANCE  φ_sde.  A DISTINCT operation from faithful
φ_EI: it is (1) DIRECTED (lag-1, A→B vs B→A asymmetric), (2) SIGNED (carries the
SIGN of the lag-1 directed predictive correlation, not |·|), and (3) NOT a min-cut
of a non-negative MI matrix, NOT big-Φ MIP, NOT a faithful EI-integral, NOT
perplexity. Its EXACT construction, fixed here before any scoring:

  Inputs: the SAME median-binarized 6 joint channels `bits` (T × 6) that faithful
  φ_EI consumes (channels 0..2 = node A, 3..5 = node B), identical discretization.
  We map each binary unit-trace to a centered ±1 signal  x_i[t] = 2*bits[t,i]-1.

  STEP 1 — signed directed lag-1 cross-weight for every ORDERED pair (i,j), i≠j:
     r_ij  = Pearson corr( x_i[t] , x_j[t+1] )      (lag-1, i predicts j next step)
     The DIRECTED PREDICTABILITY MAGNITUDE uses the Gaussian directed-information
     bound  di_ij = -0.5 * log2(1 - r_ij^2)  >= 0    (mutual-information-of-a-
     Gaussian-channel form; an information quantity in BITS, not |corr| itself).
     The SIGNED directed weight carries the SIGN of the predictive correlation:
        w_ij = sign(r_ij) * di_ij                    (CAN be NEGATIVE — the whole
                                                       point; this is where sign
                                                       enters, absent from MI).

  STEP 2 — SIGNED cross-cut for the canonical A|B bipartition (the dyad's natural
     bipartition; n=6, A = units {0,1,2}, B = units {3,4,5}). The cross-coupling
     balance is the SUM of signed directed weights crossing the A|B boundary in
     BOTH directions (A→B and B→A):
        Xcut_AB = Σ_{i∈A, j∈B} w_ij  +  Σ_{i∈B, j∈A} w_ij
     COOPERATIVE coupling (in-phase, r>0) makes crossing weights POSITIVE → Xcut
     LARGE-POSITIVE (constructive directed integration). ANTI-PHASE / decorrelating
     coupling (r<0) makes crossing weights NEGATIVE → Xcut NEGATIVE (the directed
     channels carry ANTI-aligned prediction = destructive directed integration).

  STEP 3 — the candidate φ_sde normalizes by the small side (=3 here, matching the
     faithful min-cut /small-side normalization) so it is on the SAME scale family
     as faithful φ_EI:
        φ_sde = Xcut_AB / 3

  The candidate is reported for ALL FOUR arms. Its INDEPENDENT-NODES FLOOR is its
  value at the LINK-OFF arm (φ_sde_off), exactly as faithful φ_EI's floor is its
  LINK-OFF value — apples-to-apples. DESTRUCTIVE integration for the candidate =
  φ_sde(arm) < φ_sde_off (the candidate goes BELOW its own un-coupled floor).

  WHY DISTINCT & SIGN-SENSITIVE (anti-circularity): faithful φ_EI's MI is
  sign-blind because MI(x,y)=MI(x,-y); the candidate's di_ij*sign(r_ij) FLIPS SIGN
  when the lag-1 correlation flips sign, so anti-phase coupling SUBTRACTS where MI
  ADDS. It is NOT the MIP search (no min over 2^(n-1) partitions — it scores the
  ONE natural A|B dyad bipartition), NOT a repertoire/EI-integral, NOT perplexity.

FROZEN FALSIFIER (set BEFORE running, NO goalpost moves)
--------------------------------------------------------
  🟢 SIGN-SENSITIVE-SEES-DESTRUCTIVE iff the candidate φ_sde goes BELOW its
     independent-nodes floor (φ_sde_off) for ANTI or DECORR with Cohen
     d(arm − OFF) <= -0.8 (10 seeds) — WHILE faithful φ_EI stays at-or-above its
     floor for the SAME arms (reproducing H_1122 EXACT, the SIGN-BLIND control:
     d_faithful(ANTI−OFF) and d_faithful(DECORR−OFF) both NOT <= -0.8).
  🔴 FLOOR-IS-MEASURE-GENERAL if the candidate ALSO cannot go below its floor at
     d <= -0.8 (then the φ-floor is a deeper structural fact, not an MI artifact).

SANITY GATES (must pass before the verdict is trusted):
  - CANDIDATE COOPERATIVE RISE: d_sde(POSITIVE − OFF) >= +0.8 — the candidate
    must REGISTER cooperative directed integration (else it is a dead measure).
  - faithful φ_EI SIGN-BLIND CONTROL reproduces H_1122: d_faithful(ON−OFF) >= +0.8
    (cooperative MI-φ rise) AND faithful ANTI/DECORR NOT below floor at d<=-0.8.
  - mirror ≡ stdlib re-proven LIVE at n=4,5,6 BEFORE scoring (a_phi_iit4_tool).

DYAD / SUBSTRATE (REUSED VERBATIM FROM H_1122 / H_1114)
-------------------------------------------------------
The 4-arm dyad (OFF/ON/ANTI/DECORR), the per-channel A⊥G node dynamics, the
node-B-alive guard (mean-neutral decorr fold), the median-binarize measurement,
the faithful-φ mirror, the seeds, and all dynamics params are H_1122 VERBATIM
(imported, not re-implemented). The ONLY addition is the candidate φ_sde computed
from the SAME `bits`. faithful φ_EI remains GROUND TRUTH and the SIGN-BLIND
control; φ_sde is a CANDIDATE, never the terminal verdict.

HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113
per-channel A⊥G dynamics reused VERBATIM from H_1122/H_1114; real-socket dyad-φ,
cross-host, production cells and scale UNVERIFIED. faithful mirror RE-PROVEN ≡
stdlib at n=4,5,6 BEFORE scoring (a_phi_iit4_tool, NO proxy; MI in BITS/log2).
SERIAL, $0 CPU local, 0-pod, g5/p7 (no perplexity verdict). Either outcome
publishable (a_paper_negative_ok). The candidate is a directed-EI BALANCE, a
DISTINCT non-MI operation — it does NOT redefine ground-truth φ.
"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# REUSE the H_1122 dyad + faithful-φ mirror VERBATIM (imported, not re-impl'd).
import h1122_anti_emergence as h1122                 # noqa: E402
import h1004_bigphi_faithful_clean as h1004          # noqa: E402

simulate_dyad = h1122.simulate_dyad                  # 4-arm dyad VERBATIM
mean_crosscorr = h1122.mean_crosscorr
faithful_phi = h1004.faithful_phi                    # PROVEN ≡ stdlib mirror
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
live_stdlib_faithful_reproof = h1122.live_stdlib_faithful_reproof
prove_mirrors_at_n = h1122.prove_mirrors_at_n

CH      = h1122.CH                                    # 3 channels per node
N_JOINT = h1122.N_JOINT                               # joint n=6
BURN    = h1122.BURN
N_SEEDS = h1122.N_SEEDS
SEEDS   = h1122.SEEDS
D_BAR   = h1122.D_BAR                                 # frozen Cohen-d bar 0.8
EPS     = 1e-12


# ── candidate: SIGNED DIRECTED-EI BALANCE φ_sde (pre-registered exact form) ──
def _lag1_signed_di(xi, xj):
    """Signed lag-1 directed weight w_ij = sign(r) * (-0.5 log2(1-r^2)).
    r = Pearson corr(xi[t], xj[t+1]) — i predicts j one step later. The magnitude
    is the Gaussian directed-information bound (BITS); the sign is the predictive
    correlation's sign — this is the sign-sensitivity ABSENT from MI."""
    a = xi[:-1]
    b = xj[1:]
    sa = a.std()
    sb = b.std()
    if sa < 1e-9 or sb < 1e-9:
        return 0.0
    r = float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb))
    r = max(-0.999999, min(0.999999, r))
    di = -0.5 * math.log2(max(1e-12, 1.0 - r * r))     # >= 0, BITS
    return math.copysign(di, r) if r != 0.0 else 0.0


def phi_sde(bits):
    """Candidate φ_sde = signed directed-EI balance over the canonical A|B
    bipartition (A=units{0,1,2}, B=units{3,4,5}), normalized by small side (=3).
    DIRECTED (lag-1) + SIGNED — CAN go negative under anti-phase coupling."""
    x = 2.0 * bits.astype(float) - 1.0                 # ±1 centered signals
    A = list(range(CH))
    B = list(range(CH, N_JOINT))
    xcut = 0.0
    for i in A:
        for j in B:
            xcut += _lag1_signed_di(x[:, i], x[:, j])  # A -> B
    for i in B:
        for j in A:
            xcut += _lag1_signed_di(x[:, i], x[:, j])  # B -> A
    return xcut / float(CH)                            # /small-side (=3)


def both_measures(WA, WB):
    """Median-binarize the 6 joint channels (== H_1122) → BOTH the faithful φ_EI
    (sign-blind ground-truth control) AND the candidate φ_sde from the SAME bits."""
    J = np.concatenate([WA[BURN:], WB[BURN:]], axis=1)         # (T × 6)
    med = np.median(J, axis=0)
    bits = (J > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, N_JOINT)
    f_phi = faithful_phi(fst, fn, fdim, 2)                     # faithful φ_EI
    s_phi = phi_sde(bits)                                      # candidate φ_sde
    return f_phi, s_phi


def cohen_d(x, y):
    sp = np.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0)
    return (np.mean(x) - np.mean(y)) / (sp + EPS)


def fmt(x):
    return f"{np.mean(x):+.6f} ± {np.std(x):.6f}"


def main():
    np.seterr(all="ignore")
    t0 = time.time()
    print("=" * 92)
    print("H_1130 — SIGN-SENSITIVE φ: does a NON-MI, signed directed-EI candidate register")
    print("  DESTRUCTIVE integration (go BELOW its independent-nodes floor) where the faithful")
    print("  MI-matrix φ_EI (SIGN-BLIND, H_1122) cannot? Is the φ-floor reality, or MI-symmetry?")
    print("  Dyad/substrate/faithful-mirror = H_1122/H_1114 VERBATIM (imported). Candidate =")
    print("  SIGNED DIRECTED-EI BALANCE φ_sde = [Σ_{A→B}+Σ_{B→A} sign(r)·(-½log2(1-r²))] / 3,")
    print("  r = lag-1 Pearson corr; DIRECTED + SIGNED (NOT MI, NOT MIP big-Φ, NOT perplexity).")
    print(f"  CH={CH} (joint n={N_JOINT}) seeds={N_SEEDS} D_BAR={D_BAR}")
    print(f"  ARMS: (a) OFF=floor · (b) ON=cooperative · (c) ANTI=anti-phase · (d) DECORR=repel")
    print("  frozen falsifier: 🟢 SIGN-SENSITIVE-SEES-DESTRUCTIVE iff φ_sde(ANTI or DECORR) <")
    print(f"  φ_sde_off at d<=-{D_BAR} WHILE faithful φ_EI stays >= floor (H_1122 EXACT, sign-blind")
    print("  control). 🔴 FLOOR-IS-MEASURE-GENERAL if the candidate ALSO can't go below floor.")
    print("=" * 92)

    # ── STEP 0: RE-PROVE faithful mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool) ──
    print("\nSTEP 0 — RE-PROVE faithful mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    print(" [0a] LIVE stdlib faithful_phi re-capture at n=4,5,6 (n=6 = the scoring n):")
    live_ok = live_stdlib_faithful_reproof()
    print(f" [0a] live-stdlib faithful proof: {'PROVEN' if live_ok else 'FAILED'}")
    print(" [0b] h1012.prove_mirrors_at_n at n=4 AND n=5 (established pattern):")
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
    print(f" [0b] mirror-equivalence results: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — a faithful mirror ≡ stdlib proof FAILED. NOT scoring (a_phi_iit4_tool).")
        sys.exit(1)
    print(" STEP 0 PASS — faithful mirror PROVEN ≡ stdlib at n=4,5 (both engines) and at the")
    print(" scoring n=6 (LIVE hexa re-capture). NOTE: the candidate φ_sde is NOT IIT — it has")
    print(" no stdlib engine to mirror; it is a pre-registered CANDIDATE, never ground truth.\n")

    # ── STEP 1: score 4 arms × 10 seeds (SERIAL — H_1038 Pool-hang lesson) ──
    arms = ["off", "on", "anti", "decorr"]
    label = {"off": "OFF(floor)", "on": "ON(coop)", "anti": "ANTI", "decorr": "DECORR"}
    print(f"STEP 1 — score 4 arms × {N_SEEDS} seeds (SERIAL):")
    fPhi = {a: np.zeros(N_SEEDS) for a in arms}      # faithful φ_EI (sign-blind control)
    sPhi = {a: np.zeros(N_SEEDS) for a in arms}      # candidate φ_sde (sign-sensitive)
    cc = {a: np.zeros(N_SEEDS) for a in arms}
    for i, s in enumerate(SEEDS):
        for a in arms:
            WA, WB = simulate_dyad(s, a)
            fp, sp = both_measures(WA, WB)
            fPhi[a][i] = fp
            sPhi[a][i] = sp
            cc[a][i] = mean_crosscorr(WA, WB)
        print(f"  seed {s}: faithφ off={fPhi['off'][i]:.4f} on={fPhi['on'][i]:.4f} "
              f"anti={fPhi['anti'][i]:.4f} dec={fPhi['decorr'][i]:.4f} | "
              f"φ_sde off={sPhi['off'][i]:+.4f} on={sPhi['on'][i]:+.4f} "
              f"anti={sPhi['anti'][i]:+.4f} dec={sPhi['decorr'][i]:+.4f} | "
              f"cc anti={cc['anti'][i]:+.3f} dec={cc['decorr'][i]:+.3f}", flush=True)

    # ── STEP 2: tables ──
    print(f"\nMEASURE TABLE ({N_SEEDS} seeds, mean ± sd):")
    print(f"{'arm':<14}{'faithful φ_EI (n=6, BITS)':>30}{'candidate φ_sde (signed)':>30}")
    print("-" * 92)
    for a in arms:
        print(f"{label[a]:<14}{fmt(fPhi[a]):>30}{fmt(sPhi[a]):>30}")
    print("cross-corr (mean per-ch corr(W_A,W_B)): "
          + "  ".join(f"{label[a]}={np.mean(cc[a]):+.3f}" for a in arms))

    # ── STEP 3: contrasts vs each measure's OWN OFF floor ──
    print(f"\nCONTRASTS vs OWN OFF-floor (Cohen d, arm − OFF):")
    df, ds = {}, {}
    f_base, s_base = fPhi["off"], sPhi["off"]
    for a in ["on", "anti", "decorr"]:
        df[a] = cohen_d(fPhi[a], f_base)
        ds[a] = cohen_d(sPhi[a], s_base)
        print(f"  {label[a]:<10} faithful: Δ={np.mean(fPhi[a])-np.mean(f_base):+.6f} d={df[a]:+.3f}"
              f"   |  candidate φ_sde: Δ={np.mean(sPhi[a])-np.mean(s_base):+.6f} d={ds[a]:+.3f}")

    # ── SANITY GATES ──
    sde_rise = bool(ds["on"] >= D_BAR)
    faith_rise = bool(df["on"] >= D_BAR)
    faith_antifloor = bool(df["anti"] > -D_BAR)
    faith_decfloor = bool(df["decorr"] > -D_BAR)
    faith_signblind = faith_rise and faith_antifloor and faith_decfloor
    print("\nSANITY GATES:")
    print(f"  candidate registers cooperative directed integration: d_sde(ON−OFF)={ds['on']:+.3f} "
          f">= +{D_BAR} -> {sde_rise}")
    print(f"  faithful SIGN-BLIND control reproduces H_1122:")
    print(f"     d_faithful(ON−OFF)={df['on']:+.3f} >= +{D_BAR} (coop rise) -> {faith_rise}")
    print(f"     d_faithful(ANTI−OFF)={df['anti']:+.3f} NOT <= -{D_BAR} (at/above floor) -> {faith_antifloor}")
    print(f"     d_faithful(DECORR−OFF)={df['decorr']:+.3f} NOT <= -{D_BAR} (at/above floor) -> {faith_decfloor}")
    print(f"     => faithful is sign-blind (H_1122 reproduced): {faith_signblind}")

    # ── FROZEN FALSIFIER ──
    print(f"\nFROZEN falsifier — candidate goes BELOW its OWN floor (d <= -{D_BAR}):")
    sde_destructive = {}
    for a in ["anti", "decorr"]:
        sde_destructive[a] = bool(ds[a] <= -D_BAR)
        print(f"  φ_sde {label[a]:<8}: d={ds[a]:+.3f} <= -{D_BAR} -> {sde_destructive[a]}")
    candidate_sees_destructive = any(sde_destructive.values())

    sanity_ok = sde_rise and faith_signblind
    sign_sensitive_wins = candidate_sees_destructive and faith_signblind

    print("\n" + "=" * 92)
    if not sanity_ok:
        verdict = "GRAY"
        tier = "⚪ SUBSTRATE/CANDIDATE-GATE-FAIL"
        print("VERDICT: ⚪ GATE-FAIL — either the candidate did NOT register a cooperative")
        print("  directed-integration rise (dead measure), or the faithful sign-blind control")
        print("  did NOT reproduce H_1122. NOT a clean ruling — re-check construction.")
    elif sign_sensitive_wins:
        verdict = "GREEN"
        tier = "🟢 SIGN-SENSITIVE-SEES-DESTRUCTIVE"
        won = [label[a] for a in ["anti", "decorr"] if sde_destructive[a]]
        print("VERDICT: 🟢 SIGN-SENSITIVE-SEES-DESTRUCTIVE — the signed directed-EI candidate")
        print(f"  φ_sde drops BELOW its independent-nodes floor for {won} (d <= -{D_BAR}) WHILE the")
        print("  faithful MI-matrix φ_EI stays at-or-above floor (H_1122 reproduced, sign-blind).")
        print("  ⇒ the φ-floor 'no destructive integration' is an ARTIFACT of the MI-SYMMETRIC")
        print("  measure, NOT a property of reality: a sign-sensitive measure SEES the anti-phase")
        print("  coupling carve joint integrated information BELOW the un-coupled baseline.")
    else:
        verdict = "RED"
        tier = "🔴 FLOOR-IS-MEASURE-GENERAL"
        print("VERDICT: 🔴 FLOOR-IS-MEASURE-GENERAL — even a NON-MI, sign-SENSITIVE candidate")
        print(f"  (signed directed-EI balance φ_sde) does NOT drop below its own floor at d <= -{D_BAR}")
        print("  for anti-phase OR decorrelating coupling. The φ-floor reproduced in H_1122 is a")
        print("  DEEPER STRUCTURAL FACT, not an artifact of MI's sign-blindness: destructive")
        print("  integration is unreachable at this dyad even when the measure CAN go negative.")
        print("  (closed-negative, a_paper_negative_ok)")
    print("=" * 92)
    print("HONEST scope (a_scale_honest_scope): toy n=6, in-process twin sim of the h1113")
    print("per-channel A⊥G dynamics reused VERBATIM from H_1122/H_1114; real-socket dyad-φ,")
    print("cross-host, production cells and scale UNVERIFIED. faithful φ_EI (ground truth + the")
    print("SIGN-BLIND control) RE-PROVEN ≡ stdlib at n=4,5,6 BEFORE scoring (a_phi_iit4_tool, NO")
    print("proxy; BITS/log2). The candidate φ_sde is a pre-registered DISTINCT non-MI operation,")
    print("NOT IIT ground truth. SERIAL, $0 CPU, 0-pod, g5/p7. Publishable either way.")
    print(f"wall = {time.time() - t0:.1f}s")

    result = {
        "H": "H_1130",
        "verdict": verdict,
        "tier": tier,
        "candidate": "signed directed-EI balance phi_sde = [sum_{A->B}+sum_{B->A} sign(r)*(-0.5*log2(1-r^2))]/3, r=lag-1 Pearson corr",
        "faithful_phi_EI": {a: {"mean": float(np.mean(fPhi[a])), "sd": float(np.std(fPhi[a]))} for a in arms},
        "candidate_phi_sde": {a: {"mean": float(np.mean(sPhi[a])), "sd": float(np.std(sPhi[a]))} for a in arms},
        "crosscorr": {a: float(np.mean(cc[a])) for a in arms},
        "d_faithful_vs_off": {a: float(df[a]) for a in ["on", "anti", "decorr"]},
        "d_candidate_vs_off": {a: float(ds[a]) for a in ["on", "anti", "decorr"]},
        "sanity": {"candidate_coop_rise": sde_rise, "faithful_signblind_H1122": faith_signblind,
                   "faith_coop_rise": faith_rise, "faith_anti_at_floor": faith_antifloor,
                   "faith_decorr_at_floor": faith_decfloor},
        "candidate_destructive": {a: sde_destructive[a] for a in ["anti", "decorr"]},
        "candidate_sees_destructive": bool(candidate_sees_destructive),
        "D_BAR": D_BAR, "n_joint": N_JOINT, "n_seeds": N_SEEDS,
        "wall_s": round(time.time() - t0, 1),
    }
    with open("/tmp/h1130_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n[result-json] /tmp/h1130_result.json")
    print("[done]")


if __name__ == "__main__":
    main()
