# proprioception/feedback_loop.hexa

> 3-DOF biomechanical joint (spring-damper k=8.0 N·m/rad, c=1.2, I=0.15 kg·m², dt=0.005s=200Hz) + noisy proprioceptors (muscle spindles + Golgi tendon) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P7-1 ("proprioceptive feedback loop — joint/muscle sim"). Varela enactive sensorimotor coupling. Semi-implicit (symplectic) Euler integrator. Tri-sum CLT noise (σ_θ ≈ 0.01 rad / σ_θ̇ ≈ 0.05 rad/s).

## 작동 코드 / 의존성

- 원본: `proprioception/feedback_loop.hexa` (467 LoC)
- 외부 의존: hexa run
- API: `step(state: [float], torque: [float]) -> [float]` (flat 13-float bundle; struct-field-read bug 회피)
- 상수: k=8.0 N·m/rad, c=1.2 N·m·s/rad, I=0.15 kg·m², dt=0.005s (200Hz)

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
Per-DOF rotational 2nd-order ODE:
  θ̈ = (−k · θ − c · θ̇ + τ_applied) / I
    k          spring stiffness     [N·m / rad]
    c          damping coefficient  [N·m·s / rad]
    τ_applied  commanded torque     [N·m]
    I          rotational inertia   [kg·m²]

Semi-implicit (symplectic) Euler:
  θ̇_{t+1} = θ̇_t + dt · θ̈
  θ_{t+1}  = θ_t  + dt · θ̇_{t+1}
  (velocity first, then angle uses new velocity — energy-preserving)

Proprioceptive noise (biological spindles + Golgi tendon):
  additive Gaussian-ish (tri-sum CLT from LCG)
  σ_θ  ≈ 0.01 rad  (≈ 0.6°)
  σ_θ̇ ≈ 0.05 rad/s (≈ 3°/s)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/proprioception/feedback_loop.hexa
```

## 검증 결과

- T1-T5 PASS
- 200Hz update rate verified
- 3-DOF independent (decoupled by design)

## 관련 entry

- [motor_cortex/command_encoding.md](../motor_cortex/command_encoding.md) — torque source sibling
- [vestibular/multimodal_fusion.md](../vestibular/multimodal_fusion.md)

## 출처

- README § 3 proprioception/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P7-1
