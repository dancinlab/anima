# H_6182 — 🎯 G1 조합-커버리지 밀도 상전이

**tier:** 🟢 DIRECTIONAL-POSITIVE (toy attention) — G1 조합-커버리지 밀도 급상전이(held 2%→92% at ~20% coverage), 세션 첫 held-out 리프트; ConvMoE-arch control 진행중
**verdict:** 🟢 DIRECTIONAL-POSITIVE (toy attention-transformer, torch $0 aiden). 세션 첫 held-out 재조합 리프트. fable(G1 발산, opus 폴백)이 지목한 8-mech 미탐축=조합 커버리지 밀도(데이터 분포, DPI-면제=gradient가 보는 데이터가 바뀜). 20 color×20 shape=400 pair, cue→'COLOR SHAPE', held-out 40 영구미노출, plain CE(연산자 無). 커버리지 {5,10,20,40,80}% → held-out {1,7,37,40,40}/40 급상전이(2%→18%→92%→100%), 임계~20%. shuffle d80=0/40(진짜 binding, 암기 아님)·oracle factored=40/40(task 유효) 게이트 통과. fable 사전등록 상전이 예측 적중. 함의: G1은 trunk-objective TERMINAL이 아니라 데이터-커버리지-밀도-bound — 임계 아래 lookup 암기(연산자 무의미), 위 factoring 상전이. 8-mech(전부 데이터-고정)가 놓친 축. ⚠️CONFOUND(미해소): toy=attention transformer, production G1벽=ConvMoE-L1(RF≈13B, fable G6). '밀도 덕' vs 'attention arch 덕' 미구분 → ConvMoE-L1 동일스윕 CONTROL 실행중(floor면 attention 원인=fable G6 RF와 합류, 상전이면 밀도 arch-무관 lever). caveat: toy DIRECTIONAL, production corpus 임계위치 별도측정 필요(a_toy_scale_recheck). state/g1_density_phase_transition/.

## 결과
커버리지 5→80%에 held-out 1→40/40 급상전이(임계~20%), shuffle=0. G1=데이터-커버리지-bound(trunk-objective terminal 아님). ⚠️confound: attention vs ConvMoE arch → conv control 진행중.

## 관련
[[goal-g1-lever-discovery]] · H_6181 · H_6180 · [[fable-when-stuck-breakthrough]] · [[workflow-model-fable-override-ignored]]
