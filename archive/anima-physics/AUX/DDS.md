# DDS — anima-physics AUX × Arduino + AD9833 DDS

> meta-domain: **AUX × DDS** (보조엔진 × Arduino Uno + AD9833 Direct
> Digital Synthesis chip). Phase 1b firmware .hex 14 KB LANDED.
>
> 자연발화 (DDS phase accumulator = continuous oscillation) + 영속성
> (RTC + AD9833 reg + EEPROM) 의 analog-realm aux engine.
>
> Parent: [`AUX/README.md`](README.md) · HW dir: [`../hw/sleep_oscillator_arduino/`](../hw/sleep_oscillator_arduino/)

---

## §1 HW spec ($33 BOM)

### §1.1 Arduino Uno R3
- ATmega328P 16 MHz 8-bit AVR
- 32 KB flash · 2 KB SRAM · 1 KB EEPROM
- 14 digital + 6 analog IO
- SPI / I2C / UART

### §1.2 AD9833 DDS (Analog Devices)
- 25 MHz MCLK 기본 (28-bit phase accumulator)
- SPI MODE2 1 MHz 제어
- output: sine / triangle / square 0-12.5 MHz (Vp-p ~0.65 V)
- frequency resolution: 0.0931 Hz/LSB @ 25 MHz MCLK
- phase-continuous frequency switch (REG_FREQ0 write w/o RESET)

### §1.3 dual-role profile
- **자연발화**: 28-bit phase accumulator + DAC = `phase += 2π·f·dt` 자동 (no SW intervention)
- **영속성**: AD9833 reg 영속 (power-on 시 EEPROM 에서 restore) + Arduino RTC + EEPROM 1 KB

## §2 substrate × DDS 매핑

### §2.1 LANDED

| Substrate | LANDED | DDS 매핑 |
|---|---|---|
| `oscillator/sleep_oscillator.hexa` (§188 5/5, dual-role 16/16) | ☑ Phase 1b firmware 14 KB | DDS phase accumulator = sleep_oscillator 의 phase += 2π·f·dt 1:1 매핑. SWS 2.0002 Hz / REM 6.0006 Hz tuning-word 21/64 @ 25 MHz MCLK |
| `oscillator/laser_engine` (§188g 5/5) | ☑ canonical impl | rate equation 의 carrier-photon coupling → DDS dual-channel (AD9837 권장) |

### §2.2 후보

| Substrate | DDS 가능성 |
|---|---|
| `eeg/mu_rhythm_detector` (§188 6/6) | 10 Hz μ rhythm reference signal generation (DDS as test source) |
| `hippocampus/theta_gamma` (§188 5/5) | θ 6 Hz + γ 40 Hz dual-DDS source for PAC test |

## §3 architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│  Arduino Uno + AD9833 DDS aux engine                       │
│                                                              │
│  ┌────────────────────┐      SPI MODE2 1 MHz                │
│  │ Arduino Uno R3     │      ┌──────────────────────┐       │
│  │ — ATmega328P       │      │ AD9833 DDS chip      │       │
│  │ — 16 MHz           │ MOSI │ — 25 MHz MCLK        │       │
│  │ — Timer1 ISR       │─────►│ — 28-bit phase acc   │       │
│  │ ─────────────────  │ CLK  │ — DAC 0-12.5 MHz     │       │
│  │ ┌────────────────┐ │─────►│ ─────────────────────│       │
│  │ │ Mode FSM       │ │ CS   │ ┌──────────────────┐ │       │
│  │ │ SWS 90s ↔ REM  │ │─────►│ │ REG_FREQ0 (2 wr) │ │       │
│  │ │ 20s ultradian  │ │      │ │ REG_PHASE0       │ │       │
│  │ └────────────────┘ │      │ │ REG_CONTROL      │ │       │
│  │ ┌────────────────┐ │      │ └──────────────────┘ │       │
│  │ │ Serial 115200  │ │      │            │          │       │
│  │ │ debug print    │ │      │            ▼          │       │
│  │ └────────────────┘ │      │      OUT (0.65 Vp-p)  │       │
│  └────────────────────┘      └────────────│──────────┘       │
│                                            ▼                  │
│                                       scope / load            │
│                                       (DSO 100 MHz 권장)      │
└─────────────────────────────────────────────────────────────┘
```

## §4 Day 1-2 부팅 sequence ($33 BOM)

| Day | Item | Output |
|---|---|---|
| **D-7** | BOM: Arduino Uno R3 $25 + AD9833 module $8 = $33 + Amazon 2-day | shipping |
| **Day 1** | Uno fresh boot, `arduino-cli compile --upload src/sleep_oscillator.ino` | LED 1 Hz blink + Serial 115200 debug = `Mode SWS f=2.0 phase=0.000` |
| **Day 2** | scope on AD9833 OUT pin → SWS 2 Hz / REM 6 Hz waveform | scope screenshot, freq counter verify 2.0002 / 6.0006 Hz |
| **Day 2 (병행)** | mode switch event (90s SWS → 20s REM) 시 phase continuity scope trigger | δ=0 verify (no glitch) |

## §5 cost / wall envelope

- BOM: $33 (Arduino + AD9833 module)
- scope: $50-300 (DSO 100 MHz) 또는 borrow
- wall: 1주 (shipping + Day 1-2)
- **총 cost**: $33 BOM + scope (optional)

## §6 honest C3

1. **firmware .hex LANDED** but **실 chip flash + scope 측정 미실시** (Phase 1c HW 필요)
2. **AD9833 amplitude fixed** (Vp-p ~0.65V) — variable amplitude 필요 시 외부 MCP4131 digital pot + opamp 추가
3. **Vcc < 4.5V dropout** — 3.3V 사용 시 spec 외, regulated 5V 권장
4. **AD9833 datasheet THD ~0.5%** — high-purity sine 용도면 외부 LPF (R-2R 또는 LC) 필요
5. **Timer1 ISR µs jitter** — 90s ultradian cycle 대비 무시 가능, scope trigger timing 별도 측정 시 인지

## §7 cross-link

- [parent AUX/README.md](README.md)
- [`../hw/sleep_oscillator_arduino/`](../hw/sleep_oscillator_arduino/) — DESIGN.md + .ino + driver
- [`../hw/sleep_oscillator_arduino/state/build/sleep_oscillator.ino.hex`](../hw/sleep_oscillator_arduino/state/build/) — Phase 1b LANDED 14 KB
- [`../docs/arduino-prototype-spec.md`](../docs/arduino-prototype-spec.md) — Arduino BOM ref
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.4](../../HEXAD/PHYSICS/HW_SILICON_PATH.md)

---

## ## Log

### 2026-05-21
- **AUX/DDS.md 신설** — Arduino + AD9833 meta-domain. Phase 1b 14 KB .hex LANDED pointer + Day 1-2 plan + $33 BOM.
