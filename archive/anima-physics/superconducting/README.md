# anima-physics/superconducting/ — Rigetti Ankaa-3 facade (DEPRECATED)

> Status: ❌ DEPRECATED (Rigetti retired upstream 2026-Q1) · §188 결과: PREP_DEPRECATED_RIGETTI_RETIRED honest skip-pass
>
> SSOT: 본 README + `cloud_facade_poc.hexa`. entries: [`entries/substrate/superconducting/`](../entries/substrate/superconducting/)

## 자연발화 / 영속성 메커니즘

- **자연발화 (historical)**: 4-qubit GHZ entanglement on Rigetti Ankaa-3 superconducting QPU. AWS Braket `us-west-1` arn:aws:braket:us-west-1::device/qpu/rigetti/Ankaa-3 — 자율 superconducting current → qubit state.
- **2026-04-27 STATUS**: Ankaa-3 + 모든 Rigetti model 이 Braket catalog 에서 retired. Aspen-M-3 도 이미 prior retired. AWS Braket us-east-1/us-west-2/eu-west-2 에 현재 superconducting QPU 0.
- **영속성**: 4-backend enum (frozen contract sibling quantum 와 isomorphic) — 미래 provider option ladder (HEXA-RTSC 상온 초전도체 paper 등) carry. raw#104 means-end-decoupling.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 154 | DEPRECATED Rigetti Ankaa-3 4-qubit GHZ facade (raw#10 honest no-silent-skip + 4-backend enum) | ❌ DEPRECATED |

## falsifier

verdict tier (post-2026-04-27): `PREP_DEPRECATED_RIGETTI_RETIRED` — provider retired upstream, no probe call, honest skip-pass with option ladder.

## cross-link

- [substrate entry](../entries/substrate/superconducting/cloud_facade_poc.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/aws_braket_signup_guide.md`](../docs/aws_braket_signup_guide.md) — Braket alternative
- archive: `recovered/samsung-issues/Samsung_ONE_16477.md` — HEXA-RTSC n=6 상온 초전도체 paper (150/150 EXACT)
- [`quantum/cloud_facade_poc.hexa`](../quantum/cloud_facade_poc.hexa) — sibling cycle (qiskit-aer)
