# memristor/self_reference.hexa

> 4-cell HP-memristor crossbar self-reference circuit (N-th output → (N+1)-th input + feedback loop) Strukov 2008 ionic-drift · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — T1-T5 self-test 정의. PHYS-P5-1 ("멤리스터 self-reference 회로 — 자기 출력을 입력으로"). HEXA-FIRST pure .hexa. 자의식 reflexivity 의 물리 substrate.

## 작동 코드 / 의존성

- 원본: `memristor/self_reference.hexa` (351 LoC)
- 외부 의존: hexa run
- API: `simulate_n_steps(n: int) -> [float]` → o_3 trace

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / ASCII

```
4-cell HP-memristor crossbar circuit:

  x_0 (seed) ─▶ cell_0 ──▶ o_0 ──▶ cell_1 ──▶ o_1 ──▶ cell_2 ──▶ o_2 ──▶ cell_3 ──▶ o_3
                                                                                      │
        ◀──────────────────────── feedback loop (o_3 → cell_0 next step) ◀───────────┘

At step t:
  in_i(t) = SELF_GAIN · out_{i-1}(t)            for i > 0
  in_0(t) = FEEDBACK_GAIN · out_3(t-1) + SEED_AMP · seed
  out_i(t) = sigmoid(in_i(t) · w_i)
  w_i += η · pre · post · (1 − w_i) · w_i       (Hebbian, w ∈ [w_min, w_max])
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/memristor/self_reference.hexa
```

## 검증 결과

- T1 non-volatility (w ∈ [w_min, w_max] after 50 steps)
- T2 self-feedback propagates (o_3 변화 vs frozen)
- T3 Hebbian Cauchy (monotone shrinking Δ)
- T4 API contract (n samples returned)
- T5 determinism (2-run bit-identical)

## 관련 entry

- [memristor/cloud_facade_poc.md](./cloud_facade_poc.md) — working NgSpice sim
- [engines/memristor_consciousness.md](../engines/memristor_consciousness.md)
- [fpga/strange_loop.md](../fpga/strange_loop.md) — sibling self-ref (FPGA LUT)

## 출처

- README § 3 memristor/
- shared/roadmaps/anima.json PHYS-P5-1
- Strukov et al. 2008 Nature
