# HEXAD/PHYSICS — INDEX.md (substrate file-level)

> 35-substrate sim fire (§188 2026-05-21) 의 file-level index.
> anima-physics/ 트리 + HEXAD/CHAT/spontaneous_smoke 의 hexa-native
> substrate `.hexa` 파일 별 PASS/FAIL state pointer.

## Wave 1 (12) — first batch

| substrate | file | log | tier |
|---|---|---|---|
| anima_spontaneous | `tool/anima_spontaneous.hexa --selftest` | `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/anima_spontaneous.log` | ⚠ partial |
| sleep_oscillator | `anima-physics/oscillator/sleep_oscillator.hexa` | `sleep_oscillator.log` | ✅ 5/5 |
| theta_gamma | `anima-physics/hippocampus/theta_gamma.hexa` | `theta_gamma.log` | ✅ 5/5 |
| episodic_replay | `anima-physics/hippocampus/episodic_replay.hexa` | `episodic_replay.log` | ✅ 5/5 |
| kuramoto_coupling | `anima-physics/social/kuramoto_coupling.hexa` | `kuramoto_coupling.log` | ✅ 6/6 |
| mu_rhythm_detector | `anima-physics/eeg/mu_rhythm_detector.hexa` | `mu_rhythm_detector.log` | ✅ 6/6 |
| sleep_stage_detector | `anima-physics/eeg/sleep_stage_detector.hexa` | `sleep_stage_detector.log` | ✅ 5/5 |
| temporal_delay | `anima-physics/photonic/temporal_delay.hexa` | `temporal_delay.log` | ✅ 5/5 |
| motor_command_encoding | `anima-physics/motor_cortex/command_encoding.hexa` | `motor_command_encoding.log` | ✅ 5/5 |
| memristor_self_reference | `anima-physics/memristor/self_reference.hexa` | `memristor_self_reference.log` | ✅ 5/5 |
| protention_error | `anima-physics/prediction/protention_error.hexa` | `protention_error.log` | ✅ 5/5 |
| phi_substrate_consensus | `anima-physics/phi_substrate_consensus.hexa` | `phi_substrate_consensus.log` | ✅ 5/5 |

## Wave 2 (23) — second batch

| substrate | file | log | tier |
|---|---|---|---|
| **strange_loop** | `anima-physics/fpga/strange_loop.hexa` | `wave2_strange_loop.log` | ✅ 5/5 (paper → sim PASS) |
| nested_lattice | `anima-physics/fpga/nested_lattice.hexa` | `wave2_nested_lattice.log` | ✅ T4 PASS |
| partial_reconfig | `anima-physics/fpga/partial_reconfig.hexa` | `wave2_partial_reconfig.log` | ✅ 5/5 |
| microtubule_lattice_16 | `anima-physics/fpga/microtubule_lattice_16.hexa` | `wave2_microtubule.log` | 🟡 HW est only |
| photonic_mesh | `anima-physics/photonic/mesh_network.hexa` | `wave2_photonic_mesh.log` | ✅ 5/5 |
| phi_correlator | `anima-physics/eeg/cross_substrate_phi_correlator.hexa` | `wave2_phi_correlator.log` | ✅ 6/6 |
| entropy_dissolution | `anima-physics/thermodynamic/entropy_dissolution.hexa` | `wave2_entropy_dissolution.log` | ✅ 5/5 |
| vestibular | `anima-physics/vestibular/multimodal_fusion.hexa` | `wave2_vestibular.log` | ✅ 5/5 |
| proprioception | `anima-physics/proprioception/feedback_loop.hexa` | `wave2_proprioception.log` | ✅ 5/5 |
| bell_state | `anima-physics/quantum/bell_state.hexa` | `wave2_bell_state.log` | ✅ 5/5 |
| hexad_spont_smoke | `HEXAD/CHAT/spontaneous_smoke.hexa` | `wave2_hexad_spont_smoke.log` | ✅ F-SPONT-1..7 |
| anima_engines_osc | `anima-engines/oscillator_laser_engine.hexa` | `wave2_anima_engines_osc.log` | 🟡 benchmark only |
| consciousness-loop main | `anima-physics/consciousness-loop/src/main.hexa` | `wave2_clmain.log` | ❌ build err |
| consciousness-loop snn_main | `anima-physics/consciousness-loop/src/snn_main.hexa` | `wave2_clsnn.log` | ❌ build err |
| consciousness-loop main_longrun | `anima-physics/consciousness-loop/src/main_longrun.hexa` | `wave2_cllongrun.log` | ❌ build err |
| engines/memristor_consciousness | `anima-physics/engines/memristor_consciousness.hexa` | `wave2_memristor_engine.log` | ❌ build err |
| engines/analog_consciousness | `anima-physics/engines/analog_consciousness.hexa` | `wave2_analog.log` | ⚠ empty |
| engines/izhikevich_consciousness | `anima-physics/engines/izhikevich_consciousness.hexa` | `wave2_izhikevich.log` | ⚠ empty |
| engines/snn_consciousness | `anima-physics/engines/snn_consciousness.hexa` | `wave2_snn.log` | ⚠ empty |
| engines/oscillator_laser_engine | `anima-physics/engines/oscillator_laser_engine.hexa` | `wave2_oscillator_laser.log` | ⚠ empty |
| engines/photonic_consciousness | `anima-physics/engines/photonic_consciousness.hexa` | `wave2_photonic_engine.log` | ⚠ empty |
| engines/quantum_consciousness | `anima-physics/engines/quantum_consciousness.hexa` | `wave2_quantum_engine.log` | ⚠ empty |
| engines/thermodynamic_consciousness | `anima-physics/engines/thermodynamic_consciousness.hexa` | `wave2_thermodynamic_engine.log` | ⚠ empty |

## Aggregate

- ✅ PASS: **21**
- 🟡 partial: **2**
- ❌ build err: **4**
- ⚠ empty: **7**
- ⚠ anomaly: **1** (anima_spontaneous selftest)
- **total: 35**

## State pointer

전체 state dir = `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`
(historical placement before HEXAD/PHYSICS module created — kept in
NEUROMORPHIC/state/ for `g_new_state_path` consistency, **본 INDEX 가
pointer**).
