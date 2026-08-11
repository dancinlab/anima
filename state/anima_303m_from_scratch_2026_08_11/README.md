# Anima-native 303M from-scratch rebuild — 2026-08-11

Status: COMPLETE — FALSIFIED AT THE STAGE-A G0 GATE.

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

- provider: Vast.ai H100 PCIe. The registered instance `47431163` was already absent when execution
  began, so the same GPU class was rented as execution instance `47440997`; heavy work did not run
  on mini;
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
6. After all recording and push work, instance `47440997` is deleted and the Vast.ai API must report
   zero active rentals. `anima_alive=false` after teardown is the expected final live state.

`ING.jsonl` and `stream_mi.json` are existing user files and remain untouched.

## Result

Stage A ran exactly as registered from random initialization on a Vast.ai H100 PCIe. The 303.098M
model completed 6,000 updates in `1,425.9 s`; train CE moved from `543.36487` to `1.59991`, and the
final held-out CE was `1.63467` versus the uniform `5.5452` baseline (`DESCENT`, 1/1 register).
Peak observed training VRAM was `19,947 MiB`.

The serialized engine was a valid ByteGPT mouth and the adjacent checkpoint retained
`anima-train-resume/v1`, optimizer, RNG, sampler state, and completed step 6,000. Its state digest is
`715c4b1b2357b2e0e0dbe75f05f36d02d7d47cb4c8ab82f706c6ee3628962506`. The final engine SHA-256 is
`db49408438aa66fd534d68ea3668f240d193df7dbaacd7fd9e3b5fdb72eff69d`; the exact-resume SHA-256 is
`f79baa77bc2831260bf6320992bcb183f26a87c9723b5294877a349662cbce4e`.

The frozen engine-native Stage-A gate then measured HILLOCK `LIVE` (`rep=0.0`, `distinct2=0.975`)
but rho-form only `0.60 = 3/5`, below the unchanged `0.70 = 4/5` gate. The self-shuffle control was
`0.0`, so this is a clean capability failure rather than detector leakage. Per the registered stop
rule, Stage B, chat gates, participant staging, HTTP/WebSocket conversation QA, and runtime
deployment were not run or interpreted. The final verdict is `FALSIFIED`.

Two shared trainer defects were repaired during the preflight smoke: an existing `core/` entry in
`PYTHONPATH` no longer lets the script directory shadow `core/serialize.py`, and ByteGPT conversion
now uses temporary bridge files instead of overwriting the exact-resume `<out>.pt`. H100 regression
finished `12/12`; the 303M smoke and five intermediate serialize/resume boundaries also passed.
The failed model, final exact-resume state, 1,000-step engine checkpoints, logs, hashes, and gate
outputs are preserved in the private HF repository
`dancinlab/anima-303m-from-scratch-2026-08-11`.
