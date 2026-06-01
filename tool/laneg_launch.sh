#!/usr/bin/env bash
# robust on-pod launcher — kills any stale fire, wipes the log, starts the
# d768 CUDA fire fully detached (setsid+nohup) so an SSH channel close mid-call
# never aborts it. Idempotent: re-running relaunches clean.
pkill -f laneg_d768_cuda_fire 2>/dev/null
pkill -f 'hexa run' 2>/dev/null
sleep 1
rm -f /workspace/laneg_fire.log
rm -rf /workspace/laneg_d768
chmod +x /workspace/laneg_d768_cuda_fire.sh
cd /workspace
setsid nohup bash /workspace/laneg_d768_cuda_fire.sh '' 768 12 2 16 > /workspace/laneg_fire.log 2>&1 < /dev/null &
echo "LAUNCHED pid=$!"
