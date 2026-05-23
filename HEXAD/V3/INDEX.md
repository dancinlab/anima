# HEXAD/PURE INDEX — V3 saga rebrand · session-3 누적 (2026-05-23)

## Background

HEXAD/V3 lane 은 2026-05-23 commit `a1e555ad4` 에서 HEXAD/PURE 로 rebrand 되었다 (디렉터리/문서 동기, lane semantics 보존). pure-HEXAD substrate (corpus 외 fallback axis exploration) 의 fan-out 결과 — AXIS_MAP 7-axis ranking · BUG_POSTMORTEM env-var saga · R8 base warm-init · R8c diagnostic probe — 가 누적되며 session-3 분량이 9 문서로 확장되었다. 본 INDEX 는 그 TOC + reading-order + open-question 을 1 회독 가능한 형태로 압축한다. 이 파일이 main 에 land 될 시점에는 디렉터리 또한 `HEXAD/PURE/` 로 옮겨지며, 본 INDEX 의 ASCII tree 와 reference 들이 그 최종 상태 기준으로 작성되어 있다 (현 branch 는 pre-rename `HEXAD/V3/` 에 위치하나 rebrand 후 `HEXAD/PURE/INDEX.md` 로 자연 이동).

## Document tree

```
HEXAD/PURE/
├── INDEX.md               (this doc)
├── AXIS_MAP.md            (original 7-axis ranking)
├── AXIS_MAP_RESULTS.md    (PR #206, 3/7 partial)
├── AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md  (this cycle stack)
├── AXIS_MAP_BUG_POSTMORTEM.md  (PR #211, env-var concat saga)
├── AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md  (this cycle stack)
├── AXIS_R8_BASE_WARM_INIT.md   (PR #214, R8 4-candidate spec)
├── AXIS_R8_UPDATE_CLUSTER_FINDING_2026_05_23.md  (this cycle stack)
├── AXIS_R8C_DIAGNOSTIC_PROBE.md  (PR #224, 5-cell protocol)
└── AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md   (this cycle stack)
```

## Document role table

| doc | role | status | PR # | verdict |
|---|---|---|---|---|
| `AXIS_MAP.md` | original 7-axis ranking spec (A~G fallback lanes) | landed (main) | — | spec |
| `AXIS_MAP_RESULTS.md` | partial fan-out results, 3/7 axes measured | open | #206 | 3/7 partial |
| `AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md` | 5/7 + 2 partial 으로 확장 (this cycle stack) | open | #206 stack | 5/7 + 2P |
| `AXIS_MAP_BUG_POSTMORTEM.md` | env-var concat saga chronology + root-cause | open | #211 | postmortem closed |
| `AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md` | LangBalancedSampler memory leak addendum (this cycle) | open | #211 stack | E OOM identified |
| `AXIS_R8_BASE_WARM_INIT.md` | R8 4-candidate spec (R8a/b/c/d warm-init recipes) | open | #214 | spec |
| `AXIS_R8_UPDATE_CLUSTER_FINDING_2026_05_23.md` | cluster X/Y/Z + cell-1 FALSIFIED 결과 (this cycle) | open | #214 stack | cell-1 FALSIFIED |
| `AXIS_R8C_DIAGNOSTIC_PROBE.md` | 5-cell ablation protocol | open | #224 | spec |
| `AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` | 3-cell 축소 (head_g cell-1 SKIP, this cycle) | open | #224 stack | 3-cell ready |
| `eval/multilingual_probe.hexa` (F8) | eval harness — strip parity, whitespace-only → EMPTY | open | #263 | F8 strip fixed |
| `AXIS_MAP.md` (F4 amendment) | closure rejection criterion pre-declaration (F4) | open | #264 | criterion declared |
| `launchers/_common.hexa` + `ENV_CONTRACT.md` | launcher SSOT skeleton + env-var contract | open | #265 | skeleton landed |

## Reading order (recommended)

| path | 질문 | 순서 |
|---|---|---|
| A. "What is this?" | lane 개요/현주소 | `AXIS_MAP` → `AXIS_R8_BASE_WARM_INIT` → `AXIS_R8C_DIAGNOSTIC_PROBE` |
| B. "What happened?" | saga 시간순 | `AXIS_MAP_BUG_POSTMORTEM` (+ E OOM addendum) → `AXIS_MAP_RESULTS` (+ 5/7 UPDATE) → `AXIS_R8_UPDATE_CLUSTER_FINDING` |
| C. "What's next?" | 다음 fire | `AXIS_R8C_PROBE_UPDATE_3_CELL` ($0.25 fire) → R8 ranking (R8a Qwen target match 후보) |

## Open questions

| # | question | dependent doc |
|---|---|---|
| 1 | R8c cell-2 (noise) 와 cell-3 (n_kv_head) 중 어느 것이 init_CE 14+ 천장의 dominant factor 인가? | `AXIS_R8C_PROBE_UPDATE_3_CELL` |
| 2 | cluster Y (B/F) 의 "aux-loss-lowers-init-CE" 가설은 진정한 effect 인가 noise 인가? | `AXIS_R8_UPDATE_CLUSTER_FINDING` |
| 3 | R8a Qwen target-match (1.5B keep) 가 fresh-3B 대신 production 경로가 될 것인가? | `AXIS_R8_BASE_WARM_INIT` |
| 4 | LangBalancedSampler memory leak 의 진짜 누수 지점은 어디 (sampler 자체 vs. dataset cache)? | `AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23` |
| 5 | 5/7 + 2 partial fan-out 에서 미측정 2 lane (open) 은 R8 cluster 결과로 priority 하향될 것인가? | `AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23` |

## Cross-reference

| family | doc | role |
|---|---|---|
| LORA | `HEXAD/LORA/SAGA_SESSION3.md` | session-3 LORA saga master timeline (cross-lane) |
| cross-saga | `HEXAD/WAVES_MATRIX.md` | wave × lane cross-saga master table |
