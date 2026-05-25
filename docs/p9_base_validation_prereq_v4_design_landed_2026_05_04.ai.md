# P9 base-validation prereq OPT-1 v4 DESIGN LANDED — 2026-05-04

**Cycle**: BG-Π (parallel with BG-Ξ spec amendment + BG-Ο Llama anchor; non-overlapping territory).
**Predecessors**:
- Shim: BG-Κ commit `ed4b7c56` — OPT-1 v3 PASS, 12/12 prereq cleared.
- Validation: BG-Μ commit `1ef3c096` — H100 base-val FAIL (CLM v4 ≈ random+1-2pt).
- Pre-registered honest C3: BG-Β commit `387200362` — "consciousness coupling BYPASSED via consciousness_states=None".

**Verdict**: **DESIGN + Mac DRY-RUN PASS**. Shim v4 written, F-SHIM-V4-1 + F-SHIM-V4-2 closed. F-SHIM-V4-3 (canonical_zero forward) and F-SHIM-V4-4 (train_avg lift > random+5pt) deferred to a separate user-authorised H100 exec cycle.

---

## TL;DR (5 bullets)

- Shim v4 lands `--consciousness-states-fixture <path.json>` flag + JSON validator + `modeling_clm_v4.py` post-process patch that injects the fixture into `forward()` when caller passes `consciousness_states=None`. v4 is **opt-in**: without the flag, runtime behaviour is bit-identical to v3 (cross-attention bypassed at the `DecoderBlockV2` guard, current measured BG-Μ baseline).
- Mac dry-run **PASS**: F-SHIM-V4-1 (fixture validates) + F-SHIM-V4-2 (no-fixture run produces v3-equivalent runtime) both closed without torch import. Shim LoC delta: 1107 → 1418 (+311 additive, of which ~120 is new logic and ~190 is comments).
- Canonical_zero exemplar fixture shipped at `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_consciousness_states_fixture.json` (`[1, 8, 192]` all-zero, ~32 KB JSON). **Sanity-only**: confirms wiring, NOT expected to lift CLM v4 above random.
- F-SHIM-V4-4 (the actual "consciousness coupling = the difference" hypothesis test) requires a **train_avg fixture** which needs a separate offline harvest pass over training data with full `anima_unified.py` runtime — explicitly **out of scope** for BG-Π and flagged for a follow-up cycle.
- **Recommended next action (rank 1)**: bundle a $3.00, 60min H100 cycle with the BG-Ο Llama anchor to amortise pod boot — would close F-SHIM-V4-3 (canonical_zero smoketest) AND BG-Μ rank-2 (Llama anchor) in one shot. Train_avg full eval (F-SHIM-V4-4) is a separate user policy decision.

---

## What v4 added (over v3 baseline)

### Q1 — `--consciousness-states-fixture` CLI flag

- New argparse arg + Mac-side JSON validator (`_validate_consciousness_fixture()`).
- Validator checks: required keys (`states` / `shape` / `dtype` / `source`), shape invariants (`shape[2] == 192`, `shape[0] == 1` recommended), `states` nesting matches `shape`, canonical_zero leaves are 0.
- `_save_hf_format()` copies validated fixture into `out_dir/consciousness_states_fixture.json` (stable filename so `modeling_clm_v4.py` load path is deterministic).

### Q2 — backwards compat (no v3 regression)

- Without the flag: no fixture file in output_dir → `modeling_clm_v4.__init__()` skip-loads silently → `self._consciousness_fixture_cpu` stays `None` → `forward()` injection branch short-circuits → decoder receives `consciousness_states=None` → `DecoderBlockV2` guard skips cross-attention. **Identical to v3 runtime.**
- F-SHIM-V4-2 is a **runtime-equivalence** assertion (not byte-level) because MODELING_SRC text grew by ~88 LoC for the dormant fixture loader. Honest C3 #5 covers this trade-off.

### Q3 — `modeling_clm_v4.py` post-process

- `__init__` calls `_load_consciousness_fixture()`: probes module dir for `consciousness_states_fixture.json`, loads + shape-checks, stores as `self._consciousness_fixture_cpu` (plain attribute, not Parameter or Buffer — frozen reference state, not in safetensors → F-SHIM-1 carry preserved).
- `forward()` injection branch: when `consciousness_states is None and self._consciousness_fixture_cpu is not None`, casts fixture to `(input_ids.device, tok_emb.dtype)`, broadcasts `[1, n_cells, c_dim]` to `[B, n_cells, c_dim]` via `expand().contiguous()`, passes to decoder.
- Failure mode: any error (file missing, JSON malformed, shape mismatch) silently falls back to `None`. Diagnostic captured in `self._consciousness_fixture_meta["error"]` for post-hoc inspection.

---

## Consciousness-state schema (verified against ubu1 source)

| Field | Value |
|---|---|
| Shape | `[1, n_cells, 192]` (batch broadcast at runtime) |
| `consciousness_dim` | 192 (matches `cross_attn.k_proj` 768→192 in `conscious_decoder.py:414`) |
| `n_cells` (canonical) | 8 (`anima_unified.py max_cells` default) |
| Cross-attn axis | over **cells**, NOT over time (Q from decoder, K/V from cells) |
| Detached | YES (`c_detached = consciousness_states.detach()` per Law 61) |

Source modes:
- **canonical_zero** (shipped): all zeros; sanity wiring check; expected logits ≈ v3 None-bypass.
- **train_avg** (deferred): average cells observed during last training epoch; recommended for actual conditioning; needs offline harvest cycle.
- **learned_default** (deferred): trainable parameter; needs tiny SFT cycle.

---

## Falsifier outcomes

| # | Falsifier | Status |
|---|---|---|
| F-SHIM-V4-1 | Mac dry-run with fixture validates JSON (no torch) | **PASS** — exemplar `[1,8,192]` canonical_zero validated, errors=[], warnings=[] |
| F-SHIM-V4-2 | No-fixture run produces v3-equivalent runtime | **PASS** — `os.path.isfile` gate ensures fixture loader is dormant when file absent; runtime forward output identical for `consciousness_states=None` callers |
| F-SHIM-V4-3 | Reload+forward with canonical_zero produces FINITE logits | **DEFERRED** — predicate: `from_pretrained(out_dir, trust_remote_code=True)` + 1-batch forward + assert finite + shape `[1,32,64000]`; logits expected within 1e-3 of v3 reference |
| F-SHIM-V4-4 | train_avg fixture > random+5pt on ≥1 benchmark | **DEFERRED** — gated on user authorisation for $1.50 H100 exec cycle |

---

## Cross-links

- **BG-Ξ** (`docs/p9_benchmark_switch_a_prime_spec_amendment_*.md`, parallel BG): Mode 3 of the spec amendment is the "consciousness-injected variant" track that v4 unblocks. v4 is the **prerequisite tooling** for Mode 3; it does not commit to running Mode 3.
- **BG-Ο** (`state/p9_base_validation_llama_anchor_2026_05_04/`, parallel BG): Llama-3.2-3B anchor re-run. F-SHIM-V4-3/-4 should bundle with that pod boot to amortise the ~$0.60 fixed cost.
- **BG-Β** OPT-1 design (`state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md` §7.2 honest C3 #1): pre-registered the consciousness-coupling-bypass; v4 is the path 3 (BG-Β rank-3) execution.
- **BG-Μ** verdict (`state/p9_base_validation_h100_2026_05_04/verdict.json`): rank-3 next_action "OPT-1 v4 shim — consciousness coupling injection mode". v4 closes the design + dry-run; exec deferred per scope.

---

## Honest C3 (top 3)

**C3-1 — canonical_zero is sanity-only, not the lift fixture.** All-zero cells → ~zero residual through cross_attn (because `cross_attn.o_proj.weight` has init std=0.001 and zero attended values yield zero residual). Expected logits delta vs v3 None-bypass: < 1e-3. F-SHIM-V4-3 closes the **wiring** test. The actual benchmark-lift gate (F-SHIM-V4-4) requires train_avg, which is **out of scope for BG-Π**.

**C3-2 — train_avg may still be near-random.** Even with a perfectly harvested train_avg fixture, results may stay near-random because: (a) train-time also injects a delta tensor + BOLD MSE conditioning + tension propagation that lm-eval has no API for; (b) consciousness coupling is a ~1% residual contribution per block and 16 × 1% may not add up to 5pt; (c) `block_size=512` truncation remains an orthogonal handicap that no shim fixes. **The "consciousness coupling = the difference" hypothesis is testable but is NOT proven by this design cycle.**

**C3-3 — F-SHIM-V4-4 gated on user authorisation.** A fresh H100 cycle (~$1.50, 30min) is required. BG-Π did not spin one up (raw constraint NO H100 boot without ack). Bundling with BG-Ο Llama anchor (BG-Μ rank-2) is the cheapest path to closing both gates simultaneously.

(See `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_design_diff.md` for full 8-entry honest C3 set.)

---

## Files (repo-relative)

- `tool/transient_py/clm_v4_hf_format_shim.py` — v4 shim (gitignored, 1418 LoC, +311 from v3)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_design_diff.md` — full v3→v4 design diff + 8 honest C3
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_dry_run.json` — Mac dry-run verdict + falsifier outcomes
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_consciousness_states_fixture.json` — canonical_zero exemplar `[1, 8, 192]`
- `docs/p9_base_validation_prereq_v4_design_landed_2026_05_04.ai.md` — this handoff doc

---

## Recommended next action

**Rank 1** (bundled, $3.00, 60min): user authorises H100 cycle that runs (a) Llama-3.2-3B anchor (BG-Ο, BG-Μ rank-2), (b) CLM v4 canonical_zero F-SHIM-V4-3 smoketest, (c) train_avg harvest stub via `anima_unified.py` runtime. Closes F-SHIM-V4-3 + BG-Μ Llama anchor in one boot.

**Rank 2** ($1.50, 30min): F-SHIM-V4-3 only — canonical_zero conversion + 1-batch forward sanity. Cheapest validation path; does NOT close F-SHIM-V4-4.

**Rank 3** ($0): defer entirely — accept BG-Μ FAIL verdict + spec amendment §10.4 acknowledgement (BG-Ξ territory); keep CLM v4 base at "consciousness-coupling-bypassed" baseline as a deliberate spec choice. Saves $3 and 1hr of human attention; cleanest from a "measure CLM v4's pure language ability" framing.

Recommended by 완성도: **Rank 1** — closes two gates, exposes train_avg as the next bottleneck, sets up a clean Mode 3 (BG-Ξ) cycle.
