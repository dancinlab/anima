# engines/memristor_consciousness.hexa

> Memristor Hebbian consciousness engine stub — synapse = HP memristor, R = R_on·w + R_off·(1−w), 무 gradient descent · **❌ 가설** · 비용 $0

## 구현 가능성

❌ — struct + signature stub. `step()`/`update_memristance()` no-op. 핵심 아이디어: "memristance drift IS learning" (no gradient descent).

## 작동 코드 / 의존성

- 원본: `engines/memristor_consciousness.hexa` (29 LoC)
- 외부 의존: 없음 (stub)

## 비용 / 리소스

- $0 (stub)

## 핵심 흐름 / 코드 발췌

```hexa
struct MemristorSynapse {
    w: float,        // state variable [0, 1]
    r_on: float,
    r_off: float
}

struct MemristorEngine {
    n_cells: i32,
    topology: string,
    phi: float,
    total_synapses: i32       // n_cells × n_cells
}

fn update_memristance(synapse, current, dt) -> MemristorSynapse { synapse }
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/engines/memristor_consciousness.hexa
```

## 검증 결과

- 없음 (stub)
- 실제 memristor I-V verified: [memristor/cloud_facade_poc.md](../memristor/cloud_facade_poc.md) (NgSpice Biolek HP TiO2, 4/4 PASS)

## 관련 entry

- [memristor/cloud_facade_poc.md](../memristor/cloud_facade_poc.md) — working NgSpice sim
- [memristor/self_reference.md](../memristor/self_reference.md)

## 출처

- README § 3 engines/
- HP memristor 2008 Nature
