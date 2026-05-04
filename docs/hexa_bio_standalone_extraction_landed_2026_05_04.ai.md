# hexa-bio standalone extraction — LANDED 2026-05-04

**Cycle**: hexa_bio_standalone_extraction_2026_05_04
**Verdict**: PARTIAL_PASS (1/4 verbs wired; 3/4 stubs)
**Operator directive**: "4개 통합 standalone bg go" (single repo, 4 modules)

## Summary

Extracted the WEAVE module from `nexus/sim_bridge/weave/` into a new standalone
repository `hexa-bio` housing all 4 HEXA-family verbs (WEAVE / NANOBOT /
RIBOZYME / VIROCAPSID). Mirrors the qmirror (v2.0.0, registry L22) +
sim-universe (v1.0.0, registry L23) extraction pattern. hexa-bio is the
**24th** registry entry.

## Outputs

- **Standalone repo**: `/Users/ghost/core/hexa-bio/` (23 files, ~280 LoC README, ~480 LoC CLI router, 4 modules + selftest, 5 tests, 4 examples, install hook, hexa.toml manifest)
- **GitHub**: <https://github.com/need-singularity/hexa-bio> (public, Apache-2.0, initial commit `3877f5e`, branch `main`)
- **HF Hub mirror**: <https://huggingface.co/need-singularity/hexa-bio> (model type, 23 files uploaded, commit `df9a668`)
- **Registry**: `/Users/ghost/core/hexa-lang/tool/pkg/registry.tsv` L24 added
- **Nexus refactor scaffold (4-step, NOT auto-committed)**:
  1. Created `nexus/cli/bio.hexa` (4-tier shellout, ~280 LoC, qmirror v0.3.0 pattern)
  2. Patched `nexus/engine/nexus_cli.hexa` (BIO_CLI const + cmd_bio fn + dispatch arm + help blocks)
  3. Patched `nexus/hexa.toml` (added `hexa-bio = "^1.0.0"` to `[dependencies]`)
  4. Patched `nexus/install.hexa` (added `ensure_runtime_dep("hexa-bio", "^1.0.0")`)
- **Legacy delete script**: `state/hexa_bio_standalone_extraction_2026_05_04/legacy_weave_delete.sh` (DEFERRED — run after smoke verification)

## 4-verb status

| Verb         | Status              | n=6 lattice                      | Empirical sandbox            |
|--------------|---------------------|----------------------------------|------------------------------|
| weave        | **WIRED v1.0.0**    | STRUCTURAL-EXACT (T=1, post 0.97) | cage-assembly ODE + audit    |
| nanobot      | STUB v1.0.0-stub    | hypothesized only                | deferred (cycle 25+)         |
| ribozyme     | STUB v1.0.0-stub    | hypothesized only                | deferred (cycle 25+)         |
| virocapsid   | STUB v1.0.0-stub    | partial (T=1 via weave)          | deferred (T>1: cycle 25+)    |

## Honest C3 caveats (raw#10)

1. **3/4 verbs are stub-only at v1.0.0.** The `__HEXA_BIO_*__ PASS`
   sentinels indicate module load, NOT empirical claim validation.
2. **Falsifier deadlines for stub verbs are initial-guess.** Concrete
   experimental refutation criteria + dates were drafted without
   literature corpus review for nanobot/ribozyme axes. Revision in
   cycle 25+.
3. **n=6 invariant lattice claim is speculative for 3/4 axes.** Only
   weave's σ(6)=12 (T=1 cage vertex count, posterior 0.97) is
   empirically grounded. Nanobot/ribozyme + T>1 virocapsid mappings are
   inherited algebraic conjecture.
4. **Migration of `nexus/sim_bridge/weave/` may break edge-case
   consumers.** Cross-link consumers (n6-architecture papers,
   `nexus/state/audit/cage_assembly_events.jsonl` readers) reference the
   old path. The runs/ ledger (~10MB jsonl) is not vendored into the
   standalone; archival decision deferred to user (delete script handles).
5. **Dual-mirror sync requires HF_TOKEN secret (USER_ACTION pending).**
   `.github/workflows/sync-to-hf.yml` is staged but the secret must be
   added via GitHub → Settings → Secrets and variables → Actions.
   Until then, GitHub canonical only.

## Constraints honored

- **raw#9 STRICT**: All `.hexa` for orchestration; weave's python bridge
  scripts isolated under `modules/_python_bridge/` (raw#9 `.own N` opt-out
  namespace; opt-in only via `HEXA_BIO_WITH_NUMPY=1`).
- **raw#15 (no token leak)**: HF_TOKEN consumed only via GitHub Actions
  secret env; never written to disk.
- **raw#10 (C3 honesty)**: 5 caveats embedded in README + CLI status output
  + each stub module's status block.
- **$0 cost**: public GitHub free + HF Hub free tier.
- **DO NOT auto-commit nexus changes**: 4 nexus tree edits left STAGED
  (`git status` in nexus shows them as modified/untracked).

## Pre-flight checklist (before merging nexus changes + running delete script)

1. `cd /Users/ghost/core/hexa-bio && hexa run cli/hexa-bio.hexa selftest` → expect `__HEXA_BIO_SELFTEST__ PASS`
2. `cd /Users/ghost/core/nexus && hexa run cli/bio.hexa selftest` → expect same PASS via shellout
3. (optional) `HEXA_BIO_WITH_NUMPY=1 hexa run /Users/ghost/core/hexa-bio/cli/hexa-bio.hexa weave --all` → live cage-assembly + Bayesian audit
4. Audit: `rg -n "sim_bridge/weave" /Users/ghost/core/nexus/ -t hexa -t py -t md` to find stale path references
5. Add HF_TOKEN secret to GitHub repo settings (USER_ACTION)
6. Review nexus diffs: `cd /Users/ghost/core/nexus && git diff cli/bio.hexa engine/nexus_cli.hexa hexa.toml install.hexa`
7. Commit nexus changes when ready (suggested message in `legacy_weave_delete.sh` Stage 2)
8. Run `state/hexa_bio_standalone_extraction_2026_05_04/legacy_weave_delete.sh` to remove `nexus/sim_bridge/weave/`

## Cross-links

- Standalone repo: <https://github.com/need-singularity/hexa-bio>
- HF mirror: <https://huggingface.co/need-singularity/hexa-bio>
- Sister marker: `state/markers/qmirror_2_closure_landed.marker`
- Sister marker: `state/markers/sim_universe_standalone_landed.marker` (if present)
- Upstream WEAVE concept SSOT: `n6-architecture/domains/biology/hexa-weave/hexa-weave.md`
