#!/usr/bin/env bash
# Pull campaign artifacts from the pod before teardown (a_fire_recover_complete).
# usage: harvest.sh <ssh-host> <ssh-port> [<dest>]
set -eu
HOST="$1"; PORT="${2:-22}"
DEST="${3:-$HOME/anima-weights/binding_dynamics_mouths}"
mkdir -p "$DEST"
SSHO="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT"
# pull .clm (engine-checkable), summaries, all logs. .pt (1.5GB each) = pull at least
# one representative per mouth if space allows; logs/.clm are the must-haves.
rsync -avz -e "ssh $SSHO" "$HOST:~/anima/state/binding_dynamics_mouths/_run/" "$DEST/_run/" \
  --include="*.clm" --include="*.summary.json" --include="*.log" \
  --include="*/" --exclude="*.pt"
echo "=== harvested -> $DEST/_run (clm + summaries + logs; .pt skipped) ==="
ls -la "$DEST/_run" | head -40
