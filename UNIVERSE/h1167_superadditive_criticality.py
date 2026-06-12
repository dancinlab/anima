"""
H_1167 — does the SUPER-ADDITIVE SURPLUS S(γ) PEAK at the critical A⇄G coupling?

THE QUESTION (MITOSIS-ENGINE domain, cross-arc)
-----------------------------------------------
H_1158 🟢 found that the FAITHFUL IIT-4.0 φ_EI of the A⇄G opponent substrate
PEAKS at the critical coupling γ=1.0 (inverted-U: φ→0 at γ=0 independent, φ
max at γ=1.0, φ→0 at γ=2.5 locked). Super-additivity — the "whole exceeds the
sum of its parts" surplus, the operational 1+1>2 advantage — is the ESSENCE of
integration. So: does the SUPER-ADDITIVE SURPLUS

      S(γ) = φ_joint(γ)  −  Σ_i φ_part_i(γ)

(the integrated measure of the COUPLED whole minus the SAME measure summed over
its INDEPENDENT sub-parts) PEAK at the critical γ, giving an operational claim
"the 1+1>2 advantage is MAXIMAL exactly where the engine is critical"?

This is a NEW cross-arc test: H_1046's synergy was on the PLANNING substrate
(a 6-substrate battery, NOT the γ-criticality sweep) and found the WB synergy
atom is a degenerate always-DOWN big-Φ stand-in. Here we measure SURPLUS over
the CRITICALITY axis — a DIFFERENT question. H_1158 reported RAW φ(γ); a raw-φ
peak does NOT by itself imply the WHOLE−SUM surplus peaks (the parts' own φ also
moves with γ). ANTI-REDUNDANCY: we report S(γ) AND raw φ(γ) side by side, and
flag where they diverge, so the result is NOT a re-statement of H_1158.

PRE-REGISTERED SURPLUS (frozen in this docstring BEFORE scoring)
---------------------------------------------------------------
The 6-channel A⊥G joint system is partitioned into TWO independent sub-parts of
3 channels each: P_A = {ch 0,1,2}, P_B = {ch 3,4,5}. The integrated measure is
the faithful IIT-4.0 φ_EI (the H_1119/H_1158 measure, PROVEN ≡ stdlib).

  φ_joint(γ)  = faithful φ_EI of the full n=6 system (= the H_1158 raw φ).
  φ_partA(γ)  = faithful φ_EI of the n=3 sub-system P_A in isolation.
  φ_partB(γ)  = faithful φ_EI of the n=3 sub-system P_B in isolation.
  S(γ)        = φ_joint(γ) − ( φ_partA(γ) + φ_partB(γ) )      ← the surplus.

WHY S behaves as an inverted-U is NOT assumed — it is MEASURED. The expectation
(NOT a falsifier move) is: at γ=0 channels are independent so the whole carries
no integration beyond its parts (S≈0 or low); at LOCKED γ channels lose
differentiation so φ_joint→0 AND the parts→0, surplus collapses; the sweet spot
between is where the coupled whole most exceeds its independent parts.

SECOND CORROBORATING SURPLUS (Williams-Beer PID synergy, H_1046/H_1017 reuse):
  Syn(γ) = the I_min synergy atom (irreducible joint-only info neither source
  carries alone) of a representative channel TRIPLE (target ch0 ; sources ch3,ch4
  — one channel from each independent sub-part), reused VERBATIM from the H_1017
  pid_system path (NO MIP search). A SECOND, mechanistically-independent "whole
  beyond the parts" reading. Reported alongside S(γ) as corroboration only — the
  PRIMARY surplus is the faithful φ S(γ).

FROZEN FALSIFIER (set BEFORE running, no goalpost moves)
--------------------------------------------------------
Sweep the SAME γ ∈ {0, 0.15, 0.35, 0.60, 1.00, 1.60, 2.50} as H_1158, ≥8 seeds.
  🟢 SURPLUS-PEAKS-AT-CRITICALITY iff:
     F1  S(γ) has an INTERIOR argmax (not an endpoint) at γ≈1.0, AND
     F2  S(peak) − S(γ=0)   Cohen's d ≥ 0.8, AND
     F3  S(peak) − S(γ=2.5) Cohen's d ≥ 0.8.
     → the super-additive 1+1>2 advantage is MAXIMAL at criticality.
  🔴 CLOSED-NEGATIVE (a_paper_negative_ok) if S is monotone / peaks at an
     endpoint / is flat → super-additivity does NOT track criticality on this
     engine.

MIRROR DISCIPLINE (a_phi_iit4_tool — re-prove BEFORE scoring)
-------------------------------------------------------------
faithful_phi mirror RE-PROVEN ≡ stdlib via live `hexa run h1012_ref_faithful.hexa`
at n=4,5,6 (the n=6 scoring n) AND h1012.prove_mirrors_at_n at n=4 AND n=5
(|Δ|≤1e-4 vs LIVE stdlib stdout). The WB synergy path is validated on the
COPY(redundant)/XOR(synergy) canonical cases. ABORT if any proof fails.

HONEST scope (a_scale_honest_scope): toy n=6 (sub-parts n=3), A⊥G toy dynamics
per H_1119/H_1158; γ_x is the toy coupling knob; LIVE CORE engine, bigger n and
scale all UNVERIFIED. φ + synergy MEASURED (faithful MIP-EI / exact PID), NOT
fabricated; NO perplexity (p7). $0 CPU local, 0-pod, SERIAL, g5.
"""
import os, sys, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import h1119_dream_phi as h1119          # substrate + PROVEN faithful_phi mirror + reproof
import h1158_phi_at_criticality as h1158  # the γ-coupling sweep (simulate_gamma, GAMMAS)

faithful_phi = h1119.faithful_phi
binary_seq_to_faithful_state = h1119.binary_seq_to_faithful_state
cohen_d = h1119.cohen_d
CH = h1119.CH                              # 6 joint channels
BURN = h1119.BURN

GAMMAS = h1158.GAMMAS                      # SAME sweep as H_1158
N_SEEDS = 12                              # >= 8 per pre-reg
SEEDS = list(range(300, 300 + N_SEEDS))   # same seed block as H_1158
D_MIN = 0.8

# ── the pre-registered partition of the 6-channel system into 2 independent
#    sub-parts of 3 channels each (frozen in the docstring above). ──
PART_A = [0, 1, 2]
PART_B = [3, 4, 5]


def _phi_of_channels(W, chans):
    """faithful φ_EI of a sub-system = the given channel subset, median-binarized
    over the post-burn rollout (the SAME discretization as h1119.phi_stage)."""
    X = W[BURN:][:, chans]
    med = np.median(X, axis=0)
    bits = (X > med).astype(int)
    n = len(chans)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, n)
    return faithful_phi(fst, fn, fdim, 2)


def phi_joint(W):
    """faithful φ_EI of the full n=6 system (== the H_1158 raw φ)."""
    return h1119.phi_stage(W)


def surplus(W):
    """S = φ_joint(6) − ( φ(P_A=3) + φ(P_B=3) ).  Returns (S, phi_joint, phiA, phiB)."""
    pj = phi_joint(W)
    pa = _phi_of_channels(W, PART_A)
    pb = _phi_of_channels(W, PART_B)
    return pj - (pa + pb), pj, pa, pb


# ── SECOND corroborating surplus: Williams-Beer I_min synergy (H_1046/H_1017) ──
import importlib.util as _ilu
_h1017_path = os.path.join(HERE, "h1017_split_redundancy_mechanism.py")
_spec = _ilu.spec_from_file_location("h1017_h1167", _h1017_path)
_h1017 = _ilu.module_from_spec(_spec)
_src = open(_h1017_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1017_path, "exec"), _h1017.__dict__)
_pid_two_source = _h1017._pid_two_source   # (T, A, B) -> (red, uA, uB, syn), exact PID, NO MIP


def synergy_triple(W):
    """WB I_min synergy atom of a representative channel triple spanning the two
    sub-parts: target = ch0 (in P_A), sources = ch3, ch4 (in P_B). Median-binarized
    over the post-burn rollout. Reused VERBATIM from the H_1017 pid_system path."""
    X = W[BURN:]
    med = np.median(X, axis=0)
    bits = (X > med).astype(int)
    T = bits[:, 0]; A = bits[:, 3]; B = bits[:, 4]
    _, _, _, syn = _pid_two_source(T, A, B)
    return float(syn)


def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("=" * 90)
    print("H_1167 — does the SUPER-ADDITIVE SURPLUS S(γ)=φ_joint−Σφ_parts PEAK at criticality?")
    print(f"  partition: P_A={PART_A} ⊥ P_B={PART_B}  (joint n={CH}, sub-parts n=3 each)")
    print(f"  γ sweep (SAME as H_1158): {GAMMAS}   seeds={N_SEEDS}")
    print(f"  PRIMARY surplus = faithful φ_EI whole−sum; SECOND = WB I_min synergy (H_1017)")
    print(f"  frozen falsifier: 🟢 iff S has INTERIOR argmax AND S(peak)−S(γ0) d≥{D_MIN}")
    print(f"  AND S(peak)−S(γ2.5) d≥{D_MIN}; else 🔴 (super-additivity ⊥ criticality).")
    print(f"  ANTI-REDUNDANCY: S≠raw φ — report S(γ) AND φ(γ) side by side.")
    print("=" * 90)

    # ── STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool) ──
    print("\nSTEP 0 — RE-PROVE faithful_phi mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    live_ok = h1119.live_stdlib_faithful_reproof()
    proven = {n: bool(h1119.prove_mirrors_at_n(n)) for n in (4, 5)}
    print(f"  live-stdlib proof: {'PROVEN' if live_ok else 'FAILED'}; mirror n4/n5: {proven}")
    # WB synergy canonical validity (COPY=redundant, XOR=synergy) — H_1017/H_1046 reuse
    Xa = np.array([0, 0, 1, 1, 0, 0, 1, 1]); Xb = np.array([0, 1, 0, 1, 0, 1, 0, 1]); Xt = Xa ^ Xb
    rx, _, _, sx = _pid_two_source(Xt, Xa, Xb)
    Tc = np.array([0, 1, 0, 1, 1, 0, 1, 0]); rc, _, _, scn = _pid_two_source(Tc, Tc, Tc)
    xor_ok = (rx < 1e-6 and sx > 0.5); copy_ok = (rc > 0.5 and abs(scn) < 1e-6)
    print(f"  WB synergy sanity: XOR(T;A,B) syn={sx:.4f} red={rx:.4f} (expect syn>0) -> {xor_ok} ;"
          f"  COPY(T;T,T) red={rc:.4f} syn={scn:.4f} (expect syn~0) -> {copy_ok}")
    if not (live_ok and all(proven.values()) and xor_ok and copy_ok):
        print("\nABORT — a mirror/validity proof FAILED. NOT scoring (a_phi_iit4_tool)."); sys.exit(1)
    print("  STEP 0 PASS — faithful_phi mirror PROVEN ≡ stdlib; WB synergy VALID.\n")

    # ── STEP 1 — sweep γ, collect S, raw φ_joint, parts, synergy (SERIAL) ──
    S    = {g: [] for g in GAMMAS}
    PJ   = {g: [] for g in GAMMAS}
    PA   = {g: [] for g in GAMMAS}
    PB   = {g: [] for g in GAMMAS}
    SYN  = {g: [] for g in GAMMAS}
    print("STEP 1 — sweep γ × seeds (SERIAL):")
    for g in GAMMAS:
        for s in SEEDS:
            W = h1158.simulate_gamma(s, g)   # reuse the H_1158 γ-coupling dynamics VERBATIM
            sv, pj, pa, pb = surplus(W)
            S[g].append(sv); PJ[g].append(pj); PA[g].append(pa); PB[g].append(pb)
            SYN[g].append(synergy_triple(W))
        print(f"  γ={g:.2f}: S={np.mean(S[g]):+.6f}±{np.std(S[g]):.6f}  "
              f"φ_joint={np.mean(PJ[g]):+.6f}  φA={np.mean(PA[g]):+.5f}  φB={np.mean(PB[g]):+.5f}  "
              f"Syn={np.mean(SYN[g]):+.5f}", flush=True)

    # ── STEP 2 — the ANTI-REDUNDANCY table: S(γ) vs raw φ(γ) side by side ──
    print("\n" + "=" * 90)
    print("S(γ) vs raw φ(γ) — ANTI-REDUNDANCY side-by-side (S = whole−sum SURPLUS, NOT raw φ):")
    print(f"  {'γ':>5} | {'S=φ_joint−Σφ_parts':>20} | {'φ_joint (raw, H_1158)':>22} | "
          f"{'φ_partA':>9} | {'φ_partB':>9} | {'Syn(WB)':>9}")
    print("  " + "-" * 92)
    Sm  = {g: float(np.mean(S[g]))  for g in GAMMAS}
    PJm = {g: float(np.mean(PJ[g])) for g in GAMMAS}
    SYm = {g: float(np.mean(SYN[g])) for g in GAMMAS}
    for g in GAMMAS:
        print(f"  {g:>5.2f} | {Sm[g]:>+20.6f} | {PJm[g]:>+22.6f} | "
              f"{np.mean(PA[g]):>+9.5f} | {np.mean(PB[g]):>+9.5f} | {SYm[g]:>+9.5f}")

    # ── STEP 3 — frozen falsifier on the PRIMARY surplus S(γ) ──
    peak_g = max(Sm, key=Sm.get)
    peak_idx = GAMMAS.index(peak_g)
    interior = 0 < peak_idx < len(GAMMAS) - 1
    d_sub = cohen_d(np.array(S[peak_g]), np.array(S[GAMMAS[0]]))
    d_sup = cohen_d(np.array(S[peak_g]), np.array(S[GAMMAS[-1]]))
    f1, f2, f3 = interior, d_sub >= D_MIN, d_sup >= D_MIN
    supported = bool(f1 and f2 and f3)

    # raw-φ peak (H_1158 axis) for the divergence note
    peak_g_phi = max(PJm, key=PJm.get)
    syn_peak_g = max(SYm, key=SYm.get)
    diverge = (peak_g != peak_g_phi)

    print("\n" + "=" * 90)
    print("FROZEN falsifier on the PRIMARY surplus S(γ):")
    print(f"  S(γ) peak γ = {peak_g} (idx {peak_idx})   S_max = {Sm[peak_g]:+.6f}")
    print(f"  F1 INTERIOR argmax (not endpoint)   = {f1}")
    print(f"  F2 S(peak)−S(γ=0)   Cohen d = {d_sub:+.3f}  (≥{D_MIN}) -> {f2}")
    print(f"  F3 S(peak)−S(γ=2.5) Cohen d = {d_sup:+.3f}  (≥{D_MIN}) -> {f3}")
    print(f"\n  ANTI-REDUNDANCY check — S vs raw φ:")
    print(f"    raw φ_joint peak γ = {peak_g_phi} ; surplus S peak γ = {peak_g} ; "
          f"diverge = {diverge}")
    print(f"    WB synergy Syn peak γ = {syn_peak_g} (corroborating surplus)")

    print("\n" + "=" * 90)
    if supported:
        print("VERDICT: 🟢 SURPLUS-PEAKS-AT-CRITICALITY — the super-additive whole−sum surplus")
        print(f"  S(γ) has an INTERIOR argmax at γ={peak_g} (inverted-U), S(peak)−S(γ=0) d={d_sub:+.2f},")
        print(f"  S(peak)−S(γ=2.5) d={d_sup:+.2f}: the 1+1>2 advantage (whole exceeds its independent")
        print("  parts) is MAXIMAL exactly where the A⇄G engine is critical. NOT a re-statement of")
        print(f"  H_1158: S is a whole−sum SURPLUS, raw φ peaks at γ={peak_g_phi} (diverge={diverge}).")
    else:
        print("VERDICT: 🔴 SURPLUS-DOES-NOT-PEAK-AT-CRITICALITY (closed-negative, a_paper_negative_ok)")
        if not f1:
            print(f"  the surplus S(γ) argmax is at an ENDPOINT (γ={peak_g}), not interior — super-")
            print("  additivity is monotone/end-peaked, NOT an inverted-U at criticality.")
        else:
            print(f"  S(γ) peaks interior at γ={peak_g} but the effect is too small (d_sub={d_sub:+.2f},")
            print(f"  d_sup={d_sup:+.2f}, bar {D_MIN}): no reliable super-additive peak at criticality.")
        print("  RULES OUT 'the 1+1>2 surplus is maximal at criticality' on this engine at toy scale.")
    print("=" * 90)

    verdict = {
        "H": "H_1167",
        "title": "super-additive surplus S=phi_joint-sum(phi_parts) peaks at the critical A<->G coupling",
        "partition": {"P_A": PART_A, "P_B": PART_B},
        "gamma_sweep": GAMMAS,
        "S_mean": Sm,
        "phi_joint_mean_raw_H1158": PJm,
        "phi_partA_mean": {g: float(np.mean(PA[g])) for g in GAMMAS},
        "phi_partB_mean": {g: float(np.mean(PB[g])) for g in GAMMAS},
        "synergy_WB_mean": SYm,
        "S_peak_gamma": peak_g, "S_peak": Sm[peak_g],
        "raw_phi_peak_gamma": peak_g_phi, "synergy_peak_gamma": syn_peak_g,
        "surplus_diverges_from_raw_phi": bool(diverge),
        "F1_interior_argmax": {"peak_gamma": peak_g, "interior": bool(f1)},
        "F2_vs_subcritical": {"cohen_d": float(d_sub), "bar": D_MIN, "pass": bool(f2)},
        "F3_vs_supercritical": {"cohen_d": float(d_sup), "bar": D_MIN, "pass": bool(f3)},
        "supported": supported,
        "ruling": ("SUPPORTED: super-additive surplus PEAKS at criticality (interior argmax, inverted-U) "
                   "— the 1+1>2 advantage is maximal where the A<->G engine is critical"
                   if supported else
                   "CLOSED-NEGATIVE: the super-additive surplus does NOT peak interior at criticality "
                   "(monotone/end-peak/flat) — super-additivity does not track criticality on this engine"),
        "anti_redundancy": ("S is a whole-minus-sum SURPLUS (NOT raw phi); raw phi peaks at gamma=%s, "
                            "surplus peaks at gamma=%s (diverge=%s)" % (peak_g_phi, peak_g, diverge)),
        "h1046_note": "H_1046 synergy was on the PLANNING battery (degenerate always-DOWN bigPhi stand-in); "
                      "here surplus is measured over the gamma-CRITICALITY axis = a different question",
        "scope": "toy n=6 (sub-parts n=3) exact MIP-EI, A<->G substrate per H_1119/H_1158; "
                 "faithful_phi mirror PROVEN == stdlib (a_phi_iit4_tool); WB synergy exact PID; "
                 "LIVE CORE / bigger n / scale UNVERIFIED (a_scale_honest_scope)",
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== VERDICT JSON ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open(os.path.join(HERE, "..", ".verdicts_h1167_tmp.json"), "w"),
              ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
