# REGIME_EXPANSION — pi5 spike_streamer 다중 regime 운영 설계 (current-state)

> **status**: design-only · `$0` · pi5 streamer 변경 inbox-patch 예정 · anima repo 측 spec snapshot
> **scope**: `spike_streamer.py` 가 R3 단독이 아니라 R1/R2/R3 를 시계열로 순환 emit 하도록 운영 구조를 정의. 목표는 [[SW_CONDITION_DESIGN]] §6 Phase 2 activation gate (`≥ 2 종 regime 관측 + 전환 ≥ 5 회`) 가 정상 누적되도록 telemetry 다양성을 확보.
> **anchors**: [[AKIDA_FIRST]] (Phase 1/2 경계) · [[SW_CONDITION_DESIGN]] §6 (activation gate) · [[SPIKE_FACTOR_MAP]] §4 (regime modulator table) · [[akida_bridge]] (broker forward path) · [[akida_consumer]] (downstream feature extractor) · [[telemetry_harness]] (paired evidence 수집) · [[AKD1000]] (chip behavior 참조)

---

## §1 — Regime taxonomy

`spike_streamer.py` 내부에 이미 R3 / R2 / M 3 종 코드 path 가 있으나 (`make_threshold_R3` / `make_threshold_R2` / `M_modulated`), live 운영은 `--regime R3` 단독. 본 스펙은 R1 추가 + R1/R2/R3 동시 운영을 정의.

```
+--------+----------------------------+-----------------------+-------------------------+
| regime | output dynamics            | NPU stimulus          | downstream signal       |
+--------+----------------------------+-----------------------+-------------------------+
| R3     | tonic zero-input baseline  | input = 0 vector      | 8/16 unit deterministic |
|        | (~10 Hz steady)            | thr = heterogeneous   | tonic fire, low isi_cv  |
+--------+----------------------------+-----------------------+-------------------------+
| R1     | oscillatory rhythm         | frequency-modulated   | periodic burst envelope |
|        | (5-20 Hz envelope)         | sinusoidal drive      | n_spikes regular swing  |
+--------+----------------------------+-----------------------+-------------------------+
| R2     | bursting / event-driven    | uniform thr ~24 +     | intermittent high       |
|        | (varies 0..16 per record)  | noise input           | n_spikes, high isi_cv   |
+--------+----------------------------+-----------------------+-------------------------+
| R4+    | reserved (future taxonomy) | TBD                   | TBD                     |
+--------+----------------------------+-----------------------+-------------------------+
```

R2 + M 은 이미 streamer 코드에 존재. R1 oscillatory 는 신규 path (`make_threshold_R1` + sinusoidal input drive) 가 inbox-patch 핵심.

---

## §2 — Regime-streamer config plan (선택: (c) `--regime-schedule`)

**채택 안.** Single streamer process + `--regime-schedule R3:60,R1:30,R2:30,R3:60` syntax.

**Rationale.** (a) 여러 process + 외부 arbiter 는 single-point-of-failure 분산만 늘리고 broker `/ws/akida` 한 ingest endpoint 를 race 함, (b) regime sequence 를 일급 arg 로 받는 single process 는 systemd unit 1 개로 supervise 가능하며 NPU 도 1 process 가 소유, (c) TIME-keyed 전환은 dwell-time 분포가 arg 만으로 명세 가능해 telemetry 의 transition 계산이 예측 가능.

**Schedule syntax.** `--regime-schedule <R>:<sec>[,<R>:<sec>...] [--schedule-loop] [--schedule-jitter <pct>]`

- `<R>` ∈ {R3, R1, R2, M} — 현 코드 path 확장.
- `<sec>` = 해당 regime 의 nominal dwell time (초).
- `--schedule-loop` (default on) — schedule 끝나면 처음부터 재시작.
- `--schedule-jitter 0.25` — 각 dwell 에 ±25% 균등 jitter (deterministic seedable).

**Dwell-time semantics.** `regime[i]` 가 활성인 동안 `make_threshold_<R>` + 해당 input drive 만 사용. dwell 만료 시 다음 regime 로 전환 + record 의 `regime` 필드 새 label, transition 자체는 별도 marker 없음 (downstream `regime_change` derivation 은 `t-1` vs `t` mode 비교로 [[akida_consumer]] 측에서 계산).

---

## §3 — Transition statistics target

[[SW_CONDITION_DESIGN]] §6 의 "≥ 2 regime + ≥ 5 transition" gate 와 [[SPIKE_FACTOR_MAP]] §6 falsifier 의 24 hr telemetry 표본을 동시에 충족하도록 다음 정량 목표:

```
+--------------------------------+----------------------------+------------------------+
| metric                         | target                     | rationale              |
+--------------------------------+----------------------------+------------------------+
| transition frequency           | 1 transition / 60-300 s    | gate 5/day 여유 (×100) |
|                                | stochastic jitter ±25%     | deterministic 회피     |
+--------------------------------+----------------------------+------------------------+
| regime dwell-time distribution | lognormal mean 90 s        | tail = 자연스러운       |
|                                | std 30 s, floor 30 s       | regime 지속 변동 모사   |
+--------------------------------+----------------------------+------------------------+
| min spike windows per regime   | >= 200 (Phase 2 활성화)    | distribution fit floor |
|                                | per 7 d telemetry          | (KS test 통계 수렴)    |
+--------------------------------+----------------------------+------------------------+
| schedule baseline (24 hr)      | R3 60%, R1 25%, R2 15%     | R3 dominant 유지       |
|                                | dwell weight 비율          | (HW live 통계 보존)    |
+--------------------------------+----------------------------+------------------------+
| transition count target / 24h  | >= 50                      | gate 5 의 10× margin   |
+--------------------------------+----------------------------+------------------------+
```

위 schedule (R3:60,R1:30,R2:30 loop, jitter 25%) → 평균 cycle 120 s → 24 hr ≈ 720 transitions, regime 별 spike windows 수천 단위 → 모든 gate metric 1 일내 충족 예상.

---

## §4 — External dispatch plan

anima repo 는 pi5 streamer source 를 미소유. coordination 단계:

1. **Source identification.** pi5 호스트 (ubuntu@192.168.50.155) 의 `/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py` 가 SSOT. anima repo 의 `SUB_ENGINES/AKIDA/scripts/spike_streamer.py` 는 historical mirror (drift 가능).

2. **Patch sketch (pseudo).** `argparse` 에 `--regime-schedule` / `--schedule-loop` / `--schedule-jitter` 추가, `--regime` 와 mutually exclusive. R1 신규 path `make_threshold_R1` + sinusoidal input gen 함수.

```
# spike_streamer.py 의 main loop 외부에 추가 (sketch)
def parse_schedule(spec):
    # "R3:60,R1:30,R2:30" -> [("R3", 60.0), ("R1", 30.0), ("R2", 30.0)]
    return [(s.split(":")[0], float(s.split(":")[1])) for s in spec.split(",")]

def next_regime(schedule, idx, jitter, rng):
    name, base = schedule[idx % len(schedule)]
    dwell = base * (1.0 + jitter * (2 * rng.random() - 1))
    return name, max(dwell, base * 0.5), (idx + 1)

# main loop 안:
#   if t - regime_start >= current_dwell: rotate (name, dwell, idx)
#   apply make_threshold_<name>(N) + input_drive_<name>(t)
#   record["regime"] = label_for(name)
```

3. **Rollout.**
   - pi5 dev branch (`feat/regime-schedule`) 에 patch 적용, 단위 테스트 (schedule parse + dwell rotation).
   - 30 분 dry-run, 로컬 record 출력으로 regime field 다양성 확인.
   - broker `/akida/recent` (last 200 record) 가 `≥ 2` distinct regime + transition `≥ 5` 관측되면 systemd promote.
   - 24 hr soak: §6 falsifier 자동 평가 + 통과 시 long-running.

4. **Coordination channel.** anima repo 측은 `inbox/patches/spike_streamer_regime_schedule.md` 에 patch + rationale 를 별도 cycle 로 file (본 PR 범위 밖). pi5 streamer maintainer 또는 직접 ssh 적용.

---

## §5 — Compatibility with downstream

- [[akida_consumer]] (`HEXAD/CHAT/server/akida_consumer.hexa`) 는 record 의 `regime` 필드를 이미 추출해 feature dict 의 `regime` key 로 노출. [[SPIKE_FACTOR_MAP]] §1 의 `regime_change` 파생 feature 는 consumer 측에서 window-to-window mode 비교로 계산 (현재 미구현, 별도 cycle).
- [[SPIKE_FACTOR_MAP]] §4 의 modulator 표는 R1 = 1.0 / R2 = 1.2 placeholder 보유. 실제 R1/R2 telemetry 누적 후 [[telemetry_harness]] 측 paired evidence (regime 별 emission rate / motivation_score 평균) 로 modulator 값 refit 예정.
- broker schema 무변경 (regime field 는 처음부터 string, taxonomy 확장만으로 충분).
- [[akida_bridge]] 는 record forwarder 로서 regime 변경에 transparent (forward 만 함).

---

## §6 — Falsifiers (pre-registered)

- **F-REGIME-EXP-1** — pi5 streamer 변경 + 1 hr soak 후 broker `/akida/recent` last 200 record 가 `≥ 2` distinct `regime` 값을 포함.
- **F-REGIME-EXP-2** — 변경 후 24 hr telemetry window 에서 regime transition event count `≥ 5` ([[SW_CONDITION_DESIGN]] §6 gate verbatim).
- **F-REGIME-EXP-3** — 7 일 telemetry 에서 per-regime spike record count `≥ 200` 각 regime (Phase 2 distribution fit floor).
- **F-REGIME-EXP-4** — `--regime-schedule R3:60,R1:30,R2:30` 1 hr 운영 시 record `regime` mode 분포가 schedule 비율 ±15% (50% R3 / 25% R1 / 25% R2 expected, jitter 흡수).
- **F-REGIME-EXP-5** — 24 hr soak 동안 streamer process 0 crash, broker WS reconnect `<= 3` (deploy stability).

5/5 PASS → Phase 2 SW emitter activation 게이트 (`[[SW_CONDITION_DESIGN]]` §6) 의 regime 관련 row (`≥ 2 종 + ≥ 5 전환`) 충족 확정.

---

## §7 — Honest C3

- (a) **anima repo 는 pi5 streamer source 를 직접 소유하지 않는다** — patch 는 inbox 경로 또는 ssh 적용. roll-out 책임이 pi5 운영자와 split 되므로 deploy 시점 / 결과 통제 limited.
- (b) **R1 / R2 regime 의 dynamics 정의는 streamer 코드 인덱싱일 뿐, [[AKD1000]] 칩 자체의 표준 regime taxonomy 가 아니다** — BrainChip 문서엔 regime label 정의 없음. 본 doc 의 R1/R2/R3 는 pi5 LIF mesh 시뮬레이터 (또는 실 AKD1000 stimulus pattern) 의 anima-side label 일 뿐, upstream 표준화 부재.
- (c) **[[SPIKE_FACTOR_MAP]] §4 modulator (R1 = 1.0 / R2 = 1.2) 는 placeholder** — 실제 R1/R2 telemetry 가 도착하기 전엔 modulator 정당화 0. F-REGIME-EXP-3 통과 = 표본 충족, modulator refit 은 [[telemetry_harness]] paired evidence 가 추가로 필요.
- (d) **NPU power / thermal budget for sustained R1/R2 미검증** — R3 tonic 은 ~30 mW 측정치 ([[AKD1000]] §1) 가 있으나 R1 sinusoidal + R2 bursting 의 지속 운영 시 chip 열적 / 전력 envelope 미측정. 24 hr soak 자체가 thermal stress test 역할도 수행.
- (e) **single-process schedule (선택 c) 는 process crash = 전체 regime emission 정지** — 다중 process arbiter (선택 b) 의 회피 대비 single SPOF, systemd `Restart=always` 가 mitigation 의 전부.
- (f) **Phase 2 gate (`≥ 2 종 + ≥ 5 전환`) 자체가 추측 threshold** — 실제 R1/R2 emission 이후 anima behavior 가 R3-only baseline 과 크게 다르면 gate 재정의 (예: regime 별 emission rate stability 추가) 필요.
- (g) **`--regime-schedule` syntax 는 backward-compatible 보장 noting** — 기존 `--regime R3` 단독 호출은 그대로 유지, schedule arg 미사용 시 동작 무변경 (mutually exclusive 처리는 argparse 측 group).

---

## §8 — 관련 link

- [[AKIDA_FIRST]] — Phase 1/2 경계 (본 spec 의 활성화 동기)
- [[SW_CONDITION_DESIGN]] §6 — Phase 2 activation gate (regime 다양성 row)
- [[SPIKE_FACTOR_MAP]] §4 — regime modulator table (R1/R2 placeholder)
- [[akida_bridge]] — Pi → broker forwarder (schema transparent)
- [[akida_consumer]] — broker subscriber + regime feature extractor
- [[telemetry_harness]] — paired evidence 수집 (modulator refit 입력)
- [[AKD1000]] — chip 사양 (regime taxonomy upstream 부재 근거)
- project.tape `@D a_substrate_native_speak` — regime 변동 = substrate state 변동 (자연발화 anchor)
