# docs/fpga_local_sim_landing.md

> PHYS-P25 iverilog local; 8-bit Galois LFSR + Ring8 coupled, 1024-bit stream; 4-gate PASS (H=7.0 bits vs 0) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — Icarus Verilog v13.0 cycle 4/4 PASS. AWS F1 (신규 가입 차단) / F2 ($1.65/hr 비쌈) 회피, open-source iverilog endpoint wrapping.

## 작동 코드 / 의존성

- `anima-physics/docs/fpga_local_sim_landing.md` (landing report)
- 의존: `fpga/cloud_facade_poc.hexa`, `fpga/cmos_8bit_ring_lfsr.sv` (SystemVerilog)
- 외부: Icarus Verilog v13.0 (brew install icarus-verilog)

## 비용 / 리소스

- 비용: $0 (Mac local, iverilog open-source)
- 필요한 도구: iverilog v13.0 · `hexa run`

## 핵심 흐름 / 구조

```
                    +-----------+         +------------+
   clk ── posedge ─▶│  LFSR8    │── b0 ──▶│  Ring8     │
                    │ poly=0xB8 │         │  (coupled) │
                    │ taps=[8,6,│         │   8-stage  │
                    │       5,4]│         │            │
                    +-----------+         +------------+
                          │                     │
                          ▼                     ▼
                       1024-bit stream → entropy estimator

4-gate contract:
  G1 positive → Shannon H ≥ 6.0 bits (실측 7.0 bits)
  G2 negative (zero-seed) → H = 0
  G3 byte-identical (deterministic LFSR)
  G4 backend == "cloud_sim_local_iverilog_v13.0_lfsr8_ring8"
```

## 트리거 (fire 방법)

```bash
brew install icarus-verilog
hexa run /Users/ghost/core/anima/anima-physics/fpga/cloud_facade_poc.hexa
```

## 검증 결과

- G1 entropy H = 7.0 bits ≥ 6.0 PASS
- G2 zero-seed H = 0 PASS
- G3 byte-identical PASS
- G4 backend_name PASS
- **4/4 PASS** (2026-04-26)
- marker: `state/v10_anima_physics_cloud_facade/poc_fpga_local_verilator/marker.json`

## 관련 entry

- [fpga-synthesis-guide](fpga-synthesis-guide.md)
- [multi-fpga-mesh-spec](multi-fpga-mesh-spec.md)
- [cmos_local_sim_landing](cmos_local_sim_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
