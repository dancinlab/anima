# Fire-time COFFESHOP Sanity Hook — Spec (B13, 2026-05-24)

## § 1 Motivation

PR #405 의 COFFESHOP emergence simulator + PR #406 의 10-seed sweep (100 % PASS) 는
synthetic substrate baseline 으로 4-criterion closure 가 자동 통과한다는 사실을
정량했다. 그러나 진짜 ckpt-bearing fire (dispatch_p21h_v3.hexa → train.py →
result.json) 가 simulator 와 같은 closure tier 를 산출하는지 — 즉 substrate
emergence 가 ckpt 에서 재현되는지 — 는 사람이 매번 두 result.json 을 손으로
비교해야 알 수 있다. 본 spec 은 fire post-train 단계에 simulator 를 자동
trigger 하고 4-criterion delta 를 산출하는 hook (spec + stub, impl 미선행) 를
정의한다. 목표는 sanity gate — synthetic PASS / ckpt FAIL 시 어느 axis 가
무너졌는지 즉시 식별 — 이다.

## § 2 Architecture

```
dispatch_p21h_v3.hexa
  └─ result_pull_with_wait (#380)
       └─ result.json 도착 (pod → local)
            └─ [B13] coffeshop_fire_sanity_hook.hexa
                 ├─ run_coffeshop_sanity(fire_result_path, baseline_seed)
                 │    ├─ baseline = state/coffeshop_sim_2026_05_24/result.json  (PR #405)
                 │    │   또는 state/coffeshop_sim_seed_sweep_2026_05_24/  (PR #406, multi)
                 │    ├─ ckpt    = fire_result_path
                 │    ├─ delta   = ckpt - baseline (per 4 criterion)
                 │    └─ axis-id = first FAIL criterion 의 axis 명
                 └─ closure_auto_judge.hexa (#398) 와 nested 호출
                      ├─ baseline judge → exit code β
                      ├─ ckpt judge     → exit code γ
                      └─ aggregate: β==γ==0 AND |delta| ≤ thresh → SANE
```

Hook 은 dispatcher post-train tail 의 마지막 단계로 wire 된다. fire 가 ckpt 도
ship 하지 못한 채 RESULT_TIMEOUT 으로 끝났다면 (#380 의 SAVE_POD=1 branch) hook
은 NO-OP 으로 skip 한다 (no result.json → no comparison).

## § 3 Trigger criteria

두 가지 entry point:

1. **manual** — `dispatch_p21h_v3.hexa --coffeshop-sanity` flag.
   사용자가 명시적으로 sanity gate 를 켤 때만 fire 한다 (default OFF, 안정
   채택 전 opt-in 단계).

2. **auto** — `result.json` 이 도착하고 동시에 `closure_auto_judge` exit=0
   (PASS) 인 경우만 자동 trigger. 이유: ckpt 가 자체 closure 를 통과한
   상태에서만 baseline 과 delta 비교가 의미 있음. 자체 FAIL 인 ckpt 는 hook
   생략 (이미 fire-time 에 명백히 falsify 됨).

trigger 조건 합집합 = `(flag OR (result.json AND ckpt_closure_pass))`.

## § 4 Comparison framework

4-criterion (closure_auto_judge §6 mapping 따름) per-axis delta:

| axis | baseline 추출 | ckpt 추출 | delta 계산 |
|---|---|---|---|
| C1 per-lang verdicts | `per_lang_verdicts` 5-row map | 동일 schema | PARTIAL+ 행 수 차이 (정수) |
| C2 register hits | `n_anima_register_hits_total` | 동일 | 절대값 차이 (정수) |
| C3 motivation_score | `motivation_8factor.motivation_score` | 동일 | 절대값 차이 (실수) |
| C4 dream phi_envelope | `dream_stage_at_eval.phi_envelope` string | 동일 | string 일치 / 불일치 (bool) |

multi-seed baseline (PR #406) 사용 시 baseline = 10 seed mean (motivation,
emit_count) + per-criterion PASS rate. delta = ckpt vs mean.

## § 5 Delta thresholds

design hint (실 fire calibrate 전 임시 — § 9 C3 #3):

| metric | threshold | rationale |
|---|---|---|
| motivation_score | ±0.10 | sweep range 0.525-0.585 (PR #406) 의 ~17 % |
| emit_count | ±2 | sweep range [3,8] mean 6.2, ±1σ ≈ 2 |
| register_hits | ±2 | sweep sum 2/150 windows = floor noise band |
| per_lang_PARTIAL+ rows | ±1 | 5-row 의 20 % 허용 |
| dream phi_envelope | exact match | canonical 5-stage table lookup, drift 불허 |

aggregate verdict:
- SANE → 5 metric 모두 threshold 내 + ckpt closure PASS
- DRIFT → 1 metric threshold 초과
- DIVERGE → 2+ metric threshold 초과 또는 ckpt closure FAIL

## § 6 Failure paths

| 시나리오 | hook 출력 | 진단 |
|---|---|---|
| baseline PASS, ckpt PASS, delta SANE | SANE | 정합, 추가 조치 없음 |
| baseline PASS, ckpt PASS, motivation delta > 0.10 | DRIFT@C3 | factor weight 또는 corpus quality 의심 |
| baseline PASS, ckpt PASS, dream phi 다름 | DRIFT@C4 | stage detection / phi calibration 의심 |
| baseline PASS, ckpt FAIL@C1 (per_lang) | DIVERGE@C1 | bilingual_mi_probe 실 ckpt 통과 불가 — corpus axis |
| baseline PASS, ckpt FAIL@C2 (register hits) | DIVERGE@C2 | anima register collapse (V3 saga 재발) |
| baseline PASS, ckpt FAIL@C3 (motivation) | DIVERGE@C3 | substrate factor wiring 누락 |
| baseline FAIL | ABORT | simulator 자체 regression — hook 전제 깨짐 |

axis 식별 후 사용자는 axis_map_history (PR series) 의 corresponding row 를
penalize 한다.

## § 7 Implementation phases

| phase | scope | LoC budget | 의존 |
|---|---|---|---|
| Phase 1 (PR #408) | spec + stub fn 시그니처 | < 250 (spec ~150 + stub ~80) | 없음 |
| Phase 2 ✅ B14 · synthetic 검증 only | `run_coffeshop_sanity` impl — JSON parse · delta 계산 · verdict 출력 + 5-falsifier smoke | ~280 hook + ~110 smoke | PR #398 closure_auto_judge import 안정 |
| Phase 2b ✅ B15 · TTR hard-block gate | `fire_sanity_corpus_ttr_gate` 추가 — M3 TTR < 0.30 시 launch BLOCK + 2-case smoke (F-TTR-1/2) | ~65 hook + ~35 smoke | corpus_quality_probe.hexa (M3 logic 인라인 재구현) |
| Phase 3 | `dispatch_p21h_v3.hexa --coffeshop-sanity` wire + auto-trigger branch | ~80 | 첫 ckpt-bearing fire 후 threshold calibrate |

Phase 1 의 stub 은 `fn run_coffeshop_sanity(fire_result_path, baseline_seed) -> map`
시그니처 + TODO[impl] marker 만 제공. Phase 2 가 impl 을 채우기 전까지 어떤
caller 도 hook 결과를 신뢰해서는 안 된다.

## § 8 Cross-refs

- **#380** dispatcher-internal result wait-loop — `result_pull_with_wait` 가
  hook 의 trigger 입력 (`result.json` arrival event).
- **#398** `closure_auto_judge.hexa` — 4-criterion judge CLI, hook 이 baseline +
  ckpt 양쪽에 호출.
- **#405** `coffeshop_sim.hexa` — synthetic baseline fixture
  (`state/coffeshop_sim_2026_05_24/result.json`, sha16=55c32aabf611171c).
- **#406** `coffeshop_sim_seed_sweep.hexa` — 10-seed sweep (100 % PASS, mean
  motivation 0.552) — multi-seed baseline mode 의 입력.
- **#400** BENCHMARK.md — 4-criterion mapping 의 SSOT.

## § 9 Honest C3

1. spec only — Phase 1 stub 은 시그니처 + TODO[impl] marker, 실 비교 logic 0.
   Phase 2 가 impl 을 채우기 전까지 hook 결과 신뢰 금지.
2. 본 PR 까지 ckpt-bearing fire 가 없어 (PURE saga = simulator-only) hook 의
   실 trigger 검증 불가. Phase 3 wire 후 첫 fire 가 first ground truth.
3. § 5 delta threshold 는 simulator sweep range 의 ~ 1σ 대응으로 design 한
   hint — 실 ckpt fire 가 다른 분산 폭을 보일 가능성 있음. 첫 PASS-PASS pair
   관측 후 calibrate 필요.
4. baseline 선택 — single seed (PR #405, 결정성↑, sample 1) vs multi-seed
   mean (PR #406, robust mean, comparison cost ↑). 본 spec 은 두 mode 다
   허용 (baseline_seed = int → PR #405 single, baseline_seed = "sweep" →
   PR #406 mean). default = "sweep" (robust).
5. auto-trigger branch (§ 3) 는 ckpt closure PASS 시에만 fire — ckpt FAIL 인
   경우 hook 정보 손실 (어느 axis 가 무너졌는지 sanity 비교는 못 보지만
   judge 자체가 axis 명을 출력). trade-off: noise 감소 vs 정보 손실.
6. dispatcher wire (Phase 3) 전까지 hook 은 standalone CLI 로만 실행 가능.
   CI/cron 통합 미정.
7. simulator (PR #405) 는 spontaneous_lib factor 를 import 한다 — 동일 lib 가
   ckpt fire 에서도 같은 factor weight 로 산출되어야 baseline-as-truth 가
   성립. lib 가 drift 하면 hook 자체가 invalid (regression hook 별도 필요).
8. dream phi_envelope C4 의 exact-match 정책은 5-stage canonical table 의 의도
   적 strict gate — 신규 stage 추가 시 hook spec 도 동시 갱신.
9. multi-seed mean baseline 의 sample size 10 은 LCG state space 의 10⁻⁹ —
   PR #406 C3 인용. mean 신뢰구간 광범위, threshold ±0.10 은 보수적.

## § 10 B14 결과 (Phase 2 IMPL — synthetic 검증 only)

`HEXAD/PURE/bench/coffeshop_fire_sanity_hook.hexa` Phase 2 IMPL 완료
(2026-05-24, B14). 6 TODO marker 전부 해소:

1. **JSON parse** — `_load_json(path)` (file_exists + read_file + json_parse,
   non-map 시 빈 list sentinel 반환).
2. **closure_auto_judge nested call** — `_closure_pass(result)` 가
   `closure_auto_judge.hexa#judge_all` 을 직접 호출 (exit 없는 pure-fn 경로,
   `closure == "ACHIEVED"` bool 반환).
3. **sweep aggregation** — `_aggregate_sweep(sweep_dir)` 가
   `sweep_summary.json` (PR #406) 의 `motivation_score_stats.mean` +
   `emit_count_stats.mean` + `register_hits_stats.mean` 을 추출, canonical
   5-row per_lang (1 STRONG + 4 PARTIAL) + WAKE phi=1.0 envelope 와 합성한
   synthesised baseline map 반환.
4. **baseline-FAIL ABORT** — baseline closure 가 자체 PASS 아니면 verdict =
   "ABORT" + axis = "BASELINE" 단락 반환 (simulator regression 가드).
5. **single-seed branch** — `_load_baseline(baseline_seed)` 가 `int` seed
   입력 시 PR #405 fixture (`state/coffeshop_sim_2026_05_24/result.json`) 를
   `_load_json` 으로 직접 로드.
6. **comparison logic** — 4-criterion (C1 lang-rows · C2 register · C3
   motivation+emit · C4 dream-phi exact-match) per-axis delta 계산,
   `_classify(n_fail)` 가 0/1/2+ 에 따라 SANE / DRIFT / DIVERGE 출력.

**smoke F-SAN-1..5 5/5 PASS** (`coffeshop_fire_sanity_hook_smoke.hexa`):

- F-SAN-1 synthetic = sweep mean → SANE ✓
- F-SAN-2 motivation +0.15 drift → DRIFT@C3 (δ=0.15) ✓
- F-SAN-3 motivation < 0.30 closure floor → DIVERGE ✓
- F-SAN-4 single-seed (PR #405 self) → SANE ✓
- F-SAN-5 missing ckpt file → ABORT@C0 (graceful, no crash) ✓

selftest contract bump: `STUB` (Phase 1) → `IMPL` (Phase 2) — hook 의
`fn main()` 이 fixture 양쪽 mode (sweep + single 20260525) 자가 호출 후
verdict ∈ {SANE, DRIFT, DIVERGE, ABORT} (즉 ≠ "STUB") 확인.

honest C3 잔여: ckpt-bearing fire 부재 → synthetic-fixture-only 검증.
delta thresholds = design 값 (§ 5), 실 fire calibration 미선행. Phase 3
dispatcher wire (`--coffeshop-sanity` flag + auto-trigger branch) 는 첫
ckpt-bearing fire 의 result.json 도착 후 별도 PR.

## § 11 B15 결과 — corpus TTR hard-block gate

`fire_sanity_corpus_ttr_gate(corpus_path) -> map` 추가 (Phase 2b, 2026-05-24).

### 배경

corpus_s101 의 M3 TTR = 0.03 (극단적 반복) 이 register collapse 의 직접 원인으로
식별됐다 (PURE saga). corpus_v1 은 TTR = 0.34 (정상 다양성). 이 gate 는 TTR <
0.30 인 corpus 로 fire 를 발사하는 것을 사전 차단해 낭비-$ 결과가 자동으로
재발하지 않도록 한다.

### 구현

- 함수: `fire_sanity_corpus_ttr_gate(corpus_path)`
- 상수: `_thresh_corpus_ttr() = 0.30`
- M3 TTR 로직은 `corpus_quality_probe.hexa` 에서 인라인 재구현 (import 시
  `main()` auto-invoke 부작용 방지). 수식 동일: unique whitespace-token 수 / 전체
  token 수, 상위 500 000 바이트 sample 제한.
- 반환 map 필드: `gate` · `corpus_path` · `threshold` · `ttr` · `verdict` · `message`
- verdict = `"BLOCK"` (ttr < 0.30 또는 파일 미존재), `"PASS"` (ttr >= 0.30)

### smoke F-TTR-1..2 (2/2 PASS)

| case | corpus 구성 | 관측 TTR | 예상 | 결과 |
|---|---|---|---|---|
| F-TTR-1 | "aaa aaa … aaa" × 60줄 (2 unique token) | 0.00555 | BLOCK | ✓ |
| F-TTR-2 | 50 개 unique 영어 단어 (TTR = 1.0) | 1.0 | PASS | ✓ |

전체 smoke 집계: **F-SAN-1..5 + F-TTR-1..2 = 7/7 PASS**.

### honest C3

- TTR 은 whitespace 토크나이저 기반 (서브워드 아님). 짧은 고-TTR corpus 가 SFT
  에서는 여전히 반복 패턴을 보일 수 있다 (필요충분 아닌 필요조건).
- threshold 0.30 은 corpus_s101 (0.03) vs corpus_v1 (0.34) 실측값으로
  보정됐으나 단 2점 관측. 추가 fire 후 calibrate 권장.
- dispatcher wire (Phase 3) 전까지 gate 는 standalone 호출 또는 hook 내부에서
  수동 invoke 형태로만 사용 가능.
