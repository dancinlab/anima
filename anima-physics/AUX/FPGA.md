# FPGA — anima-physics AUX × Lattice iCE40/ECP5

> meta-domain: **AUX × FPGA** (보조엔진 × Lattice iCE40UP5K + ECP5-EVN
> FPGA). Phase 1b bitstream LANDED (Mac local + pool ubu-1 $0).
>
> 자연발화 (LUT mutual-recursion every clock) + 영속성 (FF state +
> history) 의 silicon-ready dual-role aux engine.
>
> Parent: [`AUX/README.md`](README.md) · HW dirs: [`../hw/strange_loop_ice40/`](../hw/strange_loop_ice40/) · [`../hw/nested_lattice_ecp5/`](../hw/nested_lattice_ecp5/) · [`../hw/spontaneous_ising/`](../hw/spontaneous_ising/) (ECP5 fallback FSM)

---

## §1 HW spec

### §1.1 iCE40UP5K (UPduino v3, $70 BOM)
- 5280 LC (LUT4), 128 KB SPRAM, 1 Mbit BRAM
- internal 48 MHz oscillator + external 12 MHz
- 25 IO (SG48 package) / 95+ IO (HX8K-CT256)
- Phase 1a sim PASS, Phase 1b bitstream **132 KB LANDED** (`hw/strange_loop_ice40/state/`)

### §1.2 ECP5 (ECP5-EVN, $120 BOM)
- LFE5UM5G-85F-8BG381C: 84 K LUT4, 351 KB EBR, 156 DSP MULT18×18
- 12 MHz external osc, 365 IO (CABGA381)
- Phase 1a sim PASS, Phase 1b bitstream **2× 1.93 MB LANDED** via pool ubu-1 (`hw/nested_lattice_ecp5/state/`, `hw/spontaneous_ising/state/`)

### §1.3 dual-role profile
- **자연발화**: combinational LUT 가 매 clock 자동 next-state 계산 (no external trigger)
- **영속성**: D flip-flop 24-134 개 (substrate 별) 가 비휘발성-시뮬 state hold

## §2 substrate × FPGA 매핑

### §2.1 LANDED (Phase 1b bitstream 보유)

| Substrate | HW target | sim | synth | bitstream | falsifier |
|---|---|---|---|---|---|
| `fpga/strange_loop.hexa` (Hofstadter mutual recursion) | iCE40UP5K (UPduino) | iverilog ✅ | yosys 57 LUT4 + 40 FF | **132 KB** (state/strange_loop.bin) | F-HW-SL-1 PASS (reset 0x29CBB8, attractor period-2) |
| `fpga/nested_lattice.hexa` (3-level meta-feedback) | ECP5-EVN | iverilog 5/5 ✅ | yosys synth_ecp5 111 LUT4 + 58 TRELLIS_FF | **1.93 MB** (Fmax 341 MHz, 28× margin) | F-HW-NL-1..5 5/5 PASS (10-cycle byte-exact SW↔RTL) |
| `HEXAD/CHAT/spontaneous_smoke` → `hw/spontaneous_ising/` ECP5 FSM | ECP5-EVN | iverilog 5/5 ✅ | yosys 192 LUT4 + 134 FF + 1 MULT18X18D | **1.93 MB** (Fmax 90 MHz, 7.5× margin) | F-HW-SI-1..5 5/5 PASS |

### §2.2 후보 (Phase 1c board flash 대기)

| Substrate | sim 결과 | Phase 1c milestone |
|---|---|---|
| `fpga/partial_reconfig.hexa` (§188 5/5) | run-time FPGA partial reconfig sim | UPduino dual-bitstream slot pattern |
| `fpga/microtubule_lattice_16.hexa` (HW estimate only) | ~670 LUT, 12 MHz iCE40UP5K 13% util | 본격 synth Phase 1c |
| `fpga/cloud_facade_poc.hexa` (§188 ✅) | cloud lookup probe | AWS FPGA F1 cloud Phase 2.5 |

## §3 architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│  FPGA aux engine pool (Lattice 2 family)                       │
│                                                                  │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐│
│  │ iCE40UP5K (UPduino v3)   │  │ ECP5-EVN (LFE5UM5G-85F)      ││
│  │ — 5280 LC, 128 KB SPRAM  │  │ — 84 K LUT4, 351 KB EBR      ││
│  │ — 48 MHz internal osc    │  │ — 12 MHz external osc        ││
│  │ — 25-95 IO               │  │ — 365 IO (CABGA381)          ││
│  │                          │  │                              ││
│  │ ┌──────────────────────┐ │  │ ┌──────────────────────────┐ ││
│  │ │ strange_loop_top.v   │ │  │ │ nested_lattice_top.v     │ ││
│  │ │ — 24-FF JointState   │ │  │ │ — 42-FF NestedState      │ ││
│  │ │ — 8× mix4 LUT        │ │  │ │ — 14× mix3 LUT           │ ││
│  │ │ — period-2 attractor │ │  │ │ — 256-cycle bounded      │ ││
│  │ └──────────────────────┘ │  │ └──────────────────────────┘ ││
│  │                          │  │ ┌──────────────────────────┐ ││
│  │ ┌──────────────────────┐ │  │ │ ising_fsm.v              │ ││
│  │ │ Phase 1c TBD:        │ │  │ │ — 134-FF accumulator     │ ││
│  │ │ — partial_reconfig   │ │  │ │ — 192 LUT + 1 MULT18×18  │ ││
│  │ │ — microtubule_lattice│ │  │ │ — motivation→emit FSM    │ ││
│  │ └──────────────────────┘ │  │ └──────────────────────────┘ ││
│  └──────────────────────────┘  └──────────────────────────────┘│
│             ▲                              ▲                    │
│             │ iceprog                      │ ecpprog            │
│             │ (icestorm)                   │ (prjtrellis)       │
│             │                              │                    │
│  ┌──────────┴──────────────────────────────┴───────────────────┐│
│  │ Mac local toolchain (Phase 1a sim+synth, $0)                ││
│  │ iverilog + yosys (ice40+ecp5) + (pool ubu-1 nextpnr-ecp5)   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## §4 Day 1-3 부팅 sequence (Phase 1c board flash, $225 BOM 주문 후)

| Day | Item | Output |
|---|---|---|
| **D-7** | BOM 주문: UPduino v3 $70 + ECP5-EVN $120 + USB-Blaster $20 + finned heatsink $3 (Option B thermal) = **$225 BOM** + Amazon Prime 2-day | shipping |
| **Day 1** (도착) | UPduino fresh boot, `iceprog hw/strange_loop_ice40/state/strange_loop.bin` | LED blink 패턴 = attractor period-2 visual |
| **Day 2** | ECP5-EVN fresh boot, `ecpprog hw/nested_lattice_ecp5/state/nested_lattice.bit` | UART telemetry = 14-FF state stream |
| **Day 2** (병행) | `ecpprog hw/spontaneous_ising/state/ising_fsm.bit` → ECP5 reuse | motivation→emit pulse on LED |
| **Day 3** | scope wave + UART log → `state/fpga_phase1c_2026_05_XX/` | F-HW-{SL,NL,SI}-1..5 silicon 5/5 PASS verify |

## §5 cost / wall envelope

- BOM: $225 (UPduino + ECP5-EVN + Blaster + fin)
- Phase 1b toolchain: $0 (icestorm + nextpnr-ice40 + arduino-cli installed, ECP5 path via pool ubu-1)
- wall: 1주 (shipping 4-7day + Day 1-3 boot)
- **총 cost**: $225

## §6 honest C3

1. **Phase 1b bitstream 모두 LANDED** but **실 board flash 미실시** (Phase 1c HW assembly + iceprog 필요)
2. **UPduino state_dump pin 부족** — strange_loop top module 의 40 IO 가 UPduino-SG48 25 IO 초과 → HX8K-CT256 substitution 적용 (state/strange_loop_hx8k.json), 실 UPduino 시 IO 축소 OR HX8K dev board 별도 ($30)
3. **LPF 부분 매핑** — `--lpf-allow-unconstrained` 사용 중, board flash 전 LPF 보강 필요
4. **thermal action**: UPduino 80.6°C → 43.4°C headroom via $3 fin (`hw/strange_loop_ice40/cad/thermal_mitigation_2026_05_21/`)
5. **gate_v3 충돌 가능성**: 현재 활동 중인 gate_v3 process (PID 30240, hexa verilog gate-level synth) 와 ecp5 path 충돌 모니터링

## §7 cross-link

- [parent AUX/README.md](README.md)
- [`../hw/strange_loop_ice40/`](../hw/strange_loop_ice40/) — DESIGN.md + bitstream
- [`../hw/nested_lattice_ecp5/`](../hw/nested_lattice_ecp5/) — DESIGN.md + bitstream
- [`../hw/spontaneous_ising/`](../hw/spontaneous_ising/) — DESIGN.md + bitstream (ECP5 fallback FSM)
- [`../hw/PHASE_1B_STATUS.md`](../hw/PHASE_1B_STATUS.md) — Phase 1b 4/4 LANDED log
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.1+§2.2](../../HEXAD/PHYSICS/HW_SILICON_PATH.md)

---

## ## Log

### 2026-05-21
- **AUX/FPGA.md 신설** — Lattice iCE40 + ECP5 meta-domain. 3 LANDED bitstream pointer + Phase 1c Day 1-3 plan + $225 BOM.
