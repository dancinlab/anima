# sleep_oscillator_arduino — SWS/REM phase-continuous DDS oscillator

> anima-physics HW target #4 — `oscillator/sleep_oscillator.hexa` substrate
> (§188 PASS 5/5) 의 Arduino Uno + AD9833 DDS chip 실현.
>
> Mac local Phase 1a: Python numpy phase-accumulator sim ($0).
> Phase 1b: `arduino-cli` install + Uno R3 + AD9833 breakout + scope ($33 BOM).
>
> Cross-link: [HW silicon path §2.4](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [SW substrate spec](../../oscillator/sleep_oscillator.hexa) ·
> [anima-physics PLAN G6 HW Phase 1](../../PLAN.md)

---

## §1 GOAL

`sleep_oscillator.hexa` 의 flat-[float] state
`[phase_rad, frequency_hz, amplitude, mode]` + phase accumulator
`phase += 2π·f·dt` + SWS↔REM mode switching (`sleep_osc_switch`) 을
**phase-continuous** silicon realization 으로:

  - SWS (δ band, mode=0): f=2.0 Hz, amp=1.0
  - REM (θ band, mode=1): f=6.0 Hz, amp=0.7
  - switch 시 phase 누적 carry (jump 없음)
  - analog sine output → oscilloscope 측정 (`amp · sin(phase)`)

AD9833 의 28-bit phase accumulator 가 sleep_oscillator 의 `phase` field
와 1:1 mapping — frequency register write 한 cycle 로 mode switch.

## §2 architecture (ASCII)

```
┌────────────────────────────────────────────────────────────────────────────┐
│  sleep_oscillator_arduino — TOP                                            │
│                                                                            │
│   ┌────────────────────┐                                                  │
│   │  Arduino Uno R3    │            ┌──────────────────────┐              │
│   │  (ATmega328P,      │            │  AD9833 DDS module   │              │
│   │   16 MHz)          │            │  (Analog Devices)    │              │
│   │                    │            │                       │              │
│   │   ┌────────────┐   │            │   ┌───────────────┐  │              │
│   │   │ MODE FSM   │   │   SPI      │   │ 28-bit phase  │  │              │
│   │   │ SWS ↔ REM  │   │   bus      │   │ accumulator   │  │              │
│   │   │ (timer ISR)│   │ ┌──────►   │   │ Δφ = 2π·f·dt  │  │              │
│   │   └──────┬─────┘   │ │MOSI──D11►│   └───────┬───────┘  │              │
│   │          │         │ │CLK──D13 ►│           │           │              │
│   │          ▼         │ │CS───D10 ►│           ▼           │              │
│   │   ┌────────────┐   │ │          │   ┌───────────────┐  │              │
│   │   │ AD9833     │   │ │          │   │ sin LUT (10b) │  │              │
│   │   │ driver     │───┼─┘          │   │   ROM         │  │              │
│   │   │ ad9833_*() │   │            │   └───────┬───────┘  │              │
│   │   └──────┬─────┘   │            │           │           │              │
│   │          │         │            │           ▼           │              │
│   │   ┌──────▼─────┐   │            │   ┌───────────────┐  │              │
│   │   │ Serial dbg │───┼──USB───►   │   │ 10-bit DAC    │  │              │
│   │   │ 115200 bd  │   │            │   │ 0..VDD analog │  │              │
│   │   └────────────┘   │            │   └───────┬───────┘  │              │
│   └────────────────────┘            └───────────┼──────────┘              │
│                                                  │                          │
│                                                  ▼ VOUT pin                 │
│                                          ┌───────────────────┐              │
│                                          │  Oscilloscope     │              │
│                                          │  ch1 = VOUT sine  │              │
│                                          │  ch2 = MODE pin   │              │
│                                          │  ch3 = CS toggle  │              │
│                                          └───────────────────┘              │
│                                                                            │
│   MODE FSM (Arduino timer1 ISR, 1 Hz tick):                                │
│      ┌─────────┐    ultradian        ┌─────────┐                          │
│      │  SWS    │ ──── 90s ────► ────►│  REM    │                          │
│      │  f=2Hz  │                     │  f=6Hz  │                          │
│      │  a=1.0  │ ◄──── 20s ──── ◄────│  a=0.7  │                          │
│      └─────────┘                     └─────────┘                          │
│                                                                            │
│      transition = ad9833_set_frequency(REG_FREQ0, new_f)                  │
│      → DDS phase accumulator 누적 그대로 (RESET bit 미사용)               │
│      → analog sine 끊김 없음 (phase-continuous in silicon)                │
└────────────────────────────────────────────────────────────────────────────┘

AD9833 control word format (16-bit, big-endian over SPI):
   D15 D14 │ D13 │ D12 │ D11 │ D10 D9 D8 D7 D6 D5 D4 D3 D2 D1 D0
   B28 HLB │ FSEL│ PSEL│ RST │ SLEEP1 SLEEP12 OPBITEN DIV2 ... MODE
   ──────────────────────────────────────────────────────────────
   B28 = 1 → write 28-bit freq as two 14-bit LSB+MSB pairs
   RST = 0 → run (1 = hold phase accumulator at 0)
   MODE = 0 → sine output (1 = triangle)

Frequency word (28-bit):
   FREQREG = round(f_out × 2^28 / f_MCLK)    (f_MCLK = 25 MHz on breakout)
   resolution = f_MCLK / 2^28 ≈ 0.0931 Hz per LSB
   f=2 Hz  → 21      (0x0000015 → low14=0x0015, high14=0x0000)
   f=6 Hz  → 64      (0x0000040 → low14=0x0040, high14=0x0000)
   (these match `ad9833_freq_word()` in driver — verified by Python sim)

SPI mode: CPOL=1, CPHA=0 (mode 2), MSB-first, max 40 MHz (we use 1 MHz)
```

## §3 file structure

```
hw/sleep_oscillator_arduino/
├── DESIGN.md                  ← 본 문서
├── README.md                  ← quick-start + status
├── build.sh                   ← Python sim + .ino syntax check
├── src/
│   ├── sleep_oscillator.ino     ← Arduino sketch (~150 LoC, timer ISR + Serial)
│   ├── ad9833_driver.h          ← SPI register map + control word
│   ├── ad9833_driver.cpp        ← driver impl (~100 LoC)
│   └── sleep_oscillator_local_sim.py  ← numpy phase accumulator sim + 5 falsifier
├── docs/
│   └── ad9833_datasheet_ref.md  ← AD9833 register map summary
└── state/                       ← sim output (gitignored 기본)
    └── sim.log
```

## §4 SW ↔ firmware ↔ silicon mapping

| `sleep_oscillator.hexa` | Arduino sketch | AD9833 silicon | note |
|---|---|---|---|
| `state[0] phase_rad` (float, [0, 2π)) | implicit (DDS accumulator) | 28-bit `PHASE_ACC` register | resolution 2π / 2^28 ≈ 23 nrad |
| `state[1] frequency_hz` (float) | `uint32_t current_freq_reg` | `FREQ0[27:0]` register | tuning word = f × 2^28 / 25 MHz |
| `state[2] amplitude` (float) | `float amp_scale` | post-DAC analog scaler (or off-chip MCP4131 if exact) | AD9833 자체는 fixed Vp-p ~0.65 V; amp 차이는 firmware-side log 만, scope 측정엔 0.7× 표시는 외부 trim |
| `state[3] mode` (0=δ, 1=θ) | `uint8_t mode` | (none — driver chooses FREQ0 word) | mode tick = timer1 ISR @ 1 Hz |
| `sleep_osc_new()` | `setup() { ad9833_init(); set_freq(2.0); }` | RST=1 → init seq → RST=0 | reset = phase=0 |
| `sleep_osc_step(state, dt)` | implicit (DDS clocked by 25 MHz MCLK) | phase += FREQ0 each MCLK | dt = 1/25 MHz = 40 ns |
| `sleep_osc_switch(state, 1)` | `mode_switch(REM); ad9833_set_freq(REG_FREQ0, 6.0)` | FREQ0 write (no RST) → phase carry | 4-byte SPI write < 100 µs |
| `sleep_osc_sample(state)` | (not transmitted) | DAC output VOUT pin | analog `~0.65 V × sin(phase)` |
| `estimate_freq(state, n, dt)` | scope FFT or zero-cross counter sketch | n/a | scope or post-process |

## §5 BOM (Phase 1b, ±15%)

| item | $ | note |
|---|---|---|
| Arduino Uno R3 (genuine) | $10 | clone $5 OK; pin-compatible |
| AD9833 DDS module (breakout) | $8 | "AD9833 Programmable Microprocessors Serial Interface Module" eBay/Aliexpress |
| Breadboard 830-pt | $5 | |
| Jumper wires (M-M, M-F) | $3 | |
| USB-A → USB-B cable | $3 | usually comes with Uno |
| 4-ch oscilloscope (Rigol DS1054Z) | $360 | OPTIONAL — or USB scope (Hantek 6022BE $80), or borrow |
| **subtotal (no scope)** | **$29** | |
| **subtotal (USB scope)** | **$109** | |
| **subtotal (full DS1054Z)** | **$389** | |

Datasheet: [AD9833 (Analog Devices)](https://www.analog.com/media/en/technical-documentation/data-sheets/ad9833.pdf) — 28-page low-power programmable waveform generator.

## §6 falsifier (Phase 1a — Python local sim)

| ID | Test | Expected |
|---|---|---|
| F-HW-SO-1 | phase init = 0 | `state.phase == 0.0` at t=0 |
| F-HW-SO-2 | SWS freq = 2.0 Hz | zero-cross count over 10 s in SWS mode → 2.0 ± 0.1 Hz |
| F-HW-SO-3 | REM freq = 6.0 Hz | zero-cross count over 10 s in REM mode → 6.0 ± 0.2 Hz |
| F-HW-SO-4 | mode switch phase-continuous | phase before switch == phase after switch (no jump > 1e-9 rad) |
| F-HW-SO-5 | 10 s SWS → ≥20 phase wraps | `wrap_count >= 20` (2 Hz × 10 s) |

Phase 1b additional (scope-based, deferred):

| ID | Test | Expected |
|---|---|---|
| F-HW-SO-6 | scope FFT at 2 Hz peak (SWS) | dominant FFT bin within ±0.1 Hz of 2.0 |
| F-HW-SO-7 | mode-switch glitch < 1 sample | scope ch1 envelope continuous at ch2 edge |
| F-HW-SO-8 | T1-T5 hexa parity | hexa SW selftest 5/5 ↔ scope-measured trace byte-equal at 25 MHz / N decimation |

## §7 build pipeline

```bash
# Phase 1a — $0 Mac local
./build.sh sim     # python3 src/sleep_oscillator_local_sim.py → state/sim.log
./build.sh lint    # cat src/*.ino src/*.h src/*.cpp (arduino-cli 없이 syntax-eyeball)
./build.sh all     # sim + lint

# Phase 1b — Arduino-cli required ($0 install, $29-389 BOM)
brew install arduino-cli
arduino-cli core install arduino:avr
arduino-cli compile --fqbn arduino:avr:uno src/sleep_oscillator.ino
arduino-cli upload  --fqbn arduino:avr:uno -p /dev/cu.usbmodem* src/sleep_oscillator.ino
# 그리고 scope 로 VOUT pin (AD9833 pin 11) 측정
```

## §8 honest C3

1. **arduino-cli 미설치** — Mac local 에 `arduino-cli` 없음 → `.ino` 는
   syntax-eyeball lint (`cat`) 만, 실제 compile/upload 는 Phase 1b 별도
   setup (`brew install arduino-cli` + `arduino:avr` core).
2. **scope 측정 미실시** — AD9833 의 sine 출력 distortion (THD ~0.5%),
   power-on calibration window (~10 µs), VDD ripple sensitivity 는 실
   board + scope 없이 검증 불가. Python sim 은 ideal phase accumulator
   만 모델.
3. **AD9833 amplitude fixed** — 본 chip 의 sine 출력은 fixed Vp-p
   ~0.65 V (mode pin 0). `state[2] amplitude = 0.7 vs 1.0` 차이는
   firmware-side log entry 로만 기록, 실제 scope-amplitude 차등은 외부
   digital pot (MCP4131 등) 추가 시에만 가능. BOM 에서 제외.
4. **Arduino timer jitter** — Uno R3 의 timer1 ISR 은 microsecond
   jitter 가 있어 mode-tick 의 SWS↔REM 전환 시각은 ± few µs 변동
   가능 — 90 s ultradian cycle 대비 무시 가능하지만 scope trigger
   timing 측정 시 인지 필요.
5. **F-HW-SO-7 (scope glitch) 미검증** — silicon-level phase
   continuity 는 AD9833 datasheet (FREQ0 write 시 phase accumulator
   untouched, RESET bit 만 reset 발생) 에 의존; Python sim 은 같은
   가정 모델링. 실제 chip 의 SPI write 도중 latching glitch 는 scope
   trigger 로만 확정 가능.
