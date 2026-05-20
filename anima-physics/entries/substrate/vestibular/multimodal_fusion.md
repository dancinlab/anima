# vestibular/multimodal_fusion.hexa

> Vestibular + haptic + visual precision-weighted Bayesian fusion (Ernst & Banks 2002; Kording 2004) · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — README "🟡 (file detected, content estimated)" 분류. PHYS-P7-3 ("vestibular/haptic integration — multimodal sensor fusion"). T1-T2+ self-test 정의 (equal precision → mean / dominant takes over / degenerate handling). Varela sensorimotor binding cross-modality substrate.

## 작동 코드 / 의존성

- 원본: `vestibular/multimodal_fusion.hexa` (241 LoC)
- 외부 의존: hexa run
- API: `fuse(v: float, h: float, vis: float, precisions: [float]) -> float`

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
3 sensory streams (same egocentric direction):
  v   vestibular   (inner-ear head-orientation)
  h   haptic       (skin-level contact force)
  vis visual       (optic-flow self-motion)

Bayesian precision-weighted posterior mean (assuming Gaussian, known precisions):
  θ̂ = (π_v·v + π_h·h + π_vis·vis) / (π_v + π_h + π_vis)

Degenerate handling:
  all π = 0       → arithmetic mean (uninformative prior)
  π < 0           → clamp to 0
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/vestibular/multimodal_fusion.hexa
```

## 검증 결과

- T1 equal precision (π=[1,1,1]) → plain mean (v+h+vis)/3
- T2 dominant modality (π=[1000,1,1]) → θ̂ ≈ v
- self-test full PASS evidence README 미공시 (🟡 partial)

## 관련 entry

- [proprioception/feedback_loop.md](../proprioception/feedback_loop.md) — 3-DOF sibling
- [motor_cortex/command_encoding.md](../motor_cortex/command_encoding.md)

## 출처

- README § 3 vestibular/
- shared/roadmaps/anima.json PHYS-P7-3
- Ernst & Banks 2002 / Kording 2004
