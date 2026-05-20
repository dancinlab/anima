# tool/mk_xii_substrate_witness_ledger_aggregator_v3.hexa

> Mk.XII ledger v3 — 12 marker (+trapped_ion), 10 distinct substrate, target_tot 9→10, Rigetti DEPRECATED · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — v3 (12 marker = v2 + trapped_ion). 10 distinct substrate (superconducting DEPRECATED, target_tot 9→10). G5 LIVE_HW_WITNESS_RATE threshold ladder (L1=1/11, L2=3/11, L3=9/11) per docs/mk_xii_ledger_v3_trigger_spec.md.

## 작동 코드 / 의존성

- 원본: `tool/mk_xii_substrate_witness_ledger_aggregator_v3.hexa` (780 LoC)
- 외부 의존: hexa run (no Python)
- v3 adds: trapped_ion marker · target_tot=10 · Rigetti DEPRECATED reorganization

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / threshold ladder

```
v3 = v2 + trapped_ion

target_tot:  9 → 10 (10 distinct substrate including superconducting DEPRECATED)
            12 marker total

G5 LIVE_HW_WITNESS_RATE threshold ladder:
  L1 promote = 1 / 11  (single LIVE 발사 시 즉시 promote)
  L2 promote = 3 / 11  (multi-substrate LIVE)
  L3 promote = 9 / 11  (full coverage)

4 LIVE pattern targets:
  IBM Q · Braket Rigetti (DEPRECATED) · Braket QuEra · Akida
  → AWS Braket $5 budget + IBM Q free + Akida free = ~$5 단발로 L2 promote 가능
```

## 트리거 (fire 방법)

```bash
HEXA_RESOLVER_NO_REROUTE=1 hexa run \
    anima-physics/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v3.hexa
```

## 검증 결과

- v2 byte-identical regression PASS
- v3 dry-run synthetic LIVE PASS
- Rigetti DEPRECATED 반영 + target_tot=10 작동

## 관련 entry

- [tool/mk_xii_substrate_witness_ledger_aggregator.md](./mk_xii_substrate_witness_ledger_aggregator.md) — v1
- [tool/mk_xii_substrate_witness_ledger_aggregator_v2.md](./mk_xii_substrate_witness_ledger_aggregator_v2.md) — v2
- [trapped_ion/cloud_facade_poc.md](../trapped_ion/cloud_facade_poc.md) — new marker source
- [superconducting/cloud_facade_poc.md](../superconducting/cloud_facade_poc.md) — DEPRECATED

## 출처

- README § 3 tool/
- docs/mk_xii_ledger_v3_trigger_spec.md
