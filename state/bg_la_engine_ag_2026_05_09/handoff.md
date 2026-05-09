# BG-LA Engine A/G H100 Fire — Handoff State

## Status (2026-05-09T05:38Z)
- TRAINING LIVE — pod 4wxx2wvcvgjp88 H100 SXM
- step 350/12000, loss 10.54 → 2.21 in 960s, GPU 99% util, 27GB VRAM
- ETA: ~9.13hr wall, ~$27 cost (within $30 cap)

## Next agent: pickup script

```bash
SSH_HOST=87.120.211.205
SSH_PORT=10025
SSH_KEY=/Users/ghost/.runpod/ssh/RunPod-Key-Go
STATE_DIR=/Users/ghost/core/anima/state/bg_la_engine_ag_2026_05_09

# 1. Check progress
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
    'tail -10 /workspace/anima_clm_la/train.log; \
     ls /workspace/anima_clm_la/ckpts/ 2>/dev/null'

# 2. Check sentinel
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
    'cat /workspace/anima_clm_la/state/COMPLETE.sentinel 2>/dev/null'

# 3. Pull ckpts (own 30 mandate-1 — BEFORE pod delete)
mkdir -p "$STATE_DIR/results/ckpts"
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r \
    -o ConnectTimeout=3600 \
    root@$SSH_HOST:/workspace/anima_clm_la/ckpts/. \
    "$STATE_DIR/results/ckpts/"
scp -i "$SSH_KEY" -P "$SSH_PORT" -o StrictHostKeyChecking=no -r \
    root@$SSH_HOST:/workspace/anima_clm_la/state/. \
    "$STATE_DIR/results/state/"

# 4. Size sanity (own 30 mandate-2)
POD_SZ=$(ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no root@$SSH_HOST \
    'du -sb /workspace/anima_clm_la/ckpts | cut -f1')
LOCAL_SZ=$(du -sb "$STATE_DIR/results/ckpts" | cut -f1)
echo "pod=$POD_SZ local=$LOCAL_SZ (floor 0.9× pod)"

# 5. Release ONLY if pull verified (own slug only — no sibling pods touched)
if [ "$LOCAL_SZ" -ge $((POD_SZ * 9 / 10)) ]; then
    HEXA=/Users/ghost/.hx/packages/hexa/hexa.real \
      /Users/ghost/.hx/packages/resource/bin/resource release \
      h100-runpod-4wxx2wvcvgjp88-1778300273
fi
```

## Post-train: v5 probe (Mac local)
- bg-la-engine-ag v5 N=60 + V14 paired (random_init mirrors 5 seeds @ state/v14_mirrors/BG-LA)
- PPR_v5 + MTRP_v5 + Gate F D-RAND
- own 18 SIMPLE_STACK_PASS_STRICT_C3 verdict
- EXIT trigger: PPR≥0.30 + MTRP≥0.10 → first non-LoRA scratch arch EMERGE candidate

## HF private upload (own 31 Flavor B + own 37 default-private)
- target: dancinlab/clm-v5-bg-la-engine-ag-{verdict_short}-2026-05-09

## Cost tracking
- provisioned: 2026-05-09T04:18:51Z
- train_start: 2026-05-09T05:21:59Z (+1h 03min provision/upload overhead)
- $2.99/hr × ~10hr = ~$30 (at hard cap; halt + release if exceeded)
