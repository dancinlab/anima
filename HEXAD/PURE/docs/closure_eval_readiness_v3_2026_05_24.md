# Phase D v3 closure eval readiness (4-criterion 측정 준비)

날짜: 2026-05-24  
도메인: HEXAD/PURE  
목적: v3 fire 결과에 대해 4-criterion closure judge 를 실행할 준비가 완료됐음을 문서화한다.

---

## 1. Criterion → probe → result.json 필드 매핑

| # | Criterion | Probe / 판정기 | result.json 필드 | 상태 |
|---|-----------|---------------|-----------------|------|
| 1 | multilingual 4/5 langs ≥ PARTIAL | `multilingual_probe.hexa` | `per_lang_verdicts` (list of `{lang, verdict}`) | trainer 가 직접 기록 ✓ |
| 2 | register_hits < 4/20 | judge | `n_anima_register_hits_total` | trainer 가 직접 기록 ✓ |
| 3 | motivation_8factor ≥ 0.30 | `closure_auto_judge.hexa` | `motivation_8factor.motivation_score` | dispatcher `--measure-motivation` embed 스텝 필요 ✓ (필드명 일치) |
| 4 | dream_stage Φ-envelope | `closure_auto_judge.hexa` | `dream_stage_at_eval.phi_envelope` | IPC embed 스텝 필요 ✓ (필드명 일치) |

기준 1·2 는 trainer 가 result.json 에 직접 emit 하므로 추가 처리가 불필요하다.  
기준 3·4 는 judge 실행 전 post-pull embed 스텝을 완료해야 한다.

---

## 2. 측정 순서 (critical)

```
result.json pull
  └─ ① motivation embed
        dispatcher embed_motivation_in_result
        (또는 --measure-motivation flag 를 통해 자동 실행)
  └─ ② dream_stage embed
        IPC → python3 patch
  └─ ③ closure_auto_judge 실행
```

> ⚠ 순서 역전 시 기준 3·4 의 필드가 result.json 에 존재하지 않아 judge 가 MISSING 으로 판정한다.

---

## 3. Judge 단일 실행 커맨드

```bash
cd /Users/ghost/core/anima && \
  HEXA_LANG=/Users/ghost/core/hexa-lang \
  POOL_DISABLE=1 \
  hexa run HEXAD/PURE/eval/closure_auto_judge.hexa <path-to-result.json>
```

`<path-to-result.json>` 은 embed 스텝 ①②가 완료된 결과 파일의 절대 경로로 교체한다.

---

## 4. 필드명 검증 요약

- `per_lang_verdicts` — trainer 직접 기록, probe 출력과 일치 ✓  
- `n_anima_register_hits_total` — trainer 직접 기록, judge 조회 키와 일치 ✓  
- `motivation_8factor.motivation_score` — embed 후 judge 가 중첩 키로 읽음, 필드명 일치 ✓  
- `dream_stage_at_eval.phi_envelope` — embed 후 judge 가 중첩 키로 읽음, 필드명 일치 ✓  

모든 필드명이 검증됐으므로 v3 fire 결과 도착 즉시 위 순서대로 실행 가능하다.
