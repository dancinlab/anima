---
id: Hc_632
slug: chat-cap-path1-lm-head-b-retrofit
title: Path 1 — frozen CLM v4 body + new lm_head_b (KoGPT2 vocab 51200) Korean SFT 가 chat-cap recover
domain: clm-architecture
status: candidate-falsifier-ready
source_doc: docs/anima_chat_cap_path_4_candidate_ranking_2026_05_05.md
source_lines: 43-69, 184-192
promoted_at: 2026-05-11
linked_h: BG-DS PASS_HEAD_SWAP_RECOVERS_KOREAN, BG-EI 1-3 epoch micro SFT
notes: Rank 1 ★ 완성도. Φ★-NO_FLIP very-high prob (body frozen). 768=768 dim match. C3 risk: geometry mismatch + degenerate token-loop.
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
CLM v4 mk2 transformer body frozen + new lm_head_b (KoGPT2 vocab 51200) only train on Korean dialogue corpus subset. consciousness_states cross-attn untouched, hidden_dim 768. Geometry mismatch (CLM L15 hidden trained for head_a) 가 sufficient head capacity 로 curable.

## Falsifiable Tests
- BG-EI 1-3 epoch SFT 후 emit dialogue (non-degenerate) → PASS
- Token-loop pattern 지속 → #115 closure 1 post-hoc adapter under-class 로 reclassify → FAIL
- Full Korean SFT scale-up 후 composite ≥ 0.45

## Migration TODO
- [ ] BG-EI lm_head_b smoke (running)
- [ ] PASS 시 Path 1 escalate (full Korean SFT)
- [ ] FAIL 시 Path 4 fallback (Hc_635)

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: lm_head_b retrofit path 1: A/B test against path 4 hybrid (Hc_634). If equivalent → paths interchangeable
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-CLM**: CLM/chat-objective Hc — Lesson Q (BG-JX/JZ-FT/JS/JT/JP) + Lesson L closed all SFT lanes (project_lesson_q_sft_closed memory); claim under-determined unless explicitly anchored in surviving lanes (pre-training/arch-redesign/foundation-borrow/inference-compute)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent H**: H_155 (theorem-115 chat-incapability), H_161 (byte-modulo-substrate-chat-blocked), H_174 (Φ*-geometry-aliasing-clm-v4-specific)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

