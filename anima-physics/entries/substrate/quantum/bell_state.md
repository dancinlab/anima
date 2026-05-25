# quantum/bell_state.hexa

> Bell state |Φ⁺⟩=(|00⟩+|11⟩)/√2 perfect-correlation entanglement (entangled corr>0.95, separable |01⟩ corr<0.3) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P18-2 ("분산 양자 상태 — entanglement"). 4D Hilbert space (|00⟩, |01⟩, |10⟩, |11⟩) flat 4-amplitude array. Born rule + LCG deterministic measurement.

## 작동 코드 / 의존성

- 원본: `quantum/bell_state.hexa` (352 LoC)
- 외부 의존: hexa run (no qiskit required — pure hexa)
- API: `make_bell_phi_plus()` · `make_separable_0plus()` · `measure_correlation(sv, n_trials, seed)`

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 식

```
4-dim Hilbert space H_A ⊗ H_B  with basis {|00>, |01>, |10>, |11>}
state vector = [a_00, a_01, a_10, a_11]

|Φ⁺⟩ = (|00⟩ + |11⟩) / √2     →   sv = [1/√2, 0, 0, 1/√2]
|0+⟩ = |0⟩ ⊗ (|0⟩+|1⟩)/√2     →   sv = [1/√2, 1/√2, 0, 0]   (separable)

Born rule: P(|ij>) = |a_ij|²
LCG PRNG seeded per-trial → uniform u ∈ [0,1) → CDF lookup

Correlation: corr = count(qubit_A == qubit_B) / n_trials
  |Φ⁺⟩         expected corr ≈ 1.0 (perfect)
  |0+⟩ sep     expected corr ≈ 0.5 (A=0 always, B=0/1 50/50)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/quantum/bell_state.hexa
```

## 검증 결과

- T1-T5 PASS
- Entangled |Φ⁺⟩ corr > 0.95 PASS
- Separable |0+⟩ corr < 0.3 PASS (50/50 deviates from 1 by > 0.45)

## 관련 entry

- [quantum/cloud_facade_poc.md](./cloud_facade_poc.md) — qiskit-aer GHZ (cloud sim)
- [quantum/cloud_real_ibm_q_facade.md](./cloud_real_ibm_q_facade.md) — real IBM Q
- [engines/quantum_consciousness.md](../engines/quantum_consciousness.md) — engine stub

## 출처

- README § 3 quantum/
- README § 5 cheat sheet
- shared/roadmaps/anima.json PHYS-P18-2
