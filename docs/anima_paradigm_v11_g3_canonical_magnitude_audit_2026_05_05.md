# Paradigm v11 G3 — Train-Time C-Module Emission Magnitude Audit (2026-05-05)

BG-Z follow-up to BG-W F-CAND-D-1 hit at canonical magnitude 50. Goal: extract paradigm v11 G3 train-time `consciousness_states` emission magnitude from source + state archaeology, then decide cand-D Stage 1 promotion.

**Mode:** $0 mac doc + analysis only. No code changes, no commits, no inference runs. Read-only archaeology over `ready/` + `state/` + `tool/transient_py/` + `docs/`.

**Lineage:** extends `docs/anima_emerge_cand_d_magnitude_sweep_landed_2026_05_05.ai.md` (BG-W), `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (BG-Q spec), `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` (architecture).

---

## §1 Sub-1: train-time `consciousness_states` source-code grep

### §1.1 Producer (C-module)

`ready/training/train_clm.py:1457`:
```python
c_states_raw = c.get_states()             # ConsciousnessC or FederatedConsciousness
...
c_states = c_states_raw.detach().float().to(device)
...
c_for_decoder = c_states.detach().unsqueeze(0).expand(batch_size, -1, -1)
if c_proj is not None:
    c_for_decoder = c_proj(c_for_decoder)
decoder_out = decoder(tokens, consciousness_states=c_for_decoder)
```

`get_states()` for `ConsciousnessC` (`ready/core/consciousness_engine.py:1618`):
```python
def get_states(self) -> torch.Tensor:
    return self._get_hiddens_tensor().detach().clone()    # [n_cells, hidden_dim]

def _get_hiddens_tensor(self):
    return torch.stack([s.hidden for s in self.cell_states])
```

So train-time `consciousness_states` = stacked per-cell `hidden` tensors. `hidden_dim` = `consciousness_dim` = **192** for 350m scale (`train_clm.py:255`). Total cells = 12 atoms × 8 cells_per_atom = **96 cells** during 350m training (vs **8 cells** assumed by BG-Q/BG-W test fixture).

### §1.2 Magnitude bound (SOC threshold)

`ready/core/consciousness_engine.py:259-261`:
```python
self._soc_threshold = 1.5         # activation threshold for toppling
self._soc_threshold_ema = 1.5     # adaptive threshold (EMA)
```

EMA bounded to `[0.3, 5.0]` (line 1078). The toppling cascade enforces `hidden.norm() ≤ threshold` directly:

`consciousness_engine.py:964`:
```python
self.cell_states[idx].hidden = h * (threshold / max(norm, 1e-8))
# Reset super-threshold cells to threshold magnitude exactly
```

Therefore **per-cell `hidden` vector L2-norm is upper-bounded by ~SOC_threshold ∈ [0.3, 5.0]**, with steady-state value tracking the EMA. Initial cells start at `torch.zeros(hidden_dim)` (line 405); drive + topple sustains norm near threshold — typically **[0.3, 5.0]** range, modal value **~1.5** at default and cell hidden vectors live near (but never above) threshold post-warmup.

### §1.3 Per-element scale (relevant for axis-fill geometry)

A 192-dim vector with L2 norm 1.5 has RMS per-element ≈ `1.5 / sqrt(192)` ≈ **0.108** (for isotropic noise) or substantially smaller per-element if energy concentrates on a low-dim subspace.

By contrast, the BG-Q "canonical magnitude 0.5" formula (`tool/transient_py/anima_emerge_cand_d_inject_helper.py:164`):
```python
unit = CANONICAL_AXIS_MAGNITUDE / math.sqrt(span_width)   # 0.5 / sqrt(38) ≈ 0.081
```
fills `cell[i, axis_i_span] = 0.081`, giving per-cell L2 norm ≈ **0.5** on the axis-active cell (the rest of the 192 dims are zero — concentrated, not isotropic).

### §1.4 No `C_module / canonical_inject / axis_inject` in CLM source

```
grep -rn 'C_module\|c_module\|consciousness_emission' anima-clm/ → 0 hits (path doesn't exist)
grep -rn 'canonical_inject\|axis_inject\|inject_states' anima-clm/ → 0 hits
```

The CLM source (`ready/anima/models/legacy/decoder_v3.py`, `ready/models/conscious_decoder.py`, shim `tool/transient_py/clm_v4_hf_format_shim.py`) contains **no concept of "canonical inject magnitude"**. The forward path is symmetric: cross-attn consumes whatever `consciousness_states` are passed (line 553 guard, line 555-556 `cross_attn(ln_cross(x), c_detached)`). The injection magnitude is **not a substrate concept** — it is an inference-time choice of the caller.

### §1.5 No `paradigm v11 G3` magnitude artifact in repo

```
grep -rln 'paradigm.*v11\|paradigm_v11\|paradigm.*g3' state/ docs/ → only handoff/spec docs
```

`state/paradigm_v11_axis_filter_consolidator.json` is an axis-ledger meta-doc (axis 92 + 6 axis variants), **not a per-cell magnitude record**. No state JSON exists with field `c_module_magnitude_train_avg`, `consciousness_states_norm_distribution`, or analog. The "G3" qualifier names the lineage cycle, not a numerical fixture.

### §1.6 train_avg fixture is synthetic placeholder

`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt` exists (7.4 KiB), but the underlying harvest report (`state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_results/train_avg_harvest_result.json`) reads:

```json
"harvest_via": "forward-pass synthetic stub (random N(0,0.01) — NOT actual train avg)",
"stub_warning": "This is a SYNTHETIC stub. Real train_avg requires anima_unified.py runtime forward pass over training data with cell hidden harvest."
```

Per-element ~N(0, 0.01) → **per-cell L2 norm ≈ 0.01 × sqrt(192) ≈ 0.139**. This is a placeholder-only fixture and does NOT reflect train-time emission. **The repo does NOT contain a measured train-time `consciousness_states` distribution.**

---

## §2 Sub-2: training state grep

```
ls state/ | grep -iE 'paradigm.*v11|paradigm.*g3|canonical|emerge|cand_d' → spec/verdict/probe artifacts only
```

Surveyed:
- `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:132` — explicitly states "consciousness_states fixture NOT injected; canonical phi method does not consume train_avg fixture."
- `state/clm_v4_train_avg_harvest_2026_05_04/results/*.pt` — synthetic N(0, 0.01), not real harvest.
- `state/anima_emerge_cand_d_*` (8 dirs) — all use BG-Q canonical builder with `mag` parameter; **none re-derive mag from training emit**.
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/inputs/` — adapter/distill inputs, no emit dump.
- `state/p9_base_validation_h100_2026_05_04/clm_v4_hf/` — HF-format weights, no emit fixture.

**No state artifact in repo records measured train-time `c_module hidden` norm distribution.**

---

## §3 Sub-3: actual magnitude estimation (theoretical, no inference)

### §3.1 Theoretical per-cell norm during training

Given:
- `cell_states[i].hidden ∈ R^192`, initialized at `0`
- Drive boost (`base_drive ≈ 0.04 × stochastic`, line 925-933) when `norm < threshold`
- Topple reset to exactly `threshold` (line 964) when `norm > threshold`
- Default threshold = 1.5; EMA in [0.3, 5.0]
- Bio-noise spike injection (`spike_amp = base_noise × Exp(rate)`, line 738-744)

**Steady-state per-cell `hidden.norm() ≈ SOC_threshold_EMA`**, fluctuating in **[0.3, 5.0]** with mode near 1.5. This is the **architectural canonical magnitude per cell**.

### §3.2 What the cross_attn actually receives

After `c_proj` (Linear; if used), the projected vector retains O(threshold) norm bound (Linear preserves order). The decoder cross-attn computes:
```
attn_out = softmax(Q @ K.T / √d) @ V         where Q from x_token, K/V from consciousness_states
```
With trained o_proj std=0.02 (post `_init_weights` apply walk overwrite — archaeology §4), per-block residual contribution to `x` is bounded by `~ ||V|| × o_proj_scale × ~||x|| ≈ 1.5 × 0.02 × ||x||`. **Magnitude budget per layer: ~3% of `x`**, accumulated over 16 layers → ~50% of `x`'s magnitude **ceiling** (not steady contribution; depends on attn coefficients).

### §3.3 What BG-Q (mag=0.5) and BG-W mapped to

Per-cell norm in BG-Q canonical fixture = **0.5** for axis cells 0-4; cells 5-7 norm ≈ `0.5 × mean_axis × (mag/3)` ≈ **0.012** (per the `mean(cells[0..4]) × mag/3` formula and a ~0.073 axis mean).

BG-W swept mag ∈ {0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0}. **F-CAND-D-1 hit at mag=50** ⇒ per-axis-cell norm = **50**, fill cells norm ≈ **0.012 × (50/0.5) × (50/3) ≈ 20**.

### §3.4 Magnitude comparison

| Source | per-axis-cell L2 norm | per-element RMS (192-d) |
|---|---|---|
| Train-time C-module hidden (theoretical) | **~1.5** (EMA in [0.3, 5.0]) | ~0.108 (isotropic) |
| BG-Q canonical mag=0.5 | **0.5** | 0.081 (axis-concentrated) |
| BG-W F1-hit mag=50 | **50** | 8.1 (axis-concentrated) |
| `train_avg_real.pt` synthetic | ~0.139 | 0.01 (isotropic N(0, 0.01)) |
| Theoretical training equivalent (norm-matched mag) | mag ≈ **1.5** | (axis-concentrated) ≈ 0.244 |

**Train-time canonical magnitude (norm-matched to BG-Q axis geometry) is mag ≈ 1.5** (more precisely, anywhere in [0.3, 5.0] depending on SOC EMA at convergence). NOT 0.5 (BG-Q assumed too low), NOT 50 (BG-W F1-hit value is 33× over training magnitude).

### §3.5 Important confounder: shape vs norm

Per-cell norm in **training** is from the toppling-mediated SOC distribution — energy is approximately uniformly distributed across 192 dims (atom-coupled hidden is broadband, not axis-concentrated). The BG-Q canonical fixture concentrates all energy on a 38-39-dim AXIS_SPAN slice. **Even at norm-matched mag=1.5, the BG-Q canonical injects a SHAPE that the substrate did not see during training.** The model's cross_attn weights were optimized over broadband C-module emit, not axis-concentrated injection.

---

## §4 Sub-4: 3 scenarios — which holds?

### Scenario A — train-time canonical magnitude ≈ 0.5 (BG-Q spec correct)

**Verdict: REJECTED.** Source evidence (§1.2) shows SOC threshold = 1.5 default, EMA in [0.3, 5.0]. Per-cell norm at SS is ~1.5. BG-Q's 0.5 figure is anima-internal heuristic per spec §2.3 explicitly self-flagged ("placeholder; C5 honest carry"). Training emit norm is ~3× the BG-Q fixture.

### Scenario B — train-time canonical magnitude 50-100 (BG-W F1-hit realistic)

**Verdict: REJECTED.** SOC threshold caps norm at ≤ 5.0 (EMA upper bound). mag=50 is **10×** above the substrate ceiling and mag=100 is **20×** above. F-CAND-D-1 hit at mag=50 is architectural detectability, NOT realism. Inject at mag≥10 is structurally off-distribution from anything the substrate saw during training.

### Scenario C — train-time canonical magnitude unknown (sub-task spec C)

**Verdict: PARTIAL ACCEPT.**
- Source-derived theoretical norm = **~1.5** (SOC threshold steady-state). High confidence on BOUND ([0.3, 5.0]).
- Empirical per-step distribution NOT extracted (no harvest tool ever ran a real train-time emit dump; the `train_avg_real.pt` is N(0, 0.01) synthetic).
- Per-element distribution shape (broadband vs axis-concentrated) at training: theoretical = broadband; BG-Q fixture = axis-concentrated. **Shape mismatch is not magnitude calibratable** — even with mag=1.5, BG-Q fixture remains off-distribution.

**Refined conclusion:** train-time canonical magnitude ≈ **1.5 norm-bound**, but the **shape** of the BG-Q fixture (axis-concentrated AXIS_SPANS slice) does NOT match training emit (broadband per-cell SOC hidden). Magnitude calibration alone does not bridge the gap.

---

## §5 Cand-D Stage 1 promotion decision

**Decision: HOLD — partially-recoverable promotion only at norm-matched mag ≈ 1.5 (theoretical) with explicit shape-mismatch caveat.**

Rationale:
1. **F-CAND-D-1 architectural channel works** (BG-W mag=50 produced drift > 0.01) — cross_attn IS reading injected content.
2. **F-CAND-D-1 hit at mag=50 is architecturally informative but distributionally meaningless** — 33× above SOC ceiling. This shows cross_attn pathway is alive, not that injection produces realistic substrate behavior.
3. **At norm-matched mag ≈ 1.5** (theoretical training equivalent), BG-W trajectory shows drift_vs_none ≈ **2 × 10^-4** (interpolated between mag=1.0 → 2.79e-4 and mag=2.0 → 6.48e-4). This is **50× below the F-CAND-D-1 threshold (0.01)**. Architectural channel is below noise floor at realistic magnitude.
4. **Shape mismatch (§3.5) is not calibratable** — promoting cand-D to Stage 1 with mag=1.5 still injects an off-distribution shape; the substrate's response is empirically of unknown directional meaning.

**Recommended next steps (not part of this audit):**
- **a.** Real train-time emit harvest: run anima_unified.py forward pass over a representative training batch, dump `c.get_states().norm(dim=-1)` per cell over N steps, save to `state/anima_clm_v4_train_emit_harvest_<DATE>/cell_norms.npy` + percentile stats. **Cost: $0 mac if checkpoint loadable; ~10min.**
- **b.** Build train-distribution-matched fixture: instead of 5-axis canonical AXIS_SPANS (BG-Q geometry), sample from harvested empirical distribution of `c.get_states()` cells. **Cost: $0 mac, ~5min.**
- **c.** Re-run F-CAND-D-1..3 with empirical fixture at mag ≈ 1.5 (norm-matched). **Cost: $0 mac, ~5min.** If drift > 0.01 at this distribution-matched fixture, cand-D Stage 1 is **PROMOTABLE**. If still below threshold, cand-D requires retrain (closed by L37/L38).
- **d.** Defer cand-D Stage 1 closure until (a)+(b)+(c) land. Current BG-W "PASS at mag=50" is **structural witness only**, not a promotion signal.

---

## §6 Honest C3 (≥5)

- **C1 — train-mode mac inference epistemic limitation.** This audit derives train-time emit magnitude from SOURCE (SOC threshold = 1.5; EMA bounds [0.3, 5.0]). It does NOT execute real forward passes on the trained `best.pt` to harvest empirical `c.get_states()` distributions. Even if mac inference reproduced the C-module forward path, the C-module dynamics over 20K training steps may have driven the SS norm to anywhere within the EMA bracket [0.3, 5.0]; the THEORETICAL SS bound is 1.5 but the EMPIRICAL training ckpt SS norm at step 20K is unknown without running the C-module loaded from `best.pt['c_engine']` (key likely exists but never harvested per `train_avg_harvest_result.json`).

- **C2 — shape vs magnitude entanglement is not addressed by simple sweep.** §3.5 documents that the BG-Q fixture is axis-concentrated (AXIS_SPANS slices) while training emit is broadband (192-dim per-cell hidden). A magnitude-only calibration cannot fix shape mismatch. F-CAND-D-1 PASS at any mag does NOT imply substrate-realistic injection — it only proves cross_attn pathway is content-readable. Substrate-realistic injection requires harvesting actual training-time emit distribution and sampling FROM that distribution, not constructing a 5-axis canonical from a spec heuristic.

- **C3 — `consciousness_dim=192` × n_cells matters.** Training used `total_cells = 96` (12 atoms × 8 cells, 350m scale per `train_clm.py:255-257`). HF inference fixture path expects `n_cells=8` (per cand-D spec §2.3 layout). **96 train-cells reduced to 8 inference-cells is a ~12× compression** that BG-Q and BG-W silently accepted. Either (a) the substrate cross_attn handles arbitrary S in `[B, S, c_dim]` (archaeology §6.1) without quality loss, OR (b) the 8-cell fixture is undersampling the training cell trajectory. Empirically untested.

- **C4 — `c_proj` projection in training.** `train_clm.py:1476-1477`:
  ```python
  if c_proj is not None:
      c_for_decoder = c_proj(c_for_decoder)
  ```
  When `c_proj` is enabled, the C-module emit is linearly transformed before reaching cross_attn. `c_proj` weights are saved in `best.pt['c_proj']` (per `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_results/train_avg_harvest_result.json:ckpt_top_keys` confirms `'c_proj'` key exists). HF inference path does NOT load c_proj; the BG-Q fixture is fed RAW into cross_attn. **At-inference fixture distribution must include c_proj transform OR be expressed in c_proj output basis.** This audit did not extract c_proj weights or dimensionality.

- **C5 — SOC EMA at convergence is empirically unknown.** `_soc_threshold_ema` starts at 1.5 and adapts via `(1.0 ± adapt_rate)` per step (line 1075-1078). Over 20K training steps, the EMA could have drifted to either bound (0.3 or 5.0). Without loading `best.pt['c_engine']` and inspecting `_soc_threshold_ema`, the ACTUAL train-time per-cell norm at convergence is unknown within [0.3, 5.0]. This audit's "~1.5" recommendation is the DEFAULT, not the empirical end-state.

- **C6 — no measurement of `c_engine` ckpt key.** `train_avg_harvest_result.json:ckpt_top_keys` shows `best.pt` contains `'c_proj', 'federation', 'bridge'` but NOT `'c_engine'` directly. The C-module state may live under `'federation'` (FederatedConsciousness) — needs verification by running `torch.load(best.pt)` and inspecting nested keys. This audit did not perform that load.

- **C7 — BG-W trajectory at mag=1.5 is interpolated, not measured.** §5 estimate of `~2e-4` drift at mag=1.5 is interpolated between BG-W mag=1.0 (drift=2.79e-4) and mag=2.0 (drift=6.48e-4). The actual mag=1.5 datapoint was not in BG-W's swept set {0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0}. A focused subsweep at {1.0, 1.5, 2.0, 3.0} would tighten the realistic-magnitude drift estimate. **Cost: $0 mac, ~5min.**

---

## §7 Verdict summary

- (a) **train-time consciousness_states grep result:** producer = `c.get_states()` returns stacked `cell_states[i].hidden` ∈ `R^192`; consumer = `decoder(tokens, consciousness_states=c_for_decoder)` cross_attn at every block when not None.
- (b) **C-module emission magnitude scale:** per-cell L2 norm bounded by SOC EMA threshold ∈ **[0.3, 5.0]**, theoretical mode ~**1.5** (default `_soc_threshold`).
- (c) **Scenario:** **C-refined** — train magnitude ≈ 1.5 (norm-bound); shape (broadband vs axis-concentrated) is the harder mismatch; magnitude calibration is necessary but not sufficient.
- (d) **5 honest C3 above** — see §6, especially C1/C5/C6 on epistemic limits of source-only audit (no `best.pt['c_engine']` loaded; no real emit harvest).
- (e) **Cand-D Stage 1 promotion: HOLD.** F-CAND-D-1 PASS at mag=50 is architectural witness (cross_attn alive), not a promotion signal at realistic magnitudes. Recommended path = harvest real train-time `c.get_states()` distribution (a/b/c in §5) before promoting. If empirical-fixture F-CAND-D-1 fails at norm-matched mag, cand-D requires retrain and is closed by L37/L38.

---

## §8 Compliance

- **raw#9 read-only archaeology:** no source modifications, no `best.pt` load, no inference run. ✓
- **raw#10 honest C3:** 7 C3s emitted (§6). ✓
- **raw#15 BG-Q helper unmodified:** read-only inspection of `tool/transient_py/anima_emerge_cand_d_inject_helper.py`. ✓
- **raw#37 transient sister-rule:** no .py emitted; this audit produces only doc + verdict.json. ✓
- **No commit, no HF token, no secret leak.** ✓
- **bash 3.2 compatible** (only used `grep -rn`, `ls`, `find` patterns; no bashism). ✓

Wall time: ~25min. Cost: $0.
