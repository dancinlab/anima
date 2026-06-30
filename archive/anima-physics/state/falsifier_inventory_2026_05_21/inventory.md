# anima-physics falsifier inventory

_root_: `/Users/ghost/core/anima/anima-physics`
_pattern_: `F-[A-Z0-9_]+-[0-9]+`
_generated_: 2026-05-21T09:00:52Z

## 1. SW falsifier declarations (.hexa, per substrate)

| substrate | family | distinct F-* | total occurrences | source file |
|---|---|---:|---:|---|
| analog | F-ANALOG | 5 | 22 | cloud_facade_poc.hexa |
| arduino | F-ARDUINO | 5 | 22 | cloud_facade_poc.hexa |
| cmos | F-CMOS | 5 | 22 | cloud_facade_poc.hexa |
| engines | F-ANALOG | 5 | 23 | analog_consciousness.hexa |
| engines | F-IZ | 5 | 23 | izhikevich_consciousness.hexa |
| engines | F-OL | 5 | 23 | oscillator_laser_engine.hexa |
| engines | F-PH | 5 | 12 | photonic_consciousness.hexa |
| engines | F-Q | 5 | 12 | quantum_consciousness.hexa |
| engines | F-SNN | 5 | 23 | snn_consciousness.hexa |
| engines | F-TH | 5 | 12 | thermodynamic_consciousness.hexa |
| superconducting | F-SUPERCONDUCTING | 5 | 21 | cloud_facade_poc.hexa |
| tool | F-E2E | 5 | 18 | anima_physics_e2e_demo.hexa |
| trapped_ion | F-TRAPPED_ION | 5 | 22 | cloud_facade_poc.hexa |
| web | F-WEB | 5 | 22 | physics_server.hexa |

_subtotal_: 14 files, 70 unique F-* IDs, 277 total occurrences

## 2. SW falsifier declarations (.py)

| file | distinct F-* | total occurrences |
|---|---:|---:|
| tool/demiurge_chem_bridge.py | 4 | 8 |

_subtotal_: 1 files, 4 unique F-* IDs, 8 total occurrences

## 3. state/ run results (PASS / FAIL / TIMEOUT lines)

| state dir | PASS | FAIL | TIMEOUT | F-* in dir |
|---|---:|---:|---:|---:|
| state/e2e_demo_2026_05_21 | 7 | 0 | 0 | 5 |
| state/falsifier_inventory_2026_05_21 | 2 | 2 | 2 | 0 |
| state/g1_build_smoke_2026_05_21 | 103 | 35 | 1 | 0 |
| state/s188g_engines_2026_05_21 | 42 | 0 | 0 | 35 |
| state/v10_anima_physics_cloud_facade | 5 | 14 | 0 | 0 |
| hw/kuramoto_neuromorphic/state | 9 | 0 | 0 | 0 |
| hw/nested_lattice_ecp5/state | 8 | 1 | 0 | 0 |
| hw/sleep_oscillator_arduino/state | 9 | 0 | 0 | 0 |
| hw/spontaneous_ising/state | 9 | 0 | 0 | 0 |
| hw/strange_loop_ice40/state | 3 | 0 | 0 | 0 |

_subtotal_: PASS=197, FAIL=52, TIMEOUT=3

## 4. Unique F-* family roll-up (across all .hexa + .py)

| family (F-<NAME>) | members (count) | files |
|---|---:|---|
| F-ANALOG | 5 | analog/cloud_facade_poc.hexa engines/analog_consciousness.hexa |
| F-ARDUINO | 5 | arduino/cloud_facade_poc.hexa |
| F-CMOS | 5 | cmos/cloud_facade_poc.hexa |
| F-E2E | 5 | tool/anima_physics_e2e_demo.hexa |
| F-IZ | 5 | engines/izhikevich_consciousness.hexa |
| F-OL | 5 | engines/oscillator_laser_engine.hexa |
| F-PH | 5 | engines/photonic_consciousness.hexa |
| F-Q | 5 | engines/quantum_consciousness.hexa |
| F-SNN | 5 | engines/snn_consciousness.hexa |
| F-SUPERCONDUCTING | 5 | superconducting/cloud_facade_poc.hexa |
| F-TH | 5 | engines/thermodynamic_consciousness.hexa tool/demiurge_chem_bridge.py |
| F-TRAPPED_ION | 5 | trapped_ion/cloud_facade_poc.hexa |
| F-WEB | 5 | web/physics_server.hexa |

_subtotal_: 13 distinct families, 65 unique F-* IDs declared

## 4b. §188 substrate T<N> PASS/FAIL declarations (.hexa)

| substrate file | T<N> PASS literals | T<N> FAIL literals |
|---|---:|---:|
| eeg/mu_rhythm_detector.hexa | 6 | 6 |
| eeg/sleep_stage_detector.hexa | 5 | 5 |
| fpga/nested_lattice.hexa | 5 | 5 |
| fpga/partial_reconfig.hexa | 5 | 5 |
| fpga/strange_loop.hexa | 5 | 5 |
| hippocampus/episodic_replay.hexa | 5 | 5 |
| hippocampus/theta_gamma.hexa | 5 | 5 |
| hw_engine_bridge.hexa | 10 | 5 |
| hw/autonomous_expansion.hexa | 5 | 5 |
| memristor/self_reference.hexa | 5 | 5 |
| motor_cortex/command_encoding.hexa | 5 | 5 |
| oscillator/sleep_oscillator.hexa | 5 | 5 |
| phi_substrate_consensus.hexa | 5 | 5 |
| photonic/mesh_network.hexa | 5 | 5 |
| photonic/temporal_delay.hexa | 5 | 5 |
| prediction/protention_error.hexa | 5 | 5 |
| proprioception/feedback_loop.hexa | 5 | 5 |
| quantum/bell_state.hexa | 5 | 5 |
| rtc_sync.hexa | 5 | 5 |
| signal_corpus.hexa | 7 | 7 |
| social/kuramoto_coupling.hexa | 6 | 6 |
| thermodynamic/entropy_dissolution.hexa | 5 | 5 |
| verify_7cond_hw.hexa | 7 | 7 |
| vestibular/multimodal_fusion.hexa | 5 | 5 |

_subtotal_: 24 files, 131 "T<N> PASS" literals, 126 "T<N> FAIL" literals
_note_: each substrate selftest typically prints 5 PASS + 5 FAIL literals (one each per branch); divide by 2 for distinct T-tests.

## 5. Aggregate + PLAN.md G2 cross-check

- total F-* declarations (.hexa, occurrences): **277**
- total F-* declarations (.hexa, unique-per-file): **70**
- total F-* declarations (.py, occurrences): **8**
- total unique F-* IDs across tree: **65**
- total F-* distinct families: **13**
- §188 T<N> substrate selftests (distinct, from 24 files): **131**
- **combined falsifier-tests universe (F-* unique + T<N>)**: **196**
- state/ PASS lines: **197**, FAIL: **52**, TIMEOUT: **3**
- PLAN.md G2 expected (§188 21 + §188g 35 + G2 add 30): **86**
- **drift (combined vs PLAN 86)**: +110 (more declared than PLAN expected — additional E2E / cross-engine / aux falsifiers post-G2)
- **F-* only drift vs PLAN 86**: -21 — gap is because §188 21-substrate baseline uses T<N> selftest convention rather than F-<NAME>-N IDs; modern §188g/G2/E2E suites are the ones using F-<NAME>-N.

_done_
