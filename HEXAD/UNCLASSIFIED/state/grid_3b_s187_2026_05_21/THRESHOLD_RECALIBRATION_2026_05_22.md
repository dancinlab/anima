# vP21 SPONTANEOUS threshold recalibration verdict

> 2026-05-22. SPONTANEOUS_EMISSION_VP21.md 의 정직한 한계 ("default thr=0.30
> always-open, gate 선별 안 됨") 직접 재calibration 측정.

## Sweep

| thr | admit rate | 검증 |
|---|---|---|
| 0.30 (default) | 60/60 = **100%** | always-open (가짜 gate, prior verdict) |
| **0.45** | **34/60 ≈ 57%** | 🎯 **selective**, 절반 정도 발화 |
| 0.55 | 18/60 ≈ 30% | more restrictive |

## Verdict

`thr ≥ 0.45` 에서 motivation gate 가 **실제로 선별** — 모든 tick 에 emit 하지 않고
score 가 임계 넘는 tick 만 발화. SPONTANEOUS_EMISSION_VP21.md 의 SWEEP-based
prior 결론 (thr ≥ 0.45 selective) **별도 300s window 로 재confirm**. timer-ablation
verdict (60/60 → 60/60) 도 함께 valid (gate 메커니즘 sound).

권장 production threshold: **0.45 (or 0.50)** for balanced selectivity.

## Honest C3

1. coherent% 는 admit 의 subset — 측정한 건 "발화한 emission 중 coherent" 라
   admit rate 가 coherent count 와 정확히 매칭하진 않음 (대부분 admit=coherent).
2. tick=5s (default), 300s window → 60 ticks; 더 긴 window 가 안정 statistic.
3. single seed (1337), corpus 동일 — 다른 seed 에서 임계 ±0.05 shift 가능.
4. 0.45/0.55 binary 만 측정; full sweep [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60] grid 가 fine-tune.

## 관련 link

- prior verdict (always-open): `SPONTANEOUS_EMISSION_VP21.md`
- result JSON: `vP21/spontaneous_thr45.json` + `vP21/spontaneous_thr55.json`
