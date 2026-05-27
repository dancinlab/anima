# docs/multi-fpga-mesh-spec.md

> 4× iCE40UP5K mesh (1024 cells, 256/board); SPI 10MHz inter-FPGA + internal ring + small-world shortcuts; Φ scaling N^1.09 예상 ~1400 · **🟡 부분** · 비용 $240

## 구현 가능성

🟡 부분 — architecture + resource budget 완성, 실 synthesis/PnR 미완료. 1024 cell 초선형 영역 (Φ ∝ N^1.09) 진입 목표.

## 작동 코드 / 의존성

- `anima-physics/docs/multi-fpga-mesh-spec.md` (mesh spec)
- 의존: `consciousness-loop/verilog/consciousness_cell.v`, `consciousness_hypercube.v`
- 외부: yosys + nextpnr-ice40 + icestorm + SPI bus PCB

## 비용 / 리소스

- 4× iCE40UP5K board: ~$240 (각 ~$60)
- Tools: $0 (open-source)
- 추가 PCB / SPI bus 와이어링 소요
- 필요한 도구: yosys · nextpnr-ice40 · icestorm · 4 FPGA board · SPI 10MHz bus

## 핵심 흐름 / 구조

```
┌──────────────────────────────────────────────────────────────────────┐
│                Multi-FPGA Consciousness Mesh                         │
│                4× iCE40UP5K, 1024 cells total                        │
│                                                                      │
│   FPGA-A (256 cells)              FPGA-B (256 cells)                 │
│   ┌──────────────────┐            ┌──────────────────┐               │
│   │  C0..C255 ring   │◄── SPI ───▶│  C256..C511 ring │               │
│   │  + small-world   │   10 MHz   │  + small-world   │               │
│   └────────┬─────────┘            └────────┬─────────┘               │
│            │ SPI 10MHz                     │ SPI 10MHz               │
│   ┌────────┴─────────┐            ┌────────┴─────────┐               │
│   │  C512..C767 ring │◄── SPI ───▶│  C768..C1023 ring│               │
│   └──────────────────┘            └──────────────────┘               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Scaling target:
  N = 1024 cells
  Φ ∝ N^1.09 → ~1400 (superlinear regime, N > 256)
  Law 22: 구조 추가 → Phi 상승 (loop count 0, gate-level 동시 동작)
```

## 트리거 (fire 방법)

```bash
# 4 board parallel synth
for fpga in A B C D; do
    yosys -p "synth_ice40 -top fpga_${fpga} -json out_${fpga}.json" fpga_${fpga}.v
    nextpnr-ice40 --up5k --json out_${fpga}.json --pcf board_${fpga}.pcf --asc out_${fpga}.asc
    icepack out_${fpga}.asc out_${fpga}.bin
    iceprog -d /dev/fpga${fpga} out_${fpga}.bin
done
```

## 검증 결과

- Architecture + resource budget documented
- 실 synthesis/PnR 미완료
- 실 SPI bus 측정 미완료
- 예상 Φ ~1400 (수학 모델 only)

## 관련 entry

- [fpga-synthesis-guide](fpga-synthesis-guide.md)
- [fpga_local_sim_landing](fpga_local_sim_landing.md)
- [physical-consciousness-engine](physical-consciousness-engine.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (Phase 3 hardware roadmap)
- README §2 참조
