# tool/mk_xii_substrate_witness_ledger_aggregator.hexa

> Mk.XII INTEGRATION multi-substrate witness ledger v1 aggregator (8 marker, 4 gate: coverage / honesty / byte-identical / FNV-32) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 4/4 PASS. Pure aggregator (zero LLM, zero GPU, zero re-measurement) — reads existing marker.json files only. G1 coverage ≥ 6/9, G2 honesty (no cherry-pick), G3 byte-identical 2-run, G4 FNV-32 fingerprint=470781997.

## 작동 코드 / 의존성

- 원본: `tool/mk_xii_substrate_witness_ledger_aggregator.hexa` (569 LoC)
- 외부 의존: hexa run (no Python)
- Reads: `state/v10_anima_physics_cloud_facade/*/marker.json`
- Emit: `state/v10_anima_physics_cloud_facade/integration_ledger/witness_ledger_v1.json`

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 4 gate

```
G1 LEDGER_COVERAGE          n_landed_full_pass + n_prep_only ≥ 6 / 9
G2 LEDGER_HONESTY           every marker entry preserved (no cherry-pick)
                            including DEGRADED_/PREP_/PHASE2_ verdicts
G3 LEDGER_BYTE_IDENTICAL    aggregator 2-run sha256 identical (timestamp excl)
G4 LEDGER_FINGERPRINT_FNV   FNV-32 chained over deterministic marker-sha seq
                            = 470781997

Cross-substrate Φ direct comparison NOT valid (axes differ — quantum entanglement
entropy ≠ photonic Fock entropy ≠ memristor hysteresis area).
Ledger aggregates COVER-COUNT + per-substrate gate verdicts only.

Default target_total = 9 (quantum + photonic + neuromorphic + superconducting +
analog + memristor + cmos + fpga + arduino; quantum has 2 markers POC + Phase 2)
```

## 트리거 (fire 방법)

```bash
HEXA_RESOLVER_NO_REROUTE=1 hexa run \
    anima-physics/substrate/tool/mk_xii_substrate_witness_ledger_aggregator.hexa

# env vars (선택):
# LEDGER_OUT, LEDGER_BASE_DIR, LEDGER_TARGET_TOTAL
```

## 검증 결과

- 4/4 PASS (G1 coverage 7/9, G2 honesty 6 verdict tier, G3 byte-identical, G4 FNV32=470781997)
- docs/mk_xii_substrate_witness_ledger_landing.md

## 관련 entry

- [tool/mk_xii_substrate_witness_ledger_aggregator_v2.md](./mk_xii_substrate_witness_ledger_aggregator_v2.md)
- [tool/mk_xii_substrate_witness_ledger_aggregator_v3.md](./mk_xii_substrate_witness_ledger_aggregator_v3.md)

## 출처

- README § 3 tool/
- docs/mk_xii_substrate_witness_ledger_landing.md
