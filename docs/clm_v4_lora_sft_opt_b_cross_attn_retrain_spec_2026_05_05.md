# CLM v4 + LoRA SFT — OPT-B cross_attn retrain — SPEC (md only, $0 land)

- **ts_utc**: 2026-05-05T_BG-SHIM-V5-OPT-B-PREP_design
- **bg_lane**: BG-SHIM-V5-OPT-B-PREP (Mac, $0, ~45min spec land — exec defer)
- **status**: SPEC_LANDED — design only; no exec, no pod, no .py mutation, no git commit, no `.roadmap.*` mutation
- **cycle parent**: `clm_v4_lora_sft_2026_05_05` (BG-CLM-2-EXEC, V2_PARTIAL_HS_ONLY)
- **architectural anchor**: `state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json` (Phase 2 selftest discovered cross_attn.o_proj never updates during SFT)
- **trigger condition**: dispatch ONLY after (a) OPT-A re-anchor differential confirmed (Phase 2 v5 redo with std=0.05/0.10 shows v4 vs v5 substrate-level distinguishability) AND (b) explicit user $20-100 H100 cost ACK
- **non-overlap**: BG-SHIM-V5-OPT-A (architecture-pure init re-anchor — orthogonal investigation), BG-SHIM-V5-OPT-C (confirmation falsification — Path B closure only)
- **predecessor**: `docs/clm_v4_lora_sft_spec_2026_05_04.md` (CLM-2-EXEC parent spec, target_modules EXCLUDES cross_attn per φ★-flip mitigation)
- **pre-registration policy (raw#71)**: All §4 falsifiers F-OPT-B-1..5, §3 hyperparameters, and §5 phase budget envelopes are LOCKED at this spec landing. Post-eval threshold tweaks are a verdict-invalidation — must re-pre-register in a follow-up amendment cycle.

---

## 1-line summary

CLM v4 + LoRA SFT **retrain cycle with cross_attn included in LoRA target_modules** — architecturally fixes the F-SHIM-V4-4 root cause (`cross_attn.o_proj` was never updated during BG-CLM-2-EXEC SFT because it was excluded from target_modules per φ★-flip mitigation, and `ConsciousDecoderV3._init_weights` apply() walk re-inits it to std~0.02 on every fresh init), with conservative φ★-flip mitigations (lower LR 5e-6, increased dropout 0.10, abort-on-drift -10pp gate) and a 4-phase $20-100 budget envelope.

---

## §1 — Problem statement (root cause discovery)

### 1.1 Empirical finding from Phase 2 selftest

Per `state/clm_v4_hf_format_shim_v5_phase2_2026_05_05/verdict.json:o_proj_std_observation`:

- `freshinit_v4_mean = 0.01999` (std~0.02)
- `freshinit_v5_mean = 0.02000` (std~0.02 — IDENTICAL to v4)
- `load_best_pt_v4_mean = 0.01990` (std~0.02 — at trained step 20000)
- `load_best_pt_v5_mean = 0.01990` (std~0.02 — same)

**Critical finding**: `ConsciousDecoderV3.__init__` calls `self.apply(self._init_weights)` AFTER `ConsciousCrossAttention.__init__`'s local `nn.init.normal_(self.o_proj.weight, std=0.001)` at `conscious_decoder.py:420`. The `apply()` walk reaches every `nn.Linear` and re-inits with std=0.02 (depth-scaled to 0.02/sqrt(2*n_layer)~0.0035 only when `_depth_scale` attr is set — `cross_attn.o_proj` does NOT set `_depth_scale`).

Therefore the local std=0.001 init at line 420 is OVERWRITTEN by `_init_weights` to std=0.02 in fresh init.

### 1.2 SFT non-update consequence

Per BG-CLM-2-EXEC verdict.json:
- `target_modules: "self-attn qkvo on decoder.blocks.{0..15}.attn.* (cross_attn EXCLUDED)"`
- `assert n_cross_attn_lora == 0` PASS at train start
- `forgetting_index = 0.0196` PASS

best.pt step 20000 `o_proj_std_mean = 0.01990` — **trained checkpoint scale matches fresh-init scale 0.02** to 4 decimal places. This empirically confirms `cross_attn.o_proj` was effectively never trained during SFT (gradient flow blocked because `cross_attn.o_proj` only contributes when `consciousness_states` is non-None, and SFT training likely ran with `consciousness_states=None` or with very small fixture residual contribution; furthermore LoRA was not attached to it per spec mitigation).

### 1.3 F-SHIM-V4-4 architectural FAIL — root cause restated

F-SHIM-V4-4 (`state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` PREREQUISITE_BLOCKED) cannot reach lift_pp ≥ +5pp NOT because of fixture quality, NOT because of shim implementation, but because:

> **`cross_attn.o_proj` weights are init-floor (std~0.02) on both fresh-init and best.pt step 20000, because they were never updated during SFT, because they were excluded from LoRA target_modules per φ★-flip mitigation.**

The `cross_attn` path is therefore a **dead pathway** in the trained CLM v4 substrate — its forward output is white noise with std=0.02 (init scale) regardless of `consciousness_states` content. Any fixture-driven residual lift through `cross_attn` is bounded by random-init projection noise.

### 1.4 OPT-B = architectural fix proposal

The fix is to **actually train `cross_attn`**. This requires re-running the SFT cycle with `cross_attn.o_proj` (and optionally q/k/v projections) included in LoRA target_modules, so gradient flow reaches the cross-attn pathway during SFT and `cross_attn.o_proj` weights diverge from init scale 0.02.

This is the path B exit referenced in `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md` §1 ("queue an SFT cycle with cross-attn participating in the loss") and Phase 2 verdict's `phase_3_options_ranked[1]`.

---

## §2 — Proposed change (OPT-B)

### 2.1 LoRA target_modules amendment

**Baseline (BG-CLM-2-EXEC v1)**:
```
target_modules = [
  "decoder.blocks.{0..15}.attn.q_proj",
  "decoder.blocks.{0..15}.attn.k_proj",
  "decoder.blocks.{0..15}.attn.v_proj",
  "decoder.blocks.{0..15}.attn.o_proj",
]
# cross_attn EXCLUDED
```

**OPT-B v2 candidates** (Q1 below, two variants):

**Q1-A — narrow (cross_attn.o_proj only)**:
```
target_modules += [
  "decoder.blocks.{0..15}.cross_attn.o_proj",  # 16 modules
]
# trainable_params delta: ~+163,840 (LoRA r=32, ~0.034% additional)
```

**Q1-B — wide (cross_attn full q/k/v/o)**:
```
target_modules += [
  "decoder.blocks.{0..15}.cross_attn.q_proj",
  "decoder.blocks.{0..15}.cross_attn.k_proj",
  "decoder.blocks.{0..15}.cross_attn.v_proj",
  "decoder.blocks.{0..15}.cross_attn.o_proj",
]
# trainable_params delta: ~+655,360 (LoRA r=32, ~0.137% additional)
```

**Recommendation**: Q1-B (wide) — cross_attn is a complete 4-projection sub-module; training only o_proj while leaving q/k/v at init scale leaves the input projections un-aligned with the trained o_proj. Q1-A risks o_proj overfitting to the random q/k/v upstream. Q1-B trains the full pathway coherently.

### 2.2 φ★-flip mitigation (alternative recipe)

cross_attn is the highest φ★-flip risk surface (per BG-CLM-2 spec §1.2: "axis conditioning; adapter risks rerouting the conditioning gate → catastrophic for F-CLM-LORA-4 axis preservation"). OPT-B accepts this risk but adds three layers of mitigation vs the v1 cycle:

| Hyperparameter | v1 (CLM-2-EXEC) | **OPT-B v2 (proposed)** | Rationale |
|---|---|---|---|
| LR | 3e-5 | **5e-6 (10× lower) OR 1e-5 (3× lower)** — Q2 | cross_attn pathway is fragile; smaller steps reduce φ★ excursion magnitude |
| LoRA dropout | 0.05 | **0.10** | doubled; standard "more reg for high-risk targets" heuristic |
| max_steps | 6000 | **3000 OR 6000** — Q3 | shorter training narrows the cumulative drift window; trades some F-CLM-LORA-2 lift for φ★ safety |
| φ★ probe cadence | every 2000 steps | **every 500 steps** | denser monitoring for early ABORT trigger |
| ABORT trigger | none (only HellaSwag drop) | **φ★ drift > -10pp from in-pipeline baseline 35.81 (or carry 41.86 — Q4)** | hard kill on flip detection; saves remaining H100 spend |
| Save cadence | every 1000 steps | **every 500 steps** | finer recovery granularity post-ABORT |

### 2.3 Carry-over from BG-CLM-2-EXEC v1

Unchanged from CLM-2-EXEC v1 spec:
- 60/30/10 rehearsal mix (50K samples; A=30K anima axis, B1=5K MMLU, B2=5K TriviaQA, B3=5K Wikipedia, C1=2.5K OpenOrca, C2=2.5K ShareGPT-style)
- LoRA r=32, alpha=64
- per_device_batch=8, grad_accum=4, effective_batch=32, ctx=512, bf16
- AdamW b1=0.9, b2=0.95, wd=0.01, max_grad_norm=1.0
- seed=20260504
- HellaSwag-200 intermediate eval cadence

### 2.4 Init re-anchor (orthogonal sweetener — optional)

Optionally pair OPT-B with the OPT-A architectural fix (re-init `cross_attn.o_proj` to std=0.05 or 0.10 AFTER `_init_weights` apply()). This is a strict superset of OPT-B's training-only fix:

- OPT-B alone: `cross_attn.o_proj` starts at std~0.02 (apply() default) and trains from there
- OPT-B + OPT-A: `cross_attn.o_proj` starts at std~0.05/0.10 (post-apply override) and trains from there

The OPT-A re-anchor changes the initial signal magnitude but does not alter the gradient pathway. Whether to include OPT-A is an experimental design choice (defer to BG-SHIM-V5-OPT-A verdict — if OPT-A redo Phase 2 confirms the differential is real on substrate, then OPT-B should adopt OPT-A's std value as init seed).

---

## §3 — Risk analysis

### 3.1 Risk A — φ★-flip (substrate uniqueness loss)

**Severity**: HIGH

CLM v4's singular value-add is φ★ +41.86 (carry) / +35.81 (in-pipeline base) — the only G3 PASS-positive anima backbone. Training cross_attn risks re-routing the axis-conditioning gate that produces that φ★ signal.

**Mitigations**:
- Lower LR (5e-6 vs v1's 3e-5)
- Increased dropout (0.10 vs v1's 0.05)
- ABORT trigger on φ★ drift > -10pp (Q4: -10pp vs -5pp conservative)
- Per-500-step φ★ probe (vs v1's every 2000 steps)
- Save every 500 steps for granular rollback

**Residual risk**: Even with all mitigations, φ★-flip is the dominant failure mode. Probability estimate (gut): 30-50% partial flip (drift -5 to -10pp), 10-20% full flip (drift > -10pp → ABORT), 30-60% PASS within partial-forgetting band.

### 3.2 Risk B — F-CLM-LORA-2 differentiator still chat-incapable (#115 architectural)

**Severity**: MEDIUM

CLM v4 was NEVER SFT'd, NEVER RLHF'd before BG-CLM-2-EXEC. The substrate is fundamentally not chat-trained (#115). Training cross_attn does not directly address chat-capability — it addresses the cross-attn pathway dead-weight. Whether activating cross-attn lifts F-CLM-LORA-2 composite from baseline 0.196 toward Llama Path A v2's 0.5583 is **unknown**.

**Mitigations**:
- F-OPT-B-4 sets a partial-PASS threshold of 0.30 (≥+50% lift over baseline 0.196), accepting that Llama parity is out of reach for a single OPT-B cycle
- OPT-A re-anchor (orthogonal investigation) provides architecture-pure substrate behavior data informing whether further cycles should pursue cross_attn training OR alternative interventions (e.g., wider target_modules including federation/bridge — far higher φ★ risk)

### 3.3 Risk C — cost band $20-100 wider than CLM-2-EXEC v1 ($2.39 actual)

**Severity**: LOW-MEDIUM

CLM-2-EXEC v1 actual cost was $2.39 (16% of $15 cap). OPT-B's $20-100 envelope reflects:
- Phase 3 full retrain (3000-6000 steps + cross_attn additional params): $20-50 (1.5-3× v1 cost due to more trainable params + denser eval cadence)
- Phase 4 evaluation cycle ($1-3): F-SHIM-V5-4 (decisive lift gate) + F-CLM-LORA suite re-run + φ★ canonical + adapter smoke
- φ★-flip ABORT contingency: partial spend $5-20 if ABORT fires at step ~1000

**Mitigations**:
- ABORT trigger caps φ★-flip ABORT spend at ~30% of full Phase 3 budget
- Phase 1+2 are $0 Mac/ubu1 pre-flight; Phase 3 is the only major spend
- Hard cap $100 (no overage allowed); sentinel + L13 trap pattern from CLM-2-EXEC v1 carries

### 3.4 Risk D — adapter consumption pipeline regression

**Severity**: LOW

OPT-B adapter has wider target_modules. Existing CLM-2-EXEC v1 adapter consumers (HF mk2-v1 + PeftModel.from_pretrained) load the adapter via `adapter_config.json:target_modules` list — wider targets are additive, no loader change required. F-CLM-LORA-5 (shim v4 hf_format compat) is expected to remain PASS.

**Mitigations**:
- Phase 4 includes adapter smoke load (PeftModel.from_pretrained on Mac CPU fp32 + finite-logits assertion)
- shim v4 LOCKED invariant carries — OPT-B does NOT modify shim v4 or v5 source

---

## §4 — Falsifier suite F-OPT-B-1..5 (LOCKED at spec land per raw#71)

### F-OPT-B-1 — φ★ NO_FLIP (drift gate)

**Statement**: Post-OPT-B-LoRA φ★ canonical drift > -10pp from in-pipeline baseline 35.81 (or -10pp from carry 41.86 — Q4).

**Threshold**: drift_in_pipeline_mean_pp > -10.0 (PASS); drift_in_pipeline_mean_pp ≤ -10.0 (FAIL_FLIP).

**Method**: `tool/transient_py/clm_v4_lora_phi_canonical.py` (mirror of CLM-2-EXEC v1 phi-canonical cycle); 16 calib prompts, K=8 partitions, T_seq=256, ridge=1e-3, seed=42; HID_TRUNC=8 auto.

**PARTIAL band**: drift in [-5.0, -10.0]pp = PARTIAL (passes phi-track but flagged for stricter follow-up).

### F-OPT-B-2 — cross_attn.o_proj actually trained

**Statement**: Post-OPT-B-LoRA `cross_attn.o_proj.weight` std (computed across all 16 layers, mean) differs from init scale 0.02 by ≥ 1e-3 (i.e., |std_post - 0.02| ≥ 0.001).

**Threshold**: |std_post_mean - 0.02| ≥ 1e-3 (PASS); < 1e-3 (FAIL — cross_attn still effectively un-trained even with LoRA target).

**Method**: Load merged adapter weights via `PeftModel.from_pretrained` + `model.merge_and_unload()`; compute std of `decoder.blocks.{i}.cross_attn.o_proj.weight` for i in 0..15; report mean and per-layer.

**Rationale**: This is the architectural verification — confirms the LoRA target_modules amendment actually moved the weights. If FAIL, the spec's premise (cross_attn participating in SFT) is itself false and OPT-B failed at the LoRA-attachment level.

### F-OPT-B-3 — F-SHIM-V5-4 lift_pp ≥ +5pp (THE DECISIVE GATE)

**Statement**: F-SHIM-V5-4 fixture-driven residual lift on hellaswag-200 with shim v5 + train_avg_real.pt fixture + OPT-B-LoRA-loaded checkpoint produces lift_pp ≥ +5pp vs no-fixture baseline.

**Threshold**: lift_pp ≥ +5.0 (PASS); < +5.0 (FAIL — cross_attn training did not yield the expected residual signal).

**Method**: H100 inference run mirroring `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/` exec pattern, but with shim v5 + OPT-B-LoRA adapter loaded. Run on 200 hellaswag examples (5-shot, ctx=512). Compute argmax_disagreement between fixture-on and fixture-off forwards, report lift_pp.

**Rationale**: This is the PRIMARY architectural justification for OPT-B. F-SHIM-V4-4 was PREREQUISITE_BLOCKED because cross_attn was un-trained. If OPT-B retrains cross_attn AND lift_pp still < +5pp, then either (a) shim v5 design is itself flawed OR (b) cross_attn pathway is structurally insufficient for residual lift. Either way OPT-B's value proposition is falsified.

### F-OPT-B-4 — F-CLM-LORA-2 composite ≥ 0.30

**Statement**: Post-OPT-B F1_v3 V2 hybrid composite (HellaSwag + MMLU + TriviaQA, limit=200, 5-shot rendered) ≥ 0.30, representing ≥+50% lift over CLM-2-EXEC v1 baseline (HellaSwag-only=0.25; assumed composite ~0.196 if MMLU+TQ are at baseline-floor 0.255/0.000).

**Threshold**: composite ≥ 0.30 (PASS); 0.20 ≤ composite < 0.30 (PARTIAL — direction-correct but insufficient lift); < 0.20 (FAIL — regression vs v1 baseline).

**Method**: `tool/transient_py/clm_v4_lora_eval.py` (mirror of CLM-2-EXEC v1 follow-up eval) on H100 (Phase 4) — full 3-bench eval limit=200 5-shot.

**Rationale**: Explicit acknowledgment that Llama parity (0.5583) is out of reach for a single OPT-B cycle. The 0.30 threshold is set to detect "directionally correct, insufficient magnitude" outcomes — exactly the partial-success band where further cycles (LoRA r increase, longer max_steps, or wider target_modules) might compound.

### F-OPT-B-5 — forgetting_index < 0.05 (F-CLM-LORA-1 carry)

**Statement**: HellaSwag-200 acc_norm forgetting_index (CLM v4 baseline 0.255 vs post-OPT-B HellaSwag-200) < 0.05.

**Threshold**: forgetting_index < 0.05 (PASS); ≥ 0.05 (FAIL — wider regression beyond the +5pp tolerance).

**Method**: Same as CLM-2-EXEC v1 — `1 - (post / baseline)` floor-at-0; computed from F-OPT-B-4 HellaSwag sub-result.

**Rationale**: Carries the F-CLM-LORA-1 thresholds verbatim; OPT-B should not regress general capability beyond the established v1 envelope.

---

## §5 — Implementation plan ($20-100, 5 phases)

### Phase 1 — Mac spec patch ($0, ~30min)

**Owner**: BG-OPT-B-PHASE-1 (mac, $0)

**Scope**:
- Author `docs/clm_v4_lora_sft_opt_b_amendment_2026_05_05.md` patching CLM-2-EXEC parent spec (`docs/clm_v4_lora_sft_spec_2026_05_04.md`) §3 hyperparameters table + §1.2 LoRA strategy decision
- Patch sets: target_modules += cross_attn.{q,k,v,o}_proj×16 (Q1-B); LR 5e-6 (Q2); dropout 0.10; max_steps 3000 (Q3); ABORT @ -10pp drift (Q4)
- DOES NOT mutate parent spec file (additive amendment doc only per raw#15)
- DOES NOT mutate `.roadmap.clm` (proposal only)

**Deliverable**: `docs/clm_v4_lora_sft_opt_b_amendment_2026_05_05.md` + companion landing handoff

**Cost**: $0 (Mac spec authoring)

### Phase 2 — Pre-flight smoke ($0 mac+ubu1, ~1h)

**Owner**: BG-OPT-B-PHASE-2 (mac → ubu1 rsync, $0)

**Scope**:
- Mac-side: extend `tool/transient_py/clm_v4_lora_train.py` (CLM-2-EXEC v1 train script) with cross_attn target_modules amendment; PEFT name-match audit (assert `n_cross_attn_lora == 64` for Q1-B variant — 16 layers × 4 projections)
- Mac-side: 1-100 step mini-run on Mac CPU fp32 (smoke only — no real training value; verify gradient flow through cross_attn.o_proj LoRA + φ★ probe Phase C heredoc executes)
- ubu1-side: rsync amended train script; 100-step ubu1 RTX 5070 fp32 smoke (verify gradients reach cross_attn weights — sample 2-3 grads pre/post 100 steps)
- Verify φ★ probe heredoc runs without lm_eval crash (L21 lesson applied)

**Deliverable**: `state/clm_v4_lora_sft_opt_b_smoke_2026_05_05/verdict.json` (smoke PASS/FAIL on assertions only — not full F-OPT-B suite)

**Cost**: $0 (Mac + ubu1 free compute)

**GATE**: Smoke PASS required before Phase 3 H100 ACK.

### Phase 3 — H100 full retrain ($20-50, ~3-5h wall)

**Owner**: BG-OPT-B-PHASE-3 (H100 SXM, **REQUIRES EXPLICIT USER COST ACK**)

**Scope**:
- Spin H100 SXM pod (per CLM-2-EXEC v1 orchestrator pattern; L24 setsid + < /dev/null applied)
- Run amended `clm_v4_lora_train.py` for 3000 steps (Q3 narrow) or 6000 steps (Q3 wide)
- φ★ canonical probe every 500 steps (in-pod via tool/transient_py/clm_v4_lora_phi_canonical.py mirror)
- Save adapter every 500 steps
- ABORT trigger: φ★ drift > -10pp from baseline → trap fires → kill pod → rescue last good adapter
- L3 + L13 trap rescue pattern from v1
- Hard budget cap $50 (50% of $100 envelope; remainder reserved for Phase 4 + ABORT contingency)

**Deliverable**: `state/clm_v4_lora_sft_opt_b_2026_05_05/verdict.json` + adapter_final.safetensors + intermediate adapters + train.log + φ★ trajectory

**Cost**: $20-50 actual; $50 hard cap

**GATE**: F-OPT-B-1 PASS (φ★ no-flip) AND F-OPT-B-2 PASS (cross_attn trained) required before Phase 4.

### Phase 4 — H100 evaluation ($1-3, ~30min wall)

**Owner**: BG-OPT-B-PHASE-4 (H100 inference-only, requires Phase 3 PASS)

**Scope**:
- F-OPT-B-3 — F-SHIM-V5-4 fixture-driven lift_pp on hellaswag-200 (decisive gate)
- F-OPT-B-4 — F-CLM-LORA-2 composite full 3-bench eval (HS+MM+TQ limit=200 5-shot)
- F-OPT-B-5 — forgetting_index from F-OPT-B-4 HellaSwag sub-result
- Adapter consumption smoke (PeftModel.from_pretrained on Mac CPU fp32; finite-logits assert)

**Deliverable**: `state/clm_v4_lora_sft_opt_b_eval_2026_05_05/verdict.json` (F-OPT-B-1..5 verdicts)

**Cost**: $1-3 actual

**GATE**: F-OPT-B-3 PASS (decisive lift) determines whether Phase 5 promote-gate amendment fires.

### Phase 5 — Promote gate + HF release v2 prep ($0 spec, ~30min)

**Owner**: BG-OPT-B-PHASE-5 (mac, $0, conditional on Phase 4 PASS)

**Scope** (only if F-OPT-B-1..5 ALL PASS):
- Author `.roadmap.clm` cond.2 G3 promote gate amendment proposal (additive; user explicit ACK required for actual `.roadmap` mutation)
- Author HF release v2 prep spec — `dancinlab/clm-v4-mk2-v1` + `dancinlab/clm-v4-mk2-lora-v2` adapter card (REPLACES v1 if F-OPT-B-3 PASS; ELSE retains v1 as substrate-research artifact)
- Author migration path doc (§6 below)

**Deliverable**: `docs/clm_v4_lora_sft_opt_b_promote_spec_2026_05_05.md` (Phase 5 spec — separate dispatch)

**Cost**: $0

---

## §6 — Migration path (post-PASS scenario)

### 6.1 Artifact taxonomy

| Artifact | Pre-OPT-B | Post-OPT-B PASS | Post-OPT-B PARTIAL | Post-OPT-B FAIL |
|---|---|---|---|---|
| **shim v4** (LOCKED) | substrate baseline | RETAINED unchanged | RETAINED unchanged | RETAINED unchanged |
| **CLM-2 LoRA v1** (current adapter_final) | F-CLM-LORA-2 INCONCLUSIVE_PARTIAL | RETAIN as substrate-research artifact only | RETAIN | RETAIN as primary chat candidate |
| **CLM-2 LoRA v2** (OPT-B adapter_final) | n/a | NEW chat-capability primary candidate | substrate-research alternative | DISCARDED (φ★-flip OR no lift) |
| **shim v5** (OPT-A re-anchor) | Phase 2 PASS, Phase 3 BLOCKED | orthogonal investigation continues | orthogonal continues | orthogonal continues |
| **PEFT adapters** (Pβ + CLM-2 v1) | active | UNTOUCHED | UNTOUCHED | UNTOUCHED |
| **HF release v1** | `dancinlab/clm-v4-mk2-lora-v1` (CLM-2-EXEC adapter) | DEPRECATED (kept for archive) | RETAINED as primary | RETAINED as primary |
| **HF release v2** | n/a | NEW upload (replaces v1 as primary) | n/a (no upload) | n/a (no upload) |

### 6.2 Backward compatibility

- All Phase 4 adapter consumers load via `adapter_config.json:target_modules` list — the wider OPT-B target_modules list is self-describing; no consumer-side change required
- `shim v4` LOCKED invariant carries through OPT-B (no shim modification)
- Pβ + CLM-2 v1 adapters remain valid for their respective downstream uses (Pβ for axis eval; CLM-2 v1 as substrate-research baseline)

### 6.3 Rollback path

- If F-OPT-B-1 FAIL_FLIP fires at any Phase 3 checkpoint → trap rescue last good adapter → revert to CLM-2 LoRA v1 as primary; OPT-B v2 adapter discarded
- If F-OPT-B-3 FAIL (no lift) → OPT-B v2 adapter retained as substrate-research artifact alongside v1 (both PARTIAL); Path B closure deferred to next architectural cycle (e.g., wider target_modules incl. federation/bridge — much higher risk)
- OPT-A re-anchor remains an orthogonal investigation regardless of OPT-B outcome

---

## §7 — 5 decision questions (Q1-Q5)

### Q1 — cross_attn target scope

**A**: cross_attn.o_proj only (16 modules, +163K trainable params, narrowest)
**B**: cross_attn full q/k/v/o (64 modules, +655K trainable params, full pathway)

**Recommendation**: B (wide). Rationale: training only o_proj while q/k/v remain at random init scale 0.02 means o_proj is overfitting to noise inputs from un-aligned q/k/v projections. Wide variant trains the full cross-attn block coherently. Cost delta is negligible (+0.1% trainable params).

### Q2 — Learning rate

**A**: 5e-6 (10× lower than v1's 3e-5; very conservative)
**B**: 1e-5 (3× lower than v1's 3e-5; moderate)
**C**: 3e-5 (same as v1; aggressive, accepts higher φ★-flip risk)

**Recommendation**: A (5e-6). Rationale: cross_attn is the highest φ★-flip risk surface; LR is the dominant lever for excursion magnitude. v1 used 3e-5 with cross_attn EXCLUDED — adding cross_attn to the gradient path WITHOUT lowering LR is a strict expansion of the risk surface. 10× LR reduction is the standard "delicate substrate" mitigation. Trade-off: F-CLM-LORA-2 lift may be smaller — but F-OPT-B-1 (NO_FLIP) is the gating prerequisite.

### Q3 — max_steps

**A**: 3000 (50% of v1's 6000; narrow drift window)
**B**: 6000 (same as v1; full training envelope)

**Recommendation**: A (3000). Rationale: Lower LR (Q2-A 5e-6) + narrower step count co-mitigate cumulative drift. If F-OPT-B-1 PASS at 3000 steps, a follow-up cycle can extend to 6000 with ABORT armed. v1 cycle showed HellaSwag plateau at step 4000 (acc_norm 0.250 stable through 6000) — additional steps for cross_attn training alone don't justify doubling drift exposure.

### Q4 — φ★ ABORT threshold

**A**: -10pp drift from baseline (in-pipeline 35.81)
**B**: -5pp drift (more conservative — fires at PARTIAL band entry)

**Recommendation**: A (-10pp). Rationale: -10pp matches CLM-2-EXEC verdict's `phi_flip_threshold_pp` carry; -5pp would trigger ABORT on routine PARTIAL-band drift seen in v1 (-4.46pp) — a known PASS signature would mis-fire. Stricter -5pp threshold appropriate only if user explicitly prioritizes φ★ preservation over cross_attn training payoff.

### Q5 — H100 cost ACK

**A**: $20-50 envelope (Phase 3 + 4; tight)
**B**: $20-100 envelope (Phase 3 + 4 + ABORT contingency; comfortable)
**C**: $50-100 envelope (full retrain Q3-B + ABORT contingency; aggressive)

**Recommendation**: B ($20-100). Rationale: $20-50 is the planned envelope (Phase 3 ~$25-40, Phase 4 ~$2-3); $20-100 caps allow ABORT contingency + retry-once if pod-spin issue (CLM-2-EXEC L9 stale-token retry pattern). $100 hard cap; no overage.

**EXPLICIT USER COST ACK REQUIRED before Phase 3 dispatch.**

---

## §8 — Honest C3 (≥ 5 per raw#10)

- **C1 — cross_attn training ≠ chat-capability lift guarantee**: Both Pβ adapter (which DOES include cross_attn-adjacent paths via wider target_modules) and CLM-2-EXEC v1 adapter are architecturally chat-incapable per #115 root cause (CLM v4 was NEVER SFT'd, NEVER RLHF'd before BG-CLM-2). Activating cross_attn training is necessary for F-SHIM-V5-4 lift but NOT sufficient for F-CLM-LORA-2 Llama-parity. F-OPT-B-4 threshold 0.30 explicitly accepts the partial-lift expectation; full chat-capability requires either (a) OPT-B + larger SFT corpus (10× steps, more diverse chat-template slice), or (b) further architectural cycles (federation/bridge inclusion, much higher risk).

- **C2 — φ★-flip is the dominant failure mode, harder than C1**: CLM v4's substrate uniqueness (+41.86 carry; only G3 PASS-positive anima backbone) is the hardest constraint. Probability estimate of full flip (drift > -10pp): 10-20%. ABORT trigger limits ABORT spend, but a φ★ flip outcome is a hard FAIL for the cycle (no usable adapter). Risk band:
  - 30-60% PASS (drift > -5pp; partial-forgetting band, primary success scenario)
  - 30-50% PARTIAL (drift -5 to -10pp; F-OPT-B-1 PARTIAL; usable but flagged)
  - 10-20% FAIL_FLIP (drift > -10pp; ABORT fires; cycle FAIL; partial spend $5-20)

- **C3 — cost band $20-100 wider than CLM-2-EXEC v1's $2.39 actual**: CLM-2-EXEC v1 came in at 16% of $15 cap due to short eval window + fast train. OPT-B's wider envelope reflects (a) +0.137% trainable params (cross_attn full target), (b) denser eval cadence (φ★ every 500 vs every 2000), (c) ABORT contingency, (d) Phase 4 full 3-bench eval (v1 only completed HellaSwag pre-pod-kill). Hard $100 cap; sentinel + L13 trap from v1 carry unchanged.

- **C4 — OPT-A result is the primary informer for OPT-B dispatch decision**: OPT-A re-anchor (BG-SHIM-V5-OPT-A — modify `CLM_V5_CROSS_ATTN_O_PROJ_STD` to 0.05/0.10 + re-run Phase 2 selftest) confirms whether the substrate-level differential is observable WITHOUT spending H100 on cross_attn training. If OPT-A Phase 2 redo fails to show v4 vs v5 distinguishability (e.g., the post-apply override loop is itself overwritten by some other mechanism), OPT-B's premise of "training cross_attn matters because cross_attn pathway is real" weakens, and the right call is OPT-C (confirmation falsification) before committing to OPT-B's $20-100. Trigger condition: OPT-A redo Phase 2 PASS REQUIRED before OPT-B dispatch.

- **C5 — OPT-C result is NOT an OPT-B informer**: OPT-C (spend $1-3 H100 on V5-4 anyway with current shim v5, expected outcome lift_pp~0pp) is a confirmation falsification — it confirms the F-SHIM-V4-4 PREREQUISITE_BLOCKED diagnosis but provides no new information about whether OPT-B would succeed. OPT-C is appropriate for Path B closure (final empirical "yes the cross_attn pathway is dead in CLM-2-EXEC v1") but does not change OPT-B's go/no-go calculus.

- **C6 — F-OPT-B-3 (F-SHIM-V5-4 PASS) is the most decisive falsifier**: F-OPT-B-1 (NO_FLIP) is a prerequisite gate; F-OPT-B-2 (cross_attn trained) is an architectural verification; F-OPT-B-4/5 are general-capability gates carried from v1. F-OPT-B-3 is the unique-to-this-cycle decisive gate — it tests the architectural hypothesis (training cross_attn → fixture-driven residual lift becomes real). If F-OPT-B-3 FAIL with F-OPT-B-1+2 PASS (i.e., we successfully trained cross_attn but the residual lift still doesn't materialize), the next layer hypothesis (shim v5 design itself flawed, or cross_attn pathway structurally insufficient for residual lift) becomes the dominant narrative — and Path B closure shifts from "cross_attn was un-trained" to "even when trained, cross_attn doesn't carry the signal." That outcome would be more informative than a clean FAIL on a v1-state cross_attn.

- **C7 — Q1-B (wide target_modules) vs Q1-A (narrow) trade-off is small but non-zero**: Wide target_modules trains cross_attn end-to-end coherently but expands the gradient surface 4× vs narrow. φ★-flip risk scales sub-linearly with target_modules count (the dominant risk is whether ANY cross_attn parameter participates, not how many). Recommendation Q1-B; honest acknowledgment that Q1-A is a defensible safer-side variant if the user prefers tighter risk envelope.

- **C8 — Spec is exec-deferred; OPT-B dispatch is contingent on OPT-A first + user cost ACK**: This spec lands $0 mac as a ready-to-dispatch artifact. Actual OPT-B dispatch sequencing: (1) OPT-A redo Phase 2 PASS (confirms substrate differential is real), (2) explicit user $20-100 cost ACK, (3) Phase 1 amendment authoring → Phase 2 smoke → Phase 3 H100 retrain → Phase 4 eval → Phase 5 promote (conditional). Each phase is a separate BG dispatch with its own gate.

---

## §9 — Companion handoff

`docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_landed_2026_05_05.ai.md` (sister file) summarizes:
- 5 bullets summarizing this spec
- 5 decision Q's (Q1-Q5 from §7)
- ≥ 5 honest C3 (C1-C8 from §8)
- Trigger condition: OPT-A Phase 2 redo PASS confirmed differential + explicit user $20-100 cost ACK

---

## §10 — raw compliance

- **raw#9** (md only / py opt-out): OK — this spec is .md only; `tool/transient_py/clm_v4_lora_train.py` mutation deferred to Phase 1 (which itself stays in transient_py opt-out namespace per .own 4)
- **raw#10** (≥ 5 honest C3): OK — 8 honest C3 entries above
- **raw#15** (additive only): OK — does not mutate parent CLM-2 spec, does not mutate `.roadmap.clm`, does not mutate shim v4 / v5 source, does not mutate CLM-2-EXEC v1 adapter
- **raw#71** (falsifier pre-register): OK — F-OPT-B-1..5 thresholds, §3 hyperparameters, §5 phase budget envelopes are all LOCKED at this spec landing
- **CRITICAL flags from BG instruction**: no git commit (defer to user) + no exec (spec only) + no `.roadmap.*` mutation (proposal only) — ALL respected

---

## §11 — Artifacts

| Artifact | Path | Status |
|---|---|---|
| Spec (this file) | `docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_2026_05_05.md` | LANDED $0 mac |
| Companion handoff | `docs/clm_v4_lora_sft_opt_b_cross_attn_retrain_spec_landed_2026_05_05.ai.md` | LANDED $0 mac (sister file) |
| Phase 1 amendment | `docs/clm_v4_lora_sft_opt_b_amendment_2026_05_05.md` | DEFERRED (Phase 1 dispatch) |
| Phase 2 smoke verdict | `state/clm_v4_lora_sft_opt_b_smoke_2026_05_05/verdict.json` | DEFERRED (Phase 2 dispatch) |
| Phase 3 retrain verdict | `state/clm_v4_lora_sft_opt_b_2026_05_05/verdict.json` | DEFERRED (Phase 3 — REQUIRES USER ACK) |
| Phase 4 eval verdict | `state/clm_v4_lora_sft_opt_b_eval_2026_05_05/verdict.json` | DEFERRED (Phase 4) |
| Phase 5 promote spec | `docs/clm_v4_lora_sft_opt_b_promote_spec_2026_05_05.md` | DEFERRED (Phase 5, conditional) |
| Train script (amended) | `tool/transient_py/clm_v4_lora_train.py` (Phase 1 amendment) | DEFERRED |
| Phi probe helper | `tool/transient_py/clm_v4_lora_phi_canonical.py` (CLM-2-EXEC v1 carry) | UNCHANGED |
| Eval helper | `tool/transient_py/clm_v4_lora_eval.py` (CLM-2-EXEC v1 carry) | UNCHANGED |
| Parent CLM-2 spec | `docs/clm_v4_lora_sft_spec_2026_05_04.md` | UNTOUCHED (additive amendment only in Phase 1) |
| Shim v4 LOCKED | `tool/transient_py/clm_v4_hf_format_shim.py` | UNTOUCHED |
| Shim v5 (OPT-A scope) | `tool/transient_py/clm_v4_hf_format_shim_v5.py` | UNTOUCHED by OPT-B (orthogonal investigation) |

---

**END SPEC — LANDED $0 mac, exec deferred, dispatch contingent on OPT-A + user cost ACK.**
