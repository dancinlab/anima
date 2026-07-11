#!/bin/bash
# Re-run agency_T analyze WITH --phi, then combine across 3 sessions.
set -e
cd /Users/mini/dancinlab/anima/.worktrees/h9269-verdict
H=state/h1058_agency_daemon
T=/Users/mini/dancinlab/anima/state/h9269_candidateY/results/pod_harvest
O=/Users/mini/dancinlab/anima/state/h9269_candidateY/results/analysis
for s in B_mnemosyne C_thanatos D_orpheus; do
  lab=${s%%_*}
  echo "### analyze+phi $lab ###"
  PYTHONPATH=cli:core python3 $H/agency_T.py analyze $T/trace_$s.jsonl $O/depths_$lab.jsonl \
     --phi $O/phi_$lab.jsonl --exclude-forced-n3 --label $lab --out $O/result_${lab}_phi.json 2>&1 | grep -vE "^wrote:|reclassified"
  echo
done
echo "======== FROZEN FALSIFIER (3 sessions x 2 macro-maps) ========"
PYTHONPATH=cli:core python3 $H/agency_T.py falsifier $O/result_B_phi.json $O/result_C_phi.json $O/result_D_phi.json
