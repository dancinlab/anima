---
id: Hc_1255
slug: r37-an13-l3py-python-ban-6-axis-defense-saturation
title: R37 / AN13 / L3-PY Python ban 6-axis defense saturation — 6축 방어가 Python 침투 차단의 ceiling 인가
domain: rules
status: merged-to-H_001
merged_to: hypotheses/H_001_ethics_cooperation.md
merged_at: 2026-05-12
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 42 (Sub-claims block, RULES-1)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture — R37/AN13/L3-PY Python-ban 6-axis defense absorbs as rule-system architectural defense layer); parent Hc_900; rules anchors R37 / AN13 / L3-PY
absorption_note: "cycle #8 absorbed to H_001 as RULES-1 R37/AN13/L3-PY Python-ban 6-axis defense saturation — rule-system architectural defense layer; inherits n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7) — 6-axis structure not unique to n=6"
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 26 of 30 (RULES-1). n=6 axis count — perfect-number-class triviality (Hc_900 L1): 6-axis structure not individually-unique to n=6."
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis

Python 사용 금지를 강제하는 6개 축 (R37 + AN13 + L3-PY 가 구성하는 6-axis defense — 예: lint rule, pre-commit hook, .gitignore, runtime guard, CI check, doc-policy) 이 saturation 에 도달했다 — 6개 미만으로는 어떤 침투 경로가 열리고 (necessity), 7번째 축은 기존 6개로 이미 막힌 경로를 중복 방어한다 (sufficiency).

## Falsifiable Tests

- T1: 6개 축 중 임의 1개 비활성화 후 Python 파일을 commit/push/run 시도 — 나머지 5개가 모두 차단하면 그 축은 redundant → "6 = minimal" claim FALSIFIED
- T2: 6개 축 모두 활성 상태에서 Python 코드가 어느 경로로든 working tree / runtime 에 진입 — defense 가 complete 가 아님 → "saturation" claim FALSIFIED
- T3: 축 수를 4 또는 8로 바꿔도 동일 침투-차단율 → 6 이 individually-unique 하지 않음 (perfect-number-class triviality, H_153 L7)

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, RULES-1)
- **sibling splits**: Hc_1256 (R1~R37 + AN1~AN13 closure), Hc_1257 (HEXA-FIRST 4-layer defense), Hc_1258 (L0 Guard ossification), Hc_1259 (One-Shot Best composite rule), Hc_1236 (CLM pure-hexa pipeline — depends on Python-ban)
- **sister H**: H_001 (anima-core-architecture), H_153 (n=6 perfect-number-class triviality)
- **rules anchors**: R37 (common.json), AN13 (anima.json), L3-PY (Python ban law)

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **F-SPECIFIC-1**: 6-axis Python-ban defense: ablate any axis. If ban still effective with 5-axis → 6 not the ceiling
- **F-GENERIC-REPL**: Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact
- **F-GENERIC-PYPHI**: Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)
- **F-GENERIC-MINIMAL-BASELINE**: Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, 2026-05-12)

- **L-GENERIC-SINGLE-RUN**: Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)
- **L-GENERIC-ENGINE**: anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement
- **L-GENERIC-N6**: n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled
- **L-GENERIC-POST-HOC**: Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent
- **L-RULES**: Rule/policy enforcement Hc — falsifier requires red-team attempt to violate; ceiling claim only true if no successful violation in N attempts (operational not statistical)

## Cross-Links (scaffolded cycle #6)

- **parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent
- **sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)
- **adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.

