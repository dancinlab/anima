# quantum/cloud_facade_poc.hexa

> qiskit-aer statevector 4-qubit GHZ entanglement entropy (bipartition ≥ 0.64 nat ≈ ln 2) · **✅ 실현** · 비용 $0 local

## 구현 가능성

✅ — 4/4 PASS. qiskit-aer production-grade Schrödinger statevec sim. Phase 2 IBMQRuntime swap-only로 real cloud (`quantum/cloud_real_ibm_q_facade.hexa`).

## 작동 코드 / 의존성

- 원본: `quantum/cloud_facade_poc.hexa` (220 LoC)
- Helper: `scripts/anima_physics_qiskit_aer_probe.py` (raw#37 transient)
- 외부 의존: hexa run · python3 venv · qiskit-aer
- enum: {local_hexa, cloud_sim_qiskit_aer, cloud_real_ibm_q}

## 비용 / 리소스

- $0 local qiskit-aer
- Phase 2 IBM Q: free tier (token optional)

## 핵심 흐름 / ASCII

```
4-qubit GHZ state |GHZ⟩ = (|0000⟩ + |1111⟩) / √2

bipartition entanglement entropy:
  ghz       → ln(2) ≈ 0.6931 ± 0.05  (G1; bipartition ≥ 0.64 nat)
  random    → < ghz                   (G2 sign-flip)
G3 byte-identical 2-run (seed=42 deterministic statevec)
G4 backend == "qiskit_aer_statevector"
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/quantum/cloud_facade_poc.hexa
hexa run anima-physics/substrate/quantum/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS (G1 ≥ ln 2 − 0.05, G2 random < GHZ, G3 byte-identical, G4 backend)
- ref ln(2) ≈ 0.69 nat
- byte-identical 2-run

## 관련 entry

- [quantum/bell_state.md](./bell_state.md) — 2-qubit hexa-native
- [quantum/cloud_real_ibm_q_facade.md](./cloud_real_ibm_q_facade.md) — Phase 2 IBM Q
- [engines/quantum_consciousness.md](../engines/quantum_consciousness.md)
- [photonic/cloud_facade_poc.md](../photonic/cloud_facade_poc.md) — sibling B
- [analog/cloud_facade_poc.md](../analog/cloud_facade_poc.md) — Braket QuEra sibling

## 출처

- README § 3 quantum/
- README § 5 cheat sheet
