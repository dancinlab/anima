#!/bin/bash
# H_1464 engine-native decode on mini CPU (byte-faithful native-GEMM core/bytegpt_decode).
# 3 bins (pairing / shuffle / base) x 30 fragments (jobs.tsv) x gen110, top_k40 temp0.7
# (matches gauge_lib._decode defaults). Runs the 3 in parallel, commit-early per fragment.
set -u
cd /Users/mini/dancinlab/anima
D=state/1464_pairing_contrastive_bind
B=$D/bins
J=$D/jobs.tsv
O=/tmp/h1464_decode
mkdir -p "$O"
GEN=110; TOPK=40; TEMP=700
run() {
  local bin=$1 out=$2 log=$3
  rm -f "$out"
  nohup hexa run "$D/engine_decode_batch_cli.hexa" -- "$bin" "$J" "$out" "$GEN" "$TOPK" "$TEMP" \
    > "$log" 2>&1 < /dev/null &
  echo "LAUNCHED $bin -> $out (pid $!)"
}
run "$B/pairing.bin" "$O/out_pairing.txt" "$O/log_pairing.txt"
run "$B/shuffle.bin" "$O/out_shuffle.txt" "$O/log_shuffle.txt"
run "$B/base.bin"    "$O/out_base.txt"    "$O/log_base.txt"
echo "ALL_3_LAUNCHED"
