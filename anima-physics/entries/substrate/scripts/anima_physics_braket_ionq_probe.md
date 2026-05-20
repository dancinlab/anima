# scripts/anima_physics_braket_ionq_probe.py

> AWS Braket IonQ Forte 1 4-qubit GHZ gate-based circuit probe (us-east-1) · **🟡 부분** · 비용 IonQ $0.01/shot

## 구현 가능성

🟡 — DRY_RUN verified (SDK + auth path, api_call_count=0). LIVE 전환은 `ANIMA_BRAKET_DRY_RUN=0` + AWS creds + IonQ budget. raw#37 transient helper for `trapped_ion/cloud_facade_poc.hexa`.

## 작동 코드 / 의존성

- 원본: `scripts/anima_physics_braket_ionq_probe.py` (303 LoC Python)
- 외부 의존: python3 · boto3 · amazon-braket-sdk · AWS credentials
- Device ARN: `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1`
- 상수: N_QUBITS=4, SHOTS=100, AWS_PROFILE=braket
- Output: single-line JSON (caller parses via awk)

## 비용 / 리소스

- DRY_RUN: $0
- LIVE: IonQ $0.01/shot × 100 = $1 + AWS Braket task overhead $0.30

## 핵심 흐름 / output schema

```
Required JSON keys (all branches):
  credentials_present, dry_run, degraded,
  entropy_pattern_nat, sha256_program,
  backend_name, actual_backend, error,
  api_call_count, device_arn
```

## 트리거 (fire 방법)

```bash
# DRY_RUN (default)
ANIMA_BRAKET_DRY_RUN=1 python3 anima-physics/scripts/anima_physics_braket_ionq_probe.py --seed 42 --program ghz

# LIVE
export AWS_PROFILE=braket
ANIMA_BRAKET_DRY_RUN=0 python3 anima-physics/scripts/anima_physics_braket_ionq_probe.py --seed 42 --program ghz

# 또는 hexa wrapper
hexa run anima-physics/trapped_ion/cloud_facade_poc.hexa
```

## 검증 결과

- DRY_RUN PASS (creds detect + SDK path)
- LIVE 미발사 (cycle 잔여)

## 관련 entry

- [trapped_ion/cloud_facade_poc.md](../trapped_ion/cloud_facade_poc.md) — hexa wrapper
- [scripts/anima_physics_braket_quera_probe.md](./anima_physics_braket_quera_probe.md) — sibling

## 출처

- README § 3 scripts/
- README § 5 LIVE cheat sheet
- docs/aws_braket_signup_guide.md
