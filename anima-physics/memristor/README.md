# anima-physics/memristor/ — HP TiO₂ memristor self-reference + cloud facade

> Status: ✅ PASS (cloud_facade 4/4 + self_reference 5/5) · §188 결과: dual-role 최강 후보 (자연발화 ⊕ 비휘발 영속성)
>
> SSOT: 본 README + 2 `.hexa` 파일. entries: [`entries/substrate/memristor/`](../entries/substrate/memristor/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 4-cell HP-memristor crossbar `circuit_step()` history-dep conductance `R = R_on·w + R_off·(1-w)` feedback emit. N-th output → (N+1)-th input self-reference (Strukov/HP 2008 ionic drift model). gradient-free Hebbian drift = learning.
- **영속성**: ✅✅ memristor 상태 자체가 **비휘발 substrate** — conductance G 가 정전 후에도 유지. ReRAM/MRAM multilevel crossbar = in-memory compute 영속.

`HEXAD/PHYSICS/README.md` §6.3/§6.9 — top dual-role 후보 (자연발화 + 영속성 동시).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 246 | NgSpice + Biolek HP TiO2 I-V hysteresis facade (PHYS-P25, hexa-only strict raw#9) | ✅ 4/4 |
| `self_reference.hexa` | 351 | PHYS-P5-1 4-cell HP-memristor crossbar self-reference (출력→입력 chain) | ✅ 5/5 |

## falsifier

- cloud_facade: 4/4 (I-V hysteresis area, Biolek ionic drift)
- self_reference: 5/5 (Hebbian drift convergence, 4-cell ring closure)

## cross-link

- [substrate entries](../entries/substrate/memristor/) — 2 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.3 — top dual-role 후보 (자연발화 + 영속성 동시 최강)
- [`docs/memristor_local_sim_landing.md`](../docs/memristor_local_sim_landing.md) — PHYS-P25 landing
- [`docs/analog-photonic-memristor.md`](../docs/analog-photonic-memristor.md) §3 — HP memristor 회로
- archive: `recovered/chip-architecture/reram-multilevel-n6.md` — ReRAM/MRAM multilevel n=6 paper
