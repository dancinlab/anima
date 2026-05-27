# anima-physics/neuromorphic/ — BrainChip Akida cloud-facade neuromorphic substrate

> Status: 🟡 partial (token 부재 시 surrogate, token 받으면 cloud_real swap) · §188 결과: surrogate 4/4 PASS
>
> SSOT: 본 README + `cloud_facade_poc.hexa`. entries: [`entries/substrate/neuromorphic/`](../entries/substrate/neuromorphic/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: Akida 2nd gen on-chip LIF spike + STDP 자율 발화. Mac arm64 + Py3.14 wheel 부재 → surrogate algorithmic mode (event-based emit pattern simulate).
- **영속성**: substrate_backend enum (frozen contract sibling quantum 와 isomorphic — `local_hexa` / `cloud_sim_akida_simulator` / `cloud_real_akida_2gen` / `surrogate_algorithmic`). 토큰 받으면 cloud_real_akida 로 즉시 swap.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 274 | BrainChip Akida Cloud 8-substrate facade (4-backend enum, surrogate fallback) | ✅ 4/4 (surrogate) |

## falsifier

verdict tier 4-backend: `local_hexa` / `cloud_sim_akida_simulator` / `cloud_real_akida_2gen` / `surrogate_algorithmic`.

## cross-link

- [substrate entry](../entries/substrate/neuromorphic/cloud_facade_poc.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/akida_cloud_signup_guide.md`](../docs/akida_cloud_signup_guide.md) — Akida $1/day trial 가입
- [`docs/loihi-integration-spec.md`](../docs/loihi-integration-spec.md) — Loihi 2 통합 spec (131K neuron)
- [`hw/kuramoto_neuromorphic/`](../hw/kuramoto_neuromorphic/) — Loihi 2 + Akida HW realization (kuramoto)
- archive: `recovered/chip-architecture/neuromorphic-consciousness-chip.md` — n=6 LIF + ReRAM 시냅스 paper
