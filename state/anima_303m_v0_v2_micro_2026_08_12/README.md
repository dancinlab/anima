# 303M V0/V2 micro experiment — 2026-08-12

Status: **COMPLETED — FAIL-V0-V2-MICRO**.

The preceding English R0 did not fail because response supervision was silent: it failed after
the complete-document sampler and response CE were both active. The narrower shared cause is that
only 226 of 2,308 selected dialogue documents fit the 512-byte causal window; 2,082 documents were
dropped before sampling. Repeating 303M training on that support set is prohibited.

This experiment changes one data-construction axis first. It keeps the pinned human-reviewed
OpenAssistant source, eligibility, official splits, ByteGPT architecture, 512-byte block and
canonical chat format. The control is the previous one-best-path-per-root corpus. The treatment
uses every eligible human assistant turn and serializes the longest complete alternating ancestry
suffix that fits 513 bytes. It never slices a UTF-8 sequence, role prefix, prompt or response.

Only after the data gates pass, matched tiny ByteGPT arms compare V0 base CE with V2 base CE plus
the existing `answer_ce` term. The test reuses `cli/train.py`, `core/generator.py` and the existing
conversation structural checks. It does not create another trainer, decoder or evaluator.

Promotion is fail-closed. Invalid role alternation, partial turns, train/validation overlap, panel
contamination, less than 95% coverage of otherwise eligible fitting assistant turns, or any
serialized document over 513 bytes stops before GPU work. Tiny failure stops before 303M. A tiny
pass permits only a separately recorded single-seed 303M screen; it does not unlock R1 or
production. Exact conditions and stop rules are frozen in `protocol.json`.

Progress and raw results will be appended here without changing the registered thresholds.

## Result

The data treatment passed every registered integrity gate. It retained all 9,125 assistant targets
whose complete final prompt/response pair can fit the unchanged window, producing 8,635 training
and 458 validation documents. Canonical alternation errors, partial turns, cross-split exact
overlap and panel contamination were all zero. The largest serialized document was exactly 513
bytes. The private immutable dataset is
`dancinlab/anima-303m-v0-v2-turns-2026-08-12@17a1e4676d684a99a54208549445952302f389fa`.

This also exposed a harder block limit: 15,114 of 24,239 valid assistant targets (`62.35%`) have a
final prompt/response pair that cannot fit 513 bytes without truncation. They remain excluded and
were not counted as retained evidence.

The matched 0.892M ByteGPT arms ran locally on Apple MPS. Both V0 and V2 passed the single-document
test and reproduced the complete registered response exactly, proving that corpus framing,
training, serialization and canonical decode can learn one causal exchange. Both failed the
100-document test:

- V0 held-out CE descended to `2.48189`, but target recovery and structural generation were `0/8`.
- V2 held-out CE descended to `2.54702`, response CE fired on 1,031,998 positions, but target
  recovery and structural generation were also `0/8`.
- V2 was `+0.06513` CE worse than V0, outside the registered `+0.02` non-inferiority bar.
- Outputs collapsed into fragments such as `Whe s s a are are…` and `I an an an…` rather than
  meaningful answers.

The result is therefore `FAIL-V0-V2-MICRO`. No Vast.ai instance was rented, no 303M run or extra
seed was started, and R1/production remain locked. Dataset and all 58,545,350 bytes of model/raw
evidence were preserved and hash-verified in private HF `dancinlab` repositories. Full metrics are
in `result.json`.

The next allowed experiment is a separately preregistered V1 context-length micro comparison.
Adding more 303M steps or starting recurrent workspace on the present mouth remains prohibited.
