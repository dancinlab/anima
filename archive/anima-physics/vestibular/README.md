# anima-physics/vestibular/ — vestibular/haptic/visual multimodal sensor fusion

> Status: ✅ PASS · §188 결과: 5/5 (multi-sensor fusion 자율 estimate)
>
> SSOT: 본 README + `multimodal_fusion.hexa`. entries: [`entries/substrate/vestibular/`](../entries/substrate/vestibular/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: embodied agent 의 "where am I and what is touching me?" — vestibular (inner-ear head-orientation) + haptic (skin contact force) + visual (optic-flow self-motion) 3 distinct stream 의 자율 precision-weighted fusion. 각 stream 은 동일 egocentric direction estimate emit (각자 σ).
- **영속성**: per-stream Kalman state + fused estimate state propagation. body-pose 영속 ledger.

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `multimodal_fusion.hexa` | 241 | PHYS-P7-3 vestibular/haptic/visual 3-stream precision-weighted egocentric direction fusion | ✅ 5/5 |

## falsifier

T1-T5: per-stream noise calibration + precision-weight 정확도 + 3-stream agreement gate + outlier rejection + temporal continuity.

## cross-link

- [substrate entry](../entries/substrate/vestibular/multimodal_fusion.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §2 — substrate matrix
- [`proprioception/feedback_loop.hexa`](../proprioception/feedback_loop.hexa) — 3-DOF joint 짝 (body 내부)
- [`motor_cortex/command_encoding.hexa`](../motor_cortex/command_encoding.hexa) — output side 짝
- [`eeg/cross_substrate_phi_correlator.hexa`](../eeg/cross_substrate_phi_correlator.hexa) — 10-channel cross-substrate fusion 짝
