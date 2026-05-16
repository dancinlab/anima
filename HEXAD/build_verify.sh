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
  "HEXAD/D/d_train_smoke.hexa"
  "HEXAD/D/d_train2_smoke.hexa"
  "HEXAD/D/d_train3_smoke.hexa"
  "HEXAD/D/d_train4_smoke.hexa"
  "HEXAD/MITOSIS/mitosis.hexa"
  "HEXAD/hexad.hexa"        "HEXAD/integ_test.hexa"
  "HEXAD/CHAT/wiring_verify.hexa"
)
LIBS=(
  "HEXAD/S/s_lib.hexa"      "HEXAD/M/m_lib.hexa"    "HEXAD/W/w_lib.hexa"
  "HEXAD/E/e_lib.hexa"      "HEXAD/BRIDGE/bridge_lib.hexa"
  "HEXAD/C/c_lib.hexa"      "HEXAD/D/d_lib.hexa"
  "HEXAD/D/d_train_lib.hexa"
  "HEXAD/D/d_train2_lib.hexa"
  "HEXAD/D/d_train3_lib.hexa"
  "HEXAD/D/d_train4_lib.hexa"
  "HEXAD/MITOSIS/mitosis_lib.hexa"
  "HEXAD/CHAT/wiring_verify_lib.hexa"
)
# DEFERRED (honest named blocker — NOT in pass-count; hexa parse clean both):
#   HEXAD/CHAT/chat_lib.hexa  (R1 lib-split, pure-fn lib, NO main)
#   HEXAD/CHAT/anima_chat.hexa(R1 entrypoint, imports chat_lib)
# blocker: compiled codegen 에 `hexa_safetensors_mmap_data_offset` (+ ckpt
#   mmap safetensors intrinsic 일족) C decl 부재 → runtime.h/.c 0 선언.
#   interp-only builtin (이 파일 과거 `hexa run` 21/21 byte-parity 만 검증,
#   compiled native 최초 시도라 표면화). RFC 034 가 runtime.h `hexa_farr_*`
#   decl 추가로 RFC 032/033 compiled smoke 복구한 것과 동일 trivial class.
#   FIX = hexa-lang upstream: runtime.h 에 safetensors-mmap compiled decl 추가.
#   R2(Phase5 d_lib→chat_lib compiled wire) 가 이 blocker 를 상속.
#   decl land 후 위 ENTRYPOINTS 에 anima_chat.hexa / LIBS 에 chat_lib.hexa 재편입.
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

# ── Phase 6 integ_train_smoke — TWO-TIER (needs ≥PR#51 codegen) ─────────────
# integ_train_smoke.hexa parses clean but its mitosis_hook_lib cell_pool
# deep-nested mutation requires hexa-lang PR#51
# (_gen2_nested_index_assign_stmt). The system prebuilt hexa.real has the
# OLD codegen → 4× "expression is not assignable". Gating it into the
# default loop would make the gate red for unrelated work (same situation
# build_verify documents for chat_lib R2). So: SKIP-WITH-WARNING by
# default; only enforced under HEXA_P6_BOOT=<bootstrap-hexa-shim-dir>
# (a /tmp PR#51-bootstrapped toolchain — see
# docs/anima_hexad_p6_fire_2026_05_16.md §2). Never silently green.
# Honest decomposition (doc §2): bare `hexa build` cannot flatten the
# HEXAD import graph (module_loader needs an interpreter; the bootstrap
# worktree's regenerated hexa_full has separate runtime drift). So:
#   (1) FLATTEN imports → single .hexa via the SHARED interpreter
#       ($HEXA_P6_INTERP, no codegen involved) + bootstrap module_loader
#   (2) CODEGEN single .hexa → C via the PR#51 bootstrap hexa_v2
#   (3) clang + the bootstrap worktree's runtime.o
# This isolates the PR#51 fix to exactly the codegen step.
P6_SMOKE="HEXAD/integ_train_smoke.hexa"
P6_BOOT="${HEXA_P6_BOOT:-}"
P6_INTERP="${HEXA_P6_INTERP:-/Users/ghost/core/hexa-lang/build/hexa_interp.real}"
if [ -n "$P6_BOOT" ] && [ -x "$P6_BOOT/self/native/hexa_v2" ] \
   && [ -f "$P6_BOOT/self/runtime.o" ] && [ -x "$P6_INTERP" ] \
   && [ -f "$P6_BOOT/self/module_loader.hexa" ]; then
  echo "=== Phase 6 integ_train_smoke (HEXA_P6_BOOT=$P6_BOOT) ==="
  P6_FLAT="/tmp/p6_bv_flat.hexa"; P6_C="/tmp/p6_bv_flat.c"
  P6_BIN="$BUILD_DIR/p6_integ_train_smoke"
  {  HEXA_LANG="$P6_BOOT" "$P6_INTERP" "$P6_BOOT/self/module_loader.hexa" \
        "$(pwd)/$P6_SMOKE" "$P6_FLAT" \
     && "$P6_BOOT/self/native/hexa_v2" "$P6_FLAT" "$P6_C" \
     && clang -O2 -fno-strict-aliasing -std=c11 -Wno-trigraphs \
          -I "$P6_BOOT/self" "$P6_C" "$P6_BOOT/self/runtime.o" \
          -o "$P6_BIN" -Wl,-stack_size,0x4000000 \
     && codesign --force --sign - "$P6_BIN" ; } >/tmp/hexad_p6.log 2>&1
  if [ -x "$P6_BIN" ] \
     && timeout 120 "$P6_BIN" >/tmp/hexad_p6_run.log 2>&1 \
     && grep -qE "F-INTEG-FULL 5/5|selftest: true" /tmp/hexad_p6_run.log \
     && ! grep -q "is not assignable" /tmp/hexad_p6.log; then
    echo "  ✅ $P6_SMOKE (F-INTEG-FULL 5/5, PR#51 codegen — 0 'is not assignable')"
  else
    echo "  ❌ $P6_SMOKE (HEXA_P6_BOOT enforced — see /tmp/hexad_p6*.log)"
    grep -iE 'error:|not assignable|F-INTEG-FULL [0-4]/5' /tmp/hexad_p6.log /tmp/hexad_p6_run.log 2>/dev/null | head -3
    failed="$failed $P6_SMOKE"
  fi
else
  echo "=== Phase 6 integ_train_smoke: SKIPPED (needs ≥PR#51 codegen) ==="
  echo "  ⚠ system hexa.real has stale codegen (4× 'is not assignable')."
  echo "  ⚠ NOT a regression — set HEXA_P6_BOOT=<bootstrap-hexa-dir> to enforce."
  echo "  ⚠ evidence: docs/anima_hexad_p6_fire_2026_05_16.md §3 ($0 5/5 LANDED)"
fi

echo "=== compiled: entrypoint ${ep_pass}/${#ENTRYPOINTS[@]} PASS · lib ${lib_ok}/${#LIBS[@]} build OK ==="
if [ "$ep_pass" -eq "${#ENTRYPOINTS[@]}" ] && [ "$lib_ok" -eq "${#LIBS[@]}" ] \
   && [ -z "${failed# }" ]; then
  echo "ALL COMPILED-NATIVE PASS — interp-deprecation safe."
  exit 0
fi
echo "FAILED:$failed"
exit 1
