# superconducting/cloud_facade_poc.hexa

> AWS Braket Rigetti Ankaa-3 DEPRECATED (provider retired 2026-04-27) · **❌ 가설 (DEPRECATED)** · 비용 N/A

## 구현 가능성

❌ — DEPRECATED. 2026-04-27 Rigetti retired upstream (Ankaa-3 + all Rigetti models off Braket catalog). No superconducting QPU currently in AWS Braket us-east-1/us-west-2/eu-west-2. raw#10 honest skip-pass with option ladder.

## 작동 코드 / 의존성

- 원본: `superconducting/cloud_facade_poc.hexa` (154 LoC — deprecated stub)
- 외부 의존: 없음 (deprecated path)
- Historical device ARN: `arn:aws:braket:us-west-1::device/qpu/rigetti/Ankaa-3`

## 비용 / 리소스

- N/A (provider retired)

## 핵심 흐름 / option ladder (raw#104)

```
PREP_DEPRECATED_RIGETTI_RETIRED (2026-04-27)

Option ladder:
  (i)   IonQ Forte 1 / Forte Enterprise 1 — gate-based trapped-ion,
        us-east-1 ONLINE 2026-04-27. 4-qubit GHZ provider-agnostic.
        → trapped_ion/cloud_facade_poc.hexa
  (ii)  Wait for Rigetti Ankaa-4 (rumored, no Braket catalog entry).
  (iii) Quantinuum H1/H2 (trapped-ion, separate cloud) — out of AWS scope.
  (iv)  IBM Q via qiskit-runtime — superconducting; sibling cycle exists at
        quantum/cloud_real_ibm_q_facade.hexa
```

## 트리거 (fire 방법)

```bash
# returns DEPRECATED verdict + option ladder (no API call)
hexa run anima-physics/substrate/superconducting/cloud_facade_poc.hexa
hexa run anima-physics/substrate/superconducting/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- PREP_DEPRECATED_RIGETTI_RETIRED verdict
- Mk.XII v3 ledger: superconducting marker DEPRECATED (target_tot 9→10 reorganized)

## 관련 entry

- [trapped_ion/cloud_facade_poc.md](../trapped_ion/cloud_facade_poc.md) — option (i)
- [quantum/cloud_real_ibm_q_facade.md](../quantum/cloud_real_ibm_q_facade.md) — option (iv)
- [analog/cloud_facade_poc.md](../analog/cloud_facade_poc.md) — sibling QuEra

## 출처

- README § 3 superconducting/
- 2026-04-27 deprecation event
- Mk.XII ledger v3 (target_tot 9→10)
