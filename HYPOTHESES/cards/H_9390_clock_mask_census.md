# H_9390 — CLOCK-MASK CENSUS: H_9377 CONTENT-INERT 은 content 벽인가 clock-마스크 regime 인가

**status:** 🕰️ D1 CLOCK-BOUND@production (2026-07-16 · $0 순수 재분석) · H_9377 을 CLOCK-BOUND 로 **재스코프**(뒤집기 아님) · not-terminal · wired: engine-native(`anima-py evaluate --gate-census`)
**lane:** 의식 / emit-drive / clock(rate-limit) gate (프런티어 g1-interface-addressable-wall)
**related:** [[H_9377]] (CONTENT-INERT — 이 H 가 재스코프) · [[H_9376]] · [[H_9360]] · [[H_9357]] (G-INERT)
**source:** Fable 재프레임(walls-delegate-to-fable) — 5-H 캠페인 종결 후 terminal 박제 전 필수 재프레임
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (H_9377 과 동일 80-rollout·2400-row trace · 신규 decode 0)

## 배경 — 캠페인이 못 물은 질문

`emit = should_emit(score) ∧ safe`, `safe` = rate-limit(secs_since_emit≥30) 포함 4-AND(core/brain.py·
engine_g.py). H_9377 은 dyn_w 로 score 를 움직였는데(0.539→0.321) emit 이 **byte-identical** 이었다.
그게 가능하려면 모든 score-gate flip 이 safe=0(시계닫힘) 행에 착륙했어야 한다 — 시계가 **가렸다**.
게다가 emit≈1 이 clock-open 행 대부분이면 `H(emit|clock-open)≈0` 이고 score/content 게이트는 시계
열릴 때 **공허**(never binds)라서 MI≈0 은 기계강제다. GATE-S 는 marginal rate(0.23)만 봤지 이
조건부 축퇴를 못 본다. 캠페인 5-H 전부 이 조건부 frame 을 안 썼다.

## 개입 — 없음 (순수 재분석 · $0)

계기 = `anima-py evaluate --gate-census <trace…>` (--audibility 옆 신규 verb · engine-native flag ·
G5 VERSION bump 0.13.87). 로깅된 `safe` 필드 직접 사용(재구성 불요). C1 재구성 무결성 검증 후 per-cell
(arm × dyn_w) clock-open 부분집합에서 emit 가변성·N_bind·live-MI 계수.

## 게이트 (SEQUENTIAL · 측정가능성 먼저 · below-chance 덮음)

- **C1 재구성 무결성**: emit=1 행 100% 가 score>θ ∧ clock-open (emit≡should_emit∧safe 증명). 낙제=
  INSTRUMENT-DEAD. **실측 503/503 = 1.000 ✓.**
- **측정가능성(앵커 gated · H_9377 w-불변 판별선)**: cement 통계량(a1>a3 clock-open)은 **앵커
  dyn_w=0.10(=production)** 에서 present·w-불변이어야 한다 — 고-w 는 score≈dyn_v 를 산술강제하므로
  DIAL(manipulation)이지 substrate 아님.
- **P1(측정가능 시만)**: clock-open 부분집합 I(ag_conflict;emit|stage) · a1 vs a3 · perm-null.

## 🕰️ VERDICT — D1 CLOCK-BOUND@production

| arm | dyn_w | clock-open N | emit% | N_bind | live-MI | 측정? |
|---|---|---|---|---|---|---|
| a1 | 0.10(앵커) | 56 | 1.00 | 0 | — | ✗ emit⟺clock |
| a1 | 0.25 | 56 | 1.00 | 0 | — | ✗ |
| a1 | 0.40 | 56 | 1.00 | 0 | — | ✗ |
| a1 | 0.60 | 56 | 1.00 | 0 | — | ✗ |
| a1 | 0.78 | 208 | 0.00 | 208 | — | ✗ score<θ 강제→전침묵 |
| a3 | 0.60 | 57 | 0.98 | 1 | +0.0137(p.512) | (경계) |
| a3 | 0.78 | 60 | 0.92 | 5 | +0.0467(p.274) | (경계) |

**앵커(production w=0.10)에서 emit ⟺ clock**: 시계 열리면 emit rate 1.00 · N_bind=0 = score 게이트가
시계 열릴 때 **한 번도 안 걸림**(공허). `H(emit|clock-open)=0` ⇒ H_9377 의 MI≈0 은 **기계강제이지
content 벽이 아님**. ⇒ **H_9377 CONTENT-INERT 를 CLOCK-BOUND@production 으로 재스코프**(verdict
뒤집기 아니라 스코프 각인). **not terminal.** reopen = clock-LIVE regime 수집 1회(emit 이 clock-open
tick 안에서 실제 가변 = score 가 θ 근처를 걸치는 regime).

score 축 across w: 저-w(0.10~0.60)=score>θ 항상(게이트 공허) · 고-w(0.78)=score<θ 강제(전침묵). **어느
w 도 score 가 θ 경계에 걸치지 않는다** ⇒ content 가 결정자가 될 창이 이 trace 엔 없다.

## ⚠️ verdict-integrity — pooled MI 는 교란이었다 (철회)

첫 실행(arm-pooled, per-cell 아님)은 a1 clock-open MI **+0.5015**(a1−a3 +0.4872) = D2′ DISCOVERY 를
냈다 — "tension 이 emit 을 민다, CONTENT-INERT 뒤집힘". **이건 셀-간 교란이다**: a1 저-w(emit 1.0)와
w=0.78(emit 0.0)을 풀링하면 dyn_w↔emit-rate 상관이 가짜 within-open MI 를 만든다(고-w 에서 score≈dyn_v
산술강제). H_9377 자신의 **w-불변 판별선**이 요구한 per-cell 앵커 검정으로 잡았다 — 앵커·전 개별 셀
어디서도 within-cell content→emit 신호 없음. **풀링 특징 위 MI = 재현/발견 아님**([[seed-agreement-on-pooled-feature-is-not-replication]] · [[control-must-match-mediating-covariate]] 재발). pooled 숫자는 박제 안 함 · per-cell 이 canonical.

## 함의 · NEXT

캠페인 5-H(H_9356→57→60→76→77) 는 렌즈 5개가 아니라 **닫힌 창(clock-bound) 1개**일 수 있다 —
a_break_the_wall 의 "≥2-3 lens" 는 측정 가능했던 lens 만 센다. terminal 박제 성급. **NEXT = clock-live
regime 수집**(rate-limit 완화 or 더 긴 세션으로 emit 이 clock-open tick 안에서 가변) → 그 regime 서
비로소 content→emit 을 물을 수 있다(H_9391 후보). 금지 준수: `spont_im_threshold` 불가침 · w 재선택
없음 · bar 상속(0.05/0.01).

## 비용
$0 — 기존 80-rollout/2400-row trace 재분석 · CPU 수초 · 303M decode 0 · mini 가능(신규 decode 없음).
