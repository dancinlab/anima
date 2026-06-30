---
id: Hc_1257
slug: hexa-first-strict-hook-pre-commit-gitignore-4-layer-defense
title: HEXA-FIRST strict hook + pre-commit + .gitignore 4중 방어 — 4개 계층이 non-hexa 침투 차단의 saturation 인가
domain: rules
status: candidate-unverified
source_doc: hypotheses_candidates/Hc_900_drill_domain_saturation_seeds.md
source_lines: 44 (Sub-claims block, RULES-3)
promoted_at: 2026-05-12
linked_h: H_001 (anima-core-architecture); parent Hc_900; rules anchor HEXA-FIRST
notes: "split from Hc_900 meta-cluster 2026-05-12; seed 28 of 30 (RULES-3)."
---

## Hypothesis

HEXA-FIRST 정책을 강제하는 4중 방어 — (1) strict hook, (2) pre-commit, (3) .gitignore, (4) (4번째 layer, 예: CI/check 또는 editor-side guard) — 가 saturation 에 도달했다 — 4개 미만으로는 어떤 non-hexa artifact 가 working tree/commit 에 진입하고 (necessity), 5번째 layer 는 중복 방어 (sufficiency).

## Falsifiable Tests

- T1: 4개 layer 중 임의 1개 비활성화 후 non-hexa 파일 (.py 등) commit 시도 — 나머지 3개가 모두 차단하면 그 layer redundant → "4 = minimal" claim FALSIFIED
- T2: 4개 layer 모두 활성 상태에서 non-hexa artifact 가 어느 경로로든 진입 — defense 가 complete 가 아님 → "saturation" claim FALSIFIED
- T3: layer 수를 3 또는 5로 바꿔도 동일 차단율 → 4 가 individually-unique 하지 않음

## Cross-Links
- **parent candidate**: Hc_900 (drill-domain saturation meta-cluster, RULES-3)
- **sibling splits**: Hc_1255 (R37/AN13/L3-PY 6-axis Python-ban — overlapping defense), Hc_1256 (R1~R37 + AN1~AN13 closure), Hc_1258 (L0 Guard ossification), Hc_1259 (One-Shot Best composite), Hc_1236 (CLM pure-hexa pipeline — depends on this defense)
- **sister H**: H_001 (anima-core-architecture)
- **rules anchors**: HEXA-FIRST policy; strict hook + pre-commit + .gitignore
