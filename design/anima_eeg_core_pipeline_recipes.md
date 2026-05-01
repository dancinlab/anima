// anima-eeg-core pipeline recipes
// 2026-04-28 · raw#9 hexa-only · companion to anima_eeg_core_architecture_2026_04_28.md
// + anima_eeg_core_module_api.md

# anima-eeg-core — standard pipeline recipes

A "recipe" is a named, reproducible sequence of gates + metrics + (optional)
integrations applied to a single .npy or live recording. Recipes are
declared in `_core/recipes.hexa` so users can compose pipelines without
writing new dispatch logic.

## Recipe schema

```
type Recipe = {
    name: string,
    description: string,
    inputs: list[string],            # required input kinds (.npy, fs_hz, ...)
    steps: list[Step],
    outputs: list[string],           # produced JSONL audits + JSON certs
    failure_policy: string,          # "fail_fast" | "continue_on_partial" | "all_must_pass"
    raw_compliance: list[int]        # [9, 10, 12, 65, 71, 77, 82, 91, 101, 106]
}

type Step = {
    kind: string,                    # "gate" | "metric" | "integration" | "ml"
    module: string,                  # e.g. "berger_alpha"
    inputs: list[string],            # passed through to module
    pass_required: bool,             # if true, recipe halts on FAIL
    on_partial: string               # "halt" | "continue" | "downgrade_to_fail"
}
```

## Recipe 1 — `standard` (4-step minimum verifier)

The smallest defensible pipeline. Mirrors the original Tier-A bundle
(berger + lz76 + pe + hjorth) used pre-migration.

```
recipe "standard" {
  description: "Berger gate → LZ76 → PE → Hjorth on 60s+ resting EEG"
  inputs: [".npy 16ch", "fs=125Hz"]
  steps: [
    { kind: "gate",   module: "berger_alpha",       pass_required: true  },
    { kind: "metric", module: "lz76",               pass_required: true  },
    { kind: "metric", module: "permutation_entropy",pass_required: true  },
    { kind: "metric", module: "hjorth",             pass_required: true  },
  ]
  outputs: [
    "state/standard_pipeline_audit/<date>_standard.jsonl",
    "state/standard_pipeline_cert/<ts>_standard.json",
  ]
  failure_policy: "fail_fast"
  raw_compliance: [9, 10, 12, 65, 71, 77, 82, 91]
}
```

**Invocation:**
```bash
hexa run anima-eeg-core/eeg_core.hexa pipeline standard \
  --input recordings/sessions/resting_<ts>_seg00.npy
```

**Verdict matrix:**
| Berger | LZ76 | PE | Hjorth | Pipeline verdict |
|--------|------|----|----|------------------|
| FAIL | — | — | — | `STANDARD_FAIL_GATE_BERGER` |
| PASS | FAIL | — | — | `STANDARD_FAIL_LZ76` |
| PASS | PASS | FAIL | — | `STANDARD_FAIL_PE` |
| PASS | PASS | PASS | FAIL | `STANDARD_FAIL_HJORTH` |
| PASS | PASS | PARTIAL | PASS | `STANDARD_PARTIAL` |
| PASS | PASS | PASS | PASS | `STANDARD_PASS` |

## Recipe 2 — `resting_full`

Standard + 4 network metrics. Used when the session was a deliberate
eyes-closed/eyes-open resting block.

```
recipe "resting_full" {
  description: "Standard pipeline + DMN coherence + frontal asymmetry + alpha coh + spectral entropy"
  inputs: [".npy 16ch", "fs=125Hz"]
  steps: [
    { kind: "gate",   module: "berger_alpha",        pass_required: true  },
    { kind: "gate",   module: "rms_band",            pass_required: true  },
    { kind: "metric", module: "lz76",                pass_required: true  },
    { kind: "metric", module: "permutation_entropy", pass_required: true  },
    { kind: "metric", module: "hjorth",              pass_required: false, on_partial: "continue" },
    { kind: "metric", module: "gamma_theta",         pass_required: false, on_partial: "continue" },
    { kind: "metric", module: "dmn_coherence",       pass_required: false, on_partial: "continue" },
    { kind: "metric", module: "frontal_asymmetry",   pass_required: false, on_partial: "continue" },
    { kind: "metric", module: "alpha_coherence",     pass_required: false, on_partial: "continue" },
    { kind: "metric", module: "spectral_entropy",    pass_required: false, on_partial: "continue" },
  ]
  outputs: [
    "state/resting_full_audit/<date>_resting.jsonl",
    "state/resting_full_cert/<ts>_resting.json",
  ]
  failure_policy: "continue_on_partial"
  raw_compliance: [9, 10, 12, 65, 71, 77, 82, 91, 106]
}
```

## Recipe 3 — `feedback_loop` (live, non-batch)

For the engagement / drowsiness daemon (B8). Composes a sliding window
metric stream with macOS native notification side-effect.

```
recipe "feedback_loop" {
  description: "30s sliding window engagement + drowsy notify"
  inputs: ["live BrainFlow stream", "fs=125Hz"]
  steps: [
    { kind: "gate",   module: "rms_band",                         pass_required: true  },
    { kind: "metric", module: "engagement_pope_1995",             pass_required: true  },
    { kind: "metric", module: "drowsy_pollock_1990",              pass_required: true  },
    { kind: "integration", module: "macos_notification_emitter",  pass_required: false },
  ]
  outputs: [
    "state/eeg_feedback_audit/<date>_feedback.jsonl",
  ]
  failure_policy: "continue_on_partial"
  raw_compliance: [9, 10, 12, 71, 82, 91]
}
```

Notes:
- `engagement_pope_1995` and `drowsy_pollock_1990` are not in the canonical
  `_metrics/` table because they are derived (β/(α+θ) for Pope; (θ+α)/β for
  Pollock). They will live in `_metrics/derived/` and reuse Welch PSD via
  `_metrics/spectral_entropy.compute_psd_bands()`.
- `macos_notification_emitter` is in `_integrations/notification.hexa` (NEW;
  splits the osascript bit out of legacy eeg_feedback_loop.hexa).

## Recipe 4 — `daily_life_audit`

Replaces `eeg_daily_life_verifier.hexa`. 6-axis composite verdict per session.

```
recipe "daily_life_audit" {
  description: "6-axis daily-life session verdict"
  inputs: [".npy 16ch", "context.jsonl (raw#82 daily-life logger output)"]
  steps: [
    { kind: "gate",   module: "rms_band",            pass_required: true  },
    { kind: "metric", module: "lz76",                pass_required: true  },
    { kind: "metric", module: "permutation_entropy", pass_required: true  },
    { kind: "metric", module: "hjorth",              pass_required: true  },
    { kind: "metric", module: "gamma_theta",         pass_required: true  },
    { kind: "metric", module: "frontal_asymmetry",   pass_required: false, on_partial: "continue" },
    { kind: "integration", module: "behavioral",     pass_required: false, on_partial: "continue" },
  ]
  outputs: [
    "state/daily_life_audit/<date>_session.jsonl",
  ]
  failure_policy: "all_must_pass"   # need ≥4 of 6 for PAIR_OK
  raw_compliance: [9, 10, 12, 65, 71, 77, 82, 91, 106]
}
```

## Recipe 5 — `sleep_staging`

Replaces `sleep_tracker.hexa`. 30s AASM epochs → 5-state HMM → per-stage
metric aggregation.

```
recipe "sleep_staging" {
  description: "Overnight 8h → 30s epochs → AASM 5-state → per-stage LZ76/PE/Hjorth means"
  inputs: [".npy 16ch", "fs=125Hz", "duration ≥ 4h"]
  steps: [
    { kind: "gate",   module: "rms_band",                pass_required: true  },
    { kind: "ml",     module: "aasm_hmm_stager",         pass_required: true  },
    { kind: "metric", module: "lz76",                    pass_required: false, scope: "per_stage" },
    { kind: "metric", module: "permutation_entropy",     pass_required: false, scope: "per_stage" },
    { kind: "metric", module: "hjorth",                  pass_required: false, scope: "per_stage" },
    { kind: "metric", module: "spectral_entropy",        pass_required: false, scope: "per_stage" },
  ]
  outputs: [
    "state/sleep_audit/<date>_overnight.jsonl",
    "state/sleep_cert/<ts>_overnight.json",
  ]
  failure_policy: "continue_on_partial"
  raw_compliance: [9, 10, 12, 65, 71, 77, 82, 91, 106]
}
```

The per-stage scope is a new feature: the stager emits epoch-level state
labels, and each metric is computed on each stage's pooled epochs. Output
JSONL contains 5 rows per metric (one per state).

## Recipe 6 — `cross_modal_full`

Bringing 4 of the 7 integrations into one composite for the most complete
"is the user awake, engaged, and physiologically coherent" check.

```
recipe "cross_modal_full" {
  description: "Standard EEG + cardiac + webcam + wearable cross-validation"
  inputs: [".npy 16ch", "ECG/PPG aux", "webcam permission", "wearable export"]
  steps: [
    { kind: "pipeline", module: "standard",        pass_required: true  },
    { kind: "integration", module: "cardiac",      pass_required: false, on_partial: "continue" },
    { kind: "integration", module: "webcam",       pass_required: false, on_partial: "continue" },
    { kind: "integration", module: "wearable",     pass_required: false, on_partial: "continue" },
    { kind: "integration", module: "behavioral",   pass_required: false, on_partial: "continue" },
  ]
  outputs: [
    "state/cross_modal_audit/<date>_xmodal.jsonl",
    "state/cross_modal_cert/<ts>_xmodal.json",
  ]
  failure_policy: "continue_on_partial"
  raw_compliance: [9, 10, 12, 13, 65, 71, 77, 82, 91, 106]
}
```

raw#13 (privacy) is included because webcam + wearable carry I1-I7 invariants.

## Recipe 7 — `paper_p1_p2_p3` (pre-register reproducer)

Mirrors the three pre-registered paper claims (clm_eeg_p1_lz / p2_tlr /
p3_gcg). Used for falsification cycles.

```
recipe "paper_p1_p2_p3" {
  description: "P1 LZ76 + P2 TLR + P3 gamma/theta = 3 — frozen pre-register reproducer"
  inputs: [".npy 16ch", "fs=125Hz", "duration ≥ 60s eyes-closed"]
  steps: [
    { kind: "metric", module: "lz76",         pass_required: true,  freeze: "P1" },
    { kind: "metric", module: "permutation_entropy", pass_required: false },  # informational
    { kind: "metric", module: "tlr",          pass_required: true,  freeze: "P2" },
    { kind: "metric", module: "gamma_theta",  pass_required: true,  freeze: "P3" },
  ]
  outputs: [
    "state/clm_eeg_p1_lz_pre_register_real.json",
    "state/clm_eeg_p2_tlr_pre_register_real.json",
    "state/clm_eeg_p3_gamma_theta_pre_register_real.json",
    "state/paper_p1_p2_p3_audit/<date>_papers.jsonl",
  ]
  failure_policy: "continue_on_partial"
  raw_compliance: [9, 10, 12, 65, 71, 77, 82, 91, 106]
}
```

`tlr` (transient log-rate) is currently a separate stub at
`anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa`; migration adds it to
`_metrics/tlr.hexa`.

## Recipe 8 — `selftest_all`

Special meta-recipe that exercises every module's `--selftest` mode and
asserts the byte-frozen synthetic verdicts match the legacy outputs.

```
recipe "selftest_all" {
  description: "Run --selftest on every module + compare against frozen fixtures"
  inputs: ["selftest_fixtures/<module>_<mode>.expected.jsonl"]
  steps: [
    # auto-generated: 1 step per module × per --selftest-mode
  ]
  outputs: [
    "state/selftest_all_audit/<date>_selftest.jsonl",
  ]
  failure_policy: "all_must_pass"
  raw_compliance: [9, 10, 12, 65, 71]
}
```

This is what `hexa run anima-eeg-core/eeg_core.hexa selftest` runs. It
replaces the existing `anima-eeg/eeg_setup.hexa selftest` by extending the
scope from 8 backends to all 50 modules.

## Recipe author guidance

When proposing a new recipe:
1. Declare it in `_core/recipes.hexa` (extend the table; do not split files).
2. Add a 5-line description, expected duration, and target raw_compliance.
3. Add a fixture under `selftest_fixtures/<recipe>_synth_<mode>.expected.jsonl`
   so the selftest_all recipe covers it.
4. If a recipe needs a new metric, build the metric *first* (in `_metrics/`)
   and validate it standalone via `eeg_core metric <new>` before composing.
5. Recipes never embed Python or hardware code directly — they only compose
   modules. If a step "feels new," it belongs in a `_metrics/` or
   `_integrations/` module first.

## Compatibility with legacy invocations

To keep existing scripts / docs / CI running without edits, the legacy
verifier wrappers (Phase 5 of the migration plan) translate as follows:

| Legacy invocation | New equivalent |
|---|---|
| `clm_eeg_lz76_real.hexa --selftest` | `eeg_core metric lz76 --selftest` |
| `clm_eeg_pe_real.hexa --selftest` | `eeg_core metric pe --selftest` |
| `clm_eeg_berger_sanity.hexa --selftest` | `eeg_core gate berger_alpha --selftest` |
| `clm_eeg_gamma_theta_ratio.hexa` | `eeg_core metric gamma_theta` |
| `eeg_setup.hexa health` | `eeg_core hardware board_health` |
| `eeg_setup.hexa impedance` | `eeg_core hardware impedance` |
| `eeg_setup.hexa record` | `eeg_core record resting` |
| `eeg_setup.hexa selftest` | `eeg_core selftest` |
| `eeg_recorder.hexa --record --task resting_eyes_open` | `eeg_core record resting --task resting_eyes_open` |
| `long_duration_recorder.hexa --duration-min 60` | `eeg_core record long_duration --duration-min 60` |
| `sleep_tracker.hexa --record` | `eeg_core record sleep` |
| `eeg_feedback_loop.hexa --live` | `eeg_core pipeline feedback_loop --live` |
| `eeg_daily_life_verifier.hexa` | `eeg_core pipeline daily_life_audit` |
| `resting_state_network_analyzer.hexa --input X` | `eeg_core pipeline resting_full --input X` |
| `eeg_anomaly_autoencoder.hexa --train` | `eeg_core ml anomaly_autoencoder --mode train` |
| `eeg_to_token_cyborg.hexa --input X` | `eeg_core ml token_cyborg --input X` |
| `eeg_claude_cli_correlator.hexa --selftest` | `eeg_core integrate claude_cli --selftest` |
| `eeg_claude_cli_longitudinal_correlator.hexa` | `eeg_core integrate claude_cli_long` |
| `behavioral_correlates_logger.hexa` | `eeg_core integrate behavioral` |
| `eye_tracker_webcam.hexa --tick` | `eeg_core integrate webcam --tick` |
| `wearable_health_integrator.hexa --ingest --source oura` | `eeg_core integrate wearable --source oura --ingest` |
| `cardiac_eeg_integrator.hexa --tick` | `eeg_core integrate cardiac --tick` |
| `mobile_eeg_integrator.hexa` | `eeg_core integrate mobile` |
| `daily_life_context_logger.hexa` | `eeg_core integrate behavioral --logger context` |
| `pre_post_task_recorder.hexa` | `eeg_core record pre_post` |
| `longitudinal_session_recorder.hexa` | `eeg_core record longitudinal` |
| `protocols/p300_visual_oddball.hexa` | `eeg_core record visual_p300` |
| `protocol/p300_auditory_oddball.hexa` | `eeg_core record auditory_p300` |
| `headplot_helper.hexa` | `eeg_core ui headplot` |
| `full_helmet_view.hexa` | `eeg_core ui full_helmet` |
| `electrode_adjustment_helper.hexa` | `eeg_core hardware electrode_adjust` |

— end pipeline recipes.
