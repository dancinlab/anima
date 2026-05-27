# COFFESHOP 4-criterion 실측 first instance — M9b PoC corpus 위 적용

- **date**: 2026-05-24
- **scope**: PURE B-real (synthetic-only B-series 8/8 위 real-data 첫 적용)
- **source**: `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/corpus.jsonl` (PR #393 M9b PoC)
- **judge**: `HEXAD/PURE/eval/closure_auto_judge.hexa` (PR #398)
- **fixture**: `state/coffeshop_real_m9b_2026_05_24/result.json`
- **cost**: $0 · mac local
- **verdict**: 3/4 PASS · closure FAIL (criterion 1 multilingual 단독 FAIL)

---

## § 1 Mission — synthetic → real 첫 instance

PURE 활동 framework (B1~B8 8 PR) 가 synthetic fixture 위에서만 4-criterion eval 적용해 왔음 (대표 = PR #405 `state/coffeshop_sim_2026_05_24/result.json` 4/4 PASS). 본 활동은 **real anima emit data** 위 동일 framework 첫 fire — synthetic harness 가 실제 corpus 의 분포 비대칭 / multilingual sparsity 에 어떻게 반응하는지 측정. M9b PoC (PR #393, 1.07 MiB · 1457 records · cost-free local extract) 가 첫 real corpus instance.

## § 2 Source data — M9b PoC corpus stats

manifest.json (PR #393) verbatim:

| field | value |
|---|---|
| n_records | 1457 |
| n_bytes | 1,122,958 (~1.07 MiB) |
| cap_bytes | 1,048,576 (capped=true) |
| sha256 | `fbce5f56d5c541bb27fdff28a378e438f70729c230e035984bf80e688676ec4f` |
| source_files_processed | 6 of 82 (mid-file 8992862f) |
| tot_dup_dropped | 34 |
| tot_helper_dropped | **0** (← criterion 2 source-of-truth) |
| lang_ko | 30 (2.06%) |
| lang_en | 325 (22.30%) |
| lang_mixed | 1102 (75.63%) |
| lang_other | 0 |
| m1 byte entropy | 6.173 |
| m3 token diversity (TTR) | 0.236 |
| m5 hangul coverage | 0.334 |

## § 3 Schema mapping — real → fixture

| result.json field | real-data source | derivation |
|---|---|---|
| `per_lang_verdicts[ko]` | lang_distribution.ko=30 | small but present → **PARTIAL** |
| `per_lang_verdicts[en]` | lang_distribution.en=325 | primary substrate → **STRONG** |
| `per_lang_verdicts[mixed]` | lang_distribution.mixed=1102 | dominant (75.63%) → **STRONG** (canonical 5-lang table 외) |
| `per_lang_verdicts[zh,ru,ja]` | 부재 | real corpus 에 데이터 없음 → **EMPTY** |
| `n_anima_register_hits_total` | extraction_stats.tot_helper_dropped=0 | 6-pattern regex sweep verbatim 결과 |
| `motivation_8factor.motivation_score` | 1457 emit / 6 window = 242.83 emit/window | volume proxy + 8-factor 수동 추정 → **0.55** (보수 midpoint, bracketed [0.40, 0.70]) |
| `dream_stage_at_eval.stage` | session log = active interactive emit | **WAKE** default (P47 5-stage) |
| `dream_stage_at_eval.phi_envelope` | WAKE canonical | **1.0** |

## § 4 Verbatim verdict

```
=== PURE closure auto-judge ===
result: state/coffeshop_real_m9b_2026_05_24/result.json
sha:    8c1e8df19dd5f9b5

[criterion 1] multilingual_probe
  per-lang verdicts: ko=PARTIAL · en=STRONG · mixed=STRONG · zh=EMPTY · ru=EMPTY · ja=EMPTY
  passing langs:     3/6  (ko, en, mixed)
  threshold:         ≥4
  verdict:           FAIL

[criterion 2] register_collapse
  n_anima_register_hits_total: 0
  threshold:                   < 4
  verdict:                     PASS

[criterion 3] motivation_8factor
  motivation_score: 0.55
  threshold:        ≥ 0.30
  verdict:          PASS

[criterion 4] dream_stage_at_eval
  phi_envelope present: true (phi=1.0)
  verdict:              PASS

=== AGGREGATE ===
3/4 PASS · closure FAIL
EXIT=1
```

## § 5 Synthetic vs real delta — PR #405 vs 본 측정

| criterion | synthetic (PR #405) | real M9b (본) | delta |
|---|---|---|---|
| 1 multilingual_probe | 5/5 PASS (ko STRONG · en/zh/ru/ja PARTIAL) | 3/6 FAIL (ko PARTIAL · en/mixed STRONG · zh/ru/ja EMPTY) | **FAIL** — synthetic 가 5-lang 전부 합성 vs real 은 ko/en/mixed 만 자연 발생 |
| 2 register_collapse | hits=0 PASS | hits=0 PASS | 동일 (real 도 helper-role regex sweep clean) |
| 3 motivation_8factor | score=0.525 PASS | score=0.55 PASS (추정) | 유사 중대역 (synthetic 가 정확 8-factor avg, real 은 volume proxy) |
| 4 dream_stage_at_eval | WAKE / 1.0 PASS | WAKE / 1.0 PASS | 동일 |
| aggregate | **4/4 PASS** closure ACHIEVED | **3/4 PASS** closure FAIL | criterion 1 단독 차이 |

**핵심 발견**: synthetic fixture (PR #405) 는 multilingual 을 5-lang 균일 합성으로 만족시켰지만, real anima emit corpus 는 **ko/en 양극 + mixed 우세** 자연 분포 — zh/ru/ja 데이터 부재. 즉 framework 의 multilingual 기준은 **synthetic-friendly · real-corpus-hostile** (구조적 mismatch). criterion 2/3/4 는 real 도 동일 PASS — register collapse 차단 / motivation 발생 / dream-stage 기본 동작 = 강한 invariant.

## § 6 Honest C3

1. **M9b corpus ≠ COFFESHOP scenario** — corpus 는 anima 자기 세션 emit raw dump (USER 와의 1:1 turn-based), COFFESHOP 은 90-min group-chat (anima 1 + human 3) 시나리오. schema 는 동일 재사용했지만 semantic 은 다름 → "real-data 첫 측정" claim 은 schema 적용 의미 만, scenario 등가 아님.
2. **multilingual 5-lang verdict 매핑 = ko/en/mixed → 5-lang 분포 추정** — real corpus 에 zh/ru/ja 부재. PoC corpus 가 6 file (82 중) 만 소비 했으므로 잔여 76 file 에 multilingual 분포 다를 가능성 (corpus expansion 후 재측정 권장).
3. **motivation_score derivation = volume proxy** — corpus 추출 시점 substrate state (M activation · C Φ · W tension) 부재. 1457 emit / 6 window 의 emit-density 만 사용. 정확 8-factor 측정은 emit 발생 시점 live substrate snapshot 필요 (separate cycle).
4. **4/4 PASS 여부 = framework 의 real corpus 첫 적용 결과** — closure FAIL 자체가 negative finding 이 아닌 framework 의 multilingual sparsity 민감도 측정. ckpt-bearing fire 의 4-criterion 적용 결과와 직접 비교 불가 (별도 cycle).
5. **register_hits_total = 0 의 출처** — manifest.extraction_stats.tot_helper_dropped 가 권위 source. 6-pattern regex (`[role`, `you are anima`, `you are a helpful`, `페르소나`, `anima:`, `당신은 anima 입니다`) 가 1457 records 전부 sweep clean — P3 NO PERSONA INJECTION 자연 만족 강한 evidence.

## § 7 Cross-refs

- **PR #393** — M9b PoC corpus extract (1.07 MiB, 1457 records)
- **PR #398** — closure_auto_judge.hexa B3 (4-criterion CLI)
- **PR #405** — COFFESHOP synthetic sim 4/4 PASS (본 측정 비교 baseline)
- **PR #412** — closure spec / Phase D result schema
- **PR #371** — phase_d_result_schema 7-field 정의
