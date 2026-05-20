# fpga/strange_loop.hexa

> Hofstadter strange loop FPGA lattice — 2-layer (A, B) 4-bit LUTs, mutual recursion (A defines B defines A) · **❌ 가설** · 비용 $0 sim

## 구현 가능성

❌ — 396 LoC but README minimal stub 분류. PHYS-P5-2 ("FPGA strange loop lattice — Hofstadter 2층 자기 참조"). Mutual-recursion LUT 정의 + attractor (fixed point + short limit cycle) detection 명세. nested_lattice.hexa 가 본 모듈 L1 으로 인용.

## 작동 코드 / 의존성

- 원본: `fpga/strange_loop.hexa` (396 LoC)
- 외부 의존: hexa run

## 비용 / 리소스

- $0 Mac sim

## 핵심 흐름 / ASCII

```
N = 4 cells per layer, 2 layers (A, B)

  layer A:  a0 ─┬─ a1 ─┬─ a2 ─┬─ a3      (4 cells, state ∈ {0..15})
                ▼      ▼      ▼      ▼
  layer B:  b0 ─┴─ b1 ─┴─ b2 ─┴─ b3      (4 cells, state ∈ {0..15})
                ▲      ▲      ▲      ▲
                │      │      │      │    (B's truth table = f(A's outputs))
                └──────┴──────┴──────┘
                       (A's truth table = f(B's outputs))

→ Paradoxical self-reference: no base level
→ Detect attractors: fixed points + short limit cycles
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/fpga/strange_loop.hexa
```

## 검증 결과

- Mutual-recursion LUT 정의 완료
- Attractor detection 명세 (fixed point / short limit cycle)
- minimal stub (README 분류)

## 관련 entry

- [fpga/nested_lattice.md](./nested_lattice.md) — L1 base + L2 observer + L3 meta
- [fpga/microtubule_lattice_16.md](./microtubule_lattice_16.md)

## 출처

- README § 3 fpga/
- shared/roadmaps/anima.json PHYS-P5-2
