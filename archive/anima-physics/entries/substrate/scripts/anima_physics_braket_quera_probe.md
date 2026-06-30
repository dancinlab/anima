# scripts/anima_physics_braket_quera_probe.py

> AWS Braket QuEra Aquila 4-atom Rydberg AHS MIS probe (us-east-1) · **🟡 부분** · 비용 QuEra $0.30/task + $0.01/shot

## 구현 가능성

🟡 — DRY_RUN verified. LIVE 전환은 `ANIMA_BRAKET_DRY_RUN=0` + AWS creds + QuEra budget. raw#37 transient helper for `analog/cloud_facade_poc.hexa`.

## 작동 코드 / 의존성

- 원본: `scripts/anima_physics_braket_quera_probe.py` (299 LoC Python)
- 외부 의존: python3 · boto3 · amazon-braket-sdk · AWS credentials
- Device ARN: `arn:aws:braket:us-east-1::device/qpu/quera/Aquila`
- 상수: N_ATOMS=4, SHOTS=100, SPACING_M=5.5µm (Aquila default lattice), RABI=1.58e7 rad/s (~2.5 MHz), DETUNING=2e7 rad/s (~3 MHz), TOTAL_TIME=3.5 µs

## 비용 / 리소스

- DRY_RUN: $0
- LIVE: QuEra $0.30/task + $0.01/shot × 100 = $1.30 + AWS overhead

## 핵심 흐름 / output schema

```
Required JSON keys (all branches):
  credentials_present, dry_run, degraded,
  entropy_pattern_nat, sha256_program,
  backend_name, actual_backend, error,
  api_call_count, device_arn

AHS program (Rydberg neutral atom):
  4-atom MIS pattern with 5.5 µm spacing
  Rabi frequency ~2.5 MHz, detuning ~3 MHz, 3.5 µs pulse
```

## 트리거 (fire 방법)

```bash
# DRY_RUN (default)
ANIMA_BRAKET_DRY_RUN=1 python3 anima-physics/scripts/anima_physics_braket_quera_probe.py --seed 42 --program mis

# LIVE
export AWS_PROFILE=braket
ANIMA_BRAKET_DRY_RUN=0 python3 anima-physics/scripts/anima_physics_braket_quera_probe.py --seed 42 --program mis

# 또는 hexa wrapper
hexa run anima-physics/analog/cloud_facade_poc.hexa
```

## 검증 결과

- DRY_RUN PASS (creds detect + SDK path)
- LIVE 미발사

## 관련 entry

- [analog/cloud_facade_poc.md](../analog/cloud_facade_poc.md) — hexa wrapper
- [scripts/anima_physics_braket_ionq_probe.md](./anima_physics_braket_ionq_probe.md) — sibling

## 출처

- README § 3 scripts/
- README § 5 LIVE cheat sheet
- docs/aws_braket_signup_guide.md
