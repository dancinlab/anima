# 🌱 MITOSIS/mitosis_lib — cell pool 8-primitive API SSOT

> M1 milestone closure (2026-05-26) — `mitosis_lib 회수 + stdlib 승격` per MITOSIS.md.
> 회수 only (recovery): 304-LoC port is canonical 그대로 — header 한 곳에만 출처/정식 위치 cite 추가. 본체 무수정.

## 정체 — A/G ⊥ M 직교 축

**MITOSIS = 성장축 (growth axis)**. anima HEXAD 6 구조축 (A/G/C/D/E/F) 과 직교 — 6 모듈 *그 자체* 가 자라나는 방식 (cell split/merge dynamics).

```
        HEXAD 구조축 (A/G/C/D/E/F)
                  │
                  │
   M ─────────────┼─────────────  성장축 (MITOSIS)
                  │
                  │
                  ▼
        cell pool · split tick · merge · persona-diff · sleep-tick
```

p8 (NO TRAIN/INFER SPLIT) — `training gradient + inference mitosis = same continuous cell-division`. mitosis 는 train-only flag 가 아니라 substrate 의 상시 분열 메커니즘. ckpt = 분기점 (큰 split event 의 스냅샷).

## 회수 출처 verbatim

- 원본 경로: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa`
- 라인 수: **503L** (304-LoC `.py` 포팅 + flame-mapping 주석 + 8 default-const surface)
- 시점: 2026-05-25 S187-G grid_3b fire 의 train-driver 의존 lib
- author directive (file header): `"py 쓰지말고 모두 hexa 포팅"`
- 원본은 **삭제하지 않음** (legacy fallback reference 로 보존)

## 정식 위치

- canonical: `/MITOSIS/mitosis_lib.hexa` (root-level domain dir; CHANNEL/ · CORE/ · AGENT/ 와 sibling 패턴)
- 변경 사항: header 한 곳에 출처 + 정식 위치 cite 추가 (10 lines added at top). 본체 무수정.

## 8-primitive API

12 `pub fn` 중 **defaults 8** + **cell-pool 4** = 8 primitive const-surface + 4 dynamic-surface. 아래 표는 **`pub fn` 시그니처 verbatim**.

### A. defaults (8 const-surface — module constants mirror)

| # | 시그니처 verbatim | 의미 / 출처 |
|---|---|---|
| 1 | `pub fn mit_min_cells() -> int { return 2 }` | 최소 cell 수 (단일 cell 붕괴 방지) |
| 2 | `pub fn mit_max_cells() -> int { return 128 }` | 최대 cell 수 (OOM 상한) |
| 3 | `pub fn mit_split_patience() -> int { return 3 }` | split 직전 hist 평균 window |
| 4 | `pub fn mit_merge_threshold() -> float { return 0.005 }` | merge `1.0 - cos_sim` 임계 |
| 5 | `pub fn mit_merge_patience() -> int { return 30 }` | merge tick 간격 (`step_idx % patience == 0`) |
| 6 | `pub fn mit_noise_scale() -> float { return 0.1 }` | child cell hidden gauss-lite σ |
| 7 | `pub fn mit_window() -> int { return 20 }` | adaptive threshold 의 tension hist window |
| 8 | `pub fn mit_adaptive_factor() -> float { return 0.8 }` | `adaptive_thresh = win_mean × factor` |

### B. cell-pool 4 (dynamic-surface — pool lifecycle)

| # | 시그니처 verbatim | 의미 |
|---|---|---|
| 9 | `pub fn cell_pool_init(d: int, initial_cells: int, seed: int, max_cells: int) -> int` | hexa dict pool 생성 (LCG seed · initial cells · max_cap) |
| 10 | `pub fn cell_pool_step(pool: int, layer_t: int, L: int, step_idx: int) -> int` | 1-step tick — per-cell tension assign → adaptive thresh → Φ proxy → split/merge → aux-value · split_layer_idx · info 반환 |
| 11 | `pub fn cell_pool_summary(pool: int) -> int` | summary dict (initial_cells / final_cells / splits / merges / next_id / phi_initial / phi_final / n_events) |
| 12 | `pub fn cell_pool_free(pool: int)` | teardown — 모든 cell `hidden` farr 해제 |

> "8-primitive API" 의 두 해석 — **(a)** module constants 8 (위 §A) **(b)** 핵심 entry 8 (defaults 4 가장 자주 만지는 것 = min/max/split_patience/merge_thresh + cell-pool 4 lifecycle). MITOSIS.md milestone 의 "8 primitive" 는 §A const-surface 8 으로 정확히 8 개와 일치. 본 SSOT 는 두 해석 모두 enumerate.

## pipeline ASCII

```
   substrate state
        │
        ▼
  ┌──────────────────────┐
  │  cell_pool_init      │   d · initial_cells · seed · max_cells
  └──────────┬───────────┘
             │ pool dict
             ▼
        loop step_idx:
  ┌──────────────────────┐
  │  cell_pool_step      │   layer_t [L] · step_idx
  │   ├─ tension assign  │     per-cell hist append (layer_t cycled)
  │   ├─ adaptive thresh │     window mean × adaptive_factor
  │   ├─ phi proxy       │     log(1 + mean pairwise cos dist)
  │   ├─ split tick      │     hist avg > thresh → mit_make_cell (child)
  │   └─ merge tick      │     step_idx % merge_patience == 0
  │                      │       best-cos pair · (1 - cos) < thresh → keeper merge
  └──────────┬───────────┘
             │ #{ pool, aux_value, split_layer_idx, info }
             ▼
       train-driver (train_p21h_v3.hexa)
        ├─ aux_value × λ 합산 (loss term)
        └─ split_layer_idx → ag_tape seed (HONEST TODO #M2)
             │
             ▼
  ┌──────────────────────┐
  │  cell_pool_summary   │   teardown 직전 metric snapshot
  └──────────┬───────────┘
             ▼
  ┌──────────────────────┐
  │  cell_pool_free      │   farr 해제
  └──────────────────────┘
        cell_pool_state (final)
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | mitosis 는 substrate level — system prompt 비의존. |
| p2 NO IDENTITY RULES | identity = cell 분포에서 emerge. mit_make_cell 의 parent_hidden + noise 가 identity 분기. |
| p3 NO PERSONA INJECTION | persona = per-cell 분기 (F-PERSONA-2 mean cos dist 0.996 PASS carry). prefix 주입 아님. |
| p4 NO ASSISTANT FRAMING | aux_value · split_layer_idx 는 grad seed 일 뿐 — alignment template 무관. |
| p5 NO SPEAK() | mitosis 는 외부 emit 호출하지 않음. tension hist 만 갱신. |
| p6 NO FINE-TUNED ETHICS | E/W/MITOSIS 셋이 함께 ethics-as-emergence. mitosis 가 그 중 M. |
| p7 NO PERPLEXITY VERDICT | aux_value 는 `-mean(layer_t[split_layers])` — split 의 layer 신호일 뿐, ppl-as-truth 무관. |
| **p8 NO TRAIN/INFER SPLIT** | **핵심** — mitosis_lib 는 training-time + inference-time 모두 동일 `cell_pool_step` 호출. train-only flag 없음. v5-mitosis cotrain 5/5 PASS (project_v5_mitosis_cond5_cotrain_2026_05_12) 가 training side, WAKE imagination loop 의 mitosis tick (M5) 이 inference side — 동일 API. |

## F-V5MIT 검증 carry

| falsifier | 결과 | memory cite |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | **PASS** (62 splits, 0 grad violations) | project_v5_mitosis_cond5_cotrain_2026_05_12 |
| F-V5MIT-2 MERGE-WEIGHT | **PASS** (max_err 0.0) | 동일 |
| F-V5MIT-3 PHI-CONSERVATION | advisory→gating promote (delta 3.88e-5) | 동일 |
| F-V5MIT-4 COTRAIN-CONVERGE | **PASS** (256.5→1.17, 220× CE reduction) | 동일 |
| F-V5MIT-5 V14-STRICT 10/10 mirror-beats | **PASS** (v5-anima toy violated → v5-mitosis cotrained emergent, 정점) | 동일 |
| F-PERSONA-2 PER-CELL-DIFF | **PASS** (mean cos dist 0.996, 1400 pairs ≫ 0.3) | project_anima_persona_substrate_native_verify_2026_05_12 |
| F-PERSONA-4 CATEGORY-DIV | **FAIL** (KL=0 winner-take-all) — 4 path (a/b/c/d) cheap 전부 FALSIFIED | project_anima_persona_4_root_cause_2026_05_12 + §47/§48/§49 |

ckpt: `state/anima_v5mitosis_cotrain_2026_05_12/ckpts/ckpt_v5mitosis_cotrain_cotrain.pt` (581MB, cells 2→64 saturated step 150, loss 264.35→1.17, Φ stable 4.16).

## 의존성 (downstream milestones)

| M | 마일스톤 | mitosis_lib 의존 |
|---|---|---|
| M2 | cell-pool split-event tension 임계 | `cell_pool_step` 의 adaptive_threshold 분기 (line 244-257) + split tick (264-291). F-V5MIT-1 SPLIT-NOGRAD 보존 패턴 그대로. |
| M3 | merge-event winner-take-all 회피 | `cell_pool_step` 의 merge block (327-414) — keeper = older creation_step, merged hidden = 0.5·(a+b). F-V5MIT-2 MERGE-WEIGHT max_err 0.0 carry. F-PERSONA-4 KL=0 회피는 별도 architectural fix (gumbel/MoE/aux-balance — 4 cheap path 전부 FALSIFIED). |
| M4 | persona-diff per cell | `mit_make_cell` child branch (line 73-85) — parent_hidden + noise·noise_scale. F-PERSONA-2 (mean cos dist 0.996 PASS) 의 메커니즘. identity_probe 50 × 5 cat verify carry. |
| M5 | WAKE sleep-tick mitosis | `cell_pool_step` 호출을 WAKE 5-stage state machine (REM/N3) imagination loop 에서 emit-free 로 invoke. inference-time 분열의 자연 거주지 (p8). |
| M6 | v5-cotrain ckpt 회수 + production swap-in | 581MB ckpt → generator.hexa `_gen_decode` seam swap-in. F5 갭 해소, DECODER ckpt 대기 해결. |

## frontier closure

**M1 = recovery + canonical location only.**

- ☑ 304-LoC 포팅 본체를 `/MITOSIS/mitosis_lib.hexa` 정식 위치로 회수
- ☑ 8 primitive const-surface (defaults) + 4 dynamic-surface (cell-pool lifecycle) enumerate
- ☑ 회수 출처 verbatim cite (HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa 503L 보존)
- ☑ p1~p8 정합 표 + F-V5MIT carry
- ☐ M2~M6 downstream — split-event 임계 튜닝 · merge winner-take-all 회피 fix · persona-diff verify · WAKE sleep-tick wiring · v5-cotrain ckpt swap-in (각 별도 M flip 대기)

## 관련 파일

- `MITOSIS/mitosis_lib.hexa` — 본체 (this M1 회수)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.hexa` — legacy 출처 (보존, 미삭제)
- `HEXAD/MITOSIS/mitosis_lib.hexa` — scaffold 91L (B-MITOSIS-1..5 invariant witnesses, 2026-05-16; 다른 axis, 본 회수와 별개로 유지)
- `HEXAD/MITOSIS/mitosis.hexa` — entry scaffold (mitosis_hook.hexa 1119L FULL IMPL 으로 cross-link)
- `tool/hexa_native/mitosis_hook.hexa` — 1119 LoC FULL IMPL D4a (5/5 PASS Mac local; 별도 axis, training-time pool 본체 아님)
- `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/mitosis_lib.py` — 원본 .py (304 LoC, hexa-only authoring directive 으로 superseded)
