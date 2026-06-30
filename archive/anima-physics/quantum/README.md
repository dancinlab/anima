# anima-physics/quantum/ — Bell state + qiskit-aer cloud-facade + IBM Q runtime

> Status: ✅ PASS (cloud_facade 4/4 + bell_state T1-T5 + IBM Q pre-flight 🟡) · §188 결과: quantum entanglement shared-substrate
>
> SSOT: 본 README + 3 `.hexa` 파일. entries: [`entries/substrate/quantum/`](../entries/substrate/quantum/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2 = 최대 entanglement → 측정 시 A=0↔B=0, A=1↔B=1 자율 상관 emit (EPR pair, teleportation/QKD substrate). qiskit-aer statevector backend 로 4-차원 Hilbert space 자율 evolution.
- **영속성**: 양자 상태 자체는 측정 시 collapse (휘발). substrate_backend enum (frozen contract — `local_hexa` / `cloud_sim_qiskit_aer` / `cloud_real_ibm_q` / `surrogate_algorithmic`) = config 영속. IBM Q Runtime 토큰 받으면 cloud_real swap.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 221 | qiskit-aer statevector facade (4-backend enum, hexa-only strict raw#9) | ✅ 4/4 |
| `bell_state.hexa` | 353 | PHYS-P18-2 Bell |Φ+⟩ shared 2-qubit state 분산 entanglement (EPR pair) | ✅ T1-T5 |
| `cloud_real_ibm_q_facade.hexa` | 413 | Phase 2 IBM Q Runtime backend swap (qiskit-aer POC contract 위) | 🟡 pre-flight |

## falsifier

- cloud_facade: 4/4 (statevector normalization + amplitude)
- bell_state: T1-T5 (Bell state perfect correlation, single-qubit incoherent baseline)
- cloud_real_ibm_q: token + IBM Q quota 보유 시 LIVE swap

## cross-link

- [substrate entries](../entries/substrate/quantum/) — 3 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/aws_braket_signup_guide.md`](../docs/aws_braket_signup_guide.md) — Braket alternative
- [`trapped_ion/cloud_facade_poc.hexa`](../trapped_ion/cloud_facade_poc.hexa) — IonQ Forte gate-based 짝
- archive: `recovered/chip-architecture/quantum-consciousness-chip.md` — surface code + Leech lattice qubit paper
