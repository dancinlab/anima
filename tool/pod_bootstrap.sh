#!/bin/bash
# pod_bootstrap.sh — one-shot vast/runpod pod setup for anima engine-native decode.
# Encapsulates every cloud-rent/transfer pitfall learned 2026-06-21 (hexa-lang ING #71-78):
#   - GB (not MB) for --query cpu_ram          (#71)
#   - verified=false to include cheap big-RAM   (#73)
#   - dph_total<=N in --query (--max-dph ignored) (#72)
#   - mkdir -p remote parent before copy-to      (#75: scp exit 1)
#   - sequential copy-to (concurrent races)       (#76)
#   - long --max-wait-sec for big pods            (#77)
#   - copy-to (not raw rsync over proxy)          (#74)
#   - apt install clang — hexa run needs a C compiler (#79)
#   - export PATH=/root/.hx/bin in non-interactive shells (#80)
#   - setsid+nohup detach for long jobs (proxy SIGHUP)  (#81)
#
# Usage:
#   tool/pod_bootstrap.sh <pod_id> [--hexa edge|stable]
# Rents separately (see header); this sets up an ALREADY-RENTED pod id.
#   rent example (2TB cheap):
#     hexa cloud rent vast --query 'cpu_ram>=2000 verified=false dph_total<=2' --disk 60 --desc '<slug>'
set -uo pipefail
POD="${1:?usage: pod_bootstrap.sh <pod_id> [--hexa edge|stable]}"
HEXA_VER="${3:-edge}"   # $2 is the --hexa flag literal; $3 its value (kept simple)
[ "${2:-}" = "--hexa" ] && HEXA_VER="${3:-edge}"
REPO_LOCAL="/Users/mini/dancinlab/anima"
SLUG="1464_pairing_contrastive_bind"
RROOT="/root/anima"
cd "$REPO_LOCAL" || exit 1

log(){ echo "[$(date +%H:%M:%S)] $*"; }

# 1) hexa install (edge = noop-free farr fix included)
log "1/4 hexa install ($HEXA_VER) on pod $POD ..."
hexa cloud exec "$POD" --provider vast -- \
  "cd /root && setsid bash -c 'curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh | HEXA_VERSION=$HEXA_VER bash >/root/hexa_install.log 2>&1' >/dev/null 2>&1 & echo INSTALL_LAUNCHED"

# 1b) C compiler — hexa run codegens C then invokes clang; base images often lack it (ING #79)
log "1b/5 install clang (hexa run dependency) ..."
hexa cloud exec "$POD" --provider vast -- \
  "export DEBIAN_FRONTEND=noninteractive; apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq clang >/dev/null 2>&1; which clang && clang --version | head -1 || echo CLANG_MISSING"

# 2) remote dirs (mkdir -p BEFORE copy-to → avoids scp exit 1, ING #75)
log "2/4 mkdir remote dirs ..."
hexa cloud exec "$POD" --provider vast -- \
  "mkdir -p $RROOT/core $RROOT/state/$SLUG/bins && echo MKDIR_OK"

# 3) code (core/) via copy-to (proxy-stable, ING #74)
log "3/4 copy core/ ..."
hexa cloud copy-to "$POD" core "$RROOT/core" -r

# 4) bins SEQUENTIALLY with byte-exact verify (ING #76 concurrent-race avoided)
log "4/4 copy bins sequentially (verify byte-exact) ..."
SZ_EXPECT=1213440020
for b in base pairing shuffle; do
  for try in 1 2 3; do
    hexa cloud copy-to "$POD" "state/$SLUG/bins/$b.bin" "$RROOT/state/$SLUG/bins/$b.bin" >/tmp/pb_$b.log 2>&1
    sz=$(hexa cloud exec "$POD" --provider vast -- "stat -c%s $RROOT/state/$SLUG/bins/$b.bin 2>/dev/null||echo 0" 2>/dev/null | grep -oE '^[0-9]+' | head -1)
    [ "$sz" = "$SZ_EXPECT" ] && { log "$b.bin OK"; break; }
    log "$b.bin try$try incomplete sz=$sz"
  done
done
# also push the decode driver + scripts
hexa cloud copy-to "$POD" "state/$SLUG/engine_decode_batch_cli.hexa" "$RROOT/state/$SLUG/engine_decode_batch_cli.hexa" 2>/dev/null
log "BOOTSTRAP_DONE pod=$POD"

# ── DECODE LAUNCH (run AFTER bootstrap, manually) ────────────────────────────
# hexa lives at /root/.hx/bin but is NOT on a non-interactive shell's PATH (ING #80),
# and a foreground `hexa cloud exec` dies on proxy SIGHUP for long jobs (ING #81).
# So: detach with setsid + export PATH, log to a file, then poll.
#   hexa cloud exec "$POD" --provider vast -- \
#     "cd $RROOT; setsid bash -c 'export PATH=/root/.hx/bin:\$PATH; \
#        bash $RROOT/state/$SLUG/run_decode_isolated.sh $RROOT /root/h1464_decode 80 \
#        > /root/h1464_decode/run.log 2>&1' >/dev/null 2>&1 & echo LAUNCHED"
# poll: wc -l /root/h1464_decode/out_*.txt · grep -c ALL_DECODE_DONE run.log · free -g
# A bare-`hexa` script (no PATH) fails silently as 0-output DONE per frag — always
# verify the first frag log has NO 'hexa: command not found'.
