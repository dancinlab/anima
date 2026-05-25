# Submodule Cleanup Plan — 2026-05-04

**Owner**: BG-η (parallel BG run, parent serializes commits at end)
**Scope**: `ready/` (top-level) + `references/tribev2/` (sibling)
**Mode**: READ-ONLY investigation. NO git mutation, NO submodule mutation. This is a *plan*, not an *execution*.
**Targets** (the only paths flagged for submodule resolution):
- ` m ready` — dirty submodule (lowercase `m` in `git status`)
- `?? references/tribev2` — untracked-marker for a path with a tracked gitlink but no `.gitmodules` entry (raw `git status -s` shows ` ? references/tribev2`)

Bonus discovery: parent repo carries **6** ghost gitlinks under `references/`, not just `tribev2` — see §1.3.

---

## 1. Inventory

### 1.1 `ready/` — top-level dirty submodule

| Field | Value |
|---|---|
| HEAD gitlink (parent records) | `ef7aae81f41c9f9011ba2263ead2384b9fc71f9b` |
| Working-tree commit (`ready/.git` HEAD) | `ef7aae81f41c9f9011ba2263ead2384b9fc71f9b` |
| Working-tree branch | `ssot-hexa-first-fix` |
| Other local branches | `main`, `worktree-agent-abb59ac1` |
| Origin URL (inside ready) | `https://github.com/dancinlab/anima.git` |
| Origin URL (parent repo) | `https://github.com/dancinlab/anima.git` |
| Listed in `.gitmodules`? | **NO** (`.gitmodules` does not exist in parent) |
| Listed in `.git/config` `submodule.*`? | **NO** |
| Reachable via `git submodule status`? | **NO** — fatal: "no submodule mapping found in .gitmodules for path 'ready'" |
| Worktree count | 1 worktree (`ready/.git/worktrees/agent-abb59ac1`) |

**Why parent records it**: parent commits like `093d45407 chore(ready): bump submodule — 13 implicit-return fixes (codegen_c2)` and `a1b111193 chore(ready): bump submodule — hot-path arr.push 29 sites (≥93x)` show the gitlink has been bumped via direct `git update-index --cacheinfo` style operations (or `git add ready` with the 160000 mode preserved), bypassing the `.gitmodules` registration step entirely.

**Working-tree dirty status (sample)**:
- 7 modified files: `.DS_Store`, `anima/.DS_Store`, `anima/experiments/evolution/infinite_evolution.py`, `anima/modules/agent/philosophy_lenses.py`, `anima/tests/tests.hexa`, `experiments/acceleration_bm3_mamba_ssm.py`, `scripts/infinite_growth.sh`
- 40 deletions: virtually all `CLAUDE.md` files (`anima/CLAUDE.md`, `anima/archive/CLAUDE.md`, `anima/engines/CLAUDE.md`, `anima/measurement/CLAUDE.md`, `bench/CLAUDE.md`, `checkpoints/CLAUDE.md`, `data/CLAUDE.md`, `docs/CLAUDE.md`, `docs/hypotheses/{ce,cx,dd,evo,genesis,hw,inf,omega,phys,se,sing,sl,three,topo,tp}/CLAUDE.md`, `scripts/CLAUDE.md`, `tests/CLAUDE.md`, `training/CLAUDE.md`, etc.) + `core/ROADMAP.md` + 3 `data/conscious-lm*/memory.json.bak`
- 10 untracked: `anima/anima-rs/`, `anima/config/`, 6× `anima/modules/*/README.ai.md`, `state/`, `tests/hyperarithmetic_suite_runner.hexa`
- **0 staged files** — all changes are working-tree-only.

**Inferred purpose**: `ready/` is a peer clone of `dancinlab/anima.git` checked out to a feature branch `ssot-hexa-first-fix`. The dirty changes look like a coherent in-progress branch ("delete legacy CLAUDE.md scaffolding + py→hexa migration WIP") matching the branch name. The mass `D CLAUDE.md` is **likely intentional** (consistent pattern, nearly all CLAUDE.md files in the tree). The active worktree (`agent-abb59ac1`) suggests an agent session has touched this clone recently.

### 1.2 `references/tribev2/` — untracked-marker submodule

| Field | Value |
|---|---|
| HEAD gitlink (parent records) | `1731059aa7d6b87f9abd0e4ed152a76a196e8846` |
| Working-tree commit (`references/tribev2/.git` HEAD) | `1731059aa7d6b87f9abd0e4ed152a76a196e8846` |
| Working-tree branch | `docs/anima-integration-addendum-2026-05-02` |
| Origin URL | `https://github.com/facebookresearch/tribev2.git` |
| Fork remote URL | `https://github.com/dancinlife/tribev2.git` (user's fork) |
| Listed in `.gitmodules`? | **NO** (file does not exist) |
| Working-tree dirty | 3 untracked: `ANIMA_INTEGRATION_PROPOSAL.md`, `SUMMARY_KR.md`, `inventory.json` |
| Working-tree dirty (tracked) | 0 modifications, 0 deletions |
| Top commit subject | `docs: anima integration proposal addendum (Framing D 3-way bridge)` |
| Local-only commits ahead of `origin/main` | 1 (the addendum commit on a fork branch) |

**Inferred purpose**: TRIBE v2 vendored reference for the BLM (Brain LM) phase-3 cond.3 work. Confirmed via:
- `.roadmap.blm_brain_lm` cond.1 evidence: "TRIBE v2 baseline 활용", "177.21M params + 20484 vertices", explicit `references/tribev2/inventory.json` reference
- `.roadmap.i1_tribev2_pr` cond.1/cond.2 (sister roadmap, fork commit + PR #60 OPEN)
- `docs/submodule_tribev2_commit_2026_05_02.md` — addendum landed at upstream-fork commit `86ed4804`, parent gitlink **was** updated to `86ed480` per that doc, but current parent HEAD records `1731059aa` — meaning parent was bumped **further** to a newer addendum on `docs/anima-integration-addendum-2026-05-02`

**Note on the `?` status**: `git status -s` shows ` ? references/tribev2` (single-question, not `??`). This is git's compact display for a *tracked* submodule whose `.gitmodules` entry is missing — git knows the gitlink, knows the worktree commit matches, but cannot resolve the URL/path mapping.

### 1.3 Bonus: 5 sibling ghost-gitlinks under `references/`

`git ls-tree HEAD references/` reveals **6** gitlinks total at `references/`:

| Path | Gitlink commit |
|---|---|
| `references/Documentation` | `ae741b4e4e39970089e652bfdf39651b688a80ed` |
| `references/OpenBCI_Cyton_Library` | `24e1c4269b60c3bec6d831bca03cae42f267b3c6` |
| `references/OpenBCI_GUI` | `e23869e7b5cc621e733d8fa0d81f05d477264306` |
| `references/OpenBCI_Tutorials` | `a9d60c75e8606a8a412a12bb0aa7c54b154a10d8` |
| `references/V3_Hardware_Design_Files` | `6bce559c7ca6e8b4a440b557c6c7173f99612a67` |
| `references/tribev2` | `1731059aa7d6b87f9abd0e4ed152a76a196e8846` |

None are in `.gitmodules`. None are in `.git/config`. The 5 OpenBCI/Documentation/V3 siblings are not flagged in current `git status` only because their working-tree commits already match the gitlink and they have no untracked files git would surface. **Any submodule cleanup plan that doesn't address these will be partial.**

---

## 2. Risk Assessment (per submodule)

### 2.1 `ready/`

| Action | What gets lost | Severity |
|---|---|---|
| `git submodule update --force ready` | Would error (no .gitmodules); even if forced, would discard 7 modified files + 40 deleted files + 10 untracked. Active worktree `agent-abb59ac1` would be orphaned. | **HARD-DESTRUCTIVE** |
| `git submodule deinit ready` | Would error (no .gitmodules). If `.gitmodules` were synthesized first then deinit run, the entire `ready/` directory would be removed (including untracked `state/`). | **HARD-DESTRUCTIVE** |
| `git rm --cached ready` then re-add as plain dir | Loses gitlink reference (parent would need to commit ~thousands of files); blows up parent repo size. | **HIGH** (size + history pollution) |
| Defer (do nothing) | Status stays `m`. Parent commits keep using "chore(ready): bump submodule" pattern. No data loss. **However**, future `git clone --recursive` of parent will silently skip `ready/` (no .gitmodules → nothing to recurse). | **LOW-NOW / MEDIUM-LATER** (clone-time silent skip) |
| Add `.gitmodules` entry codifying current state | Synthesizes the missing metadata; preserves working tree, preserves dirty changes. Risk: if URL/path mapping is wrong, future `submodule update --init` could clone a different ref. | **LOW** (with verification) |

**User in-progress work risk**: HIGH for `ready/`. The `ssot-hexa-first-fix` branch + `agent-abb59ac1` worktree contain WIP not pushed to `origin` (per `git log origin/main..HEAD` not run here as worktree state is separate). Mass `D CLAUDE.md` could be a deliberate cleanup or accidental — **cannot be confirmed read-only**.

### 2.2 `references/tribev2/`

| Action | What gets lost | Severity |
|---|---|---|
| `git submodule update --force references/tribev2` | Would error (no .gitmodules). | N/A |
| `git rm --cached references/tribev2` then re-add as plain dir | Loses gitlink reference. Would commit ~5.6 MB of vendored TRIBE v2 code into parent. Pollutes BLM cross-link evidence chain. | **HIGH** (BLM roadmap evidence break) |
| Defer (do nothing) | Status stays `?`. Same clone-time silent-skip risk. BLM phase-3 cond.3 evidence still relies on the `references/tribev2/inventory.json` and vendored `tribev2/{model.py,pl_module.py,main.py,utils_fmri.py}`. | **LOW-NOW** |
| Add `.gitmodules` entry codifying current state | Resolves the `?` marker. Preserves the 1 local-only fork-branch commit. Required: encode `url = https://github.com/facebookresearch/tribev2.git` (origin) — but user's local has fork as primary. Need to choose URL semantics. | **LOW-MEDIUM** (URL choice = decision) |
| `git rm --cached + git add as nested git dir` | Same as above without the gitlink. | **HIGH** |

**User in-progress work risk**: MEDIUM. The 3 untracked files (`ANIMA_INTEGRATION_PROPOSAL.md`, `SUMMARY_KR.md`, `inventory.json`) are referenced by `.roadmap.blm_brain_lm` evidence chain — they MUST exist on disk for that roadmap to remain valid. The branch `docs/anima-integration-addendum-2026-05-02` carries the PR #60 commits.

---

## 3. Recommended Resolution Path (ranked by 완성도 lens)

### 3.1 `ready/` — RECOMMENDED: **Option A** (defer + status-quo gitlink)

| Option | Description | 완성도 | Cost | Reversible? |
|---|---|---|---|---|
| **A. Defer + add .gitignore noise filter** ⭐ | Leave `ready/` as a ghost-gitlink. Document the pattern in `state/submodule_cleanup_plan_2026_05_04/plan.md`. Optionally add `.gitattributes` or status-noise filter to suppress the ` m ready` marker locally. | **HIGH** (preserves all WIP) | $0, 0 min | YES |
| B. Add `.gitmodules` entry retroactively | Synthesize `[submodule "ready"] path = ready, url = https://github.com/dancinlab/anima.git, branch = ssot-hexa-first-fix`. Keep working-tree as-is. | MEDIUM (codifies but doesn't push WIP) | $0, ~5 min | YES (rm .gitmodules) |
| C. `git submodule deinit` + re-init from upstream main | Loses 57 dirty entries + active worktree. | LOW | $0, ~10 min | NO (data loss) |
| D. Full reset (`git -C ready reset --hard origin/main`) | Loses 57 dirty entries. Worktree survives. | LOW | $0, ~2 min | NO (data loss) |

**Recommendation: A**. The ghost-gitlink works *de facto* (parent commits keep bumping it). Promoting to `.gitmodules` (Option B) is the only completeness improvement, but creates a new failure mode: `git clone --recursive` would attempt to fetch `dancinlab/anima.git` recursively, which would re-clone the parent repo into `ready/`. That's the same upstream — semantically correct but operationally weird. Defer until the user decides whether `ready/` should be a true submodule (clone of self) or a separate vendored fork.

### 3.2 `references/tribev2/` — RECOMMENDED: **Option B** (codify .gitmodules)

| Option | Description | 완성도 | Cost | Reversible? |
|---|---|---|---|---|
| A. Defer | Leave as ghost-gitlink. `?` marker stays. | LOW (raw#71 falsifier perma-fail) | $0, 0 min | YES |
| **B. Add `.gitmodules` entry** ⭐ | Create `.gitmodules` with `[submodule "references/tribev2"] path = references/tribev2, url = https://github.com/facebookresearch/tribev2.git`. Optionally add the 5 sibling references entries simultaneously to fully resolve the references/ tree. | **HIGH** (resolves `?` + clone-time correctness) | $0, ~10 min | YES (rm .gitmodules) |
| C. `git rm --cached references/tribev2` + commit as plain dir | Pollutes parent with 5.6 MB. Breaks BLM roadmap evidence semantics. | LOW | $0, ~5 min | partial |
| D. `git submodule deinit` + force re-init | Loses the 1 local-only fork-branch commit (`1731059`). | LOW | $0, ~10 min | NO (data loss) |

**Recommendation: B**. The gitlink + working-tree commit already match. Adding `.gitmodules` is purely additive metadata. URL choice: use `origin` (`facebookresearch`) not `fork` (`dancinlife`) — because future contributors should clone from canonical upstream. The user's fork remote stays as a local-only setup. Same `.gitmodules` cycle should also register the 5 sibling references (Documentation, OpenBCI_*, V3_Hardware_Design_Files) to fully resolve the ghost-gitlink class.

---

## 4. Pre-Execution Checklist

Before any user-authorized fix:

1. **Backup `ready/`**:
   - `tar -czf state/submodule_cleanup_plan_2026_05_04/ready_backup_$(date +%s).tgz ready/` (preserves dirty + untracked + worktree)
   - Confirm: untracked `state/` inside `ready/` may be large — check size first with `du -sh ready/state` before tar
2. **Backup `references/tribev2/`**:
   - `tar -czf state/submodule_cleanup_plan_2026_05_04/tribev2_backup_$(date +%s).tgz references/tribev2/` (preserves the 3 untracked files + branch state)
3. **Verify upstream URLs**:
   - `cd ready && git remote -v` → confirms `dancinlab/anima.git`
   - `cd references/tribev2 && git remote -v` → confirms `facebookresearch/tribev2.git` + `dancinlife/tribev2.git`
4. **Verify gitlink commits resolvable upstream**:
   - `cd ready && git fetch origin && git cat-file -e ef7aae81 || echo "MISSING"` (gitlink may be on a feature branch only)
   - `cd references/tribev2 && git fetch origin && git fetch fork && git cat-file -e 1731059aa || echo "MISSING"`
5. **Confirm no in-flight work**:
   - User confirms the `D CLAUDE.md` mass-deletion in `ready/` is intentional (or dismisses)
   - User confirms the 3 untracked files in `references/tribev2/` are committed elsewhere or safely vendored
6. **Snapshot `git status --short`** at execution time to compare against falsifiers post-execution
7. **Race isolation**: any execution cycle MUST hold a writer lock on `ready/` AND `references/tribev2/` — no parallel agent sessions touching those paths

---

## 5. Falsifier Set (raw#71)

Pre-registered acceptance criteria for any executed cleanup:

- **F-SUBMOD-1**: `git submodule status` returns clean state for both `ready` and `references/tribev2` (and ideally for the 5 sibling references too) — exit code 0, no `fatal:` output, status chars all space (clean) or `+` (gitlink-bumped intentionally)
- **F-SUBMOD-2**: `cat .gitmodules` lists at minimum `ready` and `references/tribev2`; bonus: lists all 6 references siblings
- **F-SUBMOD-3**: `git status --short | grep -E '(^.m |^\?\? references|^ \? references)'` returns empty (no dirty submodule marker, no untracked references entry)
- **F-SUBMOD-4**: round-trip `git clone --recursive https://github.com/dancinlab/anima.git /tmp/anima_clone_test && ls /tmp/anima_clone_test/ready/ && ls /tmp/anima_clone_test/references/tribev2/` succeeds — both submodules populate from `.gitmodules`-declared URLs
- **F-SUBMOD-5** (bonus completeness): `cd /tmp/anima_clone_test && git submodule foreach 'git status --short' | wc -l` returns 0 — clean state across all registered submodules
- **F-SUBMOD-6** (preservation): the 7 modified files + 40 deletions + 10 untracked entries inside `ready/` are preserved (compared against pre-execution snapshot via `diff`); the 3 untracked files inside `references/tribev2/` survive
- **F-SUBMOD-7** (roadmap integrity): `.roadmap.blm_brain_lm` cond.1 evidence paths still resolve — `references/tribev2/inventory.json` exists with same SHA-256

---

## 6. Honest C3 Caveats (raw#10)

1. **Cannot determine user intent for `ready/` dirty changes**: the 40 `D CLAUDE.md` deletions look intentional (uniform pattern), but read-only investigation cannot confirm. The branch name `ssot-hexa-first-fix` is suggestive but not authoritative. **A wrong assumption here loses real WIP.**
2. **Active worktree `ready/.git/worktrees/agent-abb59ac1`**: there is at least one active git worktree inside `ready/`. We did not inspect what's checked out there or whether an agent session is currently writing to it. Any submodule mutation that touches `ready/` while the worktree is active risks index corruption.
3. **Submodule semantic ambiguity for `ready/`**: `ready/` clones the *same* upstream as the parent repo (`dancinlab/anima.git`). This is a self-recursive submodule. Whether the user intends this as (a) a sibling clone for cross-version diffing, (b) a stage area for upstream PRs, or (c) a legacy artifact to remove is undetermined.
4. **Irreversibility risk in any `git rm --cached` path**: removing the gitlink and re-adding as a plain dir would inflate the parent repo by ~5.6 MB (tribev2) + ~hundreds of MB (ready/), and this commit would be permanent in history. Recovery would require `git filter-repo` rewriting — a hard operation that affects all contributors.
5. **Cross-cycle dependencies**: `.roadmap.blm_brain_lm` cond.1, `.roadmap.i1_tribev2_pr` cond.1/cond.2, `docs/submodule_tribev2_commit_2026_05_02.md`, `docs/strategic_clm_phase_a1_results_2026_05_01.md`, `docs/n_substrate_consciousness_roadmap_2026_05_01.md`, `docs/blm_phase3_spec_2026_05_03.md` all reference `references/tribev2/` paths. Any cleanup must verify all these cross-links survive.
6. **5 sibling ghost-gitlinks not in scope**: this plan focuses on `ready/` and `references/tribev2/` per the brief, but `references/{Documentation, OpenBCI_Cyton_Library, OpenBCI_GUI, OpenBCI_Tutorials, V3_Hardware_Design_Files}` have the same ghost-gitlink pathology. Resolving only `tribev2` leaves a partial fix and F-SUBMOD-5 will fail.
7. **`.gitmodules` was never committed in repo history**: `git log -- .gitmodules` returns empty across all branches. This means the ghost-gitlink pattern is not a regression from a deleted `.gitmodules` — it has *always* been the case. There is no "restore from history" option. Any fix is greenfield metadata creation.
8. **Read-only constraint prevented**: confirming gitlink commits exist on the respective upstream remotes (would need `git fetch`); confirming `agent-abb59ac1` worktree state; confirming the precise contents of the untracked `state/` dir inside `ready/` (could be hundreds of MB).

---

## 7. Decision Matrix

| Submodule | Option | Cost | Risk | 완성도 | Reversible | Recommendation |
|---|---|---|---|---|---|---|
| `ready/` | A. Defer + status-quo | $0, 0 min | LOW | HIGH | YES | ⭐ **TOP** |
| `ready/` | B. Add .gitmodules entry | $0, ~5 min | LOW | MEDIUM-HIGH | YES | secondary |
| `ready/` | C. deinit + re-init | $0, ~10 min | HIGH (data loss) | LOW | NO | reject |
| `ready/` | D. reset --hard | $0, ~2 min | HIGH (data loss) | LOW | NO | reject |
| `references/tribev2/` | A. Defer | $0, 0 min | LOW now / MED later | LOW | YES | secondary |
| `references/tribev2/` | B. Add .gitmodules entry | $0, ~10 min | LOW | HIGH | YES | ⭐ **TOP** |
| `references/tribev2/` | C. rm --cached + commit | $0, ~5 min | HIGH (5.6MB pollution) | LOW | partial | reject |
| `references/tribev2/` | D. deinit + force re-init | $0, ~10 min | HIGH (loses 1731059) | LOW | NO | reject |

**Combined top-recommendation cycle (deferred — user authorization required)**:
1. Backup both submodules to `state/submodule_cleanup_plan_2026_05_04/*.tgz`
2. Synthesize `.gitmodules` with **6 entries** for `references/{Documentation,OpenBCI_Cyton_Library,OpenBCI_GUI,OpenBCI_Tutorials,V3_Hardware_Design_Files,tribev2}` using the upstream URLs (still need to discover URLs for the 5 OpenBCI siblings via the gitlink commit objects — likely `OpenBCI/*` GitHub orgs)
3. Optionally also register `ready` (decide self-clone semantics first)
4. Run `git submodule sync && git submodule absorbgitdirs` to migrate the embedded `.git` dirs into `.git/modules/`
5. Validate F-SUBMOD-1 through F-SUBMOD-7
6. Single commit `chore(submodules): codify .gitmodules + absorb 6 references gitlinks (cleanup plan 2026-05-04)`

**Cost band for top-recommendation execution**: $0, ~30-45 min wall, includes backup + URL discovery for 5 siblings + .gitmodules synthesis + absorbgitdirs + validation + commit. Single mid-priority cycle.

---

## 8. Out-of-Scope / Punted

- Resolving the 5 sibling ghost-gitlinks under `references/` (Documentation, OpenBCI_*, V3_Hardware_Design_Files) — recommended to handle in same cycle but not strictly in this plan's brief.
- Decision on `ready/` self-clone semantics (cycle gating) — needs user input.
- The active worktree `ready/.git/worktrees/agent-abb59ac1` lifecycle — separate cycle.
- Per-file audit of the 40 `D CLAUDE.md` deletions in `ready/` — needs user confirmation of intent.
- The 7 modifications in `ready/` to `.py` files (`infinite_evolution.py`, `philosophy_lenses.py`, `acceleration_bm3_mamba_ssm.py`) — user-feedback `py -> hexa only` mac-strict raw#9 conflict if these are stale untranslated `.py` files in a hexa-only working area. Out of submodule scope but flagged.

---

**End of plan.** Total LoC ~290.
