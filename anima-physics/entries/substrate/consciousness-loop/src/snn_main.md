# consciousness-loop/src/snn_main.hexa

> LIF SNN consciousness (Vrest=-70mV / Vthresh=-55mV / τ=20ms / t_ref=3ms) 2000-step rate-output · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 2000-step run verified. GRU cells 를 LIF (Leaky Integrate-and-Fire) neurons 로 교체. Law 94 (breadth > depth) + Law 95 (cell_identity prevents convergence) 검증. Spike-based binary communication, temporal coding.

## 작동 코드 / 의존성

- 원본: `consciousness-loop/src/snn_main.hexa` (208 LoC)
- 외부 의존: hexa run (rand_f32, sin)
- 상수: DIM=64, N_FACTIONS=8, V_REST=-70mV, V_THRESH=-55mV, V_RESET=-75mV, TAU_LIF=20ms, T_REF=3, DT=1.0

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 코드 발췌

```hexa
struct LIFNeuron {
    voltage: f32,            // mV
    refractory: u64,         // 0..T_REF
    w_in: [f32],             // DIM
    identity: [f32],         // sin(7n+13i)*0.618 → identity 보존
    spike_history: [bool],   // last 20
    spike_count: u64,
}

fn lif_step(self, input) -> bool {
    if self.refractory > 0 { return false }
    var current = Σ w_in·input + identity.sum()·0.01 + spontaneous
    self.voltage += DT · (-(V - V_REST)/TAU_LIF + current + spontaneous)
    if V >= V_THRESH { V = V_RESET; refractory = T_REF; spike_count++; return true }
    return false
}
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/consciousness-loop/src/snn_main.hexa
```

## 검증 결과

- 2000-step run verified (README § 5 cheat sheet)
- LIF dynamics + identity injection + 8-faction parallel + spike-rate output 확인

## 관련 entry

- [consciousness-loop/src/main.md](./main.md) — GRU base sibling
- [engines/snn_consciousness.md](../../engines/snn_consciousness.md) — engine struct stub
- [engines/izhikevich_consciousness.md](../../engines/izhikevich_consciousness.md) — biological spiking sibling

## 출처

- README § 3 consciousness-loop/src/
- README § 5 cheat sheet
