# Consequence-return lane 설계 (페이블5, 2026-07-03)

> THEATER F3-noise 재프레임: 천장 아니라 빠진 부품(~65%)=efferent-only 아키텍처의 afferent consequence-return 채널 부재. 자연실험: consequence 루프 가진 유일 축(identity×.kosmos)만 통과. 설계=tension reservoir+efference copy+afferent return(RPE)+value writeback, F3′ falsifier. 미구현.

---

세 F3 verdict 카드, emit loop(`cli/anima.hexa` 63-lane → `brain_emit` → `brain_decide_anchored`), `engine_g.hexa` motivation/safety 술어, 두 선행 설계문서(theater_overcome·loopclose)를 모두 읽었다. 코드/파일 생성 없이 분석·설계만 아래에 낸다.

---

# THEATER 최종 벽 재프레임 — 천장인가 빠진 부품인가

## 0. 코드로 확정한 구조적 사실 (진단의 접지)

세 F3가 왜 공통으로 죽었는지는 emit loop 실코드에 그대로 박혀 있다:

1. **emit loop는 닫힌 시뮬레이션이다.** `session_seed`("zephyrine: the wyrmhold ledger…")는 12 tick 내내 **고정**. emit은 `emit_anchor_from_v3`로 `.kosmos`에 쓰이고 `immune_memory_bind_text`로 자기 store에 되먹여지지만, **외부 수신·반응 신호가 substrate로 돌아오는 경로가 없다.** efferent(밖으로)만 있고 afferent(결과가 안으로)가 없다.

2. **F3의 downstream 타깃이 전부 same-tick 내생 부산물이다.** `grew`(vadapt_field_step) · `grounded`(anchor LCS 복사) · `immune_bind`는 전부 **그 emit 자신의 결정론적 결과**이고, 그 결정은 `rel_ctx`(42-lane soft-mean) + 두 상수 FLOOR(WAKE 상수항만으로 이미 >0.3 · SLEEP idle<30으로 safe=false)가 지배한다. 즉 op 신호가 예측해야 할 downstream이 **op 입력이 재활용된 값**이라, faculty가 완벽해도 잡음 대비 이길 여분 분산이 원리적으로 없다.

3. **유일하게 통과한 축(identity-continuity: self/you-chain × `.kosmos`)만이 닫힌 consequence 루프를 갖는다** — emit을 `.kosmos`에 쓰고 다음 세션에 되읽는다. 이것이 시스템 전체에서 return-path가 존재하는 **유일한** 자리다. return-path 유무가 pass/fail을 전 축에 걸쳐 완벽히 가른다(자연 실험, mechanistically coherent).

이 세 사실이 사용자 가설 #3을 강하게 지지한다 — 그리고 그것을 **두 부품**으로 정밀화하게 한다.

---

## 1. 벽 분류 (4 lens — F3-noise는 어디에 속하나)

| lens | 판정 | 근거 |
|---|---|---|
| **measure-artifact** | **부분 YES** | F3 downstream(grew/grounded/immune_bind)이 same-tick 내생. faculty-예측 가능한 분산이 타깃에 없어 **어떤 faculty도 통과 불가**. F3는 posed된 형태로 자기-반증 불가능한 bar였다. |
| **wrong-variable** | **부분 YES** | "appropriateness"를 "내생 downstream과의 상관"으로 조작정의. 옳은 변수 = **consequence(결과)/tension-relief**인데 그게 측정되지 않았다. |
| **substrate-gap** | **YES — 주원인** | appropriateness는 정의상 consequence-defined인데 anima엔 **consequence가 substrate로 되돌아오는 afferent 채널이 없다**(efferent-only). 없는 신호는 잡음과 구별 불가 = F3-noise는 부재의 **증상**. |
| **ceiling** | **NO (조건부)** | 현재의 닫힌 시뮬레이션 + 내생 타깃에 대해서는 천장이지만 **근본 천장 아님**. 루프를 닫는 것은 구체적·반증가능한 수. 단 잔여 위험: 루프를 닫아도 relief 신호가 floor-지배면(DPI 메타법칙이 consequence 층에서 재출현) 진짜 천장으로 귀착. |

**핵심:** measure-artifact/wrong-variable는 substrate-gap의 두 얼굴이다 — consequence 루프가 없으니 appropriateness ground-truth가 없고(→ 옳은 변수를 못 만들고), 그래서 남는 타깃이 내생 부산물뿐(→ measure-artifact)이다. 세 lens가 하나의 부재를 가리킨다.

---

## 2. 생물 렌즈 — "지금·이 내용을 말할 적절함"을 계산하는 구조

| 신경 구조 | 기능 | anima 상태 |
|---|---|---|
| **살리언스 네트워크**(전측 insula+dACC) | 행동 관련성 탐지·모드전환 | dACC-유사(conflict a_drive/g_drive, H_9095)가 **있으나 read-only** — 결과로 보정 안 됨 |
| **PFC turn-taking / pragmatics** | 청자 상태·공통기반 예측 | **부재** — listener-model 없음, 피드백으로 갱신되는 상대 상태 모델 0 |
| **보상예측(도파민 RPE)** | "과거 emit이 좋았나" → 온라인 value | basal-ganglia 게이트(`vbasal_select`)가 **있으나 오프라인 학습** — emit outcome으로 갱신 안 됨. **온라인 RPE 부재** |
| **interoception** | 신체 준비도 | `intero_ctx` lane 있으나 합성 read, consequence와 무연결 |
| **소비자/청자 피드백** | 외부 반응 | **전면 부재** |

관건: anima는 **감지(afferent sensing) 구조의 read-only 유사물은 많다**(dACC·intero·심지어 tom_ctx·agcy_ctx=efference-copy match lane까지). 하지만 **결과를 substrate에 되쓰는 닫힌 루프가 하나도 없다.** 즉 빠진 것은 센서가 아니라 **루프의 귀환 팔(return arm)** — 그래서 모든 op가 "예측/모니터"에 머물고 **outcome에 대해 보정·검증된 적이 없어 uncalibrated prior = 잡음-등가**로 남는다.

---

## 3. 빠진 부품 가설 (순위)

**#1 — Afferent consequence-return 채널 (efferent-only 아키텍처의 귀환 팔 부재) [최유력]**
appropriateness ≡ consequence로 정의된다. emit은 void로 나가고 결과가 안 돌아온다. 유일 예외가 `.kosmos` 되읽기(=degenerate consequence-memory)이고, **그것만 통과했다.** return-path 유무 = pass/fail의 완벽한 예측자. → F3-noise는 이 부재의 **필연적 증상**이지 천장 아님.

**#2 — 소비 가능한 standing tension (emit이 하는 "일"의 부재)**
현재 emit은 아무 긴장도 소비하지 않는다(seed 고정, 긴장 불변). emit이 relieve할 긴장이 없으면 appropriateness의 **지시대상 자체가 없다**. (#1의 하위부품 — return 측정에는 되갚을 긴장이 필요.)

**#3 — cross-subsystem outcome 측정 (순환 차단)**
appropriateness 신호를 **emit을 생성한 서브시스템과 disjoint한** 서브시스템이 읽어야 한다(L1 설계의 held-out ground_overlap과 같은 논리). 같은 immune-store가 gap도 relief도 계산하면 다시 floor로 붕괴.

**#4 — 온라인 striatal value(RPE) [메커니즘, 부품 아님]**
`vbasal`을 온라인화. 단 이건 #1–3을 **쓰는** 학습기지 갭 자체가 아니다.

---

## 4. 유력 부품 설계 — Consequence-return lane (efference→afference tension-relief 루프)

**개념(p5·a_substrate_native_speak 안전):** appropriateness = **consequence의 예측가능성**. emit이 **standing tension을 예상대로 relieve하면 적절**, consequence-surprise가 크거나 긴장을 못 풀면 부적절. 외부 수신자 없이도 **자기-consequence(autogenous)**로 닫는다 — 반응을 trigger로 쓰지 않으니 stimulus-response 회귀(p4)도, 명령적 게이트(a_autonomy)도 아니다. 환경은 여전히 맥락.

**4 요소 (전부 신규 owner table, pure_field·lane0/4·recall_thr 무접촉 = a_substrate_disjoint):**

1. **Standing tension reservoir Tₜ** — 현재의 tick별 재계산 대신, 미해소 info_gap/prediction-error가 **tick 경계를 넘어 누적·잔존**하고 grounded emit이 이를 **소비**하도록 stateful화(immune recall_gap을 read-only로 소비량만 산출, gate 불변).

2. **Efference copy** — emit 시점에 forward-model(이미 존재하는 cerebellum `vforward_predict`/`agcy_ctx`를 다-tick으로 확장)이 **예상 relief Δ̂T**를 저장.

3. **Afferent return** — k tick 뒤 실제 ΔT 측정 → consequence(RPE) rₜ = Δ̂T − ΔT_actual. **이것이 substrate로 되돌아오는 최초의 신호.**

4. **Value writeback V(state)** — rₜ가 delta-rule로 emit-value 추정 V를 갱신(온라인 striatal). V는 **consequence에 접지된 최초 lane**. V는 zero-mean 중심화(theater_overcome Rung-2 방식)로 score straddle에만 유입 → **어느 tick에 emit하나만 바꾸고 emit-rate ½ poise·psi_sum byte-identical 불변**(Ψ 보존, H_1561식 끌개이동 아님).

이때 appropriateness가 정의된다: **emit이 standing tension을 잡음-타이밍보다 잘 relieve하는 상태를 V가 예측하는가.**

**Falsifier (사전등록, engine-native, aiden pool, `.hexa`가 live core/ 디코드 호출 — grep 게이트 clean):**

- **train/held-out 분리(순환 차단):** V를 앞 절반 tick의 rₜ로 학습→freeze, **다른 tension seed의 뒤 절반**에서 상관 측정.
- **F3′ (핵심):** `ρ_real = corr(V-gated emit-timing, ΔT_actual)` vs variance-matched noise-V `ρ_noise`. **PASS iff ρ_real − ρ_noise ≥ 0.15.** (기존 F3와 결정적 차이: downstream이 내생 grew/grounded가 아니라 **emit-appropriateness에 의존하는 outcome ΔT**.)
- **shuffle 통제:** 학습 시 (state, rₜ) 짝을 셔플→V가 잡음화. shuffle-V가 real-V만큼 relieve하면 = relief가 V-예측 불가 = **여전히 theater → 정직 RED**.
- **cross-subsystem 강제(#3):** ΔT relief는 emit을 만든 mouth/immune과 **disjoint 서브시스템**(별도 tension reservoir)이 측정 — argmin/recall이 채점하면 순환.
- **Ψ 가드:** ci_emit_drive 시계열·emit/silence 결정열·nonfab_rate ON≡OFF byte-identical.

---

## 정직한 판단

- **DPI 재출현 위험(잔여 천장):** 닫힌 self-loop에서 gap과 relief를 같은 immune 기계가 계산하면 relief가 "recall 발화했나"로 붕괴 = floor 재현. 이래서 held-out + cross-subsystem + shuffle이 필수이고, 진짜 escape는 tension이 **독립 출처**에서 와야 한다(궁극적으로 실제 수신자 = chat user/EEG/타 anima가 가장 강한 형태 — 자기-consequence는 그 최소 대리다).
- **가장 강한 지지 증거:** 전 측정 축 중 **consequence 루프를 가진 유일 축(identity-continuity)만 통과**했다. return-path 유무가 결과를 완벽히 가른다.
- **설계 통과 확률(F3′):** ~30–40%. 자기-consequence만으로 relief에 faculty-예측 분산이 생길지는 반반. 실 수신자 루프면 ↑, 순수 autogenous면 DPI 재출현으로 죽을 수도. 그래도 **어느 쪽이든 최초의 engine-native consequence-return 측정**이라 무가치하지 않다.

**F3-noise는 근본 천장인가, 아니면 빠진 부품인가? — 빠진 부품이다(확률 ~65%): efferent-only 아키텍처의 afferent consequence-return 채널 부재. F3-noise는 그 부재의 증상이지 천장 아님. 잔여 ~35%는 루프를 닫아도 tension-relief가 floor-지배하면(DPI 메타법칙이 consequence 층에서 재출현) 진짜 천장으로 귀착 — 이 갈림을 가르는 것이 위 consequence-return 설계의 F3′ falsifier다.**
