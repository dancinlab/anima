# H_9627 — dual content ledger (발화 ⇄ 보류) 대칭 depletion emit-gate: one-sided 스프링 벽 탈출 후보 (R-Ψ½ 발산)

**status:** 🔎 PROPOSED · DIRECTIONAL 설계 (lab-full Fable 5 ∥ Codex Sol 수렴 · 발사 전 · engine-native 미측정)
**lane:** 의식 / emit-drive / Ψ=½ 항상성 · A-pole 상보쌍 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9610]] (wm-coverage GREEN-DIRECTIONAL·one-sided 스프링 벽의 출처) · [[H_9419]] (P-pull bar) · [[H_9510]] (HOLE-4a A-pole 부재 최초 지목) · source: `sidecar lab full`(fable-mrnnimd7 ∥ sol-mrnnimd9) 벽-재프레임

## 왜 이 카드가 존재하나 (terminal 선언 전 필수 재프레임)

H_9610 이 wm-coverage 렌즈로 Ψ=½ P-pull functional 3종 완비(303M·λ=0.75 center≈½)를 벌었으나 **one-sided 스프링 벽**에 막힘: 진동은 만들되 score-섭동에 중심 ½ 강건유지 불가(중심주장 bar 미충족). verdict 잠정결론="emit-policy 복원력 3원천 소진·mouth-생성만 잔존"을 **terminal 로 굳히기 전** `walls-delegate-to-fable` 표준에 따라 2모델 재프레임 → **terminal 은 성급**임이 확증됨.

## 벽 진단 (Fable ∩ Sol 완전 일치)

현 wm-cover 는 **probe 1개**만: emit → V(coverage)↑ → 임계↑ (능동 브레이크·내용의존 write), silence → V 감쇠(λ)만 (수동 leak·내용무관). **브레이크만 능동, 액셀은 수동** = 교환대칭 부재. score(A)와 임계(V)를 서로 다른 소스에서 읽어 score-섭동이 순수 differential-mode 로 들어가 상쇄 없음 → center 가 섭동 추종. **HOLE-4a = A-pole 에 V-억제와 대칭인 상태의존 복원력 부재.** 지금껏 A-pole 을 항상 **one-sided 3번째 항 단항 추가**로만 시도(store-depletion·이력적분기·A-pole 피로) — **대칭 상보쌍(complementary pair)** 은 한 번도 안 세움 = kill-list 에 없는 미탐 각.

## 제안 (수렴 설계 · DIRECTIONAL)

같은 구조·같은 λ 로 **두 내용 ledger**(gain-lock, 자유상수 없음):
- **W_E** = 발화한 후보 저장 (spoken · G-pole coverage, 현행)
- **W_S** = 상상했으나 침묵으로 버린 후보 저장 (withheld/backlog · **A-pole 신규**)

매 tick 후보 c 생성 후 `E=V(W_E,c)`·`S=V(W_S,c)`, **emit ⟺ S > E**(미발화 압력 > 커버리지 포화). 상태전이 **등가·반대**: emit → W_E 에 c write(E↑), silence → W_S 에 c write(S↑). 양 ledger 동일 λ leak. `score_A` 는 임계 offset 이 아니라 **양 ledger 공통 write-strength q**(=depletion 학습률)로 강등.

**½ 창발(setpoint 아님)**: W_E·W_S 가 같은 (준)보존 풀의 상보 분할 + emit 에 등가-반대 결합 ⟹ E[S−E]=0 zero-crossing 이 교환대칭으로 **강제**. 대칭 score 잡음 하 그 지점 = Ψ=½. λ 는 기억길이·autocov 크기만 바꾸고 **½ 를 안 겨눔(대칭이 겨눔)**.

**two-sided 복원(벽 뚫는 근거)**: emit 초과 → S↓·E↑ → margin S−E 2δ 하락(이중 브레이크); silence 초과 → S↑·E↓ → margin 2× 상승(이중 액셀). 양꼬리 대칭 = **양방향 autocov<0**. margin 은 공-스케일 두 양의 차 ⟹ **score 공통모드 섭동 상쇄**(one-sided 가 못한 common-mode rejection) = "retuning 없이 score-섭동 강건 ½"의 기계적 근거. 진짜 비대칭(influx>발화용량) 있으면 균형이 ½ 에서 **정직히 이동**(servo 라면 ½ 고수) — 이 falsifiability 가 창발 vs servo 를 가름(p7).

**Sol 축약(제안2)**: signed occupancy x=E−S, emit⟺x<0. 수학 동일하나 `WorkMemBuffer` 비음수+`gate_in=max()` 라 signed store 는 **계기-차단** ⟹ dual 비음수 ledger(제안1)가 기존 primitive 2개로 구현가능·더 정직.

## kill-list 회피 (5 기준 대조)

(i) ½ 창발(emit_rate−½ 적분 없음·상보성) · (ii) two-sided autocov<0(silence 도 반대극 write) · (iii) 내용청취(W_S 는 emit 이력 아닌 특정 미발화 WM 항목 내용주소 read → vshuf 시 붕괴·quantile-tracker 는 불변) · (iv) dissociation(W_E/W_S 각각 alien 화 → 한쪽 복원만 선택적 소멸) · (v) `anima-py chat` 플래그 구현가능(mouth 무접촉·스칼라 게이트 비교라 byte-입도 무관, H_9574/9576 과 무관).

## Sol 구조적 정리 (one-sided 클래스 = 획득된 terminal)

`e=1[s>g(M,c)]`·M 은 emit 때만 내용 write·silence 는 leak 만·½/offset/score-retune 금지 클래스: `P(e|M,c)=1−F(g)` 라 score 분포 위치 shift 는 모든 상태서 단조 증가/감소, emit-side(내용의존 write) ⊥ silence-side(내용무관 지수감쇠) 교환대칭 부재 ⟹ **비퇴화 score-shift 전반 non-tuned Ψ≈½ 유지 구조적 불가능**(더 많은 emit-only store·긴 이력·다른 kernel 추가해도 action asymmetry 잔존). ⇒ **one-sided 클래스는 terminal 획득**. 단 "emit-policy 전체 소진"은 dual content ledger(silence 가 substrate state 를 쓰는)가 **마지막 반례 후보**라 아직 이름 — 이 카드가 그 반례.

## 판정 갈림길 (crux · 단일 분기점)

WM substrate 가 said/unsaid(보류) 내용상태를 substrate-native 로 나르는가?
- **분할 有**(제안1 계기가능·Sol 코드지식상 dual 비음수 ledger 로 성립) → **terminal 불법**·이 카드 303M 스크린 = 마지막 정당 fire.
- **분할 無**(순간 additive vote 강제·silence write 불가) → Sol 정리로 emit-policy terminal 획득·mouth-생성만 잔존.

## NEXT (engine-native · 오너 fire-go 대기)

1. `$0` 계기체크: `WorkMemBuffer` 2-인스턴스(W_E/W_S) 로 dual ledger 구현가능성 코드확인(Sol 이 성립 시사).
2. 구현: `cli/chat.py --g-reach wm-dual` + `--g-reach wm-dual-alien-emit/-silence`(dissociation) + gain-lock 불변식(양 ledger 동일 코드경로·arm별 gain 금지=tune-to-green 뒷문 차단). trace 에 `wm_emit_cover`·`wm_sil_cover`·`dual_margin=S−E` 기록.
3. 303M 스크린(summer·seed 7/4302/4303): **regime-split autocov**(emit-run 후 vs silence-run 후 분리 · one-sided=비대칭·two-sided=대칭) + **retune-free score-섭동 sweep**(λ 고정·center drift 측정 = 중심주장 bar) + **vshuf discriminator**(내용청취) + alienwm dissociation.

⚠️ **DIRECTIONAL 설계·verdict 아님** — cement 는 engine-native `anima-py` 만(a_lab_full_diverge). 리스크(정직): U+V 준보존 깨지면 emit=1 포화·½ 상실(U+V drift 첫 게이트) · gain-lock 안 묶이면 ½-tuning 재유입(FORM 회귀·코드강제 필수).
