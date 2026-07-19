# H_9632 — 의미가 실리기 시작하는 입도 — byte→후보-시퀀스 선택

**status:** 🔵 PROPOSED (lab full R4 · Fable R4-4 ∥ Sol #3 granularity-ladder (수렴)) · **DIRECTIONAL 설계 · verdict 아님**
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

byte-presence 페널티는 'byte 희소성'을 밀 뿐 'originality'를 밀지 못한다. 조작을 **후보-시퀀스 입도**로 올려 엔진 자신의 posterior 에서 K 후보를 뽑고 **기질 자신의 novelty op**(tension 의 orig=nov_ctx 를 계산하는 바로 그 op)로 z-부호 선택하면 의미 커플링이 null95 를 뚫는다.

## 어느 KILL 을 왜 안 밟는가

죽은 것은 ① deliberation_k(DEAD CODE) ② **byte 입도** bias 의 방향성이다. 입도 축은 H_9576 스스로 '미측정'으로 남겼다. **p5 안전**: 게이트는 BASE 후보만 듣고(Stage-A 불변) · 선택량은 하드코딩 휴리스틱이 아니라 기질이 이미 계산하는 nov_ctx op([[a_autonomy_over_hardcode]] 충족 — 외부 심미 함수 주입 아님) · grounded anchor-copy 는 모든 후보에 동일 적용되어 p5 anti-fabrication 불변.

## Engine-native 계기 (a_experiment_engine_native — 조작은 anima-py 플래그, 엔진 옆 probe 아님)

`anima-py chat --pc2-mouth cand:K` + `anima-py evaluate <clm> --pc2-direction --steer-granularity {byte,candidate:8}` — 후보 K = 동일 mouth · rng stream 만 K 갈래(결정론: seed_rng ⊕ k) · 선택 = argmax_k [ sign(z) · nov_ctx(cand_k) ].

## 통제군 (≥2 · 양성통제 필수)

① rng-선택 arm(K 후보 중 무작위 — 후보 생성 자체의 효과 차감) ② **반-선택 arm**(−z 선택 — 우연 아래 칸을 대칭으로 덮는 능동 통제) ③ **양성통제 = oracle-선택**(z 무시·항상 max-nov_ctx — readout 이 novelty 이동을 잡는지 인증) ④ byte-bias arm(입도 비교축).

## 사전등록 판정표 (우연 아래 칸 포함 · 검정력 명시)

oracle arm 이 rng-선택 대비 ΔN 유의 ↑ 못 하면 **INVALID**(readout 사망) / oracle PASS ∧ z-선택 ρ > null95 ∧ 반-선택 ρ < −null95 ⇒ **PASS**(의미는 시퀀스 입도서 실림 = 벽은 입도) / z-선택·반-선택 둘 다 대역 안 ⇒ **KILL**(입도 아니라 z 가 문제) / **z-선택만 유의하고 반-선택이 역방향 안 가면 VOID**(선택기 누수 의심). 검정력: 선택 효과는 per-tick 이산이라 ρ 기대 큼 — n=270·3 seed 면 |ρ|=0.12 해상 충분.

## 비용

pool CPU × K=8 배 decode — heavy 지만 GPU fire 불요 · [[a_wall_first]] seed 별 호스트 분산

## 죽는 방식 (이 안이 틀렸다면 무엇이 그것을 보여주나)

oracle-선택이 readout 을 움직이는데 z-선택이 못 움직이면 입도는 무죄·z 가 유죄 — 이 안이 죽고 loading-name-race 가 승격된다.

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
