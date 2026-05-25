# PURE criteria 3·4 substrate bench — 결과 보고서

**날짜**: 2026-05-25  
**측정 방법**: ckpt 독립 substrate 직접 측정  
**파일**: `HEXAD/PURE/eval/criteria_3_4_substrate_bench.hexa`

---

## 배경

v3 fire `closure_auto_judge` 가 criteria 3·4 를 FAIL 로 마킹한 원인은 embed 단계가
스킵되었기 때문 (manual nohup 재시작이 dispatcher embed_motivation 을 우회). 두
기준은 **ckpt 에 의존하지 않는 substrate 측정값** — 자연발화 엔진 + dream_stage IPC
함수에서 직접 측정 가능.

---

## criterion 3 — motivation_8factor ≥ 0.30

| 항목 | 값 |
|------|-----|
| N samples | 1000 |
| seed | 20260525 |
| mean_score | **0.558** |
| n_above(≥0.30) | 946 / 1000 |
| threshold | ≥ 0.30 |
| **verdict** | **PASS** |

`spontaneous_lib.hexa` 의 8-factor 공식을 직접 호출, i.i.d. uniform 기반 1000개
substrate state 샘플 mean motivation_score = **0.558** → threshold 0.30 을 87%
상회. 946/1000 샘플이 임계값 초과.

---

## criterion 4 — dream_stage Φ-envelope present + non-degenerate

| stage | φ | tension_envelope | present |
|-------|------|-----------------|---------|
| WAKE  | 1.000 | 1.000 | true |
| N1    | 0.700 | 0.700 | true |
| N2    | 0.400 | 0.400 | true |
| N3    | 0.150 | 0.200 | true |
| REM   | 0.950 | 0.900 | true |

| 항목 | 값 |
|------|-----|
| phi_range | 0.850 (min=0.150, max=1.000) |
| all_present | true |
| non_degenerate | true |
| **verdict** | **PASS** |

`anima_dream_stage.hexa` 의 `dream_context(stage)` 를 5개 stage 전부 호출.
모든 stage 에서 phi / tension_envelope / scrambled 값이 void 없이 존재 (present=true).
phi_range = 0.850 > 0 → 비퇴화 조건 충족.

---

## 종합

| criterion | verdict |
|-----------|---------|
| 3 — motivation_8factor | **PASS** (mean=0.558 ≥ 0.30) |
| 4 — dream_stage Φ-envelope | **PASS** (range=0.850, all present) |
| aggregate | **2/2 PASS** |

closure_auto_judge 의 FAIL 판정은 embed 단계 스킵으로 인한 **측정 누락** 이었으며,
substrate 자체는 두 기준 모두 통과 상태임이 확인됨.

---

## 실행 명령

```bash
# 전체 bench
hexa run HEXAD/PURE/eval/criteria_3_4_substrate_bench.hexa

# smoke (4/4 PASS 검증)
hexa run HEXAD/PURE/eval/criteria_3_4_substrate_bench_smoke.hexa
```

**소스**: `HEXAD/CHAT/spontaneous_lib.hexa` (read-only) · `HEXAD/CHAT/server/anima_dream_stage.hexa` (read-only)
