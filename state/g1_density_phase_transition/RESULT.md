# G1 조합-커버리지 밀도 상전이 — RESULT (2026-07-02, fable 발산 발) — 🎯 세션 첫 held-out 리프트(양성)

**TIER: 🟢 DIRECTIONAL-POSITIVE (toy attention-transformer, $0 aiden).** G1이 trunk-objective terminal이 아니라
**조합 커버리지 밀도-bound**임을 실측. fable(G1 발산, opus 폴백)이 지목한 8-mech 미탐축(데이터 분포, DPI-면제).

## 셋업 (density_sweep.py)
20 color × 20 shape = 400 pair, cue→"COLOR SHAPE" emit. held-out 40 pair 영구미노출. 3-layer attention
transformer(d128). 밀도 스윕 = POOL(360)의 {5,10,20,40,80}%로 plain CE 학습(연산자 無=밀도축 격리).

## 결과 — 급상전이
| coverage | ntrain | seen | held-out(40) |
|---|---|---|---|
| oracle(factored 입력) | — | — | 40/40 (task 유효) |
| 5% | 18 | 18/18 | 1/40 (2%) |
| 10% | 36 | 36/36 | 7/40 (18%) |
| 20% | 72 | 40/40 | **37/40 (92%)** ← 상전이 |
| 40% | 144 | 40/40 | 40/40 (100%) |
| 80% | 288 | 40/40 | 40/40 (100%) |
| shuffle d80 | — | — | 0/40 (진짜 binding 확증, 암기 아님) |

## 판독
held-out 재조합이 커버리지 밀도로 2%→18%→92%→100% **급상전이**. 임계(~20%) 아래=lookup 암기(어떤
연산자도 무의미), 위=trunk가 factoring으로 상전이. shuffle=0(암기 아님)·oracle=40/40(task 학습가능) 게이트 통과.
= fable 사전등록 예측 적중. 8-mech(전부 데이터-고정)가 놓친 진짜 축.

## ⚠️ 결정적 confound (미해소 → CONTROL 진행중)
이 toy는 **attention transformer**다. production G1 벽은 ConvMoE-L1(RF≈13B, fable G6 분석). 상전이가
"밀도 덕"인지 "attention arch 덕"인지 미구분 → density_conv.py(ConvMoE-L1 동일 스윕) 실행중:
- ConvMoE도 상전이 → 밀도가 arch-무관 진짜 lever, production 처방=조합-커버리지 코퍼스
- ConvMoE floor → attention arch가 원인(fable G6 RF 발견과 합류: 벽=RF/arch, 밀도는 attention 전제)

## caveat (정직, a_toy_scale_recheck)
toy DIRECTIONAL($0). production 303M .clm은 코퍼스 커버리지 고정 — 이 결과는 "밀도가 lever다"이지 production
corpus가 임계 위/아래인지는 별도 측정 필요. transfer 미검증.

## CONTROL 결과 (density_conv.py) — confound 해소: 밀도=arch-무관 확정
ConvMoE-L1(single conv, RF-limited, attention 無, production 벽 arch)도 상전이 재현:
| coverage | attention held | ConvMoE-L1 held |
|---|---|---|
| 5% | 1/40 (2%) | 1/40 (2%) |
| 10% | 7/40 (18%) | 3/40 (8%) |
| 20% | 37/40 (92%) | 19/40 (48%) |
| 40% | 40/40 (100%) | 36/40 (90%) |
| 80% | 40/40 (100%) | 40/40 (100%) |
→ **밀도는 arch-무관 G1 lever**. attention은 상전이를 더 날카롭게(92% vs 48% at 20%) 하나 존재는 arch-무관.
confound 해소 = 밀도가 진짜. production 처방=조합-커버리지 코퍼스. G1은 trunk-objective TERMINAL 아님 확정.
