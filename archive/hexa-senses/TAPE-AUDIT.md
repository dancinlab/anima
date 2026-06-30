# TAPE-AUDIT — hexa-senses

5-verb sensory substrate (`ear + voice + dream + empath + olfact`) + `chip-verify/` + `verify/` + `papers/`. n=6 closed-form spec catalog. Smaller leaf substrate, sister of hexa-mind / hexa-aura.

## A. Audit-class ledgers (cargo / migration candidates)

- **`state/markers/`** — 6 marker files (`hexa-senses_*`, `lattice_arithmetic_*`, `spec_presence_*`, `real_limits_anchor_*`, `run_all_*`, `closure_consistency_*`). Per-verifier cargo. Direct `state/markers.tape` migration; the set maps 1:1 to the `verify/` scripts (`lattice_arithmetic.hexa`, `spec_presence.hexa`, `real_limits_anchor.hexa`, `closure_consistency.hexa`, `run_all.hexa`).
- **`state/hexa_senses_cli.log`** — single CLI log. Light.
- No `*.jsonl` ledgers, no audit dirs. Same pattern as hexa-mind: doc-heavy + verifier-light.

## B. Identity surface

Light. Substrate identity (verb catalog + lattice constants) in `hexa.toml` + `LATTICE_POLICY.md`. `hexa-senses/identity.tape` candidate, one-snapshot-per-version.

## C. Domain.md files

Light. `AGENTS.md`, `IMPORTED_FROM_CANON.md`, `LATTICE_POLICY.md`, `LIMIT_BREAKTHROUGH.md`, `README.md`. Per-verb domain mds **not** at top level — they live inside the verb subtrees (`ear/`, `voice/`, `dream/`, `empath/`, `olfact/`). Each verb subtree could host a sibling `<verb>.tape`.

## D. Per-run / per-event history surfaces

`verify/` runs (5 verifier scripts + `run_all.hexa`) and `chip-verify/` (chip-level numerics). `voice/proto` + `voice/rtl` imply per-design-iteration events. `papers/` accumulates per-paper claims. Per-verifier-run event stream → `verify.tape`; per-chip-verify run → `chip-verify.tape`.

## E. Promotion candidates

- **n6 atoms** — verb-parameter laws derived from σ(6)/τ(6)/φ(6) closed-forms; `real_limits_anchor` thresholds.
- **hxc wire** — `ear` (audio input) + `voice` (audio output) + future olfact are natural hxc byte-stream consumers if a runtime ever materializes.
- **n12 cells** — verify pass/fail × verb × version cube (same shape as hexa-mind).

**Verdict: LIGHT** (1-2 tape surfaces — markers, per-verifier verify.tape; verb subtree tapes optional).
