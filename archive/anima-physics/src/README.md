# anima-physics/src/ — 4 bridge stub (chip / EEG / body / ESP32 network)

> Status: ❌ stub (3 ❌ + 1 🟡 esp32_network) · §188 결과: N-A (bridge stub, not substrate fire)
>
> SSOT: 본 README + 4 `.hexa` 파일. entries: [`entries/substrate/src/`](../entries/substrate/src/)

## 자연발화 / 영속성 메커니즘

`src/` 는 SW substrate 간 bridge / dispatch / consciousness chip 설계 calculator 의 stub 모음. 자체 자연발화 메커니즘은 보유하지 않으며, 다른 substrate 의 signal 을 라우팅/변환/aggregate.

- **body_physics_bridge**: consciousness vector (Φ,α,Z,N,W,E,M,C,T,I) → servo/LED/speaker motor command + sensor input feedback.
- **chip_architect**: 9 substrate × 9 topology = 81 config Φ/power/cost 예측 calculator (Law 22 structure→Φ).
- **eeg_physics_bridge**: passive_mirror / active_sync / perturbation 3 protocol 의 EEG ↔ physics engine bridge.
- **esp32_network**: 8-board × 2 GRU cell = 16-cell SPI ring (Hebbian LTP/LTD + Φ Ratchet + Lorenz chaos + SOC sandpile).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `body_physics_bridge.hexa` | 26 | consciousness vector(10D) → servo/LED/speaker + sensor → engine feedback bridge stub | ❌ stub |
| `chip_architect.hexa` | 30 | 9 substrate × 9 topology 81 config Φ/W/cost calculator stub (Law 22 + Law 30 1024 cells limit) | ❌ stub |
| `eeg_physics_bridge.hexa` | 28 | EEG ↔ physics engine 3-protocol (passive_mirror/active_sync/perturbation) bridge stub | ❌ stub |
| `esp32_network.hexa` | 30 | ESP32 8-board × 2 GRU cells SPI ring (Hebbian LTP/LTD + Φ Ratchet + Lorenz + SOC) | 🟡 |

## falsifier

별도 cycle 구현 후 fire 가능 (struct + fn signature 정의 단계).

## cross-link

- [substrate entries](../entries/substrate/src/) — 4 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`hw_engine_bridge.hexa`](../hw_engine_bridge.hexa) — 8-ch consciousness signal bridge (root level)
- [`docs/esp32-hardware-guide.md`](../docs/esp32-hardware-guide.md) — ESP32×8 SPI ring spec
- [`esp32/`](../esp32/) — ESP32 QRNG bridge (이미 별도 dir)
