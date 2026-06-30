# web/physics_server.hexa

> WebSocket consciousness engine server: 6 topology (ring / small_world WS k=2 15% rewire / scale_free BA m=2 / hypercube / torus / spin_glass) + JSON broadcast 30 step/s · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — Port of `web/physics_server.py` (503 LOC) to hexa. CLI + engine + topology + JSON frame protocol 정의 + dashboard.html consumer. 실 WebSocket binding hexa stdlib 추가 대기 (현재 mock single-step run).

## 작동 코드 / 의존성

- 원본: `web/physics_server.hexa` (179 LoC)
- Consumer: `web/dashboard.html`
- 외부 의존: hexa run · (실 WS: stdlib socket-listen 추가 대기)
- 상수: PSI_COUPLING=0.014, PSI_BALANCE=0.5, PSI_F_CRITICAL=0.10, DEFAULT_CELLS=32, HIDDEN_DIM=64, SPEED=30 step/s, PORT=8765, N_FACTIONS=4

## 비용 / 리소스

- $0 Mac local · browser dashboard.html consumer

## 핵심 흐름 / topology + CLI

```
CLI: hexa physics_server.hexa [--engine sim|snn|esp32] [--cells 32]
                              [--topology ring|small_world|scale_free|hypercube|torus|spin_glass]
                              [--speed 30] [--port 8765]

Topology generators (6):
  ring          i → (i+1) % n,  weight=0.5
  small_world   Watts-Strogatz k=2, 15% rewire
  scale_free    Barabási-Albert m=2 (preferential attachment)
  hypercube     d-dim binary cube edges
  torus         2D grid wrap-around
  spin_glass    random ±J coupling

Protocol:
  Server → Client: JSON frame per step (30 step/s)
  Client → Server: config / command messages
```

## 트리거 (fire 방법)

```bash
# server
hexa run anima-physics/web/physics_server.hexa --topology small_world --cells 32 --speed 30

# browser
open anima-physics/web/dashboard.html      # connects ws://localhost:8765
```

## 검증 결과

- topology generator 6 종 정의
- JSON frame protocol 정의
- WS binding 미구현 (stdlib 대기)

## 관련 entry

- [consciousness-loop/src/main.md](../consciousness-loop/src/main.md) — engine source
- [consciousness-loop/src/snn_main.md](../consciousness-loop/src/snn_main.md) — snn engine
- [src/esp32_network.md](../src/esp32_network.md) — esp32 engine

## 출처

- README § 3 web/
- web/dashboard.html (consumer)
