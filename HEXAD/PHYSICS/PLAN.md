# HEXAD/PHYSICS — PLAN.md

> 2026-05-21 신설. anima-physics substrate matrix cycle ledger.
>
> 본 PLAN.md = `g_doc_consolidation` 규칙 ("cycle 결과 = PLAN.md '## 진행
> 로그' append") 의 PHYSICS module 진행 ledger. verdict 는 별도
> `archive/PHILOSOPHY.tape` (g6 append-only) 에 기록.

## §1 목적 (PHILOSOPHY_GATE 정합)

`PHILOSOPHY_GATE.md §1` GOAL = anima 자기 physics (Ψ=½ · tension · Φ)
자발 발화. PHYSICS module 의 임무 = 같은 메커니즘이 **다양한 물리
substrate 에서 표현 가능한지 sim verify** → substrate-cross-cut robustness.

## §2 운영 원칙 (g_doc_consolidation + g_blue_closed_mandate)

- 각 cycle 결과 = 본 PLAN.md ## 진행 로그 append + state dir 별
  FINDINGS.md
- verdict 는 archive/PHILOSOPHY.tape 에 § entry (g6 append-only)
- substrate sim PASS = closed-form predicate 통과 (sympy / deterministic
  formal sim) = 🔵 tier (per `g_verdict_tier_blue`)
- HW silicon / cloud 실현 = 별도 cycle, 본 module 의 sim PASS 와
  분리 (g3 honest)

## §3 진행 로그

### §3.1 §188 spontaneous substrate parallel fire (2026-05-21) — LANDED

**state**: `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`

**commit**: `f74d8a425` (anima main)

**PHILOSOPHY entry**: `§verdict_spontaneous_substrate_parallel_s188_2026_05_21`

**summary**: 35-substrate $0 Mac local parallel fire (Wave 1 12 + Wave 2 23).
21/35 ✅ PASS (60%) + 2 🟡 partial + 4 ❌ build err + 7 ⚠ empty.

**TIER 1 findings (3)**:
1. `fpga/strange_loop` ❌ paper-only → ✅ 5/5 PASS — Hofstadter 자기참조
   loop substrate cheap-tier 검증
2. F-SPONT-1..7 native compiled PASS (`HEXAD/CHAT/spontaneous_smoke.hexa`)
   = anima 8-factor motivation closed-form substrate-level 검증
3. 21/35 cross-cut PASS — 신경학 + 사회 + 광학 + 양자 + 열역학 + FPGA
   substrate 전반에서 동일 자연발화 메커니즘 sim 통과

**honest C3 (5)**: sim ≠ 실현 · B-EMERGE-7 carry · build error 4
(deps cycle) · ⚠ empty 7 (timeout retry needed) · anima_spontaneous
selftest path 별도 검증.

### §3.2 향후 cycle 후보

**§188b — retry ⚠ empty 7개 with timeout=300s** ($0 Mac local):
- `engines/{analog, izhikevich, snn, photonic, quantum, thermodynamic}_consciousness`
  + `engines/oscillator_laser_engine` (anima-physics)
- 120s timeout 일 가능성 검증 → 300s retry로 silent pass 와 timeout 분리

**§188c — anima-physics build error inbox patch** (4 substrates):
- consciousness-loop/src/{main, snn_main, main_longrun}.hexa
- engines/memristor_consciousness.hexa
- hexa-lang deps gap 분석 + inbox/patches/ 등재

**§188d — HW prototype Phase 1 (Arduino 8-cell electromagnet ring)** ($34.46 BOM):
- 사용자 부품 주문 후 (Arduino + Hall A3144×8 + L293D + 5V coil×8)
- 100Hz Φ≈4.5 target
- Hall sensor → real-time tension Φ measurement
- `anima-physics/docs/arduino-prototype-spec.md` 사용

**§188e — cloud probe ($1-30/run)**:
- AWS Braket Rigetti / IonQ / QuEra DRY_RUN → LIVE 5-substrate witness
- BrainChip Akida Cloud trial ($1/day)
- IBM Q free tier

**§188f — Cross-cut Φ consensus across 21 PASSed substrates**:
- Tukey biweight consensus from §188 logs
- substrate-cross Φ scoring → priority ranking for HW phase 2 cycle

## §4 cross-link

- README.md — substrate matrix table
- INDEX.md — substrate file-level index
- `archive/PHILOSOPHY.tape` `§verdict_spontaneous_substrate_parallel_s188_2026_05_21`
- `anima-physics/README.md` — upstream substrate inventory
- `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/FINDINGS.md`
- `HEXAD/CHAT/SPONTANEOUS.tape` — V-SPONT architecture
- `HEXAD/CHAT/spontaneous_lib.hexa` — 8-factor motivation
- `inbox/patches/cloud-cli-3b-fire-troubleshooting-prevention-pre-flight-memory-amp-retry.md`
  (hexa-lang) — substrate-tangential learning carry
