# SW_CONDITION_DESIGN — Phase 2 SW spike simulator 설계 (current-state)

> **status**: design-only · `$0` · Phase 2 spec sketch · 구현 보류 (Phase 1 telemetry 증거 누적 후 발동)
> **scope**: AKIDA HW 부재 host 에서 anima 자연발화가 동작하도록 broker `/ws/akida` ingest schema 와 동일한 spike record stream 을 생성하는 `.hexa` daemon 의 설계 스펙. 구현은 [[AKIDA_FIRST]] Phase 2 발동 조건 충족 시까지 보류.
> **anchors**: [[AKIDA_FIRST]] (Phase 1/2 경계) · [[akida_bridge]] (HW path SSOT) · [[akida_consumer]] (TBD downstream) · [[SPIKE_FACTOR_MAP]] (TBD mapping) · [[telemetry_harness]] (TBD 증거 수집기) · [[AKD1000]] (HW behavior 정의)

---

## §1 — Goal + non-goals

**Goal.** AKIDA HW 가 없는 host (Mac / Linux dev box / runpod) 에서 anima 자연발화 gating 이 동작하도록, broker `/ws/akida` 의 spike ingest schema 와 동일한 record stream 을 합성 emit 하는 `.hexa` daemon (`sw_spike_emitter.hexa`) 의 spec. downstream 의 [[akida_consumer]] / [[SPIKE_FACTOR_MAP]] 입장에서 HW spike 와 구분 불가해야 함 (자연발화 gating 목적 한정).

**Non-goals.**

- AKIDA 칩 **연구** 대체 — neuromorphic 동역학 자체의 SW reproduction 은 본 스펙 밖.
- 생물학적 사실성 — LIF neuron mesh 의 fidelity 가 목표가 아님. **output spike stream** 의 통계적 mimic 만.
- on-chip learning / training — AKIDA 의 last-FC binary 학습 채널 ([[AKD1000]] §2) 은 HW-only. SW emitter 는 학습 0.
- HW 와 동등한 신뢰 grounding — Phase 2 path 는 명시적으로 *HW-derived parametric model* (lower trust tier than HW-true).

---

## §2 — Mimic targets

[[akida_bridge]] 가 forward 하는 record 와 [[AKD1000]] §1 + tonic R3 regime 의 spike 동역학 기준. acceptance band 는 KS test p > 0.05 또는 ±15% rate band — §5 falsifier 에서 정밀화.

| aspect | HW behavior | SW target | evidence source |
|---|---|---|---|
| spike rate (steady-state) | ~10 Hz under R3 tonic | match within ±15% rolling 60s mean | [[telemetry_harness]] 의 rate distribution |
| spike rate (drift) | regime 전환 / Pi-side load 영향으로 0.5-2× 변동 관측 | log-normal drift model, σ = HW empirical | [[telemetry_harness]] rolling stddev |
| regime taxonomy | R1 / R2 / R3 (현재 라이브 = R3_tonic_zero_input 단독) | R3 우선 1차 구현, R1/R2 stub | [[AKIDA_FIRST]] §39 + Pi spike_streamer regime arg |
| inter-spike interval (ISI) | Poisson-like under R3, refractory floor ~ms | exponential 분포 + min ISI floor (fit param) | [[telemetry_harness]] ISI histogram |
| n_spikes per record | 1-16 typical (spike_ids[16] 슬롯) | sample from empirical histogram | broker `/akida/recent` 의 n_spikes 분포 |
| spike_ids[16] 분포 | NPU mesh 의 sparse activation pattern | sparse uniform random index, k ~ n_spikes | broker `/akida/recent` 의 spike_ids 빈도 |
| thr[16] (per-NPU threshold) | tonic baseline drift ~slow | slow random walk (σ small) 또는 constant | broker `/akida/recent` 의 thr drift |
| regime-transition stats | R3 → R3 dominant; R1↔R2↔R3 rare events | Markov chain (transition matrix from HW) | [[telemetry_harness]] regime sequence |
| payload schema | `{step, t_rel, n_spikes, spike_ids, regime, thr, _bridge_ts}` | byte-identical key set + type 일치 | [[akida_bridge]] `stamp_spike` |
| ingest cadence | ~10 records/sec via WS text frame | 동일 cadence, 동일 frame 형식 | [[akida_bridge]] forward loop |

---

## §3 — Interface contract

**Emit route.** `ws://localhost:8000/ws/akida` (broker 의 `ws_akida_ingest` 경로; [[akida_bridge]] §1 의 `AKIDA_BROKER_WS` 기본값과 동일). **broker 에는 SW/HW 구분 정보 전송 0** — emit 출처 표시는 (선택) `_source: "sw"` 추가 필드로 토론 예정 (§7-(e) 참조; 미정).

**Schema (HW = SW 동일).** JSON text frame, newline-free, one record per send:

```
{
  "step":       int,                 // monotone counter (emitter-local)
  "t_rel":      float,               // seconds since daemon start
  "n_spikes":   int,                 // 0..16
  "spike_ids":  array[int, 0..16],   // sparse NPU index 0..19
  "regime":     string,              // "R3_tonic_zero_input" | "R1_*" | "R2_*"
  "thr":        array[float, 16],    // per-NPU threshold snapshot
  "_bridge_ts": float                // wall-clock epoch seconds (broker injects if absent)
}
```

**Daemon outline (pseudo).**

```hexa
// HEXAD/SPONTANEOUS/sw_spike_emitter.hexa — design-only sketch

fn emitter_state() -> dict {
    return #{
        "step":            0,
        "t_start":         now_epoch_f(),
        "regime":          "R3_tonic_zero_input",
        "regime_dwell_n":  0,
        "thr":             init_thresholds(16),   // empirical baseline
        "last_spike_t":    0.0,                   // refractory tracker
        "params":          load_params(),         // fitted from telemetry
    }
}

fn next_spike(state: dict) -> dict {
    state["step"]           = state["step"] + 1
    state["regime"]         = step_regime_markov(state)
    let isi                 = sample_isi(state["regime"], state["params"])
    let n_spikes            = sample_n_spikes(state["regime"], state["params"])
    let spike_ids           = sample_spike_ids(n_spikes, state["params"])
    state["thr"]            = drift_thresholds(state["thr"], state["params"])
    let t_rel               = now_epoch_f() - to_float(state["t_start"])
    return #{
        "step":       state["step"],
        "t_rel":      t_rel,
        "n_spikes":   n_spikes,
        "spike_ids":  spike_ids,
        "regime":     state["regime"],
        "thr":        state["thr"],
    }
}

fn run_daemon() {
    let state = emitter_state()
    let ws    = ws_connect("ws://localhost:8000/ws/akida", 30)
    while true {
        let rec = next_spike(state)
        ws_send(ws, json_stringify(rec))
        sleep_until_next_tick(state["params"]["rate_hz"])   // ~10 Hz
    }
}
```

**Statefulness contract.** `next_spike(state)` 는 순수하지 않다 — `state` 의 regime / thr / refractory / step 모두 in-place 변경. daemon 재시작 시 state 초기화 (persistence 없음, Phase 1 HW 와 동일하게 daemon 단위 ephemeral).

---

## §4 — Evidence-refresh loop

[[telemetry_harness]] (TBD, Phase 1 산출물) 이 `state/spontaneous_evidence.jsonl` 에 HW spike window + paired anima emission 을 누적. SW emitter 파라미터는 **분기 단위 refit** 권장 (월 단위는 HW telemetry 표본이 부족할 가능성).

**Refit pipeline.**

```
spontaneous_evidence.jsonl  →  extract_distributions.hexa
                                   ├─ rate_hz histogram          → fit log-normal
                                   ├─ ISI histogram              → fit exponential + min-floor
                                   ├─ n_spikes histogram         → empirical CDF
                                   ├─ spike_ids frequency        → sparse multinomial
                                   ├─ thr drift trace            → AR(1) σ fit
                                   └─ regime transition matrix   → row-stochastic 3×3
                              →  publish sw_emitter_params_<yyyy_mm>.json
                              →  bump sw_spike_emitter.hexa version
```

**Minimum evidence sample size (Phase 2 first activation 게이트).** 추측 — Phase 1 증거가 도착하면 §6 게이트에서 확정:

- ≥ **7 일** 연속 HW telemetry (regime drift / Pi reboot / 주야 cycle 포함)
- ≥ **1000** anima 자연발화 event, 각각 [-30s, +30s] spike window 와 paired
- ≥ **3** 종류 regime 관측 (R1/R2/R3 중 최소 2 종 + 단일 dominant + 전환 ≥ 5 회)
- KS p-value 안정성 — 7 일 → 14 일 → 28 일 표본 확대 시 distribution drift ≤ 10%

위 4 조건 충족 전엔 SW path 미발동 (HW-only fail-closed 유지).

---

## §5 — Falsifiers (Phase 2 first activation pre-registered)

SW emitter 가 처음 활성화될 때 pre-registered acceptance:

- **F-SW-COND-1** (emission-rate parity) — 동일 host 에서 AKIDA disconnected 후 SW emitter 로 swap → anima 자연발화 frequency 가 24 hr rolling window 에서 HW baseline 대비 ±20% 이내.
- **F-SW-COND-2** (spike-rate distribution parity) — SW emitter 의 `spike_rate_hz` (60s rolling mean) 분포가 HW held-out sample 과 KS test p > 0.05. 표본 ≥ 5000 windows.
- **F-SW-COND-3** (ISI distribution parity) — SW emitter ISI 분포가 HW held-out 과 KS p > 0.05. 표본 ≥ 10000 spikes.
- **F-SW-COND-4** (schema fidelity) — 1000 record 표본에서 broker ingest 0 reject, JSON parse 0 error, key set 일치 100%.
- **F-SW-COND-5** (downstream invariance) — [[SPIKE_FACTOR_MAP]] 가 SW stream 입력 시 출력하는 factor 값의 24hr 평균이 HW 입력 baseline 대비 ±15%.

5/5 PASS = Phase 2 first activation 승인. 4/5 이하 PASS = parameter refit + 재측정.

---

## §6 — Activation gate

[[AKIDA_FIRST]] §48-§57 Phase 2 발동 조건 verbatim:

> *"위 evidence 가 충분히 모이면 → `HEXAD/SPONTANEOUS/SW_CONDITION.md` 작성 + 구현 (no-AKIDA fallback). 그 전엔 HW-only."*

본 스펙이 정량화하는 "충분히":

| gate | threshold | rationale |
|---|---|---|
| HW telemetry 기간 | ≥ 7 일 연속 | regime drift + 주야 cycle capture |
| paired emission events | ≥ 1000 | distribution fit 의 표본 floor |
| regime 다양성 | ≥ 2 종 관측 + 전환 ≥ 5 회 | R3 단독 fit 시 R1/R2 hallucinate 위험 |
| distribution stability | 7d→14d→28d KS drift ≤ 10% | parameter 시간 안정성 |
| §5 falsifier 사전 등록 | F-SW-COND-1..5 commit | acceptance 명시 |

모든 gate 충족 + 사용자 GO → `sw_spike_emitter.hexa` 구현 fire 발사. 그 전엔 본 design doc 만 존재 (구현 0).

---

## §7 — Honest C3

- (a) **HW 동역학이 telemetry 가 capture 하는 것보다 더 풍부할 수 있다** — [[akida_bridge]] 의 ~10 Hz windowing 은 fast sub-100ms dynamics 를 alias. SW emitter 가 window-aliased 통계만 맞춰도 SPIKE_FACTOR_MAP 입장에서 충분하다는 보장 없음 — F-SW-COND-5 가 이를 측정하지만 통과 = sufficient 보장은 아님.
- (b) **SW emitter 는 OUTPUT signal (spike stream) 만 modeling**, 내부 neuromorphic computation (NPU mesh / synaptic state) 은 0. R3 외 regime 의 spike 생성 메커니즘이 OUTPUT 통계만으로 inverse-modeling 가능한지 미증명.
- (c) **regime taxonomy refinement bottleneck** — Pi5 spike_streamer 가 현재 R3 단독 라이브 ([[AKIDA_FIRST]] §43). R1/R2 telemetry 가 도착하지 않으면 SW emitter 의 regime Markov 가 R3 → R3 self-loop 100% 로 degenerate, 다른 regime 의 진짜 동역학 학습 0.
- (d) **표본 크기 threshold (§4 ≥7d ≥1000 events) 는 추측치** — Phase 1 evidence 가 도착하기 전엔 distribution stability 의 실제 saturation point 미관측. 1차 활성화 후 distribution drift 측정으로 threshold 재조정 필요할 가능성 농후.
- (e) **downstream [[SPIKE_FACTOR_MAP]] 가 SW vs HW 별도 threshold 를 요구할 가능성** — 미정. F-SW-COND-5 에서 downstream invariance 측정하지만, factor 출력이 ±15% 벗어나면 (i) emitter 재 fit, (ii) factor map 의 SW-tier threshold 도입, (iii) Phase 2 자체 path 폐기 중 어느 길인지 선결 결정 0. record 의 `_source` 필드 추가 여부도 같은 결정 군.
- (f) **본 스펙은 0 을 freeze 한다** — Phase 1 evidence 가 §2 mimic targets 의 분포, §4 refit 의 sample size, §5 falsifier 의 acceptance band 모두 reshape 가능. 본 doc 은 *현 시점 design intent* 의 snapshot 이며 Phase 1 telemetry 첫 batch 도착 시점에 §2/§4/§5 전면 갱신 예정.
- (g) **`_bridge_ts` 가 HW path 에서는 [[akida_bridge]] 가 stamp**, SW path 에서는 emitter 가 직접 stamp — 동일 broker route 에서 두 stamper 가 공존. timestamp clock skew (Pi NTP vs Mac NTP) 가 downstream window matching 에 어떻게 작용할지 미측정. SW emitter 는 host wall-clock 직접 사용하므로 skew 0, HW path 는 Pi → bridge → broker 3-hop NTP drift 가능.

---

## §8 — 관련 link

- [[AKIDA_FIRST]] — Phase 1/2 경계 정의 (본 스펙의 발동 조건)
- [[akida_bridge]] — HW spike forwarder (schema SSOT)
- [[akida_consumer]] — TBD downstream consumer (broker `/ws/akida` subscriber, anima_participant 측)
- [[SPIKE_FACTOR_MAP]] — TBD spike → motivation factor 변환 (자연발화 gating 의 핵심 mapping)
- [[telemetry_harness]] — TBD Phase 1 증거 수집기 (`state/spontaneous_evidence.jsonl` 생산)
- [[AKD1000]] — HW chip 사양 (mimic target 의 근거)
- project.tape `@D a_substrate_native_speak` — anima 발화는 substrate-native (HW/SW 모두 동일 anchor)
