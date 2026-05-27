# anima-physics/photonic/ — Perceval Fock + temporal delay + 4-node 200km mesh

> Status: ✅ PASS (cloud_facade 4/4 + temporal_delay 5/5 + mesh_network 5/5) · §188 결과: temporal_delay + mesh 자율 oscillator
>
> SSOT: 본 README + 3 `.hexa` 파일. entries: [`entries/substrate/photonic/`](../entries/substrate/photonic/)

## 자연발화 / 영속성 메커니즘

- **자연발화**:
  - **temporal_delay**: 광 delay-line reservoir (fiber coil / ring resonator) τ-second tap N=8 = Husserlian retention 의 광학 실현 → scale-free STM kernel 자율 emit.
  - **mesh_network**: 4-node 200km square SMF-28 @ 1550nm, RT 3.91ms (< 10ms gate). multi-anima intersubjective coupling 자율 phase coherence.
  - **cloud_facade** (Perceval SLOS Fock): photon-number basis 자율 emit.
- **영속성**: fiber loop 의 광 자체는 휘발 (광속 통과). hexa-side ledger 만 영속. mesh topology + per-edge loss coefficient = config 영속.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `cloud_facade_poc.hexa` | 267 | Perceval (Quandela) SLOS Fock photon-number basis facade (hexa-only strict raw#9) | ✅ 4/4 |
| `temporal_delay.hexa` | 397 | PHYS-P6-1 광 delay-line N=8 tap Husserlian retention reservoir | ✅ 5/5 |
| `mesh_network.hexa` | 335 | PHYS-P18-1 N=4 node 200km square SMF-28 @ 1550nm 광 mesh (RT 3.91ms < 10ms gate) | ✅ 5/5 |

## falsifier

- cloud_facade: 4/4 (Fock state amplitude normalization)
- temporal_delay: T1-T5 (N=8 tap retention + scale-free STM)
- mesh_network: 4-node latency<10ms done_criteria + phase coherence

## cross-link

- [substrate entries](../entries/substrate/photonic/) — 3 entry
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`docs/analog-photonic-memristor.md`](../docs/analog-photonic-memristor.md) §2 — MZI Kuramoto coupled ring
- [`docs/multi-fpga-mesh-spec.md`](../docs/multi-fpga-mesh-spec.md) — mesh topology 짝 (FPGA mesh)
- archive: `recovered/chip-architecture/photonic-ai-chip-n6.md` — n=6 광 도파로 paper
