#!/bin/bash
# dispatch_ubu.sh — T2 real-scale d_train5 fire on ubu (owned machine, ~$0).
# Ships the d_train{2,3,4,5}_lib chain + real-scale fire entrypoint to ubu
# with import paths rewritten Mac→ubu, builds compiled-native, runs, pulls
# result. g_fire_autonomous: autonomous, no gate. g_fire_dispatch_robust:
# result captured to log + json before any cleanup (ubu is persistent — no
# instance destruction risk; pull is just scp-back of the log/json).
set -u
WT="/Users/ghost/core/anima/.claude/worktrees/agent-aa607aeba3ef838ab"
HEXAD_D="$WT/HEXAD/D"
FIRE_DIR="$WT/state/d_train5_t2_fire_2026_05_16"
UBU_ROOT="/home/aiden/anima_t2_fire"
UBU_LIB="$UBU_ROOT/HEXAD/D"
MAC_IMPORT="/Users/ghost/core/anima/HEXAD/D"

echo "=== T2 real-scale fire dispatch → ubu ($(date -u +%FT%TZ)) ==="

# 1. stage lib chain + fire entry with ubu-resolvable import paths
TMP=$(mktemp -d)
mkdir -p "$TMP/lib"
for f in d_train_lib d_train2_lib d_train3_lib d_train4_lib d_train5_lib; do
  sed "s#${MAC_IMPORT}#${UBU_LIB}#g" "$HEXAD_D/$f.hexa" > "$TMP/lib/$f.hexa"
done
sed "s#__LIBPATH__#${UBU_LIB}#g" "$FIRE_DIR/d_train5_real_fire.hexa" \
  > "$TMP/d_train5_real_fire.hexa"

# 2. push to ubu
ssh -o ConnectTimeout=10 ubu "mkdir -p $UBU_LIB" || { echo "ssh fail"; exit 2; }
scp -q "$TMP"/lib/*.hexa ubu:"$UBU_LIB/" || { echo "scp lib fail"; exit 2; }
scp -q "$TMP/d_train5_real_fire.hexa" ubu:"$UBU_ROOT/" || { echo "scp fire fail"; exit 2; }

# 3. build compiled-native + run on ubu (HEXA_MAC_BUILD_OK gate not needed on
#    Linux; this is the real-scale heavy build the Mac gate explicitly defers)
ssh -o ConnectTimeout=10 ubu bash -lc "'
set -e
cd $UBU_ROOT
echo \"[ubu] hexa \$(~/.hx/bin/hexa --version)\"
echo \"[ubu] building d_train5_real_fire.hexa (real-scale d=768·12L) ...\"
t0=\$(date +%s)
~/.hx/bin/hexa build d_train5_real_fire.hexa -o /tmp/d5fire 2>/tmp/d5fire_build.log \
  && echo \"[ubu] build OK\" || { echo \"[ubu] BUILD FAIL\"; grep -iE \"error:|redefinition\" /tmp/d5fire_build.log | head; exit 3; }
echo \"[ubu] running fire ...\"
HEXA_MEM_UNLIMITED=1 timeout 5400 /tmp/d5fire 2>&1 | tee /tmp/d5fire_run.log
rc=\${PIPESTATUS[0]}
t1=\$(date +%s)
echo \"[ubu] fire rc=\$rc wall=\$((t1-t0))s\"
'" 2>&1 | tee "$FIRE_DIR/dispatch_ubu_run.log"

# 4. pull result log back (g_fire_dispatch_robust: result captured locally)
scp -q ubu:/tmp/d5fire_run.log "$FIRE_DIR/d5fire_run.log" 2>/dev/null || true
echo "=== dispatch done; logs in $FIRE_DIR ==="
rm -rf "$TMP"
