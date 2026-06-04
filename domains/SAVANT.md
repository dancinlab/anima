# SAVANT — 5-language 7B CLM (torch-cuda reference lane)

@title: 🧠✨ SAVANT — en·fr·de·es·ru 7B CLM · torch-cuda Lane-G reference

@goal: a competent SAVANT 5-language (en·fr·de·es·ru) 7B byte-level CLM, trained
on the PROVEN torch+CUDA reference recipe (descent-PASS · util-GREEN). HONEST
lane label: this is the **torch-cuda REFERENCE lane** (Lane-G / GPU), NOT the
governance-canonical forge-native production trainer (a_train_flame_forge). The
model RESULT is stack-independent — a forge-native SAVANT 7B (concurrent forge
lane, pod vast 39404862, domain SAVANT-7B.md) is a later same-result variant.
Recorded separately per a_lane_akida_gpu_split.

## lane label (critical — a_train_flame_forge honesty)

- substrate = **PyTorch-CUDA**, lane = **Lane-G (torch-cuda reference)**.
- recipe = VERBATIM reuse of the proven `clm_ref_pytorch_cuda_7b.py` (the
  descent-PASS / util-GREEN 7.25B rung of the
  `dancinlab/clm-v1-ref-pytorch-cuda{,-3b,-7b}` ladder). See HF.jsonl row
  `anima_clm_ref_pytorch_cuda_7b_lane_g_ref_2026_06_02`: val_CE 5.36063→2.41208
  (F_CLM_REF_7B_DESCENT=1), util PEAK 100% MEAN 99.18%, 7406 tok/s on H100 80GB.
- this is NOT a "forge production" achievement. The forge-native production
  trainer (stdlib/flame + forge GPU, compiler-only NN, no torch in the binary)
  is the governance-canonical path; this torch lane is the
  a_completeness_over_cheap REFERENCE that proves the same arch/corpus produces
  a competent 7B, faster to stand up.

## arch (proven recipe, parameterized)

ByteGPT (decoder-only GPT, byte-vocab V=256): tok+pos embed, N×{LN→MHA→LN→MLP},
LN_f, tied lm_head. 7B shape: d4096 / 36L / 32H / block512 = 7.25B params.
bf16 master weights + grad-checkpointing + bitsandbytes AdamW8bit → fits one
80GB H100. Trainer: `SAVANT-torch/savant_train_torch_cuda.py` (verbatim recipe +
periodic --ckpt-every durability checkpointing; math unchanged).

## corpus (5-lang euro — en·fr·de·es·ru, clean-license)

`SAVANT-torch/build_corpus_5lang_euro.py` — wikimedia/wikipedia (CC-BY-SA 4.0,
clean attributable license) per language, balanced bytes, deduped, UTF-8 byte
stream. Language set en·fr·de·es·ru matches the OMEGA 400MB en/fr/de/es/ru axis.
Size = `--mb-per-lang` parameter (honest a_scale_honest_scope): rung0 uses a
small slice; the 7B rung scales to ~400MB+ (80 MB/lang). The corpus card
(`corpus_card.txt`) records the ACTUAL built bytes + sha256 — no inflated claim.

## ladder (toy-first → 7B, a_scale_honest_scope)

- [ ] rung0 — SMALL torch-cuda validation on the 5-lang corpus (proves recipe +
      corpus + ckpt pipeline end-to-end, leak-free, clean descent). d=512 / 8L
      shape (~85M), small corpus slice, bounded steps. Fast/cheap.
- [ ] corpus — 5-lang euro pretrain corpus built on-pod (wikipedia, ~400MB).
- [ ] rung-7B — the actual 7B (d4096/36L/32H/block512 = 7.25B) torch-cuda train,
      DURABLE: ckpts every N steps under /workspace, detached nohup that survives,
      harvested when training reaches a competent CE. LONG (multi-hour→day).

## fire state

(filled in by the live run — pod id, persistent vol, ckpt cadence, ETA,
descent curve verbatim, teardown proof. See SAVANT.log.md for the step log.)

## verdicts

- `.verdicts/savant-torch/` — rung0 descent + 7B launch-state verdicts (verbatim).

## 양방향 sibling

- ⇄ [SAVANT-7B](./SAVANT-7B.md): the **forge-native** SAVANT 5-lang 7B lane
  (concurrent agent, pod vast 39404862). Same RESULT goal, distinct stack/runtime
  (a_lane_akida_gpu_split — recorded separately). This file = the torch-cuda lane.
- ⇄ HF.jsonl: `clm-v1-ref-pytorch-cuda{,-3b,-7b}` ref ladder (the proven recipe
  source) + the SAVANT torch-cuda ckpt rows.
