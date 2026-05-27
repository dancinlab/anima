# anima-physics/hw/ — HW target index

> 2026-05-21 신설. anima 의 자연발화 + 영속성 dual-role top 5 substrate
> 의 silicon path 별 설계 + 파일 + 컴파일 통합 디렉터리.
>
> 상위 SSOT: [PLAN.md G6 — HW silicon Phase 1](../PLAN.md) ·
> [HW silicon path design](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [demiurge HW verify](../docs/demiurge_hw_verify_2026_05_21.md)

---

## §1 5 HW target

| # | Dir | SW substrate | HW target | Mac local compile | Status |
|---|---|---|---|---|---|
| 1 | [strange_loop_ice40/](strange_loop_ice40/) | `fpga/strange_loop.hexa` | Lattice iCE40UP5K FPGA | iverilog ✅ + yosys ✅ | Phase 1a LANDED (sim+synth) |
| 2 | [nested_lattice_ecp5/](nested_lattice_ecp5/) | `fpga/nested_lattice.hexa` | Lattice ECP5-EVN FPGA | iverilog + yosys (synth_ecp5) | Phase 1a BG agent |
| 3 | [kuramoto_neuromorphic/](kuramoto_neuromorphic/) | `social/kuramoto_coupling.hexa` | Intel Loihi 2 + BrainChip Akida | Python local sim only (cloud-only HW) | Phase 1a BG agent |
| 4 | [sleep_oscillator_arduino/](sleep_oscillator_arduino/) | `oscillator/sleep_oscillator.hexa` | Arduino Uno + AD9833 DDS | Python local sim only (arduino-cli 미설치) | Phase 1a BG agent |
| 5 | [spontaneous_ising/](spontaneous_ising/) | `HEXAD/CHAT/spontaneous_smoke.hexa` | Toshiba SBM cloud / Fujitsu DA / ECP5 fallback | iverilog + yosys ECP5 + Python | Phase 1a BG agent |

## §2 HW tool matrix (Mac local, 2026-05-21)

| Tool | Status | Used by | brew install |
|---|---|---|---|
| `iverilog` (Icarus Verilog) | ✅ installed | #1 #2 #5 | — |
| `yosys` (synthesis) | ✅ installed | #1 #2 #5 | — |
| `python3` + numpy | ✅ installed | #3 #4 (local sim) + #5 (cloud adapter syntax check) | — |
| `nextpnr-ice40` | ❌ not installed | #1 Phase 1b | `brew install nextpnr-ice40` |
| `nextpnr-ecp5` | ❌ not installed | #2 #5 Phase 1b | `brew install nextpnr-ecp5` |
| `icestorm` (icepack/iceprog) | ❌ not installed | #1 Phase 1b | `brew install icestorm` |
| `prjtrellis` (ECP5 bitstream) | ❌ not installed | #2 #5 Phase 1b | `brew install prjtrellis` |
| `arduino-cli` | ❌ not installed | #4 Phase 1b | `brew install arduino-cli` |
| Intel NxSDK (Loihi 2) | cloud-only (no Mac) | #3 Phase 2 | Loihi 2 Hala Point trial 신청 |
| BrainChip MetaTF (Akida) | cloud-only | #3 Phase 2 | Akida Cloud trial ($1/day) |

Phase 1a = ✅ tools 만으로 가능 (iverilog + yosys + python3).
Phase 1b = ❌ tools 가 별도 brew install 필요 (bitstream + flash).
Phase 2 = cloud trial 신청 + adapter execute on cloud.

## §3 공통 디렉터리 구조

각 HW target 디렉터리는 다음 구조를 따름:

```
hw/<target>/
├── DESIGN.md           ← ASCII 구조도 + SW↔HW 매핑 + 5 falsifier + 5 honest C3
├── README.md           ← status + quick-start + files + cross-link
├── src/                ← Verilog (.v) / Arduino (.ino) / Python adapter (.py)
├── constraints/        ← FPGA pin map (.pcf / .lpf), 해당 시
├── docs/               ← datasheet / spec reference, 해당 시
├── build.sh            ← compile pipeline (sim + synth or local sim)
└── state/              ← compile artifacts (.vcd / .json / .log)
```

## §4 진행 ledger

| Date | Target | Phase | Result |
|---|---|---|---|
| 2026-05-21 | strange_loop_ice40 | 1a sim+synth | ✅ F-HW-SL-1 PASS (reset 0x29CBB8), attractor period-2, 57 LUT4 + 40 FF |
| 2026-05-21 | nested_lattice_ecp5 | 1a sim+synth | BG agent in flight |
| 2026-05-21 | kuramoto_neuromorphic | 1a local sim | BG agent in flight |
| 2026-05-21 | sleep_oscillator_arduino | 1a local sim | BG agent in flight |
| 2026-05-21 | spontaneous_ising | 1a sim+synth | BG agent in flight |

## §5 cross-link

- [anima-physics/PLAN.md](../PLAN.md) — G6 HW silicon Phase 1 (본 디렉터리가 ☑ closure path)
- [HEXAD/PHYSICS/HW_SILICON_PATH.md](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — 5 target × HW + BOM + milestone + cost ladder
- [anima-physics/docs/demiurge_hw_verify_2026_05_21.md](../docs/demiurge_hw_verify_2026_05_21.md) — demiurge 도메인 verify 매핑
- [anima-physics/docs/fpga_local_sim_landing.md](../docs/fpga_local_sim_landing.md) — FPGA sim 도구 landing
- [anima-physics/docs/arduino-prototype-spec.md](../docs/arduino-prototype-spec.md) — Arduino HW spec
- [anima-physics/docs/loihi-integration-spec.md](../docs/loihi-integration-spec.md) — Loihi 2 통합 spec
- [anima-physics/docs/akida_cloud_signup_guide.md](../docs/akida_cloud_signup_guide.md) — Akida cloud 신청

## §6 next cycle

Phase 1a 완료 후:
- Phase 1b setup: `brew install nextpnr-ice40 nextpnr-ecp5 icestorm prjtrellis arduino-cli`
- Phase 1b execute: 5 target 의 bitstream/flash 생성
- Phase 2 cloud trial 신청: Akida ($1/day) + Loihi 2 Hala Point (free trial)
- Phase 3 dev board 주문 (UPduino $70 · ECP5-EVN $120 · Arduino+AD9833 $33 = ~$220)
