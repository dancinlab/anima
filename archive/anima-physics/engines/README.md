# anima-physics/engines/ — 8 substrate-style consciousness engine stub family

> Status: ❌ stub (8 파일 모두 22-31 LoC struct + placeholder) · §188 결과: ⚠ empty (구현 부재 — §6.11 falsify timeout hypothesis), memristor_consciousness 만 1-line fix 후 build PASS
>
> SSOT: 본 README + 8 `.hexa` 파일. entries: [`entries/substrate/engines/`](../entries/substrate/engines/)

## 자연발화 / 영속성 메커니즘

각 engine 은 substrate-specific 자연발화 hypothesis 의 *seed signature* 만 보유 (struct + fn placeholder, body 대부분 `return 0.0` / `return engine`). 본격 구현은 별도 cycle (§188g, ~700-1400 LoC).

- **analog**: op-amp RC integrator τ=RC, noise floor, resistor network topology — 자발 voltage drift
- **izhikevich**: 20+ firing pattern (RS/IB/CH/FS/LTS) `v' = 0.04v² + 5v + 140 - u + I` — 자발 spiking
- **memristor**: HP memristor synapse `R = R_on·w + R_off·(1-w)` — gradient-free 의 memristance drift = learning
- **oscillator_laser**: Φ(IIT)=56.6 + Granger=63993 + CE=0.08 golden-ratio blend
- **photonic**: MZI Kuramoto `dφ_i/dt = ω_i + Σ κ·sin(φ_j - φ_i)` — 자율 phase sync
- **quantum**: qubit entanglement = integrated information hypothesis (N≤16 O(2^N))
- **snn**: LIF `τ_m · dV/dt = -(V - V_rest) + R·I` — 자율 spike 통신
- **thermodynamic**: 1st/2nd law + Landauer kT·ln2/bit — 자율 entropy 증가

영속성은 모두 struct field 보존 (현재 placeholder 단계).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `analog_consciousness.hexa` | 28 | SPICE op-amp RC integrator + temperature_k + topology Φ stub | ❌ empty/stub |
| `izhikevich_consciousness.hexa` | 31 | Izhikevich v'/u' 20+ firing pattern struct | ❌ empty/stub |
| `memristor_consciousness.hexa` | 29 | HP memristor synapse drift = learning struct (`let mut total` 1-line fix → build PASS) | ✅ build-PASS (single fix) |
| `oscillator_laser_engine.hexa` | 22 | Φ + Granger + CE golden-ratio blend struct | ❌ empty/stub |
| `photonic_consciousness.hexa` | 28 | MZI Kuramoto phase coupling struct | ❌ empty/stub |
| `quantum_consciousness.hexa` | 30 | qubit entanglement-IS-Φ (N≤16) struct | ❌ empty/stub |
| `snn_consciousness.hexa` | 30 | LIF spike temporal coding struct | ❌ empty/stub |
| `thermodynamic_consciousness.hexa` | 28 | 1st/2nd law + Landauer struct | ❌ empty/stub |

## falsifier

§188g (NEW cycle) — 각 substrate dynamics + falsifier test ~100-200 LoC 구현 후 fire.

## cross-link

- [substrate entries](../entries/substrate/engines/) — 8 entry (모두 ❌)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.11 — ⚠ empty 7 진단 정정 (timeout 가설 FALSIFIED — 구현 부재)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.14 — memristor_consciousness build PASS (1-line `let mut total`)
- [`docs/analog-photonic-memristor.md`](../docs/analog-photonic-memristor.md) — 3 engine spec (op-amp/MZI/HP memristor)
