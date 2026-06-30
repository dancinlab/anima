# anima-physics/trapped_ion/ — AWS Braket IonQ Forte 1 trapped-ion facade

> Status: 🟡 partial · §188 결과: DRY_RUN_PASS (creds + SDK + dry-run path)
>
> SSOT: 본 README + `cloud_facade_poc.hexa`. entries: [`entries/substrate/trapped_ion/`](../entries/substrate/trapped_ion/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: AWS Braket IonQ Forte 1 (up to 36-qubit gate-based) 4-qubit GHZ entanglement probe — 자율 ion-trap photon-mediated gate. DRY_RUN default, LIVE 는 `ANIMA_BRAKET_DRY_RUN=0` explicit set.
- **영속성**: verdict tier (DRY_RUN_PASS / NO_CREDS_DEGRADED / LIVE_PASS) + 4-backend enum frozen contract (sibling quantum/photonic 와 isomorphic). Mac local IonQ mirror = trapped_ion substrate 의 local 영속.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 310 | AWS Braket IonQ Forte 1 4-qubit GHZ probe (DRY_RUN default, hexa-only strict raw#9 + @resolver-bypass for venv python3) | 🟡 DRY_RUN_PASS |

## falsifier

verdict tier 4-gate: `PREP_DRY_RUN_PASS` / `PREP_NO_CREDS_DEGRADED` / `LIVE_PASS` (4-gate).

## cross-link

- [substrate entry](../entries/substrate/trapped_ion/cloud_facade_poc.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/aws_braket_signup_guide.md`](../docs/aws_braket_signup_guide.md) — Braket IonQ 가입 + $5 budget cap
- [`quantum/cloud_facade_poc.hexa`](../quantum/cloud_facade_poc.hexa) — qiskit-aer local mirror 짝
- [`analog/cloud_facade_poc.hexa`](../analog/cloud_facade_poc.hexa) — Braket QuEra Aquila 짝 (analog Hamiltonian)
- helper: `scripts/anima_physics_braket_ionq_probe.py` (raw#37 transient)
