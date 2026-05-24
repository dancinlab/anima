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
| Phase 1 (본 PR) | spec + stub fn 시그니처 | < 250 (spec ~150 + stub ~80) | 없음 |
| Phase 2 | `run_coffeshop_sanity` impl — JSON parse · delta 계산 · verdict 출력 | ~250 | PR #398 closure_auto_judge import 안정 |
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
