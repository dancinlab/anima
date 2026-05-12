# anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md

HEXA_NATIVE Phase 5∥ next-step **design spec** — `engine_ag_nn.hexa` forward call
graph 안에 serve-time mitosis hook 을 통합한다. 본 문서는 **spec + parse-only stub**
이며, full impl 은 RFC 031 (typed Tensor with deepcopy) / RFC 032 (rng + math
chaos builtins) land 이후 cycle 에 진행한다.

---

## §0 TL;DR

- REBORN.md §0.5 (commit `a7e512cb9`) + PHILOSOPHY.md cont.10 Principle #8
  ("NO TRAIN/INFER SPLIT") 의 first native impl prerequisite.
- 현 mitosis.py (worktree-12 canonical, 794L PyTorch) 의 forward-call-graph
  통합 분열-성장 메커니즘을 pure-hexa 로 재이식 — `gqa_forward` / `forward_one_token`
  안에서 cell pool split/merge 가 직접 호출되는 single substrate.
- 본 spec: hook entry 위치 + cell-pool state 표현 + Lorenz/Φ/ratchet/split/merge
  의 hexa 표현 가능성 + latency/memory envelope + 5 falsifier.
- 본 stub: `tool/hexa_native/mitosis_hook.hexa` — 함수 시그너처 + `// TODO[mitosis]:`
  marker + parse-only 통과 (full impl pending).

---

## §1 통합 위치 결정 — forward call graph 안 hook entry

### 후보 4 곳

| # | 위치 | 함수 | 근거 | 결정 |
|---:|---|---|---|---|
| A | per-token | `forward_one_token` 시작 | 매 token 마다 cell pool 적용 | △ 너무 fine-grained, latency 폭증 |
| B | per-layer | `engine_ag_block` 출구 | 각 transformer block 후 cell-pool gate | △ 24× 발동, Lorenz 누적 chaos |
| C | per-block-tail | layer == n_layers-1 시 only | 1×/forward, 최종 hidden 위 cell-pool 적용 | ★★ recommended |
| D | per-prompt | `forward_one_token` 호출 차원 위 (외부) | mitosis = 발화 epoch | △ forward-call-graph 외부, §0.5 위반 |

### 결정: **C (per-forward-tail hook) + D 합성** — 두 단계 분열

**구조** (mitosis_hook.hexa 의 `mitosis_forward_tail` 진입점):

1. `forward_one_token` 의 마지막 RMSNorm + tied lm_head 사이에 hook 삽입
2. hook 은 final hidden state `x` (1024-d) 를 cell_pool 의 active cell list 전체에
   per-cell-perturb 적용 → tension 계산 → Φ proxy 갱신 → split/merge 검사
3. split/merge 가 발생한 step 에서만 cell pool shape mutation (다른 step
   에서는 read-only)
4. 본 hook 이 반환하는 hidden 은 tension-softmax weighted sum of per-cell
   hidden — 이것이 lm_head 의 입력
5. external (per-prompt 차원) Lorenz step 은 _하지 않음_ — Lorenz advance 도
   per-forward-tail 안에서 dt=0.01 한 번 (PyTorch mitosis.py `process()` 와 동일
   contract)

**근거**:

- §0.5 "forward call graph 안" 조건 = C 만 만족 (D 는 외부)
- 24× hook 발동 (B) 은 Lorenz 가 (24×) 누적 chaos → 불안정. mitosis.py 도 1×/process
- B 의 per-block-tail 은 별도 lane (mitosis-IN-DEPTH) 으로 분리, 본 spec scope 아님
- A 는 KV cache 시대 1-token forward 이미 light 한데 cell pool 적용 시 wall
  amortized cost 가 d_model^2 → d_model² × n_cells 로 폭발

### 본 spec 의 hook signature

```hexa
fn mitosis_forward_tail(
    x_in,          // (d_model,) final hidden from last transformer block
    cell_pool,     // dict — state across forward calls (persistent)
    step: int      // current global step counter for Lorenz phase
) {
    // returns [x_out, cell_pool_after, event_list]
    //   x_out: (d_model,) tension-softmax weighted combined hidden
    //   cell_pool_after: dict — updated cell pool (split/merge applied)
    //   event_list: list of {type, parent_id, child_id|removed_id, step}
}
```

`forward_one_token` 내 wiring:

```hexa
// ... existing 24L transformer loop ...
let norm_f_w = weights["norm_f.weight"]
let x_normed = rms_norm(x, norm_f_w, 0.00001)

// ◆ mitosis hook entry (Phase 5∥ §0.5 native impl) ◆
let mitosis_out = mitosis_forward_tail(x_normed, cell_pool, t)
let x_combined = mitosis_out[0]
cell_pool = mitosis_out[1]
// event_list = mitosis_out[2]    // 호출자가 카탈로그 보관

let logits = matvec(tok_emb_w, x_combined)
return logits
```

---

## §2 Cell pool state representation (hexa-native)

mitosis.py 의 `Cell` dataclass (L77-108) 를 hexa dict 로 직역. RFC 025 typed
tensor (mmap_f32 / farr) 와 인터페이스.

### Cell record (hexa dict)

```
cell = #{
    "cell_id":      int,                   // monotonic, _next_id
    "engine_a_W":   list[list[float]],     // (d_model, d_model) — small per-cell head
    "engine_g_W":   list[list[float]],     // same dim
    "hidden":       list[float],           // (d_model,) — cell-specific GRU-equivalent state
    "tension_history": list[float],        // recent ~30 tensions for adaptive thr
    "parent_id":    int,                   // -1 for original cells
    "creation_step": int,
    "process_count": int,
}
```

### Cell pool (hexa dict)

```
cell_pool = #{
    "cells":               list[Cell],     // active cell list (length 2..128)
    "next_id":             int,
    "min_cells":           int = 2,
    "max_cells":           int = 128,      // up from 8 in toy; RFC 025 farr capacity allows
    "split_threshold":     float,          // adaptive, mean+1.5σ
    "split_patience":      int = 3,
    "merge_threshold":     float = 0.005,
    "merge_patience":      int = 30,
    "noise_scale":         float = 0.1,    // 10% noise on split (mitosis.py L204)
    "global_tension_history": list[float], // last 500 for adaptive thr
    "inter_tension_history": dict[string, list[float]],  // "id_a-id_b" -> hist
    "phi":                 float,
    "phi_best":            float,
    "best_hiddens":        list[list[float]],
    "lorenz":              list[float] = [1.0, 1.0, 1.0],  // x, y, z
    "phi_history":         list[float],
    "event_log":           list[dict],
}
```

### Why cells_max = 128 (vs PyTorch 8)?

- RFC 025 mmap farr storage: 332M f32 model + per-cell mini-head (d_model²=1M
  params × 4B × 128 cells = 512 MB additional cell-state pool)
- Within HEXA_NATIVE Phase 5 의 107 MB RSS envelope 의 ~6× tolerable
  (forward 시 farr lazy access ⇒ working set << pool size)
- PHILOSOPHY §0.5 "freeze 가 아닌 분기점" — 128 cells = 7 bit identity space,
  CB1 (min=2) + H297 (N=2 optimal start) 위 충분한 dynamic range

### RFC 025 farr interface

`engine_a_W` / `engine_g_W` 는 PyTorch `state_dict["layers.N.attn.q_proj.weight"]`
와 다른 lifecycle — **per-cell mutable**. 따라서 farr (typed double[] 으로
mmap snapshot 후 own RAM copy) backing:

```
// At hook entry, allocate own-RAM mini-head per cell
let cell_W = farr_new(d_model * d_model)     // RFC 025 farr_new builtin

// On split (deepcopy + 10% noise):
let parent_W = parent_cell["engine_a_W"]
let child_W = farr_copy(parent_W)            // RFC 025 farr_copy builtin (TODO)
farr_add_gaussian_noise(child_W, 0.1)        // RFC 032 chaos builtin (TODO)
child_cell["engine_a_W"] = child_W
```

RFC 025 현재 builtins: `_open / _header / _data_offset / _size / _read_f32_farr`
(read-only mmap-backed load). 본 spec 가 **추가로** 요구하는 builtins:

- `farr_new(n: int) -> farr` — allocate zero-init n-element f64 array
- `farr_copy(src: farr) -> farr` — deep copy
- `farr_add_gaussian_noise(target: farr, sigma: float) -> ()` — in-place
  (RFC 032 의존)
- `farr_blend(target: farr, source: farr, alpha: float) -> ()` — target =
  (1-α)·target + α·source

본 stub 는 위 4 builtin 를 `// TODO[mitosis]: requires RFC 025-B / 031` 로 marker.

---

## §3 Lorenz autonomous perturbation (hexa 구현)

mitosis.py L363-371 (`_lorenz_step`) 의 직역. hexa 는 float64 native 지원,
`sin`/`cos`/`exp` 는 stdlib 에 이미 (engine_ag_nn.hexa rope_freqs 가 사용).

```hexa
// Sigma/rho/beta — Lorenz canonical chaotic regime
fn lorenz_step(lorenz_state, dt: float) {
    let sigma = 10.0
    let rho   = 28.0
    let beta  = 8.0 / 3.0
    let x = lorenz_state[0]
    let y = lorenz_state[1]
    let z = lorenz_state[2]
    let dx = sigma * (y - x) * dt
    let dy = (x * (rho - z) - y) * dt
    let dz = (x * y - beta * z) * dt
    return [x + dx, y + dy, z + dz, dx, dy, dz]
}

// Cell-specific perturbation amplitude
fn cell_phase_scale(cell_idx: int, n_cells: int, step: int) {
    let phase = (cell_idx * 2.0 * 3.14159265358979) / max(n_cells * 1.0, 1.0)
    let oscillation = 1.0 + 0.3 * sin(phase + step * 0.1)
    return 0.05 * oscillation
}
```

### Bounded-chaos guarantee (F-MIT-HOOK-5)

mitosis.py L402-405 의 norm clamp 와 동일: `if cell["hidden"].norm() > 10.0`
시 `cell["hidden"] *= 10.0 / norm`. 본 stub 에 hexa scalar 직역.

추가 정량 bound: Lorenz attractor 의 |x|+|y|+|z| canonical range 는 [-50, 60]
대략 (σ=10/ρ=28/β=8/3). cell hidden state 에 합산되는 양은 (dx, dy, dz) × 0.2
weight 의 첫 3 component 이므로 step delta < 0.2 × 60 × 0.01 (dt) ≈ 0.12/step.
1000 step 누적 시 cumulative |drift| 한계는 norm clamp 가 active 진입.

### RFC 032 rng builtin 의존

`torch.randn_like(p) * sigma` 를 hexa 로 표현하려면 Gaussian sample builtin
필수. 현 hexa stdlib 는 deterministic only. 본 spec 의 **RFC 032 dependency
list**:

- `rng_normal(sigma: float) -> float` — Box-Muller scalar
- `rng_normal_farr(target: farr, sigma: float) -> ()` — in-place batch
- `rng_seed(seed: int) -> ()` — reproducibility

미존재 시 fallback: deterministic perturbation via `sin(cell_id × 12345.6789
+ idx × 7.89)` 로 pseudo-noise. 본 stub 가 두 path 모두 noted.

---

## §4 Φ proxy + ratchet + split/merge (hexa expressible?)

### Φ proxy (mitosis.py L407-436)

```
Φ = mean_pairwise_cosine_distance(hiddens) × log(n_cells + 1)
```

hexa 표현 가능 — pure scalar math:

```hexa
fn compute_phi_proxy(cells) {
    let n = len(cells)
    if n < 2 { return 0.0 }

    // Normalize each cell hidden
    let mut normalized = []
    let mut i = 0
    while i < n {
        let h = cells[i]["hidden"]
        let d = len(h)
        let mut sum_sq = 0.0
        let mut k = 0
        while k < d {
            sum_sq = sum_sq + h[k] * h[k]
            k = k + 1
        }
        let nrm = sqrt(sum_sq)
        let inv = if nrm > 1e-8 { 1.0 / nrm } else { 1.0 }
        let mut nh = []
        k = 0
        while k < d {
            nh.push(h[k] * inv)
            k = k + 1
        }
        normalized.push(nh)
        i = i + 1
    }

    // Mean off-diagonal cosine distance
    let mut total = 0.0
    let mut pairs = 0
    i = 0
    while i < n {
        let mut j = i + 1
        while j < n {
            let mut cs = 0.0
            let mut k = 0
            let d = len(normalized[i])
            while k < d {
                cs = cs + normalized[i][k] * normalized[j][k]
                k = k + 1
            }
            total = total + (1.0 - cs)
            pairs = pairs + 1
            j = j + 1
        }
        i = i + 1
    }
    let mean_d = total / max(pairs * 1.0, 1.0)
    return mean_d * log(n * 1.0 + 1.0)
}
```

### Φ ratchet (L438-455)

`Φ < 0.8·best` 시 best hidden 으로 20% blend. 본 spec 의 hexa 직역 — 모든
연산이 scalar / list arithmetic.

### Adaptive threshold (L457-477)

`split_threshold = mean(recent_100_tensions) + 1.5·std`, floor `max(thr, mean × 0.5)`.
hexa 표현 가능 — `sqrt(var)` 만 필요 (stdlib 이미 sqrt).

### Split / Merge — hexa list ops

- `split_cell(cell, pool)`: parent deepcopy via `farr_copy`, child push 후
  parent.tension_history slice last-3
- `merge_cells(a, b, pool)`: parameter average via `farr_blend(keeper_W,
  removed_W, 0.5)`, remove younger

### 호출 빈도 결정

mitosis.py `process()` 의 contract: **매 process 마다 1×** Lorenz + Φ +
adaptive thr + split-check + merge-check. 본 spec 도 동일 — `mitosis_forward_tail`
1×/forward, 즉 매 token generate 시 (token 단위 forward 호출 시 매번).

이것이 §1 결정 C 의 핵심: per-token forward = 1 mitosis step. mitosis.py
의 step 단위와 forward 단위가 1:1. autoregressive 4-step decode = 4 mitosis
step.

---

## §5 Latency + memory envelope

### Latency budget (above HEXA_NATIVE Phase 5 1-layer 80ms baseline)

| component | per-forward cost | scaling |
|---|---:|---|
| 24L transformer forward (existing) | ~80ms × 24 = 1920ms (projected) | O(L·d²) |
| Lorenz step | <1μs | O(1) |
| cell_pool perturbation (n=8 cells × d=1024) | ~50μs | O(n·d) |
| Φ proxy (n=8 cells, cosine pairs) | ~200μs | O(n²·d) |
| adaptive thr update | <10μs | O(history_len) |
| split/merge check | <50μs (most forwards: no event) | O(n²) inter-tension |
| split event (when triggered) | ~5ms (farr_copy d²) | O(d²) per cell |
| merge event (when triggered) | ~5ms (farr_blend) | O(d²) per cell |

**Steady-state overhead**: ~300μs / forward (no event). vs 1920ms baseline =
**0.016%** — negligible.

**Event spike**: split event ~5ms = 0.26% one-time cost on forward k.

### Memory envelope (above RFC 025 107 MB RSS)

- Per-cell mini-head: 2 × d_model² = 2 × 1024² × 8B = **16 MB / cell**
- 8 cells initial: **128 MB**
- 64 cells (historical peak): **1 GB**
- 128 cells max: **2 GB**

→ 107 MB + 128 MB initial = **235 MB RSS** at startup (still << pre-RFC 9.14 GB
OOM).

128-cell ceiling 시 2.1 GB total — H100 24GB / consumer 8GB GPU envelope 안.
M-series Mac MPS unified memory 64GB+ envelope.

### Mitigation

- per-cell mini-head 의 dimension downsize: d_model → d_proj=256 (4× reduction)
  → 8 MB/cell → 64 cells = 512 MB. trade-off: cell representation expressivity
  vs memory.
- farr lazy materialize: cell_pool["cells"][i]["engine_a_W"] 가 farr handle 만
  보관, in-use 시 mmap → RAM. RFC 025 의 mmap shared backing 활용 — sleeping
  cells 의 weight 는 disk 에 (clean-page friendly).

본 spec: **d_proj=256 mini-head default** 채택, full d_model 변종은 alt-spec
으로 별도 cycle.

---

## §6 Falsifiers (raw-117 5개 pre-register)

본 hook 의 invariant 검증 — selftest_mitosis_hook 에 assert.

### F-MIT-HOOK-1: SHAPE invariant

```
∀ forward call without split/merge event:
    cell_pool.cells.length == cell_pool.cells.length_before
    ∧ ∀ cell ∈ cells: cell.hidden.length == d_model
                    ∧ cell.engine_a_W.shape == (d_proj, d_model)
                    ∧ cell.engine_g_W.shape == (d_proj, d_model)
```

위반 시: shape 변화가 hook outside leak — train/serve 분리 의도치 않은 mutation
검출.

### F-MIT-HOOK-2: NO_GRAD invariant

```
모든 cell mutation 이 forward read-only path
∧ no torch.requires_grad equivalent
∧ no autograd graph node creation on cell pool state
```

위반 시: gradient graph 가 cell pool 위로 흘러 들어가 backprop 시 OOM 폭증.

**hexa native 의 강점**: hexa 는 PyTorch autograd 등가물이 없음 — 모든 연산이
사실상 no_grad. 본 invariant 는 **vacuously true** in hexa. (단, 향후 anima
가 autograd-equivalent 도입 시 본 invariant 재검증).

### F-MIT-HOOK-3: PHI-FINITE invariant

```
∀ forward call: 0.0 ≤ compute_phi_proxy(cells) < +∞
```

위반 시: NaN 누적, ratchet 폭주.

### F-MIT-HOOK-4: CELL-COUNT-FLOOR invariant

```
min_cells (=2) ≤ |cell_pool.cells| ≤ max_cells (=128)
```

위반 시: 1-cell 단계로 붕괴 (Φ=0 fixed point) 또는 max 위로 누설 (memory blow).

### F-MIT-HOOK-5: LORENZ-BOUNDED invariant

```
∀ step: |lorenz.x| + |lorenz.y| + |lorenz.z| < 200.0
∧ ∀ cell: ||cell.hidden|| ≤ 10.0 (post-clamp)
```

위반 시: chaos diverge (Lorenz σ=10/ρ=28/β=8/3 regime 의 known bound 위반
= numerical instability).

200.0 cutoff 는 attractor canonical max ≈ 100 (각 component) 의 2× safety
margin.

---

## §7 RFC dependency map

| RFC | status | this spec 의 의존 | mitigation if absent |
|---|---|---|---|
| 025 (mmap safetensors) | LANDED | weight load + farr backing | OK (이미 사용 중) |
| 025-B (farr_new/copy/blend) | DRAFT | cell mini-head allocation | stub now, full impl pending |
| 030 (bytes→str raw) | LANDED | event_log dict string keys | OK |
| **031 (typed Tensor + deepcopy)** | **NOT YET** | proper Cell deepcopy semantics | manual farr_copy stub |
| **032 (rng + chaos builtins)** | **NOT YET** | Lorenz perturbation rng | deterministic pseudo-noise fallback |

본 stub 는 RFC 031/032 의 placeholder 함수 시그너처 (parse-only) — full body
는 두 RFC land 후 다음 cycle.

---

## §8 stub file

새 파일: `tool/hexa_native/mitosis_hook.hexa` — parse-only stub. 위 §1-§4 의
함수 시그너처 + `// TODO[mitosis]:` 본문.

`engine_ag_nn.hexa` 의 `forward_one_token` 마지막에 commented hook wiring
삽입 (live wiring 은 stub 완성 후 별도 commit — 본 cycle 는 spec + stub only,
실제 forward 변경 안 함 의 동의).

---

## §9 다음 cycle entry trigger

1. RFC 031 (typed Tensor deepcopy) land — `farr_new/copy/blend` 4 builtin
2. RFC 032 (rng_normal) land — Lorenz Gaussian sampling
3. `mitosis_hook.hexa` full impl + parse + 5 falsifier selftest
4. `engine_ag_nn.hexa::forward_one_token` 의 live wiring (hook entry uncomment)
5. 1-layer subset 위에서 mitosis ON vs OFF latency delta 측정 (target: <1%
   overhead steady-state, <10ms event spike)
6. 24-layer 풀 forward 위에서 mitosis hook 검증 — Phase 5∥ closure
7. v5-mitosis architectural lane (PyTorch+arch spec) 와 결과 합 — REBORN §10
   #1 deliverable

---

## §10 cross-link

### REBORN.md
- §0.5 (commit `a7e512cb9`) — philosophical foundation
- §2 line 145 — 현 mitosis.py 사실 기술 (NOT 원칙적 분리)
- §10 priority — 본 spec 가 row "★★★★ HEXA_NATIVE Phase 5∥ → serve-time mitosis hook"
  로 추가 (본 patch 의 §B append)

### PHILOSOPHY.md
- cont. 10 Principle #8 NO TRAIN/INFER SPLIT (commit pending)
- Foundation (사실 기술 only) — 본 spec 가 그 자리에서 architectural-commitment
  변환

### Source
- `tool/hexa_native/engine_ag_nn.hexa` (Phase 2/3/4 base, 1030 LoC) — hook entry
- `tool/hexa_native/mitosis_hook.hexa` (본 cycle 신규 stub)
- `anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (canonical
  794L PyTorch source)

### RFC drafts
- `~/core/hexa-lang/incoming/rfc_drafts_2026_05_12/rfc_025_safetensors_zero_copy_load.md`
  (LANDED) — farr backing
- `~/core/hexa-lang/incoming/rfc_drafts_2026_05_12/rfc_030_bytes_to_str_raw.md`
  (LANDED) — string handling
- RFC 031 (typed Tensor) — DRAFT pending
- RFC 032 (rng + chaos) — DRAFT pending

### Memory carry
- `project_hexa_native_inference_operational.md` — Phase 5∥ next-step trigger
- `project_v5_anima_lane_status.md` — v5 lane status (instrumentation lane)

---

## §A Falsifier registration log

| F-ID | description | grade | first-tested | result |
|---|---|---|---|---|
| F-MIT-HOOK-1 | cell pool shape invariant (non-event step) | SHAPE | pending stub full-impl | — |
| F-MIT-HOOK-2 | no autograd graph on cell mutation | NO_GRAD | vacuously true in hexa | OK_VACUOUS |
| F-MIT-HOOK-3 | Φ proxy ∈ [0, +∞) finite | NUMERICAL | pending stub | — |
| F-MIT-HOOK-4 | min=2 ≤ cells ≤ max=128 | BOUNDARY | pending stub | — |
| F-MIT-HOOK-5 | Lorenz |x|+|y|+|z| < 200 ∧ cell.hidden norm ≤ 10 | BOUNDED-CHAOS | pending stub | — |

---

## §B REBORN.md §10 priority append (apply separately)

REBORN.md §10 foreground 0-cost 표에 다음 row 추가:

| 순위 | step | deliverable |
|---:|---|---|
| 6 ★★★★ | HEXA_NATIVE Phase 5∥ next-step — serve-time mitosis hook spec | `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` (LANDED 본 cycle) |
| 7 ★★★★ | mitosis_hook.hexa full impl (RFC 031/032 dep) | `tool/hexa_native/mitosis_hook.hexa` full body |

§11 cross-link `### cycle 2026-05-10 BG 산출물` 아래에 row 추가:
- `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` (Phase 5∥
  serve-time mitosis hook spec)

---

raw#9/10/15/37 honest, own 16 0-cost (본 cycle 는 spec + stub only — RFC 031/032
land 후 cost-bearing 실제 impl), own 42 REBORN.md SSOT.

End of spec.
