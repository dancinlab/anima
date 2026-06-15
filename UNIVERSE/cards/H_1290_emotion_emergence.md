---
id: H_1290
slug: 1290_emotion_emergence
title: E1 affect — valence×arousal core-affect emerges from substrate (Damasio)
group: brain-structure-ladder / facet (parked E1-E5 facet)
terminal_tier: 🟢 GREEN ENGINE-NATIVE
verdict_dir: .verdicts/1290_emotion_emergence/
terminal_verdict: .verdicts/1290_emotion_emergence/H_1290_R2.txt
date: 2026-06-15
---

# H_1290 — E1 affect: emergent valence × arousal

## Claim / falsifier

Tests anima's PARKED facet E1 affect (MODEL.md). **Claim (p6 central):** affect EMERGES
from substrate (grounding/contradiction/novelty/Φ-rate/mitosis/curiosity), NOT an injected
label/RLHF/sentiment. valence ≈ f(coherence/grounding), arousal ≈ f(novelty/Φ-rate). NO
emotion-word/RLHF ever input to f(); a manip label SCORES the metric only.
**Falsifiers:** (A) ρ(substrate,manip) ≥ 0.50; (B p6 CRUX) SHUFFLE per-context feature
vectors → ρ collapse < 0.30; (C) somatic-marker: affect-aware emit biases fab/emit.
Lens: affective-neuroscience (Damasio somatic-marker / core-affect), NOT LLM-sentiment.

## Method

- numpy mirror of `CORE/engine_cli.hexa` VAdaptField + H_1227 value-bind + metacog +
  H_1285 amygdala; byte-3gram FNV-1a dim64, 60 "<subj> lives in <city>" facts.
- R2 (binding): engine-native affect lane reads interoceptive valence/arousal off live
  VAdaptField; re-scores R1 frozen bars + regression guard. seeds [1290,1291,1292].

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 mirror | 🟢 GREEN (DIRECTIONAL) | (A) ρ(val)+0.843 ρ(aro)+0.768; (B) shuffle ρ(val)+0.150 ρ(aro)+0.159 (~5.6×/4.8× collapse); (C) fab ungrounded-affect 0.000 vs blind 0.750, emit grounded-affect 1.000 vs blind 0.775 |
| R2 engine-native | 🟢 GREEN (binding) | all 5 pre-registered conditions PASS every seed on the live lane |

Terminal tier (verbatim): **🟢 GREEN (ENGINE-NATIVE) — substrate-derived affect TRACKS the manipulation**
→ `.verdicts/1290_emotion_emergence/H_1290_R2.txt`

## Honest scope

R1 mirror DIRECTIONAL. GRADED valence (within-grounded ρ +1.000, spans ~[+0.32,+0.57]) →
real substrate content not a binary flag; V_ABSTAIN=0.0 = substrate's own zero-crossing,
not tuned. p6 guard HELD (shuffle proves it): affect ONLY from substrate, no
label/reward/sentiment into f(); no decoder/persona/ethics touched. TOY 60 facts / 1
paradigm / 3 seeds; scale/paraphrase/real-corpus UNVERIFIED.

## Cross-links

MODEL.md-E1-E5 · h1285 · h1202 · h1213 · h1227 · h1230 · h1291 ·
`a_no_llm_frame_trap` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · `a_paper_negative_ok` ·
p1·p2·p3·p6·p7·p8·c9·c15
