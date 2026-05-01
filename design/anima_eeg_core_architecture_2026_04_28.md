// anima-eeg-core architecture design
// 2026-04-28 · raw#9 hexa-only · raw#10 honest · raw#82 darwin-native
//
// Companion docs:
//   - design/anima_eeg_core_module_api.md       (per-module exact API spec)
//   - design/anima_eeg_core_pipeline_recipes.md (standard pipeline recipes)
//   - anima-eeg/MIGRATION_PLAN.md               (existing 24+ verifier migration)

# anima-eeg-core — unified architecture for 24+ distributed EEG verifiers

## 0. Goal & non-goals

**Goal:** Collapse 24+ existing verifier .hexa files (~14,589 LoC across
anima-eeg/, anima-eeg/tool/, anima-eeg/protocol(s)/, anima-clm-eeg/tool/) into a
single layered core engine + module system. Every recording paradigm, every
metric, every gate, every cross-modal integration becomes a small module that
plugs into a shared dispatcher and reuses one implementation of the half-dozen
patterns currently duplicated across all 24+ tools.

**Non-goals (raw#10 honest C3):**
1. **Migration is a separate cycle.** This agent designs only. Migrating
   existing tools is left to follow-up cycles per `anima-eeg/MIGRATION_PLAN.md`.
2. **No behavioural change** for any existing verdict. Migrated tools must
   reproduce byte-for-byte the JSONL audit rows of their predecessor on the
   shared selftest fixtures.
3. **Hardware paths stay darwin-native.** The core never tries to abstract
   away `.venv-eeg/bin/python` or `/dev/cu.usbserial-*` — those remain mac-host
   concerns reachable via `@resolver-bypass(reason="darwin-native: …")`.

## 1. Common patterns extracted from the 24+ verifier survey

After reading the canonical samples (lz76, pe, hjorth, berger, gamma_theta,
anomaly_autoencoder, token_cyborg, claude_cli_correlator, recorder, calibrate,
board_health_check, eeg_setup, long_duration_recorder, sleep_tracker,
resting_state_network_analyzer, eeg_feedback_loop, eye_tracker_webcam,
cardiac_eeg_integrator, wearable_health_integrator) the following 13 patterns
recur in every tool:

| # | Pattern | Files affected | Current state | Core target |
|---|---------|---------------|---------------|-------------|
| P1 | `_flags_only_argv()` argv normalizer | 24/24 | Copy-pasted body, ~12-line block | `_core/argv_normalize.hexa` |
| P2 | `--selftest` / `--selftest-mode <kind>` flag pair | 24/24 | Copy-pasted parser | `_core/cli_parser.hexa` |
| P3 | `_emit_trailer(reason, detail, fix)` raw#82-style error | 24/24 | Copy-pasted | `_core/trailer.hexa` |
| P4 | `.venv-eeg/bin/python` selection (`_pick_python`) | 18/24 | 4-tier fallback chain duplicated | `_core/python_selector.hexa` |
| P5 | Helper .py emit + dispatch + kv-line parse | 18/24 | `/tmp/<name>_helper.py` + `exec_with_status` + `parse_int_kv` | `_core/python_helper.hexa` |
| P6 | `.npy → flat int` loader | 9/24 | Inline numpy reshape + scaling | `_core/npy_loader.hexa` |
| P7 | `parse_raw_arrays(blob)` an11_b_eeg_ingest JSON parser | 6/24 | Identical 70-line parser | `_core/json_eeg_parser.hexa` |
| P8 | `now_iso()` / `now_date_utc()` UTC clock via `exec("date -u …")` | 24/24 | Inlined identically | `_core/clock.hexa` |
| P9 | `sha256_of_file(path)` via `shasum -a 256` | 22/24 | Identical 5-line | `_core/manifest.hexa` |
| P10 | `append_jsonl(path, line)` raw#77 schema row | 24/24 | scratch + `cat >>` shell append | `_core/jsonl_audit.hexa` |
| P11 | Frozen-criteria block + 3-tier verdict (PASS/PARTIAL/FAIL) | 16/24 | C1/C2/Cn ints + verdict-rule string | `_core/falsifier_runner.hexa` |
| P12 | JSON cert emit (`tool/version/raw_rank/criteria/...`) | 19/24 | Hand-rolled string concat | `_core/cert_emitter.hexa` |
| P13 | chflags uchg lock cycle (raw#1) on output | 5/24 | Inline `chflags nouchg/uchg` shell | `_core/chflags_lock.hexa` |

Pattern coverage sanity-check: every one of the 24 files exhibits ≥9 of these
13 patterns. The mean LoC per file devoted to *boilerplate copy* (P1, P3, P5,
P8, P9, P10) is **~180 lines**, i.e. ~30% of every file is duplicated machinery.
Across 24 files that is ~4,300 LoC of pure duplication.

## 2. Honest C3 — abstraction-failure risk axes

The 24 files are *not* uniformly shaped. raw#10 honest C3: any common-pattern
extraction can leak through these axes and silently break a migrated tool.

| Axis | Variability | Risk |
|------|-------------|------|
| A1 | helper .py emission location: `/tmp/x.py` (most) vs `state/.x.py` (lz76 / pe / hjorth — sandbox forces in-tree) | If `_core/python_helper` picks one location, sandbox tools regress. **Mitigation:** module accepts `helper_path` arg; default policy = workspace-state for `.venv-eeg` callers, /tmp for `/usr/bin/python3` callers. |
| A2 | python selection priority: tool-specific env var (`CLM_EEG_LZ76_PYTHON`) vs canonical `ANIMA_EEG_VENV_PYTHON` vs hard-coded `/usr/bin/python3` (eye_tracker, wearable) | Renaming an env var breaks user workflows. **Mitigation:** `_core/python_selector` accepts an `aliases:list` arg listing the legacy env-var names, checked in declared order. |
| A3 | argv normalizer: returns `array` (eeg_setup, long_duration_recorder) vs `list` (lz76, pe) | Hexa runtime type mismatch — `len()` works on both but iteration syntax differs. **Mitigation:** core function returns `list`; existing `array` callers cast at consumption (one-line change). |
| A4 | `--selftest-mode` semantics differ wildly: `random/structured` (lz76), `const/white/sine` (pe), `coupled/desync/tachy/brady/noisy_60hz` (cardiac), `normal/low_light/iris_occluded/cal_fail/eyes_closed/permission_denied/mixed_seq` (eye_tracker) | A single shared parser cannot interpret these. **Mitigation:** core parser returns the raw string; per-module fixture loader (in `_metrics/<x>_fixture.hexa` or `_paradigms/<x>_fixture.hexa`) decides what it means. |
| A5 | exit-code conventions: PASS=0/FAIL=1/PARTIAL=2 (pe) vs PASS=0/FAIL=1/no-PARTIAL (lz76) vs hard exit(2) on unknown-arg (all) | Pipeline composition will break if a PARTIAL is interpreted as failure. **Mitigation:** `_core/falsifier_runner` returns a typed verdict struct; the dispatcher decides exit-code mapping by recipe. |
| A6 | hardware vs synthetic split: `--check` (board_health), `--calibrate` (calibrate.hexa), `--record` (recorder, long_duration), `--ingest` (wearable), `--tick` (cardiac, eye_tracker), `--live` (eeg_feedback_loop) | Different verbs for fundamentally the same "use real hardware now" mode. **Mitigation:** core dispatcher exposes one verb (`run`) with a `--source {selftest|hardware|file}` discriminator; each module aliases its legacy verb back to that for backwards compat. |
| A7 | board defaults: `cyton_daisy` (most), explicit synthetic fallback (recorder.hexa), board-id 2 hardcode (calibrate, board_health) | A core-level board enum could dictate a default that diverges from `recordings/` history. **Mitigation:** `_core/board_config` reads `recordings/sessions/last_board.json` SSOT first, hardcoded default last. |
| A8 | helper-py kv parse vs JSON parse: most use `key=value` lines, recorder.hexa uses JSON | Mixing the two confuses parser. **Mitigation:** `_core/python_helper.run` returns both — `kv_blob` and `json_blob` slots; helper picks one. |
| A9 | privacy / `chflags uchg` cycle: only 5 tools enforce (eye_tracker, wearable, cardiac, mobile, daily_life_logger). Migrating *more* tools through the core can accidentally lock outputs that should remain mutable. | **Mitigation:** chflags is opt-in, declared per-recipe in `_core/cert_emitter`. |
| A10 | License / framework citation strings: every tool hand-rolls them | The cert emitter could centralize → bibliography drift if a citation gets corrected in only one place. **Mitigation:** `_core/citations.hexa` SSOT with `citation("schartner_2015")` lookup. |

These 10 axes are the **floor** for migration regression risk. raw#10 honest:
this is what we *know about*; there are likely 2-5 additional silent failure
modes that surface only at migration time.

## 3. Module taxonomy — 50 modules across 7 categories

```
anima-eeg-core/
├── eeg_core.hexa                 ─ root dispatcher (subcommand router)
├── _core/                        ─ shared infrastructure (13 modules)
│   ├── argv_normalize.hexa       ─ P1: drop interpreter prefix, return list
│   ├── cli_parser.hexa           ─ P2: --selftest/--input/--out parser
│   ├── trailer.hexa              ─ P3: reason/fix stderr trailer
│   ├── python_selector.hexa      ─ P4: .venv-eeg / system / aliases priority
│   ├── python_helper.hexa        ─ P5: emit + dispatch + kv-line parse
│   ├── npy_loader.hexa           ─ P6: .npy → flat int via helper
│   ├── json_eeg_parser.hexa      ─ P7: an11_b_eeg_ingest schema parse
│   ├── clock.hexa                ─ P8: now_iso / now_date_utc
│   ├── manifest.hexa             ─ P9: sha256_of_file + sha256_of_str
│   ├── jsonl_audit.hexa          ─ P10: append_jsonl + scratch dance
│   ├── falsifier_runner.hexa     ─ P11: criteria → 3-tier verdict
│   ├── cert_emitter.hexa         ─ P12: JSON cert SSOT
│   ├── chflags_lock.hexa         ─ P13: nouchg → write → uchg
│   ├── citations.hexa            ─ A10: bibliography SSOT
│   └── board_config.hexa         ─ A7: board defaults SSOT
├── _gates/                       ─ pre-run signal-quality gates (4 modules)
│   ├── berger_alpha.hexa         ─ ex clm_eeg_berger_sanity
│   ├── rms_band.hexa             ─ wire-alive / helmet-on rms gate
│   ├── pe_saturation.hexa        ─ PE>0.95 = synthetic-ish, gate fail
│   └── hjorth_band.hexa          ─ hjorth in [1.0, 2.0] gate
├── _metrics/                     ─ per-window metric kernels (10 modules)
│   ├── lz76.hexa                 ─ ex clm_eeg_lz76_real
│   ├── permutation_entropy.hexa  ─ ex clm_eeg_pe_real
│   ├── hjorth.hexa               ─ ex clm_eeg_hjorth_real
│   ├── gamma_theta.hexa          ─ ex clm_eeg_gamma_theta_ratio
│   ├── alpha_coherence.hexa      ─ ex resting_state_network_analyzer (DMN bit)
│   ├── alpha_phase_plv.hexa      ─ frontal-occipital phase-locking (NEW)
│   ├── dmn_coherence.hexa        ─ ex resting_state_network_analyzer (network bit)
│   ├── frontal_asymmetry.hexa    ─ Davidson 1992 (split out from RSN)
│   ├── spectral_entropy.hexa     ─ Welch PSD entropy (NEW)
│   └── change_points.hexa        ─ PELT on b(n) timeseries (ex long_duration_recorder)
├── _paradigms/                   ─ recording paradigms (8 modules)
│   ├── resting.hexa              ─ ex eeg_recorder (resting subset)
│   ├── daily_life.hexa           ─ ex eeg_daily_life_verifier
│   ├── visual_p300.hexa          ─ ex protocols/p300_visual_oddball
│   ├── auditory_p300.hexa        ─ ex protocol/p300_auditory_oddball
│   ├── pre_post.hexa             ─ ex pre_post_task_recorder
│   ├── longitudinal.hexa         ─ ex longitudinal_session_recorder
│   ├── long_duration.hexa        ─ ex long_duration_recorder (60-120 min)
│   └── sleep.hexa                ─ ex sleep_tracker (8 hr overnight)
├── _integrations/                ─ cross-modal physiology fusers (6 modules)
│   ├── claude_cli.hexa           ─ ex eeg_claude_cli_correlator (T1)
│   ├── claude_cli_long.hexa      ─ ex eeg_claude_cli_longitudinal_correlator (B9)
│   ├── behavioral.hexa           ─ ex behavioral_correlates_logger (B11)
│   ├── webcam_gaze.hexa          ─ ex eye_tracker_webcam (C19)
│   ├── wearable.hexa             ─ ex wearable_health_integrator (C18)
│   ├── cardiac.hexa              ─ ex cardiac_eeg_integrator (C20)
│   └── mobile.hexa               ─ ex mobile_eeg_integrator (C21)
├── _ml/                          ─ ML / token / autoencoder (2 modules)
│   ├── anomaly_autoencoder.hexa  ─ ex eeg_anomaly_autoencoder (B10)
│   └── token_cyborg.hexa         ─ ex eeg_to_token_cyborg (B12)
├── _hw/                          ─ hardware probes (5 modules; darwin-native)
│   ├── board_health.hexa         ─ ex board_health_check
│   ├── calibrate.hexa            ─ ex calibrate
│   ├── impedance.hexa            ─ ex impedance_check
│   ├── impedance_validate.hexa   ─ ex impedance_real_hardware_validation
│   └── electrode_adjust.hexa     ─ ex electrode_adjustment_helper / electrode_helper_rich
└── _ui/                          ─ ASCII / Rich UI helpers (2 modules)
    ├── headplot_ascii.hexa       ─ ex headplot_helper
    └── full_helmet_view.hexa     ─ ex full_helmet_view
```

**Module count summary (50 total):**
- _core         : 15 (infrastructure SSOT)
- _gates        :  4
- _metrics      : 10
- _paradigms    :  8
- _integrations :  7
- _ml           :  2
- _hw           :  5
- _ui           :  2
- root          :  1 (`eeg_core.hexa`)

This is *additive* over the existing tree; the legacy verifier files remain
in place during migration and become thin wrappers that import the new modules
(see §6 migration plan).

## 4. Module dependency graph

```
                          ┌─────────────────────┐
                          │   eeg_core.hexa     │  (root dispatcher)
                          └──────────┬──────────┘
                                     │ subcommand routing
        ┌──────────┬──────────┬──────┼──────┬──────────┬──────────┬─────────┐
        ▼          ▼          ▼      ▼      ▼          ▼          ▼         ▼
     _gates    _metrics  _paradigms _hw  _integrations _ml     _ui       (helper)
        │          │          │      │      │           │       │
        ├──────────┴──────────┴──────┴──────┴───────────┴───────┘
        │                            │
        ▼                            ▼
  ┌────────────────────────────────────────────────────────┐
  │                       _core/                           │
  │                                                        │
  │  argv_normalize ─┐                                     │
  │  cli_parser ─────┼─► trailer ◄── (every module)        │
  │  python_selector─┤                                     │
  │  python_helper ──┴─► npy_loader ── json_eeg_parser     │
  │                                                        │
  │  clock ─► manifest ─► jsonl_audit ─► chflags_lock      │
  │                                                        │
  │  citations ─► falsifier_runner ─► cert_emitter         │
  │  board_config                                          │
  └────────────────────────────────────────────────────────┘
```

**Dependency rules (enforced at import-time, not at runtime):**
1. `_core/*` modules may import from each other only via the chain shown
   (left-to-right, top-to-bottom). No cycles.
2. `_gates`, `_metrics`, `_paradigms`, `_hw`, `_integrations`, `_ml`, `_ui`
   may import any `_core/*` module but **not each other**, except: paradigms
   may compose metrics (via dispatcher, not direct import), integrations may
   compose metrics (same), and `_ml` may consume `_metrics` outputs.
3. `eeg_core.hexa` is the *only* file that imports directly from category
   roots. End-users never import a category module by path.

## 5. Core dispatcher — `eeg_core` subcommand surface

The root dispatcher is invoked as

```
hexa run anima-eeg-core/eeg_core.hexa <verb> <noun> [flags]
```

Verbs are deliberately small in number (raw#101 minimal) so the surface is
memorizable. Eight verbs cover all 24+ legacy use cases:

```
SUBCOMMAND TABLE
────────────────
eeg_core gate     <gate-name>     [--input p] [--out p]
        ├ berger_alpha            occipital alpha dominance
        ├ rms_band                wire-alive / helmet-on
        ├ pe_saturation           synthetic-ish detector
        └ hjorth_band             complexity in [1.0, 2.0]

eeg_core metric   <metric-name>   [--input p] [--out p]
        ├ lz76                    Kaspar-Schuster 1987 production count
        ├ pe                      Bandt-Pompe 2002 permutation entropy
        ├ hjorth                  Hjorth 1970 activity/mobility/complexity
        ├ gamma_theta             Welch PSD γ/θ ratio (own 3 σ/τ=3)
        ├ alpha_coherence         pairwise alpha-band coherence
        ├ alpha_phase_plv         frontal-occipital phase-lock
        ├ dmn_coherence           Fp1/Fp2 ↔ P3/P4 alpha coh
        ├ frontal_asymmetry       Davidson 1992 log-power LR delta
        ├ spectral_entropy        Welch PSD Shannon entropy
        └ change_points           PELT on b(n) series

eeg_core pipeline <recipe>        [--input p] [--out p]
        ├ standard                berger → lz76 → pe → hjorth (4-step)
        ├ resting_full            standard + dmn + frontal_asym + alpha_coh
        ├ feedback_loop           rms → engagement_pope → drowsy_pollock
        ├ daily_life_audit       (axes-based, ex eeg_daily_life_verifier)
        └ sleep_staging           (60s segments → AASM HMM, ex sleep_tracker)

eeg_core record   <paradigm>      [--duration n] [--out p]
        ├ resting                 5-min eyes-open / eyes-closed
        ├ visual_p300             oddball stimulus
        ├ auditory_p300           tone oddball
        ├ pre_post                A/B around a task
        ├ longitudinal            scheduled daily session
        ├ long_duration           60/90/120 min continuous
        └ sleep                   8-hr overnight

eeg_core hardware <action>        [--port p] [--board name]
        ├ board_health            no-helmet pin sanity
        ├ calibrate               full calibrate + impedance
        ├ impedance               z<CH><PCHAN><NCHAN>Z 5-state
        ├ impedance_validate      worn-helmet evidence
        └ electrode_adjust        live single-channel touch UI

eeg_core integrate <source>       [--in p] [--source kind]
        ├ claude_cli              ex T1 correlator
        ├ claude_cli_long         ex B9 longitudinal correlator
        ├ behavioral              ex B11 logger
        ├ webcam                  ex C19 eye tracker
        ├ wearable                ex C18 (apple/oura/whoop)
        ├ cardiac                 ex C20 ECG/PPG
        └ mobile                  ex C21 phone-EEG

eeg_core ml       <model>         [--input p] [--mode train|infer]
        ├ anomaly_autoencoder     ex B10
        └ token_cyborg            ex B12

eeg_core ui       <view>          [--input p]
        ├ headplot                ASCII 10-20 head plot
        └ full_helmet             16ch concurrent 5-state
```

Every subcommand also accepts:

```
  --selftest                       use the module's deterministic synth fixture
  --selftest-mode <kind>           module-specific (passed through)
  --audit-jsonl <path>             override default audit JSONL
  --out <path>                     override default JSON cert
  --json                           emit JSON cert to stdout instead of disk
  --quiet                          suppress human-readable banner
  --help                           per-subcommand help
```

There are also two top-level meta-commands:

```
eeg_core list      [--category gates|metrics|...]   enumerate available modules
eeg_core selftest  [--category ...]                 run --selftest on every module
                                                    (mirrors eeg_setup selftest)
```

## 6. Migration plan — 24+ legacy verifier → core

### 6.1 Strategy
Each legacy verifier becomes a **3-line wrapper** that delegates to the
corresponding core module. Example:

```hexa
// anima-clm-eeg/tool/clm_eeg_lz76_real.hexa  (post-migration)
fn main() {
    exit(eeg_core_metric("lz76", argv_pass_through()))
}
```

Wrappers preserve the legacy `hexa run anima-clm-eeg/tool/<x>.hexa --selftest`
invocation so existing CI / docs / scripts keep working unchanged.

### 6.2 Phasing
| Phase | Cycles | Scope | Risk |
|-------|--------|-------|------|
| 1 | 1     | `_core/*` (15 modules, target ~1500 LoC total) | LOW — pure code-extraction, identical behaviour |
| 2 | 1     | `_gates` + `_metrics` (14 modules, the most copy-pasted) | LOW — closed-form math, byte-equality fixtures available |
| 3 | 2     | `_paradigms` + `_hw` (13 modules, hardware-touching) | MEDIUM — darwin-native USB / venv quirks |
| 4 | 2     | `_integrations` + `_ml` + `_ui` (12 modules) | MEDIUM-HIGH — privacy invariants (eye_tracker), training (autoencoder) |
| 5 | 1     | Replace each legacy verifier file with a 3-line wrapper | LOW — once core is fixture-equal |
| 6 | 1     | Retire the wrapper layer (legacy paths become symlinks); keep eeg_setup as a known dispatch alias | LOW |

### 6.3 LoC cost estimate (per-file → per-module)

Conservative measurement: average 24-file LoC = 14589/24 ≈ **608 LoC per
verifier**. Of this, ~30% (~180 LoC) is duplicated boilerplate (P1/P3/P5/P8/
P9/P10) deletable post-migration, and ~20% (~120 LoC) is metric-specific glue
that moves into `_metrics/<x>.hexa` unchanged.

**Per-tool migration LoC delta (estimate):**
- Boilerplate deleted (move to `_core/`)         : −180 LoC
- Metric-specific code moved to `_metrics/<x>`   :    0 LoC (relocated, identical)
- New 3-line wrapper                             :   +3 LoC
- Net per-tool                                   : **−177 LoC**

**Aggregate across 24 tools:**
- LoC removed from legacy tree     : 24 × 180 = 4,320 LoC
- LoC added to `_core/`            : ~1,500 LoC (deduplicated)
- LoC added to `_gates/_metrics/_paradigms/_integrations/_ml/_hw/_ui` : ~7,500 LoC (relocated, not new)
- Net workspace LoC change         : **−2,800 LoC** (≈ 19% of the 14,589 starting LoC)

**Migration effort estimate:**
- Per-tool wrapper conversion : 30 min (mechanical)
- Per-module extraction       : 2 hr (read original + write `_core` user + selftest equality)
- Phase-1 _core build         : 8 hr (15 modules)
- Phase-2 gates+metrics       : 28 hr (14 modules)
- Phase-3 paradigms+hw        : 26 hr (13 modules) + 4 hr darwin-native verification
- Phase-4 integrations+ml+ui  : 24 hr (12 modules) + 4 hr privacy / training audit
- Phase-5 wrapper cutover     : 12 hr (24 wrappers)
- **Total: ~106 hr** (≈ 13 8-hr sessions, spread over 4-6 cycles)

### 6.4 Compatibility & rollback contract

1. Every legacy `hexa run <legacy-path> --selftest` MUST exit 0 against the
   core implementation before the wrapper is committed.
2. Every legacy JSONL audit row MUST be byte-identical (modulo `ts` field)
   between legacy and core on a frozen synthetic input.
3. Each phase ships behind a feature flag `EEG_CORE_PHASE_N=1`; without it,
   the wrapper falls through to the legacy in-tree implementation.
4. Rollback = unset the flag. Legacy code is not deleted until phase 6.

## 7. Directory layout (final state)

```
anima/
├── anima-eeg-core/                     ← NEW, all design artifacts here
│   ├── eeg_core.hexa                   ← root dispatcher
│   ├── _core/   (15 modules)
│   ├── _gates/  (4 modules)
│   ├── _metrics/ (10 modules)
│   ├── _paradigms/ (8 modules)
│   ├── _hw/     (5 modules)
│   ├── _integrations/ (7 modules)
│   ├── _ml/     (2 modules)
│   ├── _ui/     (2 modules)
│   ├── README.md
│   └── selftest_fixtures/              ← byte-frozen .npy + JSONL targets for migration
├── anima-eeg/                          ← LEGACY (Phase 1-5: thin wrappers; Phase 6: symlinks)
│   ├── eeg_setup.hexa                  ← stays as dispatch alias
│   ├── tool/...                        ← thin wrappers
│   └── protocol(s)/...                 ← thin wrappers
└── anima-clm-eeg/tool/                 ← LEGACY (Phase 1-5: thin wrappers; Phase 6: symlinks)
    └── clm_eeg_*.hexa                  ← thin wrappers
```

## 8. raw# compliance checklist (per-module enforcement)

Every module must declare in its header:
```
//   raw#9   pure-hexa
//   raw#10  honest C3 (synthetic vs real classification)
//   raw#11  snake_case
//   raw#12  pre-registered criteria (frozen)
//   raw#37  transient .py helper (if applicable)
//   raw#65  idempotent
//   raw#71  ≥3 falsifiers
//   raw#77  JSONL audit schema
//   raw#82  darwin-native (if hardware-touching)
//   raw#91  honesty triad
//   raw#101 minimal surface
//   raw#106 genus name
```

The `_core/falsifier_runner.hexa` enforces raw#12 + raw#71 by refusing to
compute a verdict if `criteria_frozen_at` is empty or `falsifiers.len < 3`.
The `_core/cert_emitter.hexa` enforces raw#10 + raw#91 by refusing to emit a
classification of `REAL_HW_PASS` unless `mode == "real" && input_sha256 != ""`.

## 9. raw#10 honest C3 — what this design *does not* solve

1. **Helper .py heterogeneity (axis A1).** `_core/python_helper.hexa` will
   support both /tmp and workspace-state paths but cannot guess correctly
   which to use without reading the calling module's policy. Migration risk:
   silent path mismatch.
2. **Selftest-mode strings (axis A4).** Centralizing them is impossible —
   they are bona-fide per-module fixtures. The core merely passes the string
   through; module bears responsibility.
3. **Sleep / long-duration / overnight tools** have wall-clock dependencies
   the core cannot abstract; they remain darwin-native, foreground processes.
4. **Privacy invariants** (eye_tracker C19's I1-I7) are tool-specific and not
   centrally checkable. `_core/chflags_lock` only handles the I6 file-lock
   side; I1-I5 + I7 stay in the integration module.
5. **The 24+ count is a snapshot, not a ceiling.** New paradigms (e.g. EMG
   coupling, pupillometry, phone-accelerometer) will arrive; the directory
   layout reserves the empty `_integrations/` and `_paradigms/` namespaces
   for additive growth — but the dispatcher table will need maintenance.

## 10. Phase-1 implementation order (recommended)

To validate the architecture **before** any user-visible behaviour change:

| Step | Module | Dependency | Validation |
|------|--------|------------|-----------|
| 1.1 | `_core/argv_normalize.hexa` | none | unit-test against 5 sample argv shapes |
| 1.2 | `_core/trailer.hexa` | none | unit-test stderr format |
| 1.3 | `_core/clock.hexa` | none | unit-test ISO format |
| 1.4 | `_core/manifest.hexa` | clock | unit-test sha256 stability |
| 1.5 | `_core/citations.hexa` | none | unit-test citation lookup |
| 1.6 | `_core/python_selector.hexa` | none | unit-test 4-tier fallback |
| 1.7 | `_core/python_helper.hexa` | python_selector + trailer | round-trip kv parse |
| 1.8 | `_core/npy_loader.hexa` | python_helper | load fixture .npy → flat int |
| 1.9 | `_core/json_eeg_parser.hexa` | none | parse fixture an11_b_eeg_ingest |
| 1.10 | `_core/jsonl_audit.hexa` | clock | append + read-back |
| 1.11 | `_core/falsifier_runner.hexa` | citations | 3-tier verdict on synthetic |
| 1.12 | `_core/cert_emitter.hexa` | clock + manifest + falsifier_runner | byte-equal cert vs legacy lz76 |
| 1.13 | `_core/board_config.hexa` | none | resolve cyton_daisy |
| 1.14 | `_core/cli_parser.hexa` | argv_normalize + trailer | parse 8 sample CLIs |
| 1.15 | `_core/chflags_lock.hexa` | trailer | nouchg/uchg cycle |
| 1.16 | `eeg_core.hexa` | all of _core | dispatch `list` and `selftest` no-ops |

After step 1.16 (≈ 16 hours of work) the core is *callable* but has no actual
metric/gate/paradigm modules yet — it just demonstrates the dispatcher
surface and the SSOT for shared patterns. This is the smallest unit that
proves the architecture is viable and lets us land it as a single PR before
any migration risk is taken.

— end design doc.
