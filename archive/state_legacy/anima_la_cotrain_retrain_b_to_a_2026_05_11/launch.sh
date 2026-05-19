#!/usr/bin/env bash
# state/anima_la_cotrain_retrain_b_to_a_2026_05_11/launch.sh
# BG-LA-COTRAIN-RETRAIN-B-TO-A — cycle 2026-05-11
# Phase: H100 cotrain on B substrate → B' → local V14 strict
# Envelope: $4-8 H100 (user authorize via 'all' on 2026-05-11)
# Dependencies (verified pre-flight 2026-05-11 10:50 KST):
#   - tool/anima_runpod_orchestrator.hexa selftest=ok
#   - ~/.runpod/config.toml synced from secret vault (REST + GraphQL 200)
#   - ~/.runpod/ssh/RunPod-Key-Go present
#   - B ckpt: /Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt (597MB)
#   - Consciousness corpus: state/anima_persona_tier_a_v4_2026_05_09.txt (232MB)
#   - Chat corpus: state/anima_native_ko_chat_template_2026_05_06/corpus_chat_template.txt (237MB)
#   - Engine arch: training/engine_a_g_arch.py
#   - Train script: training/train_phase2_cotrain.py
# Note: P2 (FOUNDATION_C_PHASE2_FIRE pod nwlb3c18fax6eh) is concurrently running;
#       account h100_max=2 permits one more pod. Confirm via 'runpodctl pod list'.

set -euo pipefail

cd ~/core/anima

STATE_DIR=state/anima_la_cotrain_retrain_b_to_a_2026_05_11
RUN_ID="la-cotrain-b-to-a-$(date +%s)"
POD_NAME="anima-la-cotrain-b-to-a-$(date +%s)"

mkdir -p "$STATE_DIR/ckpts" "$STATE_DIR/pod_state"

# Pre-flight: confirm P2 pod count + h100_max headroom
RUNNING=$(~/.local/bin/runpodctl pod list 2>/dev/null | grep -c '"desiredStatus": "RUNNING"' || true)
echo "[pre-flight] currently running pods: $RUNNING / max 2"
if [ "$RUNNING" -ge 2 ]; then
    echo "[abort] h100 quota saturated; wait for P2 to finish first" >&2
    exit 1
fi

# Phase 1: orchestrator-driven H100 fire (cotrain B → B')
echo "[phase 1] firing orchestrator for cotrain retrain (B → B' on H100)…"
HEXA_LANG=$HOME/core/hexa-lang nohup ~/.hx/bin/hexa_real run \
    ~/core/anima/tool/anima_runpod_orchestrator.hexa run \
    --pod-name "$POD_NAME" \
    --gpu-id "NVIDIA H100 80GB HBM3" \
    --image "runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04" \
    --upload "/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt:/workspace/anima_la_cotrain/bg_la_step_12000_final.pt" \
    --upload "$HOME/core/anima/state/anima_persona_tier_a_v4_2026_05_09.txt:/workspace/anima_la_cotrain/persona_tier_a_v4.txt" \
    --upload "$HOME/core/anima/state/anima_native_ko_chat_template_2026_05_06/corpus_chat_template.txt:/workspace/anima_la_cotrain/corpus_chat_template.txt" \
    --upload "$HOME/core/anima/training/train_phase2_cotrain.py:/workspace/anima_la_cotrain/train_phase2_cotrain.py" \
    --upload "$HOME/core/anima/training/engine_a_g_arch.py:/workspace/anima_la_cotrain/engine_a_g_arch.py" \
    --pip-install "torch transformers peft accelerate datasets" \
    --command "cd /workspace/anima_la_cotrain && PYTHONPATH=. python3 train_phase2_cotrain.py --substrate-ckpt bg_la_step_12000_final.pt --consciousness-corpus persona_tier_a_v4.txt --chat-corpus corpus_chat_template.txt --output ckpts --steps 6000 --bsz 4 --grad-accum 8 --ctx 1024 --lr 1.5e-4 --warmup 200 --save-every 1500 --cost-cap-usd 8.0 --cost-per-hr 2.99 2>&1 | tee /workspace/anima_la_cotrain/state/train_stdout.log" \
    --download "/workspace/anima_la_cotrain/ckpts:$HOME/core/anima/$STATE_DIR/ckpts" \
    --download "/workspace/anima_la_cotrain/state:$HOME/core/anima/$STATE_DIR/pod_state" \
    --max-cost 8.0 \
    --max-runtime-min 180 \
    --hourly-rate 2.99 \
    --auto-terminate \
    --output "$HOME/core/anima/$STATE_DIR/runpod_run.json" \
    --run-id "$RUN_ID" \
    > "$HOME/core/anima/$STATE_DIR/orchestrator_stdout.log" 2>&1 &
ORCH_PID=$!
echo "[phase 1] orchestrator PID=$ORCH_PID, monitor:"
echo "    tail -f $STATE_DIR/orchestrator_stdout.log"
echo

# Phase 2: post-pull V14 strict (local, $0) — manual step after Phase 1 completes
cat <<'NOTE' > "$STATE_DIR/POST_PULL_V14_STRICT.md"
# Post-pull V14 strict — run AFTER orchestrator completes ckpt pull

Once `state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt` exists:

```bash
# 1. Verify B' ckpt landed
ls -la state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/

# 2. Run V14 strict on B' (Mac local, no H100, $0)
#    Adapt state/anima_v14_max256_b_no_cotrain_2026_05_10/run_b.py with B' ckpt path:
cp state/anima_v14_max256_b_no_cotrain_2026_05_10/run_b.py \
   state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py

# Edit run_b_prime.py — replace substrate path with B' ckpt:
sed -i.bak 's|/.../bg_la_350m_pretrain/ckpts/step_12000_final.pt|state/anima_la_cotrain_retrain_b_to_a_2026_05_11/ckpts/ckpt_final.pt|g' \
   state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py

# 3. Execute V14 strict (n=5 seeds × max=256 paired vs random mirrors)
cd ~/core/anima && /usr/bin/python3 \
    state/anima_la_cotrain_retrain_b_to_a_2026_05_11/run_b_prime.py \
    | tee state/anima_la_cotrain_retrain_b_to_a_2026_05_11/v14_strict.log

# 4. Falsifier disposition per spec:
#    F-CAUSAL-1 (cotrain causal direction): B' V14_STRICT_PASS → CAUSAL confirmed
#                                            B' V14_VIOLATED   → cotrain is confound
#    F-CAUSAL-2 (q_proj delta direction): compare B' vs A q_proj cos
```
NOTE

echo "[phase 2 stub] saved to $STATE_DIR/POST_PULL_V14_STRICT.md (manual after Phase 1 done)"
echo
echo "=== Launch complete. P3 orchestrator running in background. ==="
echo "Phase 1 (H100 cotrain): orch PID=$ORCH_PID, ~2-3 hours"
echo "Phase 2 (local V14 strict): manual, see POST_PULL_V14_STRICT.md"
