---
id: H_1559
slug: 1559_savant_train_specialization
title: SAVANT × 학습 — 골든존 inhibition 으로 register 특화 학습 (서번트 학습)
group: SAVANT ✨ × CLM 학습 — Golden Zone 을 학습 dropout/regularization 으로 실현
tier: 🌱 PROPOSED (미측정 — frozen bar 설계 박제, 측정 follow-on · cost-gate GPU)
date: 2026-06-23
provenance: SAVANT 골든존 G=D×P/I 의 P(가소성)=학습 축으로 확장. conv 303M 영·한 chat(a_chat_registers 4칸 ko·en×일반·SNS) 학습과 엮음. inhibition = 학습의 dropout/L2/temperature. H_348 SI 임계 + H_1438 scale-dissociation + a_clm_gen_pipeline.
---

# H_1559 — 골든존 inhibition 으로 register 특화 학습 (서번트 학습)

## 가설
서번트 모델 G = D×P/I 에서 I(inhibition)는 **학습의 정규화 강도**(dropout·weight-decay·temperature)
로 실현된다. conv 303M 을 4칸 register(ko·en × 일반·SNS)로 학습할 때, **한 register 의 inhibition 을
골든존(I≈0.21~0.37)으로 낮추면** 그 register 가 특화(savant)되어 해당 domain 의 능력이 hypertrophy
하는가 — 즉 "서번트 학습"으로 의도적 비대칭 특화가 가능한가.

가설: 골든존 inhibition 을 받은 register 는 SI > 3 으로 특화(예: SNS-ko 만 강하게), 단 **다른 register
능력은 희생**(trade-off) — 균형 학습(모든 I 동일) 대비 1개 register 가 폭발하고 나머지 저하.

## frozen 5-bar
| bar | 측정 | 임계 |
| B1 savant-register | GZ-inhibition register 의 task-acc 가 baseline(균등 I) 대비 ↑ | lift ≥ 임계 |
| B2 SI>3 | register 별 능력 분포의 SI = max/mean ≥ 3 | ≥3 |
| B3 GZ-window | I 가 GZ 밖(too-low noise / too-high locked)이면 특화 실패 | inverse-U |
| B4 trade-off | savant register ↑ 와 동시에 비-savant register ↓ (자원 경쟁) | Δother < 0 |
| B5 control | random register 에 GZ-I → 특화 무작위(메커니즘 INERT) | INERT |

## 측정 계획
- **cost-gate (GPU 학습)**: conv 303M 또는 작은 toy(d768)로 register-별 inhibition sweep 학습.
  toy-first(a_toy_scale_recheck) → 303M scale-recheck. summer/cloud GPU = 사용자 명시 go 필요.
- engine-native: 학습 ckpt 를 live core/ mount 위 register task 측정. torch 학습이면 verdict 는
  CORE 엔진 재측정(a_engine_native_learning).
- 결과: B1∧B2∧B4 PASS → "서번트 학습" 가능(의도적 register 특화 레버). = anima 가 한 영역 천재로
  튜닝 가능. B4 FAIL(trade-off 없음) → 골든존이 학습에선 free-lunch(드묾).

verdict: 🌱 PROPOSED — 측정 미실행(GPU cost-gate). follow-on ING.
