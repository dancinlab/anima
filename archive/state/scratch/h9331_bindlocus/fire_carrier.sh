#!/bin/bash
# H_9331 캐리어-스팬 swap pedestal — Fable 예측: 캐리어flip>=0.75 ∧ 원자flip<=0.25.
# C4 먼저(H_9334 가독 캐리어결합 보장=pedestal) → n2. --bl-swap-span carrier.
set -u
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/root/.local/bin:$PATH
export PYTHONUTF8=1 LC_ALL=C.UTF-8
export OMP_NUM_THREADS=16 OPENBLAS_NUM_THREADS=16 MKL_NUM_THREADS=16 NUMEXPR_NUM_THREADS=16
cd /root
APY=$(command -v anima-py) || { echo "[gate] anima-py 없음"; exit 127; }
for f in swap_c4_s7.clm swap_c4_s11.clm natem_n2_main_s7.clm natem_n2_main_s11.clm bl_manifest_v2.json; do
  [ -s "$f" ] || { echo "[gate] $f 없음"; exit 1; }
done
echo "[gate] anima-py=$APY ver=$($APY 2>/dev/null|grep -o '0\.[0-9.]*'|head -1)"
run(){ echo "=== CARRIER $1 ==="; "$APY" evaluate "$2" --bind-locus bl_manifest_v2.json --bl-swap-span carrier --out "$3" --win 64 --perm 200 > "${3%.json}.log" 2>&1; echo "  rc=$? dev=$(head -1 "${3%.json}.log"|grep -o 'GPU-FIRED\|GPU-FALLBACK')"; grep -E "swap-span|INVALID|l\* FROZEN|verdict|swap=" "${3%.json}.log"|tail -4; }
run c4_s7  swap_c4_s7.clm       bl_carrier_c4_s7.json
run c4_s11 swap_c4_s11.clm      bl_carrier_c4_s11.json
run n2_s7  natem_n2_main_s7.clm bl_carrier_n2_s7.json
run n2_s11 natem_n2_main_s11.clm bl_carrier_n2_s11.json
echo "CARRIER_DONE"
