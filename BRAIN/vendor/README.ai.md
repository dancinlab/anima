---
schema: hexa-brain/vendor/ai-native/1
last_updated: 2026-05-12
ssot:
  catalog:        external_deps.yaml
  policy:         license_policy.yaml
  enforcer:       ../bin/check_licenses.sh
  policy_doc:     ../LICENSE_FIREWALL.md
  design_doc:     ../design/license_firewall.md
status: active — Part A (License Firewall) Sprint 1 landing
raws:
  - R9 hexa-only (markdown + yaml + the bash enforcer are the explicit opt-outs)
  - R10 honest C3 (catalog is HAND-CURATED, not pkg-manager-derived)
  - R11 snake_case
  - R65 idempotent
---

# vendor/ — license firewall catalog (AI-native entry)

Hand-curated catalog and machine-readable policy for the four protected
layers (`eeg/`, `eeg_core/`, `core/`, `tool/`). Read together with
`../LICENSE_FIREWALL.md` (human-readable rules) and
`../bin/check_licenses.sh` (enforcer).

## TL;DR for an agent reading this cold

- `external_deps.yaml` — every external dep we explicitly know about, with
  its SPDX license, source URL, allowed coupling modes, and any blocked
  import regex patterns.
- `license_policy.yaml` — per-layer allow-list of SPDX ids. Loose-coupling
  (HTTP/CLI/subprocess) gets an `loose_extra` escape that admits AGPL /
  CC-BY-NC-4.0 / no-license / UNKNOWN.
- `../bin/check_licenses.sh` — reads both YAML files, walks the 4 protected
  dirs, greps each `blocked_import_pattern`, emits a marker + ledger row.


1. **The catalog is HAND-CURATED, not auto-derived.** Project has no
   `requirements.txt`, no `pyproject.toml`, no `package.json`. BrainFlow and
   numpy are *implicit* runtime deps invoked from inside `/tmp` helper
   cannot consume metadata from a package manager — it consumes this
   hand-written YAML instead. New deps must be appended here by a human
   (or by an agent reading this very note) before they appear in code.
2. **BrainFlow SPDX is verified MIT** by inspecting the upstream LICENSE
   file at <https://github.com/brainflow-dev/brainflow/blob/master/LICENSE>
   (BSD/MIT-style headers across C++ + Python bindings). If a future audit
   discovers a different sub-license inside the BrainFlow tree the entry
   must be flipped to `UNKNOWN` and that fact disclosed here.
3. **Declared-not-implemented entries are catalog placeholders, not
   integrations.** `braingenix_nes`, `cl_sdk`, `neuroglancer_py` are listed
   so the firewall can warn early. None are imported anywhere in the repo
   today (the firewall is the proof — it exits 0 on the clean tree).
4. **`cl` regex was deliberately tightened.** Earlier drafts used `cl` as
   the cl-sdk import regex; that false-positives on `cloudpickle`,
   `cluster`, etc. The catalog now uses `cl_sdk` and `cortical_labs` as the
   only blocked patterns for Cortical Labs.
5. **The enforcer is bash + inline python3, not hexa.** This is an
   firewall must run BEFORE any `.hexa` is invoked, so it cannot itself
   depend on the hexa runtime.
