// sleep_oscillator.ino — SWS/REM phase-continuous DDS oscillator firmware
//
// Target: Arduino Uno R3 + AD9833 DDS module on SPI bus
// Source: anima-physics/oscillator/sleep_oscillator.hexa (§188 PASS 5/5)
//
// Behavior:
//   - boot in SWS mode (δ band, f=2.0 Hz, amp logged as 1.0)
//   - timer-driven ultradian FSM: SWS 90 s → REM 20 s → SWS 90 s → ...
//   - on mode switch: ad9833_set_freq0_hz(new_f) — FREQ0 write WITHOUT RESET
//     → 28-bit phase accumulator carries over → analog sine continuous
//   - Serial @ 115200 baud: prints mode + freq + cumulative tick on each
//     transition (and once per second heartbeat)
//
// Wiring:
//   Arduino D10 → AD9833 FSYNC
//   Arduino D11 → AD9833 SDATA  (MOSI)
//   Arduino D13 → AD9833 SCLK
//   Arduino 5V  → AD9833 VCC
//   Arduino GND → AD9833 GND
//   AD9833 OUT  → oscilloscope CH1 (and optional 200 Ω → GND for proper load)
//   Arduino D9  → scope CH2 (mode pin: LOW=SWS, HIGH=REM)
//
// Mirror of hexa selftest:
//   T1 initial δ 2 Hz       → boot state
//   T2 switch to θ 6 Hz     → first FSM tick after 90 s
//   T3 switch back to δ     → second FSM tick after 90+20 s
//   T4 determinism          → identical Serial trace on reboot
//   T5 latency (500 sample) → SPI write < 100 µs (well under 500 ms spec)

#include "ad9833_driver.h"
#include <Arduino.h>

// ───── tunable constants (compile-time) ─────
#define MODE_PIN          9      // GPIO mirror of current mode (scope CH2)
#define SERIAL_BAUD       115200
#define HEARTBEAT_MS      1000   // print state once per second
#define SWS_DURATION_MS   90000UL  // 90 s SWS phase (compressible for bench)
#define REM_DURATION_MS   20000UL  // 20 s REM phase

// ───── waveform parameters (mirror of sleep_oscillator.hexa) ─────
static const float DELTA_FREQ_HZ = 2.0f;  // SWS
static const float DELTA_AMP     = 1.0f;
static const float THETA_FREQ_HZ = 6.0f;  // REM
static const float THETA_AMP     = 0.7f;

enum SleepMode { MODE_SWS = 0, MODE_REM = 1 };

// ───── module state ─────
static SleepMode g_mode = MODE_SWS;
static uint32_t  g_mode_start_ms = 0;
static uint32_t  g_last_heartbeat_ms = 0;
static uint32_t  g_switch_count = 0;

// ───── helpers ─────
static const char* mode_name(SleepMode m) {
    return (m == MODE_SWS) ? "SWS_delta" : "REM_theta";
}

static float mode_freq(SleepMode m) {
    return (m == MODE_SWS) ? DELTA_FREQ_HZ : THETA_FREQ_HZ;
}

static float mode_amp(SleepMode m) {
    // AD9833 has fixed Vp-p; amp is logged only (would drive an external
    // digital pot if precision amplitude were required — see DESIGN.md §C3.3)
    return (m == MODE_SWS) ? DELTA_AMP : THETA_AMP;
}

static uint32_t mode_duration_ms(SleepMode m) {
    return (m == MODE_SWS) ? SWS_DURATION_MS : REM_DURATION_MS;
}

static void apply_mode(SleepMode m) {
    g_mode = m;
    digitalWrite(MODE_PIN, m == MODE_REM ? HIGH : LOW);
    // PHASE-CONTINUOUS switch: write FREQ0 only, no RESET bit.
    // AD9833 keeps its 28-bit phase accumulator; analog sine carries over.
    ad9833_set_freq0_hz(mode_freq(m));
    g_switch_count++;
    g_mode_start_ms = millis();
    Serial.print(F("[mode-switch #"));
    Serial.print(g_switch_count);
    Serial.print(F("] -> "));
    Serial.print(mode_name(m));
    Serial.print(F("  f="));
    Serial.print(mode_freq(m), 4);
    Serial.print(F(" Hz  amp="));
    Serial.print(mode_amp(m), 4);
    Serial.print(F("  freq_word=0x"));
    Serial.println(ad9833_freq_word(mode_freq(m)), HEX);
}

static void heartbeat(void) {
    uint32_t now = millis();
    if (now - g_last_heartbeat_ms < HEARTBEAT_MS) return;
    g_last_heartbeat_ms = now;
    uint32_t elapsed_s = (now - g_mode_start_ms) / 1000UL;
    Serial.print(F("[hb] t="));
    Serial.print(now);
    Serial.print(F("ms  mode="));
    Serial.print(mode_name(g_mode));
    Serial.print(F("  elapsed_in_mode="));
    Serial.print(elapsed_s);
    Serial.println(F("s"));
}

// ───── Arduino entry points ─────
void setup() {
    Serial.begin(SERIAL_BAUD);
    while (!Serial && millis() < 2000) { /* wait briefly for USB */ }
    pinMode(MODE_PIN, OUTPUT);

    Serial.println();
    Serial.println(F("================================================"));
    Serial.println(F(" sleep_oscillator.ino — anima-physics HW #4"));
    Serial.println(F(" SWS(delta 2Hz) <-> REM(theta 6Hz) DDS oscillator"));
    Serial.println(F(" SW source: oscillator/sleep_oscillator.hexa"));
    Serial.println(F("================================================"));

    // T1 mirror: initialize chip, default to SWS @ 2 Hz, phase=0.
    ad9833_init();
    apply_mode(MODE_SWS);  // first apply also writes FREQ0=2Hz, sets pin
    g_mode_start_ms = millis();
}

void loop() {
    heartbeat();
    uint32_t now = millis();
    if ((now - g_mode_start_ms) >= mode_duration_ms(g_mode)) {
        // Ultradian FSM tick: SWS -> REM -> SWS -> ...
        SleepMode next = (g_mode == MODE_SWS) ? MODE_REM : MODE_SWS;
        apply_mode(next);
    }
    // Nothing more — DDS runs autonomously off MCLK (25 MHz on breakout).
    // Loop budget is dominated by heartbeat print (~few ms / sec).
}
