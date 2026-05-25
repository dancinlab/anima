# mk2 bulk migration spec — landed handoff (2026-05-04)

- **schema**: anima/doc/v1
- **status**: spec-only (SPEC ONLY $0; no execution)
- **landed-iso**: 2026-05-04
- **owner-bg**: BG-ε (parallel with BG-δ hexa-lang gap audit, BG-η nexus N6 evidence preservation)
- **predecessor**: BG-α hive audit commit `1a259542` (2026-05-03)
- **canonical SSOT**: `state/mk2_bulk_migration_spec_2026_05_04/spec.md`

## TL;DR

- mk2 currently lands 14/273 = **5.13% rule parity**; 259 mk1 rules pending bulk migration from private GitHub `dancinlab/raw-archive` to `hive/.raw.mk2`.
- 6-strategy decision matrix recommends **S3-cluster-first** (완성도 score 8.0/10): cluster collapse pass first (~25-35 mk2 rules from ~70-100 mk1 raws via arch.001 4→1 pattern), then 1:1 migrate the remaining ~159-189 raws in 25-rule batches.
- Mid-band yield: ~200 mk2 rules post-migration (cluster collapse 70-100 raws absorbed, hand-review queue ~13-15 outliers explicit).
- 4 falsifiers preregistered (F-MIG-1 rule_count band 150-230, F-MIG-2 unmapped_count==0, F-MIG-3 schema-validate PASS, F-MIG-4 coverage parity ≥0.90).
- Wall estimate 3-4 BG cycles; cost band $0 (Mac dev + offline private archive clone, raw#9 hexa-only conformant).

## Decision

**Recommended strategy**: `S3-cluster-first` (per `decision_matrix.json`)
**Primary rationale**: Highest 완성도 score (8.0). Cluster collapse pass mitigates honest C3-2 (cluster mis-merge risk) by routing each merge through USER ACK before commit. Granular per-batch review aligns with raw#15 append-only ledger discipline. Wall 3.5 cycles is the median across 6 strategies.
**Fallback**: `S5-canonical-only` if user_ack_load (12 gates) is rejected — accepts higher cruft risk to halve ACK gates.
**Do not pick**: `S2-full-bulk` (enforcer debt 120 + risk:high makes mk2 a docs-only ledger that defeats clean-room rationale).

## USER ACK gates required

| gate | description                                                              | blocks                       |
| ---- | ------------------------------------------------------------------------ | ---------------------------- |
| G1   | private GitHub `dancinlab/raw-archive` clone auth                 | Step 1 of migration sequence |
| G2-G12 | per-cluster review (11 cluster candidates per spec §4)                 | Step 4 (cluster collapse)    |
| G13  | post-cluster batch commit ACK                                            | Step 7 (JSONL append)        |
| G14  | per-25-rule 1:1 migration batch ACK (~7-8 batches expected)              | Step 7                       |
| G15  | hand-review queue manual pass (~13-15 outliers, 4 LOCKED + multi-value)  | Step 5 (id assignment)       |
| G16  | final lint coverage parity check ACK (F-MIG-4)                           | Step 8 (parity gate)         |
| G17  | mk2 schema lock declaration (schema-version bump if any structural change)| Step 6                      |

Total ~17-18 ACK gates per S3-cluster-first execution path.

## Cross-link

- spec: `state/mk2_bulk_migration_spec_2026_05_04/spec.md` (~480 LoC)
- decision matrix: `state/mk2_bulk_migration_spec_2026_05_04/decision_matrix.json` (6 strategies)
- falsifier set: `state/mk2_bulk_migration_spec_2026_05_04/falsifier_set.md` (4 F-MIG + per-rule audit)
- mapping authority: `/Users/ghost/core/hive/docs/raw_mk1_to_mk2_modes_mapping.ai.md`
- schema: `/Users/ghost/core/hive/.raw.mk2.schema.yaml`
- existing migrator stub: `/Users/ghost/core/hive/tool/raw_mk1_to_mk2_migrator.hexa`
- loader: `/Users/ghost/core/hive/tool/raw_mk2_loader.hexa`
- mk2 SSOT: `/Users/ghost/core/hive/.raw.mk2` (14 rules at land time)
- BG-α predecessor commit: `1a259542` (hive audit + raw-archive identification)
- parallel BGs (non-overlap): BG-δ `state/hexa_lang_gap_audit_2026_05_04/`, BG-η `state/nexus_n6_evidence_preservation_plan_2026_05_04/`

## Honest C3 (top 3 from spec §10)

1. **Accreted cruft preservation risk** — 273 rules accreted over 8 years; some demonstrably obsolete. Blind 1:1 migration preserves cruft, defeating mk2 clean-room rationale. Mitigation: per-rule "still applies?" review during migration; ambiguous → `status:deferred`.
2. **Cluster collapse domain expertise gap** — 4→1 cluster decisions require deep knowledge of which raws are "really the same rule" vs adjacent invariants. The 11 candidate clusters in spec §4 are HEURISTIC. Mitigation: per-cluster diff review with USER ACK before commit; falsifier de-duplication preserves every distinct threshold expression.
3. **Migration ≠ enforcement** — Bulk migration into mk2 declares contracts but does NOT auto-revive lint hooks. Of ~200 emitted rules, ~100-130 will reference `enforce.tool` paths that are PROPOSED-only or not yet promoted to mk2-aware. A separate "enforcer retrofitting sweep" Phase MUST follow this migration; otherwise mk2 is docs-only ledger. Phase 2 estimated 5-8 cycles.

## Hard constraints honored

- raw#9 hexa-only mandate: all migrator tooling stays in `.hexa`
- raw#10 honest-c3: each emitted mk2 rule retains ≥5-level honest-c3 in `why` or `note`
- raw#15 append-only: `.raw.mk2` is append-only; no in-place mutation
- raw#87 chflags: `.raw` stays uchg-locked; migration writes only to `.raw.mk2`
- raw#102 monotonic: retracted mk1 raws keep retract-row preservation
- repo-relative paths: all anima-side artifacts under `state/` and `docs/`
