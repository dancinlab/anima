# H_9630 — 사슬 분해 + 계기 인증 — z→물리효과→근접량→원격 readout 어느 링크가 끊겼나

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-1 ∥ Sol #2 source-channel-readout-trident (수렴)) · **DIRECTIONAL 설계 · verdict 아님**
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

z→ΔD 널의 원인은 readout 사슬의 링크 단절이며, **근접량 P**(steered 출력 중 T-창 문맥-byte 점유율의 Δ)로 재면 z→P 커플링이 null95 를 뚫는다. 뚫지 못하면 채널이 물리적으로 죽은 것이다.

## 어느 KILL 을 왜 안 밟는가

H_9576 이 죽인 것은 'byte bias 의 **D(bigram-seed-overlap) 방향성**'이지 채널의 근접 효과가 아니다. 근접량 P = 조작이 **직접 미는 바로 그 양** — 측정된 적 없다. 🐞 코드-확증(origin/main): `core/decode.py:2041` 주석이 명시 — bias 는 **grounded anchor-copy step 을 절대 안 지난다**(lm-branch 전용) ⇒ 유효 용량 = z × (그 tick 의 lm-step 수)로 **tick 마다 다르다**.

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py evaluate <clm> --pc2-direction --readout {distal,proximal,chain}` — `proximal` = 출력 byte 중 창-집합 소속 비율 · `chain` = z→P 와 P→D 를 각각 permutation null 과 함께 보고. 기존 270-tick 프로토콜 그대로 결정론 재발사.

## 통제군 (≥2 · 양성통제 필수)

① rng arm(draw-stream null) ② off arm(null) ③ **양성통제 = 고정 포화용량 arm** `--pc2-dose fix:±4` (z 무시 · ζ=±4 nats 페널티는 문맥-byte 를 반드시 억제해야 하며 그래도 P 가 안 움직이면 P 계기 INSTRUMENT-DEAD).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

양성통제 ρ(ζ,ΔP) < +0.5 ⇒ **INVALID**(P 계기 사망 · 아래 칸 개봉 금지) / 양성 PASS ∧ ρ(z,ΔP) > +null95 ⇒ **PASS**(채널 살아있음 · 끊긴 건 P→D 링크 = readout 교체 정당화) / 양성 PASS ∧ ρ(z,ΔP) ∈ null95 ⇒ **KILL**(라이브 z 용량서 채널 물리적 침묵) / **우연 아래: ρ(z,ΔP) < −null95 ⇒ KILL-REVERSED**(부호 배선 감사) / n<270 or seed<3 ⇒ VOID. 검정력: n=270 → |ρ|≳0.12 해상(H_9576 동일).

## 비용

pool CPU(303M 결정론 decode · 기존 프로토콜 재탕) — GPU fire 불요

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

양성 PASS 인데 z→P 도 P→D 도 유의하면 사슬은 온전하고 H_9576 KILL 이 그대로 선다 — 링크-단절 전제가 죽는다.

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
