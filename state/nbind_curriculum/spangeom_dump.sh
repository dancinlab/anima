#!/bin/bash
# spangeom_dump.sh <POD> <HOST> <PORT> — SPAN-GEOM stage-1: dump-hidden base 303M over 1763 span prompts.
set -uo pipefail
POD="$1"; HOST="$2"; PORT="$3"
SP=/private/tmp/claude-501/-Users-mini-dancinlab-anima/f5b1994e-2cff-42cb-9e82-494c5e7d490b/scratchpad
CK=~/anima-weights/nbind_cement
BASE=~/anima-weights/clm303_clean/clm303_clean.clm
NVLIB='/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_runtime/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cuda_nvrtc/lib'
S="scp -P $PORT -o StrictHostKeyChecking=no"

echo "$(date +%H:%M:%S) [SG] setup pod $POD"
timeout 500 hexa cloud exec "$POD" 'mkdir -p /workspace/sg; export PATH=$PATH:$HOME/.local/bin
if ! python3 -m pip --version >/dev/null 2>&1; then python3 -m ensurepip --upgrade 2>/dev/null || { curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/gp.py && python3 /tmp/gp.py 2>&1|tail -1; }; fi
python3 -m pip -q install --break-system-packages "anima-python[train,gpu]" nvidia-cublas-cu12 nvidia-cuda-runtime-cu12 2>&1 | tail -2
AP=$(python3 -c "import anima_py,os;print(os.path.dirname(anima_py.__file__))")
curl -fsSL https://raw.githubusercontent.com/dancinlab/anima/main/cli/evaluate.py -o $AP/cli/evaluate.py
command -v anima-py && echo setup-ok' 2>&1 | grep -vE "^\[cloud\] (resolved|registry)" | tail -3

echo "$(date +%H:%M:%S) [SG] upload base ckpt + prompts(1763)"
$S "$BASE" "root@$HOST:/workspace/sg/base.clm" 2>&1 | tail -1
$S "$SP/spangeom_prompts.json" "root@$HOST:/workspace/sg/spangeom_prompts.json" 2>&1 | tail -1

echo "$(date +%H:%M:%S) [SG] dump-hidden (read-only trunk forward · 1763 prompts · win48)"
FIRE="set -e
export LD_LIBRARY_PATH=$NVLIB:\$LD_LIBRARY_PATH; export PATH=\$PATH:\$HOME/.local/bin; export PYTHONUTF8=1
cd /workspace/sg
stdbuf -oL -eL anima-py evaluate /workspace/sg/base.clm --dump-hidden /workspace/sg/spangeom_prompts.json --out /workspace/sg/spangeom_hidden.npz --win 48 2>&1 | tail -8
ls -la /workspace/sg/spangeom_hidden.npz | awk '{print \$5,\$9}'
echo SG_DUMP_DONE"
timeout 2400 hexa cloud exec "$POD" "$FIRE" 2>&1 | grep -vE "^\[cloud\] (resolved|registry)"
mkdir -p "$CK"
$S "root@$HOST:/workspace/sg/spangeom_hidden.npz" "$CK/spangeom_hidden.npz" 2>&1 | tail -1
echo "$(date +%H:%M:%S) [SG] pulled ($(wc -c <"$CK/spangeom_hidden.npz" 2>/dev/null)B) — running SPAN-GEOM probe"
python3 "$SP/spangeom_probe.py" "$CK/spangeom_hidden.npz" --prompts "$SP/spangeom_prompts.json" --win 48
echo "$(date +%H:%M:%S) SG_COMPLETE POD=$POD"
