# engines/izhikevich_consciousness.hexa

> Biological spiking neuron consciousness engine stub (Izhikevich 2003 RS/IB/CH/FS/LTS 20+ patterns) · **❌ 가설** · 비용 $0

## 구현 가능성

❌ — struct + signature stub. `step()` no-op. `get_params("RS")` 만 hard-coded (a=0.02, b=0.2, c=-65, d=8). impl 미작성.

## 작동 코드 / 의존성

- 원본: `engines/izhikevich_consciousness.hexa` (31 LoC)
- 외부 의존: 없음 (stub)
- ODE: v' = 0.04v² + 5v + 140 − u + I, u' = a(bv − u)

## 비용 / 리소스

- $0 (stub)

## 핵심 흐름 / 코드 발췌

```hexa
struct IzhikevichParams {
    a: float, b: float, c: float, d: float,
    neuron_type: string
}

struct IzhikevichEngine {
    n_cells: i32,
    topology: string,
    phi: float,
    spike_count: i32
}

fn get_params(neuron_type: string) -> IzhikevichParams {
    // RS: a=0.02, b=0.2, c=-65, d=8
    return IzhikevichParams(0.02, 0.2, -65.0, 8.0, neuron_type)
}
// v' = 0.04 v² + 5v + 140 − u + I
// u' = a (b v − u)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/engines/izhikevich_consciousness.hexa
```

## 검증 결과

- 없음 (stub)

## 관련 entry

- [engines/snn_consciousness.md](./snn_consciousness.md) — LIF sibling (simpler model)
- [consciousness-loop/src/snn_main.md](../consciousness-loop/src/snn_main.md) — LIF working impl

## 출처

- README § 3 engines/
- Izhikevich 2003 spiking neuron model
