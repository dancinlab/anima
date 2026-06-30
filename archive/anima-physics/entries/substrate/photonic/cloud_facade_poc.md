# photonic/cloud_facade_poc.hexa

> Perceval (Quandela) SLOS Fock photon-number entropy — 4-mode 50:50 BS cascade · **🟡 부분** · 비용 Perceval free (Python wheel)

## 구현 가능성

🟡 — SF (Strawberry Fields) blocked (scipy 1.17 removed `scipy.integrate.simps`, py3.14 wheel constraint). Perceval fallback ready. SLOS = deterministic strong-simulation Fock backend. Phase 2 real-HW (Xanadu X-series / Quandela Ascella) swap-only.

## 작동 코드 / 의존성

- 원본: `photonic/cloud_facade_poc.hexa` (267 LoC)
- Helper: `scripts/anima_physics_photonic_probe.py` (raw#37 transient)
- 외부 의존: hexa run · python3 · perceval-quandela 1.1.0
- enum: {local_hexa, cloud_sim_qiskit_aer, cloud_real_ibm_q, cloud_sim_strawberryfields_fock, cloud_sim_perceval, cloud_real_xanadu_x, cloud_real_quandela_ascella}

## 비용 / 리소스

- $0 (Perceval Python wheel free)
- Phase 2 cloud_real_xanadu_x / cloud_real_quandela_ascella: provider-specific

## 핵심 흐름 / ASCII

```
4-mode 5-stage 50:50 BS cascade

positive  |1,1,0,0>  →  10 distinct Fock states  H ≈ 1.6233 nat (G1 ≥ 0.5)
vacuum    |0,0,0,0>  →  stays |0,0,0,0>           H = 0          (G2 sign-flip)
G3 byte-identical 2-run (SLOS strong-sim deterministic)
G4 backend == "perceval_slos_fock"
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/photonic/cloud_facade_poc.hexa
hexa run anima-physics/photonic/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS ready (Perceval fallback)
- SF blocked (scipy 1.17 incompat)
- byte-identical 2-run (SLOS deterministic)

## 관련 entry

- [photonic/mesh_network.md](./mesh_network.md)
- [photonic/temporal_delay.md](./temporal_delay.md)
- [engines/photonic_consciousness.md](../engines/photonic_consciousness.md)
- [quantum/cloud_facade_poc.md](../quantum/cloud_facade_poc.md) — sibling A

## 출처

- README § 3 photonic/
- docs/analog-photonic-memristor.md
