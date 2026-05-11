# anima repo mk1 + .own dual-SSOT EOL audit (2026-05-04)

**status**: spec / inventory only — READ-ONLY (no chflags / no git mutation / no delete)
**scope**: `/Users/ghost/core/anima` mk1 `.raw*` + `.own` artifacts removal impact
**audit_ts**: 2026-05-04T18:55:00Z
**owner**: BG-β (parallel with BG-α hive / BG-γ sisters)

---

## §0 TL;DR

| metric | count |
| --- | --- |
| mk1 root files/dirs (`.raw*`, `raw_archive/`) | 5 (1 file + 4 dirs) |
| `.own` declarations (own 1..own 13) | 13 |
| own-1 protected `.py` files in active source | **0** (all PRE-PURGED — only backup remains) |
| `state/raw*` dirs | 2 (`raw1_lock_audit/` 124K, `raw_136_compliance_scan/` 16K) |
| `tool/raw*` + `tool/h_last_raw*` | 5 (raw15_token_leak_validator + raw15_post_bg_audit + raw_audit_drill_integration + h_last_raw_rotate + h_last_raw_regen_r5.bash) |
| `tool/anima_own3_*` + `anima_raw_own_*` + `anima_ready_raw9_*` | 8 |
| `docs/raw*` + `docs/own*` files | 16 |
| total uchg-locked files in repo | 834 |
| uchg files mk1/own related | **19** (2.3%) |
| uchg files unrelated (EEG/CLM/etc) | 815 (out of scope) |
| raw#N references (raw#9/10/15/37/71/91 across `.hexa`/`.md`/`.json`/`.bash`/`.txt`) | 1764 |

**Top 3 delete blockers**:
1. **19 uchg-locked files** require chflags noschg unlock ceremony (Phase 2a-anima)
2. **1764 raw#N citations** become stale (informational; runtime hexa unaffected)
3. **`.own` is mk2 SSOT, NOT mk1.raw** — must NOT be deleted (memory note misleading)

**leak_guard hook impact**: **DECOUPLED** — hook lives in `~/.hive/`, anima repo `.raw-ref` deletion has NO runtime effect.

---

## §1 mk1 + .own file tree

### Root level (depth 1)
```
/Users/ghost/core/anima/
├── .raw-ref                       1327B  2026-04-26  (pin to hive .raw)
├── .own                          63595B  2026-05-04  (mk2 anima-local SSOT — 13 own N)
├── .raw-audit/                       6 files, 21K
├── .raw-audit-shadow/                2 files, 14K
├── .raw-exemptions/                  4 files, 14K
└── raw_archive/                  108K, 7 files (recent migration archive)
    └── 2026-05-04T/
        ├── docs/  (2 files: anima_dot_own_namespace_spec*.md)
        └── tool/  (5 files: roadmap_*.hexa)
```

### .raw-audit/ contents
```
.raw-audit/active_redteam_l1.log               833B   2026-04-26
.raw-audit/adversarial_bench.log              5029B   2026-05-04 (recently active)
.raw-audit/phase_progression.log              1060B   2026-04-21
.raw-audit/problem_solving_protocol.log       1706B   2026-04-21
.raw-audit/true_closure.log                   7720B   2026-04-26
.raw-audit/unified_eval.log                   5770B   2026-04-26
```

### .raw-exemptions/ contents
```
.raw-exemptions/raw_6.list      1195B
.raw-exemptions/raw_7.list      8805B
.raw-exemptions/raw_8.list      1257B
.raw-exemptions/README.md       3034B
```

### state/ raw / own directories
```
state/raw1_lock_audit/                       5 jsonl files, 124K, mtime 2026-04-28
state/raw_136_compliance_scan/               2 files, 16K, mtime 2026-04-28 (BOTH uchg-locked)
state/own3_jamba_throughput_validation/      (subdir; own 3 sigma-tau validation)
state/own3_e_golden_moe_validation/          (subdir)
state/own3_d_law70_validation/               (subdir)
state/own3_de_apply_ready_package.json       (single file)
state/own3_de_wording_revision_verifier.json (single file)
```

### tool/ raw + own files (13 hexa + 1 bash)
```
tool/raw15_token_leak_validator.hexa
tool/raw15_post_bg_audit.hexa
tool/raw_audit_drill_integration.hexa            [uchg]
tool/h_last_raw_rotate.hexa                      [uchg]
tool/h_last_raw_regen_r5.bash
tool/anima_raw_own_tree_report.hexa              [uchg]
tool/anima_ready_raw9_policy_proposer.hexa       [uchg]
tool/anima_own3_d_law70_measure.hexa             [uchg]
tool/anima_own3_de_apply_ready_package.hexa      [uchg]
tool/anima_own3_de_wording_revision_verifier.hexa [uchg]
tool/ps_3_raw_revise.hexa                        [uchg]
tool/anima_unknown_4_repos_deep_audit.hexa       [uchg]
tool/anima_unknown_5_repos_audit.hexa            [uchg]
tool/anima_holographic_ib_ksg_validate.hexa     (mk2 hexa-port replacement; KEEP)
```

### docs/ raw + own files (16)
```
docs/raw_15_residual_leak_spec_2026_05_01.md
docs/raw_audit_backfill_20260421.md
docs/raw_audit_drill_integration_spec.md
docs/raw95_compliance_audit_omega_cycle_20260427_landing.md
docs/raw95_audit_ledger_schema.md                [uchg]
docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md  [uchg, raw95 cite]
docs/own1-raw100-archive-2026-04-26.md          (own 1 verbose closure)
docs/own2_implementation_gap_audit_20260426.md
docs/own3_d_e_wording_revision_proposal_20260427.md
docs/own3_cross_check_4axis_evidence_20260426.md
docs/own3_own4_grep_evidence_2026-04-28.txt     [uchg]
docs/anima_dot_own_namespace_spec_2026_05_03.md
docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md
docs/drill_supplement_tmp/iter_65_rules_l4_lockdown.{err,json}
docs/download-models.md (raw cited)
```

---

## §2 chflags uchg inventory

### Total: 834 uchg-locked files (much higher than the 96 stated in memory)

By top-level dir:
| dir | count | mk1/own related |
| --- | --- | --- |
| tool/ | 499 | 10 |
| state/ | 106 | 5 |
| anima-eeg-core/ | 50 | 0 |
| docs/ | 43 | 3 |
| anima-clm-eeg/ | 33 | 0 |
| design/ | 30 | 0 |
| anima-eeg/ | 30 | 0 |
| anima-hci-research/ | 12 | 0 |
| anima-cpgd-research/ | 12 | 0 |
| scripts/ | 4 | 0 |
| anima-physics/ | 4 | 0 |
| anima-serve/ | 3 | 0 |
| edu/ | 2 | 0 |
| n6/ | 1 | 1 |
| consciousness/ | 1 | 0 |
| config/ | 1 | 0 |
| bench/ | 1 | 0 |
| ready/.git/hooks | 1 | 0 |
| **TOTAL** | **834** | **19** |

### mk1/own related uchg list (19 files — Phase 2a unlock targets)
```
n6/atlas.append.session-2026-04-28-raw-135-136-pattern-7c-self-enforcement.n6
docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md
docs/own3_own4_grep_evidence_2026-04-28.txt
docs/raw95_audit_ledger_schema.md
state/f5_cycle1_ablation_grid/grid_raw.json   ⚠ (filename = raw measurement output, NOT mk1.raw — exclude from delete)
state/audit/daily_life_recorder_own4_fix.jsonl
state/audit/daily_life_recorder_own4_fix_annotation.jsonl
state/raw_136_compliance_scan/session_2026-04-28T0515Z.txt
state/raw_136_compliance_scan/verdict.json
tool/anima_unknown_4_repos_deep_audit.hexa
tool/anima_ready_raw9_policy_proposer.hexa
tool/anima_own3_d_law70_measure.hexa
tool/anima_own3_de_apply_ready_package.hexa
tool/anima_unknown_5_repos_audit.hexa
tool/anima_raw_own_tree_report.hexa
tool/h_last_raw_rotate.hexa
tool/raw_audit_drill_integration.hexa
tool/ps_3_raw_revise.hexa
tool/anima_own3_de_wording_revision_verifier.hexa
```

### Note on uchg root-level mk1 files
`.raw-ref`, `.own`, `.raw-audit/*`, `raw_archive/*` are **NOT uchg-locked** — direct git rm OK without chflags ceremony for these.

---

## §3 .own own #N protection map

`.own` is a **single 63595-byte file** with mk2 frontmatter (`schema_version: project/own/v1`, `mk: 2`, `last_updated: 2026-05-02`), NOT a directory. It contains 13 `own N` declarations:

| own N | status | slug | base raw | mk1-coupled? |
| --- | --- | --- | --- | --- |
| own 1 | live | anima-hexa-only-scope | raw 9 | YES — extends raw#9 with grandfather list |
| own 2 | live | production-consciousness-triad | (independent) | NO |
| own 3 | live | sigma-tau-three-phase-acceleration | (independent) | NO |
| own 4 | live | training-resource-root-cause-only | raw 27 cross-ref | weakly |
| own 5 | live | anima-research-completeness-no-cap | (independent) | NO |
| own 6 | live | gpu-dispatch-no-restriction-no-approval | (independent) | NO |
| own 7 | new | heredoc-arg-max-content-size-guard | (independent) | NO |
| own 8 | new | HXC-content-class-topology-declaration | raw 142 D1 mirror | YES — mirrors hive raw#142 |
| own 9 | new | try-and-revert-orthogonality-wrapper | raw 142 D2/D3 mirror | YES |
| own 10 | new | algorithm-placement-axis-declaration | raw 142 D5 mirror | YES |
| own 11 | live | parallel-loop-mandate | (independent) | NO |
| own 12 | new | raw-own-tree-ASCII-reporting | (meta) | YES (operates on raw/own tree) |
| own 13 | new | user-facing-response-friendliness | hive raw 165 mirror | YES |

### own 1 grandfather list (raw#9 hexa-only scope opt-out)
```
opt-out ready/                                                           (1431 files, .gitignore'd)
opt-out .claude/                                                         (1045 files, vendor)
opt-out .raw-audit/                                                      (raw 77 separate format)
opt-out node_modules/ build/ dist/ checkpoints/ data/                    (vendor + build)
opt-out tool/active_redteam_dEF_proto.py                                 (.gitignore'd Python)
opt-out tool/active_redteam_prototype.py                                 (.gitignore'd Python)
opt-out tool/anima_holographic_ib_ksg_validate_prod.py                   (raw 9 explicit relaxation, F3 KSG MI scipy)
```

### Protected .py file existence verification (live tree)
```
tool/active_redteam_dEF_proto.py                            NOT FOUND
tool/active_redteam_prototype.py                            NOT FOUND
tool/anima_holographic_ib_ksg_validate_prod.py              NOT FOUND
```

Found copies (archive only):
```
state/py_to_hexa_audit_2026_05_03/backup/anima_holographic_ib_ksg_validate_prod.py
tool/__pycache__/anima_holographic_ib_ksg_validate_prod.cpython-314.pyc
```

Hexa replacement: `tool/anima_holographic_ib_ksg_validate.hexa` (already migrated). Verdict: **own 1 grandfather list is already FULLY VACATED**. Deleting `.own` (or own 1 declaration) creates ZERO new raw#9 violations because the protected files no longer exist in active source.

### Critical: KEEP .own
`.own` is the **mk2 anima-local L1 SSOT** (parallel to hive `.own`). It is NOT a mk1 artifact. Memory note "own #1 system grandfathering 4 .py files" refers to own 1 declaration body content, not the .own file itself. **Recommendation: KEEP `.own`** — only delete mk1 `.raw*` artifacts.

---

## §4 raw#N reference grep

### Total: 1764 references across `.hexa` / `.md` / `.json` / `.bash` / `.txt`

Top 20 most-referenced files (raw#9 / raw#10 / raw#15 only, in `.hexa`/`.md`/`.json`):
| count | file |
| --- | --- |
| 38 | docs/anima_math_raw_axiom_dag_20260425.md |
| 32 | docs/anima_clm_eeg_migration_plan_2026_04_29.md |
| 30 | anima-eeg-core/tool/modules/_metrics/hjorth_native.hexa |
| 25 | anima-eeg-core/tool/modules/_metrics/pe_native.hexa |
| 22 | state/clm_v4_tokenizer_caller_migration_spec_2026_05_04/spec.md |
| 22 | anima-eeg-core/tool/modules/_metrics/gamma_theta_native.hexa |
| 20 | tool/anima_ready_raw9_policy_proposer.hexa |
| 20 | docs/own1-raw100-archive-2026-04-26.md |
| 19 | state/proof_carrying/anima_roadmap.json |
| 19 | state/docs_pending_audit_2026_05_04/audit_plan.md |
| 18 | docs/cp2_interim_public_minimum_path_recommendation_2026_04_29.md |
| 18 | design/cp2_beta_eeg_shortcut_omega_cycle_2026_04_28.md |
| 18 | anima-eeg/docs/anima_eeg_unified_cli_daemon_spec_2026_05_04.md |
| 18 | anima-eeg/collect.hexa |
| 18 | anima-clm-eeg/docs/c2_floor_revision_spec_2026_05_01.md |
| 17 | docs/mk_xii_n1_honest_fail_followup_spec_2026_05_01.md |
| 17 | docs/cp2_interim_public_release_investigation_2026_04_29.md |
| 17 | anima-eeg/protocols/cyton_only_250hz.hexa |
| 16 | docs/preprint_anima_mk_xi_v10_paradigm_v11_stack_20260426.md |
| 16 | docs/commit_msg_drift_audit_2026_04_29.md |

### Classification
- **Documentation citations** (docs/*.md, design/*.md): historical refs — informational only, no jurisdiction loss
- **Runtime hexa source** (anima-eeg-core/tool/modules/_metrics/*.hexa, anima-eeg/*.hexa, anima-clm-eeg/*.hexa): raw#N in **comment headers only** — runtime semantics unaffected by mk1 deletion
- **State JSONs** (state/proof_carrying/*, state/clm_v4_tokenizer_*): pre-registered hypothesis ledgers citing raw#10/#12 — historical immutable

Verdict: post-delete grep will show ~1764 stale citations; recommend mass-rewrite citation `raw#N` → `mk2 raw N` (or strip) as separate Phase 3 cleanup, not a delete blocker.

---

## §5 .raw-ref pin status

```
ref 1 live "hive canonical (anima)"
  source github.com/dancinlab/hive
  branch main
  path .raw
  pinned-hash 2c67adde9f9068274db8f034f135a9c6e57503bb1e4395a112cd50a0666099ce
  checked-at 2026-04-26T11:30:36Z
  hive-commit-ref e3fd4865108d9af98485e7baa06eaaa14a1b8f33
  prev-pinned-hash c6c23e08bbcf762688404584ae32380256b5ce96c418612e3920c0d3cbd5f37d
  prev-checked-at 2026-04-26T10:09:18Z
  prev-hive-commit-ref 82b06154fd89cd4ca7981a2ed9d2021c2fcc6604
```

Pin is **8 days stale** (hive HEAD has advanced since 2026-04-26).

### Decision recommendation: **DELETE** (do not redirect)
- mk2 SSOT is `.own` + `.guide` pair (not `.raw`)
- Redirecting `.raw-ref` to mk2 would invent a non-existent concept
- Pin already obsolete pre-EOL → delete is net-positive
- Archive copy at `state/dual_ssot_eol_archive/anima_mk1_2026_05_04.tar.gz` for migration trail

---

## §6 anima-specific artifacts

### state/raw1_lock_audit/ — 124K, 5 files
Last activity: 2026-04-28 22:51
```
2026-04-28_batch.jsonl                                        4697B
2026-04-28_clm_eeg_lz76_retraction.jsonl                      2023B
2026-04-28_clm_eeg_p1_lz_pre_register_mirror_retraction.jsonl 2247B
2026-04-28_followup.jsonl                                     4878B
2026-04-28_scope_wide_batch.jsonl                            99122B
```
raw#1 = chflags uchg L0 lock baseline; audit log for unlock/relock events. **Delete OK** — historical only.

### state/raw_136_compliance_scan/ — 16K, 2 files (both uchg-locked)
Last activity: 2026-04-28 05:15
```
session_2026-04-28T0515Z.txt   890B   [uchg]
verdict.json                  1185B   [uchg]
```
raw#136 = compliance scan rule (jurisdiction unclear from name). **Delete OK** after chflags unlock.

### raw_archive/ — 108K, 7 files (RECENT — 2026-05-04 13:29 mtime)
This is a **recently created** archive (today!) holding migrated files. Contents:
```
raw_archive/2026-05-04T/docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md
raw_archive/2026-05-04T/docs/anima_dot_own_namespace_spec_2026_05_03.md
raw_archive/2026-05-04T/tool/roadmap_lint.hexa
raw_archive/2026-05-04T/tool/roadmap_compile.hexa
raw_archive/2026-05-04T/tool/roadmap_render.hexa
raw_archive/2026-05-04T/tool/roadmap_op.hexa
raw_archive/2026-05-04T/tool/_roadmap_repo_resolver.hexa
```
**CAUTION**: this is an **active/recent** archive directory used by ongoing migration work. Verify before delete — may contain the *only* copies of these archived files. If files exist elsewhere (mk2 location), safe to delete. Otherwise treat as in-progress migration buffer.

### .raw-audit/ — 21K, 6 logs
Most recent: `adversarial_bench.log` (2026-05-04 16:49 — TODAY active). Other 5 logs: 2026-04-21 to 2026-04-26.
**Delete OK** — historical audit trail; archive recommended.

### .raw-audit-shadow/ + .raw-exemptions/ — 28K combined
Stale (mtime 2026-04-21 / 2026-04-26). **Delete OK**.

### h_last_raw_*.json — 45 files (FALSE POSITIVE — DO NOT DELETE)
P9 training/synthesis manifests:
```
state/h_last_raw_p[1-4]_TRAINED_r[3-14].json   (P9 training history per phase × seed)
state/h_last_raw_r7_optD_qwen14_synthesis_manifest.json
state/h_last_raw_rotate_result.json
state/an11b_*_run/h_last_raw_*.json            (per-run training history)
```
Filename `h_last_raw` = "history last raw output" (raw measurement, NOT mk1.raw). **MUST PRESERVE** — these are P9/AN11 training records, ω-cycle output state.

### state/markers/raw*.marker (~12 files) — also FALSE POSITIVE
e.g. `raw15_token_leak_validator_*.marker`, `raw_271_baseline_17_conformed.marker`. These are tool-output markers; safe to leave (informational only).

---

## §7 leak_guard hook impact

### Hook location
`~/.hive/scripts/leak_guard_pretool.bash` (NOT in anima repo)

### Anima dependency
- `docs/raw_15_residual_leak_spec_2026_05_01.md` — anima-local doc citing raw#15 personal-path-leak rule (mk1.raw 15)
- `tool/raw15_token_leak_validator.hexa` — anima-local validator (uchg-NOT-locked)
- `tool/raw15_post_bg_audit.hexa` — anima-local post-BG audit

### Runtime coupling
- Hook is **hardcoded** with personal-path patterns; does NOT read `.raw-ref` or any anima-side mk1 file at runtime
- Hook reads from `~/.hive/` only

### Verdict: **DECOUPLED**
- Anima `.raw-ref` / `.raw-audit/` / `raw_archive/` deletion: **NO runtime impact** on leak_guard
- Anima `tool/raw15_*.hexa` deletion: **NO runtime impact** (those are validators that complement hook, not call/from-call)
- Anima `docs/raw_15_residual_leak_spec_2026_05_01.md` deletion: **provenance citation breaks** (informational only)

### Recommendation
- Hook survives anima mk1 purge unchanged
- Optional: update hook header citation from "raw#15" to "personal-path-leak-rule" post-mk1-EOL (cosmetic, not blocking)

---

## §8 Recommended delete sequence

### Phase 2a-anima — chflags unlock (19 files)
```
chflags noschg \
  n6/atlas.append.session-2026-04-28-raw-135-136-pattern-7c-self-enforcement.n6 \
  docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md \
  docs/own3_own4_grep_evidence_2026-04-28.txt \
  docs/raw95_audit_ledger_schema.md \
  state/audit/daily_life_recorder_own4_fix.jsonl \
  state/audit/daily_life_recorder_own4_fix_annotation.jsonl \
  state/raw_136_compliance_scan/session_2026-04-28T0515Z.txt \
  state/raw_136_compliance_scan/verdict.json \
  tool/anima_unknown_4_repos_deep_audit.hexa \
  tool/anima_ready_raw9_policy_proposer.hexa \
  tool/anima_own3_d_law70_measure.hexa \
  tool/anima_own3_de_apply_ready_package.hexa \
  tool/anima_unknown_5_repos_audit.hexa \
  tool/anima_raw_own_tree_report.hexa \
  tool/h_last_raw_rotate.hexa \
  tool/raw_audit_drill_integration.hexa \
  tool/ps_3_raw_revise.hexa \
  tool/anima_own3_de_wording_revision_verifier.hexa
```
EXCLUDE: `state/f5_cycle1_ablation_grid/grid_raw.json` (filename false positive — keep uchg + keep file).

### Phase 2b-anima — archive
```
mkdir -p state/dual_ssot_eol_archive/
tar -czf state/dual_ssot_eol_archive/anima_mk1_2026_05_04.tar.gz \
  .raw-ref .raw-audit/ .raw-audit-shadow/ .raw-exemptions/ \
  raw_archive/ \
  state/raw1_lock_audit/ state/raw_136_compliance_scan/
```

### Phase 2c-anima — git rm root mk1
```
git rm -r .raw-ref .raw-audit/ .raw-audit-shadow/ .raw-exemptions/ raw_archive/
git rm -r state/raw1_lock_audit/ state/raw_136_compliance_scan/
```

### Phase 2d-anima — review tool/ raw + own3 hexa (per-file decision)
```
git rm tool/raw15_token_leak_validator.hexa     (mk1.raw 15 jurisdiction-out)
git rm tool/raw15_post_bg_audit.hexa            (mk1)
git rm tool/raw_audit_drill_integration.hexa   (mk1)
git rm tool/h_last_raw_rotate.hexa              (mk1.raw rotate)
git rm tool/h_last_raw_regen_r5.bash            (mk1)
git rm tool/anima_raw_own_tree_report.hexa      (mk1 namespace tree report)
git rm tool/anima_ready_raw9_policy_proposer.hexa (mk1.raw 9 jurisdiction)
git rm tool/ps_3_raw_revise.hexa                (mk1)
# own 3 measurements — KEEP (own 3 is mk2 declaration, not mk1):
#   tool/anima_own3_d_law70_measure.hexa
#   tool/anima_own3_de_apply_ready_package.hexa
#   tool/anima_own3_de_wording_revision_verifier.hexa
# unknown_repos audits — KEEP (cross-repo audit, mk2 useful):
#   tool/anima_unknown_4_repos_deep_audit.hexa
#   tool/anima_unknown_5_repos_audit.hexa
```

### Phase 2e-anima — KEEP .own
**DO NOT** delete `.own` — it IS the mk2 anima-local L1 SSOT.
Optional: rewrite own 1 body to remove obsolete grandfather list (.py files no longer exist).

### Phase 2f-anima — KEEP h_last_raw_*.json (P9 output, false positive)

### Phase 2g-anima — post-delete grep verify
```
find . -path ./.git -prune -o \( -name '.raw*' -o -name 'raw_archive' \) -print
# expect: zero matches
grep -rln 'raw#9\|raw#10\|raw#15' --include='*.hexa' --include='*.md' --include='*.json' .
# expect: ~1764 stale citation matches (informational only — Phase 3 mass-rewrite optional)
```

---

## §9 Falsifier set F-EOL-ANIMA-1..4

| ID | claim | falsifier |
| --- | --- | --- |
| F-EOL-ANIMA-1 | mk1 root files gone | `find . -maxdepth 1 \( -name '.raw*' -o -name 'raw_archive' \) -print` returns zero |
| F-EOL-ANIMA-2 | chflags unlock-set clean | `find . -flags uchg \| grep -E '(raw_136|raw1_lock|anima_own3_de|anima_unknown_[45]|anima_raw_own_tree|anima_ready_raw9|raw_audit_drill|h_last_raw_rotate|ps_3_raw_revise|own4_fix|raw95_audit|cp2_eta_cost|raw95_compliance)'` returns zero |
| F-EOL-ANIMA-3 | own 1 protected .py decision recorded | `state/dual_ssot_eol_archive/anima_mk1_2026_05_04.tar.gz` exists AND `state/py_to_hexa_audit_2026_05_03/backup/anima_holographic_ib_ksg_validate_prod.py` decision logged (delete OR archive elsewhere) |
| F-EOL-ANIMA-4 | .raw-ref pin archived (not redirected) | tar.gz contains `.raw-ref` AND `find . -name '.raw-ref'` returns zero AND no replacement `.raw-ref-mk2` created |

---

## §10 Honest C3 (≥5)

### C3-1: own 1 grandfather list is ALREADY VACATED
The 3 `.py` files protected by own 1 (`active_redteam_dEF_proto.py`, `active_redteam_prototype.py`, `anima_holographic_ib_ksg_validate_prod.py`) have **ALREADY been removed** from `tool/` active source. Only backup at `state/py_to_hexa_audit_2026_05_03/backup/anima_holographic_ib_ksg_validate_prod.py` and `__pycache__/.cpython-314.pyc` artifact remain. Hexa replacement `tool/anima_holographic_ib_ksg_validate.hexa` is in place. **Effective post-delete impact on raw#9 jurisdiction: ZERO** — no live `.py` to lose grandfathering.

### C3-2: 834 uchg-locked files, only 19 (2.3%) are mk1-related
The memory note "96/175 uchg locked files" is **stale** (current count is 834 across the repo). Of these, only 19 are mk1/own related. The remaining 815 are EEG/CLM/research immutability locks (anima-eeg, anima-clm-eeg, anima-eeg-core, design, etc.) — **MUST NOT be touched**. Naive `find . -flags uchg | xargs chflags noschg` would catastrophically unlock 815 unrelated files. Filename grep is **required** with allowlist (`raw_136|raw1_lock|anima_own3_de|anima_unknown_[45]|...`).

### C3-3: sister anima sub-directories vs separate repos — scope ambiguity
`anima-eeg/`, `anima-clm-eeg/`, `anima-eeg-core/`, `anima-physics/`, `anima-hci-research/`, `anima-cpgd-research/`, `anima-serve/` are subdirs WITHIN `/Users/ghost/core/anima/`, NOT separate git repos at this level. BG-γ scope clarification needed: are "sister repos" these subdirs OR independent `/Users/ghost/core/anima-*` dirs (if those exist outside this repo)? This audit treats subdirs as in-repo; their root-level mk1 artifacts: **none found** (no `.raw*` or `.own*` at subdir roots). 815 uchg files in these subdirs are unrelated.

### C3-4: filename `raw` collision — h_last_raw + state/markers + grid_raw false positives
- `state/h_last_raw_*.json` (45 files) = P9 training history (raw measurement output, NOT mk1.raw rule)
- `state/markers/raw_*.marker` (~12 files) = tool execution markers
- `state/f5_cycle1_ablation_grid/grid_raw.json` = ablation raw output, uchg-locked, **MUST NOT delete**
- `state/format_witness/2026-04-28_raw142_*.jsonl`, `_raw_137_*.jsonl`, etc. = format witness logs (raw#N citations, but the files are immutable witness records — keep)
- `state/n_substrate_*/raw_results.json`, `state/qmirror_*/raw_results/` = experimental raw output

Naive `find . -name '*raw*' -delete` would destroy 100+ legitimate output files. Whitelist required.

### C3-5: `.own` is mk2 SSOT — DO NOT DELETE
`.own` (single 63595-byte file with mk2 frontmatter `schema_version: project/own/v1`, `mk: 2`) IS the **mk2 anima-local L1 SSOT** — parallel to hive `.own`, sister to `.guide`. Deleting `.own` removes mk2 jurisdiction (wrong). The user instruction "delete mk1 .raw + .own" appears to confuse the namespace: mk1 had no `.own` (it had `.raw` + own-N rules embedded in `.raw`); mk2 has `.own` as a separate first-class SSOT file. **Recommendation: KEEP `.own`** — only delete mk1 `.raw*` + `raw_archive/` + `state/raw1_lock_audit/` + `state/raw_136_compliance_scan/` artifacts. Confirm with user before .own delete.

### C3-6: `.raw-ref` pin already 8 days stale
Current pin: hive commit `e3fd48651` checked at 2026-04-26T11:30:36Z. Today is 2026-05-04 — 8 days have passed and hive HEAD has advanced significantly (`raw_sync.hexa check` would update if run). Pin was already obsolete pre-EOL, so delete is **net-positive** (removes false-pinned reference no one is honoring).

### C3-7: leak_guard hook is decoupled from anima mk1
Hook lives at `~/.hive/scripts/leak_guard_pretool.bash`, hardcoded with personal-path regex patterns. It does NOT read anima `.raw-ref` or any anima `tool/raw15_*.hexa` at runtime. Anima mk1 deletion has **NO runtime impact** on leak_guard. The provenance link "raw#15 personal-path-leak-spec → leak_guard" breaks at the documentation level only.

### C3-8: raw_archive/ contains TODAY-mtime files (active migration buffer)
`raw_archive/2026-05-04T/` was created **today (2026-05-04 13:29)** holding 7 files migrated from somewhere. Verify these files are NOT the only copies before delete. Likely safe (migrated TO this archive as part of mk2 migration; canonical mk2 copies should exist), but explicit verification recommended.

---

## Summary

- mk1 footprint in anima: 5 root entries (1 file `.raw-ref` + 4 dirs) + 2 state subdirs + 13 tool/ files + 16 docs/ files + 19 uchg-locked files (subset of above)
- own 1 protected `.py` files: ALREADY VACATED (zero in active source) — no jurisdiction loss
- Critical: `.own` is mk2 SSOT (KEEP); only delete `.raw*` + `raw_archive/` + `state/raw1_*` + `state/raw_136_*`
- 1764 raw#N citations: stale post-delete but informational only (no runtime impact)
- leak_guard hook: decoupled, survives anima mk1 purge
- Phase 2 sequence: chflags unlock 19 → archive tar.gz → git rm 4 root + 2 state + 5-8 tool/ → KEEP .own + h_last_raw_*.json + format_witness raw* logs

deliverables:
- `state/dual_ssot_eol_audit_2026_05_04/anima_audit.md` (this file)
- `state/dual_ssot_eol_audit_2026_05_04/anima_inventory.json`
