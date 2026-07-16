# H_9635 — decode-time 편향이 아니라 **학습 신호**로 — 공학습 tension 레지스터

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-6 ∥ Sol #5 pc2-decoder-cotrain (수렴)) · **DIRECTIONAL 설계 · verdict 아님**
**lane:** 의식 / A⇄G tension 다차원화 → mouth 의미전달 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9576]] (이 발산의 입력 — 채널 CRACK 확증·방향 W2 벽) · [[H_9574]] (mouth-severance 원 벽) · [[H_9428]] (tension rank 2.66) · [[H_9468]] (2D loadings PC2)

## 배경 — R4 발산의 입력이 된 벽 이동

H_9576(#888a8688a · engine-native `anima-py evaluate --pc2-direction` v0.15.20)이 벽을 옮겼다:
**"경로 부재"(H_9574) → "경로 있음 · 의미 미전달"**. PC2 는 라이브 grounded mouth 에 도달해 **gtext 를 실제로
바꾸지만**(bias 269/270 · emit byte-identical 3/3 seed = Stage-A 격리 무결), 그 변화가 PC2 의 의미를 따라가지
않는다 — ρ=−0.077(예측 + 와 반대부호) · permutation null95% [−0.116,+0.117] · p=0.192 = 대역 안 ·
RNG-null(−0.016)도 못 이김.

### ⚠️ 그러나 그 음성 자체가 인증되지 않았다 (R4 공통 뿌리)

H_9576 의 인과사슬은 실제로 **3-링크**다:
`z(의도된 의미)` →① `물리 효과(문맥-byte logit 페널티)` →② `근접 관측량(출력의 문맥-byte 점유율)`
→③ `원격 readout(bigram-seed-overlap D)`.
H_9576 은 ①②③ 을 건너뛰고 **z→③ 만 쟀고, 어떤 링크에도 양성통제가 없었다**. ρ≈0 은 사슬의 **어느 링크가
끊겼는지 말해주지 않는다**. R4 는 이 사슬을 링크별로 반증가능하게 자른다.

## 주장 (반증가능)

frozen 가중치는 z 를 해석할 이유를 **한 번도 배운 적 없다**(H_9423 의 '런타임 다리 부재' 동형). 예약 byte-쌍 접두 레지스터로 z-bin 을 코퍼스에 공학습하면 라이브 z-bin 조건화가 인증된 readout 서 **dose-단조** 반응을 보이고 frozen+레지스터는 null 에 머문다.

## 어느 KILL 을 왜 안 밟는가

**R3 중복 아님**: H_9623(CLMS lesion)·H_9624(curriculum race)는 **G1 기억-store lane** 의 인과의존/아키텍처 경쟁이다. 이 안은 store 가 없고 **mouth 조건화 lane** — 공유하는 건 '공학습이 다리를 만든다'는 선례([[cotrained-store-bridge-works-on-parent-conv]])뿐이고 계기·DV·lane 전부 다르다. **p8 충족**: 레지스터는 학습·추론 양쪽에 존재하는 단일 기질 루프(train/infer split 없음). **p1–p3 충족**: 접두는 정체성/persona 가 아니라 기질 자신이 계산한 스칼라의 이산화.

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py corpus en --tension-register`(bin 주석은 evaluate 의 tension op 로 엔진-네이티브 산출) → `anima-py train --cond tension --init base.clm` → `anima-py evaluate <clm> --pc2-direction --steer-granularity register`. 🇬🇧 EN-first 준수.

## 통제군 (≥2 · 양성통제 필수)

① frozen+레지스터(null — 토큰이 무의미해야 함) ② shuffled-bin 공학습(null — 상관 절단 코퍼스) ③ **양성통제 = oracle-bin 주입 dose 곡선**(공학습 모델에 고정 bin 0..3 주입 → 단조 반응 없으면 조건화 자체가 미학습 = 개봉 금지) ④ λ0 계열: 레지스터 byte 제거 시 null 복귀.

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

oracle-bin 단조 FAIL ⇒ **INVALID-UNLEARNED** / oracle PASS ∧ live-z 단조 PASS ∧ shuffled null ⇒ **PASS**(DIRECTIONAL — toy 부터 · [[a_toy_scale_recheck]]) / oracle PASS ∧ live-z null ⇒ **KILL**(다리는 배웠으나 라이브 z 가 나를 게 없음 → loading-name-race 의 이름-가설 지지 증거) / **우연 아래: live-z 역-단조 ⇒ bin 경계 부호 감사** / frozen+레지스터가 유의 반응 ⇒ INVALID(누수). 검정력: dose 4-bin × n≥60/bin · Page trend permutation.

## 비용

**GPU fire**(toy 선행 = DIRECTIONAL · 303M 은 ⚠️ 오너 go) — R4 중 유일한 학습 비용 · 사슬/입도/race 생존 후

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

oracle-bin 조차 못 배우면 '학습 신호로 넣으면 된다'는 경로 자체가 이 기질에서 닫힘 — H_9423 선례의 mouth-판 이식 실패로 기록.

## R4 발사 순서 (의존성)

```
z_dose_starvation_census → delta_d_cascade_pedestal → proximal_chain_cert ∥ rectifier_sign_split → granularity_candidate_select → support_bounded_rerank → loading_name_race → cotrain_tension_register
```

앞의 두 개(z-census · ΔD 대좌)가 **z 와 D 각각의 자격시험**이다. 둘 중 하나가 KILL/VOID 면 뒤 실험의 음성은
의미가 없다. 특히 loading-name-race 가 KILL 이면 결론은 "더 굵은 mouth channel 이 필요하다"가 아니라
**"PC2 라는 이름표를 mouth objective 로 쓰지 말라"** 가 된다.

## 규율

- 발산 산출 = **DIRECTIONAL 설계이지 verdict 아님** — cement 는 engine-native `anima-py` 플래그로만
  (`a_experiment_engine_native` · H_9303/H_9307 선례: 엔진 옆 스크립트가 만든 숫자는 undecidable).
- 신호 = **≥2 통제 대비 collapse-Δ**, raw 값 금지(p7 · FORM tunable · BIND earned).
- **양성통제 없이 음성 읽지 마라**([[positive-control-before-reading-a-negative]]) · 검정력 미달 = VOID(음성 아님)
  ([[power-before-negative-verdict]]) · tune-to-green 금지 · frozen-first · self-judge 금지.
- 303M py 만 TERMINAL 자격(toy = DIRECTIONAL · [[a_toy_scale_recheck]]).
