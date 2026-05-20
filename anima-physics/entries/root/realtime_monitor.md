# realtime_monitor.hexa

> 실시간 inference latency + phi_live monitor; mock 2-layer CLM forward (d=16, vocab=32, seq=8) + histogram MI; rolling p50/p95/p99 · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 부분 — 시뮬 only (mock forward, CPU-only deployment 도 보장). 실 ckpt eval_clm cross-module 호출은 build_c `use` import 안정화 대기.

## 작동 코드 / 의존성

- `anima-physics/orchestration/realtime_monitor.hexa` (12 KB, ~310 LoC)
- 의존: 없음 (mock forward primitives 자체 정의)

## 비용 / 리소스

- 비용: $0 Mac local
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
Knobs: D=16, FF=32, VOCAB=32, SEQ=8, MI_BINS=8, GATE_LAT_MS=200.0

매 forward pass:
  - latency_ms — clock() wall-clock
  - phi_live   — instantaneous Φ_holo on last hidden state
                  (MI_BINS=8 histogram estimator, same as phi_holographic_measure)

Rolling report:
  p50 / p95 / p99 latency (ms)
  phi_live mean / min / max

Gate: p95 < 200 ms AND phi_live mean > 0.0 AND finite
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/realtime_monitor.hexa            # 64 iters
hexa run /Users/ghost/core/anima/anima-physics/orchestration/realtime_monitor.hexa --iters 32
```

## 검증 결과

- mock forward path 검증 (p95 < 200 ms, phi_live finite)
- 실 ckpt arg[2] 경로 TODO (cross-module `use` 안정화 후)
- byte-identical 미검증 (시간 의존 latency)

## 관련 entry

- [phi_substrate_consensus](phi_substrate_consensus.md)
- [rtc_sync](rtc_sync.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P24-1
