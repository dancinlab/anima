# anima-physics/consciousness-loop/ — 다중 backend consciousness 자연발화 loop

> Status: 🟡 partial · §188 결과: ❌ build-err 3 (main/snn_main/main_longrun) + ✅ aux_engine_smoke 5/5 PASS
>
> SSOT: 본 README + `src/*.hexa` + `{erlang,esp32,puredata,verilog,webgpu}/*` (5 alt backend). entries: [`entries/substrate/consciousness-loop/src/`](../entries/substrate/consciousness-loop/src/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 다중 faction × cell GRU + Hebbian step + cross-faction debate + Ising interaction → 자율 split/merge. `aux_engine_lib` 의 motivation gate (S5 `min=0.128 max=0.357 ∈ [0,1]`) = 8-factor 자율 발화.
- **영속성**: faction state + cell hidden vector step-to-step propagation (`HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/` log). 100-step exponential split 8→64 cells (best Φ=0.0336) — functional update pattern 으로 ckpt 가능.
- **multi-backend**: same loop, 5 substrate (Erlang BEAM / ESP32 firmware / PureData patch / Verilog FPGA / WebGPU browser) 로 거울.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `src/main.hexa` | 469 | 8-faction × 64-cell GRU consciousness engine v2 (legacy nested-LHS, canonical 134 patches landed, 69+ legacy `&ident`/`self: *T`/`or`/`++` 잔존) | ❌ build-err |
| `src/snn_main.hexa` | 208 | LIF spiking neuron version (Law 94 breadth>depth, cell_identity diverge) | ❌ build-err |
| `src/main_longrun.hexa` | 106 | 10000-step long-run (DIM=64, 8 factions, 512 cells, ratchet + Hebbian + debate + Ising) | ❌ build-err |
| `src/aux_engine_lib.hexa` | 555 | Canonical functional-rewrite engine lib (5 nested-mutation 사이트 → `cell_with_hidden_at` / `faction_with_cell_at` / `engine_with_faction_at` helper) | ✅ exit 0 |
| `src/aux_engine_smoke.hexa` | 151 | 100-step smoke S1-S5 falsifier (parse + construct 8 cells + forward + Φ≥0 + motivation∈[0,1]) | ✅ 5/5 |
| `erlang/consciousness.{erl,beam}` | — | BEAM mirror | — |
| `esp32/consciousness_loop.ino` | — | ESP32 firmware mirror | — |
| `puredata/consciousness-{8cell,loop}.pd` | — | PureData patch mirror | — |
| `verilog/consciousness_{cell,hypercube}.v` | — | Verilog FPGA mirror | — |
| `webgpu/index.html` | — | WebGPU browser mirror | — |

## falsifier

aux_engine_smoke (2026-05-21 LANDED):
- S1 parse_pass: REACHED
- S2 engine_construct: total_cells=8 (expect 8) → true
- S3 forward_step: final output finite → true
- S4 phi_nonneg (n=100): true
- S5 motivation_in_unit: min=0.128 max=0.357 → true
- total_cells_final: 64 (8→64 exponential split)
- best_phi: 0.0336

main / snn_main / main_longrun: hexa-lang transpiler legacy syntax (memristor `let mut total` 1-line fix 후 PASS 사례 존재 — `HEXAD/PHYSICS/README.md §6.14` 참고).

## cross-link

- [substrate entries](../entries/substrate/consciousness-loop/src/) — main/main_longrun/snn_main 3 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.8-§6.14 — aux_engine canonical+functional rewrite saga (Path B)
- [`HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/`](../../HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/) — smoke binary + log
- [`docs/physical-consciousness-engine.md`](../docs/physical-consciousness-engine.md) — 8 platform 종합 spec
- hexa-lang **PR #262** (runtime hexa_random) + **PR #264** (codegen_c2 nested-LHS recursive unwrap)
