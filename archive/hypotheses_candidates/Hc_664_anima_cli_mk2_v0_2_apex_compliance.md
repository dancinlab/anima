---
id: Hc_664
slug: anima-cli-mk2-v0-2-apex-compliance-refinement
title: anima cli mk2 v0.2 refinement (289→638 LoC, 7→14 sections, 5→8 falsifiers, 6→10 honest C3) 가 hive mk2_apex (1535 LoC) compliance
domain: anima-cli
status: candidate-unverified
source_doc: docs/anima_cli_mk2_v0_2_refinement_landed_2026_05_06.ai.md
source_lines: 28-80
promoted_at: 2026-05-11
linked_h: hive/spec/mk2_apex.spec.yaml, raw#15 additive, ALM 영구 보류
notes: F-anima_cli-6 (backend_canonical=anima-native invariant) SPEC-STUB until Phase 2. F-7 30d 무진전 strengthen_or_retire. F-8 spec↔roadmap bidirectional drift.
---

## Hypothesis
anima cli mk2 v0.2 가 hive mk2_apex (Section 8 backend_stack_versions / 9 compatibility_matrix / 10 mk2_apex_compliance / 11 enforcement / 12 agent_directive / 13 status_lifecycle / 14 hive_prefs_compliance) 7개 신규 section + 3 falsifier + 4 honest C3 추가로 apex compliance 충족 — 단 9 compliant_items + 10 gaps_remaining (G1-G10 severity+resolution_phase). raw#15 additive: 기존 v0.1 entry 0건 변경.

## Falsifiable Tests
- F-anima_cli-6: backend_canonical=anima-native invariant 강제 — Llama/Mistral 진입 시 hard_fail (SPEC-STUB until Phase 2 T1 wire BG)
- F-anima_cli-7: gaps_remaining G1-G10 30d 무진전 → strengthen_or_retire (apex F-MK2-APEX-4 mirror)
- F-anima_cli-8: spec ↔ .roadmap.cli mk1 entries bidirectional drift → amend_spec_or_roadmap

## Migration TODO
- [ ] Phase 2 T1 backend wire BG (F-anima_cli-6 lift SPEC-STUB)
- [ ] BR-MK2-AI-NATIVE-ENGLISH-ONLY 2026-05-20 mass conversion
- [ ] enforcement runtime grep lint tool (Phase 1.5)
- [ ] 10 gaps_remaining G1-G10 closure
