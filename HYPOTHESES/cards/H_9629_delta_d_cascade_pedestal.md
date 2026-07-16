# H_9629 — ΔD 는 애초에 읽을 수 있는 양인가 — 참값-0 캐스케이드 대좌

**status:** ⛔ **INVALID** (measured 2026-07-17 · engine-native `anima-py evaluate --pc2-direction --cascade-null` v0.15.22 · n=270 paired emit tick · 3 seed)
**낙착 칸:** 사전등록 판정표의 **'양성이 대좌 못 이김 ⇒ INVALID'** — 그리고 **ratio=0.968 ≤ 1.5 = VOID-BY-SNR 칸도 동시 발화**. 두 칸이 같은 방향을 가리킨다: **H_9576 의 방향 KILL 은 음성으로 읽을 수 없다.**
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


---

# 📊 측정 결과 (2026-07-17 · engine-native · verbatim → 아래 재현 커맨드)

```
anima-py evaluate --pc2-direction /tmp/pmp/pmp_traces --cascade-null
```

| arm | n | mean ΔD | sd | var | 역할 |
|---|---|---|---|---|---|
| off | 270 | 0 | 0 | 0 | 기저(구성상 0) |
| static | 270 | +2.012e-04 | +3.222e-03 | +1.038e-05 | 참값-0 · **re-roll 없음 = 하한** |
| rng | 270 | +6.645e-03 | +9.469e-02 | +8.966e-03 | 참값-0 · dose-matched · **full cascade = 1차 대좌** |
| bias | 270 | +6.307e-03 | +9.317e-02 | +8.681e-03 | 조작 arm |

- **(0) 기저 PASS** — base gtext 가 off==bias==rng byte-identical(3/3 seed · 150 tick) ⇒ ΔD_off ≡ 0.
- **(2) 대좌 LIVE** — rng ΔD≠0 269/270 · static 60/270 ⇒ **우연-아래 칸(치환 미작동 배선결함) 아님**.
- **(4) 사전등록 통계** — `ratio(bias/rng) = 0.968` · F(269,269) **p=0.791** · paired-swap null95%=[0.829,1.194] **p=0.741**
  ⇒ bias 의 ΔD 분산은 **방향-공허** dose-matched 대좌와 **통계적으로 구별 불가**(1.0 이 null 한가운데).
  `ratio(bias/static) = 836` (p=0.000) ⇒ **ΔD 분산의 사실상 전부가 하류 re-roll 캐스케이드에서 나온다** = 카드 주장 확증.
- **(3) readout 양성통제 FAIL** — toward-seed dose ladder 는 5 dose **단조·부호 정확**(k=16 ΔD=−0.174)이나
  2·sd(ΔD_rng)=0.189 를 못 넘음. 즉 **텍스트의 20%(16/80 byte)를 seed 로 직접 덮어써도 방향-공허 섭동의 노이즈 바닥에 못 미친다.**
  away-pole 은 비단조·부호역전(k=16 서 예측과 반대).

## 🔑 기전 규명 — D 는 seed 를 안 보고도 움직인다 (코드-확증)

`cli/evaluate.py::_ov` 의 정의는 **집합 농도비**다:

```
D = |bigrams(text) ∩ bigrams(seed)| / |bigrams(text)|      # _big() 은 set 을 반환
```

분모가 **steered 텍스트 자신의 bigram 다양성**이다 ⇒ steering 이 텍스트의 다양성만 바꿔도 ΔD 가 움직인다.
측정 (5):

```
bias rho(ΔD, Δ|distinct bigrams|) = -0.510   (n=270)
rng  rho(ΔD, Δ|distinct bigrams|) = -0.531   (n=270)
```

- 두 팔에서 **거의 동일** ⇒ 이 항은 조작과 무관한 순수 교란.
- H_9576 이 쫓던 신호 **ρ(z,ΔD) = −0.077** 보다 **~7배 큰** 교란이 readout 안에 들어 있었다.
- away-pole 붕괴도 이것으로 설명된다: 반복 filler byte 가 집합 원소 **1개로 붕괴** → 분모 축소 → D **상승**(예측과 반대).

## 판정 — H_9576 의 'W2 벽'은 유지되는가

**아니다. VOID 로 재분류된다.** 세 근거가 독립적으로 같은 곳을 가리킨다:

1. **SNR**: bias ΔD 분산 ≈ 방향-공허 대좌 분산(ratio 0.968 · p=0.741) ⇒ per-tick 입도에서 방향은 **원리적으로 미측정**.
2. **양성통제**: 20% 텍스트 덮어쓰기라는 거대 dose 도 대좌 위로 못 솟음 ⇒ readout **미인증**.
3. **기전**: ΔD 의 지배항은 seed 를 참조하지 않는 다양성 교란(|ρ|≈0.52)이며 표적 신호(0.077)의 7배.

⇒ H_9576 의 ρ≈0 은 "byte 입도가 PC2 의미를 표현 못 한다"(W2 벽)의 증거가 **아니라**, **읽을 수 없는 계기로 읽은 값**이다.
[[positive-control-before-reading-a-negative]] · [[phi-estimator-needs-zero-truth-pedestal]] 의 mouth 판 재현.

## 이 판정이 R4 체인에 미치는 영향 (⚠️ 하류 차단)

R4 발사 순서의 뒷 실험(H_9630~9635)은 **전부 D 를 원격 readout 으로 물려 있다** ⇒ **D 를 그대로 쓰면 그 음성들도 전부 읽을 수 없다.**
선행조건 = **readout 재설계**: ① 분모 고정(base 텍스트의 bigram 집합으로 정규화하거나 다중집합 카운트 사용) ② 블록-집계
(per-tick 입도 포기) ③ 재설계된 readout 에 **먼저 dose-ladder 양성통제**를 통과시킨 뒤에야 방향 실험 재개.
특히 [[H_9634]] loading-name-race 는 **이 readout 위에서 발사하면 안 된다**.

## SCOPE — 이 런이 못 하는 것 (a_scale_honest_scope · 없는 숫자 금지)

- 카드의 cascade arm(**2nd-best byte 강제 + 하류 re-roll**)과 **ζ=±4 포화 양성통제**는 **라이브 디코드 필요** — `py303_full.clm` 은
  pool-side 라 **이 숫자에 없다**. 대신 트레이스가 이미 가진 `rng`(dose-matched · full-cascade · direction-void)를 1차 대좌로,
  `static`(re-roll 없는 **하한** — bias SNR 을 과대평가하므로 VOID 판독은 a fortiori 성립)을 2차로 썼다.
- oracle dose ladder 는 **readout 측** 양성통제이지 ζ arm 의 대체가 **아니다**.
- ⚠️ oracle 의 `2·sd` 바는 **카드에 사전등록된 바가 아니라 이 구현이 정한 바**다. 결과를 보고 되돌리지 않았다(tune-to-green 금지).
  이 바가 임의적이라는 점을 감안해도 판정은 흔들리지 않는다 — (4)의 ratio=0.968 과 (5)의 |ρ|≈0.52 는 바와 무관하다.

## pool 발사 스펙 (남은 arm · summer/aiden · **mini 금지** · [[heavy-anima-eval-pool-not-mini]])

```bash
anima-py chat --pc2-mouth cascade --pc2-zeta 0   <ckpt>   # 2nd-best byte @ 결정론 lm-step 1곳
anima-py chat --pc2-mouth bias    --pc2-zeta 4   <ckpt>   # ζ=+4 포화 arm
anima-py chat --pc2-mouth bias    --pc2-zeta -4  <ckpt>   # ζ=-4 포화 arm
# seeds 7,4302,4303 · 동일 150 tick → 새 traces dir 에 대해 이 플래그 재실행
```
⚠️ 단, **위 발사는 readout 재설계 이후에만 의미가 있다** — 현 D 로는 ζ=±4 arm 도 같은 다양성 교란을 탄다.
