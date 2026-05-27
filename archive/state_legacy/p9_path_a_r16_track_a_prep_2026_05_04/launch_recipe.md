# P9 Path A r=16 + Track A Corpus Retrain — Launch Recipe

**Status**: READY-TO-FIRE (pre-prep complete, no $ spent yet)
**Trigger**: r=16 multi-seed (s42+s43+s44) verdict @ 13:26 UTC = MITIGATION_PARTIAL or FAIL
**Cost when launched**: $20-30 (fresh H100 pod provision + 4-6h training)

## TL;DR — 1-Command Launch Sequence

```bash
# Step 1: provision fresh H100 pod (RunPod CLI; mirrors s43/s44 pattern)
runpodctl create pod \
  --name p9-path-a-r16-track-a \
  --gpuType "NVIDIA H100 80GB HBM3" \
  --imageName runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 \
  --containerDiskSize 100 \
  --volumeSize 50 \
  --ports "22/tcp"
# Capture POD_ID from response
export POD_ID=<pod_id>

# Step 2: upload artifacts (corpus + train script + HF token)
runpodctl send /tmp/p9_path_a_track_a_corpus_50k.jsonl $POD_ID:/workspace/p9_path_a_track_a_corpus_50k.jsonl
runpodctl send /tmp/train_llama_lora_r16_track_a.py $POD_ID:/workspace/train_llama_lora_r16_track_a.py
runpodctl send /tmp/launch_r16_track_a.txt $POD_ID:/workspace/launch_r16_track_a.txt
# HF token: write a fresh valid token to /workspace/hf_token (ubu1 has all-invalid tokens; rotate first)
runpodctl send /path/to/fresh/hf_token $POD_ID:/workspace/hf_token

# Step 3: launch training (detached)
runpodctl exec $POD_ID -- bash /workspace/launch_r16_track_a.txt

# Step 4: arm host-side terminator + cost watchdog (mirror s43 pattern)
# (use state/p9_path_a_r16_3seed_2026_05_04/host_terminator_s43.txt template,
#  swap pod-id and out-dir to track_a)
```

## Detailed Steps

### Pre-Launch Checklist (5 min)
1. Verify r=16 verdict requires Track A retrain (MITIGATION_PARTIAL or FAIL — not OK)
2. Refresh HF token if needed: `hf auth login --force` (current ubu1 tokens all invalid)
3. Confirm RunPod balance ≥ $30 (H100 80GB ~ $3.50/hr × 6h + provision overhead)
4. Confirm corpus + script SHAs match preflight.json (ubu1 /tmp artifacts unchanged)

### Provision (10-15 min)
- Fresh H100 80GB pod (no reuse — all 6 prior pods purged 2026-05-03)
- Image: runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04 (matches s43/s44)
- Container disk 100GB, volume 50GB

### Upload (5-10 min over runpodctl send)
- Corpus 89MB
- Train script 8KB
- Launcher 2KB
- HF token (fresh, validated)

### Launch (instant)
- `bash /workspace/launch_r16_track_a.txt`
- Auto-detached via nohup; PID written to $OUT_DIR/train.pid

### Training (4-6h ETA on H100 80GB)
- 10000 steps × ~1.5-2s/step
- save_steps=2000 → 5 savepoints + final
- Per-savepoint HF push (every_save strategy)

### Terminator + Cost Watchdog (mirror s42/s43 pattern)
```bash
# host_terminator_track_a.txt template — adapted from
# state/p9_path_a_r16_3seed_2026_05_04/host_terminator_s43.txt
# - Watches for TRAIN_DONE.json with phase=final_saved
# - Polls every 60s; terminates pod within 10min of completion
# - Logs to host_terminator_track_a.log
# Cost watchdog: kills pod if cost exceeds $35 (safety margin)
```

## 4 Caveats (raw#10)

1. **Pre-prep based on PREDICTION**: Corpus audit predicts HIGH chat-mode collapse risk on 50/50 corpus, but r=16 may empirically pass (MITIGATION_OK at 13:26 UTC). In that case Track A prep is unused (not wasted: artifacts persist, $0 sunk).

2. **Corpus dedup ceiling 38K not 50K**: P9 SFT chat side caps at ~23397 unique after MD5 dedup. Final composition is 61% chat / 20% trivia / 18% mmlu — still below 70/30 Track A spec. To hit true 70/30, would need to either (a) augment chat side with +10-15K synthetic pairs, or (b) downsample factual side. Current Track A is "best-effort with available rows".

3. **Mini vs full decision DEFERRED**: Full 38K corpus is the default (this recipe). Mini 5K corpus is also pre-built (`/tmp/p9_path_a_track_a_mini_corpus_5k.jsonl`) for fast-iteration if r=16 verdict is severe and cheap empirical signal is preferred over full-budget retrain. Decision deferred to verdict moment.

4. **Fresh H100 pod $20-30 cost NOT yet incurred**: All 6 EXITED H100 pods purged 2026-05-03; Phase 2 launch must boot fresh from HF base mirror. $0 spent on this prep cycle. Cost only triggers if recipe is fired.

## Additional Concerns Flagged During Prep

- **HF token blocker (BLOCKING for hub_strategy=every_save)**: All 3 HF tokens on ubu1 (`~/.cache/huggingface/token`, `~/.hf_token`, `/home/aiden/anima/.secrets/hf_token`) return 401 Unauthorized from whoami-v2. Pre-create of `dancinlab/llm-llama32-3b-paradigm-a-prime-r16-track-a-sft-stage1` was NOT possible during prep. **Mitigation**: launcher writes `/workspace/hf_token` from fresh source at upload time; if HF push must happen, validate token at upload step, NOT relying on stale ubu1 tokens.

- **Epoch count delta**: Track A 38K @ 10K steps = 8.38 epochs vs sister r=16 @ 50K = 6.4 epochs (+31% more passes). Risk of slightly more aggressive overfitting on Track A side. **Mitigation option**: reduce `--max-steps 7600` for epoch parity (not applied in default recipe — kept 10000 for cross-comparison consistency).

- **Track A composition is 61/20/18**, not the audit's stated "70/30 chat:factual target". The corpus IS re-balanced toward chat (vs 50/50 baseline) but not all the way to 70/30 due to dedup ceiling. Reframe: "Track A as-built" not "Track A spec-compliant".
