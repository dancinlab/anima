# H_9629 — ΔD 는 애초에 읽을 수 있는 양인가 — 참값-0 캐스케이드 대좌

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-2 ∥ Sol #1 semantic-gauge-calibration (수렴)) · **DIRECTIONAL 설계 · verdict 아님**
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

per-tick ΔD 의 분산은 방향 신호가 아니라 **디코드 캐스케이드 노이즈**(byte 하나 바뀌면 하류 re-roll + anchor-copy 히트 패턴 변동)가 지배하며, 의미-공허 단일-byte 치환의 ΔD 분산이 bias arm 과 구별 불가하면 n=270 에서 방향은 **원리적으로 미측정**이다.

## 어느 KILL 을 왜 안 밟는가

H_9576 은 ρ 값을 죽였지 **ΔD 의 SNR 을 잰 적이 없다**. [[phi-estimator-needs-zero-truth-pedestal]] 의 mouth 판 — 참효과 0 인 대좌 arm 없이 음성을 읽었다([[positive-control-before-reading-a-negative]]).

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --cascade-null` — steered decode 대신 결정론 선택 lm-step 1곳에서 2nd-best byte 강제 치환(의미 용량 0), 나머지 무편향 → ΔD_cascade 분포 산출.

## 통제군 (≥2 · 양성통제 필수)

① off(무섭동 · ΔD=0 확인) ② cascade arm(참값-0 대좌) ③ **양성통제 = ζ=±4 포화 arm**(ΔD 가 대좌 위로 반드시 솟아야 함).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

var(ΔD_bias)/var(ΔD_cascade) ≤ 1.5 ⇒ **VOID-BY-SNR**(H_9576 방향 KILL 을 'per-tick 입도서 미측정'으로 재분류 · 블록-집계 필수) / ratio > 3 ∧ 양성 PASS ⇒ readout 유효 · KILL 유지 / 양성이 대좌 못 이김 ⇒ INVALID / **우연 아래: cascade arm 이 off 와 구별 불가(치환 미작동) ⇒ 계기 배선 결함 INVALID**. 검정력: 분산비 F-검정 n=270/270 → ratio 1.5 는 α=.05 서 검출 가능.

## 비용

$0급 pool CPU

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

cascade 대좌가 bias 분산의 ≤⅓ 이면 노이즈 바닥은 낮고 신호가 진짜 없는 것 — 이 안이 죽고 KILL 강화.

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
