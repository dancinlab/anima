# `.own N` namespace + `tool/transient_py/` formalization spec — 2026-05-03

**Status**: SPEC — informal ratification (cycle 1: namespace land + dir scaffold + .gitignore policy). Formal `own N` rule entry into `anima/.own` deferred to Track A transpiler first-real-artifact cycle.

**Cost**: $0 (Mac local, pure spec — no .py created, no tool installed).

**Constraints honored**: raw#9 STRICT (hexa-only on Mac for active source; this spec creates `.gitkeep` + `.gitignore` + `README.md` + this `.md` only — no `.py`, no `.hexa` install). raw#15 (ω-cycle output = SSOT, this doc tagged `2026-05-03`). raw#10 (4 honest C3 caveats — see §10). raw#0 (root SSOT triad preserved — this doc is project-local L1 scope candidate, not L0 raw).

---

## 1. Motivation

### 1-1. Upstream context

- **hexa-lang upstream audit** recommended `own N` policy formalization for `tool/transient_py/` as the auto-gen `.py` namespace.
- **Track A transpiler** (sister BG `a6293670c` prototyping `tool/atp_to_pytorch.hexa`) will emit `.py` to this namespace. Without a declared landing zone, output would either (a) collide with hand-edited `tool/*.hexa` (raw#9 violation), or (b) leak into ad-hoc paths (raw#0 root SSOT erosion).
- **Existing `.own 1` grandfathers** (per `anima/.own` own 1 opt-out list):
  - `tool/active_redteam_dEF_proto.py`
  - `tool/active_redteam_prototype.py`
  - `tool/anima_holographic_ib_ksg_validate_prod.py`
  - (3 redteam .py + 1 holographic_ib_ksg .py = 4 grandfathered slots.)
- **Existing raw#37 transient sister-rule** (`anima/.own` line 51 cross-link "raw 37 (helper /tmp transient) — raw 9 sister rule"): `state/.X_helper.py` ~25 files (e.g. `.hjorth_helper.py`, `.berger_alpha_gate_helper.py`, `.welch_to_bandpower_helper.py`, ...). Pattern: dot-prefixed disposable helpers under `state/`, gitignored via root `.gitignore` lines 187-191 (`state/.npy_helper.py`, `state/.clm_eeg_*`, ...).

### 1-2. Problem statement

Ad-hoc `.py` placement under `tool/` violates raw#9 and breaks lint expectations. Auto-gen output that LOOKS like hand-written hexa-source corrupts the SSOT signal. We need a **declared, lint-checkable namespace** with **per-file lifecycle metadata** so:

- Auto-gen `.py` is segregated (`tool/transient_py/`).
- Each `.py` declares its origin + retirement criterion via `# .own N` header.
- Validators can prove every Mac-side `.py` declares a valid `.own` level (F-OWN-1).
- Regeneration vs. grandfathering is unambiguous.

---

## 2. `.own N` declaration grammar (per-file header)

### 2-1. Syntax

Every `.py` under `tool/transient_py/` (and `state/.*_helper.py` via raw#37 sister) MUST begin with a header block of the following form:

```python
# .own N
# generator: <path/to/generator.hexa>          # required for .own 2/4
# source: <path/to/source.hexa>@<commit-hash>  # required for .own 2
# generated: <ISO-8601 UTC timestamp>          # required for .own 2/3/4
# retire-when: <human-readable trigger>        # required for .own 2/3
```

- `# .own N` MUST be the first non-shebang line.
- `N` is one of `1`, `2`, `3`, `4` (see §3).
- Fields after `# .own N` are level-conditional (see §3 per-level requirements).
- Lines beginning with `#` are Python comments (no parser change needed).

### 2-2. Example

```python
#!/usr/bin/env python3
# .own 2
# generator: tool/atp_to_pytorch.hexa
# source: anima-voice/audio_token_predictor.hexa@a6293670c
# generated: 2026-05-03T22:00:00Z
# retire-when: tool/atp_to_pytorch.hexa updated OR source .hexa changed

import torch
# ... auto-generated body ...
```

### 2-3. Grammar rationale

- Comment-prefixed (`#`) — zero Python parser impact, runs as no-op import.
- ISO-8601 UTC `generated` — sortable, audit-trail-compatible.
- `retire-when` is **human-readable** in cycle 1 (cycle TBD: machine-parseable predicate language).
- `@<commit-hash>` on `source` makes upstream drift detection trivial (`git log --oneline <source>` vs. recorded hash).

---

## 3. Four `.own` levels (proposed)

### 3-1. `.own 1` — grandfathered legacy `.py`

| field | value |
|---|---|
| **scope** | `.py` predating namespace formalization, listed in `anima/.own` own 1 opt-out |
| **count (current)** | 4 (3 redteam + 1 holographic_ib_ksg) |
| **lifecycle** | static — no regeneration; managed via `anima/.own` own 1 retirement criterion (raw 71 cite-of-violation = re-violation) |
| **audit cadence** | per anima/.own own 1 — opportunistic (long-term hexa-native rewrite track per raw 38) |
| **retirement criterion** | hexa-native equivalent lands AND becomes invocation-canonical (per anima/.own own 1 raw 71 clause) |
| **git tracked?** | YES (existing repo state) |
| **header required?** | NO (grandfathered — adding header is a future hardening cycle, not enforced this cycle) |
| **example** | `tool/active_redteam_dEF_proto.py`, `tool/anima_holographic_ib_ksg_validate_prod.py` |

### 3-2. `.own 2` — transpiler auto-gen output

| field | value |
|---|---|
| **scope** | `.py` emitted by `tool/<x>_to_pytorch.hexa` family transpilers |
| **count (current)** | 0 (Track A pre-first-emit as of 2026-05-03) |
| **lifecycle** | regenerated on every transpiler run (idempotent overwrite); stale on source-hexa-commit-change |
| **audit cadence** | per-transpile (every regeneration revalidates header) |
| **retirement criterion** | source `.hexa` deleted OR transpiler retired |
| **git tracked?** | NO (gitignored under `tool/transient_py/*.py` per root `.gitignore`) |
| **header required?** | YES — full template (`generator` + `source` + `generated` + `retire-when`) |
| **landing zone** | `tool/transient_py/<descriptive_name>.py` |
| **example (future)** | `tool/transient_py/atp_pytorch.py` (atp_to_pytorch.hexa output) |

### 3-3. `.own 3` — transient sister-rule (raw#37)

| field | value |
|---|---|
| **scope** | one-shot helper `.py` placed under `state/.<name>_helper.py` for hexa-side numpy/scipy fixture generation |
| **count (current)** | ~25 files (`state/.hjorth_helper.py`, `.berger_*_helper.py`, `.welch_to_bandpower_helper.py`, ...) |
| **lifecycle** | per-run scratch — deleted/overwritten freely; survives only as long as the calling `.hexa` needs the output |
| **audit cadence** | spot-check during raw#9 sweep (semi-annual) |
| **retirement criterion** | calling `.hexa` retired OR migrated to native hexa numerics |
| **git tracked?** | NO (gitignored under root `.gitignore` lines 187-191 + extension to `state/.*_helper.py` glob) |
| **header required?** | YES — minimal (`# .own 3` + `generated` + `retire-when`); `generator` + `source` OPTIONAL (often produced by ad-hoc hexa script not worth tracking) |
| **landing zone** | `state/.<name>_helper.py` (dot-prefix preserved) |
| **example** | `state/.hjorth_helper.py`, `state/.welch_to_bandpower_helper.py` |

### 3-4. `.own 4` — test fixtures (future)

| field | value |
|---|---|
| **scope** | `.py` test harness fixtures auto-generated by `--selftest` modes of generator hexa scripts |
| **count (current)** | 0 (reserved for future use) |
| **lifecycle** | regenerated per `--selftest` invocation; never long-lived |
| **audit cadence** | per-selftest (CI integration follow-up) |
| **retirement criterion** | parent `.hexa` `--selftest` removed |
| **git tracked?** | NO |
| **header required?** | YES — `generator` + `generated` + `retire-when` (no `source` since fixture is synthesized, not transpiled) |
| **landing zone** | `tool/transient_py/_fixture_<name>.py` (underscore-prefix to disambiguate from `.own 2`) |
| **example (future)** | `tool/transient_py/_fixture_atp_minibatch.py` |

---

## 4. `.gitignore` policy summary

| level | tracked? | mechanism |
|---|---|---|
| `.own 1` | YES | existing repo state (no .gitignore entry); managed via `anima/.own` own 1 |
| `.own 2` | NO | root `.gitignore` `**/*.py` ban + explicit `tool/transient_py/*.py` documentation block (added 2026-05-03) |
| `.own 3` | NO | root `.gitignore` lines 187-191 (existing) + per-file `state/.<name>_helper.py` glob |
| `.own 4` | NO | root `.gitignore` `**/*.py` ban + explicit `tool/transient_py/*.py` block (shared with .own 2) |

### 4-1. `tool/transient_py/.gitignore` (namespace-local)

Created this cycle. Mirrors root `**/*.py` ban plus negates `.gitkeep`, `.gitignore`, `README.md` so the namespace metadata is preserved.

### 4-2. Root `.gitignore` documentation block

Added 2026-05-03 (this cycle):

```gitignore
# tool/transient_py/ — auto-generated python namespace (.own 2/3/4)
# Spec: docs/anima_dot_own_namespace_spec_2026_05_03.md
# Policy: *.py here are gitignored (regeneratable from .hexa transpiler).
#         The directory is preserved via .gitkeep + README.md + .gitignore.
tool/transient_py/*.py
tool/transient_py/__pycache__/
!tool/transient_py/.gitkeep
!tool/transient_py/.gitignore
!tool/transient_py/README.md
```

---

## 5. Validator (PROPOSED — separate cycle, NOT installed this cycle)

### 5-1. `tool/dot_own_validate.hexa` (proposed name)

**Purpose**: walk every `.py` under anima git-tracked paths AND state/ + tool/transient_py/ helpers, parse `# .own N` header, fail on:

- missing `# .own N` first-comment-line
- `N` not in `{1, 2, 3, 4}`
- level-conditional fields missing (e.g. `.own 2` without `source`)
- `source@<hash>` hash not in current git log of source path (drift detection)
- `generated` ISO-8601 parse failure

**Selftest**: 5 fixtures (one per level + one negative).

**Selftest emission** (per hive lint convention): `__DOT_OWN_VALIDATE_SELFTEST__ <PASS|FAIL> n=5 fail=<M>`.

**Severity ramp**: `warn → block` after 30d clean streak post-Track-A first-artifact.

### 5-2. F-OWN-1 falsifier (proposed)

| field | value |
|---|---|
| `id` | `F-OWN-1` |
| `description` | every Mac-side `.py` (under anima git-tracked paths excluding `**/site-packages/**`, `**/__pycache__/**`, `references/**`) declares a valid `.own N` header |
| `threshold` | `dot_own_missing_header_count == 0` AND `dot_own_invalid_level_count == 0` |
| `action-on-fail` | strengthen (raise severity warn→block) |

---

## 6. Migration plan (cycles)

| cycle | scope | status |
|---|---|---|
| **1 (THIS, 2026-05-03)** | namespace dir + .gitignore + README + spec doc + handoff + marker | LANDED |
| **2 (TBD, post-Track-A)** | first `.own 2` artifact lands → ratify spec into `anima/.own` as `own N` formal entry | DEFERRED |
| **3 (TBD)** | implement `tool/dot_own_validate.hexa` + selftest + F-OWN-1 emission | PROPOSED |
| **4 (TBD)** | backfill `.own 1` headers into 4 grandfathered files (ONE-TIME, no `.py` body change) | PROPOSED |
| **5 (TBD)** | backfill `.own 3` headers into ~25 `state/.*_helper.py` files | PROPOSED |
| **6 (TBD)** | severity ramp warn → block (gated on 30d clean) | DEFERRED |

This cycle (1) deliberately does **NOT**:
- Modify `anima/.own` (no `own N` entry yet — informal until Track A first artifact)
- Touch any existing `.py` file (raw#9 STRICT — Mac-side .py creation/modification banned this cycle)
- Install the validator
- Modify `state/.*_helper.py` headers

---

## 7. Cross-link to existing rules

| rule | relationship |
|---|---|
| **raw#0** (root SSOT) | `.own N` declarations are project-local L1 metadata; do not promote to L0 raw without sister-repo demand (raw#47) |
| **raw#9** (hexa-only) | `.own 2/3/4` formalize the EXEMPTION class; raw#9 jurisdiction unchanged for hand-written code |
| **raw#37** (helper /tmp transient) | `.own 3` is the formal name for raw#37's namespace; semantics preserved |
| **raw#10** (honest disclosure) | this spec carries 4 honest C3 caveats (§10) |
| **raw#15** (ω-cycle output = SSOT) | this doc tagged `2026-05-03`; supersession via dated re-spec |
| **raw#20** (own-monotonic) | when `own N` ratification (cycle 2) lands, MUST monotonically strengthen any preceding raw 9 / raw 37 baseline |
| **raw#71** (cite-of-violation = re-violation) | `.own 1` retirement clause inherited |
| **raw#91** (honest C1-C5) | C3 caveats explicit in §10 |
| **raw#95** (triad-universal-mandate) | validator (cycle 3) will register at L2 lint reference layer per `tool/<concern>_lint.hexa` convention (lint.001 in hive .raw.mk2) |
| **anima/.own own 1** | grandfather list inherited as `.own 1` cohort; this spec adds METADATA (`.own N` header) without modifying own 1 retirement criterion |

---

## 8. Directory state created this cycle

```
anima/
├── .gitignore                         (modified — added tool/transient_py/ block)
├── docs/
│   ├── anima_dot_own_namespace_spec_2026_05_03.md     (NEW — this doc)
│   └── anima_dot_own_namespace_spec_landed_2026_05_03.ai.md  (NEW — handoff)
├── state/
│   └── markers/
│       └── anima_dot_own_namespace_spec_landed.marker  (NEW)
└── tool/
    └── transient_py/                  (NEW dir)
        ├── .gitkeep                   (NEW — preserve empty dir)
        ├── .gitignore                 (NEW — namespace-local policy)
        └── README.md                  (NEW — namespace explanation)
```

---

## 9. Validation (this cycle, manual)

| check | result |
|---|---|
| `tool/transient_py/` directory exists | PASS (mkdir 2026-05-03) |
| `.gitkeep` + `.gitignore` + `README.md` present | PASS (3 files) |
| Root `.gitignore` documents `tool/transient_py/*.py` | PASS (block added 2026-05-03) |
| No `.py` created in this cycle | PASS (raw#9 honored) |
| No existing `.own 1` grandfathered file modified | PASS (all 4 untouched) |
| No `state/.*_helper.py` modified | PASS (all ~25 untouched) |
| Spec doc + handoff doc + marker emitted | PASS (3 outputs) |
| Cost | $0 (Mac local) |

---

## 10. Honest C3 caveats (raw 91)

1. **`.own` ratification is INFORMAL this cycle.** No `own N` entry has been added to `anima/.own`. The spec lives only in this `.md` and the namespace dir scaffolding. Formal `anima/.own` insertion is deferred to cycle 2 (post-Track-A first artifact) so we do not codify a level taxonomy before observing real auto-gen behavior.

2. **Level definitions (`.own 2/3/4`) are SPECULATIVE.** The 4-level split is a proposal informed by current usage patterns (3 grandfathered + 25 raw#37 helpers + 0 transpiler outputs). Track A's first real `.py` may reveal that `.own 2` and `.own 4` should merge (both transpiler-style) or that a fifth level is needed (e.g. `.own 5` for vendored `.py` from upstream pip-installable libs that anima patches). **Do not treat the 4-level taxonomy as final until cycle 2 ratification.**

3. **Retirement enforcement is TBD.** The `retire-when` field is currently free-form text. There is no automated GC that deletes stale `.own 2/3/4` files when their generator or source changes. A future `tool/dot_own_gc.hexa` (separate cycle) would parse `retire-when` against current repo state and emit deletion candidates. Until then, retirement is operator-discipline-based — falsifiable but not auto-enforced.

4. **Audit tooling is FUTURE CYCLE.** `tool/dot_own_validate.hexa` and falsifier `F-OWN-1` are PROPOSED only. The header presence + level grammar check is not currently runnable. Until cycle 3 lands the validator, claims like "every Mac-side .py declares a valid .own level" are aspirational, not evidenced. The 4 grandfathered `.own 1` files DO NOT currently carry `.own 1` headers (backfill is cycle 4).

---

## 11. References

- **Cross-sister context**: hexa-lang upstream audit recommendation (cited in task brief 2026-05-03).
- **Track A transpiler prototype**: sister BG `a6293670c` (`tool/atp_to_pytorch.hexa` design).
- **anima/.own own 1**: line 78-93, raw 9 hexa-only scope override + grandfather list.
- **anima/.own raw 37 cross-link**: line 51 ("raw 37 (helper /tmp transient) — raw 9 sister rule").
- **Root .gitignore current state**: lines 1-7 (Python ban), lines 187-191 (state helper patterns), lines 230+ (this cycle's tool/transient_py/ block).
- **hive .raw.mk2 lint.001**: `tool/<concern>_lint.hexa` convention (basis for future `dot_own_validate.hexa` registration).

---

**End of spec.** Cycle 1 LoC: ~280 (this doc) + ~50 (README) + ~30 (.gitignore) ≈ 360 LoC total deliverable.
