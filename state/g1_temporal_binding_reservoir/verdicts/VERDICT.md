# H_9259 VERDICT — 🧱 KILL: CONJUNCTION-MUST-BE-BAKED (DIRECTIONAL · numpy mirror)

**date:** 2026-07-10 · **seed:** 20260710 · **substrate:** $0 CPU numpy (a_scale_honest_scope · a_engine_native_learning ⇒ ceiling DIRECTIONAL, not GREEN)
**frozen bar:** card §6 (fixed BEFORE measurement, unmoved) · raw: `h9259_run1.txt` (arms+swap-margin) · `h9259_run2.txt` (retention-confound closer)

## Validity gates (card §6 ⛔) — PASS
- oracle-additive held8=0.000 (≤ chance 0.125), bitacc 0.292 → additive floor is REAL (XOR additive-immune, as the §3 theorem requires).
- oracle-bitprod held8=1.000, bitacc=1.000 → task IS learnable + compositionally generalizes from the D⊗R products.
- oracle-lookup held8=0.125 (chance) → memorization cannot generalize to unseen (D,R). Task valid.

## Result
| arm | held8 | Dprobe (retention) | swap-margin |
|---|---|---|---|
| conv-emit (anima emit point) | 0.099 | 0.019 | +0.002 |
| conv-pool (anima 0.95 probe analog) | 0.009 | **0.517** | −0.002 |
| esn-rho 0.0 / 0.6 / 0.9 / 1.1 | 0.015 / 0.057 / 0.062 / 0.041 | 0.000 | ≈0 |
| conv→esn rho 0.0 / 0.9 | 0.106 / 0.051 | 0.015 / 0.168 | — |
| **retention-fixed (v2):** esn-pool/esn-cat rho 0.6–1.1 | 0.001–0.015 | **1.000** | — |
| esnfeat-pool/cat rho 0.9 | 0.005–0.015 | **1.000** | — |
| convpool+esn (max info to linear head) | 0.006 | **1.000** | — |

## Reading
1. **anima signature reproduced** — conv-pool retains D (0.517) but XOR-binding floors (0.009); conv-emit loses D at the generation point (Dprobe 0.019) despite RF=31≥T=26 (formal coverage, effective RF-decay). Matches the session's 0.95-pool / emit-loss finding in a clean toy.
2. **Confound closed** — with retention forced to perfect (Dprobe=1.000, v2 pooled reservoir arms), held-out binding STILL floors and bit-accuracy lands at the ADDITIVE floor (~0.29 = oracle-additive 0.292). The floor is about **products, not retention**.
3. **ρ=0 vs ρ≥0.6 ablation** — no lift from the reservoir's nonlinear temporal feedback (0.015→0.062, all ≈ chance). An UNTRAINED random Volterra basis does not linearly expose the specific d_i·r_i products; only the hand-built exact basis (oracle-bitprod) does.

## Verdict (frozen rule 🧱)
**🧱 KILL — CONJUNCTION-MUST-BE-BAKED.** Every reservoir arm floors on held-out while oracle-bitprod solves it (1.000), and the floor persists at Dprobe=1.000. Retention is free; the non-additive D×R product is NOT obtainable from an *untrained* substrate + bounded linear readout. The combination operator must be **TRAINED into the trunk** (γ, H_1840).

**Consequence:** the frozen-readout G1 terminal **hardens**. Recurrent / spiking / neuromorphic substrates are **ruled out for the G1 wall** as *untrained* levers — 1st-gen AKD1000 (H_848: feedforward conv/FC/sepconv/pool/int4 op envelope) is a **distraction**. This falsifies H_1638's core bet (ESN transient-kernel gives the product basis for free). It converges with H_1000 (direct-trained GRU fails XOR) and H_1003 (curriculum-TRAINED GRU cracks XOR) — the conjunction is learnable only by *training* it into the substrate, i.e. γ trained-constructive-bind (H_1840, GPU-cost-gated, STEP-0 frozen-gate already guards a naive bolt-on).
