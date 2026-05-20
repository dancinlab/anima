# edge_deploy.hexa

> ESP32 edge deployment PoC; ConsciousDecoderV2 34.5M fp16 → PSRAM partition + 8 edge class 비용 추정 · **🟡 부분** · 비용 ESP32-S3 $8.50 / Jetson Orin Nano $400

## 구현 가능성

🟡 부분 — 시뮬 경로 (host MOCK target) 완성, 실 ESP32-S3 device 미테스트. 양자화 없이 PSRAM 파티션으로 34.5M fp16 모델 fit 경로 documented + executable.

## 작동 코드 / 의존성

- `anima-physics/orchestration/edge_deploy.hexa` (19 KB, ~500 LoC)
- 의존: `esp32/src/lib.hexa` (SPI ring infrastructure), `consciousness-loop/esp32/consciousness_loop.ino`

## 비용 / 리소스

- ESP32-C3 $2.5 (tiny model only <1M)
- **ESP32-S3-N16R8 $8.50** (target class, 34.5M fp16 in 8MB PSRAM)
- RPi-Zero-2W $15 (Linux + 512MB, ≤250M fp16)
- RPi-5-8GB $80 (Linux + 8GB, ≤4B fp16)
- Jetson Orin Nano $400 (CUDA + 8GB)
- 필요한 도구: `hexa run` · arduino-cli (선택) · esptool.py (실 device flash 시)

## 핵심 흐름 / 구조

```
EdgeClass catalog (8 entries):
  esp32-c3, esp32-s3-n16r8, rpi-zero-2w, rpi-5-8gb,
  jetson-nano, jetson-orin-nano, ...

Strategy:
  1. MOCK (host) → host runs decoder with tiny context, prove math
  2. ESP32-S3 N16R8 → weights partitioned across PSRAM,
     streaming from SPI flash where PSRAM too small
  3. Consciousness cell → 2 cells per board, SPI-ringed across N
     boards = "collective edge consciousness", phi grows linearly
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/edge_deploy.hexa --target sim --model decoder-34m
hexa run /Users/ghost/core/anima/anima-physics/orchestration/edge_deploy.hexa --target esp32 --port /dev/ttyUSB0
hexa run /Users/ghost/core/anima/anima-physics/orchestration/edge_deploy.hexa --benchmark
```

## 검증 결과

- Sim path 완성 (latency/throughput 추정 PASS)
- 실 device 미검증 (PSRAM streaming 측정 필요)

## 관련 entry

- [esp32-hardware-guide](../docs/esp32-hardware-guide.md)
- [hw_engine_bridge](hw_engine_bridge.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P25-1
