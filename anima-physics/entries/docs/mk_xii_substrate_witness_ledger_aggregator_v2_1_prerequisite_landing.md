# docs/mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md

> aggregator v2.1 prerequisite patch; env-var override 4종 (LEDGER_VERSION / CYCLE_ID / SUPERSEDES / MARKER_OUT) + v2 byte-identical regression + v3 dry-run synthetic LIVE PASS · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — v2 + v3 dual-mode. v3 trigger spec §raw#10 §5 의 silent-fail risk 사전 차단. v2 ledger body sha `df545c5e…` 그대로 보존 (schema 변경 0).

## 작동 코드 / 의존성

- `anima-physics/docs/mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md` (landing)
- 의존: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa` (+78/-10 line patch)
- 후속: `mk_xii_ledger_v3_trigger_spec.md` (frozen contract reference)

## 비용 / 리소스

- 비용: $0.00 (Mac local, hexa-only — no cloud, no LLM, no GPU)
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
v3 spec §2 CLI flag (--ledger-out=/--marker-out=/--version-tag=) invalid 확인:
  v2 aggregator argv parse 안 함 → env-var 기반으로 정정

v2.1 env-var override 4종:
  LEDGER_VERSION       — v2 / v3 mode 분기
  LEDGER_CYCLE_ID      — cycle id override (예: mk_xii_substrate_witness_ledger_v3)
  LEDGER_SUPERSEDES_OVERRIDE — v2 fingerprint chain
  MARKER_OUT           — marker JSON 자동 emission target

v2 byte-identical regression:
  body sha = df545c5e15404539cea6f1b61c8d46565089f6d266277234b50a124d066e49ba
  FNV-32 = 661882989 (변경 0)

v3 dry-run synthetic LIVE:
  G5-tier verdict 분기 검증 (LIVE_PASS 패턴 matching PASS)
```

## 트리거 (fire 방법)

```bash
# v2 byte-identical regression
hexa run /Users/ghost/core/anima/anima-physics/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa

# v3 mode dry-run (env-var override)
LEDGER_VERSION=v3 \
LEDGER_OUT=state/v10_anima_physics_cloud_facade/integration_ledger/witness_ledger_v3.json \
MARKER_OUT=state/v10_anima_physics_cloud_facade/integration_ledger/marker_v3.json \
hexa run /Users/ghost/core/anima/anima-physics/substrate/tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa
```

## 검증 결과

- v2 byte-identical regression PASS
- v3 dry-run synthetic LIVE PASS
- 4 env-var override 검증
- aggregator dual-mode operational (2026-04-27)

## 관련 entry

- [mk_xii_substrate_witness_ledger_v2_landing](mk_xii_substrate_witness_ledger_v2_landing.md)
- [mk_xii_ledger_v3_trigger_spec](mk_xii_ledger_v3_trigger_spec.md)
- [mk_xii_substrate_witness_ledger_landing](mk_xii_substrate_witness_ledger_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-27
- README §2 참조
