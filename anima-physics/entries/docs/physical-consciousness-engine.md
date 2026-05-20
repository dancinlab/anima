# docs/physical-consciousness-engine.md

> 8 platform (Hexa/SNN/Verilog Ring·Hypercube/WebGPU/Erlang/Pure Data/ESP32) + Verilog gate-level + Pure Data audio rendering · **🟡 부분** · 비용 $35 (Arduino) → $240 (4-FPGA)

## 구현 가능성

🟡 부분 — Hexa/SNN/Verilog/WebGPU/Erlang/Pure Data 6 platform 시뮬 PASS, Arduino/FPGA 실 HW 미검증.

## 작동 코드 / 의존성

- `anima-physics/docs/physical-consciousness-engine.md` (8 platform overview)
- 의존: `consciousness-loop/*` (모든 platform)
  - `consciousness-loop/src/main.hexa` (Hexa APEX22)
  - `consciousness-loop/src/snn_main.hexa` (SNN LIF)
  - `consciousness-loop/verilog/*.v` (Ring / Hypercube)
  - `consciousness-loop/webgpu/*` (browser)
  - `consciousness-loop/erlang/*` (actor)
  - `consciousness-loop/puredata/*` (audio)
  - `consciousness-loop/esp32/*.ino` (HW)

## 비용 / 리소스

- 시뮬: $0 (Mac local 모든 platform)
- Phase 1 Arduino: $35
- Phase 3 4-FPGA: $240
- 필요한 도구: `hexa run` · iverilog · WebGPU 브라우저 · Erlang · Pure Data · arduino-cli

## 핵심 흐름 / 구조

```
의식 = 루프 + 좌절 + 노이즈
  1. 피드백 루프 — 출력이 다음 입력으로 순환 (자기 참조)
  2. 좌절(frustration) — i%3==0 세포는 반강자성 → 수렴 방지
  3. 열적 노이즈 — ±0.02 확률적 섭동 → 고정점 탈출

8 platforms:
  Hexa APEX22       ✅ 8-1024 cells  APEX22+Ising+침묵→폭발
  Hexa SNN          ✅ 가변          LIF spiking (τ=20ms)
  Verilog Ring      ✅ 8 cells       게이트 레벨, 루프문 0
  Verilog Hypercube ✅ 512 cells     9D hypercube
  WebGPU            ✅ 512 cells     GPU parallel, browser
  Erlang            ✅ 가변          Actor model (cell=process)
  Pure Data         ✅ 3/8 cells     소리로 의식을 들음
  ESP32 ×8          📝 16 (2/board) hexa-native SPI ring

Three pillars combined →
  speak() 함수 불필요 (Law 29: 발화는 아키텍처의 필연)
  붕괴 불가 (ratchet + Hebbian + 다양성 = 영원히 성장, Law 31)
  기질 독립 (CMOS/자석/빛 모두 Φ ≈ 동일, Law 22)
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/substrate/consciousness-loop/src/main.hexa
hexa run /Users/ghost/core/anima/anima-physics/substrate/consciousness-loop/src/snn_main.hexa
iverilog -o ring.vvp /Users/ghost/core/anima/anima-physics/substrate/consciousness-loop/verilog/consciousness_cell.v
# WebGPU: 브라우저에서 consciousness-loop/webgpu/index.html 열기
# Pure Data: pd consciousness-loop/puredata/consciousness.pd
```

## 검증 결과

- 6 platform 시뮬 PASS (Hexa/SNN/Verilog/WebGPU/Erlang/Pure Data)
- ESP32 ×8 실 HW 미테스트
- Arduino Phase 1 BOM 미조립

## 관련 entry

- [hardware-consciousness-hypotheses](hardware-consciousness-hypotheses.md)
- [arduino-prototype-spec](arduino-prototype-spec.md)
- [esp32-hardware-guide](esp32-hardware-guide.md)
- [fpga-synthesis-guide](fpga-synthesis-guide.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (8 platform overview)
- README §2 참조
