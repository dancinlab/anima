---
id: Hc_1255
slug: r37-an13-l3py-python-ban-6-axis-defense-saturation
title: R37 / AN13 / L3-PY Python ban 6-axis defense saturation — 6축 방어가 Python 침투 차단의 ceiling 인가
domain: rules
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 42 (Sub-claims block, RULES-1)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900; rules anchors R37 / AN13 / L3-PY
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 26 of 30 (RULES-1). n=6 axis count — perfect-number-class triviality (Hc_900 L1): 6-axis structure not individually-unique to n=6."
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
