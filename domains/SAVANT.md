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

## fire state (LAUNCHED 2026-06-04 — leak-safe single pod)

- **pod** = vast `39416669` (the ONE and ONLY SAVANT pod; single rent, NO re-rent
  policy per hexa-lang #2686 no-autorent — a rent FAIL would have STOPPED + reported,
  no escalation/rotation/durable-re-fire). H100 SXM 80GB (81559 MiB), 120 GB disk,
  image `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel`, ~$2.40/hr.
- **ssh** = `ssh -i ~/.vast/ssh/vast-key -p 19690 root@80.188.223.202`
  (direct endpoint; proxy `ssh8.vast.ai:16668` also exists). Key =
  registered `anima-orchestrator-2026-04-28` ed25519.
- **persistent /workspace** = all artifacts under `/workspace/savant/` (survives
  reboot): scripts, `corpus_rung0.txt`, `corpus_5lang.txt`, `rung0/`, `rung7b/`.
- **onramp** = `/workspace/savant/pod_onramp.sh` launched DETACHED
  (`setsid nohup`, survives the orchestrator's death). Sequence on the ONE pod:
  (1) deps → (2) rung0 corpus (4 MB/lang) → (3) rung0 train (d512/8L, 120 steps)
  → (4) IF rung0 descends: 7B corpus (80 MB/lang ~400 MB) → (5) 7B durable nohup.
  State machine writes `/workspace/savant/ONRAMP_STATE`
  (`RUNG0_PASS` / `FAILED_RUNG0` / `7B_LAUNCHED pid=...`). FAIL-LOUD: rung0
  no-descent aborts the 7B (recipe/corpus problem surfaces, no silent 7B burn).
- **7B rung** = d4096/36L/32H/block512 = 7.25B, bf16 + grad-ckpt + AdamW8bit,
  batch 8 × grad_accum 4, 6000 steps, `--ckpt-every 200` →
  `/workspace/savant/rung7b/ckpt_step_*.pt` (durable, `--resume`-able). Detached
  nohup pid in `/workspace/savant/rung7b/train_7b.pid`, stdout
  `/workspace/savant/rung7b/train_7b.out`, result JSON
  `/workspace/savant/rung7b/savant_5lang_7b_train.log.json`.

## harvest plan (NOT babysat — harvested later by pod-id)

1. `ssh ... 'cat /workspace/savant/ONRAMP_STATE'` — confirm `7B_LAUNCHED`.
2. `ssh ... 'tail -40 /workspace/savant/rung7b/train_7b.out'` — descent curve.
3. when `savant_5lang_7b_train.log.json` shows a competent CE (descent PASS):
   `scp` the latest `rung7b/ckpt_step_*.pt` + `savant_5lang_7b.pt` + result JSON
   + `corpus_card.txt` to `state/savant_torch_recover/`.
4. HF upload: ckpts PRIVATE during training; promote to PUBLIC only on a
   competent closure-PASS 7B (a_hf_autonomous). Add HF.jsonl rows (rung0 ckpt,
   7B ckpt, 5-lang corpus dataset).
5. teardown ONLY after artifacts pulled + verified + HF uploaded
   (a_fire_recover_complete): `vastai destroy instance 39416669`.

**ETA**: rung0 ~2-4 min after deps (~5 min). 7B at ~400 MB corpus, 6000 steps,
batch 8×4 grad-accum, block 512 on one H100 ≈ multi-hour → ~1 day to a competent
CE (a_scale_honest_scope: bounded-step REFERENCE rung, NOT a convergence claim).

## verdicts

- `.verdicts/savant-torch/` — rung0 descent + 7B launch-state verdicts (verbatim).

## 양방향 sibling

- ⇄ [SAVANT-7B](./SAVANT-7B.md): the **forge-native** SAVANT 5-lang 7B lane
  (concurrent agent, pod vast 39404862). Same RESULT goal, distinct stack/runtime
  (a_lane_akida_gpu_split — recorded separately). This file = the torch-cuda lane.
- ⇄ HF.jsonl: `clm-v1-ref-pytorch-cuda{,-3b,-7b}` ref ladder (the proven recipe
  source) + the SAVANT torch-cuda ckpt rows.
