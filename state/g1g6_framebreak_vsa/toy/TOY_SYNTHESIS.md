# TOY-RESONATOR-READHEAD — 종합 (H_9211 토이 검증 · aiden pool $0)

**판정: 🟠 DIRECTIONAL / MIXED** — operator escape는 실재하나 사전등록 clean GREEN은 미달.
2026-07-08 · aiden RTX5070 · torch 2.10 · 3 seed · Fable5 설계 스펙 구현.

## 질문
G1 재조합벽이 전 축 terminal(#3046/3107/3108/3109) 후, Fable framebreak 재프레임: DPI가 지목하는 건 "bind가 CE-gradient서 학습됨". 정보가 존재하는 task에서, **고정 resonator read-path**가 CE-readhead가 붕괴하는 held-out 재조합을 일반화하는가?

## 설정 (Fable 스펙)
role-filler 회상, R=6·F=30, held-out cell = `r==f mod6`(30셀, 나머지 150 train). episode k=3 pair+query role→target filler. 4 arm 동일 codebook(U,V·매step unit-L2 renorm): A=CE-readhead(MLP bind+read, end-to-end) · B=고정 HRR(circconv bind+Wiener unbind+cosine cleanup, U/V만 학습) · B0=frozen(학습0) · C=additive((u+v)/√2, 고정 read-path).

## 결과 (indist 통제 정정 후 · clean)
| seed | A held | B held | C held | B bind-destroy | A/B indist | train A/B/C |
|---|---|---|---|---|---|---|
| 0 | 0.499 | 0.953 | 0.085 | 0.347 | 1.00/1.00 | 1.0/1.0/0.49 |
| 1 | 0.091 | 0.961 | 0.094 | 0.355 | 1.00/1.00 | 1.0/1.0/0.46 |
| 2 | 0.016 | 0.933 | 0.088 | 0.328 | 1.00/1.00 | 1.0/1.0/0.42 |
chance=0.033 · in-scene chance=0.33

## 정직한 해석
- ✅ **B vs C (연산자 격리 = Fable가 "진짜 판정 담는 비교") CLEAN·ROBUST**: 고정 HRR(B) 0.93~0.96 ≫ additive(C) 0.085~0.094, 전 seed. 나머지 전부 동일·연산자(⊛ vs +)만 차이 → held-out 재조합 우위는 **연산자에 귀속**. bind-destroy(B의 ⊛→+ 교체)=0.33 붕괴가 within-B로 재확인(margin=Δ under controlled break, 측정 메타법칙).
- ⚠️ **clean GREEN 미달(→MIXED)**: 사전등록 GREEN은 "A≤0.40 all seeds" 요구인데 seed0 A=0.499로 초과. A(CE-readhead)는 seed-요동(0.50/0.09/0.02) — CUDA 학습 비결정성 하에 때때로 부분 일반화(in-scene chance 0.33 근처). no-tune-to-green으로 바 못 옮김 → MIXED.
- ⚠️ **B≈B0**(frozen 0.949~0.971 = trained B): 승리 대부분이 HRR **대수 자체**(Plate 1995 기지). 정직한 주장 = "CE-gradient가 고정-bind read-path를 **오염하지 않는다**"(B train 1.0·held-out 0.95 = B0와 동급), **"B가 bind를 학습"은 아님**. anima 제안(연산자 고정+atoms를 gradient로)에 필요한 최소 명제는 성립.
- **C는 train조차 0.42~0.49**: additive 연산자는 binding task를 **애초에 못 맞춤**(floor 확증) — held-out 저조는 일반화 실패가 아니라 표현 불능.

## scope (a_toy_scale_recheck · a_scale_honest_scope)
symbolic ID 입력·byte surface 無·LM objective 無·`core/` decode 無 = **DIRECTIONAL, cement 불가**. 다음(engine-native 승격): atoms를 byte에서 학습(공유 encoder)+LM objective+`anima evaluate --py` terminal. KILL 조건 유지: CE-readhead 재도입 시 additive 재붕괴 or 정보벽#3109 지배.
