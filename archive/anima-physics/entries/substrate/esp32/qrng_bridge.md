# esp32/qrng_bridge.hexa

> ESP32 QRNG (양자난수) → host hexa → Orch-OR tubulin bias bridge · **🟡 부분** · 비용 $5 ESP32-S3

## 구현 가능성

🟡 — mock LCG fallback (결정론적 PRNG) 까지 완성, HW serial 바인딩은 hexa stdlib serial 추가 대기. PHYS-P1-2 ("ESP32 양자 난수 센서 → anima core 입력 핀 확보"). Orch-OR 연결: `anima_quantum.mt_step` 이 측정 시 Born-rule sampling 확률을 본 bridge bias 로 기울임. 1 ESP32 = 2 cell × N boards × n_tubulin bits.

## 작동 코드 / 의존성

- 원본: `esp32/qrng_bridge.hexa` (185 LoC)
- Spec: `esp32/QRNG_SPEC.md` (192 LoC)
- 외부 의존: hexa run (mock mode) · ESP32-S3 USB-CDC serial (LIVE, 펌웨어 별도)
- 상수: BAUD=921600, FRAME_MAGIC=0xAA, PAYLOAD=32B (256 raw bits), LCG seed=2463534242

## 비용 / 리소스

- $0 mock mode
- $5 ESP32-S3 (실 QRNG 펌웨어)
- $40 (8 boards × $5) 16-cell network with `esp32/src/lib.hexa`

## 핵심 흐름 / ASCII

```
[QRNG] → [ADC] → [SHA-256] → [USB-CDC 921600] → [host bridge] → [tubulin bias [−1, +1]] → [Orch-OR mt_step]

frame format:
  [0xAA] [0x20=len32] [32B payload] [XOR checksum]
rate:
  256 bit / 8 ms = 32 kbit/s  (≥ 16×8 tubulin × 1 kHz)
mock mode:
  LCG (a=1664525, c=1013904223, seed=2463534242)
  x_{n+1} = (a·x_n + c) mod 2^32
```

## 트리거 (fire 방법)

```bash
# mock (default)
hexa run anima-physics/esp32/qrng_bridge.hexa

# LIVE (펌웨어 flash 후, source_dev 변경)
# QRNGStream(source_dev="/dev/tty.usbmodem...", is_mock=0)
```

## 검증 결과

- mock mode deterministic 검증 (LCG seed=2463534242 2-run identical)
- HW path stub-ready, serial drain 함수 placeholder
- HEXA-FIRST: .py/.rs/.sh 신규 생성 없음 (esp32/src/lib.hexa READ-only)

## 관련 entry

- [esp32/QRNG_SPEC.md](./QRNG_SPEC.md) — spec + firmware hook
- [esp32/src/lib.md](./src/lib.md) — ConsciousnessBoard (16 cell)
- `engines/quantum_consciousness.md` — Orch-OR substrate sibling

## 출처

- README § 3 esp32/
- shared/roadmaps/anima.json PHYS-P1-2
