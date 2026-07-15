#!/bin/bash
# H_9331 결정 통제 — same-class donor swap (극성-무관). Fable frozen 표:
#   same≈cross≈0.50 → (B) swap-patch 국소화불가 STOP · same≈0 → (A) multi-site.
# n2 s7 (cross=0.50 peak) + C4 s7 (cross=0.35), 카레이어 스팬.
set -u
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/root/.local/bin:$PATH
export PYTHONUTF8=1 LC_ALL=C.UTF-8 OMP_NUM_THREADS=16 OPENBLAS_NUM_THREADS=16 MKL_NUM_THREADS=16
cd /root
APY=$(command -v anima-py) || { echo "no anima-py"; exit 127; }
echo "[gate] ver=$(pip show anima-python 2>/dev/null|grep -i version)"
run(){ echo "=== SAME-CLASS $1 ($2) ==="; "$APY" evaluate "$2" --bind-locus bl_manifest_v2.json --bl-swap-span carrier --bl-swap-donor-class same --out "$3" --win 64 --perm 200 > "${3%.json}.log" 2>&1; echo "  rc=$?"; python3 -c "import json;d=json.load(open('$3'));sa=d.get('stageA') or [];print('  verdict=%s donor=%s maxswap=%.3f'%(d.get('verdict'),d.get('donor_class'),max([r.get('swap',0) for r in sa],default=0)))"; }
run n2_s7 natem_n2_main_s7.clm bl_same_n2_s7.json
run c4_s7 swap_c4_s7.clm       bl_same_c4_s7.json
echo "CONTROL_DONE"
