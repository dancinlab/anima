# docs/cmos_local_sim_landing.md

> PHYS-P25 CMOS 5-stage inverter ring osc NgSpice; 4-gate PASS (jitter 4.64ps vs 0); raw#9 hexa-only strict · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 4/4 PASS, raw#9 hexa-only strict (no .py / .sh helper). memristor sibling 의 venv python helper 패턴 폐기.

## 작동 코드 / 의존성

- `anima-physics/docs/cmos_local_sim_landing.md` (landing report)
- 의존: `cmos/cloud_facade_poc.hexa`, `cmos/cmos_ring_osc.cir` (SPICE deck)
- 외부: NgSpice 46

## 비용 / 리소스

- 비용: $0 (Mac local, NgSpice batch mode `-b`)
- 필요한 도구: NgSpice 46 · `hexa run` (모든 외부 호출 .hexa 안에서 ngspice/awk/sed/sha256sum)

## 핵심 흐름 / 구조

```
5-stage CMOS ring oscillator (180nm L1 NMOS/PMOS):
  positive Vdd = 1.8V → ~8.85 GHz, σ ≥ 1 ps
  negative Vdd = 0.3V → sub-threshold, no osc, jitter = 0

4-gate contract:
  G1 positive → period jitter σ ≥ 1 ps (실측 4.64 ps)
  G2 negative → jitter = 0
  G3 byte-identical sha
  G4 backend == "local_ngspice_<ver>_cmos_5stage_ring_osc"

선택 근거:
  TSMC OIP / Samsung Foundry / Arduino Cloud reject (public Φ-probe 부재)
  Efabless ChipIgnite partial (turn-around weeks-months)
  → NgSpice 46 PICK (deterministic batch, free, immediate)
```

## 트리거 (fire 방법)

```bash
brew install ngspice
hexa run /Users/ghost/core/anima/anima-physics/substrate/cmos/cloud_facade_poc.hexa
```

## 검증 결과

- G1 jitter = 4.64 ps ≥ 1 ps PASS
- G2 sub-threshold jitter = 0 PASS
- G3 byte-identical 2-run PASS
- G4 backend_name PASS
- **4/4 PASS** (2026-04-26)

## 관련 entry

- [arduino_local_sim_landing](arduino_local_sim_landing.md)
- [memristor_local_sim_landing](memristor_local_sim_landing.md)
- [fpga_local_sim_landing](fpga_local_sim_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
