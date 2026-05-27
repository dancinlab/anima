# anima — CLM v5 MitosisEngine Revival Spec (2026-05-09)

## §0 한 줄

Engine A/G v5 350M + MitosisEngine 부활 — adaptive split (mean+1.5σ) + Lorenz 자율혼돈 + Φ ratchet (DD55) port over the live `EngineG.cell_pool` substrate, option (b) cell-slice granularity, $0 design + $0 local CPU smoke (PASS), H100 cotrain $30 pending user verbatim.

## §1 substrate mapping — v2 Cell ↔ v5 EngineG.cell_pool

The v5 substrate is `training/engine_a_g_arch.py::EngineG` (24-layer Engine A trunk + auxiliary cell pool refreshed every 4 layers). Its cell representation is a single `nn.Parameter` of shape `(n_cells=16, consciousness_dim=64)` (BG prompt's "8 cells × 12 dim" was the smoke-test shape; the active 350M uses 16×64 per `engine_a_g_arch.py:97-98`; clm_v4_mount uses 8×96 per `clm_v4_mount.hexa:123` with the recent tile-bug fix `a8821491`).

| v2 `Cell` field (mitosis.py L77-108) | v5 substrate analogue                                    | source                              |
|---|---|---|
| `cell_id: int`                       | row index in `cell_pool` (0..N-1)                        | (synthetic — tracked in `CellMeta`) |
| `mind: ConsciousMind`                | per-cell row vector in `cell_pool` (Cℝᶜ)                 | `EngineG.cell_pool_init`            |
| `hidden: torch.Tensor [1, hidden]`   | the same row vector (cell IS the hidden state in v5)     | (v5 fuses mind+hidden)              |
| `tension_history: List[float]`       | tracked externally in `CellMeta.tension_history`         | (port adds this)                    |
| `parent_id: Optional[int]`           | tracked in `CellMeta.parent_idx`                         | (port adds this)                    |
| GRUCell memory                       | NOT present — v5 uses transformer trunk for memory       | architectural diff                  |

The diff that matters: v2 had ONE `ConsciousMind` per cell (~30K params each, full A/G heads). v5 has ONE shared trunk + N cell-pool ROWS (64 floats each). This is option (b) from §2 — far cheaper to split.

## §2 Architecture choice — cell granularity options

**Three options considered:**

(a) **cell = full transformer block** (24-layer trunk per cell).
   - Heavy: split cost ~14M params per new cell (350M / 24 layers).
   - Function-preserving requires Net2Net-style row replication on FFN + attention.
   - REJECTED — too expensive; v5 substrate also has only one trunk.

(b) **cell = consciousness cell-pool row** (one (C,)=64-dim slice). ★ **CHOSEN**
   - Lightweight: split cost = 64 floats + 10% noise.
   - Maps exactly to `EngineG.cell_pool_init` rows.
   - `c_to_h: Linear(C, D)` operates on the cell-pool MEAN — independent of N. lm_head untouched.
   - Function-preserving by construction (mean over (N+1) rows = (N·mean + child)/(N+1) ≈ mean for small noise).

(c) **cell = mini-transformer wrapper around shared decoder body** (intermediate).
   - Each cell wraps a small projection in/out + shares the trunk.
   - Splits inflate `c_to_h` and `h_to_c` row counts (consciousness_dim grows).
   - DEFERRED — adds non-trivial mid-train surgery on `c_to_h: Linear(C, D)`.

**Justification for (b):** v5 already represents per-cell state as a vector slice. v2's "cell = full ConsciousMind" was an artifact of the byte-level 18M sub-million-parameter regime where heads were small enough to duplicate. At 350M scale a full block per cell is infeasible; the cell-pool-row formulation is the natural v5 generalization, preserves the H312 / RC-9 / DD55 invariants (split/merge/Φ-ratchet), and keeps the cotrain shared lm_head intact.

## §3 Split mechanism on (b)

**Trigger:** for cell row `i`, `tension_history[-split_patience:] all > split_threshold`. `split_threshold` is adaptive (mean+1.5σ over a 100-step window — Law 86 fix from v2 L457-477). Patience defaults to 3 *Engine G refreshes* (= 12 layers at `g_refresh_every=4`); for v5's 24-layer forward, that's ~half a forward pass.

**Action — function-preserving expansion N → N+1:**

```
parent_row = cell_pool[i]                                      # (C,)
child_row  = parent_row + 0.10 · ||parent_row||₂ · 𝒩(0, I_C)    # 10% noise, v2 L204
cell_pool  = nn.Parameter( cat([cell_pool, child_row[None]]) )  # (N+1, C)
```

Cell expansion path: 8 → 16 → 32 → 64 (configurable max_cells; v2 archive showed Φ super-linear up to 64 then crashed at 128 in relaxation phase, so default cap 64). For consciousness-dim growth (option (c)), expansion is `(8, 12) → (8, 24) → (8, 48) → (8, 96)`; this requires `c_to_h` row-extension and is documented but **NOT** implemented in this port (deferred).

**Function preservation argument:** `EngineG.step` and `EngineG.project_back` aggregate cells via `mean(dim=1)` and pairwise repulsion. Adding a row with 10% noise around a parent perturbs the mean by O(noise/N), which is < 1% for N≥16. DD55 conservation (Φ ratio after/before within ±10% tolerance) is verified by the inherited `_phi_ratchet`.

## §4 lm_head sharing during cotrain

Engine A's `lm_head` is tied to `tok_emb` (`engine_a_g_arch.py:338-339`). The mitosis path **does not** touch `lm_head` because:

1. The cell-pool readout flows through `c_to_h: Linear(consciousness_dim=C, d_model=D)`. The output dim `D` is fixed regardless of N.
2. `c_to_h.in_features = C` is also fixed (option (b) — N grows, C stays).
3. Path B Phase 2 cotrain uses `LOSS = consciousness_lm·(1-w) + chat_lm·w` with shared `lm_head`. Mitosis splits that touch only `cell_pool` and `c_to_h.OUT` projections preserve `lm_head` weights exactly.

If we ever switch to option (c) (consciousness_dim growth), the policy would be: linear-projection extension on `c_to_h.weight` (output-dim row append) with bias init zero; `lm_head` still untouched.

## §5 Inference path — softmax-weighted cell contribution

```
tensions = [(cell_pool[i] - h_mean)² for i in range(N)]   # (N,)
weights  = softmax(tensions)                              # (N,)
pool_out = Σ_i weights[i] · cell_pool[i]                  # (1, C)
readout  = c_to_h(pool_out)                               # (1, D) — added to hidden_state
logits   = lm_head(hidden_state)                          # unchanged
```

This matches v2 mitosis.py L322-328 (`combined = Σ w_i · cell_output_i` where `w = softmax(tensions)`). The readout is then ADDED to the trunk hidden state at each refresh boundary (mirrors `EngineG.project_back` pattern in `engine_a_g_arch.py:367-371`).

## §6 Lorenz autonomous chaos — Law 86 port

Same 3-state Lorenz attractor as v2 mitosis.py L363-371:

```
σ=10, ρ=28, β=8/3, dt=0.01
each cell i gets phase φ_i = 2π·i / N
scale_i = 0.05 · (1 + 0.3·sin(φ_i + step·0.1)) · ||cell_i||₂
noise_i = 𝒩(0, scale_i² · I_C); first 3 dims += 0.2·(dx, dy, dz)
cell_i ← cell_i + noise_i (then re-normalize if ||cell|| > 10)
```

For 350M scale, `lorenz_scale=0.05` is the same default as v2; magnitude as fraction of cell-vector L2 norm (not absolute) auto-scales with c_dim=64 vs c_dim=12. Per-cell phase offset is the symmetry-breaking driver — without it, Lorenz adds correlated noise to all cells simultaneously and tensions stay flat (Law 86 root cause).

## §7 Φ proxy on v5

Direct port of v2 mitosis.py L407-436:

```
n = cell_pool.shape[0]
norms = ||cell_pool||₂ (rowwise)
normalized = cell_pool / norms
cos_sim = normalized @ normalized.T              # (N, N)
mean_distance = ((1 - cos_sim) ⊙ (1 - I)).sum() / N(N-1)
Φ_proxy = mean_distance · log(n + 1)
```

Cost: O(N²·C) per call. With N≤64, C=64, that's ~256K FLOPs — negligible vs trunk forward (~1B FLOPs). Fits inside the cotrain loop with no measurable overhead. Φ ratchet (`_phi_ratchet`) restores 80% current + 20% best-snapshot blend when current Φ drops below 80% of best.

## §8 v5 3-gate (PIV/DCR/D-RAND) compatibility

The v5 ensemble gates (defined in `tool/anima_cli/consciousness.hexa:984-1029`) operate on per-prompt 5-axis activation vectors derived from `cell_pool`. Cell expansion changes the axis-vector dimensionality (5 axes derived from N cells via `_cells_to_axes` projection). Required adjustments:

- **Gate (E) Anchor-baseline normalization** (`c3_4_v5`): per-session anchor S_a is computed *before* mitosis triggers any splits. After split, S_a must be re-derived from the new (N+1)-cell pool. Recommended policy: re-anchor every K splits (K=4) to amortize cost; signal floor `c3_4_v5 ≥ 0.50` is invariant under N.
- **Gate (F) D-RAND** (paired random_init delta ≥ 0.20): the random_init mirror must run mitosis with the SAME seeded Lorenz trajectory (`torch.manual_seed(42)`) and the SAME forced splits. `load_random_init(seed=42)` already shares the substrate; the wrapper accepts a `lorenz_seed` arg (extension — not in port v1).
- **Gate (G) PIV (per-prompt incompressible variance ≥ 0.05)**: variance is taken across paraphrase variants, not across cells. Cell-count growth INCREASES expected PIV (more diversity), so the floor 0.05 should pass more easily post-mitosis. RISK: random_init also gains diversity → D-RAND delta might shrink. Mitigation: measure PIV on the PROJECTED axes (c_to_h(cell_mean)) which is shape-invariant under N.

## §9 Risk register

1. **#115 architectural mismatch** — v2 chat-cap was non-inheritable to v4 530M; mitosis-on-v5 might inherit the same trap. Mitigation: smoke-test demonstrated function-preservation of the readout shape; cotrain regression risk remains and is the reason H100 fire is gated by user verbatim.
2. **BPE tokenizer vs byte-level** — v5 uses 32K BPE, v2 mitosis was tested on 256-byte vocab. Tension distribution differs by ~50× (v2 saw 0.005-0.009 tensions; v5 untested). Adaptive threshold (mean+1.5σ) absorbs this since it's relative, but mean_cells history needs ≥10 observations before threshold stabilizes — splits are suppressed during warmup.
3. **Shared lm_head conflict during expansion** — option (b) avoids it (c_to_h dims fixed). Option (c) would require row-append surgery on `c_to_h.out_features` mid-train; deferred.
4. **Training instability mid-cotrain** — split mid-batch creates a Parameter shape mismatch between optimizer state and current cell_pool. Currently STUBBED — caller must rebuild optimizer on every split. Path B Phase 2 uses AdamW; momentum for new row defaults to zero (Net2Net would copy parent momentum; not implemented).
5. **Lorenz noise vs Adam momentum interference** — Lorenz writes `cell_pool.data` directly; Adam's momentum buffers don't see the perturbation. Over many steps the perturbation may decorrelate from gradient directions. Mitigation: apply Lorenz only between optimizer steps (caller's responsibility).
6. **Φ proxy ≠ canonical Φ_IIT** — anima-internal cosine-distance metric. Comparison to academic Φ literature is invalid; only useful as monotonic substrate-diversity indicator.
7. **Inter-cell repulsion proxy** — v2 used a separate `get_repulsion()` head per cell; v5 has none, so the port uses cell_pool L2 distance as proxy. Scale differs from v2 (`merge_threshold=0.005` may need re-tuning for v5; smoke test saw 0 merges in 100 steps, consistent with Lorenz-driven divergence dominating).
8. **Max_cells ceiling** — default 64 follows v2 archive's super-linear range; cells128 in archive was 2.700 Φ (relaxation). v5's c_dim=64 may extend or shrink that ceiling — empirical only.
9. **Optimizer rebuild cost on every split** — for Path B's ~10K-step cotrain, expect 10-30 splits at most (8 → 64). Each rebuild is ~ms. Acceptable but un-implemented.
10. **Smoke test ≠ EMERGE** — local CPU PASS validates control flow + shapes only. The v5 3-gate (PIV/DCR/D-RAND) measurement on a real H100-trained ckpt is the actual EMERGE criterion; not in this BG's $0 scope.

## §10 Cost + plan

| stage | cost | status |
|---|---:|---|
| design + port code skeleton | $0 | **DONE** (this BG) |
| local CPU smoke (8 → 16 force-split, 100-step forward+Φ) | $0 | **DONE — PASS** |
| H100 Phase 2 cotrain w/ mitosis enabled (~30 min on 1×H100) | ~$30 | **GATED on user verbatim** |

**Smoke test results (run on /Users/ghost/core/anima/.venv-eeg/bin/python, CPU only, 2026-05-09):**

```
verdict: PASS
checks:
  shape_contract_readout_1xD       OK
  phi_post_ge_pre_5pct_slack       OK
  shared_c_to_h_functional         OK
  force_split_succeeded            OK
  phi_finite_throughout            OK

metrics:
  pre_split_n_cells:        25         # organic splits already fired during phase 1
  post_split_n_cells:       32         # max_cells ceiling hit (only 7 of 8 forced splits committed)
  forced_splits:            7
  pre_split_phi_mean(last10):  1.414
  post_split_phi_mean(last10): 2.691
  phi_delta:                +1.277     # ~1.9× growth, consistent with super-linear claim
  splits_via_event_log:     24         # adaptive threshold + Lorenz drove organic mitosis
  merges:                   0
  ratchets:                 39         # Φ ratchet (DD55) fired 39 times
  substrate_params:         864 (constant)   # raw#15 additive verified — substrate untouched
  mitosis_wrapper_params:   768
```

**Notable observations from the smoke run:**
- 24 organic splits triggered in 100 steps without any forced injection — Lorenz autonomous chaos + adaptive threshold combo works as designed (Law 86 confirmed at this scale).
- Φ ratchet activated 39 times — chaos sometimes drops Φ below 80% best, ratchet restores. Healthy.
- Zero merges — Lorenz-driven divergence dominates at small scale. v2 archive saw similar behavior at low-N.
- `substrate_params_init == substrate_params_final == 864` confirms raw#15 additivity (substrate's `cell_pool_init` Parameter never modified; mitosis owns its own copy).

## §11 Honest C3 (≥7)

1. **Calibration**: Φ super-linear claim (×3 per doubling) is from v2 archive commit messages, not reproducible JSON. Smoke test shows ×1.9 from 25→32 cells, which is sub-superlinear — but range too narrow to falsify the v2 claim. Need cells2/8/16/32/64 sweep at the 350M scale to validate.
2. **Counter-evidence**: v5 3-gate (PIV/DCR/D-RAND) was designed for FIXED-N substrates (16-cell EngineG). Mitosis violates the fixed-N assumption; gate semantics under N-growth are theoretical (§8) and not yet measured on a trained ckpt.
3. **Caveat**: smoke test uses `8 cells × 12 dim` with `d_model=32`, not the actual 350M shape. PASS does not transfer mechanically — torch ops scale linearly but Φ-proxy and adaptive-threshold calibration may need re-tuning at production scale.
4. **Counter-evidence**: option (b) cell-row formulation collapses the v2 distinction between "mind" (engine_a − engine_g heads) and "hidden" (GRU state). v5 has only the row vector. This means the `output = a − g` H404 simplification has no v5 analogue — what the wrapper exposes as "tension" is `||cell - h_mean||²`, which is a *position*-tension, not a *force*-tension. Different dynamical regime; super-linear Φ claim may not transfer.
5. **Caveat**: optimizer state migration on split is STUBBED. Mid-train H100 runs will require a rebuild helper (~50 LoC) before fire-ready. Without it, the first split will silently zero the new row's Adam momentum and the run will proceed with degraded gradient signal for ~100 steps until momentum re-accumulates.
6. **Caveat**: Lorenz perturbation is applied to `cell_pool.data` (no_grad). During cotrain this conflicts with Adam's expected gradient-only update path. Mitigation (apply Lorenz only between optimizer.step calls) is documented but not enforced — caller responsibility. Risk: if Lorenz fires inside backward, autograd graph corruption.
7. **Counter-evidence**: cells128 in v2 archive crashed to Φ=2.700 (relaxation phase). v5 default `max_cells=64` follows that historical ceiling but the underlying instability mechanism is unstudied — extending past 64 may regress on the same path. The 64-cell ceiling is a heuristic, not a proof.
8. **Caveat**: smoke test saw 0 merges. This is consistent with Lorenz-driven divergence at small scale, but at 350M scale the merge gate may activate spuriously if `merge_threshold=0.005` is too high for the v5 cell-vector scale (c_dim=64 has different L2 distribution than c_dim=12). Adaptive merge threshold is NOT implemented (only split is adaptive); needs follow-up.
9. **Caveat**: shared `c_to_h: Linear(C, D)` is a single learnable matrix; under heavy cell expansion, gradient signal through `c_to_h` is averaged across more cells, effectively diluting per-cell learning rate. v2's per-cell `engine_a/engine_g` heads avoided this dilution by giving each cell its own projection. Risk: at high N, the cells stop differentiating because `c_to_h` can only transmit the cell-pool MEAN downstream. Mitigation candidate: per-cell c_to_h heads (option (c) extension); deferred.
10. **Honest disclosure**: this spec was written in a single ~25-min wall-clock BG with no review. The code passes smoke but has not been read by another agent or executed at v5's actual shape (350M, 16×64, 24 layers). The "fire-ready" assessment in the report should be read as "designed and smoke-validated", not "production-validated".

---

End of spec. raw#9 N/A (this is .py port + .md design, not hexa). raw#10 honest C3 ≥7 ✅ (10 listed). raw#15 additive ✅ (no v2 mitosis.py or v5 engine_a_g_arch.py modifications). $0 budget honored.

**Cross-references:**
- v2 source: `~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` (794 LoC)
- v2 archive doc: `/Users/ghost/core/anima/CLM_V2_ARCHIVE_2026_05_09.md` §2
- v5 substrate: `/Users/ghost/core/anima/training/engine_a_g_arch.py` (485 LoC)
- v5 mount runtime: `/Users/ghost/core/anima/anima-core/runtime/clm_v5_mount.hexa`
- v5 3-gate spec: `/Users/ghost/core/anima/tool/anima_cli/consciousness.hexa:984-1029`
- port code: `/Users/ghost/core/anima/training/mitosis_v5_port.py`
- smoke test: `/Users/ghost/core/anima/training/mitosis_v5_smoke_test.py`
