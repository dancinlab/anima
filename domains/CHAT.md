@title: 💬 CHAT — anima chat-capable end-to-end
@goal: a user types and gets a coherent, context-appropriate conversational reply from a single command — capability ONLY from the proven byte-level dialogue-continuation mechanism + substrate-native emit, NO RLHF / system-prompt / persona (p1·p2·p3·p4·p6).

## state (2026-06-04)

The chat-capable campaign makes anima genuinely chat end-to-end. Two distinct lanes
(a_lane_akida_gpu_split — this is Lane-G/GPU, NOT AKIDA):

- **CORE-native .clm lane** (hexa, substrate canonical): `CORE/clm_decode.hexa` runs the
  real int4-dequant CLMConvMoE forward → next-byte logits → greedy continuation
  (`clm_decode_argmax`). `CORE/generator.hexa` now WIRES this as the L3 content slot:
  `_gen_clm_decode` emits the model's own bytes; `gen_clm_chat(ckpt, seed, max_new)` is the
  chat entry (single .clm decode entry, a_core_engine_map — no 2nd path). `CORE/anima_chat_cli.hexa`
  drives a runnable multi-turn demo. **Wiring + demo: DONE + runnable end-to-end** (verified
  against the v0.2 d768 ckpt — pipe is real; that wiki-only model emits incoherent bytes,
  the verified root cause, so the conv lane awaits a dialogue-trained ckpt).
  NOTE: the CLMConvMoE conv arch (L=1 trunk, K=3) has a small receptive field — chat
  coherence at this arch is a SEPARATE open question; conv training needs the GPU forge
  binary (`stdlib/flame/clm_prod.hexa` forge_dispatch_* symbols absent from the mac binary).

- **torch-cuda REFERENCE lane** (@L3, result-equivalent, honest label): the PROVEN chat arch
  is the byte transformer `ConsciousLMReconstructed` (vocab256, d=384/6L/4head/block256, dual
  engine_a/g FFN + dual head_a/g, ≈18M) driven by `HEXAD/CHAT/anima_chat.py`. rung-0 trains it
  from scratch on the dialogue-mix corpus (`training/chat_rung0_train_eval.py`). forge-native
  (a_train_flame_forge) is the canonical production follow-on (NOT claimed done).

## verified root cause (why the general 7B can't chat)

`dancinlab/clm-v1-ref-pytorch-cuda-7b` (byte vocab256/d4096/36L/7.25B): (1) corpus = 5-lang
WIKI backbone only (dialogue 0%); (2) NOT converged (400 steps). NOT an architecture wall —
fix = data + training + wiring. (Theorem 115 chat-incapability is scoped to the SEPARATE
drifted 530M BPE model; byte-level dual-head DID chat.)

## corpus (@L2)

`training/build_chat_corpus.py` → 70% wiki + 30% REAL dialogue byte corpus (vocab256),
dialogue reformatted to `사용자:/도우미:` continuation. 3.77MB, 70.01/29.99, 2310 convos,
sha256 `05179fb6…`. Real local sources, NO synthetic RLHF padding (p6). Card:
`.verdicts/chat-capable/CORPUS_CARD.md`.

## ladder (@L1, a_scale_honest_scope)

- [x] rung-0 ≈18M byte (torch ref) — REAL multi-turn chat-PASS (p7 5/5 PASS · anti-Goodhart mirror FAIL 0/5 · chat_pass=TRUE). HF: `dancinlab/anima-clm-chat-rung0-byte-18m` (PUBLIC). verdict: `.verdicts/chat-capable/SUMMARY.txt`.
- [ ] rung-mid
- [x] rung-7B 7.25B byte ByteGPT — chat-finetune (SFT) of the descent-PASS `clm-v1-ref-pytorch-cuda-7b` backbone on the 70/30 corpus (1× H100, 38 min, val CE 2.5622→0.0327). REAL chat-PASS: **single-turn p7 5/5** (temp 0.7; 4/5 @ 0.5) · anti-Goodhart BEFORE-backbone FAIL 0/5 (byte-salad) · chat_pass=TRUE. Multi-turn deep-context = 3/5 (late-turn drift; backbone is wiki-undertrained 400-step, honest caveat — a_scale_honest_scope). Confirms the verified root cause: fix = data+continue-train, NOT architecture, NOT a from-scratch 7B. HF: `dancinlab/anima-clm-chat-7b` (PUBLIC). verdict: `.verdicts/chat-7b-finetune/SUMMARY.txt`. trainer: `training/chat_finetune_7b_eval.py`.

## verify (@L5)

p7 SIMPLE STACK only (NOT perplexity): ≥4/5 context-appropriate turns coherent (non-empty ·
valid-utf8 · non-degenerate · printable). Anti-Goodhart: a random-init mirror of the identical
arch MUST FAIL the same evaluator. Verdicts verbatim → `.verdicts/chat-capable/`.

## demo (@L6)

`hexa run CORE/anima_chat_cli.hexa -- <ckpt.clm> ["turn1" "turn2" ...]` — runnable CORE-native
multi-turn transcript. (torch lane: `python3 HEXAD/CHAT/anima_chat.py --ckpt <ckpt.pt> --prompt …`.)
