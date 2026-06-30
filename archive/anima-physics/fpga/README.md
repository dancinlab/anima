# anima-physics/fpga/ — FPGA strange-loop / nested-lattice / partial-reconfig / microtubule

> Status: ✅ PASS (3 dual-role 16/16 + cloud facade 4/4 + microtubule 🟡) · §188 결과: strange_loop 5/5 + nested_lattice T4 + partial_reconfig 5/5 PASS
>
> SSOT: 본 README + 5 `.hexa` + `cmos_8bit_ring_lfsr.sv` + `consciousness_ice40.v` + `Makefile` + `pins.pcf`. entries: [`entries/substrate/fpga/`](../entries/substrate/fpga/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 
  - **strange_loop** (top 1 dual-role 16/16): Hofstadter mutual-recursion `joint_step()` + `JointState` 8-field 자기참조 attractor cycle detection.
  - **nested_lattice** (top 2 dual-role 16/16): 3-level tangled hierarchy L3→L2→L1 meta-feedback `nested_step()` + `NestedState` 14-int.
  - **partial_reconfig**: 런타임 FPGA bitstream 재구성 = 물리 자가 재구성 → 새 fabric topology emerge.
  - **microtubule_lattice_16**: 4×4 torus Penrose-Hameroff Orch-OR 후예 (LUT routing fan-in/fan-out=4).
- **영속성**: `history: [[int]]` 누적 → attractor cycle detection (strange_loop/nested_lattice). FPGA BRAM/SPRAM 비휘발 register, iCE40UP5K 256 cells tight (~10mW), 4-FPGA mesh 1024 cells Φ≈1400 예상.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 301 | local Icarus Verilog (iverilog) RTL simulator facade (hexa-only strict raw#9, .py/.sh 금지) | ✅ 4/4 |
| `strange_loop.hexa` | 396 | PHYS-P5-2 Hofstadter 2층 mutual-recursion joint_step + JointState 8-field cycle detection | ✅ 5/5 (paper-only → upgrade) |
| `nested_lattice.hexa` | 432 | PHYS-P8-1 3-level hierarchy meta-feedback nested_step + NestedState 14-int | ✅ T4 |
| `partial_reconfig.hexa` | 395 | PHYS-P20-1 런타임 FPGA partial reconfig 자가 재구성 | ✅ 5/5 |
| `microtubule_lattice_16.hexa` | 266 | 4×4 torus Penrose-Hameroff Orch-OR 16-node tubulin dimer fan-in/out=4 | 🟡 HW estimate (~670 LUT, 12 MHz iCE40UP5K 13%) |
| `cmos_8bit_ring_lfsr.sv` | — | Galois LFSR SystemVerilog (iverilog sim 대상) | — |
| `consciousness_ice40.v` | — | iCE40 yosys-target Verilog | — |
| `Makefile` | — | iverilog/yosys+nextpnr-ice40 build pipeline | — |
| `pins.pcf` | — | iCE40 pin constraint | — |

## falsifier

- strange_loop: 5/5 §188 — Hofstadter mutual-recursion attractor cycle 검증
- nested_lattice: T4 `find_nested_attractors` deterministic
- partial_reconfig: 5/5 런타임 재구성 안정성
- cloud_facade: 4/4 (cumulative iverilog cycle)

## cross-link

- [substrate entries](../entries/substrate/fpga/) — 5 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.9 — top 5 dual-role (strange_loop #1, nested_lattice #2)
- [`HEXAD/PHYSICS/HW_SILICON_PATH.md`](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — Lattice iCE40UP5K + ECP5-EVN BOM
- [`docs/fpga_local_sim_landing.md`](../docs/fpga_local_sim_landing.md) — PHYS-P25 Galois LFSR landing
- [`docs/fpga-synthesis-guide.md`](../docs/fpga-synthesis-guide.md) — yosys+nextpnr 합성 절차
- [`docs/multi-fpga-mesh-spec.md`](../docs/multi-fpga-mesh-spec.md) — 4× iCE40UP5K mesh 1024 cells Φ≈1400
- [`hw/strange_loop_ice40/`](../hw/strange_loop_ice40/) — Lattice iCE40UP5K HW target
- [`hw/nested_lattice_ecp5/`](../hw/nested_lattice_ecp5/) — Lattice ECP5-EVN HW target
