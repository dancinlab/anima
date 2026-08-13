# R4 complete-trajectory support admission — 2026-08-13

Status: **COMPLETE — INVALID-CONTROL-MISMATCH**.

## Why this axis comes next

The fixed-data capacity ladder showed stronger memorization without independent meaning, but its
shared admission helper was not neutral. The immutable source contains 8,635 canonical training
documents, including 1,194 multi-turn trajectories. The helper accepted only documents whose role
sequence was exactly `[user, assistant]` and whose final response fit the runtime's 192-byte output
budget. The resulting 3,500-document training view therefore contained **zero** multi-turn
trajectories. The trainer itself supports every canonical assistant span, so this was an admission
loss before the shared trainer rather than a ByteGPT or context-window limitation.

This makes the prior memory/correction failures uninterpretable as capacity evidence. It does not
invalidate the recorded `0/7` single-turn semantic result, and no past artifact or verdict is
rewritten.

## Exhausted design space

The following candidates were considered before choosing the smallest identifying experiment.

| Candidate | Decision now | Reason |
|---|---|---|
| Rerun 303M | reject | data support and compute scaling are still unresolved |
| Increase capacity beyond 30M | reject | fixed-exposure capacity already increased memorization and worsened held-out CE |
| Add more steps to the same 3,500 documents | reject | the 0.89M exposure ladder already reached a stable CE floor at semantic `0/7` |
| Select a post-hoc checkpoint | reject | violates fixed-endpoint evidence and cannot restore absent multi-turn support |
| Change greedy decode or add repetition penalties | reject | teacher-forced generalization is already poor; decode changes would mask it |
| Add unlikelihood or contrastive loss | defer | objective changes cannot identify the upstream admission loss |
| Increase context to 1,024/2,048 bytes | defer | V1 already showed coverage improvement without meaning; all current documents fit 513 bytes |
| Byte patching, BLT or MEGABYTE | defer | new architecture would mix efficiency with the missing-support cause |
| Retrieval or canned answer routing | reject | would bypass rather than train a native mouth |
| IIT candidate selection or latent prefix | defer | IIT must not select among meaningless mouth outputs |
| Add synthetic panel-shaped examples | reject | contamination and benchmark teaching |
| Add a new external conversation corpus | defer | provenance, license, dedup and data-quality effects would be a second axis |
| Expand the broad corpus view and compute | next if this fails | necessary, but it changes language-data/compute rather than dialogue admission |
| Admit all existing complete trajectories | **run** | directly restores support already present in the immutable HF source |

The interpretation follows
[`dancinlab/anima-research@03d55ef`](https://github.com/dancinlab/anima-research/commit/03d55ef9848df304a435a88a2b90a74722bc5b73):
language is a late expression path, missing support is not evidence about internal consciousness,
and a functional pass is never a phenomenal-consciousness claim.

## Frozen experiment

Only the dialogue admission policy changes. The exact 2.817M ByteGPT language checkpoint, broad
train/validation byte views, 120,000 broad replay rows, 120,000 dialogue rows, seed, batch,
optimizer, objective, schedule, 512-byte context, canonical generator, seven-response English
panel, thresholds and fixed final checkpoint remain unchanged.

All three nested arms run:

1. `CONTROL-3500`: exact prior 3,500 single-turn, final-response-≤192-byte view.
2. `SHORT-COMPLETE`: every complete trajectory whose final response is ≤192 bytes; 4,625 documents,
   including 1,010 multi-turn trajectories.
3. `ALL-COMPLETE`: all 8,635 immutable complete trajectories; 1,194 are multi-turn.

The final arm is the registered primary endpoint. A lower arm cannot be selected after observing
results. The same eight short control exchanges are used only as a training-wiring probe in all
arms; the unchanged independent conversation panel remains the behavioral gate. An automatic pass
still requires manual review before any scale-up.

The shared `core.generator` parser is the only runtime change: it parses the same complete
alternating trajectory that the existing renderer emits. The corpus builder, trainer, ByteGPT,
loss, evaluator and participant are not replaced.

## Stop rules

- A control mismatch makes the experiment invalid; treatment results are not interpreted.
- All three arms run regardless of intermediate results; no sweep, extra seed or threshold change.
- Primary automatic failure blocks 303M, IIT-mouth coupling, participant mounting and production.
- Primary automatic pass permits only manual review and a separately preregistered replication.
- Models, data and checkpoints remain private in HF `dancinlab`; result compute may use one
  non-H100 Vast.ai GPU and the protocol-owned instance must be destroyed.
- `ING.jsonl` and `stream_mi.json` remain untouched.

## Result

The registered three-arm run completed on a Vast.ai RTX 4090. The root flow finding was real:
the immutable source had 8,635 canonical documents and 1,194 multi-turn trajectories, while the
old exact-two-turn helper admitted 3,500 documents and zero multi-turn trajectories. The new
canonical parser now preserves complete alternating trajectories and round-trips the existing
renderer. This changes no past verdict; it only makes the support loss explicit.

The frozen control did not reproduce. Its broad CE was `1.60649` versus registered `1.60953`, its
held-out assistant CE was `2.27695` versus `2.25676`, and its structural result was `4/7` versus
the required prior `7/7`; semantic remained `0/7`. The absolute CE tolerance was `0.00001`, so the
registered fail-closed verdict is `INVALID-CONTROL-MISMATCH` and neither treatment arm is interpreted
as causal evidence.

For raw evidence only, `SHORT-COMPLETE` reached held-out assistant CE `1.96128`, semantic `0/7`,
structural `4/7`, and failed memory/correction. Primary `ALL-COMPLETE` reached held-out assistant CE
`1.34827` and top-1 `0.62771`, but semantic `0/7`, structural `0/7`, and failed memory/correction.
Its outputs retained meaningless loops around consciousness/construction, ice crystals, the blue
box, and favorite colors. Diagnostic review was therefore meaningful `0/7`. Restoring the existing
support was insufficient to form a conversational mouth, even though the teacher-forced metric
improved; the control mismatch prevents attributing that improvement to admission alone.

The first evaluation attempt found the remote CuPy dependency absent after control training had
completed. It was stopped before producing a result. A fail-closed resume path now reuses a
completed arm only when checkpoint/state/log/summary are all present and parameter count, completed
step, dialogue rows, document count, training bytes, and both validation descents match the active
protocol. CUDA decode was then enabled for every recorded arm; no extra training trajectory was
created.

Local preregistration QA passed `95 tests + 3 subtests`; the resume change passed `27/27` locally
and remotely. Vast.ai passed `97 tests, 1 expected skip, 3 subtests` before the run and `74/74`
focused tests afterward; final local regression passed `73` tests with one expected CUDA skip.
Raw models, exact-resume states, responses, logs, protocol, QA and power
telemetry are held only in private HF revision
`dancinlab/anima-303m-r4-support-admission-2026-08-13@7e750e4e1b0d2e08a501df8857bbbf576d5d9188`.
An independent snapshot verified all 36 manifest entries (`142,697,226` bytes) with zero size or
SHA-256 mismatches.

The final run used approximately `410,580 J`, peaked at `1,919 MiB` and `121.23 W`; the interrupted
evaluation run used approximately `164,671 J`. Estimated total rental cost is about `$0.83`.
Both protocol-owned instances were destroyed and an unrelated H100 was preserved. No model was
mounted; 303M, IIT-mouth coupling, participant and production remain blocked. The next result-bearing
work must first explain the frozen control trajectory mismatch byte-for-byte.
