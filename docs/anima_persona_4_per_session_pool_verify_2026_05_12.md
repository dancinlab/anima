# `anima_persona_4_per_session_pool_verify` — REBORN §89 hexa-native per-session pool F-PERSONA-4 audit

**Date**: 2026-05-12 KST
**BG slot**: PSCC §49
**Mission slot**: GOAL.md cond #3 D3 path (d) (REBORN §89 hexa-native per-session pool)
**Cost**: $0 Mac local (wall ~1 min/run × 3 runs + analysis)
**Verdict**: **SCENARIO (iii) — (d) FALSIFIED** · cond #3 STRONG 4/5 carry MAINTAINED
**Author**: anima reborn cycle

---

## §1 PURPOSE — what this BG measures

cond #3 ☑ 잔여 path 4 후보 중 3 falsify 됨 (PSCC §44 → §45/§47/§48 trail):

| Path | Description | Status |
|---|---|---|
| (a) | cotrain v2 multi-corpus | FALSIFIED ubu-2 SMALL (PSCC §48) · LARGE H100 in-flight (PSCC §45) |
| (b) | softmax τ tunable | FALSIFIED ubu-1 (PSCC §47, 10-T sweep best KL 5e-3) |
| (c) | z-score metric §A2 redefinition | FALSIFIED PSCC §45 null-test (z=-0.03, p=0.46) |
| **(d)** | **REBORN §89 hexa-native per-session pool** | ★ **본 BG** |

본 §49 = path (d) 의 explicit single-purpose audit. 가설:

- F-PERSONA-4 의 KL=0 monopoly 는 cotrain ckpt 의 cell-pool routing winner-take-all (cell-0 tension 793 vs runner-up 7.4) 결과
- **inference-time fresh cell pool per session** = 각 session 마다 random-init cell pool (untrained baseline 처럼) → cells 가 orthogonal basis 유지
- D3 measurement pre-cotrain (PSCC §40/§42 §A1) 시점에 KL 이 STRONG path candidate 였음
- per-session pool 이 cotrain ckpt 의 routing 을 BYPASS → category-specific divergence emergent?

이 가설이 PASS scenario (i) 면 cond #3 ☑ DONE, 5-cond aggregate **5/5 ☑ ACHIEVED 🎉**.

---

## §2 METHOD — harness design

**File**: `state/anima_d3_per_session_pool_2026_05_12/anima_persona_4_per_session_pool_verify.hexa` (28 KB, ~580 LoC)

**Phase order**:

1. `prompt_to_vec(prompt, d_model)`: PSCC §40 byte-parity FNV-1a + LCG fold → d-dim float vector (deterministic per prompt)
2. **Per-session pool** (5 sessions, one per identity_probe category):
   - `cell_pool_init(d_model, n_cells)` (RFC 033 gaussian, stream advances per call)
   - `tension_softmax_weights(pool, x_in)` for each of the 10 prompts in that category
   - aggregate → 5 category-mean weight distributions (one per session/cat)
3. **Observed KL matrix**: 5×5 over cat-pairs (10 upper-triangle, 5C2), with `mean_KL`, `min_KL`, `max_KL`
4. **Null permutation test** (n_perms=100, hexa-side LCG seed 20260512):
   - For each perm: shuffle category labels across all 50 (prompt, weights) triples
   - Re-aggregate, re-compute `mean_KL`
   - Tally `n_above` (null ≥ observed), compute `null_mean`, `null_std`, `z = (obs - null_mean)/null_std`
5. **Verdict scenarios**:
   - (i) `obs ≥ 0.5 AND z ≥ 1.65 AND p ≤ 0.05` → cond #3 ☑ DONE via (d)
   - (ii) `obs ≥ 0.5 AND null FAIL` → artifact (PSCC §45 lesson — z-score §A2 trap)
   - (iii) `obs < 0.5` → (d) FALSIFIED

**Reuse**: `_mit_cell_forward`, `_mit_list_to_farr`, `_mit_sqrt_safe`, `_mit_log_safe`, `cell_pool_init` all imported from `tool/hexa_native/mitosis_hook.hexa` (REBORN §91 LANDED). No reimplementation → byte-parity with PSCC §40 baseline routing math.

**Determinism**:
- `__HEXA_FARR_GAUSS_SEED__` env controls cell_pool gaussian draws (RFC 033 splitmix64; one stream advancing across all 5 `cell_pool_init` calls)
- Hexa-side LCG (seed 20260512) controls null-permutation order — independent of gauss stream

---

## §3 CONFIGURATION SWEEP — 3 runs

| Tag | d_model | n_cells | __HEXA_FARR_GAUSS_SEED__ | wall | RSS peak |
|---|---|---|---|---|---|
| `base` | 64 | 8 | 20260512 | ~25s | < 100 MB |
| `prod` | 384 | 64 | 20260512 | ~60s | ~768 MB |
| `prod_seed2` | 384 | 64 | 99999 | ~60s | ~768 MB |

`base` config matches PSCC §40 baseline (d=64, cells=8) exactly to preserve dependent-variable rigor — KL delta vs §40 attributable solely to the per-session-pool ablation.

`prod` config matches BG prompt explicit ask (d=384, cells=64) — production scale per `tool/hexa_native/mitosis_hook.hexa` max_cells=128 budget. `HEXA_MEM_UNLIMITED=1` required (768 MB cap exceeded at init; 64×384² = 9.4 M floats per pool × 5 pools + scratch).

`prod_seed2` = different gauss seed to test robustness of null-test signal.

---

## §4 RESULTS

### §4.1 base (d=64, cells=8, seed=20260512)

| Metric | Value |
|---|---|
| observed `mean_KL` | **6.48 × 10⁻⁵** nats |
| observed `min_KL` | 2.47 × 10⁻⁵ |
| observed `max_KL` | 1.41 × 10⁻⁴ |
| `null_mean` | 7.50 × 10⁻⁵ |
| `null_std` | 2.07 × 10⁻⁵ |
| `n_above` (null ≥ obs) | 66 / 100 |
| `p_value` | 0.66 |
| `z_score` | **−0.49** |
| observed_pass (≥ 0.5) | **false** |
| null_pass (z ≥ 1.65 ∧ p ≤ 0.05) | **false** |
| Verdict | **(iii) FALSIFIED** |

**Comparison to PSCC §40 baseline** (single shared pool, same d/cells/probes):

- PSCC §40 single-pool: `mean_KL = 9.74 × 10⁻⁵`
- §49 per-session pool: `mean_KL = 6.48 × 10⁻⁵`

Per-session pool **decreased** observed `mean_KL` slightly. The null test confirms there is no category-specific signal beyond chance: `z = −0.49` (observed is below null mean), `p = 0.66` (66/100 permutations beat observed). No emergent category divergence at this scale.

### §4.2 prod (d=384, cells=64, seed=20260512)

| Metric | Value |
|---|---|
| observed `mean_KL` | **1.79 × 10⁻⁵** nats |
| observed `min_KL` | 1.15 × 10⁻⁵ |
| observed `max_KL` | 2.44 × 10⁻⁵ |
| `null_mean` | 1.46 × 10⁻⁵ |
| `null_std` | 1.26 × 10⁻⁶ |
| `n_above` (null ≥ obs) | 1 / 100 |
| `p_value` | 0.01 |
| `z_score` | **+2.64** |
| observed_pass (≥ 0.5) | **false** |
| null_pass (z ≥ 1.65 ∧ p ≤ 0.05) | **true** |
| Verdict | **(iii) FALSIFIED** (despite null-pass; absolute magnitude ≪ threshold) |

**Interesting** — prod scale produces a statistically detectable per-session category signal (`z=2.64`, `p=0.01`) but the absolute magnitude is **28,000× below threshold** (`1.79e-5` vs `0.5`). The signal exists but is in the noise band of the per-cell tension softmax; the per-session-pool ablation cannot produce a category-level routing distinction strong enough to clear F-PERSONA-4.

### §4.3 prod_seed2 (d=384, cells=64, seed=99999) — null-test robustness check

| Metric | Value |
|---|---|
| observed `mean_KL` | 1.83 × 10⁻⁵ nats |
| `null_mean` | 1.52 × 10⁻⁵ |
| `null_std` | 1.40 × 10⁻⁶ |
| `n_above` | 20 / 100 |
| `p_value` | 0.20 |
| `z_score` | **+0.86** |
| observed_pass | false |
| null_pass | **false** |
| Verdict | **(iii) FALSIFIED** |

Different gauss seed → null-test PASSES drop (z 2.64 → 0.86, p 0.01 → 0.20). The prod-seed1 null-pass was **seed-dependent**; the per-session-pool category signal is NOT robust across initializations.

---

## §5 VERDICT — SCENARIO (iii) FALSIFIED

All 3 configs: `observed_mean_KL < 0.5` by ≥ 4 orders of magnitude. **(d) FALSIFIED**.

**Cross-config robustness**: prod-seed1 had `z=2.64` (null PASS), but prod-seed2 had `z=0.86` (null FAIL) at same d/cells. The seed-dependent null-test result confirms the small signal at prod scale is not a robust per-session category divergence — it's noise-level fluctuation amplified by larger cell count.

**Comparison to all 4 paths**:

| Path | Status | Best `mean_KL` | Path closed? |
|---|---|---|---|
| (a) ubu-2 SMALL per-cat corpus | FALSIFIED (§48) | 0.0 | YES (LARGE H100 §45 in-flight) |
| (b) softmax τ sweep ubu-1 | FALSIFIED (§47) | 5.3 × 10⁻³ | YES |
| (c) z-score metric §A2 | FALSIFIED (§45) | KL=0.97 but z=−0.03 artifact | YES |
| **(d) hexa-native per-session pool** | **FALSIFIED (§49 본 BG)** | **6.5 × 10⁻⁵** (base) / **1.8 × 10⁻⁵** (prod) | **YES** |

**All 4 cheap paths now CLOSED**. Sole remaining lane = **cotrain v2 entropy-reg H100** (PSCC §45 in-flight, λ_ent=0.1, balanced 5-cat corpus 1.3 MB on H100 SXM).

cond #3 D3 **STRONG 4/5 carry MAINTAINED** — F-PERSONA-1/2/3/5 PASS + F-PERSONA-4 FAIL (untrained-pool architecture limitation, not measurement gap).

5-cond aggregate **4/5 ☑ MAINTAINED** (cond #1 PSCC §46 / cond #2 hexa port v0.3 / cond #4 mitosis live evidence / cond #5 Principle #3) + cond #3 single 🔶 STRONG 4/5 carry.

---

## §6 WHY DID (d) FAIL — interpretation

The per-session-pool hypothesis assumed that with untrained random-init cells, the prompt → cell-tension mapping would be category-conditional via the natural prompt-vector × random-rotation interaction. Empirically at d=384 cells=64:

1. The prompt-byte-hash vectors `prompt_to_vec(p)` for each category produce x_in vectors that are essentially statistically interchangeable from the standpoint of random-init cell weights — both x_in's and engine_a/g weights are sampled from zero-mean small-variance gaussian distributions.

2. The cell forward `y_a − y_g` mean-square tension is dominated by the variance product of x_in and weight columns, with no preferred direction. Each cell yields tension in a narrow band (prod prompt 0: tensions span [0.14, 0.19], spread 35% of mean) — softmax over this band → near-uniform weights → categories produce near-identical distributions.

3. PSCC §40 with single shared pool yielded `KL ≈ 9.7e-5`. §49 per-session-pool reduced this further (to `1.8e-5` at prod scale) because each category sees a *different* pool but in expectation those pools sample the same gaussian — the category-mean distributions become more similar (variance reduction via session-averaging).

4. The (d) hypothesis essentially confused "winner-take-all" (cotrained cell-0 monopoly) with "category routing". Fresh per-session pools eliminate the cell-0 dominance but ALSO eliminate any directional structure that could differentially route categories. There's nothing left to discriminate categories with.

The architecturally sound solution remains the path identified in PSCC §45-FINAL: **(i) M4 aggregated cosine alternative metric** (cond #3 ☑ NOW possible given v2 z=3.20 PASS on cell content), or **(ii) gumbel-softmax / load-balanced MoE routing** (architectural fix).

---

## §7 HONEST C3 (raw#10)

1. **d_model=64 / cells=8 byte-parity is the primary scientific control**. Production d=384 cells=64 was added per BG prompt explicit ask but introduces a 7.5× cell-count delta + 6× d delta; the comparison with PSCC §40 baseline (9.7e-5) is rigorously valid only at the `base` config.

2. **Fresh-per-session pool via gauss stream advance** is a defensible but imperfect proxy for "fresh seed per session". A perfectly orthogonal alternative would run the harness 5 times with 5 different `__HEXA_FARR_GAUSS_SEED__` values, one per category. We did not do this because (a) the gauss stream within a single process is itself a high-quality PRNG (splitmix64), and (b) the cross-seed sanity check (prod_seed2 vs prod) confirms the seed dependency is BENIGN — both seeds yield mean_KL ≈ 1.8e-5 (within 2% of each other), only the null z-score differs.

3. **The null permutation test uses 100 permutations** matching PSCC §45 methodology. n=100 is the established mission convention. Higher n_perms (e.g., 1000) would refine the z-score precision but cannot change the qualitative verdict — the gap between observed (1.8e-5) and threshold (0.5) is too large to be a precision issue.

4. **The hexa-side LCG (seed 20260512) for permutations** is a simple 32-bit multiplicative recurrence — adequate for shuffle determinism on n=50 elements. We did not benchmark against scipy.stats.permutation_test because the verdict is unambiguous at >4 OoM margin.

5. **The `prod` config null PASS (z=2.64, p=0.01) is intriguing but not actionable** — it's seed-fragile (prod_seed2 z=0.86) and its absolute magnitude (1.8e-5) is irrelevant to F-PERSONA-4's 0.5-nat acceptance bar. We report it for honest discoverability and to warn future investigators against repeating the §A2 z-score artifact (real signal at noise-floor magnitude).

6. **Memory cap lifted via `HEXA_MEM_UNLIMITED=1`** — prod config (d=384, cells=64) needs ~768 MB RSS for 5 cell pools + per-cell engine_a/g weight farrs + scratch. This is well within Mac local budget but does cross the default hexa runtime guard. Not a portability concern (env-toggleable, documented in run command).

7. **F-PERSONA-2/3/5 are NOT re-measured** in this harness — PSCC §40/§42 verdicts carry. §49 ablates ONLY the F-PERSONA-4 path. The aggregate cond #3 verdict (STRONG 4/5) is unchanged by this BG.

---

## §8 ARTIFACT MANIFEST

```
state/anima_d3_per_session_pool_2026_05_12/
├── anima_persona_4_per_session_pool_verify.hexa     (28 KB harness, ~580 LoC)
├── per_session_pool_results_base.json               (d=64,   cells=8,  seed=20260512)
├── per_session_pool_results_prod.json               (d=384,  cells=64, seed=20260512)
├── per_session_pool_results_prod_seed2.json         (d=384,  cells=64, seed=99999)
├── per_session_pool_run_base.log                    (text log replay)
├── per_session_pool_run_prod.log
└── per_session_pool_run_prod_seed2.log
docs/anima_persona_4_per_session_pool_verify_2026_05_12.md  ← THIS DOC
```

**RUN COMMANDS (reproducibility)**:

```sh
# base config — PSCC §40 byte-parity
RESOURCE_LOCAL_HEXA=1 __HEXA_FARR_GAUSS_SEED__=20260512 \
  PSPV_D_MODEL=64 PSPV_N_CELLS=8 PSPV_TAG=base \
  hexa run --no-sentinel \
    state/anima_d3_per_session_pool_2026_05_12/anima_persona_4_per_session_pool_verify.hexa

# prod scale — d=384 cells=64
RESOURCE_LOCAL_HEXA=1 HEXA_MEM_UNLIMITED=1 __HEXA_FARR_GAUSS_SEED__=20260512 \
  PSPV_D_MODEL=384 PSPV_N_CELLS=64 PSPV_TAG=prod \
  hexa run --no-sentinel \
    state/anima_d3_per_session_pool_2026_05_12/anima_persona_4_per_session_pool_verify.hexa

# prod scale — seed perturbation check
RESOURCE_LOCAL_HEXA=1 HEXA_MEM_UNLIMITED=1 __HEXA_FARR_GAUSS_SEED__=99999 \
  PSPV_D_MODEL=384 PSPV_N_CELLS=64 PSPV_TAG=prod_seed2 \
  hexa run --no-sentinel \
    state/anima_d3_per_session_pool_2026_05_12/anima_persona_4_per_session_pool_verify.hexa
```

---

## §9 CROSS-LINK

- **GOAL.md cond #3 D3 row** — verdict updated `path (d) FALSIFIED 2026-05-12 PSCC §49`
- **PASS_STRICT_SPONTANEOUS_CHAT.md §49** — saga history append (this BG)
- **REBORN §89** — hexa-native serve-time hook spec (path (d) source-of-truth)
- **D4c CLI spec** `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` Phase 1 (session cell-pool persistence — would still be useful for D4c chat sessions, just not as F-PERSONA-4 cond #3 lever)
- **PSCC §40** — pre-cotrain single-pool baseline (`mean_KL = 9.74 × 10⁻⁵`)
- **PSCC §44** — F-PERSONA-4 cotrain KL=0.0 first observation (winner-take-all root)
- **PSCC §45** — z-score §A2 metric FALSIFIED via null-permutation test (artifact lesson carried over to this BG)
- **PSCC §45-FINAL** — M4 aggregated hidden cosine z=3.20 PASS on v2 cotrain (cond #3 ☑ alternative metric path live)
- **PSCC §47** — softmax τ sweep ubu-1 FALSIFIED
- **PSCC §48** — per-cat corpus SMALL ubu-2 FALSIFIED
- **PSCC §49** ← **THIS BG**

---

## §10 NEXT ACTIONS (post-§49)

1. **cotrain v2 H100 lane** (PSCC §45 in-flight) — only path remaining at this point. If v2 PASSES F-PERSONA-4 KL ≥ 0.5 → cond #3 ☑.
2. **F-PERSONA-4 metric amendment** (PSCC §45-FINAL §7) — adopt M4 aggregated cosine z>3.0 as alternative cond #3 ☑ criterion. v2 ckpt already has z=3.20.
3. **Architectural fix** (D4 lane) — Gumbel-softmax or load-balanced MoE on the routing softmax (combine_outputs). Would require mitosis_hook.hexa edit + cotrain re-fire. Cost: $30-40 H100.
4. **D4c CLI session cell-pool persistence** — not a cond #3 lever but still useful for multi-conversation continuity. Phase 1 spec at `docs/anima_cli_mitosis_integration_spec_2026_05_12.md`.

---

**End of §49 audit. cond #3 D3 STRONG 4/5 carry MAINTAINED. 5-cond aggregate 4/5 ☑ MAINTAINED.**
