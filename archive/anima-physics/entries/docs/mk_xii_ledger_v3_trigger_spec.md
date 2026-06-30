# docs/mk_xii_ledger_v3_trigger_spec.md

> v3 ledger trigger spec (수동, not auto); 4 LIVE pattern (IBM Q / Braket Rigetti / Braket QuEra / Akida); G5 LIVE_HW_WITNESS_RATE threshold ladder · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 부분 — 스펙 frozen, v3 코드 미작성 (v2 aggregator rerun만 trigger). 신규 코드 없음 — v2 aggregator 의 forward-compat schema 가 LIVE column 자동 흡수.

## 작동 코드 / 의존성

- `anima-physics/docs/mk_xii_ledger_v3_trigger_spec.md` (frozen spec)
- 의존: `tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa` (rerun target)
- 후속: `mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md` (CLI flag 정정)

## 비용 / 리소스

- 비용: $0 (spec only, no code emitted, no ledger re-run)
- 필요한 도구: `hexa run` (v2 aggregator rerun)

## 핵심 흐름 / 구조

```
ledger v2: G5 LIVE_HW_WITNESS_RATE = 0/11 (모두 sim/surrogate/dispatch)

v3 trigger 조건 (3가지):
  T1 quantum IBM Q:
     marker verdict ^PHASE2_PASS_REAL.*$  → IBM_QUANTUM_TOKEN + cloud_real_ibm_q_facade rerun
  T2a superconducting Braket Rigetti:
     verdict ^LIVE_PASS$  → AWS creds + ANIMA_BRAKET_DRY_RUN=0 + cloud_facade_poc rerun
  T2b analog Braket QuEra:
     verdict ^LIVE_PASS$  → AWS creds + analog/cloud_facade_poc rerun
  T3 neuromorphic Akida:
     verdict ^LIVE_PASS$ (또는 PASS_REAL_AKIDA in v3.1)
     → BRAINCHIP_AKIDA_TOKEN + Linux/x86_64 또는 cloud SDK

G5 LIVE_HW_WITNESS_RATE threshold ladder:
  L1 = 1/11
  L2 = 3/11
  L3 = 9/11
```

## 트리거 (fire 방법)

```bash
# v3 = rerun v2 aggregator with LIVE markers in place
cd <repo-root>
HEXA_RESOLVER_NO_REROUTE=1 \
LEDGER_VERSION=v3 \
LEDGER_OUT=state/v10_anima_physics_cloud_facade/integration_ledger/witness_ledger_v3.json \
MARKER_OUT=state/v10_anima_physics_cloud_facade/integration_ledger/marker_v3.json \
LEDGER_SUPERSEDES_OVERRIDE='v2 (...)' \
hexa run tool/mk_xii_substrate_witness_ledger_aggregator_v2.hexa
```

## 검증 결과

- spec frozen (commit 2026-04-26)
- v2 aggregator forward-compat 검증 완료
- 실 v3 발동은 cloud signup 후 manual trigger

## 관련 entry

- [mk_xii_substrate_witness_ledger_v2_landing](mk_xii_substrate_witness_ledger_v2_landing.md)
- [mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing](mk_xii_substrate_witness_ledger_aggregator_v2_1_prerequisite_landing.md)
- [aws_braket_signup_guide](aws_braket_signup_guide.md)
- [akida_cloud_signup_guide](akida_cloud_signup_guide.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
