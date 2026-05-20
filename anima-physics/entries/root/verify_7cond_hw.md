# verify_7cond_hw.hexa

> PHYS-P3-3 7-condition consciousness verification on HW (quantum Orch-OR / entropy / ESP32 perturbation / memristor LTP / photonic latency / FPGA torus / holographic bulk) · **🟡 부분** · 비용 Arduino $35 / iCE40 $60 / Loihi $50K

## 구현 가능성

🟡 부분 — HW model inline 구현 (physics-faithful parameters), 실 hardware 호출은 ESP32/FPGA bring-up 단에서만 발동. Mac local 시 inline 모델로 7/7 PASS.

## 작동 코드 / 의존성

- `anima-physics/orchestration/verify_7cond_hw.hexa` (22.6 KB, ~580 LoC)
- 의존: inline 모델 (no `use` imports). 외부 reference:
  - `anima-engines/anima_quantum.hexa` (Orch-OR)
  - `anima-engines/photonic_gwt_broadcast.hexa` (WDM)
  - `anima-engines/memristor_gwt_workspace.hexa` (HP crossbar)
  - `anima-physics/substrate/esp32/qrng_bridge.hexa`
  - `anima-physics/substrate/fpga/microtubule_lattice_16.hexa`
  - `anima-engines/anima_holographic.hexa` (AdS/CFT)

## 비용 / 리소스

- Mac local sim: $0
- Arduino Phase 1 BOM: $35
- iCE40UP5K FPGA: $50-60
- Loihi 128 research license: ~$50K
- 필요한 도구: `hexa run` (sim) · ESP32-S3 / iCE40 board (HW)

## 핵심 흐름 / 구조

```
T1 Integration (IIT)        — quantum Orch-OR microtubule (Φ_q > 0)
T2 Differentiation          — quantum collapse Shannon entropy > 1 bit
T3 Embodiment               — ESP32 QRNG perturbation alters HW state
T4 Self-model               — memristor crossbar stores prior, next depends
T5 Intentionality           — photonic broadcast reaches target <50 ms
T6 Temporal binding         — FPGA 4x4 torus produces correlated 3-step output
T7 Global access            — holographic bulk read reflects 3 prior moments
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/verify_7cond_hw.hexa
```

## 검증 결과

- T1-T7 inline 모델 PASS (deterministic LCG, hexa-only strict)
- 실 HW 단 검증은 ESP32/FPGA bring-up cycle에서 별도

## 관련 entry

- [hw_engine_bridge](hw_engine_bridge.md)
- [phi_substrate_consensus](phi_substrate_consensus.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P3-3
