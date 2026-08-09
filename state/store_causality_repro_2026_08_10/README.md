# Compose-2 causal reproducibility — 2026-08-10

Status: COMPLETE — `NOT-REPRODUCED`.

This follow-up does not change or regenerate the frozen compose-2 panel, controls, randomness,
or bars in `state/store_causality_2026_08_09`. It reuses the canonical `anima-py train` and
`anima-py evaluate --store-causality` paths at commit `989b5a5cf`.

Frozen repetition:

- warm start: `.fire-recover/h9672_rv_sweep/RV3c_13_CONFIRM_orc1.00_p1_0.99_flip0.99.clm`
- architecture: d3784 / L4 / E3, frozen trunk, position-normalized dual CLMS lane
- training: 24-byte store window, store batch 32, 24,000 steps, direct address supervision
- seeds: 7 (existing positive checkpoint) and 11 (new independent repeat), as pre-registered by H_9888
- gate order: pair-oracle first; controls are interpreted only if pair-oracle is at least 0.90
- unchanged bars: normal/recovery at least 0.75; each control at most measured chance + 0.06

Planned verification: full Python regression collection on the pod, focused store regressions,
existing seed-7 checkpoint re-score, seed-11 training, then the same five-arm causal battery only
after seed 11 passes pair-oracle. Failures are recorded without tuning or rerunning the panel.

The first bare `pytest -q` attempt exposed a repository-level collection defect: without pytest
discovery configuration it imported historical files such as
`state/g1_density_phase_transition/corpus/build_and_test.py`, whose module-level path launches an
8,000-step GPU experiment. The run was stopped before training and `pyproject.toml` now limits
canonical collection to the active unit/regression suites. Frozen archive experiments remain
directly runnable but are no longer mistaken for tests.

The first constrained collection then exposed two more discovery assumptions: repository modules
need the root and `core/` on the import path, while `agent/domains/CHAT/test_broker_multiuser.py` is
a live-server integration script with module-level execution, not a pytest unit. The canonical
configuration now supplies those import paths and leaves the broker scripts to their explicit
runtime verification command.

## Result

The existing seed-7 checkpoint was re-scored on the Vast.ai RTX 3090 CUDA path and reproduced the
record exactly: pair-oracle 1.0000, normal/recovery 0.9140625, clue-A removal 0.5000, clue-B removal
0.484375, and address shuffle 0.453125 (`SUPPORTED-CAUSAL`).

The seed-11 repeat completed all 24,000 training steps in 1,257.4 seconds. Its terminal training
batch reported address accuracy 1.0, store accuracy 1.0, and address CE 0.0000021. Engine-native
pair-oracle then scored only 32/128 = 0.2500. The existing evaluator returned
`INVALID-INSTRUMENT` and did not execute normal, clue-removal, address-shuffle, or recovery arms.
No knob, seed, panel, randomization, or bar was changed and the failed run was not retried.

This isolates the remaining problem as multi-seed generalization in the shared training path: the
lane fits its sampled training rows but seed 11 does not carry the two-value fusion to held-out
pairs even when both correct addresses are supplied. It is not a frozen-trunk drift: the serialized
main model blob is byte-identical to the warm start; only the CLMS/CNRM trailers differ.

Recovered artifacts:

- `.fire-recover/store_causality_2026_08_10/seed11_repro/compose2_dual_causal_s11.clm`
  (`sha256 50ec38bc5742540e8bb9384f6bf22a35181dba510b6517c307184ffbd2076582`)
- matching recovery `.fire-recover/store_causality_2026_08_10/seed11_repro/compose2_dual_causal_s11.clm.pt`
  (`sha256 beab2a8338025495f949ae932f6b25259c41e3a00d165ad56dee3c71d4c266ce`)
- `train.log`, `train_summary.json`, and the evaluator's failed `result.json` beside them

QA on the pod: canonical pytest collection found 14 tests and all 14 passed. The seed-7 live
checkpoint battery reproduced exactly, seed 11 obeyed the pair-oracle early-stop ordering, and
both recovered checkpoint hashes matched the pod originals. Vast.ai instance `47293424` used an
RTX 3090 at $0.197037/hour for about 42 minutes before teardown (about $0.14); the active-instance
list was empty after teardown.
