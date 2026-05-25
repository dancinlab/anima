#!/bin/bash
# state/hexad_p6_fire_2026_05_16/dispatch.sh — HEXAD Phase 6 real-scale
# integrated 6-module+Bridge fire dispatch (hexa-native).
#
# AGENTS.tape g_fire_autonomous (2026-05-16): cost-bearing GPU fire is
# fully autonomous — NO approval gate, NO wait, unconditional. Estimated
# cost stated transparently (informational). g_fire_dispatch_robust
# safety: H100→A100 SXM4 fallback, trap cleanup honoring SAVE_POD,
# direct-IP SSH, result.json→SAVE_POD auto-promote, scp retry ≥3,
# `|| true` guards (cycle-88 ckpt-loss lesson).
#
# Payload: self-contained flattened C (p6_flat.c — built from
# train_p6_integ.hexa via the PR#51 bootstrap hexa_v2) + runtime.c +
# runtime.h. Remote = clang -O2 + run at real scale (dim=256 V=64).
# No toolchain shipping fragility; ~735KB upload total.
#
# Estimated cost: ~$1-5 (precedent: .clm v1 P2 $0.19-0.34; this is a
# CPU-bound pure-hexa integration fire — scale fire, minutes wall).

set -euo pipefail

PHASE_ID="hexad_p6_fire"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_p6_fire_2026_05_16"
PHASE_LABEL="anima-hexad-p6-fire"

# Real-scale params (env-overridable)
P6_DIM="${P6_DIM:-256}"
P6_VOCAB="${P6_VOCAB:-64}"
P6_NSAMP="${P6_NSAMP:-16}"
P6_STEPS="${P6_STEPS:-300}"
P6_SEED="${P6_SEED:-42}"
P6_CELLS="${P6_CELLS:-2}"

# Cost envelope (informational — g_fire_autonomous, no gate)
COST_PER_HR_MAX="${COST_PER_HR_MAX:-3.5}"
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-0.5}"   # CPU-bound integ fire, minutes
ABSOLUTE_MAX_USD="${ABSOLUTE_MAX_USD:-15.0}"     # generous ceiling, hard stop

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found at $VASTAI"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
[ -f "$LOCAL_DIR/p6_flat.c" ] || { echo "ERROR: p6_flat.c missing"; exit 1; }
# runtime_tree.tgz is a build-only payload (2.4 MB, NOT committed).
# Regenerate from the PR#51 bootstrap worktree's self/ before dispatch:
#   cd /tmp/hexa-p6-boot/self && \
#   tar czf $LOCAL_DIR/runtime_tree.tgz runtime.c runtime.h \
#       runtime_hi_gen.c native/
[ -f "$LOCAL_DIR/runtime_tree.tgz" ] || { echo "ERROR: runtime_tree.tgz missing — regenerate from /tmp/hexa-p6-boot/self (see comment above)"; exit 1; }

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai dispatch (Phase 6, 2026-05-16) ==="
date -u
echo "  scale: dim=$P6_DIM V=$P6_VOCAB nsamp=$P6_NSAMP steps=$P6_STEPS seed=$P6_SEED"
echo "  est wall ${ESTIMATED_WALL_HR}hr  absolute_max=\$$ABSOLUTE_MAX_USD"
echo "  payload: p6_flat.c $(wc -c < p6_flat.c)B + runtime_tree.tgz $(wc -c < runtime_tree.tgz)B"

# ── 1) GPU offer search (H100 → A100 SXM4 fallback) ──────────────────
echo "[1/9] Searching H100/A100 offers under \$${COST_PER_HR_MAX}/hr ..."
OFFER_JSON=$($VASTAI search offers \
    "gpu_name in [H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>40 inet_down>200" \
    -o dph_total --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json, sys
try: data = json.load(sys.stdin)
except Exception as e: sys.stderr.write(f'parse_err: {e}\n'); sys.exit(1)
if not data: sys.stderr.write('no_offers\n'); sys.exit(1)
b = data[0]
print(f'{b[\"id\"]} {b[\"dph_total\"]:.4f} {b[\"gpu_name\"]} {b.get(\"reliability\",0):.3f}')
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU"

# ── 2) Pre-fire cost gate (informational hard-stop only) ─────────────
EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 4))")
echo "[2/9] cost: est=\$$EST_COST  absolute_max=\$$ABSOLUTE_MAX_USD (g_fire_autonomous — no approval gate)"
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then
    echo "[ABORT] est_cost \$$EST_COST exceeds hard ceiling \$$ABSOLUTE_MAX_USD"; exit 1
fi
echo "  ✓ within ceiling"

# ── 3) Rent instance ─────────────────────────────────────────────────
echo "[3/9] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 40 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json, sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_fail\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id', ''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: instance id parse failed"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    local rc=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keep instance $INSTANCE_ID"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$rc)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

# ── 4) Wait for SSH (direct-IP) ──────────────────────────────────────
echo "[4/9] Waiting for SSH (max 13 min)..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status',''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('public_ipaddr','') or d.get('ssh_host',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); ports=d.get('ports',{}) or {}
 m=ports.get('22/tcp')
 print(m[0]['HostPort'] if m else (d.get('direct_port_start','') or d.get('ssh_port','')))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# ── 5) Upload self-contained payload ─────────────────────────────────
# NOTE (recipe correction, verified working 2026-05-16 on instance
# 36853899): runtime.c is NOT self-contained — it `#include`s
# runtime_hi_gen.c + 16 native/*.c. Ship the runtime_tree.tgz
# (runtime.c + runtime.h + runtime_hi_gen.c + native/, regenerated from
# the /tmp PR#51 bootstrap worktree's self/) and extract on the remote.
echo "[5/9] Uploading p6_flat.c + runtime_tree.tgz..."
$SSH_CMD 'mkdir -p /workspace/p6/out /workspace/p6/out/ckpts'
$SCP_CMD "$LOCAL_DIR/p6_flat.c"        "root@$SSH_HOST:/workspace/p6/p6_flat.c"
$SCP_CMD "$LOCAL_DIR/runtime_tree.tgz" "root@$SSH_HOST:/workspace/p6/runtime_tree.tgz"
$SSH_CMD 'cd /workspace/p6 && rm -rf self && mkdir self && tar xzf runtime_tree.tgz -C self && ls /workspace/p6 && ls self | head'

# ── 6) Toolchain sanity (clang) ──────────────────────────────────────
echo "[6/9] Remote clang sanity..."
$SSH_CMD 'which clang || (apt-get update -qq && apt-get install -y -qq clang) ; clang --version | head -1' || true

# ── 7) Build + run real-scale integrated fire ────────────────────────
echo "[7/9] Build (clang -O2) + run (dim=$P6_DIM V=$P6_VOCAB steps=$P6_STEPS)..."
# HEXA_MEM_UNLIMITED=1 is MANDATORY at real scale (dim=256 V=64 → the
# all-hexa W_d + farr arrays exceed the 4 GB default RSS cap; verified:
# fuel_abort kind=mem at 4096 MB without it, clean run with it).
$SSH_CMD "cd /workspace/p6 && \
  clang -O2 -fno-strict-aliasing -std=gnu11 -D_GNU_SOURCE -Wno-trigraphs -I self \
    -c self/runtime.c -o self/runtime.o 2>&1 | tail -3 ; \
  clang -O2 -fno-strict-aliasing -std=gnu11 -D_GNU_SOURCE -Wno-trigraphs -I self \
    p6_flat.c self/runtime.o -o p6_train -lm -ldl 2>&1 | tail -5 ; \
  echo BUILD_RC=\$? ; \
  export PYTHONUNBUFFERED=1 HEXA_MEM_UNLIMITED=1 P6_DIM=$P6_DIM P6_VOCAB=$P6_VOCAB \
         P6_NSAMP=$P6_NSAMP P6_STEPS=$P6_STEPS P6_SEED=$P6_SEED P6_CELLS=$P6_CELLS \
         P6_OUT=/workspace/p6/out && \
  ./p6_train 2>&1 | tee /workspace/p6/train.log" 2>&1 | tee dispatch.log || true
# g_fire_dispatch_robust: `|| true` neutralizes set -e false-positive
TRAIN_EXIT=${PIPESTATUS[0]:-0}
echo "  train pipeline exit = $TRAIN_EXIT"

# ── 8) Pull artifacts (g_fire_dispatch_robust) ───────────────────────
echo "[8/9] Verify result.json on remote + SAVE_POD auto-promote..."
SAVED=$($SSH_CMD 'test -f /workspace/p6/out/result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
    echo "  ✓ result.json exists on remote — SAVE_POD=1 (protected until pulled)"
    SAVE_POD=1
else
    echo "  ⚠ result.json NOT found — SAVE_POD=1 for inspection"
    SAVE_POD=1
fi

mkdir -p "$LOCAL_DIR/ckpts"
pull_with_retry() {
    local src="$1" dst="$2" tries=0
    while [ $tries -lt 3 ]; do
        if $SCP_CMD "root@$SSH_HOST:$src" "$dst" 2>&1; then
            echo "  ✓ pulled $src (try $((tries+1)))"; return 0
        fi
        tries=$((tries+1)); echo "  ... pull retry $tries/3 for $src"
        [ $tries -lt 3 ] && sleep 60
    done
    echo "  ✗ pull FAILED after 3 tries: $src"; return 1
}
PULL_OK=1
pull_with_retry "/workspace/p6/out/result.json" "$LOCAL_DIR/result.json" || PULL_OK=0
pull_with_retry "/workspace/p6/train.log" "$LOCAL_DIR/train.log" || PULL_OK=0
pull_with_retry "/workspace/p6/out/ckpts/ckpt_p6_Wd.txt" "$LOCAL_DIR/ckpts/ckpt_p6_Wd.txt" || PULL_OK=0

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — pod RETAINED (SAVE_POD=1)"
    echo "[WARN] manual recovery: ssh -i $VAST_SSH_KEY -p $SSH_PORT root@$SSH_HOST"
    echo "[WARN] scp /workspace/p6/out/result.json + ckpts/ then: $VASTAI destroy instance $INSTANCE_ID"
    SAVE_POD=1
else
    echo "[OK] all artifacts pulled — destroying instance now (explicit, pre-trap)"
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    SAVE_POD=1  # trap skip (already destroyed explicitly above)
fi

# ── 9) Summary ───────────────────────────────────────────────────────
echo "[9/9] === ${PHASE_ID} DONE ==="
date -u
if [ -f "$LOCAL_DIR/result.json" ]; then
    python3 -c "
import json
with open('$LOCAL_DIR/result.json') as f: d = json.load(f)
t = d.get('training', {}); fa = d.get('falsifier_aggregate', {})
print(f'  wall_ms: {t.get(\"wall_ms\",0)}')
print(f'  steps: {t.get(\"steps_actual\")} cells: {t.get(\"n_cells_init\")}→{t.get(\"n_cells_max\")} (min {t.get(\"n_cells_min\")})')
print(f'  gn2: {t.get(\"gn2_first\"):.4f} → {t.get(\"gn2_last\"):.6f}  (×{t.get(\"gn2_reduction_factor\",0):.1f})')
print(f'  verdict: {fa.get(\"n_pass\")}/{fa.get(\"n_total\")} {fa.get(\"verdict\")}')
for k,v in d.get('falsifiers',{}).items(): print(f'    {k} {v.get(\"name\")}: passed={v.get(\"passed\")}')
"
fi
echo "DONE"
