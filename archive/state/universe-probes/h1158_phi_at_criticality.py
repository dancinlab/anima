"""
H_1158 — does FAITHFUL IIT-4.0 φ_EI PEAK at criticality (the A⇄G coupling sweet
spot)? Substrate-unique re-test of H_931/H_927, which found a Φ-PEAK at the
self-organized-critical point using the SILICON PROXY (phi_silicon_proxy) — NOT
the faithful measure. a_phi_iit4_tool warns proxies are purpose-blind (H_988/989
scored random==intentional). So: does the criticality↔consciousness peak SURVIVE
the faithful IIT-4.0 φ_EI, or was it a proxy artifact? Connects H_1153 (σ≈1
branching critical point) + H_931 (SOC Φ-peak) + the faithful Φ stack.

METHOD: reuse the H_1119 6-channel A⊥G opponent substrate + the PROVEN faithful_phi
mirror (≡ stdlib iit4/faithful_phi.hexa, re-proved at n=4/5/6 BEFORE scoring), but
sweep the INTEGRATION/COUPLING knob gamma_x (sub-critical independent → critical →
super-critical locked) at a FIXED wake-baseline envelope (NOT the dream stages).
Faithful φ_EI at each gamma over >=12 seeds.

FROZEN FALSIFIER:
  F1 INVERTED-U: argmax over the gamma sweep is INTERIOR (not the smallest or
     largest gamma) — a peak at criticality, not a monotone.
  F2: φ(peak) − φ(gamma_min) Cohen's d ≥ 0.8.
  F3: φ(peak) − φ(gamma_max) Cohen's d ≥ 0.8.
  SUPPORTED iff F1 ∧ F2 ∧ F3 → faithful φ PEAKS at criticality (H_931 proxy-peak
  CONFIRMED faithfully — criticality↔consciousness holds under the rigorous measure).
  CLOSED-NEGATIVE iff monotone / end-peak → the proxy-Φ-peak was a proxy artifact;
  faithful φ does NOT track the SOC critical point (a_paper_negative_ok).
toy n=6 exact MIP-EI; A⊥G substrate per H_1119 (a_scale_honest_scope).
"""
import os, sys, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import h1119_dream_phi as h1119   # reuse substrate + PROVEN faithful_phi mirror + reproof

CH = h1119.CH
N_STEPS = h1119.N_STEPS
N_SEEDS = 12
SEEDS = list(range(300, 300 + N_SEEDS))
# criticality knob = the A<->G integration/coupling gamma_x (sub -> critical -> super)
GAMMAS = [0.0, 0.15, 0.35, 0.60, 1.00, 1.60, 2.50]
D_MIN = 0.8


def simulate_gamma(seed, gamma):
    """H_1119 dynamics at a FIXED wake-baseline envelope (no dream modulation),
    sweeping ONLY gamma_x (the A<->G coupling / criticality knob)."""
    rng = np.random.default_rng(seed)
    m, h = h1119.init_node(rng)
    sigma_m = h1119.SIGMA_M0          # wake baseline (TEMP=1.0)
    sigma_h = h1119.SIGMA_H0
    tenv = 1.0                         # wake homeostatic envelope (TENV=1.0)
    W = np.empty((N_STEPS, CH))
    for t in range(N_STEPS):
        em = rng.standard_normal(CH); eh = rng.standard_normal(CH)
        m, h = h1119.step_node(m, h, gamma, sigma_m, sigma_h, tenv, em, eh)
        W[t] = 2.0 * np.abs(h)
    return W


def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("="*88)
    print("H_1158 — does FAITHFUL φ_EI PEAK at criticality (A⇄G coupling gamma_x sweep)?")
    print(f"  re-test of H_931 proxy-Φ-peak with the FAITHFUL measure; CH={CH} exact MIP-EI")
    print(f"  gamma sweep (sub→critical→super): {GAMMAS}  seeds={N_SEEDS} N_STEPS={N_STEPS}")
    print(f"  frozen falsifier: SUPPORTED iff interior argmax (inverted-U) AND")
    print(f"  φ(peak)-φ(min) d>={D_MIN} AND φ(peak)-φ(max) d>={D_MIN}; else 🔴 (proxy artifact).")
    print("="*88)

    # STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool), reused from H_1119
    print("\nSTEP 0 — RE-PROVE mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    live_ok = h1119.live_stdlib_faithful_reproof()
    proven = {n: bool(h1119.prove_mirrors_at_n(n)) for n in (4, 5)}
    print(f" live-stdlib proof: {'PROVEN' if live_ok else 'FAILED'}; mirror n4/n5: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — mirror ≡ stdlib proof FAILED. NOT scoring (a_phi_iit4_tool)."); sys.exit(1)
    print(" STEP 0 PASS — faithful_phi mirror PROVEN ≡ stdlib.\n")

    phis = {g: [] for g in GAMMAS}
    for g in GAMMAS:
        for s in SEEDS:
            phis[g].append(h1119.phi_stage(simulate_gamma(s, g)))
        arr = np.array(phis[g])
        print(f"  gamma={g:.2f}: phi = {arr.mean():+.6f} ± {arr.std():.6f}", flush=True)

    means = {g: float(np.mean(phis[g])) for g in GAMMAS}
    peak_g = max(means, key=means.get)
    peak_idx = GAMMAS.index(peak_g)
    interior = 0 < peak_idx < len(GAMMAS)-1
    d_min = h1119.cohen_d(np.array(phis[peak_g]), np.array(phis[GAMMAS[0]]))
    d_max = h1119.cohen_d(np.array(phis[peak_g]), np.array(phis[GAMMAS[-1]]))
    f1, f2, f3 = interior, d_min >= D_MIN, d_max >= D_MIN
    supported = bool(f1 and f2 and f3)
    verdict = {
        "H": "H_1158", "title": "faithful IIT-4.0 phi peaks at criticality (A<->G coupling sweet spot)",
        "gamma_sweep_phi_mean": means,
        "peak_gamma": peak_g, "peak_phi": means[peak_g],
        "F1_interior_argmax": {"peak_gamma": peak_g, "interior": bool(f1)},
        "F2_vs_subcritical": {"cohen_d": float(d_min), "bar": D_MIN, "pass": bool(f2)},
        "F3_vs_supercritical": {"cohen_d": float(d_max), "bar": D_MIN, "pass": bool(f3)},
        "supported": supported,
        "ruling": ("SUPPORTED: faithful phi PEAKS at criticality (inverted-U) — H_931 proxy-Phi-peak CONFIRMED under the faithful measure; criticality<->consciousness holds rigorously on the A<->G engine"
                   if supported else
                   "CLOSED-NEGATIVE: faithful phi does NOT peak interior at criticality (monotone/end-peak) — the H_931 silicon-proxy Phi-peak was a proxy artifact, not faithful"),
        "h931_ref": "proxy Phi-peak at K~4/edge-of-chaos (phi_silicon_proxy, NOT faithful)",
        "scope": "toy n=6 exact MIP-EI, A<->G substrate per H_1119; faithful_phi mirror proven == stdlib (a_phi_iit4_tool); a_scale_honest_scope",
        "wall_s": round(time.time()-t0, 1),
    }
    print("\n=== VERDICT ===\n"+json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open(os.path.join(HERE, "..", ".verdicts_h1158_tmp.json"), "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__": main()
