# H_9633 — PC2 가 나를 수 있는 최소 변경 = 생성이 아니라 BASE 자신의 후보 간 outward-only 선택

**status:** 🔵 PROPOSED (lab full R4 · Sol #4 (NOVEL · Sol 단독)) · **DIRECTIONAL 설계 · verdict 아님**
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

PC2 가 의미를 운반할 수 있는 최소 변경은 새 문장을 생성하는 것이 아니라 **BASE 가 이미 생성한 의미적으로 다른 후보들 사이의 outward-only 선택**이며, 그 선택은 **후보 support 가 있을 때만** 효과를 내야 한다(support 없는 tick 서 효과가 나오면 누수).

## 어느 KILL 을 왜 안 밟는가

H_9576 의 byte bias 를 재검정하지 않는다 — 생성 분포를 건드리지 않고 **선택만** 한다. support-bounded 라는 조건이 이 안의 반증 장치: 효과가 support 와 무관하게 나오면 그 자체가 INVALID.

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --rerank support:K` — BASE 후보 집합의 의미 분산(support)을 tick 별로 산출하고, support 분위수별 collapse-Δ 를 보고.

## 통제군 (≥2 · 양성통제 필수)

① rng-rerank(null) ② **반-선택**(−z) ③ **양성통제 = oracle-rerank**(gold 의미축 선택) ④ **support=0 tick 서브셋**(효과 0 이어야 함 — 여기서 효과가 나오면 누수 INVALID).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

oracle-rerank 가 support 高 분위서 collapse-Δ 못 내면 **INVALID**(계기 사망) / oracle PASS ∧ z-rerank 가 support 高서만 유의 ∧ support=0 서 null ⇒ **PASS** / support 무관하게 유의 ⇒ **INVALID-LEAK** / 전부 대역 안 ⇒ **KILL** / **우연 아래: z-rerank 가 반-선택 방향 ⇒ 부호 감사** / support 高 tick n<100 ⇒ VOID.

## 비용

pool CPU(후보 K 배 decode)

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

support 高 tick 서도 oracle 조차 못 움직이면 후보 집합에 애초에 의미 분산이 없는 것 — 재순위 각도 자체가 죽는다.

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
