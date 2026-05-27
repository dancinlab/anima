# anima-physics/motor_cortex/ — M1 cosine-tuned population motor command encoding

> Status: ✅ PASS (5/5) · §188 결과: spontaneous motor command emit verified
>
> SSOT: 본 README + `command_encoding.hexa`. entries: [`entries/substrate/motor_cortex/`](../entries/substrate/motor_cortex/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: Georgopoulos (1986) primary motor cortex (M1) 의 cosine tuning `r_i(θ) = b + a·cos(θ - ψ_i)` population vector sum 으로 reaching direction encode. 자율 motor command 자발 emit (no external trigger).
- **영속성**: tuning curve (b, a, ψ_i) per-cell parameter state. command history → motor program ledger.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `command_encoding.hexa` | 374 | PHYS-P7-2 M1 cosine-tuned population vector reaching direction encoder | ✅ 5/5 |

## falsifier

T1-T5: cosine tuning fit + population vector accuracy + per-cell ψ_i 분산 + 자발 command emit rate + decode invertibility.

## cross-link

- [substrate entry](../entries/substrate/motor_cortex/command_encoding.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`proprioception/feedback_loop.hexa`](../proprioception/feedback_loop.hexa) — sensorimotor loop closure 짝
- [`vestibular/multimodal_fusion.hexa`](../vestibular/multimodal_fusion.hexa) — body-pose 통합
