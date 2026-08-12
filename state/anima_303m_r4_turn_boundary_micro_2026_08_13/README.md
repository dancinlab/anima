# R4 assistant-turn boundary micro experiment — 2026-08-13

Status: **COMPLETED — FAIL-R4-TURN-BOUNDARY-MICRO**.

The objective micro experiment falsified payload-only response CE at its single-document positive
control. It learned the complete target but continued with junk because the raw-byte vocabulary has
no EOS token and the loss excludes the only canonical stop signal: the next line-start `user:` role
boundary. The existing additive/full CE arms learn that delimiter incidentally from full-window CE.

This experiment changes only the supervised span boundary. It extends the existing answer-mask
path with an assistant-turn mode that supervises assistant payload, internal newlines and the next
canonical user-role delimiter, but never the following user content. It reuses the same immutable
data views, ByteGPT, sampler, seed, optimizer, schedule, steps, serializer, generator, scorer and
bars. Payload-only response CE is the preserved negative control; assistant-turn-only CE is the
treatment. No EOS token, vocabulary, data, decoder, stop parser or evaluator is added or changed.

The treatment must exactly pass the single-document control before the 100-document arm. It then
must descend on held-out full CE, produce at least six non-empty and six distinct replies, recover
the first 16 target bytes on at least six of eight probes and structurally pass all eight. Failure
blocks 303M, IIT-mouth coupling, participant mounting and production. A pass allows only a separate
303M single-seed preregistration. Conditions and stop rules are frozen in `protocol.json`.

## Result

The mask regression selected assistant payload, internal newlines and the next `\nuser: ` role
delimiter while leaving following user content unselected. Protocol, parent-result, panel, source
file and immutable view hashes all matched. The turn-only single-document treatment reproduced the
registered response exactly and stopped at the canonical role boundary, fixing the direct failure
of payload-only response CE.

The fixed 100-document arm then ran for 600 steps on local Apple MPS with two CPU threads. Held-out
full CE descended from `5.49208` at step 1 to final `2.66085`; turn-only CE was active on all 600
steps. All eight outputs were non-empty and distinct. The meaning gates nevertheless failed:
target-prefix recovery was `0/8` and structural generation was `0/8`. Outputs remained loops such
as `the the...`, `an an...`, `toure toure...` and `ion ion...`.

The verdict is `FAIL-R4-TURN-BOUNDARY-MICRO`. The missing stop target was a real shared-flow defect,
but it was not the sufficient cause of the 100-document repetition attractor. No 303M model, IIT
mouth coupling, participant mount or production deployment is allowed by this result. No Vast.ai
instance was rented.

The single- and 100-document checkpoints, exact-resume states, logs and lossless results are
preserved with the preceding controls in private HF revision
`dancinlab/anima-303m-r4-mouth-objective-micro-2026-08-13@9d7641389b1ddff73bd12f17f155f448500d1edb`.
Its manifest registered and re-downloaded 26 files totaling 73,146,099 bytes; every SHA-256 matched.
Focused Python QA passed `41/41`; full Python/CHAT QA passed `153` tests and `3` subtests with one
expected unavailable CUDA/CuPy case skipped. Canonical CLI help, compile and JSON checks passed.
The built wheel's training and evaluation modules also passed from an isolated install target.
Vast.ai/H100 use and cost were zero, the API reported zero active instances, and temporary local
model/data copies were removed after HF verification. `ING.jsonl` and `stream_mi.json` were not
modified.

The chat serving path was not changed and no failed mouth was mounted. The unchanged LaunchAgent
remains running; public HTTPS returned `200` and WebSocket returned `hello` with the honest blocked
status `anima_alive=false`. No broker restart or production deployment was performed.
