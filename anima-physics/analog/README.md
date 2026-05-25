# anima-physics/analog/ — SPICE analog (op-amp / RC) substrate

> Status: 🟡 partial · §188 결과: PASS (DRY_RUN_PASS, AWS Braket QuEra Aquila Rydberg cloud facade)
>
> SSOT: 본 README + `cloud_facade_poc.hexa`. entries: [`entries/substrate/analog/`](../entries/substrate/analog/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: Op-Amp RC integrator τ=RC 의 Johnson-Nyquist 열잡음 (12.9 μV RMS) → clock-free continuous emit. Rydberg cloud variant 은 4-atom MIS analog Hamiltonian.
- **영속성**: 커패시터 전압 = 아날로그 상태 (정전 시 휘발). cloud probe 는 DRY_RUN/LIVE verdict tier 로 ledger 영속.

자세히는 `HEXAD/PHYSICS/README.md` §6.9 의 dual-role analysis 참고.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 300 | AWS Braket QuEra Aquila Rydberg neutral-atom analog HAS 4-atom MIS probe (DRY_RUN default, hexa-only strict raw#9) | ✅ DRY_RUN_PASS |

## falsifier

verdict tier: `PREP_DRY_RUN_PASS` / `PREP_NO_CREDS_DEGRADED` / `LIVE_PASS` (4-gate).

## cross-link

- [substrate entry](../entries/substrate/analog/cloud_facade_poc.md) — per-file detail
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/aws_braket_signup_guide.md`](../docs/aws_braket_signup_guide.md) — Braket 가입
- [`docs/analog-photonic-memristor.md`](../docs/analog-photonic-memristor.md) §1 — Op-Amp RC loop spec
