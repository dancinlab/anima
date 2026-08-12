# R4 mouth D0–D6 diagnostics — 2026-08-13

Status: **PREREGISTERED — NOT YET EXECUTED**.

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
