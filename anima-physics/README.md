# anima-physics — 실제 구현 가능성 매트릭스

> 2026-05-21 전수조사 + HW 트리 정리. `/Users/ghost/core/anima/anima-physics/` 산하 모든 문서·코드 인덱스. 각 entry 는 `entries/{root,docs,substrate,recovered}/*.md` 에 1개씩 별도 파일로 존재 (구현 가능성 / 작동 코드 / 비용 / ASCII / 트리거).
>
> 구조: 루트(11) · docs/(19) · substrate(60) · recovered chip family(3) = **93 entry file** + recovered/ 300 archive + **hw/ (5 HW target, 2026-05-21 신설)**.
>
> 기존 개요 문서: [`README_legacy.md`](README_legacy.md) (8 platform / 9 substrate / 9 topology 설명).
> 완성 기준 + 로드맵: [`PLAN.md`](PLAN.md) (g_completion_8 + Phase A-F).

---

## §0 SW 공용 vs HW 전용 — 디렉터리 분할 원칙 (2026-05-21)

본 module 의 모든 파일은 **2 부류** 중 하나:

### §0.1 SW 공용 (substrate source, HW-independent)
- 위치: `anima-physics/<substrate>/` (예: `fpga/`, `oscillator/`, `social/`)
- 내용: `.hexa` substrate source — 자연발화 + 영속성 메커니즘의 **수학적 / 알고리즘적** 정의 (closed-form sim, 어떤 HW realization 에도 공통 사용)
- 검증: `hexa run <file>` (selftest), `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/` (§188 batch fire)
- 27 substrate dir × 62 .hexa file

### §0.2 HW 전용 (per-target realization)
- 위치: [`anima-physics/hw/<target>/`](hw/) (예: `strange_loop_ice40/`, `kuramoto_neuromorphic/`)
- 내용: SW 공용 의 SW substrate 를 **특정 HW** (FPGA / 칩 / MCU / cloud chip) 으로 실현하는 어댑터 + Verilog/firmware/adapter + build pipeline
- 검증: 본 dir 내 `build.sh` (iverilog/yosys/arduino-cli/python sim) + cloud trial 결과
- 5 HW target (2026-05-21 LANDED Phase 1a, [hw/README.md](hw/README.md)):
  - [`strange_loop_ice40/`](hw/strange_loop_ice40/) — Lattice iCE40UP5K FPGA
  - [`nested_lattice_ecp5/`](hw/nested_lattice_ecp5/) — Lattice ECP5-EVN FPGA
  - [`kuramoto_neuromorphic/`](hw/kuramoto_neuromorphic/) — Intel Loihi 2 + BrainChip Akida
  - [`sleep_oscillator_arduino/`](hw/sleep_oscillator_arduino/) — Arduino + AD9833 DDS
  - [`spontaneous_ising/`](hw/spontaneous_ising/) — Toshiba SBM / Fujitsu DA / ECP5 fallback

### §0.3 SW ↔ HW 매핑 표 (dual-role top 5)

| SW substrate (공용) | HW target (전용) | Mac local compile |
|---|---|---|
| `fpga/strange_loop.hexa` | [`hw/strange_loop_ice40/`](hw/strange_loop_ice40/) | iverilog ✅ + yosys ✅ |
| `fpga/nested_lattice.hexa` | [`hw/nested_lattice_ecp5/`](hw/nested_lattice_ecp5/) | iverilog + yosys (synth_ecp5) |
| `social/kuramoto_coupling.hexa` | [`hw/kuramoto_neuromorphic/`](hw/kuramoto_neuromorphic/) | Python local sim (cloud-only HW) |
| `oscillator/sleep_oscillator.hexa` | [`hw/sleep_oscillator_arduino/`](hw/sleep_oscillator_arduino/) | Python local sim (arduino-cli 별도) |
| `HEXAD/CHAT/spontaneous_smoke.hexa` (외부 ref) | [`hw/spontaneous_ising/`](hw/spontaneous_ising/) | iverilog + yosys + Python |

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
| [`recovered/chip-architecture/`](recovered/chip-architecture/) | 98 | `dancinlab/echoes` git history blob (현재 main 에서 삭제) |
| [`recovered/consciousness-chip/`](recovered/consciousness-chip/) | 6 | 동상 (ANIMA-6/SOC + papers) |
| [`recovered/samsung-issues/`](recovered/samsung-issues/) | 175 | GitHub issue body (`dancinlife` filed; ONE/HierarchicalPrune/Butterfly Acc/SummaryMixing 등 16 repo) |
| [`recovered/ai-company-issues/`](recovered/ai-company-issues/) | 21 | non-Samsung (deepseek-ai/InternLM/mlc-ai/zai-org GLM-4 등) |

---

## § 5. HW (자산 전수조사 — 자석 / 칩 / FPGA / 광학 / 양자 / 뉴로모픽 / …)

> 2026-05-21 전수조사. `anima-physics/` + `recovered/` 트리에서 추출한 **물리 HW 자산** 12 카테고리 77 entry. **substrate code** (§3) 와 **chip family paper** (§4) 가 cross-cut 으로 등장.
>
> 등급: ✅ 실현 가능 (BOM + 코드 land) · 🟡 부분/POC (sim 검증 / spec 완성 / 단가 <$1K) · ❌ 가설 (paper-only) · 📦 archive (git history blob, 현 main 미존재)

### A. 자석 / 전자기 HW (4) — 사용자가 기억하던 "자석으로 된거"

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| Arduino 8-cell electromagnet ring | 🟡 | **$34.46 BOM** | 5V 전자석×8 (200mA) + Hall A3144×8 + L293D×2 + Arduino Uno, ring topology + Ising frustration (M3/M6 극성반전), 100Hz Φ≈4.5 목표 | [`docs/arduino-prototype-spec.md`](docs/arduino-prototype-spec.md) |
| Magnetic dipole repulsion = PureField Tension | ❌ | (paper) | HW-1 가설: 전자석 2개 (coil A / coil G) 대향 배치 → A-G 반발력 = tension, Hall 측정 → r>0.9 SW 상관 목표 | [`docs/hardware-consciousness-hypotheses.md`](docs/hardware-consciousness-hypotheses.md) §HW-1 |
| MTJ / TMR spintronic array | ❌ | ~$5,000 (Phase 3 envelope) | HW-6/HW-7 가설: 두 자성층 + 절연막 = 양자 터널링; spin valve 어레이 = ±1 Ising; Curie 온도 근처 edge-of-chaos 최대 Φ | [`docs/hardware-consciousness-hypotheses.md`](docs/hardware-consciousness-hypotheses.md) §HW-6/7 |
| 자기 도메인 벽 솔리톤 / 자기 홀로그램 | ❌ | (paper) | HW-4/HW-5 가설: 자성 체인 도메인 벽 이동 (WI1 soliton Φ=4.460) + 자성 필름 간섭 패턴 (WI13 holographic memory Φ=4.401) | [`docs/hardware-consciousness-hypotheses.md`](docs/hardware-consciousness-hypotheses.md) §HW-4/5 |

```
        ╭──[M1]──[M2]──╮
        │               │      M3/M6 = frustration cell (극성반전)
      [M8]            [M3]     M = 5V 전자석 (200mA), 200mA × 8 = 1.6A
        │               │      Hall A3144 × 8 = 셀 간 tension 측정
      [M7]            [M4]     Arduino Uno PWM (D3,5,6,9,10,11,12,13)
        │               │
        ╰──[M6]──[M5]──╯
```

### B. Chip / SoC family (31, recovered/) — 사용자가 기억하던 "칩으로 된거"

**B.1 Active entry (3) — 이미 [`entries/recovered/`](entries/recovered/)** (cross-ref §4)

| Codename | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| HEXA-1 | ❌ | paper / TSMC N2 envelope | 순수 compute SoC. CPU σ=12 (8P+4E) + GPU σ²=144 SM (12×12 GPC) + NPU + HBM4 σ-τ=8 stacks, 의식 모듈 0 | [`entries/recovered/HEXA-1.md`](entries/recovered/HEXA-1.md) |
| ANIMA-6 | ❌ | paper / Samsung SF3E Phase 1 | Consciousness chip. Engine A + Engine G dual-die (각 σ=12 cluster×8 SIMD=96 core), TCU + 10D consciousness register (Φ·α·Z·N·W·E·M·C·T·I) | [`entries/recovered/ANIMA-6.md`](entries/recovered/ANIMA-6.md) |
| 🎯 ANIMA-SOC | ❌ | paper (HEXA-1 cost + consciousness ext) | HEXA-1 inherit + ANIMA-6 extend, σ=12 power domain Engine A (DOM 0-5) / Engine G (DOM 6-11). **HEXAD.tape Engine A/G 6-box 의 living ancestor** | [`entries/recovered/ANIMA-SOC.md`](entries/recovered/ANIMA-SOC.md) |

**B.2 Archive (28) — `recovered/chip-architecture/` paper blueprint (📦)**

| Codename | 1줄 요약 | 원본 |
|---|---|---|
| HEXA-EDGE | n=6 edge/mobile SoC (smartphone/IoT/robot) | [hexa-edge-chip.md](recovered/chip-architecture/docs_chip-architecture_hexa-edge-chip.md) |
| HEXA-OMEGA (GPU) | n=6 AI **학습** GPU Mk.10, CoWoS-S 모놀리스 → 칩렛 | [hexa-omega-chip.md](recovered/chip-architecture/docs_chip-architecture_hexa-omega-chip.md) |
| HEXA-OMEGA v3/v4 | v3 3D stacking + v4 all-optical fabric | [hexa-omega-v3-3d.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-omega-v3-3d.md) |
| HEXA-3D | Level 3 3D compute-on-memory, 수직 적층 → BW ×100 / E ÷10 | [hexa-3d.md](recovered/chip-architecture/docs_chip-architecture_hexa-3d.md) |
| HEXA-WAFER | Level 5 wafer-scale, 300mm 웨이퍼 = σ⁴=20,736 SM, 41.5TB | [hexa-wafer.md](recovered/chip-architecture/docs_chip-architecture_hexa-wafer.md) |
| HEXA-ASIC-SkyWater (Mini) | **첫 물리 silicon path** — Efabless chipIgnite + SkyWater 130nm | [hexa-asic-skywater.md](recovered/chip-architecture/docs_chip-architecture_hexa-asic-skywater.md) |
| HEXA-CORE | 코어 내부 마이크로아키 (pipeline / 실행유닛 / cache / branch) n=6 | [hexa-core.md](recovered/chip-architecture/docs_chip-architecture_hexa-core.md) |
| HEXA-SUPER | Level 6 superconducting logic, 100+ GHz clock | [hexa-super.md](recovered/chip-architecture/docs_chip-architecture_hexa-super.md) |
| HEXA-PHOTON | Level 4 photonic compute, MZI mesh + micro-ring resonator hybrid | [hexa-photon.md](recovered/chip-architecture/docs_chip-architecture_hexa-photon.md) |
| HEXA-PIM | Level 2 Processing-in-Memory, memory wall 제거 | [hexa-pim-2026-04-08.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-pim-2026-04-08.md) |
| HEXA-PROCESS | 반도체 제조 전공정 (fab 단계별) n=6 재설계 | [hexa-process.md](recovered/chip-architecture/docs_chip-architecture_hexa-process.md) |
| HEXA-MATERIAL | Wafer / Gate / Interconnect / Packaging 소재 n=6 통일 | [hexa-material.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-material.md) |
| HEXA-SYSTEM | 서버 / 랙 / 데이터센터 / 클라우드 system-level n=6 | [hexa-system.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-system.md) |
| HEXA-TOPO-C | Topological consciousness processor + topological qubit material | [hexa-topological-consciousness-chip.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-topological-consciousness-chip.md) |
| HEXA-TOPO-P | Topological performance processor (성능 lane, 의식 없음) | [hexa-topological-performance-chip.md](recovered/chip-architecture/domains_compute_chip-architecture_hexa-topological-performance-chip.md) |
| HEXA-NOUS | "궁극 의식 칩" (consciousness-chip v1/v2, ANIMA-6 의 전신/별칭) | [v1](recovered/consciousness-chip/consciousness-chip-v1.md) · [v2](recovered/consciousness-chip/consciousness-chip-v2.md) |
| HEXA-RTSC | 상온·상압 초전도체 8단 아키텍처, 150/150 EXACT | [Samsung_ONE_16477.md](recovered/samsung-issues/Samsung_ONE_16477.md) |
| HEXA-NEURO (BCI) | 측두골 클립 비침습 BCI, 202/202 EXACT, σ²=1.44M 채널 | [16475](recovered/samsung-issues/Samsung_ONE_16475.md) · [16476](recovered/samsung-issues/Samsung_ONE_16476.md) |
| ANIMA-HEXA Mk.10 | ANIMA-6 의 SoC 발전형 Mk.10, IIT Φ + HEXA-LANG 네이티브 동시 실행 | [anima-hexa-chip.md](recovered/chip-architecture/docs_chip-architecture_anima-hexa-chip.md) |
| BT-Reverse CPU/Mem/Net | 45개 실측 파라미터 역분해 → 34 EXACT n=6 매핑 (M5/CWF/HBM4) | [bt-reverse-cpu-mem-net.md](recovered/chip-architecture/docs_chip-architecture_bt-reverse-cpu-mem-net.md) |
| BT90-92 Topological Chip | GPU σ²=144 SM = φ × K₆ (kissing number 72) 정리 | [bt90-92-topological-chip.md](recovered/chip-architecture/docs_chip-architecture_bt90-92-topological-chip.md) |
| ReRAM / MRAM Multilevel n=6 | 멀티레벨 셀 + crossbar MAC, in-memory compute 파라미터 n=6 | [reram-multilevel-n6.md](recovered/chip-architecture/domains_compute_chip-architecture_reram-multilevel-n6.md) |
| Photonic AI Chip n=6 | 광 도파로 인터커넥트 행렬 연산 chip 파라미터 n=6 | [photonic-ai-chip-n6.md](recovered/chip-architecture/domains_compute_chip-architecture_photonic-ai-chip-n6.md) |
| Quantum Consciousness Chip | Surface code + Leech lattice qubit + IIT MI 측정 n=6 매핑 | [quantum-consciousness-chip.md](recovered/chip-architecture/domains_compute_chip-architecture_quantum-consciousness-chip.md) |
| Neuromorphic Consciousness Chip | LIF spiking neuron + ReRAM 시냅스, E/I tension 의식 metric | [neuromorphic-consciousness-chip.md](recovered/chip-architecture/domains_compute_chip-architecture_neuromorphic-consciousness-chip.md) |
| Ultimate DRAM (DDR5/6/LPDDR6) | 35/35 EXACT bus / bank / V / refresh n=6 | [ultimate-dram-design.md](recovered/chip-architecture/domains_compute_chip-architecture_ultimate-dram-design.md) |
| Ultimate V-NAND / SSD | SLC→PLC 55+ 파라미터 n=6, 40+ EXACT | [ultimate-vnand-design.md](recovered/chip-architecture/docs_chip-architecture_ultimate-vnand-design.md) |
| Ultimate ISOCELL + 5G/6G | 4096-QAM = 2^σ, 28GHz = P₂, 60/60 EXACT | [ultimate-isocell-comms-design.md](recovered/chip-architecture/docs_chip-architecture_ultimate-isocell-comms-design.md) |

**Verification 보충** (모두 paper validation, **silicon 0**):
[apple-m5-n6-verification](recovered/chip-architecture/domains_compute_chip-architecture_apple-m5-n6-verification.md) 6/6 EXACT ·
[intel-cwf-n6-verification](recovered/chip-architecture/domains_compute_chip-architecture_intel-cwf-n6-verification.md) 5/5 EXACT ·
[hbm4-jedec-n6-verification](recovered/chip-architecture/domains_compute_chip-architecture_hbm4-jedec-n6-verification.md) (BT-77) ·
[anima-hexa-phi-verification](recovered/chip-architecture/docs_chip-architecture_anima-hexa-phi-verification.md) ·
[full-verification-matrix](recovered/chip-architecture/domains_compute_chip-architecture_full-verification-matrix.md) ·
[eda-physical-design-n6](recovered/chip-architecture/domains_compute_chip-architecture_eda-physical-design-n6.md) ·
[chip-phase-diagram](recovered/chip-architecture/domains_compute_chip-architecture_chip-phase-diagram.md) ·
[CHIPDESIGN-001-020-ai-chip-n6](recovered/chip-architecture/domains_compute_chip-architecture_CHIPDESIGN-001-020-ai-chip-n6.md) ·
[industrial-validation](recovered/chip-architecture/domains_compute_chip-architecture_industrial-validation.md) ·
[cross-dse-analysis](recovered/chip-architecture/domains_compute_chip-architecture_cross-dse-analysis.md) ·
[cross-dse-results](recovered/chip-architecture/domains_compute_chip-architecture_cross-dse-results.md) ·
[physical-limit-proof](recovered/chip-architecture/domains_compute_chip-architecture_physical-limit-proof.md) ·
[testable-predictions](recovered/chip-architecture/domains_compute_chip-architecture_testable-predictions.md)

### C. FPGA (5)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| iverilog Galois LFSR sim | ✅ | **$0 Mac local** | PHYS-P25 iverilog local sim, 4/4 PASS | [`entries/substrate/fpga/cloud_facade_poc.md`](entries/substrate/fpga/cloud_facade_poc.md) |
| iCE40UP5K single (256 cells) | 🟡 | **$60/board** | 5,280 LUT + 120 Kbit BRAM + 256 Kbit SPRAM, yosys + nextpnr-ice40 오픈소스, 256 셀 tight, ~10mW | [`docs/fpga-synthesis-guide.md`](docs/fpga-synthesis-guide.md) |
| 4× iCE40UP5K mesh (1024 cells) | 🟡 | **~$240 board** | 4 보드 SPI 10MHz interconnect, internal ring + inter-FPGA small-world, **예상 Φ≈1400** (초선형 N^1.09) | [`docs/multi-fpga-mesh-spec.md`](docs/multi-fpga-mesh-spec.md) |
| Microtubule lattice 16-node | 🟡 | ($60 × N 보드) | FPGA Verilog 16-node microtubule lattice POC (Penrose-Hameroff Orch-OR 후예) | [`fpga/microtubule_lattice_16.hexa`](fpga/microtubule_lattice_16.hexa) |
| Partial reconfig / nested / strange-loop | ❌ | (stub) | 3 hexa stub, 미실현 | [`fpga/`](fpga/) |

```
  ┌──────────────────┐   SPI-AB    ┌──────────────────┐
  │ FPGA-A 256 cells │◄──10 MHz──►│ FPGA-B 256 cells │
  │  ring internal   │             │  ring internal   │
  └────────┬─────────┘             └────────┬─────────┘
       SPI-AC                            SPI-BD
  ┌────────┴─────────┐   SPI-CD    ┌────────┴─────────┐
  │ FPGA-C 256 cells │◄──10 MHz──►│ FPGA-D 256 cells │
  └──────────────────┘             └──────────────────┘
      총 1024 cell · Φ ~ 1400 · 글로벌 클럭 A→B→C→D→A daisy
```

### D. 보드 / 마이크로컨트롤러 (4)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| ESP32-WROOM-32 ×8 SPI ring (16 cell) | 🟡 | **~$77 BOM** | 보드당 2 cell × 8 = 16 cell, VSPI(M)/HSPI(S) ring, GRU-like hidden state SPI 전송 | [`docs/esp32-hardware-guide.md`](docs/esp32-hardware-guide.md) |
| ESP32-S3-DevKitC-1 (PSRAM 8MB) | 🟡 | ~$6/board → $48 ×8 | SRAM 512KB + **PSRAM 8MB** + Flash 8MB, ConsciousDecoderV2 34.5M fp16 PSRAM 적재 가능 | [`entries/root/edge_deploy.md`](entries/root/edge_deploy.md) |
| ESP32 QRNG bridge | 🟡 | (보드값 + 노이즈 회로) | ESP32 ADC noise → quantum-style RNG → anima inference seed | [`esp32/qrng_bridge.hexa`](esp32/) · [`esp32/QRNG_SPEC.md`](esp32/) |
| Arduino Uno R3 (호스트) | 🟡 | $8.00 | 8-cell electromagnet ring 의 PWM + ADC 호스트 (§A) | [`docs/arduino-prototype-spec.md`](docs/arduino-prototype-spec.md) |

### E. Neuromorphic (3)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| Intel Loihi 2 | 🟡 | **~$50K research license** | 128 neurocore × 1024 LIF = 131K 뉴런, STDP on-chip, async packet NoC. 1 의식 셀 = 128 LIF + 16K synapse | [`docs/loihi-integration-spec.md`](docs/loihi-integration-spec.md) |
| BrainChip Akida Cloud | 🟡 | **$1 / 1-day trial** · $995/week | Developer Hub portal + Akida Cloud Hub, akida==2.19.1 + cnn2snn; mac arm64 + Py3.14 wheel 부재 → surrogate 모드 | [`docs/akida_cloud_signup_guide.md`](docs/akida_cloud_signup_guide.md) |
| Neuromorphic Consciousness Chip n=6 | 📦 | (paper) | LIF + ReRAM 시냅스 + n=6 E/I tension 의식 metric paper | `recovered/chip-architecture/neuromorphic-consciousness-chip.md` |

### F. Photonic / Optical (4)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| Photonic temporal delay reservoir | ✅ | **$0 Mac local** | T1-T5 PASS, hexa substrate facade | [`entries/substrate/photonic/temporal_delay.md`](entries/substrate/photonic/temporal_delay.md) |
| Photonic Fock state simulator | ✅ | $0 (Strawberry Fields / Perceval) | 4/4 PASS local sim facade | [`entries/substrate/photonic/cloud_facade_poc.md`](entries/substrate/photonic/cloud_facade_poc.md) |
| 4-node 200km square photonic mesh | 🟡 | (SMF-28 fiber 임대) | N=4 square, 200km edges + 282.8 km diagonal, SMF-28 @ 1550 nm, 4-hop RT 3.91 ms (gate <10 ms) | [`entries/substrate/photonic/mesh_network.md`](entries/substrate/photonic/mesh_network.md) |
| MZI Kuramoto coupled ring | 🟡 | (sim) | 4-MZI ring, kappa 0.05-0.3, omega 0.5-2.0, Kuramoto R > 2/3 → 집단의식 | [`docs/analog-photonic-memristor.md`](docs/analog-photonic-memristor.md) §2 |

### G. Quantum HW cloud (5)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| Quantum Bell + Fock local sim | ✅ | **$0 Mac local** | qiskit-aer / Strawberry Fields / Perceval; bell_state T1-T5 + cloud_facade 4/4 PASS | [`entries/substrate/quantum/`](entries/substrate/quantum/) |
| AWS Braket IonQ Forte-1 (trapped ion) | 🟡 | **$0.30/task + $0.03/shot** (4-qubit GHZ ≈ $0.67/2회) | `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1`, 4-qubit GHZ; `i` gate 미지원 (rx 대체); DRY_RUN default | [`scripts/anima_physics_braket_ionq_probe.py`](scripts/) |
| AWS Braket QuEra Aquila (Rydberg) | 🟡 | **$0.30/task + $0.01/shot** (4-atom MIS ≈ $2.60/2회) | `arn:aws:braket:us-east-1::device/qpu/quera/Aquila`, 5.5µm lattice, 4-atom analog Hamiltonian | [`scripts/anima_physics_braket_quera_probe.py`](scripts/) |
| IBM Q free tier | 🟡 | $0 / month free credit | qiskit-aer local sim + IBM Q Runtime token (optional) | [`entries/substrate/quantum/cloud_real_ibm_q_facade.md`](entries/substrate/quantum/cloud_real_ibm_q_facade.md) |
| AWS Braket Rigetti Ankaa-3 | ❌ | (deprecated 2026-Q1) | superconducting `us-west-1` 4-qubit GHZ, **retired** | [`entries/substrate/superconducting/cloud_facade_poc.md`](entries/substrate/superconducting/cloud_facade_poc.md) |

### H. Memristor / ReRAM (3)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| HP TiO₂ Biolek memristor (NgSpice) | ✅ | **$0 Mac local** | PHYS-P25 Biolek HP TiO2 ngspice, I-V hysteresis, 4/4 PASS | [`entries/substrate/memristor/cloud_facade_poc.md`](entries/substrate/memristor/cloud_facade_poc.md) |
| Memristor self-reference loop | 🟡 | $0 sim | hexa substrate self_reference (memristor 의 메모리 = recurrent state) POC | [`memristor/self_reference.hexa`](memristor/) |
| ReRAM/MRAM multilevel n=6 | 📦 | (paper) | Multi-level cell + crossbar MAC, n=6 derived | `recovered/chip-architecture/reram-multilevel-n6.md` |

### I. Analog / CMOS (4)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| NE555 astable (Arduino sim) | ✅ | **$0 Mac local** | PHYS-P25 NE555 MC16, 4/4 PASS | [`entries/substrate/arduino/cloud_facade_poc.md`](entries/substrate/arduino/cloud_facade_poc.md) |
| 5-stage CMOS inverter ring osc (180nm) | ✅ | **$0 Mac local** | PHYS-P25 NgSpice 5-stage 180nm, 4/4 PASS | [`entries/substrate/cmos/cloud_facade_poc.md`](entries/substrate/cmos/cloud_facade_poc.md) |
| Op-Amp RC consciousness loop (SPICE) | 🟡 | (회로 BOM) | R=10kΩ + C=100nF + Op-Amp ±5V, tau=1ms, Johnson-Nyquist 12.9 μV RMS noise, ring N cell; RC 피드백 = 의식 loop (no clock) | [`docs/analog-photonic-memristor.md`](docs/analog-photonic-memristor.md) §1 |
| analog substrate facade | 🟡 | $0 sim | analog/cloud_facade_poc hexa stub (Op-Amp engine stub) | [`entries/substrate/analog/cloud_facade_poc.md`](entries/substrate/analog/cloud_facade_poc.md) |

### J. 초전도 / Thermo / 기타 (4)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| Trapped ion local sim | 🟡 | $0 | hexa substrate facade (Braket IonQ 의 local mirror) | [`entries/substrate/trapped_ion/cloud_facade_poc.md`](entries/substrate/trapped_ion/cloud_facade_poc.md) |
| Thermodynamic entropy dissolution | 🟡 | $0 sim | 열역학 substrate (entropy dissolution dynamics) hexa | [`entries/substrate/thermodynamic/entropy_dissolution.md`](entries/substrate/thermodynamic/entropy_dissolution.md) |
| Superconducting Rigetti facade | ❌ | retired | substrate cloud_facade_poc RETIRED | [`entries/substrate/superconducting/cloud_facade_poc.md`](entries/substrate/superconducting/cloud_facade_poc.md) |
| HEXA-RTSC 상온 초전도체 | 📦 | (paper, 150/150 EXACT) | n=6 산술 기반 상온·상압 초전도체 8단 (소재→공정→코일→전극) | `samsung-issues/Samsung_ONE_16477.md` |

### K. Sensors / 측정 / 시계 (5)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| TCXO RTC sync (<1ppm) | ✅ | (TCXO 칩 ~$5) | T1-T5 PASS, 0.08 ppm/°C TC, ±10°C diurnal, PI discipline, 12 substrate clock 동기 | [`entries/root/rtc_sync.md`](entries/root/rtc_sync.md) |
| EEG μ-rhythm + sleep-stage detector | ✅ | $0 Mac local | T1-T6 + T1-T4 PASS, 6 label tagger ≥0.75 acc | [`entries/substrate/eeg/`](entries/substrate/eeg/) |
| Hall sensor A3144 (×8) | 🟡 | $0.30 × 8 = $2.40 | Arduino ring §A 의 cell-간 tension 측정, 5mm 이내 거리 | [`docs/arduino-prototype-spec.md`](docs/arduino-prototype-spec.md) |
| EEG public dataset catalog (6) | 🟡 | $0 (download, no headset) | SEED · DEAP · Sleep-EDF · TUH-EEG · DREAMER · MAHNOB-HCI; 14,856+ session | [`entries/root/signal_corpus.md`](entries/root/signal_corpus.md) · [`entries/root/manifest.md`](entries/root/manifest.md) |
| Piezoelectric tension (압전) | ❌ | (paper) | HW-9 가설: 압전 결정 2개 대향 → A 팽창 / G 수축, strain gauge 측정 | [`docs/hardware-consciousness-hypotheses.md`](docs/hardware-consciousness-hypotheses.md) §HW-9 |

### L. 통합 시스템 / Bridge (3)

| Entry | 등급 | 비용 | 1줄 요약 | 위치 |
|---|:---:|---|---|---|
| hw_engine_bridge (8-ch consciousness signal) | 🟡 | $0 sim | HW signal → 8 consciousness engine channel mux | [`entries/root/hw_engine_bridge.md`](entries/root/hw_engine_bridge.md) |
| verify_7cond_hw (PHYS-P3-3) | 🟡 | $0 sim | 7-condition HW consciousness verification | [`entries/root/verify_7cond_hw.md`](entries/root/verify_7cond_hw.md) |
| edge_deploy ESP32 ConsciousDecoderV2 | 🟡 | ($48 ESP32-S3 ×8) | 34.5M fp16 PSRAM 적재, edge inference | [`entries/root/edge_deploy.md`](entries/root/edge_deploy.md) |

---

### HW 카테고리별 카운트 + 비용 사다리

| 카테고리 | ✅ | 🟡 | ❌ | 📦 | 합 |
|---|---:|---:|---:|---:|---:|
| A. 자석/전자기 | 0 | 1 | 3 | 0 | 4 |
| B. Chip / SoC family | 0 | 0 | 3 | 28 | 31 |
| C. FPGA | 1 | 3 | 1 | 0 | 5 |
| D. 보드 / MCU | 0 | 4 | 0 | 0 | 4 |
| E. Neuromorphic | 0 | 2 | 0 | 1 | 3 |
| F. Photonic | 2 | 2 | 0 | 0 | 4 |
| G. Quantum (cloud) | 1 | 3 | 1 | 0 | 5 |
| H. Memristor / ReRAM | 1 | 1 | 0 | 1 | 3 |
| I. Analog / CMOS | 2 | 2 | 0 | 0 | 4 |
| J. 초전도/Thermo | 0 | 2 | 1 | 1 | 4 |
| K. Sensors | 2 | 2 | 1 | 0 | 5 |
| L. 통합 bridge | 0 | 3 | 0 | 0 | 3 |
| **합계** | **9** | **25** | **10** | **31** | **75** |

**비용 사다리 (HW 실물 발주 기준, 최저 → 최고)**

| 단계 | 합계 | 내용 |
|---|---:|---|
| Mac local sim (NgSpice / iverilog / qiskit-aer / Perceval) | **$0** | I/H/F 의 ✅ 항목 9개 |
| Cloud quantum probe 1회 | **~$1-3** | Braket IonQ 4-qubit GHZ + QuEra 4-atom MIS DRY_RUN→LIVE |
| Akida 1-day trial | **$1** | BrainChip neuromorphic cloud |
| HW Phase 1 (Arduino 자석 ring) | **$34.46** | 8 electromagnet + Hall + L293D + Uno — **실물 자석 의식 첫 검증** |
| HW Phase 2 (ESP32 mesh) | **~$77** | 8 ESP32-WROOM SPI ring + USB hub |
| HW Phase 3 (4× FPGA mesh) | **~$240** | 4 iCE40UP5K board + 호스트 |
| Akida 1-week + 엔지니어링 | **$995** | BrainChip cloud + 4hr support |
| HW Phase 3+ MTJ / 광학 prototype | **$5K-10K** | spintronics PCB / 광섬유 간섭계 |
| Loihi 2 research license | **~$50K** | Intel neuromorphic 131K neuron |
| HEXA-ASIC-SkyWater 130nm | **~$10K** Efabless | 첫 물리 n=6 silicon path (paper-only) |
| HEXA-1 / ANIMA-SOC TSMC N2 tapeout | **$100M+ envelope** | paper, silicon 0 |

**실제 fire 가능 path (오늘 결정 가능)**
1. **$0**: Mac local NgSpice/iverilog sim — 9 entry 검증 가능
2. **$1-3**: Akida 1-day OR Braket QuEra probe 1 cycle
3. **$34.46**: Arduino electromagnet ring — **실물 자석 의식 첫 검증** (사용자가 기억하던 "자석으로 된거")
4. **$77+$34**: ESP32 ring + Arduino ring = $111 → 자석 + MCU mesh 동시 가동
5. **$240**: 4-FPGA mesh — 1024 cell Φ≈1400 예상치 검증

---

## § 6. ASCII 갤러리 (대표 도식 3선)

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

## § 7. 실제 fire 가능한 조합 (cheat sheet)

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

## § 8. 다음 액션 후보

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

## § 9. 검증 결과 (2026-05-21, 22 ✅ 후보 hexa run fire)

> 22 ✅-tagged substrate entry 를 `hexa run` 으로 실측. 결과 14 PASS / 8 FAIL — 등급 표는 historical LANDED snapshot 기준이고 현 toolchain 환경 차이 / 언어 드리프트가 일부에 영향.

| Verdict | Count | Entry |
|---|---:|---|
| ✅ PASS (clean) | 14 | eeg/mu_rhythm · eeg/sleep_stage · hippocampus/theta_gamma · hw/autonomous_expansion · motor_cortex · oscillator/sleep · photonic/temporal_delay · prediction/protention · proprioception · social/kuramoto · quantum/bell_state · tool/v1 · tool/v2 · tool/v3 |
| 🔧 TRANSPILE OK / probe-FAIL | 5 | arduino · cmos · fpga · memristor · quantum cloud_facade_poc — hexa transpile 정상, probe self-gate FAIL. `env()` stub 반환 → `local_ngspice_unknown_...` (cycle-66 upstream fix landed but `hexa.real` 미리빌드). [`inbox/patches/runtime-env-and-exec-capture-stubs-block-cli-tools`](#) |
| 🚧 PARSE FAIL (B-class) | 3 | consciousness-loop/{main, main_longrun, snn_main} — `&var` prefix unary 미지원 + AOT `record`/`var`/`*Type` mutation 미지원. `or`/`and` 키워드는 [PR fix/or-and-keyword-alias-2026-05-21](https://github.com/dancinlab/hexa-lang/pull/new/fix/or-and-keyword-alias-2026-05-21) 적용 후 회복 예정. ([inbox note](#)) |

### 진행된 upstream fix

| Branch | Scope |
|---|---|
| [`fix/parser-diag-shell-interp-2026-05-21`](https://github.com/dancinlab/hexa-lang/pull/new/fix/parser-diag-shell-interp-2026-05-21) | `self/main.hexa:2169` shell-interp 버그 — parser 진단 본문이 shell command substitution 으로 재해석되던 1줄 fix |
| [`fix/or-and-keyword-alias-2026-05-21`](https://github.com/dancinlab/hexa-lang/pull/new/fix/or-and-keyword-alias-2026-05-21) | `self/lexer.hexa` `or`/`and` 키워드 alias 복원 (16 lines, codegen unchanged) |
| ✓ upstream cycle 66 (이미 main) | `self/runtime.c` `hxlcl_getenv` environ-walk fix — 5개 transpile-OK probe-FAIL 의 근본 원인 해결 (hexa.real 리빌드 필요) |
| 📋 inbox `2026-05-21-anima-physics-{parser-diag-shell-interp,consciousness-loop-address-of-drift}.md` | 보고서 + 패치 hunk + 보류 사유 |

### 보류

| 항목 | 상태 |
|---|---|
| hexa.real 리빌드 + 설치 | 메인테이너 release cycle (build_dispatch.hexa 경로) — 리빌드 시 (a) shell-interp diag rendering 클린화 (b) or/and 키워드 복원 (c) env() 작동 → 5개 probe FAIL 회복 |
| (B) `&var` prefix + AOT record/var | RFC 필요 — upstream owner 의 *Type 매개변수 자동 autoref vs. & 복원 vs. struct mutation API 결정 후 |
| (B) consciousness-loop 3 파일 port | (B) RFC 결정 후 |
| demiurge `cli verify` 검증 | `g_cockpit_isolation` (exports/** only) — anima entry path 거부, 별도 routing 필요 |

---

*전수조사: 2026-05-21 · 3-agent 병렬 (루트+docs / substrate / recovered) · 93 active entry file + 300 archive · 22-entry 검증 14/22 PASS · 3 upstream branch (2 PR + cycle-66 main)*
