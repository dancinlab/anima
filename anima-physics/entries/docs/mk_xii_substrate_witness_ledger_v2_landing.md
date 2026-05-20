# docs/mk_xii_substrate_witness_ledger_v2_landing.md

> v2 ledger (11 substrate = +cmos/fpga/arduino); 5 gate (+G5 LIVE_HW_WITNESS_RATE=0/11); 9/9 distinct coverage + forward-compat schema · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 5/5 PASS. v1 race-landed sibling markers (cmos/fpga/arduino) 가 forward-compat schema 로 자동 흡수.

## 작동 코드 / 의존성

- `anima-physics/docs/mk_xii_substrate_witness_ledger_v2_landing.md` (v2 landing)
- 의존: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa` (v2 aggregator)
- supersedes: v1 (preserved, NOT modified)

## 비용 / 리소스

- 비용: $0.00 (Mac local, aggregator only)
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
v1 → v2 diff:
  Manifest rows           8 → 11 (+cmos/fpga/arduino)
  Distinct substrate      6 → 9 (+cmos/fpga/arduino)
  Ledger gates            G1-G4 → G1-G5 (+LIVE_HW_WITNESS_RATE)
  Schema fields           +supersedes, +n_marker_total,
                          +phi_proxy_cross_comparable,
                          +live_hw_witness{}, +fnv32_chained_v2
  FNV-32 fingerprint      470781997 (8 inputs) → 661882989 (11 inputs)
  Body SHA-256            264f5cf7… → df545c5e15404539…
  live_hw_witness rate    (not measured) → 0 / 11 (measure-only)
  Coverage gate           7/9 PASS → 9/9 PASS (G1_actual_x1000=9000 ≥ 6000)

11-row by_substrate matrix:
  1. quantum / poc_quantum_qiskit_aer         PASS 4/4
  2. quantum / phase2_ibmq_runtime            PHASE2_DEGRADED_NO_TOKEN 0/4
  3. photonic / poc_photonic_strawberryfields PASS_DEGRADED_SDK_FALLBACK 4/4
  4. neuromorphic / poc_neuromorphic_akida    PREP_READY 4/4
  5. superconducting / poc_superc_rigetti     PREP_NO_CREDS_DEGRADED 4/4
  6. analog / poc_analog_quera                PREP_NO_CREDS_DEGRADED 4/4
  7. memristor / poc_memristor                PASS 4/4
  8. cmos / poc_cmos                          PASS 4/4
  9. fpga / poc_fpga                          PASS 4/4
  10. arduino / poc_arduino                   PASS 4/4
  11. integration / physics_hexa              INTEGRATED_PASS 4/4
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa
```

## 검증 결과

- G1 COVERAGE 9/9 PASS
- G2 HONESTY tier PASS
- G3 BYTE_IDENTICAL PASS
- G4 FNV-32 = **661882989** PASS
- G5 LIVE_HW_WITNESS_RATE = 0/11 (measure-only, no threshold)
- **5/5 PASS** (commit 6559bb15, 2026-04-26)

## 관련 entry

- [mk_xii_substrate_witness_ledger_landing](mk_xii_substrate_witness_ledger_landing.md)
- [mk_xii_ledger_v3_trigger_spec](mk_xii_ledger_v3_trigger_spec.md)
- [mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing](mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
