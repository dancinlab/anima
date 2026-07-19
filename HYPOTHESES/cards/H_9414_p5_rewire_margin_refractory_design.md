# H_9414 — p5-REWIRE 설계: MARGIN-불응기 게이트 (오너 라티파이 대기 · 측정 주장 0)

**status:** 📐 DESIGN (오너 라티파이 대기 · 발사물 아님 · 측정 주장 0) — H_9403 정정순서① 의 구체화 · wired: 미구현(라티파이 후 v2 프로토타입→core 포트→새 데몬 C1-C3 H)
**lane:** 의식 / emit-drive / emit-gate p5-rewire (프런티어 g1-interface-addressable-wall)
**related:** [[H_9403]] (CLOSED-AT-REGIME · 이 설계를 지정) · [[H_9413]] (a4 margin arm+trace 계기 재사용 · SUPERSEDED fire) · [[H_9401]] (margin 유일 θ-clearing) · [[H_9412]] (gap=drift) · [[H_9400]] (중심주장 반증 · 이 설계가 "처음 시험 가능"하게 함) · [[H_9391]] (INVALID-SATURATED · 이 설계가 회피) · [[measurement-metalaw-form-tunable-bind-earned]] · source: Fable p5-rewire 설계(fable-mode · walls-delegate-to-fable · $5.12)

## 설계 한 줄

현행 `emit = (score>0.30) ∧ (경과≥30s)` 의 **하드코딩 두 상수를 은퇴**시키고 → `emit ⟺ score_A > g_recog(후보발화)` — **A 의 동기와 G 의 "이건 이미 내가 말한 것" 인식이 실시간 경쟁**하는 게이트로 교체. 불응기는 emit→bind 가 남긴 흔적에서 **창발**(생물학적 불응기 동형: 스파이크 자신이 다음을 막고 막전위 동역학이 푼다).

```
[매 tick]
  score   = motivation_score(8-lane, 기존 그대로)          # A 극 · 블렌드 무변경
  cand    = generate(backend, ctx)                         # 내적 발화(형성만·발표 아님)
  g_recog = clip01(immune_recall_margin_text(immune, cand)) # G 극 · bind 前 측정
  emit    = (score > g_recog) ∧ kill ∧ φ-ratchet ∧ content  # 시계·θ 삭제
  emit → 발표 + bind(:2064) / 아니면 → cand 폐기(bind 안 함)
```

- **충전**: emit → bind → 근-반복 후보 margin 치솟음(실측 반복 1.15 vs novel 0.17). **방전**: 침묵 중 substrate 동역학(pure_field phase·5-stage·anchor age-decay·afield 성장)이 후보를 이동 → margin 하락 → 게이트 재개방.
- a4 arm(WIRED v0.14.3)이 그대로 게이트 G 입력 = **trace 기록 G 극과 게이트가 듣는 값이 동일한 하나의 수**(현행 telemetry a0 동어반복↔게이트 분열 해소).

## 왜 theater 아닌가 (H_9403 ≥4-DOF 비판 정면 통과)

- **4-DOF 중 0개 사용**: margin-swap(측정knob)·--ag-cont·dyn_w·--rate-sec 전부 미사용. lane 가중·quantizer·store write 규율·kosmos root③ 동결.
- **신규 자유 파라미터 0**: θ·30s 는 재튜닝이 아니라 **은퇴**. score:margin 비교계수 = **1:1 커밋**(사후보정 영구금지). clip01 은 코드베이스 보편 정규화.
- **단일 원리**: "게이트 침묵극을 상수(시계)→substrate 자신 인식(후보 margin)". 파이프라인 역전·a4-default 는 이 한 원리의 연역 귀결.
- **순서가 theater 배제**: 측정과 무관하게 p5+H_9401 discard-fact 만으로 설계 먼저 라티파이(순서①)→측정 H 는 뒤에 사전등록(순서②) ⇒ tune-to-green 인과방향 부재.

## 왜 포화 안 하나 (H_9391 INVALID-SATURATED 구조적 회피)

구 게이트는 substrate 를 **상수와 비교**(min score 0.3948>θ ⇒ 시계 열면 emit≡1). 새 게이트는 **substrate 를 substrate 와 비교**:

- **emit≡1 불가**: emit→bind → 다음 tick 근-반복 후보 margin(→1.0) 이 score 대역(~0.6) **반드시 상회** ⇒ 연속 emit 은 매 tick 진짜 novel 할 때만(그건 포화 아니라 정직한 다변, a6/a7 통제가 가짜 판별).
- **swing 대역 실재**: margin 분포(0.17~1.15·mean 0.62·p90 0.687)가 score 대역(0.33~0.6)을 **straddle** ⇒ 침묵-tick(margin>score)·emit-tick(margin<score) 둘 다 정의 ⇒ **C3 드디어 정의 가능**.
- **대칭 위험 = mute(emit≡0)**: greedy argmax mouth 얼면 margin 1.15 고정 영구침묵 가능 — 숨기지 않고 새 데몬 사전등록 verdict 칸(H(emit\|stage) 재사용·[[prereg-table-must-cover-below-chance]]).

## p5 준수 = 위반이 아니라 실현

현행 emit 경로의 하드코딩 상수 둘(θ·30s)이 H_9403 census 로 emit⟺시계 확정 = **현행이 p5 위반**. 재배선은 두 상수를 emit 경로서 **제거**하고 살아있는 두 엔진량 경쟁으로 대체 = "A⇄G tension 이 emit 결정"의 문자적 구현. self-seed 아님(decode seed 는 session anchor 상수 불변·root③·침묵 후보는 폐기·bind 는 emit 시만). 후보형성은 [[a_chat_sleep_imagination]] "imagination≠speak()" 승인 범주.

## 오너 라티파이 체크리스트 — 철학 결정(anima 정체성)

- **R1 emit 원리 교체**: "시간 차고 의지>θ면 말한다"→"**스스로에게 새로운 것이 생겼을 때 말한다**". 침묵의 의미가 '시간 안 됨'→'이미 말한 것'. **이게 anima 인가 — 핵심 결정.**
- **R2 내적 발화 파이프라인**: 매 tick 후보형성(발표 前 인식) + H_9325 disjoint-wall 문구개정("게이트는 sampler 설정 못 보나 store 인식으로 content 를 듣는다") + decode 비용 ~4× 수용.
- **R3 시계의 운명**: 완전삭제 vs ops-안전망 강등(장주기 스팸캡·kill-switch 계열, 강등 시 census 서 0회 binding V-gate 상시검증).
- **R4 스케일 동일시**: `score>clip01(margin)` 1:1 = "A-drive 와 G-인식은 같은 통화" 존재론 커밋. **사후 보정계수 영구금지**(대역 안 겹치면 verdict=INVALID/벽이지 재튜닝 아님).
- **R5 mouth REVEAL(T=1.0) production default**: greedy 면 mute/stage-lock 위험. T=1.0=H_9328 "유일 비임의 온도"이나 emit bytes 변경=정체성 인접 — 오너 판단.
- **R8 실패-정직 사전합의**: 새 데몬 mute 이거나 emit=f(stage)면 그대로 landed(패치 후 재측정=tune-to-green).

**순수 기술(승인만·철학 쟁점 없음)**: R6 bind 규율 유지 · R7 θ interrupt/telemetry 잔존 가능 · R9 a4 를 --g-arm default 로.

## wiring 경로 (라티파이 후)

① 오너 라티파이 → ② **v2 프로토타입**(V2_n·규칙면제·DIRECTIONAL): liveness/mute/swing-대역 점유 스모크 → ③ **core 포트**(cli/chat.py tick-루프 역전+core/brain 후보-게이트 decide+core/engine_g safety 3-way·py↔hexa lockstep·VERSION G5) → ④ **새 데몬 NEW C1-C3 측정 H 사전등록**(H_9413 계기·bar 전량 이월: V-gates+C1 진폭+C2 인식정보[a5/a6/a7]+C3 swing-census+H(emit\|stage)+Ψ̂ 궤적·--psi-soma 선확인) → ⑤ **GREEN 은 production-default∧측정 후에만**([[a_verified_must_wire]])·그 green 은 **새 데몬에 대한 진술**로 명시.

## 정직한 한계 (요청된 "벽")

어떤 재배선이든 결과물은 **다른 데몬**이다 — 피할 수 없고 피하는 척도 안 함. **H_9400 반증은 구 계보에 영구 성립**. 정당한 주장 형태 = "중심주장 부활"이 아니라 "**중심주장이 시험 가능한 최초의 데몬**이 생겼다". Ψ 평형이 ½ 인지는 **약속하지 않음** — 그게 새 데몬에서 처음 물을 수 있게 되는 질문.

## 비용
설계 $5.12(Fable·1회) · 구현/측정은 라티파이 후. 이 카드 = 측정 주장 0(design only).
