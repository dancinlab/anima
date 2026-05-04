---
schema: hive/state/dual-ssot-eol-audit/v1
audit_ts: 2026-05-04T09:44:44Z
audit_target: /Users/ghost/core/hive
audit_scope: dual-SSOT mk1 EOL feasibility (READ-ONLY)
auditor: BG-α
parallel_audits:
  - BG-β: /Users/ghost/core/anima
  - BG-γ: sister repos
---

# Hive Repo Dual-SSOT EOL Audit (2026-05-04)

## TL;DR

- **Mk1 `.raw` is ALREADY GONE** from `/Users/ghost/core/hive/`. So are `.own`, `.ext`, `.guide` — no glob match. Local cleanup pre-dated this audit (rounds 1+2+remnant landed 2026-05-02 → archived to private repo `need-singularity/raw-archive` 2026-05-03 per `docs/raw_archive_repo_landed_2026_05_03.ai.md`).
- **Remaining mk1-era artifacts**: `.raw-audit` (uchg-locked, 814 lines = audit ledger of historical unlock/relock events), `.raw-english-violations.jsonl` (94 B), `.raw.modes.jsonl` (mk2 mode override file — keep), `.raw-exemptions/` (raw_6 + raw_7 path-prefix lists — referenced by 2+ tools), `raw_archive/2026-05-04T/` (today's pre-EOL backup).
- **Mk2 SSOT**: `.raw.mk2` carries **14 rules** (not 3 as spec text suggests). Domains: arch (1), ai-native (1), lint (1), resource (7), cli (4). All 14 rules have non-empty `derives-from` (~30 mk1.raw/own references), but only 2 rules (`arch.001`, `ai-native.001`) have non-empty `supersedes` (6 mk1 rules total).
- **Parity vs mk1**: 14/273 ≈ **5.1 %** rule count. Migration tool `tool/raw_mk1_to_mk2_migrator.hexa` is explicitly a STUB; modes-mapping migrator doesn't exist yet. Bulk migration is out of scope for this EOL turn.
- **Top blockers**: (1) sister-repo pin `anima/.raw-ref` still expects hive `.raw` at the canonical path, with a `pinned-hash` SHA-256 that is now provably unverifiable; (2) ≥80 hexa tools still string-reference `.raw` for runtime path resolution (e.g., `meta_lint.hexa`, `raw_taxonomy_lint.hexa`, `raw_mk2_inline_loader.hexa`) — they will hard-fail or warn on missing path; (3) `.raw-audit` is uchg-locked (chflags) and would require `chflags nouchg` before `git rm`.

## 1. mk1 SSOT inventory

### 1a. Files that DO NOT exist (already deleted)

| Path | Status |
|---|---|
| `/Users/ghost/core/hive/.raw` | absent — `ls` returns ENOENT, `wc -l` returns ENOENT |
| `/Users/ghost/core/hive/.own` | absent (zsh `no matches found`) |
| `/Users/ghost/core/hive/.ext` | absent |
| `/Users/ghost/core/hive/.guide` | absent (note: still uchg-flagged in audit ledger; may be elsewhere or ledger is historical) |

### 1b. Files that EXIST (mk1-adjacent, not the SSOT itself)

| Path | Size | Lines | chflags | Last mod |
|---|---|---|---|---|
| `.raw-audit` | 693 632 B | 814 | **uchg** | 2026-05-02 16:25 |
| `.raw-english-violations.jsonl` | 94 B | 1 | — | 2026-04-26 16:16 |
| `.raw.modes.jsonl` | 577 B | 6 | — | 2026-05-02 13:51 (mk2 override file — KEEP) |
| `.raw-exemptions/raw_6.list` | 786 B | — | — | 2026-04-26 12:49 |
| `.raw-exemptions/raw_7.list` | 7 484 B | — | — | 2026-04-26 19:42 |

### 1c. Today's backup snapshot (already produced)

`raw_archive/2026-05-04T/` — produced earlier today (2026-05-04 13:32) and contains:

```
.raw.mk2.bak                                42 486 B  (mk2 SSOT snapshot)
.raw.mk2.schema.yaml.bak                     8 540 B
.raw.modes.jsonl.bak                           577 B
.no-lineage-citation-recording-baseline.bak 33 179 B
.roadmap.format.bak / .lint_chain.bak / .raw_ssot.bak / .spec_apex.bak
bin/ config/ core/ docs/ modules/ packages/ spec/ state/ tool/    (full directory snapshots)
```

Note: this archive captures **mk2 + mk2 schema**, NOT mk1 `.raw`. The mk1 file itself was already removed in the 2026-05-02 cleanup; the historical content lives only in `need-singularity/raw-archive` (private GitHub repo).

## 2. mk2 SSOT current state

### 2a. Files

| Path | Size | Lines | chflags |
|---|---|---|---|
| `.raw.mk2` | 42 486 B | 100 | — |
| `.raw.mk2.schema.yaml` | 8 540 B | 130 | — |
| `.raw.modes.jsonl` | 577 B | 6 | — |

### 2b. Rule enumeration (14 rules)

```
arch.001         core-module-architecture-canonical-pattern    (supersedes mk1.raw270/271/272/273)
ai-native.001    ai-native-convention-foundation               (supersedes mk1.raw3/11)
lint.001         lint-canonical-tool-locations                 (supersedes [])
resource.001     host-pool-ssot-canonical                      (supersedes [])
resource.002     ssh-direct-no-docker-reroute                  (supersedes [])
resource.003     capacity-scoring-algorithm                    (supersedes [])
resource.004     backpressure-adaptive-limit                   (supersedes [])
resource.005     capability-probe-contract                     (supersedes [])
resource.006     dispatch-routing-tier-rr                      (supersedes [])
resource.009     oauth-slot-rotation-policy                    (supersedes [])
cli.001          kick-canonical-entry-singleton                (supersedes [])
cli.002          kick-meta-bundle-cross-cut-permission         (supersedes [])
cli.003          kick-roi-singleton-scoring-axis               (supersedes [])
cli.004          kick-roi-strategy-pluggable-registry          (supersedes [])
```

Parity = **14 / 273 ≈ 5.1 %** by rule count. By **semantic coverage** the parity is higher because each mk2 rule typically collapses 2–4 mk1 rules (arch.001 collapses 4, ai-native.001 collapses 2, resource family collapses ~10), so semantic parity is roughly 30–40 %, but ~60 % of mk1 rules have NO mk2 successor at all.

## 3. Tooling refs to mk1

### 3a. Files that READ mk1 path strings (sample)

| File | Lines | Ref type | Severity |
|---|---|---|---|
| `tool/meta_lint.hexa` | 47, 133, 142–144 | reads `env("HIVE")+"/.raw"`; explicitly errors `".raw not present"` | HIGH (hard-fail on missing) |
| `tool/raw_taxonomy_lint.hexa` | 18, 519–520 | const `RAW_PATH=".raw"`; emits "io-error: cannot read .raw or .own" | HIGH |
| `tool/raw_mk2_inline_loader.hexa` | 208 | `let _RAW_PATH = env("HIVE")+"/.raw"` | MEDIUM (this loader scans `.raw` for inline mk2 blocks; obsolete now that `.raw.mk2` is the JSONL SSOT) |
| `tool/raw_mode_op.hexa` | 26, 27, 477 | reads `_MK2_PATH() = env("HIVE")+"/.raw.mk2"` and `.raw.modes.jsonl` (project state) — **mk2-only reader, NOT mk1** | (clean) |
| `tool/raw13_pretooluse_governance_proposal_lint.hexa` | 13, 209, 214 | scans `.raw` for governance-proposal classification | MEDIUM |
| `tool/raw_addition_disposition_lint.hexa` | 97 | reads baseline `.raw-addition-disposition-baseline` | LOW (baseline file, not `.raw`) |
| `tool/feature_completion_test_lint.hexa` | 66, 70 | classifies `.raw` as behavior-change SSOT | MEDIUM |
| `tool/heavy_compute_mac_audit.hexa` | 98 | comment reference only | LOW |
| `tool/module_lock.hexa` | 62, 80, 282–283 | uses `/.raw` in lock-eligible-paths array | MEDIUM |
| `tool/hive_cli_canonical_lint.hexa` | 363, 388–389, 413 | example classifications of `chflags ... .raw` | LOW (test fixtures) |
| `tool/own_8_audit_log_lint.hexa` | (grep hit) | likely audit-ledger-related | LOW |
| `tool/canonical_path_health_lint.hexa` | (grep hit) | health check references | MEDIUM |
| `tool/canonical_term_disambiguation_lint.hexa` | (grep hit) | term canonicalization | LOW |
| `tool/stale_marker_auto_archive.hexa` | (grep hit) | marker archival | LOW |
| `tool/raw_paired_lint_atomicity_lint.hexa` | 172–202 | `/tmp/raw192_selftest/p1.raw` — **synthetic test fixtures**, NOT real `.raw` | NONE |
| `tool/raw241_strengthening_2026-04-30_lint.hexa` | 7 | comment | NONE |
| `tool/ext_lint.hexa` | 8 | comment | NONE |
| `tool/runtime_path_portability_lint.hexa` | 18, 168 | comments referencing `.raw` rule numbers | LOW |
| `tool/aot_native_build.hexa` | 16, 45 | comment | NONE |
| `tool/ad_hoc_signing_production_ban_lint.hexa` | 165 | error message text | LOW |

Total files matching `\.raw\b` across `tool/ + core/ + self/ + spec/`: **134** (many are comment-only or self-test fixtures; the runtime hard-failure set is ~6–10 tools).

### 3b. Files that WRITE mk1 (expected: 0)

`grep -rln '"/.raw"' ... | xargs grep 'write\|append\|exec.*"/.raw"'` returns 0 production-write paths to `.raw`. The only "writes" found are inside `tool/raw_paired_lint_atomicity_lint.hexa` self-tests writing to `/tmp/raw192_selftest/*.raw` (synthetic fixtures). Confirmed: no tool currently mutates the canonical `.raw` (consistent with chflags uchg lock when it existed).

### 3c. Migration tool

`tool/raw_mk1_to_mk2_migrator.hexa` — explicitly labeled `STUB (spec only)` in line 1–4. Reads single mk1 entry by N, emits skeleton mk2 candidate JSON, requires manual review. No bulk migration exists. The `raw_mk1_to_mk2_modes_migrator.hexa` (mode-field migrator) does NOT exist — only the spec doc `docs/raw_mk1_to_mk2_modes_mapping.ai.md` does.

### 3d. mk2 readers (ones to keep)

```
tool/raw_mk2_loader.hexa
tool/raw_mk2_cli.hexa
tool/raw_mk2_jsonl_cli.hexa
tool/raw_mode_op.hexa            (mk2 modes CLI)
tool/raw_mode_lint.hexa
tool/host_pool_mk2_loader.hexa
tool/kick_mk2_loader.hexa
tool/kick_roi_mk2_loader.hexa
tool/mk2_catalog_lint.hexa
core/raw_mode/{source,registry,router,raw_mode_main}.hexa
```

These do NOT depend on mk1 `.raw` paths and survive EOL cleanly.

## 4. chflags inventory

`find /Users/ghost/core/hive -flags uchg | wc -l` → **244** uchg-flagged paths (entire repo).

mk1-relevant uchg files (the only one in this audit's deletion scope):

| Path | Owner | Size | Reason |
|---|---|---|---|
| `/Users/ghost/core/hive/.raw-audit` | ghost | 693 632 B | unlock/relock ledger of past `.raw` edits — historical only |

Other uchg-flagged paths in `/Users/ghost/core/hive/` (NOT in deletion scope):

```
.meta                                                  (active SSOT)
.claude/                                               (settings)
core/test_source_info.hexa, core/resource/test_*.hexa  (frozen tests)
core/session/project.hexa
docs/{formats/marker_lifecycle.md, postmortem_*, handoff_*, *_landed_*.ai.md}   (frozen docs)
state/inbox_protocol_audit/audit.jsonl
state/markers/*.marker
state/autonomous_loop_audit/audit.jsonl
state/{remote_call_test, emergence_bench, auth_store_bench}/fixtures/*
archive/2026-04-30-ts-legacy-retired/*               (frozen archive)
```

**Critical**: deletion of `.raw-audit` requires `chflags nouchg /Users/ghost/core/hive/.raw-audit` first. Done as user `ghost` (no sudo needed).

## 5. mk2 → mk1 cross-link breakage risk

### 5a. `supersedes` field (post-deletion target validity)

| mk2 rule | supersedes | breakage risk |
|---|---|---|
| `arch.001` | mk1.raw270, mk1.raw271, mk1.raw272, mk1.raw273 | LOW — `mk1.rawN` strings are textual references to a SSOT that no longer exists locally; refs become **provenance-only** |
| `ai-native.001` | mk1.raw3, mk1.raw11 | LOW (same) |
| 12 other rules | `[]` | none |

### 5b. `derives-from` field

All 14 rules carry non-empty `derives-from`, totaling ~30 unique mk1 raw/own references:

```
mk1.raw3, mk1.raw9, mk1.raw11, mk1.raw36, mk1.raw40, mk1.raw42,
mk1.raw92, mk1.raw95, mk1.raw105, mk1.raw162, mk1.raw173, mk1.raw200,
mk1.raw240, mk1.raw261, mk1.raw262, mk1.raw269, mk1.raw270, mk1.raw271,
mk1.raw272, mk1.raw273, mk1.own5
```

These refs are **textual** (no resolver round-trip exists today). Breakage severity: **LOW** at runtime, **MEDIUM** at provenance audit (no canonical path to resolve `mk1.raw270`'s body text after `.raw` deletion → must consult private archive).

### 5c. Recommendation

Either:
- **Option A**: leave `derives-from`/`supersedes` strings as historical fingerprints (lightweight; current tooling does not resolve them).
- **Option B**: bulk-replace `mk1.rawN` → `archive:need-singularity/raw-archive#raw_N` (URL pointer to private archive) — explicit dead-end pointer; more honest, but mutates 14 mk2 entries.

Recommend **Option A** (minimal churn) with a 1-line note in `.raw.mk2` header pointing readers at `need-singularity/raw-archive` for historical resolution.

## 6. Migration completeness

Currently delivered:
- mk2 schema + 14 rules + loader + mode toggle CLI + mode lint dispatcher: **complete**.
- mk1→mk2 rule migrator: **STUB** (`tool/raw_mk1_to_mk2_migrator.hexa` line 1–4 says so explicitly).
- Modes-field migrator: **DOES NOT EXIST** (only spec doc `docs/raw_mk1_to_mk2_modes_mapping.ai.md` exists).

Coverage gap: ~250+ mk1 rules have NO mk2 successor entry. Per the mk1→mk2 mapping spec line 7–9, mk1 was the live canonical SSOT and mk2 carries a partial draft. Deleting mk1 NOW (which is what already happened on 2026-05-02) means those ~250 rules effectively vanished from the LIVE canonical layer.

Honest read: this is in tension with the mk1→mk2 mapping doc's stated policy "mk1 EOL is a separate Ω-cycle decision (after mk2 reaches lint coverage parity + sister-repo adoption)." The current state is **post-decision**: deletion happened before parity. The `raw_archive_repo_landed` doc explicitly framed this as cleanup of a backup pile, not as the canonical EOL act.

## 7. Recommended delete sequence

This audit's user-instructed scope: "dual-SSOT period 해지 모든 mk1 .raw .own 모든프로젝트에서 삭제." Since `.raw` and `.own` are already gone from hive, the residual cleanup is:

1. **Backup verification**: confirm `raw_archive/2026-05-04T/` contains everything wanted-to-keep. Optionally also verify private archive `need-singularity/raw-archive` clones cleanly (cross-check SHA).
2. **chflags unlock**: `chflags nouchg /Users/ghost/core/hive/.raw-audit` (1 file).
3. **Optional removal of mk1-era residuals**:
   - `.raw-audit` (814-line ledger of past edits — historical only; can be moved to private archive instead of deleted).
   - `.raw-english-violations.jsonl` (1-line stub).
   - `.raw-exemptions/raw_6.list`, `.raw-exemptions/raw_7.list` — **CAUTION**: still consumed by `tool/ai_native_scan.hexa` per the file's header comment. Do NOT delete without a tooling sweep + mk2 replacement.
4. **Tooling sweep** (HIGH priority, separate sub-cycle):
   - Migrate `tool/meta_lint.hexa`, `tool/raw_taxonomy_lint.hexa`, `tool/raw_mk2_inline_loader.hexa` away from `.raw` path constants.
   - Either retire `raw_mk2_inline_loader.hexa` (its premise — inline mk2 blocks inside `.raw` — is moot now that `.raw.mk2` is JSONL).
   - Update tools whose error messages still cite `.raw must always exist per raw 0 root-ssot` to cite mk2 instead.
5. **Sister repo pin update**: `/Users/ghost/core/anima/.raw-ref` (and any other sister repo) carries a `pinned-hash` for `hive/.raw`. With hive `.raw` gone, the pin is unverifiable. Either:
   - Retire the `.raw-ref` mechanism repo-wide (replace with `.raw.mk2-ref` if cross-pin is still desired).
   - Re-pin to `need-singularity/raw-archive#main` for archival pointer.
6. **mk2 dangling reference policy**: Choose Option A (do nothing) or Option B (bulk-replace `mk1.rawN` → `archive:...`) per §5c.
7. **Doc updates**:
   - Append note to `.raw.mk2` header that mk1 EOL completed 2026-05-04.
   - Update `docs/raw_mk1_to_mk2_modes_mapping.ai.md` `applies_to` block — remove `hive/.raw (mk1, ~273 rules)` line.
   - Add closure marker `state/markers/dual_ssot_eol_landed.marker`.

## 8. Falsifier set

- **F-EOL-HIVE-1**: post-delete `find /Users/ghost/core/hive -maxdepth 2 -name '.raw' -o -name '.own' -o -name '.ext' -o -name '.guide' -o -name '.raw-audit' -o -name 'raw_archive'` returns exactly **0** for the SSOT files (`.raw`/`.own`/`.ext`/`.guide` already pass; `.raw-audit` and `raw_archive/` MAY be retained or relocated — adjust expectation).
- **F-EOL-HIVE-2**: post-delete tooling lint passes on a representative sample: `hexa run tool/meta_lint.hexa --selftest` exit 0 (currently will fail because `.raw not present` is treated as harness configuration error per line 133–134).
- **F-EOL-HIVE-3**: mk2 entries don't carry dangling `mk1.rawN` `supersedes` pointers — either kept as provenance-only strings (Option A) OR replaced with archive pointers (Option B). Whichever chosen must be uniform across all 14 mk2 entries.
- **F-EOL-HIVE-4**: round-trip clone `git clone git@github.com:need-singularity/hive.git tmp-clone && hexa run tmp-clone/tool/raw_mk2_loader.hexa --selftest` exits 0 (mk2 still self-validates).
- **F-EOL-HIVE-5**: sister-repo `anima/.raw-ref` either deleted, repointed to private archive, or marked retired with a tombstone — not left dangling with an unverifiable `pinned-hash`.
- **F-EOL-HIVE-6**: search the repo for the exact byte sequence `env("HIVE")+"/.raw"` (and `env("HIVE") + "/.raw"`) — count must be 0 in production-tier files (i.e., excluding test fixtures and historical comments) post-cleanup.

## 9. Honest C3

1. **mk2 has only 14 rules at EOL time — the bulk 250+ mk1 rules are NOT migrated.** Deleting mk1 without migration means LIVE rules from the mk1 era effectively vanished from the canonical layer. The historical content is preserved in `need-singularity/raw-archive` (private repo) but not in any reachable runtime path. This is the dominant risk; it is in direct tension with the mk1→mk2 mapping doc's stated gating ("after mk2 reaches lint coverage parity").

2. **chflags uchg unlock is single-file (`.raw-audit`) and trivially reversible — but the broader 244-uchg-file inventory in hive contains many frozen archive directories whose unlocking would be a separate operational mistake.** Audit recommendation: scope the unlock strictly to `.raw-audit`. Do NOT do a blanket `chflags nouchg -R` across the repo.

3. **Sister repo pin chain is real and ALREADY broken at the time of this audit.** `/Users/ghost/core/anima/.raw-ref` carries `pinned-hash 2c67adde9f9068274db8f034f135a9c6e57503bb1e4395a112cd50a0666099ce` against `path .raw` in `github.com/need-singularity/hive`. Since the on-disk `.raw` was deleted on 2026-05-02 and presumably purged from upstream too, that hash is no longer resolvable from `HEAD`. The pin file has not been updated, and `tool/raw_sync.hexa check` will fail. This is a pre-existing breakage, not one this audit creates.

4. **Migration spec explicitly named the gate ("mk2 reaches lint coverage parity + sister-repo adoption"); current decision is BEFORE that gate.** Per `docs/raw_mk1_to_mk2_modes_mapping.ai.md` and `.raw.mk2` header line 42–43: "mk1 EOL is a separate Ω-cycle decision (after mk2 reaches lint coverage parity + sister-repo adoption)." Today's user instruction overrides that gate. The audit captures this explicit override; the operational risk is that the overriding decision is a deliberate one (user knows the gap) vs. inadvertent.

5. **Some tools will HARD-FAIL post-delete rather than gracefully fall back to mk2.** Notably `tool/meta_lint.hexa` line 133–134: error message `cause: ".raw not present at <path> — composition cross-link cannot be verified" / remedy: "harness configuration error — .raw must always exist per raw 0 root-ssot"`. This tool will treat the missing `.raw` as a harness config error, not as expected EOL state. Pre-deletion mitigation: amend the tool's error path to recognize "EOL legitimately removed" vs "config error".

6. **`raw_mk2_inline_loader.hexa` premise is moot post-EOL.** The tool's stated job (line 4) is to scan `.raw` for inline mk2 blocks (`# mk2-rule-begin`/`# mk2-rule-end`). With `.raw` gone, the tool has no input. It should either be retired or rebranded as a no-op. Same applies to any tool whose only job was mk1↔mk2 dual-SSOT bridge work.

7. **`.raw-exemptions/raw_*.list` files are still consumed by `tool/ai_native_scan.hexa`** per their own header comment. These were named after mk1 rule numbers (raw 6 = folder-naming F4, raw 7 = ai-native scan exemption) but contain LIVE allowlists. Deleting them deletes runtime configuration, not historical data. Recommend rename (`raw_6.list` → `arch.001.exempt.list` mapping mk1.raw6 → mk2.arch.001 if applicable, or simply preserve under a non-mk1-numbered name).

8. **Today's `raw_archive/2026-05-04T/` snapshot is helpful but not git-managed.** The whole directory is ad-hoc; it captures bin/config/core/docs/modules/packages/spec/state/tool dirs as well as mk2 files. Without an explicit retention policy this directory will accumulate. The `need-singularity/raw-archive` private repo is the durable answer; `raw_archive/` local directory should be retained briefly then cleaned per its own policy.
