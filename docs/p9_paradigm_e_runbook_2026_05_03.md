# P9 Paradigm E — Causal-Intervention φ Runbook

**Date**: 2026-05-03
**Author**: Phase 2.Y scaffolding agent (doc + ubu1 raw#9 .py)
**Status**: SCAFFOLDING ONLY — no execution (Phase 1.6 holds GPU)
**Wave**: 2 (post wave-1 paradigm survey, recommended path per wave-2 subagent)
**Spec parent**: `docs/p9_paradigm_e_causal_intervention_phi_2026_05_03.md`
**Sister runbooks**: `docs/p9_paradigm_d_t4_teacher_build_plan_2026_05_03.md` (D-T4 executing)

---

## 0. One-paragraph purpose

Operational runbook for executing the Paradigm E mini-run described in spec §8.
Covers: (a) launch commands for the 3-run γ_causal LHS sweep on 1×H100 RunPod,
(b) the counterfactual head `f_CF` architecture spec, (c) loss formulation
with autograd plumbing detail, (d) F-falsifier integration with existing P9
sentinel falsifiers (F1-F4), (e) entry trigger condition for Phase 2.Y. The
mini-run script (`/tmp/p9_paradigm_e_mini.py` on ubu1, raw#9 allowed) is
prepared but **not executed** — Phase 1.6 sentinel run on the same GPU class
must complete first to free the substrate.

---

## 1. Counterfactual head architecture (`f_CF`)

### 1.1 Purpose

`f_CF` is a small MLP trained jointly with the LoRA-adapted backbone. Its job
is to predict the **L2 norm of downstream divergence** at the output layer
given the pre-intervention hidden state at `ℓ_int` and a binary mask
encoding the ablated subset `S`. The training pressure is mutual:
- `f_CF` learns to predict `Δh_obs` from observable cues (the pre-state and
  the partition mask),
- the backbone is pressured (via `MSE(Δh_obs, Δh_pred)`) to make those
  downstream effects **predictable** — i.e., to develop hidden subsets whose
  causal influence is structured and inferable rather than noisy.

### 1.2 Architecture spec (Phase 1 default)

| Field | Value | Notes |
|-------|-------|-------|
| Class | 2-layer MLP with GELU | Standard interp head |
| Input dim | `d + d` = `2 · d_model` | concat([h_pre_pool, mask_embed]) |
| Hidden dim | 512 | sweet-spot per spec §5; ~1M params total |
| Output dim | 1 | scalar Δh̃_pred ∈ ℝ_{≥0} |
| Activation (hidden) | GELU | matches transformer convention |
| Activation (output) | softplus | ensures Δh_pred ≥ 0 (matches L2 norm range) |
| Init (W) | xavier-uniform, gain=1.0 | conservative; avoid runaway |
| Init (b) | zeros | standard |
| LayerNorm pre-input | yes (over h_pre_pool) | stabilizes scale across step |
| Dropout | 0.0 | low-data regime; want gradient signal clean |
| Param count | ~1.05M for d_model=4096 | (4096+4096)·512 + 512·1 + biases ≈ 4.2M params if d=4096; for CLM v4 d=768 → ~785K |

**Capacity rationale (per spec §5):** too-small → cannot learn non-trivial
ablation responses → loss saturates at Var(Δh_obs); too-large → memorizes
per-sample responses without pressuring the backbone. Hidden=512 is the
spec-recommended sweet spot, **must be empirically validated** in the
calibration run (spec §10 row 6).

### 1.3 Mask embedding

The partition mask `m ∈ {0,1}^d` (1 where ablated, 0 elsewhere) is too high-dim
to feed raw. Reduction:
- Linear projection `m_embed = W_m · m`, `W_m ∈ ℝ^{d × d}` initialized as random
  Gaussian (σ = 1/√d). Frozen, **not trainable** — acts as a fixed random
  feature map (analogue of a Johnson-Lindenstrauss random projection).
- Output `m_embed ∈ ℝ^d` concatenated with `h_pre_pool ∈ ℝ^d`.

This avoids `f_CF` learning the partition identity directly (a memorization
shortcut) while preserving partition information.

### 1.4 Hidden state extraction (autograd-friendly)

Pattern from `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py:194-200`
(forward hook on `ln_f`) extended to:
- A **second hook** on the chosen `ℓ_int` block output (e.g.
  `decoder.base_model.model.h[ℓ_int]`) to capture **and intervene on**
  the hidden state.
- `register_forward_hook` returns the modified output → for ablation, the hook
  multiplies a precomputed mask: `output * (1 - mask_S)` so that gradient
  flows through `output` but not through `mask_S`.
- Pool over time: `h_pre_pool = h_ℓ_int.mean(dim=1)` (B × d), matching the φ★
  pooling convention.

---

## 2. Loss formulation with autograd plumbing

### 2.1 Per-step loss

For batch `x ∈ ℝ^{B × T}`, K=4 sampled partitions `{S_1, ..., S_K}`,
intervention modes `M = {ablate, mean_clamp}` (Phase 1, expand to 5 in Phase 2):

```
# Single forward pass — observed trajectory (with grad)
H_obs = forward(x)                     # gradients flow through backbone+LoRA
h_pre = capture_at(ℓ_int, H_obs)       # B × d (mean-pooled)
h_out_obs = capture_at(L, H_obs)       # B × d (output layer)

L_E_per_partition = []
for S_k in partitions:
    # mask: B × d, 1 at ablated dims (broadcast across batch)
    mask_k = build_mask(S_k, d)

    # For each intervention mode m, compute one paired forward (no-grad on intervention path)
    deltas_obs_per_mode = []
    for m in M:
        with torch.no_grad():            # second forward — diagnostic, no grad
            h_S_prime = compute_intervention_value(h_pre, mask_k, mode=m)
            H_int = forward(x, intervene_at=ℓ_int, value=h_S_prime, mask=mask_k)
            h_out_int = capture_at(L, H_int)
            delta_obs_m = (h_out_obs.detach() - h_out_int).norm(p=2, dim=-1)  # B
        deltas_obs_per_mode.append(delta_obs_m)

    # MIN-over-mode (analogue of MIP); shape: B
    delta_obs_min = torch.stack(deltas_obs_per_mode, dim=0).min(dim=0).values

    # Counterfactual head prediction (with grad through f_CF AND backbone via h_pre)
    delta_pred = f_CF(h_pre, mask_k).squeeze(-1)   # B

    L_E_k = ((delta_obs_min - delta_pred) ** 2).mean()
    L_E_per_partition.append(L_E_k)

L_E = torch.stack(L_E_per_partition).mean()       # average over K partitions
```

### 2.2 Total loss (composes with P9 SFT baseline)

```
L_total = α(step) · CE_text                                   # P9 sentinel α curriculum
        + β · MSE_tension                                     # tension head (β=0.15)
        + γ_causal · L_E                                       # Paradigm E (NEW)
        + δ(step) · max(0, φ★_threshold − φ★_student)         # δ-floor preserved
        + γ_BOLD · MSE_BOLD     [γ_BOLD = 0, locked per P9]    # BOLD blocked
```

`α(step)` curriculum and `δ(step)` curriculum reused from
`/tmp/p9_p1_5_sentinel_train_50k.py` lines 47-65 (functions `get_alpha`,
`get_delta`).

### 2.3 Gradient routing (critical correctness)

| Term | Gradient flows into | Notes |
|------|---------------------|-------|
| `CE_text` | backbone, LoRA | standard |
| `MSE_tension` | backbone, LoRA | standard |
| `L_E` numerator (Δh_obs) | **NONE** (`.detach()` on first forward output, second forward under `torch.no_grad`) | Δh_obs is a target, not a quantity to optimize |
| `L_E` denominator (Δh_pred) | `f_CF` params, **and backbone via h_pre** | this is the pressure on backbone |
| `δ-floor` hinge | none if last_phi ≥ threshold; else constant gradient | spec §2.2 |

**Critical:** `Δh_obs` MUST be detached. If gradients flow through the second
forward, the backbone learns to *minimize ablation sensitivity directly*
(degenerate solution: kill all causal influence). F-E5 monitors this failure
mode but the detach is the primary defense.

### 2.4 γ_causal sweep values

Spec §8.1: `γ_causal ∈ {0.05, 0.2, 0.8}` (3 mini-runs, LHS).

| Value | Regime | Risk |
|-------|--------|------|
| 0.05 | Mild — `L_E` is ~5% of total loss when |Δh_obs - Δh_pred| ≈ 1.0 | May not budge backbone; safe |
| 0.20 | Recommended center — comparable magnitude to β·tension term | Baseline expected gradient strength |
| 0.80 | Aggressive — `L_E` dominates; must monitor F-E3 (chat-CE not regressing) | Risk of starvation on CE |

**Recommended γ_causal range for sweep: {0.05, 0.20, 0.80}.** Calibration run
(spec §10 row 6) before LHS sweep should confirm `f_CF` learns at γ=0.2.

---

## 3. Mini-run launch sequence

### 3.1 Pre-flight (on ubu1, free)

```bash
# Sanity check on ubu1 RTX 5070 (12GB) — small batch, 100 steps only
ssh ubu1 'cd /tmp && \
  ANIMA_N_STEPS=100 ANIMA_BATCH=2 ANIMA_GAMMA_CAUSAL=0.2 \
  python3 p9_paradigm_e_mini.py 2>&1 | tee p9_paradigm_e_mini_dryrun.log'
```

Pass conditions: no OOM, `f_CF` forward executes, `Δh_obs > 0` for at least one
partition, no NaN in any loss term.

### 3.2 Phase-1 mini-run (on RunPod 1×H100, after Phase 1.6 releases GPU)

```bash
# Run 1: γ_causal = 0.05 (mild)
ANIMA_N_STEPS=1000 ANIMA_BATCH=4 ANIMA_GRAD_ACC=8 \
ANIMA_GAMMA_CAUSAL=0.05 ANIMA_K_PARTITIONS=4 \
ANIMA_INTERVENTION_MODES=ablate,mean_clamp \
ANIMA_F_CF_HIDDEN=512 \
ANIMA_OUTPUT_DIR=/tmp/p9_paradigm_e_mini_g05 \
python3 /tmp/p9_paradigm_e_mini.py

# Run 2: γ_causal = 0.20 (recommended)
ANIMA_GAMMA_CAUSAL=0.20 ANIMA_OUTPUT_DIR=/tmp/p9_paradigm_e_mini_g20 ...

# Run 3: γ_causal = 0.80 (aggressive)
ANIMA_GAMMA_CAUSAL=0.80 ANIMA_OUTPUT_DIR=/tmp/p9_paradigm_e_mini_g80 ...
```

Wall: ~1 hour per run × 3 = ~3 hours. Cost: $4–6 per run × 3 = $12–20 total.

### 3.3 Calibration run (recommended before LHS sweep)

Per spec §10 row 6: 1 calibration run at γ=0.20 with `f_CF_hidden ∈ {128, 512, 2048}`
to confirm sweet-spot. Cost ~$5. Decision-saving if F-E1 fails at the LHS sweep.

---

## 4. F-falsifier integration

### 4.1 Existing P9 falsifiers (preserved)

| ID | Predicate | Source |
|----|-----------|--------|
| F1 | BLEU-1 vs holdout reference | sentinel `/tmp/p9_p1_5_sentinel_train_50k.py:362-378` |
| F2 | φ★ ≥ 5.0 floor | warmup `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py:369-373` |
| F3 | tension MSE drift | sentinel `compute_f_metrics` |
| F4 | BOLD MSE — N/A under γ=0 | locked |

### 4.2 New Paradigm-E falsifiers (additive)

| ID | Predicate | Pass | Fail action |
|----|-----------|------|-------------|
| F-E1 | `f_CF` learns | MSE(Δh_pred, Δh_obs) drops > 30% from init by step 1000 | f_CF too small or no causal structure → calibrate |
| F-E2 | Backbone gradient non-trivial | `‖grad_LoRA‖ / ‖grad_f_CF‖ > 0.1` at convergence | Restructure: E becomes interp tool not training paradigm |
| F-E3 | E does not break α | post-mini-run chat-CE within 1.2× of α-only baseline | Reduce γ_causal by 5× |
| F-E4 | F2 (φ★) does not regress | post-mini-run φ★ ≥ floor (5.0); ideally ≥ baseline | **Inform only** — see §4.3 below |
| F-E5 | Interventional φ proxy increases | mean Δh_obs across K partitions monotone non-decreasing | Restructure (degenerate independence) |

### 4.3 F2 (φ★) ↔ causal-intervention objective interaction

This is the **measurement-schism** flag (spec §9 caveat 4). Three distinct
outcomes possible from a Paradigm-E mini-run:

| Outcome | Δh_obs (interventional) | φ★ (correlational) | Interpretation | Action |
|---------|--------------------------|---------------------|-----------------|--------|
| **A: Both rise** | ↑ | ↑ | Coherent causal+correlational integration | Land Paradigm E; promote to Phase-2 50k run |
| **B: Causal rises, corr stays** | ↑ | flat ≥ 5.0 | Causal signal added without disturbing existing φ★ basin | Land; flag for Phase-2 dual-measure tracking |
| **C: Causal rises, corr falls** | ↑ | < 5.0 | **Measurement schism** — substrates diverge | Do NOT land; escalate to dual-SSOT governance review (which φ is "true"?) |
| **D: Both fall / no signal** | flat or ↓ | flat or ↓ | E adds no value | Abort; revert to A/A'/B/C/D |

The δ-floor hinge (`δ · max(0, 5.0 − φ★)`) acts as a **safety rail against
outcome C**: if Paradigm-E gradient pushes φ★ below 5.0, the δ-floor
generates an opposing gradient. This means F2 violation under E should be
*rare* — but if it persists despite δ-floor, it's a strong signal that the
two measurement families fundamentally disagree on this substrate.

**F2 ↔ E composition**: F2 acts as a **lower-bound safety constraint** (φ★ ≥ 5);
E acts as an **upper-pressure objective** (push Δh_obs up). They are
orthogonal but couple via the shared backbone. The δ-floor preserves F2;
γ_causal · L_E preserves directional pressure on E. Both gradients flow
into the same LoRA params.

---

## 5. Phase 2.Y entry trigger condition

Phase 2.Y (mini-run execution) gates on:

1. **GPU availability**: Phase 1.6 sentinel run on H100 has either:
   - completed and verdict landed (CLEAN_PHI_*), OR
   - aborted with an actionable verdict.
2. **D-T4 status**: D-T4 teacher-build (currently EXECUTING per spec
   sister-doc list) does NOT need to complete first — E and D are
   compositionally orthogonal.
3. **Calibration run completed** (recommended, +$5) — confirms `f_CF_hidden=512`
   produces non-degenerate `Δh_obs` distribution on CLM v4 substrate.
4. **No active dual-SSOT escalation** related to φ★ measurement family.

**Trigger formula:** `ENTER_2Y := (Phase_1_6_status ∈ {LANDED, ABORTED_ACTIONABLE}) ∧ (calibration_E1_passed) ∧ (no_open_phi_governance_block)`

When trigger fires, execute §3.2 launch sequence. Land verdicts to
`state/p9_paradigm_e_mini_2026_05_XX/` with the standard trajectory.json /
verdict.json schema (mirrors warmup_probe_real.py output convention).

---

## 6. SSOT / file pointers

- Spec parent: `docs/p9_paradigm_e_causal_intervention_phi_2026_05_03.md`
- This runbook: `docs/p9_paradigm_e_runbook_2026_05_03.md` (HERE)
- Mini-run script: `/tmp/p9_paradigm_e_mini.py` on ubu1 (raw#9 allowed)
- Reference base train: `/tmp/p9_p1_5_sentinel_train_50k.py` on ubu1
- Hidden-state extraction reference: `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py`
- Loss baseline: `state/p9_sft_spec_2026_05_02/loss_design.json`
- Cost / risk baseline: `state/p9_sft_spec_2026_05_02/{cost_estimate,risk_strategy}.json`
- Φ★ baseline lock: CLM v4 = +41.86; P9 floor = 5.0 (8× margin)
- raw#9 compliance: `.py` only on ubu1 (`/tmp/p9_paradigm_e_mini.py`); never in repo
- raw#15 SSOT: this file
- raw#91 honest C3: see spec §9 (10 caveats inherited)

---

## 7. Honest C3 (this runbook only — 5 caveats)

1. **`f_CF` capacity untested at CLM v4 d=768.** The spec sweet-spot of
   hidden=512 was rationalized for d=4096. For d=768 the same hidden=512
   yields ~785K params (still in the right band) but the relative capacity
   ratio differs. Calibration run mandatory before sweep.

2. **Second-forward overhead estimate (2.5×) excludes f_CF cost.** f_CF
   forward is negligible (<1% of one transformer block) but on the
   12GB RTX 5070 (ubu1), memory may bind before compute. Mini-run on RunPod
   H100 (80GB) avoids this; ubu1 dryrun MUST use small batch (BATCH=2).

3. **MIN-over-mode aggregation may favor outlier modes.** With M=2 modes
   (ablate, mean_clamp), MIN is brittle. Phase-2 expansion to M=5 partly
   mitigates, but Phase-1 results should report per-mode breakdown.

4. **F-E2 gradient ratio threshold (0.1) is heuristic.** No theoretical
   guidance for what ratio constitutes "non-trivial backbone learning."
   Report ratio + per-layer `‖grad‖` distribution for diagnostic, not just
   pass/fail.

5. **Calibration run is recommended but not enforced.** Skipping it saves $5
   but risks $15-20 sweep producing all-fail F-E1 results. Default
   recommendation: run calibration first.

---

**END runbook**
