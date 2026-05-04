# mk2 Bulk Migration Spec — 273 mk1 rules from need-singularity/raw-archive

- **status**: spec-only (SPEC ONLY $0; no execution this BG)
- **since**: 2026-05-04
- **owner-bg**: BG-ε (parallel with BG-δ hexa-lang gap audit, BG-η nexus N6 evidence preservation)
- **predecessor**: BG-α hive audit commit `1a259542` (2026-05-03)
- **driver**: mk2 currently lands 14/273 = **5.13% rule parity** (semantic ~35% via cluster collapse). 259 rules pending bulk migration.
- **target SSOT**: `/Users/ghost/core/hive/.raw.mk2` (JSONL append-only)
- **source archive**: private GitHub `need-singularity/raw-archive` (snapshot of pre-cleanup hive `.raw` mk1 SSOT, ~273 rules; chflags-uchg before purge 2026-05-02)
- **mapping authority**: `/Users/ghost/core/hive/docs/raw_mk1_to_mk2_modes_mapping.ai.md`

## §1 — Migration scope

| axis                       | value                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------ |
| total mk1 rules            | 273 (±5 per mapping doc C6 — runtime recount mandatory)                              |
| mk2 rules already landed   | 14 (arch.001, ai-native.001, lint.001, resource.001-006/009, cli.001-004)            |
| explicit supersedes claims | mk1.raw3, raw9, raw11, raw40, raw42, raw92, raw95, raw105, raw162, raw173, raw200,   |
|                            | raw240, raw261, raw262, raw269, raw270, raw271, raw272, raw273 (≈19 raws supersede   |
|                            | one or more of the 14 mk2 rules; some are listed in derives-from but not supersedes) |
| net rules to migrate       | **259 mk1 raws have no mk2 entry yet**                                               |
| expected mk2 rule yield    | ~150-200 after cluster collapse (see §4)                                             |
| hand-review queue          | ~13-15 outliers (~5% per mapping doc Caveat C1)                                      |
| domain whitelist size      | 14 (arch, ai-native, os-enforcement, format-grammar, lint, meta-enforcement,         |
|                            | resource, cli, auth, closure, axis + scoring/dispatch/meta added 2026-05-03)         |

Out of scope: `.own`, `.ext`, `.guide` (separate SSOT axes; this spec is `.raw → .raw.mk2` only).

## §2 — Migration sequence

```
Step 1.  Auth-clone archive
         ────────────────────────────────────────────────────────────
         git clone git@github.com:need-singularity/raw-archive.git \
             $HOME/.cache/raw-archive-mk2-migration
         requirement: USER ACK (private repo SSH key already provisioned per BG-α audit)

Step 2.  Parse mk1 .raw → per-rule records
         ────────────────────────────────────────────────────────────
         INPUT:  archive/.raw  (free-form mk1 SSOT)
         OUTPUT: state/mk2_bulk_migration_spec_2026_05_04/mk1_records.jsonl
         PARSER: tool/raw_mk1_parser.hexa  (NEW — promote raw_mk1_to_mk2_migrator.hexa
                 stub fn extract_mk1_raw() to a multi-line aware parser)
         FIELDS extracted per rule: {n, slug, status, title, severity, category,
                 decl, scope, why, note, falsifiers, related, derives-from}
         OBSERVABILITY: per-rule extraction success/fail JSONL row

Step 3.  Apply canonical mk1→mk2 mapping table
         ────────────────────────────────────────────────────────────
         AUTHORITY: docs/raw_mk1_to_mk2_modes_mapping.ai.md
         FOR EACH mk1 record:
           a. derive mk2.status from mk1.status (live | warn | new | deferred |
              convention | retracted) — direct passthrough per migrator stub
           b. derive mk2.modes block per 4-class canonical table
              (~95% of rules use one of 4 default class shapes)
           c. apply locked overrides (raw 1, 87, 91, 92) by name
           d. apply multi-value overrides (own #13 friendliness etc.) by slug

Step 4.  Cluster collapse pass
         ────────────────────────────────────────────────────────────
         IDENTIFY clusters of mk1 raws that resolve to one mk2 rule:
           - arch.001 pattern (4→1): raw270+raw271+raw272+raw273 already done
           - probable additional clusters: see §4 candidate list
         COLLAPSE strategy: union of derives-from + supersedes; pick richest
                 mk1 entry as title/decl seed; merge falsifiers de-duplicated;
                 merge why with explicit "(merged from raw N + raw M)" attribution
         OUTPUT: per-cluster mk2 candidate object with multi-source
                 derives-from + supersedes arrays

Step 5.  Domain.NNN id assignment
         ────────────────────────────────────────────────────────────
         FOR EACH candidate:
           a. infer domain via heuristic (see §3 mapping table)
           b. allocate next available <domain>.<3-digit> id
           c. ZERO-PAD seq numbers to 3 digits (loader L97-110 enforces)
         CONFLICT RESOLVE: alphabetical mk1.raw N order within domain → seq order

Step 6.  Schema validation
         ────────────────────────────────────────────────────────────
         hexa run tool/raw_mk2_loader.hexa --selftest
         REQUIRED-KEY check (id/mk/schema/status/title/since/domain/category/why)
         WHITELIST checks: status, domain, severity, enforce.layer
         CROSS-LINK check: related[] resolves intra-mk2

Step 7.  JSONL emit + append
         ────────────────────────────────────────────────────────────
         APPEND-ONLY to /Users/ghost/core/hive/.raw.mk2 (raw#102 monotonic;
                 raw#15 append-only state ledger)
         BATCH SIZE: 25 rules per commit (preserves diff hygiene; bisect-friendly)
         GUARD: post-append `tool/raw_mk2_loader.hexa --selftest` must PASS

Step 8.  Lint coverage parity check
         ────────────────────────────────────────────────────────────
         METRIC: mk2_rule_count / (mk1_rule_count - retracted_count)
         GATE: ≥ 90% before declaring migration COMPLETE (mapping doc parallel-period
                 EOL gating per .raw.mk2.schema.yaml#migration_policy)
         REPORT: state/mk2_bulk_migration_2026_05_NN/coverage_report.jsonl
```

## §3 — Domain mapping heuristics

Anchored on rules already migrated + mapping doc sample table:

| mk1 raw                        | slug                             | mk2 domain          | rationale                   |
| ------------------------------ | -------------------------------- | ------------------- | --------------------------- |
| 1                              | os-lock                          | os-enforcement      | LOCKED (chflags+launchd)    |
| 3                              | attr-usage                       | ai-native           | merged into ai-native.001   |
| 9                              | hexa-only-mandate                | ai-native           | hexa SSOT class             |
| 10                             | honest-c3 (self-applied here)    | meta-enforcement    | meta rule about rules       |
| 11                             | ai-native-default-strict         | ai-native           | merged into ai-native.001   |
| 15                             | append-only-state-ledger         | meta-enforcement    | mutation discipline         |
| 36                             | resource-backpressure-scheduler  | resource            | merged into resource.004    |
| 40, 42                         | ssh-direct, host-pool-membership | resource            | merged into resource.002    |
| 47                             | 30d-ramp                         | meta-enforcement    | ramp policy                 |
| 87                             | chflags-mandate                  | os-enforcement      | LOCKED (kernel EPERM)       |
| 91                             | honest-c3                        | meta-enforcement    | LOCKED-PARTIAL (off banned) |
| 92                             | no-silent-errors                 | lint                | LOCKED-PARTIAL (silent ban) |
| 95                             | parser-owner-self-test           | lint                | merged into lint.001        |
| 102                            | strengthen-monotonic             | meta-enforcement    | rules-about-rules           |
| 105                            | meta-bundle-permission           | cli                 | merged into cli.002         |
| 162                            | host-capacity-probe              | resource            | merged into resource.005    |
| 173                            | dispatch-routing-rr              | resource            | merged into resource.006    |
| 200                            | kick-canonical-entry             | cli                 | merged into cli.001         |
| 240                            | resource-manager-routing         | resource            | merged into resource.003    |
| 261, 262                       | auth-store / oauth-rotation      | auth (or resource)  | merged into resource.009    |
| 269                            | dispatch-table-singleton         | dispatch (new 5-03) | meta-cli                    |
| 270, 271, 272, 273             | core-module-* cluster            | arch                | merged into arch.001        |
| {own #13 friendliness}         | own-stream                       | (own SSOT)          | OUT OF SCOPE — `.own` axis  |
| {ext / response-style}         | ext-stream                       | (ext SSOT)          | OUT OF SCOPE — `.ext` axis  |

Heuristic rule of thumb (extends migrator stub `_heuristic_domain` lookup table):

```
mk1.category → mk2.domain
─────────────────────────────────────
"module-architecture"   → arch
"format-grammar"        → format-grammar
"os-enforcement"        → os-enforcement
"code-quality"          → ai-native
"ai-native"             → ai-native
"meta-triad"            → meta-enforcement
"audit-ledger"          → meta-enforcement
"design-strategy"       → meta-enforcement
"routing-dispatch"      → cli   (or new "dispatch" bucket post-2026-05-03)
"security-sandbox"      → os-enforcement
"naming"                → ai-native
"deploy-publication"    → resource
"scoring-axis-*"        → scoring (new 2026-05-03)
"meta-cross-cutting"    → meta (new 2026-05-03; use sparingly)
unknown                 → MANUAL OVERRIDE REQUIRED
```

## §4 — Cluster collapse opportunities

Cluster pattern is established by arch.001 (4→1) and validated by 5 already-landed clusters in resource/cli domains. Candidate clusters for the bulk migration to detect:

| cluster signature                              | est. mk1 raws | proposed mk2 id   | confidence |
| ---------------------------------------------- | ------------- | ----------------- | ---------- |
| chflags + os-lock + launchd-watcher            | 3-4 raws      | os-enforcement.NN | high       |
| 30d-ramp + warn-to-block + raw-strengthen-row  | 3-4 raws      | meta-enforce.NN   | high       |
| audit-ledger + jsonl-append + tail-witness     | 3-5 raws      | meta-enforce.NN   | medium     |
| pan-axis-lint + closure-loop + axis-marker     | 4-6 raws      | closure.001       | high       |
| hive-cli-fast-path + bin-singleton             | 2-3 raws      | cli.005           | medium     |
| auth-slot pool sub-rules (rotation/cooldown/…) | 2-3 raws      | already → res.009 | (done)     |
| friendliness/response-style multi-value        | 2-3 raws      | (own / ext axis)  | OUT-SCOPE  |
| AI-native @attr-family extensions              | 5-8 raws      | ai-native.NN      | high       |
| hexa-stdlib enforcement + import-discipline    | 3-4 raws      | ai-native.NN      | medium     |
| nexus-axis-marker + N6 conventions             | 4-6 raws      | axis.NNN          | medium     |
| roi-scoring + capacity-aware-LB ensemble       | 3-4 raws      | scoring.NN        | high       |

Estimated total cluster collapse: **70-100 mk1 raws → 25-35 mk2 rules**, leaving ~159-189 raws as 1:1 migrations → final mk2 yield ~184-224 rules. Mid-band estimate: **~200 mk2 rules** post-migration.

Risk: mis-collapse (see §10 honest C3). Each cluster MUST be hand-reviewed before commit.

## §5 — Hand-review outlier queue (~5%)

Per mapping doc C1 + lessons from 14 already-landed mk2 rules:

| rule type                                       | est count | hand-review reason                                  |
| ----------------------------------------------- | --------- | --------------------------------------------------- |
| LOCKED rules (raw 1, 87, 91, 92)                | 4         | explicit lock_reason override per name              |
| Multi-value enforcer dependency (own/ext)       | 3-5       | enforcer not yet retrofitted to read modes          |
| Self-applied meta rules (raw 10 honest-c3-self) | 2-3       | meta-of-meta handling                               |
| Idiosyncratic semantics (no canonical class)    | 2-3       | rule has bespoke severity model not in 4-class      |
| Cross-axis bridge rules (.raw + .own join)      | 1-2       | this spec scope is .raw only; bridges deferred      |
| Retracted-but-unrecorded mk1 rules              | ~3        | identify retract intent via `# RETRACTED` mk1 prose |
| **TOTAL hand-review queue**                     | **~13-15** | (target 5% of 273 ≈ 13-14 rules)                    |

Hand-review workflow: per-rule `state/mk2_bulk_migration_2026_05_NN/handreview/<raw_N>.candidate.jsonl` + USER ACK gate before commit to `.raw.mk2`.

## §6 — Falsifier set (cross-link to falsifier_set.md)

| ID      | description                                                               | threshold                                          | action-on-fail                       |
| ------- | ------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------ |
| F-MIG-1 | post-migration mk2 rule_count                                             | rule_count ≥ 150 AND ≤ 230 (post-cluster-collapse) | scope-review (re-tune cluster pass)  |
| F-MIG-2 | every non-retracted mk1.rawN has mk2 supersedes link OR retracted marker  | unmapped_count == 0                                | strengthen (manual hand-add)         |
| F-MIG-3 | schema validation (raw_mk2_loader.hexa --selftest) PASS                   | loader_rc == 0                                     | strengthen-fail-loud                 |
| F-MIG-4 | lint coverage parity                                                      | mk2_rules / mk1_live_rules ≥ 0.90                  | scope-review or extend cluster pass  |

## §7 — Cost band

- Mac dev only (raw#9 hexa-only): $0
- Archive clone: bandwidth only (private repo, no API spend)
- No GPU compute / no API calls
- **Total cost band: $0**

## §8 — Wall estimate

| phase                                               | wall (BG cycles) |
| --------------------------------------------------- | ---------------- |
| 1. Migrator hexa promotion (stub → real parser)     | 1 cycle          |
| 2. Bulk migration execution (clone → emit JSONL)    | 1 cycle          |
| 3. Hand-review outlier pass                         | 1 cycle          |
| 4. Schema validation + lint coverage parity check   | 0.5 cycle        |
| 5. Doc handoff + cross-link                         | 0.5 cycle        |
| **Total**                                           | **3-4 cycles**   |

## §9 — Cross-link

- BG-α hive audit: commit `1a259542` (2026-05-03)
- mapping authority: `/Users/ghost/core/hive/docs/raw_mk1_to_mk2_modes_mapping.ai.md`
- schema: `/Users/ghost/core/hive/.raw.mk2.schema.yaml`
- migrator stub: `/Users/ghost/core/hive/tool/raw_mk1_to_mk2_migrator.hexa` (extract_mk1_raw() + build_skeleton())
- loader: `/Users/ghost/core/hive/tool/raw_mk2_loader.hexa` (selftest, validate_rule, verify_cross_links)
- mk2 cli: `/Users/ghost/core/hive/tool/raw_mk2_cli.hexa` (list-mk2/show-mk2/verify-mk2)
- existing mk2: `/Users/ghost/core/hive/.raw.mk2` (14 rules: arch.001 + ai-native.001 + lint.001 + resource.001-006/009 + cli.001-004)
- decision matrix: `state/mk2_bulk_migration_spec_2026_05_04/decision_matrix.json`
- falsifier set: `state/mk2_bulk_migration_spec_2026_05_04/falsifier_set.md`
- handoff: `docs/mk2_bulk_migration_spec_landed_2026_05_04.ai.md`

## §10 — Honest C3 (raw#10 + raw#91)

**C3-1 — accreted cruft preservation risk (high)**
273 mk1 rules accreted over 8 years. Some are demonstrably obsolete (overridden by later rules, scope-reviewed, or implicitly retracted). Blind 1:1 migration into mk2 PRESERVES the cruft, defeating the clean-room rationale of mk2. Mitigation: every migrated rule MUST be reviewed for "still applies?" before assignment of `status:live`; ambiguous cases get `status:deferred` with `defer-until` per schema. This is roughly the inverse of cluster collapse: collapse merges related rules, retract-flag prunes dead ones.

**C3-2 — cluster collapse domain expertise gap (high)**
Cluster collapse decisions (4→1 per arch.001 pattern) require deep knowledge of which raws are "really the same rule" vs "thematically adjacent but distinct invariants." The 11 candidate clusters in §4 are HEURISTIC. Mis-collapse risks: (a) erasing a falsifier that was implicit in a sub-rule, (b) merging two rules whose enforcers are different tools. Mitigation: per-cluster diff review with USER ACK before commit; falsifier de-duplication MUST preserve every distinct threshold expression.

**C3-3 — enforce-tool retrofitting backlog (medium)**
Each mk2 rule needs a working enforcer. Today many mk1 enforcers do NOT read modes (per mapping doc C2). Bulk-loading 200+ rules into mk2 with `enforce.tool=tool/<X>_lint.hexa` references doesn't auto-revive lint hooks — it just declares the contract. Mitigation: a separate "enforcer retrofitting sweep" Phase MUST follow this migration; otherwise mk2 is a docs-only ledger. Phase 2 estimated 5-8 cycles.

**C3-4 — sister repo .raw-ref pinning drift (medium)**
Sister repos (anima, nexus, n6, airgenome, papers, hexa-lang) currently pin a hive `.raw` hash that no longer exists post-2026-05-02 cleanup. Even after mk2 fully populated, sister repos must re-pin to mk2 OR lazy-resolve via `.raw-ref` indirection. The migration spec's "lint coverage parity" gate (F-MIG-4) measures hive-internal coverage, NOT sister adoption. Sister adoption is separate Ω-cycle per `.raw.mk2.schema.yaml#migration_policy`. Migration ≠ sister adoption.

**C3-5 — migration ≠ enforcement (medium)**
Bulk migration into mk2 doesn't auto-revive lint hooks. The 14 rules already in mk2 each had a paired enforcer (or a PROPOSED follow-up tool with explicit ramp date). Bulk-migrating 259 raws blindly will produce hundreds of rules whose `enforce.tool` points at tools that may not exist on disk OR whose existing tools haven't been promoted to mk2-aware. Mitigation: every migrated rule MUST declare either (a) a confirmed-on-disk enforcer or (b) `enforce.tool: PROPOSED — bootstrap follow-up cycle <ID>` with a falsifier-1 of "tool exists by <date>".
