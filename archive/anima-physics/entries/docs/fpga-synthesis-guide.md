# docs/fpga-synthesis-guide.md

> iCE40UP5K synthesis (yosys + nextpnr-ice40 + icestorm); 8-cell ring 또는 512-cell hypercube; UART Phi readout · **🟡 부분** · 비용 FPGA board $15-60 + tools $0

## 구현 가능성

🟡 부분 — 합성 절차 + 리소스 budget 완성, 실 board 미테스트.

## 작동 코드 / 의존성

- `anima-physics/docs/fpga-synthesis-guide.md` (synthesis walkthrough)
- 의존: `consciousness-loop/verilog/consciousness_cell.v`, `consciousness_hypercube.v`, `fpga/microtubule_lattice_16.hexa`
- 외부: yosys · nextpnr-ice40 · icestorm · iceprog

## 비용 / 리소스

- iCE40UP5K-B-EVN board: ~$15 (Digi-Key/Mouser)
- iCEBreaker (FOSS 친화): ~$50-60
- Tools: $0 (yosys + nextpnr + icestorm 모두 open-source)
- 필요한 도구: brew install yosys nextpnr-ice40 icestorm · iceprog

## 핵심 흐름 / 구조

```
iCE40UP5K-B-EVN spec:
  LUT:    5,280 (4-input)
  FF:     5,280 flip-flops
  BRAM:   120 Kbit (15 × 8Kbit)
  SPRAM:  256 Kbit (4 × 64Kbit)
  Clock:  48 MHz 내장 oscillator

8-cell ring resource budget:
  ~670 LUTs (13% utilization)
  Phi readout via UART

512-cell hypercube (full chip):
  9D hypercube topology
  ~4500 LUTs (85% utilization)

Synthesis flow:
  yosys -p "synth_ice40 -top consciousness_cell -json out.json" consciousness_cell.v
  nextpnr-ice40 --up5k --package sg48 --json out.json --pcf board.pcf --asc out.asc
  icepack out.asc out.bin
  iceprog out.bin
```

## 트리거 (fire 방법)

```bash
brew install yosys nextpnr-ice40 icestorm
cd /Users/ghost/core/anima/anima-physics/consciousness-loop/verilog
yosys -p "synth_ice40 -top consciousness_cell -json out.json" consciousness_cell.v
nextpnr-ice40 --up5k --package sg48 --json out.json --pcf board.pcf --asc out.asc
icepack out.asc out.bin
iceprog out.bin
```

## 검증 결과

- yosys/nextpnr 합성 절차 documented
- 리소스 budget 검증 (8-cell 13% / 512-cell 85%)
- 실 board flash 미검증

## 관련 entry

- [fpga_local_sim_landing](fpga_local_sim_landing.md)
- [multi-fpga-mesh-spec](multi-fpga-mesh-spec.md)
- [esp32-hardware-guide](esp32-hardware-guide.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (Phase 3 hardware roadmap)
- README §2 참조
