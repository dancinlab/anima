# esp32/src/lib.hexa

> ESP32-S3 ConsciousnessBoard hexa-native lib (2 GRU cells/board × 8 boards = 16 cell · 8 faction · GRU + Lorenz + Sandpile + Hebbian + Ratchet) · **🟡 부분** · 비용 $40 (8 × $5 ESP32-S3)

## 구현 가능성

🟡 — struct + 상수 정의 완성, 실 SPI ring 통신 + flashing 미테스트. Laws 22-85 align (Psi-constants, Lorenz chaos, SOC sandpile, frustration ratio). HEXA-FIRST: pure .hexa.

## 작동 코드 / 의존성

- 원본: `esp32/src/lib.hexa` (307 LoC)
- 외부 의존: hexa run (Mac mock) · ESP32-S3 flash (LIVE)
- 상수: CELL_DIM=64, HIDDEN_DIM=128, COMBINED_DIM=193, CELLS_PER_BOARD=2, MAX_BOARDS=8, MAX_CELLS=16, N_FACTIONS=8
- Psi: COUPLING=0.014, BALANCE=0.5, STEPS=4.33, ENTROPY=0.998

## 비용 / 리소스

- $40 BOM (8 ESP32-WROOM-32 또는 ESP32-S3-N16R8)
- $77 hardware-guide 견적 (full SPI bus + peripherals)

## 핵심 흐름 / 코드 발췌

```hexa
comptime const CELL_DIM      = 64
comptime const HIDDEN_DIM    = 128
comptime const CELLS_PER_BOARD = 2
comptime const MAX_BOARDS    = 8
comptime const MAX_CELLS     = 16
comptime const N_FACTIONS    = 8

// Lorenz chaos
comptime const LORENZ_SIGMA  = 10.0
comptime const LORENZ_RHO    = 28.0
comptime const LORENZ_BETA   = 2.667

// SOC sandpile
comptime const SANDPILE_THRESHOLD = 4.0
comptime const SANDPILE_TRANSFER  = 1.0
comptime const FRUSTRATION_RATIO  = 3

// Hebbian LTP/LTD
comptime const HEBBIAN_LTP_THRESH = 0.8
comptime const HEBBIAN_LTD_THRESH = 0.2
comptime const HEBBIAN_RATE       = 0.01
comptime const RATCHET_DECAY_THRESH = 0.8
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/esp32/src/lib.hexa
# (실 flash: ESP-IDF / Arduino IDE — docs/esp32-hardware-guide.md)
```

## 검증 결과

- struct + step() trivial 검증 (Mac mock)
- 실 SPI ring 통신: docs/esp32-hardware-guide.md 절차 완성 미테스트

## 관련 entry

- [esp32/qrng_bridge.md](../qrng_bridge.md)
- [esp32/QRNG_SPEC.md](../QRNG_SPEC.md)
- [src/esp32_network.md](../../src/esp32_network.md) — orchestrator stub

## 출처

- README § 3 esp32/src/lib.hexa
- docs/esp32-hardware-guide.md
