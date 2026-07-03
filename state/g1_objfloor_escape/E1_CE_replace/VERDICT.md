# Escape-1 — CE-REPLACE contrastive/energy trunk objective (H_9121)

**Distinction vs EXP-1 (H_9120):** EXP-1 closed the *additive-aux* form
`L = CE + γ·L_recomb` (FALSIFIED, garble + novel=0). Escape-1 tests the *replace* form —
CE deleted entirely, trunk trained ONLY by an InfoNCE contrastive ranking
(bound-pair positive vs echo/wrong-D negatives). This moves the CE-basin's
echo-global-minimum (non-basin-preserving) rather than penalizing it additively. That
replace form was **unmeasured** before this run.

## TOY discriminator (numpy, mini, $0, DIRECTIONAL — not engine-native)
`toy_ce_replace_contrastive.py` — N=24 concepts, D=96, held-out compositional split
(20% pairs never seen composed), 400 epochs InfoNCE. Two arch variants under the
**same** contrastive-replace objective:
- **ADD** = additive/bilinear readout `h=C[A]+C[B]` (the current ConvMoE-class arch,
  no multiplicative binding slot) = **Escape-1 proper** (2×2 cell A01).
- **TPR** = role-filler tensor-product (multiplicative slot) = attribution side-probe
  (cell A11).

Probes on HELD-OUT pairs (echo-guarded, mirrors frozen G1 novel≥2 ∧ >max_single ∧
SCRAMBLE collapse): `margin = E(echo) − E(bound)` (>0 ⇒ bound preferred);
`reach_novel` = frac held pairs whose argmin-energy decode covers BOTH sigs AND
> max_single; `SCRAMBLE` control must not reach.

## Result (5/5 seeds {7,11,23,42,101,777})
| arch | margin | reach_novel | SCRAMBLE | verdict |
|------|--------|-------------|----------|---------|
| **ADD** (Escape-1) | **−0.47** (negative, all seeds) | **0.00** | 0.00 | **AT-FLOOR** |
| TPR (attribution) | +3.30 | 1.00 | ~0.01 | REACHABLE |

InfoNCE loss on ADD plateaus at ~1.20 (cannot fit the ranking); on TPR it drops to
~0.09 and generalizes to held-out pairs.

## Verdict: TOY AT-FLOOR → **TOY-FLOOR-SKIP** (303M training skipped, cost-saving)
The CE-replace contrastive objective is **INERT on the current additive/no-slot
architecture** — negative margin, zero held-out recombination reach, in every seed. The
*same* objective on a TPR (multiplicative binding slot) arch fully reaches (margin +3.3,
reach 1.0). Therefore the G1 floor is **ARCHITECTURAL, not objective**: replacing CE does
NOT move the floor unless a binding slot exists. This is exactly the design's own A01
prediction ("신호만 → 슬롯 없어 INERT, objective 무죄") and is consistent with H_9120
(additive-aux FALSIFIED) + H_1816 (additive L_bind trivial collapse).

Per the pre-registered cost gate (TOY AT-FLOOR ⇒ skip 303M), no pool/pod rent was
issued. The decisive unmeasured cell remains **A11 = TPR-register × contrastive**
(Escape target for a *future* experiment) — NOT contrastive-replace alone.

**Scope:** toy numpy DIRECTIONAL, not engine-native; not a 303M/frozen-bar verdict. No
HYPOTHESES/card/commit/PR/frozen touched (state artifact only; parent does bookkeeping).
Cost = $0.
