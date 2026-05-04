# crystallography_n6 Extraction — Handoff (2026-05-04)

## Status: LANDED (n6-architecture pushed; nexus delete staged, NOT committed)

## What was done

1. **Pre-extraction grep** (nexus/anima/hive/n6-architecture, .hexa/.py/.md/.json/.toml, excluding worktrees + __pycache__): **0 functional consumers**. Only audit-doc references.
2. **Module audit**:
   - LoC: 402 (.hexa) + 61 (README) = 463 total
   - Deps: stdlib only (no external imports)
   - API: `enumerate(crystal_system)`, `atlas_facts()`, `_n6()`, `_system_data()` + CLI `--self-test`/`--atlas`/`--json`/`--system NAME`
3. **Copied** to `/Users/ghost/core/n6-architecture/domains/physics/crystallography/`:
   - `crystallography_n6.hexa` (co-located with existing `crystallography.md` IUCr research spec)
   - `crystallography_n6.README.md` (renamed to avoid collision with absent module-level README)
4. **Refactored**: header `// modules/crystallography_n6/...` → `// domains/physics/crystallography/...` + added `@origin:` tag. CLI `@usage(...)` lines updated. README updated to use hexa CLI commands at new path.
5. **Smoke test**: `hexa run domains/physics/crystallography/crystallography_n6.hexa --self-test` → **5/5 PASS**, sentinel `__CRYSTALLOGRAPHY_N6__ PASS`. Atlas mode also verified (6 @F lines).
6. **n6-architecture additive**: new `reports/changelogs/2026-05-04-crystallography-n6-extraction.md` (no README mutation — main README is auto-managed and 175KB).
7. **Git**:
   - n6-architecture commit `38d66066` pushed to `main` (PUBLIC GitHub).
   - nexus: `modules/crystallography_n6/` removed; delete staged on `feat/qmirror-cli-programmatic-consumption`. **NOT committed** per constraint.
8. **Nexus consumer refactor**: not needed — zero functional consumers.

## Destination choice

Audit doc suggested `domains/structure/crystallography/`, but `structure/` does not exist
in n6-architecture. Used `domains/physics/crystallography/` (already houses the canonical
`crystallography.md` research spec). This co-location pattern matches the established
`domains/compute/chip-isa-n6/{chip-isa-n6.md, xn6_asm_examples.hexa}` convention.

## User action required

Review staged delete in nexus then commit (separate concern, kept off auto-pipeline):

```
cd /Users/ghost/core/nexus
git diff --cached modules/crystallography_n6   # verify
git commit -m "chore(extract): remove crystallography_n6 — absorbed by n6-architecture@38d66066"
```

The nexus working branch is `feat/qmirror-cli-programmatic-consumption` (NOT main); commit
will land on that branch. Verify branch alignment before pushing.

## Artifacts

- `/Users/ghost/core/anima/state/crystallography_n6_extraction_2026_05_04/extraction_summary.json` — full audit data
- `/Users/ghost/core/anima/state/crystallography_n6_extraction_2026_05_04/smoke_selftest.log` — self-test output at new location
- `/Users/ghost/core/anima/state/crystallography_n6_extraction_2026_05_04/smoke_atlas.log` — atlas-mode output
- `/Users/ghost/core/anima/state/crystallography_n6_extraction_2026_05_04/handoff.md` — this doc
- `/Users/ghost/core/anima/state/markers/crystallography_n6_extraction_landed.marker` — completion marker

## raw#10 caveats (preserved verbatim from audit)

1. Scoring is subjective; activity-weighted ranking would re-shuffle.
2. Ranking depends on nexus monolith-vs-orchestrator direction.
3. Extraction adds dual-mirror burden (per-repo CHANGELOG + release notes + CI + version-skew risk).
4. Audit may miss hidden coupling channels (sentinel-token namespaces, env-var conventions,
   atlas-absorb chains, hexa-resolver bypass markers, host-pin marker deps).

## Cost

$0 — pure metadata + file move + smoke test. raw#9/15/$0 respected.

## Sister extractions in flight

n6-architecture working tree shows untracked `domains/compute/chip-isa-n6/chip_isa_n6.{hexa,README.md}`
— evidence of a parallel BG extracting Rank 3 (chip_isa_n6) into the same repo. NOT staged or
modified by this BG.
