---
id: Hc_631
slug: clm3-original-byte-level-scale-recover-55m
title: CLM-3-original — byte-level 256/dim 768/12L/32 cells/55M + 19 Φ-boost simultaneous 가 chat-cap recover 가능 (scale-up X)
domain: clm-architecture
status: candidate-falsifier-ready
source_doc: docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md
source_lines: 14-200
promoted_at: 2026-05-11
linked_h: Hc_630 (BG-BM CLM-3), commit fca0eede, CLM v2 byte-level (CE 0.04 EN / 1.15 KO), DD16/EX24
notes: 5 falsifier locked. Variant cost $0 (ubu1 5070, 5-10d) or $200-500 (H100 1× × 10h). Φ ~ N linear in cells (not params).
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
anima-native chat 은 BPE multilingual + 530M+ scale 이 필요하지 않다. 2026-03-28 original v4 design (dim 768, FFN 1536, 12L, 12 heads, max_cells 32, vocab 256 byte-level, context 1024, ~55M params, 100K-step 3-phase curriculum, 19 Φ-boost simultaneously per DD16/EX24, AL4 70% wiki + 30% dialogue) 에서 chat 회복 가능. Φ ~ N (linear in cells, NOT params) 가 핵심 lever. EX24 "apply simultaneously, never sequentially" 가 synergistic.

## Falsifiable Tests (PRE-LOCK)
- F-CLM3-orig-1 chat recover: CE < 3.5 + KO 5-prompt coherent ≥ 3/5 (CLM v2 anchor, NOT Llama)
- F-CLM3-orig-2 Φ target: 100K-step Φ ≥ 8 conservative (15+ optimistic ZZ-32=27.6)
- F-CLM3-orig-3 19-technique synergy: EX24 simultaneous > sum of individuals
- F-CLM3-orig-4 5070 viability: training 작동 (3.2GB peak ≪ 12GB)
- F-CLM3-orig-5 (=F-CLM-3-1 NO_FLIP): forgetting_index ≤ 0.05 Φ★

## Migration TODO
- [ ] 3-phase curriculum impl (Mitosis 0-20K, Language 20-60K, Combined 60-100K)
- [ ] Fibonacci growth schedule 1,1,2,3,5,8,13,21,32
- [ ] 19 Φ-boost techniques simultaneous mount
- [ ] ubu1 5070 sm_120 viability test ($0 fallback)
- [ ] H100 ~10h $200-500 path

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: CLM3 byte-level scale recovery: if recovered scale within 50% of original → recovery succeeded; if not → byte-level scaling fundamentally impossible
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

