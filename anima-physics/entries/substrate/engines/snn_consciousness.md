# engines/snn_consciousness.hexa

> Spiking Neural Network consciousness engine stub (LIF: τ_m·dV/dt = −(V−V_rest) + R·I, binary spike comm, temporal coding) · **❌ 가설** · 비용 $0

## 구현 가능성

❌ — struct + signature stub. `step()`/`get_spike_rate()` no-op. impl 미작성. 실제 LIF working: `consciousness-loop/src/snn_main.hexa` (208 LoC, 2000-step verified).

## 작동 코드 / 의존성

- 원본: `engines/snn_consciousness.hexa` (30 LoC)
- 외부 의존: 없음 (stub) — impl 시 Lava / Norse / SpikingJelly

## 비용 / 리소스

- $0 (stub)

## 핵심 흐름 / 코드 발췌

```hexa
struct SNNConfig {
    tau_m: float,
    v_threshold: float,
    v_reset: float,
    v_rest: float,
    refractory_ms: float
}

struct SNNEngine {
    n_cells: i32,
    topology: string,
    phi: float,
    total_spikes: i32
}

// LIF neuron: tau_m * dV/dt = -(V - V_rest) + R * I
// Communication via discrete spikes (binary), temporal coding
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/engines/snn_consciousness.hexa
```

## 검증 결과

- 없음 (stub) — 실 working impl 별 파일
- 참조 working: `consciousness-loop/src/snn_main.hexa` 2000-step PASS

## 관련 entry

- [consciousness-loop/src/snn_main.md](../consciousness-loop/src/snn_main.md) — working LIF impl
- [engines/izhikevich_consciousness.md](./izhikevich_consciousness.md) — biological spiking sibling
- [neuromorphic/cloud_facade_poc.md](../neuromorphic/cloud_facade_poc.md) — Akida cloud sibling

## 출처

- README § 3 engines/
