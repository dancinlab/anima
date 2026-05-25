# tool/transient_py/ — auto-generated python namespace

**Status**: namespace ratification — INFORMAL spec (2026-05-03), pending dot_own_validate.hexa land + 30d clean streak (cycle TBD).

**Spec**: [`docs/anima_dot_own_namespace_spec_2026_05_03.md`](../../docs/anima_dot_own_namespace_spec_2026_05_03.md)

## Purpose

Hold `.py` files that are **auto-generated** by hexa transpilers (track A: `tool/atp_to_pytorch.hexa` family) or are **transient runtime helpers**. These files are NEVER hand-edited; the .hexa source upstream is the SSOT.

## Why a separate namespace?

raw#9 (hexa-only) bans `.py` under `tool/` git-tracked. Auto-generated `.py` is a legitimate exception class but does NOT belong with hand-written `.hexa` source. Segregating into `tool/transient_py/` makes the boundary lint-checkable and prevents drift (someone mistaking auto-gen for hand-edit).

## .own levels (declared per file via header `# .own N`)

| level | semantics | git tracked? | example |
|---|---|---|---|
| `.own 1` | grandfathered legacy (existing `.py` predating namespace) | yes (existing repo state) | `tool/active_redteam_dEF_proto.py` |
| `.own 2` | transpiler auto-gen output (regeneratable from .hexa) | NO (regen on demand) | `tool/transient_py/atp_pytorch.py` (future) |
| `.own 3` | transient sister-rule (raw#37 helper, one-shot disposable) | NO (per-run scratch) | `state/.X_helper.py` (~25 files) |
| `.own 4` | test fixtures (auto-gen test harness scratch) | NO (regen via selftest) | `tool/transient_py/_fixture_*.py` (future) |

## Header template (mandatory for every .py in this namespace)

```python
# .own 2
# generator: tool/atp_to_pytorch.hexa
# source: anima-voice/audio_token_predictor.hexa@<commit-hash>
# generated: 2026-05-03T22:00:00Z
# retire-when: tool/atp_to_pytorch.hexa updated OR source .hexa changed
```

Required fields: `# .own N`, `generator`, `source`, `generated`, `retire-when`.

## What goes here vs elsewhere

- `tool/transient_py/` — `.own 2` + `.own 4` (this namespace, gitignored)
- `state/.X_helper.py` — `.own 3` (raw#37 sister-rule, gitignored under root `state/.npy_helper.py`-style patterns)
- `tool/active_redteam_*.py`, `tool/anima_holographic_ib_ksg_validate_prod.py` — `.own 1` grandfathered (per anima/.own own 1 opt-out list)

## Lifecycle

1. Hexa transpiler emits `.py` here (`.own 2` header).
2. Caller imports/executes the `.py`.
3. On next transpile run, `.py` is overwritten (idempotent regen).
4. On `tool/<gen>.hexa` schema change, all dependent `.py` are stale-marked and regenerated.
5. **No file in this namespace is committed** (gitignored). If a CI artifact is needed, the .hexa source + transpiler version is the artifact.

## Honest C3 caveats (raw 91)

1. **Ratification is informal** — this namespace is spec'd in `docs/anima_dot_own_namespace_spec_2026_05_03.md` but not yet ratified into anima/.own as a formal `own N` entry. Intent: ratify after Track A transpiler lands first real `.own 2` artifact.
2. **Level definitions are speculative** — `.own 2/3/4` boundaries are proposed; real-world drift may merge or split levels post-Track-A measurement.
3. **Retirement enforcement is TBD** — `retire-when` field is human-readable; no automation deletes stale auto-gen yet (separate cycle: `tool/dot_own_gc.hexa`).
4. **Audit tooling is future cycle** — `tool/dot_own_validate.hexa` (header presence + level grammar check) is PROPOSED, not yet implemented; F-OWN-1 falsifier is design-stage.

## Related rules

- `anima/.own` own 1 — raw 9 hexa-only scope override + grandfather list (`.own 1` legacy)
- raw#9 — hexa-only mandate
- raw#37 — helper /tmp transient (anima-local interpretation; sister to raw#9)
- raw#0 — root SSOT (.raw + .own + .guide); .own 2/3/4 derivation must not violate
