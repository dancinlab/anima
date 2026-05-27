#!/usr/bin/env bash
# IonQ Forte-1 task poller - 30-min cap retry per task constraint.
# Polls 4 task ARNs every 3 minutes for max 30 min; downloads results from S3 if COMPLETED.
set -u
export AWS_PROFILE=braket
ROOT="/Users/ghost/core/anima/state/qmirror_chsh_xvendor_2026_05_03"
RAW="$ROOT/raw_results"
LOG="$ROOT/poll_ionq_30min.log"
ANALYZER="$ROOT/analyze.py"

declare -a NAMES=("circuit_a_b" "circuit_a_bprime" "circuit_aprime_b" "circuit_aprime_bprime")
declare -a ARNS=(
  "arn:aws:braket:us-east-1:267673635495:quantum-task/8ce894fd-1eff-49b0-aafc-bbf35a66bd7d"
  "arn:aws:braket:us-east-1:267673635495:quantum-task/d32038b2-cac0-4336-ac92-f5593455ab3f"
  "arn:aws:braket:us-east-1:267673635495:quantum-task/6c0c2f9e-408b-476f-b633-aa5e2dc8e881"
  "arn:aws:braket:us-east-1:267673635495:quantum-task/ccb1d421-5f00-45f4-8e55-887af43377a8"
)
BUCKET="amazon-braket-us-east-1-267673635495"

START_TS=$(date +%s)
MAX_SEC=1800   # 30 min cap
INTERVAL=180   # 3 min

echo "=== IonQ collector RETRY (30min cap) started $(date -u +%FT%TZ) ===" > "$LOG"

ITER=0
while :; do
  ITER=$((ITER+1))
  NOW=$(date +%s)
  ELAPSED=$((NOW - START_TS))
  if [ "$ELAPSED" -ge "$MAX_SEC" ]; then
    echo "$(date -u +%FT%TZ) iter=$ITER ELAPSED=${ELAPSED}s >= ${MAX_SEC}s cap, exit" >> "$LOG"
    break
  fi
  done_count=0
  for i in 0 1 2 3; do
    name="${NAMES[$i]}"
    arn="${ARNS[$i]}"
    out="$RAW/ionq_${name}.json"
    if [ -s "$out" ]; then
      done_count=$((done_count+1))
      continue
    fi
    st=$(aws braket get-quantum-task --quantum-task-arn "$arn" --region us-east-1 --query 'status' --output text 2>>"$LOG")
    echo "$(date -u +%FT%TZ) iter=$ITER elapsed=${ELAPSED}s $name => $st" >> "$LOG"
    if [ "$st" = "COMPLETED" ]; then
      task_id=$(echo "$arn" | awk -F'/' '{print $NF}')
      # Try multiple S3 paths
      aws s3 cp "s3://$BUCKET/tasks/$task_id/results.json" "$out" --region us-east-1 --quiet 2>>"$LOG" || \
      aws s3 cp "s3://$BUCKET/$task_id/results.json" "$out" --region us-east-1 --quiet 2>>"$LOG"
      if [ -s "$out" ]; then
        echo "  downloaded $out" >> "$LOG"
        done_count=$((done_count+1))
      else
        # Last resort: try looking up outputS3 path from task metadata
        meta=$(aws braket get-quantum-task --quantum-task-arn "$arn" --region us-east-1 --output json 2>>"$LOG")
        s3bkt=$(echo "$meta" | /Users/ghost/.hx/bin/python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('outputS3Bucket',''))")
        s3key=$(echo "$meta" | /Users/ghost/.hx/bin/python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('outputS3Directory',''))")
        if [ -n "$s3bkt" ] && [ -n "$s3key" ]; then
          aws s3 cp "s3://$s3bkt/$s3key/results.json" "$out" --region us-east-1 --quiet 2>>"$LOG"
          if [ -s "$out" ]; then
            echo "  downloaded via meta $out" >> "$LOG"
            done_count=$((done_count+1))
          fi
        fi
      fi
    elif [ "$st" = "FAILED" ] || [ "$st" = "CANCELLED" ]; then
      echo "  TERMINAL FAILURE: $st" >> "$LOG"
      done_count=$((done_count+1))
      echo "{\"status\":\"$st\",\"measurements\":[]}" > "$out"
    fi
  done
  /Users/ghost/.hx/bin/python3 "$ANALYZER" >> "$LOG" 2>&1
  if [ $done_count -ge 4 ]; then
    echo "=== all 4 tasks resolved at $(date -u +%FT%TZ) ===" >> "$LOG"
    break
  fi
  sleep "$INTERVAL"
done

# Final analyzer pass
/Users/ghost/.hx/bin/python3 "$ANALYZER" >> "$LOG" 2>&1
echo "=== IonQ collector exit $(date -u +%FT%TZ) iter=$ITER ===" >> "$LOG"
