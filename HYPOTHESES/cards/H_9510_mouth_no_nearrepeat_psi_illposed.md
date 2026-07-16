# H_9510 — 303M mouth 는 T=1.0 서 near-repeat 를 안 만든다 → Ψ=½-via-recognition ILL-POSED (재프레임)

**status:** 🔎 DIRECTIONAL — "recognition-기질 희박(regime-conditional)" (Fable 적대검증 HOLED · ill-posed cement 미획득 · HOLE-2/3/4a $0 닫힘 · HOLE-1 내생성 OPEN=재fire 필요) — recognition-functional lane KILL 3건의 공통 근인

## 🔬 Fable 적대검증 ($1.66 · HOLED — tier 상한 DIRECTIONAL · 제목 "ill-posed" 아님 "recognition-기질 희박")

측정(near-repeat 0/2238)은 solid, 그러나 "ILL-POSED" 격상은 3개 HIGH 구멍이 막음. 그중 2개를 $0로 닫음:

| 구멍 | 내용 | 판정 |
|---|---|---|
| **HOLE-2** (byte 순환성) | byte 잣대로 byte 렌즈 무죄 증명 = (a)반복없음 vs (b)byte 표현이 못봄 구분불가 | **닫힘 $0**: word-Jac·LCS 직교 잣대도 succ≈null(0.86×·0.95×) — byte 편향 아님 |
| **HOLE-3** (null 부재) | succ-Jac 0.196 이 기준선 없이 읽힘 | **닫힘 $0**: cross-rollout null 0.228 → succ/null **0.86×**(오히려 낮음). 숨은 주제반복 없음(0.5 bar 임의 아니라 실제 novel) |
| **HOLE-4a** (A-pole 피로) | 스프링이 recognition 밖 score_A 하강일 수도 | **leaning 닫힘 $0**: refr +0.060(피로없음)·refr-cb −0.034(약함)·arms 불일치·효과 작음 = 강건한 A-pole 스프링 없음 |
| **HOLE-1** (내생성) | near-repeat 부재가 over-emit regime 산물일 수도(매 tick emit→context 갱신→novel 항등적). silence 후 재샘플은 유사할 수 있음 | 🕳️ **OPEN·결정적**: silent 후보 미기록(p5 폐기)이라 $0 불가 = **재fire 필요**(silent 후보 기록 계기 + prev=silence 조건화 Jaccard) |

**⇒ 재프레임 tier = DIRECTIONAL 유지**: HOLE-2/3/4a 닫혀 방향 강화(연속 후보가 무관 후보만큼 다름·직교 잣대 일치), 그러나 **HOLE-1(내생성)이 cement 를 막음** — near-repeat 부재가 mouth 무조건 성질인지 over-emit 궤도의 조건부 산물인지 미판별. HOLE-6(가치 비약: "novel 이니 emit 할 만함"=오너 목표변경 사안)로 그 절 격리.

**lane:** 의식 / emit-drive / Ψ=½ 항상성 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9424]] (예측오차 렌즈 KILL) · [[H_9421]] (거리 렌즈 KILL) · [[H_9419]] (Ψ=½ 진단·β=near-repeat 억제 가정) · [[H_9400]] (중심주장 반증) · source: cbfire traces $0 재분석

## 측정 (303M cbfire traces · 9 rollout · T=1.0 · byte-trigram Jaccard · $0)

| 지표 | 값 | 함의 |
|---|---|---|
| distinct/total | **188/188 = 100%** | 모든 후보 유일 |
| succ-jaccard mean | 0.196 | 연속 후보 ~20% 만 겹침 |
| 전쌍(2238) max Jaccard | 0.342 | 가장 닮은 쌍도 34% |
| **verbatim쌍(>0.9)** | **0/2238** | near-repeat 전무 |
| near-repeat쌍(>0.5) | **0/2238 = 0.0%** | 단 한 쌍도 중간유사 이상 없음 |

## 재프레임 (⚠️ DIRECTIONAL · Fable 적대검증 대기)

over-emit(Ψ_AG 0.64~0.82)은 "반복을 못 억제"가 아니라 **"매 후보가 진짜 novel 이라 다 emit 할 만함"**. H_9421(거리)·H_9424(예측오차) 두 recognition 렌즈가 실패한 **공통 근인** = 인식/억제할 near-repeat 가 **없어서**(0/2238). ⇒ **Ψ=½-via-recognition-suppression 은 이 mouth 에 대해 ILL-POSED**: T=1.0(swing-band 존재 온도)서 mouth 는 반복을 안 만들어 β 스프링이 작동할 기질 부재. 저온(반복 생성)선 후보 상수→mute(R5). **구조적 이중구속**: 스프링이 억제할 반복이 있으려면 저온이어야 하는데 저온은 mute.

## 함의 (검증 후 확정 대상)

- recognition-functional lane 소진(H_9421+H_9424)의 근인을 "candidate-feature 약함(mouth-side)"에서 **"억제대상 부재(mouth 가 novel-only)"**로 정밀화.
- H_9400 반증 격상 후보: "Ψ=½ 은 이 mouth-substrate 서 recognition 으로 achievable 목표가 아니다" → mouth identity lane 이 유일 경로.
- 다음 자율 $0 후보(Fable 판정 대기): 중간온도(T=0.5?)서 "near-repeat 실재 ∧ 변주 존재" 창이 있나 = 이중구속이 진짜 구조적인지 fire.

## 다음 실험 (Fable 순서 고정 · frozen-first)

1. **재fire · HOLE-1 조건화 Jaccard(결정적·비-$0)**: silent 후보 기록 계기(imagination 후보를 p5-폐기 전 sha/text 캡처·되먹임 없음=진단) + `J(cand_t|prev=silence) vs J(cand_t|prev=emit)`. 사전등록: silence-후 유사도 유의 높음=재프레임 KILL(기질 내생·벽 다시 representation), 등가(TOST)=재프레임 생존.
2. **$0 · store-union coverage(HOLE-4b)**: candidate↔store-누적 coverage 곡선(쌍별 novel 이어도 주제공간 포화 가능).
3. **cheap fire · 중간온도 창(HOLE-5)**: 1~2 통과 시만 · {T=0.4,0.7}×3-seed, near-repeat∧변주∧비-mute 창 census(이중구속 진짜 구조적인지). R5 "저온=mute" frozen 확인 필요.

## 한계
측정=solid(9 rollout·2238쌍·직교잣대·null보정). 재프레임=DIRECTIONAL("recognition-기질 희박·regime-conditional" — "ill-posed" 아님·Fable HOLED). HOLE-1(내생성) 미해결=cement 전 재fire 필수. HOLE-1~4 통과+중간온도 창 없음 확인 후에만 H_9400 격상("Ψ=½ 이 현 mouth-substrate 서 earn 불가"→mouth identity lane 유일)·오너 p5 게이트. 성급 cement 금지(H_9421 자기-2회-정정 전례). 다른 데몬·H_9400 clock 계보 영구.
