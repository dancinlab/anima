set -u
# ONE script, ONE code version (0.13.47), for every number that enters the verdict.
#
# 0.13.47 is the version that REFUSES to silently truncate an --xbind manifest. The bug it fixes
# already bit this arm: the 240-row held-out manifest was scored on its first 200 rows (n=101/99),
# dropping six whole stems off the end, and nothing in the output said so. Every held-out read below
# therefore passes --n-decode 240 explicitly, and the engine now errors out if that is ever too small.
#
# Gate map, fixed by the corpus census (ground_keep TOUCHES held-out flip0 + SEEN flip1; it OMITS
# SEEN flip0 + held-out flip1):
#   WRITE     held-out flip0  — did the planted fact land?          (touched -> should be HIGH)
#   FORGET    SEEN flip0      — the stratum the corpus NEVER touches = the honest forgetting gate
#                               (H_9327 died gating on a stratum its own corpus reinforced every step)
#   OPERATOR  SEEN flip1      — replayed, so a LIVENESS check, not a forgetting gate (bar 0.75)
#   DV        held-out flip1  — 0/120 of these prompts occur in the corpus (audited). THE QUESTION.
#
# LIE arm: identical budget, opposite planted polarity. If the DV moves the same way in BOTH arms the
# model is reading a surface bias, not the planted fact. This is the control that decided H_9327.
cd $HOME/en_arm; export OMP_NUM_THREADS=4 PYTHONUTF8=1
$HOME/decon/venv/bin/pip install -q --upgrade anima-python 2>&1 | tail -1
A=$HOME/decon/venv/bin/anima-py
V=$($HOME/decon/venv/bin/pip show anima-python 2>/dev/null | awk '/^Version/{print $2}')
echo "=== anima-py $V (판정에 들어가는 모든 숫자가 이 버전에서 나온다) ==="

echo "=== 절단 가드가 살아있는지 확인 (240행을 기본 캡 200 으로 때려본다 — 거부해야 정상) ==="
$A evaluate en_c34_s7_b20k.clm --xbind man_en_held.json --out /tmp/guard_probe.json 2>&1 | grep -m1 "n-decode" \
  && echo "  ✅ 가드 살아있음" || echo "  ⛔ 가드 미발동 — 조사 필요"

echo "=== BASE 재측정 (한 버전 · 전 행) ==="
for B in en_c34_s7_b20k en_c34_s11_b20k; do
  $A evaluate $B.clm --xbind man_en_seen.json --n-decode 240 --out F_v1v2_$B.json > /dev/null 2>&1
  $A evaluate $B.clm --xbind man_en_held.json --n-decode 240 --out F_before_$B.json > /dev/null 2>&1
  echo "  BASE $B rc=$?"
done

echo "=== CPT (6000 @ 2e-4 · 바닥은 KO 에서 이식됨 = floor_transplanted · WRITE 게이트가 판정한다) ==="
for S in 7 11; do
  $A train --arch clm --canon --emax 3 --e0 2 --init en_c34_s${S}_b20k.clm \
     --corpus cpt_ground_keep_en_s${S}.txt --cell-label en-general \
     --steps 6000 --batch-size 8 --seq-len 128 --lr 2e-4 --bf16 --seed $S \
     --out cpt_en_s${S}.clm > cpt_s${S}.log 2>&1
  echo "  CPT_s${S} rc=$? $(ls -la cpt_en_s${S}.clm 2>/dev/null | awk '{print $5}')"
done
$A train --arch clm --canon --emax 3 --e0 2 --init en_c34_s7_b20k.clm \
   --corpus cpt_ground_keep_lie_en_s7.txt --cell-label en-general \
   --steps 6000 --batch-size 8 --seq-len 128 --lr 2e-4 --bf16 --seed 7 \
   --out cpt_en_lie_s7.clm > cpt_lie_s7.log 2>&1
echo "  CPT_LIE_s7 rc=$?"

echo "=== 게이트 4종 (전 행 · 한 버전) ==="
for C in cpt_en_s7 cpt_en_s11 cpt_en_lie_s7; do
  [ -f "$C.clm" ] || { echo "  SKIP $C"; continue; }
  $A evaluate $C.clm --xbind man_en_seen.json --n-decode 240 --out F_post_seen_$C.json > /dev/null 2>&1
  $A evaluate $C.clm --xbind man_en_held.json --n-decode 240 --out F_post_held_$C.json > /dev/null 2>&1
  echo "  EVAL $C done"
done
echo "EN_FINAL_DONE"
