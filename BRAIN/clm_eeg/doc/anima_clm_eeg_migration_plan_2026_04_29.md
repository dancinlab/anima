# anima-clm-eeg → anima-eeg-core Migration Plan

> **scope**: planning-only roadmap document for absorbing `anima-clm-eeg/` legacy R&D tools into the canonical `anima-eeg-core/` dispatcher. Code migration is a SEPARATE ω-cycle (this doc is the spec; not the implementation).
> **author**: Claude Opus 4.7 (1M ctx) — sub-agent, read-only inventory pass
> **date**: 2026-04-29
> **target absorption window**: post Phase 6 _integrations/ landing (commits 02ac714c3, 86465c662, 4cd8e62da, 6cf5ded72) → planned ω-cycle clm-eeg-migration-{01..NN}

---

## §0. Executive summary


The dispatcher already **soft-routes** to legacy paths via `legacy:anima-clm-eeg/tool/...` strings (5 sites: `berger`, `claude-cli`, `claude-cli-long`, `anomaly`, `token-cyborg`), so the migration is **already partially staged**. This plan formalizes the remaining absorption.

**Categorization summary** (28 hexa tools + 1 .sh.txt):
- **ABSORB-PORT** (rewrite native eeg-core hexa): 4 tools (~2,026 LoC source ported)
- **DEPRECATE** (superseded by Phase 6 _integrations/): 5 tools (~1,991 LoC archived)
- **ARCHIVE** (Mk.XII research artifacts, out-of-EEG-axis): 11 tools (~7,159 LoC frozen)
- **KEEP-EXTERNAL** (CLM-only / non-EEG): 3 tools (~1,213 LoC unchanged)
- **DELETE** (deprecated escape-hatch): 1 .sh.txt

**Estimated effort**: ~24 engineering hours (3 working days) split across 4 ω-cycles.



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



---

## §3. Categorization (per-file decision matrix)

### §3.1 ABSORB-WRAP (5 tools, ~3,107 LoC frozen)


| tool | LoC | dispatcher hint | rationale |
|---|---|---|---|
| clm_eeg_berger_sanity.hexa | 646 | `metric berger` (active) | already routed; landing-doc level evidence |
| eeg_to_token_cyborg.hexa | 730 | `token-cyborg` (active) | already routed; cyborg session ledger frozen |
| eeg_anomaly_autoencoder.hexa | 908 | `anomaly` (active) | already routed; ML autoencoder weights frozen |
| eeg_claude_cli_correlator.hexa | 335 | `claude-cli` (active) | already routed; correlator pinned |
| eeg_claude_cli_longitudinal_correlator.hexa | 869 | `claude-cli-long` (active) | already routed; longitudinal pinned |
| **Σ** | **3,488** | | (revised from 3,107 to 3,488 — sum-check) |


### §3.2 ABSORB-PORT (4 tools, ~2,026 LoC source)

Rewrite as native `_integrations/` or `_metrics/` modules per anima-eeg-core/ pattern. These have native Phase 6 sibling already; legacy file is the **reference impl** to delete after byte-identical port.

| tool | LoC | target module | rationale |
|---|---|---|---|
| clm_eeg_p1_lz_pre_register.hexa | 353 | `_integrations/clm_eeg_p1.hexa` (already exists) | port reference impl, deprecate legacy |
| clm_eeg_p3_gcg_pre_register.hexa | 475 | `_integrations/clm_eeg_p3.hexa` (already exists) | port reference impl, deprecate legacy |
| clm_eeg_p2_tlr_pre_register.hexa | 433 | `_integrations/clm_eeg_p2.hexa` (NEW — gap) | Phase 6 missing P2 TLR Kuramoto; create + port |
| clm_eeg_harness_smoke.hexa | 256 | `_integrations/_integration_test.hexa` (already exists, expand) | port end-to-end smoke into existing test harness |
| **Σ** | **1,517** | | |


### §3.3 DEPRECATE (5 tools, ~3,524 LoC archived after port)

> **NOTE 2026-05-01 (audit `867392918` reframe)**: 본 §3.3 의 원래 의미("legacy file 삭제")는 **잘못된 전제** 위에 작성되었음. 실제 `_metrics/{lz76, permutation_entropy, hjorth, gamma_theta}.hexa` 4 native 파일 모두 docstring 에 `"DECISION: WRAP (not PORT). Re-implementation deferred until Phase 5 port"` 명시. native (~250L) = thin wrapper, legacy (~534-1055L) = real numeric backend. native 는 `hexa.real run <LEGACY>` 형태로 legacy 를 runtime backend 로 호출 → **legacy file 물리 삭제 시 backend_rc=127 FAIL** 확정.
>
> 따라서 DEPRECATE class 의 의미를 다음과 같이 reframe:
>   - **(舊)** "legacy file 삭제" — physical removal, ARCHIVE class 와 합쳐 chflags uchg + .marker
>   - **(新)** "external entrypoint 격리 (이미 완료)" — legacy file 은 native wrapper 의 backend 로 잔존, 다만 (a) `anima-clm-eeg/` 외부 caller 가 직접 `legacy:anima-clm-eeg/tool/clm_eeg_*_real.hexa` 로 invoke 하는 경로 차단, (b) 모든 호출이 `tool/eeg_core.hexa metric <noun>` 단일 entrypoint 를 거치도록 dispatcher pinning. 이 격리는 Phase 6 dispatcher landing (commits 02ac714c3, 86465c662, 4cd8e62da, 6cf5ded72) 시점에 **이미 사실상 완료**됨.
>
> **legacy file physical delete 는 §11 Phase 5 port (신설) 이후로 deferred** — wrapper 가 진짜 native re-implementation 으로 교체되기 전에는 backend 의존이 살아있다.

Already covered by Phase 6 native module **as wrapper** (NOT port); legacy file = wrapper 의 runtime backend, **물리 삭제 금지**, dispatcher entrypoint 만 격리.

| tool | LoC | wrapper module (native) | reframe class |
|---|---|---|---|
| clm_eeg_lz76_real.hexa | 1055 | `_metrics/lz76.hexa` (~250L wrapper) | **WRAP-BACKEND** (entrypoint 격리 완료, file 보존) |
| clm_eeg_pe_real.hexa | 562 | `_metrics/permutation_entropy.hexa` (~250L wrapper) | **WRAP-BACKEND** (동) |
| clm_eeg_hjorth_real.hexa | 534 | `_metrics/hjorth.hexa` (~250L wrapper) | **WRAP-BACKEND** (동) |
| clm_eeg_gamma_theta_ratio.hexa | 718 | `_metrics/gamma_theta.hexa` (~250L wrapper) | **WRAP-BACKEND** (동) |
| clm_eeg_synthetic_fixture.hexa | 274 | Phase 6 `_integrations/synthetic_fixture.hexa` 존재 — A4 commit `7fc8c7e87` 사후 입증 | (§4 caveat 갱신 — §11 참조) |
| **Σ** | **3,143** | | (4 metric backends 격리 완료 + 1 fixture §11 재분류) |


### §3.4 ARCHIVE (11 tools, ~7,159 LoC frozen, no migration target)

> **NOTE 2026-05-01 (audit `867392918` + A4 `7fc8c7e87` cross-check)**: ARCHIVE class 는 §3.3 DEPRECATE 의 reframe 와 **동일 logic 적용 대상이 아님** — 이유는:
>   1. ARCHIVE 12 tools (g8 x5, g9 x3, g10 x1, mk_xii x3) 는 dispatcher 가 **호출하지 않는다** (legacy: resolver hint 부재). 따라서 wrapper-backend 의존성 없음.
>   2. native `_integrations/_metrics/` Phase 6 모듈 어떤 것도 g8/g9/g10/mk_xii 를 backend 로 invoke 하지 않는다 (filename grep + dispatcher noun-table cross-ref 양쪽으로 zero hit).
>   3. 즉 ARCHIVE 는 **순수 historical artifact** — entrypoint 격리가 아니라 **chflags uchg lock + ARCHIVE_INDEX.md** 가 본래 목표 그대로 유효.
>
>
> 따라서 ARCHIVE class 는 **변경 없음** — 다만 §6.6 + §11 cross-ref 추가만.

Mk.XII research artifacts + g8/g9/g10 scaffolds — historical Mk.XII Integration tier evidence. Out-of-scope for `eeg_core` dispatcher (no EEG axis OR research-only one-shots whose evidence already lives in .roadmap entries #170-173, #239). Lock with chflags uchg + landing-doc preservation.

| tool | LoC | preserve why |
|---|---|---|
| g8_n_bin_85_falsification_analysis.hexa | 1123 | #170 sister evidence |
| g8_n_bin_128_analysis.hexa | 563 | #170 sister evidence |
| g8_n_bin_sweep_extended.hexa | 489 | #170 sister evidence |
| g8_n_bin_sweep.hexa | 461 | #170 sister evidence |
| g8_transversal_mi_matrix.hexa | 456 | #170 sister evidence |
| g9_adjacency_sweep.hexa | 342 | #170 G9 sister |
| g9_robustness_sweep.hexa | 339 | #170 G9 sister |
| g10_hexad_triangulation_scaffold.hexa | 923 | #173 G10 family×band×backbone |
| mk_xii_d_day_simulated_dry_run.hexa | 852 | Mk.XII D-day dry run evidence |
| mk_xii_eeg_corroboration.hexa | 396 | Mk.XII EEG corroborate |
| mk_xii_preflight_cascade.hexa | 376 | #172 Mk.XII pre-flight green evidence |
| **Σ** | **6,682** | (12 tools — count revised from 11) |


### §3.5 KEEP-EXTERNAL (3 tools, ~877 LoC, non-EEG axis)

These have CLM/L-IX axis but the EEG axis is incidental; they belong with edu/cell/lagrangian/ or anima-physics/ rather than eeg_core dispatcher.

| tool | LoC | note |
|---|---|---|
| an_lix_01_alpha_bridge_real.hexa | 462 | L-IX alpha bridge (CLM-side primary) |
| an_lix_01_alpha_bridge_synthetic_marker.hexa | 415 | L-IX synth marker (CLM-side primary) |


### §3.6 DELETE (1 file)

| file | rationale |
|---|---|


28 .hexa total:
- ABSORB-WRAP: 5
- ABSORB-PORT: 4
- DEPRECATE: 5 (including synthetic_fixture pending §4)
- ARCHIVE: 12
- KEEP-EXTERNAL: 2
- **Σ**: 5+4+5+12+2 = **28** ✓


---


| principle | application |
|---|---|

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
roadmap clm-eeg-migration-03 pending "[absorption phase 3: ARCHIVE class] 12 tools (g8 x5 / g9 x3 / g10 x1 / mk_xii x3) — chflags uchg lock + ARCHIVE.md inventory + cross-link from .roadmap #170-173/239 to archive index; dispatcher routes nothing here"
roadmap clm-eeg-migration-04 pending "[absorption phase 4: ABSORB-PORT class] 5 tools (clm_eeg_p1/p2/p3 + harness_smoke + synthetic_fixture) — port to native _integrations/clm_eeg_p2.hexa NEW + verify byte-identical against legacy on synth fixture + delete legacy + dispatcher noun-table cleanup"
roadmap clm-eeg-migration-05 pending "[absorption phase 5: KEEP-EXTERNAL relocation] 2 tools (an_lix_01_alpha_bridge_*) → edu/cell/lagrangian/ or anima-physics/ — out-of-eeg_core scope confirmed + cross-link policy ratified"
roadmap clm-eeg-migration-06 pending "[absorption phase 6: anima-clm-eeg/ closure] post all phases: README.md → ARCHIVED status + chflags uchg whole tree + final fingerprint + .roadmap #157 status updated done→archived"
```


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


5 ABSORB-WRAP backends are auto-invoked via `legacy:` resolver hint. Failure modes:
- (a) backend hexa source mutates → wrapper sha mismatch → dispatcher rejects (correct) BUT user sees confusing routing-error message
- (b) backend dependency (e.g., synth fixture path) hard-codes `anima-clm-eeg/fixtures/`; if directory archived, backend breaks at runtime
- (c) backend uses HEXA stdlib version drift between legacy folder and `anima-eeg-core/.venv-eeg`

**Mitigation**: sha256 + chflags uchg pre-cycle freeze of all 5 ABSORB-WRAP files BEFORE phase 2; integration test runs them with PHASE 6 dispatcher in CI before phase commit.

### §6.3 .venv-eeg dependency divergence

`anima-eeg-core/.venv-eeg/` is the canonical venv (status shows fresh PIL/charset_normalizer/certifi installs). `anima-clm-eeg/` has NO venv — relies on hexa-runtime stdlib only. **Risk LOW** for ABSORB-WRAP/ARCHIVE; **MED** for ABSORB-PORT if legacy used implicit numpy/scipy via Python escape hatch.


### §6.4 State ledger schema drift (raw 77)

State JSONL ledgers (eeg_artifact_audit/, cyborg_eeg_audit/, rsn_audit/, clm_eeg_*_audit/) are append-only by raw 77. If Phase 6 native module writes a different schema than legacy, **schema-drift** risk: downstream verifiers (e.g., daily_life_verifier.json) consume mixed-schema records.

**Mitigation**: schema freeze in `docs/anima_eeg_core_phase4_paradigms_integration_audit.jsonl` (already modified per git status) MUST be ratified pre-migration. Native modules emit `schema_version: "v2_post_migration"` discriminator field.

### §6.5 .roadmap omega-stop FIXPOINT reopening

#248 declared FIXPOINT with raw 37/38/39 invocation. Adding 6 new clm-eeg-migration-NN entries technically reopens the roadmap. **Risk LOW** (deliberate, scoped to integration work, not new R&D); requires fixpoint-witness disclaimer in each migration entry.

### §6.6 anima-clm-eeg/ silent-edit dual-lock

`silent_edit_dual_lock.sh.txt` exists in `tool/` (escape hatch). DELETE class. If anyone has running cron/launchd hooks invoking it, deletion breaks them. **Risk LOW** but verify.

### §6.7 WRAP-not-PORT runtime backend dependency (2026-05-01 신규)

**Risk HIGH (신설)**: §3.3 reframe 에 따라 `_metrics/{lz76, permutation_entropy, hjorth, gamma_theta}.hexa` 4 native wrapper 가 `hexa.real run <LEGACY>` 형태로 legacy backend 를 invoke 한다. 실패 모드:
- (a) legacy file physical delete (e.g., 누군가 ARCHIVE class 와 혼동) → backend_rc=127, dispatcher 에서 `metric lz76` 호출 시 silent FAIL 또는 verbose route-error
- (b) legacy hexa runtime path (`hexa.real`) 가 stdlib 버전 drift 로 wrapper 의 `run` invocation 과 incompatible → wrapper sha 무결성 OK 인데도 backend 실행 실패
- (c) wrapper 의 `legacy:` resolver hint 가 hardcoded 절대 경로일 경우, anima-clm-eeg/ tree 이동 시 backend resolution 실패

**Mitigation**:
1. §11 Phase 5 port 완료 전까지 4 metric legacy file 모두에 chflags uchg + sha256 lock (A4 commit `7fc8c7e87` 의 5 legacy file 같은 정책 확장).
2. dispatcher CI 에 `metric {lz76, pe, hjorth, gamma_theta}` selftest mode 강제 — backend_rc != 0 시 dispatcher 자체가 noun-table 에서 routing 거부.


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


---

## §8. Order of operations (lowest risk + highest ROI first)

> **NOTE 2026-05-01 (audit `867392918` + A4 `7fc8c7e87` reframe)**: Phase 1 DEPRECATE 의 actual operation 은 "legacy file 삭제" 가 아니라 "external entrypoint 격리 (이미 완료) + WRAP-BACKEND lock" 이다. **Phase 1 ROI 재평가**: active surface 14% drop 주장은 무효 — file 은 그대로 잔존 (wrapper backend) 하고, dispatcher entrypoint pinning 만 효과. 진짜 "active surface drop" 은 §11 Phase 5 port 후에야 측정 가능.

2. **Phase 3 — ARCHIVE (12 tools, 3 hrs)**: pure metadata operation. chflags uchg + write `anima-clm-eeg/ARCHIVE_INDEX_2026_04_29.md` (또는 `ARCHIVE_INDEX_2026_05_01.md` — A4 `7fc8c7e87` 가 이미 5 legacy file 분 작성). No source change. **RISK LOWEST**.
4. **Phase 5 — KEEP-EXTERNAL (2 tools, 1 hr)**: relocate `an_lix_01_alpha_bridge_*` to `edu/cell/lagrangian/` or `anima-physics/`. **RISK LOW**.
5. **Phase 4 — ABSORB-PORT (5 tools, 7.5 hrs)**: highest risk. clm_eeg_p1/p3 already partially native (Phase 6); need byte-identical port verification. P2 is NEW (no Phase 6 sibling). harness_smoke + synthetic_fixture port last. 2026-05-01 NOTE: A4 `7fc8c7e87` 이 5 legacy 모두 uchg-locked 사후 입증 — physical mv 0 건, header-attestation 수준의 semantic-identical 만 확인됨 (kernel-equivalence proof 미수행).
6. **Phase 5b — Numeric port (4 metric backends + 5 integrations, ~22 hrs)** [신설, §11 참조]: §3.3 4 metric backend (lz76/pe/hjorth/gamma_theta, ~1,650 LoC numeric core) 를 진짜 native re-implementation 으로 교체 + canonical fixture cross-validation harness. 이 phase 까지 완료해야 §3.3 가 진짜 DEPRECATE (legacy file physical delete 가능) 가 된다.
7. **Phase 6 — closure (1 hr)**: README → ARCHIVED, .roadmap #157 → archived, whole tree chflags uchg. **사전 조건**: Phase 5b 완료 (4 metric backend 에 대한 진짜 port 가 끝나야 클로저 가능).

---



1. **C1**: per-file diff between legacy and Phase 6 native NOT performed; categorization is filename + dispatcher-routing + landing-doc level only.
2. **C2**: LoC sum 15,036 measured vs 15,707 categorized → +4.5% drift; explained by overlap accounting for synthetic_fixture (§4 caveat).
3. **C3**: ABSORB-PORT byte-identical verification protocol not specified; recommend `state/clm_eeg_synthetic_fixture.json` as 16ch deterministic ground truth.
5. **C5**: `.roadmap` reopen (§6.5) is deliberate side-effect; if user wants strict FIXPOINT preserved, all migration entries must live in a SEPARATE roadmap shard (e.g., `anima-eeg-core/.roadmap`).
6. **C6**: 5 ABSORB-WRAP tools currently route via dispatcher hint with no wrapper.hexa file — wrapper-emission step (phase 2) MUST happen before any caller depends on the route.
7. **C7**: state ledger schema (§6.4) frozen-spec contract is informally referenced; raw 77 SSOT for jsonl append-only is canonical but no enforcement helper exists in eeg_core.
8. **C8**: g8/g9/g10/Mk.XII tools (12 ARCHIVE) have evidence value extending BEYOND the migration window — they support roadmap entries #170-173, #239 + atlas_convergence_witness.jsonl 19-line ledger. ARCHIVE-with-preservation, NOT delete.
9. **C9**: synthetic_fixture decision (§4) is a §4 caveat, not a measured fact; recommended ABSORB-PORT but defensible as DEPRECATE if Phase 6 elects real-only ingest.
10. **C10**: Effort estimate 24 hrs assumes single-engineer serial path; parallel multi-agent execution could reduce wallclock to ~8 hrs but introduces merge-conflict risk on shared dispatcher (`eeg_core.hexa` noun table edits).


**F1 — over-broad ABSORB-WRAP**: if `_integrations/clm_eeg_p1.hexa` (Phase 6 native) ends up calling `legacy:anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa` as a wrapper backend (i.e., delegates rather than ports), then this plan's ABSORB-WRAP category covers > **5+2 = 7** tools, contradicting the §3.1 5-tool count → ABSORB-WRAP class is **over-broad by ≥ 40%** and should be re-justified.


**F3 — KEEP-EXTERNAL leakage**: if `an_lix_01_alpha_bridge_real.hexa` reads any `state/*eeg*` ledger or writes a state file under `anima-eeg-core/state/`, then it is NOT pure CLM/L-IX axis (per §3.5 claim) and KEEP-EXTERNAL category is wrong → reclassify as ABSORB-PORT under `_integrations/`.



**Falsifier on the plan itself**: if at the end of clm-eeg-migration-06 the post-migration `find anima-clm-eeg/ -name "*.hexa" | wc -l` is > **3**, the absorption was incomplete (target ≤ 3 files: an_lix_01 alpha bridge x2 if KEEP-EXTERNAL retained in tree + 0-1 README pointer).

> **NOTE 2026-05-01 (post-audit reframe)**: 위 falsifier 는 "post-migration `*.hexa` ≤ 3" 을 가정하지만, audit `867392918` 발견에 따라 4 metric backend (lz76/pe/hjorth/gamma_theta) 가 **§11 Phase 5 numeric port 완료 전까지 잔존 필수**. 따라서 실제 falsifier 임계값은 **post-Phase-5b 시점에서만** ≤ 3 적용 — 그 이전 단계 (Phase 1~4 완료) 에서는 ≤ **3 + 4 metric backend = 7** 가 새 임계값.

---


> **본 plan 은 audit `867392918` 이전 작성됨 (2026-04-29).** §10 은 그 이후 cross-axis 발견을 inline 에 묻지 않고 ledger 형태로 누적 기록.

### §10.1 갱신 entry

| date | source | finding | impacted §§ | reframe summary |
|---|---|---|---|---|
| 2026-04-29 | original draft | 28 .hexa categorization (5/4/5/12/2/1) | §§3.1-3.7 | 초안 commit (categorization commitment) |
| 2026-05-01 | audit `867392918` | 4 native `_metrics/*.hexa` 모두 docstring `"WRAP (not PORT). Re-implementation deferred until Phase 5 port"` 명시 | §3.3, §6.2, §6.7, §8, §9.3, §11 | DEPRECATE class → WRAP-BACKEND class 로 reframe; legacy file physical delete 는 §11 Phase 5 까지 deferred |


- (b) 4 metric pair 의 docstring marker 는 docstring-level 사실 — runtime backend 호출 자체를 byte-level 로 검증하지 않았다 (e.g., `legacy:` resolver 가 진짜 어떤 entry point 를 invoke 하는지 trace 미수행).
- (c) §3.4 ARCHIVE 12 tool 에 대한 "dispatcher 가 호출하지 않는다" 주장은 grep 기반 — runtime-trace 기반 음성 증명 부재.

---

## §11. Phase 5 port spec (신설 — 2026-05-01)

### §11.1 motivation

audit `867392918` 가 4 native `_metrics/*.hexa` (lz76 / permutation_entropy / hjorth / gamma_theta) 가 thin wrapper (~250L) 이고 진짜 numeric backend 는 legacy `clm_eeg_*_real.hexa` (~534-1055L, 합계 ~2,869L) 라는 사실을 사후 입증함. wrapper 의 `"WRAP (not PORT). Re-implementation deferred until Phase 5 port"` docstring marker 는 **본 §11 의 phase 명시적 reference**.

### §11.2 scope (4 짝, 1,650 LoC numeric core 추정)

본 phase 는 4 metric pair 의 numeric core 를 native hexa 로 진짜 이식.

| pair | legacy LoC | wrapper LoC | numeric core 추정 LoC | dependency |
|---|---|---|---|---|
| lz76: legacy `clm_eeg_lz76_real.hexa` → native `_metrics/lz76.hexa` | 1055 | ~250 | ~750 (Lempel-Ziv 1976 chunked, ASCII window) | mmap+ASCII hexa-stdlib |
| permutation_entropy: legacy `clm_eeg_pe_real.hexa` → native `_metrics/permutation_entropy.hexa` | 562 | ~250 | ~280 (Bandt-Pompe ordinal pattern) | log/sort hexa-stdlib |
| hjorth: legacy `clm_eeg_hjorth_real.hexa` → native `_metrics/hjorth.hexa` | 534 | ~250 | ~250 (activity/mobility/complexity) | 1차/2차 미분 hexa-stdlib |
| gamma_theta: legacy `clm_eeg_gamma_theta_ratio.hexa` → native `_metrics/gamma_theta.hexa` | 718 | ~250 | ~370 (FFT band-power 4-8/30-100 Hz) | FFT/welch hexa-stdlib |
| **Σ** | **2,869** | **~1,000** | **~1,650** | |


### §11.3 port acceptance criteria

각 pair 별 다음 4 조건 모두 만족시 "진짜 PORT" 로 인정 (wrapper docstring `"WRAP (not PORT)"` marker 제거 가능):

1. **C-numeric**: native re-impl 이 legacy 호출 없이 standalone numeric 결과 emit. `hexa.real run <LEGACY>` invocation 0건 (grep 음성 증명).
4. **C-rc-clean**: dispatcher CI 에서 legacy file 을 일시적으로 rename (`*.hexa.bak`) 후 `metric <noun>` selftest 가 PASS — backend_rc 부재 환경에서도 native 단독 실행 가능.

### §11.4 canonical fixture cross-validation harness


- (a) canonical synth fixture load (16ch deterministic, fingerprint frozen post-audit-867392918 cross-check)
- (b) native re-impl invoke + result vector emit
- (c) legacy backend invoke (Phase 5 cutover 전까지는 wrapper 가 invoke 하던 그 backend 그대로) + result vector emit
- (d) element-wise diff: `max(abs(native_i − legacy_i) / abs(legacy_i)) < 1e-3`
- (e) ledger emit: `state/clm_eeg_phase5_port_xvalidate/<date>_<noun>.jsonl` (raw 77 append-only)


### §11.5 effort + ordering

| pair | port 추정 | xvalidate harness | 합계 |
|---|---|---|---|
| hjorth | 2 hr (numeric core 가장 단순) | 0.5 hr | 2.5 hr |
| permutation_entropy | 3 hr | 0.5 hr | 3.5 hr |
| gamma_theta | 4 hr (FFT band power) | 0.5 hr | 4.5 hr |
| lz76 | 8 hr (chunked + ASCII window 가장 복잡) | 1 hr | 9 hr |
| 합계 | **17 hr** | **2.5 hr** | **19.5 hr** ≈ **2.5 days** |

ordering: 단순한 것부터 (hjorth → pe → gamma_theta → lz76) — lz76 가 마지막 (P1 LZ OOM mitigation 이력 commit `e94936e1` 참조).


- **F-port-01**: Phase 5 port 후 native re-impl 의 `hexa.real run <LEGACY>` invocation 이 grep 으로 1건 이상 검출 → port 미완.
- **F-port-03**: legacy file 을 dispatcher CI 에서 rename 후 selftest 시 backend_rc=127 발생 pair 가 1건이라도 있으면 port 미완 — wrapper 가 여전히 legacy 호출.

### §11.7 Phase 5 완료 후 §3.3 실효화

§11 4 pair 모두 C-numeric/C-fixture/C-falsifier/C-rc-clean 통과 후에야:

- §3.3 가 진짜 DEPRECATE class 로 효력 발휘 (legacy file physical delete 가능)
- §6.7 risk (WRAP-not-PORT runtime backend dependency) 해소
- §9.3 falsifier 의 `*.hexa ≤ 3` 임계값이 그대로 적용 가능
- 4 legacy metric file (~2,869 LoC) 가 chflags uchg + ARCHIVE 또는 hard-delete 로 결정 가능

---

> END OF MIGRATION PLAN — original 2026-04-29 draft + 2026-05-01 audit `867392918`/`7fc8c7e87` reframe NOTE inline + §10 ledger + §11 Phase 5 port spec 신설.
