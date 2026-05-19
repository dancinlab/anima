#!/bin/bash
# state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13/dispatch_h100_v5_ddp.sh
#
# v5-mitosis cotrain v5 DDP — 4× H100 SXM multi-GPU scale-up resuming from v4 step 2000.
# (post-★★★★★ 2026-05-13)
#
#   v1: d=384  cells=64  5K  $1.26    F-PERSONA-4 KL=0
#   v2: d=768  cells=128 10K ~$3.5    M4 cosine z=3.20 PASS
#   v3-routing: d=384 cells=64 8K    routing fix (top-K MoE)
#   v4: d=1024 cells=256 20K (single A100, ~17hr ETA, in-flight) — ckpt_step_2000 source
#   v5 DDP (THIS): 4× H100 SXM, resume step 2000 → step 20000, expected ~4-5hr wall
#       Same arch as v4 (d=1024 cells=256). Cells FROZEN (mitosis-skip) for DDP safety;
#       v4 already saturated cells=256 at step 2000 so no loss.
#       find_unused_parameters=True for top-K=8 over 256 cells.
#       per_gpu_batch=4 × world_size=4 = effective_batch=16 (vs v4 single batch=8).
#
# Reference: state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12/dispatch_h100_v4.sh
#   (PSCC §45 direct-IP; trap cleanup + SAVE_POD on pull-fail) +
#   memory feedback_no_scale_caps + feedback_orchestrator_h100_gotchas +
#   feedback_dispatch_vast_template_gotchas (§45 direct-IP, set -o pipefail remote).
#
# To fire:  bash dispatch_h100_v5_ddp.sh
# Env overrides: STEPS RESUME_STEP BATCH CTX LR WARMUP D_MODEL N_HEAD FFN_DIM MAX_CELLS
#                INITIAL_CELLS TOP_K AUX_ALPHA LAMBDA_INIT LAMBDA_FINAL LAMBDA_SCHEDULE
#                READOUT_MODE COST_CAP_USD COST_PER_HR_MAX ESTIMATED_WALL_HR SEED N_PERMS
#                GPU_FILTER NUM_GPUS SAVE_POD=1

set -euo pipefail

PHASE_ID="v5mitosis_cotrain_v5_ddp"
LOCAL_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v5_ddp_2026_05_13"
SRC_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"          # mitosis_model_v5.py, identity_probe.jsonl
SRC_V2_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v2_2026_05_12"    # corpus_5cat_balanced.txt
SRC_V4_DIR="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v4_scaleup_2026_05_12"  # ckpt_step_2000.pt
TRAINING_DIR="/Users/ghost/core/anima/training"                                     # cotrain_v5mitosis_v5_ddp.py
PHASE_LABEL="anima-v5mit-v5-ddp"

# ── DDP / arch ──
NUM_GPUS="${NUM_GPUS:-4}"          # 4× H100 SXM
STEPS="${STEPS:-20000}"            # target global step
RESUME_STEP="${RESUME_STEP:-2000}" # v4 step-2000 ckpt
BATCH="${BATCH:-4}"                # per-GPU; effective = 4 × NUM_GPUS = 16
CTX="${CTX:-512}"
LR="${LR:-1e-4}"
WARMUP="${WARMUP:-2000}"
D_MODEL="${D_MODEL:-1024}"
N_HEAD="${N_HEAD:-16}"
FFN_DIM="${FFN_DIM:-4096}"
INITIAL_CELLS="${INITIAL_CELLS:-256}"   # MUST match v4 ckpt n_cells
MAX_CELLS="${MAX_CELLS:-256}"
READOUT_MODE="${READOUT_MODE:-a_minus_g}"
SEED="${SEED:-42}"
TOP_K="${TOP_K:-8}"
AUX_ALPHA="${AUX_ALPHA:-0.01}"
LAMBDA_INIT="${LAMBDA_INIT:-1.0}"
LAMBDA_FINAL="${LAMBDA_FINAL:-0.01}"
LAMBDA_SCHEDULE="${LAMBDA_SCHEDULE:-cosine}"
N_PERMS="${N_PERMS:-100}"
CKPT_EVERY="${CKPT_EVERY:-5000}"
DISK_GB="${DISK_GB:-200}"

# ── cost (no scale caps; cap = floor not ceiling; memory feedback_no_scale_caps) ──
COST_CAP_USD="${COST_CAP_USD:-100.0}"
COST_PER_HR_MAX="${COST_PER_HR_MAX:-20.0}"  # 4× H100/H200/B200 ~$3-5/hr each (H100 SXM often empty)
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-5.0}"
ABSOLUTE_MAX_USD=$(python3 -c "print($COST_CAP_USD * 1.10)")

# Prefer 4× H100 SXM; fall back to H100_NVL/PCIE/H200/B200 (all multi-GPU NVLink-capable).
# 2026-05-13 H100_SXM often unavailable as 4-GPU node; H200 4× ~$12-15/hr is cheapest viable.
MIN_GPU_RAM_MB="${MIN_GPU_RAM_MB:-75000}"
GPU_FILTER="${GPU_FILTER:-gpu_name in [H100_SXM,H100_NVL,H100_PCIE,H200,B200] num_gpus=${NUM_GPUS} reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>${DISK_GB} inet_down>200}"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/.local/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || VASTAI="/Users/ghost/Library/Python/3.13/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found"; exit 1; }

mkdir -p "$LOCAL_DIR/ckpts"
cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai ${NUM_GPUS}× H100 dispatch (v5 DDP) ==="
date -u
echo "  resume from v4 ckpt_step_2000.pt :: steps $RESUME_STEP -> $STEPS"
echo "  per_gpu_batch=$BATCH world_size=$NUM_GPUS effective_batch=$((BATCH * NUM_GPUS))"
echo "  arch: d=$D_MODEL n_head=$N_HEAD ffn=$FFN_DIM cells=$INITIAL_CELLS-$MAX_CELLS ctx=$CTX"
echo "  routing: top_k=$TOP_K aux_alpha=$AUX_ALPHA λ_init=$LAMBDA_INIT λ_final=$LAMBDA_FINAL sched=$LAMBDA_SCHEDULE"
echo "  cost_cap=\$$COST_CAP_USD absolute_max=\$$ABSOLUTE_MAX_USD per_hr_max=\$$COST_PER_HR_MAX"

# ckpt source check — prefer v4 step_2000 (extracted), else v3-routing step_2000 (same arch).
# If neither valid (corrupt / partial), fall through to fresh start (initial_cells=256, no split).
RESUME_CKPT_LOCAL="$SRC_V4_DIR/ckpts/ckpt_step_2000.pt"
USE_RESUME=1
if [ ! -f "$RESUME_CKPT_LOCAL" ]; then
    RESUME_CKPT_LOCAL="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_v3_routing_2026_05_12/ckpts/ckpt_step_2000.pt"
fi
if [ ! -f "$RESUME_CKPT_LOCAL" ]; then
    echo "[INFO] no resume ckpt available — proceeding with FRESH START (initial_cells=$INITIAL_CELLS, no mitosis)"
    USE_RESUME=0
    RESUME_CKPT_LOCAL=""
    RESUME_STEP=0
else
    # Validate ckpt is loadable (not partial / corrupt) by reading the zip central directory.
    if ! python3 -c "import zipfile; zipfile.ZipFile('$RESUME_CKPT_LOCAL').namelist()" >/dev/null 2>&1; then
        echo "[WARN] resume ckpt CORRUPT (zip cd missing): $RESUME_CKPT_LOCAL — falling back to FRESH START"
        USE_RESUME=0
        RESUME_CKPT_LOCAL=""
        RESUME_STEP=0
    else
        RESUME_SIZE_MB=$(du -m "$RESUME_CKPT_LOCAL" | awk '{print $1}')
        echo "[INFO] resume ckpt validated: $RESUME_CKPT_LOCAL (${RESUME_SIZE_MB}MB)"
    fi
fi

echo "[1/9] Searching ${NUM_GPUS}× GPU offers ($GPU_FILTER) — cheapest with gpu_ram>=${MIN_GPU_RAM_MB}MB ..."
OFFER_JSON=$($VASTAI search offers "$GPU_FILTER" -o dph_total --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | MIN_GPU_RAM_MB="$MIN_GPU_RAM_MB" python3 -c "
import json, os, sys
try: data = json.load(sys.stdin)
except Exception as e: sys.stderr.write(f'parse_err: {e}\n'); sys.exit(1)
if not data: sys.stderr.write('no_offers\n'); sys.exit(1)
minram = float(os.environ.get('MIN_GPU_RAM_MB', '75000'))
cand = sorted((x for x in data if float(x.get('gpu_ram', 0) or 0) >= minram), key=lambda x: x['dph_total'])
if not cand: sys.stderr.write(f'no_offers_ge_{int(minram)}MB (had {len(data)} but all < {int(minram)}MB)\n'); sys.exit(1)
b = cand[0]
print(f'{b[\"id\"]} {b[\"dph_total\"]:.4f} {b[\"gpu_name\"].replace(\" \", \"_\")} {b.get(\"reliability\",0):.3f} {int(b.get(\"gpu_ram\",0) or 0)} {b.get(\"num_gpus\",0)}')
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_NGPU=$(echo "$OFFER_PARSED" | awk '{print $6}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$(echo "$OFFER_PARSED" | awk '{print $3}') num_gpus=$OFFER_NGPU gpu_ram=$(echo "$OFFER_PARSED" | awk '{print $5}')MB rel=$(echo "$OFFER_PARSED" | awk '{print $4}')"

EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then echo "[ABORT] est_cost \$$EST_COST > absolute_max \$$ABSOLUTE_MAX_USD"; exit 1; fi
echo "[2/9] cost gate OK (est \$$EST_COST)"

echo "[3/9] Renting..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk "$DISK_GB" --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try: d=json.load(sys.stdin)
except Exception: sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: parse instance id from: $CREATE_OUT"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    local exit_code=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keeping instance $INSTANCE_ID (exit=$exit_code)"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$exit_code)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

echo "[4/9] Waiting SSH (direct-IP) ..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 180); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status',''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); print(d.get('public_ipaddr','') or d.get('ssh_host',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin)
 p=d.get('direct_port_start','')
 if not p:
  pm=d.get('ports',{}) or {}
  v=pm.get('22/tcp') or pm.get('22/tcp'.replace('/tcp',''))
  if v and isinstance(v,list) and v: p=v[0].get('HostPort','')
 if not p: p=d.get('ssh_port','')
 print(p)
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... $i/180 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; SAVE_POD=1; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt

SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

echo "[5/9] Uploading code+corpus+probe+(maybe)resume_ckpt ..."
$SSH_CMD 'mkdir -p /workspace/anima/training /workspace/anima/corpus /workspace/anima/output /workspace/anima/probe /workspace/anima/ckpts'
$SCP_CMD "$SRC_DIR/mitosis_model_v5.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$TRAINING_DIR/cotrain_v5mitosis_v5_ddp.py" "root@$SSH_HOST:/workspace/anima/training/"
$SCP_CMD "$SRC_V2_DIR/corpus_5cat_balanced.txt" "root@$SSH_HOST:/workspace/anima/corpus/"
$SCP_CMD "$SRC_DIR/identity_probe.jsonl" "root@$SSH_HOST:/workspace/anima/probe/"
if [ "$USE_RESUME" = "1" ]; then
    echo "  uploading resume ckpt (${RESUME_SIZE_MB}MB) ..."
    $SCP_CMD "$RESUME_CKPT_LOCAL" "root@$SSH_HOST:/workspace/anima/ckpts/ckpt_step_2000.pt"
else
    echo "  no resume ckpt — fresh start"
fi

echo "[6/9] (image already has torch — skip pip install)"
# Sanity check: GPUs visible to torchrun.
$SSH_CMD 'nvidia-smi -L; python3 -c "import torch; print(\"torch=\", torch.__version__, \"cuda=\", torch.cuda.is_available(), \"n_gpu=\", torch.cuda.device_count())"' 2>&1 | head -20

echo "[7/9] Train v5 DDP (torchrun nproc_per_node=$NUM_GPUS) ..."
TRAIN_RC=99
CUR_BATCH=$BATCH
for attempt in 1 2 3; do
    echo "  >>> attempt $attempt: per_gpu_batch=$CUR_BATCH (effective $((CUR_BATCH * NUM_GPUS)))"
    set +e
    RESUME_ARG=""
    if [ "$USE_RESUME" = "1" ]; then
        RESUME_ARG="--resume-ckpt ckpts/ckpt_step_2000.pt --resume-step $RESUME_STEP"
    fi
    $SSH_CMD "set -o pipefail; cd /workspace/anima && export PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True NCCL_DEBUG=WARN && \
        torchrun --standalone --nproc_per_node=$NUM_GPUS training/cotrain_v5mitosis_v5_ddp.py \
        $RESUME_ARG \
        --corpus corpus/corpus_5cat_balanced.txt \
        --output-dir output \
        --steps $STEPS --batch $CUR_BATCH --ctx $CTX --lr $LR --warmup $WARMUP \
        --d-model $D_MODEL --n-head $N_HEAD --ffn-dim $FFN_DIM \
        --initial-cells $INITIAL_CELLS --max-cells $MAX_CELLS --readout-mode $READOUT_MODE \
        --seed $SEED --log-every 50 --ckpt-every $CKPT_EVERY \
        --cost-cap-usd $COST_CAP_USD --cost-per-hr $OFFER_DPH --estimated-wall-hr $ESTIMATED_WALL_HR \
        --identity-probe probe/identity_probe.jsonl \
        --top-k $TOP_K --aux-alpha $AUX_ALPHA \
        --lambda-init $LAMBDA_INIT --lambda-final $LAMBDA_FINAL --lambda-schedule $LAMBDA_SCHEDULE \
        --n-perms $N_PERMS --freeze-mitosis 1 2>&1 | tee train_v5_ddp.log" 2>&1 | tee -a dispatch_v5_ddp.log
    TRAIN_RC=${PIPESTATUS[0]}
    set -e
    OOM=$($SSH_CMD "grep -ci 'out of memory\|CUDA out of memory\|OutOfMemoryError' /workspace/anima/train_v5_ddp.log 2>/dev/null || echo 0" 2>/dev/null || echo 0)
    if [ "$TRAIN_RC" = "0" ] && [ "${OOM:-0}" -eq 0 ]; then echo "  train OK (rc=0, no OOM)"; break; fi
    if [ "${OOM:-0}" -gt 0 ] && [ "$CUR_BATCH" -gt 1 ]; then
        CUR_BATCH=$(( CUR_BATCH / 2 )); [ "$CUR_BATCH" -lt 1 ] && CUR_BATCH=1
        echo "  [OOM detected] retry with per_gpu_batch=$CUR_BATCH"
        $SSH_CMD 'rm -rf /workspace/anima/output && mkdir -p /workspace/anima/output' 2>&1 | tail -1
        continue
    fi
    echo "  train rc=$TRAIN_RC (oom_count=$OOM) — no further retry"
    break
done

echo "[8/9] Downloading (MANDATORY before pod delete — memory feedback_orchestrator_h100_gotchas) ..."
PULL_OK=1
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_final.pt" "$LOCAL_DIR/ckpts/ckpt_v5mitosis_cotrain_v5_ddp.pt" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/cotrain_v5_ddp_result.json" "$LOCAL_DIR/cotrain_v5_ddp_result.json" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/train_v5_ddp.log" "$LOCAL_DIR/train_v5_ddp.log" || PULL_OK=0
$SCP_CMD "root@$SSH_HOST:/workspace/anima/output/ckpt_step_*.pt" "$LOCAL_DIR/ckpts/" 2>/dev/null || true
if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] pull failed — SETTING SAVE_POD=1 (pod retained for manual recovery)"
    SAVE_POD=1
fi

echo "[9/9] DONE"
date -u
if [ -f "$LOCAL_DIR/cotrain_v5_ddp_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/cotrain_v5_ddp_result.json'))
t = d.get('training', {}); rf = d.get('routing_fix', {}); cfg = d.get('config', {}); dp = d.get('ddp', {}); rs = d.get('resume', {})
a = d.get('f_persona_4a_routing', {}); aw = a.get('topk_weights', {})
b = d.get('f_persona_4b_content', {}); fv = d.get('f_v5mit_regression', {})
print(f'  DDP: world={dp.get(\"world_size\")} per_gpu_batch={dp.get(\"per_gpu_batch\")} effective_batch={dp.get(\"effective_batch\")} freeze_mitosis={dp.get(\"freeze_mitosis\")}')
print(f'  RESUME: from step {rs.get(\"resume_step\")} → target {rs.get(\"target_step\")} (this session ran {rs.get(\"steps_run_this_session\")} steps)')
print(f'  arch: d={cfg.get(\"d_model\")} n_head={cfg.get(\"n_head\")} ffn={cfg.get(\"ffn_dim\")} cells_max={cfg.get(\"max_cells\")} ctx={cfg.get(\"max_seq\")}')
print(f'  routing: top_k={rf.get(\"top_k\")} aux_alpha={rf.get(\"aux_alpha\")} λ {rf.get(\"lambda_init\")}→{rf.get(\"lambda_final\")}  n_params={d.get(\"n_params\")}')
print(f'  wall={t.get(\"wall_hours\",0):.2f}hr cost=\${t.get(\"cost_usd_actual\",0):.2f} ce={t.get(\"ce_final_avg100\",0):.3f} cost_aborted={t.get(\"cost_aborted\")}')
print(f'  cells_final={t.get(\"n_cells_final\")} splits(saved)={t.get(\"splits\")} phi={t.get(\"phi_final\",0):.3f} phi_best={t.get(\"phi_best\",0):.3f}')
print(f'  wmax={t.get(\"wmax_final_avg100\",0):.4f} active>.01={t.get(\"n_active_gt01_final_avg100\",0):.1f}/{t.get(\"n_cells_final\")} gate_max={t.get(\"gate_max_final_avg100\",0):.3f} aux={t.get(\"aux_final_avg100\",0):.3f}')
print(f'  F-PERSONA-4a routing: {a.get(\"verdict\")} KL={aw.get(\"mean_kl\",0):.4f} z={aw.get(\"z_score_vs_null\",0):.2f} p={aw.get(\"p_value_one_sided\",0):.4f}')
sg = a.get(\"soft_gate\")
if sg: print(f'  F-PERSONA-4a soft gate: KL={sg.get(\"mean_kl\",0):.4f} z={sg.get(\"z_score_vs_null\",0):.2f}')
print(f'  F-PERSONA-4b content (M4 aggregated cosine): {b.get(\"verdict\")} z={b.get(\"z_score_vs_null\",0):.2f} (v2 carry z={b.get(\"v2_carry_z\",0):.2f})')
print(f'  F-V5MIT-1..5: {fv.get(\"verdict\")}')
"
fi
