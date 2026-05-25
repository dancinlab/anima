#!/usr/bin/env bash
# lan_boot.sh — anima SUB_ENGINES/AKIDA pack 의 LAN deploy wrapper
# Usage: ./lan_boot.sh <host> [--days N-M] [--install] [--dry-run]
#   host: pool roster name (e.g. pi5-akida)
#   --days N-M: BOOT.sh args (default: 1 7)
#   --install: INSTALL.sh only
#   --dry-run: echo only
#
# constitution Principle I 정합: pool 의 generic primitive (pool on <host>) 위에
# anima-specific knowledge (SUB_ENGINES/AKIDA path + BOOT.sh args) 를 얹는 wrapper.

set -eu

if [ $# -lt 1 ]; then
    echo "Usage: ./lan_boot.sh <host> [--days N-M] [--install] [--dry-run]"
    exit 1
fi

HOST="$1"
shift
DAYS="1 7"
MODE="boot"
DRY=0

while [ $# -gt 0 ]; do
    case "$1" in
        --days) DAYS="$(echo "$2" | tr '-' ' ')"; shift 2 ;;
        --install) MODE="install"; shift ;;
        --dry-run) DRY=1; shift ;;
        *) echo "unknown arg: $1"; exit 1 ;;
    esac
done

# pre-flight: pack 디렉터리 확인 (anima/SUB_ENGINES/AKIDA on remote host)
if ! pool on "$HOST" 'test -d ~/anima/SUB_ENGINES/AKIDA' 2>/dev/null; then
    echo "ERROR: ~/anima/SUB_ENGINES/AKIDA not found on $HOST"
    echo "  -> ssh $HOST 'git clone https://github.com/dancinlab/anima ~/anima' first"
    exit 1
fi

# dispatch
case "$MODE" in
    install)
        CMD='cd ~/anima/SUB_ENGINES/AKIDA && ./INSTALL.sh' ;;
    boot)
        CMD="cd ~/anima/SUB_ENGINES/AKIDA && ./BOOT.sh $DAYS" ;;
esac

if [ "$DRY" = 1 ]; then
    echo "DRY: pool on $HOST '$CMD'"
else
    pool on "$HOST" "$CMD"
fi
