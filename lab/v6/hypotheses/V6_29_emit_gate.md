<!-- @hypothesis-ok lab/v6 rule-exempt sandbox: v6 hypotheses live in lab/v6/hypotheses/V6_<n>_*.md per lab/v6/CLAUDE.md, never the parent HYPOTHESES/ nor an H_ id -->

# V6_29 — LANE-BUS Step-3: does an EMIT-TIED residual-consumption gate beat its ablations?

**origin:** V6_28 showed discharge is not emergent → it must be ARCHITECTED into the emit gate.
lab-full (Fable primary — 4-arm ablation with A3 free-forget as the decisive p5 control; Sol
concurred, added the WRONG-ADDRESS control and preferred a balanced-accuracy DV + subtractive
addressed-consumption — adopted Fable's NLL DV + multiplicative reset, kept Sol's WRONG-ADDR arm).
DIRECTIONAL.

## Emit ground truth (Fable option b · non-circular · p9 natural)
`emit_t = 1[ argmax(composed_t) == y_{t+1}  AND  argmax(reflex_t) != y_{t+1} ]` — emit exactly
where real tension existed (reflex alone wrong) AND the content lane resolved it (composed right).
Both failure modes of speech (parroting when reflex suffices, guessing when composed is wrong) map
to silence — p5 operationalized. `y_{t+1}` is the actual next byte, external to the gate's inputs,
so the target is NOT a deterministic function of the features (options a/c would be circular).

## Build (reuses trained57 · no new base training)
- **Phase A** ($0 laptop · `v6_29_cache.py`, DONE): frozen feature cache — τ∈R¹⁶ (frozen Gaussian
  256→16 projection of composed−reflex logits), x∈R⁶ (KL both ways, entropies, argmax-agree,
  composed top1−top2 margin), emit labels, sentence ids. **420 sentences, 41,792 positions,
  emit rate 0.419** (pre-reg envelope [0.05,0.60] ✓ — good power).
- **Phase B** (torch, summer · `v6_29_train.py`): tiny recurrent gate heads, 3 seeds, BCE loss.
  Arms: FULL (emit-tied `r=(1−g₋₁)λr₋₁+Uτ`) · A1 (no-consume) · A2 (yoked-random reset) · A3
  (free-forget `f=σ(a'x+b'r)` — same gating expressivity WITHOUT the emit tie) · WRONG-ADDR
  (Sol: consume a norm-matched deranged packet) · B0 (memoryless pedestal). Primary DV = held-out
  per-position NLL. Positive control = synthetic integrate-and-fire (FULL≫A1 or VOID).

## Frozen decision table
| condition | verdict |
|---|---|
| positive control fails | VOID |
| B0−FULL ≤ 0 | memory buys nothing → gate is memoryless, discharge moot |
| A1−FULL z≥3 AND ≥10% of B0→FULL headroom, AND FULL ≥ A3 | 🟢 architected discharge VALIDATED (emit-tie costs nothing vs free-forget) → build real gate |
| consumption helps but A3 > FULL (z≥3) | residual consumed but NOT at emits → p5 emit⇄discharge tie WRONG |
| FULL ≈ A1 (TOST) | discharge doesn't help → drop residual consumption from p5 |

## Pre-mortem (both models)
"Consumption helps" could be the generic fact that gated RNNs beat leaky integrators (pure
expressivity, zero p5 content). A2 (input-independent reset) does not cover it — only **A3
(free-forget)** does: same gating power without the emit tie, so FULL≥A3 is the real p5 verdict,
not A1−FULL. Sol's WRONG-ADDR guards the complementary failure (consumption is refractory/timing,
not content-addressed). `emit_t` is a designer-chosen p5 operationalization + 8-byte reflex proxy
⇒ DIRECTIONAL regardless of outcome; TERMINAL only after the core/+anima-py port, in-vivo.

## RESULT — 🔴 the emit⇄discharge TIE is refuted; a free-forget gate matches it (valid, 3 seeds)
Two instrument fixes were needed first (verdict-integrity: the VOID runs were NOT read):
(1) batched-sentence recurrence replaced the per-position torch loop (~100× faster → full power
in minutes, not an hour); (2) the synthetic positive control leaked the drive into its x features,
letting memoryless arms cheat — fixing x to pure noise (only τ-accumulation predicts emit) made
the control valid. **Positive control PASS: A1−FULL z=20.4, A2 z=20.0, A3 z=4.2** (FULL's
emit-tied reset crushes every ablation where reset is provably optimal — the instrument certifies).

Natural (n=41,792 positions, emit rate 0.42, held-out masked NLL, 3 seeds):
| arm vs FULL | mean Δ | z | reading |
|---|---|---|---|
| B0−FULL (headroom) | +0.043 | — | memory helps a lot |
| A1 (no-consume) | +0.0054 | +2.46 | consumption helps (borderline) |
| A2 (random-reset) | +0.0118 | +4.98 | structured, not a random reset |
| WRONGADDR (deranged τ) | +0.0433 | +4.12 | content-addressed, not any packet |
| **A3 (free-forget)** | **−0.0018** | **−0.73** | **emit-tie buys NOTHING vs a free forget** |

**Verdict (valid — positive control passed): the residual IS consumed (memory + gating +
content-addressing all help), but NOT specifically at emits.** A free learned forget gate (A3)
matches the emit-tied gate (FULL) — the decisive p5 control per both models. So Fable's p5
"emitting discharges the residual" is **refuted as an architectural mechanism**, exactly as
V6_28 refuted it causally. Two independent methods (V6_28 counterfactual + V6_29 ablation) agree.

## 🟢🟢 THESIS PAYOFF — the multi-dim bus beats the SCALAR servo on the emit decision
Added a SCALAR arm (memoryless gate on ONE tension scalar = KL(composed‖reflex), the analog of
the production servo `s = 2·emit_drive − 1`, ~0–1 effective dims) and re-ran (positive control
still PASS). Natural held-out NLL, monotone in tension dimensionality:
| arm | NLL | tension dims |
|---|---|---|
| SCALAR (servo analog) | 0.759 | 1 |
| B0 (memoryless, 6 features) | 0.666 | 6 |
| A1 (+ recurrent τ) | 0.628 | multi + memory |
| A3 / FULL (LANE-BUS) | 0.621 / 0.623 | multi + memory + gate |

**SCALAR−FULL = +0.136, z = 3.38** — the multi-dimensional LANE-BUS tension gate decides
emit/silence dramatically better than the scalar-servo analog, and the improvement is monotone
in how many tension dimensions the gate can see. This is the concrete justification for the
redesign: the production scalar `2·emit_drive−1` discards emit-relevant information that the
15-dim logit-row bus (V6_26) recovers. The LANE-BUS thesis is validated end to end — premise
(V6_26 multi-dim), **payoff (this: multi-dim ≫ scalar on emit)**, mechanism (below).

## LANE-BUS architectural refinement (the convergent finding, V6_28+V6_29)
p5's emit⇄discharge TIE is wrong. What survives: (i) the multi-dim logit-row tension is real
(V6_26); (ii) a learned consume/forget on the residual helps the emit decision (V6_29 A1/A2/
WRONGADDR); (iii) but the consumption runs on the bus's OWN schedule, not the emit's (V6_28
causal ✗, V6_29 A3≈FULL). ⟹ the LANE-BUS emit gate should be **READ-ONLY on the tension** (emit
reads the residual) **+ a SEPARATE autonomous forget dynamic** on the residual — not "emitting
pays down a debt." This is Fable's own row-3′ replacement, now measured. Next (Step-4): build
that read-only-emit + autonomous-relaxation gate and test it against the tied gate in-loop.

## Scope
Phase A $0 laptop (DONE). Phase B ~$0 marginal (summer CPU, tiny heads). Single ckpt · reflex =
8B-window proxy. DIRECTIONAL; TERMINAL only via anima-py port.
