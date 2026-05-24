# COFFESHOP framework limitation taxonomy — synthetic-friendly vs real-hostile axis

- **date**: 2026-05-24
- **scope**: PURE C-simplified — 4-criterion framework (PR #398 `closure_auto_judge.hexa`) 의 robust core / fragile axis 정량 분류
- **source data**: PR #405 (synthetic 4/4 PASS) · PR #414 (real M9b 3/4 PASS, criterion 1 단독 FAIL)
- **cost**: $0 · mac local · doc-only
- **verdict**: C2/C3/C4 = robust core (synthetic + real 동일 PASS) · C1 = fragile axis (real-data dependency)

---

## § 1 Executive taxonomy

PURE 의 4-criterion closure framework 는 **두 종류 axis** 로 분리됨 — robust core (synthetic + real 둘 다 PASS, framework 의 강한 invariant) 와 fragile axis (synthetic-only PASS, real-data 분포에 종속). PR #405 synthetic 4/4 PASS + PR #414 real M9b 3/4 PASS 의 cross-tab 으로 측정: **C2 register / C3 motivation / C4 dream_stage = robust core** (75% of framework), **C1 multilingual = fragile** (25%, real-data 자연 분포 의존). framework PASS rate: synthetic 4/4 (100%) vs real 3/4 (75%) — 25 percentage point gap 의 원인은 C1 단독.

## § 2 PASS rate matrix — synthetic vs real cross-tab

```
                        | synthetic (PR #405) | real M9b (PR #414) | invariance |
                        |---------------------|--------------------|------------|
C1 multilingual_probe   |  PASS  (5/5 lang)   |  FAIL  (3/6 lang)  |  fragile   |
C2 register_collapse    |  PASS  (hits=0)     |  PASS  (hits=0)    |  robust    |
C3 motivation_8factor   |  PASS  (0.525)      |  PASS  (~0.55)     |  robust    |
C4 dream_stage_at_eval  |  PASS  (WAKE/1.0)   |  PASS  (WAKE/1.0)  |  robust    |
                        |---------------------|--------------------|------------|
AGGREGATE               |  4/4 ACHIEVED       |  3/4 FAIL          |  -1 cell   |
```

총 8 cell (4 criterion × 2 source) · PASS 7 / FAIL 1 · invariance robust 3 / fragile 1. fragile cell 1 개 = aggregate closure 전체 FAIL 결정 (4/4 → 3/4).

## § 3 C1 multilingual axis 의 fragility 분석

**spec (PR #398 `closure_auto_judge`)**: 5-lang per_lang_verdicts {ko, en, zh, ru, ja} 의 verdict 가 STRONG / PARTIAL 가 ≥ 4/5 면 PASS, 미만 FAIL. mixed lang 은 canonical 5-lang 표 외 추가 cell.

**synthetic (PR #405)** — `coffeshop_sim.hexa` 가 simulator 단계에서 5-lang 균일 verdict 합성 (ko STRONG, en/zh/ru/ja PARTIAL): 5/5 PASS by design.

**real M9b (PR #414)** — anima own session JSONL 추출 (1457 records / 1.07 MiB):
| lang | n_records | share | verdict |
|---|---|---|---|
| ko | 30 | 2.06% | PARTIAL |
| en | 325 | 22.30% | STRONG |
| mixed | 1102 | 75.63% | STRONG (canonical 외) |
| zh | 0 | 0% | **EMPTY** |
| ru | 0 | 0% | **EMPTY** |
| ja | 0 | 0% | **EMPTY** |

real 의 자연 분포 = **bimodal (ko/en) + mixed dominant**, zh/ru/ja 자연 출현 0. canonical 5-lang 표 기준 3/6 verdict (ko PARTIAL + en STRONG + mixed STRONG, zh/ru/ja EMPTY) → threshold ≥ 4 미달 → FAIL.

**failure mode**: real anima emit 의 자연 lang distribution 이 5-lang uniform synthesis 의 design 강제 와 분리 — synthetic 은 합성 단계에서 자동 충족, real 은 자연 corpus 분포 에 종속. 즉 framework 의 multilingual 기준 = synthetic-friendly · real-hostile 구조.

## § 4 C2 / C3 / C4 robust core 분석

**C2 register_collapse** (n_anima_register_hits_total < 4):
- synthetic PR #405: hits=0 (sim convention) → PASS.
- real M9b: 6-pattern regex sweep (`[role`, `you are anima`, `you are a helpful`, `페르소나`, `anima:`, `당신은 anima 입니다`) × 1457 records → tot_helper_dropped=0 → PASS.
- **robust 근거**: Principle #3 (NO PERSONA INJECTION) 가 anima session emit baseline 에 자연 통합 — register-free 가 default 상태, framework 가 그 default 를 검출. 데이터 source 변경에 invariant.

**C3 motivation_8factor** (motivation_score ≥ 0.30):
- synthetic PR #405: 8-factor avg 0.525067 (relevance / info_gap / curiosity / pain / coherence / originality / balance / dynamics) → PASS.
- real M9b: emit volume proxy 1457 / 6 window = 242.83 emit/window → 0.55 (보수 midpoint [0.40, 0.70]) → PASS.
- **robust 근거**: threshold (0.30) 가 활성 anima 의 emit 발생 baseline 보다 충분히 낮음. synthetic 의 정확 8-factor avg 와 real 의 volume proxy 가 유사 중대역 도달 — measurement protocol 분기 에도 invariant.

**C4 dream_stage_at_eval** (phi_envelope present):
- synthetic PR #405: WAKE / phi=1.0 → PASS.
- real M9b: active interactive emit session → WAKE / phi=1.0 default → PASS.
- **robust 근거**: WAKE 가 active emit 의 canonical default, P47 5-stage 의 안전 default 시점만 충족. 데이터 source 가 active session 이라는 가정 하 항상 PASS.

## § 5 후속 path 권고 — multi-lang gap 해소

| path | 설명 | cost | type |
|---|---|---|---|
| **P1** ckpt fire (option A) | Phase D 재발사 — real ckpt 의 multi-lang emit 측정, COFFESHOP scenario 90-min group-chat actual run | cost-bearing (runpod $30-60 추정) | empirical |
| **P2** multi-lang corpus 보강 | M3b/M3b' (사용자 보류) wiki extract 후 다시 fixture build, zh/ru/ja seed 확보 | $0 mac local | data |
| **P3** external model API cross-comparison | gpt/claude/qwen 의 multi-lang COFFESHOP scenario 응답 baseline 비교, 다른 model 의 자연 lang distribution 측정 | API token cost | comparative |
| **P4** threshold 조정 (design change) | 4/5 → 3/5 또는 lang-weighted (ko/en 우선, zh/ru/ja optional). framework spec 변경 path | $0 doc-only | design |

**default 권고**: P1 ckpt fire (option A) — Phase D 자체가 framework 의 real-data first cycle 이므로 framework limitation 의 직접 해소. P2 / P3 / P4 는 P1 대기 중 병행 가능.

## § 6 Honest C3

1. **real corpus single instance** — M9b PoC 1.07 MiB / 1457 records / 6 of 82 source files only. 잔여 76 files 의 multi-lang 분포 미측정, corpus expansion 후 fragile claim 재검증 필요.
2. **synthetic design 강제 명시** — PR #405 `coffeshop_sim.hexa` 가 5-lang verdict 를 simulator 단계에서 합성. C1 의 synthetic PASS = framework artifact (실제 multi-lang emit 측정 아님). 본 문서가 이 artifact 표면화.
3. **robust core claim 의 fragile evidence base** — C2/C3/C4 의 robust 분류 근거 = synthetic 1 instance + real 1 instance = 2-point 비교. ckpt-bearing fire 의 4-criterion 적용 데이터 부재 (P1 path 권고 의 이유).
4. **threshold (4/5) 의 reasonable choice 검증 path 미실시** — 4/5 가 design 선택, 3/5 / 5/5 alternative 의 비교 측정 없음. P4 path 의 design change 권고 정당성 미입증.
5. **framework limitation = real-data dependency** — 본 문서가 표면화한 한계 = framework 자체의 design fragility. C1 의 multi-lang 가정 (5-lang 자연 균일) 이 real anima emit 분포 (ko/en bimodal + mixed dominant) 와 mismatch — framework spec 의 reasonable scope 가 synthetic 위주 임을 명시적 surface.
6. **semantic mismatch (PR #414 C3 carry-over)** — M9b corpus = anima 1:1 USER turn emit, COFFESHOP = 90-min group-chat scenario. schema 재사용했지만 scenario 등가 아님. 본 문서의 robust/fragile 분류 도 이 semantic mismatch 위에서 도출.

## § 7 Cross-references

- **PR #393** — M9b PoC corpus (1.07 MiB / 1457 records / lang distribution 정량 source)
- **PR #398** — `closure_auto_judge.hexa` 4-criterion CLI spec
- **PR #405** — COFFESHOP simulator synthetic 4/4 PASS (robust/fragile cross-tab synthetic column)
- **PR #412** — BLOCKERS CLOSURE deferred marker (4 fire-blocked deferred + auto-unblock chain)
- **PR #414** — real measurement first instance (robust/fragile cross-tab real column, 본 문서 직접 source)
