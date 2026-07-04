#!/usr/bin/env bash
# One-shot bootstrap for the r3 pod: wait ssh -> push -> HF pull h1129 -> launch sweep.
SP=/private/tmp/claude-501/-Users-mini-dancinlab-anima/a1a1adf6-9373-4338-9ac2-15fadbeffce4/scratchpad
cd /Users/mini/dancinlab/anima
PID=${1:?pod-id}
HOST=${2:?ssh-host}; PORT=${3:?ssh-port}
ex(){ timeout ${1:-60} hexa cloud exec $HOST --port $PORT --insecure -- "$2" 2>&1; }
cp(){ timeout ${3:-150} hexa cloud copy-to $HOST "$1" "$2" --port $PORT --insecure 2>&1; }

echo "[bs] waiting for ssh ready..."
i=0
while [ $i -lt 45 ]; do
  R=$(ex 30 "echo READY; nvidia-smi --query-gpu=name --format=csv,noheader")
  echo "$R" | grep -q READY && { echo "[bs] SSH READY (try $i): $(echo "$R"|grep -A1 READY|tail -1)"; break; }
  i=$((i+1)); sleep 20
done
[ $i -ge 45 ] && { echo "[bs] NEVER_READY"; exit 1; }

echo "[bs] mkdir + push token+bundle"
ex 40 "mkdir -p ~/g1robust"
for a in 1 2 3; do cp "$SP/hftok" "/root/g1robust/.hftok" 90 | tail -1; cp "$SP/bundle.tgz" "/root/g1robust/bundle.tgz" 120 | tail -1
  OK=$(ex 40 "cd ~/g1robust && md5sum bundle.tgz 2>/dev/null | cut -d' ' -f1")
  echo "[bs] bundle md5 on pod: $OK (want cba43b3d85ff073c82fc90d0ad9405c3)"
  echo "$OK" | grep -q cba43b3d85ff073c82fc90d0ad9405c3 && break; sleep 5
done

echo "[bs] extract + deps + HF pull + launch"
ex 240 "cd ~/g1robust && rm -rf bundle && tar -xzf bundle.tgz && grep -c STEPS bundle/run_all.sh && pip install -q huggingface_hub hf_transfer 2>&1 | tail -1; python3 -c 'import hf_transfer;print(\"hf_transfer\",hf_transfer.__version__)' 2>&1 | tail -1; echo DEPS_OK"
# HF pull h1129 (fast on this host) + then launch sweep, all nohup on pod
ex 60 'cat > ~/g1robust/launch.sh <<"LEOF"
#!/usr/bin/env bash
cd ~/g1robust
echo "[launch] HF pull h1129 (hf_transfer) $(date)"
rm -rf .cache/huggingface h1129.bin
HF_HUB_ENABLE_HF_TRANSFER=1 python3 -c "from huggingface_hub import hf_hub_download; hf_hub_download(\"dancinlab/anima-bytegpt-303m-h1129\",\"h1129.bin\",local_dir=\"/root/g1robust\",token=open(\"/root/g1robust/.hftok\").read().strip())" > hfdl.log 2>&1
SZ=$(stat -c%s h1129.bin 2>/dev/null || echo 0)
echo "[launch] h1129 size=$SZ"
[ "$SZ" -lt 1200000000 ] && { echo "[launch] H1129_BAD"; tail -5 hfdl.log; exit 1; }
export ROOT=$HOME/g1robust H1129=$HOME/g1robust/h1129.bin
echo "[launch] run_all start $(date)"
bash ~/g1robust/bundle/run_all.sh
echo "[launch] run_all done rc=$? $(date)"
LEOF
chmod +x ~/g1robust/launch.sh && nohup bash ~/g1robust/launch.sh > drive.log 2>&1 & echo LAUNCHED $!'
sleep 8
echo "[bs] drive.log head:"; ex 40 "tail -4 ~/g1robust/drive.log 2>/dev/null; du -sh ~/g1robust/.cache/huggingface 2>/dev/null"
echo "[bs] DONE_BOOTSTRAP endpoint=$HOST:$PORT pid=$PID"
