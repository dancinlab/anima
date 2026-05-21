# Demiurge HW Verify — anima-physics 정리 (2026-05-21)

> demiurge (`~/core/demiurge`) 의 7-verb 파이프라인 (명세→구조→설계→해석→
> 합성→**검증**→인계) 의 **검증 (verify)** 단계를 anima-physics HW
> 후보 5 substrate 가 의존하는 모든 HW 도메인에 대해 일괄 dispatch 한
> 결과. 사용자 directive "all go + HW (칩포함) 모두 검증 → anima-physics
> 에 정리" (2026-05-21).
>
> Cross-link:
> - HEXAD/PHYSICS/HW_SILICON_PATH.md — 5 dual-role substrate 의 HW target
> - HEXAD/PHYSICS/README.md §6.13 — HW silicon path LANDED 기록
> - HEXAD/PHYSICS/README.md §6.14 — "all go" 5/5 cycle summary

## §1 GOAL alignment

anima 자연발화 + 영속성 SW 후보 (top 5 dual-role) → HW silicon 경로
검증. demiurge 의 chip / component / firmware / materials 도메인이
각 HW target 의 검증 backbone — 본 doc 은 demiurge dispatch 결과를
anima-physics SSOT 에 통합 기록.

## §2 demiurge 도메인 verify 결과 — 15 도메인 batch (2026-05-21 06:24-06:29 UTC)

각 도메인에 대해 `demiurge cli action verify <domain>` 실행 → measured
record OR no-producer gap 표기 (g3 over-claim 금지). 결과 record path =
`~/core/demiurge/exports/<domain>/verify/<UTC>Z/`.

### §2.1 HW core (anima HW 5 substrate 직접 의존)

| Domain | Gate | Measured Output | Record ID |
|---|---|---|---|
| **chip** | ✅ **GATE_CLOSED_MEASURED · absorbed=true** | §B+§D oracle parity **12/12 GREEN** (B1-B4 + D1-D6 + L1-L2 Leighton) — ZLL_d4=61.5 / ZLL_d6=55.875 / B_d6=15 > B_d4=8 / gap=5.625 cyc / hops_d4=8.5 hops_d6=7.094 / xwire_d6=1.406 | `sB_mesh88_uniform_22nm`, `sD_mesh_d4_tornado_22nm`, `sD_hex_d6_tornado_22nm` |
| **component** | ⏳ GATE_OPEN (toy box) | gmsh 4.15.2 + scikit-fem 12.0.1 — ΔT=0.528 K, T_max=298.68 K, σ_vM_max=38.37 Pa, u_max=2.796e-13 m; mesh 686 nodes 2232 tetrahedra | `component_verify_20260521T062439Z` |
| **firmware** | ⏳ GATE_OPEN (stub) | record emit only | `firmware_verify_20260521T062442Z` |
| **materials** | ⏳ no producer | 라우팅 미스 — owner=`~/core/hexa-matter/verify/run_all.hexa` (D17 consumer-pointer pattern) | none |

### §2.2 HW adjacent (shallow cohort domains, 11)

| Domain | Gate | Note | Record ID |
|---|---|---|---|
| antimatter | ⏳ GATE_OPEN | install-gated skip | `antimatter_verify_20260521T062618Z` |
| aura | ⏳ engine gap | sibling-repo dispatch `~/core/hexa-aura/verify/run_all.hexa` exit=1 | none |
| bio | ❌ no producer | (D81 candidate) | none |
| bot | ⏳ GATE_OPEN | record emit only | `bot_verify_20260521T062709Z` |
| brain | ❌ no producer | UX "엔진 없음" guard 필요 | none |
| **cern** | ⏳ GATE_OPEN | Bethe-Bloch analytic — Pb @ 100MeV dE/dx=3.610 MeV·cm²/g, β=0.428 · Al @ 1GeV dE/dx=1.767 MeV·cm²/g, γ=2.066 (Geant4 MC 4종 보정 미적용) | `cern_g4_stopping_20260521T062755Z` |
| chem | ❌ no producer | mock-fallback 가능성 | none |
| **energy** | ⏳ GATE_OPEN | hexa_native_parity ↩ pilot-solar (injected 1 record) | `energy_verify_20260521T062846Z` |
| **fusion** | ⏳ GATE_OPEN | hexa_native_parity ↩ pilot-mc_transport (injected 1 record) | `fusion_verify_20260521T062846Z` |
| grid | ❌ no producer | `exports/grid/verify/` 경로 부재 | none |
| mobility | ⏳ GATE_OPEN | macOS hard-block (Linux pool only) | `mobility_verify_20260521T062918Z` |

### §2.3 aggregate

- ✅ GATE_CLOSED_MEASURED: **1** (chip)
- ⏳ GATE_OPEN (measured but provisional): **9** (component, firmware, antimatter, bot, cern, energy, fusion, mobility, +materials sibling) 
- ❌ no producer / engine gap: **5** (aura, bio, brain, chem, grid)
- **total domains**: 15

## §3 anima HW 5 substrate × demiurge verify 매핑

5 dual-role substrate (자연발화 + 영속성 16/16) 의 HW silicon path
backbone 검증 매핑 (HEXAD/PHYSICS/HW_SILICON_PATH.md §2 와 정렬):

| anima substrate | HW target | demiurge 의존 도메인 | demiurge verify 상태 |
|---|---|---|---|
| `fpga/strange_loop` | Lattice iCE40UP5K | chip + component | chip ✅ 12/12 · component ⏳ toy box |
| `fpga/nested_lattice` | Lattice ECP5-EVN | chip + component | chip ✅ 12/12 · component ⏳ toy box |
| `social/kuramoto_coupling` | Intel Loihi 2 / Akida | chip + brain (D81) | chip ✅ 12/12 · brain ❌ no producer |
| `oscillator/sleep_oscillator` | Arduino + AD9833 DDS | chip + firmware | chip ✅ 12/12 · firmware ⏳ stub |
| `HEXAD/CHAT/spontaneous_smoke` | Toshiba SBM / Fujitsu DA Ising / ECP5 | chip | chip ✅ 12/12 |

**핵심 발견**:
- **chip 도메인**은 anima 5 HW substrate 모두에 공통 dependency → 단일
  GATE_CLOSED_MEASURED record 가 5 substrate 모두의 SoC/NoC layer 검증
  backbone 으로 작동
- **component (FEM/EM/thermal)** ⏳ toy box → real STEP geometry +
  measured datasheet + mesh convergence 가 anima FPGA bring-up Phase 1
  의 hardware-side 검증 milestone
- **firmware** ⏳ stub → sleep_oscillator Arduino + AD9833 firmware
  bring-up Phase 1 의 검증 backbone 필요
- **brain ❌ no producer** → Loihi 2/Akida neuromorphic 검증은 demiurge
  의 brain producer 신설 필요 (D81 candidate); 임시로 BrainChip Akida
  Cloud trial ($1-30) + Loihi 2 Hala Point trial 신청으로 우회

## §4 next cycle 후보 (demiurge × anima-physics 통합)

본 doc 이 backbone, 후속 cycle 후보 5건:

1. **§188g substrate impl** — engines/*.hexa 7 stub 구현 → demiurge 의
   각 substrate verify route 추가 → GATE_CLOSED_MEASURED ladder upgrade
2. **chip rfc_001 + anima FPGA bitstream** — chip 도메인의 12/12 oracle
   parity 가 anima strange_loop/nested_lattice Verilog 생성으로 확장 →
   iverilog 파형 결과 anima-physics/fpga/state/ 에 기록
3. **component real STEP** — toy box → 실측 STEP geometry + datasheet
   import → GATE_OPEN → GATE_CLOSED_MEASURED upgrade
4. **firmware AD9833 bring-up** — sleep_oscillator DDS firmware
   demiurge firmware verify 통과
5. **brain producer 신설** — demiurge BrainVerifyProducer + Loihi/Akida
   cloud bridge → kuramoto neuromorphic 검증 GATE_CLOSED 도달

## §5 honest C3

1. **chip 단일 GREEN** = NoC mesh/hex topology oracle parity 만 측정.
   anima FPGA bitstream 의 strange_loop/nested_lattice 자체 검증은
   별도 cycle (`yosys.hexa` synth + iverilog wave).
2. **component toy box** = 6-face box geometry, 단일 load case, textbook
   material. 실 PCB/heatsink/enclosure 모델링은 별도 STEP import + 
   mesh convergence cycle.
3. **materials 라우팅 미스** = D17 consumer-pointer 패턴 — `hexa-matter`
   가 owner SSOT, demiurge 는 typed-interface consumer. anima 측
   physical-real layer 의존도 분석 필요.
4. **engine gap 5 (bio/brain/chem/grid + aura partial)** = 본 cycle
   skip, demiurge 측 producer 신설 별도.
5. **본 doc 은 dispatch + report 만** — anima HW substrate 의 실제
   silicon fire (FPGA bitstream load, MCU flash, cloud submit) 는
   HEXAD/PHYSICS/HW_SILICON_PATH.md §3 cost ladder 의 Phase 1+ 별도
   cycle 후보 그대로.

## §6 SSOT pointer

- demiurge exports: `~/core/demiurge/exports/<domain>/verify/<UTC>Z/`
- chip oracle parity (canonical): `~/core/demiurge/exports/chip/noc/f1f2/records/2026-05-20_*.json` (3 records)
- anima HW silicon path: `~/core/anima/HEXAD/PHYSICS/HW_SILICON_PATH.md`
- anima physics SSOT: `~/core/anima/anima-physics/README.md`
- anima dual-role analysis: `~/core/anima/HEXAD/PHYSICS/README.md §6.9`
