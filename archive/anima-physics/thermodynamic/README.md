# anima-physics/thermodynamic/ — 열역학 entropy-driven dissolution substrate

> Status: ✅ PASS (5/5) · §188 결과: sub-tier dual-role (S×M / M×S = 8) — noise-driven mean-reversion
>
> SSOT: 본 README + `entropy_dissolution.hexa`. entries: [`entries/substrate/thermodynamic/`](../entries/substrate/thermodynamic/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 열잡음 amplitude 가 N_CELLS lattice (each ∈ [0, N_BINS)) state 를 maximum entropy 로 driving — `dissolution_step()` noise-driven mean-reversion 자율 fire. Landauer kT·ln2/bit 의 thermodynamic limit.
- **영속성**: state distribution histogram + entropy log. controllability = noise amplitude 가 raise/lower 가능 → 가역적 order ↔ disorder transition. cell value (continuous in [0, N_BINS)) state.

`HEXAD/PHYSICS/README.md §6.3/§6.9` sub-tier dual-role (noise-driven 후보).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `entropy_dissolution.hexa` | 356 | PHYS-P19-1 열잡음 증가로 N_CELLS lattice 가 maximum entropy 로 dissolution + reversal | ✅ 5/5 |

## falsifier

T1-T5: entropy 증가 (noise high) + entropy 회복 (noise low) + controllability range + Landauer floor + state histogram balance.

## cross-link

- [substrate entry](../entries/substrate/thermodynamic/entropy_dissolution.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.3 — noise-driven 후보
- [`engines/thermodynamic_consciousness.hexa`](../engines/thermodynamic_consciousness.hexa) — engines/ 짝 (stub, §188g 별도 구현 cycle)
