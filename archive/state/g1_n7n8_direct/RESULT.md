# N7/N8 직접 probe — EXPLORATORY 스케치 (verdict 아님)

**날짜:** 2026-06-30 · **scope:** DIRECTIONAL-synthetic, NOT a card verdict (H_1832/H_1833 미박제)

## 무엇

오너 "직접 진행(서브에이전트 X)" 지시로 N7(H_1832 조각학습→mitosis 조합)·N8(H_1833 학습-中 kosmos 기하 관찰)을 cheap 합성 numpy로 스케치. `probe.py` (fp64, 32-dim 합성 개념, no clm303 load, $0).

## 결과 (raw: RESULT.txt)

- **N7**: single 0/24 · additive 0/24 · shuffle 0/24 · constructive 0/24 → 표면상 FLOOR.
- **N8**: 학습 진행하며 parent-specificity −0.04→+0.062 상승(>random −0.016) → 표면상 FORMS.

## ⚠️ 왜 verdict 아닌가 (정직 · verdict-integrity)

1. **N7 metric 결함:** 합성 32-dim 직교 개념에서 `composed_distinct≥2`(두 부모에 동시 근접, THRESH=0.30)는 **구조적으로 거의 불가능** — self-test 판별자(planted-bind 회복) 없이는 "FLOOR"가 진짜인지 metric-unsatisfiable artifact인지 구분 불가. agent의 `he_levers.py`는 self-test SEPARATES(12/12 vs 1/12)로 metric 살아있음을 증명했으나 이 스케치는 그게 없음.
2. **N8 결과 동어반복:** bilinear regressor가 타깃을 맞추면 parent-specificity가 *정의상* 생김 = 발견 아님(toy artifact).
3. **합성 fixture:** 실 학습된 표현(clm/ByteGPT) 아님 = transfer 미검증.

## 진짜 측정 (real)

- **N7 real** = 실제 조각 개별 gradient 학습 on clm303/ByteGPT penultimate embed + he_levers self-test 규율 + control(additive/single/shuffle). FLOOR면 그때 H_1832 🧱.
- **N8 real (H_1833)** = live trunk-objective A/B의 ON(infonce) vs OFF(ce) ckpt에서 kosmos/anchor 기하 비교 — "엮기 채점표가 anchor 기하를 다르게 형성하나". ARM-ON ckpt 착륙 대기.
