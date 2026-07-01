# Toy Co-train Bind Derisk — DIRECTIONAL (toy scale)

**Date:** 2026-06-29  
**Probe:** Pure numpy, $0 CPU, mini-safe. NOT engine-native TERMINAL.  
**Related 303M run:** `state/g1_cotrain_live_bind/` (a46b60ee, co-trained bilinear on 303M CLMConvMoE)  
**Background:** `state/g1_frozen_mouthbind_screen/RESULT.md` — frozen weights: all bind ops INERT/DESTRUCTIVE.

---

## Task Design

Two synthetic tasks to test whether co-trained bilinear binding generalizes to held-out concept combinations.

**Setup:** N_A=6 × N_B=6 = 36 combos, 8 held-out (stratified: each A and B value appears in training).  
D=12, Adam, 4000 steps, seeds=[7, 4302, 4303].

### Task A — Pure product regression (provable bilinear advantage)
Fixed random concept keys k_A[6×12], k_B[6×12]. Target: t_{a,b} = k_A[a] ⊙ k_B[b].

- **bind-ON**: pred = emb_A[a] ⊙ emb_B[b] (element-wise product, co-trained)
- **bind-OFF**: pred = emb_A[a] + emb_B[b] (additive, λ=0 equivalent)

*Why this task?* The additive model is structurally UNABLE to represent product targets (additive ≠ product). The bilinear can match the product by learning emb_A[a] ≈ k_A[a] and emb_B[b] ≈ k_B[b], which then generalizes to unseen combos.

### Task B — 36-class composition (closer to 303M setup)
Predict y = a·N_B + b (unique class per combo).

- **bind-ON**: trunk([ha;hb]) + bilinear(ha,hb) residual, co-trained (WD on weights only)
- **bind-OFF**: trunk([ha;hb]) only (λ=0)

---

## Results

### Task A: Product regression

| seed | bind-ON tr_MSE | bind-ON te_MSE | ratio | bind-OFF tr_MSE | bind-OFF te_MSE | ratio |
|------|---------------|----------------|-------|-----------------|-----------------|-------|
| 7    | 0.00012       | 0.00036        | 3.0   | 0.02453         | 0.08228         | 3.4   |
| 4302 | 0.00014       | 0.00011        | **0.8**| 0.03196        | 0.07389         | 2.3   |
| 4303 | 0.00018       | 0.00015        | **0.8**| 0.04149        | 0.11910         | 2.9   |

**bind-ON test_MSE < bind-OFF test_MSE: 3/3 seeds ✓**  
**bind-ON generalizes (ratio<2.0): 2/3 seeds ✓ | bind-OFF: 0/3 seeds ✗**

Key contrast:
- bind-ON absolute test_MSE: {0.00036, 0.00011, 0.00015} — very low, near-perfect prediction of held-out products
- bind-OFF absolute test_MSE: {0.082, 0.074, 0.119} — 200–700× higher; additive approximation fails to generalize

**Task A VERDICT: YES** — co-training with product composition CAN generalize to held-out combos.

### Task B: 36-class composition

| seed | bind-ON train | bind-ON te_acc | bind-ON te_CE | bind-OFF train | bind-OFF te_acc | bind-OFF te_CE |
|------|--------------|----------------|---------------|----------------|-----------------|----------------|
| 7    | 1.000        | **0.000**      | 10.48         | 1.000          | **0.000**       | 12.20          |
| 4302 | 1.000        | **0.000**      | 10.75         | 1.000          | **0.000**       | 12.41          |
| 4303 | 1.000        | **0.000**      | 10.24         | 1.000          | **0.000**       | 11.74          |

Both models memorize training set (100% train accuracy). Neither generalizes to held-out combos (0% test accuracy).

bind-ON does show consistently **lower held-out CE**: ~10.5 vs ~12.1 (∆≈1.5–1.7 nats). This suggests the bilinear op reduces confident-wrong predictions on unseen combos, even without exact-match improvement. (Note: CE>>ln(36)≈3.58 for both; both are confidently wrong, just bind-ON slightly less so.)

**Task B VERDICT: NO** (acc), WEAK-SIGNAL (CE) — trunk memorization dominates; bilinear residual insufficient.

---

## OVERALL VERDICT: PARTIAL-YES

**Mechanism check (Task A): YES** — product composition generalizes to held-out combos at toy scale.  
**Production-alike setup (Task B): NO** — trunk memorization overwhelms the bilinear's compositional advantage.

---

## Interpretation

### Why Task A works but Task B doesn't

**Task A** is designed so the additive model is STRUCTURALLY UNABLE to represent the targets. The bilinear MUST be used to fit training data, and this forces factored representations (emb_A[a] ≈ k_A[a], emb_B[b] ≈ k_B[b]), which then generalize.

**Task B** (classification) has no such constraint. The trunk MLP([ha;hb]) can memorize all 28 training combos independently using entangled representations. The bilinear residual is optional — and with the trunk already fitting training data, the bilinear's gradient doesn't push toward factored representations.

This mirrors the 303M finding precisely:
- **Frozen screen**: concept inputs = 0 → bilinear has nothing to bind → INERT
- **Task B**: trunk memorizes without concept axes → bilinear gets no useful gradient → INERT
- **Task A / co-train sweet-spot**: bilinear is REQUIRED by the task → gradients force factored reps → generalizes

### Implication for the 303M co-training run

The binding mechanism **CAN work** (Task A). But it requires an objective that **cannot be solved without composition**. For the 303M:

1. **If the CE objective on token sequences is enough** to force concept-axis encoding → bilinear co-training should help G1. Task A shows the mechanism works when needed.

2. **If the trunk can memorize G1-relevant sequences without concept axes** (likely, given clm303 G1=0 baseline) → bilinear will again be inert (same dynamic as Task B). This is the early warning.

3. **Decisive question for 303M:** does the G1 training signal (if any) make it IMPOSSIBLE for the trunk to fit training without the bilinear? Without a specific recombination objective (H_1602), the answer is likely NO.

**Confidence call for the 303M co-training run:**  
Mechanism is real (Task A ✓). But without a training signal that REQUIRES composition (like H_1602 recombination objective), the 303M trunk will memorize and the bilinear will remain inert. **MARGINAL early warning: co-training alone may not be sufficient if the trunk can memorize.**

---

## Framing

**TOY DIRECTIONAL** — a_toy_scale_recheck applies:
- Task A result (product generalizes) demonstrates the mechanism but uses synthetic targets that explicitly require bilinear computation.
- Task B uses a realistic setup and shows the memorization failure mode.
- Transfer to 303M scale is NOT verified. Toy green ≠ production verdict.

---

## Files

```
state/g1_toy_cotrain_bind_derisk/
├── probe.py           — full numpy probe (Task A + Task B)
├── raw_results.json   — machine-readable per-seed per-arm results
└── RESULT.md          — this file
```

**Related:**
- `state/g1_frozen_mouthbind_screen/` — frozen screen (INERT baseline)
- `state/g1_cotrain_live_bind/` — 303M co-train run (in-flight, a46b60ee)
- `state/binding_arch_census/exp3_303m/RESULT.md` — trained Hadamard G1=0 ∧ G6=0 ALL 9 arms
- `g1-closure-campaign-3lever-not-supported.md` — G1 closure NOT-SUPPORTED via 3 levers

**wired:** DIRECTIONAL (toy numpy probe, NOT engine-native TERMINAL)
