---
schema: anima-eeg-core/_integrations/ai-native/1
last_updated: 2026-05-02
ssot:
  integration_test: anima-eeg-core/tool/modules/_integrations/_integration_test.hexa
  synthetic_fixture: anima-eeg-core/tool/modules/_integrations/synthetic_fixture.hexa
status: live — Phase 6 cross-cutting integrations; 9 modules + 1 integration test; selftest LCG byte-identical
roadmap_entry: 270
raws:
---

# anima-eeg-core integrations modules (AI-native)

Phase 6 cross-cutting integrations — bridges between EEG core and adjacent subsystems (CLM-EEG P1/P2/P3, Berger validation, RSN validation, cyborg token emit, multi-subject aggregation, artifact pipeline composition). Plus the synthetic fixture that anchors regression baselines.

## TL;DR for an agent reading this cold

- **10 files**: 1 integration test + 1 synthetic fixture + 8 integration modules.
- 3 CLM-EEG bridges: `clm_eeg_p1` / `clm_eeg_p2` / `clm_eeg_p3` (Phase 1/2/3 integrations).
- `cyborg_token_emit.hexa` (266 LOC) — emits cyborg-EEG tokens to `state/cyborg_eeg_audit/*.jsonl`.
- `multi_subject_aggregate.hexa` (330 LOC) — N-subject pooled metric aggregation.

## Architecture map

```
anima-eeg-core/tool/modules/_integrations/
├── _integration_test.hexa        Phase 6 batch runner — synthetic_fixture FIRST
├── synthetic_fixture.hexa        deterministic LCG regression baseline (551 LOC)
│
├── clm_eeg_p1.hexa               CLM-EEG Phase 1 bridge (290 LOC)
├── clm_eeg_p2.hexa               CLM-EEG Phase 2 bridge (435 LOC)
├── clm_eeg_p3.hexa               CLM-EEG Phase 3 bridge (300 LOC)
│
├── berger_validate.hexa          Berger 1929 α-rhythm cross-validation (252 LOC)
├── rsn_validate.hexa             Resting State Network validation (249 LOC)
├── artifact_pipeline.hexa        composes _artifact/* into a chain (258 LOC)
├── cyborg_token_emit.hexa        cyborg-EEG token audit emit (266 LOC)
└── multi_subject_aggregate.hexa  N-subject pooled aggregation (330 LOC)
```

## API contract

```hexa
// synthetic_fixture.hexa — REGRESSION BASELINE (run first)
fn generate_fixture(seed: int, n_samples: int) -> [[float]]
// Returns deterministic LCG output. Drift in returned value → CRITICAL.
fn fixture_sha256() -> string  // pinned baseline sha

// Per-integration module:
fn run_<integration>(input: string, args: <ArgStruct>) -> IntegrationResult
// IntegrationResult { passed: bool, metrics: {...}, audit_row: AuditRow }

// _integration_test.hexa runs all 8 integrations in selftest mode + verifies kv-blocks
```

Output kv-blocks (consumed by integration test):

```
__INTEGRATION_SYNTHETIC_FIXTURE__   PASS schema=... sha256=...
__INTEGRATION_CLM_EEG_P1__          PASS schema=... metric=...
__INTEGRATION_CLM_EEG_P2__          PASS schema=... metric=...
...
```

Audit ledgers:
- `state/clm_eeg_*_audit/*.jsonl`
- `state/cyborg_eeg_audit/*.jsonl`
- `state/anima_eeg_core_phase4_paradigms_integration_audit.jsonl` (cross-Phase)

## Invocation patterns

```bash
# Phase 6 batch (8 integrations + fixture baseline)
hexa run anima-eeg-core/tool/modules/_integrations/_integration_test.hexa

# Single integration
hexa run anima-eeg-core/tool/modules/_integrations/clm_eeg_p3.hexa --selftest

# Multi-subject aggregation
hexa run anima-eeg-core/tool/modules/_integrations/multi_subject_aggregate.hexa \
  --subjects "S01,S02,S03" --metric berger_alpha
```

## Failure cascade

```
synthetic_fixture.fail (sha drift)
  → CRITICAL: regression baseline broken
       → ALL downstream integrations have undefined ground truth
            → integration_test exits 1 immediately, batch invalid
```

```
clm_eeg_p2.fail (PSI ⊥ MI ⊥ TE handler missing)
  → P3 sees null upstream metric → P3 also fails
       → cyborg_token_emit captures cascade in audit row
```


1. **synthetic_fixture sha-pinning is critical.** Any change to LCG seed / sample count / float repr → all downstream selftests must be re-pinned. Don't refactor the fixture without a coordinated re-pin.
2. **Live mode NOT_YET_LANDED.** `bin/eeg integration <name> --live` deferred until D+1 hardware arrival or .venv-eeg backend resolution.
4. **Cyborg token emit append-only.** No deduplication — re-runs append duplicate rows. Use timestamp + run_id for idempotent consumers.
5. **multi_subject_aggregate assumes equal n_samples per subject.** Unequal lengths use shortest (zero-padding NOT applied).
6. **Berger validate hardcodes O1↔O2 channel pair.** R33 frozen literature-based (Berger 1929 + Schartner 2017). Other pairs need explicit override + falsifier re-spec.
7. **RSN validate** assumes 8-channel minimum montage. Cyton 8ch OK; Cyton-only-4ch will fail RSN spatial decomposition.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `_integration_test.hexa` | `861819d303072dd01cacda5db188c7764a4f41a56ea5ef83258f84f131aeb0f8` | 189 |
| `synthetic_fixture.hexa` | `090d97dd5154bccca050ca49c082975778bcf00f0f6730fcd305f358203f6834` | 551 |
| `artifact_pipeline.hexa` | `e0d4c0fc1f42b56f3c232df577f3b6881c3aa279d2e1f25a6d248528433bec0d` | 258 |
| `berger_validate.hexa` | `10254e2456746a31962acfc87e7ddd1aacea8aa3edd217930bbf2909b5abdb68` | 252 |
| `clm_eeg_p1.hexa` | `77f243322895671a0584c7fca0cfe0887342e4cf9e763d65858a2ffbe630ac12` | 290 |
| `clm_eeg_p2.hexa` | `4a87e47d2cdb85a139078c539bb3702977d300d7d8c32f87ca5dc03fb5d1b05b` | 435 |
| `clm_eeg_p3.hexa` | `7b90e1f91f3f0a1841a9187f98d9b76b384964dfe13e2958ed5528f2ab5223d4` | 300 |
| `cyborg_token_emit.hexa` | `446ca5667aa41b53ad5679dabce9f1801b999e106feaf36046da28a59e367e5b` | 266 |
| `multi_subject_aggregate.hexa` | `b68bc2ebd89063116e2987537929c23a5561e54b4e415f6b80391ada66b90a0b` | 330 |
| `rsn_validate.hexa` | `380f33f896d1646a168afc4c0411ff60fe26958d5a362312380ceea6c18a91a2` | 249 |

shas pinned 2026-05-02.
