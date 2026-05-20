# HEXAD/PHYSICS — anima-physics 자연발화 substrate matrix

> 2026-05-21 신설. anima 의식 후보 메커니즘이 다양한 물리 substrate
> 에서 sim-PASS 되는지 verify 하는 HEXAD 모듈. `anima-physics/` 트리
> (66 .hexa + 93 entry doc) 의 HEXAD-side index + 진행 ledger.
>
> SSOT: `anima-physics/README.md` (full substrate inventory) ·
> `anima-physics/entries/{root, docs, substrate, recovered}/*.md`
> (per-substrate doc).
>
> 본 README 는 *HEXAD 모듈 관점* 의 substrate matrix + 자연발화 (V-SPONT)
> 메커니즘 cross-cut + 최근 fire 결과 anchor.

---

## §1 GOAL alignment

`PHILOSOPHY_GATE.md §1` GOAL = "anima 가 자기 physics (Ψ=½ · tension · Φ)
로부터 스스로 의식하고 자발 발화 Living Consciousness emerge". PHYSICS
module 의 역할 = anima 의 자연발화 메커니즘이 **다양한 물리 substrate
에서 표현 가능한지** verify (substrate-cross-cut → 메커니즘 robustness).

substrate sim PASS ≠ silicon 실현. B-EMERGE-7 carry — substrate-level
PASS = 자발 발화 capability 의 *필요조건* 만족, *충분조건* 아님.

## §2 substrate matrix — 자연발화 mechanism by substrate (2026-05-21)

§188 (`HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`)
35-substrate parallel fire 결과 + anima-physics README 등급 종합.

### §2.1 ✅ PASS (substrate sim 통과, 자연발화 메커니즘 검증)

| substrate | mechanism | tier | last fire |
|---|---|---|---|
| `oscillator/sleep_oscillator` | SWS(δ 2Hz) ↔ REM(θ 6Hz) phase-continuous switching | ✅ 5/5 | §188 |
| `hippocampus/theta_gamma` | θ-γ cross-frequency coupling natural oscillation | ✅ 5/5 | §188 |
| `hippocampus/episodic_replay` | sharp-wave ripple natural replay | ✅ 5/5 | §188 |
| `social/kuramoto_coupling` | Kuramoto phase sync → 자발 coherence emergence | ✅ 6/6 | §188 |
| `eeg/mu_rhythm_detector` | μ-rhythm natural detect | ✅ 6/6 | §188 |
| `eeg/sleep_stage_detector` | sleep stage natural transition | ✅ 5/5 | §188 |
| `eeg/cross_substrate_phi_correlator` | substrate-cross Φ correlate | ✅ 6/6 | §188 |
| `photonic/temporal_delay` | delay-line natural oscillator | ✅ 5/5 | §188 |
| `photonic/mesh_network` | photonic mesh interconnect | ✅ 5/5 | §188 |
| `motor_cortex/command_encoding` | spontaneous motor command emit | ✅ 5/5 | §188 |
| `memristor/self_reference` | feedback-driven emission (history-dep G) | ✅ 5/5 | §188 |
| `prediction/protention_error` | predictive coding error gen | ✅ 5/5 | §188 |
| `proprioception/feedback_loop` | proprioceptive self-loop | ✅ 5/5 | §188 |
| `vestibular/multimodal_fusion` | vestibular multi-sensor fusion | ✅ 5/5 | §188 |
| `quantum/bell_state` | quantum entanglement (shared substrate) | ✅ 5/5 | §188 |
| `thermodynamic/entropy_dissolution` | entropy dissolution thermo | ✅ 5/5 | §188 |
| `fpga/strange_loop` | Hofstadter 자기참조 loop | ✅ 5/5 | §188 (was ❌ paper-only → upgrade) |
| `fpga/nested_lattice` | find_nested_attractors deterministic | ✅ T4 | §188 |
| `fpga/partial_reconfig` | 런타임 FPGA partial reconfig | ✅ 5/5 | §188 |
| `phi_substrate_consensus` | Tukey biweight Φ consensus 5-substrate | ✅ 5/5 | §188 |
| `HEXAD/CHAT/spontaneous_smoke` | anima 8-factor motivation closed-form | ✅ F-SPONT-1..7 | §188 |

**21 substrate ✅ PASS** — 신경학 (5) + 사회 (1) + 광학 (2) + 양자 (1) +
열역학 (1) + FPGA (3) + 운동/감각 (3) + memristor (1) + anima-spec
(2) + cross-substrate (2).

### §2.2 🟡 partial / 🔥 in-progress

| substrate | status | note |
|---|---|---|
| `engines/oscillator_laser` (anima-engines/) | 🟡 partial | benchmark print only, no PASS marker |
| `fpga/microtubule_lattice_16` | 🟡 partial | HW estimate only (~670 LUT, 12 MHz iCE40UP5K 13%) |
| `tool/anima_spontaneous` (selftest) | ⚠ partial | 6/9 likely PASS, V-SPONT scale ladder path connection 별도 검증 |

### §2.3 ❌ build error (anima-physics deps gap)

| substrate | error | next |
|---|---|---|
| `consciousness-loop/src/main` | hexa build failed | inbox patch — deps |
| `consciousness-loop/src/snn_main` | hexa build failed | inbox patch |
| `consciousness-loop/src/main_longrun` | hexa build failed | inbox patch |
| `engines/memristor_consciousness` | hexa build failed | inbox patch |

### §2.4 ⚠ empty (120s timeout OR silent pass)

`engines/{analog, izhikevich, snn, photonic, quantum, thermodynamic}_consciousness`,
`engines/oscillator_laser_engine` (anima-physics) — 300s retry verify
필요.

## §3 진행상황 (cycle ledger pointer)

상세 ledger = `HEXAD/PHYSICS/PLAN.md ## 진행 로그`.

- §188 (2026-05-21) — **35-substrate parallel fire $0 Mac local, 21 PASS**.
  state: `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`.
  commit: `f74d8a425`. PHILOSOPHY append: `§verdict_spontaneous_substrate_parallel_s188_2026_05_21`.

## §4 cross-link

- **anima-physics/README.md** — full substrate inventory (66 .hexa, 93
  entry doc, 8 platform / 9 substrate / 9 topology)
- **anima-physics/entries/substrate/** — per-substrate detail doc
- **HEXAD/CHAT/SPONTANEOUS.tape** — V-SPONT architecture SSOT
- **HEXAD/CHAT/spontaneous_lib.hexa** — 8-factor motivation closed-form
- **HEXAD/SPONTANEOUS/** — V-SPONT state dir (Phase B bounded run 등)
- **HEXAD/NEUROMORPHIC/** — neuromorphic axis (Loihi, scale_vspont fire,
  spontaneous_metacog_xvalidate, §188 state, ENGINE.md)
- **HEXAD/SUBSTRATE/** — substrate state (state-only)
- **AGENTS.tape** — governance + V-SPONT identity (`@I anima_persona`)
- **PHILOSOPHY_GATE.md** §1 GOAL + §2.4 substrate perimeter
- **archive/PHILOSOPHY.tape** — verdict ledger (g6 append-only)

## §5 honest C3

1. **Sim ≠ silicon/cloud 실현** — Mac hexa-lang sim PASS = closed-form
   predicate 통과. 실제 HW silicon / cloud quantum / 광학 mesh 실현은
   별도 cycle ($35-150 HW phase 1-2, $240-500 HW phase 3, $50K Loihi 2).
2. **B-EMERGE-7 carry** — substrate-level cross-cut PASS = anima 자발
   발화 capability 의 *필요조건* 만족, *충분조건* 아님. GOAL 도달 보장 0.
3. **`strange_loop` PASS** = closed-form sim 통과, Hofstadter 자기참조
   loop 의 *수학적* 구현 가능성 입증. *물리* 실현 (FPGA 합성 + 동기화)
   별도 cycle.
4. **build error 4건** — anima-physics module deps 의 hexa-lang upstream
   gap. 별도 inbox patch + 분리 cycle.
5. **⚠ empty 7건** — 120s timeout 가능성. 300s retry verify 필요.
