# motor_cortex/command_encoding.hexa

> Georgopoulos 1986 population vector encoding (M1 motor cortex, 16 cosine-tuned neurons, ψ_i=2πi/16) round-trip θ→encode→decode · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS (round-trip error < 0.01 rad). PHYS-P7-2 ("motor cortex simulation — motor command encoding"). N=16 neurons uniformly spaced on [0, 2π), baseline b=1.0, tuning a=1.0, rates clamped ≥ 0.

## 작동 코드 / 의존성

- 원본: `motor_cortex/command_encoding.hexa` (374 LoC)
- 외부 의존: hexa run (cos/sin, atan2 내장)
- API: `encode(direction: float) -> [float]` (N=16) · `decode(population: [float]) -> float`

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
N = 16 neurons
preferred directions:  ψ_i = 2π · i / N,  i = 0..15

cosine tuning:
  r_i(θ) = b + a · cos(θ − ψ_i)        b=1.0 baseline, a=1.0 gain
  r_i = max(0, r_i)                    biologically positive rates

population vector decode:
  P(θ) = Σ_i  r_i · (cos ψ_i, sin ψ_i)        vector sum
  θ̂   = atan2(P_y, P_x)                        readout angle

round-trip target: |θ − θ̂| < 0.01 rad
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/motor_cortex/command_encoding.hexa
```

## 검증 결과

- T1-T5 PASS (round-trip error < 0.01 rad, N=16)
- Georgopoulos 1986 population vector reproduces θ within float precision

## 관련 entry

- [proprioception/feedback_loop.md](../proprioception/feedback_loop.md) — 3-DOF biomechanical sibling
- [hippocampus/episodic_replay.md](../hippocampus/episodic_replay.md) — narrative consolidation

## 출처

- README § 3 motor_cortex/
- README § 5 cheat sheet
- Georgopoulos et al. 1986
- shared/roadmaps/anima.json PHYS-P7-2
