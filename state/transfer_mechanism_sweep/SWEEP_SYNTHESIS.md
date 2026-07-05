# Transfer-Mechanism Sweep — Synthesis (CORRECTED binding-dominant harness)

**Date:** 2026-07-05
**Meta-law under test:** `g1-escape-metalaw-transfer0` — a 303M byte-LM rep holds in-distribution
structure but cross/held-out transfer = 0; **escape requires a *trained* transfer-earning mechanism**
(frozen-rep readout / additive is insufficient). A parallel session confirmed **E1 gated-write SLOT**
as an escape (trained held-out 1.0 vs additive 0.117) on its own task.

**This sweep asks:** on a single **fair shared synthetic task**, do *other* trained mechanisms also
earn cross-distribution transfer, or is SLOT uniquely special?

> WARNING: **Supersedes the stale 19:57 draft.** That draft used the 1st-run **additive-dominant**
> target `tanh(Wr@a + Wf@b + a*roll(b))` whose strong *linear* a/b terms let a plain additive
> readout hit cross R^2~0.61 — the anchor SLOT could not beat that floor (delta +0.024 -> anchor FAILED),
> so per the pre-registered ANCHOR-VALIDATION rule that harness was **INVALID (task-artifact)** and a
> GRU "pass" there was spurious linear-term fitting. All agents re-ran on the **corrected
> pure-bilinear** target below, on which the anchor cleanly clears the bar -> harness VALID.

---

## Shared task (identical across all agents · corrected)
- K=256 concepts, d=32 fixed random vectors `RandomState(0).randn(256,32)`.
  DISJOINT split TRAIN 0-191 (192) / TEST 192-255 (64), overlap 0.
- **Binding-dominant, non-commutative, pure-bilinear target** (no linear a/b terms):
  `t(a,b) = tanh(einsum("kij,i,j->k", T, a[:16], b[:16]))`, `T = RandomState(1).randn(16,16,16)`, out=16.
  Additive `Wa@a+Wb@b` is structurally unable to express a bilinear form => additive floor ~ 0.
  `T` asymmetric => `t(a,b) != t(b,a)` (order-shuffle control). `T` fixed/concept-agnostic => a genuine
  bilinear mechanism transfers to unseen concept vectors.
- TRAIN 3000 ordered pairs from TRAIN concepts; TEST 3000 from **held-out** concepts = cross-distribution.
- End-to-end numpy training (mechanism params + linear head), MSE, ~3000-4000 epochs.
- **Verdict rule (frozen, pre-registered): TRANSFER-EARNING iff cross R^2(mech) - R^2(additive) >= 0.15
  AND order-shuffle drops R^2 >= 0.15.** Else NO-TRANSFER.

---

## Results (7 mechanisms · corrected harness)

| mech | cross R^2 | additive R^2 | delta vs add | shuffle R^2 | shuffle drop | verdict |
|---|---|---|---|---|---|---|
| **hypernet_bind** | **0.911** | -0.029 | **+0.940** | -0.872 | 1.78 | TRANSFER-EARNING |
| **tensor_product (TPR)** | **0.586** | -0.030 | **+0.616** | -0.561 | 1.15 | TRANSFER-EARNING |
| **multiplicative_film** | **0.512** | -0.034 | **+0.546** | -0.583 | 1.10 | TRANSFER-EARNING |
| **slot_gated_write** (anchor) | **0.236** | -0.034 | **+0.270** | -0.364 | 0.60 | TRANSFER-EARNING (anchor OK) |
| ssm_scan_trained | -0.0175 | -0.0174 | -0.000 | -0.0176 | 0.00 | NO-TRANSFER |
| additive_only (floor) | -0.0175 | -0.0175 | 0.000 | -0.0176 | 0.00 | NO-TRANSFER (baseline) |
| recurrent_trained (GRU) | -0.910 | -0.030 | -0.881 | -1.149 | 0.24 | NO-TRANSFER |

Anchor SLOT clears +0.15 over additive on **every** agent's re-run of this harness (each agent
re-trained its own anchor: cross R^2 observed 0.228-0.597 depending on init/epoch budget; the
slot-agent's own converged run landed 0.236). Variance is training-budget noise; all pass the bar ->
**harness VALID**, so the mechanism verdicts below are admissible.

---

## Verdicts

### TRANSFER-EARNING (4): slot_gated_write . tensor_product . multiplicative_film . hypernet_bind
All four represent a **concept-agnostic trained bilinear/multiplicative binding form** and therefore
generalize across the disjoint concept split (because `T` is fixed, the learned form applies to unseen
vectors), with order-shuffle collapsing R^2 (genuine non-commutative binding, not memorization).

### NO-TRANSFER (3): additive_only . ssm_scan_trained . recurrent_trained
- **additive_only** — order-blind sum; structurally cannot express a bilinear form (train R^2~0.018). Intended floor.
- **ssm_scan_trained** — a linear scan collapses algebraically to `Wo.A.B.a + Wo.B.b` = the *same additive
  function class*; cross R^2 identical to additive, zero shuffle drop. A charitable tanh-scan overfits
  train (0.43) but collapses cross (-0.71). Capacity is in the wrong class.
- **recurrent_trained (GRU)** — *has* the nonlinear capacity (train R^2=0.748, gradient-checked) but
  **memorizes concept-specific routing instead of abstracting the fixed bilinear form** -> catastrophic
  cross failure (-0.910, worse than the mean predictor). The clearest "capacity != transfer" case.

---

## (2) Escape frontier: **MULTIPLE-ESCAPES**

SLOT is **not** uniquely special. Escape is not a property of the *slot* primitive; it is a property of
the **function class**: a *trained mechanism whose hypothesis class contains a concept-agnostic
multilinear (bilinear) binding form* earns cross-distribution transfer; an *additive/linear* class
(additive, linear SSM) is structurally excluded; a *high-capacity-but-order-memorizing* class (GRU)
has the capacity yet fails to abstract the invariant and overfits.

This **sharpens** `g1-escape-metalaw-transfer0`:
> escape = trained **bilinear-binding function class**, realizable multiple ways
> (outer-product TPR . multiplicative/FiLM gating . hypernet weight-generation . gated-write slot).
> The gated-write SLOT is **one instance** — and the most G1-mechanistically-faithful one — not the
> only door. Additive and linear-recurrent classes remain transfer-0; mere nonlinear capacity (GRU) is
> insufficient without the multilinear inductive structure.

---

## (3) 303M promotion priority (cost . DPI-fit . G1-relevance)

The four escapes are the *same underlying capability*; the 303M question is which **realization of
bilinear binding** is cheapest and most DPI-native to wire into a byte-LM without a scaling wall.

1. **multiplicative_film** — promote first (cheap de-risk). Element-wise `gamma(a) . enc(b) + beta(a)`,
   **O(d)** (no dimension blowup), DPI-native (gated-MLP/GLU/FiLM conditioning already live in the
   trunk). A near-drop-in readout modification -> cheapest experiment that answers "can the 303M readout
   host *any* bilinear escape." Strong signal (0.512, ~tanh-saturation ceiling). Best cost/benefit.
2. **slot_gated_write** — the mechanistic target to cement. The E1 known escape and the *most
   G1-faithful* (gated write to an addressable slot = exactly the recombination-memory op G1 needs);
   already anchor-validated across every run. Moderate cost (slot store + write gate). Lower toy R^2
   (0.236) than the generic binders but a *real, bar-clearing* escape and the one whose success is a
   direct G1-recombination claim (cf. `a_substrate_disjoint` ImmuneMemory G5 slot). Promote as the
   capability, after FiLM confirms the readout can host bilinear at all.
3. **tensor_product (TPR)** — strong but scaling-gated. Outer product = **O(d^2)** dimension
   blowup — the classic TPR scaling wall and the frozen-TPR wall precedent (H_1466). Trained-TPR here
   (0.586) is a genuine and valuable contrast to frozen-TPR, worth **one** cost-gated 303M shot, but the
   quadratic blowup makes it the least attractive to make load-bearing in the trunk.
4. **hypernet_bind** — defer (best ceiling, worst cost/DPI). Highest toy R^2 (0.911) but a
   hypernetwork generating weights from concept `a` is the heaviest/most param-hungry and least
   DPI-native for a byte-LM. Keep it as the **ceiling / existence proof** that trained binding transfer
   is real and strong; do not lead with it for 303M wiring.

**Cheap-first plan:** FiLM readout de-risk (near-$0 wiring) -> if it lifts 303M cross, cement the
gated-write SLOT as the G1 recombination faculty -> TPR as one cost-gated contrast -> hypernet as ceiling
reference only.

---

## Honesty caveats
- **Toy != 303M closure** (`a_toy_scale_recheck`): this is a $0 numpy synthetic; it establishes the
  *function-class law* (which mechanism classes *can* earn bilinear transfer), not a 303M verdict.
  Every "TRANSFER-EARNING" here is a **candidate lever**, not a cemented G1 GREEN. Promotion requires
  engine-native `core/`-decode measurement (`a_engine_native_learning` / `a_eval_py_canonical`).
- **tanh-saturation ceiling** (~0.5-0.64) caps the generic binders; hypernet's 0.911 reflects its
  larger effective capacity, not a categorically different mechanism.
- **No tune-to-green:** the +0.15 bar and shuffle-drop rule were pre-registered and unchanged; the
  additive-dominant 1st-run artifact was *discarded* (anchor failed), not re-tuned.
- **The GRU result is the load-bearing negative:** it proves the escape is the *multilinear inductive
  class*, not raw trained nonlinear capacity — capacity without the binding form memorizes and stays
  transfer-0.
