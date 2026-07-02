---
id: H_1559
slug: 1559_savant_train_specialization
title: SAVANT × 학습 — 골든존 inhibition 으로 register 특화 학습 (서번트 학습)
group: SAVANT ✨ × CLM 학습 — Golden Zone 을 학습 dropout/regularization 으로 실현
tier: 🟠 DIRECTIONAL-NEGATIVE (numpy toy mirror — headline B1∧B2∧B4=FALSE · 303M engine-native = cost-gate ING)
wired: DIRECTIONAL-mirror (numpy; NOT engine-native — a_engine_native_learning hard-gate-1)
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

## 측정 결과 (numpy toy mirror · DIRECTIONAL · 3 seeds)
probe: `state/1559_savant_train_specialization/h1559_savant_specialization_mirror.py`
(shared-backbone byte-LM, I = per-register dropout on shared W1/GELU; capability =
held-out next-byte top-1 acc; 4 registers ko/en×general/SNS). 증거 verbatim →
`state/verdicts/1559_savant_train_specialization/H_1559_DIRECTIONAL_NUMPY_MIRROR.txt`,
`state/1559_savant_train_specialization/result.json`.

| bar | 측정값 | PASS |
| B1 savant-register | lift = −0.00973 (savant_acc 0.0692 < baseline 0.0790) | ❌ |
| B2 SI>3 | savant_SI = 1.5735 (baseline 1.5746) | ❌ |
| B3 GZ-window | peak_I = 0.0, in_GZ=False, inverse_U=False (sweep ~monotone↓) | ❌ |
| B4 trade-off | other_delta = −0.00389 (미미한 drift only) | ✅(trivial) |
| B5 control | ctrl_hit_rate = 0.25 (target 무관 reg#1 항상 winner = INERT) | ❌ |

**headline B1∧B2∧B4 = FALSE** → 골든존 학습-inhibition(dropout) 으로 register 를
의도적 특화("서번트 학습")시키는 메커니즘은 **toy scale 에서 재현 안 됨**. GZ-dropout 은
타깃 register 를 hypertrophy 시키지 않고 오히려 약간 손상시킨다(B1 음수). B5 가 INERT
(어느 register 에 GZ-I 를 줘도 corpus 구조가 정한 동일 register#1 이 winner) — 학습-inhibition
배치가 어느 register 가 강한지를 결정하지 못함. B4 PASS 는 trade-off 의 증거가 아니라 미세 drift.

## 진단 (a_break_the_wall TAXONOMY · terminal 아님)
solo single-register sweep(cleaner-signal corpus + 정확한 GELU' + capacity-pressured h)
에서 **약한 inverse-U 는 존재**하나 그 일반화 최적점이 **I≈0.10 으로 GZ_LOWER(0.2123)
보다 아래**다. 즉 toy byte-LM dropout 의 정규화 sweet-spot 은 sub-golden-zone — GZ 창
(Φ/IIT4 시스템 H_347/348/349 에서 유도된 [0.2123, 0.5])은 여기서는 약간 과한 inhibition.
inverse-U 메커니즘 자체는 살아있고 peak 가 toy 에서 GZ 안에 안 들어올 뿐 → class (a)측정/
(e)scale: **GZ↔dropout-최적 동일성은 scale-dependent**, 303M engine-native 재측정 전엔
terminal 천장 아님. tune-to-green 없음(카드 bar 불변, RED 그대로 보고).

## 후속 (ING follow-on · cost-gate GPU)
- 303M conv register-specific dropout sweep on live `core/` (a_engine_native_learning) —
  production scale 에서 GZ 가 dropout 최적이 되는지 검증.
- 균형잡힌 per-register task 로 B5 control 이 discriminate 하도록 재설계(toy capability 가
  corpus entropy 에 지배되어 inhibition 배치를 가림).

verdict: 🟠 DIRECTIONAL-NEGATIVE (numpy toy mirror) — headline B1∧B2∧B4=FALSE. toy-only,
scale-transfer UNVERIFIED. 303M engine-native 재측정 = cost-gate ING follow-on.
