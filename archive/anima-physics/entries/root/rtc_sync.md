# rtc_sync.hexa

> PHYS-P11-2 물리 timestamp; TCXO drift <1ppm PI discipline + 온도 보정 + NTP-style sync · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — T1-T5 PASS (free-running drift / 24h·48h disciplined <1ppm / monotonic / determinism). Husserlian retention-chain 일관성 보장.

## 작동 코드 / 의존성

- `anima-physics/rtc_sync.hexa` (13 KB, ~340 LoC)
- 의존: 없음 (struct return bug 회피 위해 모든 clock state flat `let mut` 인라인)

## 비용 / 리소스

- 비용: $0 Mac local
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
TCXO 모델:
  Raw TCXO drift (ppm) at temp T ≈ TEMP_COEFF · (T - T_NOM)
  T_NOM = 25 °C, TEMP_COEFF = 0.08 ppm/°C
  ±10 °C diurnal swing → peak |drift| ~0.8 ppm

PI discipline (every SYNC_INTERVAL_SEC):
  adj_ppm := adj_ppm - (K_P · e_ppm + K_I · integrator)
  K_P = 0.35, K_I = 0.010

API:
  simulate_rtc(total_hours, sync_interval_sec) -> drift_ppm
  simulate_free(total_hours) -> drift_ppm
  rtc_timestamp(sample_hour) -> float seconds
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/rtc_sync.hexa
```

## 검증 결과

- T1 free-running crystal has non-trivial peak drift PASS
- T2 disciplined 24h drift < 1 ppm PASS (roadmap criterion)
- T3 disciplined 48h temperature-sweep drift < 1 ppm PASS
- T4 rtc_timestamp monotonic + correct magnitude PASS
- T5 API contract + determinism (two calls bit-identical) PASS
- **5/5 PASS**

## 관련 entry

- [realtime_monitor](realtime_monitor.md)
- [signal_corpus](signal_corpus.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-14
- README §1 참조 · roadmap PHYS-P11-2
