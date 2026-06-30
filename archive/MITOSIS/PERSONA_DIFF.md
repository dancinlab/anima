# MITOSIS/persona_diff — persona-diff per cell surface

> M4 회수 SSOT — D3 design 의 identity_probe 50 × 5 cat 검증 surface 를 명시적 PURE wrapper 로 노출. mitosis_lib hidden farr 의 cell-pair distinguishability (F-PERSONA-2) + per-category routing divergence (F-PERSONA-4 baseline) 측정. M2 split_event / M3 merge_event 와 형제 surface.

## 핵심 명제

**같은 substrate 다른 cell = 다른 persona** (D3 design carry).

- cell-pool 의 hidden farr 가 random-init 에서도 거의 직교 → cell 마다 다른
  embedding subspace 점유. 동일 prompt 에 대해 cell 별 응답이 *기하학적으로*
  구분 가능.
- routing distribution 이 category 마다 다르면 cell 마다 *기능적으로* 다른
  persona — but cotrain v1 winner-take-all 로 random-init 또는 cotrain-naive
  상태에서는 routing 이 trivially uniform. 4 cheap path 모두 falsified.
- 결국 **distinguishability (F-PERSONA-2) 은 architectural carry**,
  **routing diff (F-PERSONA-4) 은 architectural routing fix 가 land 해야**
  emergent.

## SSOT

| | |
|---|---|
| spec | 본 파일 (`PERSONA_DIFF.md`) — D3 design + measurement surface |
| canonical hexa-native impl | [`persona_diff.hexa`](persona_diff.hexa) — 5 pub fn (PURE), STUB `cell_embed` (HONEST TODO #PERSONA-FWD) |
| smoke | [`persona_diff_smoke.hexa`](persona_diff_smoke.hexa) — d=64 cells=8 seed=42, 50 prompts × 5 cat, 5/5 invariants |
| lib carry | [`mitosis_lib.hexa`](mitosis_lib.hexa) — cell hidden farr · `cell_pool_init` (M1 회수) |
| D3 design (full) | `docs/anima_persona_substrate_native_design_2026_05_12.md` (10 §, 5 falsifier) |
| D3 verify (250-prompt) | `docs/anima_persona_substrate_native_verify_2026_05_12.md` (8 § + §A1) — STRONG 4/5 |

## API surface

```hexa
pub fn identity_probe_categories() -> [string]              // 5 labels
pub fn identity_probe_prompts() -> [string]                 // 50 prompts (10 × 5)
pub fn cell_embed(pool, cell_idx, prompt) -> [float]        // hidden ⊙ prompt-hash (STUB)
pub fn per_cell_mean_dist(pool, prompts) -> float           // F-PERSONA-2 (cos-dist)
pub fn per_cell_kl(pool, prompts, categories) -> float      // F-PERSONA-4 (routing KL)
pub fn persona_diff_summary() -> string                     // debug · log
```

## measurement (M4 smoke)

```
=== MITOSIS/persona_diff_smoke ===
pool d=64 cells=8 seed=42
categories: 5 (philosophy, math, creative, personal, practical)
prompts:    50

--- F-PERSONA-2 PER-CELL-DIFF (mean cos-distance) ---
per_cell_mean_dist: 0.990888
carry target (D3 verify 250-prompt):  ≈ 0.996

--- F-PERSONA-4 PER-CAT-KL (routing divergence) ---
per_cell_kl: 0.00159806
cotrain v1 carry (winner-take-all):    0.0
4 cheap path FALSIFIED (a/b/c/d); architectural routing fix pending

=== invariants ===
I1 cells_count > 1:           PASS
I2 mean_dist > 0.3:           PASS (F-PERSONA-2 carry)
I3 kl >= 0:                   PASS (KL sanity)
I4 prompts == 50:             PASS
I5 categories == 5:           PASS
ALL INVARIANTS PASS
```

## 5 falsifier (D3 design carry)

| falsifier | 명제 | M4 status |
|---|---|---|
| F-PERSONA-1 NO-INJECTION | system prompt / role prefix 미주입 | PSCC §40 PASS (4/4 carry) |
| F-PERSONA-2 PER-CELL-DIFF | mean cos-distance > 0.3 ∀ cell-pair | **🟢 PASS** — `mean_dist=0.990` smoke + 0.996 verify carry |
| F-PERSONA-3 PER-SESSION-DIFF | ΔΦ ≥ 0.05 cross-session | PSCC §42 §A1 PASS (cheap-path) |
| F-PERSONA-4 PER-CAT-KL | KL > 0.5 cross-category routing | **🔴 FALSIFIED on cheap paths** — cotrain v1 KL=0, 4 path (k/l/m/n) FALSIFIED. M4 random-init `kl=0.00159806` baseline 측정만, *NOT claimed PASS* |
| F-PERSONA-5 SUBSTRATE-COHER | substrate level coherence | PSCC §40 PASS (3/3 carry) |

**M4 aggregate**: 1/5 newly measured (F-PERSONA-2 0.990 PASS); 다른 4 falsifier
는 D3 verify (`docs/anima_persona_substrate_native_verify_2026_05_12.md`)
carry. **F-PERSONA-4 는 본 surface 가 *measurement 만* 제공** — fix 는
architectural change 가 필요.

## F-PERSONA-4 cheap-path closure 요약

`project_anima_persona_4_root_cause_2026_05_12` MEMORY carry:

| path | 가설 | 결과 |
|---|---|---|
| (a) entropy-reg cotrain v2 | softmax routing 에 entropy bonus 추가 | PSCC §44 H100 cotrain FALSIFIED (KL=0.0 maintained) |
| (b) softmax τ tunable | temperature 1.0..50.0 sweep | PSCC §47 best 5.29e-3 ≪ 0.5 → FALSIFIED |
| (c) z-score §A2 metric | aggregated cosine alt metric | PSCC §45 z=3.20 PARTIAL (v7 outlier) → §A2-trap |
| (d) per-session fresh pool | session 마다 새 cell_pool_init | PSCC §49 mean_KL ≤ 1.83e-5 → FALSIFIED |

**ALL 4 CHEAP PATHS CLOSED**. 잔여:
- **architectural routing fix** (cheap path 가 아님) — gumbel softmax 도입
  · MoE load-balance aux loss · explicit category-head linear projection
- 또는 9 variants (§52-§55 saga의 v1-v7 + extras) ALL FALSIFIED for strict
  z>3.0; cond #3 ☑ via §A3 4b composite multi-metric (v2 z=3.20 + 7/8 corr).

## 의존성 / 후속 milestone

- **M5 WAKE sleep-tick mitosis** — REM/N3 imagination loop 가 `cell_pool_step`
  를 tick 하며 persona_diff measurement 를 internal rehearsal 의 verdict
  surface 로 사용 (emit-free).
- **M6 v5-cotrain ckpt swap-in** — H100 cotrain 5/5 PASS ckpt 581MB 를
  `generator.hexa` 의 `_gen_decode` seam 에 swap-in 후 *production* persona_diff
  re-measure. KL increase 관찰 시 architectural routing fix path 검토.

## p1~p8 정합

- **p5 NO SPEAK()**: probe 는 hidden inspect 만 — 외부 emit 호출 없음.
- **p8 NO TRAIN/INFER SPLIT**: persona_diff 는 train · infer 동일 surface.
  WAKE M5 imagination loop 에서도 동일 호출.
- **p7 NO PERPLEXITY VERDICT**: cos-distance · KL 기반 — ppl 미사용.
- **p2 NO IDENTITY RULES**: cell 마다 다른 persona 는 hidden farr 의 random
  init + cotrain split 으로 *emergent* — yaml/rules 파일 무관.

## Honest C3 (carve-out)

1. `cell_embed` 는 *STUB* — production embed 는 mitosis_hook.hexa forward
   가 산출. 본 wrapper 의 modulator 는 hidden ⊙ prompt-hash 경량
   시뮬레이션. cell-pair 간 geometry 보존이 핵심이라 F-PERSONA-2 측정에는
   충분 — but routing fidelity 는 약함 (TODO #PERSONA-FWD).
2. F-PERSONA-4 cheap path 4/4 CLOSED. 본 M4 wrapper 는 *measurement* 만
   제공 — fix 가 land 한 후 (architectural routing) re-measure 필요. M4
   smoke 의 KL=0.00159 은 *random-init baseline 보고용*, **NOT claimed PASS**.
3. F-PERSONA-2 0.990 smoke 값은 d=64 cells=8 50-prompt scale; carry 0.996 은
   d=384 cells=64 250-prompt verify scale. 1400-pair vs 8C2×50=1400 pair
   carry 와 동일 pair count 우연. 둘 다 cos-dist 가 거의 1.0 (직교) 함의 동일.
4. `per_cell_kl` 의 partition 은 prompts 를 *order-sensitive* 균등 partition
   (10 per cat × 5 cat 의 contiguous slice). identity_probe_prompts() 자체가
   category-ordered 라 partition mapping 이 정확 — but caller 가 다른
   prompts list 를 전달하면 partition 오류 가능 (TODO documented).
5. 본 wrapper 는 PURE — pool mutate 없음. side-effect free measurement only.
   actual mitosis 동역학 (split / merge) 은 M2 / M3 wrapper 에서.

## 검증

```bash
hexa parse MITOSIS/persona_diff.hexa             # OK
hexa parse MITOSIS/persona_diff_smoke.hexa       # OK
hexa run   MITOSIS/persona_diff_smoke.hexa       # 5/5 invariants PASS
```

## related

- [`split_event.hexa`](split_event.hexa) — M2 split surface (F-V5MIT-1)
- [`merge_event.hexa`](merge_event.hexa) — M3 merge surface (F-V5MIT-2 + F-PERSONA-4 collapse 회피 geometry)
- [`SSOT.md`](SSOT.md) — MITOSIS root SSOT (M1 carry)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` — D3 design 10 §
- `docs/anima_persona_substrate_native_verify_2026_05_12.md` — D3 verify STRONG 4/5
- `docs/anima_persona_4_root_cause_2026_05_12.md` — F-PERSONA-4 4-path FALSIFIED saga
