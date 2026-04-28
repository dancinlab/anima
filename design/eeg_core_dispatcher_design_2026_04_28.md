# eeg_core dispatcher design — unified EEG entry point + anima cli absorption

**Date:** 2026-04-28
**Author:** anima-eeg-core dispatcher cycle
**Schema:** `anima-eeg-core/eeg_core/1`
**Companion docs:**
- `design/anima_eeg_core_architecture_2026_04_28.md` (50-module taxonomy)
- `design/anima_eeg_core_module_api.md` (per-module exact API)
- `design/anima_eeg_core_pipeline_recipes.md` (composite recipes)

raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen · raw#37 transient
raw#65 idempotent · raw#82 darwin-native · raw#91 honest · own5

---

## 0. Goal

Single canonical entry point (`bin/eeg` → `anima-eeg-core/tool/eeg_core.hexa`)
that dispatches to every EEG operation across the four EEG-touching repos:

- `anima-eeg/` (16 hardware + recording verifiers)
- `anima-eeg/tool/` (14 paradigm/integration tools)
- `anima-clm-eeg/tool/` (12 metric + ML kernels)
- `anima-eeg-core/tool/modules/` (Phase-1+2 landed modules — gates so far)

The dispatcher **routes** but does not own logic. Logic lives in modules.
Most subcommands currently wrap legacy tools (`legacy:`); migration to
`landed:` modules is a per-cycle task tracked in the architecture doc's
50-module migration table.

## 1. Subcommand tree (43 routes)

```
eeg list                                ─ enumerate all subcommands
eeg selftest                            ─ dispatcher integrity test

eeg gate-all      [--input <npy>]       ─ landed (composite of 4 gates)
eeg gate-berger   [--input <npy>]       ─ landed
eeg gate-rms      [--input <npy>]       ─ landed
eeg gate-pe       [--input <npy>]       ─ landed
eeg gate-hjorth   [--input <npy>]       ─ landed

eeg metric lz76         --input <npy>   ─ legacy (clm-eeg)
eeg metric pe           --input <npy>   ─ legacy
eeg metric hjorth       --input <npy>   ─ legacy
eeg metric gamma_theta  --input <npy>   ─ legacy
eeg metric berger       --input <npy>   ─ legacy
eeg metric all          --input <npy>   ─ pending

eeg pipeline standard   --input <npy>   ─ pending
eeg pipeline daily-life --input <npy>   ─ legacy
eeg pipeline feedback   --input <npy>   ─ legacy

eeg record resting      --duration 60   ─ legacy (eeg_recorder)
eeg record daily-life   --duration 300  ─ legacy
eeg record sleep        --duration 28800─ legacy
eeg record long         ...             ─ legacy
eeg record longitudinal ...             ─ legacy
eeg record pre-post     ...             ─ legacy

eeg hardware health             [--selftest]    ─ legacy (board_health_check)
eeg hardware impedance          [--check]       ─ legacy
eeg hardware impedance_validate                 ─ legacy
eeg hardware adjust                             ─ legacy (electrode_adjust)
eeg hardware rich                               ─ legacy (Rich TUI)
eeg hardware headplot                           ─ legacy
eeg hardware full                               ─ legacy (16ch concurrent)
eeg hardware ftdi-fix                           ─ legacy
eeg hardware brainflow-sanity                   ─ legacy

eeg artifact detect-all          --input <npy>  ─ pending
eeg artifact environmental-emi   --input <npy>  ─ landed (Phase-artifact)

eeg integrate claude-cli      --cli-jsonl <p>   ─ legacy
eeg integrate claude-cli-long --cli-jsonl <p>   ─ legacy
eeg integrate wearable        --source apple    ─ legacy
eeg integrate mobile          ...               ─ legacy
eeg integrate cardiac         ...               ─ legacy
eeg integrate eye-tracker     ...               ─ legacy

eeg ml anomaly       --input <npy>      ─ legacy (autoencoder)
eeg ml token-cyborg  --input <npy>      ─ legacy

eeg analyze rsn               --input <npy>     ─ legacy
eeg analyze behavioral        ...               ─ legacy
eeg analyze daily-life-verify ...               ─ legacy
```

Status counts at land time: **landed=6 · legacy=33 · pending=4 · total=43**.

## 2. anima cli absorption mapping

Existing `anima` top-level CLI (`bin/anima` → `tool/anima_cli/<topic>.hexa`)
provides 28 topics: compute / weight / proposal / cert / roadmap / serve /
paradigm / inbox / cost / audit / doctor / sync / log / bench / handoff /
metrics / watch / snap / replay / onboard / backup / reproducibility / gc /
health / stats / paradigm.

**EEG topic in `tool/anima_cli/`?** None. After scanning all 27 anima_cli/*.hexa
files for "eeg|electrode|impedance|brain", **zero** matches. The existing
anima CLI has **no EEG subcommand at all**.

**Implication:** there is nothing to "absorb" from anima_cli — `bin/eeg` is
a parallel top-level entry, mirroring `bin/anima`'s topic-dispatcher pattern
but specialized for EEG. The two coexist:

```
bin/anima ........... compute-agnostic operational CLI (28 topics, no EEG)
bin/eeg ............. unified EEG dispatcher (anima-eeg-core)
anima-eeg/eeg_setup ─ backward-compat shim (8 hardware backends)
```

Future option (deferred to a later cycle): expose `anima eeg <verb>` as an
`anima` topic that proxies to `eeg_core.hexa`. Cheap to add via a
`tool/anima_cli/eeg.hexa` module of ~30 LoC. **Not done in this cycle**
to keep PR diff minimal and avoid touching `bin/anima` semantics.

## 3. Migration plan from `eeg_setup.hexa`

`anima-eeg/eeg_setup.hexa` is the existing 8-backend hardware dispatcher.
`eeg_core.hexa` is a strict super-set:

| eeg_setup verb        | eeg_core route                           |
|-----------------------|------------------------------------------|
| `health`              | `eeg hardware health`                    |
| `impedance`           | `eeg hardware impedance`                 |
| `impedance_validate`  | `eeg hardware impedance_validate`        |
| `headplot`            | `eeg hardware headplot`                  |
| `adjust`              | `eeg hardware adjust`                    |
| `rich`                | `eeg hardware rich`                      |
| `full`                | `eeg hardware full`                      |
| `record`              | `eeg record resting`                     |

**Backward compatibility:** `anima-eeg/eeg_setup.hexa` is **unchanged**. It
remains callable via `hexa run anima-eeg/eeg_setup.hexa <sub>` for any
existing scripts / muscle memory. No deprecation warning emitted in this
cycle (raw#10 honest: a forced deprecation would break existing harnesses).

A future cycle may add a one-line deprecation notice to `eeg_setup.hexa`'s
`_print_usage` recommending `eeg hardware <noun>` as the new path.

## 4. bin/eeg PATH installation

`bin/eeg` is a 87-line bash wrapper that:

1. Resolves `ANIMA_ROOT` via `$ANIMA` env / sibling-dir probe / git toplevel
2. Resolves `HEXA_BIN` via `$HEXA_BIN` / `$HEXA_LANG/hexa.real` /
   `/Users/ghost/core/hexa-lang/hexa.real` / `command -v hexa`
3. `cd` to repo root (so backends can resolve relative paths)
4. `exec hexa run anima-eeg-core/tool/eeg_core.hexa "$@"`

This mirrors `bin/anima`'s pattern. To install on PATH, add
`$WS/anima/bin` to `$PATH` (already on user's PATH per existing `bin/anima`
usage). After install:

```bash
eeg list
eeg selftest
eeg gate-all --selftest-mode awake
eeg gate-all --input recordings/sessions/X.npy
eeg hardware health --selftest
```

## 5. Pending modules (4)

raw#10 honest C3: subcommands listed below emit `NOT_YET_LANDED` verdict
with exit 4. They are tracked here for the next migration cycle.

| Subcommand                  | Reason                                | Module to land                     |
|-----------------------------|---------------------------------------|------------------------------------|
| `metric all`                | requires per-metric dispatcher loop   | `_metrics/all_dispatcher.hexa`     |
| `pipeline standard`         | gate→metric→audit composite recipe    | `_paradigms/pipeline_standard.hexa`|
| `artifact detect-all`       | aggregates _artifact/* modules        | `_artifact/detect_all.hexa`        |

## 6. Selftest results

```
$ eeg selftest
── eeg_core dispatcher selftest ──
  T1: routing-coverage PASS (9 pairs)
  T2: composite_gate.hexa present
  T3: legacy eeg_setup.hexa present (backward compat)
  T4: bin/anima top-level present
pass: 4  fail: 0
verdict: DISPATCHER_SELFTEST_PASS ✓

$ eeg gate-all --selftest-mode awake
verdict: BACKEND_PASS ✓ (all 4 gates PASS)

$ eeg gate-all --input recordings/sessions/baseline_resting_post_battery_20260428T132612Z_seg000_eeg16_filtered.npy
verdict: BACKEND_FAIL ✗ rc=1
  (berger PASS, rms PASS, pe PASS, hjorth FAIL — gates honestly distinguish
   selftest fixture vs real recording dynamics; this is expected raw#10
   behaviour, not a dispatcher bug.)
```

## 7. Next-cycle recommendations

1. **`metric` migration** (highest leverage). Land `_metrics/lz76.hexa`,
   `_metrics/pe.hexa`, `_metrics/hjorth.hexa`, `_metrics/gamma_theta.hexa`
   per the architecture doc's exact API. ~5 modules · ~600 LoC each ·
   regression-test against the `clm_eeg_*_real.hexa` predecessors on the
   shared selftest fixtures.
2. **`pipeline standard`** composite recipe (`gate-all → metrics → audit`)
   once metric modules exist.
3. **`artifact detect-all`** aggregating the partially-landed `_artifact/`
   modules (currently only `environmental_emi_classifier.hexa` is in tree).
4. **Optional `anima eeg` proxy topic** in `tool/anima_cli/eeg.hexa` (~30 LoC)
   so the user can also reach EEG tools via the existing `anima` CLI.
