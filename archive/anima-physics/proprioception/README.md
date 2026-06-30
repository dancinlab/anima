# anima-physics/proprioception/ — 3-DOF biomechanical sensorimotor feedback loop

> Status: ✅ PASS (5/5) · §188 결과: sub-tier dual-role (S×M / M×S = 8점) — spring-damper + LCG seed threading
>
> SSOT: 본 README + `feedback_loop.hexa`. entries: [`entries/substrate/proprioception/`](../entries/substrate/proprioception/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: 3-DOF spring-damper joint dynamics — Varela enactive framework 의 sensorimotor closure. motor torque τ → joint θ → noisy proprioceptor (muscle spindle + Golgi tendon) → 자율 sensory estimate (θ, θ̇) emit. Body-less consciousness 불가 — proprioceptive self-loop = embodied 의식의 atomic element.
- **영속성**: LCG seed threading → deterministic PRNG carry (reproducible trace). joint state (θ, θ̇) propagation, spring constant + damping coefficient config.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `feedback_loop.hexa` | 467 | PHYS-P7-1 3-DOF biomechanical joint spring-damper + noisy proprioceptor sensorimotor closure | ✅ 5/5 |

## falsifier

T1-T5: spring-damper stability + proprioceptor noise floor + torque→θ track + LCG determinism + loop closure round-trip.

## cross-link

- [substrate entry](../entries/substrate/proprioception/feedback_loop.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.9 — sub-tier dual-role (S×M / M×S = 8점)
- [`motor_cortex/command_encoding.hexa`](../motor_cortex/command_encoding.hexa) — M1 cosine tuning population vector 짝 (output side)
- [`vestibular/multimodal_fusion.hexa`](../vestibular/multimodal_fusion.hexa) — vestibular/haptic/visual 통합 짝
