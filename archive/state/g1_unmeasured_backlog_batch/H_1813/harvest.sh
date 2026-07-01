#!/bin/bash
# H_1813 result harvest — run in next session after eval completes
# Usage: bash state/g1_unmeasured_backlog_batch/H_1813/harvest.sh
set -e

POD=43098811
CKDIR="state/g1_unmeasured_backlog_batch/H_1813/ckpt"
LOCAL="state/g1_unmeasured_backlog_batch/H_1813/ckpt"
SSH_CMD="ssh -p 18810 -o StrictHostKeyChecking=no root@ssh1.vast.ai"

echo "=== H_1813 harvest ==="
echo ""

# 1. Check if eval complete
echo "--- 1. Check eval status ---"
hexa cloud exec $POD -- "tail -3 /root/anima/$CKDIR/eval.log 2>/dev/null || echo 'eval.log not found'"
hexa cloud exec $POD -- "tail -3 /root/anima/$CKDIR/aggregate.log 2>/dev/null || echo 'aggregate.log not found'"

echo ""
echo "--- 2. Check ckpt files on pod ---"
hexa cloud exec $POD -- "ls -la /root/anima/$CKDIR/"

echo ""
echo "--- 3. Pull result files (no .clm/.pt) ---"
mkdir -p "$LOCAL"
rsync -az --progress -e "ssh -p 18810 -o StrictHostKeyChecking=no" \
    --include="*.txt" --include="*.json" --include="*.log" --include="*.md" \
    --exclude="*.clm" --exclude="*.pt" \
    root@ssh1.vast.ai:/root/anima/$CKDIR/ "$LOCAL/"

echo ""
echo "--- 4. Show aggregate.log ---"
cat "$LOCAL/aggregate.log" 2>/dev/null || echo "aggregate.log not yet pulled"

echo ""
echo "--- 5. Summary of G0-G6 per arm ---"
for ARM in ctrl tlora; do
    for SEED in 7 4302 4303; do
        TAG="${ARM}_seed${SEED}"
        F="$LOCAL/${TAG}_g0g6.txt"
        if [ -f "$F" ] && [ -s "$F" ]; then
            echo "=== $TAG ==="
            grep -E "(G0|G1|G6|kwr|distinct|fals|PASS|FAIL|closure)" "$F" | head -15
        else
            echo "=== $TAG === MISSING or EMPTY"
        fi
    done
done

echo ""
echo "--- 6. Descent gate results ---"
for ARM in ctrl tlora; do
    for SEED in 7 4302 4303; do
        TAG="${ARM}_seed${SEED}"
        F="$LOCAL/${TAG}_descent.txt"
        if [ -f "$F" ] && [ -s "$F" ]; then
            echo "=== $TAG descent ==="
            grep -E "(model_ce|uniform|shuffle|DESCENT|PASS|FAIL|gap)" "$F" | head -5
        else
            echo "=== $TAG === descent MISSING"
        fi
    done
done

echo ""
echo "=== harvest done ==="
echo "Next: fill in RESULT.md, update H_1813 card + HYPOTHESES.jsonl, pull .clm/.pt to HF, teardown pod."
echo ""
echo "Pull large ckpts before teardown (a_fire_recover_complete):"
echo "  rsync -az --progress -e 'ssh -p 18810 -o StrictHostKeyChecking=no' \\"
echo "    root@ssh1.vast.ai:/root/anima/$CKDIR/*.clm $LOCAL/"
echo "  rsync -az --progress -e 'ssh -p 18810 -o StrictHostKeyChecking=no' \\"
echo "    root@ssh1.vast.ai:/root/anima/$CKDIR/*.pt $LOCAL/"
echo "Teardown: hexa cloud rm $POD"
