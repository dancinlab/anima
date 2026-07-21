# tool — shared runnable harness for HYPOTHESES

Repo-root machinery that `HYPOTHESES/` hypothesis cards run against. Shared, reusable
code lives here in `tool/`; per-hypothesis run scripts and their `result.json` live
under `state/<hX>_.../` and import from here.

## Key files

- `anima_v4.py` — deterministic, stdlib-only primitives for the anima-v4 problem:
  - `ratio(value, baseline)` / `headroom(current, floor)` — generic improvement factors.
  - `log_ratio(x)` — worked `math` example (replace with the campaign's real relations).
  - `Falsifier` + `evaluate(metrics, falsifiers)` — pre-registered falsifier ledger.

## Rules

- **No hidden constants / fitting** — every input is explicit and documented so a
  card's falsifiers evaluate against returned numbers.
- **Deterministic** — no randomness, no network, $0 local. Same input → same output.
- **Pure & reusable** — functions here are shared across cards; hypothesis-specific
  parameters belong in the `state/<hX>/run_*.py` script, not here.

## Gotcha

- Import path: run scripts insert `tool/` on `sys.path` via a repo-root-relative
  path, so they run from anywhere (`python3 state/<hX>/run_*.py`).
