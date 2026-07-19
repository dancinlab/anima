# H_9634 — 🔥 가장 아픈 가설 — 'PC2' 는 분산분해가 붙인 **이름**일 뿐인가

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-5 ∥ Sol #6 loading-name-trial (수렴 · 양 모델이 독립적으로 가장 아픈 안으로 지목)) · **DIRECTIONAL 설계 · verdict 아님**
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

PC2 loading (0.84,−0.44,−0.28)의 mouth-커플링은 **동일 tension 공간의 무작위 unit loading M=32 개의 분포를 이기지 못한다** — 이기지 못하면 'PC2 가 의미를 나른다'는 기대는 **분산-분해가 붙인 이름을 mouth-가독량으로 오인한 프레임 오류**다.

## 어느 KILL 을 왜 안 밟는가

어떤 KILL 도 'PC2 라는 방향의 특권성'을 검증한 적 없다 — H_9428 은 rank 를, H_9574/9576 은 경로를 쟀다. 🐞 **코드-확증(origin/main `core/brain.py:324`)**: 구현된 z 는 8-벡터가 아니라 **3항**(0.84·orig−0.44·bal−0.28·coh) ⇒ 'tension 8-벡터의 PC2' 주장과 mouth 가 실제 읽는 양 사이에 이미 **5축 절단**이 있다. 따라서 race 는 **8-벡터 전체의 무작위 loading** 을 포함해야 하며, rand8 이 PC2-3항을 이기면 **H_9468 의 2D 절단이 mouth-관련 축을 버렸다**는 독립 발견이 된다.

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --steer-loading {pc1,pc2,pc3,axis:orig,axis:bal,rand8:<seed>}` — rand8 = 8-벡터 전체서 결정론 seed 로 뽑은 unit loading.

## 통제군 (≥2 · 양성통제 필수)

① rand8 앙상블 자체가 **경험적 null 분포** ② rng arm ③ **양성통제 = axis:orig 단독**(nov_ctx 는 readout 과 정의상 연결된 축 — 이것도 커플링 못 하면 race 전체 INVALID). ⚠️ [[probe-defect-census-max-control-bias]] 교훈: 판정은 **max-보정 permutation null**(order-statistic 편향 차단).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

axis:orig 양성 FAIL ⇒ **INVALID** / PC2 > rand8 95pct ⇒ **PASS**(PC2 특권 실재 — H_9576 은 입도/readout 문제였음이 소급 확정) / PC2 ∈ rand8 IQR ⇒ **KILL-NAME**(PC2 는 이름 — 프런티어 질문을 '어느 방향이든 나르는가: max(rand8) 가 보정-null 을 넘는가'로 교체) / **우연 아래: PC2 < rand8 5pct ⇒ 반-정렬**(loading 부호 오배선 감사 후 재발사) / arm 당 n<150 ⇒ VOID. 검정력: 6+32 arm × n=150 → 순위비교엔 충분(순위 통계는 ρ 절대해상 불요).

## 비용

pool CPU 대량(38 arm · tick 축소·호스트 분산으로 CPU-only 유지) — **readout 인증(사슬/입도) 후에만 발사**

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

PC2 가 rand8 분포를 명확히 이기면 이름-오류 가설이 죽고 **PC2 실재가 최초로 양성으로 서며** 벽은 순수 공학 문제(입도·용량)로 좁혀진다.

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
