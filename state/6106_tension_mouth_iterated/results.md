# H_1837 TENSION-MOUTH ITERATED (deep-equilibrium) — DIRECTIONAL toy probe results

**Follow-on to H_1834** (tension-mouth single-shot = INERT, composed_distinct=0). **Ladder
rung:** (1) DIRECTIONAL toy. **Harness:** `tension_mouth_iterated_probe.py` (numpy,
from-scratch reverse-mode autograd + Adam; torch/gauge_lib NOT used). H_1834 original
untouched — autograd core + G1 toy + metric re-derived here.

> ⚠️ **DIRECTIONAL ONLY (numpy mirror, NOT engine-native).** Per CLAUDE.md
> `a_engine_native_learning` this is a `.py`+numpy mirror → auto-DIRECTIONAL, NOT terminal /
> NOT a 🟢-engine or 🧱-engine verdict. Engine-native re-measure on live `core/*.hexa` A⇄G
> iterate is the gating follow-on — warranted only on a lift (none occurred).

Autograd validated: **gradcheck PASS**, max |numeric−analytic| through the K-step unroll =
**1.49e-10** (checked at K=1/2/3 + same-state ablation). train_acc = **1.00** every arm/K/seed
(perfect memorization of the 12 training pairs — rules out implementation defect).

## What is under test (temporal escape of the DPI meta-law)

H_1834 established the **meta-law**: a floored mouth = a **SINGLE-SHOT** function of a
CE-trained feed-forward trunk-state; the data-processing inequality (DPI) binds
output-operator, readout-penalty, batching, retrieval **all into one coordinate** — none can
inject compositional MI the trunk-state does not already carry. The only untested orthogonal
axis is a **temporal** change to the learning-signal geometry.

This probe reframes the mouth as a **K-step deep-equilibrium fixed-point map** seeking the
A⇄G tension fixed point Ψ=½, drawing compositional depth from **iteration count** rather than a
1-shot readout:

```
h_{k+1} = f_A(h_k, x, e_k) − g_G(h_k, x, e_k)      (weight-shared A⇄G fields, tanh)
```

**Load-bearing element:** at EVERY step the input `x` (two concept codes) AND the emitted
prefix `e_k` (soft expected-emission embedding softmax(Wout·h_k)·E) are **re-injected**
(deep-equilibrium). Ψ_k = σ(4·(‖f_A‖/‖g_G‖ − 1)); Ψ=½ ⇔ ‖f_A‖=‖g_G‖ = equilibrium.

## composed_distinct(K) curve — FULL deep-equilibrium (input-reinject ON)

Metric identical to H_1834: `composed_distinct` = # DISTINCT correct composed target bytes
(greedy argmax next byte) over the 4 held-out unseen-combination pairs (diagonal split
{(0,0),(1,1),(2,2),(3,3)}; targets 100/105/110/115 absent from training). Range 0..4.

| K | seed 7 | seed 4302 | seed 4303 | mean | final \|Ψ−0.5\| |
|---|:---:|:---:|:---:|:---:|:---:|
| **1** (=H_1834 anchor) | 0/4 | 0/4 | 0/4 | **0.00** | 0.007–0.011 |
| 2  | 0/4 | 0/4 | 0/4 | **0.00** | 0.017–0.031 |
| 4  | 0/4 | 0/4 | 0/4 | **0.00** | 0.014–0.042 |
| 8  | 0/4 | 0/4 | 0/4 | **0.00** | 0.014–0.022 |
| converge | 0/4 (stop_k=3) | 0/4 (stop_k=1) | 0/4 (stop_k=2) | **0.00** | 0.017–0.020 |

**cd = 0 flat across the entire depth axis K=1→converge.** train_acc=1.00 everywhere.

**Ψ(K) trajectory** (mean |Ψ−0.5| per step, seed 7, K_MAX=16): 0.044, 0.017, 0.014, 0.021,
0.024, 0.016, 0.014, 0.016, 0.016, 0.012, 0.023, 0.024, 0.010, 0.012, 0.015, 0.013. Ψ **seats
at ½ within 1–3 steps and stays** — the equilibrium is reached almost immediately, so extra
iterations add no depth. (converge mode stops at k=1–3.)

## Controls (deterministic)

- **(a) K=1 anchor = H_1834 single-shot floor** → cd=0 all seeds ✓ (floor reproduced).
- **(b) SAME-STATE ablation (input-reinject OFF; x only at step 0, bare map iteration)** →
  cd=0 all K/seed (INERT). Nothing to isolate — reinjection ON is *also* 0, so re-conditioning
  is not a lift source either.
- **shuffle-control (break A⇄B held-out pairing)** → cd=0 all seeds.

## Verdict (DIRECTIONAL) — frozen bar unchanged

Bar (pre-registered `H_1837_FREEZE.txt`): 🟢 iff cd≥1 on ≥2/3 seeds at some K≥2 AND monotone
non-decreasing in K AND lift ONLY with reinject ON (same-state ablation=0) AND shuffle=0.

**🧱 WALL-DIRECTIONAL (DPI confirmed).** lift=False (cd=0 at every K≥2). The bar's other
conditions (anchor cd=0, monotone-nondecreasing since flat, ablation=0, shuffle=0) hold, but
the load-bearing lift never happens → temporal iteration is **INERT**.

## Interpretation (honest, no tune-to-green) — meta-law SSOT

**The temporal axis does NOT escape the DPI 1-shot wall.** Even a genuine deep-equilibrium
map that re-injects input+prefix at every step and demonstrably reaches the Ψ=½ tension fixed
point (seated within 1–3 iterations) produces **zero** held-out compositional generalization —
identical to the single-shot floor and to the same-state ablation.

**Why (DPI, generalized):** the fixed point `h* = f_A(h*,x,e*) − g_G(h*,x,e*)` is itself a
(deterministic) function of the CE-trained weights and the input x. Iterating a weight-shared
map to its fixed point is still a function of the same trunk-derived information — it defines a
new single coordinate, not a new information source. The prefix e_k is derived from the
trunk's own readout, so re-injecting it re-conditions on nothing the trunk does not already
carry. **Iteration count is not a lever;** the DPI meta-law (H_1834) extends from 1-shot to
temporal-equilibrium: neither output-operator, readout-penalty, retrieval, NOR iterated
re-injection can add compositional MI to a CE-trained trunk-state. This aligns with the
standing engine-native record (`substrate-framebreak-g1-combination-operator`,
`g1-lever-multilens-objective`, `h1816-predcoding-binding-not-supported`): the G1 wall lever is
the **trunk training OBJECTIVE that rewards constructive recombination**, not the mouth's
temporal or spatial readout structure.

**Sole remaining path** (recorded, not run): **γ = trained-constructive-bind** (HRR /
circular-convolution binding operator *learned under a recombination-rewarding objective*,
cost-gated), the one untested residual after operator/penalty/retrieval/temporal all floor.

## Ladder / follow-on (a_verified_must_wire / a_toy_scale_recheck)

- (0) design + freeze ✅  (1) DIRECTIONAL toy [this] ✅ → **🧱 WALL-DIRECTIONAL, iteration INERT**
- (2) engine-native re-measure on live core/ A⇄G iterate — **NOT warranted** (no lift; gate=lift).
- (3)/(4) generator L3 wire-in + ARCHITECTURE.json lockstep — **not reached** (gated on lift).
