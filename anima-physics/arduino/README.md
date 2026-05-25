# anima-physics/arduino/ — Arduino / NE555 astable RC-oscillator substrate

> Status: ✅ PASS · §188 결과: 4/4 PASS (NgSpice NE555 Monte Carlo n=16 facade)
>
> SSOT: 본 README + `cloud_facade_poc.hexa` + `ne555_astable.cir`. entries: [`entries/substrate/arduino/`](../entries/substrate/arduino/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: NE555 astable RC duty-cycle (nominal 2/3) 의 자발 주기 발진 — 외부 trigger 없이 PWM 출력. Component tolerance(R/C ±5/10%) 가 Monte Carlo 분산 → "noise-driven auto-fire".
- **영속성**: Capacitor charge state = 1-cycle 영속. Arduino hosting 시 PWM duty register persistence (power-cycle 휘발). 실 자석 ring 8-cell 결합 (`docs/arduino-prototype-spec.md`) 시 Hall A3144×8 측정 → ledger 영속.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 321 | NgSpice NE555 astable RC oscillator Monte Carlo n=16 duty drift probe (G1-G3 gate, hexa-only strict raw#9) | ✅ 4/4 |
| `ne555_astable.cir` | — | NgSpice netlist (R1=10k ±5% / R2=10k ±5% / C=100n ±10% / sgauss seed=42) | — |

## falsifier

G1: duty std ≥ 0.001 (positive Monte Carlo) · G2: tolerance=0 → std=0 (sign-flip) · G3: deterministic byte-identical re-run.

## cross-link

- [substrate entry](../entries/substrate/arduino/cloud_facade_poc.md) — per-file detail
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/arduino_local_sim_landing.md`](../docs/arduino_local_sim_landing.md) — PHYS-P25 landing
- [`docs/arduino-prototype-spec.md`](../docs/arduino-prototype-spec.md) — 8-cell electromagnet ring $34.46 BOM
- [`hw/sleep_oscillator_arduino/`](../hw/sleep_oscillator_arduino/) — HW realization (AD9833 DDS)
