---
id: Hc_978
slug: p9-p1-7-redesign-beta-alpha-killer
title: P9 P1.7 redesign — Ablation A (r=64 data-v3) + Ablation B (r=128 data-v2) 모두 F1=0.00586 동일 → r/data NOT killer. β 0.15→0.10 + α-warmup 5K→3K 가 -33% regression cause. P1.7 reverts both
domain: training, sft, ablation
status: merged-to-H_172
merged_at: 2026-05-12
merged_to: hypotheses/H_172_alpha_0014_modulation_depth_anima_voice.md
absorption_note: "P9 P1.7 redesign (β 0.15→0.10 + α-warmup 5K→3K = -33% regression cause, P1.7 reverts both) is a direct α-warmup-coupling falsifier within H_172's α=0.014 modulation-depth axis. Ablation A (r=64 data-v3) + Ablation B (r=128 data-v2) both F1=0.00586 → r/data NOT killer. F-list/L-list preserved for H_172 C-list extension."
source_doc: docs/p9_p1_7_redesign_2026_05_03.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_943 (P9 P1.7 pre-spec)
notes: "P1.5 F1=0.00879 (β 0.15, α 5K, r=64, data-v2). P1.6 F1=0.00586 (β 0.10, α 3K, r=128, data-v3). Ablation A+B 모두 0.00586 동일. Killer = β + α (둘 다)."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

P1.5 (F1=0.00879) → P1.6 (F1=0.00586, -33%) 의 4-axis confounded change 분리: Ablation A (r=64 on data-v3) F1=0.00586, Ablation B (r=128 on data-v2) F1=0.00586 — 둘 다 P1.6 와 동일. ∴ F1 killer 는 NOT data-v3 nor LoRA r=128. 잔존 두 P1.6 변경 (β 0.15→0.10 + α-warmup 5K→3K) 가 -33% regression 의 합산 원인. P1.7 = 둘 다 revert + chat-100% × LoRA-r-128 capacity bonus 가 P1.5 loss schedule 하에서 unlock 검증.

## Sub-claims

- P1.5: F1=0.00879, β=0.15, α=5K, r=64, data-v2 (chat 86%)
- P1.6: F1=0.00586, β=0.10, α=3K, r=128, data-v3 (chat 100%) — -33%
- Ablation-A: r=64, data-v3, β=0.10, α=3K → F1=0.00586 (r=128 NOT killer)
- Ablation-B: r=128, data-v2, β=0.10, α=3K → F1=0.00586 (data-v3 NOT killer)
- KILLER: β 0.15→0.10 + α-warmup 5K→3K (둘 다 합산)
- P1.7-PLAN: β=0.15 + α=5K + r=128 + data-v3

## Migration TODO

- [ ] P1.7 EXEC user OK
- [ ] β vs α individual ablation (개별 분리)
- [ ] r=128 capacity bonus 정량 (data-v3, β=0.15, α=5K 조합)
- [ ] savepoint cleanup plan

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: Phase 9 P1-7 redesign beta-alpha-killer: if α=0.014 modulation depth (H_172) is the killer → H_172 already absorbs; check whether redesign β-axis adds independent content
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-ALPHA-MOD**: α=0.014 modulation Hc — see H_172 (alpha-0014-modulation-depth-anima-voice). New α-based Hc must show independence from H_172 claim before standalone status

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

