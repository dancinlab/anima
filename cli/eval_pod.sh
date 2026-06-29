#!/usr/bin/env bash
# cli/eval_pod.sh — anima 엔진-네이티브 eval 을 fresh GPU pod 에서 한 명령으로 발사.
#
# WHY: GPU pod 는 휘발이라 `anima eval <ckpt>` (core/g_gates G0-G6 · Ψ=½ · G5 · savant SI)
#      을 돌릴 때마다 import-closure 를 손으로 push 하는 고고학을 반복하게 된다. 이 스크립트가
#      그 절차(번들→push→추출→detached 발사→회수)를 박제한다. SSOT 설명 = state/clm303_clean_corpus/EVAL_KIT.md.
#
# 전제: `hexa cloud` 로 렌트한 live pod 이 있고 hexa stable ≥ v0.311.0 (farr 누수 fix) 가 깔려 있어야 한다.
#       (없으면 --bootstrap 으로 설치. 렌트 자체는 `hexa cloud rent vast --gpu A40 --image
#        nvidia/cuda:12.4.1-devel-ubuntu22.04 --disk 40` 로 먼저 — provisioning 실패 시 다른 offer 재시도.)
#
# Usage:
#   cli/eval_pod.sh <pod_id> [clm_path] [--bootstrap] [--gen N] [--harvest <local_out>]
#
# Examples:
#   cli/eval_pod.sh 42403448                                  # clm303_clean 기본, --gen 5
#   cli/eval_pod.sh 42403448 ~/anima-weights/foo/foo.clm --gen 3
#   cli/eval_pod.sh 42403448 --bootstrap --harvest state/clm303_clean_corpus/engine_eval.txt
#
# 발사 후 eval 은 pod 의 /root/anima/eval_out.txt 에 detached 로 쓰인다(수십분, glue-bound).
#   진행:  hexa cloud exec <pod> -- "tail -20 /root/anima/eval_out.txt"
#   회수:  hexa cloud copy-from <pod> /root/anima/eval_out.txt <local>
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- args ---
POD="${1:?usage: eval_pod.sh <pod_id> [clm_path] [--bootstrap] [--gen N] [--harvest <out>]}"; shift
CLM_LOCAL="$HOME/anima-weights/clm303_clean/clm303_clean.clm"
GEN=5
BOOTSTRAP=0
HARVEST=""
while [ $# -gt 0 ]; do
  case "$1" in
    --bootstrap) BOOTSTRAP=1; shift ;;
    --gen) GEN="$2"; shift 2 ;;
    --harvest) HARVEST="$2"; shift 2 ;;
    -*) echo "unknown flag: $1" >&2; exit 2 ;;
    *) CLM_LOCAL="$1"; shift ;;
  esac
done
CLM_NAME="$(basename "$CLM_LOCAL")"
[ -f "$CLM_LOCAL" ] || { echo "ckpt not found: $CLM_LOCAL" >&2; exit 1; }

# --- import-closure lane dirs (core/*.hexa + cli/anima.hexa imports; core/cli/stdlib excluded) ---
# 도출: grep -rhoE 'import "[^"]+"' core/*.hexa cli/anima.hexa | sed -E 's/import "//;s/"//' \
#        | awk -F/ 'NF>1{print $1}' | sort -u | grep -vE '^(core|cli|stdlib)$'
# 리터럴로 나열한다 — zsh 는 unquoted $VAR 를 word-split 하지 않아 변수로 넘기면 find 가 깨진다.
LANE_LIST="/tmp/anima_eval_lanes.$$.txt"
find AESTHETIC BRAIN BRIDGE CHANNEL DREAM EMBODIMENT HEXAD HIVE-MIND \
     INTENT METACOG NARRATIVE OTHER-MIND SAVANT TIME WAKE \
     -name '*.hexa' > "$LANE_LIST"
N_LANE="$(wc -l < "$LANE_LIST" | tr -d ' ')"
[ "$N_LANE" -ge 100 ] || { echo "lane .hexa count too low ($N_LANE) — wrong cwd?" >&2; exit 1; }
TGZ="/tmp/anima_bundle.$$.tgz"
# core/ + cli/ + lane .hexa in ONE tarball. A single tar transfer is robust where
# `copy-to <dir> --recursive` is NOT: scp -r retries nest core/core and can land a
# partial tree (e.g. 127/332 .hexa at top, the rest stranded in core/core).
tar czf "$TGZ" -T "$LANE_LIST" core cli
echo "[eval_pod] bundle: core/ + cli/ + $N_LANE lane .hexa, $(du -h "$TGZ" | cut -f1)"

# --- optional: install hexa stable (farr-fixed) ---
if [ "$BOOTSTRAP" = 1 ]; then
  echo "[eval_pod] bootstrap hexa stable on pod $POD ..."
  hexa cloud bootstrap "$POD" --hexa stable
fi

# --- push bundle + ckpt (single tarball each; no scp -r recursion) ---
echo "[eval_pod] push bundle + ckpt → pod $POD ..."
hexa cloud copy-to "$POD" "$TGZ" /root/anima/anima_bundle.tgz
hexa cloud copy-to "$POD" "$CLM_LOCAL" "/root/anima/$CLM_NAME"

# --- clean target, extract bundle (core/ cli/ lanes), de-nest, FAIL-LOUD sanity ---
# Aborts (set -e propagates the remote exit) on every trap this script was built to kill:
#   ① stale source — core/g_gates.hexa missing OR cli/anima.hexa has no `eval` subcommand
#      (the bug where a stale main-repo checkout ran the consciousness daemon with ckpt=eval).
#   ④ lane closure — SAVANT/savant_lib.hexa missing ([module_loader] FATAL).
#   ⑤ farr OOM — pod hexa < v0.311.0 leaks the bump allocator to 85GB. (--bootstrap to fix.)
hexa cloud exec "$POD" -- "cd /root/anima && rm -rf core cli && tar xzf anima_bundle.tgz && rm -rf core/core && \
  v=\$(/root/.hx/bin/hexa --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1); echo \"hexa: \$v\"; \
  awk -v v=\"\$v\" 'BEGIN{n=split(v,a,\".\"); if(n<2||(a[1]==0&&a[2]<311)){print \"FATAL ⑤: hexa \"v\" < v0.311.0 (farr OOM) — re-run with --bootstrap\"; exit 1}}'; \
  ls core/g_gates.hexa >/dev/null 2>&1 || { echo 'FATAL ①: core/g_gates.hexa MISSING (stale/partial core)'; exit 1; }; \
  [ \"\$(grep -c 'argv\[0\] == \"eval\"' cli/anima.hexa)\" -ge 1 ] || { echo 'FATAL ①: cli/anima.hexa lacks eval subcommand (stale source → daemon, not G0-G6)'; exit 1; }; \
  ls SAVANT/savant_lib.hexa >/dev/null 2>&1 || { echo 'FATAL ④: SAVANT/savant_lib.hexa MISSING (lane closure)'; exit 1; }; \
  ls /root/anima/$CLM_NAME >/dev/null 2>&1 || { echo 'FATAL: ckpt $CLM_NAME MISSING'; exit 1; }; \
  echo 'sanity OK: hexa≥v0.311 · g_gates · eval-branch · savant_lib · ckpt'"

# --- launch eval detached (exec-session-timeout irrelevant; glue-bound decode = tens of minutes) ---
# HEXA_DET=1 = forge determinism safety-pin (hexa-lang #4208 fast-default follow-on): this
# launch reaches cli/anima.hexa DIRECTLY (not the bin/anima shim), so it sets HEXA_DET here
# to keep G0-G6 scoring + cross-host byte-parity reproducible (#4208 made non-det atomic
# forge kernels the default; HEXA_DET=1 selects the bit-identical deterministic kernels).
echo "[eval_pod] launch: anima eval $CLM_NAME --gen $GEN (detached) ..."
hexa cloud exec "$POD" -- "cd /root/anima && export PATH=/root/.hx/bin:\$PATH HEXA_FRAG_LOG=1 HEXA_DET=1; \
  nohup hexa run cli/anima.hexa -- eval $CLM_NAME --gen $GEN > eval_out.txt 2>&1 & echo LAUNCHED_PID=\$!"

rm -f "$LANE_LIST" "$TGZ"
echo "[eval_pod] launched. poll:  hexa cloud exec $POD -- \"tail -20 /root/anima/eval_out.txt\""
echo "[eval_pod]          harvest: hexa cloud copy-from $POD /root/anima/eval_out.txt <local>"

# --- optional inline harvest (blocks until eval_out.txt shows G0-G6 closure) ---
if [ -n "$HARVEST" ]; then
  echo "[eval_pod] --harvest set → polling for G0-G6 closure (a7b_pass), then copy-from ..."
  for _ in $(seq 1 120); do   # up to ~60min at 30s
    sleep 30
    if hexa cloud exec "$POD" -- "grep -qE 'a7b_pass|G6|VERDICT' /root/anima/eval_out.txt 2>/dev/null"; then
      hexa cloud copy-from "$POD" /root/anima/eval_out.txt "$HARVEST"
      echo "[eval_pod] harvested → $HARVEST"
      break
    fi
  done
fi
