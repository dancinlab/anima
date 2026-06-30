# tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa

> Mk.XII ledger v2 — 11 marker (+cmos/fpga/arduino), 5 gate (+G5 LIVE_HW_WITNESS_RATE 0/11) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 5/5 PASS. v1 (8 marker) → v2 (11 marker = +cmos + fpga + arduino 신규 substrate). 9/9 distinct coverage + forward-compat schema. v2.1 prerequisite patch (env-var override 4종 + v3 dry-run synthetic LIVE PASS) 포함.

## 작동 코드 / 의존성

- 원본: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa` (760 LoC)
- 외부 의존: hexa run (no Python)
- v2.1 patch: +78/-10 line (env-var override LEDGER_VERSION / CYCLE_ID / SUPERSEDES / MARKER_OUT)

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 5 gate

```
v2 = v1 + 3 substrate (cmos / fpga / arduino) + G5 gate

G1 LEDGER_COVERAGE          ≥ 9 / 11 (9 distinct substrate)
G2 LEDGER_HONESTY           every marker preserved
G3 LEDGER_BYTE_IDENTICAL    2-run sha256 identical
G4 LEDGER_FINGERPRINT_FNV   FNV-32 chained
G5 LIVE_HW_WITNESS_RATE     real-HW witnessed / total
                            current 0 / 11 (no LIVE 발사 cycle)

v2.1 env-var overrides:
  LEDGER_VERSION  CYCLE_ID  SUPERSEDES  MARKER_OUT
  → v2 byte-identical regression + v3 dry-run synthetic LIVE PASS

Forward-compat: schema includes future-substrate fields (gracefully extends)
```

## 트리거 (fire 방법)

```bash
HEXA_RESOLVER_NO_REROUTE=1 hexa run \
    anima-physics/tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa

# v2.1 mode (synthetic LIVE for v3 dry-run testing):
LEDGER_VERSION=v3-dryrun MARKER_OUT=/tmp/test_v3.json \
    hexa run anima-physics/tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa
```

## 검증 결과

- 5/5 PASS (G1-G5)
- v2.1 patch: v2 byte-identical regression + v3 dry-run synthetic LIVE PASS
- 11 marker (=9 distinct substrate × 일부 multi-marker)

## 관련 entry

- [tool/mk_xii_substrate_witness_ledger_aggregator.md](./mk_xii_substrate_witness_ledger_aggregator.md) — v1 parent
- [tool/mk_xii_substrate_witness_ledger_aggregator_v3.md](./mk_xii_substrate_witness_ledger_aggregator_v3.md)

## 출처

- README § 3 tool/
- docs/mk_xii_substrate_witness_ledger_v2_landing.md
- docs/mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md
