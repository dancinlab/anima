# Anima 303M R0 proportional meaningful-conversation recovery — 2026-08-12

Status: **COMPLETED — FAIL-MEANINGLESS-REPETITION.** R1 and production remain locked.

The parent seed-7 run reduced train CE but failed meaningful conversation `0/14`. Its shared
training path gave each cell an equal number of windows, so the 1.30 MB Korean MRC cell received
the same byte exposure as each approximately 57 MB general cell. The corpus builder also collapsed
explicit chat-turn newlines while the evaluator seeded turns with newlines. This recovery changes
those two shared inputs before any new checkpoint is measured.

No new trainer or evaluator is introduced. `cli/train.py --sample proportional` already implements
training-byte-weighted selection and remains the canonical sampler. The run only exposes its
per-cell realized window counts in the normal training summary. The existing dataset builder keeps
canonical newlines between `user:` and `assistant:` turns, while exact dedup still uses normalized
document hashes.

The English dialogue cell remains the pinned, human-reviewed OpenAssistant path. KLUE MRC is
replaced because it is single-answer reading comprehension rather than conversation. The Korean
cell is the pinned Apache-2.0 `jojo0217/korean_safe_conversation` instruction/context/response
file. Empty-role records are rejected. Every source and output file is hashed, exact train-to-
validation overlap must be zero, and the fixed conversation panel is removed from training before
the private HF `dancinlab` revision is published.

The architecture, random initialization, seed 7, 14,000-step endpoint, optimizer, LR schedule,
greedy decode, 14 prompts, panel SHA-256, and every pass threshold are unchanged from the parent
run. The conversation gate runs before other language or consciousness diagnostics. A failure is
recorded as-is and keeps R1 and production deployment locked.

Execution order:

1. certify the unchanged conversation scorer controls;
2. build, audit, upload, and re-download the private immutable dataset revision;
3. verify proportional sampler frequencies and chat-turn newline preservation locally;
4. run the tiny Python corpus → trainer → checkpoint → evaluator flow;
5. run one 303M seed on a 24–48 GB non-H100 Vast.ai GPU;
6. evaluate the fixed meaningful-conversation panel first;
7. preserve model and raw responses in private HF `dancinlab`, record pass or failure, push Git,
   and delete the Vast.ai instance.

`protocol.json` is the execution SSOT. User-owned `ING.jsonl` and `stream_mi.json` must remain
untouched.

## Preflight record

- Protocol SHA-256: `b4b19bedb3a3765523f3c41a5f1f54c64437eaa06bca3e416f96cf7f691885d8`.
- Private HF dataset: `dancinlab/anima-303m-r0-proportional-conversation-data-2026-08-12`
  at immutable revision `ee143002d9494cac4ed4a821dadfb5ece60c1e74`.
- The build saw 649,355 candidates, retained zero exact train/validation overlap, preserved chat
  turn newlines, and independently re-verified all eight remote cell hashes (150,761,977 bytes).
- Train bytes imply fixed proportional sampling probabilities: English general `0.3997366`,
  Korean general `0.4008607`, English dialogue `0.0300839`, Korean dialogue `0.1693188`.
- Local QA passed 33 tests plus 3 subtests with one CUDA-only skip. The tiny full Python flow
  passed 4/4 validation descent, recorded all 160 sampled windows, certified scorer controls,
  and rejected the untrained model as expected. Vast.ai RTX 4090 preflight passed 25 tests plus
  3 subtests, including CPU↔CuPy ByteGPT parity.
- Vast.ai instance `47504399` was a verified RTX 4090 24 GB at approximately `$0.3317/hour`.
  H100 was not used.

## Result

The fixed run completed 14,000 steps in 5,961.6 seconds with peak measured VRAM of 19,773 MiB.
The sampler ledger recorded every one of 448,000 selected windows and matched the preregistered
train-byte proportions: English general `0.39913`, Korean general `0.40148`, English dialogue
`0.02973`, and Korean dialogue `0.16965`. All four held-out cells descended. Macro validation CE
improved from the parent run's `1.49157` to `0.95471`; Korean dialogue improved from `2.29729` to
`0.74589`. This confirms that equal-cell overexposure caused the prior validation divergence.

It did not make the model conversational. The unchanged meaningful-conversation panel failed:

- English semantic relevance `2/7`; Korean `0/7`.
- Structural pass `0/14`; all final multi-turn answers failed.
- Manual deployment review `0/14` because every answer was repetitive, incomplete, irrelevant,
  byte-damaged, stale after correction, or a combination of these.
- English answers looped phrases such as “the concept of the concept”; Korean answers repeated the
  question or a short assertion and some ended in invalid UTF-8 bytes.
- The Korean correction prompt changed the favorite drink to tea, but the model kept repeating
  that it was coffee.

The first evaluation attempt exposed a shared evaluator bug: a damaged model byte was correctly
retained with `surrogateescape`, then the next-turn seed-length metric re-encoded it with strict
UTF-8 and crashed. The metric now uses the same lossless byte convention as the decoder and scorer.
A regression with invalid bytes carried across a multi-turn seed passes locally and on Vast.ai.
The unchanged checkpoint, panel, and decode then produced the complete 14-response failure record.

The final model, exact-resume checkpoint, sampler ledger, raw lossless responses, logs, GPU metrics,
protocol, panel, and data manifest are private at
`dancinlab/anima-303m-r0-proportional-conversation-seed7-2026-08-12@0c3b69323959247f05b45f2628e956fd4547b8ec`.
Ten registered artifacts were independently SHA-256 verified. Full evidence is in `result.json`.
The RTX 4090 instance was destroyed after HF preservation; active Vast.ai rentals are `0`, with an
estimated cost of `$0.73`.

The proportional sampler and turn framing fixes stay in the shared Python engine. The next work
must isolate why the fixed next-byte objective collapses into repetition before any R1 workspace
experiment. The panel, thresholds, seed, endpoint, and this failed checkpoint remain frozen.
