# R4 mouth D0–D6 diagnostics — 2026-08-13

Status: **COMPLETED — DIAGNOSED-TEACHER-FORCED-UNDERLEARNING**.

The assistant-turn boundary repair fixed exact stopping on one document but the same existing
ByteGPT collapsed into `the/an/toure/ion` loops on 100 documents. That observation does not yet
distinguish serialization, insufficient teacher-forced learning, missing prompt conditioning, or
autoregressive rollout failure. This protocol freezes the next bounded Python-only diagnosis before
downloading the preserved private artifacts or starting new training.

The experiment reuses the immutable 100-document data view, the actual failed `.pt/.bin` pair, the
existing trainer, serializer, NumPy decoder, canonical generator and scorer. D0 compares Torch,
serialized engine, resident-KV, full-forward and ranged canonical paths. D1 traces gold-prefix byte
probabilities and the first free-generation divergence. D2 trains a fixed 1/4/16/32/64/100-document
memorization ladder. D3 compares full, additive and assistant-turn-only CE at 100 documents. D4
ablates or shuffles prompts, D5 replays all 32 fixed validation documents, and D6 records the
100/200/300/400/500/600-step trajectory without permitting post-hoc checkpoint promotion.

At most eight local training arms may run. Seed, order, endpoint, learning rate, optimizer, decoder,
bars and data revision cannot be changed after observing results. D0 failure blocks interpretation
until the shared serializer/decode path is repaired. No outcome authorizes a 303M run, IIT-mouth
coupling, participant mount or production deployment; a later change requires a separate protocol.
Models and training data remain private under HF `dancinlab`. `ING.jsonl` and `stream_mi.json` must
remain untouched. Exact conditions and the decision table are in `protocol.json`.

## Result

D0 passed on the actual preserved 100-document failure. The `.pt` and `.bin` tensors were exactly
equal, maximum Torch-versus-engine logit error was `0.00000615`, every argmax agreed, and resident
KV, full-forward and ranged canonical generation emitted identical bytes. The repeated output is
therefore not explained by serialization or decoder divergence.

D1 located the failure before free rollout. Across the eight frozen training probes, gold-prefix
teacher forcing scored CE `2.41848`, top-1 byte accuracy `0.27712`, mean gold probability `0.15405`
and mean gold rank `5.48`. Canonical free generation recovered `0/8` target prefixes and passed
`0/8` structural checks. Rebuilding the same registered 100-document arm reproduced those values,
so the preserved failure and the new local trajectory agree.

The D2 memorization ladder identified the first break between one and four unique documents:

| Unique documents | Teacher top-1 | Target prefix | Structural | Maximum repeated-word run |
| ---: | ---: | ---: | ---: | ---: |
| 1 | `1.0000` | `1/1` | `1/1` | `1` |
| 4 | `0.6978` | `2/4` | `1/4` | `3` |
| 16 | `0.5602` | `1/8` | `1/8` | `18` |
| 32 | `0.4621` | `1/8` | `1/8` | `30` |
| 64 | `0.3484` | `0/8` | `0/8` | `28` |
| 100 | `0.2771` | `0/8` | `0/8` | `63` |

D3 did not support the proposed full-CE-first curriculum at the frozen 600-step endpoint. At 100
documents, teacher-forced top-1 was `0.2689` for full CE, `0.2883` for additive CE and `0.2771` for
assistant-turn-only CE; all three recovered `0/8` target prefixes and passed `0/8` structural
checks. D4 shows that turn-only is not wholly prompt-blind: normal prompt CE beat both blank and
cyclic-shuffle controls on `6/8`, and all eight outputs changed under at least one intervention.
Full and additive controls scored `5/8` and `4/8`, below the frozen prompt-causality bar.

D5 removed the random four-batch validation noise. On all 32 fixed held-out documents, assistant
turn CE/top-1 were `2.86936/0.22694` for turn-only, `2.82570/0.23976` for full and
`2.86013/0.23976` for additive. This is memorization without meaningful held-out generalization.
D6 also rules out a late collapse: turn-only teacher CE improved gradually from `2.66112` at step
100 to `2.41848` at step 600, while target recovery and structural generation stayed `0/8` at every
checkpoint and repeated-word runs were already present at step 100. No historical checkpoint is
promoted.

The root classification is therefore teacher-forced underlearning under this tiny fixed-budget
recipe, with partial prompt conditioning but no learned conditional response distribution. It is
not a decoder bug and the matched 600-step evidence does not establish full CE as the remedy. The
next admissible experiment is a separately preregistered single-axis optimization/capacity test at
the four-document break point; 303M training, IIT-mouth coupling, participant mounting and
production remain blocked.

All eight registered training arms ran locally on Apple MPS with two CPU threads in `308.9s` total
trainer wall time. The interrupted reporting pass did not duplicate them: exact completed-step and
recipe checks reused all eight checkpoints before D5/D6 resumed. No Vast.ai/H100 instance or HF
source repository was changed during measurement. The 42 model/evidence artifacts totaling
`146,667,478` bytes were then preserved in private HF
`dancinlab/anima-303m-r4-mouth-diagnostics-2026-08-13@8d67bb6e5eeea9a917892fba39310b7306c84718`;
every re-downloaded size and SHA-256 matched manifest
`1a262046aaaafcedf1169d07a67649f2f6b58a232d2d2a4de732ec45bccacaca`.
The Vast.ai API showed one pre-existing RTX 5090 instance, id `47562136`, label
`anima-native-screen-20260813`; this local diagnostic did not create, use or modify it, so it was
left running rather than deleting another workload.

Focused diagnostics QA passed `31 tests + 3 subtests` with one expected unavailable CUDA/CuPy
skip. Full Python/CHAT QA passed `160 tests + 3 subtests` with the same single skip. Compile, CLI
help, protocol/result JSON and diff checks also passed. Runtime serving code was not changed and no
failed mouth was mounted.
