# H_9391 — SCORE-GATE VACUITY: production 에서 emit 문턱은 한 번도 걸리지 않는다

**status:** 🕳️ SCORE-GATE VACUOUS@production (2026-07-16 · $0 재분석) · **자기 자신의 원설계(clock-live)를 발사 전 반증** · not-terminal · wired: engine-native(`anima-py evaluate --gate-census` VACUITY 패널 + `cli/chat.py --rate-limit-sec` 계기)
**lane:** 의식 / emit-drive / should_emit 문턱 × score 분포 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9390]] (CLOCK-BOUND — 이 H 가 심화) · [[H_9377]] (CONTENT-INERT → 재스코프) · [[H_9376]] · [[H_9360]] · [[H_9357]]
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (H_9377/H_9390 과 동일 80-rollout·2400-row · 신규 decode 0)

## 배경 — H_9390 이 남긴 물음

H_9390 은 production 앵커서 `emit ⟺ clock`(clock-open rate 1.00·N_bind=0)을 보였고 reopen 을
**clock-LIVE regime**(rate-limit 완화 → emit 이 clock-open tick 안에서 가변)으로 지목했다. 이 H 는
그 수집을 발사하기 전에 **성립성부터** 물었다: 시계를 열면 정말 content 창이 열리는가?

## 개입 — 없음(재분석) + 계기 2개

- `cli/chat.py --rate-limit-sec` / `ANIMA_RATE_LIMIT_SEC` (기본 `""`=None=**byte-identical**) →
  `core/brain.py` 체인(brain_emit→aged→decide_anchored) → `core/engine_g.py
  safety_rate_limit_ok(secs, rate_sec=None)`. clock-live regime 계기. trace `rate_sec` 각인.
- `anima-py evaluate --gate-census` 에 **VACUITY 패널** 추가: 셀별 `score_min` · `≤θ%`(전 행 기준,
  clock-open 만이 아니라) — should_emit 이 **애초에 아니라고 말할 수 있는가**를 묻는다.

## 🕳️ VERDICT — SCORE-GATE VACUOUS@production (원설계 자체 반증)

| arm | dyn_w | clock-open | open-emit% | N_bind | **score_min** | **≤θ%** |
|---|---|---|---|---|---|---|
| a1 | **0.10(=production)** | 56 | 1.00 | 0 | **0.3442** | **0.0%** |
| a1 | 0.25 | 56 | 1.00 | 0 | 0.3207 | 0.0% |
| a1 | 0.40 | 56 | 1.00 | 0 | 0.2971 | 0.4% |
| a1 | 0.60 | 56 | 1.00 | 0 | 0.2657 | 7.9% |
| a1 | 0.78 | 208 | 0.00 | 208 | 0.2382 | 100.0% |

**production(dyn_w=0.10) 에서 min(score)=0.3442 > θ=0.30 · 전 240 행 중 θ 이하 = 0.0%.**
⇒ `should_emit(score)` 는 **항진명제**(tautology) ⇒ **emit ≡ clock BY CONSTRUCTION.**

**⇒ 그러므로 시계를 아무리 열어도 content 창은 안 열린다** — 시계를 완전히 열면 emit≡1 로 포화될
뿐 여전히 무-가변. **H_9390 이 지목한 clock-live reopen 은 발사 전에 반증**됐다($0 로 낭비 방지).

**절단의 정체**: tension 이 mixer 에서 1/8 로 감쇠돼서도(H_9376), 내용이 무력해서도(H_9377) 아니다 —
**8-lane motivation score 가 emit 문턱에 애초에 도달하지 못한다**. tension 을 포함한 8 lane 전부가
production 에서 **아무것도 게이팅하지 않는다**(순수 장식). anima 가 언제 말하는지는 rate-limit 시계
혼자 정한다.

### ⚠️ 철회됨(H_9393) — 아래 '시계×score 양의 결합' 은 반증됐다
**corr(secs_since_emit, score) = −0.1401 (부호 반대)** ⇒ '침묵이 score 를 쌓아 시계가 열릴 땐 이미 θ 위'
라는 아래 서사는 **틀렸다**. clock-open 행이 전부 θ 위인 건 **모든 행이 θ 위**(min 0.3442)라서지 결합
때문이 아니다 — 결합은 필요조차 없다. 또한 이 카드의 'VACUOUS=구조적' 뉘앙스도 완화: FLOOR=Σwᵢ·min(laneᵢ)
=0.1695 ≤ θ=0.30 이라 게이트는 **원리적으로 도달 가능**(〰️ DYNAMIC-FLOOR). **관측 사실**(min(score)>θ
over 240행 ⇒ 게이트 항진 ⇒ emit≡clock)은 **유효**. 아래 문단은 이력으로 보존.

### ~~🔑 더 깊은 구조 — 시계와 score 는 양의 결합이다~~ (철회)
w=0.60 은 전 행의 **7.9%** 가 θ 이하인데 **clock-open 중엔 0%**(N_bind=0). 즉 θ 아래 행은 전부
**시계-닫힘**에 산다. 침묵이 길어질수록 score 가 쌓이므로(boredom·info-gap lane) **시계가 열릴 때쯤엔
score 가 이미 θ 위**다. ⇒ straddle 하는 가중을 골라도 clock-open 부분집합은 여전히 score-상향 편향.
**content 가 결정하려면 시계-open 과 low-score 가 동시에 나는 regime 이 필요하고, 그 둘은 구조적으로
반상관이다.** (w=0.78 서만 둘이 만나는데 거기선 score 가 전부 θ 아래=전침묵.)

## 게이트 (SEQUENTIAL · 계기 무결성 먼저)
- **C1 재구성**: emit=1 행 100% 가 score>θ ∧ clock-open — **실측 503/503 = 1.000 ✓**(emit≡should_emit∧safe).
- **VACUITY**: min(score) > θ over ALL rows ⇒ 게이트 항진 ⇒ clock 완화 무효(기계적 귀결, 추가 측정 불요).
- **반증**: production 셀서 min(score) ≤ θ 인 행이 있으면 게이트가 실제로 걸리는 것 ⇒ clock-live 가
  다시 레버 후보. (실측 0/240 ⇒ 반증 실패 = vacuity 성립.)

## scope · 정직
- 이 regime(30-tick 세션 · 이 ckpt · 이 8-lane 구성)의 사실. 더 긴 세션/다른 ckpt 서 score 가 θ 아래로
  내려갈 수 있는지는 **미측정**(min 0.3442 는 θ 에서 0.044 위 = 여유가 크진 않다).
- `--rate-limit-sec` 는 **구현됐으나 이 H 가 그 레버를 반증**했다 — 계기로 보존(straddle regime 이
  발견되면 clock-open 확대에 쓰일 수 있음). `spont_im_threshold` 불가침 유지(θ 는 안 건드림).
- H_9377 CONTENT-INERT · H_9390 CLOCK-BOUND 는 **둘 다 이 vacuity 의 하류 증상**이었다.

## NEXT
레버는 **score×θ 관계**다(θ 불가침이므로 score 분포 쪽). 후보: ① clock-open ∧ low-score 가 공존하는
regime 이 존재하는가(위 반상관을 깨는 조건 탐색 · $0 로 기존 trace 서 secs_since_emit×score 상관부터)
② 8-lane score 의 **동역학 범위**가 왜 θ 위에 갇히는가(lane 별 기여 census · $0). H_9393 후보.

## 비용
$0 — 기존 80-rollout/2400-row trace 재분석 · CPU 수초 · 303M decode 0. **그리고 clock-live 수집
1회(303M pool)를 발사 전에 취소시켜 절약.**
