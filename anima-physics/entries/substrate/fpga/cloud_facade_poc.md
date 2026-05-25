# fpga/cloud_facade_poc.hexa

> Local iverilog 8-bit Galois LFSR (poly=0xB8, taps=[8,6,5,4]) + ring8 counter coupled, 1024-bit Shannon entropy · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 4/4 PASS (H≥6.0 G1). Icarus Verilog v13.0 deterministic on identical RTL+seed → byte-identical sha. raw#9 hexa-only strict (no .py/.sh; exec(iverilog/awk/jq/sha) only). AWS F1 차단 + F2 비싸 ($1.65/hr) → local iverilog facade.

## 작동 코드 / 의존성

- 원본: `fpga/cloud_facade_poc.hexa` (300 LoC)
- RTL: `fpga/cmos_8bit_ring_lfsr.sv` (SystemVerilog testbench)
- 외부 의존: iverilog v13.0 (brew install icarus-verilog)
- enum: substrate_backend ∈ {"local_hexa", "cloud_sim_local_iverilog", "cloud_real_aws_fpga"}

## 비용 / 리소스

- $0 Mac local (iverilog open-source)
- Phase 2 AWS F2: $1.65/hr (대기)

## 핵심 흐름 / ASCII

```
8-bit Galois LFSR (poly_mask=0xB8, taps=[8,6,5,4]) + 8-bit ring counter coupled
1024 clock cycles → 1024-bit stream → 128 × 8-bit symbol Shannon entropy (max=8.0)

positive  rst released after 2 cycles → max-length seq → H ≈ 7.0  (G1)
negative  rst held forever → bit_out=0 stuck → H = 0.0           (G2)
G3 sha256(positive run1) == sha256(positive run2) byte-identical
G4 backend == "local_iverilog_<ver>_lfsr8_galois_ring8_coupled"

SEED_LFSR = 0x42 · SEED_RING = 0xA5 · POLY = 0xB8
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/fpga/cloud_facade_poc.hexa
hexa run anima-physics/fpga/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS (G1 H=7.0 bits vs 0, G2 sign-flip, G3 byte-identical, G4 backend)
- docs/fpga_local_sim_landing.md: H=7.0 positive vs 0 negative
- iverilog determinism 2-run

## 관련 entry

- [fpga/microtubule_lattice_16.md](./microtubule_lattice_16.md) — 4×4 torus Orch-OR
- [fpga/nested_lattice.md](./nested_lattice.md)
- [fpga/partial_reconfig.md](./partial_reconfig.md)
- [fpga/strange_loop.md](./strange_loop.md)
- [arduino/cloud_facade_poc.md](../arduino/cloud_facade_poc.md) — NgSpice sibling

## 출처

- README § 3 fpga/
- docs/fpga_local_sim_landing.md
- docs/fpga-synthesis-guide.md (iCE40UP5K)
