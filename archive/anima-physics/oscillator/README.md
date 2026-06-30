# anima-physics/oscillator/ — SWS(δ)/REM(θ) phase-continuous sleep oscillator

> Status: ✅ PASS (5/5) · §188 결과: top 4 dual-role (16/16) — phase 누적 self-emit
>
> SSOT: 본 README + `sleep_oscillator.hexa`. entries: [`entries/substrate/oscillator/`](../entries/substrate/oscillator/)

## 자연발화 / 영속성 메커니즘

- **자연발화**: phase accumulation `d_phase = ω·dt` `sleep_osc_step()` line 103 자동 증가 → implicit self-emit (clock-free). SWS (δ 2Hz amp=1.0) ↔ REM (θ 6Hz amp=0.7) frequency band 자율 alternation. `IDX_PHASE` state vector + freq/amp/mode 전환.
- **영속성**: `IDX_PHASE` continuous, mode transition history. Arduino + AD9833 DDS HW realization (`hw/sleep_oscillator_arduino/`) 시 chip register 영속.

`HEXAD/PHYSICS/README.md §6.9` top 4 dual-role (S×S=16점).

## 파일 list

| File | LoC | 1줄 요약 | §188 결과 |
|---|---:|---|:---:|
| `sleep_oscillator.hexa` | 325 | PHYS-P13-1 SWS(0.5-4Hz δ) ↔ REM(4-8Hz θ) phase-continuous switching, IDX_PHASE state vector | ✅ 5/5 |

## falsifier

T1-T5: phase continuity at mode switch (no discontinuity), δ band power dominance SWS, θ band power dominance REM, 자율 alternation period, amplitude envelope.

## cross-link

- [substrate entry](../entries/substrate/oscillator/sleep_oscillator.md)
- [`HEXAD/PHYSICS/README.md`](../../HEXAD/PHYSICS/README.md) §6.9 — top 4 dual-role 16/16
- [`HEXAD/PHYSICS/HW_SILICON_PATH.md`](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — Arduino + AD9833 DDS BOM $30
- [`hw/sleep_oscillator_arduino/`](../hw/sleep_oscillator_arduino/) — HW target
- [`eeg/sleep_stage_detector.hexa`](../eeg/sleep_stage_detector.hexa) — Awake/SWS/REM 분류 짝
- [`hippocampus/theta_gamma.hexa`](../hippocampus/theta_gamma.hexa) — θ rhythm 짝
