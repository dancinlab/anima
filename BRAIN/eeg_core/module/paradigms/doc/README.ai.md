---
schema: anima-eeg-core/_paradigms/ai-native/1
last_updated: 2026-05-02
ssot:
  integration_test: anima-eeg-core/tool/modules/_paradigms/_integration_test.hexa
  paradigm_root:    anima-eeg-core/tool/modules/_paradigms/
roadmap_entry: 270
raws:
---

# anima-eeg-core paradigm modules (AI-native)

Phase-4 paradigm runners — 4 EEG experimental paradigms (resting baseline / daily life / visual P300 / auditory P300) with synthetic-fixture selftest mode and live-data driver hooks.

## TL;DR for an agent reading this cold

- **5 files**: 4 paradigms + 1 integration test.
- **Live mode** runs on the host via `bin/eeg paradigm <name> --live` (NOT_YET_LANDED until Phase 5).
- Each paradigm emits a kv-block contract (`__PARADIGM_<NAME>__ PASS|FAIL ...`) consumable by the integration test.

## Architecture map

```
anima-eeg-core/tool/modules/_paradigms/
├── _integration_test.hexa     batch-1 integration runner — calls all 4 paradigms in selftest
├── resting_baseline.hexa      eyes-open / eyes-closed resting baseline (Berger α dominant)
├── daily_life.hexa            unstructured daily-life schedule (1+ hour)
├── visual_p300.hexa           visual oddball P300 (target/non-target)
└── auditory_p300.hexa         auditory oddball P300 (1k Hz / 2k Hz tones)
```

## API contract

```hexa
// Per paradigm:
let SCHEMA = "anima-eeg-core/_paradigms/<name>/1"
fn run_selftest() -> (ok: bool, summary: string)
fn run_live(args: ParadigmArgs) -> EegSession      // NOT_YET_LANDED until Phase 5

// Output kv-block (consumed by integration test):
//   __PARADIGM_RESTING_BASELINE__ PASS schema=... epochs=N artifacts=... gates_passed=...
//   __PARADIGM_VISUAL_P300__ PASS schema=... target_count=... non_target_count=...
```

Integration test entry:

```bash
hexa run anima-eeg-core/tool/modules/_paradigms/_integration_test.hexa
hexa run anima-eeg-core/tool/modules/_paradigms/_integration_test.hexa --selftest    # alias
```

## Invocation patterns

```bash
# Selftest single paradigm
hexa run anima-eeg-core/tool/modules/_paradigms/visual_p300.hexa --selftest

# Live (Phase 5)
bin/eeg paradigm visual_p300 --live --duration 600

# Batch integration (verifies all 4 contracts)
hexa run anima-eeg-core/tool/modules/_paradigms/_integration_test.hexa
```

## Failure modes

- **Selftest fail** = synthetic fixture drifted OR module schema mismatch. Re-pin fixture sha and verify upstream.


1. **Live mode NOT_YET_LANDED.** `--live` paths are stubbed; Phase 5 hardware arrival required (D+1 on roadmap).
2. **Synthetic fixtures are LCG.** Selftest fixtures use deterministic LCG seed — byte-identical 2-run guaranteed but lacks real EEG noise structure.
3. **P300 paradigms assume monitor refresh rate 60 Hz.** Visual P300 timing accurate to ±16 ms; not validated on 120 Hz / variable refresh displays.
4. **Auditory P300 uses afplay backend on Mac.** Phase 5 host-side switch to PortAudio / Pyglet for cross-platform parity.
5. **`daily_life.hexa` is ≥1 hour run.** Bench cost on selftest is moderate (~10s synthetic fixture); live cost is participant-time-bound.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `_integration_test.hexa` | `3b8edadbbcffaae2cfe9574a11288eab8bc6fa52b89ef024955020ca6bc16915` | 171 |
| `auditory_p300.hexa` | `5485c923ba43f6b3850b2c113cf35c27f72773522f2786fdadb08a45a553cc17` | 340 |
| `daily_life.hexa` | `359417f36487165bd50ae415c604712e6a7122d42c19cfbba9d48aa052fc1ee3` | 212 |
| `resting_baseline.hexa` | `afc58f80a7344e3dbc9cc9dfb308647bb4e91c2623fb1f740609054382aef736` | 220 |
| `visual_p300.hexa` | `0e01c56dc9cadb63b2da55d5aaac411ed9e707a2beefe3eec09c4fdaea77c486` | 308 |

shas pinned 2026-05-02.
