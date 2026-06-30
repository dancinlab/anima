// ad9833_driver.cpp — Analog Devices AD9833 DDS chip SPI driver impl
//
// See ad9833_driver.h for register map summary and API contract.
//
// SPI configuration:
//   - hardware SPI (Arduino Uno: D11=MOSI, D13=SCK, D10=user-driven FSYNC)
//   - mode 2 (CPOL=1, CPHA=0) — AD9833 latches MOSI on falling SCK edge
//   - 1 MHz bus (well under AD9833's 40 MHz max; conservative for breadboard)
//   - MSB-first
//
// Frequency word: tuning_word = round(f_out × 2^28 / f_MCLK)
//   2 Hz @ 25 MHz MCLK → 21474836 (0x0147AE14)
//   6 Hz @ 25 MHz MCLK → 64424509 (0x03D70A3D)
//
// Phase-continuous switching:
//   Writing FREQ0 register WITHOUT toggling RESET bit leaves the 28-bit
//   phase accumulator untouched. Only Δφ per MCLK changes on next clock
//   edge → analog sine output transitions smoothly (no DC jump, no
//   restart-from-zero glitch).

#include "ad9833_driver.h"

#ifdef ARDUINO
  #include <Arduino.h>
  #include <SPI.h>
#endif

// ───── low-level SPI primitive ─────
void ad9833_send16(uint16_t word) {
#ifdef ARDUINO
    SPI.beginTransaction(SPISettings(1000000UL, MSBFIRST, SPI_MODE2));
    digitalWrite(AD9833_FSYNC_PIN, LOW);     // frame start
    SPI.transfer((uint8_t)((word >> 8) & 0xFF));  // MSB
    SPI.transfer((uint8_t)(word & 0xFF));         // LSB
    digitalWrite(AD9833_FSYNC_PIN, HIGH);    // frame end → AD9833 latches
    SPI.endTransaction();
#else
    // host-side stub for unit testing — no-op
    (void)word;
#endif
}

// ───── lifecycle ─────
void ad9833_init(void) {
#ifdef ARDUINO
    pinMode(AD9833_FSYNC_PIN, OUTPUT);
    digitalWrite(AD9833_FSYNC_PIN, HIGH);
    SPI.begin();
#endif
    // 1) Send RESET=1 control word to hold phase accumulator at 0.
    //    Also set B28=1 so subsequent freq writes are accepted as
    //    two 14-bit halves.
    ad9833_send16(AD9833_REG_CONTROL | AD9833_CTRL_B28 | AD9833_CTRL_RESET);
    // 2) Write FREQ0 = 0 (LSB then MSB). Both halves use REG_FREQ0_LSB
    //    prefix (0x4000) because B28=1 already established LSB→MSB order.
    ad9833_send16(AD9833_REG_FREQ0_LSB | 0x0000);  // LSB 14 bits
    ad9833_send16(AD9833_REG_FREQ0_MSB | 0x0000);  // MSB 14 bits
    // 3) Write PHASE0 = 0
    ad9833_send16(AD9833_REG_PHASE0 | 0x0000);
    // 4) Clear RESET → chip starts running (sine output, FREQ0/PHASE0).
    ad9833_send16(AD9833_REG_CONTROL | AD9833_CTRL_B28);
}

// ───── frequency word calculation ─────
uint32_t ad9833_freq_word(float f_out_hz) {
    if (f_out_hz <= 0.0f) return 0;
    // tuning_word = f_out × 2^28 / f_MCLK
    // 2^28 / 25e6 ≈ 10.7374182  (constant; precompute as double)
    const double scale = (double)(1UL << 28) / (double)AD9833_MCLK_HZ;
    double tw_d = (double)f_out_hz * scale + 0.5;  // round-to-nearest
    if (tw_d >= (double)((1UL << 28) - 1UL)) return (1UL << 28) - 1UL;
    return (uint32_t)tw_d;
}

// ───── phase-continuous frequency set (FREQ0 only, no RESET) ─────
void ad9833_set_freq0(uint32_t freq_word) {
    // mask to 28 bits, split into two 14-bit halves
    freq_word &= 0x0FFFFFFFUL;
    uint16_t lsb14 = (uint16_t)(freq_word & 0x3FFF);
    uint16_t msb14 = (uint16_t)((freq_word >> 14) & 0x3FFF);
    // B28=1 control word already issued at init; we can now send the
    // two halves directly. AD9833 expects LSB first (HLB=0).
    //
    // NOTE: no RESET bit set anywhere — phase accumulator persists.
    ad9833_send16(AD9833_REG_FREQ0_LSB | lsb14);
    ad9833_send16(AD9833_REG_FREQ0_MSB | msb14);
}

void ad9833_set_freq0_hz(float f_out_hz) {
    ad9833_set_freq0(ad9833_freq_word(f_out_hz));
}

// ───── debug helper (pure function — host-testable) ─────
uint16_t ad9833_pack_control(bool b28, bool reset, bool sleep1, bool sleep12,
                              bool opbiten, bool mode_triangle, bool fsel,
                              bool psel) {
    uint16_t w = AD9833_REG_CONTROL;
    if (b28)            w |= AD9833_CTRL_B28;
    if (reset)          w |= AD9833_CTRL_RESET;
    if (sleep1)         w |= AD9833_CTRL_SLEEP1;
    if (sleep12)        w |= AD9833_CTRL_SLEEP12;
    if (opbiten)        w |= AD9833_CTRL_OPBITEN;
    if (mode_triangle)  w |= AD9833_CTRL_MODE;
    if (fsel)           w |= AD9833_CTRL_FSEL;
    if (psel)           w |= AD9833_CTRL_PSEL;
    return w;
}
