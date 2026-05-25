---
date: 2026-05-04
package: hexa-brain
subsystem: core
status: LANDED
owner: hexa-brain repo
cycle: v1.1.0
ssot_artifact: tool/core/eeg_core.hexa + tool/module/{_paradigms,_metrics,_gates,_artifact,_integrations,_hw,_core,_prng}/
---

# core subsystem module manifest — v1.1.0 (2026-05-04)

## §1 Purpose

The **core** subsystem is the substrate-agnostic primitives layer: paradigms
(stimulus + response shapes), metrics (information-theoretic + spectral
brain-likeness signals), gates (composite verdict thresholders), artifact
detectors, integrations (clm_eeg p1/p2/p3, RSN/Berger validators), hardware
abstractions (substrate-agnostic recorder/headplot/impedance/adjustment), core
utilities (npy loader, filter pipeline, falsifier runner, jsonl audit ledger,
chflags lock, eeg export), and PRNG primitives.

Where the eeg subsystem talks to specific hardware, the core subsystem
operates on **already-captured artifacts** and provides the pure-hexa
substrate that paradigm + gate + metric + artifact + integration modules are
layered on. It was migrated from the parent monorepo at `anima/anima-eeg-core/`
via subtree split in v1.1.0 (commit `c8860844`), preserving 44 commits of
history.

## §2 File inventory

68 hexa files total / 1.3 MB on-disk. Top-level entry + 8 module subdirectories
under `tool/module/`.

### §2.1 Top-level entry (1 file)

| File | Purpose |
|---|---|
| `tool/core/eeg_core.hexa` | Top-level core subsystem entry; default `hexa-brain core` invocation |

### §2.2 `tool/module/_paradigms/` (5 files)

Stimulus + response paradigms substrate-agnostic of capture device:

| File | Purpose |
|---|---|
| `daily_life.hexa` | Daily-life free-running paradigm |
| `resting_baseline.hexa` | Eyes-open/closed resting baseline |
| `visual_p300.hexa` | Visual oddball P300 evoked-potential paradigm |
| `auditory_p300.hexa` | Auditory oddball P300 paradigm |
| `_integration_test.hexa` | Cross-paradigm integration test |

### §2.3 `tool/module/_metrics/` (20 files)

Pure-hexa metric primitives (no Python deps):

- **Information-theoretic native**: `lz76_native.hexa`, `lz76.hexa`,
  `lz76_chunked.hexa`, `pe_native.hexa`, `permutation_entropy.hexa`,
  `phi_proxy_native.hexa`, `spectral_entropy.hexa`.
- **Hjorth native**: `hjorth_native.hexa`, `hjorth.hexa`.
- **Band power**: `band_power_5.hexa`, `gamma_theta.hexa`, `gamma_theta_native.hexa`.
- **Coherence + phase**: `alpha_coherence.hexa`, `alpha_phase_plv.hexa`,
  `plv_preserving.hexa`, `dmn_coherence.hexa`.
- **Asymmetry + change**: `frontal_asymmetry.hexa`, `change_points.hexa`.
- **Test + entry**: `_integration_test.hexa`, `README.ai.md`.

### §2.4 `tool/module/_gates/` (5 files)

Composite verdict thresholders that combine metric signals:

| File | Purpose |
|---|---|
| `composite_gate.hexa` | Multi-metric composite verdict |
| `hjorth_band.hexa` | Hjorth complexity in normal-brain band |
| `rms_band.hexa` | RMS amplitude in expected band |
| `pe_saturation.hexa` | Permutation entropy saturation gate |
| `berger_alpha.hexa` | Berger alpha eyes-open/closed gate |

### §2.5 `tool/module/_artifact/` (11 files)

Detectors for non-brain signal contamination:

- `emg_muscle_detector.hexa`, `electrode_aging_classifier.hexa`,
  `reference_drift_detector.hexa`, `rail_flat_detector.hexa`,
  `ai_cleaning_pipeline.hexa`, `ecg_heart_artifact_detector.hexa`,
  `eye_blink_detector.hexa`, `motion_artifact_detector.hexa`,
  `environmental_emi_classifier.hexa`, `hpf_dc_drift.hexa`,
  `artifact_meta_classifier.hexa`.

### §2.6 `tool/module/_integrations/` (9 files + integration test)

Cross-track consumers + producers:

| File | Purpose |
|---|---|
| `clm_eeg_p1.hexa` | CLM-EEG phase 1 (LZ pre-register) consumer |
| `clm_eeg_p2.hexa` | CLM-EEG phase 2 (TLR pre-register) consumer |
| `clm_eeg_p3.hexa` | CLM-EEG phase 3 (GCG pre-register) consumer |
| `rsn_validate.hexa` | Resting-state network validator |
| `berger_validate.hexa` | Berger alpha validator |
| `multi_subject_aggregate.hexa` | Multi-subject aggregator |
| `synthetic_fixture.hexa` | Synthetic fixture emitter |
| `cyborg_token_emit.hexa` | Cyborg-mode token emitter (LM coupling) |
| `artifact_pipeline.hexa` | Artifact-detection pipeline orchestrator |
| `_integration_test.hexa` | Cross-integration test |

### §2.7 `tool/module/_hw/` (6 files + integration test)

Substrate-agnostic hardware abstractions:

| File | Purpose |
|---|---|
| `recorder.hexa` | Substrate-agnostic recorder |
| `headplot.hexa` | Substrate-agnostic headplot |
| `board_health.hexa` | Generalized board health |
| `impedance.hexa` | Generalized impedance |
| `adjustment.hexa` | Generalized adjustment |
| `_integration_test.hexa` | HW integration test |

### §2.8 `tool/module/_core/` (9 files + integration test)

Core utilities (the substrate that paradigm + gate + metric + artifact +
integration modules are layered on):

| File | Purpose |
|---|---|
| `npy_loader.hexa` | NPY file loader |
| `filter_pipeline.hexa` | Notch + bandpass filter pipeline |
| `falsifier_runner.hexa` | Run a falsifier spec against bound data |
| `jsonl_audit.hexa` | Append-only JSONL audit ledger |
| `chflags_lock.hexa` | macOS chflags-uchg immutability locker |
| `eeg_export.hexa` | EEG export (npy / jsonl) |
| `pipeline_suggester.hexa` | Recommend filter + gate chain |
| `_adapter.hexa` | venv-eeg / BrainFlow adapter |
| `_integration_test.hexa` | Core utilities integration test |

### §2.9 `tool/module/_prng/` (2 files)

Pure-hexa PRNG primitives for deterministic seeding:

| File | Purpose |
|---|---|
| `pcg32_native.hexa` | PCG32 generator |
| `splitmix64_native.hexa` | SplitMix64 generator |

### §2.10 `docs/core/` and `design/core/`

| File | Purpose |
|---|---|
| `docs/core/phase1_deprecate_byte_identical_audit_2026_05_01.md` | Phase 1 audit |
| `docs/core/phase3_metrics_v1_2026_04_28.md` | Phase 3 metrics v1 design |
| `docs/core/phase3_metrics_batch2_2026_04_29.md` | Phase 3 metrics batch 2 |
| `docs/core/phase3_metrics_batch3_2026_04_29.md` | Phase 3 metrics batch 3 |
| `docs/core/phase4_paradigms_batch1_2026_04_29.md` | Phase 4 paradigms batch 1 |
| `docs/core/phase5_hw_v1_2026_04_29.md` | Phase 5 HW v1 |
| `docs/core/phase5_port_spec_2026_05_01.md` | Phase 5 port spec |
| `design/core/eeg_artifact_ai_cover_paradigm_2026_04_28.md` | Artifact AI cover paradigm design |

## §3 Public API surface

Verbs (via `bin/hexa-brain core <verb>` dispatcher):

| Verb | Backing file | Description |
|---|---|---|
| `core core` (default) | `tool/core/eeg_core.hexa` | Top-level core entry |
| `core paradigm-resting` | `_paradigms/resting_baseline.hexa` | Resting baseline paradigm |
| `core paradigm-daily-life` | `_paradigms/daily_life.hexa` | Daily-life paradigm |
| `core paradigm-p300-visual` | `_paradigms/visual_p300.hexa` | Visual P300 paradigm |
| `core paradigm-p300-auditory` | `_paradigms/auditory_p300.hexa` | Auditory P300 paradigm |
| `core paradigm-integration-test` | `_paradigms/_integration_test.hexa` | Paradigm integration test |
| `core export` (alias `eeg-export`) | `_core/eeg_export.hexa` | EEG export (npy / jsonl) |
| `core jsonl-audit` | `_core/jsonl_audit.hexa` | JSONL audit ledger |
| `core adapter` | `_core/_adapter.hexa` | venv-eeg adapter |
| `core filter-pipeline` | `_core/filter_pipeline.hexa` | Filter pipeline |
| `core pipeline-suggester` | `_core/pipeline_suggester.hexa` | Pipeline suggester |
| `core falsifier-runner` | `_core/falsifier_runner.hexa` | Falsifier runner |
| `core chflags-lock` | `_core/chflags_lock.hexa` | chflags immutable lock |
| `core npy-loader` | `_core/npy_loader.hexa` | NPY loader |

Direct invocation supported for any of the 68 files via
`hexa run tool/core/...`. The dispatcher does **not** currently expose verbs
for `_metrics/`, `_gates/`, `_artifact/`, `_integrations/`, `_hw/`, or
`_prng/` modules — those are accessed by importing into other paradigms or by
direct `hexa run`. Adding verbs for the remaining 49 modules is a v1.2+ task.

## §4 Dependencies

- **hexa-lang runtime** for all `.hexa` files (mostly pure-hexa).
- **`.venv-eeg/` Python adapter** for `_core/_adapter.hexa` only — wraps
  `/tmp/anima_eeg_core_phase1_integration/`.
- **No NumPy / SciPy / matplotlib** — pure-hexa metrics are the stated
  direction; `_metrics/*_native.hexa` files implement LZ76, permutation
  entropy, Hjorth, phi proxy, gamma/theta natively.
- **Recordings consumer**: `eeg/recordings/sessions/*.npy` produced by the eeg
  subsystem. No back-pressure on the eeg subsystem; core operates strictly
  read-only on captured artifacts.

## §5 Sibling subsystems

- **eeg** subsystem (`eeg_subsystem_module_manifest_2026_05_04.ai.md`) —
  produces the `.npy` session artifacts that core consumes.
- **cli** subsystem (`cli_dispatch_design_2026_05_04.ai.md`) — exposes 14
  core verbs via `hexa-brain core <verb>`.

## §6 Future evolution

- **v1.2**: extend dispatcher to expose `_metrics/`, `_gates/`,
  `_artifact/` modules as verbs (currently dispatcher only routes 14 of 68
  files; the rest require direct `hexa run`).
- **v1.3+**: consolidate `eeg/core/quality_audit + quality_ledger` into the
  top-level `core/` namespace to remove the eeg/core vs core name collision
  (see eeg manifest C3 #6).
- **v1.x**: pure-hexa adapter (`_core/_adapter.hexa`) BrainFlow Python
  removal or formal `.own N` registration of the carve-out.
- **v2 substrate change** (intracranial): add high-bandwidth recorder + spike
  sorting under `_hw/` since these are substrate-agnostic primitives that
  belong here.


1. **Core subsystem maturity asymmetry**: eeg/ has 7 production cycles of
   real-hardware evidence; core/ paradigms + metrics are mostly
   spec/synthetic-fixture tested, with selected real-data integration via
   `_integrations/clm_eeg_p[1-3]` consumers in anima. Treat core/ as
   research-stage rather than production-ready.
2. **Cross-subsystem integration not stabilized**: `tool/module/_hw/`
   has overlapping concerns with `eeg/`'s hardware drivers (e.g.
   `_hw/board_health.hexa` vs `eeg/board_health_check.hexa`). Consolidation
   is deferred; no formal interface contract between eeg/ and core/ yet.
3. **44-commit subtree-split history paths stale**: history is from
   `anima-eeg-core/` subtree split, so commit messages reference
   `anima-eeg-core/`-rooted paths that no longer exist (now under `core/`).
   No functional break; rebase intentionally avoided to preserve attribution.
4. **CLI dispatcher exposes 14 of 68 files**: the remaining 49 modules
   (`_metrics/*`, `_gates/*`, `_artifact/*`, `_integrations/*`, `_hw/*`,
   `_prng/*`) are not directly invocable as `hexa-brain core <verb>`. Users
   who need them must use `hexa run tool/module/<dir>/<file>.hexa`. v1.2+
   will close this gap.
5. **eeg/core/ vs core/ name collision**: as noted in the eeg manifest C3 #6,
   `eeg/core/quality_audit.hexa` and `tool/core/eeg_core.hexa` share the
   "core" name but serve different layers. Documentation must always be
   explicit about which one is meant.
6. **`_integration_test.hexa` modules are mostly synthetic-fixture only**:
   real-hardware integration tests live in `eeg/` but gate only the v1
   substrate. v2-v5 substrates have no test scaffolding yet — adding
   intracranial / Neuropixels / closed-loop BMI integration tests would
   require hardware acquisition first.

## §8 Composability

- **Upstream**: eeg subsystem (consumes its `.npy` outputs); hexa-lang
  runtime; `.venv-eeg/` Python (only for the `_adapter.hexa` carve-out).
- **Downstream**:
  - anima's consciousness research pipeline (consumes
    `_integrations/clm_eeg_p[1-3]` outputs + paradigm verdicts).
  - Future hexa-brain v1.x cycles that build on top of paradigms + metrics
    (e.g. cross-paradigm aggregators, real-time metric streamers).
  - Other hexa-lang ecosystem packages that want substrate-agnostic neural
    primitives (none confirmed yet beyond anima).
