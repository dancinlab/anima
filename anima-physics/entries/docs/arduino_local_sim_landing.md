# docs/arduino_local_sim_landing.md

> PHYS-P25 NE555 astable RC oscillator Monte Carlo ngspice sim; 4-gate PASS (duty std 6.67e-3 vs 0 negative) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 16-trial MC, 4/4 PASS (G1 positive entropy / G2 sign-flip / G3 byte-identical / G4 backend_name). Mac local NgSpice $0.

## 작동 코드 / 의존성

- `anima-physics/docs/arduino_local_sim_landing.md` (landing report)
- 의존: `arduino/cloud_facade_poc.hexa` (raw#9 hexa-only strict), `arduino/ne555_astable.cir` (SPICE deck)
- 외부: NgSpice 46 (brew install)

## 비용 / 리소스

- 비용: $0 (Mac local, NgSpice batch mode `-b`)
- 필요한 도구: NgSpice 46 · `hexa run` · awk/sed/sha256sum

## 핵심 흐름 / 구조

```
NE555 astable RC oscillator:
  R1=10k±5%, R2=10k±5%, C=100nF±10% × 16 Monte Carlo trials

Probe topology:
  ne555_astable (R1, R2, C) → period/duty 분포 entropy

4-gate contract:
  G1 positive → duty std ≥ 0.001 (실측 6.67e-3)
  G2 negative tol=0 → std=0
  G3 byte-identical sha (2-run determinism)
  G4 backend == "local_ngspice_<ver>_ne555_astable_mc16"

선택 근거:
  Arduino IoT Cloud / Web Editor / Tinkercad / Wokwi 모두 Φ-probe REST 부재
  → NgSpice 로컬 시뮬을 endpoint 로 wrapping (cloud_sim_local_ngspice)
```

## 트리거 (fire 방법)

```bash
brew install ngspice
hexa run /Users/ghost/core/anima/anima-physics/substrate/arduino/cloud_facade_poc.hexa
```

## 검증 결과

- G1 duty std = 6.67e-3 ≥ 0.001 PASS
- G2 tol=0 → std=0 PASS
- G3 byte-identical 2-run PASS
- G4 backend=`local_ngspice_<ver>_ne555_astable_mc16` PASS
- **4/4 PASS** (commit 2026-04-26)

## 관련 entry

- [arduino-prototype-spec](arduino-prototype-spec.md)
- [cmos_local_sim_landing](cmos_local_sim_landing.md)
- [memristor_local_sim_landing](memristor_local_sim_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
