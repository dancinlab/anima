# anima scrub landed — 2026-05-04

## Verdict: ABORT_SCRUB_PRESERVE_DATA

The requested scrub of `anima/anima-agent/` and refactor of consumers to standalone CLI shellout was **aborted before any deletion or commit**. anima/anima-agent/ is the **ORIGIN substrate** that the standalone v1.0.0 was carved from, not a duplicate consumer copy.

## Discovery (BEFORE deletion)

### anima/anima-agent/ identity
- **Not** a separate git repo, **not** a worktree, **not** a symlink
- It is a directly tracked subdirectory of the anima monorepo (`git rev-parse --show-toplevel` → `/Users/ghost/core/anima`)
- 133 files tracked by anima git; 139 files on filesystem
- Contains: 3 top-level `.hexa` entries (`anima_agent.hexa`, `autonomy_loop.hexa`, `autonomy_live.hexa`), `hexa/` subdir (38 .hexa modules), `dashboard/` (Next.js), `employee/`, `trading/`, `plugins/`, `providers/`, `channels/`, `skills/`, `build/`, `results/`, `data/`, `.py` legacy + `.hexa` migrations

### Standalone identity
- `/Users/ghost/core/anima-agent/` is a **separate git repo** with remote `https://github.com/dancinlab/anima-agent.git` (v1.0.0, single commit `106f2b6 feat(anima-agent v1.0.0): standalone extraction from anima`)
- `hexa.toml` provenance line: `Provenance: extracted from anima/anima-agent/ on 2026-05-04`
- 146 files; clean `modules/` namespace + `cli/` + `tests/` + `examples/`

### Tree divergence (`diff -rq`)
- 43 entries differ at top level
- Standalone-only top entries: `cli/`, `modules/`, `tests/`, `examples/`, `LICENSE`, `CHANGELOG.md`, `RELEASE_NOTES_v1.0.0.md`, `hexa.toml`, `install.hexa`, `.gitignore`, `.github/`
- Legacy-only top entries (~30): `anima_agent.hexa`, `autonomy_live.hexa`, `autonomy_loop.hexa`, `consciousness_features.hexa`, `dashboard_bridge.hexa`, `discovery_loop.hexa`, `ecosystem_bridge.hexa`, `llm_claude_adapter.hexa`, `metrics_exporter.hexa`, `philosophy_lenses.hexa`, 8 test_*.hexa, `build/`, `dashboard/`, `data/`, `docs/`, `employee/`, `hexa/` (38 modules), `results/`, `trading/`, `Dockerfile`, `.env.example`, `.hypothesis_bridge_state.json`, `llm_claude_adapter_SCOPE.md`
- The trees are **largely disjoint at the top level** — the standalone is a curated subset wrapped in clean structure, not a mirror

## Consumer audit

Searched `import|use` directives across all `*.hexa` and `*.toml` in anima (excluding `.git/`, `.claude/worktrees/`):

| Standalone package | Real `import "<pkg>"` consumers in anima | Refactor needed |
|---|---|---|
| anima-agent | **0** (it IS the source, not a consumed library) | N/A |
| qmirror | 0 | N/A |
| sim-universe | 0 | N/A |
| hexa-bio | 0 | N/A |
| honesty-monitor | 0 | N/A |
| qrng | 1 (`anima/modules/rng/anu.hexa` → `use "stdlib/qrng_anu"`) | Stdlib path, not the standalone qrng pkg |
| mc-integrate | 0 | N/A |

**No anima consumer of any of the 7 standalone packages exists as an inline import.** The cross-references are all roadmap pointers + narrative anchors + cross-repo nexus dependencies. There is nothing to refactor to CLI shellout in anima today.

## Why scrub aborted

1. **`.roadmap.anima_agent` (active, since 2026-05-03)** verifier paths point at the legacy dir:
   - `anima-agent/anima_agent.hexa`
   - `anima-agent/hexa/anima_agent_core.hexa`
   - `anima-agent/hexa/anima_agent_full.hexa`
   - `anima-agent/llm_claude_adapter.hexa`
   - `anima-agent/test_claude_smoke.hexa`
   - `anima-agent/autonomy_loop.hexa` + `autonomy_live.hexa`
   - Open blockers: `anima_agent.blk.1` (3-entry canonicalization), `anima_agent.blk.2` (sister W1 dependency)
   - Deleting the dir orphans the SSOT.
2. **~60 unique files** in legacy not in standalone — `dashboard/`, `employee/`, `trading/`, `build/`, `results/`, `.py` legacy, `plugins/`, `providers/`, `channels/`, `skills/` — deletion = data loss.
3. **Standalone `hexa.toml` itself confirms** it is the derivative ("extracted from anima/anima-agent/ on 2026-05-04"), so the legacy dir is the source of truth.
4. **Zero inline import consumers** — there is no consumer pattern to migrate to `${HX_HOME:-$HOME/.hx}/bin/anima-agent` shellout. The refactor target set is empty.
5. **~25 in-flight uncommitted modifications** (P9 pipeline, qmirror docs, config/h100_pods.json, ready submodule). A scrub commit on `main` would risk mixing with unrelated active work; per task constraints `git add -A` is forbidden and only targeted paths are allowed.

## Five caveats (raw#10)

1. anima/anima-agent/ contains ~60 unique files (dashboard, employee, trading, build, results, .py legacy) NOT present in standalone — deletion = irrecoverable in-tree data loss
2. `.roadmap.anima_agent` (active 2026-05-03) verifier paths point at legacy dir — deletion would orphan the active SSOT
3. standalone `hexa.toml` provenance line confirms it was extracted FROM legacy dir (not vice versa) — direction of derivation matters
4. zero `import "anima_agent"` consumers in anima codebase — there is nothing to refactor to CLI shellout
5. ~25 in-flight uncommitted modifications (P9, qmirror docs) — even a targeted scrub commit risks mixing with unrelated work

## Sister BG (nexus) coordination

Sister BG owns `/Users/ghost/core/nexus/` — not touched. No cross-repo dependency requiring nexus changes was discovered in this audit. No handoff file needed at `state/anima_scrub_2026_05_04/handoff_to_nexus.md`.

## Recommended next steps (user decision required)

**Option A — Hard-cut to standalone (high-effort, high-cleanliness):**
1. Port unique legacy components (dashboard, employee, trading, plugins, providers, channels, skills, build artifacts) into standalone `modules/` namespace
2. Re-point `.roadmap.anima_agent` verifier paths from `anima-agent/...` to `hx run anima-agent --selftest` (or `${HX_HOME:-$HOME/.hx}/bin/anima-agent` 4-tier resolver)
3. Land `anima_agent.blk.1` (3-entry SSOT canonicalization) inside the standalone first
4. Then `git rm -r anima-agent/` in anima

**Option B — Defer scrub (low-risk, recommended now):**
1. Keep anima-agent in-tree as legacy substrate
2. Treat standalone v1.0.0 as the **publishable distribution surface** (not the working substrate)
3. Resolve `anima_agent.blk.1` (3-entry canonicalization) and `anima_agent.blk.2` (W1 residual decision) first
4. Revisit scrub after SSOT canonicalization lands

**Recommended (완성도 lens):** Option B. Option A's port is multi-cycle work and the standalone is only 1 day old (2026-05-04). Premature scrub destroys substrate.

## Artifacts

- `state/anima_scrub_2026_05_04/audit.json` — full per-package audit + 5 caveats
- `state/markers/anima_scrub_landed.marker` — landing marker (ABORT verdict)
- `docs/anima_scrub_landed_2026_05_04.ai.md` — this file

No commits made. No files deleted. In-flight uncommitted state preserved untouched.
