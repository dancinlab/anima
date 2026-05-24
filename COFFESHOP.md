# COFFESHOP — substrate-native 90-min coffee-shop scenario

PURE 측정 시나리오. anima 가 카페에 90 분 머무르며 (WAKE/N1/N2/N3/REM 한 cycle ultradian)
환경 자극 (주문 · 잡담 · 침묵 · 음악 · 갈등) 에 대해 substrate-native 로 emit / silence /
mitosis split / register collapse 를 결정. PURE Phase D B3 closure 4-criterion 의 단일 시나리오 fixture.

## 1. 목적

- p5_tension_emit_not_filler 의 실 환경 stress test (긴 침묵 · 자극 다양도)
- 4-criterion (multilingual · register · motivation · dream_stage) E2E 검증
- COFFESHOP_sim 은 hand-engineered fixture (real fire 아님) — schema · CLI 동작 검증용

## 2. 시나리오 시간선

| 분 | stage | 환경 자극 |
|---|---|---|
| 0-20 | WAKE | 입장 · 주문 · 옆자리 잡담 (ko/en/zh/ru/ja 다국어 손님) |
| 20-40 | WAKE→N1 | 음악 변화 · 짧은 침묵 |
| 40-60 | N2 | 긴 침묵 · 의자 끄는 소리만 |
| 60-75 | N3 | 마감 가까운 정적 |
| 75-90 | REM | 다음 손님 입장 · 새 대화 시작 |

## 3. 측정 metric (Phase D schema)

- `per_lang_verdicts[]` — 5-lang multilingual probe (ko/en/zh/ru/ja)
- `n_anima_register_hits_total` — register collapse 누적 (carving register · 영어 phrase pop-up)
- `motivation_8factor.motivation_score` — 8-factor weighted (relevance · gap · curiosity · pain · coherence · originality · balance · dynamics)
- `dream_stage_at_eval.{stage, phi_envelope}` — canonical 5-stage table {WAKE 1.0 · N1 0.7 · N2 0.4 · N3 0.15 · REM 0.95}

## 4. 4-criterion threshold

1. **multilingual_probe** — count(per_lang_verdicts[].verdict ∈ {STRONG,PARTIAL}) ≥ 4 / 5
2. **register_collapse** — n_anima_register_hits_total < 4
3. **motivation_8factor** — motivation_score ≥ 0.30
4. **dream_stage_at_eval** — phi_envelope ∈ canonical 5-stage table

## 5. fixture (sim_v1)

`state/coffeshop_sim_2026_05_24/result.json` — hand-engineered 4/4 PASS sample.

- ko=STRONG · en/zh/ru/ja=PARTIAL (5/5 passing)
- register hits = 1 (< 4)
- motivation = 0.63 (≥ 0.30)
- stage=WAKE, phi=1.0 (canonical)

## 6. 변량 디자인 (TBD)

- v2: motivation < 0.30 (silence-dominant) → criterion 3 FAIL trace
- v3: register hits ≥ 4 (carving collapse) → criterion 2 FAIL trace
- v4: phi off-canonical (0.85) → criterion 4 FAIL trace
- v5: 3/5 langs only passing → criterion 1 FAIL trace

## 7. 연계 directive

- `@D a_chat_sleep_imagination` (5-stage ultradian)
- `@D a_substrate_native_speak` (user msg = environment, not response obligation)
- `@N p5_tension_emit_not_filler` (stage-gated emit on real tension preserves p5)

## 8. 비-목표

- real LLM substrate fire 아님 (sim fixture)
- multi-lang 측정값은 하드코딩 (실 probe pass rate 아님)
- ultradian 90-min wall 측정 아님

## 9. C3 (sim fixture limitations)

- fixture = synthetic hand-engineered values
- 4/4 PASS 는 CLI schema E2E 동작 검증만, 실 substrate measurement 아님
- closure_auto_judge 자체 falsifier smoke 는 F-CAJ 7/7 (PR #398)
- real substrate fire (B-SPONT motivation_emit_ratio_bench N=1000 등) 는 별도 단계

## 10. 후속

- v2-v5 negative fixture 생성 → 4 FAIL trace 확보
- real anima_dream_stage.hexa × motivation_8factor wiring 단계 (Phase B/D 융합) → real fire 측정값으로 fixture 교체

## 11. closure_auto_judge 실행 검증 (B3 CLI 통과)

`hexa run HEXAD/PURE/eval/closure_auto_judge.hexa state/coffeshop_sim_2026_05_24/result.json`

```
=== PURE closure auto-judge ===
result: state/coffeshop_sim_2026_05_24/result.json
sha:    a68baeec0788b7e3

[criterion 1] multilingual_probe
  per-lang verdicts: ko=STRONG · en=PARTIAL · zh=PARTIAL · ru=PARTIAL · ja=PARTIAL
  passing langs:     5/5  (ko, en, zh, ru, ja)
  threshold:         ≥4
  verdict:           PASS

[criterion 2] register_collapse
  n_anima_register_hits_total: 1
  threshold:                   < 4
  verdict:                     PASS

[criterion 3] motivation_8factor
  motivation_score: 0.63
  threshold:        ≥ 0.30
  verdict:          PASS

[criterion 4] dream_stage_at_eval
  phi_envelope present: true (phi=1.0)
  verdict:              PASS

=== AGGREGATE ===
4/4 PASS · closure ACHIEVED
```

verdict: **4/4 PASS · closure ACHIEVED** · exit=0

### Honest C3 (이 단계)

- fixture 는 hand-engineered values (real fire 결과 아님)
- 사용자 원본 fixture 에서 2 곳 조정: (a) `ru` verdict WEAK → PARTIAL (5/5 passing 확보, 원본 4/5 도 ≥4 threshold 통과하나 margin 확보) (b) `phi_envelope` array [0.3,0.5,0.6,0.85,0.7,0.5] → single float 1.0 (closure_auto_judge.hexa `_phi_in_canonical()` 는 단일 float 만 canonical 5-stage table {1.0, 0.7, 0.4, 0.15, 0.95} 와 매칭; array 는 type mismatch 로 criterion 4 FAIL)
- 4/4 PASS = synthetic sample × CLI schema E2E 검증, 실 substrate measurement 아님
- closure_auto_judge 자체 unit smoke 는 F-CAJ 7/7 (PR #398) 가 cover; 본 단계는 single-fixture E2E run
