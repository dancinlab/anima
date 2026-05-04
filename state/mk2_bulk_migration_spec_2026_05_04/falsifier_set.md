# Falsifier set — mk2 bulk migration

Cross-link: `state/mk2_bulk_migration_spec_2026_05_04/spec.md` §6
Authority: mk2 schema falsifier shape per `.raw.mk2.schema.yaml#rule.falsifiers`

## F-MIG-1 — post-migration mk2 rule_count band

- **id**: `F-MIG-1`
- **description**: After bulk migration completion, mk2 rule count must land in the predicted range derived from §4 cluster collapse estimate (mid-band ~200; lower bound 150 if aggressive collapse; upper bound 230 if minimal collapse)
- **threshold**: `mk2_rule_count >= 150 AND mk2_rule_count <= 230`
- **action-on-fail**:
  - if `< 150`: scope-review (cluster pass over-merged; may have erased distinct invariants)
  - if `> 230`: scope-review (cluster pass under-applied; redundancy preserved)
- **audit method**:
  - command: `hexa run /Users/ghost/core/hive/tool/raw_mk2_loader.hexa` (output line `[raw_mk2_loader] OK rules=<N>`)
  - cross-check: `grep -c '^{' /Users/ghost/core/hive/.raw.mk2`
- **expected baseline post-S3 strategy**: ~200

## F-MIG-2 — every non-retracted mk1.rawN has mk2 link OR retracted marker

- **id**: `F-MIG-2`
- **description**: Every mk1 raw N entry that is not explicitly retracted must have either a forward `supersedes` link from at least one mk2 rule, OR a `# RETRACTED` marker recorded in mk1 .raw, OR a `derives-from` reference from mk2 (for non-superseding lineage)
- **threshold**: `unmapped_mk1_count == 0`
- **action-on-fail**: strengthen (manual hand-add via mk2 rule emit OR retract-row append)
- **audit method (per-rule)**:
  ```
  for N in 1..273:
      mk1_status = parse_mk1_status(N)
      if mk1_status == "retracted": continue
      mk2_links = grep_jsonl_for(".raw.mk2",
          ["supersedes contains mk1.rawN",
           "derives-from contains mk1.rawN"])
      if len(mk2_links) == 0:
          unmapped.push(N)
  ```
- **rollup**: emits `state/mk2_bulk_migration_2026_05_NN/coverage_report.jsonl` with one row per N

## F-MIG-3 — schema validation passes

- **id**: `F-MIG-3`
- **description**: Every newly emitted mk2 rule line passes schema validation per `tool/raw_mk2_loader.hexa --selftest`
- **threshold**: `loader_rc == 0 AND fail_count == 0`
- **action-on-fail**: strengthen-fail-loud (raw 92 paired) — block append until validation passes
- **audit method**:
  - per-batch: `hexa run /Users/ghost/core/hive/tool/raw_mk2_loader.hexa --selftest`
  - sentinel: `__RAW_MK2_LOADER_SELFTEST__ <PASS|FAIL> n=<N> fail=<M>`
  - all 5 internal tests (T1 load / T2 ≥3 rules / T3 cross-link / T4 unique id / T5 negative case) must PASS
- **gate**: any batch failing this falsifier MUST be rolled back via .raw.mk2 line-prune before next batch

## F-MIG-4 — lint coverage parity

- **id**: `F-MIG-4`
- **description**: After migration completes, mk2 rule count over `live` mk1 rule count meets the parallel-period EOL gating threshold per `.raw.mk2.schema.yaml#migration_policy`
- **threshold**: `mk2_rules / mk1_live_rules >= 0.90`
- **action-on-fail**:
  - scope-review if 0.85 ≤ ratio < 0.90 (re-tune cluster pass to add specificity)
  - extend cluster pass to fill missing domains if ratio < 0.85
- **audit method**:
  ```
  mk1_live = grep -c '^raw [0-9]\+ live ' archive/.raw
  mk1_retracted = grep -c '^raw [0-9]\+ retracted ' archive/.raw
  mk1_denominator = mk1_total - mk1_retracted   # exclude retract-rows from denominator
  mk2_count = hexa run tool/raw_mk2_loader.hexa | grep -oE 'rules=[0-9]+' | cut -d= -f2
  ratio = mk2_count / mk1_denominator
  ```
- **expected post-S3**: ratio ≈ 0.92 (within ±5% tolerance)

## Per-rule audit method (cross-falsifier)

For every emitted mk2 rule, the following per-rule checks run inline at append time:

| check                                         | source                                | falsifier link |
| --------------------------------------------- | ------------------------------------- | -------------- |
| `id` matches `<domain>.<3-digit>`             | loader L97-110                        | F-MIG-3        |
| `domain` ∈ DOMAINS whitelist                  | loader L91-94                         | F-MIG-3        |
| `status` ∈ STATUSES whitelist                 | loader L84-87                         | F-MIG-3        |
| `enforce.layer` ∈ ENFORCE_LAYERS              | loader L116-119                       | F-MIG-3        |
| `enforce.severity` ∈ SEVERITIES               | loader L121-124                       | F-MIG-3        |
| `mk == 2` AND `schema == hive/rule/v2`        | loader L69-80                         | F-MIG-3        |
| REQUIRED_KEYS present (id/mk/schema/status/title/since/domain/category/why) | loader L34-35 + L60-66 | F-MIG-3 |
| `related[]` resolves intra-mk2                | loader verify_cross_links             | F-MIG-3        |
| `derives-from[]` references valid mk1.rawN format | format-only check (full resolve = follow-up) | F-MIG-2 |
| `supersedes[]` referenced mk1.rawN is parseable | format-only check                   | F-MIG-2        |
| `modes` block present per canonical 4-class OR explicit lock_reason | mapping doc canonical table | (per-rule) |

Every per-rule check failure: emit `state/mk2_bulk_migration_2026_05_NN/per_rule_audit.jsonl` row + halt batch + USER ACK to fix or skip.

## Falsifier preregistration discipline (raw#15)

This falsifier set is REGISTERED before migration execution begins. Mid-flight threshold relaxation is forbidden. If migration produces results outside the predicted bands (F-MIG-1 / F-MIG-4), the resolution is one of:

1. **scope-review** — re-examine the cluster collapse pass logic; do not bend the falsifier
2. **strengthen** — add hand-review entries to fix unmapped raws
3. **strengthen-fail-loud** — block migration completion until F-MIG-3 passes

No silent threshold drift. (raw#92 + raw#15 paired.)
