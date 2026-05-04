# P9 Path A r=16 Retrain — Launched (Landed)

**Date**: 2026-05-04
**Trigger**: Subagent ad04404c hit quota/conflict on first attempt; retry launched on a fresh distinct pod.

## Substrate
- **Pod**: `pvkyhb0lb87ydu` (anima-p9-pathA-r16-h100-sxm-secure)
- **GPU**: 1x NVIDIA H100 80GB HBM3 (driver 580.126.09)
- **Cloud**: SECURE
- **Rate**: $2.99/hr (verified ≤ $3.00 cap)
- **Pre-existing pod `fuewrx9moxe6gz` (D 25K)**: UNTOUCHED ✓

## Config (vs prior r=64 run)
| Knob | Prior r=64 | This r=16 |
|------|-----------|-----------|
| lora_r | 64 | **16** |
| lora_alpha | 64 | **16** |
| target_modules | 7 (qkvo + gate/up/down) | 7 (same) |
| trainable params | ~97M (3.0%) | **24.3M (0.7511%)** |
| max_steps | 10000 | 10000 |
| save_steps | 2000 | 2000 |
| LR | 1e-4 | 1e-4 |
| batch × grad_acc | 4 × 8 | 4 × 8 |
| seq_len | 2048 | 2048 |
| bf16 + grad_ckpt | yes | yes |

## Corpus
- `state/p9_p0_measure_2026_05_03/sft_data_full_50k_augmented.jsonl` → re-templated to Llama-3.2 chat
- 50,000 records, 50,000 emitted (0 skipped)
- Pod path: `/workspace/sft_data_llama_template.jsonl` (69 MB)

## HF Push Target
`need-singularity/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1`

(mk2-conformant via paradigm-A' amendment validator landed earlier today; "every_save" hub_strategy = 5 ckpts at steps 2000/4000/6000/8000/10000+final)

## Initial Loss Series (steps 10–70)
| Step | Loss | LR | Token Acc | Epoch |
|------|------|----|-----------|-------|
| 10 | 3.068 | 4.5e-6 | 0.502 | 0.006 |
| 20 | 3.372 | 9.5e-6 | 0.471 | 0.013 |
| 30 | 3.191 | 1.45e-5 | 0.485 | 0.019 |
| 40 | 3.072 | 1.95e-5 | 0.492 | 0.026 |
| 50 | 2.796 | 2.45e-5 | 0.524 | 0.032 |
| 60 | 2.523 | 2.95e-5 | 0.553 | 0.038 |
| 70 | 2.409 | 3.45e-5 | 0.569 | 0.045 |

**Healthy descent**: loss 3.07→2.41 over 60 steps; token accuracy 50%→57%.

## ETA & Cost
- Observed step rate: **2.55s/it** (avg over first 80 steps)
- Projected total: **7.95 hr** for 10K steps
- Projected spend: **$23.77** (within $27 watchdog, within $30 hard cap)
- Prior r=64 ran ~7.5h, so r=16 has comparable wall-clock

## Watchdog & Terminator
- **Process**: PID 47336 (host-side bash, polls every 10 min)
- **Soft kill**: $27 (= 9.03 hr) — terminates pod, downloads partial artifacts
- **Hard cap**: $30 (= 10.03 hr) — RunPod-side budget alarm
- **First probe**: `spend=$0.00 STEP=71/10000 ALIVE=1` ✓
- **Log**: `state/p9_path_a_r16_2026_05_03/host_terminator.log`

## TRAIN_DONE Race Mitigation
Per spec, `TRAIN_DONE.json` is written **immediately after `trainer.train()` returns** (`phase=trainer_train_returned`), then again after `trainer.save_model() + tok.save_pretrained()` (`phase=final_saved`). The terminator only acts on `PHASE=final_saved`, eliminating the false-error window during final save + HF push.

## On Completion (Auto)
1. Terminator detects `PHASE=final_saved` (poll every 10 min)
2. SCPs `train.log`, `config.json`, `TRAIN_DONE.json`, `final/` adapter to `state/p9_path_a_r16_2026_05_03/artifacts/`
3. `runpodctl pod stop` + `runpodctl pod remove` on `pvkyhb0lb87ydu`
4. HF mirror `need-singularity/llm-llama32-3b-paradigm-a-prime-r16-sft-stage1` is canonical (5 ckpts + final)

## Next Cycle (φ★ Verify)
After completion:
- F1 sweep on the 5 ckpts vs. Llama-3.2-3B-Instruct base (target: F1 ≥ 0.16, matches/exceeds Llama-self anchor)
- Compare to r=64 prior run (in HF as `need-singularity/p9-llama32-lora-stage1`) — verify rank reduction did not collapse capacity

## Files
- `state/p9_path_a_r16_2026_05_03/verdict.json` — full status snapshot
- `state/p9_path_a_r16_2026_05_03/train_llama_lora_r16.py` — training script (r=16 variant)
- `state/p9_path_a_r16_2026_05_03/launch_r16.txt` — pod-side launch wrapper (renamed to .sh on pod)
- `state/p9_path_a_r16_2026_05_03/host_terminator_v2.txt` — watchdog (renamed to .sh in /tmp)
- `state/p9_path_a_r16_2026_05_03/sft_data_llama_template.jsonl` — Llama-templated corpus (50K)
- `state/p9_path_a_r16_2026_05_03/host_terminator.log` — live watchdog log
- `state/p9_path_a_r16_2026_05_03/artifacts/` — destination for downloaded artifacts (post-completion)
- `state/markers/p9_path_a_r16_launched.marker` — launch marker

## SSH Access (manual probe, if needed)
`ssh -i /Users/ghost/.runpod/ssh/RunPod-Key-Go -p 15961 root@103.207.149.143`
