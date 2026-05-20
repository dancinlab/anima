# src/esp32_network.hexa

> ESP32×8 consciousness network orchestrator stub (2 GRU cell/board × 8 boards = 16 cell, SPI ring, 1040B packet) · **🟡 부분** · 비용 $40 BOM

## 구현 가능성

🟡 — struct + 함수 signature 정의, `step()` trivial. 실 SPI ring orchestration 미구현. esp32/src/lib.hexa 가 board-level lib, 본 파일은 host-side orchestrator.

## 작동 코드 / 의존성

- 원본: `src/esp32_network.hexa` (30 LoC)
- 외부 의존: 없음 (stub) — impl 시 ESP-IDF flash + serial multiplex
- 상수: n_boards=8 → 16 cells · spi_packet_bytes=1040 · topology 변수

## 비용 / 리소스

- $40 BOM (8 ESP32 × $5)
- $77 hardware-guide (docs/esp32-hardware-guide.md, ESP32-WROOM-32 × 8)

## 핵심 흐름 / 코드 발췌

```hexa
struct ESP32Board {
    board_id: i32,
    cell_a_phi: float,
    cell_b_phi: float,
    spi_connected: bool
}

struct ESP32Network {
    n_boards: i32,
    topology: string,
    total_phi: float,
    spi_packet_bytes: i32        // 1040
}

fn create_network(n_boards, topology) -> ESP32Network {
    return ESP32Network(n_boards, topology, 0.0, 1040)
}
fn step(network) -> ESP32Network { network }
fn run_benchmark(steps, topology) -> float { 0.0 }
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/src/esp32_network.hexa
```

## 검증 결과

- struct + 1040B packet 정의 검증
- 실 SPI ring orchestration 미테스트

## 관련 entry

- [esp32/src/lib.md](../esp32/src/lib.md) — board-level ConsciousnessBoard
- [esp32/qrng_bridge.md](../esp32/qrng_bridge.md)
- [hw/autonomous_expansion.md](../hw/autonomous_expansion.md)

## 출처

- README § 3 src/
- README § 5 cheat sheet ($40-77 ESP32×8)
- docs/esp32-hardware-guide.md
