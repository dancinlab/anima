# spontaneous_ising

> anima-physics HW target #5 — anima 자율 발화 (motivation gate + safety
> ratchet + audit) 의 silicon-level realization.
> SW source: `HEXAD/CHAT/spontaneous_smoke.hexa` (F-SPONT-1..7 PASS).

## Status (2026-05-21 Mac local Phase 1a)

- **Path A — Ising annealing cloud** (Toshiba SBM, Fujitsu DA): REST adapter
  skeleton committed; SDK 미설치 → `py_compile` syntax check only.
- **Path B — ECP5 FPGA FSM fallback**: iverilog sim + yosys `synth_ecp5`
  Mac local end-to-end. F-HW-SI-1..5 falsifier 사전등록.

See [DESIGN.md](DESIGN.md) for the full ASCII architecture (both paths),
SW↔HW mapping table, and honest C3 5-bullet list.

## Quick start

```bash
./build.sh sim       # iverilog → state/sim.log (Path B)
./build.sh synth     # yosys synth_ecp5 → state/ising_fsm.json (Path B)
./build.sh adapters  # py_compile Toshiba SBM + Fujitsu DA (Path A)
./build.sh all       # all of the above (Phase 1a $0 Mac local)
```

Phase 1b (별도 setup, out of scope this cycle):

- **Path A**: Toshiba SBM trial or AWS Marketplace; `TOSHIBA_SBM_KEY` env var
  → real cloud round-trip ($1-10/solve).
- **Path B**: `brew install --HEAD prjtrellis nextpnr-ecp5`; `nextpnr-ecp5
  --25k --json state/ising_fsm.json --lpf constraints/ecp5_evn.lpf
  --textcfg state/ising_fsm.cfg`; `ecppack`; `openFPGALoader -b ecp5_evn
  state/ising_fsm.bit`. Board: Lattice ECP5-EVN (~$200).

## Files

- [DESIGN.md](DESIGN.md) — 2-path ASCII architecture + falsifier spec + SW↔HW mapping
- `src/ising_fsm.v` — Path B ECP5 FSM TOP (~150 LoC, 8 factor weighted-sum +
  threshold cmp + 3-state emit FSM + safety AND + 8-deep audit RB)
- `src/ising_fsm_tb.v` — iverilog testbench (F-HW-SI-1..5)
- `src/toshiba_sbm_adapter.py` — Path A Toshiba SBM REST adapter (QUBO encode)
- `src/fujitsu_da_adapter.py` — Path A Fujitsu DA REST adapter (Ising encode)
- `constraints/ecp5_evn.lpf` — ECP5-EVN pin map (Phase 1b reference)
- `state/sim.log` + `state/ising_fsm.vcd` + `state/synth.log` +
  `state/ising_fsm.json` + `state/adapter_syntax.log`

## Cross-link

- [HW silicon path §2.5](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) (this target)
- [SW source spontaneous_smoke.hexa](../../../HEXAD/CHAT/spontaneous_smoke.hexa)
- [spontaneous_lib.hexa](../../../HEXAD/CHAT/spontaneous_lib.hexa)
- [anima-physics PLAN G6](../../PLAN.md) HW Phase 1 target #5
