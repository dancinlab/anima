# memristor/cloud_facade_poc.hexa

> NgSpice Biolek HP TiO2 memristor pinched I-V hysteresis shoelace area · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 4/4 PASS (mem 6.8e-3 V·A vs R 4e-14). NgSpice deterministic on identical netlist → byte-identical. raw#9 hexa-only strict + raw#37 transient .py helper. cloud API 부재 → NgSpice 로컬 시뮬 endpoint wrap.

## 작동 코드 / 의존성

- 원본: `memristor/cloud_facade_poc.hexa` (245 LoC)
- 외부 의존: ngspice · python3 venv (Biolek model spice file) · awk · shasum
- Helper: `scripts/anima_physics_memristor_ngspice_probe.py` (raw#37 transient)

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / ASCII

```
Biolek HP TiO2 memristor model
  input: 0.1 Hz sin, 1.5 V amplitude, 20 s, 2000 samples
  positive  → expected pinched I-V hysteresis area ≈ 6.8e-3 V·A  (G1 ≥ 1e-4)
  negative  pure 1kΩ resistor + 동일 input
            → expected area ≈ 4e-14 V·A  (numerical floor)        (G2 sign-flip)
  G3 byte-identical (ngspice deterministic)
  G4 backend == "local_ngspice_<ver>_biolek_hp_memristor"

shoelace formula: A = 1/2 · |Σ (x_i · y_{i+1} − x_{i+1} · y_i)|
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/memristor/cloud_facade_poc.hexa
hexa run anima-physics/memristor/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS (G1 hysteresis area 6.8e-3 vs 4e-14 resistor)
- docs/memristor_local_sim_landing.md landing
- byte-identical 2-run

## 관련 entry

- [memristor/self_reference.md](./self_reference.md)
- [engines/memristor_consciousness.md](../engines/memristor_consciousness.md) — stub
- [arduino/cloud_facade_poc.md](../arduino/cloud_facade_poc.md)
- [cmos/cloud_facade_poc.md](../cmos/cloud_facade_poc.md)

## 출처

- README § 3 memristor/
- docs/memristor_local_sim_landing.md
