# LZ76 SSOT Mirror Audit — 2026-04-28

Follow-up to commit 98d61133 (Schartner retraction in clm_eeg_lz76_real.hexa).

Purpose: locate every file that mirrors the frozen LZ76 criteria
(C1=650, C2=200, baseline=850) or the Schartner 2017 / 0.85 references,
classify each as **mirror** (needs same C3 retraction) or **descriptive**
(narrative reference, out of scope for own4 root-cause-only).

## Tier-1 SSOT mirrors (uchg-locked, retraction REQUIRED)

| File | Lines | Issue | Action |
|---|---|---|---|
| `anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa` | 13, 43, 61, 296, 302 | "Schartner 2017" cited as criterion source; 0.65 floor labelled paper-derived | unlock → retract → relock → audit |
| `state/clm_eeg_p1_lz_pre_register.json` (uchg) | 31, 37 | cert.note + workflow.replace cite "Schartner 2017" | regenerate from .hexa run after fix (auto) |

## Tier-2 cert / runtime artifacts (selftest output, gitignore candidate)

| File | Status | Action |
|---|---|---|
| `state/clm_eeg_p1_lz_pre_register_real.json` | tracked + modified; selftest auto-output (timestamp + random/structured mode flips per run) | git rm --cached → add to .gitignore |

## Tier-3 narrative descriptions (out of scope, own4 root-cause-only)

These cite "Schartner 2017" as a literature reference without claiming it
is the source of the 0.65/0.85/200 frozen values. They predate the
retraction; rewriting all of them is cosmetic mass edit. Recommended:
add a forward-pointer in clm_eeg_lz76_real.hexa header (already done in
commit 98d61133); leave historical docs intact.

- design/eeg_daily_life_paradigm_design_2026_04_28.md (5 hits)
- design/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md (5 hits)
- design/anima_legacy_tech_eeg_integration_omega_cycle_2026_04_28.md (5 hits)
- design/anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md (2 hits)
- docs/phenomenal_consciousness_measurable_surrogates_20260425.md (2 hits)
- docs/clm_research_handoff_20260427.md (1 hit)
- docs/eeg_cross_substrate_validation_plan_20260425.md (1 hit)
- anima-clm-eeg/docs/{eeg_arrival_impact_5fold,g8_transversality_landing,clm_eeg_d_day_chain_review_20260427_landing,omega_cycle_mk_xii_phenomenal_axis_20260426}.md
- tool/an11_b_v_phen_lz_complexity.hexa (not uchg, descriptive header)
- tool/an11_consciousness_unified_verifier.hexa (not uchg, descriptive header)
- anima-eeg/tool/eeg_daily_life_verifier.hexa (not uchg, descriptive header)
- state/cp2_dry_run_synthetic/{p1_lz/result.json,summary_dry_run.json} (historical dry-run cert)
- state/phenomenal_surrogate_proposals_20260425.json (proposal-stage doc)
- recordings/sessions/baseline_resting_60s_20260428_filtered.json (run-time annotation)

## raw#10 honest C3 — main file vs mirror alignment

After retraction:
- `clm_eeg_lz76_real.hexa` (main, 98d61133): explicit 2015/2017 disambig + Bódizs binarisation note + "operational pre-commitment" relabel
- `clm_eeg_p1_lz_pre_register.hexa` (mirror, this audit): SAME retraction applied
- `clm_eeg_p1_lz_pre_register.json` (mirror cert): regenerated from .hexa after fix
