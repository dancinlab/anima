---
schema: anima/state/anima_cli_mk2_v0_2_refinement/diff/v1
last_updated: 2026-05-06
ssot: anima/spec/anima_cli_mk2.spec.yaml
cycle: anima_cli_mk2_v0_2_refinement_2026_05_06
---

# anima cli mk2 v0.1 → v0.2 refinement diff

## Scope

- v0.1 base: anima/spec/anima_cli_mk2.spec.yaml (289 LoC, 7 sections, 5 falsifiers, 6 honest_c3)
- v0.2 target: 7 → 14 sections (additive), 5 → 8 falsifiers (additive), 6 → 10 honest_c3 (additive)
- raw#15 additive only — 기존 모든 entry 보존, 신규 section/falsifier/honest_c3 append

## Added (v0.2 신규)

### Sections 7개 추가

| # | New section | Source / rationale |
|---|-------------|--------------------|
| 8 | `backend_stack_versions` | apex § stack_versions 양식 mirror (version+status+canonical_module+alternatives+notes) |
| 9 | `backend_compatibility_matrix` | apex § compatibility_matrix mirror (CLM v4 × T1 = COMPATIBLE / Llama × T1 = INCOMPATIBLE per own 17) |
| 10 | `hive_mk2_apex_compliance` | compliant_items 9 + gaps_remaining 10 catalog |
| 11 | `enforcement` | apex § enforcement mirror (mode + raw primitives + bypass env) |
| 12 | `agent_directive` | apex § agent_directive mirror (consult_triggers + workflow + keyword_match) |
| 13 | `status_lifecycle` | apex § status_enum 8 enum mirror (active/draft/unmet/met/partial/closed/archived/retired_intentional) |
| 14 | `hive_prefs_compliance` | apex § hive_prefs declaration (lang.reply ko / lang.code en in user-facing surface) |

### Falsifiers 3개 추가

| ID | Description | action_on_fail |
|----|-------------|----------------|
| F-anima_cli-6 | backend_canonical=anima-native invariant (own 17 enforcement) — Llama/Mistral가 backend slot 진입 시 | hard_fail |
| F-anima_cli-7 | gaps_remaining 30d 무진전 (apex F-MK2-APEX-4 axis mirror) | strengthen_or_retire |
| F-anima_cli-8 | spec ↔ .roadmap.cli mk1 entries bidirectional drift | amend_or_retract |

### Honest C3 4개 추가

| ID | Caveat |
|----|--------|
| C7 | hive mk2_apex consumer-only — anima cli mk2는 apex inventory 미진입 (catalog slot only, kick/check/atlas pattern mirror) |
| C8 | BR-MK2-AI-NATIVE-ENGLISH-ONLY migration (2026-05-20) 정합 — v0.1/v0.2 한국어 prose 잔존, mass conversion cycle 도착 시 변환 |
| C9 | F-MK2-APEX-3 perspective_mismatch axis — anima cli mk2 자체 perspective 필드 부재; apex per_repo_override.anima.perspective=consumer cross-check는 .roadmap.cli header 의존 |
| C10 | own 17 enforcement는 spec-level declarative만 — runtime grep 검증은 별도 lint tool (tool/anima_cli_mk2_backend_lint.hexa) phase 1.5 필요. F-anima_cli-6은 현재 SPEC-STUB |

## Changed (v0.1 → v0.2 modify)

| Field | v0.1 | v0.2 |
|-------|------|------|
| `version` | `1` | `2` (additive amend, schema unchanged) |
| `status` | `design` | `design_v0_2_refined` (still pre-baseline) |
| `description` | unchanged content | append "v0.2 refinement: hive mk2_apex 정합 ↑ (Section 8-14 신규, F-anima_cli-6/7/8 신규, C7-C10 신규)" |

## Removed (v0.1 → v0.2 retract)

- 없음 (raw#15 additive only)

## Compliance trajectory

| Axis | v0.1 | v0.2 |
|------|------|------|
| apex stack_versions mirror | 부분 (backend_canonical 1줄) | 전체 (Section 8 신규) |
| apex compatibility_matrix mirror | 부재 | 전체 (Section 9 신규, 3 COMPATIBLE + 1 INCOMPATIBLE) |
| apex enforcement.primitives | raw#15 only | 11 raw primitive (apex parity) |
| apex agent_directive | 부재 | 전체 (Section 12 신규) |
| apex status_enum | status: design 1값 | 8 enum (Section 13 신규) |
| apex hive_prefs declaration | 부재 | declarative (Section 14 신규) |
| own 17 ALM 영구 보류 enforcement | T1 backend_directive prose | T1 backend_directive + F-anima_cli-6 falsifier (SPEC-STUB → activates Phase 2) |
| BR-MK2-AI-NATIVE-ENGLISH-ONLY | 미선언 | C8 명시 (mass conversion 2026-05-20+) |

## Out_of_scope (v0.2 미진입, v0.3+ 후속 cycle)

- spec yaml lint enforcement tool (tool/anima_cli_mk2_lint.hexa) — F-anima_cli-1~8 observable 자동 검증 별도 cycle
- catalog mirror (hive/spec/mk2_ecosystem_catalog.spec.yaml component_20 신규 entry) — hive 측 PR 별도, 사용자 승인 후
- BR-MK2-AI-NATIVE-ENGLISH-ONLY mass conversion (Korean prose → English) — BG-MK2-EN-ONLY 2026-05-20 expected_completion
- bin/anima refactor (352 → 30-50 LoC) — Phase 1 별도 BG
- T1 backend wire (clm_v4_mount.hexa load) — Phase 2 별도 BG
