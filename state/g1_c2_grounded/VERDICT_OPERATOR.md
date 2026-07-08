# VERDICT — operator-vs-association clean toy (H_9234 · C2 Stage C closure)

**date** 2026-07-08 · **path** `state/g1_c2_grounded/operator_test.py` · numpy · torch-free · $0 mini · 3 seed

## Question
C2 Stage A+B (H_9216) proved the world channel is a valid **fuel** lever (association: held-out P(B|A) 0.49→0.96)
but left OPEN: does ANY fuel source (text OR grounded) let the CE substrate build the **combination OPERATOR**
(a non-additive function of both concepts), or is the operator architecturally unreachable so fuel never suffices?

## Rig (Fable design · zero-unary-MI · frozen-first)
- **32 atoms** = the 32 distinct 5-bit codes → bit marginal exactly 0.5 ⇒ `MI(output-bit ; single atom)=0` (additive floor = exact chance).
- **Operator target** `g(A,B)=φ_A XOR φ_B` (5 bits) — provably non-additive (a two-unary-detector-then-add model is exactly chance).
- **Substrate** = additive-readout (linear over `E[A]+E[B]`, CLMConvMoE-style summed logits) — the walled arch.
- **Positive control** = interaction arch (MLP over `concat(E[A],E[B])`) — must PASS (proves the split is learnable).
- **Fuel** (additive substrate only): held-out-pair co-occurrence as association exposure, NO target.
  `text` = same token embeddings; `grounded` = disjoint world embeddings `Ew` + bridge `T`, `E_eff=E+T·Ew` (a_substrate_disjoint).
- **Dual probe**: ASSOCIATION `P(B|A)` retrieval AUC (fuel should lift) vs OPERATOR XOR per-bit acc (the real bar).
- **FROZEN**: crack = grounded operator ≥0.85 ∧ text operator ≤0.60 ∧ gap ≥0.15.

## Result
```
GATE:  additive op=0.377 (XOR FAIL) · attention op=1.000 (PASS) · shuffle op=0.517 (chance ✓)
FUEL(additive substrate · 3-seed mean):
  no-fuel   operator 0.373 · association 0.079
  text-fuel operator 0.373 · association 0.495
  grounded  operator 0.375 · association 0.494
```

## 🔴 VERDICT — OPERATOR-WALL is readout-arch-localized; fuel builds ASSOCIATION not OPERATOR
- **crack = FALSE** (grounded op 0.375 ≪ 0.85). **modal prediction CONFIRMED.**
- Fuel lifts ASSOCIATION substantially (0.079→0.49, +0.41) but leaves OPERATOR at the additive floor (0.373, **identical to 3 decimals across no/text/grounded**).
- **text ≡ grounded** on both metrics (op 0.373 vs 0.375; assoc 0.495 vs 0.494) ⇒ the disjoint grounded channel confers **NO** operator advantage over text. `a_substrate_disjoint` does not crack the additive-readout operator wall.
- The operator is **reachable ONLY by an interaction arch** (attention/MLP = 1.000 on 150 held-out pairs), NOT by any coverage source.

## Reframe (the load-bearing finding)
The G1 wall is **not** "operator unreachable by any substrate" — it is **specific to the additive/linear readout** (production .clm sums per-position logits). An interaction/binding lane reaches the operator perfectly (1.00 held-out). This confirms the binding-lane reframe (ING #42492882: deep-ConvMoE + binding-lane REACHABLE) and the surviving γ trained-constructive-bind lever (#3108).

## Honest caveat (handed atoms)
This toy's atoms are **clean discrete tokens** (32 ids + explicit unary exposure teaching φ) = the HANDED-factorization condition. The kill-shot control (#3135) showed operator bind collapses on **blind learned encoder hiddens**. So the toy isolates that (a) additive readout can't do the operator even with clean atoms, and (b) interaction can — GIVEN clean atoms. Whether real byte-LM hiddens are clean enough for an interaction lane remains the #3135-open question. Two necessary conditions for the operator: interaction readout **and** clean/separable atoms.

## Consequence for C2
C2 = **fuel-only, confirmed.** The world channel feeds coverage-density (association) and never the operator; no coverage source (text or grounded) supplies the combination operator on an additive substrate. The one surviving engine lever for the operator = an **interaction/binding lane** on clean atoms (γ #3108), not more data / scale / fuel.
