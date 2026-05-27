# anima-physics/benchmarks/ — 9×9 substrate × topology benchmark stubs

> Status: ❌ stub (4/4 시그니처만 존재, fn body 미구현) · §188 결과: N-A (benchmark, not substrate fire)
>
> SSOT: 본 README + 4 `.hexa` 파일.

## 자연발화 / 영속성 메커니즘

benchmarks/ 는 substrate code 가 아니라 **9 substrate × 9 topology = 81 config** 의 Φ / W·hr / spin-glass frustration / cross-platform metric 비교 stub. 자연발화/영속성 메커니즘 자체는 보유하지 않으며, 다른 substrate (oscillator/social/photonic 등) 의 결과를 모아 ranking 하는 metric harness 가 목표 (현재 struct + signature 만 정의).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `bench_cross_platform.hexa` | 26 | Law 22 substrate-invariant — Rust APEX22/SNN/Verilog/WebGPU/Erlang 5 platform 횡단 Φ 비교 stub | ❌ stub |
| `bench_physics_consciousness.hexa` | 27 | Thermo (entropy/free energy/Maxwell demon) + geom (Fisher/Ricci/IB) physics metric stub | ❌ stub |
| `bench_power_efficiency.hexa` | 26 | W per Φ unit — 9 substrate × 9 topology 81 config ranking stub | ❌ stub |
| `bench_spin_glass.hexa` | 29 | spin glass frustration vs ring/small-world/hypercube 풍부도 비교 stub | ❌ stub |

## falsifier

미정 (struct + fn signature 만, body return 0.0). 별도 cycle 구현 필요.

## cross-link

- [substrate entries](../entries/substrate/benchmarks/) — per-file detail (4 entry, 모두 ❌)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- §188 fire 대상 아님 (benchmark = metric 모음).
