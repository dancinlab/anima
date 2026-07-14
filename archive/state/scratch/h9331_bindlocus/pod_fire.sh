#!/bin/bash
# H_9330 (2 arm 순차) → H_9331 BIND-LOCUS (s7 → s11 순차)
#   ⚠️ rc=127 재발방지: setsid 비대화형 셸은 PATH 가 최소다 ⇒ anima-py 를 절대경로로 못박고,
#      시작 전에 존재를 하드게이트한다 ("명령 없음"이 조용히 rc=127 로 흘러가면 ALL_DONE 껍데기가 남는다).
#   self-kill-own-fire-1 : 절대 kill 하지 않는다 · many-core 스레드 캡
set -u
export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/root/.local/bin:$PATH
export PYTHONUTF8=1 LC_ALL=C.UTF-8
export OMP_NUM_THREADS=16 OPENBLAS_NUM_THREADS=16 MKL_NUM_THREADS=16 NUMEXPR_NUM_THREADS=16
cd /root

APY=$(command -v anima-py || true)
[ -n "$APY" ] || { echo "[gate] ❌ anima-py 없음 (PATH=$PATH) — 발사 중단"; exit 127; }
echo "[gate] anima-py = $APY"
"$APY" 2>/dev/null | head -1 || { echo "[gate] ❌ anima-py 실행 실패 — 발사 중단"; exit 127; }
for f in py303.clm natem_n2_main_s7.clm natem_n2_main_s11.clm valence_k182.json valence_k182_tail.json bl_manifest_v2.json; do
  [ -s "$f" ] || { echo "[gate] ❌ $f 없음 — 발사 중단"; exit 1; }
done
echo "[gate] py303 sha=$(sha256sum py303.clm | cut -c1-16)"
echo "[gate] s7    sha=$(sha256sum natem_n2_main_s7.clm | cut -c1-16)"
echo "[gate] s11   sha=$(sha256sum natem_n2_main_s11.clm | cut -c1-16)"
echo "[gate] nproc=$(nproc) threads=16 · GATE PASS"

echo "=== H_9330 ARM 1/2 (tail · 읽는 자리를 한 칸 뒤로) ==="
"$APY" evaluate py303.clm --valence-audit valence_k182_tail.json --out h9330_tail.json --win 64 --perm 200 > h9330_tail.log 2>&1
echo "  rc=$? device=$(head -1 h9330_tail.log | grep -o 'GPU-FIRED\|GPU-FALLBACK')"
echo "=== H_9330 ARM 2/2 (base · AUDIT-A 재현) ==="
"$APY" evaluate py303.clm --valence-audit valence_k182.json --out h9330_base.json --win 64 --perm 200 > h9330_base.log 2>&1
echo "  rc=$?"
echo "H9330_DONE"

echo "=== H_9331 BIND-LOCUS s7 ==="
"$APY" evaluate natem_n2_main_s7.clm --bind-locus bl_manifest_v2.json --out bl_s7.json --win 64 --perm 200 > bl_s7.log 2>&1
echo "  rc=$?"; grep -E "BIND-LOCUS|l\* FROZEN|INVALID" bl_s7.log | tail -2
echo "=== H_9331 BIND-LOCUS s11 ==="
"$APY" evaluate natem_n2_main_s11.clm --bind-locus bl_manifest_v2.json --out bl_s11.json --win 64 --perm 200 > bl_s11.log 2>&1
echo "  rc=$?"; grep -E "BIND-LOCUS|l\* FROZEN|INVALID" bl_s11.log | tail -2
echo "ALL_DONE"
