# analog/cloud_facade_poc.hexa

> AWS Braket QuEra Aquila Rydberg neutral-atom AHS 4-atom MIS blockade probe · **🟡 부분** · 비용 AWS Braket QuEra $0.30/task + $0.01/shot

## 구현 가능성

🟡 — DRY_RUN PASS (creds + SDK + dry-run path verified, api_call_count=0). LIVE 전환은 `ANIMA_BRAKET_DRY_RUN=0` + AWS creds + $5 budget cap 필요. raw#9 hexa-only strict (exec(awk/sha/python3) only) · raw#37 transient helper script.

## 작동 코드 / 의존성

- 원본: `analog/cloud_facade_poc.hexa` (300 LoC)
- Helper: `scripts/anima_physics_braket_quera_probe.py` (raw#37 transient)
- 외부 의존: AWS Braket SDK · python3 venv (`.venv/bin/python3`) · QuEra Aquila device ARN `arn:aws:braket:us-east-1::device/qpu/quera/Aquila`
- Probe: 4-atom AHS, shots=100, seed=42

## 비용 / 리소스

- DRY_RUN: $0 (api_call_count=0)
- LIVE: QuEra $0.30/task + $0.01/shot × 100 = $1.30/run + AWS overhead

## 핵심 흐름 / ASCII

```
mis        → blockade-induced anti-ferromagnetic pattern → H ≥ 0.3 nat (G1)
uncoupled  → trivial ground state (no Rabi)              → entropy=0    (G2)
G3 byte-identical sha · G4 backend == aws_braket_quera_<actual>
shots=100 · seed=42 · N_ATOMS=4
```

## 트리거 (fire 방법)

```bash
# DRY_RUN (default)
hexa run anima-physics/substrate/analog/cloud_facade_poc.hexa
hexa run anima-physics/substrate/analog/cloud_facade_poc.hexa --selftest

# LIVE
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_DEFAULT_REGION=us-east-1
ANIMA_BRAKET_DRY_RUN=0 hexa run anima-physics/substrate/analog/cloud_facade_poc.hexa
```

## 검증 결과

- DRY_RUN 4-gate PASS (PREP_DRY_RUN_PASS verdict)
- Verdict tier: PREP_DRY_RUN_PASS / PREP_NO_CREDS_DEGRADED / LIVE_PASS / LIVE_FAIL_<reason>
- G3 byte-identical, G4 backend=="aws_braket_quera_<actual>"
- LIVE 미발사 (cycle 잔여)

## 관련 entry

- [trapped_ion/cloud_facade_poc.md](../trapped_ion/cloud_facade_poc.md) — Braket IonQ sibling
- [quantum/cloud_facade_poc.md](../quantum/cloud_facade_poc.md) — qiskit-aer sibling
- [superconducting/cloud_facade_poc.md](../superconducting/cloud_facade_poc.md) — DEPRECATED Rigetti
- [scripts/anima_physics_braket_quera_probe.md](../scripts/anima_physics_braket_quera_probe.md)

## 출처

- README § 3 analog/
- 원본 파일 SCHEMA `anima_physics/cloud_facade_analog/1_braket_quera_aquila`
