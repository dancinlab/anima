# H_9631 — 채널은 방향이 아니라 크기만 나른다 — 정류기(rectifier) 가설

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-3 (NOVEL · Fable 단독)) · **DIRECTIONAL 설계 · verdict 아님**
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

문맥-byte logit 은 이미 posterior 를 지배하므로 z<0(문맥 쪽 끌기)은 **포화로 효과가 유계**이고 z>0(문맥에서 밀기)만 열려 있다 — 채널은 부호를 **정류**하며, ρ 를 z 부호별로 쪼개면 z>0 반쪽에서만 커플링이 나타난다.

## 어느 KILL 을 왜 안 밟는가

H_9576 의 ρ 는 **양쪽 부호 풀링 값** — 정류기라면 풀링 ρ≈0 은 **필연**이고, 죽은 건 '선형 방향성'이지 '반파 방향성'이 아니다. [[polarity-split-before-headline]] 의 연속판(그 교훈은 이진 라벨이었고 이건 연속 z).

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --split-sign` — 부호별 ρ + ρ(|z|,|ΔD|) + 각각의 permutation null 보고.

## 통제군 (≥2 · 양성통제 필수)

① rng arm 부호별 split(null — 정류가 draw-stream 인공물 아님 증명) ② off ③ **양성통제 = ζ∈{+1,+4} vs {−1,−4} 고정용량 비대칭 측정**(포화 가설 직접 확인 — −4 가 +4 보다 |ΔP| 작으면 정류 물리 확증).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

z>0 반쪽 ρ > +0.17(n≈135 해상한계) ∧ z<0 반쪽 대역 안 ⇒ **PASS-RECTIFIER**(후속 = 대칭화 재설계: 페널티 대신 문맥/비문맥 재정규화) / 양쪽 다 대역 안 ∧ 사슬-인증 양성 PASS ⇒ KILL 유지 / **우연 아래: z>0 반쪽 ρ<−0.17 ⇒ 부호 배선 역전 INVALID** / n<135/half ⇒ VOID. 검정력: 반쪽 n=135 → |ρ|≳0.17 · 참효과가 그보다 작으면 미해상 명시.

## 비용

pool CPU · 기존 프로토콜 재채점 재발사

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

고정용량 ±4 가 대칭 |ΔP| 를 보이면 포화 물리가 없다는 뜻 — 정류기 가설 즉사.

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
