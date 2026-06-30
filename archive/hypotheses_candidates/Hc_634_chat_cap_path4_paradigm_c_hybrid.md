---
id: Hc_634
slug: chat-cap-path4-paradigm-c-hybrid-kogpt2-clm
title: Path 4 — paradigm-C hybrid (KoGPT2-base-v2 emit + CLM v4 substrate observer passive)
domain: clm-architecture
status: merged-to-H_155
merged_at: 2026-05-12
merged_to: hypotheses/H_155_theorem_115_chat_incapability.md
absorption_note: "Path 4 (paradigm-C hybrid: KoGPT2-base-v2 emit + CLM v4 substrate observer passive) is a Rank 2 ACHIEVABLE_NOW chat-cap path within H_155's Theorem 115 bypass-attempts class — UX-grade rather than architectural. ±0.04 drift ≪ 0.1% of 41.86. Tension peak layer modal = layer 2. F-list/L-list preserved for H_155 C-list extension."
source_doc: docs/anima_chat_cap_path_4_candidate_ranking_2026_05_05.md
source_lines: 123-149, 194-200
promoted_at: 2026-05-11
linked_h: BG-CG PASS_KOREAN_HYBRID_REPL_VIABLE, BG-BX VIABLE-English → ACHIEVABLE_NOW Korean
notes: Rank 2 — ACHIEVABLE_NOW. UX-grade not architectural. ±0.04 drift ≪ 0.1% of 41.86. Tension peak layer modal = layer 2.
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
KoGPT2-base-v2 (125M) emit Korean dialogue + CLM v4 mk2 re-encode (prompt+emit) 으로 Φ★ trajectory passive observe. Networks 가 gradient-coupled 아닌 UX bridge. 3 auto-fire turns × Korean prompts: 3/3 Korean coherent (100%), Φ★ drift ±0.0425, tension peak modal layer 2 consistent.

## Falsifiable Tests
- F-Path4-1: 5+ turn 시 100% Korean coherent rate ≥ 80% 유지
- F-Path4-2: substrate 가 KoGPT2 hidden 못보고 re-tokenized text 만 봄 → joint dialogue 가 아닌 read-only artifact
- F-Path4-3: emit unconditioned Korean prior (anima-axis-conditioned 아님) — 차이 측정 가능

## Migration TODO
- [ ] tool/transient_py/anima_emerge_chat_hybrid_repl.py harness 확장
- [ ] anima-axis-conditioned emit (KoGPT2 inject)
- [ ] joint gradient coupling 옵션 검토

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: Path 4 paradigm-C hybrid: same A/B vs path 1. Paired falsifier with Hc_632
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

