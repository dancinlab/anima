#!/bin/bash
# H_9331 BIND-LOCUS on the C4 ckpts — H_9334 의 NEXT 가 지목한 가장 결정적 표적.
#   C4 = 극성이 **연산자 자신의 키**(`{s}지 않다`-계열 담체)로 쓰인 모델 ⇒ H_9334 가 12/12 로
#        "연산자가 그 값을 읽는다"(H-ε TERMINAL)를 확정했다.
#   여기에 인과 주입을 걸면 '자리'와 '키'가 **둘 다** 충족된 상태의 확인이 된다:
#     dep1 ≤ −0.50 (P) → 인터페이스 addressable 을 **읽기 축에서 독립 확증**
#     TOST 등가  (S) → 올바른 자리·올바른 키인데도 무시 ⇒ addressable 해석 **재검토**
set -u
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/root/.local/bin:$PATH
export PYTHONUTF8=1 LC_ALL=C.UTF-8
export OMP_NUM_THREADS=16 OPENBLAS_NUM_THREADS=16 MKL_NUM_THREADS=16 NUMEXPR_NUM_THREADS=16
cd /root
APY=$(command -v anima-py) || { echo "[gate] ❌ anima-py 없음 — 중단"; exit 127; }
for f in swap_c4_s7.clm swap_c4_s11.clm bl_manifest_v2.json; do
  [ -s "$f" ] || { echo "[gate] ❌ $f 없음 — 중단"; exit 1; }
done
echo "[gate] anima-py=$APY · c4_s7 sha=$(sha256sum swap_c4_s7.clm | cut -c1-16) · c4_s11 sha=$(sha256sum swap_c4_s11.clm | cut -c1-16)"
echo "=== BIND-LOCUS C4 s7 ==="
"$APY" evaluate swap_c4_s7.clm --bind-locus bl_manifest_v2.json --out bl_c4_s7.json --win 64 --perm 200 > bl_c4_s7.log 2>&1
echo "  rc=$? device=$(head -1 bl_c4_s7.log | grep -o 'GPU-FIRED\|GPU-FALLBACK')"; grep -E "BIND-LOCUS|l\* FROZEN|INVALID" bl_c4_s7.log | tail -2
echo "=== BIND-LOCUS C4 s11 ==="
"$APY" evaluate swap_c4_s11.clm --bind-locus bl_manifest_v2.json --out bl_c4_s11.json --win 64 --perm 200 > bl_c4_s11.log 2>&1
echo "  rc=$?"; grep -E "BIND-LOCUS|l\* FROZEN|INVALID" bl_c4_s11.log | tail -2
echo "C4_DONE"
