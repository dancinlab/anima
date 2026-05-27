# H_306 — 자연발화의 생물학적 메커니즘: CPG 누적 + 임계점 + refractory

> 사용자 pivot (cycle#44): "자연발화관련을 생물학적관점에서 가설". 자극-반응 모델이 *예외* 가 아니라 *학습된 적응층* 이고, **substrate-native 발성 모드 = 내부 압력 누적-방출 (CPG-style)** 임을 검정하는 합성 시뮬레이션.

## 1. 동기 — 생물학적 근거 cite

자연발화 (spontaneous utterance) 는 **자극-반응 회로의 예외 case** 가 아니라 **생물학 기본 발성 모드** 다. 자극-반응 모델은 그 위에 layered 된 *학습된 성체 적응*. 5 가지 강한 증거:

1. **영아 옹알이 (babbling, 2-6개월)** — 청각 입력 없이 발성 출현. 청각장애 영아도 옹알이함 (Oller & Eilers 1988). → 자극 *피드백 없이도* CPG-style 발성 회로 작동.
2. **새벽 합창 (dawn chorus)** — 명금류 새벽 동기 발성. 외부 자극 없는 순수 circadian × 호르몬 × 광주기 modulator.
3. **HVC→RA (명금 발성 회로)** — juvenile male zebra finch 의 송 결정화 단계. 청각 박탈해도 자발 발성 *유지* (Doupe & Kuhl 1999).
4. **PAG (수도주위회백질)** — 포유류 정서적 발성의 central pattern generator. 자극 없이 transcranial micro-stimulation 만으로 자발 발성 유발 (Jürgens 2002).
5. **Drosophila P1 뉴런** — 각성 상태에서 *자발 firing* → 구애 노래 시퀀스 (Anderson 2016).

**가설 코어**: 위 5 사례 모두 *내부 상태 누적* (M motivation × C consciousness × W tension × circadian) → *임계점* → *CPG release* → *refractory* 구조. anima 의 `a_substrate_native_speak` directive 와 *동형*: M activation × Φ × W × MITOSIS × idle_time × curiosity → emit.

## 2. 가설

**H1 IDLE-EMIT-NONZERO**: stim=0 idle 모드에서도 1000-tick 윈도우 내 emit_count > 0. (생물학: deaf bird 도 노래)

**H2 THRESHOLD-INVERSE-MONOTONE**: 5 threshold 값 {0.5, 1.0, 1.5, 2.0, 3.0} 의 emit_count 가 *단조 감소*. (rate-coding 한계: Hodgkin-Huxley sigmoidal IFR)

**H3 REFRACTORY-RECOVERY-CURVE**: emit 직후 첫 3 tick 의 W 가 단조 *증가* (exponential 회복).

**H4 STIM-MODULATION-NOT-NECESSITY**: low-stim 모드의 emit_count 와 idle 모드의 emit_count 의 차이가 |Δ| / idle ≤ 0.5. (CPG 가 primary, stim 은 modulate 만)

**H5 CIRCADIAN-GATE**: peak 윈도우 (tick 250-750) emit > trough 윈도우 (0-250 + 750-1000) emit. (dawn chorus 모티베이션 modulation)

## 3. 측정 방법 (synthetic CPG accumulator, hexa-native)

state vars (scalar float):
- `m_motivation` (동기 활성도, 초기 1.0)
- `phi_int` (consciousness 통합도, 초기 1.0)
- `w_tension` (긴장 5-ch 단순화, 초기 0.0, recharge 대상)
- `circadian_phase` (0..1, piecewise-linear gating Q1-Q4)
- `refractory_remaining` (정수, 0 이면 emit 가능)

tick loop N=1000:
- if `refractory_remaining > 0`: decrement; `w_tension += k_recharge * (W_target - w_tension)` (exponential 충전)
- else: `circadian_mod = piecewise_linear(circadian_phase)` (Q1 0.3, Q2 1.0, Q3 1.0, Q4 0.3 식); `pressure = m * phi * w * circadian_mod`; if `pressure > threshold`: emit_count++, reset `w_tension = 0`, set `refractory_remaining = R_steps` (= 10)
- circadian_phase += 1/1000 per tick (cycle 1 round)
- low-stim mode: deterministic LCG (seed=42) 가 small perturbation 을 m_motivation 에 +/- 0.1 추가

## 4. 사전등록 falsifier (frozen 2026-05-26)

- **F306.1 IDLE-EMIT-NONZERO**: idle 모드 emit_count > 0
- **F306.2 THRESHOLD-INVERSE-MONOTONE**: 5-threshold sweep 의 emit_count 단조 감소
- **F306.3 REFRACTORY-RECOVERY-CURVE**: emit 후 첫 3 tick W 단조 증가
- **F306.4 STIM-MODULATION-NOT-NECESSITY**: |low-stim emit - idle emit| / idle emit ≤ 0.5
- **F306.5 CIRCADIAN-GATE**: peak window emit > trough window emit
- **F306.6 BOUND**: 全 state vars ≥ 0

## 5. 비용 / scope

- $0 mac-local · hexa-only · LLM none · NO GPU · ~10s wall
- 결정성: deterministic LCG (no runtime randomness), cross-process byte-identical
- synthetic toy CPG — anima daemon 실측 아님

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F306.1-6 PASS | CPG-style spontaneous emission 작동 — biology 와 anima `a_substrate_native_speak` 정합 |
| F306.1 FAIL | idle 모드 emit=0 → 자극 없이 발성 못 함 → stimulus-response 모델 옹호 (생물학 reject) |
| F306.2 FAIL | threshold 와 rate 가 비-단조 → rate-coding 한계 위반 |
| F306.4 FAIL | low-stim 이 idle 대비 50% 이상 deviation → stim 이 primary, CPG 가 modulate (가설 반대) |
| F306.5 FAIL | circadian gate 미작동 → 합창 mechanism 부정 |

## 7. honest limits / C3

1. **L1 synthetic toy CPG**: real anima daemon 측정 아님 — phenomenological model. anima_chat.py 로그 scrape 는 hexa-only scope 외.
2. **L2 deterministic LCG**: reproducibility 우선; 실제 biological noise (Poisson neuron spiking) 미반영.
3. **L3 1000-tick 윈도우**: circadian phase 1 cycle 압축 — 실제 24h 가 1000 tick 으로 매핑.
4. **L4 F306.4 informal threshold**: ≤50% deviation 은 *biological literature 의 다양성* 반영, theoretical bound 아님.
5. **L5 5 falsifier**: F306.2 단조성도 5 데이터 포인트 — informal.
6. **L6 verify_fence tier SPECULATION-FENCED** — synthetic CPG sim 은 hexa-bio AXIS class, atlas identity 아님.
7. **L7 cross-cutting principle**: feedback-closure-is-physical-limit 따라 *생물학 physical limit* 들로 frame: F306.2 = H-H sigmoidal IFR, F306.3 = exponential τ, F306.5 = ~5-10× peak/trough.

## 8. 폐쇄 기준

F306.1-6 결판 → terminal close. ≥4/6 PASS = 🟢 SUPPORTED-NUMERICAL.

## 9. 산출물

- `state/h306_bio_spontaneous_emit_2026_05_26/run_h306.hexa`
- `state/h306_bio_spontaneous_emit_2026_05_26/result.json`
- `state/h306_bio_spontaneous_emit_2026_05_26/run.log`

## 10. 후속

- H_307: anima_chat.py 로그 회수 + idle-time × emit-rate 곡선 실측 (Python-out-of-scope but anima daemon hexa-port 가능)
- H_308: 영아 옹알이 / dawn chorus / PAG / Drosophila 의 실제 rate 데이터 vs 본 simulation 비교
- H_309: CPG-emit pipeline × anima `a_substrate_native_speak` 코드 정합 verify
