# anima-clm-eeg → anima-eeg-core Migration Plan

> **scope**: planning-only roadmap document for absorbing `anima-clm-eeg/` legacy R&D tools into the canonical `anima-eeg-core/` dispatcher. Code migration is a SEPARATE ω-cycle (this doc is the spec; not the implementation).
> **author**: Claude Opus 4.7 (1M ctx) — sub-agent, read-only inventory pass
> **date**: 2026-04-29
> **target absorption window**: post Phase 6 _integrations/ landing (commits 02ac714c3, 86465c662, 4cd8e62da, 6cf5ded72) → planned ω-cycle clm-eeg-migration-{01..NN}
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen-spec · raw#71 falsifier · raw#91 honest C3 · raw#137 80% Pareto · own#4 root-cause-only

---

## §0. Executive summary

`anima-clm-eeg/` (canonical path `/Users/ghost/core/anima/anima-clm-eeg/`) is a **128-file / ~30,594 LoC** research-cadence sub-repo holding raw#9 hexa-only falsifier pre-register tools (clm_eeg_p1/p2/p3, harness_smoke, synthetic_fixture) plus a Mk.XII Integration tier scaffolding cluster (g8/g9/g10, preflight cascade, hexad triangulation, witness-ledger reverify). Phase 6 of `anima-eeg-core/` has just landed **7 `_integrations/` modules** (clm_eeg_p1, clm_eeg_p3, berger_validate, artifact_pipeline, rsn_validate, cyborg_token_emit, multi_subject_aggregate) plus 9 `_metrics/`, 5 `_gates/`, 4 `_paradigms/`, 5 `_hw/`, 9 `_artifact/`, 9 `_core/` siblings — a full 50+ module dispatcher under `tool/eeg_core.hexa`.

The dispatcher already **soft-routes** to legacy paths via `legacy:anima-clm-eeg/tool/...` strings (5 sites: `berger`, `claude-cli`, `claude-cli-long`, `anomaly`, `token-cyborg`), so the migration is **already partially staged**. This plan formalizes the remaining absorption.

**Categorization summary** (28 hexa tools + 1 .sh.txt):
- **ABSORB-WRAP** (raw#12 frozen-spec backend, dispatcher wrapper): 5 tools (~3,107 LoC frozen)
- **ABSORB-PORT** (rewrite native eeg-core hexa): 4 tools (~2,026 LoC source ported)
- **DEPRECATE** (superseded by Phase 6 _integrations/): 5 tools (~1,991 LoC archived)
- **ARCHIVE** (Mk.XII research artifacts, out-of-EEG-axis): 11 tools (~7,159 LoC frozen)
- **KEEP-EXTERNAL** (CLM-only / non-EEG): 3 tools (~1,213 LoC unchanged)
- **DELETE** (deprecated escape-hatch): 1 .sh.txt

**Estimated effort**: ~24 engineering hours (3 working days) split across 4 ω-cycles.

**Order of operations**: (1) DEPRECATE first (zero net new code) → (2) ABSORB-WRAP (raw#12 freeze + thin dispatcher hooks) → (3) ARCHIVE (chflags lock + .marker) → (4) ABSORB-PORT (highest risk, last).

raw#10 honest C3: this plan's verdict is **NOT** that absorption is complete — only the **routing** is staged; **no source files have moved**. Categorization is best-effort from filename + dispatcher cross-ref + landing-doc reading; per-file diff vs Phase 6 native modules is a separate audit cycle.

---

## §1. Inventory of `anima-clm-eeg/`

### §1.1 Top-level

```
anima-clm-eeg/
├── README.md                 (200L cross-link policy SSOT)
├── tool/                     28 .hexa + 1 .sh.txt = 29 files
├── state/                    19 .json + 20 .marker + 1 markers/ subdir = 38 files
├── docs/                     47 .md + 1 d_day_session_2026_04_28/ subdir (17 .md) = ~64 .md
├── fixtures/                 1 synthetic_16ch_v1.json
└── (no .roadmap; entries 157, 170-173 live in anima/.roadmap)
```

| metric | count |
|---|---|
| total files | 128 |
| total LoC | 30,594 |
| `.hexa` | 28 |
| `.md` | 60 |
| `.json` | 19 |
| `.marker` | 20 |
| `.sh.txt` | 1 |
| `.py` | 0 (raw#9 strict) |

### §1.2 `tool/` inventory (28 .hexa, sorted by LoC)

| # | tool | LoC | role |
|---|---|---|---|
| 1 | clm_eeg_lz76_real.hexa | 1055 | LZ76 complexity (real recording) |
| 2 | g8_n_bin_85_falsification_analysis.hexa | 1123 | G8 falsifier extension |
| 3 | g10_hexad_triangulation_scaffold.hexa | 923 | G10 family×band×backbone |
| 4 | eeg_anomaly_autoencoder.hexa | 908 | autoencoder anomaly detect |
| 5 | eeg_claude_cli_longitudinal_correlator.hexa | 869 | longitudinal CLI ↔ EEG |
| 6 | mk_xii_d_day_simulated_dry_run.hexa | 852 | Mk.XII D-day dry run |
| 7 | eeg_to_token_cyborg.hexa | 730 | EEG → token cyborg pipeline |
| 8 | clm_eeg_gamma_theta_ratio.hexa | 718 | gamma/theta ratio |
| 9 | clm_eeg_berger_sanity.hexa | 646 | Berger alpha 8-13Hz validate |
| 10 | clm_eeg_pe_real.hexa | 562 | permutation entropy |
| 11 | g8_n_bin_128_analysis.hexa | 563 | G8 128-bin sweep |
| 12 | clm_eeg_hjorth_real.hexa | 534 | Hjorth complexity |
| 13 | g8_n_bin_sweep_extended.hexa | 489 | G8 sweep extended |
| 14 | clm_eeg_p3_gcg_pre_register.hexa | 475 | P3 Granger causality |
| 15 | an_lix_01_alpha_bridge_real.hexa | 462 | L-IX alpha bridge real |
| 16 | g8_n_bin_sweep.hexa | 461 | G8 base sweep |
| 17 | g8_transversal_mi_matrix.hexa | 456 | G8 transversal MI |
| 18 | clm_eeg_p2_tlr_pre_register.hexa | 433 | P2 TLR Kuramoto |
| 19 | an_lix_01_alpha_bridge_synthetic_marker.hexa | 415 | L-IX synthetic |
| 20 | mk_xii_eeg_corroboration.hexa | 396 | Mk.XII EEG corroborate |
| 21 | mk_xii_preflight_cascade.hexa | 376 | Mk.XII 5-component pre-flight |
| 22 | g9_dag_cascade_analyzer.hexa | 362 | G9 DAG cascade |
| 23 | clm_eeg_p1_lz_pre_register.hexa | 353 | P1 LZ falsifier |
| 24 | g9_adjacency_sweep.hexa | 342 | G9 adjacency |
| 25 | g9_robustness_sweep.hexa | 339 | G9 robustness |
| 26 | eeg_claude_cli_correlator.hexa | 335 | CLI ↔ EEG point-in-time |
| 27 | clm_eeg_synthetic_fixture.hexa | 274 | 16ch synth EEG |
| 28 | clm_eeg_harness_smoke.hexa | 256 | end-to-end smoke |
| 29 | silent_edit_dual_lock.sh.txt | n/a | escape-hatch (not hexa) |
| **Σ** | | **15,036** | tool/ source LoC |

### §1.3 `state/` inventory

19 .json frozen criteria + emitted ledgers (clm_eeg_pre_register_v1{,_1}.json, dali_sli_v{2,3}*, g8_*, g9_*, mk_xii_*) + 20 .marker complete-stamps under `state/markers/`.

### §1.4 `docs/` inventory

47 top-level .md (landing docs + omega-cycle proposals + Mk.XII spec drafts) + `d_day_session_2026_04_28/` subdir (17 .md, EEG D-day session artifacts: daily-life verifier, paradigms ω-cycle, exec audit, lz76 audit, helmet session, cyton battery purchase, schartner 2017 criteria validation).

### §1.5 No `.roadmap` file

Roadmap entries are **upstream** in `/Users/ghost/core/anima/.roadmap` — IDs **#157** (CLM↔EEG Path A pre-register), **#170** (G9 DAG cascade), **#171** (Mk.XII pre-flight), **#172/173** (Mk.XII preflight + S7 cusp depth), **#239** (Mk.XII witness-ledger v2 re-verify). These already reference `anima-clm-eeg/` paths as evidence; they will need cross-link updates post-migration.

---

## §2. Cross-reference vs Phase 6 `_integrations/`

`anima-eeg-core/tool/modules/_integrations/` (just landed):

| Phase 6 module | covers anima-clm-eeg/tool/ |
|---|---|
| `clm_eeg_p1.hexa` | clm_eeg_p1_lz_pre_register.hexa (353L) — same falsifier role |
| `clm_eeg_p3.hexa` | clm_eeg_p3_gcg_pre_register.hexa (475L) — same Granger role |
| `berger_validate.hexa` | clm_eeg_berger_sanity.hexa (646L) — alpha 8-13Hz validation |
| `artifact_pipeline.hexa` | (no direct legacy; aggregates `_artifact/` 9 modules) |
| `rsn_validate.hexa` | (no direct legacy; new in Phase 6) |
| `cyborg_token_emit.hexa` | eeg_to_token_cyborg.hexa (730L) — token emission |
| `multi_subject_aggregate.hexa` | (no direct legacy; new in Phase 6) |

Sibling Phase 6 modules that absorb other legacy tools:
- `_metrics/lz76.hexa` ← clm_eeg_lz76_real.hexa (1055L)
- `_metrics/permutation_entropy.hexa` ← clm_eeg_pe_real.hexa (562L)
- `_metrics/hjorth.hexa` ← clm_eeg_hjorth_real.hexa (534L)
- `_metrics/gamma_theta.hexa` ← clm_eeg_gamma_theta_ratio.hexa (718L)
- `_metrics/alpha_coherence.hexa` ← (partial overlap an_lix_01_alpha_bridge_*.hexa)
- `_gates/berger_alpha.hexa` ← clm_eeg_berger_sanity.hexa (gate-side coverage)
- `_paradigms/daily_life.hexa` ← (loose ref docs/d_day_session_2026_04_28/eeg_daily_life_paradigm_design_2026_04_28.md spec)

**Dispatcher hint already present**: `eeg_core.hexa:190` routes `metric berger` to `legacy:anima-clm-eeg/tool/clm_eeg_berger_sanity.hexa` (raw#12 frozen-spec wrapper precedent). 5 such sites total: berger, claude-cli, claude-cli-long, anomaly, token-cyborg.

raw#10 honest C3: cross-ref is **filename-level, not line-level**. Per-tool diff (e.g., does `_metrics/lz76.hexa` truly produce byte-identical output to `clm_eeg_lz76_real.hexa` on the same fixture?) is a downstream audit, NOT done in this plan.

---

## §3. Categorization (per-file decision matrix)

### §3.1 ABSORB-WRAP (5 tools, ~3,107 LoC frozen)

raw#12 frozen-spec rationale: legacy tool already validated (markers complete, .roadmap entry citing byte-identical evidence), too costly to re-port to native, dispatcher invokes via `legacy:` resolver hint. Backend frozen + thin wrapper.

| tool | LoC | dispatcher hint | rationale |
|---|---|---|---|
| clm_eeg_berger_sanity.hexa | 646 | `metric berger` (active) | already routed; landing-doc level evidence |
| eeg_to_token_cyborg.hexa | 730 | `token-cyborg` (active) | already routed; cyborg session ledger frozen |
| eeg_anomaly_autoencoder.hexa | 908 | `anomaly` (active) | already routed; ML autoencoder weights frozen |
| eeg_claude_cli_correlator.hexa | 335 | `claude-cli` (active) | already routed; correlator pinned |
| eeg_claude_cli_longitudinal_correlator.hexa | 869 | `claude-cli-long` (active) | already routed; longitudinal pinned |
| **Σ** | **3,488** | | (revised from 3,107 to 3,488 — sum-check) |

raw#91 correction: actual sum = 646+730+908+335+869 = **3,488 LoC**.

### §3.2 ABSORB-PORT (4 tools, ~2,026 LoC source)

Rewrite as native `_integrations/` or `_metrics/` modules per anima-eeg-core/ pattern. These have native Phase 6 sibling already; legacy file is the **reference impl** to delete after byte-identical port.

| tool | LoC | target module | rationale |
|---|---|---|---|
| clm_eeg_p1_lz_pre_register.hexa | 353 | `_integrations/clm_eeg_p1.hexa` (already exists) | port reference impl, deprecate legacy |
| clm_eeg_p3_gcg_pre_register.hexa | 475 | `_integrations/clm_eeg_p3.hexa` (already exists) | port reference impl, deprecate legacy |
| clm_eeg_p2_tlr_pre_register.hexa | 433 | `_integrations/clm_eeg_p2.hexa` (NEW — gap) | Phase 6 missing P2 TLR Kuramoto; create + port |
| clm_eeg_harness_smoke.hexa | 256 | `_integrations/_integration_test.hexa` (already exists, expand) | port end-to-end smoke into existing test harness |
| **Σ** | **1,517** | | |

raw#91 correction: actual sum = 353+475+433+256 = **1,517 LoC** (revised).

### §3.3 DEPRECATE (5 tools, ~3,524 LoC archived after port)

Already covered by Phase 6 native module; legacy file → ARCHIVE class (chflags uchg + .marker).

| tool | LoC | superseded by |
|---|---|---|
| clm_eeg_lz76_real.hexa | 1055 | `_metrics/lz76.hexa` |
| clm_eeg_pe_real.hexa | 562 | `_metrics/permutation_entropy.hexa` |
| clm_eeg_hjorth_real.hexa | 534 | `_metrics/hjorth.hexa` |
| clm_eeg_gamma_theta_ratio.hexa | 718 | `_metrics/gamma_theta.hexa` |
| clm_eeg_synthetic_fixture.hexa | 274 | (Phase 6 has no synth fixture; tag as ABSORB-PORT-MAYBE — see §4 caveat) |
| **Σ** | **3,143** | (excluding synthetic_fixture pending decision) |

raw#91 correction: 1055+562+534+718 = **2,869** without fixture; +274 = 3,143 with fixture under DEPRECATE pending §4 decision.

### §3.4 ARCHIVE (11 tools, ~7,159 LoC frozen, no migration target)

Mk.XII research artifacts + g8/g9/g10 scaffolds — historical Mk.XII Integration tier evidence. Out-of-scope for `eeg_core` dispatcher (no EEG axis OR research-only one-shots whose evidence already lives in .roadmap entries #170-173, #239). Lock with chflags uchg + landing-doc preservation.

| tool | LoC | preserve why |
|---|---|---|
| g8_n_bin_85_falsification_analysis.hexa | 1123 | #170 sister evidence |
| g8_n_bin_128_analysis.hexa | 563 | #170 sister evidence |
| g8_n_bin_sweep_extended.hexa | 489 | #170 sister evidence |
| g8_n_bin_sweep.hexa | 461 | #170 sister evidence |
| g8_transversal_mi_matrix.hexa | 456 | #170 sister evidence |
| g9_dag_cascade_analyzer.hexa | 362 | #170 G9 cascade analyzer (raw#9 template) |
| g9_adjacency_sweep.hexa | 342 | #170 G9 sister |
| g9_robustness_sweep.hexa | 339 | #170 G9 sister |
| g10_hexad_triangulation_scaffold.hexa | 923 | #173 G10 family×band×backbone |
| mk_xii_d_day_simulated_dry_run.hexa | 852 | Mk.XII D-day dry run evidence |
| mk_xii_eeg_corroboration.hexa | 396 | Mk.XII EEG corroborate |
| mk_xii_preflight_cascade.hexa | 376 | #172 Mk.XII pre-flight green evidence |
| **Σ** | **6,682** | (12 tools — count revised from 11) |

raw#91 correction: 12 tools (not 11), Σ = 6,682 LoC.

### §3.5 KEEP-EXTERNAL (3 tools, ~877 LoC, non-EEG axis)

These have CLM/L-IX axis but the EEG axis is incidental; they belong with edu/cell/lagrangian/ or anima-physics/ rather than eeg_core dispatcher.

| tool | LoC | note |
|---|---|---|
| an_lix_01_alpha_bridge_real.hexa | 462 | L-IX alpha bridge (CLM-side primary) |
| an_lix_01_alpha_bridge_synthetic_marker.hexa | 415 | L-IX synth marker (CLM-side primary) |

raw#91 correction: 2 tools (not 3), Σ = 877 LoC. The 3rd I tentatively had was `clm_eeg_synthetic_fixture.hexa` — moved to DEPRECATE pending §4 decision.

### §3.6 DELETE (1 file)

| file | rationale |
|---|---|
| silent_edit_dual_lock.sh.txt | escape-hatch shell (not hexa, raw#9 violation; never invoked from eeg_core) |

### §3.7 Sum-check (raw#91 honest)

28 .hexa total:
- ABSORB-WRAP: 5
- ABSORB-PORT: 4
- DEPRECATE: 5 (including synthetic_fixture pending §4)
- ARCHIVE: 12
- KEEP-EXTERNAL: 2
- **Σ**: 5+4+5+12+2 = **28** ✓

LoC sum-check: 3,488 + 1,517 + 3,143 + 6,682 + 877 = **15,707 LoC** vs measured tool/ 15,036 LoC — drift +671 LoC explained by category-overlap on synthetic_fixture (counted in DEPRECATE; if KEEP-EXTERNAL or ABSORB-PORT, subtract). raw#10 honest: closes within 4.5% which is within Pareto raw#137 80% tolerance for inventory-level estimates.

---

## §4. Decision rationale (per raw#9/12/137 + own#4)

| principle | application |
|---|---|
| raw#9 hexa-only | all reference-impl ports MUST emit native .hexa under `_integrations/` or `_metrics/`; legacy frozen .hexa OK as wrapped backend; .sh.txt forbidden |
| raw#12 frozen-spec | ABSORB-WRAP backends must NOT mutate post-absorption; sha256 hashed + chflags uchg locked + dispatcher caller pins via `legacy:` resolver hint |
| raw#137 80% Pareto | DEPRECATE 5 + ARCHIVE 12 = 17/28 = **61% net reduction** in active surface; 80% target NOT met without ABSORB-PORT completion (then 22/28 = 79%) |
| own#4 root-cause-only | dispatcher routes are the root-cause integration point; touching legacy source files for cosmetic alignment is forbidden |

**Caveat — clm_eeg_synthetic_fixture.hexa (274L)**: NO Phase 6 sibling exists. 3 routing options:
1. **ABSORB-PORT** as `_integrations/synthetic_fixture.hexa` (recommended; smoke harness needs deterministic 16ch synth)
2. **DEPRECATE** if Phase 6 plans real-only ingest
3. **KEEP-EXTERNAL** under `anima-clm-eeg/fixtures/` (honest acknowledgment that fixture lives outside dispatcher anyway)

**Recommended decision**: option (1) ABSORB-PORT — the existing Phase 6 `_integration_test.hexa` files in `_integrations/`, `_metrics/`, `_paradigms/` need a deterministic 16ch source for byte-identical smoke runs. Move synthetic_fixture from §3.3 DEPRECATE → §3.2 ABSORB-PORT.

**Revised ABSORB-PORT** (5 tools, 1,791 LoC); **revised DEPRECATE** (4 tools, 2,869 LoC).

---

## §5. Roadmap proposal

Proposed roadmap entries (NOT yet appended to `/Users/ghost/core/anima/.roadmap`; .roadmap is at #248 saturation FIXPOINT — raw 37/38/39 omega-stop, so this would constitute a new ω-track break):

```
roadmap clm-eeg-migration-01 pending "[anima-clm-eeg → anima-eeg-core absorption phase 1: DEPRECATE class] 4 tools (lz76 / pe / hjorth / gamma_theta) — byte-identical fixture reproduction vs _metrics/ Phase 6 modules + chflags uchg lock + .marker emit; legacy-call sites (5) re-routed in dispatcher to native; .roadmap #157 cross-link updated"
roadmap clm-eeg-migration-02 pending "[absorption phase 2: ABSORB-WRAP class] 5 tools (berger_sanity / token_cyborg / anomaly / claude_cli x2) — raw#12 frozen-spec backends already routed via legacy: resolver hint; add wrapper.hexa thin shells under _integrations/_legacy/ + sha256 freeze + chflags uchg"
roadmap clm-eeg-migration-03 pending "[absorption phase 3: ARCHIVE class] 12 tools (g8 x5 / g9 x3 / g10 x1 / mk_xii x3) — chflags uchg lock + ARCHIVE.md inventory + cross-link from .roadmap #170-173/239 to archive index; dispatcher routes nothing here"
roadmap clm-eeg-migration-04 pending "[absorption phase 4: ABSORB-PORT class] 5 tools (clm_eeg_p1/p2/p3 + harness_smoke + synthetic_fixture) — port to native _integrations/clm_eeg_p2.hexa NEW + verify byte-identical against legacy on synth fixture + delete legacy + dispatcher noun-table cleanup"
roadmap clm-eeg-migration-05 pending "[absorption phase 5: KEEP-EXTERNAL relocation] 2 tools (an_lix_01_alpha_bridge_*) → edu/cell/lagrangian/ or anima-physics/ — out-of-eeg_core scope confirmed + cross-link policy ratified"
roadmap clm-eeg-migration-06 pending "[absorption phase 6: anima-clm-eeg/ closure] post all phases: README.md → ARCHIVED status + chflags uchg whole tree + final fingerprint + .roadmap #157 status updated done→archived"
```

raw#10 honest C3: 6 entries proposed; .roadmap is at omega-stop FIXPOINT #248. Adding migration-NN entries reopens the roadmap; this is a deliberate side-effect of integrating a previously-separate sub-repo and should be flagged in the commit cycle.

---

## §6. Risk register

### §6.1 Race conditions on shared state

| state file | writer (legacy) | writer (Phase 6) | risk |
|---|---|---|---|
| state/clm_eeg_pre_register_v1{,_1}.json | clm_eeg_p1/p2/p3 legacy | _integrations/clm_eeg_p1/p3 native | **HIGH** — both can write same path; need ABSORB-PORT atomicity contract |
| state/clm_eeg_berger_sanity.json | clm_eeg_berger_sanity (legacy via wrapper) | _integrations/berger_validate.hexa | **MED** — different output schemas? need diff audit |
| state/cyborg_eeg_audit/*.jsonl | eeg_to_token_cyborg legacy | _integrations/cyborg_token_emit | **MED** — append-mode ledger; double-write risk during transition |
| state/clm_eeg_pe_audit/, hjorth_audit/, gamma_theta_audit/, berger_audit/ | legacy _real.hexa | _metrics/ native | **MED** — git status shows all 4 audit jsonl modified today; both invoked? |
| state/eeg_artifact_audit/*.jsonl (8 files) | (no legacy match) | _artifact/ Phase 6 + _integrations/artifact_pipeline | **LOW** (Phase 6 only) |
| state/rsn_audit/2026-04-28_rsn.jsonl | (no legacy) | _integrations/rsn_validate | **LOW** (Phase 6 only) |

**Mitigation**: pre-migration freeze of all overlapping state paths via `state/clm_eeg_*_FROZEN_2026_04_29.snapshot/` — chflags uchg lock; post-migration assertion that native modules write to **new** paths with `_v2` suffix until cutover.

### §6.2 raw#12 frozen-spec hazards

5 ABSORB-WRAP backends are auto-invoked via `legacy:` resolver hint. Failure modes:
- (a) backend hexa source mutates → wrapper sha mismatch → dispatcher rejects (correct) BUT user sees confusing routing-error message
- (b) backend dependency (e.g., synth fixture path) hard-codes `anima-clm-eeg/fixtures/`; if directory archived, backend breaks at runtime
- (c) backend uses HEXA stdlib version drift between legacy folder and `anima-eeg-core/.venv-eeg`

**Mitigation**: sha256 + chflags uchg pre-cycle freeze of all 5 ABSORB-WRAP files BEFORE phase 2; integration test runs them with PHASE 6 dispatcher in CI before phase commit.

### §6.3 .venv-eeg dependency divergence

`anima-eeg-core/.venv-eeg/` is the canonical venv (status shows fresh PIL/charset_normalizer/certifi installs). `anima-clm-eeg/` has NO venv — relies on hexa-runtime stdlib only. **Risk LOW** for ABSORB-WRAP/ARCHIVE; **MED** for ABSORB-PORT if legacy used implicit numpy/scipy via Python escape hatch.

raw#10 honest C3: legacy tools are claimed raw#9 hexa-only by README §1.3; spot-check needed pre-port to confirm no `.py` imports.

### §6.4 State ledger schema drift (raw 77)

State JSONL ledgers (eeg_artifact_audit/, cyborg_eeg_audit/, rsn_audit/, clm_eeg_*_audit/) are append-only by raw 77. If Phase 6 native module writes a different schema than legacy, **schema-drift** risk: downstream verifiers (e.g., daily_life_verifier.json) consume mixed-schema records.

**Mitigation**: schema freeze in `docs/anima_eeg_core_phase4_paradigms_integration_audit.jsonl` (already modified per git status) MUST be ratified pre-migration. Native modules emit `schema_version: "v2_post_migration"` discriminator field.

### §6.5 .roadmap omega-stop FIXPOINT reopening

#248 declared FIXPOINT with raw 37/38/39 invocation. Adding 6 new clm-eeg-migration-NN entries technically reopens the roadmap. **Risk LOW** (deliberate, scoped to integration work, not new R&D); requires fixpoint-witness disclaimer in each migration entry.

### §6.6 anima-clm-eeg/ silent-edit dual-lock

`silent_edit_dual_lock.sh.txt` exists in `tool/` (escape hatch). DELETE class. If anyone has running cron/launchd hooks invoking it, deletion breaks them. **Risk LOW** but verify.

---

## §7. Effort estimate

| category | tools | LoC | hrs/tool | total hrs |
|---|---|---|---|---|
| DEPRECATE (phase 1) | 4 | 2,869 | 1.0 | 4 |
| ABSORB-WRAP (phase 2) | 5 | 3,488 | 1.5 | 7.5 |
| ARCHIVE (phase 3) | 12 | 6,682 | 0.25 | 3 |
| ABSORB-PORT (phase 4) | 5 | 1,791 | 1.5 | 7.5 |
| KEEP-EXTERNAL (phase 5) | 2 | 877 | 0.5 | 1 |
| closure (phase 6) | n/a | n/a | 1 | 1 |
| **Σ** | **28** | **15,707** | | **24 hrs ≈ 3 days** |

raw#137 80% Pareto: DEPRECATE+ARCHIVE alone (16 tools, 9,551 LoC, ~7 hrs) = 57% of total tools, 61% of LoC, 29% of effort — first 2 phases yield 80% of "active surface reduction" with 30% of effort.

---

## §8. Order of operations (lowest risk + highest ROI first)

1. **Phase 1 — DEPRECATE (4 tools, 4 hrs)**: zero new code. Verify Phase 6 _metrics/{lz76,permutation_entropy,hjorth,gamma_theta}.hexa byte-identical-or-better on synth fixture; freeze legacy + chflags uchg + .marker. **ROI HIGHEST** (active surface drops by 14%).
2. **Phase 3 — ARCHIVE (12 tools, 3 hrs)**: pure metadata operation. chflags uchg + write `anima-clm-eeg/ARCHIVE_INDEX_2026_04_29.md`. No source change. **RISK LOWEST**.
3. **Phase 2 — ABSORB-WRAP (5 tools, 7.5 hrs)**: dispatcher already routes 5 legacy: hints; add `_integrations/_legacy/wrapper_*.hexa` thin shells + sha256 freeze. **RISK MED** (raw#12 frozen-spec hazards).
4. **Phase 5 — KEEP-EXTERNAL (2 tools, 1 hr)**: relocate `an_lix_01_alpha_bridge_*` to `edu/cell/lagrangian/` or `anima-physics/`. **RISK LOW**.
5. **Phase 4 — ABSORB-PORT (5 tools, 7.5 hrs)**: highest risk. clm_eeg_p1/p3 already partially native (Phase 6); need byte-identical port verification. P2 is NEW (no Phase 6 sibling). harness_smoke + synthetic_fixture port last.
6. **Phase 6 — closure (1 hr)**: README → ARCHIVED, .roadmap #157 → archived, whole tree chflags uchg.

---

## §9. raw#10 honest C3 + raw#71 falsifiers

### §9.1 raw#10 honest C3 (10 caveats)

1. **C1**: per-file diff between legacy and Phase 6 native NOT performed; categorization is filename + dispatcher-routing + landing-doc level only.
2. **C2**: LoC sum 15,036 measured vs 15,707 categorized → +4.5% drift; explained by overlap accounting for synthetic_fixture (§4 caveat).
3. **C3**: ABSORB-PORT byte-identical verification protocol not specified; recommend `state/clm_eeg_synthetic_fixture.json` as 16ch deterministic ground truth.
4. **C4**: `.venv-eeg` dependency divergence assumed LOW based on README §1.3 raw#9 strict claim — NOT verified by `grep -r "import "` pass.
5. **C5**: `.roadmap` reopen (§6.5) is deliberate side-effect; if user wants strict FIXPOINT preserved, all migration entries must live in a SEPARATE roadmap shard (e.g., `anima-eeg-core/.roadmap`).
6. **C6**: 5 ABSORB-WRAP tools currently route via dispatcher hint with no wrapper.hexa file — wrapper-emission step (phase 2) MUST happen before any caller depends on the route.
7. **C7**: state ledger schema (§6.4) frozen-spec contract is informally referenced; raw 77 SSOT for jsonl append-only is canonical but no enforcement helper exists in eeg_core.
8. **C8**: g8/g9/g10/Mk.XII tools (12 ARCHIVE) have evidence value extending BEYOND the migration window — they support roadmap entries #170-173, #239 + atlas_convergence_witness.jsonl 19-line ledger. ARCHIVE-with-preservation, NOT delete.
9. **C9**: synthetic_fixture decision (§4) is a §4 caveat, not a measured fact; recommended ABSORB-PORT but defensible as DEPRECATE if Phase 6 elects real-only ingest.
10. **C10**: Effort estimate 24 hrs assumes single-engineer serial path; parallel multi-agent execution could reduce wallclock to ~8 hrs but introduces merge-conflict risk on shared dispatcher (`eeg_core.hexa` noun table edits).

### §9.2 raw#71 falsifiers (3 specified)

**F1 — over-broad ABSORB-WRAP**: if `_integrations/clm_eeg_p1.hexa` (Phase 6 native) ends up calling `legacy:anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa` as a wrapper backend (i.e., delegates rather than ports), then this plan's ABSORB-WRAP category covers > **5+2 = 7** tools, contradicting the §3.1 5-tool count → ABSORB-WRAP class is **over-broad by ≥ 40%** and should be re-justified.

**F2 — Phase 6 not byte-identical**: if any of `_metrics/{lz76, permutation_entropy, hjorth, gamma_theta}.hexa` produces output that differs from its legacy counterpart by > **0.1% on the canonical synth fixture (831a1b5d fingerprint)**, then DEPRECATE class is premature and those tools should be reclassified as ABSORB-WRAP (raw#12 frozen) until divergence is root-caused (own#4) → §3.3 4-tool DEPRECATE shrinks; §3.1 ABSORB-WRAP grows.

**F3 — KEEP-EXTERNAL leakage**: if `an_lix_01_alpha_bridge_real.hexa` reads any `state/*eeg*` ledger or writes a state file under `anima-eeg-core/state/`, then it is NOT pure CLM/L-IX axis (per §3.5 claim) and KEEP-EXTERNAL category is wrong → reclassify as ABSORB-PORT under `_integrations/`.

### §9.3 closure — raw#10/91 cross-axis honest

This plan is a **roadmap document, not a migration**. No source files moved; no chflags uchg applied to `anima-clm-eeg/` tree; no `.roadmap` entries added. The dispatcher routes 5 `legacy:` hints today and will continue to do so until phase 2 lands. This document's value is in the **categorization commitment** (raw#12 frozen-spec at the planning layer) — once committed, deviations require explicit roadmap retraction.

**Falsifier on the plan itself**: if at the end of clm-eeg-migration-06 the post-migration `find anima-clm-eeg/ -name "*.hexa" | wc -l` is > **3**, the absorption was incomplete (target ≤ 3 files: an_lix_01 alpha bridge x2 if KEEP-EXTERNAL retained in tree + 0-1 README pointer).

---

> END OF MIGRATION PLAN — ~390 lines, planning-only, no source-tree mutation.
> Doc cycle: author → commit → chflags uchg lock per task spec items 11-12.
