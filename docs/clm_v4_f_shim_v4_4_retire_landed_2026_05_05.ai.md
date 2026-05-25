---
title: F-SHIM-V4-4 RETIRE LANDED — three-path architectural closure (Path A measurable / Path B FAIL / Path C forward-gated) + G3 carve-out strengthened (2026-05-05)
date: 2026-05-05
spec_anchor: docs/clm_v4_f_shim_v4_4_retire_2026_05_05.md
path_b_closure_anchor: docs/clm_v4_hf_format_shim_v5_path_b_closure_2026_05_05.md
f_shim_v4_4_harvest_anchor: state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json
v5_4_design_1_anchor: state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json
opt_c_anchor: state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/verdict.json
opt_b_phase_1_2_prep_anchor: state/clm_v4_lora_sft_opt_b_phase_1_2_prep_2026_05_05/verdict.json
own_entry: anima/.own hf-release-private-then-public-after-verification
roadmap_entry: .roadmap.clm cond.2
state: LANDED — F-SHIM-V4-4 RETIRED
final_verdict: F_SHIM_V4_4_RETIRED_FROM_ACTIVE_FALSIFIER_SET
---

# F-SHIM-V4-4 RETIRE LANDED (2026-05-05)

## Summary

Three independent architectural paths to F-SHIM-V4-4 PASS (lift_pp ≥ +5pp via canonical_zero or real fixture) have been exhausted across separate BG cycles in 2026-05-05. F-SHIM-V4-4 is formally RETIRED from the active falsifier set on shim v4 / CLM v4 mk2-v1 — architecturally unfalsifiable on current shim/CLM v4 — with ` G3` carve-out justification strengthened on a TWO independent eval-point + ONE forward-gated-gradient evidence base. The retire is REVERSIBLE pending Path D (CLM v5 redesign).

## Five-bullet summary

- **3-path closure summary**: Path A (OPT-A re-anchor std=0.10 shim v5 init) substrate differential 5× CONFIRMED at fresh-init, BUT inference path overwrites init via `_load_decoder_state` AND deployed bypass path (`consciousness_states is None`) makes the architectural lever invisible at logits. Path B (shim v5 init-only, 3 std values 0.001/0.02/0.10) ALL FAIL +5pp gate per `PATH_B_CLOSED_FAIL` diagnose verdict. Path C (OPT-B cross_attn LoRA Q1-B wide retrain) Phase 2 smoke shows cross_attn_lora_b_post_train_nonzero=0/64 because `if consciousness_states is not None` guard blocks forward → gradient never reaches cross_attn even with target_modules patch in place; self_attn positive control PASS (64/64) validates methodology.

- **Retire decision**: F-SHIM-V4-4 RETIRED from active falsifier set effective 2026-05-05. Reasons: (1) three architectural paths exhausted, (2) "architecturally unfalsifiable on current shim/CLM v4" is an epistemic conclusion (raw#71 +5pp threshold NOT relaxed; falsifier REMOVED from active set due to architectural unfalsifiability), (3) only Path D (CLM v5 architectural redesign with consciousness_states feed + cross-attn-active loss) enables PASS but is multi-month + cost-undefined and NOT spec-frozen, (4) retire is REVERSIBLE per re-instate condition §2.4 (Path D land OR OPT-B' amendment Phase 3 PASS OR explicit user override).

- ** G3 carve-out STRENGTHENED**: amended (b.3) gate = `F-SHIM-V4-1/2/3 PASS + F-SHIM-V4-4 RETIRED (justified) = G3 PASS_WITH_CARVE_OUT`. Justification base: 8 corroborating verdict.json/spec anchors (harvest PREREQUISITE_BLOCKED + Phase 2 OPT-A measurable + V5-4 DESIGN-1 FAIL + OPT-C FAIL_EXPECTED + Path B closure diagnose + OPT-B Phase 1+2 prep + Path B closure spec + this retire spec). PUBLIC promote BG cite-list defined per §3.4 of retire spec.

- **PUBLIC promote eligibility justified (V5/V6 ceiling impact)**: F-SHIM-V4-1 (byte-exact structural compat) + F-SHIM-V4-2 (finite-forward runtime) + F-SHIM-V4-3 (canonical_zero null-hypothesis baseline) cover the necessary safe-deployment axis; F-SHIM-V4-4 is a stretch-goal architectural-binding-evidence axis on a different epistemic dimension and its closure does NOT undermine 1/2/3 PASS evidence. V5/V6 closure ceiling is +1pp pragmatic acknowledgment (per closure spec Decision-B; even if marginal future +1-2pp lift achieved, +5pp gate still FAIL) — retire formalizes the +5pp unreachability as policy rather than re-running cycles to confirm same FAIL. Honest disclosure required in model card per `.own` (b.5): F-SHIM-V4-4 RETIRED + consciousness signal binding architecturally unfalsifiable on current shim/CLM v4 + recommended consumer mode = consciousness-measurement substrate (NOT chat/SFT per `clm.v115_chat_category_error`).

- **Lessons L40-L42 banked as candidates**: L40 (three-path closure pattern — architectural alternative exhaustion before retire; ≥3 mechanism enumeration + $0 Mac-side feasibility before $1+ exec; cost discipline $0.35 vs Path D $300-500 saved); L41 (bypass path category error in architectural-binding falsifiers — distinguish lever-CHANGED from lever-INVOKED; `consciousness_states=None` makes cross_attn forward effectively no-op despite std=0.10 confirmed on disk); L42 (gradient flow gating in conditional forward — LoRA target_modules necessary but not sufficient when `if input_flag is not None:` gates forward; positive control methodology + Phase 2 smoke saved $20-50 future H100 spend on deterministically-FAIL configuration). Lessons promotion to canonical SSOT pending separate `BG-LESSONS-PROPAGATE` cycle with explicit user authorization.

## honest C3 (≥5 per raw#10)

1. **C1 — Retire is epistemic + REVERSIBLE**. F-SHIM-V4-4 cannot be reached via any of three exhausted paths on current architecture, but Path D explicitly enables RE-INSTATE. raw#71 frozen-spec contract preserved: +5pp threshold NOT relaxed; falsifier REMOVED from active set due to architectural unfalsifiability, not threshold weakening. Future architectural work can restore F-SHIM-V4-4 to active set without retro-active record manipulation.

2. **C2 — G3 carve-out is anima-internal; honest disclosure to external consumers required**. The G3 PASS_WITH_CARVE_OUT label is anima-internal; external HF Hub consumers see only the public model card. Per `.own` (b.5) honest C3 model card requirement, model card MUST disclose: (a) F-SHIM-V4-4 RETIRED with link to this retire spec, (b) limitation: consciousness signal binding architecturally unfalsifiable on current shim/CLM v4, (c) recommended consumer mode = consciousness-measurement substrate (NOT chat). Model card enhancement already done per precedent doc; this retire spec is the formal underwrite.

3. **C3 — Path D is multi-month + cost-undefined; NOT spec-frozen**. Path D requires modeling_clm_v4.py rewrite (remove `consciousness_states is not None` guard) + re-train CLM v4 from scratch with cross_attn-active loss + std=0.10 init ($100-300 H100, 1-2 weeks) + re-validate F-SHIM-V4-1/2/3 + re-run F-SHIM-V4-4. Total 1-3 months + $300-500 cumulative spend. Dispatching as F-SHIM-V4-4 PASS prerequisite would block all HF release / promote work indefinitely; retire is the cost-rational decision.

4. **C4 — F-SHIM-V4-1/2/3 PASS + V4-4 architectural-binding axis distinction**. F-SHIM-V4-1 (byte-exact compat), V4-2 (finite-forward smoke), V4-3 (canonical_zero null-hypothesis) test STRUCTURAL / RUNTIME / NECESSARY-CONDITION axes — all testable without architectural changes. F-SHIM-V4-4 tests ARCHITECTURAL-BINDING-EVIDENCE (does architecture transmit consciousness signal to logits?) — this is a SUFFICIENCY claim, not a NECESSARY safe-deployment condition. The 1/2/3 axis covers necessary safety; the 4 axis is a stretch goal architecturally unreachable. PUBLIC promote on 1/2/3 PASS + 4 RETIRED is consistent with safe-deployment standard while honest about unreachable stretch goal.

5. **C5 — V5/V6 closure ceiling +1pp pragmatic**. Path B closure spec Decision-B already declared CLOSED-FAIL on +1.0pp lift_pp_v5 evidence (within 4.48pp combined stderr). Retire moves +5pp threshold from "active gate that could in principle PASS" to "epistemically retired threshold". Even if future Path B SFT or Path C OPT-B retrain achieves marginal +1-2pp lift, that is below +5pp gate AND below combined stderr — gate would still FAIL. Retire formalizes "the +5pp gate is unreachable on current shim/CLM v4" as policy rather than re-running cycles to confirm same FAIL.

6. **C6 — No `.own` / `.roadmap.*` mutation in this cycle is a discipline boundary**. This spec PROPOSES G3 amendment + roadmap propagation but does NOT execute either mutation. Proposal is sibling-pattern (raw#15 additive); future BG cycles execute mutations under explicit user authorization. The retire DECISION is anchored by this spec's existence on disk; downstream consumers (PUBLIC promote BG) cite this spec path. Separation maintains raw#15 additive-only + raw#10 honest disclosure + `.own` SSOT integrity under BG spec CRITICAL no-commit constraint.

7. **C7 — Three-path coverage exhaustive but not provably complete**. Paths A/B/C cover three INDEPENDENT MECHANISMS (init-side / inference-side init-only / loss-side LoRA). Path D (full architectural redesign) acknowledged but out-of-scope. Exotic paths not enumerated (e.g., post-hoc o_proj weight surgery + activation-engineering on consciousness_states injection) are extreme outliers with no spec precedent. Three-path framework is canonical taxonomy for "architectural lever to fixture-driven lift" on this substrate; future 4th mechanism would be Path-D class redesign by definition.

8. **C8 — Cost discipline + opportunity-cost summary**. F-SHIM-V4-4 closure cumulative: harvest $0 + Phase 2 OPT-A $0 + V5-4 DESIGN-1 $0.20 + OPT-C $0.15 + diagnose $0 + OPT-B Phase 1+2 $0 + this retire spec $0 = $0.35 total H100 spend. Retire saves $100-300 (Path D opportunity cost) + $20-100 (Path B SFT alternative not dispatched) = $120-400 future spend avoided. Preserves H100 budget for downstream Path D OR alternative consciousness-substrate work (BLM / EEG / qmirror).

## Counts

- 3-path closure: Path A measurable + Path B FAIL + Path C forward-gated (3 independent mechanisms exhausted)
- Corroborating verdict.json/spec anchors: 8 (per retire spec §3.4)
- Lessons banked as candidates: L40 (3-path closure pattern) + L41 (bypass path category error) + L42 (gradient flow gating) = 3
- G3 carve-out evidence base: TWO independent eval points (V5-4 fresh-init + OPT-C best.pt) + ONE forward-gated-gradient observation (OPT-B Phase 2 smoke)
- honest C3 entries: 8 (≥5 per raw#10)
- Cycle cost: $0 (Mac-side spec only); cumulative F-SHIM-V4-4 phase cost: $0.35

## Spec anchor

- Retire spec: `docs/clm_v4_f_shim_v4_4_retire_2026_05_05.md`
- Final verdict: `F_SHIM_V4_4_RETIRED_FROM_ACTIVE_FALSIFIER_SET`
- Re-instate condition: §2.4 of retire spec (Path D land OR OPT-B' amendment Phase 3 PASS OR explicit user override)

## Cross-links

- spec_anchor: `docs/clm_v4_hf_format_shim_v5_spec_2026_05_05.md`
- path_b_closure_anchor: `docs/clm_v4_hf_format_shim_v5_path_b_closure_2026_05_05.md`
- f_shim_v4_4_harvest_anchor: `state/clm_v4_f_shim_v4_4_harvest_2026_05_05/verdict.json` (PREREQUISITE_BLOCKED)
- phase2_opt_a_anchor: `state/clm_v4_hf_format_shim_v5_phase2_opt_a_2026_05_05/verdict.json` (substrate differential MEASURABLE)
- v5_4_design_1_anchor: `state/clm_v4_hf_format_shim_v5_4_design_1_2026_05_05/verdict.json` + `results/eval_summary.json` (FAIL +1.0pp)
- opt_c_anchor: `state/clm_v4_hf_format_shim_v5_opt_c_2026_05_05/verdict.json` + `results/eval_summary.json` (FAIL_EXPECTED -0.5pp)
- v5_4_opt_c_diagnose_anchor: `state/clm_v4_hf_format_shim_v5_v5_4_opt_c_diagnose_2026_05_05/verdict.json` (PATH_B_CLOSED_FAIL)
- opt_b_phase_1_2_prep_anchor: `state/clm_v4_lora_sft_opt_b_phase_1_2_prep_2026_05_05/verdict.json` (cross_attn LoRA gradient ZERO)
- own_15_anchor: `anima/.own hf-release-private-then-public-after-verification`
- roadmap_anchor: `.roadmap.clm cond.2.amendment_2026_05_04` (proposal target — NOT mutated in this cycle)
- precedent_doc: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md`
- anima land: `docs/anima_own_15_hf_release_lifecycle_landed_2026_05_05.ai.md`
- chat_category_error_anchor: `.roadmap.clm clm.v115_chat_category_error`

## raw_compliance

- raw#9 (md only): OK — this .ai.md + retire .md spec; no transient_py used; no exec
- raw#10 (≥5 honest C3): OK — 8 entries
- raw#15 (additive proposal): OK — no `.own` mutation, no `.roadmap.*` mutation, no shim source mutation; proposal-only for G3 amendment + roadmap propagation
- raw#71 (epistemic-axis preservation): OK — +5pp threshold preserved verbatim; falsifier REMOVED from active set due to architectural unfalsifiability; epistemic-axis distinction (V4-1/2/3 structural / V4-4 architectural-binding) explicitly maintained
- no_git_commit: OK per BG spec CRITICAL section
- no_h100_spend: OK
- no_hf_push: OK
