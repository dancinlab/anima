# strange_loop_ice40

> anima-physics HW target #1 — Hofstadter mutual-recursion FPGA substrate.
> SW source `fpga/strange_loop.hexa` (§188 PASS, dual-role 16/16).

## Status (2026-05-21 Mac local Phase 1a)

- ✅ **iverilog sim PASS** — F-HW-SL-1 reset seed verified (`state=0x29CBB8`),
  attractor period-2 detected at cycle 3 (`249249 ↔ 492492`).
- ✅ **yosys synth PASS** — 57 SB_LUT4 + 40 FF (24 state + 16 step_count) on
  iCE40UP5K target. F-HW-SL-5 (LUT ≤ 200) PASS.
- ⏳ Phase 1b PNR/bitstream/flash — requires `brew install icestorm nextpnr-ice40` + $70 UPduino v3 board.

## Quick start

```bash
./build.sh sim    # iverilog simulation + VCD + state dump
./build.sh synth  # yosys → iCE40 cell mapping
./build.sh all    # both (Phase 1a)
```

Phase 1b (별도 setup):
```bash
brew install icestorm nextpnr-ice40
./build.sh pnr    # nextpnr-ice40 place + route
./build.sh pack   # icepack → bitstream
./build.sh prog   # iceprog → UP5K board flash
```

## Files

- [DESIGN.md](DESIGN.md) — ASCII architecture + 5 falsifier spec + SW↔RTL map
- `src/mix4.v` — combinational mixing function (`(x+a+2b+1)%8`, fold)
- `src/strange_loop_top.v` — 8-cell mutual-recursion TOP (24 FF + 8×mix4)
- `src/strange_loop_tb.v` — iverilog 100-cycle testbench + VCD dump
- `constraints/ice40up5k_sg48.pcf` — UP5K-SG48 pin map (Phase 1b)
- `state/sim.log` + `state/strange_loop.vcd` + `state/synth.log` + `state/strange_loop.json`

## Cross-link

- [HW silicon path §2.1](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) (this target)
- [hexa source](../../fpga/strange_loop.hexa) — SW substrate (LUT_DOMAIN=8, JointState)
- [anima-physics PLAN G6](../../PLAN.md) — HW Phase 1 ☑ (this target = first-fire candidate, now ☑ sim+synth)
