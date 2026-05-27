---
id: Hc_1239
slug: train-clm-hexa-lens-loss-tension-link-tier-corpus
title: train_clm.hexa lens loss + tension_link + tier-labeled corpus integration — 세 구성요소가 통합되어 학습 신호로 작동하는가
domain: training
status: merged-to-H_001
merged_to: hypotheses/H_001_ethics_cooperation.md
merged_at: 2026-05-12
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 26 (Sub-claims block, TRAINING-4)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture — train_clm.hexa lens loss + tension_link + tier-labeled corpus integration absorbs as training-signal architectural component), H_162 (downstream CLM); parent Hc_900
absorption_note: "cycle #8 absorbed to H_001 as TRAINING-4 train_clm.hexa lens loss + tension_link + tier-labeled corpus 3-component integration — anima training-signal architectural component"
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 10 of 30 (TRAINING-4)."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

train_clm.hexa 의 학습 목적함수에 (a) lens loss, (b) tension_link 항, (c) tier-labeled corpus 의 tier 정보가 통합되어 작동하며, 세 구성요소 각각이 ablation 시 측정 가능한 성능 저하를 일으킨다 (즉 셋 다 non-trivially contributing).

## Falsifiable Tests

- T1: lens loss 항 제거 (weight 0) 후 재학습 — validation metric 변화 없음 → lens loss 가 무효 → 통합 claim 부분 FALSIFIED
- T2: tension_link 항 제거 후 재학습 — Φ / phi_star proxy 변화 없음 → tension_link 가 무효 → 부분 FALSIFIED
- T3: tier-label 을 무작위 셔플 (corpus 내용 동일, tier 만 무작위) 후 재학습 — 동일 성능 → tier 정보가 학습에 안 쓰임 → 부분 FALSIFIED
- T4: 세 항 모두 제거 (baseline LM) 와 셋 다 켠 버전의 출력 동일 → 통합 전체가 무효 → 전면 FALSIFIED

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, TRAINING-4)
- **sibling splits**: Hc_1236 (CLM pure-hexa pipeline), Hc_1237 (ALM LoRA convergence), Hc_1238 (dual-track AGI gate), Hc_1240 (phi_holo gap)
- **sister H**: H_001 (anima-core-architecture), H_162 (CLM downstream)
- **engineering**: train_clm.hexa (lens loss, tension_link, tier-labeled corpus loader)

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: 3-component integration (lens loss + tension link + tier corpus): ablate each. If training signal works with 2-of-3 → 3-way integration claim falsified
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
- **adjacent H**: H_001 (anima-core-architecture), H_011 (iit-geometry — Φ ceiling), H_162 (Φ-normalized-anima-iit4-lower-bound), H_163 (8-cells-127-mip atom)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

