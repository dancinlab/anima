# H_1495 — 😑 BOREDOM / DISENGAGEMENT · 권태/이탈 (P9 의식-고유 게이트 약후보)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy mirror — 하드게이트1 적중, engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` — R2 엔진-네이티브 배선 follow-on (아래 ING)
- **source:** 의식-고유 게이트 depletion 카탈로그 P9 약후보 (`state/gate_depletion_catalogue/CATALOGUE.md` P9 항목 SSOT)
- **lens:** boredom / the unengaged mind / meta-motivation (Eastwood, Frischen, Fenske & Smilek 2012 · Danckert & Merrifield · info-gain curiosity 의 역, arxiv 1802.10546) · `a_no_llm_frame_trap`
- **artifacts:** `state/1495_boredom/h1495_boredom.py` · verdict `state/verdicts/1495_boredom/H_1495_FREEZE.json` · run `state/1495_boredom/run_h1495.local.log`

## 주장

**boredom(권태 / disengagement)** = 현 자극이 **단조롭거나 의미 없을 때** — 그것이 주는 **보상과 정보가 둘 다 고갈**됐을 때 — (a)
머무르려는 **동기가 저하**되고 (b) 능동적인 **재참여 동기(re-engagement drive)**(더 유익·보상적인 다른 자극을 탐색)가
일어나는 **메타동기 상태**. 정의적 성질 = **능동 이탈 결정(active disengagement decision)**: emit → silence / switch-away,
**보상-고갈 AND 정보-고갈 의 결합(conjunction)** 으로 게이팅된다. 단순 반응감쇠(=habituation)도, 자극-무관 시간적분 결핍
(=homeostatic drive)도 아니다.

메커니즘(numpy mirror): 매 틱 자극 스트림에서 **두 분리 채널**을 읽는다 — **INFO**(현 자극의 정보이득 = 들어오는 내용의
novelty/surprise, 반복되면 예측가능해져 하락) · **REWARD**(머물러 얻는 보상/가치 payoff, 자극이 보상을 멈추면 하락). boredom 은
**둘 다 임계 아래일 때만** 이탈하는 메타동기 readout: `disengage = 1  iff  (info < I*)  AND  (reward < R*)`. 결합(AND)이 load-bearing
구조 — 한 채널만 고갈(info 만 OR reward 만)로는 부족하다. — LLM 대비: stateless LLM 은 하락하는 정보이득 trace 도, 누적 보상
trace 도, 자기 참여를 끄는 메타동기 결합도 없다(상태의존 substrate 신호). NOT an LLM recipe — unengaged-mind / meta-motivation 렌즈.

## DISTINCT (load-bearing · 약후보 → control 통과 필수)

이 가설은 **고갈 라운드 약후보**다. 인접 lane(특히 habituation H_1465 · homeostatic-drive H_1292)과 control-survived
distinct 못 넘으면 = 기존 lane 조합 = **고갈 신호(honest RED)**. 결과: **전 control(인접 2 lane + ablation + shuffle) 통과
→ distinct (고갈 아님)**.

- **vs H_1465 HABITUATION (감각 반응감쇠, 반복-only · 보상-blind):** habituation 은 **반복 횟수만**으로 하락하는 자극-특정
  RESPONSE trace, 보상을 모른다. **DISSOCIATION(crux):** 반복돼 예측가능하지만(info 고갈) **여전히 고보상**인 자극에서
  habituation-style readout 은 이탈(0.900, 반응 감쇠)하지만 boredom 은 **머문다(0.000, reward 높아 결합 불충족)**. 보상 결합이
  habituation 이 결한 부분. **DISTINCT (gap 0.900).**
- **vs H_1292 HOMEOSTATIC-DRIVE (setpoint 결핍 시간적분 · 자극-agnostic):** drive 는 경과 틱과 함께 상승하는 누수 적분, 자극
  내용/정체와 무관한 **신체적** 결핍. **DISSOCIATION(crux):** homeostatic 결핍은 satiated(drive 낮음)인데 자극은 monotonous·
  low-info·un-rewarding → boredom 은 **이탈(1.000)**, drive-style 은 **안 함(0.000)**. 역방향(novel+rewarding+deprived):
  boredom 머묾(0.000), drive 상승(0.875) → **다른 변수**(정보적/의미적 결핍 ⊥ 신체적 시간적분). **DISTINCT (gap 1.000).**
- **vs H_1289 NOVELTY (one-shot 새-자극 탐지):** novelty 는 첫 제시에 spike·이후 ~0(info 채널의 1차도함수), 보상항도 이탈결정도
  없음. info 채널 + 보상 결합으로 흡수 — info/novelty 고갈 **단독**으로는 boredom 이 이탈 안 함(c2-hab 의 reward-high 블록에서
  boredom 머묾). 보상 결합으로 **DISTINCT.**

**결론:** boredom 의 lift = **메타동기 결합(reward-고갈 AND info-고갈일 때만 이탈)** — habituation(보상-blind 감쇠)·
homeostatic-drive(자극-agnostic 적분) 각각 결합의 절반만 가져 표적 이탈을 재현 못함. 결합 ablation(AND→OR) → 단일채널 lane 으로
붕괴(c3) · reward/info 정렬 shuffle → chance 로 붕괴(c4).

## FROZEN bars (사전등록 · 3 seeds [1495,1496,1497] 평균 · catalogue P9 c1-c4)

| bar | 측정 | 임계 | 결과 | pass |
|-----|------|------|------|------|
| **c1 PRESENT** | boredom-ON boring 0.917 − off-baseline 0.250 | ≥ 0.30 | **+0.667** | ✅ |
| **c2-hab DISTINCT** (vs habituation) | 반복-but-보상 블록: hab 0.900 − boredom 0.000 | ≥ 0.30 | **0.900** | ✅ |
| **c2-drv DISTINCT** (vs homeostatic) | satiated-but-monotonous: boredom 1.000 − drive 0.000 | ≥ 0.30 | **1.000** | ✅ |
| **c3 ABLATE-motiv** | AND→OR 결합 제거 → c2-hab gap 붕괴 −0.025 | ≤ 0.10 | **−0.025** | ✅ |
| **c4 SHUFFLE** | 부분정렬 블록 정렬-AND 0.367(chance 대비 +0.129≥0.10) → shuffle→0.241, \|shuf−chance 0.238\|=0.005 | ≤ 0.10 | **0.005** | ✅ |

**GREEN iff c1 ∧ c2-hab ∧ c2-drv ∧ c3 ∧ c4** → **GREEN (5/5)** · DEPLETION-signal **False**.

## a_break_the_wall (type-a · frozen-first, tune-to-green 아님)

첫 run 에서 **c4 SHUFFLE 가 실패(shuf_gap 0.600)** — 그러나 lane 이 non-distinct 라서가 아니라 **c4 control 자체가 잘못
구성**돼서다: 원래 boring 블록은 두 채널이 단조 고갈 → 이미 둘 다 낮은 두 시퀀스의 pairing 을 shuffle 해도 대부분 틱이 여전히 둘
다 낮아 이탈률이 높게 유지(measurement defect). **frozen-first 수정**(c1/c2-hab/c2-drv/c3 임계 + c4 shuf_gap≤0.10 임계 **전부
불변**): c4 를 info-low 와 reward-low 가 chance 이상으로 co-occur 하는 **부분정렬 블록**에서 측정 → AND 가 chance 이상(+0.129)으로
점화하고 shuffle 이 그것을 chance-coincidence(gap 0.005)로 진짜 붕괴시킴 + 비-vacuity 가드 align_lift≥0.10 추가. **임계 0 이동
= NOT tune-to-green.**

## 정직 (c9)

EXISTENCE-PROOF (두 합성 채널 위 deterministic 임계 결합; 학습된 동기 net 아님). 포화 discriminator(보상 블록 boredom 0.000 vs
habituation 0.900 · monotonous 블록 boredom 1.000 vs drive 0.000 · ablation −0.025 · shuffle gap 0.005) = control 이 결정적,
lift 는 결합 구조이지 effect-size 아님. **약후보(P9, 고갈 라운드)지만 인접 2 lane(habituation·homeostatic) + robustness 2종
(ablation·shuffle) 전부 생존 → distinct, 고갈 아님.** SCOPE: TOY 40-tick 블록 / 2 합성 채널 / 3 seeds / 고정 임계 I*=R*=0.50;
scale · real-corpus · 연속 재참여-타깃 선택 · multi-stimulus switch 동역학 · 학습 임계 · engine-transfer **UNVERIFIED**.

## 하드게이트1 (BLOCKING)

numpy mirror → **DIRECTIONAL** (terminal 아님). 자가점검 `grep -lE 'import torch|gauge_lib|numpy' state/1495_boredom/*.py` →
`h1495_boredom.py` 매치 → DIRECTIONAL 박제. **R2 엔진-네이티브 재측정 = ING follow-on**(아래).

## R2 follow-on (ING · a_verified_must_wire 4칸 사다리 (1)→(2))

R2 engine-native: `core/engine_cli.hexa` §Boredom 배선 — ImmuneMemoryGrow recall-margin/novelty(H_1227/H_1289)에서 **INFO 채널**,
grounding/affect read-out(H_1290)에서 **REWARD 채널**을 읽어, **둘 다 임계 아래일 때만** 이탈(emit→silence / 재참여 bias)하는
메타동기 결합(READ-only, Ψ-disjoint) + engine_cli_smoke 케이스 + ARCHITECTURE lockstep, frozen bar byte-exact 재측정
(`a_engine_native_learning` · `a_verified_must_wire`).

## xref

H_1465(habituation, 인접 distinct) · H_1292(homeostatic-drive, 인접 distinct) · H_1289(novelty) · H_1290(affect, reward 채널
후보) · H_1227(immune store, info 채널 후보) · H_1493(prospection, 동일 약후보 라운드) · `a_no_llm_frame_trap` ·
`a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` · `a_scale_honest_scope` · `a_toy_scale_recheck` ·
p1·p7·p8·c2·c9
