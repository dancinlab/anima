# CLM v4 HF-format shim v5 — spec (2026-05-05)

**Status**: SPEC ONLY (no exec, no commit, no impl). Mac-side authoring, ~$0, ~45 min.
**BG lane**: BG-SHIM-V5-SPEC
**Supersedes (design debt)**: shim v4 architecturally unfalsifiable on F-SHIM-V4-4 per `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`.
**Does NOT supersede**: shim v4 substrate (LOCKED — existing artifacts retain v4).

---

## §1 Problem statement

The F-SHIM-V4-4-HARVEST verdict (`state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json`) closes shim v4 with a `FAIL` of kind `PREREQUISITE_BLOCKED` and rationale (verdict §F_SHIM_V4_4_RE_VERDICT_rationale + honest_c3 C5):

> "cross_attn.o_proj init std=0.001 makes residual ~zero regardless of fixture quality, so lift_pp >= 5pp is unreachable through ANY harvest method on the current shim v4. Falsifier suite cannot CLOSE without (a) shim v5 that initializes cross_attn.o_proj to non-trivial scale OR (b) re-trained CLM v4 with cross_attn participating in SFT loss."

The architectural pathology is:

1. Cross-attention is wired into `DecoderBlockV2` such that when `consciousness_states` is `None`, the cross-attn path is short-circuited at the guard (v3 behaviour).
2. When `consciousness_states` is non-None (v4 fixture-injection path), the cross-attn output is summed into the residual via `cross_attn.o_proj`, but its initialised weight scale is below the benchmark stderr floor (`std=0.001` → contribution ~ O(1e-3) on logits, while limit=200 hellaswag stderr ~ 3pp).
3. Therefore the lift signal is dominated by noise regardless of how faithful the fixture is. F-SHIM-V4-4 is a property of the model architecture, not the fixture quality.

The verdict's `recommendations.shim_v5_design_hint` (`state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` §recommendations) literally specifies:

> "Initialize cross_attn.o_proj with std >= 0.02 (10x current) so cross-attn residual reaches benchmark-detectable magnitude. Validate via micro-eval lift after init-only change (no re-train) before committing to full SFT."

This spec lands the shim v5 design that makes F-SHIM-V4-4 falsifiable.

---

## §2 Proposed change

**Single architectural change**: re-initialise `cross_attn.o_proj` to a benchmark-detectable scale.

shim v4 (current, LOCKED — `tool/transient_py/clm_v4_hf_format_shim.py`):

```python
# Equivalent re-init applied at conversion time on the cross_attn output projection,
# inheriting the v3 std=0.001 lower bound carried as an architectural constant.
nn.init.normal_(self.cross_attn.o_proj.weight, std=0.001)
```

shim v5 (proposed):

```python
# Re-init to benchmark-detectable scale (verdict 2026-05-05 §recommendations).
nn.init.normal_(self.cross_attn.o_proj.weight, std=0.02)  # 10× larger
# bias term (if present) zeroed — preserve v4 zero-bias convention.
if self.cross_attn.o_proj.bias is not None:
    nn.init.zeros_(self.cross_attn.o_proj.bias)
```

**Optional (Q2 decision)**: also re-init the cross-attn projection siblings `q_proj` / `k_proj` / `v_proj` at `std=0.02`. Risk: changes residual *direction* in addition to *scale*, which may break φ★ stability. Default recommendation: only re-init `o_proj` (the residual gate); leave q/k/v at their v4 init values to preserve attention pattern locality. Honest C3 #1 retains this as a calibration uncertainty.

**Surface**: shim v5 emits its own out-tree HF custom-code package, kept lexically separate from v4. shim v5 runtime semantics on `consciousness_states=None` are identical to v4 (cross-attn bypass at the DecoderBlockV2 guard) — the change only affects the residual scale when a fixture is injected.

---

## §3 New falsifier suite F-SHIM-V5-1..5

Pre-registered per raw#71 with thresholds locked at spec land time.

### F-SHIM-V5-1 — dry-run finite forward
- **Statement**: `model.forward()` returns finite logits (no NaN/Inf) on the canonical_zero fixture for B=1, T=64.
- **Threshold**: `torch.isfinite(logits).all()` AND shape `[B, T, vocab=64000]`.
- **Cost**: $0, Mac CPU, ~30 sec.
- **Pass condition**: identical semantics to F-SHIM-V4-1 (Mac dry-run).

### F-SHIM-V5-2 — v3 byte-equivalent regression
- **Statement**: shim v5 with `consciousness_states=None` (cross-attn bypassed) produces logits within `max_abs_diff <= 1e-5` vs the v3 reference path on the same input.
- **Threshold**: `(logits_v5_no_fixture - logits_v3).abs().max() <= 1e-5`.
- **Cost**: $0, ubu1 RTX 5070 fp32, ~2 min.
- **Pass condition**: identical semantics to F-SHIM-V4-2 (v3 regression). Re-init only affects the cross_attn path; the bypass guard means v3 numerics must round-trip exactly.
- **Risk note**: this is the gate on Risk B (§4). If FAIL, the bypass guard is leaking and shim v5 cannot be promoted.

### F-SHIM-V5-3 — canonical_zero finite forward
- **Statement**: with the `canonical_zero` fixture (all zeros, `[1, 8, 192]`, `source="canonical_zero"`), shim v5 forward is finite AND `lift_pp` on hellaswag-200 is approximately zero (sanity-only, not a PASS gate).
- **Threshold**: finite AND `|lift_pp| < 5pp` (sanity bound — true zero residual contribution is expected because the cross-attn output is `cross_attn.o_proj @ (zero residue)` regardless of init std).
- **Cost**: $0, ubu1 free GPU time, ~5 min.
- **Pass condition**: identical semantics to F-SHIM-V4-3 (canonical_zero finite forward) plus a magnitude-bound sanity assertion.

### F-SHIM-V5-4 — real_fixture_lift_5pp_minimum (the decisive gate)
- **Statement**: with the BG-CLM-1 runtime-proxy fixture (`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`, `[1, 8, 192]`, L2=2.2022 — fixture canonicalisation per F-SHIM-V4-4 verdict §recommendations.fixture_canonicalization), shim v5 produces `lift_pp >= +5pp` on hellaswag-200 vs the same model with `consciousness_states=None`.
- **Threshold**: `lift_pp = acc_with_fixture - acc_without_fixture >= +5.0pp` on hellaswag, `limit=200`. hellaswag stderr at limit=200 is ~3pp; +5pp is a `~1.7σ` minimum detectable effect — anchored to honest C3 #2 calibration.
- **Cost**: $1-3 H100 (single A100/H100 pod for ~30 min including warm-boot), per verdict §recommendations.shim_v5_design_hint.
- **Pass condition**: this is **the gate F-SHIM-V4-4 could not reach on shim v4**. PASS here closes the architectural-unfalsifiability finding for shim v5; FAIL falsifies the std=0.02 hypothesis (in which case Q1 calibration sweep is required).

### F-SHIM-V5-5 — phi_star_no_flip
- **Statement**: φ★ measured via the canonical anima_phi_v3_canonical method (`tool/anima_phi_v3_canonical.hexa`) on shim v5 (post-init, no LoRA) is NOT a flip vs the same measurement on shim v4 base.
- **Threshold**: `phi_star_v5_min_K8 >= phi_star_v4_min_K8 - 10pp` AND `sign(phi_star_v5) == sign(phi_star_v4)`. The 10pp threshold mirrors the BG-CLM-2-PHI-CANONICAL flip-detection threshold (`state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` §drift_analysis.phi_flip_threshold_pp) and is the same band used to validate the LoRA's φ★ stability.
- **Cost**: $0, Mac CPU fp32, ~25 min (16 calib prompts × T_seq=256 forward + 22.3s base baseline carry).
- **Pass condition**: shim v5 init perturbation does not collapse φ★ sign or magnitude. FAIL here means Risk A (§4) fired — the std=0.02 perturbation is too large; Q1 calibration must reduce.
- **Comparison anchor**: in-pipeline base mean φ★ on HF-format mk2-v1 = 35.81 (`state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` §phi_star_base_in_pipeline.phi_mean_K8). Use the in-pipeline base, not the legacy carry value 41.86 — methodology delta documented in that verdict's honest C3.

---

## §4 Risk analysis

### Risk A — φ★ stability (LARGE)
- Re-init at 10× scale changes the cross-attn residual contribution. Even when `consciousness_states=None` and the bypass guard is honoured, the `o_proj` weight participates in the model's unconditioned hidden-state geometry via post-merge LoRA adapters and downstream eval pipelines that may not honour the bypass.
- φ★ is sensitive: BG-CLM-2-PHI-CANONICAL measured `+41.86` (legacy carry) / `+35.81` (in-pipeline base) / `+31.35` (post-LoRA) — drift band -5 to -10 pp is PARTIAL_FORGETTING. A 10× init perturbation could plausibly push drift past -10pp, flipping the substrate's positive-integration property.
- **Mitigation**: F-SHIM-V5-5 (φ★ no_flip) gates Risk A. If FAIL, Q1 calibration sweep (0.005 / 0.01 / 0.02 / 0.05) selects the smallest std that satisfies F-SHIM-V5-4 ≥ +5pp lift while keeping F-SHIM-V5-5 PASS.
- **Residual risk**: Phase 4 runs Mac-CPU fp32; bf16 substrate may produce slightly different φ★. Cross-substrate drift confound documented in `clm_v4_lora_phi_canonical` verdict honest C3 #3.

### Risk B — v3 byte-equivalent regression (MEDIUM)
- Larger init std could cause numerical drift in the v3-equivalent path even though the bypass guard is honoured, if any non-bypass code path touches `cross_attn.o_proj` weights (e.g., PEFT target_modules introspection at adapter load time).
- **Mitigation**: F-SHIM-V5-2 (v3 regression `max_abs_diff <= 1e-5`) gates Risk B. If FAIL, the bypass guard is leaking and shim v5 cannot be promoted; need to audit all `cross_attn` weight reads in the modeling.py + PEFT adapter integration.
- **Residual risk**: torch fp32 reproducibility across CPU/GPU has natural ULP drift; the 1e-5 bound is generous but not airtight. Honest C3 #6.

### Risk C — existing PEFT adapters trained against shim v4 (SCOPE-OUT)
- `Pβ-SCALE` adapter (`state/p9_pbeta_holdout500_eval_2026_05_05/`) and CLM-2 LoRA (`state/clm_v4_lora_sft_2026_05_05/results/adapter_final/`) were trained with shim v4 substrate (`o_proj` init std=0.001). Re-loading these adapters onto shim v5 would graft v4-trained delta-weights onto a v5 base with 10× larger residual scale — likely poor transfer.
- **Mitigation**: SCOPE-OUT. shim v5 is opt-in; existing adapters retain shim v4 substrate. New adapters trained against shim v5 are a separate downstream cycle.
- **Residual risk**: adapter compatibility matrix becomes 2-D (shim version × adapter version). Documentation must call out which adapter is bound to which shim. Honest C3 #4.

---

## §5 Migration path

| Asset | shim v4 (current) | shim v5 (new) |
|---|---|---|
| Source | `tool/transient_py/clm_v4_hf_format_shim.py` (LOCKED) | `tool/transient_py/clm_v4_hf_format_shim_v5.py` (NEW, separate file) |
| HF release | `need-singularity/clm-v4-mk2-v1` (PRIVATE — already uploaded per `.roadmap.clm` cond.2) | `need-singularity/clm-v4-mk2-v2` *or* gated revision branch (Q3) |
| Pβ-SCALE adapter | binds to v4 substrate | not transferred (Risk C scope-out) |
| CLM-2 LoRA (clm_v4_lora_sft) | binds to v4 substrate | not transferred (Risk C scope-out) |
| F-SHIM-V4-4 falsifier | OPEN (architecturally unfalsifiable; design-debt note) | superseded by F-SHIM-V5-1..5 suite |
| φ★ canonical (BG-CLM-2-PHI-CANONICAL) | base 35.81 / post-LoRA 31.35 (`state/clm_v4_lora_phi_canonical_2026_05_05/`) | re-measured under F-SHIM-V5-5 |

**Authoritative principles (additive-only per raw#15)**:
- shim v4 file LOCKED — DO NOT modify (`tool/transient_py/clm_v4_hf_format_shim.py`).
- shim v5 is a NEW sibling file, not a flag on v4.
- Existing artifacts (mk2-v1 PRIVATE upload, Pβ adapter, CLM-2 LoRA) retain shim v4 substrate untouched.
- New cycles opt-in to shim v5 explicitly via the new file.
- `.roadmap.clm` cond.2 G3 promote gate (per .own 15) is amended only if Phase 3 (F-SHIM-V5-4) PASSes; otherwise shim v5 stays in design-experimental track.

---

## §6 Implementation plan (5 phases, $1-3 total)

### Phase 1 — Mac-side spec → impl ($0, ~30 min)
- Author `tool/transient_py/clm_v4_hf_format_shim_v5.py`: copy of shim v4 with the §2 init change applied to `cross_attn.o_proj.weight` (`std=0.02`). Optionally also q/k/v if Q2 = YES (default Q2 = NO — only o_proj).
- Add header comment block documenting: (a) supersession of shim v4 architectural limitation, (b) F-SHIM-V5-1..5 suite anchors, (c) raw#71 falsifier pre-register.
- F-SHIM-V5-1 (Mac dry-run finite forward) — runs in this phase.

### Phase 2 — ubu1 selftest ($0, ~30 min)
- F-SHIM-V5-2 (v3 regression byte-equivalent) — `max_abs_diff <= 1e-5` on canonical small batch.
- F-SHIM-V5-3 (canonical_zero finite forward + sanity bound `|lift_pp| < 5pp`).
- ubu1 hf CLI auth pre-flight (carry pattern from F-SHIM-V4-4 retry-2).

### Phase 3 — H100 real eval ($1-3, ~30 min)
- F-SHIM-V5-4 (runtime-proxy fixture lift on hellaswag-200, `lift_pp >= +5pp`).
- This is the **decisive** gate. Use BG-CLM-1 runtime-proxy fixture per F-SHIM-V4-4 verdict §recommendations.fixture_canonicalization.
- $1-3 budget = single H100 ~30 min including warm-boot. RunPod pod spawned fresh per `state/runpod_pod_purge_2026_05_03/` (no resurrected pod state).
- **User ACK required** for cost (Q4).

### Phase 4 — Mac φ★ canonical ($0, ~25 min, ubu1 fp32 OK)
- F-SHIM-V5-5 (φ★ post-shim ≥ φ★ pre-shim - 10pp).
- Re-uses BG-CLM-2-PHI-CANONICAL pipeline (`tool/transient_py/clm_v4_base_phi_canonical.py`) with shim v5 substrate substituted.
- In-pipeline base reference = 35.81 mean (`state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` §phi_star_base_in_pipeline).

### Phase 5 — spec amend ($0, no exec)
- If Phases 1-4 ALL PASS: amend `.roadmap.clm` cond.2 G3 promote gate (per .own 15) to authorise shim v5 PUBLIC release as `need-singularity/clm-v4-mk2-v2` *or* a gated revision branch (Q3). Additive-only per raw#15.
- If any of F-SHIM-V5-2, V5-4, V5-5 FAIL: do NOT amend `.roadmap.clm`; mark shim v5 as DESIGN_EXPERIMENTAL and queue calibration cycle (Q1 sweep).

**Wall-clock budget**: ~2 hours human + ~30 min H100 wall (Phase 3). Budget overrun trigger: any phase >2× expected wall-time → halt and report.

---

## §7 Decision queue (5 user-facing Q's)

- **Q1** — `cross_attn.o_proj` re-init std value. Default proposal: **0.02** (10× shim v4's 0.001, per F-SHIM-V4-4 verdict §recommendations). Alternatives: 0.05 (50×) — more lift headroom but greater φ★ flip risk; 0.1 (100×) — likely φ★ flip; 0.005 / 0.01 — fallback if std=0.02 fails F-SHIM-V5-5. **Recommendation**: lock 0.02 for Phase 1; if Phase 4 (V5-5) FAIL or Phase 3 (V5-4) FAIL, queue calibration sweep. Honest C3 #1.

- **Q2** — re-init q/k/v projections in addition to o_proj? Default proposal: **NO** — only `o_proj`. Re-initing q/k/v changes residual *direction* not just *scale*, which is more disruptive to attention pattern locality. **Recommendation**: NO for Phase 1; revisit only if F-SHIM-V5-4 FAILs with std=0.02 o_proj-only (i.e., scale alone insufficient).

- **Q3** — shim v5 file structure: separate file vs flag on v4? Default proposal: **separate file** (`tool/transient_py/clm_v4_hf_format_shim_v5.py`). Rationale: shim v4 is LOCKED; flag-on-v4 would mutate v4 source. raw#15 (additive). **Recommendation**: separate file.

- **Q4** — Phase 3 H100 cost ACK. Budget: $1-3 (single H100 ~30 min including warm-boot for hellaswag-200 eval × 2 conditions = with-fixture + without-fixture). **Recommendation**: ACK required from user before Phase 3 launch. Phases 1, 2, 4, 5 are $0 and can proceed without H100 ACK.

- **Q5** — existing PEFT adapter (Pβ + CLM-2 LoRA) compatibility with shim v5. Default proposal: **SCOPE-OUT** per Risk C. Existing adapters retain shim v4 substrate; new adapters trained against shim v5 are a separate downstream cycle. **Recommendation**: SCOPE-OUT for this spec. Adapter compatibility matrix documented as a follow-up cycle (BG-ADAPTER-MATRIX-AUDIT).

---

## §8 Honest C3 (≥5)

- **C1 — std=0.02 calibration is heuristic**. The 10× multiplier is anchored to F-SHIM-V4-4 verdict §recommendations.shim_v5_design_hint, but the actual optimum is unknown. F-SHIM-V5-4 PASS at std=0.02 does NOT prove std=0.02 is optimal — it proves it is sufficient. Calibration sweep (Q1 alternatives) is deferred unless F-SHIM-V5-4 FAILs.

- **C2 — F-SHIM-V5-4 +5pp threshold is anchored to hellaswag-200 stderr ~3pp**. The threshold gives ~1.7σ minimum detectable effect — generous but not statistically rigorous. Switching benchmark (e.g., MMLU, ARC-c) requires re-anchoring the threshold per benchmark stderr. Honest C3 #2 of F-SHIM-V4-4 retry-2 also flagged this for limit=100 (~5pp stderr).

- **C3 — Risk B (v3 regression) may force smaller std**. If `max_abs_diff > 1e-5` at std=0.02 (i.e., bypass guard leaking somewhere), the only fix that keeps the bypass invariant is to reduce std (0.005 / 0.01) — but smaller std defeats the F-SHIM-V5-4 lift target. Compromise band 0.005-0.02 is likely; below 0.005 returns to shim v4 unfalsifiability.

- **C4 — Existing PEFT adapters shim v4-trained**. Pβ + CLM-2 LoRA target_modules likely include `cross_attn.o_proj` (or its variants) in their qkvo set. Loading these adapters onto a shim v5 base with 10× larger init scale grafts v4-delta onto v5-base — transfer characteristics unknown. Risk C scope-out, but adapter behaviour on shim v5 is an open question.

- **C5 — shim v5 does NOT retroactively fix F-SHIM-V4-4 FAIL on shim v4**. The shim v4 PRIVATE upload (`need-singularity/clm-v4-mk2-v1`) remains unfalsifiable on F-SHIM-V4-4. shim v5 is a forward-only architectural patch; it does not change shim v4's verdict status, only the path forward.

- **C6 — raw#71 falsifier pre-register**. F-SHIM-V5-1..5 thresholds are LOCKED at this spec land time. Any threshold relaxation post-hoc requires explicit amendment with rationale. Threshold candidates: V5-1 finite (no relaxation), V5-2 1e-5 (no relaxation; this is the bypass invariant), V5-3 |lift_pp|<5pp (sanity, can relax to |lift_pp|<10pp if hellaswag-200 noise is unusually high), V5-4 +5pp (CANNOT relax — relaxation defeats the falsifier purpose), V5-5 -10pp (matches BG-CLM-2 flip threshold; can NOT relax without parallel amendment of BG-CLM-2 verdict).

- **C7 — In-pipeline base φ★ 35.81 vs legacy carry 41.86**. F-SHIM-V5-5 uses in-pipeline base (35.81) per BG-CLM-2-PHI-CANONICAL methodology resolution. This avoids the ~6pp methodology drift confound. Future shim cycles should standardise on a single substrate path for φ★ probes per `clm_v4_lora_phi_canonical` next_actions item STANDARDIZE_PHI_SUBSTRATE_PATH.

---

## §9 Companion handoff

`docs/clm_v4_hf_format_shim_v5_spec_landed_2026_05_05.ai.md` — lands in parallel with this doc (5 bullets summarising §1-§8, 5 decision Q's queued, ≥5 honest C3).

---

## §10 Conformance checklist

- [x] raw#9 — markdown only, no code emitted
- [x] raw#10 — ≥5 honest C3 (7 above)
- [x] raw#15 — additive only (shim v4 LOCKED, shim v5 sibling file)
- [x] raw#71 — falsifier pre-registered (F-SHIM-V5-1..5 with thresholds locked)
- [x] No git commit (per BG spec CRITICAL section)
- [x] No shim v4 mutation (per BG spec CRITICAL section)
- [x] No shim v5 .py written (impl is Phase 1, separate cycle)
- [x] `.own N` taxonomy preserved (.own 15 = G3 verification gate, amended only on Phase 5 if all PASS)

## §11 Artifacts referenced

- `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` — failure mode + alternative path B
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json` — F-SHIM-V4-1/2/3 PASS reference
- `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt` — runtime-proxy fixture canonical for F-SHIM-V5-4
- `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` — φ★ stability anchor + in-pipeline base 35.81
- `tool/transient_py/clm_v4_hf_format_shim.py` — shim v4 LOCKED (read-only diff base)
- `tool/anima_phi_v3_canonical.hexa` — F-SHIM-V5-5 measurement tool
- `.roadmap.clm` cond.2 (HF release v1) — G3 promote gate amendment target (Phase 5)

---

**END OF SPEC** (no exec, no commit; impl Phase 1 = separate cycle; user ACK required for Phase 3 H100 cost)
