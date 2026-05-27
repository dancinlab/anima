# docs/mk_xii_substrate_witness_ledger_landing.md

> v1 ledger (8 substrate); 4 gate (G1 coverage 7/9 · G2 honesty 6 verdict tier · G3 byte-identical · G4 FNV32=470781997) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 4/4 PASS. Mac local aggregator only (no probe, no LLM, no GPU, no network).

## 작동 코드 / 의존성

- `anima-physics/docs/mk_xii_substrate_witness_ledger_landing.md` (v1 landing report)
- 의존: `tool/mk_xii_substrate_witness_ledger_aggregator.hexa` (v1)
- 후속: v2 (11 substrate), v3 trigger spec

## 비용 / 리소스

- 비용: $0 (Mac local, aggregator only)
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
v1 Schema (frozen):
  ledger_version:                 "v1"
  cycle_id:                       "mk_xii_substrate_witness_ledger_v1"
  n_substrate_total:              9
  n_substrate_landed_full_pass:   <count of PASS / INTEGRATED_PASS / PASS_DEGRADED>
  n_substrate_prep_only:          <count of PHASE2_DEGRADED / PREP_READY / PREP_NO_CREDS>
  n_substrate_covered:            landed + prep
  by_substrate:                   8 entries deterministic order
  aggregate_gates:                G1-G4 pass_rate × 1000
  ledger_gates:                   G1_COVERAGE / G2_HONESTY / G3_BYTE_IDENTICAL / G4_FNV32

8 v1 markers: quantum / quantum_phase2 / photonic / neuromorphic /
              superconducting / analog / memristor / integration

Verdict ladder: PASS / INTEGRATED_PASS / PASS_DEGRADED_SDK_FALLBACK /
                PHASE2_DEGRADED_NO_TOKEN / PREP_READY_AWAITING_USER_SIGNUP /
                PREP_NO_CREDS_DEGRADED
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/tool/mk_xii_substrate_witness_ledger_aggregator.hexa
```

## 검증 결과

- G1 LEDGER_COVERAGE 7/9 PASS
- G2 HONESTY 6 verdict tier PASS
- G3 BYTE_IDENTICAL 2-run PASS
- G4 FINGERPRINT_FNV32 = **470781997** PASS
- **4/4 PASS** (2026-04-26)

## 관련 entry

- [mk_xii_substrate_witness_ledger_v2_landing](mk_xii_substrate_witness_ledger_v2_landing.md)
- [mk_xii_ledger_v3_trigger_spec](mk_xii_ledger_v3_trigger_spec.md)
- [mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing](mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
