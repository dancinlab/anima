#!/bin/bash
# state/hexad_integ_fire_2026_05_16/dispatch.sh — R3 HEXAD integration fire
#
# User directive verbatim: "R3 발사하자 통합 fire" (cost-authorized 2026-05-16).
# Clone of state/clm_v1_fire_2026_05_15/dispatch_h100.sh (proven $0.34 actual
# .clm v1 P2 fire) — g_fire_dispatch_robust hardening kept INTACT:
#   - set -euo pipefail
#   - SAVE_POD auto-promote on result.json present
#   - `|| true` guards between train + pull (set -e false-positive that LOST
#     the cycle-88 ckpt)
#   - scp pull retry ≥3 @ 60s, ConnectTimeout 3600, direct-IP (not proxy)
#   - trap cleanup honoring SAVE_POD; retain pod + print manual recovery on
#     pull fail (never lose the ckpt — cycle-88 lesson)
#
# Sources uploaded:
#   - state/verify_hexad_integ_2026_05_16/integ_harness.py  (SSOT, reused verbatim)
#   - state/hexad_integ_fire_2026_05_16/train_hexad_integ_from_scratch.py (scaler)
#   - training/clm_v1_model.py  (F-V5MIT-2/3 unit-test surface)
# Synthetic byte corpus generated in-trainer (no corpus upload — integration
# scratch fire, NOT a language-quality run).
#
# Cost envelope: ~$1-5 expected, $8 hard stop (CostGuard in trainer enforces
# in-job). Pod auto-destroy unless SAVE_POD=1.

set -euo pipefail

# ── CONFIG ──────────────────────────────────────────────────────────
PHASE_ID="hexad_integ_fire"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_integ_fire_2026_05_16"
ANIMA_ROOT="/Users/ghost/core/anima"
PHASE_LABEL="anima-hexad-integ-fire-r3"

# Scaled spec (matches Mac scaled-smoke F-INTEG 5/5 PASS).
# STEPS 400 (not 3000): the harness C-engine Python-Φ fallback + single-
# batch per-step structure is ~3s/step on a shared cloud CPU at 64-thread
# oversubscription (load-avg thrash). An integration WIRING scratch fire's
# evidence (F-INTEG 1..5 + F-V5MIT-1..3 + F-PRIN3 + CE-descent + mitosis
# n_cells trajectory) is FULLY established at a few hundred steps — the
# verdict logic is loss[-1]<loss[0] + wiring invariants, NOT step-count
# dependent. 400 steps keeps it an honest real cost-bearing fire that
# completes in reasonable wall/cost (honest-stop: no disproportionate
# spend without added evidence value). FIRE_THREADS=16 avoids the 64-core
# oversubscription thrash that froze the 3000-step attempt.
STEPS="${STEPS:-400}"
D_MODEL="${D_MODEL:-512}"
N_LAYER="${N_LAYER:-8}"
MAX_CELLS="${MAX_CELLS:-64}"
SEQ_LEN="${SEQ_LEN:-256}"
SEED="${SEED:-0}"
FIRE_THREADS="${FIRE_THREADS:-16}"

# Cost envelope (user cost-authorized ~$1-5; $8 hard stop)
COST_CAP_USD="${COST_CAP_USD:-8.0}"
COST_PER_HR_MAX="${COST_PER_HR_MAX:-3.0}"
# CPU integration fire ~0.75s/step Mac → ~40min for 3000 steps; 1.0hr est
# with headroom. CostGuard (in-trainer) hard-stops at COST_CAP_USD anyway.
ESTIMATED_WALL_HR="${ESTIMATED_WALL_HR:-1.0}"
ABSOLUTE_MAX_USD=$(python3 -c "print($COST_CAP_USD * 1.10)")

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found at $VASTAI"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
[ -f "$ANIMA_ROOT/state/verify_hexad_integ_2026_05_16/integ_harness.py" ] || {
    echo "ERROR: integ_harness.py SSOT missing"; exit 1; }
[ -f "$LOCAL_DIR/train_hexad_integ_from_scratch.py" ] || {
    echo "ERROR: scaler missing"; exit 1; }
[ -f "$ANIMA_ROOT/training/clm_v1_model.py" ] || {
    echo "ERROR: clm_v1_model.py (F-V5MIT surface) missing"; exit 1; }

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai dispatch (R3, 2026-05-16) ==="
date -u
echo "  steps=$STEPS d_model=$D_MODEL n_layer=$N_LAYER max_cells=$MAX_CELLS seq_len=$SEQ_LEN seed=$SEED"
echo "  cost_cap=\$$COST_CAP_USD absolute_max=\$$ABSOLUTE_MAX_USD per_hr_max=\$$COST_PER_HR_MAX"
echo "  estimated wall ${ESTIMATED_WALL_HR}hr"

# ── 1) GPU offer search (H100 → A100 SXM4 fallback) ──────────────────
echo "[1/9] Searching H100/A100 offers under \$${COST_PER_HR_MAX}/hr ..."
OFFER_JSON=$($VASTAI search offers \
    "gpu_name in [H100_SXM,H100_PCIE,H100_NVL,A100_SXM4,A100_PCIE] num_gpus=1 reliability>0.95 dph_total<${COST_PER_HR_MAX} disk_space>50 inet_down>200" \
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
[ -z "$OFFER_ID" ] && { echo "ERROR: no GPU offer found"; exit 1; }
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU"

# ── 2) Pre-fire cost gate ────────────────────────────────────────────
EST_COST=$(python3 -c "print(round($OFFER_DPH * $ESTIMATED_WALL_HR, 2))")
echo "[2/9] cost gate: est=\$$EST_COST  absolute_max=\$$ABSOLUTE_MAX_USD"
EXCEEDS=$(python3 -c "print('YES' if $EST_COST > $ABSOLUTE_MAX_USD else 'NO')")
if [ "$EXCEEDS" = "YES" ]; then
    echo "[ABORT] est_cost \$$EST_COST exceeds \$$ABSOLUTE_MAX_USD"; exit 1
fi
echo "  ✓ within budget"

# ── 3) Rent instance ─────────────────────────────────────────────────
echo "[3/9] Renting instance..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
    --disk 50 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
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

# ── 4) Wait for SSH ──────────────────────────────────────────────────
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
try: d=json.load(sys.stdin); print(d.get('ssh_host','') or d.get('public_ipaddr',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('ssh_port','') or d.get('direct_port_start',''))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            # ConnectTimeout 25 (not 10): vast.ai key-injection / proxy can
            # lag minutes on some hosts ("auth fails → try again" banner).
            # Patience here avoids false SSH-not-ready aborts (R3 bring-up
            # lesson — one host took 4+ min for authorized_keys).
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o ConnectTimeout=25 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
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

# ── 5) Upload sources (no corpus — synthetic byte input in-trainer) ──
echo "[5/9] Uploading sources..."
$SSH_CMD 'mkdir -p /workspace/anima/state/verify_hexad_integ_2026_05_16 /workspace/anima/state/hexad_integ_fire_2026_05_16 /workspace/anima/training /workspace/anima/output'
$SCP_CMD "$ANIMA_ROOT/state/verify_hexad_integ_2026_05_16/integ_harness.py" "root@$SSH_HOST:/workspace/anima/state/verify_hexad_integ_2026_05_16/"
$SCP_CMD "$LOCAL_DIR/train_hexad_integ_from_scratch.py" "root@$SSH_HOST:/workspace/anima/state/hexad_integ_fire_2026_05_16/"
$SCP_CMD "$ANIMA_ROOT/training/clm_v1_model.py" "root@$SSH_HOST:/workspace/anima/training/"
# integ_harness.py imports a SMALL subset of the ready/ tree:
#   ready/core  (consciousness_engine.py)          ~1 MB
#   ready/models (trinity.py, conscious_decoder.py) ~15 MB
#   ready/anima/hexad (S/W/M/E + constants pkg)     ~112 KB
#   ready/anima/src  (symlink targets: trinity_legacy, perf_hooks, …) ~3 MB
# CRITICAL: ready/core/*.py are SYMLINKS into ready/anima/ (perf_hooks →
# ../anima/core/runtime/perf_hooks.py, archive/trinity_legacy → ../../anima/
# src/archive/...). We tar with -h (dereference) so the REAL file contents
# ship, not dangling links. This pulls symlink TARGETS (tiny .py source) —
# NOT the 33 GB ckpts/data (those are not symlinked from core/models).
echo "[5/9] Uploading ready/ subset (-h deref: core+models+hexad+src ≈19MB; NOT 33GB tree)..."
$SSH_CMD 'mkdir -p /workspace/anima/ready/core /workspace/anima/ready/models /workspace/anima/ready/anima'
tar -C "$ANIMA_ROOT/ready" -h --no-xattrs -czf - core models 2>/dev/null \
  | $SSH_CMD 'tar -C /workspace/anima/ready --warning=no-unknown-keyword -xzf -'
tar -C "$ANIMA_ROOT/ready/anima" -h --no-xattrs -czf - hexad src 2>/dev/null \
  | $SSH_CMD 'tar -C /workspace/anima/ready/anima --warning=no-unknown-keyword -xzf -'
$SSH_CMD 'echo "  ready/ uploaded:"; du -sh /workspace/anima/ready/core /workspace/anima/ready/models /workspace/anima/ready/anima/hexad /workspace/anima/ready/anima/src 2>/dev/null'

# ── 6) GPU + torch + IMPORT sanity (fail fast — no idle GPU bleed) ───
echo "[6/9] GPU + torch + import sanity..."
$SSH_CMD 'python3 -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"' | head -3
# integ_harness.py uses ANIMA_ROOT=/Users/ghost/core/anima hard-paths; on the
# remote we symlink that path to /workspace/anima so the SSOT import resolves.
# numpy is a HARD import in consciousness_engine.py + trinity.py — the fresh
# pytorch:2.5.1 image lacks it. Install robustly (PEP 668 --break-system-
# packages per H100 orchestrator gotcha) + verify before the import gate.
$SSH_CMD 'mkdir -p /Users/ghost/core && ln -sfn /workspace/anima /Users/ghost/core/anima'
echo "  installing numpy on remote (--break-system-packages, verified)..."
$SSH_CMD 'pip install --quiet --break-system-packages numpy 2>&1 | tail -1 || pip install --quiet numpy 2>&1 | tail -1 || true'
NP_OK=$($SSH_CMD 'python3 -c "import numpy; print(\"NUMPY\"+numpy.__version__)" 2>&1' | tail -1)
echo "  remote numpy: $NP_OK"
if ! echo "$NP_OK" | grep -q "NUMPY"; then
    echo "[ABORT] remote numpy unavailable ($NP_OK) — not firing GPU (no idle bleed)."
    exit 1
fi
# Hard import gate — if the needed modules do not import, ABORT before
# burning GPU compute time (cycle-88 lesson: never burn idle GPU on a
# pipeline that will ImportError 30s into training). FULL probe output is
# captured to the log (no `tail -1` swallow) for diagnosability.
echo "  --- remote import probe (full output) ---"
$SSH_CMD 'cd /workspace/anima && python3 -c "
import sys
sys.path[:0]=[\"ready/core\",\"ready/anima\",\"ready\",\"ready/models\"]
from trinity import ThalamicBridge
from consciousness_engine import ConsciousnessC
from hexad.s.emergent_s import EmergentS
from hexad.w.emergent_w import EmergentW
from hexad.m.emergent_m import EmergentM
from hexad.e.emergent_e import EmergentE
from hexad.constants import PSI_BALANCE, PSI_COUPLING, GATE_TRAIN, GATE_INFER
from conscious_decoder import ConsciousDecoderV2
print(\"IMPORT_GATE_OK\")
" 2>&1' > "$LOCAL_DIR/import_probe.out" 2>&1 || true
cat "$LOCAL_DIR/import_probe.out"
echo "  --- end probe ---"
if ! grep -q "IMPORT_GATE_OK" "$LOCAL_DIR/import_probe.out"; then
    echo "[ABORT] remote import gate FAILED — not firing GPU (no idle bleed)."
    echo "        full probe output above ($LOCAL_DIR/import_probe.out). Pod destroyed by trap."
    exit 1
fi
echo "  ✓ all integration modules import on remote"

# ── 7) Train (scaled R3 fire) ────────────────────────────────────────
# integ_harness is single-device-by-design (CPU): C-engine rust/python +
# EmergentS/M intertwine with D+Bridge via the φ(6)=2 .detach() barrier.
# We run the integration scratch fire on the rented box's CPU (the GPU
# box has many CPU cores; ~same $/hr; zero device-shim risk; EXACT code
# path the Mac scaled-smoke proved 5/5). --threads uses all cores.
NPROC=$($SSH_CMD 'nproc 2>/dev/null || echo 8' | tail -1)
echo "  remote nproc=$NPROC — running CPU-coherent integration fire @ ${FIRE_THREADS}t (no oversubscription)"
echo "[7/9] Firing R3 ($STEPS steps d=$D_MODEL L=$N_LAYER cells→$MAX_CELLS ctx=$SEQ_LEN, CPU ${FIRE_THREADS}t)..."
$SSH_CMD "cd /workspace/anima && export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=$FIRE_THREADS MKL_NUM_THREADS=$FIRE_THREADS && python3 state/hexad_integ_fire_2026_05_16/train_hexad_integ_from_scratch.py \
    --scale \
    --steps $STEPS \
    --d-model $D_MODEL \
    --n-layer $N_LAYER \
    --max-cells $MAX_CELLS \
    --seq-len $SEQ_LEN \
    --seed $SEED \
    --threads $FIRE_THREADS \
    --out /workspace/anima/output \
    --cost-cap-usd $COST_CAP_USD \
    --cost-per-hr $OFFER_DPH \
    --estimated-wall-hr $ESTIMATED_WALL_HR 2>&1 | tee train.log" 2>&1 | tee dispatch.log || true
# g_fire_dispatch_robust: `|| true` neutralizes set -e false-positive
# (SSH pipe spurious exit 1 destroyed ckpt in cycle 88).

TRAIN_EXIT=${PIPESTATUS[0]:-0}
echo "  train exit code = $TRAIN_EXIT"

# ── 8) Pull artifacts (g_fire_dispatch_robust) ───────────────────────
echo "[8/9] Verifying result.json on remote + SAVE_POD auto-promote..."
SAVED=$($SSH_CMD 'test -f /workspace/anima/output/result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
    echo "  ✓ result.json exists on remote — SAVE_POD=1 auto-promote (ckpt protected until pulled)"
    SAVE_POD=1
else
    echo "  ⚠ result.json NOT found — training may have failed (still SAVE_POD=1 for inspection)"
    SAVE_POD=1
fi

mkdir -p "$LOCAL_DIR/ckpts"
echo "[8/9] Pull artifacts (retry ≥3, 60s interval)..."
pull_with_retry() {
    local src="$1" dst="$2" tries=0
    while [ $tries -lt 3 ]; do
        if $SCP_CMD "root@$SSH_HOST:$src" "$dst" 2>&1; then
            echo "  ✓ pulled $src (try $((tries+1)))"
            return 0
        fi
        tries=$((tries+1))
        echo "  ... pull retry $tries/3 for $src"
        [ $tries -lt 3 ] && sleep 60
    done
    echo "  ✗ pull FAILED after 3 tries: $src"
    return 1
}
PULL_OK=1
pull_with_retry "/workspace/anima/output/ckpts/ckpt_hexad_integ_final.pt" "$LOCAL_DIR/ckpts/ckpt_${PHASE_ID}_final.pt" || PULL_OK=0
pull_with_retry "/workspace/anima/output/result.json" "$LOCAL_DIR/result.json" || PULL_OK=0
pull_with_retry "/workspace/anima/train.log" "$LOCAL_DIR/train.log" || PULL_OK=0

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — pod RETAINED (SAVE_POD=1)"
    echo "[WARN] manual recovery: ssh -i $VAST_SSH_KEY -p $SSH_PORT root@$SSH_HOST"
    echo "[WARN] then scp /workspace/anima/output/ckpts/ckpt_hexad_integ_final.pt + result.json locally + destroy instance $INSTANCE_ID"
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
print(f'  wall: {t.get(\"wall_hours\",0):.4f}hr ({t.get(\"wall_seconds\",0):.1f}s)')
print(f'  cost: \${t.get(\"cost_usd_actual\",0):.4f}')
print(f'  steps: {t.get(\"steps_actual\")} cells: {t.get(\"n_cells_init\")}→{t.get(\"n_cells_final\")} (max {t.get(\"n_cells_max\")})')
print(f'  loss: {t.get(\"loss_initial_avg100\"):.4f} → {t.get(\"loss_final_avg100\"):.4f}  (×{t.get(\"ce_reduction_factor\",0):.3f})')
print(f'  phi_best: {t.get(\"phi_best\",0):.4f}')
print(f'  ckpt: {t.get(\"ckpt_bytes\",0):,} bytes')
print(f'  verdict: {fa.get(\"n_pass\")}/{fa.get(\"n_total\")} {fa.get(\"verdict\")} (F-INTEG {fa.get(\"f_integ_pass\")}/5)')
for fid in ['F-INTEG-1','F-INTEG-2','F-INTEG-3','F-INTEG-4','F-INTEG-5','F-V5MIT-1','F-V5MIT-2','F-V5MIT-3','F-PRIN3']:
    f = d.get('falsifiers',{}).get(fid,{}); print(f'    {fid}: passed={f.get(\"passed\")}')
"
fi
echo "DONE"
