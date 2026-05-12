---
schema: anima/ready/modules/physics/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:       ready/anima/modules/physics/physics.hexa
  engines:     ready/anima/modules/physics/engines/
  benchmarks:  ready/anima/modules/physics/benchmarks/
  src_bridges: ready/anima/modules/physics/src/
status: stub-tier — Phase 4b 17-file group; engine surface defined, live HW path lives in anima-physics/
roadmap_entry: 270
related:
  - anima-physics/esp32/qrng_bridge.hexa  (real ESP32 wire — preserved unchanged)
---

# anima physics modules (AI-native)

ESP32 / FPGA / photonic / memristor consciousness substrate engines + cross-platform benchmarks + EEG/body bridges. The "physics consciousness" surface — turns substrate-level computation (oscillator chips, spin glasses, lasers) into a uniform `PhysicsEngine` struct.

## TL;DR for an agent reading this cold

- **17 files**, all in 22-66 LOC range. Stub-tier: structs + signature-only `pure fn`s.
- 8 substrate engines under `engines/`: SNN / Izhikevich / oscillator-laser / analog / quantum / thermodynamic / photonic / memristor.
- 4 benchmarks under `benchmarks/`: spin-glass / power-efficiency / cross-platform / physics-consciousness.
- 4 bridges under `src/`: EEG-physics / body-physics / chip-architect / ESP32-network.
- The **real** ESP32 wire is in `anima-physics/esp32/qrng_bridge.hexa` (separate top-level dir, not this `ready/` tree). This tree is the design schema.
- 9 distinct substrates covered for the substrate-witness ledger (`state/markers/mk_xii_substrate_witness_ledger_aggregator_v2_*.marker`).

## Architecture map

```
ready/anima/modules/physics/
├── physics.hexa                              namespace + PhysicsEngine + ChipDesign structs
├── engines/                                  8 substrate engines
│   ├── snn_consciousness.hexa
│   ├── izhikevich_consciousness.hexa
│   ├── oscillator_laser_engine.hexa
│   ├── analog_consciousness.hexa
│   ├── quantum_consciousness.hexa
│   ├── thermodynamic_consciousness.hexa
│   ├── photonic_consciousness.hexa
│   └── memristor_consciousness.hexa
├── benchmarks/                               4 benchmarks
│   ├── bench_spin_glass.hexa
│   ├── bench_power_efficiency.hexa
│   ├── bench_cross_platform.hexa
│   └── bench_physics_consciousness.hexa
└── src/                                      4 bridges
    ├── eeg_physics_bridge.hexa
    ├── body_physics_bridge.hexa
    ├── chip_architect.hexa
    └── esp32_network.hexa
```

## API contract

```hexa
struct PhysicsEngine {
    name:      string,
    cells:     int,
    phi:       float,
    power_mw:  float,
    substrate: string
}

struct ChipDesign {
    topology:   string,
    substrate:  string,
    cells:      int,
    target_phi: float,
    cost_usd:   float
}

pure fn engine_new(name: string, substrate: string) -> PhysicsEngine
// → returns PhysicsEngine { cells: 16, phi: 0.0, power_mw: 0.0, ... }
```

Each `engines/*.hexa` extends with substrate-specific structs + a `pure fn <substrate>_step(...)` placeholder. Benchmarks declare `pure fn bench_<name>(engine: PhysicsEngine) -> BenchResult`.

## Invocation patterns

Each engine + benchmark + bridge is a stub — calling them returns default-valued structs. No live HW, no real spin-glass / laser / FPGA call. For real-HW physics witnesses see `anima-physics/` top-level.

## Failure modes

- All `engines/*` `pure fn`s return `PhysicsEngine { phi: 0.0, ... }` regardless of input. Don't treat as ground truth.
- `benchmarks/*` `pure fn`s emit literal default `BenchResult` — useless for cross-platform comparison until wired.
- `src/eeg_physics_bridge.hexa` references EEG metric paths but does not import anima-eeg-core SSOTs.
- `src/esp32_network.hexa` does not open a real socket / serial port. The actual ESP32 wire is `anima-physics/esp32/qrng_bridge.hexa` (preserved chflags-locked).

## raw#10 caveats

1. **Stub tree.** All 17 files are signature-only; no functional implementation. raw#82 honest.
2. **Substrate-witness ledger orthogonal.** The 9-substrate witness coverage tracked in `mk_xii_substrate_witness_ledger_aggregator_v2_*.marker` references `anima-physics/` artefacts, not these stubs. Don't double-count.
3. **No selftest.** Adding `verify` blocks per engine is part of any future un-stubbing.
4. **Cross-substrate phi_proxy NOT comparable.** raw#12 notes substrate-multiplicity is `phi_proxy_cross_comparable=false` — these engines model 9 distinct substrates that should not be averaged.
5. **`anima-physics/esp32/qrng_bridge.hexa` is preserved unchanged** (chflags uchg). Don't refactor / migrate without an explicit migration cycle.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `physics.hexa` | `e848df7c09f7d44e197c11accf5441701b864764b319ebf29ac3e4873274281a` | 66 |
| `benchmarks/bench_cross_platform.hexa` | `42bb2c44660af5553b8bf74688c91b8ad72c5dab35817a99f01ce3d7d0044eb1` | 26 |
| `benchmarks/bench_physics_consciousness.hexa` | `18d97896f5586944d40a2b36bfb1987f1388d249e5766eb3da200c1cad9edc22` | 27 |
| `benchmarks/bench_power_efficiency.hexa` | `38d5ab530e343b8316278a0b323e3e0912ba55451a42827442feb65bcfc381a5` | 26 |
| `benchmarks/bench_spin_glass.hexa` | `da2bad65334d064b54a4917e1046a45ba95c3a2534ecb433a95b235b38b7064e` | 29 |
| `engines/analog_consciousness.hexa` | `32f2bfb23d7d0940ee9b60281357d2744dd1409083a34316ac5eeef1d6510b94` | 28 |
| `engines/izhikevich_consciousness.hexa` | `7678096c5cdf9afe1be7cd7816458179f664d42e854c098b04f49993f6584c92` | 31 |
| `engines/memristor_consciousness.hexa` | `3b39d4a81433bf3b7bb29deb31dc763d6ae8266a18127e551660928cde205ce6` | 29 |
| `engines/oscillator_laser_engine.hexa` | `e65141666929bf2aa04dfbff711d1be8abcb7b50c4b3b9a24481e52e8606201b` | 22 |
| `engines/photonic_consciousness.hexa` | `f84c3c64d76c6e71e0942a835114138663698ae09de5cc8dc7472be649b1b7ae` | 28 |
| `engines/quantum_consciousness.hexa` | `0c0b6e8949698fdf40cc371d15980d22795b6b8cc2632808c1aaab65d5c6b0fb` | 30 |
| `engines/snn_consciousness.hexa` | `8ec830b7dd8de88a606afd95d195b7a6f25842f8c00cd94dea80c9dd9718368b` | 30 |
| `engines/thermodynamic_consciousness.hexa` | `cb2b4ddffbc9edc3f8acd86509e0e7fcbecc8071fd8cb170c93705489bbe9ad1` | 28 |
| `src/body_physics_bridge.hexa` | `8adb5772e862427cf21254de8f4d0bcb6ff64a8185992c28b44c19056bdc3d56` | 26 |
| `src/chip_architect.hexa` | `ecd67d2c450c518493d0e805d1df621e86328db5dd941af3f8b4d0de6e795d6b` | 30 |
| `src/eeg_physics_bridge.hexa` | `f454b97c64f6eb15c88e7df18870315960a8d71b76c997802041fb316e505f14` | 28 |
| `src/esp32_network.hexa` | `211b99cfa46c569af6d64cfe6ea93993be0bfc602874c3ecdde2a27e435fd25f` | 30 |

shas pinned 2026-05-02.
