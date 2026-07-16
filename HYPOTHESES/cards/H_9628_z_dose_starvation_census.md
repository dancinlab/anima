# H_9628 — 라이브 z 는 애초에 유효 용량인가 — dose-starvation census ($0 선행 관문)

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-7 (NOVEL · Fable 단독)) · **DIRECTIONAL 설계 · verdict 아님**
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

라이브 z 의 분포 폭이 같은 decode 의 posterior logit-gap 을 뒤집는 flip-dose ζ½ 에 크게 못 미치면(|z|₉₅ < ζ½/4), H_9576 의 방향 null 은 **용량-기아 VOID** 이지 벽이 아니다.

## 어느 KILL 을 왜 안 밟는가

H_9576 은 gain=1 고정으로 쐈다 — 'log-prob natural unit' 은 **측정이 아니라 가정**이었다. 용량 캘리브레이션 축은 한 번도 측정된 적 없다(H_9610 λ dose-response 가 WM-leak lane 서 선례).

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --z-census` — ① 라이브 z 분포(var·IQR·tick 별 lm-step 수=유효 노출) ② 같은 트레이스의 lm-step posterior gap census ③ 합성 ζ 스윕으로 argmax-flip 50% 지점 ζ½ 산출. 전부 기존 decode 의 부산물 — 새 fire 없음.

## 통제군 (≥2 · 양성통제 필수)

① gap census = 모델 자신의 posterior(raw 값 아님·z 대비 비율) ② rng arm flip 률(대좌) ③ **양성통제 = ζ=ζ½ 주입 시 flip 률 ≈50% 재현**(캘리브레이션 자기일관성).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

|z|₉₅ ≥ ζ½ ⇒ **PASS-DOSED**(용량 충분 — H_9576 KILL 은 용량 탓 아님) / |z|₉₅ < ζ½/4 ⇒ **VOID-STARVED**(H_9576 재분류 + gain 스윕 g∈{2,4,8} 정당화 · 단 gain 은 FORM tunable 이라 방향 판정은 여전히 z-상관으로만) / 중간 ⇒ PENDING / **lm-step=0 tick 비율 >30% ⇒ INVALID-EXPOSURE**(anchor-copy 가 채널을 굶김 — 용량 이전에 노출 문제) / 캘리브레이션 자기일관 FAIL ⇒ INVALID.

## 비용

$0급 pool CPU — **R4 전체의 첫 발사 관문**

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

라이브 z 가 이미 ζ½ 급이면 용량-기아 가설 즉사 · H_9576 은 정직한 KILL 로 유지.

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
