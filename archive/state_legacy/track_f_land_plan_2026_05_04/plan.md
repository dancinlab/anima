# Track F land plan — .own opt-out namespace (cycle 1)

**ts_utc**: 2026-05-04T01:12:50Z
**Verdict**: **COMMIT_READY** (6 files to stage, 1 file to exclude by-spec)
**Cycle dir**: `state/track_f_land_plan_2026_05_04/`
**Parent action required**: execute the recommended `git add` + `git commit` (see §6).

This BG is **READ-ONLY** vs Track F source. No source files modified.

---

## 1. Track F scope (file list + sizes)

| path | LoC | status | stage? |
|---|---:|---|---|
| `.gitignore` | +12 | modified | YES |
| `docs/anima_dot_own_namespace_spec_2026_05_03.md` | 290 | untracked | YES |
| `docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md` | 149 | untracked | YES |
| `tool/transient_py/.gitignore` | 29 | untracked | YES |
| `tool/transient_py/.gitkeep` | 0 | untracked | YES |
| `tool/transient_py/README.md` | 62 | untracked | YES |
| `tool/transient_py/atp_pytorch.py` | 645 | gitignored | **NO** (by-spec) |

**Total stageable**: 6 files, ~542 LoC of tracked content + 12 LoC delta on `.gitignore`.

---

## 2. raw#9 exemption analysis per file

### 2-1. Spec / docs / metadata files (6 of 7)

All non-`.py` — no raw#9 concern. Markdown spec docs + dotfiles + dir-keeper are policy + scaffold, not source code.

### 2-2. `tool/transient_py/atp_pytorch.py` (645 LoC, the only `.py`)

**Decision**: `EXEMPT_BUT_GITIGNORED_BY_DESIGN`.

- Header line 1 declares `# .own 2  auto-gen-pytorch-port` (canonical level-2 artifact).
- Header lines 9-12 declare `Generator: HAND-PORT (Phase 1 of Track A2->A escalation)` — i.e. it's a hand-port of `anima-voice/audio_token_predictor.hexa` (1576 LoC source), serving as the "first real `.own 2`" placeholder until Track A transpiler (`tool/atp_to_pytorch.hexa`) auto-generates it.
- Header line 19-21: `Policy: raw#9 hexa-only (Mac canonical = .hexa); this .py exists only in tool/transient_py/ and is gitignored (see .gitignore). Human edits = raw violation.`

**Per spec doc §4 lifecycle item 5** (`docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md` line 48 echo): **"No file in this namespace is committed"**.

Three-layer enforcement:
1. Root `.gitignore` line 3: `**/*.py` (global ban)
2. Root `.gitignore` line 235: `tool/transient_py/*.py` (namespace-explicit, redundant-by-design)
3. `tool/transient_py/.gitignore` line 22: `*.py` (namespace-local, redundant-by-design)

`git check-ignore` confirms: `tool/transient_py/.gitignore:22:*.py	tool/transient_py/atp_pytorch.py` — file IS ignored.

`git add tool/transient_py/` (no `-f`) naturally excludes it. **No manual exclusion required**; gitignore + spec semantics align.

---

## 3. `.gitignore` diff review (semantic check)

```
+# tool/transient_py/ — auto-generated python namespace (.own 2/3/4)
+# Spec: docs/anima_dot_own_namespace_spec_2026_05_03.md
+# Policy: *.py here are gitignored (regeneratable from .hexa transpiler).
+#         The directory is preserved via .gitkeep + README.md + .gitignore.
+# Note: REDUNDANT with `**/*.py` ban above — kept here as documentation
+# anchor so future audits find the policy at the namespace declaration site.
+tool/transient_py/*.py
+tool/transient_py/__pycache__/
+!tool/transient_py/.gitkeep
+!tool/transient_py/.gitignore
+!tool/transient_py/README.md
```

**Validation**:

- **Syntax**: valid gitignore (glob + negation patterns).
- **Redundancy**: explicitly disclosed in comment line "REDUNDANT with `**/*.py` ban above". This is honest C5 (raw 91 explicit-over-implicit) — kept for audit traceability at the declaration site.
- **Negation correctness**: `!tool/transient_py/.gitkeep` etc. are technically belt-and-suspenders. The global `**/*.py` matches `*.py` only; `.gitkeep`, `.gitignore`, `README.md` are NOT matched, so they pass through naturally. The negation patterns serve only as readability anchors.
- **No conflict with `atp_pytorch.py` policy**: spec wants `*.py` ignored; pattern matches → correct.
- **No accidental whitelist of `.py`**: no `!*.py` anywhere — `atp_pytorch.py` stays ignored.

**Conclusion**: gitignore additions are semantically correct, redundant-by-design (disclosed), and consistent with spec.

---

## 4. Cross-reference with memory `feedback_dot_own_opt_out_system.md`

Memory expects: *"anima `.own N` taxonomy + raw#37 transient sister-rule + tool/transient_py/ namespace; formal opt-outs from py->hexa rule"*.

| memory element | implemented? | evidence |
|---|---|---|
| `.own N` taxonomy | YES (informal) | spec §3 (4 levels: 1/2/3/4) |
| raw#37 transient sister-rule | acknowledged | spec §1-1 cross-link to `state/.X_helper.py` ~25 helpers |
| `tool/transient_py/` namespace | YES (scaffold) | dir + .gitkeep + .gitignore + README.md |
| formal opt-outs from py→hexa rule | DEFERRED | informal cycle-1 land; formal `anima/.own own N` entry awaits Track A transpiler first artifact |

**Memory feedback honored**, with explicit deferral disclosure for the formal-ratification step. This is C3-honest scope discipline (raw#20 own-monotonic — don't codify until validated).

---

## 5. Cross-BG non-overlap audit

This BG runs in parallel with BG-omega and BG-Beta:

| BG | scope | overlap with F? |
|---|---|---|
| BG-omega | `tool/p9_path_b_hellaswag_eval.hexa` etc | None (different file family) |
| BG-Beta | `tool/transient_py/clm_v4_hf_format_shim.py` + `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_*` | **Touches F's namespace dir** — but Beta's `.py` is gitignored by F's policy (correct by design). No staged-file overlap. |

**Sequence**: F **must land BEFORE** Beta's commit if Beta's commit also touches `tool/transient_py/` metadata. If Beta only adds a gitignored `.py`, no commit conflict (Beta has no staged-file delta in F's namespace).

**Recommendation**: parent should commit F first, then Beta — to ensure Beta's BG run sees the policy already landed (not just locally-uncommitted).

---

## 6. Commit boundary recommendation

**Single combined commit** — all 6 files share one purpose (formalize `.own` opt-out namespace) and one cycle date (2026-05-03 work landing on 2026-05-04).

**Subject**:
```
chore(.own opt-out namespace 2026-05-03): tool/transient_py/ scaffold + .gitignore policy + spec docs
```

**Body** (parent should adapt):
```
Formalize the .own N taxonomy (1=grandfathered / 2=transpiler auto-gen / 3=raw#37 transient / 4=test fixtures) with informal cycle-1 land: namespace dir scaffold (.gitkeep + .gitignore + README.md), root .gitignore +12 LoC policy block, and 290+149 LoC spec docs.

atp_pytorch.py (.own 2 first artifact, 645 LoC hand-port pre-Track-A) intentionally NOT staged — per spec lifecycle, transpiler-output .py are regeneratable and gitignored; only namespace metadata + spec are tracked. Formal anima/.own own N entry deferred to cycle 2 after Track A transpiler emits first real .own 2 artifact.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### Suggested ready-to-execute command (parent runs)

```bash
cd /Users/ghost/core/anima
git add \
  .gitignore \
  docs/anima_dot_own_namespace_spec_2026_05_03.md \
  docs/anima_dot_own_namespace_spec_landed_2026_05_03.ai.md \
  tool/transient_py/.gitignore \
  tool/transient_py/.gitkeep \
  tool/transient_py/README.md
# Verify atp_pytorch.py is NOT staged:
git status --short tool/transient_py/  # should show only the 3 metadata files
git diff --cached --stat               # should show 6 files, ~553 LoC
git commit -m "$(cat <<'EOF'
chore(.own opt-out namespace 2026-05-03): tool/transient_py/ scaffold + .gitignore policy + spec docs

Formalize the .own N taxonomy (1=grandfathered / 2=transpiler auto-gen / 3=raw#37 transient / 4=test fixtures) with informal cycle-1 land: namespace dir scaffold (.gitkeep + .gitignore + README.md), root .gitignore +12 LoC policy block, and 290+149 LoC spec docs. atp_pytorch.py (.own 2 first artifact, 645 LoC hand-port pre-Track-A) intentionally NOT staged per spec lifecycle. Formal anima/.own own N entry deferred to cycle 2 after Track A transpiler first real artifact.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**Pre-flight verifications** (parent should run before commit):
1. `git status --short tool/transient_py/` → expect 3 lines (`.gitignore`, `.gitkeep`, `README.md` only — NOT `atp_pytorch.py`).
2. `git diff --cached --stat` after `git add` → expect exactly 6 files.
3. `git ls-files --others --exclude-standard tool/transient_py/` → after staging should be empty.

---

## 7. Honest C3 caveats (raw#10, ≥4)

1. **Informal ratification only** — `anima/.own` formal `own N` entry NOT added this cycle; deferred until Track A transpiler proves the level-2 taxonomy with a real auto-gen artifact. Premature codification risks raw#20 own-monotonic violation.
2. **`atp_pytorch.py` orphan-in-working-tree** — 645 LoC hand-port file is gitignored, present locally, not committed, not auto-regenerated yet (Track A transpiler is later cycle scope). If ubu1 needs it before Track A lands, manual rsync/scp is required (disclosed friction; accepted because hand-port is bridging artifact, not durable).
3. **Root `.gitignore` block is REDUNDANT** — 12 LoC are duplicative with global `**/*.py` ban at line 3. Kept solely as documentation anchor at namespace declaration site for future audit traceability (raw 91 explicit-over-implicit C5). A leaner `.gitignore` would only need the namespace-local file.
4. **Negation patterns (`!tool/transient_py/.gitkeep`, etc.) are belt-and-suspenders** — global `**/*.py` does not match metadata files, so negations are technically unnecessary. Kept for clarity at namespace declaration site.
5. **Sequence assumption (F-before-G2) inherited from BG-psi audit** — if parent reorders Tracks, F's standalone validity still holds (spec docs + scaffold + policy are self-contained; no foreign dependency).
6. **BG-Beta concurrent .py emission into namespace** — Beta is writing `tool/transient_py/clm_v4_hf_format_shim.py` in parallel. F's policy correctly silently absorbs it (gitignored). Parent should ensure Beta's commit body acknowledges its `.own 2` status if Beta produces a separate spec doc, to avoid orphan auto-gen artifacts being mistaken for hand-edits.
7. **Self-disclosed redundancy in `tool/transient_py/.gitignore`** — lines 18-20 already say "REDUNDANT with the root `**/*.py` ban" — honest disclosure baked into source, no audit fudging needed.
