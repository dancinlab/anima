# Compose-2 CLMConvMoE 7B rho-form recovery gate — 2026-08-11

Status: FALSIFIED — rho-form and pair-oracle recovered, but normal/recovery stayed below the
frozen positive bar; production serving was not run.

This gate follows `state/store_causality_7b_serving_2026_08_11`. It keeps the frozen rho-form
detector, compose-2 fixture, causal controls, seeds, and bars unchanged. It reuses
`cli/evaluate.py --rho-axon --rho-axes form`, `cli/train.py --store-bridge`, the existing CLMS
lane, `core/decode.py`, and the existing chat `Substrate` boundary. It adds no engine, evaluator,
prompt, corpus, randomization, or threshold.

## Root-cause hypothesis and fixed diagnostic order

The failed serving checkpoint descends from `dancinlab/clm-7b-undertrained-step2000`, whose model
card identifies it as step 2,000 of 3,500 and WIP/undertrained. Store training froze its tensors and
trained only the CLMS trailer. The diagnostic found that the lane itself remains a store-absent
passthrough, but warm-start rebuilt the legacy-global trunk as position-normalized and serialized a
`CNRM` marker. That changed the common forward pass despite `--freeze-trunk`.

The following read-only checks run in this order on Vast.ai:

1. score the step-2,000 base and the failed final store checkpoint through the same canonical
   rho-form-only path and compare all raw continuations and scores;
2. score the compatible completed step-3,500 trunk once through that unchanged path;
3. stop if step 3,500 is below the frozen `0.70` form-rate bar;
4. only if it passes, train a fresh canonical parity CLMS lane on that trunk for the already
   established total 2,200 store updates, then verify that store-absent rho-form output remains
   unchanged;
5. run pair-oracle first; below `0.90` stops causal interpretation. A pass unlocks the unchanged
   normal -> clue-A removal -> clue-B removal -> address shuffle -> recovery battery;
6. only if rho-form, pair-oracle, and the causal battery pass, repeat serving, HTTP/WebSocket,
   performance, 30-minute soak, and rollback QA before any production decision.

## Frozen inputs and bars

- source baseline: Git commit `1b3de6714`
- failed store checkpoint: private HF repository
  `dancinlab/anima-store-causality-7b-longrun-2026-08-10`, commit
  `0e26f4623c514bc6192a93f14e7a466a6f8bd59a`, SHA-256
  `0e4ff48cbba04ac49f1f005350a9c51a74de87393c35c20551b9374a1a2c9b04`
- diagnostic parent: `dancinlab/clm-7b-undertrained-step2000`, SHA-256
  `05b558e1fe2d4fc507f3826fcd44e9fe8b877b4a576df615b8bd48604b58fabe`
- fixed completed trunk: private HF repository `dancinlab/clm-7b-undertrained-step3500`, commit
  `c3c6d127545ccde6737fb96f99b51a2ac581d9e9`, `clm_7b.clm` SHA-256
  `5e0db1371bc4ed7246ef5adcebe245c3991c053acd5fbde8107873add7853de5`
- frozen compose-2 dataset: private HF repository
  `dancinlab/anima-store-causality-compose2-2026-08-09`, commit
  `8f29c2f16f214734d9b5fa4010c57c48fff3979e`
- store recipe: seed 7, 24-byte window, batch 32, direct-address weight 1.0, frozen trunk,
  source-preserving global normalization, value centering, canonical parity lane 10
- rho-form: canonical five probes and seeds, KWR `>=0.50`, form-rate `>=0.70`, self-shuffle
  `<=0.05`; no alternate draw or retry
- causal bars: pair-oracle `>=0.90`; normal/recovery `>=0.75`; controls `<=0.56`
- serving bars: unchanged from `state/store_causality_7b_serving_2026_08_11/README.md`

No result-dependent step extension, alternate checkpoint, seed, data regeneration, decode option,
or bar change is allowed. Infrastructure failure may be rerun only with identical inputs. Models,
checkpoints, and training data remain HF-only in private repositories under `dancinlab`; Vast.ai
scratch is deleted after verified upload. Heavy work never runs on mini. `ING.jsonl` and
`stream_mi.json` remain untouched. A failed result is recorded without production deployment.

## Root-cause amendment after the fixed diagnostic

The registered diagnostic measured the step-2,000 source at rho-form `0.60`, the derived CLMS
checkpoint at `0.20`, and the fixed completed step-3,500 source at `1.00`; all self-shuffle controls
were `0.00`. Raw cache entries also differed between the step-2,000 source and derived checkpoint,
falsifying the original assumption that the complete store checkpoint was store-absent identical.

The configuration trace explains the difference: the source `.clm` has no `CNRM` trailer and is
therefore legacy-global, while the store runs explicitly rebuilt it with `--trunk-norm position`.
Changing only that reduction changes every trunk activation. The recovery run is therefore amended
to use the source's canonical global setting. This is a root-cause correction, not a result-driven
model, data, seed, step, decode, or threshold change. The common warm-start path must first reject
future source/request normalization mismatches, with a regression proving both rejection and a
matching warm-start. The original registered position setting remains documented here as the
falsified configuration.

## Result

The common warm-start path now reads the source `.clm` normalization through the canonical trailer
walker and refuses a source/request mismatch before training. A matching legacy-global warm-start
still round-trips byte-identically. The focused Vast.ai H100 regression suite passed `20/20` and
the local CPU-capable subset passed `7/7` (`6` Torch-dependent tests skipped because mini has no
Torch).

The fixed diagnostic and registered recovery run produced:

- step-2,000 source rho-form: `0.60`; failed position-normalized store checkpoint: `0.20`;
  completed step-3,500 source: `1.00`; every self-shuffle control: `0.00`;
- fresh source-preserving global checkpoint rho-form: `1.00`, self-shuffle `0.00`; its five raw
  store-absent continuations are exactly equal to the step-3,500 source cache
  (`9ac73185e0d4049579e30cb87276212a8a96864f41306b1c34fcd200b2594114`);
- pair-oracle: `1.0000`, which unlocked the complete causal battery;
- normal `0.6094` -> clue A removed `0.5469` -> clue B removed `0.4609` -> address shuffled
  `0.4688` -> recovery `0.6094`.

The controls are at or below the measured chance `0.50 + 0.06` ceiling and recovery exactly
matches normal, but normal and recovery both miss the frozen `0.75` positive bar. The engine-native
verdict is therefore `FALSIFIED`. No retry, extension, seed/data/decode/bar change, serving test, or
production deployment was performed after that failure.

The failed checkpoint and exact-resume state are preserved only in the private HF model repository
`dancinlab/anima-store-causality-7b-rho-form-recovery-2026-08-11`; HF metadata independently
matches both local SHA-256 values and byte sizes. The Vast.ai H100 instance was deleted after
upload (active rentals `0`, estimated cost `$2.82`). Machine-readable evidence is in `result.json`.
