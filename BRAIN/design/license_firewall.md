# design/license_firewall.md — Design Rationale

> Companion to `LICENSE_FIREWALL.md`. The user-facing doc says *what* to do.
> This doc says *why* the firewall is shaped the way it is.

## Why a firewall at all

hexa-brain (MIT) is wiring up to integrate at least 8 external OSS projects
identified in `GOOGLE_CONSCIOUSNESS_CHIP.md`. Two carry copyleft / NC
clauses (BrainGenix-NES AGPL-3.0; Cortical Labs cl-sdk CC-BY-NC-4.0). Plain
prose policy doesn't survive contact with PR velocity — see the existing
README sentence "blocked only by CC BY-NC 4.0 license" which is correct
but not enforced. The firewall is the load-bearing version of that prose.

The firewall does **not** try to prove the codebase license-clean. It tries
to prevent the most common failure mode: a PR author seeing the substrate
abstraction (E-1) and writing `import braingenix_nes` in
`eeg/substrates/sim_nes.hexa` because that's the obvious shape.

## Why YAML over a package manifest

The project deliberately has no `requirements.txt`, no `pyproject.toml`,
canonical Python manifest because the manifest itself would be a
"dependency-graph SSOT" outside hexa.

So the catalog is a hand-curated YAML. Trade-offs:

| Dimension | Hand-curated YAML | Auto-derived from manifest |
|---|---|---|
| SSOT freshness | discipline (reviewer reads diff) | tool-enforced |
| Pre-import of new deps | catalog-edit required before code | code lands first, manifest catches up |
| False-positive rate | low (only listed deps gate) | varies (transitive resolver) |
| Build-time cost | none (read once, grep) | non-trivial (resolver) |

The hand-curated path was chosen because (a) the catalog scales to the
~10 deps we expect at full Sprint completion, (b) the project has no
package manager to derive from, and (c) catalog freshness sits inside the
existing reviewer attention budget (every PR that adds an `import` line
also adds or references a catalog entry).

## Why grep over AST

Two options were considered for the actual enforcement:

1. **Bash grep against import-pattern regex** (chosen)
2. **Python AST walk** (not chosen)

The AST walk is strictly more powerful — it can catch
`importlib.import_module("brain" + "genix_nes")` and dynamic-eval
exotica. Grep cannot.

But:

- AST walk requires Python + a hexa-AST analyser (no existing hexa AST
  Python helper for every .hexa file).
- Grep against a small fixed set of literal namespaces is what the
  realistic threat model demands. The threat is **accidental tight
  coupling by a PR author who didn't read LICENSE_FIREWALL.md** — not
  an adversarial committer trying to smuggle AGPL in via string
  concatenation. Defending against the adversary is out of scope; that
  would also require sandboxing the build, signing commits, etc.
- The firewall **must run before any `.hexa` file is invoked** (it's the
  gate). It cannot depend on the hexa runtime to bootstrap itself. Bash
  + sha256sum + python3 (for sha when sha256sum is missing) is the
  smallest robust toolset that runs identically on Linux + macOS without
  a venv.

predate hexa": `bin/check_licenses.sh` is that exception.

## Falsifier design (F_LF_01 / F_LF_02 / F_LF_03)

The script's `--selftest` mode runs three falsifiers against an
isolated sandbox tree (`mktemp -d`). The triple is chosen to bracket the
three behaviors a firewall must demonstrate:

| Falsifier | Tests | What would fail this |
|---|---|---|
| F_LF_01 | Clean tree → PASS | Off-by-one in the scan loop that flags imaginary violations |
| F_LF_02 | Plant `from braingenix import x` → FAIL | Regex too narrow; pattern matching broken |
| F_LF_03 | Plant `// import cl_sdk` (comment) → PASS | Regex too broad; comment-strip broken |

This is the **smallest set** that exercises the false-negative,
true-positive, and false-positive boundaries respectively. Any expansion
(F_LF_04+) would add coverage but not fundamentally change the assurance
shape. Each falsifier resets `CHECKED_FILES`, `VIOLATIONS_COUNT`,
`VIOLATIONS_LIST` to ensure independence — running them in a different

## Why a marker + ledger

The project already uses `state/markers/<test>_<ts>.marker` (snapshot of
one run) + `state/<topic>_ledger.jsonl` (append-only history) for every
other validation tool (`alpha_eyes_closed`, `board_health_check`,
`impedance_check`, etc.). Re-using the pattern means:

- CI / dashboard tooling that already groks the marker convention
  works for license-check too, with no new code.
- Operators who already know "look in `state/markers/` for the most
  recent verdict" get one more entry there.
- The audit trail survives `git clean` (state/ is in .gitignore for
  large logs but markers themselves are small and committable).

The marker's `fingerprint` field is the first 8 chars of
`sha256(vendor/external_deps.yaml)` — a quick way for a reviewer to
notice "this marker is stale because the catalog changed."

## Threat model (what the firewall does and does NOT defend against)

| Threat | Defended? |
|---|---|
| Author types `import braingenix_nes` in `eeg/substrates/` by reflex | YES |
| Author types `from cl_sdk import open` in `eeg/closed_loop.hexa` | YES |
| Reviewer misses a PR that adds an AGPL `import` | YES (firewall catches; CI rejects) |
| Author dynamically loads AGPL via `importlib.import_module(name)` | NO (out of scope) |
| Author links AGPL via `ctypes.CDLL("libagpl.so")` | NO (out of scope) |
| Transitive AGPL dep: catalog says BSD, but BSD pkg depends on AGPL | PARTIAL (reviewer must audit catalog entries; firewall doesn't follow chains) |
| Catalog stale: new dep imported without catalog entry | NO (firewall has nothing to match against) — mitigated by reviewer attention |
| Adversarial committer | NO (out of scope; would need signing, sandboxing, etc.) |

## Sprint-1 scope locked

This design is what landed in Sprint 1 Part A. Future expansion (Sprint 2+):

- F_LF_04: dynamic-import detection (`importlib.import_module(...)`) with
  string-literal extraction
- Per-layer policy divergence (e.g., loosen `tool/` to allow GPL for
  experimental sandbox modules)
- Per-PR delta scan (only files changed in this PR, faster than full
  tree scan)
- GitHub Actions integration (run the firewall as a required check on
  every PR — depends on CI infrastructure landing)

None of those expansions change the SSOT location (still YAML), the
enforcement mechanism (still bash + grep), or the audit-trail shape
(still marker + ledger).
