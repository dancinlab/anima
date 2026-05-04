# hexa-lang Module Versioning + Capability Governance — Spec 2026-05-03

**Status**: Phase 1 (header additions landed for P0/P1 stdlib modules)
**Author**: anima-core
**Scope**: hexa-lang stdlib (`/Users/ghost/core/hexa-lang/stdlib/*.hexa`)
**Target consumers**: anima, nexus, qmirror — every project that imports stdlib
**Falsifier**: F-VERSION-1 (defined in §7)

---

## 1. Problem Statement

The hexa-lang stdlib has grown to 30+ modules without any version metadata or
declared capability surface. This produces three concrete failure modes:

1. **Silent breakage on rename**. A maintainer renames a public function
   (e.g. `http_get` → `http_get_body`). Downstream callers in anima / nexus
   compile-fail at next pull with no warning that this was a breaking change
   vs an additive refactor.

2. **No deprecation channel**. There is no place to mark a function
   "deprecated, will be removed in 2.0" without burying the notice in a body
   comment that consumers never read.

3. **Capability drift opaque to imports**. A consumer that depends on
   `proc_run_json_bridge` has no way to assert "I require stdlib/proc
   ≥ 1.0.0 with capability `proc_run_json_bridge`" — the import is
   effectively `*` with no version constraint.

This spec introduces a comment-only header convention that solves (1) and
(2) immediately and lays the contract for an opt-in validator (Phase 2)
that solves (3) by parsing the headers and emitting machine-readable manifests.

---

## 2. Header Format

Every public stdlib module **MUST** carry the following header block in its
top-of-file comment, after the existing `// @module(...)` / `// @usage(...)`
lines and before the body PROBLEM/STRATEGY narrative:

```hexa
// ── module governance metadata (hexa-lang module versioning spec 2026-05-03) ──
// @version 1.0.0
// @capabilities [func_a, func_b, func_c]
// @stability stable
// @since 2026-04-25
// @maintainer anima-core
// @priority P0
// Versioning policy: docs/hexa_lang_module_versioning_spec_2026_05_03.md
```

### 2.1 Field semantics

| field          | type   | required | semantics                                                                |
|----------------|--------|----------|--------------------------------------------------------------------------|
| `@version`     | semver | yes      | major.minor.patch — see §3 for bump rules                                |
| `@capabilities`| list   | yes      | public function names exported by module (the *contract surface*)        |
| `@stability`   | enum   | yes      | one of: `experimental`, `beta`, `stable`, `deprecated`                   |
| `@since`       | date   | yes      | ISO date the module first reached its current `@stability` level         |
| `@maintainer`  | string | yes      | owning team (`anima-core`, `nexus-core`, `qmirror-core`, …)              |
| `@priority`    | enum   | yes      | `P0` / `P1` / `P2` — load-bearing tier for downstream consumers          |

### 2.2 Comment-only invariant

All fields **MUST** be in `//`-prefixed comments. They are NOT parsed by the
hexa runtime today; the validator in Phase 2 will parse them via a
text-grep over the file head. Comment-only means:

- zero runtime cost (the parser elides comments before AST construction)
- zero risk of breaking AOT codegen or interpreter dispatch
- adding a header to an existing module is a pure additive diff (validated:
  4 P0/P1 modules edited in this cycle, 42 LoC added, 0 logic changes)

---

## 3. Versioning Rules (semver, with stdlib-specific clarifications)

### 3.1 Bump rules

| change                                                          | bump      |
|-----------------------------------------------------------------|-----------|
| add a new function (extend `@capabilities`)                     | minor     |
| internal-only refactor (no `@capabilities` delta, no behaviour) | patch     |
| bug fix that preserves documented contract                      | patch     |
| widen a parameter type / accept more inputs                     | minor     |
| narrow a parameter type / reject inputs that previously worked  | **major** |
| rename or remove a name in `@capabilities`                      | **major** |
| change a return-type contract (e.g. int → map)                  | **major** |
| change a documented error sentinel (e.g. `""` → `null`)         | **major** |
| `@stability` transition `experimental` → `beta` → `stable`      | minor     |
| `@stability` transition `* → deprecated`                        | major     |

### 3.2 Pre-1.0 escape hatch

Modules at `@stability experimental` MAY use `0.x.y` versioning where ANY
change is allowed without a major bump (caller-beware contract). The
transition `experimental → beta` triggers the first `1.0.0` release and
locks the contract.

The 4 modules landed in Phase 1 (`proc`, `json`, `http`, `bytes`) are all
declared `1.0.0 stable` because they have downstream callers in qmirror /
anima nexus already, and we want major-bump signalling enforced from cycle 1.

### 3.3 Versioning is NOT a substitute for spec docs

`@version 1.0.0` does NOT mean "this module is fully spec'd and frozen". It
means "the contract surface listed in `@capabilities` is what callers can
rely on; any breaking change to those names triggers a `2.0.0` release with
a migration note in `@since` and a CHANGELOG entry (see §6)".

---

## 4. Capability Discovery

### 4.1 Phase 1 (manual)

Consumers grep the source file:

```bash
grep -A 1 '@capabilities' /Users/ghost/core/hexa-lang/stdlib/proc.hexa
```

Output:

```
// @capabilities [proc_spawn_supervised, proc_lease_renew, proc_deregister, proc_kill, proc_alive, proc_reap, proc_run_with_stdin, proc_run_json_bridge]
```

### 4.2 Phase 2 (validator — deferred to next cycle)

A `tool/hexa_module_version_validate.hexa` will:

1. Walk every `stdlib/*.hexa` file
2. Parse the governance header (text-grep, no AST needed)
3. Emit a JSON manifest at `state/hexa_stdlib_manifest.json`:

```json
{
  "modules": {
    "proc": {
      "version": "1.0.0",
      "capabilities": ["proc_spawn_supervised", "proc_lease_renew", "..."],
      "stability": "stable",
      "since": "2026-04-25",
      "maintainer": "anima-core",
      "priority": "P0",
      "file": "stdlib/proc.hexa"
    }
  }
}
```

4. Cross-check that every name in `@capabilities` actually exists as a
   `pub fn <name>` in the file body (no phantom advertised capabilities).

5. Cross-check that every `pub fn` in the file body is listed in
   `@capabilities` (no undeclared public surface).

The validator is **deferred** to a separate cycle (Phase 2) to keep this
landing additive-only and reviewable.

### 4.3 Phase 3 (import-time check — speculative)

A future hexa runtime extension MAY support:

```hexa
use "stdlib/proc" require version >= "1.0.0" capability proc_run_json_bridge
```

This would fail the compile if the imported module's header doesn't
satisfy the constraint. Not committed; listed here so Phase 1 / Phase 2
don't paint themselves into a corner that blocks import-time enforcement.

---

## 5. Deprecation Lifecycle

### 5.1 States

```
experimental ──→ beta ──→ stable ──→ deprecated ──→ (removed in major bump)
```

### 5.2 Deprecation procedure

1. Maintainer flips `@stability stable` → `@stability deprecated`
2. Bumps `@version` major (e.g. 1.4.2 → 2.0.0)
3. Adds a `// @deprecated_since YYYY-MM-DD` line below `@since`
4. Adds a `// @replaced_by stdlib/<new-module>::<new-fn>` line if applicable
5. Adds a CHANGELOG entry (see §6)
6. Body code MUST continue to function for at least one release cycle —
   deprecation is a notice, not an immediate removal.

### 5.3 Removal procedure

After at least one minor release with `@stability deprecated`, the
maintainer MAY remove the function. This requires:

1. Bump major (`2.0.0` → `3.0.0`)
2. Remove the function name from `@capabilities`
3. CHANGELOG entry with migration guidance

---

## 6. CHANGELOG Convention (per-module)

Each module SHOULD maintain an inline CHANGELOG block at the bottom of the
top-of-file comment, in reverse-chronological order:

```hexa
// ── CHANGELOG ─────────────────────────────────────────────────────
// 1.0.0 (2026-04-25) — initial stable release; capabilities frozen
// 0.9.0 (2026-04-20) — beta; proc_run_json_bridge added
// 0.1.0 (2026-04-15) — experimental; proc_spawn_supervised only
```

Phase 1 does NOT add CHANGELOG blocks to the 4 landed modules (would be
empty / just-now). Phase 2 cycle adds CHANGELOG when the validator lands
and the first 1.1.0 minor bump happens.

---

## 7. Falsifier F-VERSION-1

**Statement**: every P0/P1 stdlib module has a valid governance header
that parses cleanly under the format defined in §2.

**Concretely**: for every file in the P0/P1 set
{`proc.hexa`, `json.hexa`, `http.hexa`, `bytes.hexa`}, the following
shell pipeline emits all 7 required fields:

```bash
for f in proc.hexa json.hexa http.hexa bytes.hexa; do
  echo "=== $f ==="
  grep -E '^// @(version|capabilities|stability|since|maintainer|priority)' \
    /Users/ghost/core/hexa-lang/stdlib/$f
done
```

**Pass criterion**: each file emits exactly 6 matches (one per `@field`).
The 7th field (`Versioning policy:`) is a free-form line, not `@`-prefixed.

**Falsified if**: any module is missing a field, has a malformed semver,
or has a `@stability` value outside the enum.

---

## 8. P0 / P1 Set Definition (Phase 1 scope)

The 4 modules landed in this cycle are the **P0/P1 set** — modules with
known downstream callers in anima / nexus / qmirror today:

| module        | priority | downstream callers                              | initial version |
|---------------|----------|-------------------------------------------------|-----------------|
| `proc.hexa`   | P0       | qmirror engine_aer, anima orchestrator          | 1.0.0           |
| `json.hexa`   | P1       | nexus calibration_v2, qmirror cache writeback   | 1.0.0           |
| `http.hexa`   | P1       | qmirror entropy.hexa (ANU REST API)             | 1.0.0           |
| `bytes.hexa`  | P1       | qmirror sampler.hexa (per-shot fold)            | 1.0.0           |

Phase 2 cycle extends the headers to **P2 modules** (no current downstream
callers but exported as stdlib): `optim.hexa`, `qrng_anu.hexa`,
`collections.hexa`, `parse.hexa`, `math.hexa`, `string.hexa`, `yaml.hexa`,
`portable_fs.hexa`, `consciousness.hexa`, `nn.hexa`, etc.

---

## 9. Caveats (raw#10 honest C3)

The following four caveats are filed against this spec — none are
blockers for Phase 1 landing but each is a known limitation that future
cycles must address.

### C1 — Semver subjective on early-stage stdlib

The bump rules in §3.1 assume a stable contract surface. The hexa-lang
stdlib is < 6 months old; many modules have not yet had a real "API
mistake to correct" event. The first time a P0 module needs to narrow a
parameter type to fix a real-world bug, the maintainer faces a judgment
call: bump major (correct per §3.1, but disruptive) or patch and
document (pragmatic but violates the rule). This spec does NOT solve
that tension — it only commits the team to picking ONE convention and
applying it uniformly. Phase 2 cycle should add concrete worked examples
from the first real major-bump event.

### C2 — Capabilities list may drift from actual public surface

Phase 1 has no validator. The `@capabilities` list is hand-maintained by
the maintainer. There is no enforcement that the list matches the actual
`pub fn` symbols in the file. A maintainer who adds a new `pub fn` and
forgets to update `@capabilities` produces a silent contract drift. The
Phase 2 validator (§4.2) closes this gap; until then the list is
**advisory, not authoritative**. Consumers should still grep the source
file for `pub fn` if they need ground truth.

### C3 — Validator deferred to Phase 2

The validator (`tool/hexa_module_version_validate.hexa`) is the single
piece of automation that turns this spec from "convention" into
"enforced contract". It is deferred to keep Phase 1 reviewable as a
pure header-additions diff. Until Phase 2 lands, F-VERSION-1 is checked
manually (the §7 shell pipeline). This is a 2-week-cycle gap, not a
permanent state — the validator is the next cycle's #1 deliverable.

### C4 — Ratification with hexa-lang core team pending

This spec was authored from the anima/qmirror consumer perspective. The
hexa-lang core maintainer team has not yet ratified the convention.
Specifically pending:

- agreement that `@version` / `@capabilities` are the right field names
  (vs e.g. `@semver` / `@exports`);
- agreement that comment-only is acceptable (vs a future runtime
  `@module(version=...)` attribute extension);
- agreement on the deprecation lifecycle in §5 (alternative: hard-fail
  imports of deprecated modules instead of soft-warn).

Phase 1 ships the convention unilaterally; if the hexa-lang core team
ratifies a different schema in the next cycle, the 4 P0/P1 module
headers can be migrated via a single sed pass (comment-only delta).

---

## 10. References

- hexa-lang stdlib root: `/Users/ghost/core/hexa-lang/stdlib/`
- hexa-lang attr review (the analysis that surfaced these 4 modules):
  `anima/docs/hexa_lang_attr_review_for_qmirror_2026_05_03.md`
- per-module landing handoff:
  `anima/docs/hexa_lang_module_versioning_landed_2026_05_03.ai.md`
- marker file:
  `anima/state/markers/hexa_lang_module_versioning_landed.marker`

---

## 11. Out-of-Scope (explicit non-goals)

To prevent scope creep, this spec explicitly does NOT cover:

- runtime version-check builtin (Phase 3, speculative — §4.3)
- automatic semver bump tooling (manual maintainer responsibility)
- module dependency declaration (`@requires stdlib/json >= 1.0.0`) —
  may be added in Phase 3 once import-time check exists
- third-party / non-stdlib hexa modules (this spec covers stdlib only;
  user-project modules MAY adopt the same convention voluntarily)
- versioning of the hexa **runtime** (`runtime.c`) itself — that is
  governed by the hexa-lang main project, not this spec
