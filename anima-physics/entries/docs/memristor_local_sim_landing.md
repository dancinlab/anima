# docs/memristor_local_sim_landing.md

> PHYS-P25 memristor Biolek HP TiO2 ngspice + PySpice; 4-gate PASS (hysteresis area 6.82e-3 V·A vs 4.18e-14 resistor) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 4/4 PASS. HP / HPE / Knowm / Crossbar / IBM Analog AI Cloud Composer 모두 public REST API 부재 → NgSpice + Biolek HP TiO2 subcircuit 로컬 시뮬 endpoint.

## 작동 코드 / 의존성

- `anima-physics/docs/memristor_local_sim_landing.md` (landing report)
- 의존: `memristor/cloud_facade_poc.hexa`
- 외부: NgSpice 46 + Biolek 2009 model · (secondary) PySpice 1.5 wrapper

## 비용 / 리소스

- 비용: $0 (Mac local, NgSpice batch `-b -n`)
- 필요한 도구: NgSpice 46 (brew install ngspice) · `hexa run`

## 핵심 흐름 / 구조

```
Biolek HP TiO2 thin-film memristor (Strukov-Williams 2008 + Biolek 2009 SPICE):
  M(q) = R_off + (R_on - R_off) * w/D
  dw/dt = μ_v * R_on * i(t) / D  (window function)

Probe: pinched I-V hysteresis loop (sine 1V @ 1Hz)
  shoelace area = ∮ I dV (hysteresis 영역 면적)

4-gate contract:
  G1 positive memristor → area ≥ 1e-3 V·A (실측 6.82e-3)
  G2 negative resistor (M = constant) → area ≈ 0 (실측 4.18e-14)
  G3 byte-identical sha
  G4 backend == "local_ngspice_<ver>_biolek_hp_tio2"

선택 근거 (web-search 2026-04):
  HP / HPE: research demos only, no API
  Knowm: SDK only, no hosted API
  Crossbar / Weebit Nano: foundry partnership only
  IBM Analog AI Cloud Composer: GUI only, no REST
  → NgSpice 46 + Biolek PICK (open-source, deterministic batch)
```

## 트리거 (fire 방법)

```bash
brew install ngspice
hexa run /Users/ghost/core/anima/anima-physics/memristor/cloud_facade_poc.hexa
```

## 검증 결과

- G1 hysteresis area = 6.82e-3 V·A ≥ 1e-3 PASS
- G2 resistor area = 4.18e-14 ≈ 0 PASS
- G3 byte-identical PASS
- G4 backend_name PASS
- **4/4 PASS** (commit dd8fdbdb, 2026-04-26)

## 관련 entry

- [analog-photonic-memristor](analog-photonic-memristor.md)
- [cmos_local_sim_landing](cmos_local_sim_landing.md)
- [arduino_local_sim_landing](arduino_local_sim_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
