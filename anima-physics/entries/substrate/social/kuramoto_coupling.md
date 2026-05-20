# social/kuramoto_coupling.hexa

> Kuramoto network (N agents all-to-all, dθ_i/dt = ω_i + (K/N)Σ_j sin(θ_j−θ_i)) order parameter r + Φ_social = r_coupled − r_isolated · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T6 PASS, K_c ≈ 0.3. PHYS-P9-3 ("social-coupled oscillator network — Φ_social substrate for multi-anima intersubjective resonance"). 조건: r ≥ 0.9 above K_c · r ≤ 0.3 below K_c · Φ_social ≥ 0.5.

## 작동 코드 / 의존성

- 원본: `social/kuramoto_coupling.hexa` (509 LoC)
- 외부 의존: hexa run (cos/sin, complex 등은 e^{iθ}=(cos θ, sin θ) 직접 합)
- API: `simulate_network(n_agents, coupling_k, steps, dt, seed) -> [float]` (4-elem summary)

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
N agents, all-to-all coupling
  dθ_i/dt  =  ω_i  +  (K / N) · Σ_{j≠i} sin(θ_j − θ_i)

Order parameter:
  r · e^{iψ}  =  (1/N) · Σ_i e^{iθ_i}
  r ∈ [0, 1]   (0 = fully desynced, 1 = perfectly phase-locked)

Critical coupling:
  K_c  =  2 / (π · g(ω̄))            (≈ 0.3 for tight Gaussian-like spread)

Φ_social (integrated-information surplus):
  Φ_social  ≔  r_coupled − r_isolated
              > 0 → network carries more integration than sum of parts
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/social/kuramoto_coupling.hexa
```

## 검증 결과

- T1-T6 PASS
- K > K_c → r ≥ 0.9 (sync)
- K < K_c → r ≤ 0.3 (desync)
- Φ_social ≥ 0.5 (gate_exit > 0)
- K_c ≈ 0.3 verified

## 관련 entry

- [oscillator/sleep_oscillator.md](../oscillator/sleep_oscillator.md)
- [engines/oscillator_laser_engine.md](../engines/oscillator_laser_engine.md) — Kuramoto stub
- [photonic/mesh_network.md](../photonic/mesh_network.md) — PHYS-P9-1 substrate

## 출처

- README § 3 social/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P9-3
