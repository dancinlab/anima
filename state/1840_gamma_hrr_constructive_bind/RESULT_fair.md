# H_1840 STAGE-1 — FAIR (non-rigged) cheap-gate RESULT (DIRECTIONAL · GPU NOT fired)

**Verdict: 🧱 DIRECTIONAL — FAIR frozen-bar FAIL (0/3 on BOTH dominance clauses). The distilled
surviving delta — bypass-denied bilinear bottleneck (invertibility-agnostic) — is FALSIFIED as a
G1 lever. STAGE-2 engine-native GPU run NOT authorized (pre-registration honored, p7). γ / the
bypass-denied bilinear bottleneck collapses to the census G1 floor. G1 recombination wall
CONFIRMED (DPI meta-law) — all local + cheap levers now exhausted.**

Compute: aiden pool CPU, $0 (torch 2.10, OMP=4, seconds). torch mirror => DIRECTIONAL
(a_engine_native_learning) — no engine-native measurement, no 🟢/🧱 TERMINAL G1 verdict claimed.
Pre-registration = `FREEZE_fair.md` (frozen before run). This gate REPLACES the RIGGED PR#2689
cheap-gate whose target `K=circ_conv(A,B)` matched the HRR operator (operator↔algebra match).

## FAIR target (operator-agnostic random 2-way latent-interaction table T[fa,fb], C=9 classes)

chance heldout top-1 = 1/9 = 0.111. Target = random NON-additive P×P table over random class
keys — no arm's operator equals T (non-rigged by construction).

| arm | train_acc | heldout_acc (seeds 7 / 4302 / 4303) | composed_distinct |
|---|---|---|---|
| (a) additive | .944/.900/1.00 | 0.448 / 0.467 / 0.600 | 7/5/7 |
| (b) hadamard_bypass (=H_1819, bypass OPEN) | 1.00 | 0.655 / 0.667 / 0.733 | 7/7/8 |
| (c) hrr_bottleneck (invertible ⊛, bypass DENIED) | 1.00 | 1.000 / 0.767 / 0.967 | 9/7/8 |
| (d) noninv_bottleneck (⊛ ablated, bypass DENIED) | 1.00 | 0.862 / 0.833 / 0.967 | 8/8/8 |
| **(e) bilinear_bottleneck (NEW decisive: full learned bilinear, bypass DENIED, invertibility-agnostic)** | 1.00 | **0.552 / 0.567 / 0.533** | 6/7/8 |

### FROZEN-BAR verdict (FREEZE_fair.md, pre-registered)
- c1  e > additive + 0.34  (>=2/3): **FAIL 0/3**  (e=.55/.57/.53 vs a=.45/.47/.60)
- c2  e > bypass-open + 0.34 (>=2/3): **FAIL 0/3**  (e is WORSE than bypass-open on ALL 3 seeds)
- c3  all train >= .95 (>=2/3): FAIL 1/3 (additive under-fit on 2 seeds)
- c4  non-rigged control (bilinear NOT-dom additive & additive>=.50 on additive-target): FAIL
- => **STAGE-1 GATE: FAIL. GPU-fire authorized: FALSE.**

## What the FAIR gate actually falsified (two independent kills of the premise)

1. **The decisive arm is the WORST bottleneck, not the best.** The full learned bypass-denied
   bilinear bottleneck (e) generalizes at only 0.53–0.57 — below every structured bottleneck (c
   hrr, d noninv) and even below bypass-OPEN Hadamard (b). Denying the bypass + using a general
   bilinear path did NOT lift held-out recombination; it hurt it (the huge D×D² projection
   overfits, lacking the parameter-sharing inductive bias of the circulant ⊛). The one delta
   γ had left over H_1819 is measured-negative.

2. **Bypass-OPEN did NOT floor here (0.66–0.73).** The entire "deny the additive bypass" thesis
   rested on H_1819's bypass-open flooring. On a FAIR 2-way target, the bypass-open arm (b)
   generalizes fine — so denying the bypass is not the load-bearing lever. If the open bypass
   already recombines, closing it cannot be the missing mechanism.

Note: (c) hrr again generalizes well, but that is the SAME operator-inductive-bias flavor the
old (rigged) toy already showed — it is not the newly-registered decisive arm, and it does not
transfer any claim about natural language (a random synthetic table is not NL composite structure).

## Decision (a_break_the_wall · p7 · a_fire_autonomous)

GPU **not fired**. Rationale (multi-lens, evidence not budget — pool GPU was FREE $0):
1. Pre-registered FAIR gate FAILED as frozen; p7 forbids moving the bar. Card SSOT: "미통과면
   G1 벽 confirmed". Clauses c1 & c2 fail 0/3 — not a marginal miss.
2. γ's last unmeasured delta (bypass-denied bilinear bottleneck, invertibility-agnostic) is now
   measured-FALSIFIED on a FAIR (non-operator-matched) target — the arm is worst, not best.
3. bypass-OPEN already generalized on the fair target → the "deny bypass" mechanism is not
   load-bearing. Firing ~1 H100-day would be tune-to-green fishing against two independent kills.

## Honest scope (c9)

torch mirror => DIRECTIONAL. This is a mechanism screen: a PASS would only have AUTHORIZED the
engine-native `anima evaluate --py` GPU run (the terminal G1 test); a FAIL means the mechanism
does not survive even a fair synthetic task where genuine 2-way structure EXISTS — so it will not
survive natural language, whose composite structure the DPI meta-law + H_1819 engine-native floor
already indicate is not trunk-recoverable under CE. G1 recombination wall = trunk-objective /
combination-operator floor, CONFIRMED; the census's cheap + local lever space is now exhausted.

## Artifacts
- `FREEZE_fair.md` — pre-registration (frozen before run)
- `toy_fair_gate.py` + `toy_fair_result.json` + `run_fair.log` — 5-arm × 3-seed FAIR run + rig-control
- (superseded rigged gate: `FREEZE_toy.md` / `toy_cheap_gate.py` / `RESULT.md` — PR#2689)
