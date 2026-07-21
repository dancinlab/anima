# tool — shared runnable harness for HYPOTHESES

Repo-root machinery that `HYPOTHESES/` hypothesis cards run against. Shared, reusable
code lives here in `tool/`; per-hypothesis run scripts and their `result.json` live
under `state/<hX>_.../` and import from here.

## Key files

- `anima_v3.py` — deterministic, stdlib-only primitives for the anima-v3 problem:
  - **L1 gate** — `participation_ratio(sv)` is the campaign's PRE-REGISTERED effective-rank
    estimator; `effective_rank(sv)` (entropy) and `stable_rank(sv)` are independent
    cross-checks. Quote the gate on PR, never on whichever estimator clears the threshold.
  - `singular_values(vectors)` / `gram_matrix(vectors)` — seam spectrum via a stdlib Jacobi
    eigensolver (no numpy). Rows = observations, columns = seam channels.
  - **L2 gate** — `ablation_delta(ce_ablated, ce_full)` in nats;
    `ablation_fraction(..., ce_floor)` expresses it as a share of the headroom above a
    measured control floor, which is the comparable-across-rigs form.
  - **codec-invariant unit** — `bits_per_byte(ce_nats_per_token, n_tokens, n_bytes)`. Any
    comparison crossing a codec boundary MUST be in this unit (per-token CE is not
    comparable when the vocabulary moves).
  - `Falsifier` + `evaluate(metrics, falsifiers)` — pre-registered falsifier ledger.
- `test_anima_v3.py` — closed-form known-answer fixtures for every estimator above. This is
  a POSITIVE CONTROL on the instrument (pre-registered as H_001's falsifier G-3), not test
  hygiene: it fails loudly when an estimator goes blind. Wired into `sidecar ci` as
  `estimator-fixtures` (`harness.config.json`). Run: `python3 tool/test_anima_v3.py`.

## Rules

- **No hidden constants / fitting** — every input is explicit and documented so a
  card's falsifiers evaluate against returned numbers.
- **Deterministic** — no randomness, no network, $0 local. Same input → same output.
- **Pure & reusable** — functions here are shared across cards; hypothesis-specific
  parameters belong in the `state/<hX>/run_*.py` script, not here.

## Gotcha

- Import path: run scripts insert `tool/` on `sys.path` via a repo-root-relative
  path, so they run from anywhere (`python3 state/<hX>/run_*.py`).
- This module owns the **estimators, not the experiment**. A card's run script extracts the
  raw quantities (seam activations, CE values, byte counts) from whatever rig produced them
  and passes them here; keeping the estimator pre-registered and identical across runs is
  what makes two runs comparable at all. Heavy/seeded/GPU work never lives here.
