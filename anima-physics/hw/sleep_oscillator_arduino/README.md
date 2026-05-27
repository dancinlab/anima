# sleep_oscillator_arduino

> anima-physics HW target #4 — SWS(δ 2Hz) ↔ REM(θ 6Hz) phase-continuous
> oscillator on Arduino Uno + AD9833 DDS chip.
> SW source `oscillator/sleep_oscillator.hexa` (T1-T5 PASS, §188 5/5).

## Status (2026-05-21 Mac local Phase 1a)

- ✅ **Python local sim PASS** — F-HW-SO-1..5 5/5
  (init phase = 0, SWS = 2.0 Hz, REM = 6.0 Hz, switch phase-continuous,
  10 s SWS produces ≥20 phase wraps).
- ✅ **Firmware sketch + AD9833 driver written** (lint-only;
  `arduino-cli` 별도 설치 시 `./build.sh compile` 진입 가능).
- ⏳ Phase 1b — `brew install arduino-cli` + Uno + AD9833 breakout
  ($29-389 BOM, scope 포함 여부 따라) → 실 board + scope 측정.

## Quick start

```bash
./build.sh sim     # Python phase-accumulator sim → state/sim.log
./build.sh lint    # cat .ino + .h + .cpp (arduino-cli 없이 eyeball)
./build.sh all     # sim + lint (Phase 1a)
```

Phase 1b (별도 setup):
```bash
brew install arduino-cli
arduino-cli core install arduino:avr
arduino-cli compile --fqbn arduino:avr:uno src/sleep_oscillator.ino
arduino-cli upload  --fqbn arduino:avr:uno -p /dev/cu.usbmodem* src/sleep_oscillator.ino
```

## Wiring (Arduino Uno → AD9833 module)

| Arduino pin | AD9833 pin | signal |
|---|---|---|
| D11 (MOSI) | DAT/SDATA | SPI data out |
| D13 (SCK)  | CLK/SCLK  | SPI clock |
| D10        | FSYNC/CS  | active-low chip select |
| 5V         | VCC       | 2.3-5.5 V supply |
| GND        | GND       | |
| (analog)   | OUT       | → oscilloscope CH1 |

## Files

- [DESIGN.md](DESIGN.md) — full ASCII architecture + BOM + falsifier
- [docs/ad9833_datasheet_ref.md](docs/ad9833_datasheet_ref.md) — register map summary
- `src/sleep_oscillator.ino` — Arduino sketch (mode FSM + Serial debug)
- `src/ad9833_driver.{h,cpp}` — SPI driver + control word + freq word calc
- `src/sleep_oscillator_local_sim.py` — numpy phase accumulator + F-HW-SO-1..5
- `state/sim.log` — Python sim output

## Cross-link

- [HW silicon path §2.4](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) (this target)
- [hexa source](../../oscillator/sleep_oscillator.hexa) — SW substrate (T1-T5 PASS)
- [anima-physics PLAN G6](../../PLAN.md) — HW Phase 1 ☑ (target #4)
