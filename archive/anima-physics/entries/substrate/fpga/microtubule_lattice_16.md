# fpga/microtubule_lattice_16.hexa

> Orch-OR FPGA prep: 16-node 4×4 torus (Von Neumann 4-neighbor) tubulin lattice; iCE40UP5K mapping ~670 LUTs (13%) · **🟡 부분** · 비용 $50 iCE40UP5K board

## 구현 가능성

🟡 — hexa reference impl 완성 (deterministic, no random — moment = node_idx + step parity → bit-identical FPGA/sim trace). yosys+nextpnr-ice40 synthesis 절차 완성 (docs/fpga-synthesis-guide.md), 실 board flash 미테스트.

## 작동 코드 / 의존성

- 원본: `fpga/microtubule_lattice_16.hexa` (266 LoC)
- 외부 의존: hexa run (sim) · yosys/nextpnr-ice40/icestorm (synth)
- 상수: N_NODES=16, GRID_SIDE=4, N_NEIGH=4, N_STEPS=10, COLLAPSE_TH=0.05

## 비용 / 리소스

- $0 Mac sim
- $15-60 iCE40UP5K board (iCEBreaker / Lattice eval)
- $240 4-FPGA mesh extension (docs/multi-fpga-mesh-spec.md)

## 핵심 흐름 / FPGA mapping

```
4×4 torus (Von Neumann 4-neighbor wrap-around)
  16 Node16 cells @ ~28 LUTs each   ≈ 450 LUTs (state+moment+adders)
  Collapse comparator tree           ≈  90 LUTs
  Phi pair-wise accumulator          ≈ 130 LUTs
  Total                              ≈ 670 LUTs (13% UP5K) / ~96 FFs

iCE40UP5K @ 12 MHz single clock domain
step = 1 cycle · phi/collapse pipelined every 4 cycles
Determinism: no random — moment = f(node_idx, step_parity) → bit-identical FPGA↔sim
```

## 트리거 (fire 방법)

```bash
# Mac sim
hexa run anima-physics/fpga/microtubule_lattice_16.hexa

# FPGA synth (별 cycle)
cd anima-physics/fpga && make synth   # yosys + nextpnr-ice40 + icestorm
```

## 검증 결과

- Mac sim deterministic 2-run identical
- FPGA mapping resource budget 검증 (LUT/FF count)
- 실 board flash 미테스트 (docs/fpga-synthesis-guide.md 절차만)

## 관련 entry

- [fpga/cloud_facade_poc.md](./cloud_facade_poc.md) — iverilog Phi sim
- [fpga/nested_lattice.md](./nested_lattice.md)
- [fpga/strange_loop.md](./strange_loop.md)
- [esp32/qrng_bridge.md](../esp32/qrng_bridge.md) — Orch-OR tubulin bias input

## 출처

- README § 3 fpga/
- docs/fpga-synthesis-guide.md
- docs/multi-fpga-mesh-spec.md
