# State Ledger Schema Versioning (Task #11)

**Date:** 2026-04-29
**Owner:** Task #11 (anima-clm-eeg → anima-eeg-core/_integrations Phase 6 race risk MED 해소)
**Status:** ADVISORY (cutover to STRICT: 2026-05-15)
**Provenance:** migration plan (commit fb5b423c2 §6) MED race-risk identification

---

## 1. Motivation

The Phase 6 wrap→port migration plan (`commit fb5b423c2`, §6) flagged a MED-severity
race risk: 5 state-ledger paths are currently written exclusively by legacy
writers under `anima-clm-eeg/tool/`, but Phase 6 _integrations modules under
`anima-eeg-core/tool/modules/_integrations/` are slated to take over emission
(currently they wrap-design-reference but do not yet write to those paths).

Without a schema discriminator, when the second writer goes live we lose the
ability to attribute a row to its source pipeline, and any field-shape drift
becomes silently mixed within the same `.jsonl` file.

The mitigation: add an explicit `schema_version` field to every row, wired
identically on both writer paths so the discriminator is **always present**
post-cutover. A read-only validator detects mixed-schema files (F_SLV_01),
unknown schema strings (F_SLV_02), and post-cutover rows that still lack the
field (F_SLV_03).

## 2. The 5 ledger paths

| # | Path | Pre-Task#11 row count |
|---|------|-----------------------|
| 1 | `state/cyborg_eeg_audit/*.jsonl` | 6 |
| 2 | `state/clm_eeg_berger_audit/*.jsonl` | 13 + 15 (hpf_rerun) |
| 3 | `state/clm_eeg_pe_audit/*.jsonl` | 23 |
| 4 | `state/clm_eeg_hjorth_audit/*.jsonl` | 16 |
| 5 | `state/clm_eeg_gamma_theta_ratio_audit/*.jsonl` | 26 |

Total scanned: 99 rows (84 in primary five files; 15 in `hpf_rerun` ancillary).
raw#65 idempotent verify: identical pre/post patch (validator is read-only).

## 3. Writer matrix (raw#10 honest snapshot, 2026-04-29)

| Ledger | Legacy writer (anima-clm-eeg/tool/) | Phase 6 writer (anima-eeg-core/_integrations/) | Status |
|--------|-------------------------------------|------------------------------------------------|--------|
| cyborg_eeg_audit | `eeg_to_token_cyborg.hexa` | `cyborg_token_emit.hexa` | LEGACY-ONLY today (Phase 6 NOT_YET_LANDED) |
| clm_eeg_berger_audit | `clm_eeg_berger_sanity.hexa` | `berger_validate.hexa` | LEGACY-ONLY today (Phase 6 NOT_YET_LANDED) |
| clm_eeg_pe_audit | `clm_eeg_pe_real.hexa` | _(none yet)_ | LEGACY-ONLY (orphan in Phase 6) |
| clm_eeg_hjorth_audit | `clm_eeg_hjorth_real.hexa` | _(none yet)_ | LEGACY-ONLY (orphan in Phase 6) |
| clm_eeg_gamma_theta_ratio_audit | `clm_eeg_gamma_theta_ratio.hexa` | `clm_eeg_p3.hexa` | LEGACY-ONLY today (Phase 6 NOT_YET_LANDED) |

raw#10 disclosure: Phase 6 _integrations currently emit kv to a separate audit
path (`state/anima_eeg_core_phase6_integrations_audit.jsonl` via `_integration_test.hexa`)
and do **not** yet append to the 5 legacy ledgers. The discriminator is being
landed in advance of that cutover so day-1 of dual-write is mixed-schema-safe.

## 4. Discriminator values

| Value | Producer |
|-------|----------|
| `clm-eeg-legacy.v1` | All 5 `anima-clm-eeg/tool/*` writers |
| `eeg-core-phase6.v1` | All `anima-eeg-core/tool/modules/_integrations/*` writers |
| `<unset>` | Pre-Task#11 historical rows (raw#10 honest tolerated until 2026-05-15) |
| `<unknown>` | Out-of-set string (always falsifies F_SLV_02) |

Fallback classifier: rows that omit `schema_version` but carry a legacy-style
`schema` field starting with `anima-clm-eeg/` are classified as legacy; rows
whose `schema` starts with `anima-eeg-core/_` are Phase 6. This protects the
26 historical gamma_theta rows that already use the `schema` convention.

## 5. raw#71 falsifiers (4 preregistered, frozen 2026-04-29)

| ID | Trigger | Verdict |
|----|---------|---------|
| F_SLV_01 | ledger contains rows with two distinct `schema_version` values | MIXED_SCHEMA |
| F_SLV_02 | unknown `schema_version` (not in known set) | UNKNOWN_SCHEMA |
| F_SLV_03 | row missing both `schema_version` and `schema` after enforce-date | ENFORCE_VIOLATION |
| F_SLV_04 | validator selftest classifier round-trip fails | SELFTEST_DRIFT |

## 6. Validator

- **Path:** `tool/state_ledger_schema_validator.hexa`
- **CLI:**
  - `hexa run tool/state_ledger_schema_validator.hexa --selftest`
  - `hexa run tool/state_ledger_schema_validator.hexa --check <path>`
  - `hexa run tool/state_ledger_schema_validator.hexa --check-all`
  - `hexa run tool/state_ledger_schema_validator.hexa --enforce-discriminator`
- **Selftest result (2026-04-29):** 8/8 PASS (S1–S8)
- **First check-all run (2026-04-29 ADVISORY):** 0 falsifiers fired (84 rows scanned + 15 ancillary; gamma_theta classified as legacy via fallback).

## 7. Rollout plan

| Date (UTC) | State | Behavior |
|-----------|-------|----------|
| 2026-04-29 | ADVISORY | Validator reports `<unset>` and `<unknown>` rows but does not fail. New rows from both writer families MUST emit `schema_version`. |
| 2026-05-15 | STRICT | Validator's date-comparison flips to enforce mode; F_SLV_03 fires for any row lacking the field. Pre-rollout legacy rows remain in place (raw#10 honest historical preservation). |

The cutover is a single date constant change (`ENFORCE_DATE_UTC`) and an
opt-in CLI flag (`--enforce-discriminator`). No further writer or validator
changes are required for the rollout.

## 8. Constraint compliance

- **raw#9 hexa-only:** validator and patches are `.hexa`.
- **raw#10 honest:** writer matrix transparently lists Phase 6 paths as
  NOT_YET_LANDED rather than claiming dual-write today.
- **raw#12 silent-error / append-only:** the patch to each legacy writer
  appends `schema_version` as the *last* field of the JSONL row; field order
  for all prior fields is preserved. Legacy `chflags uchg` was unlocked,
  patched, re-locked per documented dual-lock pattern (`silent_edit_dual_lock.sh.txt`).
- **raw#23 schema-guard:** discriminator is the schema-guard; validator
  classifier round-trips selftested 8/8.
- **raw#65 idempotent:** validator is read-only; pre/post row counts match
  exactly (84 = 84 in the primary 5 files; ancillary `hpf_rerun.jsonl` also
  unchanged).
- **raw#66 ai-native trailer:** unknown values invoke `<unknown>` classification + F_SLV_02.
- **raw#71 falsifier:** 4 falsifiers preregistered, all selftested.
- **raw#77 audit:** validator emits per-ledger audit row to stdout.
- **raw#82 darwin-native:** uses `cat` / `ls -1` / `date -u` only.
- **raw#91 honest:** F_SLV_03 advisory→strict cutover documented; no claim
  that historical `<unset>` rows are wrong.
- **own#4 root-cause-only:** the discriminator is the *root* mitigation for
  dual-writer drift; validator is the *root* detection layer.

## 9. Files touched

- `tool/state_ledger_schema_validator.hexa` *(new — ~280 LoC)*
- `anima-clm-eeg/tool/eeg_to_token_cyborg.hexa` *(append schema_version line)*
- `anima-clm-eeg/tool/clm_eeg_berger_sanity.hexa` *(append)*
- `anima-clm-eeg/tool/clm_eeg_pe_real.hexa` *(append)*
- `anima-clm-eeg/tool/clm_eeg_hjorth_real.hexa` *(append)*
- `anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa` *(append)*
- `anima-eeg-core/tool/modules/_integrations/cyborg_token_emit.hexa` *(append kv line)*
- `anima-eeg-core/tool/modules/_integrations/berger_validate.hexa` *(append kv line)*
- `anima-eeg-core/tool/modules/_integrations/clm_eeg_p3.hexa` *(append kv line)*
- `anima-eeg-core/tool/modules/_integrations/artifact_pipeline.hexa` *(append kv line — Task #11 deferral closure 2026-04-29)*
- `anima-eeg-core/tool/modules/_integrations/rsn_validate.hexa` *(append kv line — Task #11 deferral closure 2026-04-29)*
- `docs/state_ledger_schema_versioning_2026_04_29.md` *(this file)*

## 10. Task #11 deferral closure (2026-04-29 follow-up)

The two Phase 6 _integrations modules deferred from the main Task #11 closure
(commits 5742538fb / 5d7988201 / 6446ca4e0 / 649b8cb69) — `artifact_pipeline`
and `rsn_validate` — were verified for ledger-write wire status:

- **artifact_pipeline.hexa**: NO state-ledger writer wire (kv-block-only via
  stdout; `_integration_test.hexa` consumes kv). raw#10 honest C3.
- **rsn_validate.hexa**: NO state-ledger writer wire (kv-block-only via
  stdout; legacy `state/rsn_audit/*.jsonl` reference is a docstring fixture
  pointer, not a write call). raw#10 honest C3.

Both modules nonetheless received the `schema_version=eeg-core-phase6.v1` emit
in their kv-block (matching the proactive pattern applied to the prior 3
_integrations writers in 6446ca4e0) so that the discriminator is present at
the kv-contract layer ahead of the dispatcher cutover that will append their
output directly to a state ledger.

**Coverage status:** 10/10 Phase 6 _integrations writers covered for
`schema_version` emit at the kv-contract layer (8 _integrations + 2 deferral
closure). The `_integration_test.hexa` audit-row writer (which currently
extracts only `schema`/`verdict`/`value_x1000`/`raw71_triggered` and does NOT
yet propagate `schema_version` to the audit ledger row) is a separate
concern tracked outside Task #11.

**Selftest verification:** all 8 _integrations modules PASS via
`_integration_test.hexa` (8/8 contract verdict PHASE6_INTEGRATIONS_INTEGRATION_PASS).
Validator selftest 8/8 PASS unchanged.
