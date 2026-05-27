---
id: Hc_389
slug: gap4-post-process-restoration-70-30
title: process() 직후 cells를 0.7*saved + 0.3*after_process 비율로 부분 복원하면 Φ ~10 (7x)
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/PHI-GAP-816x-investigation.md
source_lines: 78-91, 170-176
promoted_at: 2026-05-11
linked_h: Hc_388
notes: 3줄 추가. 비율을 Phi 기반 동적 조절 가능
---

## Hypothesis
saved = [c.hidden.clone() for c in cells] + engine.process(x) + c.hidden = 0.7*saved + 0.3*c.hidden 의 post-process restoration 패턴이 GRU 언어 정보 30%만 수용 + Φ 구조 70% 보존하여 Φ ~10 (7x baseline) 달성한다.

## Migration TODO
- [ ] ratio sweep (50/50, 70/30, 90/10)
- [ ] dynamic ratio (Phi-based)
