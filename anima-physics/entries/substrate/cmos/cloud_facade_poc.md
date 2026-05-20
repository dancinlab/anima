# cmos/cloud_facade_poc.hexa

> Local NgSpice 5-stage CMOS inverter ring oscillator period jitter · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 4/4 PASS. 180nm L1 NMOS/PMOS 5-stage ring osc, NgSpice deterministic. raw#9 hexa-only strict. docs/cmos_local_sim_landing.md landing PASS (jitter 4.64ps vs 0).

## 작동 코드 / 의존성

- 원본: `cmos/cloud_facade_poc.hexa` (311 LoC)
- 네트리스트: `cmos/cmos_ring_osc.cir` (5-stage ring, 180nm BSIM3)
- 외부 의존: ngspice · awk · shasum

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / ASCII

```
5-stage CMOS inverter ring (180nm L1 NMOS/PMOS)
  positive  Vdd=1.8V → ~8.85 GHz, period jitter σ ≥ 1 ps (G1)
  negative  Vdd=0.3V → sub-threshold, no oscillation, jitter=0 (G2)
G3 byte-identical (NgSpice deterministic on identical netlist+seed)
G4 backend == "local_ngspice_<ver>_cmos_ring_osc_5stage"
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/cmos/cloud_facade_poc.hexa
hexa run anima-physics/substrate/cmos/cloud_facade_poc.hexa --selftest
```

## 검증 결과

- 4/4 PASS
- docs/cmos_local_sim_landing.md: jitter 4.64ps positive vs 0 negative
- byte-identical 2-run determinism

## 관련 entry

- [arduino/cloud_facade_poc.md](../arduino/cloud_facade_poc.md) — NgSpice NE555 sibling
- [memristor/cloud_facade_poc.md](../memristor/cloud_facade_poc.md) — NgSpice memristor sibling
- [fpga/cloud_facade_poc.md](../fpga/cloud_facade_poc.md) — iverilog sibling

## 출처

- README § 3 cmos/
- docs/cmos_local_sim_landing.md
