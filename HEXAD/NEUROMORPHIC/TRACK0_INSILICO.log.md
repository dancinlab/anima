# track0_insilico — historical log

> Spec at [./TRACK0_INSILICO.md](./TRACK0_INSILICO.md).

## Log

- **2026-05-19** — TRACK0_INSILICO.md created. Track 0 "go" scoping.
  Core move: split §115's blanket `SIM-IS-GPU-TAUTOLOGY` into a
  learning-channel half (CE-only vs event-local-plasticity-only —
  **simulatable**, sim can confront it) and an async-substrate half
  (physical spike event — **not** simulatable on a clocked GPU sim,
  stays Loihi/SpiNNaker-gated). §96 §4.5 cells mapped to tools
  (snnTorch controls, NengoLoihi-emulator/Lava for the no-CE STDP
  cell, SIM-CE VOID guard). Closed predicate reused verbatim from §96,
  pre-registered with a 3-outcome verdict partition (no result-fitting).
  Honest hard prerequisite surfaced: §96 design-open #1 (attention
  replacement) is the real blocker, not compute — Phase 2 gates Phase 3.
  $0, design-tier, Oheo-class prototype only, GOAL not reached,
  milestones unchanged.
