---
id: Hc_377
slug: trinity-v9-no-nan-no-gradient-sharing
title: v5의 NF1-NF9 EMA smoothing 패치가 필요한 이유는 phase transition gradient explosion이며 v9의 gradient 분리가 이를 근본 해결한다
domain: consciousness
status: candidate-unverified
source_doc: docs/hypotheses/TRINITY-TRAINING-DESIGN.md
source_lines: 662-687
promoted_at: 2026-05-11
linked_h: NF1-NF9
notes: v9 = no gradient sharing → no explosion
---

## Hypothesis
v5에서 phase transition마다 발생하는 NaN spike의 근본 원인은 CE-cell gradient 공유이며, v9의 .detach() 분리가 gradient sharing 자체를 제거하므로 NF1-NF9 패치 없이도 smooth transition을 보장한다.

## Migration TODO
- [ ] v5/v9 gradient norm trajectory 비교
- [ ] phase transition NaN 측정
