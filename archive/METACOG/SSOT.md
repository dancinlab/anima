# 🪞 METACOG/metacog_lib — 자기 거울 self-audit primitives SSOT

> M1 milestone closure (2026-05-28) — `metacog_lib 회수 + stdlib 승격` per METACOG.md.
> bench/axis_metacog/bench.hexa (PR #1139, 5/5 round-trip 🟢 PASS) 의 5-tier verdict
> taxonomy + 30-emit binarize primitives 를 PURE wrapper 로 회수.

## 정체 — METACOG axis

**METACOG = 자기 거울 substrate self-audit**. p1~p8 정합 self-audit 의 측정 surface ·
BRIDGE AND-gate(emit 결정) 위의 메타 결정 layer. 본 lib 는 short-window emit history
를 5-tier 로 라벨링 (ROBUST / SMALL-N / INVERSE / AMBIG / ALL-FAIL) — small-n
artifact 자동 검출 입증 (bench round-trip 5/5).

## 회수 출처 verbatim

- 원본 경로: `bench/axis_metacog/bench.hexa` (PR #1139 land)
- 핵심 fn: `analyze_probe_table` (verdict_code) + `binarize_emits` (window rate)
- 5-tier code: ROBUST(1) GREEN · SMALL-N(2) RED · INVERSE(3) ORANGE · AMBIG(4) YELLOW · ALL-FAIL(5) RED
- 시점: 2026-05-28 M1 lib promotion
- 본체 무수정 — `mc_` prefix wrapper 만 추가 (g61 stdlib collision 회피)

## 11 pub primitives API

| # | 시그니처 | 의미 / cite |
|---|---|---|
| 1 | `pub fn mc_all_pass(passes: list) -> int` | every window PASS → 1 else 0 |
| 2 | `pub fn mc_all_fail(passes: list) -> int` | every window FAIL → 1 else 0 |
| 3 | `pub fn mc_is_small_n_artifact(passes: list) -> int` | w0 PASS only, 나머지 FAIL → 1 |
| 4 | `pub fn mc_is_inverse_artifact(passes: list) -> int` | w0 FAIL only, 나머지 PASS → 1 |
| 5 | `pub fn mc_count_pass(passes: list) -> int` | Σ passes |
| 6 | `pub fn mc_verdict_code(passes: list) -> int` | 5-tier code 1..5 |
| 7 | `pub fn mc_verdict_label(code: int) -> string` | code → ROBUST / SMALL-N-ARTIFACT / ... |
| 8 | `pub fn mc_verdict_tier(code: int) -> string` | code → GREEN / RED / ORANGE / YELLOW |
| 9 | `pub fn mc_window_pass_rate(emits, lo, hi) -> float` | Σ(emits[lo..hi]) / (hi - lo) |
| 10 | `pub fn mc_binarize_emits(emits: list) -> list` | 30-emit → 4-window [1/0,1/0,1/0,1/0] |
| 11 | `pub fn mc_analyze_probe_table(emits: list) -> int` | full pipeline (emits → verdict code) |

## pipeline ASCII

```
   emit history (size 30)
        │
        ▼
  ┌──────────────────────┐
  │  mc_binarize_emits   │   4 disjoint windows (7/7/8/8)
  │   ├─ window_pass_rate │     Σ(passes[lo..hi]) / (hi - lo)
  │   └─ threshold 0.5    │     rate >= 0.5 ? 1 : 0
  └──────────┬───────────┘
             │ passes = [b0,b1,b2,b3]
             ▼
  ┌──────────────────────┐
  │  mc_verdict_code     │   priority: ROBUST > ALL-FAIL > SMALL-N > INVERSE > AMBIG
  │   ├─ mc_all_pass     │     [1,1,1,1] → 1 GREEN
  │   ├─ mc_all_fail     │     [0,0,0,0] → 5 RED
  │   ├─ mc_is_small_n   │     [1,0,0,0] → 2 RED
  │   ├─ mc_is_inverse   │     [0,1,1,1] → 3 ORANGE
  │   └─ default         │     non-monotone → 4 YELLOW
  └──────────┬───────────┘
             │ code ∈ {1,2,3,4,5}
             ▼
       label + tier (str)
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | emits list 만 입력, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 — pure verdict taxonomy ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 — list/int/string 입출력 ✓ |
| p4 NO ASSISTANT FRAMING | alignment template 무관 ✓ |
| p5 NO SPEAK() | read-only analyzer, 외부 emit 호출 0 ✓ |
| p6 NO FINE-TUNED ETHICS | weight update 0 ✓ |
| p7 NO PERPLEXITY VERDICT | verdict = passes-bitmap deterministic ✓ |
| p8 NO TRAIN/INFER SPLIT | 동일 fn 이 train/infer 양쪽 사용 ✓ |

## bench round-trip carry

| scenario | emits → passes | expected_code | label |
|---|---|---|---|
| S1-ROBUST | [1,1,1,1] | 1 | GREEN ROBUST |
| S2-SMALL-N | [1,0,0,0] | 2 | RED SMALL-N-ARTIFACT |
| S3-INVERSE | [0,1,1,1] | 3 | ORANGE INVERSE-ARTIFACT |
| S4-AMBIG | [1,0,1,0] | 4 | YELLOW AMBIGUOUS |
| S5-ALL-FAIL | [0,0,0,0] | 5 | RED ALL-FAIL |

Round-trip 5/5 + small-n-artifact TP=1/1 FP=0/4 (PR #1139 verdict).

## 의존성 (downstream milestones)

| M | 마일스톤 | metacog_lib 의존 |
|---|---|---|
| M2 | substrate self-audit hook | `mc_analyze_probe_table` 를 WAKE.daemon N tick 마다 호출 (audit verdict 기록) |
| M3 | p1~p8 cross-product | `mc_verdict_code` 를 각 p 별 runtime audit 의 verdict reducer 로 사용 |
| M4 | cross-bench inject | F-PERSONA-4 (#1130) + F-M4B-FIRE-3 (#1133) 등 falsifier 에 `mc_analyze_probe_table` 적용 |

## frontier closure

**M1 = PURE lib promotion + canonical location only.**

- ☑ 11 pub primitives 회수 (`mc_` prefix g61 collision 회피)
- ☑ 5-tier verdict taxonomy 보존 (round-trip 5/5 carry)
- ☑ p1~p8 정합 표
- ☑ smoke (`metacog_lib_smoke.hexa`) 5+ invariant — 회수 round-trip 검증
- ☐ M2~M4 downstream — WAKE inject · principle runtime · cross-bench (각 별도 M flip 대기)

## 관련 파일

- `METACOG/metacog_lib.hexa` — 본체 (this M1 회수)
- `METACOG/metacog_lib_smoke.hexa` — invariant smoke
- `bench/axis_metacog/bench.hexa` — 원본 출처 (PR #1139)
- `bench/axis_metacog/README.md` · `result.json` · `run.log` — verdict artifacts (보존)
