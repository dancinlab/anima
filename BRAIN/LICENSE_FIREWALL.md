# License Firewall

> Machine-enforced policy preventing AGPL-3.0 / CC-BY-NC-4.0 / no-license code
> from being **tight-coupled** (in_process Python `import`) into the four
> protected layers (`eeg/`, `eeg_core/`, `core/`, `tool/`) of this MIT-licensed
> project.
>
> Single source of truth: `vendor/external_deps.yaml` (catalog) +
> `vendor/license_policy.yaml` (per-layer allow-lists).
> Enforcer: `bin/check_licenses.sh`.
> Audit trail: `state/markers/license_firewall_check_<ts>.marker` +
> `state/license_firewall_checks.jsonl`.

---

## Why this exists

hexa-brain is **MIT-licensed**. The `GOOGLE_CONSCIOUSNESS_CHIP.md` survey
identified 8 external OSS projects we plan to integrate (BrainFlow, NumPy,
Neuroglancer, CloudVolume, BrainGenix-NES, BrainEmulationChallenge, cl-sdk,
c302). Two of those — **BrainGenix-NES (AGPL-3.0)** and
**Cortical Labs cl-sdk (CC-BY-NC-4.0)** — would license-infect hexa-brain
if imported tight-coupled (in_process). The project README already
acknowledges this with prose ("blocked only by CC BY-NC 4.0 license"), but
prose is not a gate. The license firewall is the gate.

Without this firewall:

- A future PR could `import braingenix_nes` in `eeg/substrates/sim_nes.hexa`
  and silently relicense the entire dependency closure under AGPL-3.0
  (network-distribution clause activated).
- Or `from cl_sdk import open` in `eeg/closed_loop.hexa` and quietly forbid
  commercial use of the whole tree (CC-BY-NC-4.0 NonCommercial restriction).

The firewall makes both into hard build-time failures.

## What it checks

For every `.hexa` and `.py` file under the four protected layers:

```
eeg/         — scalp EEG capture pipeline
eeg_core/    — lower-level EEG primitives
core/        — repo-root paradigm/metric host (pre-migration)
tool/        — paradigm/metric/filter modules (post-migration)
```

…the firewall runs each `blocked_import_patterns` regex from
`vendor/external_deps.yaml` against the file content. Hits on
**non-comment** lines that match `^[^/]*import\s+<pat>` or
`^[^/]*from\s+<pat>` are **violations**.

**Comment-only lines** (starting with `//` for hexa, `#` for Python after
whitespace strip) are **ignored** — referencing a forbidden namespace inside
a comment is documentation, not coupling.

## Layered policy (allow-list per coupling tier)

From `vendor/license_policy.yaml`:

| Layer | Tight-coupling allow-list (`allow_spdx`) | Loose-coupling extras (`loose_extra`) |
|---|---|---|
| `eeg/` | MIT, BSD-3-Clause, BSD-2-Clause, Apache-2.0, ISC | AGPL-3.0, CC-BY-NC-4.0, no-license, UNKNOWN |
| `eeg_core/` | (same) | (same) |
| `core/` | (same) | (same) |
| `tool/` | (same) | (same) |

The four layers carry the **same** policy. Per-layer rows exist so a future
revision (e.g., loosening `tool/` to allow GPL-3.0 for an experimental
sandbox) is a one-row edit.

**Rule**:

- A dep with `coupling_modes ⊆ {http, cli, subprocess}` may have a license
  in `allow_spdx ∪ loose_extra` — the GPL/AGPL/NC viral clauses do not
  cross an IPC boundary.
- A dep with `in_process` in `coupling_modes` MUST have a license in
  `allow_spdx`.

## Escape hatches (loose-coupling)

AGPL-3.0 (BrainGenix-NES) and CC-BY-NC-4.0 (Cortical Labs cl-sdk) are
**allowed when accessed via HTTP / CLI / subprocess** from a separate
process boundary. The firewall does NOT block:

- A `requests.post("http://127.0.0.1:8410/Simulation/Create", ...)` call
- A `subprocess.run(["nes-cli", ...])` invocation
- A `urllib.request.urlopen("http://localhost:.../...")` shim

The firewall DOES block:

- `import braingenix_nes` / `from braingenix import x` anywhere in the four
  protected layers
- `import cl_sdk` / `from cortical_labs import y` anywhere in the four
  protected layers

If you need a new dep that is AGPL/CC-NC/no-license, add it to
`vendor/external_deps.yaml` with `coupling_modes: [http]` (or `[cli]` /
`[subprocess]`), wire the adapter via the substrate protocol
(`eeg/substrates/`), and document the IPC boundary in
`design/<feature>_design_<date>.md`. See `eeg/substrates/sim_nes.hexa`
(when it lands) as the canonical example.

## How to run the check

```bash
# Default — scan the full tree, emit marker + ledger row, exit 0 if clean
bin/check_licenses.sh

# Selftest — run F_LF_01 / F_LF_02 / F_LF_03 falsifiers, emit synthetic marker
bin/check_licenses.sh --selftest

# Via top-level dispatcher (registered in bin/hexa-brain — see CHANGELOG)
hexa-brain license-check
```

## Marker output

On success the firewall writes a marker at:

```
state/markers/license_firewall_check_<unixts>.marker
```

Content (single JSON line):

```json
{
  "source": "bin/check_licenses.sh",
  "exit": 0,
  "fingerprint": "<first 8 chars of sha256(external_deps.yaml)>",
  "ts": 1747000000,
  "checked_files": 87,
  "violations": 0
}
```

On a violation the marker filename gains a `_FAILED` suffix and the
`exit` field is `2`. The script also prints every offending
`file:lineno: blocked import for dep=<id> ...` line to stderr.

A separate **ledger** at `state/license_firewall_checks.jsonl`
accumulates one row per check (append-only) with schema
`hexa-brain/license_firewall_check/1`.

## Falsifiers (built into `--selftest`)

| Id | Setup | Expected verdict |
|---|---|---|
| `F_LF_01` | Clean sandbox tree (`eeg/`, `eeg_core/`, `tool/` empty) | exit 0, PASS |
| `F_LF_02` | Plant `from braingenix import x` in `<sandbox>/eeg/_lf02_fixture.hexa` | exit 2, violations ≥ 1 |
| `F_LF_03` | Plant `// import cl_sdk should be ignored` (comment-only) | exit 0, PASS (no match) |

`--selftest` runs all three against a `mktemp -d`-allocated sandbox tree
(it does not touch the real `eeg/` etc.) and emits one synthetic marker
labelled `license_firewall_selftest`.

## How to add a new dep

1. Open `vendor/external_deps.yaml` and append a `deps:` entry:
   ```yaml
   - id: <snake_case_id>
     name: <Human Name>
     spdx: <SPDX-id-or-UNKNOWN>
     source_url: https://...
     coupling_modes: [in_process]      # or [http] / [cli] / [subprocess]
     blocked_import_patterns: []        # populate if forbidden namespace
     status: active                     # or declared-not-implemented
     advisory: |
       Why this dep, where it's used, license rationale.
   ```
2. If license is OUTSIDE `allow_spdx ∪ loose_extra` for any layer, the
   firewall will refuse it. Either:
   - Demote to loose coupling (`coupling_modes: [http]`) and add an HTTP
     adapter under `eeg/substrates/`, OR
   - Loosen the layer policy in `vendor/license_policy.yaml` (rare —
     requires reviewer approval and a `design/`-doc rationale).
3. If license is `AGPL-3.0` / `CC-BY-NC-4.0` / `no-license`, the dep
   **must** be `coupling_modes ⊆ {http, cli, subprocess}` — no `in_process`.
4. Run `bin/check_licenses.sh --selftest` and `bin/check_licenses.sh` —
   both must exit 0.
5. Commit `vendor/external_deps.yaml` together with the adapter code.


1. **Grep, not AST** — the firewall uses bash regex against raw source
   lines. A pathological obfuscation like
   `importlib.import_module("brain" + "genix_nes")` would slip past it.
   This is acceptable because the firewall protects against **accidental**
   tight coupling by PR authors who didn't read this file; it is not a
   precludes building a Python-AST analyser inside the firewall (would
   require a Python dep manifest, which the project deliberately lacks).
2. **No transitive scan** — if a `vendor/external_deps.yaml`-listed dep
   itself depends on something AGPL, the firewall does not follow that
   chain. Reviewer must read the dep's own manifest. For the seed deps
   (BrainFlow, NumPy, pyserial) this has been audited.
3. **Hand-curated catalog** — there is no auto-derivation from a package
   manager (project has no `requirements.txt` / `pyproject.toml` by
   design). Catalog freshness is a human discipline. Mitigation:
   `vendor/external_deps.yaml` is part of every PR review; new
   `import` / `from` statements in `eeg/` etc. that name a not-yet-cataloged
   namespace will be caught by the firewall only after the namespace is
   added to a `blocked_import_patterns` list — meaning a non-blocked
   import passes silently. This is the **lower** bound; the **upper** bound
   is reviewer attention.
4. **Linker / dynamic-load loophole** — `ctypes.CDLL("libagpl.so")` is
   invisible to the import-pattern firewall. Same mitigation as (1): this
   is not a security boundary.
5. **License field "UNKNOWN"** — some catalog entries (e.g., a future
   pre-release dep) may legitimately carry `spdx: UNKNOWN`. These are
   allowed in `loose_extra` only — never `in_process`. If a dep's license
   later resolves to a real SPDX id, update the catalog.

## See also

- `vendor/external_deps.yaml` — catalog (canonical)
- `vendor/license_policy.yaml` — per-layer allow-lists
- `vendor/README.ai.md` — AI-native frontmatter doc
- `bin/check_licenses.sh` — enforcer script
- `design/license_firewall.md` — design rationale (why YAML, why grep)
- `LATTICE_POLICY.md` §3.4 — universal lattice-policy cross-reference
- `GOOGLE_CONSCIOUSNESS_CHIP.md` — research survey that motivated this firewall
- `/home/summer/.claude/plans/hazy-kindling-wind.md` — Sprint 1 plan (Part A)
