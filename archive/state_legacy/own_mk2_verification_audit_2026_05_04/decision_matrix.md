# own_mk2_verification — decision matrix

audit_ts: 2026-05-04T19:30 KST
scope: 10 top-level `.own*` files across 7 git repos (excluding 102 worktree-scoped legacy snapshots and 2 raw_archive backups)

---

## Per-file decision table

| # | repo | path | schema_class | timestamp_class | rules | cross_link_dep | recommendation | rationale |
|---|------|------|--------------|-----------------|------:|----------------|----------------|-----------|
| 1 | anima | `.own` | mk2_VERIFIED | PRE_MK2_BORN_MK2_UPGRADED | 13 | hive/spec/schema/own_v1.schema.yaml + cpre + .guide | **KEEP** | canonical mk2 baseline; BG-β confirmed; anchor for cross-repo schema |
| 2 | hexa-lang | `.own` | mk1_GRANDFATHER | PRE_MK2 | 3 | tool/own_self_host_lint.hexa; raw_loader.hexa parser-owner | **REMEDIATE (optional)** or **DEFER** | parser-owner exemption acceptable per anima own#1 grandfather pattern; additive mk2 frontmatter optional |
| 3 | hexa-os | `.own-rules.json` | UNKNOWN (JSON raw-own/1.0) | PRE_MK2 | 5 (HOS1-HOS5) | docs/HEXA_SERVE_V01.md + hexa_os_self_mk2_tuning_landed_*.ai.md + 2 markers | **DEFER** | hexa-os mk2 rewrite docs explicitly preserve `.own-rules.json` UNCHANGED — documented L1 JSON exception, not cruft |
| 4 | CANON | `.own.readme` | mk2_VERIFIED (n6-local schema) | POST_MK2_RECENT | 5 | docs/n6_architecture_own_readme_mk2_reconstruction_*.ai.md + absolute_rules.json | **KEEP** | mk2-compliant via n6-local schema variant `CANON/own/readme/2`; documented mk2 reconstruction (mk1 retired commit 442afa7b) |
| 5 | CANON | `.own.group_p` | mk2_VERIFIED (n6-local schema) | POST_MK2_EARLY | 1 (own#6 unified) | docs/n6_architecture_own_group_p_mk2_reconstruction_*.ai.md + own6/own31 lint | **KEEP** | same n6-local mk2 family as `.own.readme` |
| 6 | nexus | `.own` | mk1_GRANDFATHER | PRE_MK2 | 9 | **launchctl dev.hexa-lang.atlas-absorb-sweeper LOADED** + tool/atlas_absorb_*.hexa + plist | **REMEDIATE (urgent)** | operational launchd dep — add mk2 frontmatter + fix stale "0 rules" header to "9 rules"; preserve rule body byte-identical |
| 7 | orpheus | `.own` | mk1_GRANDFATHER (mk:1 explicit) | POST_MK2_RECENT | 8 | cpre/contracts.ai.md C1-C7 + .roadmap.orpheus | **REVIEW** | POST_MK2_RECENT queue; mk2 spirit HIGH (structural sections present); likely MK2_UPGRADE (mk:1 → mk:2) after lint pass |
| 8 | wraith-wallet | `.own` | mk1_GRANDFATHER (mk:1 explicit) | POST_MK2_RECENT | 8 | cpre/contracts.ai.md W1-W8 + .roadmap.wraith-wallet | **REVIEW** | POST_MK2_RECENT queue; sibling cycle to orpheus; same recommendation |
| - | CANON | `raw_archive/2026-05-04T/.own.group_p.bak` | BACKUP | - | - | already archived | **NO_ACTION** | byte-identical backup; raw#15 backup chain |
| - | CANON | `raw_archive/2026-05-04T/.own.readme.bak` | BACKUP | - | - | already archived | **NO_ACTION** | byte-identical backup; raw#15 backup chain |

---

## Decision summary by recommendation

### KEEP (3)

- `anima/.own`
- `CANON/.own.readme`
- `CANON/.own.group_p`

### REMEDIATE — additive frontmatter only, preserve rule body byte-identical (1 urgent + 2 optional)

- **URGENT**: `nexus/.own` — operational launchd dep + stale header
- OPTIONAL: `hexa-lang/.own` — parser-owner self-host exemption acceptable
- OPTIONAL: `hexa-os/.own-rules.json` — JSON `_meta.mk:2` field add

### REVIEW (POST_MK2_RECENT manual pass) (2)

- `orpheus/.own` — likely MK2_UPGRADE
- `wraith-wallet/.own` — likely MK2_UPGRADE (sibling cycle)

### DEFER (1)

- `hexa-os/.own-rules.json` — documented L1 JSON exception; defer to hexa-os repo owner

### DELETE (0)

- **NONE recommended for top-level files**. User policy "mk2 아니면 폐기" applied conservatively — every top-level `.own*` has cross-link blocker.
- Worktree-scoped 102 `.own*` files: DEFER to separate worktree GC cycle (out of mk2 audit scope; not active SSOT; legacy detached snapshots).

### NO_ACTION (2)

- `CANON/raw_archive/2026-05-04T/.own.group_p.bak` — backup, leave per raw#15
- `CANON/raw_archive/2026-05-04T/.own.readme.bak` — backup, leave per raw#15

---

## Cross-link blocker classes (for delete-gate enforcement)

| blocker_class | files | impact |
|---------------|-------|--------|
| operational_launchd | nexus/.own | LOADED launchctl dep — delete = production break |
| tool_lint_dep | hexa-lang/.own + n6/*.own.* | lint dispatcher break |
| doc_marker_ref | hexa-os/.own-rules.json | 5 ref points (docs + markers + index) |
| cpre_contract_mirror | orpheus/.own + wraith-wallet/.own | C/W contract drift |
| spec_canonical_ref | anima/.own | hive/spec own_v1 schema canonical anchor |

Every top-level `.own*` falls into at least ONE blocker class — hence no DELETE recommendations for top-level scope.

---

## Worktree-scoped scope note (102 files)

| repo | count | recommendation |
|------|------:|----------------|
| hexa-lang/.claude/worktrees | 88 | DEFER → worktree GC cycle |
| CANON/.claude/worktrees | 3 | DEFER → worktree GC cycle |
| nexus/.claude/worktrees | 6 | DEFER → worktree GC cycle |
| void/.claude/worktrees | 5 | DEFER → worktree GC cycle |

These are git-detached worktree branch snapshots — none referenced by tools, plists, or active SSOT. Safe to GC during a separate worktree cleanup pass; explicitly OUT OF SCOPE for this mk2 audit.

---

end of decision_matrix.md
