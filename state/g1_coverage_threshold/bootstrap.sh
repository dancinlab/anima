#!/usr/bin/env bash
# H_1824 pod bootstrap — run from the worktree root on the LOCAL mac.
#   bash state/g1_coverage_threshold/bootstrap.sh <SSH_HOST> <SSH_PORT>
# rsyncs the self-contained payload (core/ cli/ train/clm/model + clean corpus +
# variants + lane scripts) to ~/anima on the pod, installs torch deps if missing,
# then kicks the smoke phase. Idempotent.
set -uo pipefail
HOST="${1:?ssh host}"; PORT="${2:?ssh port}"
SSH="ssh -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@$HOST"
RSYNC_E="ssh -p $PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "=== [bootstrap] mkdir remote tree ==="
$SSH 'mkdir -p ~/anima/state/clm303_clean_corpus ~/anima/state/g1_coverage_threshold'

echo "=== [bootstrap] rsync payload ==="
rsync -az -e "$RSYNC_E" core/ "root@$HOST:~/anima/core/"
rsync -az -e "$RSYNC_E" cli/ "root@$HOST:~/anima/cli/"
rsync -az -e "$RSYNC_E" --relative train/./clm/model/ "root@$HOST:~/anima/train/"
rsync -az -e "$RSYNC_E" state/clm303_clean_corpus/ "root@$HOST:~/anima/state/clm303_clean_corpus/"
rsync -az -e "$RSYNC_E" state/g1_coverage_threshold/ "root@$HOST:~/anima/state/g1_coverage_threshold/"

echo "=== [bootstrap] torch presence ==="
$SSH 'python3 -c "import torch;print(\"torch\",torch.__version__,\"cuda\",torch.cuda.is_available(),torch.cuda.device_count())" 2>&1 || pip install -q torch numpy'

echo "=== [bootstrap] SMOKE ==="
$SSH 'cd ~/anima && bash state/g1_coverage_threshold/run_pod.sh smoke 2>&1 | tail -25'
echo "=== [bootstrap] DONE — to fire: ssh then nohup run_pod.sh all ==="
