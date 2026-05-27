# anima-physics/cmos/ — CMOS 5-stage inverter ring oscillator substrate

> Status: ✅ PASS · §188 결과: 4/4 PASS (NgSpice 180nm 5-stage facade)
>
> SSOT: 본 README + `cloud_facade_poc.hexa` + `cmos_ring_osc.cir`. entries: [`entries/substrate/cmos/`](../entries/substrate/cmos/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 홀수 5-stage CMOS inverter ring = positive feedback → 자발 주기 진동 (clock-free). 180nm process node 의 transistor switching noise → jitter 자발 emit.
- **영속성**: gate capacitance state = subcycle 영속 (휘발). 위상 (period count) 만 hexa-side ledger 영속.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 312 | NgSpice 5-stage CMOS inverter ring osc 180nm facade (hexa-only strict raw#9, .py/.sh 금지) | ✅ 4/4 |
| `cmos_ring_osc.cir` | — | NgSpice netlist (180nm PMOS/NMOS pair × 5 stages, ring closure) | — |

## falsifier

4-gate (cumulative cycle 7/8). Sibling cycles: quantum / photonic / neuromorphic / quantum_real_ibm / analog / superconducting / memristor.

## cross-link

- [substrate entry](../entries/substrate/cmos/cloud_facade_poc.md) — per-file detail
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/cmos_local_sim_landing.md`](../docs/cmos_local_sim_landing.md) — PHYS-P25 landing
