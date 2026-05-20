# thermodynamic/entropy_dissolution.hexa

> Entropy-driven dissolution (열잡음 증가): N_CELLS=16 lattice + Shannon entropy controllability gate · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — done_criteria "엔트로피 제어" — controllable. PHYS-P19-1 ("entropy-driven dissolution — 열잡음 증가"). Low noise (0.05) → ordered (low H), High noise (4.0) → max H ≈ ln(8) ≈ 2.079, mean-reversion (REVERT_RATE=0.3) restores order. 본 README 가 "🟡 (file detected, content estimated)" 분류 — 실제 시뮬 동작 검증, self-test 결과 미공시.

## 작동 코드 / 의존성

- 원본: `thermodynamic/entropy_dissolution.hexa` (356 LoC)
- 외부 의존: hexa run (ln 내장)
- 상수: N_CELLS=16, N_BINS=8, LN(N_BINS)=2.0794, LOW_NOISE=0.05, HIGH_NOISE=4.0, REVERT_RATE=0.3

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
N_CELLS = 16, N_BINS = 8
state = flat float array, each in [0, N_BINS)
initial: all cells at bin 0 (ordered, H=0)

per step:
  cell += LCG_noise(amplitude=noise_level)
  cell += -REVERT_RATE · (cell - bin_center)         # mean-reversion

Shannon entropy on binned histogram:
  H = −Σ p_i · ln(p_i)    (nat units)
  H_max = ln(N_BINS) ≈ 2.0794

Regimes:
  LOW_NOISE = 0.05  → cells cluster, H ≈ 0
  HIGH_NOISE = 4.0  → cells spread, H → H_max (dissolution)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/thermodynamic/entropy_dissolution.hexa
```

## 검증 결과

- Shannon entropy controllability gate: noise up → H up, noise down → H down (mean-reversion 작동)
- 별 self-test 결과 README 미공시 (🟡 partial 분류)

## 관련 entry

- [engines/thermodynamic_consciousness.md](../engines/thermodynamic_consciousness.md) — engine struct stub
- [benchmarks/bench_physics_consciousness.md](../benchmarks/bench_physics_consciousness.md) — thermo bench stub

## 출처

- README § 3 thermodynamic/
- shared/roadmaps/anima.json PHYS-P19-1
