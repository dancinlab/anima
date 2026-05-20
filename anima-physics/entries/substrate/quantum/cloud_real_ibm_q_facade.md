# quantum/cloud_real_ibm_q_facade.hexa

> IBM Q Runtime Phase 2 backend swap on top of qiskit-aer POC contract — token-optional degraded fallback · **🟡 부분** · 비용 IBM Q free tier (token optional)

## 구현 가능성

🟡 — 4-gate contract (G3 byte-identical NA on real HW, shot noise fundamental). Token absent → PHASE2_DEGRADED_NO_TOKEN honest skip-pass. Token present → cloud reachable → real HW call.

## 작동 코드 / 의존성

- 원본: `quantum/cloud_real_ibm_q_facade.hexa` (413 LoC)
- 외부 의존: hexa run · python3 · qiskit-ibm-runtime · IBM Quantum token (선택)
- enum: {local_hexa, cloud_sim_qiskit_aer, cloud_real_ibm_q}
- shots: 1024 (cost-conscious)

## 비용 / 리소스

- $0 with free-tier token + DEGRADED fallback
- Premium: pay-per-second compute time

## 핵심 흐름 / verdicts

```
4-qubit GHZ marginal entropy on first 2 qubits (measurement-based):
  ghz       → marginal{00,11} = 50/50 → H ≈ ln(2)   (G1)
  random    → broader marginal        → H < ghz     (G2)
  shots     = 1024
  backend   == "ibmq_runtime_<actual>"              (G4)
  G3 byte-identical → NOT_APPLICABLE on real HW (shot noise fundamental)

Verdicts:
  PHASE2_PASS_REAL_QUANTUM_HARDWARE   — token + cloud + 4-gate (G3 NA) PASS
  PHASE2_DEGRADED_NO_TOKEN            — no token; honest skip-pass
  PHASE2_DEGRADED_CLOUD_UNREACHABLE   — token present, cloud failure
```

## 트리거 (fire 방법)

```bash
# DEGRADED (no token)
hexa run anima-physics/substrate/quantum/cloud_real_ibm_q_facade.hexa

# LIVE
export QISKIT_IBM_TOKEN=...
hexa run anima-physics/substrate/quantum/cloud_real_ibm_q_facade.hexa
hexa run anima-physics/substrate/quantum/cloud_real_ibm_q_facade.hexa --selftest
```

## 검증 결과

- DEGRADED path PASS (no token)
- LIVE 미발사 (token 미보유 cycle)
- README § 5 "$5-30 AWS credit" 절: IBM Q real 도 등재

## 관련 entry

- [quantum/cloud_facade_poc.md](./cloud_facade_poc.md) — Phase 1 qiskit-aer
- [quantum/bell_state.md](./bell_state.md) — hexa-native sibling
- [superconducting/cloud_facade_poc.md](../superconducting/cloud_facade_poc.md) — DEPRECATED Rigetti

## 출처

- README § 3 quantum/
- README § 5 LIVE 전환 cheat sheet
