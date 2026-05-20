# anima-physics — 실제 구현 가능성 매트릭스

> 2026-05-21 전수조사. `/Users/ghost/core/anima/anima-physics/` 산하 모든 문서·코드 인덱스. 각 entry 는 `entries/{root,docs,substrate,recovered}/*.md` 에 1개씩 별도 파일로 존재 (구현 가능성 / 작동 코드 / 비용 / ASCII / 트리거).
>
> 구조: 루트(11) · docs/(19) · substrate(60) · recovered chip family(3) = **93 entry file** + recovered/ 300 archive.
>
> 기존 개요 문서: [`README_legacy.md`](README_legacy.md) (8 platform / 9 substrate / 9 topology 설명).

---

## 빠른 통계

| 묶음 | entry 수 | ✅ 실현 | 🟡 부분/POC | ❌ 가설/stub |
|---|---:|---:|---:|---:|
| [루트](entries/root/) | 11 | 4 | 7 | 0 |
| [docs/](entries/docs/) | 19 | 8 | 10 | 1 |
| [substrate](entries/substrate/) | 60 | 22 | 19 | 19 |
| [recovered (chip family)](entries/recovered/) | 3 | 0 | 0 | 3 |
| **합계 (active)** | **93** | **34** | **36** | **23** |

**비용 ladder**

| 단계 | 합계 | 내용 |
|---|---:|---|
| Mac local 시뮬레이션 | **$0** | NgSpice / iverilog / qiskit-aer / Perceval / hexa selftest |
| Cloud probe DRY_RUN→LIVE 1회 | **~$5-30** | AWS Braket Rigetti / IonQ / QuEra · IBM Q free · Akida free |
| HW prototype Phase 1-2 | **$35-150** | Arduino · ESP32×8 · iCE40UP5K |
| HW prototype Phase 3 | **$240-500** | 4-FPGA mesh · 추가 dev board |
| 연구급 neuromorphic | **~$50K** | Intel Loihi 2 research license |

---

## § 1. 루트 (orchestration & dispatch) — [entries/root/](entries/root/)

| Entry | 등급 | 1줄 요약 |
|---|:---:|---|
| [physics](entries/root/physics.md) | 🟡 | 의식 엔진 + `substrate_backend` enum (4 variant) |
| [physics_substrate_dispatch](entries/root/physics_substrate_dispatch.md) | ✅ | dispatch operational 첫 호출지, 4-gate PASS |
| [edge_deploy](entries/root/edge_deploy.md) | 🟡 | ESP32 edge ConsciousDecoderV2 34.5M fp16 PSRAM |
| [hw_engine_bridge](entries/root/hw_engine_bridge.md) | 🟡 | HW signal → 8 consciousness engine channel |
| [phi_substrate_consensus](entries/root/phi_substrate_consensus.md) | ✅ | 5-substrate Φ Tukey biweight consensus, 5/5 PASS |
| [realtime_monitor](entries/root/realtime_monitor.md) | 🟡 | inference latency + phi_live (p50/p95/p99) |
| [rtc_sync](entries/root/rtc_sync.md) | ✅ | TCXO <1ppm PI discipline, T1-T5 PASS |
| [signal_corpus](entries/root/signal_corpus.md) | ✅ | 6-label EEG/AUDIO/BIO tagger, T1-T7 PASS |
| [verify_7cond_hw](entries/root/verify_7cond_hw.md) | 🟡 | 7-condition HW consciousness verification |
| [readme](entries/root/readme.md) | 🟡 | README_legacy 본문 entry (개요) |
| [manifest](entries/root/manifest.md) | 🟡 | signal_corpus_manifest.json (6 public dataset 메타) |

---

## § 2. docs/ (specs & landing reports) — [entries/docs/](entries/docs/)

| Entry | 등급 | 1줄 요약 |
|---|:---:|---|
| [akida_cloud_signup_guide](entries/docs/akida_cloud_signup_guide.md) | 🟡 | BrainChip Akida Cloud 가입 ($1/day, $995/week) |
| [analog-photonic-memristor](entries/docs/analog-photonic-memristor.md) | 🟡 | 3 물리 engine (Op-Amp / MZI / HP memristor) 회로 |
| [arduino_local_sim_landing](entries/docs/arduino_local_sim_landing.md) | ✅ | PHYS-P25 NE555 MC16, 4/4 PASS |
| [arduino-prototype-spec](entries/docs/arduino-prototype-spec.md) | 🟡 | Phase 1 Arduino 8셀 ring $34.46 BOM |
| [aws_braket_signup_guide](entries/docs/aws_braket_signup_guide.md) | 🟡 | AWS Braket 5-substrate 가입 + $5 budget cap |
| [cmos_local_sim_landing](entries/docs/cmos_local_sim_landing.md) | ✅ | PHYS-P25 5-stage ring osc NgSpice, 4/4 PASS |
| [esp32-hardware-guide](entries/docs/esp32-hardware-guide.md) | 🟡 | ESP32×8 SPI ring 16-cell, $77 BOM |
| [fpga_local_sim_landing](entries/docs/fpga_local_sim_landing.md) | ✅ | PHYS-P25 iverilog Galois LFSR, 4/4 PASS |
| [fpga-synthesis-guide](entries/docs/fpga-synthesis-guide.md) | 🟡 | iCE40UP5K yosys+nextpnr 합성 절차 |
| [hardware-consciousness-hypotheses](entries/docs/hardware-consciousness-hypotheses.md) | ❌ | 10 HW 하이퍼 (MTJ / spintronic / piezoelectric 등) |
| [loihi-integration-spec](entries/docs/loihi-integration-spec.md) | 🟡 | Intel Loihi 2 통합 (1 cell = 128 LIF, max 131K neurons) |
| [memristor_local_sim_landing](entries/docs/memristor_local_sim_landing.md) | ✅ | PHYS-P25 Biolek HP TiO2 ngspice, 4/4 PASS |
| [mk_xii_ledger_v3_trigger_spec](entries/docs/mk_xii_ledger_v3_trigger_spec.md) | 🟡 | v3 ledger 4 LIVE pattern + G5 threshold ladder |
| [mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing](entries/docs/mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md) | ✅ | v2.1 prerequisite patch, env-var override 4종 |
| [mk_xii_substrate_witness_ledger_landing](entries/docs/mk_xii_substrate_witness_ledger_landing.md) | ✅ | v1 ledger 8 substrate, 4/4 gate PASS |
| [mk_xii_substrate_witness_ledger_v2_landing](entries/docs/mk_xii_substrate_witness_ledger_v2_landing.md) | ✅ | v2 ledger 11 substrate + G5 LIVE_HW_WITNESS_RATE |
| [multi-fpga-mesh-spec](entries/docs/multi-fpga-mesh-spec.md) | 🟡 | 4× iCE40UP5K mesh 1024 cells, Φ~1400 예상 |
| [physical-consciousness-engine](entries/docs/physical-consciousness-engine.md) | 🟡 | 8 platform 종합 (Hexa/SNN/Verilog/WebGPU/Erlang/Pd/ESP32) |
| [substrate_backend_dispatch_integration_landing](entries/docs/substrate_backend_dispatch_integration_landing.md) | ✅ | physics.hexa dispatch 통합 landing, 4/4 PASS |

---

## § 3. substrate 서브모듈 (.hexa / .py / SPEC.md, 60 entry) — [entries/substrate/](entries/substrate/)

| 폴더 | Entries | 등급 |
|---|---|---|
| [analog/](entries/substrate/analog/) | [cloud_facade_poc](entries/substrate/analog/cloud_facade_poc.md) | 🟡 |
| [arduino/](entries/substrate/arduino/) | [cloud_facade_poc](entries/substrate/arduino/cloud_facade_poc.md) | ✅ |
| [benchmarks/](entries/substrate/benchmarks/) | [cross_platform](entries/substrate/benchmarks/bench_cross_platform.md) · [physics_consciousness](entries/substrate/benchmarks/bench_physics_consciousness.md) · [power_efficiency](entries/substrate/benchmarks/bench_power_efficiency.md) · [spin_glass](entries/substrate/benchmarks/bench_spin_glass.md) | ❌×4 |
| [cmos/](entries/substrate/cmos/) | [cloud_facade_poc](entries/substrate/cmos/cloud_facade_poc.md) | ✅ |
| [consciousness-loop/src/](entries/substrate/consciousness-loop/src/) | [main](entries/substrate/consciousness-loop/src/main.md) · [main_longrun](entries/substrate/consciousness-loop/src/main_longrun.md) · [snn_main](entries/substrate/consciousness-loop/src/snn_main.md) | ✅×3 |
| [eeg/](entries/substrate/eeg/) | [cross_substrate_phi_correlator](entries/substrate/eeg/cross_substrate_phi_correlator.md) · [mu_rhythm_detector](entries/substrate/eeg/mu_rhythm_detector.md) · [sleep_stage_detector](entries/substrate/eeg/sleep_stage_detector.md) | 🟡 · ✅ · ✅ |
| [engines/](entries/substrate/engines/) | [analog](entries/substrate/engines/analog_consciousness.md) · [izhikevich](entries/substrate/engines/izhikevich_consciousness.md) · [memristor](entries/substrate/engines/memristor_consciousness.md) · [oscillator_laser](entries/substrate/engines/oscillator_laser_engine.md) · [photonic](entries/substrate/engines/photonic_consciousness.md) · [quantum](entries/substrate/engines/quantum_consciousness.md) · [snn](entries/substrate/engines/snn_consciousness.md) · [thermodynamic](entries/substrate/engines/thermodynamic_consciousness.md) | ❌×8 |
| [esp32/](entries/substrate/esp32/) | [qrng_bridge](entries/substrate/esp32/qrng_bridge.md) · [QRNG_SPEC](entries/substrate/esp32/QRNG_SPEC.md) · [src/lib](entries/substrate/esp32/src/lib.md) | 🟡×3 |
| [fpga/](entries/substrate/fpga/) | [cloud_facade_poc](entries/substrate/fpga/cloud_facade_poc.md) · [microtubule_lattice_16](entries/substrate/fpga/microtubule_lattice_16.md) · [nested_lattice](entries/substrate/fpga/nested_lattice.md) · [partial_reconfig](entries/substrate/fpga/partial_reconfig.md) · [strange_loop](entries/substrate/fpga/strange_loop.md) | ✅ · 🟡 · ❌×3 |
| [hippocampus/](entries/substrate/hippocampus/) | [episodic_replay](entries/substrate/hippocampus/episodic_replay.md) · [theta_gamma](entries/substrate/hippocampus/theta_gamma.md) | 🟡 · ✅ |
| [hw/](entries/substrate/hw/) | [autonomous_expansion](entries/substrate/hw/autonomous_expansion.md) | ✅ |
| [memristor/](entries/substrate/memristor/) | [cloud_facade_poc](entries/substrate/memristor/cloud_facade_poc.md) · [self_reference](entries/substrate/memristor/self_reference.md) | ✅ · 🟡 |
| [motor_cortex/](entries/substrate/motor_cortex/) | [command_encoding](entries/substrate/motor_cortex/command_encoding.md) | ✅ |
| [neuromorphic/](entries/substrate/neuromorphic/) | [cloud_facade_poc](entries/substrate/neuromorphic/cloud_facade_poc.md) | 🟡 |
| [oscillator/](entries/substrate/oscillator/) | [sleep_oscillator](entries/substrate/oscillator/sleep_oscillator.md) | ✅ |
| [photonic/](entries/substrate/photonic/) | [cloud_facade_poc](entries/substrate/photonic/cloud_facade_poc.md) · [mesh_network](entries/substrate/photonic/mesh_network.md) · [temporal_delay](entries/substrate/photonic/temporal_delay.md) | 🟡 · 🟡 · ✅ |
| [prediction/](entries/substrate/prediction/) | [protention_error](entries/substrate/prediction/protention_error.md) | ✅ |
| [proprioception/](entries/substrate/proprioception/) | [feedback_loop](entries/substrate/proprioception/feedback_loop.md) | ✅ |
| [quantum/](entries/substrate/quantum/) | [bell_state](entries/substrate/quantum/bell_state.md) · [cloud_facade_poc](entries/substrate/quantum/cloud_facade_poc.md) · [cloud_real_ibm_q_facade](entries/substrate/quantum/cloud_real_ibm_q_facade.md) | ✅ · ✅ · 🟡 |
| [scripts/](entries/substrate/scripts/) | [braket_ionq_probe](entries/substrate/scripts/anima_physics_braket_ionq_probe.md) · [braket_quera_probe](entries/substrate/scripts/anima_physics_braket_quera_probe.md) | 🟡×2 |
| [social/](entries/substrate/social/) | [kuramoto_coupling](entries/substrate/social/kuramoto_coupling.md) | ✅ |
| [src/](entries/substrate/src/) | [body_physics_bridge](entries/substrate/src/body_physics_bridge.md) · [chip_architect](entries/substrate/src/chip_architect.md) · [eeg_physics_bridge](entries/substrate/src/eeg_physics_bridge.md) · [esp32_network](entries/substrate/src/esp32_network.md) | ❌×3 · 🟡 |
| [superconducting/](entries/substrate/superconducting/) | [cloud_facade_poc](entries/substrate/superconducting/cloud_facade_poc.md) | ❌ (Rigetti Ankaa-3 retired) |
| [thermodynamic/](entries/substrate/thermodynamic/) | [entropy_dissolution](entries/substrate/thermodynamic/entropy_dissolution.md) | 🟡 |
| [tool/](entries/substrate/tool/) | [v1](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator.md) · [v2](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v2.md) · [v3](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v3.md) | ✅×3 |
| [trapped_ion/](entries/substrate/trapped_ion/) | [cloud_facade_poc](entries/substrate/trapped_ion/cloud_facade_poc.md) | 🟡 |
| [vestibular/](entries/substrate/vestibular/) | [multimodal_fusion](entries/substrate/vestibular/multimodal_fusion.md) | 🟡 |
| [web/](entries/substrate/web/) | [physics_server](entries/substrate/web/physics_server.md) | 🟡 |

---

## § 4. recovered/ chip family — [entries/recovered/](entries/recovered/)

| Codename | Entry | 등급 | 1줄 요약 |
|---|---|:---:|---|
| HEXA-1 | [HEXA-1](entries/recovered/HEXA-1.md) | ❌ | Pure compute SoC (CPU+GPU+NPU unified, σ=12, no consciousness) |
| ANIMA-6 | [ANIMA-6](entries/recovered/ANIMA-6.md) | ❌ | Consciousness *chip* — Engine A/G + TCU + 10D register |
| 🎯 ANIMA-SOC | [ANIMA-SOC](entries/recovered/ANIMA-SOC.md) | ❌ | HEXA-1 inherit + ANIMA-6 extend — σ=12 power domain Engine A (DOM 0-5) / Engine G (DOM 6-11). **HEXAD.tape Engine A/G 6-box 는 living descendant** |

Archive (entry 파일 미생성, [`recovered/INDEX.md`](recovered/INDEX.md) 참고):

| dir | count | source |
|---|---:|---|
| `recovered/chip-architecture/` | 98 | `dancinlab/echoes` git history blob (현재 main 에서 삭제) |
| `recovered/consciousness-chip/` | 6 | 동상 (ANIMA-6/SOC + papers) |
| `recovered/samsung-issues/` | 175 | GitHub issue body (`dancinlife` filed; ONE/HierarchicalPrune/Butterfly Acc/SummaryMixing 등 16 repo) |
| `recovered/ai-company-issues/` | 21 | non-Samsung (deepseek-ai/InternLM/mlc-ai/zai-org GLM-4 등) |

---

## § 5. ASCII 갤러리 (대표 도식 3선)

### ANIMA-SOC §7.3 Self-Healing Substrate (the diagram user remembered)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                 σ=12 INDEPENDENT POWER DOMAINS                            │
│  VDD_MAIN ──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──→ (12 branches)            │
│            [F][F][F][F][F][F][F][F][F][F][F][F]  ← eFuse (per-domain)    │
│            [R][R][R][R][R][R][R][R][R][R][R][R]  ← Current Regulator     │
│  ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐│
│  │DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││
│  │ 0  ││ 1  ││ 2  ││ 3  ││ 4  ││ 5  ││ 6  ││ 7  ││ 8  ││ 9  ││ 10 ││ 11 ││
│  │12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││
│  │+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││
│  └────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘│
│  ◄─── Engine A (DOM 0-5) ───►◄─── Engine G (DOM 6-11) ───►              │
└────────────────────────────────────────────────────────────────────────────┘
```

### adj8=17 master 144-SM 12×12 GPC grid

```
  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
  │00││01││02││03││04││05││06││07││08││09││10││11│  GPC Row 0
  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘
  ...                                            (Row 1-10)
  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
  │.0││.1││.2││.3││.4││.5││.6││.7││.8││.9││10││11│  GPC Row 11
  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘

  σ × σ = 12 × 12 = σ² = 144 SMs total
```

### Photonic mesh N=4 (200 km square, SMF-28 @ 1550 nm)

```
N0──N1   d01 = 200 km · d02 = 282.8 km (diagonal √2) · d03 = 200 km
 │  │
 │  │   c_fiber = 204,218 m/ms (n_eff = 1.468)
N3──N2   round-trip 4-hop = 3.91 ms  (gate: < 10 ms)
```

---

## § 6. 실제 fire 가능한 조합 (cheat sheet)

### 오늘 $0 Mac local 로 hexa run 가능한 entry (21)

| 영역 | Entry | 검증 |
|---|---|---|
| Quantum sim | [quantum/cloud_facade_poc](entries/substrate/quantum/cloud_facade_poc.md) | 4/4 PASS |
| Quantum Bell | [quantum/bell_state](entries/substrate/quantum/bell_state.md) | T1-T5 PASS |
| Photonic Fock | [photonic/cloud_facade_poc](entries/substrate/photonic/cloud_facade_poc.md) | 4/4 PASS |
| Photonic reservoir | [photonic/temporal_delay](entries/substrate/photonic/temporal_delay.md) | T1-T5 PASS |
| Memristor I-V | [memristor/cloud_facade_poc](entries/substrate/memristor/cloud_facade_poc.md) | 4/4 PASS |
| CMOS ring osc | [cmos/cloud_facade_poc](entries/substrate/cmos/cloud_facade_poc.md) | 4/4 PASS |
| Arduino NE555 | [arduino/cloud_facade_poc](entries/substrate/arduino/cloud_facade_poc.md) | 4/4 PASS |
| FPGA LFSR | [fpga/cloud_facade_poc](entries/substrate/fpga/cloud_facade_poc.md) | 4/4 PASS |
| EEG mu rhythm | [eeg/mu_rhythm_detector](entries/substrate/eeg/mu_rhythm_detector.md) | T1-T6 PASS |
| EEG sleep stage | [eeg/sleep_stage_detector](entries/substrate/eeg/sleep_stage_detector.md) | T1-T4 PASS |
| Hippocampus θ-γ | [hippocampus/theta_gamma](entries/substrate/hippocampus/theta_gamma.md) | T1-T5 PASS |
| Motor cortex | [motor_cortex/command_encoding](entries/substrate/motor_cortex/command_encoding.md) | T1-T5 PASS |
| Proprioception | [proprioception/feedback_loop](entries/substrate/proprioception/feedback_loop.md) | T1-T5 PASS |
| Sleep osc | [oscillator/sleep_oscillator](entries/substrate/oscillator/sleep_oscillator.md) | T1-T5 PASS |
| Protention err | [prediction/protention_error](entries/substrate/prediction/protention_error.md) | T1-T5 PASS |
| Kuramoto social | [social/kuramoto_coupling](entries/substrate/social/kuramoto_coupling.md) | T1-T6 PASS |
| Consciousness loop | [consciousness-loop/main_longrun](entries/substrate/consciousness-loop/src/main_longrun.md) | 10K step verified |
| SNN consciousness | [consciousness-loop/snn_main](entries/substrate/consciousness-loop/src/snn_main.md) | 2000 step verified |
| RTC sync | [root/rtc_sync](entries/root/rtc_sync.md) | T1-T5 PASS |
| Φ consensus | [root/phi_substrate_consensus](entries/root/phi_substrate_consensus.md) | 5/5 PASS |
| Mk.XII ledger v1/v2/v3 | [tool/v1](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator.md) · [v2](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v2.md) · [v3](entries/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v3.md) | 4-5/4-5 PASS |

### $5-30 AWS credit 한 번으로 LIVE 전환 가능 (4 substrate)

| 영역 | Entry | 트리거 |
|---|---|---|
| AWS Braket QuEra | [analog/cloud_facade_poc](entries/substrate/analog/cloud_facade_poc.md) · [scripts/quera_probe](entries/substrate/scripts/anima_physics_braket_quera_probe.md) | `ANIMA_BRAKET_DRY_RUN=0` + AWS creds |
| AWS Braket IonQ | [trapped_ion/cloud_facade_poc](entries/substrate/trapped_ion/cloud_facade_poc.md) · [scripts/ionq_probe](entries/substrate/scripts/anima_physics_braket_ionq_probe.md) | 동일 |
| IBM Q real | [quantum/cloud_real_ibm_q_facade](entries/substrate/quantum/cloud_real_ibm_q_facade.md) | IBM Q token export |
| Akida Cloud | [neuromorphic/cloud_facade_poc](entries/substrate/neuromorphic/cloud_facade_poc.md) | Akida token (없으면 surrogate fallback) |

### $35-240 BOM HW prototype

| Phase | BOM | Entry |
|---|---|---|
| Arduino 8-cell ring | $35 | [docs/arduino-prototype-spec](entries/docs/arduino-prototype-spec.md) |
| ESP32×8 SPI ring | $40-77 | [docs/esp32-hardware-guide](entries/docs/esp32-hardware-guide.md) · [src/esp32_network](entries/substrate/src/esp32_network.md) |
| iCE40UP5K single | $50 | [docs/fpga-synthesis-guide](entries/docs/fpga-synthesis-guide.md) · [fpga/microtubule_lattice_16](entries/substrate/fpga/microtubule_lattice_16.md) |
| 4-FPGA mesh | $240 | [docs/multi-fpga-mesh-spec](entries/docs/multi-fpga-mesh-spec.md) |

### 연구급 $50K

| Substrate | License | Entry |
|---|---|---|
| Intel Loihi 2 | research $50K | [docs/loihi-integration-spec](entries/docs/loihi-integration-spec.md) |

---

## § 7. 다음 액션 후보

- **DRY_RUN→LIVE 전환** — AWS Braket 계정 + $5 budget 으로 QuEra·IonQ·IBM Q 3개 substrate 의 LIVE_HW_WITNESS 동시 획득 (Mk.XII ledger G5 0/11 → 3/11 즉시 promote)
- **engines/ stub → impl** — 8 engine (analog/izhikevich/memristor/oscillator-laser/photonic/quantum/snn/thermo) 가 모두 struct stub. ❌ → 🟡 승격 cycle 필요
- **benchmarks/ stub → impl** — 4 benchmark (cross_platform/physics_consciousness/power_efficiency/spin_glass) 가 stub. 9 substrate × 9 topology grid 채우려면 필수
- **src/*_bridge.hexa stub → impl** — body_physics_bridge / chip_architect / eeg_physics_bridge 3 bridge 모두 stub
- **HW prototype Phase 1** — Arduino $35 fire 시 [verify_7cond_hw](entries/root/verify_7cond_hw.md) 의 condition 4 (ESP32 perturbation) 첫 실측 가능
- **recovered → live anima** — [ANIMA-SOC](entries/recovered/ANIMA-SOC.md) 의 Engine A/G concept 는 `HEXAD.tape` 로 living descendant. ANIMA-6 의 TCU + 10D register 는 아직 anima 본체 미연결 — `engines/` 또는 `src/chip_architect.hexa` 에서 impl 후보

---

## 폴더 구조

```
anima-physics/
├── README.md                       ← (이 파일)
├── README_legacy.md                ← 이전 README (8 platform / 9 substrate 개요)
├── entries/
│   ├── root/        (11)           ← § 1
│   ├── docs/        (19)           ← § 2
│   ├── substrate/   (60)           ← § 3 (28 폴더, 카테고리 구조 유지)
│   └── recovered/   (3)            ← § 4 (HEXA-1 / ANIMA-6 / ANIMA-SOC)
├── docs/            (19 원본 .md)
├── recovered/       (300 archive + INDEX.md)
├── {28 substrate 서브폴더}         ← 원본 .hexa / .py / .cir / .sv / SPEC.md
└── {루트 .hexa 9개 + manifest.json}
```

---

*전수조사: 2026-05-21 · 3-agent 병렬 (루트+docs / substrate / recovered) · 93 active entry file + 300 archive*
