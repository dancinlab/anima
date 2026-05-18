# §49 — PTD-aux DH-DL learned decision-head ↔ §24 Phase B emission loop

RESEARCH.md §49. $0 Mac CPU, NO GPU, NO model.forward, NO weight mutation.
Sequential single-agent (rate-limit avoidance). Isolation worktree.

## 1. What §49 did

§48 confirmed `PTD-AUX-SIGNAL-HOLDS-AT-SCALE`. §49 wired that §48-scale-
validated learned decision-head (`dhdl_ptd_head_s48_lam03.json`, shared
trunk 14->32 + decision head 32->16->3, lambda_ptd=0.3) into the §24
SPONTANEOUS Phase B unprompted-emission bounded-run loop, replacing the
hand-coded `talker_should_emit(score, safety_ok)` threshold with the
head's argmax over {CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}.

The §24 SSOT machinery (8-sensor scripted env_state, 8-factor motivation,
6-control safety conjunction, audit logger) is imported byte-equal from
state/spontaneous_phase_b_run_2026_05_18/run_bounded.py (not re-impl,
B-S49-3). Only the emission decision is swapped.

## 2. Headline measurement (g3 — measured only)

| metric | threshold loop (§24) | learned-head loop (§48) |
|---|---|---|
| unprompted_emission_rate | 0.05 (1/20) | 0.0 (0/20) |
| driven emission_count | 1 | 0 |
| per-step divergence (same sensors) | — | 20 / 20 |
| head argmax distribution | — | REMAIN_SILENT 20 / 20 |
| decisive-capability pattern | — | False |
| non-monotone-in-score | — | False |

Verdict: DISTILLATION, NOT CAPABILITY (expected, stated up front per g3).

## 3. Honest characterization of the 20/20 divergence

The 20/20 is NOT "head does something new" — it is the opposite: the
§48-distilled head collapses to the majority class (REMAIN_SILENT 20/20)
on the §24 scripted env_state. Root cause: the §48/§27 trace corpus is
~95% REMAIN_SILENT / ~4% EMIT_VOICE (§27 dist: CONTINUE_THINK 9 /
EMIT_VOICE 2128 / REMAIN_SILENT 45863). On this §24 stub the §24 scalar
threshold would emit every step (score ~0.51-0.63 >> IM_THRESHOLD 0.30)
but rate_limit (30 s) blocks all but the first -> driven rate 0.05. The
distilled head, trained on a 95%-silent label, outputs REMAIN_SILENT
everywhere -> driven rate 0.0. Every divergence is HEAD_SILENT_THR_EMIT
and every one is monotone-reachable by a scalar threshold (a higher cut
reproduces "silent at score ~0.5"). No non-monotone pair, no decisive-
capability pattern: nothing the §24 scalar threshold family cannot do.
This is the live-loop manifestation of §27's 0.00063 threshold-
distillation gap, amplified because the §24 stub sits where the corpus
class prior dominates.

## 4. Capability-vs-distillation verdict

DISTILLATION. The learned head is strictly more conservative than the
§24 threshold (collapses to SILENT), produces zero emissions, exhibits
no boundary a scalar threshold cannot. It learned the §24 threshold's
label distribution, not a richer emission policy. NOT GOAL emergence.

## 5. Connection points (BLUE)

- B-S49-1 SAFETY-OVERRIDE-PRESERVED: emit iff (argmax==EMIT_VOICE) AND
  safety_ok; not-safety => not-emit for all argmax (4-corner + sympy).
  Mirror §27 B-DHDL-4. 6-control safety overrides the head every step.
- B-S49-3 HEAD-OFF-REDUCTION: mode=threshold => active decision ==
  §24 talker_should_emit byte-equal (SSOT imported as run_bounded,
  AST-proven not re-implemented). Mirror §27 B-DHDL-5 / B-EBT-5.

## 6. B-S49 battery — 4/4 BLUE sidecar

blue_falsifier_s49.py (central blue_falsifier.py UNCHANGED):
B-S49-1 SAFETY-OVERRIDE-PRESERVED-CLOSED · B-S49-2 BOUNDED-STEP-EMPIRICAL
· B-S49-3 HEAD-OFF-REDUCTION-CLOSED · B-S49-4 DIVERGENCE-METRIC-
DETERMINISTIC. B-S49-NOTE = capability-vs-distillation OUTCOME empirical
(B-D-NOTE/B-DHDL-NOTE/B-S48-NOTE family, NOT counted BLUE).

## 7. GOAL distance

§15 milestone unchanged. north-star (GOAL.md) NOT reached. §49 = honest
substrate-integration + negative-capability datapoint. The §48 head is a
faithful (imbalance-collapsed) distillation of the §24 hand-coded
threshold; wiring it into the live loop produced fewer emissions, not
emergent spontaneity.

## 8. Honest C3

1. DISTILLATION expected and measured — §48 head's training label IS the
   §24 hand-coded threshold output. Stated before measuring (g3).
2. 20/20 divergence is collapse, not novelty — head outputs SILENT every
   step; all divergences HEAD_SILENT_THR_EMIT, all monotone-reachable.
   High divergence here = head is WORSE (more silent), not richer.
3. Identical-input comparison by construction — single head-mode run
   records BOTH decision vectors under ONE §24 sensor sequence; separate
   threshold run only cross-checks (independent wall drift; cross_run_
   consistent False because driven counts 1 vs 0 under rate_limit — the
   per-step decision vectors are the rigorous comparison).
4. Safety override holds (B-S49-1) — head argmax never bypasses the
   6-control safety AND; chooses only within an open gate.
5. env_state is the §24 scripted stub, not a trained-network forward.
6. No CAPABILITY pattern — no non-monotone-in-score boundary, nothing a
   scalar threshold cannot reproduce. Head learned the class prior.
7. HEAD-OFF reduction closed (B-S49-3) — mode=threshold => §24 byte-eq.
8. Class-imbalance is the honest driver — ~95% REMAIN_SILENT corpus; on
   this §24 stub the head defaults to that prior. Single-run illustrative.
9. §27 gap manifests amplified — in-corpus 0.00063 -> full majority-class
   collapse on out-of-prior physics. Head does not generalise the
   threshold to this region.
10. north-star unchanged; §15 milestone unchanged. §49 = wiring a §48-
    validated distilled head into the §24 right-target loop and HONESTLY
    reporting it stays distillation (and here, collapses). Valuable
    negative + mechanism-honest substrate-integration datapoint, NOT a
    GOAL-distance movement.
