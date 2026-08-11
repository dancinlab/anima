# Anima 303M R0 local micro audit — 2026-08-12

Status: COMPLETE — 25 local experiments exhausted the shared-path hypotheses; R1 remains locked.

Follow-up execution policy (2026-08-12): all future Anima implementation, experiments, training,
evaluation, runtime QA, and deployment use the canonical Python `anima-py` path only. Existing Hexa
artifacts are retained for provenance but are no longer an execution or release gate. The source
`python -m anima_py` entry smoke, Python compilation, JSON validation, Markdown diff validation, and
the targeted evaluator/trainer regression (`15 tests + 3 subtests`) passed after this policy update.

This audit started with the ten predeclared low-load local experiments and continued until the shared
evaluator, corpus, sampler, optimizer, ByteGPT forward, initialization, serialization, and decode
hypotheses were exhausted. It did not train or load a 303M checkpoint, change any R0 data, seed,
endpoint, decode option, detector, or threshold, and it did not unlock R1.

## Root cause

The English rho-form detector calls `core/rho_fan.py::_rho_fan_dict_load`, which was documented as a
235k-word lexicality check but silently fell back to only 49 stop/concept words whenever
`/usr/share/dict/words` was absent. The three H100 evaluations used that fallback: recalculating all
75 stored KWR values with the 49-word set reproduced every stored value exactly. Replaying the same
raw generations with the intended Web2 bytes changed the aggregate form rate from `0.40/0.60/0.20`
to `1.00/1.00/0.80`, but it also raised the fixed self-shuffle control to `0.20/0.20/0.20` against
the unchanged `0.05` cap. The complete rho-form verdict therefore remains FAIL for all three seeds.

This replay is diagnostic evidence, not a replacement terminal checkpoint evaluation. A 3,000-draw
null calibration found that the Web2 self-shuffle false-positive rate is `0.216`, because Web2 includes
single-letter entries such as `e`, `t`, `a`, and `n`. That is incompatible with the frozen `0.05`
control cap. Therefore merely rerunning the three HF checkpoints cannot certify R0: the original
`R0_FAILED_0_OF_3` conclusion is now `INVALID-MEASUREMENT`, and R1 remains locked. No word filtering,
shuffle rule, threshold, seed, or output was changed after seeing the result.

The shared Python and Hexa detector now require the exact Web2 SHA-256
`be41ad97963bf8dabedd5871d5d691596175269d540956b0f9965a885c2bbab9`. Missing or different bytes fail
before model scoring instead of changing the metric. Every new Python rho panel also records the
lexicon SHA and word count. The evaluation input is pinned in the private
HF dataset `dancinlab/anima-rho-form-web2-2026-08-12` at revision
`0ec91c65c3d97c6a20a691fbf7f3cf6216fa4d30`.

## Exhaustive experiment ledger

1. **Evaluation replay:** fallback KWR reproduced 75/75 stored scores. Canonical Web2 replay cleared
   the aggregate form bar at `1.00/1.00/0.80`, but every aggregate failed because self-shuffle was
   `0.20`; several English cells failed the same control. Korean cells retained `0.00` shuffle.
2. **Checkpoint series:** held-out CE continued descending through step 14,000 on all seeds. Only the
   fixed final endpoint has raw rho text; no intermediate rho evidence exists to select an endpoint.
3. **UTF-8 roundtrip:** all five corpora contain zero invalid UTF-8 bytes; surrogateescape roundtrip
   and 5,000 sampled 513-byte windows were byte-exact. Two Korean 95% split offsets fall inside a
   code point, but the byte-native target stream loses no byte.
4. **Sampler dry-run:** the exact seed-42 interleaved sampler produced 448,000 windows in the expected
   proportional mix (maximum fraction error `0.00113`). Each cell received only `0.850–0.860` effective
   passes; total targets were 229,376,000 bytes, `0.7568` target byte per parameter.
5. **Contamination audit:** the tail split is byte-disjoint but not document-disjoint. The broad
   dialogue cell had 1,363,153 normalized train-line hits in its validation tail; the sampled SimHash
   audit found 64,531 near pairs. Its very low `~0.15` validation CE is therefore not clean generalization
   evidence. Frozen R0 data was not edited.
6. **LR/optimizer trace:** all 45 logged schedule points match the shared warm-up/cosine function
   within `4.55e-12`; AdamW beta2 `0.95`, weight decay `0.1`, and the `3e-4 → 3e-5` schedule match the
   protocol.
7. **Evaluation path parity:** every seed used final step 14,000 `.bin`, canonical `anima evaluate`,
   ByteGPT dispatch, five corpora, generation length 40, and wrote the registered rho JSON.
8. **Tiny single-batch overfit:** the existing 120,576-parameter ByteGPT configuration reduced CE
   from `42.77996` to `5.48e-7` in 200 CPU steps.
9. **Tiny exact resume:** the existing uninterrupted versus save/restore trajectory regression passed.
10. **Short decode regression:** canonical serialization and decode generated the exact held-out bytes
    `ows through memo`; repeated decode was deterministic, KV/full streams matched, and UTF-8 was valid.

11. **Full Web2 self-shuffle replay:** aggregate shuffle was `0.20` for every seed. English cells also
    failed controls while Korean cells stayed at `0.00`; the full rho-form verdict remained `0/3`.
12. **Shuffle null calibration:** 30 stored English outputs × 100 deterministic shuffles produced
    3,000 null draws. False-positive rates were `0.00133` for the accidental 49-word fallback and
    `0.216` for Web2. Single-letter Web2 entries dominated the false matches.
13. **Frozen-panel contamination:** none of the 20 exact rho-form concept strings appeared in either
    side of any of the five corpus splits.
14. **Sampler RNG separation:** 100 uninterrupted train draws matched `50 → RNG snapshot → 50` exactly;
    interspersed validation draws did not move the train stream. Model seeds 7/11/13 intentionally used
    the same seed-42 corpus stream.
15. **Validation aggregation audit:** `final_val_ce_pooled` was an equal-cell macro average, not a
    sample-count-pooled CE. The macro values were `0.999064/0.999855/1.009928`; proportional values were
    `0.617689/0.617241/0.620623`. The trainer now emits the truthful additive field and keeps the old key
    only as a compatibility alias.
16. **Corpus multiplicity:** broad dialogue contained 2,182,065 substantive train lines but only
    711,831 unique normalized lines; 1,470,234 were duplicate instances and one line occurred 43,547
    times. Its validation tail contained 69,285 duplicate instances. The other cells were nearly clean.
17. **Byte-window boundary proof:** 1,000 train and 100 validation windows per corpus stayed inside the
    exact mmap regions and all returned `512→512` pairs. Byte separation works; document separation does
    not. Corpus script census also confirmed the intended English/Hangul register assignments.
18. **Initialization scale matrix:** PyTorch defaults initialized tied byte embeddings at standard
    deviation about `1.0`. Random CE grew from `23.04` at width 32 to `159.66` at width 256; the actual
    R0 step-1 CE was `531.87–550.08`. Canonical GPT initialization (`0.02` plus residual projection
    scaling) held the same matrix near the uniform CE `5.545`.
19. **Initialization seed sweep:** all 20 width-128/layer-8 random starts landed between CE `5.5454` and
    `5.6538`; embedding standard deviation stayed `0.01990–0.02021`. The existing 120,576-parameter
    structure and checkpoint byte grammar were unchanged.
20. **Forward/codec interventions:** changing future input bytes moved suffix logits but changed prefix
    logits by exactly `0.0`. Torch↔engine last-logit maximum error was `5.87e-8`; KV and full-forward
    streams matched across 17 block rollovers; identical sampler seeds repeated exactly and different
    seeds diverged. Random byte output can be invalid UTF-8, validating lossless surrogate evidence.
21. **Canonical CLI smoke:** the installed `anima-py train` dispatcher ran the existing five-cell
    ByteGPT path for two CPU steps. Step-1 CE was `5.54626`; the emitted summary carried canonical
    initialization provenance, both macro/legacy CE fields agreed at `5.53918`, and the `.bin` was
    serialized through the normal bridge.
22. **Cell-registration guard:** the same canonical entry with four usable corpora and
    `--require-cells 5` exited `1` before its first update and named the incomplete register.
23. **Canonical evaluator smoke:** `anima-py evaluate --rho-axon` wrote a raw panel containing the
    exact 234,461-word count and pinned Web2 SHA. The tiny random model's score was explicitly
    directional and was not interpreted.
24. **Full-width initialization isolation:** five width-768/layer-1 models reconstructed the former
    PyTorch defaults while keeping the tied head. Their mean initial CE was `521.39`, matching the
    R0 step-1 range `531.87–550.08`; the canonical twins averaged `5.636`. Thus the causal mechanism
    is the tied head inheriting `nn.Embedding` scale near `1.0`, not the dataset or optimizer.
25. **Resource-lifetime regression:** checkpoint inverse and decode QA exposed unclosed binary readers.
    The shared CLM/ByteGPT decode and serializer readers now close deterministically; the affected
    suite passes with `ResourceWarning` promoted to an error.

## Confirmed shared-path defects

- Host-dependent rho lexicon silently changed the measurement.
- The intended Web2 lexicon makes the frozen byte-shuffle control intrinsically high-noise.
- Broad dialogue byte-tail validation is heavily duplicated across train and validation.
- The trainer mislabeled an equal-cell macro CE as pooled CE.
- ByteGPT inherited PyTorch embedding initialization at standard deviation about `1.0`, making
  random-start CE scale catastrophically with width.

The first, fourth, and fifth defects were fixed in shared code without changing any frozen R0 result.
The second and third are recorded blockers: repairing them would require a separately preregistered
instrument and an immutable new corpus revision, respectively. They were not tuned or rewritten here.

Final regression passed 17/17 executable tests with one expected CUDA/CuPy skip. Python compilation,
JSON validation, Markdown diff checks, canonical two-step train/evaluate smokes, checkpoint overwrite,
and the private HF dataset revision also passed. The unavailable compiled Hexa smoke is preserved as a
historical QA fact but is not a remaining task under the Python-only execution policy. Models and training data remained under HF
`dancinlab`; temporary corpus and tiny-model files were diagnostic only and were not added to Git or
model custody. `ING.jsonl` and `stream_mi.json` remained untouched.
