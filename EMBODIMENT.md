# EMBODIMENT — current state

@title: 💞 EMBODIMENT — 감각-운동 coupling · sensor↔actuator 통합층

@goal: anima 의 sensor (perception ingest) ↔ actuator (emit channel) coupling 측정자 — 감각 입력과 출력 행동의 시간-닫힌 loop 강도. bench F axisbench (#1142) 🟠 4/5 PARTIAL — BROKEN coupling 0.45 (sensor↔actuator coupling 깨진 시나리오에서 0.45 측정, threshold 0.3 미만 기대). CHANNEL dispatcher 의 perception↔emit 통합, AGENT DESKTOP role 의 motor surface.

(edit me — describe current state in completed-form; no history, no changelog inside this file)

- [x] AxisBench F EMBODIMENT 측정 surface — `bench/axis_embodiment/` sensor-motor coupling 5 시나리오 · 4/5 PASS · BROKEN coupling 0.45 residual (PR #1142).
- [ ] M1 embodiment_lib — `EMBODIMENT/{embodiment_lib.hexa,SSOT.md}` PURE wrapper · bench/axis_embodiment 의 sensor↔actuator correlation + delay-coupled mutual info stdlib 화.
- [ ] M2 CHANNEL.perception 통합 — WAKE.perception 4-sensor (stdin/env/timer/env-event) ↔ CHANNEL.dispatcher 3-channel emit 의 시간-닫힌 loop coupling 측정 hook.
- [ ] M3 BROKEN coupling 0.45 residual — coupling 깨진 시나리오에서 0.45 측정의 원인 분해 (noise floor? sensor lag? actuator delay?) + threshold 0.3 미만으로 회복.
- [ ] M4 AGENT.DESKTOP motor surface — AGENT/DESKTOP 의 window-op · task-primitive 행동을 actuator side 로 노출, embodiment coupling 측정에 inject.

## 양방향 sibling
- ⇄ [CHANNEL](./CHANNEL.md): CHANNEL.dispatcher (3-channel emit) 가 actuator side · WAKE.perception (4-sensor) ↔ CHANNEL.emit 시간-닫힌 loop coupling
- ⇄ [AGENT](./AGENT/AGENT.md): AGENT.DESKTOP role 의 motor surface (window-op · task-primitive) embodiment 의 actuator extension
- ⇄ [WAKE](./WAKE.md): WAKE.perception (4-sensor) 가 sensor side · WAKE.daemon loop 가 embodiment loop 의 substrate
- ⇄ [OTHER-MIND](./OTHER-MIND.md): embodiment 가 self body, OTHER-MIND 가 other body · 2-body coupling 의 self-half
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (Session 2026-05-28 — AxisBench 8)
