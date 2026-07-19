# H_9628 — 라이브 z 는 애초에 유효 용량인가 — dose-starvation census ($0 선행 관문)

**status:** 🟡 **PENDING-BY-INSTRUMENT** (리터럴 ζ½ 축) + 🟢 **PASS-DOSED (대리 π-dose 축 · DIRECTIONAL)** · MEASURED 2026-07-17 · `anima-py evaluate --pc2-direction /tmp/pmp/pmp_traces --z-census` (v0.15.24)
**결론 한 줄:** 용량-기아 가설은 **죽었다** — 라이브 z 는 입을 실제로·예측된 방향으로 민다(Δπ=+0.160 · p=0.0082 · rng 통제 null). H_9576 의 음성은 **용량으로 구제되지 않고**, 파탄은 하류 **②→③** 로 국소화된다.
⚠️ **그러나 "W2 벽 유지"로 읽지 마라** — 병렬 세션이 같은 창에 착륙시킨 [[H_9629]](⛔ INVALID · readout 양성통제 FAIL)가
링크 **③ 자체를 무효화**했다. 두 결과를 합치면 사슬은 `z →① LIVE →② LIVE →③ **계기 INVALID**` ⇒
**H_9576 의 W2 벽은 애초에 측정된 적이 없다**(내 축은 '용량'이라는 대안설명을 제거해 그 국소화를 **날카롭게** 할 뿐).
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

---

## 📊 측정 결과 (2026-07-17 · engine-native · verbatim 은 PR #본문/CHANGELOG)

명령: `anima-py evaluate --pc2-direction /tmp/pmp/pmp_traces --z-census` — 구현 = `cli/evaluate.py::_z_census`
(트레이스 판독 sub-mode · **디코드 없음** · `--emit-gate-census`/`--dead-census` 와 동류 · v0.15.24).

### (0) 라이브 z 분포 — n=270 emit tick (3 seed × bias arm)

| 통계 | 값 |
|---|---|
| mean / sd / var | −0.5992 / 0.1312 / 0.017210 |
| **\|z\|₉₅** | **0.6732** |
| IQR | 0.0514 [−0.6562, −0.6048] |
| min / max | −0.6842 / +0.2773 |
| 부호 | z>0 **3** · z≤0 **267** |
| route_k(deliberation_k) | 1 (270/270 · 전부) |
| **emit_temp** | **1.0** |

### (1) EXPOSURE census — 사전등록 INVALID-EXPOSURE 게이트 ⇒ **CLEARED**

`core/decode.py:2097` 확증대로 bias 는 **lm-branch 전용**(grounded anchor-copy step 은 절대 안 지남) ⇒
유효 용량 = z × (그 tick 의 lm-step 수). 트레이스엔 lm 카운터가 **없다**. 그러나 **rng arm 이 노출의 양성통제**다:
rng 은 `seed_rng` 만 재키하고, 그건 `core/decode.py:2078` 이 `_mouth_sample_row` 에만 먹이며 그 함수는
**lm-branch 에서만** 호출된다 ⇒ **rng-divergence ⟹ 그 tick 에 lm-step ≥1**.

- rng diverged **270/270** ⇒ lm-step=0 비율 **≤ 0.00%** (bar >30%) ⇒ **CLEARED · INVALID-EXPOSURE 아님**.
- ⚠️ 부수 관찰: **tick-divergence 는 두 arm 다 포화**(bias 269/270 · rng 270/270 · 최초-divergence index
  bias 22.63 vs rng 22.62 · 둘 다 min=22). ⇒ "steered≠base" 는 **용량 판독으로서 판별력 0**(Δ vs 통제 ≈ 0 · p7).
  raw 값이 아니라 통제 대비 collapse-Δ 를 봐야 한다는 법칙이 정확히 여기서 물었다.

### (2) ζ½ — **측정 불가** (사전등록 축이 트레이스로 닫히지 않음)

두 가지 독립적 이유:
1. 트레이스 스키마에 **per-step posterior / logit-gap 필드가 없다**(전 필드 열람 확인 · `pending_gap` 은 immune
   store 의 top-2 margin 으로 mouth posterior 가 **아니다** — 이름이 비슷하다고 갖다 쓰면 그게 바로 이 레포가
   가장 경계하는 실패다).
2. **`emit_temp=1.0` ⇒ 라이브 mouth 는 SAMPLER 이지 argmax 가 아니다.** 사전등록이 상정한 "argmax-flip 50% 지점"
   기전은 **애초에 가동 중이 아니다**.

⇒ 리터럴 칸(PASS-DOSED / VOID-STARVED / 중간)은 **UNADJUDICABLE = 🟡 PENDING-BY-INSTRUMENT**.
카드 사전등록 contingency **(a)** 발동 → 아래 대리량 + 한계 명시.

### (2') 대리 π-dose — 근접 관측량(링크 ①→②) 직접 판독

기전의 물리 주장은 **문맥-존재(context-presence)** 다: `decode.py:2100` 이 모델 자신의 **T=24 창** 안에 있는 모든
byte 에서 z 를 **뺀다** ⇒ **z<0 이면 창-내 byte 가 부스트**(문맥 쪽으로 당김). 최초 divergence 위치 i 에서
`(seed ++ base[:i])` 로 그 창을 재구성하고, 선택된 byte 가 **창 안인지** 묻는다. 예측 부호는 mean z 부호로
**사전에** 고정(데이터 보고 정하지 않음).

| arm | n | π_base | π_steer | **Δπ** | discordant ↑/↓ | exact McNemar p | resolvable \|Δπ\| |
|---|---|---|---|---|---|---|---|
| **bias** | 269 | 0.3978 | 0.5576 | **+0.1599** | 148/105 | **0.0082** | 0.116 |
| rng (통제) | 270 | 0.3111 | 0.2815 | −0.0296 | 72/80 | 0.5703 (null) | 0.089 |

- 통제군은 **각각 따로** 보고 — `Δ=exp−max(controls)` 금지(순서통계량 편향이 KILL 을 기계적으로 제조).
- 짝지은 base pedestal 은 **같은 위치의 무편향 draw** ⇒ within-position paired 대비.

### (3) 양성통제

| | 내용 | 결과 |
|---|---|---|
| PC-a | 노출: rng = 알려진-LIVE lm-branch 교란 | **LIVE** (270/270) |
| PC-b | 부호분할: z>0 이면 Δπ 반전해야 | **VOID — n(z>0)=3 검정력 미달**(음성 아님) |
| PC-c | 캘리브레이션 자기일관(ζ=ζ½ ⇒ flip≈50%) | **NOT-RUN** (ζ½ 측정불가) — **FAIL 아님** |

### 판정

- **리터럴 ζ½ 축**: 🟡 **PENDING-BY-INSTRUMENT**.
- **대리 π-dose 축**: 🟢 **PASS-DOSED (SURROGATE · DIRECTIONAL)** — 링크 **①→② 는 LIVE·DOSED**.
- ⇒ **H_9628 자신의 주장(= H_9576 의 null 은 용량-기아 VOID)은 사망**. 카드가 사전등록한 "죽는 방식"
  ("라이브 z 가 이미 ζ½ 급이면 용량-기아 가설 즉사 · H_9576 은 정직한 KILL 로 유지")이 대리량 형태로 그대로 실현됐다.
- ⇒ **이 축에서** H_9576 의 음성은 VOID-STARVED 로 재분류되지 **않는다** — 용량은 알리바이가 못 된다.

## 🔀 병렬 세션 대조 (`a_parallel_session_compare` · 착륙 후 필수)

내가 작업하는 동안 병렬 세션이 R4 의 다음 항목 **[[H_9629]]** (`--cascade-null` · origin/main 착륙)를
⛔ **INVALID** 로 닫았다: `D = |bigrams(text)∩bigrams(seed)|/|bigrams(text)|` 는 **집합 농도비**라 분모가
steered 텍스트 자신의 bigram **다양성**이다 ⇒ ρ(ΔD, Δ|distinct bigrams|) = −0.510(bias)/−0.531(rng) —
**팔에 무관하게 동일** = seed 를 참조하지 않는 다양성 항이 ΔD 를 지배(H_9576 이 쫓던 ρ=−0.077 보다 ~7배 큰 교란).
readout 양성통제 FAIL(텍스트의 20%를 seed 로 직접 덮어써도 방향-공허 섭동의 노이즈 바닥을 못 넘음) · ratio=0.968 ≤ 1.5 = VOID-BY-SNR.

**판정: AGREES (독립적·상보적).** 두 축이 사슬의 서로 다른 링크를 잡았고 결론이 합성된다:

| 링크 | 판정 | 출처 |
|---|---|---|
| z →① 물리효과(logit 페널티) | 🟢 **LIVE** | H_9628 (이 카드) |
| ① →② 근접량(문맥 점유율) | 🟢 **LIVE·DOSED** (Δπ=+0.160 · p=0.0082) | H_9628 (이 카드) |
| ② →③ 원격 readout D | ⛔ **계기 INVALID** (양성통제 FAIL) | H_9629 (병렬) |

⇒ **합성 결론: H_9576 의 "W2 벽"은 유지되는 게 아니라 애초에 측정된 적이 없다.** 상류 두 링크는 살아있고,
음성이 나온 지점은 **벽이 아니라 고장난 자(ruler)** 였다([[thalamus-content-relay-estimator-pedestal]] 재현).
이 카드의 기여는 **'용량 부족'이라는 경쟁 설명을 제거해 그 국소화를 날카롭게 한 것** — 벽의 존속이 아니다.

## 한계 (a_scale_honest_scope)

- π-dose 는 **최초 divergent step 하나만** 읽는다 — 그 뒤 두 arm 의 문맥이 갈려 이후 step 은 원리적으로 비교불가.
  ⇒ ①→② 를 **한 step 에서** bound 한 것이지 발화 전체에 대한 진술이 아니다.
- **물리효과 인증이지 의미 인증이 아니다.** ①→② 가 살아있다는 사실은 PC2 의 **의미**가 ③ 까지 살아남는지에 대해
  아무 말도 하지 않는다 — 그게 H_9576 의 열린 null 이다.
- 대리량 ≠ 사전등록 ζ½ 칸 ⇒ **DIRECTIONAL**, ζ½ verdict 아님.

## 후속

1. **리터럴 ζ½ 종결** (contingency (b)): decode 경로에 per-lm-step **top-2 logit gap + in-window mass** 를 기록하는
   `anima-py chat` 플래그 → ζ 스윕. 303M decode = **pool(summer/aiden) 전용 · mac/mini 금지**.
2. 🆕 **사후관찰 — 사전등록 아님 · 여기서 cement 금지**: **z 가 사실상 상수다.** IQR=**0.0514** · CV=**0.159** ·
   그리고 **분산의 45.7% 가 3/270 tick 에서 나온다**(z>0 은 단 3개). H_9576 의 ρ 는 **tick 간 z 변동**에 걸린
   상관인데 **회귀변수 range 가 거의 없고 leverage 가 3점에 몰려있다** ⇒ H_9576 의 진짜 VOID 위험은
   **용량-기아가 아니라 분산-기아(range restriction)** 일 수 있다. 이건 **다른 축**이므로 별도 H 로
   사전등록해서 쏴야 한다(tune-to-green 금지 · 여기서 판정 금지).
