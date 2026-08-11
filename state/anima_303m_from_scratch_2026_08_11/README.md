# Anima-native 303M from-scratch rebuild — 2026-08-11

Status: REGISTERED BEFORE EXECUTION.

Live inspection falsified the intended model identity of the current H100 deployment. The running
participant uses `--substrate lora`, `ANIMA_BASE=/workspace/qwen7b`, and no adapters. The recovered
broker/FIFO/motivation flow is valid, but its language generator is a base-only Qwen artifact, not
an anima-native byte mouth. The compose-2 7B checkpoint remains valid only for its frozen synthetic
store-causality experiment and must not be promoted as a conversational model.

This rebuild starts at the frozen 303M reference scale required by `CONDITIONS.md`. It adds no
trainer, model architecture, evaluator, prompt, or threshold. Training uses the existing canonical
`cli/train.py --arch bytegpt`; serialization and inference use `core/serialize.py` and
`core/decode.py`; a passing mouth reaches chat only through the existing participant and broker.

## Frozen custody and protocol

- provider: Vast.ai, existing H100 PCIe instance `47431163`; heavy work does not run on mini;
- all model and training-data custody: Hugging Face organization `dancinlab` only;
- Stage-A data: `dancinlab/anima-corpus-en-general`, commit
  `e1c4ef4f595d72b959d0aa73a5cc5c8ba2a065a0`, file SHA-256
  `6614094432707127c82d6ee1ffd3a65f27c5aa118498be1623f1394f182f8ef9`;
- Stage-B data: `dancinlab/anima-chat-corpus-mix-70wiki-30dialogue`, commit
  `32e16ed21ab6b86c22b2993a9a2c3de7a96638a7`, file SHA-256
  `05179fb6684d41e4cefa928fe1c24683294c17997666eed5c03a00480e5acb70`;
- architecture: ByteGPT V256, d1024, 24 layers, 16 heads, block 512; seed 7;
- Stage A: random initialization, CE marginal, 6,000 updates, global batch 32, bf16, lr `3e-4`,
  proportional sampling, held-out tail 5%, checkpoint every 1,000 updates;
- Stage B: allowed only after Stage A passes G0 (`known-word-ratio >=0.50` on at least 4/5),
  warm-start only from the Stage-A checkpoint, 2,000 updates, global batch 16, bf16, lr `8e-5`,
  checkpoint every 1,000 updates;
- no result-dependent seed, data, update count, prompt, evaluator, or bar changes; a failed gate is
  recorded and stops the dependent stage.

The Stage-B lineage is still from scratch: no prior model weights or external base model enter it;
its only parent is the random-initialized Stage-A model trained in this run.

## Frozen gates and deployment order

1. Python regression and exact-resume regression pass on the H100.
2. The serialized Stage-A ByteGPT is engine-decodable and passes G0. A G0 failure stops the run.
3. Stage B passes engine-native rho-form/G0 and the existing chat gate: single-turn at least 4/5 and
   multi-turn deep-context at least 3/5. G1/G2 and remaining frozen reach rows are reported honestly;
   no failing row is hidden by the chat result.
4. Only a Stage-B pass unlocks participant staging, exact `reply_to` multi-user QA, Korean/English
   semantic conversation, HTTP/WebSocket, VRAM, process recovery, and a non-injecting soak.
5. Results, hashes, HF revision, cost, and failures are written here and to `result.json`, committed,
   and pushed to `origin/main`.
6. After all recording and push work, instance `47431163` is deleted and the Vast.ai API must report
   zero active rentals. `anima_alive=false` after teardown is the expected final live state.

`ING.jsonl` and `stream_mi.json` are existing user files and remain untouched.
