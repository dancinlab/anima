---
schema: anima/anima-eeg/docs-ai-native/1
last_updated: 2026-05-03
parent: anima-eeg/README.ai.md
status: scaffold-only
raws: [R10, R65]
---

# anima-eeg/docs/ai-native

Agent-first documentation. `.ai.md` with YAML frontmatter (schema, ssot, status, raws), ranked for LLM cold-start.

## Distinguishes from docs/user/

- ai-native = TL;DR + architecture map + raw caveats, optimized for cold-start LLM reading
- user = human prose, runbooks, narrative

## Currently landed

- README.ai.md (this file)
- anima_eeg_structure_refactor_plan_2026_05_03.ai.md

## Migration candidates next cycle (19 .md at anima-eeg/docs/)

ai-native targets: anima_eeg_protocols_quickstart, cyton_daisy_wiring_diagram, cyton_soft_reset_v_command_spec, full_helmet_health_view_design, headplot_ascii_design, impedance_z_command_implementation_plan, preflight_re_cascade_hook_spec, rich_tui_upgrade_design

user targets: cyton_first_real_session, commit_msg_diff_alignment_lint, d_day_helmet_session_results, electrode_adjustment_16ch_concurrent, integration-guide, openbci_bundle_ear_clip_options, openbci_ear_pad_audit, openbci_gui_lsl_coexistence, openbci_pragma_practice, phase4_remaining_priority1_3_landing, phase4_remaining_priority4_7_landing

## Caveats

1. Triage is suggestion, not committed. Final decision at actual move cycle.
2. .md to .ai.md rename requires adding YAML frontmatter.
3. External index (ready/.growth/absorbed/) not auto-updated by scaffold.
