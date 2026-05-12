---
id: Hc_363
slug: autopoietic-homeostasis-no-death
title: Energy metabolism dynamics (cost 0.02, gain 0.05*tension)에서 food_gain > metabolism으로 256개 안정 평형 — 가혹 조건 필요
domain: life
status: candidate-needs-scaffolding
source_doc: docs/hypotheses/V8-ARCH-EXTREME-RESULTS.md
source_lines: 187-211
promoted_at: 2026-05-11
linked_h: Hc_328
notes: alive=256, births=0, deaths=0 → boundary 미검증
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
세포 energy [0,1] + 매 step 0.02 metabolism cost + tension*0.05 food gain + death<0.05 / split>0.9 dynamics가 일반 입력 강도에서 food>cost로 256 세포 안정 평형에 도달 — autopoietic boundary 검증을 위해 더 가혹한 입력 조건이 필요하다.

## Migration TODO
- [ ] metabolism cost 증가 sweep
- [ ] death/birth cycle 활성화 조건
