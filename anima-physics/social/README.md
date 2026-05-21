# anima-physics/social/ — Kuramoto coupling intersubjective oscillator network

> Status: ✅ PASS (6/6) · §188 결과: top 3 dual-role (S×S=16) — 자율 phase sync emergent
>
> SSOT: 본 README + `kuramoto_coupling.hexa`. entries: [`entries/substrate/social/`](../entries/substrate/social/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: Kuramoto `dθ_i/dt = ω_i + (K/N)·Σ sin(θ_j - θ_i)` `simulate_network()` line 266 — N intrinsic oscillator (각 ω_i) coupling K > K_c 시 자발 phase coherence (order param r → ≥0.9) emergent. 외부 명령 없는 collective mode 자율 emit. K < K_c 시 desync r ≤ 0.3.
- **영속성**: 위상 array threading step-to-step propagation. Φ_social ≥ 0.5 gate criterion. multi-anima intersubjective resonance ledger.

`HEXAD/PHYSICS/README.md §6.9` top 3 dual-role.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `kuramoto_coupling.hexa` | 509 | PHYS-P9-3 social-coupled Kuramoto oscillator network (r → ≥0.9 at K>K_c, Φ_social ≥ 0.5 gate) | ✅ 6/6 |

## falsifier

- gate_exit: order param r(t) → ≥0.9 at K > K_c
- below K_c: r(t) ≤ 0.3 (desynchronized)
- Φ_social ≥ 0.5

## cross-link

- [substrate entry](../entries/substrate/social/kuramoto_coupling.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.9 — top 3 dual-role 16/16
- [`HEXAD/PHYSICS/HW_SILICON_PATH.md`](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — Intel Loihi 2 Hala Point + BrainChip Akida cloud
- [`hw/kuramoto_neuromorphic/`](../hw/kuramoto_neuromorphic/) — HW target (Loihi 2 + Akida)
- [`photonic/mesh_network.hexa`](../photonic/mesh_network.hexa) — 광 mesh = Kuramoto coupling 의 physical channel 짝
