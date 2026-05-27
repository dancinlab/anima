# nested_lattice_ecp5

> anima-physics HW target #2 — 3-level tangled hierarchy FPGA substrate
> ("I am a strange loop" at N=3, meta-consciousness 의 silicon realization).
> SW source `fpga/nested_lattice.hexa` (PHYS-P8-1, §188 T4 PASS).

## Status (2026-05-21 Mac local Phase 1a)

- ✅ **iverilog sim 5/5 PASS** — F-HW-NL-1..5 all PASS
  - F-HW-NL-1 reset seed `42'h2443c171160` (= nested_new(1) byte-exact)
  - F-HW-NL-2 first nested_step byte-exact
  - F-HW-NL-3 10-cycle SW chain bit-identical (0 mismatches)
  - F-HW-NL-4 state bounded in 14×3-bit domain over 256 cycles (no X/Z)
  - F-HW-NL-5 L3.m0 perturbation reaches L1.a-cells within 10 cycles
- ✅ **yosys `synth_ecp5` PASS** — 111 LUT4 + 58 TRELLIS_FF + 8 CCU2C
  on ECP5UM5G-85K target (≈ 0.16% LUT / 0.07% FF utilisation).
- ⏳ Phase 1b PNR/bitstream/flash — requires `brew install nextpnr-ecp5 prjtrellis`
  + $150 Lattice ECP5-EVN board (CABGA381, LFE5UM5G-85F-8BG381C).

## Quick start

```bash
./build.sh sim    # iverilog simulation + VCD + sim.log
./build.sh synth  # yosys → ECP5 cell mapping + stats
./build.sh all    # both (Phase 1a)
```

Phase 1b (별도 setup):
```bash
brew install yosys nextpnr-ecp5 prjtrellis
./build.sh pnr    # nextpnr-ecp5 place + route
./build.sh pack   # ecppack → bitstream
# flash via openocd / Lattice Diamond programmer (board-specific)
```

## Files

- [DESIGN.md](DESIGN.md) — ASCII 3-level architecture + 5 falsifier spec + SW↔RTL map
- `src/mix3.v` — combinational mixing function `(x+a+2b+1)%8 + fold` (P8 sibling of P5 mix4)
- `src/nested_lattice_top.v` — 14-cell 3-level top (42 FF + 14×mix3 + 16-FF counter)
- `src/nested_lattice_tb.v` — iverilog testbench (10-step bit-exact + 256-cycle horizon + perturbed-DUT coupling probe)
- `constraints/ecp5_evn.lpf` — ECP5-EVN-CABGA381 pin map (Phase 1b)
- `state/sim.log` + `state/nested_lattice.vcd`
- `state/synth.log` + `state/nested_lattice.json`

## Cross-link

- [HW silicon path §2.2](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) (this target)
- [sibling HW #1 strange_loop_ice40](../strange_loop_ice40/README.md) — P5 N=2 substrate (iCE40UP5K)
- [hexa source](../../fpga/nested_lattice.hexa) — SW substrate (LUT_DOMAIN=8, NestedState 14 cells)
- [anima-physics PLAN G6](../../PLAN.md) — HW Phase 1 (HW #2 sim+synth ☑ this commit)
