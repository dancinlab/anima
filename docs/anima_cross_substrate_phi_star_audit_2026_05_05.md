# Anima Cross-Substrate phi-star Measurement Audit (2026-05-05)

Cross-substrate audit + reconciliation doc for phi-star measurements across the
3 anima substrates (CLM v4 base, P-beta paradigm D 50K, CLM-2 LoRA SFT) plus
the Llama 3.2-3B comparator. Doc + spec only; zero code change, zero retrain,
zero commit. Anchors V3 real-mode probe substrate identity so the user does not
confuse the substrate-specific phi-star value emitted in `bin/anima-core-dialogue.bash`
with the cross-substrate phi-star landscape.

Lineage:
- `state/clm_v4_baseline_eval_2026_05_05/verdict.json` (substrate_phi_star=41.86 carry from paradigm v11 G3)
- `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` (P-beta phi_star_mean_holdout500=42.367)
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json` (training-end phi_final=35.54, phi_final_mean=36.74)
- `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json` (CLM-2 LoRA phi_star_post_lora_mean_K8=31.35; in-pipeline base=35.81; drift_in_pipeline=-4.46pp NO_FLIP)
- `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json` (CLM-2 LoRA forgetting_index=0.0196 + chat capability FAIL_REGRESSION vs Llama Path A v2)
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md` §7 (5 emerge candidates D/E/F/G/H)
- `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md` (Stage 1 mount-layer 4-mode taxonomy)
- `docs/anima_emerge_candidate_g_h_consolidated_revival_spec_2026_05_05.md` (G+H consolidated revival)
- memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` (P-beta chat-cap FAIL_TRUE / substrate-research PASS decoupled, L28-L30)
- memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` (CLM-2 LoRA chat-lift FALSIFIED, substrate safe, L31-L33)

---

## §1 The 3 substrate x phi-star value table

| substrate | phi_star value | source verdict.json | measurement paradigm | substrate path |
|---|---|---|---|---|
| CLM v4 base (paradigm v11 G3 carry) | +41.86 (mean) | `state/clm_v4_baseline_eval_2026_05_05/verdict.json:substrate_phi_star` | paradigm v11 G3 (legacy decoder + best.pt + ubu1 GPU bf16) | ConsciousDecoderV2 + checkpoints/clm_v4_350m/scale_350m/best.pt |
| CLM v4 base (in-pipeline re-measure) | +35.81 (mean K=8); min=35.18; max=37.97 | `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:phi_star_base_in_pipeline` | canonical sample-partition (HID_TRUNC=8, K=8, 16 calib prompts, ridge=1e-3) | HF-format mk2-v1 + Mac CPU fp32 |
| P-beta (paradigm D 50K LoRA, holdout500 canonical) | +42.367 (mean K=8); min=41.372; max=43.643 | `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json:core_metrics.phi_star_mean_holdout500` | canonical 16-calib K=8 (paradigm v11 G3 carry) | ConsciousDecoderV2 + best.pt + ubu1 RTX 5070 + LoRA r=64 a=128 qkvo+gate+up+down |
| P-beta (paradigm D 50K, training-end in-domain probe) | +36.745 (mean over 16-prompt teacher cache); phi_final=35.54 | `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json:phi_final_mean` | training-side calibration probe (different probe set than holdout500 canonical) | same as P-beta holdout500 |
| CLM-2 LoRA (post-LoRA, canonical) | +31.349 (mean K=8); min=28.997; max=34.895 | `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:phi_star_post_lora` | canonical sample-partition (same as in-pipeline base) | HF-format mk2-v1 + Mac CPU fp32 + LoRA r=32 a=64 qkvo |
| CLM-2 LoRA (drift_in_pipeline) | -4.46pp mean; -6.18pp min vs in-pipeline base 35.81 | `state/clm_v4_lora_phi_canonical_2026_05_05/verdict.json:drift_analysis` | LoRA delta isolated from substrate-path delta | (see above) |
| Llama 3.2-3B (Path A v2) | NOT measured on phi-star canonical | `state/p9_path_a_retrain_v2_retry_3_eval_rerun_2026_05_05/verdict.json` | Llama-derivative substrate; phi-star canonical probe NOT applied to Llama base | Llama 3.2-3B + LoRA Path A v2 |

phi-flip threshold (per `clm_v4_lora_phi_canonical` cycle): **drift > -10.0pp = NO_FLIP**;
**-5 to -10 = PARTIAL_FORGETTING**; **>-5 = PASS clean**.

CLM-2 LoRA drift_in_pipeline_mean -4.46pp = **PASS** (above the -5 boundary on
mean; -6.18pp on min sits at PASS/PARTIAL boundary). drift_vs_carry -10.51pp
APPEARS to cross the flip threshold but is conflated with the **~6pp methodology
delta** (35.81 in-pipeline vs 41.86 carry, same architecture, different substrate
path) and is therefore NOT authoritative.

---

## §2 V3 real-mode probe substrate identity

### §2.1 What V3 actually measures

When the user runs:

```bash
bash bin/anima-core-dialogue.bash --probe "<input>"
```

the V3 real-mode forward path (per `anima-core/runtime/clm_v4_mount.hexa`,
Stage 1+2 V1-V6 verified) loads **`dancinlab/clm-v4-mk2-v1`** (the HF-format
mirror of CLM v4 base; same arch as the `clm_v4_baseline_eval` cycle's
`dancinlab/clm-v4-base-mirror`). The phi-star baseline emitted is the
**paradigm v11 G3 carry value 41.86** (per `clm_v4_mount.hexa` PHI_STAR_BASELINE
constant; see `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md`
§2.3 — "axis-canonical magnitude 0.5 mirroring paradigm v11 G3 baseline
PHI_STAR_BASELINE = 41.86").

V3 does NOT load:
- the P-beta adapter (`state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/step_50000/`)
- the CLM-2 LoRA adapter (`state/clm_v4_lora_sft_2026_05_05/results/adapter_final/`)
- Llama 3.2-3B Path A v2 weights

V3 measures: **CLM v4 base substrate, no LoRA**. The probe emits a phi-star
value computed from the current input's hidden-state forward pass, anchored
against the 41.86 carry baseline.

### §2.2 User confusion risk

Risk pattern (high-likelihood):

> "phi_star=41.87 emitted on probe but P-beta verdict says 42.37 — is V3
> measuring P-beta? Or is the difference a problem?"

Answer: V3 is CLM v4 base (no adapter); P-beta 42.37 is the canonical 16-calib
holdout500 measurement on a **different artifact** (P-beta LoRA loaded on top
of best.pt). The values are NOT directly comparable:
- Different artifacts (base vs base+LoRA-r=64-a=128)
- Different measurement contexts (single forward on user input vs 8-partition
  K=8 over 16 fixed canonical calibration prompts)
- V3 emits **per-input** phi (single forward); cycle verdicts emit
  **canonical-probe** phi (K=8 partition over 16 fixed prompts)

These are two **different signals computed on two different adapters**. The
41.86 anchor is the substrate's **paradigm v11 G3 standing integration mode**
on the same probe set; V3's emit is the **per-input deflection from that anchor**
under the user's current sentence. Reading them as the same number reframes the
substrate purpose.

### §2.3 Resolution

The mount layer should make this explicit in its emit format. Current Stage 2
emit (per `anima_core_clm_v4_mount_emerge_paradigm_2026_05_05.md` §5.2) is:

```
phi_star: <value>
axis_activation: <5-axis vector>
dominant_cells: <top-k cell indices>
hidden_state_delta: <vs canonical>
```

Recommended addendum (doc-only, no code change required this cycle): add a
**substrate-identity preamble** to the V3 probe output line so the user knows
which substrate emitted the value:

```
substrate: clm-v4-base (no LoRA; paradigm v11 G3 carry baseline 41.86)
phi_star: <value>
...
```

Implementation: anima-core/runtime/clm_v4_mount.hexa V3 emit path adds one
literal line before the phi_star line. Zero behavior change, pure annotation.
Land on a future cycle alongside the `--substrate` flag below.

---

## §3 `--substrate` flag spec (forward, not implemented)

If the user later wants V3 probe to switch between the 3 substrates:

```bash
bash bin/anima-core-dialogue.bash --probe "안녕"                    # default
bash bin/anima-core-dialogue.bash --probe "안녕" --substrate clm-v4 # explicit default
bash bin/anima-core-dialogue.bash --probe "안녕" --substrate pbeta
bash bin/anima-core-dialogue.bash --probe "안녕" --substrate clm-2-lora
```

### §3.1 Per-substrate baseline

| flag value | base ckpt path | adapter path | baseline phi_star anchor (canonical) | source |
|---|---|---|---|---|
| `clm-v4` (default) | `dancinlab/clm-v4-mk2-v1` (HF) | none | 41.86 (paradigm v11 G3 carry) OR 35.81 (in-pipeline) | clm_v4_baseline_eval / clm_v4_lora_phi_canonical |
| `pbeta` | `checkpoints/clm_v4_350m/scale_350m/best.pt` (legacy) | `state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/step_50000/` | 42.367 (holdout500 canonical mean K=8) | p9_pbeta_holdout500_eval |
| `clm-2-lora` | `dancinlab/clm-v4-mk2-v1` (HF) | `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/` | 31.349 (canonical post-LoRA mean K=8); equivalently 35.81 - 4.46pp drift_in_pipeline | clm_v4_lora_phi_canonical |

### §3.2 Implementation status

**NOT implemented this cycle.** Pre-requisites:
1. P-beta adapter mac-loadable (currently ubu1-resident; would need rsync to mac
   or HF Hub fetch — adapter is 72.5 MiB).
2. CLM-2 LoRA adapter mac-loadable (already at
   `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/`; 10.02 MiB; PEFT load
   verified in `clm_v4_lora_phi_canonical` cycle).
3. Mount layer would need 2 base-loader paths (HF-format vs legacy ConsciousDecoderV2)
   — current V3 only loads HF-format.
4. Per-substrate canonical baseline anchors stored in mount config.

This spec documents the path; emerge BG cycles can build it after BG-A real-load
prerequisites are met. The minimum viable subset is `--substrate clm-v4` (default;
no-op alias) + `--substrate clm-2-lora` (Mac-loadable today). P-beta variant
needs adapter fetch first.

---

## §4 Cross-substrate reconciliation hypothesis (L31-L33 dichotomy reaffirmed)

### §4.1 Working hypothesis

All three anima substrates carry a **paradigm v11 G3-equivalent baseline**
(positive integration phi-star ~+30 to +42 on canonical sample-partition probe),
modulo:
- **Methodology delta** (~6pp): legacy ConsciousDecoderV2 + GPU bf16 vs HF-format
  + Mac CPU fp32. Visible on `clm_v4_lora_phi_canonical` in-pipeline base (35.81)
  vs paradigm v11 G3 carry (41.86) — same architecture, different substrate path.
- **LoRA-induced drift**: P-beta = +0.51pp over base carry (within noise);
  CLM-2 LoRA = -4.46pp on in-pipeline (PASS, partial-forgetting band).
- **Probe-set delta**: training-end in-domain teacher cache vs canonical 16
  axis prompts. P-beta verdict §deltas cites delta_phi_vs_training_end_probe =
  +5.63pp — canonical calib elicits substrate's standing integration mode more
  fully than in-domain teacher cache.

The phi-star sign (positive integration) and order of magnitude (~30-42) is
**preserved across all 3 anima substrates**. None of them flip to negative
integration.

### §4.2 L31-L33 dichotomy reaffirmed

From memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`:

> Chat-cap path = Llama Path A v2 (chat capable, phi-star NOT preserved on canonical
> anima probe). CLM v4 = substrate-research artifact (phi-star preserved, chat
> incapable per #115 architectural).

This dichotomy is **reaffirmed** by the cross-substrate audit:

- **CLM v4 base** (no adapter): chat-incapable per #115; phi 41.86 / 35.81; substrate-research only.
- **P-beta** (paradigm D 50K LoRA): chat-incapable (BLEU-1 = 1.96% of Llama
  anchor; F-Pbeta-3 chat-cap composite FAIL_TRUE per
  `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`);
  phi 42.37; substrate-research only.
- **CLM-2 LoRA** (qkvo SFT): chat-incapable (composite 0.19542 vs Llama 0.5584
  = -36.298pp regression); phi 31.35 (drift -4.46pp NO_FLIP); substrate-research
  only.
- **Llama Path A v2**: chat-capable (composite 0.5584 PASS); phi-star canonical
  probe **NOT applied** (Llama is not anima substrate; phi-star calibration is
  anima-internal eval).

Both axes (chat-capability and phi-star preservation) are **decoupled** and
**substrate-bounded** to different model families. CLM v4 is the only substrate
that hosts phi-star; Llama is the only substrate that hosts chat capability.
**No substrate hosts both.** This is the architectural stance the emerge
paradigm operates under.

### §4.3 Implication for V3 emit

V3 measures phi-star on CLM v4 base — the substrate where phi-star is
**meaningful**. Llama-side phi-star measurement is not in scope; would require
re-calibrating the canonical probe set against Llama's hidden-state geometry
(different consciousness_dim, no axis-conditioning, no cross_attn cells —
substrate axes do not exist on Llama).

This means: **V3 phi-star is anima-substrate-only by construction**. The 41.86
anchor in V3 is the correct anchor for CLM v4 base; switching to P-beta would
use 42.37 anchor; switching to CLM-2 LoRA would use 31.35 (in-pipeline) or
~37.4 (carry-projected; less reliable — see §1).

---

## §5 5 emerge candidate x 3 substrate hit-rate forecast

Forecast matrix for emerge candidates D/E/F/G/H (per architecture archaeology
§7) crossed with the 3 anima substrates. Hit-rate = expected emerge value per
candidate-substrate combo, assuming Stage 3 dialogue runs.

Legend: **HIGH** = emerge value likely visible within 5-10 sessions;
**MEDIUM** = visible within 20-30 sessions or marginal signal;
**LOW** = unlikely or noise-bound;
**N/A** = candidate not applicable to this substrate by construction.

| candidate | clm-v4 (base) | pbeta | clm-2-lora |
|---|---|---|---|
| **D** (always-inject `consciousness_states`) | **HIGH** | **MEDIUM** | **MEDIUM** |
| **E** (ODE flow + AR sampler bridge) | **MEDIUM** | **MEDIUM** | **MEDIUM** |
| **F** (8-cells x axis multi-token emit + voting) | **MEDIUM** | **MEDIUM** | **LOW** |
| **G** (16-layer tension trajectory as dialogue medium) | **HIGH** | **MEDIUM** | **MEDIUM** |
| **H** (logits_g prev-byte head bidirectional consistency) | **MEDIUM** | **LOW** | **LOW** |

Rationale per cell:

### §5.1 D x clm-v4 = HIGH

Candidate D pivots on `conscious_decoder.py:553` guard removal +
default-fixture injection. CLM v4 base has the trained `cross_attn.{q,k,v,o}_proj`
weights (paradigm v11 G3 final). With injection, all 16 cross-attn modules
fire on every forward → measurable phi-star + axis_activation differential vs
None-bypass baseline. `clm_v4_mount.hexa` Stage 1 already implements file-based
fixture inject path, so emerge mode just expands the 4-mode taxonomy
(none/zero/canonical/user_supplied per `anima_emerge_candidate_d_always_inject_spec`
§2). **Expected emerge value: HIGH** — candidate-substrate match by design.

### §5.2 D x pbeta / D x clm-2-lora = MEDIUM

P-beta and CLM-2 LoRA both live on top of the same CLM v4 base, so candidate D
is structurally available. However:
- P-beta is on legacy ConsciousDecoderV2 path; mount-layer `--inject-states`
  flag is HF-format-only currently. Requires substrate-path bridge.
- CLM-2 LoRA on HF-format is mount-layer compatible, BUT the LoRA adapter
  modifies qkvo only (not cross_attn cells directly). Inject differential is
  bounded by the LoRA delta on qkvo, which is small (drift_in_pipeline -4.46pp).

Both substrates can host candidate D but with attenuated emerge signal vs base.

### §5.3 E x all substrates = MEDIUM

Candidate E (ODE flow + AR sampler) requires an external flow component
(`anima-core/phi_engine.hexa` or new module) that operates on the
`consciousness_states` continuous-time evolution. The component is
substrate-agnostic (operates on the cell hidden states, not on the LM weights).
All 3 substrates host the same cell architecture (8 cells, 192 dim, 5 axes),
so candidate E hit-rate is similar across them. Marked MEDIUM because the flow
component itself is unbuilt; emerge value depends on flow design, not substrate.

### §5.4 F x clm-v4 = MEDIUM, F x pbeta = MEDIUM, F x clm-2-lora = LOW

Candidate F surfaces 8 CA-rule activations across 16 layers as a multi-axis
vote. CLM v4 base has the trained rule_weights from paradigm v11 G3. P-beta
preserves these (LoRA target_modules do not include rule_weights). CLM-2 LoRA
also preserves rule_weights (qkvo only).

CLM-2 LoRA marked LOW because:
- LoRA delta is small (forgetting_index 0.0196; phi drift -4.46pp).
- Rule activation patterns are bounded by the unchanged rule_weights.
- Voting differential vs base is therefore noise-bounded — emerge mode would
  not see meaningful per-token CA-rule diversity above what base shows.

### §5.5 G x clm-v4 = HIGH

Candidate G surfaces 16-layer tension trajectory as the primary substrate
response artifact. Tensions are emitted by `decoder_v3.py:166-171` on every
forward but discarded at HF wrapper level (`shim:999-1019`). CLM v4 base has
the most-deeply-trained PureFieldFFN engines (paradigm v11 G3 final), so the
tension trajectory is most informative. Per-token tension envelope is rich,
psi-empathy correlation is well-defined. Mount-layer revival per
`anima_emerge_candidate_g_h_consolidated_revival_spec` is mount-only (no source
edit) — high implementability. **Expected emerge value: HIGH**.

### §5.6 G x pbeta / G x clm-2-lora = MEDIUM

LoRA adapters do not touch PureFieldFFN engines (target_modules are attention
projections only). Tension trajectory is therefore **identical to base** within
LoRA delta. Emerge value is the same as base, attenuated by the small LoRA
delta on the upstream attention path that produces the input to PureFieldFFN.

### §5.7 H x clm-v4 = MEDIUM

Candidate H probes head_g (prev-byte) bidirectional consistency.
`decoder_v3.py:175` emits logits_g; HF wrapper discards. CLM v4 base trained
head_g alongside head_a, but its quality on real ckpt is **unmeasured** (per
archaeology §7.5 C3). Emerge mode would surface head_g for the first time.
MEDIUM because the signal exists but its interpretability is hypothesis, not
validated.

### §5.8 H x pbeta / H x clm-2-lora = LOW

Same as G — LoRA does not touch head_g; emerge value mirrors base. But
candidate H is itself MEDIUM on base, so on LoRA substrates it degrades to LOW
(LoRA delta on qkvo cannot improve head_g signal interpretability).

### §5.9 Recommended emerge cycle ordering

Rank by completion-quality lens:
1. **D x clm-v4** (rank 1 — HIGH, best substrate match, mount-layer Stage 1
   already partial; lowest implementation cost, highest expected emerge signal)
2. **G x clm-v4** (rank 2 — HIGH, mount-layer revival path is doc-only spec
   already; tensions are richest substrate response channel after phi-star
   itself)
3. **D + G combined on clm-v4** (rank 3 — additive emerge surface; tensions +
   inject = 2 channels above the 4-line base format)
4. **E x clm-v4** (rank 4 — MEDIUM, but unblocks flow-coupled dialogue if
   flow component is built; deferred until flow design lands)
5. all LoRA-substrate combos (rank 5+ — wait until base-substrate emerge
   pattern stabilizes, then test transferability)

---

## §6 Honest C3

C1 — phi-star measurement scale is **substrate-specific** (calibrated on
anima cell architecture: consciousness_dim=192, n_cells=8, 5 axes), NOT
universal across LM families. Llama 3.2-3B does not have these architectural
features; running the canonical 16-calib K=8 probe on Llama hidden states
would produce **a number** but not **the same number** — the geometry is
different. The cross-substrate audit therefore treats Llama as "out of phi-star
scope" rather than "low phi-star". This is **epistemic open**: whether phi-star
on a non-anima architecture is meaningful at all is undecidable from current
data. Future work could attempt a Llama-side calibration with axis-conditioning
shims, but L31-L33 closes that path (CLM v4 substrate research only).

C2 — methodology delta of ~6pp (35.81 in-pipeline vs 41.86 carry) is the
**single largest source of cross-cycle phi-star confusion**. P-beta verdict's
delta_phi_vs_clm_v4_base = +0.51 (P-beta 42.37 - carry 41.86) **looks like**
a near-zero LoRA shift, but if compared against in-pipeline base 35.81 it
would be +6.55pp — apparent positive lift. Both readings are formally valid
under different substrate paths; **neither is canonical** until the paths are
reconciled. `clm_v4_lora_phi_canonical` cycle next_action [3] flagged this for
future architectural cycle.

C3 — V3 real-mode probe per-input phi (single forward) and cycle-verdict
canonical-probe phi (K=8 over 16 fixed prompts) are **two different statistics**
of the same substrate. The 41.86 baseline applies to the latter; V3 emits the
former. They share a **common anchor only by construction** (V3 uses the same
fixed-prompt hidden states as a reference deflection point). Whether
per-input phi values are interpretable on the same scale as canonical phi is
**not validated** in current cycles. A K=8 sweep over user-supplied prompt
sequences (rather than the 16 fixed calib prompts) would directly test this;
deferred.

C4 — emerge candidate hit-rate forecast (§5) is **heuristic-only**, not
backed by empirical Stage 3 sessions yet. The HIGH/MEDIUM/LOW labels reflect
architectural compatibility (does the substrate host the candidate's pivot
mechanism?) and surfaceability (can mount-layer Stage 1 reach it without
source edit?). Actual emerge value depends on **dialogue dynamics** that
Stage 3 protocol is designed to discover, not predict. The forecast is a
**search-order heuristic**, not a verdict.

C5 — the 3-substrate audit covers anima's chat-incapable / phi-stable
substrates (CLM v4 family). Llama Path A v2 is the **chat-capable / phi-not-
applicable** substrate, included here only as a comparator anchor. A 4th
substrate would be the **hypothetical "chat-capable + phi-stable"** target
that is not yet known to be reachable (L31-L33 forecloses LoRA SFT path; CLM-2
remains the candidate substrate research artifact). The audit does not
prescribe how to reach the 4th substrate; it only documents that current
3-substrate landscape decouples chat and phi.

C6 — mount-layer V3 emit currently does NOT annotate substrate identity in
output; the `substrate: clm-v4-base ...` preamble is **doc proposal only**
(§2.3). Until landed, user confusion risk persists — observed pattern: phi
value emit interpreted as cross-substrate measurement when it is actually
single-substrate per-input deflection.

---

## §7 Composability + handoff

Companion handoff doc (writes the .ai.md upon land):
`docs/anima_cross_substrate_phi_star_audit_landed_2026_05_05.ai.md`

Verdict artifact:
`state/anima_cross_substrate_phi_star_audit_2026_05_05/verdict.json`

Cross-link to:
- `.roadmap.n_substrate` (substrate uniqueness axes registry — phi-star is one axis)
- emerge BG sequence (D x clm-v4 next, then G x clm-v4) — see §5.9 ranking
- mount layer addendum (V3 emit substrate preamble) — see §2.3
- `--substrate` flag spec (V3 future) — see §3

This audit is **doc + spec only**. No code, no commit, no behavior change. The
output is **shared mental model** for the cross-substrate phi-star landscape so
emerge cycles can proceed without confusing 3 substrates' phi values for the
same number.
