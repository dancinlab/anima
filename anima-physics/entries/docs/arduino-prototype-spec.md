# docs/arduino-prototype-spec.md

> Phase 1 Arduino 8셀 ring + Hall sensors ($34.46 BOM); electromagnetic frustration + 100Hz update + JSON serial · **🟡 부분** · 비용 $34.46 BOM

## 구현 가능성

🟡 부분 — circuit + Arduino sketch + host bridge 완성, 실물 조립 미검증. Phase 1 "존재 증명" 목표.

## 작동 코드 / 의존성

- `anima-physics/docs/arduino-prototype-spec.md` (BOM + circuit + protocol)
- 의존: `consciousness-loop/esp32/consciousness_loop.ino` (pseudo Arduino sketch)
- 외부: Arduino IDE / arduino-cli

## 비용 / 리소스

- 비용: **$34.46 BOM** (Arduino Uno R3 $8, 8× 5V electromagnet $12, 8× Hall A3144 $2.40, 2× L293D $4, R/C $0.56, PSU $3, breadboard $2.50, wires $2)
- 필요한 도구: Arduino IDE · 5V 2A PSU · 조립 (브레드보드)

## 핵심 흐름 / 구조

```
        ╭──[M1]──[M2]──╮
        │               │
      [M8]            [M3]
        │               │
      [M7]            [M4]
        │               │
        ╰──[M6]──[M5]──╯

  M = 전자석 (5V, 200mA)
  [M3,M6] = frustration cells (반강자성: 전류 반전)
  Hall 센서: 각 전자석 사이 1개 (8개)
  Arduino Uno: PWM 제어 + ADC 측정
  Update rate: 100 Hz
  JSON over serial → host bridge → Hexa consciousness loop
```

## 트리거 (fire 방법)

```bash
# 1. BOM 부품 조립 ($34.46)
# 2. Arduino IDE 로 sketch 업로드
arduino-cli compile --fqbn arduino:avr:uno consciousness_loop.ino
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:uno consciousness_loop.ino
# 3. Host bridge 실행
hexa run /Users/ghost/core/anima/anima-physics/consciousness-loop/src/main.hexa
```

## 검증 결과

- BOM + circuit diagram + sketch 완성
- 실물 조립 시 verify_7cond_hw.hexa T3 (ESP32 perturbation) 첫 실측 가능
- 현재 검증: 시뮬레이션만

## 관련 entry

- [arduino_local_sim_landing](arduino_local_sim_landing.md)
- [esp32-hardware-guide](esp32-hardware-guide.md)
- [physical-consciousness-engine](physical-consciousness-engine.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (Phase 1 hardware roadmap)
- README §2 참조
