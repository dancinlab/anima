// ad9833_driver.h — Analog Devices AD9833 DDS chip SPI driver
//
// Target: Arduino Uno R3 (ATmega328P, 16 MHz, hardware SPI on D11/D12/D13)
// Companion: ad9833_driver.cpp · sleep_oscillator.ino
//
// AD9833 reference: Analog Devices datasheet (Rev. F, 28 pages)
//   https://www.analog.com/media/en/technical-documentation/data-sheets/ad9833.pdf
//
// Register map (16-bit SPI words, MSB-first, mode 2 = CPOL=1 CPHA=0):
//   D15 D14 = address bits
//     00  → CONTROL register
//     01  → FREQ0 register (28-bit, written as two 14-bit halves)
//     10  → FREQ1 register
//     11  → PHASE0/PHASE1 (D13 selects)
//   Frequency tuning word:
//     FREQREG = round(f_out × 2^28 / f_MCLK)
//     f_MCLK = 25 MHz on standard breakout module
//   Sine output: VOUT = 0.32 + 0.32·sin(2π·FREQREG·n / 2^28)  [V, into 200Ω]

#ifndef AD9833_DRIVER_H
#define AD9833_DRIVER_H

#include <stdint.h>

// ───── pin assignments (Arduino Uno → AD9833 module) ─────
#ifndef AD9833_FSYNC_PIN
#define AD9833_FSYNC_PIN 10   // active-low chip select (D10)
#endif
// MOSI = D11, SCK = D13 — fixed by SPI hardware
// MISO (D12) unused — AD9833 has no readback

// ───── control register bit fields (16-bit, address D15:D14 = 00) ─────
#define AD9833_CTRL_B28      (1u << 13)  // write 28-bit freq as two 14-bit halves
#define AD9833_CTRL_HLB      (1u << 12)  // 0 = write LSB then MSB (with B28)
#define AD9833_CTRL_FSEL     (1u << 11)  // 0 = use FREQ0, 1 = FREQ1
#define AD9833_CTRL_PSEL     (1u << 10)  // 0 = PHASE0, 1 = PHASE1
#define AD9833_CTRL_RESET    (1u <<  8)  // 1 = hold phase accumulator at 0
#define AD9833_CTRL_SLEEP1   (1u <<  7)  // 1 = disable MCLK
#define AD9833_CTRL_SLEEP12  (1u <<  6)  // 1 = power down DAC
#define AD9833_CTRL_OPBITEN  (1u <<  5)  // 1 = OUT pin = MSB of DAC data (square)
#define AD9833_CTRL_DIV2     (1u <<  3)  // square wave divide-by-2 select
#define AD9833_CTRL_MODE     (1u <<  1)  // 0 = sine, 1 = triangle

// ───── register address prefixes (top 2 bits of 16-bit word) ─────
#define AD9833_REG_CONTROL   (0x0000)
#define AD9833_REG_FREQ0_LSB (0x4000)
#define AD9833_REG_FREQ0_MSB (0x4000)  // same prefix; LSB then MSB ordering
#define AD9833_REG_FREQ1_LSB (0x8000)
#define AD9833_REG_FREQ1_MSB (0x8000)
#define AD9833_REG_PHASE0    (0xC000)
#define AD9833_REG_PHASE1    (0xE000)

// ───── master clock (Hz) — standard AD9833 breakout uses 25 MHz crystal ─────
#ifndef AD9833_MCLK_HZ
#define AD9833_MCLK_HZ 25000000UL
#endif

// ───── lifecycle ─────
// Initialize SPI bus, FSYNC pin, and send reset sequence + sine-mode control
// word with FREQ0 selected. Leaves phase accumulator at 0 and chip running.
void ad9833_init(void);

// ───── frequency control (sine mode, FREQ0) ─────
// Compute the 28-bit tuning word for `f_out_hz` at `AD9833_MCLK_HZ` MCLK.
//   freq_word = round(f_out_hz × 2^28 / MCLK)
// Returns 0 for f_out_hz <= 0; clamps to (2^28 - 1) for >= MCLK/2.
uint32_t ad9833_freq_word(float f_out_hz);

// Write a new tuning word to FREQ0 without resetting the phase accumulator.
// This is the **phase-continuous** mode-switch primitive — the DDS phase
// register keeps its current value across the SPI transaction; only Δφ per
// MCLK changes. Used by sleep_oscillator.ino on SWS↔REM switch.
void ad9833_set_freq0(uint32_t freq_word);

// Convenience: ad9833_set_freq0(ad9833_freq_word(hz))
void ad9833_set_freq0_hz(float f_out_hz);

// ───── low-level SPI primitive ─────
// Send one 16-bit word over hardware SPI to AD9833 (FSYNC framing, MSB-first).
void ad9833_send16(uint16_t word);

// ───── debug helper (no Serial dependency) ─────
// Pack control register from individual fields (testable on host).
uint16_t ad9833_pack_control(bool b28, bool reset, bool sleep1, bool sleep12,
                              bool opbiten, bool mode_triangle, bool fsel,
                              bool psel);

#endif // AD9833_DRIVER_H
