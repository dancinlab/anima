#!/bin/bash
# HEXAD/build_verify.sh — COMPILED-native verification gate (interp deprecating)
#
# User directive 2026-05-16: "컴파일 버전에 해야되 · 인터프리터 폐기 예정 참고".
# `hexa run` (interpreter) 는 폐기 예정 → 모든 HEXAD 모듈은 `hexa build`
# (native binary) 로 검증한다. 이 스크립트가 그 canonical gate.
#
# Compiled-first lib/entrypoint split (2026-05-16):
#   <X>/<x>_lib.hexa  — pure fns, NO main / NO _selftest (import 대상)
#   <X>/<x>.hexa      — import <x>_lib + _selftest + main (standalone entry)
#   integ_test.hexa   — imports *_lib.hexa only (no main/_selftest collision)
# 이전 단일파일 (main+_selftest 동거) 은 컴파일러에서 `_selftest`/`u_main`
# C 심볼 중복정의 → interp-only. lib-split 가 compiled-native 정석.
#
# Mac build gate: HEXA_MAC_BUILD_OK=1 (2026-04-20 kernel panic guard bypass,
# non-heavy tiny formulaic modules only). 출력 = _hexa_build/ (gitignored).
# Heavy build 는 ubu 권장: ssh ubu 'cd ~/Dev/anima && hexa build ...'.
#
# Usage:  bash HEXAD/build_verify.sh        # build+run all, assert PASS
# Exit 0 iff 11/11 entrypoints PASS + 9/9 libs build clean.
# (11th entrypoint / 9th lib = HEXAD/CHAT/wiring_verify — inter-module
#  wiring 조건 W5/W6/W8 F-WIRE battery, 2026-05-16 closure.)

set -u
cd "$(dirname "$0")/.." || exit 2
export HEXA_MAC_BUILD_OK=1
BUILD_DIR="_hexa_build"
mkdir -p "$BUILD_DIR"

ENTRYPOINTS=(
  "HEXAD/S/s.hexa"          "HEXAD/M/m.hexa"        "HEXAD/W/w.hexa"
  "HEXAD/E/e.hexa"          "HEXAD/BRIDGE/bridge.hexa"
  "HEXAD/C/c.hexa"          "HEXAD/D/d.hexa"
  "HEXAD/MITOSIS/mitosis.hexa"
  "HEXAD/hexad.hexa"        "HEXAD/integ_test.hexa"
  "HEXAD/CHAT/wiring_verify.hexa"
)
LIBS=(
  "HEXAD/S/s_lib.hexa"      "HEXAD/M/m_lib.hexa"    "HEXAD/W/w_lib.hexa"
  "HEXAD/E/e_lib.hexa"      "HEXAD/BRIDGE/bridge_lib.hexa"
  "HEXAD/C/c_lib.hexa"      "HEXAD/D/d_lib.hexa"
  "HEXAD/MITOSIS/mitosis_lib.hexa"
  "HEXAD/CHAT/wiring_verify_lib.hexa"
)
PASS_MARKER='selftest: true|7/7 cross-file|spec invariants: true|scaffold check: true'

ep_pass=0; ep_fail=0; lib_ok=0; lib_fail=0; failed=""

echo "=== HEXAD compiled-native verification (hexa build, interp deprecating) ==="
for f in "${ENTRYPOINTS[@]}"; do
  base=$(echo "$f" | tr '/' '_' | sed 's/\.hexa//')
  bin="$BUILD_DIR/$base"
  if hexa build "$f" -o "$bin" >/tmp/hexad_bld.log 2>&1 \
     && [ -x "$bin" ] \
     && timeout 60 "$bin" >/tmp/hexad_run.log 2>&1 \
     && grep -qE "$PASS_MARKER" /tmp/hexad_run.log; then
    echo "  ✅ $f"
    ep_pass=$((ep_pass+1))
  else
    echo "  ❌ $f"
    grep -iE 'error:|redefinition' /tmp/hexad_bld.log /tmp/hexad_run.log 2>/dev/null | head -2
    ep_fail=$((ep_fail+1)); failed="$failed $f"
  fi
done
for lib in "${LIBS[@]}"; do
  base=$(echo "$lib" | tr '/' '_' | sed 's/\.hexa//')
  if hexa build "$lib" -o "$BUILD_DIR/$base" >/tmp/hexad_lib.log 2>&1; then
    lib_ok=$((lib_ok+1))
  else
    echo "  ❌ lib build $lib"; lib_fail=$((lib_fail+1)); failed="$failed $lib"
  fi
done

echo "=== compiled: entrypoint ${ep_pass}/${#ENTRYPOINTS[@]} PASS · lib ${lib_ok}/${#LIBS[@]} build OK ==="
if [ "$ep_pass" -eq "${#ENTRYPOINTS[@]}" ] && [ "$lib_ok" -eq "${#LIBS[@]}" ]; then
  echo "ALL COMPILED-NATIVE PASS — interp-deprecation safe."
  exit 0
fi
echo "FAILED:$failed"
exit 1
