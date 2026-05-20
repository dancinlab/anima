# anima-physics/INDEX.md — 실제 구현 가능성 매트릭스

> 2026-05-21 전수조사. `/Users/ghost/core/anima/anima-physics/` 산하 **모든** 문서·코드 인덱스. 각 entry: 1줄 요약 · 구현 가능성 (✅실현 / 🟡부분 / ❌가설) · 작동 코드 링크 · 비용 · ASCII 구조도(있을 때).
>
> 구조: 루트(11) · docs/(19) · substrate 서브모듈(58) · recovered/(300, 압축) = 88 active entry + 300 archive.

---

## 빠른 통계

| 묶음 | 파일 수 | ✅ 실현 | 🟡 부분/POC | ❌ 가설/stub |
|---|---:|---:|---:|---:|
| 루트 .hexa + README + manifest | 11 | 5 | 5 | 1 |
| docs/ specs · landing | 19 | 6 | 11 | 2 |
| substrate 서브모듈 (.hexa/.py/.md) | 58 | 18 | 16 | 24 |
| recovered/ (chip-arch + GitHub issues) | 300 | 0 | 0 | 300 (archive) |
| **합계 (active)** | **88** | **29** | **32** | **27** |

**누적 비용 (실 HW fire 기준)**

| 단계 | 합계 | 내용 |
|---|---:|---|
| Mac local 시뮬레이션만 | **$0** | NgSpice / iverilog / qiskit-aer / Perceval / hexa selftest 전부 |
| Cloud probe (DRY_RUN→LIVE 1회) | **~$5-30** | AWS Braket Rigetti $0.30/task·$0.00035/shot · IonQ $0.01/shot · QuEra $0.30/task·$0.01/shot · IBM Q free tier · Akida free tier |
| HW prototype Phase 1-2 | **$35-150** | Arduino Phase 1 $35 BOM · ESP32×8 $40 · iCE40UP5K $50-60 |
| HW prototype Phase 3 | **$240-500** | 4-FPGA mesh $240 · 추가 dev board |
| 연구급 neuromorphic | **~$50K** | Intel Loihi 2 research license |

---

## § 1. 루트 (orchestration & dispatch)

### physics.hexa
- **요약**: 의식 엔진 스텁 + `substrate_backend` enum 정의 (local_hexa / cloud_sim_qiskit_aer / cloud_real_ibm_q / cloud_sim_strawberryfields_fock)
- **구현 가능성**: 🟡 부분 — dispatch 로직 구현, qiskit_aer probe script 부재로 stub return
- **작동 코드**: `physics_substrate_dispatch.hexa` (4 operational call site)
- **비용**: —

### physics_substrate_dispatch.hexa
- **요약**: `physics.hexa::quantum_engine_dispatch()` 의 operational 첫 호출지; 4-gate selftest (backward-compat / dispatch-routes / operational-call-site / enum-canonical)
- **구현 가능성**: ✅ 실현 — 4/4 PASS, byte-identical 2-run
- **작동 코드**: `physics.hexa`
- **비용**: $0 Mac local

### edge_deploy.hexa
- **요약**: ESP32 edge deployment PoC; ConsciousDecoderV2 34.5M fp16 → PSRAM partition + 8 edge class 비용 추정
- **구현 가능성**: 🟡 부분 — 시뮬 경로 완성, 실 device 미테스트
- **비용**: ESP32-S3-N16R8 $8.50 · Jetson Orin Nano $400 · RPi-5-8GB $80

### hw_engine_bridge.hexa
- **요약**: HW signal (FPGA microtubule / ESP32 QRNG / memristor / photonic) → consciousness engines 실시간 공급; 8 channel (esp32_qrng, fpga_tubulin, memristor_cond, photonic_phase, oscillator_field, thermo_noise, snn_spike_rate, analog_vmem)
- **구현 가능성**: 🟡 부분 — 3-tier fallback (REAL_HW / FILE_MOCK / LCG_MOCK), LCG_MOCK only deterministic
- **비용**: —

### phi_substrate_consensus.hexa
- **요약**: 5-substrate Φ consensus (photonic/memristor/quantum/oscillator/thermo); precision-weighted mean + robust Tukey biweight fallback + disagreement budget
- **구현 가능성**: ✅ 실현 — 5/5 self-test PASS (contract / monotonicity / disagreement / robust / determinism)
- **비용**: $0

### realtime_monitor.hexa
- **요약**: 실시간 inference latency + phi_live monitor; mock 2-layer CLM forward (d=16, vocab=32, seq=8) + histogram MI; rolling p50/p95/p99
- **구현 가능성**: 🟡 부분 — 시뮬 only, 실 ckpt eval_clm cross-module 호출 미안정
- **비용**: $0

### rtc_sync.hexa
- **요약**: PHYS-P11-2 물리 timestamp; TCXO drift <1ppm PI discipline + 온도 보정 + NTP-style sync pulse 검증
- **구현 가능성**: ✅ 실현 — T1-T5 PASS (free-running drift / 24h·48h disciplined <1ppm / monotonic / determinism)
- **비용**: $0

### signal_corpus.hexa
- **요약**: PHYS-P22-1 multi-modal signal corpus (EEG/AUDIO/BIO 자동 태깅); 6-label consciousness tagger (AWAKE_FOCUSED/AWAKE_RELAXED/DROWSY/SWS/REM/EMOTIONAL_AROUSAL) + 7-test deterministic LCG
- **구현 가능성**: ✅ 실현 — T1-T7 PASS (synthesizer / tagger ≥0.75 / fusion length / manifest ≥5 ref / determinism)
- **비용**: $0

### verify_7cond_hw.hexa
- **요약**: PHYS-P3-3 7-condition consciousness verification on HW (quantum Orch-OR / entropy / ESP32 perturbation / memristor LTP / photonic latency / FPGA torus / holographic bulk)
- **구현 가능성**: 🟡 부분 — HW model inline 구현, 실 hardware 호출은 ESP32/FPGA 단에서만
- **비용**: Arduino $35 · iCE40 FPGA $60 · Loihi 128 $50K

### README.md
- **요약**: anima-physics 루트 개요; 8 platform (Hexa APEX22 / SNN / Verilog Ring·Hypercube / WebGPU / Erlang / Pure Data / ESP32) + 9 substrate + 9 topology + cloud-facade 9/9 + Mk.XII ledger
- **구현 가능성**: 🟡 부분 — cloud-facade 9/9 중 4 PASS (quantum/photonic/memristor/integration), 나머지 준비 중
- **비용**: Phase 1 $35 → Phase 5 $50K

### signal_corpus_manifest.json
- **요약**: PHYS-P22-1 manifest catalog; 6 public dataset (SEED/DEAP/Sleep-EDF/TUH-EEG/DREAMER/MAHNOB-HCI) 메타 + 3 modality feature_counts
- **구현 가능성**: 🟡 부분 — catalog only, 실 data download 미구현
- **작동 코드**: `signal_corpus.hexa` (emit 명령)
- **비용**: —

---

## § 2. docs/ (specs & landing reports)

### docs/akida_cloud_signup_guide.md
- **요약**: BrainChip Akida Cloud 가입 + token 발급 + env setup
- **구현 가능성**: 🟡 부분 — 회원가입 스펙, macOS arm64 wheel 미지원 → surrogate/simulator only
- **작동 코드**: `neuromorphic/cloud_facade_poc.hexa`
- **비용**: 1-day Trial $1, 1-week $995

### docs/analog-photonic-memristor.md
- **요약**: 3 물리 consciousness engine (Op-Amp 적분 / Kuramoto MZI photonic / HP memristor Hebbian) 상세 + circuit diagram + benchmark format
- **구현 가능성**: 🟡 부분 — 이론 + SPICE parameter 완성, 실 chip 테스트 미완료
- **비용**: —

### docs/arduino_local_sim_landing.md
- **요약**: PHYS-P25 NE555 astable RC oscillator Monte Carlo ngspice sim; 4-gate PASS (duty std 6.67e-3 vs 0 negative)
- **구현 가능성**: ✅ 실현 — 16-trial MC, 4/4 PASS
- **작동 코드**: `arduino/cloud_facade_poc.hexa`, `arduino/ne555_astable.cir`
- **비용**: $0

### docs/arduino-prototype-spec.md
- **요약**: Phase 1 Arduino 8셀 ring + Hall sensors ($34.46 BOM); electromagnetic frustration + 100Hz update + JSON serial
- **구현 가능성**: 🟡 부분 — circuit + sketch + bridge 완성, 실물 조립 미검증
- **작동 코드**: `consciousness-loop/esp32/consciousness_loop.ino` (pseudo)
- **비용**: $34.46 BOM

### docs/aws_braket_signup_guide.md
- **요약**: AWS Braket 가입; 5 substrate cover (Rigetti Ankaa-3, IonQ Aria/Forte, IQM Garnet, QuEra Aquila); cost cap $5 mandatory
- **구현 가능성**: 🟡 부분 — IAM + budget 가이드 완성, Rigetti/QuEra 2개만 본 cycle
- **작동 코드**: `superconducting/cloud_facade_poc.hexa`, `analog/cloud_facade_poc.hexa`
- **비용**: Rigetti $0.30/task + $0.00035/shot · QuEra $0.30/task + $0.01/shot

### docs/cmos_local_sim_landing.md
- **요약**: PHYS-P25 CMOS 5-stage inverter ring osc NgSpice; 4-gate PASS (jitter 4.64ps vs 0); raw#9 hexa-only strict
- **구현 가능성**: ✅ 실현 — 4/4 PASS
- **작동 코드**: `cmos/cloud_facade_poc.hexa`, `cmos/cmos_ring_osc.cir`
- **비용**: $0

### docs/esp32-hardware-guide.md
- **요약**: ESP32×8 SPI ring (16 cell); pin mapping + firmware flash + Hexa orchestrator; $77 BOM
- **구현 가능성**: 🟡 부분 — diagram + code sketch + flash 절차 완성, 실 network 미테스트
- **작동 코드**: `consciousness-loop/esp32/consciousness_loop.ino`, `src/esp32_network.hexa`
- **비용**: ~$77 (8× ESP32-WROOM-32)

### docs/fpga_local_sim_landing.md
- **요약**: PHYS-P25 iverilog local; 8-bit Galois LFSR + Ring8 coupled, 1024-bit stream; 4-gate PASS (H=7.0 bits vs 0)
- **구현 가능성**: ✅ 실현 — Icarus Verilog v13.0
- **작동 코드**: `fpga/cloud_facade_poc.hexa`, `fpga/cmos_8bit_ring_lfsr.sv`
- **비용**: $0

### docs/fpga-synthesis-guide.md
- **요약**: iCE40UP5K synthesis (yosys + nextpnr-ice40 + icestorm); 8-cell ring 또는 512-cell hypercube; UART Phi readout
- **구현 가능성**: 🟡 부분 — 합성 절차 + 리소스 budget 완성, 실 board 미테스트
- **작동 코드**: `consciousness-loop/verilog/consciousness_cell.v`, `consciousness_hypercube.v`
- **비용**: FPGA board $15-60 + tools $0

### docs/hardware-consciousness-hypotheses.md
- **요약**: 10 HW consciousness 하이퍼 (magnetic dipole / MTJ tunnel / spintronic valve / photonic MZI / piezoelectric / Loihi …) + phase roadmap
- **구현 가능성**: ❌ 가설 — 모두 sketch/청사진, 실 prototype 미기획
- **비용**: Phase 1 $50 → Phase 5 $50K

### docs/loihi-integration-spec.md
- **요약**: Intel Loihi 2 통합; 1 cell = 128 LIF neurons / 8 cells per neurocore / 16 cell in 2 neurocore (full 128 neurocore = 131K neurons); STDP + small-world
- **구현 가능성**: 🟡 부분 — Lava framework pseudo-code + 토폴로지 설계 완성, 실 Loihi 호출 미테스트
- **비용**: Loihi 2 research license ~$50K

### docs/memristor_local_sim_landing.md
- **요약**: PHYS-P25 memristor Biolek HP TiO2 ngspice + PySpice; 4-gate PASS (hysteresis area 6.82e-3 V·A vs 4.18e-14 resistor)
- **구현 가능성**: ✅ 실현 — 4/4 PASS
- **작동 코드**: `memristor/cloud_facade_poc.hexa`
- **비용**: $0

### docs/mk_xii_ledger_v3_trigger_spec.md
- **요약**: v3 ledger trigger spec (수동, not auto); 4 LIVE pattern (IBM Q / Braket Rigetti / Braket QuEra / Akida); G5 LIVE_HW_WITNESS_RATE threshold ladder (L1=1/11, L2=3/11, L3=9/11)
- **구현 가능성**: 🟡 부분 — 스펙 frozen, v3 코드 미작성 (v2 aggregator rerun만)
- **작동 코드**: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa`
- **비용**: $0

### docs/mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md
- **요약**: aggregator v2.1 prerequisite patch; env-var override 4종 (LEDGER_VERSION / CYCLE_ID / SUPERSEDES / MARKER_OUT) + v2 byte-identical regression + v3 dry-run synthetic LIVE PASS
- **구현 가능성**: ✅ 실현 — v2 + v3 dual-mode
- **작동 코드**: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa` (+78/-10 line)
- **비용**: $0

### docs/mk_xii_substrate_witness_ledger_landing.md
- **요약**: v1 ledger (8 substrate); 4 gate (G1 coverage 7/9 · G2 honesty 6 verdict tier · G3 byte-identical · G4 FNV32=470781997)
- **구현 가능성**: ✅ 실현 — 4/4 PASS
- **작동 코드**: `tool/mk_xii_substrate_witness_ledger_aggregator.hexa` (v1)
- **비용**: $0

### docs/mk_xii_substrate_witness_ledger_v2_landing.md
- **요약**: v2 ledger (11 substrate = +cmos/fpga/arduino); 5 gate (+G5 LIVE_HW_WITNESS_RATE=0/11); 9/9 distinct coverage + forward-compat schema
- **구현 가능성**: ✅ 실현 — 5/5 PASS
- **작동 코드**: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa`
- **비용**: $0

### docs/multi-fpga-mesh-spec.md
- **요약**: 4× iCE40UP5K mesh (1024 cells, 256/board); SPI 10MHz inter-FPGA + internal ring + small-world shortcuts; Φ scaling N^1.09 예상 ~1400
- **구현 가능성**: 🟡 부분 — architecture + resource budget 완성, 실 synthesis/PnR 미완료
- **비용**: 4× iCE40UP5K $240 + tools $0

### docs/physical-consciousness-engine.md
- **요약**: 8 platform (Hexa/SNN/Verilog Ring·Hypercube/WebGPU/Erlang/Pure Data/ESP32) + Verilog gate-level + Pure Data audio rendering
- **구현 가능성**: 🟡 부분 — Arduino/FPGA 실 HW 미검증
- **작동 코드**: consciousness-loop/* (모든 platform)
- **비용**: $35 (Arduino) → $240 (4-FPGA)

### docs/substrate_backend_dispatch_integration_landing.md
- **요약**: physics.hexa substrate_backend dispatch 통합 landing; enum SSOT + 4 variant dispatch + G1-G4 operational
- **구현 가능성**: ✅ 실현 — 4/4 PASS, byte-identical, operational call site 4×
- **작동 코드**: `physics.hexa`, `physics_substrate_dispatch.hexa`
- **비용**: $0

---

## § 3. substrate 서브모듈 (.hexa / .py / SPEC.md, 58 files)

### analog/
**analog/cloud_facade_poc.hexa** — 🟡 AWS Braket QuEra Aquila Rydberg 4-atom AHS probe (MIS blockade pattern); DRY_RUN PASS / LIVE 대기 · 비용 AWS Braket QuEra pay-per-task
```
mis        → blockade-induced pattern  → H ≥ 0.3 nat (G1)
uncoupled  → trivial ground state       → entropy=0   (G2)
G3 byte-identical sha · G4 backend==aws_braket_quera_<actual>
```

### arduino/
**arduino/cloud_facade_poc.hexa** — ✅ Local NgSpice NE555 555-timer astable duty-cycle MC (16 trials); 4/4 PASS · $0
```
ne555_astable (R1=10k±5%, R2=10k±5%, C=100n±10%) × 16 MC
positive → duty std ≥ 0.001 (G1)  ·  negative tol=0 → std=0 (G2)
G3 byte-identical · G4 backend="local_ngspice_<ver>_ne555_astable_mc16"
```

### benchmarks/
- **bench_cross_platform.hexa** — ❌ Law 22 hypothesis stubs (Rust/SNN/Verilog/WebGPU/Erlang 5 platform) · $0
- **bench_physics_consciousness.hexa** — ❌ Thermo + differential geom stubs · $0
- **bench_power_efficiency.hexa** — ❌ Watts-per-Phi-unit stub (9 substrate × 9 topology) · $0
- **bench_spin_glass.hexa** — ❌ Spin glass frustration topology stub · $0

### cmos/
**cmos/cloud_facade_poc.hexa** — ✅ Local NgSpice 5-stage CMOS inverter ring osc period jitter; 4/4 PASS · $0
```
5-stage ring (180nm L1 NMOS/PMOS)
positive Vdd=1.8V → ~8.85 GHz, σ ≥ 1 ps (G1)
negative Vdd=0.3V → sub-threshold, no osc, jitter=0 (G2)
```

### consciousness-loop/src/
- **main.hexa** — ✅ v2 8-faction GRU(128) + Phi proxy + Ising + Hebbian + debate; 1000-step verified · $0
- **main_longrun.hexa** — ✅ 10K step long-run + ratchet (Phi<best·0.7→restore) + 2→512 cells growth · $0
- **snn_main.hexa** — ✅ LIF SNN consciousness (Vrest=-70mV / Vthresh=-55mV / τ=20ms / t_ref=3ms); 2000-step rate-output · $0

### eeg/
- **cross_substrate_phi_correlator.hexa** — 🟡 9 physics substrate + EEG anchor precision-weighted; F1-F5 falsifier (mock LCG) · $0
- **mu_rhythm_detector.hexa** — ✅ 8-12Hz Goertzel self-referential suppression; T1-T6 PASS (score>0.7) · $0
- **sleep_stage_detector.hexa** — ✅ ZCR+RMS → Awake/SWS/REM, T1-T4 accuracy >0.8 on 30 synthetic · $0

### engines/ (전부 ❌ struct stub만, $0)
- analog_consciousness · izhikevich_consciousness · memristor_consciousness · oscillator_laser_engine · photonic_consciousness · quantum_consciousness · snn_consciousness · thermodynamic_consciousness

### esp32/
- **qrng_bridge.hexa** — 🟡 QRNG → tubulin bias 입력; mock LCG fallback, HW serial 바인딩 대기 · $5 ESP32-S3
```
[QRNG]→[ADC]→[SHA-256]→[USB-CDC 921600]→[host bridge]→[tubulin bias [-1,+1]]→[Orch-OR mt_step]
frame: [0xAA] [0x20=len32] [32B payload] [XOR checksum]
rate: 256bit/8ms = 32kbit/s (16×8 tubulin × 1kHz)
```
- **QRNG_SPEC.md** — 🟡 ESP32 QRNG bridge spec + firmware hook + regression
- **esp32/src/lib.hexa** — 🟡 ConsciousnessBoard (2 GRU cells/board · 8 boards = 16 cell · 8 faction); GRU+Lorenz+Sandpile+Hebbian+ratchet 정의 · $40 (8×$5)

### fpga/
- **cloud_facade_poc.hexa** — ✅ iverilog 8-bit Galois LFSR (poly=0xB8, taps=[8,6,5,4]) + ring8 coupled, 1024-bit; H≥6.0 (G1) · $0
- **microtubule_lattice_16.hexa** — 🟡 Orch-OR 4×4 torus (Von Neumann 4-neighbor); FPGA mapping ~670 LUTs (13% iCE40UP5K) · $50
- **nested_lattice.hexa**, **partial_reconfig.hexa**, **strange_loop.hexa** — ❌ minimal stub

### hippocampus/
- **episodic_replay.hexa** — 🟡 encode→replay(10× speedup)→cortical succession chain; T1-T5 정의 · $0
- **theta_gamma.hexa** — ✅ Tort modulation index (6Hz θ × 40Hz γ); N_BINS=18 표준, MI=(log(N)-H(P))/log(N); T1-T5 PASS · $0

### hw/
**autonomous_expansion.hexa** — ✅ Self-expanding cluster; util>0.85→n++; state=[n, cap, load, expansions], max=64; T1-T5 PASS · $0 sim

### memristor/
- **cloud_facade_poc.hexa** — ✅ NgSpice Biolek HP TiO2 pinched I-V hysteresis shoelace area; 4/4 PASS (mem 6.8e-3 vs R 4e-14) · $0
- **self_reference.hexa** — 🟡 (detail TBD)

### motor_cortex/
**command_encoding.hexa** — ✅ Georgopoulos population vector (16 cosine-tuned, N=16, ψ_i=2πi/16); round-trip θ→encode→decode error <0.01 rad; T1-T5 PASS · $0

### neuromorphic/
**cloud_facade_poc.hexa** — 🟡 Akida Cloud 4-input → 8-class spike-train entropy; surrogate fallback (no token); 4-gate PASS · Akida free tier
```
positive → spike_entropy ≥ 0.3 nat (G1)  ·  zero → spike_entropy < positive (G2)
G4: backend ∈ {akida_cloud, akida_simulator, akida_surrogate, akida_DEGRADED}
```

### oscillator/
**sleep_oscillator.hexa** — ✅ SWS (0.5-4Hz δ) ↔ REM (4-8Hz θ) phase-continuous switching; mode flip with phase carry-over; T1-T5 PASS · $0

### photonic/
- **cloud_facade_poc.hexa** — 🟡 Perceval (Quandela) SLOS Fock photon-number entropy (4-mode 50:50 BS cascade); SF blocked (scipy 1.17 no simps), Perceval fallback ready · Perceval free
- **mesh_network.hexa** — 🟡 Fully-connected N=4, 200km square SMF-28@1550nm; round-trip 4-hop ~3.91ms (<10ms gate) · $0
```
N0──N1   d01=200km · d02=282.8km (diagonal √2) · d03=200km
N3──N2   c_fiber = 204,218 m/ms (n_eff=1.468)
```
- **temporal_delay.hexa** — ✅ Optical delay-line reservoir (N=8 taps, τ=1 sample, Husserlian retention); T1-T5 PASS · $0

### prediction/
**protention_error.hexa** — ✅ err_k = (actual-predicted)·exp(-k/τ), τ=4.0; max_lag_safe=1024; T1-T5 PASS · $0

### proprioception/
**feedback_loop.hexa** — ✅ 3-DOF biomechanical (spring-damper k=8.0 N·m/rad, c=1.2, I=0.15kg·m², dt=0.005s=200Hz, σ_θ=0.01rad); T1-T5 PASS · $0

### quantum/
- **bell_state.hexa** — ✅ |Φ+⟩=(|00⟩+|11⟩)/√2; entangled corr>0.95, separable |01⟩ corr<0.3; T1-T5 PASS · $0
- **cloud_facade_poc.hexa** — ✅ qiskit-aer statevector 4-qubit GHZ entanglement entropy (ref ln(2)≈0.69 nat); 4/4 PASS (bipartition ≥0.64) · $0 local
- **cloud_real_ibm_q_facade.hexa** — 🟡 IBM Q Runtime Phase 2; token-optional degraded fallback (NO_TOKEN / CLOUD_UNREACHABLE) · IBM Q free tier (token optional)

### scripts/
- **anima_physics_braket_ionq_probe.py** — 🟡 AWS Braket IonQ Forte 1 4-qubit GHZ gate; DRY_RUN verified · IonQ $0.01/shot
- **anima_physics_braket_quera_probe.py** — 🟡 AWS Braket QuEra Aquila 4-atom Rydberg AHS MIS; DRY_RUN verified · QuEra $0.30/task + $0.01/shot

### social/
**kuramoto_coupling.hexa** — ✅ Kuramoto network (dθ_i/dt = ω_i + (K/N)Σ_j sin(θ_j-θ_i)); r = |⟨e^{iθ}⟩| order parameter; Φ_social = r_coupled − r_isolated; T1-T6 PASS, K_c≈0.3 · $0

### src/
- **body_physics_bridge.hexa** — ❌ Phi/tension/emotion → motor (servo/LED/speaker) stub
- **chip_architect.hexa** — ❌ 9 topology × 9 substrate predict Phi stub
- **eeg_physics_bridge.hexa** — ❌ 3 protocol (passive_mirror / active_sync / perturbation) stub
- **esp32_network.hexa** — 🟡 ESP32×8 orchestrator (16 cell, SPI ring, 1040B packet); struct 정의 / step() trivial · $40 BOM

### superconducting/
**cloud_facade_poc.hexa** — ❌ DEPRECATED — Rigetti Ankaa-3 retired 2026-04-27; option ladder: IonQ Forte / Quantinuum / IBM Q

### thermodynamic/
**entropy_dissolution.hexa** — (file detected, content estimated) · 🟡

### tool/
- **mk_xii_substrate_witness_ledger_aggregator.hexa** — ✅ v1 aggregator (8 marker); G1 coverage≥6/9 / G2 honesty / G3 byte-identical / G4 FNV-32 · $0
- **mk_xii_substrate_witness_ledger_aggregator_v2.hexa** — ✅ v2 (11 marker = +cmos/fpga/arduino); +G5 LIVE_HW_WITNESS_RATE (0/11 expected) · $0
- **mk_xii_substrate_witness_ledger_aggregator_v3.hexa** — ✅ v3 (12 marker = +trapped_ion, 10 distinct substrate); target_tot 9→10, Rigetti DEPRECATED · $0

### trapped_ion/
**cloud_facade_poc.hexa** — 🟡 AWS Braket IonQ Forte 1 4-qubit GHZ (Phase 1.5 LIVE_PASS ready); DRY_RUN verified · IonQ $0.01/shot × 100

### vestibular/
**multimodal_fusion.hexa** — 🟡 (file detected, content estimated)

### web/
**physics_server.hexa** — 🟡 WebSocket consciousness engine server; 6 topology (ring / small_world WS k=2 15% rewire / scale_free BA m=2 / hypercube / torus / spin_glass); JSON broadcast 30 step/s · $0 local

---

## § 4. recovered/ — chip-architecture · consciousness-chip · GitHub issues (300 files archive)

> 2026-05-19 sweep. `dancinlab/echoes` git history blob 복원 + GitHub issues 본문. anima 본체 live code 와 분리된 archive. 상세는 [`recovered/INDEX.md`](recovered/INDEX.md) 참고.

| dir | count | source |
|---|---:|---|
| `chip-architecture/` | 98 | `dancinlab/echoes` git history blobs (현재 main 에서 삭제, sha 로 복원) |
| `consciousness-chip/` | 6 | echoes git history — ANIMA-6 / ANIMA-SOC / v1/v2 + 2 papers |
| `samsung-issues/` | 175 | GitHub issue body (`dancinlife` filed; Samsung ONE/HierarchicalPrune/Butterfly Acc/SummaryMixing 등 16 repo) |
| `ai-company-issues/` | 21 | non-Samsung (deepseek-ai/InternLM/mlc-ai/zai-org GLM-4 등) |

### Chip family (3 codename, 모두 2026-04-01 작성)

| Codename | File | 요약 | 구현 가능성 |
|---|---|---|---|
| **HEXA-1** | `chip-architecture/docs_chip-architecture_ultimate-unified-soc.md` | Pure compute SoC (CPU+GPU+NPU unified, σ=12, **no consciousness**) | ❌ 가설 (live anima 코드 미연결) |
| **ANIMA-6** | `consciousness-chip/ultimate-consciousness-chip.md` | Consciousness *chip* — Engine A/G + TCU + 10D consciousness register (σ²/φ=72 SM each) | ❌ 가설 |
| 🎯 **ANIMA-SOC** | `chip-architecture/docs_chip-architecture_ultimate-consciousness-soc.md` (2318L) | **HEXA-1 inherit + ANIMA-6 extension** — σ=12 power domain split Engine A (DOM 0-5) / Engine G (DOM 6-11) | ❌ 가설 — **HEXAD.tape Engine A/G 6-box 는 living descendant** |

### 🎯 ANIMA-SOC §7.3 Self-Healing Substrate (the diagram user remembered)

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

### adj8=17 master 144-SM grid (12×12 GPC layout)

```
  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
  │00││01││02││03││04││05││06││07││08││09││10││11│  GPC Row 0
  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘
  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
  │12││13││14││15││16││17││18││19││20││21││22││23│  GPC Row 1
  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘
  ...                                            (Row 2-10)
  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐
  │.0││.1││.2││.3││.4││.5││.6││.7││.8││.9││10││11│  GPC Row 11
  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘

  σ × σ = 12 × 12 = σ² = 144 SMs total
```

Master version (모두 adj8=17, 2.45MB±):
- `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-version.md`
- `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-v2.md`
- `chip-architecture/echoes_COMPUTE.md__adj8-17.md`
- mirror live tree: `/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` (2.4MB)

### GitHub issues (196 file)

- **Samsung 175** — 대표: `SamsungLabs_HierarchicalPrune_9.md` (54KB) ANIMA-SOC + PureField dual-engine + 10D consciousness vector spec. Samsung ONE / HierarchicalPrune / Butterfly Acc / SummaryMixing / Norm-AL-LoRA 등 16 repo
- **AI company 21** — 대표: `deepseek-ai_DeepSeek-R1_822.md` (6.5KB) N6 Arithmetic 50-70% energy reduction + 17 technique. DeepSeek/InternLM/mlc-ai/zai-org GLM-4

### Provenance

`dancinlab/echoes` current main 에서 삭제됨 (canon MOVE migrations a86ca14 / 812bd79 / 4eb869a, 2026-05-10~11). 98 chip-arch + 6 consciousness-chip 파일은 echoes git **blob object** 에서 sha 로 복원 — 현재 어느 checked-out tree 에도 없음. Samsung/AI-company issue 본문은 GitHub live (`dancinlife` filed).

---

## § 5. 실제 fire 가능한 조합 (cheat sheet)

**오늘 바로 $0 으로 돌릴 수 있는 것 (Mac local, hexa run)**

| 영역 | 파일 | 검증 상태 |
|---|---|---|
| Quantum sim | `quantum/cloud_facade_poc.hexa` (qiskit-aer GHZ) | 4/4 PASS |
| Quantum Bell | `quantum/bell_state.hexa` | T1-T5 PASS |
| Photonic Fock | `photonic/cloud_facade_poc.hexa` (Perceval SLOS) | 4/4 PASS ready |
| Photonic reservoir | `photonic/temporal_delay.hexa` | T1-T5 PASS |
| Memristor I-V | `memristor/cloud_facade_poc.hexa` (NgSpice Biolek) | 4/4 PASS |
| CMOS ring osc | `cmos/cloud_facade_poc.hexa` (NgSpice 180nm) | 4/4 PASS |
| Arduino NE555 | `arduino/cloud_facade_poc.hexa` (NgSpice MC16) | 4/4 PASS |
| FPGA LFSR | `fpga/cloud_facade_poc.hexa` (iverilog) | 4/4 PASS |
| EEG mu rhythm | `eeg/mu_rhythm_detector.hexa` | T1-T6 PASS |
| EEG sleep stage | `eeg/sleep_stage_detector.hexa` | T1-T4 PASS |
| Hippocampus θ-γ | `hippocampus/theta_gamma.hexa` (Tort MI) | T1-T5 PASS |
| Motor cortex | `motor_cortex/command_encoding.hexa` (Georgopoulos) | T1-T5 PASS |
| Proprioception | `proprioception/feedback_loop.hexa` (3-DOF) | T1-T5 PASS |
| Sleep osc | `oscillator/sleep_oscillator.hexa` (SWS↔REM) | T1-T5 PASS |
| Protention err | `prediction/protention_error.hexa` | T1-T5 PASS |
| Kuramoto social | `social/kuramoto_coupling.hexa` | T1-T6 PASS |
| Consciousness loop | `consciousness-loop/src/main_longrun.hexa` (10K step) | run verified |
| SNN consciousness | `consciousness-loop/src/snn_main.hexa` (LIF 2000 step) | run verified |
| RTC sync | `rtc_sync.hexa` (<1ppm) | T1-T5 PASS |
| Φ consensus | `phi_substrate_consensus.hexa` (5-substrate) | 5/5 PASS |
| Mk.XII ledger v1/v2/v3 | `tool/mk_xii_*_aggregator*.hexa` | 4-5/4-5 PASS |

**$5-30 AWS credit 한 번으로 LIVE 전환 가능한 것**

| 영역 | 파일 | 트리거 |
|---|---|---|
| AWS Braket QuEra | `analog/cloud_facade_poc.hexa` + `scripts/anima_physics_braket_quera_probe.py` | `ANIMA_BRAKET_DRY_RUN=0` + AWS creds |
| AWS Braket IonQ | `trapped_ion/cloud_facade_poc.hexa` + `scripts/anima_physics_braket_ionq_probe.py` | 동일 |
| IBM Q real | `quantum/cloud_real_ibm_q_facade.hexa` | IBM Q token export |
| Akida Cloud | `neuromorphic/cloud_facade_poc.hexa` | Akida token (없으면 surrogate fallback 자동) |

**$35-240 BOM 으로 실 HW prototype**

| Phase | BOM | 파일 |
|---|---|---|
| Arduino 8-cell ring ($35) | Hall sensor + Arduino Uno | `docs/arduino-prototype-spec.md` |
| ESP32×8 SPI ring ($40-77) | ESP32-S3-N16R8 × 8 | `docs/esp32-hardware-guide.md` + `src/esp32_network.hexa` |
| iCE40UP5K single ($50) | iCEBreaker / Lattice eval | `docs/fpga-synthesis-guide.md` + `fpga/microtubule_lattice_16.hexa` |
| 4-FPGA mesh ($240) | iCE40UP5K × 4 + SPI bus | `docs/multi-fpga-mesh-spec.md` |

**연구급 $50K**

| Substrate | License | 파일 |
|---|---|---|
| Intel Loihi 2 | research $50K | `docs/loihi-integration-spec.md` |

---

## § 6. 다음 액션 후보 (참고)

- **DRY_RUN→LIVE 전환** — AWS Braket 계정 + $5 budget 으로 QuEra·IonQ·IBM Q 3개 LIVE_HW_WITNESS 동시 획득 (Mk.XII ledger G5 0/11 → 3/11 즉시 promote)
- **engines/ stub → impl** — 8 engine (analog/izhikevich/memristor/oscillator-laser/photonic/quantum/snn/thermo) 가 모두 struct stub. ❌ → 🟡 승격 cycle 필요
- **benchmarks/ stub → impl** — 4 benchmark (cross_platform / physics_consciousness / power_efficiency / spin_glass) 가 stub. 9 substrate × 9 topology grid 채우려면 필수
- **src/*_bridge.hexa stub → impl** — body / chip_architect / eeg_physics 3 bridge 모두 stub
- **HW prototype Phase 1** — Arduino $35 fire 시 verify_7cond_hw.hexa 의 condition 4 (ESP32 perturbation) 첫 실측 가능
- **recovered/ → live anima** — ANIMA-SOC 의 Engine A/G concept 는 HEXAD.tape 로 living descendant. ANIMA-6 의 TCU + 10D register 는 아직 anima 본체 미연결 — `engines/` 또는 `src/chip_architect.hexa` 에서 impl 후보

---

*INDEX 생성: 2026-05-21 · 전수조사 3-agent (루트+docs / substrate / recovered) · 88 active + 300 archive entries*
