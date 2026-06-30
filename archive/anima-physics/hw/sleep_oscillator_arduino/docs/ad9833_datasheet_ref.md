# AD9833 datasheet quick reference

> Summary distilled from Analog Devices AD9833 datasheet Rev. F (28 pp,
> Apr 2003). Full datasheet:
> https://www.analog.com/media/en/technical-documentation/data-sheets/ad9833.pdf
>
> Companion to `src/ad9833_driver.h` + `src/ad9833_driver.cpp`.

## Part identification

| field | value |
|---|---|
| device | AD9833 |
| function | Low-power 0 - 12.5 MHz programmable waveform generator (DDS) |
| package | 10-lead MSOP |
| supply | 2.3 V to 5.5 V |
| supply current | 4.5 mA (@ 3 V) |
| MCLK max | 25 MHz |
| frequency resolution | 28 bits → ~0.1 Hz @ 25 MHz MCLK |
| phase resolution | 12 bits |
| output | sine, triangle, or square wave |

## Pinout (10-MSOP)

| pin | name | function |
|---|---|---|
| 1 | COMP | DAC bias compensation (cap to AVDD, 10 nF typ) |
| 2 | VDD  | digital supply |
| 3 | CAP/2.5V | internal 2.5 V regulator output (decoupling cap 100 nF) |
| 4 | DGND | digital ground |
| 5 | MCLK | master clock input (≤25 MHz) |
| 6 | SCLK | SPI clock (≤40 MHz) |
| 7 | SDATA | SPI MOSI (data in) |
| 8 | FSYNC | active-low frame sync / chip select |
| 9 | AGND | analog ground |
| 10 | VOUT | analog output (sine/triangle DAC or square) |

Standard breakout module wires MCLK to an on-board 25 MHz crystal.

## SPI protocol

- mode 2: CPOL = 1, CPHA = 0 (clock idles HIGH, data latched on falling edge)
- MSB-first
- 16-bit words framed by FSYNC pulled LOW
- FSYNC must return HIGH before the next 16-bit word

```
FSYNC ‾‾‾\___________________________________/‾‾‾
SCLK   ___|‾|_|‾|_|‾|_|‾|_|‾|_|‾|_ ...  |‾|___
SDATA  XXX< D15 >< D14 >< D13 > ... < D0 >XXXX
       ↑ FSYNC↓ latches word     ↑ FSYNC↑ commits
```

## 16-bit word address field (D15:D14)

| D15 D14 | register |
|---|---|
| `00` | CONTROL |
| `01` | FREQ0 (28-bit, two 14-bit halves) |
| `10` | FREQ1 (28-bit) |
| `11` | PHASE0 (D13=0) / PHASE1 (D13=1) — 12-bit |

## CONTROL register (D15:D14 = 00)

| bit | name | function |
|---|---|---|
| D13 | B28 | 1 → next two writes to FREQ form 28-bit word (LSB then MSB) |
| D12 | HLB | 0 with B28=0 → next FREQ write addresses LSB half |
| D11 | FSEL | 0 → use FREQ0, 1 → use FREQ1 |
| D10 | PSEL | 0 → use PHASE0, 1 → use PHASE1 |
| D9  | RESERVED (must be 0) |
| D8  | RESET | 1 → hold internal phase register at 0; output = midscale |
| D7  | SLEEP1 | 1 → disable MCLK (low-power) |
| D6  | SLEEP12 | 1 → power down DAC (square wave still works) |
| D5  | OPBITEN | 1 → OUT pin = MSB of DAC data (square output) |
| D4  | RESERVED (must be 0) |
| D3  | DIV2 | square wave divide-by-2 select |
| D2  | RESERVED (must be 0) |
| D1  | MODE | 0 → sine output, 1 → triangle output |
| D0  | RESERVED (must be 0) |

## FREQ0 / FREQ1 register (D15:D14 = 01 or 10)

28-bit tuning word, written as two 14-bit halves:

```
write order (B28=1):
  word1 = 0x4000 | (LSB14 & 0x3FFF)   ← FREQ0 LSB
  word2 = 0x4000 | (MSB14 & 0x3FFF)   ← FREQ0 MSB

tuning_word = round(f_out × 2^28 / f_MCLK)

at f_MCLK = 25 MHz (resolution = 25e6 / 2^28 ≈ 0.0931 Hz / LSB):
  f =  2 Hz → tw = 21       (0x0000015)
                  LSB14 = 0x0015  MSB14 = 0x0000
  f =  6 Hz → tw = 64       (0x0000040)
                  LSB14 = 0x0040  MSB14 = 0x0000

(verify: `python3 src/sleep_oscillator_local_sim.py` prints this table.)
(quantization error: 2 Hz commanded → 21 × 25e6/2^28 ≈ 1.956 Hz actual;
 below scope-FFT resolution at 10 s capture — acceptable for sleep band.)
```

## PHASE0 / PHASE1 register

12-bit phase offset (0 to 2π in 4096 steps).
Δphase = 2π × PHASE / 4096.

Used by `ad9833_init()` only — we set PHASE0 = 0 once at boot, never
modify after. SWS↔REM phase continuity relies on the **phase
accumulator** (28-bit internal register, not user-visible), NOT on
PHASE0/PHASE1.

## Phase-continuous frequency switch (KEY for sleep_oscillator)

Writing FREQ0 (or FREQ1) **without** setting the RESET bit leaves the
internal 28-bit phase accumulator untouched. Only Δφ per MCLK changes
on the next MCLK rising edge. The analog DAC output therefore
transitions smoothly through whatever phase the accumulator happened
to be at — no DC step, no restart-from-zero glitch.

This is the silicon primitive that mirrors `sleep_osc_switch()` in
`sleep_oscillator.hexa`: phase carries, freq/amp updates.

Scope verification (Phase 1b): trigger CH2 on MODE_PIN edge,
observe CH1 (VOUT). Expected: sine envelope continuous across the
mode-switch instant; only the period changes.

## Initialization sequence (used in `ad9833_init()`)

1. SPI bus setup (mode 2, 1 MHz, MSB-first)
2. `0x2100` — CONTROL: B28=1, RESET=1 (hold phase accumulator)
3. `0x4000` — FREQ0 LSB = 0
4. `0x4000` — FREQ0 MSB = 0
5. `0xC000` — PHASE0 = 0
6. `0x2000` — CONTROL: B28=1, RESET=0 (chip runs at sine, f=0)
7. then `ad9833_set_freq0_hz(2.0)` from `sleep_oscillator.ino setup()`

After this sequence: chip outputs ~0.65 Vp-p sine wave at 2 Hz on VOUT,
biased around 0.32 V (mid-rail of internal 0.65 V DAC range).

## Output specifications (sine mode)

| param | typ | unit |
|---|---|---|
| VOUT peak-to-peak | 0.65 | V |
| VOUT DC offset | 0.32 | V |
| total harmonic distortion (THD) | 0.5 | % |
| spurious-free dynamic range (SFDR) | 60 | dBc @ 100 kHz |
| output impedance | 200 | Ω (typ) |

For high-precision applications (anti-aliasing, scope-CH FFT), follow
VOUT with a 200 Ω termination and an RC LPF (e.g. R=200 Ω, C=22 nF
→ fc ≈ 36 kHz) before measurement. Not required for sleep_oscillator
band (2-6 Hz) — DC-coupled scope read directly is fine.
