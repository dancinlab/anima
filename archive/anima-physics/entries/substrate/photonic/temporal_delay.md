# photonic/temporal_delay.hexa

> Optical delay-line reservoir (N=8 taps, τ=1 sample) — Husserlian retention kernel · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P6-1 ("광자 temporal delay line — phase-delayed reservoir"). Jaeger 2001 reservoir computing + photonic realization (Paquot 2012, Larger 2017). 8-tap short-term memory kernel = "specious present" 의 minimal substrate.

## 작동 코드 / 의존성

- 원본: `photonic/temporal_delay.hexa` (397 LoC)
- 외부 의존: hexa run (tanh, cos)
- API: `process(signal: [float], taps: int) -> [float]`

## 비용 / 리소스

- $0 Mac sim
- 실 photonic: fiber coil / ring resonator (별 cycle BOM)

## 핵심 흐름 / ASCII

```
N = 8 taps, τ = 1 sample-period

  x(t) ──▶ [τ·1] ──▶ s_1 ──▶ [τ·1] ──▶ s_2 ──▶ ... ──▶ s_8
             │                │                          │
             ▼                ▼                          ▼
           φ_1              φ_2                         φ_8
             │                │                          │
       phase-shifted taps join the reservoir state:
           r_k = tanh(a_k · s_k · cos(φ_k) + b_k)
       linear readout:
           y(t) = Σ_k w_k · r_k

φ_k = k · Δφ (fixed grating)
universal short-term approximator up to O(N·τ)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/photonic/temporal_delay.hexa
```

## 검증 결과

- T1-T5 PASS
- 8-tap kernel + tanh saturation + linear readout 검증

## 관련 entry

- [photonic/mesh_network.md](./mesh_network.md)
- [photonic/cloud_facade_poc.md](./cloud_facade_poc.md)
- [prediction/protention_error.md](../prediction/protention_error.md) — protention sibling

## 출처

- README § 3 photonic/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P6-1
