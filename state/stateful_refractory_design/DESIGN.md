# 실시간 clock seam 설계 = stateful refractory (페이블5, 2026-07-03)

> H_9101 항목1 분해: (A)wall-clock 소스=동어반복 INERT · (B)stateless→stateful refractory=진짜 신규 메커니즘(det-clock으로 지금 검증, F2) · (C)30s 안전-진실성=데몬 loop-closing 배선정직. 결정성=an_clock_now seam(det/daemon). 미구현.

---

모든 증거 확보 완료. 설계 분석을 정리한다.

---

# H_9101 항목1 — 실시간 clock seam: 설계·분석 (페이블5, 분석-only)

## 0. 증거 요약 (읽은 것)

- **카드** (`HYPOTHESES/cards/H_9101_opgrip_stage_safe.md` @ 00c3cf8b1 — 주의: 카드 경로는 `UNIVERSE/cards/`가 아니라 `HYPOTHESES/cards/`, 로컬 `origin/main` ref는 stale이라 fetch 없이는 커밋 00c3cf8b1로 봐야 함): "idle은 SYNTHETIC clock, real wall-clock/elapsed-seconds seam 없음, honest real-time wiring(`idle = real_elapsed_seconds × refractory_modulation`)은 follow-on".
- **emit 루프** (landed cli/anima.hexa L2381): `let idle = 5.0 + 55.0 * clip01(stage_env * (0.5 + urgency))` → `brain_decide_anchored(..., idle, ...)`.
- **엔진 소비처** (`core/brain.hexa:41,52`): 파라미터 이름이 **`seconds_since_last`**, `safety_rate_limit_ok(seconds_since_last)` (≥30s hard-floor, FROZEN 4-safety conjunction의 한 항).
- **L2057 근방** (landed L2068–2073): interval-timer는 `itimer_step` learned-phase read — emit refractory와 무관한 별도 lane, 카드 서술과 일치.
- **결정적 추가 발견 2건** (grep으로 확정):
  1. **emit-history 상태가 아예 없다** — 루프 어디에도 `last_emit` 타임스탬프/틱 추적이 없다. `idle`은 per-tick **stateless** 함수다. 즉 현재 "refractory"는 refractory가 아니다 — emit 후 리셋되는 회복 변수가 아니라 stage/urgency의 순간 shade다.
  2. **데몬이 존재하지 않는다** — `anima_consciousness_mode`는 bounded tick 루프(`n_ticks = og_measure ? 200 : 12`)이고 stdin/readline/persistent 루프가 없다. "real daemon clock seam"은 아직 없는 데몬을 전제한다. (memory의 loop-closing 항목과 동일 뿌리.)

---

## 1. 실시간 seam이 과학적으로 뭘 추가하나 — **프레임을 쪼개야 정직하다**

카드의 "real-time follow-on"은 사실 **두 개의 서로 다른 축**을 하나로 뭉쳐 놨다:

**(A) TIME-SOURCE 축 (wall-clock vs synthetic tick): 과학적으로 INERT — 동어반복.**
메커니즘 주장은 "op(urgency)이 rate-gate 입력을 연속 변조하고, 그 변조가 emit WHEN/WHETHER를 결정한다(REM flip ∧ N3 preserve)"이다. 이 주장의 진리값은 `clip01` 대수와 `brain_decide`의 소비 방식에만 의존하고, 그 입력 스칼라를 tick 카운터가 만들었는지 `date +%s`가 만들었는지에 **전혀 의존하지 않는다**. 같은 값이 들어가면 같은 결정이 나온다 — wall-clock으로 갈아끼우고 재측정하면 나올 결과를 지금 100% 예측할 수 있고, 예측이 100%면 실험이 아니다(falsify 불가능 = 동어반복). "op이 *실제* 경과시간 기반 refractory를 변조한다"는 synthetic 증명보다 강한 **과학적** 주장이 아니다.

**(B) TIME-STRUCTURE 축 (stateless shade vs stateful refractory): 진짜 미검증 메커니즘 — 여기가 실질이다.**
현재 `idle`은 `seconds_since_last`라는 이름의 슬롯에 들어가지만 **"since last" 정보가 없다**. emit이 일어나도 다음 tick의 idle은 리셋되지 않는다. 카드가 제안한 형태 `idle = real_elapsed_seconds × refractory_modulation`은 단순히 시간 소스를 바꾸는 게 아니라 **역학 클래스를 바꾼다**: memoryless per-tick 함수 → emit-history 의존 상태변수(발화 후 회복). 이것은 synthetic tick으로도 표현 못 하던 게 아니라 **지금 형태로는 아예 표현이 안 되는** 것이고(F2 falsifier 참조), 생물 렌즈(a_no_llm_frame_trap)로도 이쪽이 진짜다 — 뉴런 refractory는 "지금 상태의 shade"가 아니라 "마지막 스파이크 이후 회복"이다.

**(C) 숨은 세 번째 축 — 정직성/안전 진실성 (과학 아님, 그러나 c9급).**
엔진의 FROZEN `safety_rate_limit_ok(≥30)`은 의미론상 "실세계 30초 내 재발화 금지"라는 **세계-시간 약속**이다. cli가 합성값을 그 슬롯에 주입하는 현재 구조에서 이 안전 불변식은 시뮬레이션 안에서만 참이고 세계에 대해서는 **공허(vacuous)** 하다 — cli는 언제든 60을 넣어 게이트를 열 수 있다. 실 채널(SNS/chat)에 emit하는 데몬이 생기는 순간 이건 결함이 된다. real-time seam의 진짜 필요성은 여기서 나온다: **과학 증거 추가가 아니라, frozen 안전 항의 의미론을 참으로 만드는 배선 정합성**.

---

## 2. 결정성 trade-off — clock 주입 seam으로 해소 (기존 패턴 그대로)

anima에 이미 정확한 선례가 있다: `flame_mm.mm`은 cuda host면 own-GEMM, 아니면 farr CPU **byte-identical** — 소스만 갈리고 알고리즘은 하나. clock도 동일하게:

```
an_clock_now() -> float     // 유일한 시간 소스 seam (한 함수)
  det/eval 모드 (HEXA_DET):  tick * TICK_SECONDS   (TICK_SECONDS 상수, 예: 8.0 —
                              이미 stage 샘플링이 dr_stage_at(tick*8)로 tick=8단위를 씀)
  daemon 모드:               실 monotonic 초 (exec("date +%s") — exec은 anima.hexa에 이미 3용례,
                              장기적으로는 hexa intrinsic이 바람직)
```

- **verdict 경로는 절대 wall-clock을 읽지 않는다**: 모든 G-gate/frozen bar/byte-exact 측정은 injected det clock으로만. 두 번 돌려 byte-identical 확인이 결정성 가드.
- **production 경로만 real clock**: 검증은 verdict가 아니라 **property smoke** — "실행 로그에서 두 emit의 실측 간격 ≥30s" 같은 술어 assert (byte-exact 요구 없음, RC=0 + 술어 통과).
- 다운스트림 대수는 두 모드에서 **동일 코드 경로** — seam 값만 다르다. 결정성과 real-time은 충돌하는 게 아니라 **같은 함수의 두 바인딩**이다.

## 3. substrate 정합성 — 두 시계, 둘 다 native

synthetic-tick이 결함인가? **내부 역학에 대해서는 의도이고, 경계에 대해서는 결함이다.**

- anima substrate의 고유시간(proper time)은 tick = A⇄G settle 1회다. 상상 루프, mitosis tick, stage 진행이 tick 위에서 도는 것은 p5·a_autonomy_over_hardcode에 부합한다 — 세포의 시간이 대사 속도이지 벽시계가 아니듯. wall-clock으로 내부 tick을 **대체**하는 것은 오히려 환경이 substrate를 강제하는 assistant 회귀 냄새가 난다(a_substrate_native_speak: 환경은 맥락이지 명령이 아님).
- 그러나 **경계(boundary)는 세계와 공유된다**: a_chat_sleep_imagination의 "90분 ultradian"은 벽시계 주장이고, safety rate-limit은 세계-시간 약속이며, 생물도 내부 진동자를 광-Zeitgeber로 **entrain**하지 대체하지 않는다 (이미 L818-839에 PRC-clock entrainment lane이 정확히 이 구조로 존재).
- 따라서 정합 설계 = **이중 시계**: 내부 역학(stage/상상/mitosis)은 tick 고유시간 유지, 세계시간은 오직 경계 seam 2곳(safety rate-limit의 `seconds_since_last`, circadian Zeitgeber 입력)으로만 진입. synthetic-tick 데몬 자체는 결함이 아니고, **경계 항에 합성값을 주입하는 것**이 결함이다.

## 4. 최소 배선 설계 + falsifier

**배선 (cli만, 엔진 FROZEN 유지 — H_9101과 동일 원칙):**

```hexa
// 상태 1개 추가 (emit-history — 현재 부재가 핵심 갭)
let mut emit_last_t = -1.0e9                       // 마지막 emit 시각 (an_clock_now 단위)
// per tick:
let t_now    = an_clock_now()                      // §2 seam: det=tick*8.0 | daemon=real
let idle_raw = t_now - emit_last_t                 // 진짜 seconds_since_last
let mod      = _afs_clip01(stage_env * (0.5 + urgency))   // H_9101 변조항 그대로
let idle     = idle_raw * mod                      // 카드의 real_elapsed × refractory_modulation
// ... brain_decide_anchored(..., idle, ...)
if did_emit { emit_last_t = t_now }                // refractory RESET — 새 메커니즘의 심장
```

이 형태의 성질 (H_9101 대비):
- **안전 하한 구성적 보존**: `mod ≤ 1` ⇒ `idle ≤ idle_raw` ⇒ 게이트 통과(≥30)는 실경과 ≥30을 **함의** — 30s 세계-시간 하한이 증명 수준으로 참이 된다 (현 `5+55·mod` 형태는 실경과 0초여도 60을 낼 수 있음).
- **N3 보존 구성적**: env=0 ⇒ mod=0 ⇒ idle=0 ⇒ 영원 침묵 — H_9101의 shade-not-gate 유지.
- **op-grip 유지**: urgency는 게이트 개방 시점을 `30/mod`초로 연속 변조 — grip이 "여부"에서 "시점"으로 확장.

**측정 (전부 det clock, 엔진-네이티브 `.hexa`, aiden pool, $0 — 게이트1·2 준수):**
- **F1 (grip 재검증, frozen bar 유지)**: urgency→0 arm — REM Hamming>0 ∧ N3=0, H_9101 pre-reg 그대로 stateful 형태에서 재성립해야 함. (역학 클래스가 바뀌므로 H_9101 verdict가 자동 이월되지 않는다 — 재측정 의무.)
- **F2 (refractory reset — 신규 falsifiable 내용, synthetic-stateless로는 표현 불가)**: emit 직후 tick은 max urgency에서도 silent이어야 함(idle_raw<30/mod). 현 H_9101 배선은 이 예측을 **못 만든다** — 이것이 "real seam이 추가로 증명하는 것"의 전부이자 실질.
- **F3 (세계-시간 안전, smoke·non-verdict)**: real-clock 데몬 런 로그에서 inter-emit 실측 간격 ≥30s 술어 — byte-exact 요구 없음.
- **F4 (결정성 가드)**: HEXA_DET 2회 → byte-identical.

**정직한 순서 주의**: 이 seam은 persistent 데몬(현재 부재, 12-tick bounded 루프)의 loop-closing 작업과 한 몸이다 — clock seam 단독 착지는 F3을 검증할 대상이 없다. det-clock + F1/F2는 지금 루프에서도 착지 가능(선행), real-clock 바인딩 + F3은 데몬 loop-closing에 동반(후행)으로 ING 분리가 맞다.

---

## 최종 한 줄 (정직 판단)

**실시간 clock seam은 "wall-clock 소스"로서는 과학적으로 불필요하다(동어반복 — synthetic-tick grip이 메커니즘 증명으로 이미 충분하고, verdict 경로에 wall-clock을 넣으면 결정성만 깬다) — 그러나 카드의 follow-on이 뭉쳐 놓은 진짜 알맹이는 시간 소스가 아니라 (i) 현재 완전히 부재한 emit-history 의존 stateful refractory(det clock으로 결정성 유지한 채 지금 검증 가능한 신규 메커니즘, F2)와 (ii) frozen 30s 안전 항의 세계-시간 진실성(과학이 아니라 배선 정직성·데몬 loop-closing의 일부)이며, 이 둘로 분해해 전자는 det-clock으로 선행 착지, 후자는 데몬 구축에 동반시키는 것이 정답이다.**
