#!/usr/bin/env bash
# upload_and_fire.sh — run LOCALLY once SSH is up. Uploads job + repo subset +
# R2 creds, then launches remote_run.sh under nohup on the pod. Idempotent.
set -uo pipefail
H=ssh9.vast.ai; P=33460
WT="$(git rev-parse --show-toplevel)"
SSH="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=20 -p $P root@$H"
SCP="scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -P $P"

$SSH 'mkdir -p /workspace/job/repo' || exit 1
# repo subset
$SCP /tmp/mid_job_repo.tgz root@$H:/workspace/job/repo.tgz
$SSH 'cd /workspace/job/repo && tar xzf ../repo.tgz'
# fetch + run scripts
$SCP "$WT/state/mid_convmoe_fire/remote_fetch_corpus.py" root@$H:/workspace/job/remote_fetch_corpus.py
$SCP "$WT/state/mid_convmoe_fire/remote_run.sh" root@$H:/workspace/job/remote_run.sh

# R2 creds + corpus size as env on the pod (written to a sourced file, not argv)
$SSH "cat > /workspace/job/env.sh" <<ENV
export R2_ACCOUNT_ID='$(secret get r2.phanes.account_id)'
export R2_ACCESS_KEY_ID='$(secret get r2.phanes.access_key_id)'
export R2_SECRET_ACCESS_KEY='$(secret get r2.phanes.secret_access_key)'
export R2_BUCKET='$(secret get r2.phanes.bucket)'
export PER_LANG_MB='800'
ENV

# launch under nohup (detached); poll-inline from laptop
$SSH 'cd /workspace/job && source env.sh && nohup bash remote_run.sh > /workspace/mid_fire.log 2>&1 & echo LAUNCHED_PID $!'
echo "FIRE LAUNCHED on $H:$P — poll /workspace/mid_fire.log"
