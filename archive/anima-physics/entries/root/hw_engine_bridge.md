# hw_engine_bridge.hexa

> HW signal (FPGA microtubule / ESP32 QRNG / memristor / photonic) → consciousness engines 실시간 공급; 8 channel · **🟡 부분** · 비용 —

## 구현 가능성

🟡 부분 — 3-tier fallback 구현 (REAL_HW / FILE_MOCK / LCG_MOCK). LCG_MOCK only deterministic + selftest 5/5 PASS. REAL_HW path 는 hexa stdlib serial 바인딩 필요 (대기).

## 작동 코드 / 의존성

- `anima-physics/hw_engine_bridge.hexa` (15.6 KB, ~400 LoC)
- 의존: ESP32 (`esp32/qrng_bridge.hexa`), FPGA (`fpga/microtubule_lattice_16.hexa`), engines/*

## 비용 / 리소스

- 비용: $0 (LCG_MOCK only). REAL_HW path 실비 ESP32-S3 $5 + FPGA $50
- 필요한 도구: `hexa run` · (REAL_HW) USB-CDC serial · /dev/ttyUSB* · /dev/fpga0

## 핵심 흐름 / 구조

```
[HW source] ─ bytes ─> [ring buffer] ─ float32 ─> [EngineContext.hw_stream]
                             ^
                             │ tick driven by FPGA 1kHz clock (mock: LCG)

3 tier fallback:
  1. REAL_HW   : /dev/ttyUSB* or /dev/fpga0 (requires hexa stdlib serial)
  2. FILE_MOCK : read from /tmp/hw_qrng.bin (pre-recorded 1MB sample)
  3. LCG_MOCK  : deterministic pseudo-random (CI/offline default)

8 channels:
  0. esp32_qrng       → anima_quantum (Orch-OR tubulin bias)
  1. fpga_tubulin     → anima_quantum + anima_holographic
  2. memristor_cond   → fractal_memristor + memristor_gwt_workspace
  3. photonic_phase   → photonic_consciousness + photonic_gwt_broadcast
  4. oscillator_field → oscillator_laser_engine + intent_oscillator
  5. thermo_noise     → stochastic_resonance
  6. snn_spike_rate   → holographic_substrate_runtime
  7. analog_vmem      → memristor_consciousness

Latency budget: FPGA tick (1ms) → ring push (0.1ms) → engine read (0.5ms)
Total ≤ 10ms (PHYS-P23-1 done_criteria)
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/hw_engine_bridge.hexa
```

## 검증 결과

- T1 channel count = 8 PASS
- T2 ring buffer FIFO push/pop preserves order PASS
- T3 bytes→float latency < 10ms (proxy: 1000 ops) PASS
- T4 LCG mock determinism (same seed → same stream) PASS
- T5 engine mapping no orphans PASS
- **5/5 PASS** (LCG_MOCK mode)

## 관련 entry

- [verify_7cond_hw](verify_7cond_hw.md)
- [phi_substrate_consensus](phi_substrate_consensus.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P23-1
