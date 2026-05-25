# VLM Stage 1 Training Launched on ubu1 (2026-05-04)

> **TL;DR**: VLM stage1 LoRA training is now running detached on ubu1 RTX 5070 (PID 31960). atp_pytorch.AudioTokenPredictor (35.94M base, 0.0799M LoRA r=8) is consuming LibriSpeech-clean train.100 transcripts via Mistral SP-32k tokenizer. **Initial signal at step 1000: loss 10.5602 (random init) → 9.1830 (Δ −1.39 nats, ≈4× perplexity reduction). Steady throughput 2.43 sps → ETA 5.6h to 50K steps.** This stage trains TEXT-CE only because no audio codec (Encodec/Mimi) is installed; full 0.5*audio_CE + 0.5*text_CE deferred to stage2.

---

## 1. What Landed

| Artifact | Path |
|---|---|
| Training wrapper | `tool/transient_py/vlm_stage1_train.py` (332 LoC, NEW) |
| Verdict | `state/vlm_stage1_2026_05_04/verdict.json` |
| Train log (snapshot) | `state/vlm_stage1_2026_05_04/train.log` |
| F1 stub | `state/vlm_stage1_2026_05_04/F1_audio_pred.json` |
| Marker | `state/markers/vlm_stage1_ubu1_train_launched.marker` |
| This handoff | `docs/vlm_stage1_ubu1_train_launched_2026_05_04.ai.md` |
| ubu1 wrapper | `/tmp/vlm_stage1_train.py` (scp from mac) |
| ubu1 ATP port | `/tmp/atp_pytorch.py` (scp from mac, 29137 bytes) |
| ubu1 savepoints | `/tmp/vlm_stage1_savepoints/` (created, populated every 5K steps) |
| ubu1 logs | `/tmp/vlm_stage1_logs/{train.log, nohup.out}` |

---

## 2. Predecessor Resolution

Prior cycle `vlm_stage1_2026_05_03` ABORTED with 4 gates FAIL. Today's status:

| Gate | Status | Resolution |
|---|---|---|
| atp_pytorch.py exists | ✅ RESOLVED | Sister BG `a1819ebac` landed `tool/transient_py/atp_pytorch.py` (645 LoC, F-VLM-TRANSPILE-1 PASS) |
| ubu1 base loadable | ✅ RESOLVED | scp atp_pytorch.py → /tmp/; loads 35.94M params on RTX 5070 in <2s |
| LibriSpeech corpus | ✅ RESOLVED | HF datasets streaming (no full ~6GB download required) |
| LoRA wrapper | ✅ RESOLVED | peft.LoraConfig r=8 on `wq, wk, wv, wo, intent_proj` → 0.0799M trainable (0.222%) |
| Sentinel script | ⚠️ DEFERRED | text_CE log every 50 steps + savepoints every 5K (no separate sentinel script — log-driven) |

---

## 3. Substrate (ubu1 RTX 5070 12GB)

```
host         | ubu1
venv         | /home/aiden/venv_orchestrator/bin/python
torch        | 2.11.0+cu128 (sm_120 compatible)
gpu_total    | 12227 MiB
gpu_free     | 12150 MiB at launch
gpu_used     | 819 MiB steady (6.7%, ample head-room)
gpu_util     | 0-72% oscillating (data-bound, not compute-bound)
disk_free    | 585 GB
deps_added   | soundfile==0.13.1, librosa==0.11.0, torchcodec==0.11.1+cpu
running_bg   | 3 tail-only processes (eval_llama × 2, p9_p1_6_sentinel) — no GPU contention
```

---

## 4. Training Configuration

```
model            | atp_pytorch.AudioTokenPredictor (text_vocab_size=32768)
base params      | 35.94M
LoRA r           | 8
LoRA alpha       | 16
LoRA dropout     | 0.05
LoRA targets     | wq, wk, wv, wo, intent_proj
trainable params | 79.9K (0.222% of base)
tokenizer        | mistralai/Mistral-7B-Instruct-v0.3 (SP-32768)
corpus           | openslr/librispeech_asr config=clean split=train.100 (HF streaming)
batch_size       | 4
grad_accum       | 4 → effective batch 16
seq_len          | 128 (mean LibriSpeech BPE ~70 + headroom)
lr_peak          | 5e-4
warmup_steps     | 500
total_steps      | 50,000
save_every       | 5,000 steps
log_every        | 50 steps
lr_schedule      | linear warmup → cosine decay
optimizer        | AdamW betas=(0.9, 0.95), wd=0.01
grad_clip        | 1.0
loss             | text_CE on Mistral SP tokens (audio_CE = 0 this stage)
```

---

## 5. Initial Loss Trajectory (step 0 → 1000)

```
step    elapsed_s    loss      lr         sps    eta_h
0       0.0          —         (start)    —      —
50      20.4         10.5602   5.00e-05   2.46   5.7
200     90.3         9.8179    2.00e-04   2.22   6.2
500     214.0        9.4979    5.00e-04   2.34   5.9   (warmup complete)
800     334.8        9.3165    5.00e-04   2.39   5.7
1000    411.5        9.1830    5.00e-04   2.43   5.6
```

**Δ from random init**: −1.39 nats (≈ 4× perplexity reduction: 38824 → 9711).
**Trajectory**: monotone decrease (modulo step-450 oscillation during warmup).
**Throughput**: 2.43 steps/s steady; data-bound between batches (GPU util 0-72%).

---

## 6. Rate vs Original Estimate

Original blocker_doc `training_plan.md` estimated **36-72h** on RTX 5070. Realized rate is **~10× faster** (5.6h projected). Three reasons:

1. Stage1 here is **text-CE only** (no audio path → no RVQ heads compute).
2. **seq_len=128** (vs ATP_CTX=1576 max).
3. **LoRA only 0.222%** of base params trainable (rest of fwd/bwd is tiny vs full FT).

Risks that could extend ETA:
- HF streaming back-pressure (observed ~30s shard-fetch stall around step 600 boundary).
- Network instability on tailscale0 (used for HF hub access).
- Worst case: 8-10h.

---

## 7. Detached Process Status

```
PID    | 31960 (parent ppid=1, nohup-detached)
log    | /tmp/vlm_stage1_logs/nohup.out
       | /tmp/vlm_stage1_logs/train.log
saves  | /tmp/vlm_stage1_savepoints/step-{5,10,15,...}k/
final  | /tmp/vlm_stage1_savepoints/step-50k-final/
```

Survives ssh disconnect. NO process supervision wrapper — see C5 below.

---

## 8. Honest C3 (raw#10)

1. **Text-CE only this cycle, not the spec'd dual loss.** Spec called for `0.5*audio_CE + 0.5*text_CE`. Audio path requires an audio codec (Encodec/Mimi) which is not installed on ubu1; precomputed RVQ codes do not exist for LibriSpeech. Audio column was dropped from the HF stream to avoid torchcodec decode overhead. The 8 RVQ heads still receive gradients via the shared backbone but their head weights drift toward noise. Best framed as **backbone warmup on natural-speech transcripts**; full VLM stage1 needs stage2 with audio loss added.
2. **Tokenizer is Mistral SP-32768, not 'CLM v4 SP-32k'.** CLM v4 base mirror in HF cache only contains `best.pt` (no `tokenizer.json`/`.model`). Mistral SP-32768 is the closest available 32k-class SentencePiece. If cond.3 cross-LM r ≥ 0.85 requires same-tokenizer fidelity, this stage1 will need re-training once a real CLM-v4 SP tokenizer ships.
3. **RTX 5070 OOM risk LOW for current config but reappears in stage2.** 819 MiB used of 12227 MiB → ~11.4 GB head-room. OOM returns if (a) seq_len bumped to 1576 (ATP_CTX), (b) audio path activated with full-sequence RVQ heads, (c) batch increased. Stage2 batch may need to drop to 1-2 with grad_accum 8-16.
4. **F1_audio_pred.json is a stub.** F1 requires GT audio tokens (no codec) AND a trained audio path (not yet exercised). True F1 evaluation must wait for stage2.
5. **No watchdog supervisor.** Detached process (ppid=1) survives ssh disconnect, but if torchcodec segfaults on a malformed audio file (we observed PyGILState_Release noise during interpreter teardown in smoke runs — cosmetic) or HF stream dies, the run terminates silently. Recommend a sister BG that tails nohup.out for `Traceback|Killed|OOM` patterns and rescues savepoints to HF.

---

## 9. Constraint Compliance

| Constraint | Status |
|---|---|
| raw#9 (.py only on ubu1 via @resolver-bypass) | PASS — atp_pytorch.py + vlm_stage1_train.py live in `tool/transient_py/` on Mac, scp to `/tmp/` on ubu1; NO writes into `anima-voice/` or `/home/aiden/anima/` |
| raw#10 (5 honest C3 caveats) | PASS — §8 above |
| raw#15 (no preempt of other ubu1 BG) | PASS — verified existing tail-only processes (eval_llama × 2, p9_p1_6_sentinel) untouched; GPU was idle pre-launch |
| $0 ubu local | PASS — no cloud spend |
| no anima-voice mutation | PASS |
| detached after launch + initial loss | PASS — returning after step 1000 confirmed |

---

## 10. Next Cycle Recommendations

1. **Watchdog BG** — tail `/tmp/vlm_stage1_logs/nohup.out` for `Traceback|Killed|OOM`; mirror savepoints to HF every 10K steps so we don't lose work if `/tmp` is wiped.
2. **Stage1 completion eval** — at step 50K (or whichever savepoint we reach), compute final text_CE on a held-out LibriSpeech-clean subset; verify monotone decrease through 50K.
3. **Codec install for stage2** — pick Encodec or Mimi, pre-encode LibriSpeech-clean-100 audio → RVQ codes parquet, re-launch with full `0.5*audio_CE + 0.5*text_CE`.
4. **HF push** — mk2 conform naming = `vlm-anima-voice-paradigm-stage1-step-{Nk}`; gated on stage1 final convergence (not the per-savepoint dumps).
5. **Real CLM-v4 SP tokenizer** — coordinate with CLM cycle to publish the SP-32k vocab so we can re-train (or LoRA-fine-tune) on aligned vocab for cond.3 r-evaluation.

---

## 11. Cost

```
cost band            | $0 (mac-local + ubu1-local)
wallclock used       | ~30 min (3 smoke runs + launch + monitor to step 1000)
ubu1 ETA to 50K      | 5.6h (continues detached after this cycle returns)
destructive actions  | 0
in-place anima-voice | 0
```
