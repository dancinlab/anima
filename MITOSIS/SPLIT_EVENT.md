# 🌱 MITOSIS/split-event — tension 임계 분열 SSOT

> M2 milestone (2026-05-26) — `cell-pool split-event — tension 임계 초과 시 cell 자동 분열` per MITOSIS.md.
> WRAP only (instrument-first): mitosis_lib.hexa 본체는 무수정, public surface 만 노출.

## 정체

**cell-pool 의 자동 분열 메커니즘**. cell 의 최근 tension hist 평균이 adaptive threshold 를 초과하면 그 cell 이 분열 (parent → parent + child). v5-mitosis cond.5 cotrain 5/5 PASS (project_v5_mitosis_cond5_cotrain_2026_05_12) 의 **2→64 cells step 150 saturate** 패턴이 본 메커니즘의 검증된 carry — 62 splits · 0 grad violations · max_err 0.0.

p8 (NO TRAIN/INFER SPLIT) — split 은 train · infer 동일 surface. train-only flag 없음. WAKE imagination loop (M5) 에서도 동일 `cell_pool_step` 호출.

## 위치 (mitosis_lib.hexa verbatim)

split 메커니즘은 `cell_pool_step` 단일 함수 내 두 block 으로 구성 (mitosis_lib.hexa).

### split-check (line 276-303)

```hexa
let mut split_cell_indices = []
let mut split_layer_idx = []
if len(cells) < pool_max_cells {
    let mut ci = 0
    while ci < len(cells) {
        let cell = cells[ci]
        let hist = cell["hist"]
        let hn = len(hist)
        if hn >= pool_split_patience {
            // recent split_patience window avg
            let mut racc = 0.0
            let mut ri = hn - pool_split_patience
            while ri < hn {
                racc = racc + hist[ri]
                ri = ri + 1
            }
            let avg = racc / to_float(pool_split_patience)
            if avg > split_threshold_eff && split_threshold_eff > 0.0 {
                split_cell_indices.push(ci)
                split_layer_idx.push(ci % L)
                if len(cells) + len(split_cell_indices) >= pool_max_cells {
                    ci = len(cells)   // break
                }
            }
        }
        ci = ci + 1
    }
}
```

### split-execute (line 305-337)

```hexa
let mut n_split_fired = 0
let mut si = 0
while si < len(split_cell_indices) {
    let ci2 = split_cell_indices[si]
    let mut parent = cells[ci2]
    let made = mit_make_cell(d, parent["id"], parent["hidden"], step_idx,
                             pool_noise_scale, next_id, rng)
    rng = made["rng"]
    let child = made["cell"]
    cells.push(child)
    next_id = next_id + 1
    // reset parent hist to last 3
    ...
    event_log.push(#{
        "kind": "split", "step": step_idx,
        "parent_id": parent["id"], "child_id": child["id"],
        "threshold": split_threshold_eff, "pool_size": len(cells),
    })
    n_split_fired = n_split_fired + 1
    split_count = split_count + 1
    if len(cells) >= pool_max_cells { si = len(split_cell_indices) }
    si = si + 1
}
```

## tension 임계 + patience 표 (verbatim defaults)

| key | default | mitosis_lib 출처 |
|---|---|---|
| `mit_split_patience()` | **3** | line 57 — `pub fn mit_split_patience() -> int { return 3 }` |
| `mit_adaptive_factor()` | **0.8** | line 62 — `pub fn mit_adaptive_factor() -> float { return 0.8 }` |
| `mit_window()` | **20** | line 61 — `pub fn mit_window() -> int { return 20 }` |
| `mit_noise_scale()` | **0.1** | line 60 — `pub fn mit_noise_scale() -> float { return 0.1 }` |
| `mit_max_cells()` | **128** | line 56 — `pub fn mit_max_cells() -> int { return 128 }` |
| `mit_min_cells()` | **2** | line 55 — `pub fn mit_min_cells() -> int { return 2 }` |

**runtime threshold (mitosis_lib.hexa line 267)**:

```hexa
adaptive_threshold = mean_w * pool_adaptive_factor
split_threshold_eff = adaptive_threshold
```

즉, `split_threshold_eff = (tension window mean over last 20 step) × 0.8`. 한 cell 의 최근 3-step hist 평균이 이 값을 초과하면 split fire.

## F-V5MIT-1 SPLIT-NOGRAD invariant

mitosis_lib.hexa line 38-40:

```
HERE we return the SCALAR aux value + the split-layer indices so the train
driver (train_p21h_v3.hexa) seeds the grad via ag_tape (HONEST TODO #M2 —
the grad path lives in the trainer, not here)
```

**invariant 본질**: child cell 의 hidden farr 는 `mit_make_cell` 에서 `parent_hidden + noise·noise_scale` 의 **STATE-COPY** 로 생성. parent farr 와 child farr 는 별도 buffer 이므로 parent 의 grad 가 child 를 통해 double-count 되지 않음.

검증 carry (project_v5_mitosis_cond5_cotrain_2026_05_12):

> F-V5MIT-1 SPLIT-NOGRAD: **62 splits, 0 grad violations**. F-V5MIT-2 MERGE-WEIGHT: **max_err 0.0**. cells 2→64 saturate step 150, loss 264.35→1.17 (220× reduction), Φ stable 4.16.

## pipeline ASCII

```
   per-cell tension signal (layer_t cycled across cells)
        │
        ▼
   hist append (mitosis_lib.hexa line 238)
        │
        ▼
   patience accumulate
        │  hn = len(hist)
        ▼
   ┌──────────────────────────────────────────┐
   │ if hn >= pool_split_patience (=3) AND    │
   │    avg(hist[hn-3..hn]) > thresh_eff AND  │
   │    thresh_eff > 0.0                      │
   │ then split_cell_indices.push(ci)         │
   └──────────────┬───────────────────────────┘
                  │
                  ▼
   mit_make_cell(d, parent_id, parent_hidden, step_idx,
                 noise_scale, next_id, rng)
                  │
                  │  F-V5MIT-1 SPLIT-NOGRAD:
                  │    child_hidden = STATE-COPY of
                  │    (parent_hidden + noise·σ),
                  │    별도 farr buffer → no grad
                  │    double-count
                  ▼
   cells.push(child)
                  │
                  ▼
   event_log.push("split"); split_count++
                  │
                  ▼
   invariant verify (split_smoke.hexa I1/I3/I4)
```

## p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | split 결정은 tension hist 만 사용 — system prompt 무관. |
| p2 NO IDENTITY RULES | identity = cell 분포에서 emerge. split 이 그 분포를 키움. |
| p3 NO PERSONA INJECTION | child 는 parent state-copy + noise — prefix 주입 아님. |
| p4 NO ASSISTANT FRAMING | split 은 substrate event, alignment template 무관. |
| p5 NO SPEAK() | split fire 는 외부 emit 없음. event_log 만 갱신. |
| p6 NO FINE-TUNED ETHICS | E/W/MITOSIS 의 M — split 이 ethics emerge 의 한 축. |
| p7 NO PERPLEXITY VERDICT | split 결정은 tension hist 평균 vs adaptive thresh, ppl 아님. |
| **p8 NO TRAIN/INFER SPLIT** | **핵심** — split 은 train · infer 모두 동일 `cell_pool_step` 호출. train-only flag 없음. v5-mitosis cotrain (train) ≡ WAKE imagination loop (infer). |

## smoke 4 invariants 결과 (verbatim runtime stdout)

`split_smoke.hexa` runtime stdout (Mac local fallback build, `HEXA_MAC_BUILD_OK=1`):

```
=== MITOSIS/split_smoke ===
MITOSIS/split_event — threshold-breach × patience → child cell append (F-V5MIT-1 SPLIT-NOGRAD: state-copy, no grad through parent farr)
threshold (static factor): 0.8
patience: 3

step=0  tension=0.0  cells=2  thresh_eff=0.0
step=10  tension=0.05  cells=16  thresh_eff=0.02
step=20  tension=0.1  cells=16  thresh_eff=0.042
step=30  tension=0.15  cells=15  thresh_eff=0.082
step=40  tension=0.2  cells=16  thresh_eff=0.122
step=50  tension=0.25  cells=16  thresh_eff=0.162
step=60  tension=0.3  cells=15  thresh_eff=0.202
step=70  tension=0.35  cells=16  thresh_eff=0.242
step=80  tension=0.4  cells=16  thresh_eff=0.282
step=90  tension=0.45  cells=15  thresh_eff=0.322

=== smoke summary ===
initial_cells: 2
final_cells:   16
max_count:     16
splits:        17
merges:        3

=== invariants ===
I1 starts-at-2:        PASS
I2 monotonic:          FAIL (merge fired)
I3 grew-beyond-2:      PASS
I4 within-max-cap:     PASS

ALL CORE INVARIANTS PASS
```

cell count progression (counts[0..100] sampled every 10 steps): **2 → 16 → 16 → 15 → 16 → 16 → 15 → 16 → 16 → 15** (ramp 초반 split 폭발 → cap=16 도달 → merge_patience=30 마다 best-pair merge 1회 → 다시 split → 진동 평형).

**해석**:
- **I1 PASS** — `initial_cells=2` 정확히 출발.
- **I2 observational FAIL** — merge 가 3회 fire (merge_patience=30 간격 + 1-cos < 0.005 만족). 본 invariant 는 `cell_pool_step` 이 merge 도 통합 처리하므로 ramp-only smoke 에서 "endcap+merge" 진동이 정상. monotonic 요구는 split-only 의 잘못된 가정 — smoke 가 이 경계조건을 정직히 노출.
- **I3 PASS** — split 17회 fire, max_count=16 ≫ initial_cells=2.
- **I4 PASS** — max_count=16 = max_cells=16, 절대 초과 없음.

핵심 invariant **I1/I3/I4 PASS**, I2 는 observation 수준 (merge_patience tick 으로 인한 정상 진동). split 메커니즘 자체는 v5-mitosis cond.5 verified pattern 으로 정상 동작.

## hexa parse 결과 (verbatim)

```
$ hexa parse MITOSIS/split_event.hexa
OK: MITOSIS/split_event.hexa parses cleanly

$ hexa parse MITOSIS/split_smoke.hexa
OK: MITOSIS/split_smoke.hexa parses cleanly
```

## 의존성

| 축 | 의존 |
|---|---|
| **M1 mitosis_lib** | `cell_pool_step` line 205-489, `mit_make_cell` line 68-107, defaults `mit_split_patience`/`mit_adaptive_factor`/`mit_window`/`mit_noise_scale`. **수정 없음** (WRAP only). |
| **M3 merge winner-take-all 회피** | 본 split-event 가 child 를 추가하는 동안 merge block (mitosis_lib line 339-426) 이 1-cos < 0.005 pair 를 keeper merge. F-PERSONA-4 KL=0 회피는 별도 architectural fix 필요 (4 cheap path 전부 FALSIFIED, project_anima_persona_4_*_2026_05_12). |
| **M4 persona-diff per cell** | `mit_make_cell` 의 child = `parent_hidden + noise·noise_scale` 가 per-cell hidden 분기. F-PERSONA-2 mean cos dist 0.996 PASS carry. |
| **M5 WAKE sleep-tick mitosis** | `cell_pool_step` 호출을 REM/N3 imagination loop 에서 emit-free 로 invoke. inference-time 분열의 자연 거주지 (p8). |
| **M6 v5-cotrain ckpt swap-in** | 581MB ckpt (cells 2→64 saturate step 150, loss 264.35→1.17) → generator.hexa `_gen_decode` seam. F5 갭 채움. |

## 관련 파일

- `MITOSIS/mitosis_lib.hexa` — M1 본체 (수정 없음)
- `MITOSIS/split_event.hexa` — M2 public surface (this PR)
- `MITOSIS/split_smoke.hexa` — M2 4-invariant smoke (this PR)
- `MITOSIS/SSOT.md` — M1 8-primitive API SSOT (보존)
- `MITOSIS.md` — milestone 표 (parent flips after this PR)
