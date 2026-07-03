# EEG-consequence-loop 설계 판정 (페이블5, 2026-07-03)

> 오너 질문 "EEG로는 안되나?" 답: EEG 원리적 exogenous ~85%지만 현 계측 ≥0.15 통과 ~25%(16ch SNR·A4 near-floor 재현). 현 EEG=afferent-only(닫힌 루프 아님·live 미구현). chat-user가 첫 exogenous 루프로 우월(高대역폭·오늘실행·자명 falsifier). 순서: chat-user로 원리 먼저 → EEG는 불수의 2차 채널.

---

충분한 증거를 확보했다. 세 EEG 파일 모두 동일 헤더(`ds005620 sub-1010 awake vs sedated`)의 **정적 녹화 데이터셋** 위에서 도는 toy이고, `BRAIN/EEG.md`는 실 OpenBCI live 경로가 아직 미구현(Mac에 헤드셋 없음)임을 확인해준다. 판정을 정리한다.

---

# EEG는 real-external-consequence 루프를 닫을 수 있나 — 설계 판정

## 확률 판정 (선요약)
- **EEG가 *원리적으로* exogenous consequence가 될 수 있나: 예 (~85%).** 인간 뇌 응답은 anima state에서 파생 불가능한 정보(인간의 사적 world-model)를 운반하므로, self-contained 4축을 죽인 DPI 동어반복(autogenous relabel)에 해당하지 **않는다**. 이건 identity×.kosmos가 통과한 것과 **구조적으로 같은 이유** — anima가 자가생성 못 하는 영역을 실제로 건넌다.
- **EEG가 *현 계측으로* ≥0.15 falsifier를 통과하나: 낮음 (~25%).** 병목은 원리가 아니라 **coupling 대역폭/SNR** — 정확히 A4를 near-floor(1/12)로 죽인 실패모드가 EEG에서 더 나쁘게 재현된다.
- **chat-user가 더 나은 첫 exogenous 루프인가: 예 (높은 확신).** 같은 원리적 escape인데 대역폭·잡음·falsifiability·실현성 전부 우월.

---

## 1. 수동 기록 vs 닫힌 consequence 루프 — 현 인프라는 **afferent-only**

현 EEG 스택은 **입력(구심성) 기록/탑재이지, emit→인간→EEG변화→복귀의 닫힌 원심-구심 루프가 아니다.** 코드가 이걸 명시적으로 증명한다:

| 파일 | 실제로 하는 일 | 루프 상태 |
|---|---|---|
| `h1247_state_discrim` | 녹화 ds005620 파일에서 awake vs sedated **분류** | afferent, 인과 없음 |
| `h1250_mount_emit` | 실 EEG를 A⇄G brain-context(motivation)로 **read-only 탑재** → emit propensity 구동(awake>sed). **Ψ byte-identical** | EEG=입력, emit이 EEG를 못 바꿈 |
| `h1256_closed_loop` | anima 내부 적분기 `y = y + k*(eeg_ctx − y)`가 **정적** EEG setpoint에 lock-on | **anima 내부에서만** 폐루프; 원심-구심 arc는 열림 |

즉 `h1256`의 "폐루프"는 **제어이론적 lock-on** — anima가 *고정된* 외부값을 추적한다. 인간은 루프 안에 없다(녹화 파일이다). **anima emit이 인간 EEG를 인과적으로 이동시킨 적이 한 번도 없다.** consequence(적절성)로 쓰려면 반드시 필요한 efference→afference 화살표가 통째로 부재.

게다가 `BRAIN/EEG.md`는 **실 OpenBCI live 경로조차 미완**임을 보여준다 — 모든 "real" 실행은 녹화 공개 데이터셋(ds005620)이거나 synth/replay. 헤드셋이 Mac에 없다. 닫힌 루프는커녕 live afferent도 아직 안 돌았다. (그리고 NES 가상뇌 경로 = "사람 없이" 시뮬 뇌 → 자극의 결정론적 함수 = **파생가능=INERT** = DPI 함정이라 이 목적엔 무효.)

## 2. 진짜 닫힌 루프 설계 — 정확한 seam (emit → EEG → 복귀)

```
t0  anima emit E  (brain_decide/generator, .kosmos anchor 위)
t1  인간이 E를 읽음/들음  ← onset을 t=0로 time-lock (ERP windowing 필수)
t2  인간 뇌 응답 (exogenous: E × 인간의 사적 priors/mood/attention)
      • 300–500ms  N400  = 의미부적합 (음성↑ = 덜 적절)  ← 최적 적절성 프록시
      • 250–400ms  P300  = surprise/salience
      • 1–4s 지속  frontal-midline θ↑ + α-desync = engagement
t3  스칼라 적절성  a = f(EEG window)   예: a = −N400amp  또는 engagement band-power
t4  복귀 RPE = a − a_expected  (a_expected = anima 사전 예측 = efference copy)
      → **disjoint 레인**에 배선 (emit-drive lane 0/4·§ImmuneMemory recall_thr 절대 아님, a_substrate_disjoint)
      → basal-ganglia go/no-go(R7)의 learned-precision/value 변조. emit *내용* 직접 아님.
```

**consequence가 REAL인 이유:** `a`는 인간의 사적 world-model에 의존(exogenous) → `RPE`가 anima의 emit-시점 자기 state의 어떤 함수로도 표현 불가. 이게 4 자가축(self-relief=state 동어반복)과 갈리는 지점.

**A4 near-floor(DPI 재현)을 피할 coupling 대역폭 조건:**
- 단일 스칼라 band-power/Φ를 16ch@123Hz 잡음바닥 위에서 뽑으면 A4처럼 near-floor. single-trial N400은 ~1–2µV vs 잡음 ~10–50µV → 파묻힌다.
- **탈출 조건 = 차분(contrast) 구조:** 매 real emit을 scrambled/off-topic control emit과 **쌍**으로 제시, EEG *차이*(within-subject, 같은 block)를 측정. 차분 N400은 절대 N400보다 훨씬 robust. 이게 falsifier이자 신호추출을 겸함.
- 또는 single-trial 살아남는 sustained 측정(θ/α engagement, 수 초)만 쓰되 real-time RPE 해상도는 포기.

## 3. Falsifier (사전등록·frozen-first)

- **H:** EEG 적절성 신호 `a`가 anima emit 적절성을 surrogate EEG보다 잘 예측.
- **설계:** N개 적절 emit vs N개 의도적 부적절(word-salad/off-topic) emit, time-locked. 각각 `a` 측정.
- **대조 3중:** (1) real EEG → `D_real = mean_diff/pooled_sd`; (2) **phase-shuffle surrogate**(a_eeg 이미 보유) → `D_surr`; (3) **autogenous baseline**(인간 없이 anima 자기예측 `a_expected`만) → A4식 self-pair 통제, floor여야 함.
- **PASS 🟢 iff `D_real − D_surr ≥ 0.15` ∧ `autogenous < 0.05`.** 아니면 🔴 floor = EEG는 진짜 exogenous faculty 아님 → 4 자가축에 합류.
- **정직한 prior: ~25% PASS.** A4의 near-floor coupling이 EEG SNR에서 더 나쁘게 재현.

## 4. EEG vs chat-user — 정직 비교 (둘 다 exogenous receiver)

| 축 | **chat-user 텍스트** | **EEG** |
|---|---|---|
| 대역폭 | 高 (한 문장 = 수십 bit, 적절성 명시 인코딩) | 低 (µV 스칼라) |
| 잡음 | 低 | 高 (single-trial ERP 파묻힘) |
| 지연 | 초 단위 | 유사하나 신호 약함 |
| falsifiability | 자명 ("말이 안 됨" vs "정확해") | 차분설계 필요, 취약 |
| 실현성 | **오늘 실행 가능** (임의 chat 세션) | live OpenBCI 미구현 + 세션마다 배선된 인간 필요 |
| exogenous 내용 | 인간의 **평가적 판단** | 인간의 **불수의적/전언어적** 뇌상태 |

**chat-user가 결정적으로 우월:** 같은 원리적 escape(exogenous 인간 판단, anima state서 파생불가)인데 대역폭·잡음·falsifiability·실현성 전부 이긴다. EEG가 유일하게 더 나은 단 하나 = **불수의/전언어** — 사용자가 *말로 안 하는/못 하는* 적절성(잠재적 surprise, 타이핑 안 할 engagement)을 잡는다. 실재하지만 좁은 edge.

**따라서 올바른 순서:** exogenous-consequence *원리*를 **chat-user로 먼저** 증명(高 SNR·저비용·자명한 falsifier). chat-user가 floor면 EEG는 확실히 floor(더 나쁜 SNR). chat-user가 ≥0.15 넘으면 그때 EEG가 *불수의 채널*로서 의미를 가진다.

## 5. 치명적 한계 (원리적으론 되는데 실무적으로 막힘)

- **16ch@123Hz 천장(a_eeg):** single-trial N400이 잡음 위로 겨우 나옴 → 차분/평균 없이는 near-floor.
- **live-human 의존:** 닫힌 루프가 emit마다 배선된 인간을 요구 → anima가 혼자 못 돌린다. 세션 밖 의존이고 `a_substrate_native_speak`의 자율성을 깨뜨린다(emit이 인간 센서를 기다림). **exogenous지만 비자율** 루프.
- **평균화↔실시간 모순:** real-time RPE는 single-trial을 원하고 SNR은 평균화를 원함 — consequence 입도에서 화해 불가.
- **인프라 부재:** live OpenBCI 경로가 아직 안 지어짐(월 단위 하드웨어/계측). chat-user는 오늘 falsifier 실행 가능.

---

**한 줄 판정:** EEG는 *원리적으로* DPI 천장을 깰 수 있는 진짜 exogenous 루프다(인간 뇌 응답은 파생불가) — 하지만 현 16ch 계측에선 A4 near-floor가 재현될 공산이 커(~25%) 첫 exogenous faculty로는 약하고, **chat-user 텍스트 반응이 같은 원리를 高대역폭·低잡음·오늘-실행-가능으로 먼저 증명할 더 나은 첫 루프다 — chat-user로 exogenous-consequence 원리를 세운 뒤, EEG는 사용자가 말 안 하는 불수의 적절성을 잡는 2차 채널로 붙이는 순서가 맞다.**
