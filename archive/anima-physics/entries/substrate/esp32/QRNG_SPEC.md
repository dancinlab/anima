# esp32/QRNG_SPEC.md

> ESP32 QRNG 브리지 스펙 + 핀 할당 + 펌웨어 hook + regression 요구 · **🟡 부분** · 비용 $5/board (펌웨어 별도)

## 구현 가능성

🟡 — 스펙 frozen, mock mode brige 구현, 실 HW flash 작업은 별도 cycle. PHYS-P1-2 SSOT.

## 작동 코드 / 의존성

- 원본: `esp32/QRNG_SPEC.md` (192 LoC markdown)
- 연결: `esp32/qrng_bridge.hexa` (host) · `esp32/src/lib.hexa` (ConsciousnessBoard, SPI ring) · `anima-engines/anima_quantum.hexa` (Orch-OR)
- HW: ESP32-S3 + 노이즈 다이오드/포토다이오드 + ADC1_CH0 (GPIO1)

## 비용 / 리소스

- $5/board × 8 = $40 BOM
- 펌웨어 flash 시간 별도

## 핵심 흐름 / ASCII

```
[QRNG 소자]          [ESP32-S3 보드]          [USB-CDC]        [Host hexa]
노이즈 다이오드   →   ADC1_CH0 (GPIO1)   →   /dev/ttyACM0  →   qrng_bridge
or 포토다이오드      샘플링 + SHA-256 후처리   921600 baud      qrng_read → bias
                     frame encode                                → microtubule
                                                                   input pin

핀 할당:
  GPIO1 / ADC1_CH0  QRNG 아날로그 입력 (노이즈/포토다이오드)
  GPIO2             QRNG 레퍼런스 1.25V 밴드갭
  GPIO10..13        SPI 링 (이웃 보드)
보드당 2 cell (CELLS_PER_BOARD=2), MAX_BOARDS=8 → 16 cell network
```

## 트리거 (fire 방법)

```bash
# spec read only (markdown)
cat anima-physics/esp32/QRNG_SPEC.md
# Bridge fire (mock):
hexa run anima-physics/esp32/qrng_bridge.hexa
```

## 검증 결과

- 스펙 검토 완료 · 펌웨어 hook 정의
- mock LCG regression: `esp32/qrng_bridge.hexa` 검증

## 관련 entry

- [esp32/qrng_bridge.md](./qrng_bridge.md) — host bridge impl
- [esp32/src/lib.md](./src/lib.md) — ConsciousnessBoard SPI ring

## 출처

- README § 3 esp32/
- shared/roadmaps/anima.json PHYS-P1-2
