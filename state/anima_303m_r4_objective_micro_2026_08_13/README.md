# R4 mouth objective micro experiment — 2026-08-13

Status: **COMPLETED — FAIL-R4-OBJECTIVE-MICRO**.

The completed V1 experiment improved complete-dialogue coverage from `37.6%` at 512 bytes to
`91.3%` at 2048 bytes, but both 2048-byte arms collapsed into `an/the/ic` repetition. Increasing
context is therefore prohibited as the next lever. The remaining shared-flow question is narrower:
the canonical trainer has full next-byte CE and an additive answer CE, but no standard dialogue-SFT
mode in which only assistant response targets receive language-model gradient. The prior V2 arm
did not test that claim because its loss was `full_ce + answer_ce`.

This protocol changes only that objective-selection axis. It reuses the immutable SHA-ordered
100-document and 32-document held-out views, 512-byte block, existing ByteGPT, canonical complete
chat-document sampler, serializer, greedy generator, structural scorer, seed, optimizer, schedule,
step count and bars from the completed V0/V2 micro run. Three matched arms are run from identical
initial weights: full CE, the existing additive response CE, and assistant-response-only CE. The
new mode extends `cli/train.py`; it is not a new trainer or evaluator, defaults off, is recorded in
the exact-resume recipe and fails closed if a framed batch has no supervised assistant bytes.

All three arms must first exactly overfit the registered single exchange. On 100 documents the
response-only arm must finish below its initial held-out full CE, produce at least six non-empty and
six distinct replies, structurally pass all eight probes, and recover the first 16 target bytes on
at least six probes. The existing full/additive arms are controls and must be reported losslessly;
they cannot authorize promotion. A response-only failure blocks 303M training, IIT-mouth coupling,
participant mounting and production. A pass permits only a separately preregistered single-seed
303M screen. Exact hashes, conditions and stop rules are frozen in `protocol.json`.

Progress and lossless raw outputs will be appended here without changing the registered bars.

## Result

All protocol, panel and immutable data-view hashes matched. The full-CE and additive-response-CE
single-document controls reproduced the registered assistant response exactly. Response-only CE
generated the entire registered response exactly and then continued with meaningless suffix bytes:
`...questions!ions toues!ionsioutacould ses`. Its response CE was active on every one of 300 steps
and fell to `0.0805` on the last batch, so the failure is not a silent loss or missing target.

The fail-closed single-document gate therefore failed and the registered 100-document arms were
not run. The verdict is `FAIL-R4-OBJECTIVE-MICRO`; 303M, IIT-mouth coupling, participant mounting
and production remain blocked. This identifies a narrower shared-flow defect: byte vocabulary 256
has no EOS token, while the response-only mask excludes the next role boundary. Full/additive CE
learn the boundary from full-window targets; response-only has no supervised way to stop. A new
experiment must be separately preregistered before changing that mask.

All three single-document checkpoints, exact-resume states, logs and lossless results are preserved
in private HF revision
`dancinlab/anima-303m-r4-mouth-objective-micro-2026-08-13@9d7641389b1ddff73bd12f17f155f448500d1edb`.
