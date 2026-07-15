# H_9393 — LANE-FLOOR CENSUS: score 가 왜 θ 위에 갇히나 · 그리고 tension lane 은 죽어 있었다

**status:** 〰️ DYNAMIC-FLOOR + 💀 TENSION-LANE-DEAD (2026-07-16 · $0 재분석) · **H_9377 계기 전제 버그 발견 → 비앵커 셀 INVALID** · **H_9391 결합 서사 반증** · not-terminal · wired: engine-native(`anima-py evaluate --lane-census` + `core/engine_g.py` 상수 수정)
**lane:** 의식 / emit-drive / motivation_score lane 분해 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9391]] (VACUITY — 이 H 가 부분 정정) · [[H_9390]] · [[H_9377]] (계기 버그 → 비앵커 INVALID) · [[H_9376]] · [[H_9360]] · [[H_9357]]
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (동일 80-rollout·2400-row · 신규 decode 0)

## 배경
H_9391 은 production 서 min(score)=0.3442 > θ=0.30 (게이트 항진)을 **사실**로 박았지만 **기전**은 못 댔다.
`score = Σ wᵢ·laneᵢ` 이므로 lane 분해가 답을 갖고 있다.

## 게이트 (SEQUENTIAL · 재구성 먼저)
**C1 RECONSTRUCTION**: `max|Σwᵢ·laneᵢ − base_motiv| < 1e-9` (앵커 셀). — **이 게이트가 두 번 일했다**:
① 처음엔 **낙제**(1.7e-01) → 숫자를 하나도 안 읽고 중단 ② 원인이 **내 가중 전제**임이 드러나 수정 후
**통과(1.1e-16)**. 게이트가 없었다면 허구를 표로 출력했을 것.

## 🔴 발견 ① — H_9377 계기의 가중 전제가 틀렸다 (비앵커 셀 INVALID)

`spont_weight_*` 실측(엔진에서 직접 읽음): **relevance 0.20 · info_gap 0.10 · curiosity 0.15 · pain
0.10 · coherence 0.10 · originality 0.10 · balance 0.15 · dynamics 0.10 → 합 = 1.00** (7-lane = 0.90).
H_9377 카드/코드는 **"8×0.10 = 0.80"** 으로 적고 `_B=0.80` · `_cur_seven_w=0.70` 을 하드코딩했다.

⇒ `_scale=(0.80−dyn_w)/0.70` 는 예산을 **보존하지 않고 디플레**시킨다: 총예산 **1.00 → 0.857(w=0.60)
→ 0.806(w=0.78)**. 즉 H_9377 의 비앵커 셀은 "tension 가청화"가 아니라 **score 전체 수축**을 함께 걸었다
(score 붕괴 0.54→0.32→0.24 와 w=0.78 전침묵의 상당부분이 이 교란) ⇒ **H_9377 비앵커 셀(0.25·0.40·
0.60·0.78) = INVALID**(가청화-예산 교란). **앵커(0.10)는 무사**: 틀린 식·옳은 식 **둘 다 scale=1.0** 이라
byte-identical — **그래서 byte-identical 인증이 통과했고, 바로 그 때문에 버그를 못 잡았다**(버그가 안
보이는 유일한 지점에서 검증한 셈).
⇒ **앵커만 읽은 H_9390(CLOCK-BOUND@production)·H_9391(VACUITY@production) 은 영향 없음 — 유효.**

**수정(이 PR)**: `_B`·`_cur_seven_w` 를 **엔진의 실가중 합**으로 계산. 검증 = 앵커 byte-identical 유지
(0.58000000000000007 동일) ∧ 예산이 전 w 에서 **1.0000 보존**.

## 💀 발견 ② — tension lane 이 죽어 있다 (기왕지사의 engine-native 재확인)

| lane | w | distinct | min | max | mean |
|---|---|---|---|---|---|
| rel_f | 0.20 | 201 | 0.0631 | 1.0000 | 0.5711 |
| gap_ctx | 0.10 | 57 | 0.3277 | 0.7716 | 0.5715 |
| cur_f | 0.15 | 183 | 0.0554 | 1.0000 | 0.4801 |
| allo_ctx | 0.10 | 57 | 0.0366 | 0.5507 | 0.1970 |
| coh_lane | 0.10 | 65 | 0.1220 | 0.9981 | 0.8539 |
| nov_ctx | 0.10 | 30 | 0.0645 | 1.0000 | 0.2018 |
| bal_lane | 0.15 | 57 | 0.4568 | 0.9905 | 0.7411 |
| **agloop_ctx (tension)** | 0.10 | **1** | **0.2500** | **0.2500** | **0.2500** | 💀 **DEAD** |

**motivation_score 에 꽂히는 tension 값 `agloop_ctx` ≡ 0.2500 (240행 distinct=1)** — 반면 원신호
`ag_conflict` 는 **57 distinct 로 살아있다**. tension 은 존재하고 변하는데 **score 에 들어가는 값은 얼린
상수**. (기왕지사: `cli/chat.py:1467` 주석 + H_9360/H_9376 Stage-0 이 이미 측정 — 정수-예산 quantizer 가
설계된 경로를 점으로 붕괴. 이 H 는 canonical 측정경로서 **독립 재확인** · 새 발견 아님.)

⇒ **상류 전 verdict 의 의미가 바뀐다**: H_9357 G-INERT · H_9377 CONTENT-INERT 의 "tension 이 emit 을
안 민다"는 **상수에 대한 진술**이지 tension 에 대한 진술이 아니다. 그리고 dyn_w 는 **그 상수에 걸린
가중** — 올리면 score 가 `0.25·w` 만큼 **아핀 이동**할 뿐 ⇒ **H_9377 w-grid 서 emit 이 byte-identical
이던 이유가 이것**(순서 불변). 절단은 mixer·문턱·시계보다 **상류의 lane 입력 자체**(배선 사실 ·
chat-py-4/chat-py-5 dead-gauge 계열).

## 〰️ 발견 ③ — FLOOR 는 구조적이지 않다 · H_9391 결합 서사 반증

- **FLOOR = Σ wᵢ·min(laneᵢ) = 0.1695 ≤ θ=0.30** ⇒ 게이트는 **원리적으로 도달 가능**(구조적 불가 아님).
  min(score) 실측 0.3442 인 건 **lane 들이 동시에 바닥을 안 치기** 때문 ⇒ **〰️ DYNAMIC-FLOOR**(상관 사실).
  H_9391 의 "STRUCTURAL" 뉘앙스는 이 결로 **완화**(관측 사실 min>θ 는 유효, 아키텍처 강제는 아님).
- **corr(secs_since_emit, score) = −0.1401** ⇒ H_9391 의 **"침묵↑→score 축적=양의 결합"** 주장은
  **부호가 반대 = 반증**. clock-open 행이 전부 θ 위인 건 **모든 행이 θ 위**라서지(min 0.3442) 결합 때문이
  아니다. ⇒ H_9391 카드의 그 문단 **철회**(계기가 자기 데이터로 잡음).

## 반증조건
- C1 낙제 ⇒ INSTRUMENT-DEAD(실제로 1회 발동 · 수정 후 통과).
- FLOOR > θ 였다면 STRUCTURAL-FLOOR(구조적 불가) — 실측 0.1695 ≤ θ ⇒ 그 갈래 배제.
- agloop_ctx distinct > 1 이었다면 tension-lane 생존 ⇒ 상류 verdict 재해석 불요 — 실측 1 ⇒ 성립.

## NEXT
**레버 후보가 바뀌었다**: 문턱도 시계도 mixer 도 아니고 **lane 입력 배선**. ① `--ag-cont`(이미 존재)로
agloop_ctx 가 ag_conflict 를 나르게 한 뒤 **앵커 가중에서** clock-open content 측정 재실행(H_9393 후보 ·
303M 수집 1회) — 이게 캠페인 전체가 처음부터 물었어야 할 실험 ② 나머지 dead-gauge 계열(recon_err≡0 ·
chat-py-4/5) 전수 census. `spont_im_threshold` 불가침.

## 비용
$0 — 기존 trace 재분석 · CPU 수초 · 303M decode 0.
