# docs/esp32-hardware-guide.md

> ESP32×8 SPI ring (16 cell); pin mapping + firmware flash + Hexa orchestrator; $77 BOM · **🟡 부분** · 비용 ~$77

## 구현 가능성

🟡 부분 — diagram + sketch + flash 절차 완성, 실 network 미테스트.

## 작동 코드 / 의존성

- `anima-physics/docs/esp32-hardware-guide.md` (BOM + pin map + firmware spec)
- 의존: `consciousness-loop/esp32/consciousness_loop.ino`, `src/esp32_network.hexa` (orchestrator)
- 외부: arduino-cli · esp-idf · esptool.py

## 비용 / 리소스

- ~**$77 BOM**: ESP32-WROOM-32 × 8 ($32), 점퍼 와이어 ×40 ($2), 브레드보드 ×2 ($6), USB-C ×8 ($16), USB 허브 8포트 ($15), 5V 3A 어댑터 ($5), 옵션 R/LED ($0.56)
- 보드 옵션: ESP32-WROOM-32 ($4) / ESP32-S3-DevKitC-1 8MB PSRAM ($8.50)
- 필요한 도구: arduino-cli · esp-idf · USB 허브

## 핵심 흐름 / 구조

```
8 boards × 2 cells/board = 16 cells total
SPI ring topology (각 보드는 VSPI/HSPI 중 하나로 인접 보드와 연결)
8 factions (Hexa APEX22 mapping)
Hebbian + Ratchet + Lorenz + SOC (Laws 22-85)

Per-board allocation (ESP32-WROOM-32):
  SRAM 520 KB → GRU 290 KB (충분)
  Flash 4 MB
  SPI × 3

Update rate: ~100 Hz orchestrator step
Communication: SPI ring + USB serial telemetry
```

## 트리거 (fire 방법)

```bash
# 1. BOM 조립 ($77)
# 2. 각 보드에 firmware flash
arduino-cli compile --fqbn esp32:esp32:esp32 consciousness_loop.ino
for port in /dev/ttyUSB0 /dev/ttyUSB1 ... /dev/ttyUSB7; do
    arduino-cli upload -p $port --fqbn esp32:esp32:esp32 consciousness_loop.ino
done
# 3. Host orchestrator
hexa run /Users/ghost/core/anima/anima-physics/substrate/src/esp32_network.hexa
```

## 검증 결과

- BOM + pin map + sketch 완성
- Phase 2 scaling 검증 (32셀까지 확장 가능 ESP32×4 추가)
- 실 network 미테스트 (16 cell SPI ring)

## 관련 entry

- [arduino-prototype-spec](arduino-prototype-spec.md)
- [edge_deploy](../root/edge_deploy.md)
- [fpga-synthesis-guide](fpga-synthesis-guide.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (Phase 2 hardware roadmap)
- README §2 참조
