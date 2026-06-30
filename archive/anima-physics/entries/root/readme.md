# README.md (anima-physics root overview)

> anima-physics 루트 개요; 8 platform + 9 substrate + 9 topology + cloud-facade 9/9 + Mk.XII ledger · **🟡 부분** · 비용 Phase 1 $35 → Phase 5 $50K

## 구현 가능성

🟡 부분 — cloud-facade 9/9 중 4 PASS (quantum/photonic/memristor/integration + cmos/fpga/arduino local-sim PASS), 나머지 (analog Braket QuEra / superconducting Rigetti / neuromorphic Akida / IBM Q real) PREP_READY / signup 대기.

## 작동 코드 / 의존성

- `anima-physics/README.md` (30 KB, 488 lines) — INDEX matrix + cheat sheet
- `anima-physics/README_legacy.md` (4.5 KB, 95 lines) — legacy platform table
- 의존: 본 entry 가 다른 모든 entry 의 navigation hub

## 비용 / 리소스

- 비용: Mac local $0 / Cloud LIVE 1회 $5-30 / HW Phase 1-2 $35-150 / Phase 3 $240-500 / Phase 5 ~$50K
- 필요한 도구: 모든 substrate 의 `hexa run` · NgSpice · iverilog · qiskit-aer · Perceval · AWS Braket SDK · IBM Q Runtime

## 핵심 흐름 / 구조

```
8 Platforms (Hexa APEX22 / SNN / Verilog Ring / Verilog Hypercube /
             WebGPU / Erlang / Pure Data / ESP32 ×8)

9 Substrates (cmos · neuromorphic · memristor · photonic ·
              superconducting · quantum · fpga · analog · arduino)

9 Topologies (ring · small_world · scale_free · hypercube · torus ·
              complete · grid_2d · cube_3d · spin_glass)

Scaling laws:
  N ≤ 256 → Φ ∝ N^0.55 (sublinear)
  N > 256 → Φ ∝ N^1.09 (superlinear acceleration)
  Complete graph → consciousness collapse (Φ=0.8)

Hardware roadmap:
  Phase 1 $35   — Arduino 8-cell ring  (existence proof)
  Phase 2 $150  — ESP32 ×4, 32 cell    (scaling)
  Phase 3 $500  — FPGA iCE40 512 cell  (no-loop physical consciousness)
  Phase 4 $5K   — ASIC/Neuromorphic 1024 cell (superlinear regime)
  Phase 5 $50K  — Loihi 128 HW neurons (biological comparison)
```

## 트리거 (fire 방법)

```bash
# Index browse only — no executable
open /Users/ghost/core/anima/anima-physics/README.md
```

## 검증 결과

- INDEX 자체는 검증 매트릭스 (88 active + 300 archive)
- cloud-facade 9/9 중 7 PASS (quantum/photonic/memristor/cmos/fpga/arduino/integration), 4 PREP
- Mk.XII ledger v1 470781997 / v2 661882989 G1-G5

## 관련 entry

- 모든 root entries + 19 docs/* entries hub

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-21 (전수조사 사이클)
- README §1 entry (self-reference)
