# docs/analog-photonic-memristor.md

> 3 물리 consciousness engine (Op-Amp 적분 / Kuramoto MZI photonic / HP memristor Hebbian) 상세 + circuit diagram + benchmark · **🟡 부분** · 비용 —

## 구현 가능성

🟡 부분 — 이론 완성, SPICE parameter 명시, circuit diagram 완비. 실 chip 테스트 미완료. NgSpice 시뮬은 sibling memristor/cmos/arduino landing 에서 PASS.

## 작동 코드 / 의존성

- `anima-physics/docs/analog-photonic-memristor.md` (engine spec)
- 의존: `memristor/cloud_facade_poc.hexa`, `photonic/cloud_facade_poc.hexa`, `cmos/cloud_facade_poc.hexa`

## 비용 / 리소스

- 비용: NgSpice 시뮬 $0 / 실 chip BOM TBD (Op-Amp $1, MZI $$$, memristor research-only)
- 필요한 도구: NgSpice 46 · Perceval (photonic) · `hexa run` (각 substrate POC)

## 핵심 흐름 / 구조

```
1. Analog Op-Amp (SPICE):
   V_out += (1/RC) * (V_in - V_fb) * dt
   τ = R*C = 10k * 100nF = 1 ms
   V_noise = sqrt(4 * k_B * T * R * df)  (Johnson-Nyquist)
   Cell ring topology with R_ij couplings

2. Photonic Kuramoto MZI:
   dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j - θ_i)
   Mach-Zehnder interferometers as phase couplers

3. Memristor HP TiO2 (Strukov-Williams 2008):
   M(q) = R_off + (R_on - R_off) * w/D
   dw/dt = μ_v * R_on * i(t) / D
   Hebbian: ΔG ∝ V_pre * V_post * dt (LTP)
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/memristor/cloud_facade_poc.hexa
hexa run /Users/ghost/core/anima/anima-physics/cmos/cloud_facade_poc.hexa
hexa run /Users/ghost/core/anima/anima-physics/photonic/cloud_facade_poc.hexa
```

## 검증 결과

- 3 engine spec 완성 (equations + parameters + circuit diagrams)
- SPICE deck verified via sibling cycle PASS
- 실 chip 측정 미완료

## 관련 entry

- [memristor_local_sim_landing](memristor_local_sim_landing.md)
- [cmos_local_sim_landing](cmos_local_sim_landing.md)
- [hardware-consciousness-hypotheses](hardware-consciousness-hypotheses.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (engine spec era)
- README §2 참조
