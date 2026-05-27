# arduino/cloud_facade_poc.hexa

> Local NgSpice NE555 555-timer astable RC-oscillator duty-cycle Monte Carlo (16 trials) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 4/4 PASS (16-trial MC). NgSpice deterministic on identical netlist+seed → byte-identical (G3). raw#9 hexa-only strict (exec(awk/sha/ngspice) only; **no .py / .sh helper**). Arduino IoT Cloud 가 substrate Phi-probe 부적합이라 NgSpice 로컬 sim 을 endpoint 로 wrapping = "cloud_sim_local_<sim>" facade 패턴.

## 작동 코드 / 의존성

- 원본: `arduino/cloud_facade_poc.hexa` (320 LoC)
- 네트리스트: `arduino/ne555_astable.cir` (frozen Monte Carlo)
- 외부 의존: ngspice (brew install ngspice) · awk / shasum
- 시뮬 파라미터: R1=10k±5%, R2=10k±5%, C=100n±10%, sgauss(seed=42), n=16 trial

## 비용 / 리소스

- $0 Mac local (NgSpice + hexa run)
- Phase 1 실 HW BOM (별도): Arduino Uno + Hall sensor ~$35 (docs/arduino-prototype-spec.md)

## 핵심 흐름 / ASCII

```
ne555_astable (R1=10k±5%, R2=10k±5%, C=100n±10%) × 16 MC
  positive  → duty std ≥ 0.001 (G1)   (nominal duty=2/3, σ ~ 0.005-0.010)
  negative  → tolerance=0 (ideal)     → all 16 trials identical → std=0 (G2 sign-flip)
G3 byte-identical · G4 backend == "local_ngspice_<ver>_ne555_astable_mc16"
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/arduino/cloud_facade_poc.hexa
hexa run anima-physics/arduino/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS (G1 duty std ≥ 0.001, G2 std=0, G3 byte-identical, G4 backend_name)
- docs/arduino_local_sim_landing.md: duty std 6.67e-3 vs 0 negative
- byte-identical 2-run determinism 검증

## 관련 entry

- [cmos/cloud_facade_poc.md](../cmos/cloud_facade_poc.md) — NgSpice ring osc sibling
- [memristor/cloud_facade_poc.md](../memristor/cloud_facade_poc.md) — NgSpice memristor sibling
- [fpga/cloud_facade_poc.md](../fpga/cloud_facade_poc.md) — iverilog sibling

## 출처

- README § 3 arduino/
- docs/arduino_local_sim_landing.md
- SCHEMA `anima_physics/cloud_facade_arduino/1`
