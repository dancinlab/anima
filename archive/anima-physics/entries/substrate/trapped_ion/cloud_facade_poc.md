# trapped_ion/cloud_facade_poc.hexa

> AWS Braket IonQ Forte 1 4-qubit GHZ entanglement probe (gate-based, up to 36-qubit, us-east-1) · **🟡 부분** · 비용 IonQ $0.01/shot × 100

## 구현 가능성

🟡 — Phase 1.5 LIVE_PASS ready. DRY_RUN verified. Rigetti DEPRECATED 대체 substrate (option (i) ladder). LIVE 전환: `ANIMA_BRAKET_DRY_RUN=0` + AWS creds.

## 작동 코드 / 의존성

- 원본: `trapped_ion/cloud_facade_poc.hexa` (310 LoC)
- Helper: `scripts/anima_physics_braket_ionq_probe.py` (raw#37 transient, 303 LoC Python)
- 외부 의존: hexa run · python3 venv · amazon-braket-sdk · AWS credentials
- Device ARN: `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1`
- 상수: N_QUBITS=4, SHOTS=100, SEED=42

## 비용 / 리소스

- DRY_RUN: $0
- LIVE: $1 (100 shots × $0.01) + AWS Braket task overhead

## 핵심 흐름 / ASCII

```
4-qubit GHZ on IonQ Forte 1:
  H(0) + CNOT(0,1) + CNOT(1,2) + CNOT(2,3)  →  |0000⟩ + |1111⟩ 

positive  ghz         → 100-shot bitstring H ≥ 0.5 nat (G1)  (ideal ln(2) ≈ 0.69)
negative  unentangled → H(0) only product state            (G2 sign-flip)
G3 byte-identical sha256 (DRY_RUN deterministic) — NA on LIVE (shot noise)
G4 backend == "aws_braket_ionq_<actual>"

Verdict tier:
  PREP_DRY_RUN_PASS / PREP_NO_CREDS_DEGRADED / LIVE_PASS / LIVE_FAIL_<reason>
```

## 트리거 (fire 방법)

```bash
# DRY_RUN (default)
hexa run anima-physics/trapped_ion/cloud_facade_poc.hexa
hexa run anima-physics/trapped_ion/cloud_facade_poc.hexa --selftest

# LIVE
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_DEFAULT_REGION=us-east-1
ANIMA_BRAKET_DRY_RUN=0 hexa run anima-physics/trapped_ion/cloud_facade_poc.hexa
```

## 검증 결과

- DRY_RUN PASS (PREP_DRY_RUN_PASS)
- LIVE 미발사 (cycle 잔여)
- Mk.XII v3 ledger: trapped_ion marker added (target_tot 9→10)

## 관련 entry

- [analog/cloud_facade_poc.md](../analog/cloud_facade_poc.md) — Braket QuEra sibling
- [superconducting/cloud_facade_poc.md](../superconducting/cloud_facade_poc.md) — DEPRECATED Rigetti
- [quantum/cloud_facade_poc.md](../quantum/cloud_facade_poc.md) — qiskit-aer sibling
- [scripts/anima_physics_braket_ionq_probe.md](../scripts/anima_physics_braket_ionq_probe.md)

## 출처

- README § 3 trapped_ion/
- README § 5 LIVE cheat sheet
- docs/aws_braket_signup_guide.md
