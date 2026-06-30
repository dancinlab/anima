# anima-physics/web/ — WebSocket consciousness engine streaming dashboard

> Status: 🟡 partial (server + dashboard.html LANDED, live engine 통합 별도 cycle) · §188 결과: N-A (streaming infrastructure, not substrate fire)
>
> SSOT: 본 README + `physics_server.hexa` + `dashboard.html`. entries: [`entries/substrate/web/`](../entries/substrate/web/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: web/ 는 substrate 가 아니라 consciousness engine 의 real-time state streaming infrastructure. WebSocket protocol (port 8765 default) 로 dashboard.html → server JSON frame per step. 자체 발화 메커니즘 없음 — engine (sim/snn/esp32) 의 emit 를 *visualize*.
- **영속성**: engine type (sim/snn/esp32) + topology (ring/small_world/scale_free/hypercube/torus/spin_glass) + cells (default 32) + speed (default 30) config 영속. session state 휘발 (browser ↔ server live).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `physics_server.hexa` | 179 | Consciousness Engine WebSocket Server (port 8765 default, JSON frame stream, 3 engine type × 6 topology) | 🟡 |
| `dashboard.html` | — | Browser-side real-time state visualization (consciousness engine config + Ψ const + live frame) | 🟡 |

## falsifier

별도 cycle — engine 통합 + browser-side render verify + protocol roundtrip.

## cross-link

- [substrate entry](../entries/substrate/web/physics_server.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`realtime_monitor.hexa`](../realtime_monitor.hexa) — inference latency + phi_live p50/p95/p99 짝
- [`physics_substrate_dispatch.hexa`](../physics_substrate_dispatch.hexa) — substrate_backend dispatch 짝
- source: `anima-physics/web/physics_server.py` (503 LOC, hexa port 의 원본)
