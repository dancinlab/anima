# own_mk2_verification_audit — cross-repo `.own` mk2 schema verification (READ-ONLY)

audit_ts: 2026-05-04T19:30 KST
auditor: BG-ζ
scope: every git repo under `/Users/ghost/core/*/` containing `.own*` files
mode: READ-ONLY (no deletes, no modifications, no chflags, no git mutations)

---

## TL;DR

- 110 `.own*` files discovered across 8 git repos (anima / hexa-lang / hexa-os / n6-architecture / nexus / orpheus / void / wraith-wallet).
- 102 of 110 are worktree-scoped legacy snapshots under `.claude/worktrees/agent-*/.own`. Top-level (active SSOT) `.own*` count = 10 (across 7 repos: anima 1, hexa-lang 1, hexa-os 1, n6-architecture 4 [2 active + 2 backups], nexus 1, orpheus 1, wraith-wallet 1).
- by_schema_class (top-level only): mk2_VERIFIED=3 (anima, n6/.own.readme, n6/.own.group_p) / mk2_PARTIAL=0 / mk1_GRANDFATHER=4 (orpheus, wraith-wallet, hexa-lang, nexus) / UNKNOWN=1 (hexa-os `.own-rules.json`) / BACKUP=2 (n6 raw_archive `.bak`).
- by_timestamp_class (top-level git first_added): PRE_MK2=4 (anima 2026-04-21 / hexa-lang 2026-04-26 / hexa-os 2026-04-19 / nexus 2026-04-21) / POST_MK2_EARLY=1 (n6 .own.group_p 2026-05-03) / POST_MK2_RECENT=3 (n6 .own.readme 2026-05-04 / orpheus 2026-05-04 / wraith-wallet 2026-05-04).
- Top 3 review-queue items (POST_MK2_RECENT): orpheus `.own` (mk: 1, post-mk2 spec) / wraith-wallet `.own` (mk: 1, post-mk2 spec) / n6-architecture `.own.readme` (n6-local mk2 schema variant, not anima `project/own/v1`).
- Cross-link blockers: nexus `.own` own#1 atlas-absorb-mandatory wired to active launchctl `dev.hexa-lang.atlas-absorb-sweeper` (verified loaded). hexa-os `.own-rules.json` referenced in 2 docs + 2 markers + .git/index. Other top-level files referenced by sibling repos via cpre/.guide/.roadmap.
- Worktree-scoped 102 `.own*` files are legacy snapshots from worktrees (Apr 19-26 mtimes); none govern current state — DEFER all to worktree GC pass (out of mk2 scope).

---

## §1 — File enumeration table (top-level, active SSOT)

| repo | path | size | mtime | git first_added | git last_modified | schema_class | timestamp_class | cross_link |
|------|------|-----:|-------|-----------------|-------------------|--------------|-----------------|-----------|
| anima | `.own` | 63595 | 2026-05-04T13:29 | 2026-04-21 | 2026-05-04 | mk2_VERIFIED | PRE_MK2 (born) → mk2-upgraded 2026-05-02 | hive/spec/schema/own_v1.schema.yaml; cpre; .guide |
| hexa-lang | `.own` | 3679 | 2026-05-03T00:24 | 2026-04-26 | 2026-04-26 | mk1_GRANDFATHER | PRE_MK2 | self/raw_loader.hexa; cross-repo parser SSOT |
| hexa-os | `.own-rules.json` | 1052 | 2026-04-19T00:58 | 2026-04-19 | 2026-04-19 | UNKNOWN (JSON, pre-mk2 raw-own/1.0) | PRE_MK2 | docs/HEXA_SERVE_V01.md, hexa_os_self_mk2_tuning_landed_*.ai.md, 2 markers, .git/index |
| n6-architecture | `.own.readme` | 17682 | 2026-05-04T09:46 | 2026-05-04 | 2026-05-04 | mk2_VERIFIED (n6-local schema `n6-architecture/own/readme/2`) | POST_MK2_RECENT | docs/n6_architecture_own_readme_mk2_reconstruction_2026_05_04.ai.md; absolute_rules.json |
| n6-architecture | `.own.group_p` | 10283 | 2026-05-04T09:46 | 2026-05-03 | 2026-05-03 | mk2_VERIFIED (n6-local schema `n6-architecture/own/group_p/2`) | POST_MK2_EARLY | docs/n6_architecture_own_group_p_mk2_reconstruction_2026_05_03.ai.md |
| nexus | `.own` | 37054 | 2026-05-04T17:37 | 2026-04-21 | 2026-04-28 | mk1_GRANDFATHER (no frontmatter, raw-format only) | PRE_MK2 | launchctl dev.hexa-lang.atlas-absorb-sweeper (LOADED); tool/atlas_absorb_*.hexa |
| orpheus | `.own` | 24296 | 2026-05-04T18:59 | 2026-05-04 | 2026-05-04 | mk1_GRANDFATHER (`mk: 1` explicit; uses `schema_version: project/own/v1`) | POST_MK2_RECENT | cpre/contracts.ai.md C1-C7; .roadmap.orpheus |
| wraith-wallet | `.own` | 21321 | 2026-05-04T17:11 | 2026-05-04 | 2026-05-04 | mk1_GRANDFATHER (`mk: 1` explicit; uses `schema_version: project/own/v1`) | POST_MK2_RECENT | cpre/contracts.ai.md W1-W8; .roadmap.wraith-wallet |

### Backup files (already archived)

| path | size | mtime | class |
|------|-----:|-------|-------|
| n6-architecture/raw_archive/2026-05-04T/`.own.group_p.bak` | 10283 | 2026-05-04T13:28 | BACKUP (byte-identical to active .own.group_p) |
| n6-architecture/raw_archive/2026-05-04T/`.own.readme.bak` | 17682 | 2026-05-04T13:28 | BACKUP (byte-identical to active .own.readme) |

### Worktree-scoped (legacy snapshots — NOT active SSOT)

| repo | count | example header | class |
|------|------:|----------------|-------|
| hexa-lang/.claude/worktrees | 88 (84 `.own` + 4 `.own-rules.json`) | "hexa-lang /.own — L1 project-local (3 rules)" | mk1_GRANDFATHER (snapshots, mtimes 2026-04-19 .. 2026-04-26) |
| n6-architecture/.claude/worktrees | 3 | "n6-architecture /.own — L1 unified governance DSL (21 rules)" | mk1_GRANDFATHER (snapshots, mtimes 2026-04-24) |
| nexus/.claude/worktrees | 6 | "nexus /.own — L1 project-local (0 rules)" (215 bytes — empty stub) | mk1_GRANDFATHER (snapshots, mtimes 2026-04-21) |
| void/.claude/worktrees | 5 | "#!raw\nvoid /.own — L1 project-local rules\ninherits hexa-lang/.raw" | mk1_GRANDFATHER (snapshots, mtimes 2026-04-21) |

---

## §2 — Per-class detail

### mk2_VERIFIED (3 files)

1. **`anima/.own`** — 63595 bytes, 13 own declarations.
   Frontmatter excerpt:
   ```
   # ---
   # schema_version: project/own/v1
   # last_updated: 2026-05-02
   # mk: 2
   # ---
   ```
   References anima `roles`/`baselines`/`project_directives`/`cross_link_to_specs`/`cross_link_to_raws` sections. SSOT baseline confirmed by BG-β audit (commit a3295309). RECOMMEND: KEEP (canonical mk2 reference).

2. **`n6-architecture/.own.readme`** — 17682 bytes, 5 README-bound rules (own#14/17/20/21/29).
   Frontmatter excerpt:
   ```
   # ---
   # schema: n6-architecture/own/readme/2
   # last_updated: 2026-05-04
   # ssot: { parent_handoff: ..., sibling_emit: .own.group_p, axis_spine: .roadmap.n6_architecture, ... }
   # status: live
   # omega_cycle: 6-step single-pass
   # ---
   ```
   Uses n6-local schema variant (`n6-architecture/own/readme/2`) — NOT anima `project/own/v1` but follows mk2 spirit (frontmatter + structured ssot block + status). RECOMMEND: KEEP (n6-local mk2 schema is intentional; reconstructed 2026-05-04 from mk1 .own delete at commit 442afa7b).

3. **`n6-architecture/.own.group_p`** — 10283 bytes, 1 unified rule (own#6 paper-3pack-verify-embedded).
   Frontmatter excerpt:
   ```
   # ---
   # schema: n6-architecture/own/group_p/2
   # last_updated: 2026-05-03
   # ssot: { ... }
   # status: live
   # ---
   ```
   Same n6-local schema family as `.own.readme`. RECOMMEND: KEEP.

### mk2_PARTIAL (0 files)

None.

### mk1_GRANDFATHER (4 files — top-level)

1. **`hexa-lang/.own`** — no frontmatter, 3 own rules (own#1 parser-format-stability / own#3 hexa-lang-self-host). Header is plain "# hexa-lang /.own — project-local SSOT layer, self-hosting only" comment. **NOT a delete candidate** — this repo IS the parser-owner for raw-format; header style predates mk2 spec by design (parser-owner self-host invariance). Diagnostic: technically pre-mk2 but functionally critical (self-host fixpoint enforced by tool/own_self_host_lint.hexa). RECOMMEND: REMEDIATE (add mk2 frontmatter additively — `# ---\n# schema_version: project/own/v1\n# mk: 2\n# ---` — without changing rule body) or DEFER (parser-owner exemption per anima own#1 grandfather pattern).

2. **`nexus/.own`** — no frontmatter, 9 own rules (own#1 atlas-absorb-mandatory ... own#9 user-facing-response-friendliness). Header "# nexus /.own — L1 project-local (0 rules)" is stale — actual rule count is 9. **CRITICAL CROSS-LINK**: own#1 atlas-absorb-mandatory wired to launchctl `dev.hexa-lang.atlas-absorb-sweeper` (verified loaded in user launchd). Also references `tool/atlas_absorb_lint.hexa`, `tool/atlas_absorb_sweeper.hexa`, `tool/witness_emit.hexa`, `launchd/dev.hexa-lang.atlas-absorb-sweeper.plist`. RECOMMEND: REMEDIATE (urgent — add mk2 frontmatter; fix stale "0 rules" header to "9 rules"; preserve rule body byte-identical). DELETE blocker: high (operational launchd plist depends on rule body).

3. **`orpheus/.own`** — has `schema_version: project/own/v1` + `mk: 1` explicit. Use mk2 SCHEMA_VERSION but mk1 schema-mode declared. Has structured roles/baselines/project_directives/cross_link sections (mk2 spirit). Created 2026-05-04 — POST_MK2 but author chose mk1 mode explicitly. RECOMMEND: REVIEW (POST_MK2_RECENT queue) — likely just needs `mk: 1` → `mk: 2` upgrade after auditor confirms structural mk2 compliance.

4. **`wraith-wallet/.own`** — same pattern as orpheus. `schema_version: project/own/v1` + `mk: 1`. Created 2026-05-04 sibling cycle to orpheus. RECOMMEND: REVIEW (same as orpheus).

### UNKNOWN (1 file — top-level)

- **`hexa-os/.own-rules.json`** — JSON, schema `raw-own/1.0`, 5 rules HOS1-HOS5. NOT raw-format DSL — entirely separate JSON convention. Created 2026-04-19 (predates mk2 by 13 days). Referenced in 2 docs + 2 markers (`docs/HEXA_SERVE_V01.md`, `docs/hexa_os_self_mk2_tuning_landed_2026_05_02.ai.md`, `docs/hexa_os_mk2_rewrite_landed_2026_05_03.ai.md`, 2 .marker files). hexa-os mk2 rewrite docs explicitly preserve `.own-rules.json` UNCHANGED. RECOMMEND: DEFER — hexa-os mk2 rewrite deliberately preserves L1 JSON convention; this is a documented exception, not cruft. Optionally REMEDIATE by adding `_meta.mk: 2` field if uniformity desired.

---

## §3 — POST_MK2_RECENT review queue (deep-read)

Per user policy "mk2 설계 이후 작성된 .own 진지하게 검토":

### 3.1 — orpheus/.own (created 2026-05-04, mk: 1 explicit)

**What it grandfathers**: 8 own rules covering external-cli-only-access, found-key-encryption-at-write, hexa-only (raw 9 mirror), honest-disclosure (raw 10 mirror), puzzle-target-staleness-check, sweep-tx-no-public-mempool, etc. C1-C7 cpre contract mirror.

**Why post-mk2 but mk1**: orpheus repo was scaffolded 2026-05-04 (sibling repo for Bitcoin Puzzle work). Author flagged `mk: 1` likely because the rule body uses raw-format DSL but did not yet add mk2-spec sections (no `cross_link_to_specs` to anima.spec.yaml; no formal owner-self-verify proof line set). Functionally it IS structured (roles/baselines/project_directives/cross_link blocks present) — just self-flagged as mk1 to be conservative.

**mk2 spirit consistency**: HIGH. Frontmatter structure matches anima exactly except `mk: 1` instead of `mk: 2`. Has structured comment-prefix sections. Uses raw_loader.hexa-compatible body.

**RECOMMEND: REVIEW → likely MK2_UPGRADE** (author flips `mk: 1` → `mk: 2` after lint confirms compliance).

### 3.2 — wraith-wallet/.own (created 2026-05-04, mk: 1 explicit)

**What it grandfathers**: 8 own rules covering external-cli-only-access, backend-swap-uniformity (Stage 1 cake wrap ↔ Stage 2 native), broadcast-policy-gate-default-dry-run, separation-of-knowledge (orpheus↔wraith↔ghost layer separation), hexa-only, etc. W1-W8 cpre contract mirror.

**Why post-mk2 but mk1**: Same sibling cycle as orpheus (orpheus duo pair: 🗝️ orpheus ↔ 🫥 wraith-wallet). Same conservative `mk: 1` self-flag.

**mk2 spirit consistency**: HIGH (same structural pattern as orpheus).

**RECOMMEND: REVIEW → likely MK2_UPGRADE** (sibling cycle — apply same decision as orpheus).

### 3.3 — n6-architecture/.own.readme (created 2026-05-04)

**What it grandfathers**: 5 README-bound rules (own#14 readme-sealed-required / own#17 public-readme-english-only / own#20 readme-techniques-count-drift / own#21 readme-nexus6-tests-count-drift / own#29 P0 readme-friendly-toolkit-required).

**Why post-mk2**: Reconstruction after mk1 .own (881 LoC, 32 rules) deleted 2026-05-03 commit 442afa7b. n6 chose to split mk1 .own into multiple mk2 files by axis: `.own.readme` (README governance) + `.own.group_p` (paper-md governance) + future axis files. This is INTENTIONAL mk2 design choice (axis-split additive over collapse).

**mk2 spirit consistency**: VERY HIGH — has frontmatter (schema/last_updated/ssot/policy/status/omega_cycle), structured 6-step omega_cycle, predecessor_handoff chain to mk1 recovery blob (`/tmp/n6_own_mk1.txt commit 442afa7b^:.own`). Uses n6-local schema namespace `n6-architecture/own/readme/2` rather than anima's `project/own/v1` — DIFFERENT pattern from anima but mk2-compliant in spirit.

**Caveat**: n6 schema variant means cross-repo schema validators (e.g., `hive/spec/schema/own_v1.schema.yaml`) will NOT validate n6 .own files. Acceptable if n6 has own validator.

**RECOMMEND: KEEP** (mk2-compliant via n6-local schema variant; documented mk2 reconstruction).

---

## §4 — Cross-link impact

### Active launchd plists

- `dev.hexa-lang.atlas-absorb-sweeper` LOADED (verified `launchctl list | grep atlas`). Wired to `nexus/.own` own#1 atlas-absorb-mandatory + `nexus/launchd/dev.hexa-lang.atlas-absorb-sweeper.plist`. Also `com.nexus.atlas-meta-scan` loaded.
- DELETE BLOCKER: nexus `.own` MUST not be deleted — operational sweeper depends on rule body for orphan detection.

### Tool/doc references

- `hexa-os/.own-rules.json` referenced in 5 places (2 docs + 2 markers + git index) — DELETE BLOCKER.
- `anima/.own` referenced in cpre/.guide/hive specs — DELETE BLOCKER (canonical mk2 reference).
- `hexa-lang/.own` self-host fixpoint enforced by `tool/own_self_host_lint.hexa` — DELETE BLOCKER.
- n6 `.own.readme` + `.own.group_p` enforced by lint tools (own6 / own29 / own_doc_lint) — DELETE BLOCKER.
- orpheus + wraith-wallet `.own` mirror cpre C-rules / W-rules — DELETE BLOCKER (cross-repo handoff sibling pair).

### Worktree snapshots (delete-safe)

- 102 worktree-scoped `.own*` files are git-detached snapshots in `.claude/worktrees/agent-*/` directories. None referenced by tools, plists, or active SSOT. SAFE to GC during worktree cleanup pass.

---

## §5 — Recommended action plan

### Phase A — Backup archival (no-op)

- n6 raw_archive `.own.*.bak` files already in `raw_archive/2026-05-04T/` per BG-γ audit; no further action needed.
- DECISION: leave in place (per raw#15 raw_archive backup chain).

### Phase B — Deletes per user policy "mk2 아니면 폐기"

- **NONE recommended for top-level**. Every top-level `.own*` has cross-link blocker (launchd / lint / spec ref). User policy must be applied with cross-link gate.
- Worktree scope: 102 `.own*` files — DEFER to separate worktree GC cycle (out of mk2-scope; not active SSOT).

### Phase C — Review queue manual pass (3 files)

- orpheus/.own: confirm structural mk2 compliance + author flip `mk: 1` → `mk: 2`.
- wraith-wallet/.own: same as orpheus (sibling cycle).
- n6-architecture/.own.readme: already mk2 (n6-local schema variant) — DOCUMENT cross-repo schema variance in audit (anima `project/own/v1` ≠ n6 `n6-architecture/own/readme/2`).

### Phase D — REMEDIATE candidates (additive frontmatter only)

- nexus/.own: add mk2 frontmatter `# ---\n# schema_version: project/own/v1\n# mk: 2\n# ---` + fix stale "0 rules" header to "9 rules". Preserve rule body byte-identical (raw#15).
- hexa-lang/.own: optionally add mk2 frontmatter (parser-owner can exempt; defer to repo owner).
- hexa-os/.own-rules.json: optionally add `_meta.mk: 2` JSON field.

### Phase E — KEEP unchanged

- anima/.own (canonical mk2 baseline)
- n6/.own.readme (mk2 n6-local)
- n6/.own.group_p (mk2 n6-local)

---

## §6 — Falsifier set

- **F-OWN-MK2-1** (post-decision invariant): every kept top-level `.own*` either has `mk: 2` frontmatter OR documented cross-repo schema variant OR explicit grandfather exemption.
- **F-OWN-MK2-2** (no orphan launchd): post-cleanup, no launchd plist references a deleted .own (verified via launchctl list ↔ grep cross-check).
- **F-OWN-MK2-3** (review queue documented): every POST_MK2_RECENT file has REVIEW entry in this audit with deep-read summary + recommendation.
- **F-OWN-MK2-4** (worktree scope discrimination): active top-level vs worktree-detached snapshot classification preserved (no top-level `.own*` accidentally deleted as part of worktree GC).

---

## §7 — Honest C3 (≥4)

1. **mtime/ctime modifiable**: `touch -t` and `chflags`/copy operations can rewrite filesystem timestamps. Git first_added is canonical — but git log requires file is tracked. Worktree `.own` snapshots are partly git-tracked, partly not (worktree branches diverge); some worktree mtimes may be touch-modified. For top-level files, git log was used as ground truth — backup `.bak` files trusted by mtime.

2. **Schema variant ambiguity**: n6-architecture uses n6-local schema namespace (`n6-architecture/own/readme/2`, `n6-architecture/own/group_p/2`) rather than anima's `project/own/v1`. Both are mk2-spirit compliant but cannot share validators. Cross-repo schema canonicalization is OUT OF SCOPE for this audit; documented as caveat.

3. **Frontmatter parsing brittleness**: This audit checked first 30 lines for `# ---\n#` markers. JSON files (hexa-os) have entirely different convention (`_meta` block). hexa-lang and nexus have NO frontmatter (raw-format only). Lenient parse used here — strict YAML/TOML parser would reject 5 of 7 top-level files. Manual classification preferred over automated parse for this audit.

4. **Delete decision irreversibility**: All top-level files have cross-link blockers; this audit recommends REMEDIATE/REVIEW/KEEP for ALL top-level files (no DELETE). User policy "mk2 아니면 폐기" applied conservatively here — no top-level deletes recommended without operational impact analysis. Worktree GC (102 snapshots) is the proper deletion track but out of mk2 audit scope.

5. **Worktree count exclusion**: 102 worktree `.own*` snapshots dominate the file count but are operationally inert (legacy worktree branches). Including them in by_schema_class would skew the picture; this audit reports them separately as "worktree-scoped legacy".

6. **launchctl scope**: `launchctl list` was checked in user-scope only; system-scope launchd plists not audited. Verified `dev.hexa-lang.atlas-absorb-sweeper` LOADED in user scope; assumed no system-scope cross-link.

---

end of audit.md
