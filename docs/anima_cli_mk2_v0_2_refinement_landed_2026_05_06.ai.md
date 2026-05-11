---
schema: anima/docs/landing.ai.md/v1
last_updated: 2026-05-06
ssot: anima/spec/anima_cli_mk2.spec.yaml
project: anima
purpose: |
  anima cli mk2 v0.2 refinement landing — hive mk2_apex 정합 ↑ (Section 8-14
  신규, F-anima_cli-6/7/8 falsifier 신규, C7-C10 honest_c3 신규). raw#15
  additive only — 기존 v0.1 entry 0건 변경.
language: en+ko
canonical-files:
  - anima/spec/anima_cli_mk2.spec.yaml (289 → 638 LoC)
  - state/anima_cli_mk2_v0_2_refinement_2026_05_06/full_read_summary.json
  - state/anima_cli_mk2_v0_2_refinement_2026_05_06/v0_2_diff.md
related-specs:
  - hive/spec/mk2_apex.spec.yaml (1535 LoC, layer 4, mode mandatory)
  - hive/spec/mk2_ecosystem_catalog.spec.yaml (606 LoC, layer 4, mode advisory)
  - hive/spec/schema/spec_v1.schema.yaml
related-raws:
  - "raw#15 (additive only)"
  - "raw#91 (honest C3)"
  - "raw#92 (no_silent_errors)"
  - "raw#168 (minimum-viable carve-out)"
  - "raw#270, #271, #272, #273 (apex enforcement primitives)"
  - "own_17 (anima-no-external-substrate-wrapping ALM 영구 보류)"
---

# anima cli mk2 v0.2 refinement landed (2026-05-06)

<!-- [Hc_664 anima-cli-mk2-v0-2-apex-compliance-refinement — moved to hypotheses_candidates/Hc_664_anima_cli_mk2_v0_2_apex_compliance.md on 2026-05-11] -->

## TL;DR

**hive mk2_apex (1535 LoC, baseline 2026-05-02 + 7 amends) full read**:
- Section 1 inventory (12 components, 2026-05-05 snapshot)
- Section 2 stack_versions (10 components, version+status+canonical_module+alternatives+notes)
- Section 2.5 canonical_layout (singular core/module/doc + `<feature>/lint.<ext>` 4th sibling, 2026-05-05)
- Section 3 compatibility_matrix (3 COMPATIBLE + 3 INCOMPATIBLE)
- Section 4 per_repo_override (29 repos: anima=consumer, nexus=provider, hexa-lang=peer, hive=meta, 25 peer/archived)
- Section 5 migration_paths (3 completed + 6 in_progress + 3 deferred — BG-MK2-EN-ONLY 2026-05-20 신규)
- Section 5.5 hive_prefs (5 user-pref keys SSOT, ~/.hive/config.hive)
- Section 6 agent_directive (5-step workflow, 17 keyword, fresh_session_bootstrap single phase 2026-05-06)
- Section 6.5 status_enum (8 enum + retired_intentional pass_equivalence)
- Section 7 enforcement (mode=mandatory, 11 raw primitives, bypass=HIVE_SPEC_MK2_APEX_DISABLE=1)
- Section 8 consumers (7), Section 9 related_specs (5), Section 10 falsifiers (9 — 2 SPEC-STUB until 2026-05-12), Section 11 history (8 amend dates), raw10_caveats 13.

**anima cli mk2 v0.1 → v0.2 refinement** (additive only):

| Axis | v0.1 (289 LoC) | v0.2 (638 LoC) |
|------|----------------|----------------|
| Sections | 7 | 14 (+7 신규) |
| Falsifiers | 5 | 8 (+3 신규: F-anima_cli-6/7/8) |
| Honest C3 | 6 | 10 (+4 신규: C7/C8/C9/C10) |
| version | 1 | 2 |
| status | design | design_v0_2_refined |
| 기존 entry 변경 | — | 0건 (raw#15 additive 정합) |

## Section 8-14 신규 (요약)

| # | Section | apex 정합 mirror |
|---|---------|------------------|
| 8 | backend_stack_versions | apex § stack_versions (T1/T2/T3 backend 별 version+canonical_module+alternatives+rejected_alternatives) |
| 9 | backend_compatibility_matrix | apex § compatibility_matrix (3 COMPATIBLE + 3 INCOMPATIBLE — own 17 enforcement Llama/Mistral × T1 = INCOMPATIBLE) |
| 10 | hive_mk2_apex_compliance | 9 compliant_items + 10 gaps_remaining (G1-G10, severity + resolution_phase) |
| 11 | enforcement | apex § enforcement (mode=mandatory, 9 primitives, ramp 4 phases, bypass=ANIMA_CLI_MK2_DISABLE=1) |
| 12 | agent_directive | apex § agent_directive (4 consult_triggers + 5-step workflow + 8 keyword_match) |
| 13 | status_lifecycle | apex § status_enum (8 enum + pass_equivalence_for_coverage_gates) |
| 14 | hive_prefs_compliance | apex § hive_prefs (4 user-facing surfaces × lang.reply ko / reply_style friendly 정합) |

## Falsifier 3건 신규

- **F-anima_cli-6**: backend_canonical=anima-native invariant (own 17 ALM 영구 보류 enforcement) — Llama/Mistral 진입 시 hard_fail. SPEC-STUB until Phase 2 T1 backend wire BG.
- **F-anima_cli-7**: hive_mk2_apex_compliance.gaps_remaining 30d 무진전 → strengthen_or_retire (apex F-MK2-APEX-4 axis mirror).
- **F-anima_cli-8**: spec ↔ .roadmap.cli mk1 entries bidirectional drift → amend_spec_or_roadmap (apex F-MK2-APEX-3 axis mirror).

## Honest C3 4건 신규

- **C7**: hive mk2_apex consumer-only — anima cli mk2 spec은 apex inventory 미진입 (catalog component slot only, kick/check/atlas pattern mirror).
- **C8**: BR-MK2-AI-NATIVE-ENGLISH-ONLY (BG-MK2-EN-ONLY 2026-05-20 expected_completion) 정합 — 본 spec v0.1/v0.2 한국어 prose 잔존, mass conversion cycle 도착 시 변환.
- **C9**: F-MK2-APEX-3 perspective_mismatch axis 정합 — anima cli mk2 자체 perspective 필드 부재; .roadmap.cli mk1 header 의존.
- **C10**: own 17 ALM 영구 보류 enforcement = spec-level declarative만; runtime grep 검증 별도 lint tool (Phase 1.5).

## own 17 + hive mk2 cross-check

own 17 (anima-no-external-substrate-wrapping ALM 영구 보류, 2026-05-06)와 hive mk2_apex consumer 정합:
- **apex per_repo_override.anima.perspective=consumer** ↔ **anima cli mk2 T1.rejected_external_substrate** (Llama 3건) 정합
- **apex status_enum.retired_intentional** ↔ **anima cli mk2 Section 13 status_lifecycle.retired_intentional examples=[llama_path_a_v2_backend, mistral_g3_backend]** 정합 (external_blocker=own_17_directive)
- **apex F-MK2-APEX-2 INCOMPATIBLE pair actual use → hard_fail** ↔ **F-anima_cli-6 backend_canonical=anima-native invariant** 정합
- **apex enforcement.primitives raw#270/271/272/273** ↔ **anima cli mk2 Section 11 enforcement.primitives** 정합 (+ own_17 anima-specific)

## 다음 cycle 권고

1. **v0.3 spec yaml lint enforcement** — `tool/anima_cli_mk2_lint.hexa` + `tool/anima_cli_mk2_backend_lint.hexa` 작성 (F-anima_cli-1~8 8건 모두 observable 자동 검증).
2. **catalog mirror PR** — `hive/spec/mk2_ecosystem_catalog.spec.yaml component_20_anima_cli_mk2` entry 사용자 승인 후 hive 측 PR (apex inventory 미진입, catalog slot only, kick/check/atlas pattern).
3. **Phase 1 bin/anima refactor BG** — 본 spec read → 30-50 LoC dispatcher (F-anima_cli-1 통과).
4. **Phase 2 T1 backend wire BG** — `clm_v4_mount.hexa` load + own 17 strict enforce (F-anima_cli-6 activates) + clm-v2 KO 회복 verification.
5. **BG-MK2-EN-ONLY mass conversion** — 2026-05-20 도착 시 description / falsifier description / honest_c3 / open_questions Korean prose → English (identifier / handler path / canonical CLI 보존).
6. **own 17 cross-spec enforcement audit** — anima/spec/anima_cli_mk2.spec.yaml + .roadmap.cli + .roadmap.clm_native_chat + anima/.own own17 4 file 의 backend_directive verbatim 동기 (drift 방지).

## 출력 산출물

- `anima/spec/anima_cli_mk2.spec.yaml` (Edit, 289 → 638 LoC)
- `state/anima_cli_mk2_v0_2_refinement_2026_05_06/full_read_summary.json` (Write)
- `state/anima_cli_mk2_v0_2_refinement_2026_05_06/v0_2_diff.md` (Write)
- `docs/anima_cli_mk2_v0_2_refinement_landed_2026_05_06.ai.md` (this file, Write)

## 제약 정합

- $0 mac doc-only ✓ (compute spend 0)
- raw#9 hexa-only ✓ (yaml + md only, no .py)
- raw#10 honest C3 ≥5 ✓ (10 items: C1-C10)
- raw#15 additive ✓ (기존 entry 0건 변경, Section 1-7 + Falsifier 1-5 + Honest C1-C6 보존)
- own 17 ALM 영구 보류 ✓ (T1 backend section anima-native enforce 유지 + Section 9 INCOMPATIBLE matrix Llama/Mistral 명시 + F-anima_cli-6 hard_fail + Section 13 status_lifecycle.retired_intentional examples)
- commit X ✓ (commit 별도 사용자 승인 후)
