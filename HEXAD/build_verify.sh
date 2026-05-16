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
# Two tiers (honest, see TOOLCHAIN below):
#   • always-gated (stale-toolchain-clean): 17 entrypoints + 13 libs.
#     Exit 0 requires all of these PASS — unrelated work never blocked.
#   • bootstrapped-toolchain-gated (chat_lib in import closure): the
#     CHAT/D-R2 set {chat_lib, anima_chat, d_lib, d, integ_test}. These
#     need a hexa.real from hexa-lang ≥0fccac5c; with a stale system
#     hexa.real they are SKIPPED-WITH-WARNING (NOT in the denominator,
#     NOT a hard failure). With HEXA_BOOT set they ARE gated + counted.
# (always-gated tail = HEXAD/CHAT/wiring_verify —
#  inter-module wiring 조건 W5/W6/W8 F-WIRE battery, 2026-05-16 closure.)
#
# ── TOOLCHAIN (honest, READ THIS) ───────────────────────────────────────────
# HEXAD/CHAT/chat_lib.hexa + HEXAD/CHAT/anima_chat.hexa use a nested mutable
# index-assignment pattern (cell_pool[l][...] = ...) whose CORRECT C lowering
# (`_gen2_nested_index_assign_stmt`) + the `hexa_abs` runtime decl only exist
# in hexa-lang ≥ commit 0fccac5c — i.e. PR #49 (safetensors_mmap_* decls),
# PR #50 (slice-family decls), PR #51 (nested-index-assign CODEGEN + hexa_abs
# decl). The codegen is BAKED INTO the hexa.real binary (self/codegen_c2.hexa
# → self/native/hexa_cc.c → hexa_v2 → hexa.real); a *stale* system
# /Users/ghost/.hx/bin/hexa.real built before 0fccac5c emits 4 + 2
# `expression is not assignable` clang errors on these 2 files and produces
# NO binary — this is a TOOLCHAIN gap, not an anima-source defect.
#
# To build the 2 CHAT targets you need a hexa.real bootstrapped from
# hexa-lang ≥ 0fccac5c. Point this gate at it with:
#
#   HEXA_BOOT=/path/to/bootstrapped/hexa  bash HEXAD/build_verify.sh
#
# (HEXA_BOOT = a `hexa` shim/binary; if its module_loader needs a macOS
#  interpreter, also export HEXA_INTERP=/abs/path/to/working/hexa_interp.real
#  and HEXA_LANG=/path/to/the/≥0fccac5c/checkout — both forwarded only to the
#  CHAT builds, never to the other modules.)
#
# Without HEXA_BOOT the gate probes the system `hexa` for the codegen fix;
# if absent, the 2 CHAT targets are reported `⏭  SKIP (stale toolchain …)`
# and EXCLUDED from the pass-count denominator. The other 17/13 still gate
# normally, so unrelated work is never blocked or falsely greened.

set -u
cd "$(dirname "$0")/.." || exit 2
export HEXA_MAC_BUILD_OK=1
BUILD_DIR="_hexa_build"
mkdir -p "$BUILD_DIR"

# ── toolchain selection ─────────────────────────────────────────────────────
# Default toolchain for the 14/13 non-CHAT modules: plain `hexa` (system).
# CHAT_HEXA = the toolchain used ONLY for the 2 CHAT targets. If HEXA_BOOT is
# set we trust it (caller asserts it is ≥ 0fccac5c). Otherwise we probe the
# system `hexa` for the PR #51 codegen by compiling a 1-line nested
# index-assign and checking it does NOT emit "expression is not assignable".
HEXA="${HEXA:-hexa}"
CHAT_HEXA="${HEXA_BOOT:-}"
CHAT_TOOLCHAIN_OK=0
CHAT_PRE=""              # env prefix forwarded ONLY to CHAT builds
if [ -n "$CHAT_HEXA" ]; then
  CHAT_TOOLCHAIN_OK=1
  [ -n "${HEXA_INTERP:-}" ] && CHAT_PRE="$CHAT_PRE HEXA_INTERP=$HEXA_INTERP"
  [ -n "${HEXA_LANG:-}"   ] && CHAT_PRE="$CHAT_PRE HEXA_LANG=$HEXA_LANG"
  echo "[toolchain] CHAT targets → HEXA_BOOT=$CHAT_HEXA (caller-asserted ≥0fccac5c)"
else
  CHAT_HEXA="$HEXA"
  # Probe must mirror chat_lib's EXACT trigger: a 3-level nested mutable
  # index-assign through a string-keyed dict (cell_pool[K][i][K2] = v). A
  # trivial 2-level array assign (g[0][0]=v) lowers fine even pre-0fccac5c
  # and would FALSE-POSITIVE — the bug only surfaces on this deeper shape.
  _probe_dir=$(mktemp -d 2>/dev/null || echo /tmp/_hexad_probe.$$)
  mkdir -p "$_probe_dir"
  printf 'fn main(){\n let mut cp = #{ "L": [ #{ "h": 1 } ] }\n cp["L"][0]["h"] = 7\n print(to_string(cp["L"][0]["h"]))\n}\n' > "$_probe_dir/p.hexa"
  if HEXA_MAC_BUILD_OK=1 "$CHAT_HEXA" build "$_probe_dir/p.hexa" -o "$_probe_dir/p" >"$_probe_dir/log" 2>&1 \
     && ! grep -q "expression is not assignable" "$_probe_dir/log" \
     && [ -x "$_probe_dir/p" ]; then
    CHAT_TOOLCHAIN_OK=1
    echo "[toolchain] system hexa carries nested-index-assign codegen (≥0fccac5c) — CHAT targets ENABLED"
  else
    echo "[toolchain] system hexa is STALE (pre-0fccac5c: no nested-index-assign codegen)"
    echo "[toolchain] → HEXAD/CHAT/{chat_lib,anima_chat}.hexa will be SKIPPED-WITH-WARNING"
    echo "[toolchain]   (set HEXA_BOOT=/path/to/bootstrapped/hexa to enable — see header)"
  fi
  rm -rf "$_probe_dir" 2>/dev/null
fi

# ── always-gated modules (no chat_lib in their import closure) ──────────────
# These compile clean on a STALE system toolchain — they must keep gating
# normally so unrelated work is never blocked.
ENTRYPOINTS=(
  "HEXAD/S/s.hexa"          "HEXAD/M/m.hexa"        "HEXAD/W/w.hexa"
  "HEXAD/E/e.hexa"          "HEXAD/BRIDGE/bridge.hexa"
  "HEXAD/E/e_gate_smoke.hexa"
  "HEXAD/BRIDGE/bridge_forward_smoke.hexa"
  "HEXAD/C/c.hexa"
  "HEXAD/C/c_phi_smoke.hexa"
  "HEXAD/D/d_train_smoke.hexa"
  "HEXAD/D/d_train2_smoke.hexa"
  "HEXAD/D/d_train3_smoke.hexa"
  "HEXAD/D/d_train4_smoke.hexa"
  "HEXAD/D/d_train5_smoke.hexa"
  "HEXAD/MITOSIS/mitosis.hexa"
  "HEXAD/hexad.hexa"
  "HEXAD/CHAT/wiring_verify.hexa"
)
LIBS=(
  "HEXAD/S/s_lib.hexa"      "HEXAD/M/m_lib.hexa"    "HEXAD/W/w_lib.hexa"
  "HEXAD/E/e_lib.hexa"      "HEXAD/BRIDGE/bridge_lib.hexa"
  "HEXAD/C/c_lib.hexa"
  "HEXAD/D/d_train_lib.hexa"
  "HEXAD/D/d_train2_lib.hexa"
  "HEXAD/D/d_train3_lib.hexa"
  "HEXAD/D/d_train4_lib.hexa"
  "HEXAD/D/d_train5_lib.hexa"
  "HEXAD/MITOSIS/mitosis_lib.hexa"
  "HEXAD/CHAT/wiring_verify_lib.hexa"
)
# ── bootstrapped-toolchain-gated targets (R2, 2026-05-16) ───────────────────
# These transitively pull HEXAD/CHAT/chat_lib.hexa into their import closure
# and need a hexa.real bootstrapped from hexa-lang ≥ 0fccac5c (PR #49 + #50
# decls, PR #51 nested-index-assign CODEGEN + hexa_abs decl). Codegen is
# BAKED into hexa.real (HEXA_LANG only redirects *source* read, not the baked
# codegen) — a stale system hexa.real emits `expression is not assignable`
# and produces NO binary. Control-compared: stale → no binary; bootstrapped
# → OK + binary. The R1 "safetensors decl" comment was imprecise — PR #49
# landed those decls; the real residual is the PR #51 CODEGEN.
#   chat_lib.hexa     R1 lib-split (pure-fn lib, NO main)
#   anima_chat.hexa   R1 entrypoint (imports chat_lib)
#   d_lib.hexa        R2: now `import chat_lib` (d_forward delegation)
#   d.hexa            imports d_lib  → chat_lib transitive
#   integ_test.hexa   imports d_lib  → chat_lib transitive
# Built ONLY when CHAT_TOOLCHAIN_OK=1 (HEXA_BOOT set, or system hexa probed
# ≥0fccac5c); else SKIP-WITH-WARNING (NOT in denominator, NOT a failure).
#   integ_train_smoke R3/Phase6: imports mitosis_hook_lib (nested-index-assign)
CHAT_ENTRYPOINTS=( "HEXAD/D/d.hexa" "HEXAD/integ_test.hexa" "HEXAD/CHAT/anima_chat.hexa" "HEXAD/integ_train_smoke.hexa" )
CHAT_LIBS=(        "HEXAD/D/d_lib.hexa" "HEXAD/CHAT/chat_lib.hexa"                       )
PASS_MARKER='selftest: true|7/7 cross-file|spec invariants: true|scaffold check: true'

ep_pass=0; ep_fail=0; lib_ok=0; lib_fail=0; failed=""
chat_skipped=0

echo "=== HEXAD compiled-native verification (hexa build, interp deprecating) ==="
for f in "${ENTRYPOINTS[@]}"; do
  base=$(echo "$f" | tr '/' '_' | sed 's/\.hexa//')
  bin="$BUILD_DIR/$base"
  if "$HEXA" build "$f" -o "$bin" >/tmp/hexad_bld.log 2>&1 \
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
  if "$HEXA" build "$lib" -o "$BUILD_DIR/$base" >/tmp/hexad_lib.log 2>&1; then
    lib_ok=$((lib_ok+1))
  else
    echo "  ❌ lib build $lib"; lib_fail=$((lib_fail+1)); failed="$failed $lib"
  fi
done

# ── CHAT targets (R2) — bootstrapped-toolchain-gated, skip-with-warning ──────
# CHAT_PRE (HEXA_INTERP/HEXA_LANG) is forwarded ONLY here, never to the loops
# above — keeps the 11/9 modules on the plain system toolchain unchanged.
ep_total=${#ENTRYPOINTS[@]}; lib_total=${#LIBS[@]}
if [ "$CHAT_TOOLCHAIN_OK" -eq 1 ]; then
  for lib in "${CHAT_LIBS[@]}"; do
    base=$(echo "$lib" | tr '/' '_' | sed 's/\.hexa//')
    if env $CHAT_PRE HEXA_MAC_BUILD_OK=1 "$CHAT_HEXA" build "$lib" -o "$BUILD_DIR/$base" >/tmp/hexad_chatlib.log 2>&1 \
       && [ -x "$BUILD_DIR/$base" ]; then
      echo "  ✅ $lib (lib · bootstrapped toolchain)"
      lib_ok=$((lib_ok+1))
    else
      echo "  ❌ lib build $lib (bootstrapped toolchain)"
      grep -iE 'error:|not assignable|Undefined' /tmp/hexad_chatlib.log 2>/dev/null | head -2
      lib_fail=$((lib_fail+1)); failed="$failed $lib"
    fi
    lib_total=$((lib_total+1))
  done
  for f in "${CHAT_ENTRYPOINTS[@]}"; do
    base=$(echo "$f" | tr '/' '_' | sed 's/\.hexa//')
    bin="$BUILD_DIR/$base"
    if ! env $CHAT_PRE HEXA_MAC_BUILD_OK=1 "$CHAT_HEXA" build "$f" -o "$bin" >/tmp/hexad_chatep.log 2>&1 \
       || [ ! -x "$bin" ]; then
      echo "  ❌ $f (bootstrapped toolchain — build)"
      grep -iE 'error:|not assignable|Undefined' /tmp/hexad_chatep.log 2>/dev/null | head -2
      ep_fail=$((ep_fail+1)); failed="$failed $f"; ep_total=$((ep_total+1)); continue
    fi
    # anima_chat.hexa is a REPL entrypoint (no scaffold marker, awaits stdin)
    # → compile-clean + binary is the honest PASS criterion. d.hexa /
    # integ_test.hexa DO emit a PASS_MARKER scaffold line → run + assert it.
    case "$f" in
      *anima_chat.hexa)
        echo "  ✅ $f (entrypoint · bootstrapped toolchain · compile-clean [REPL, no marker])"
        ep_pass=$((ep_pass+1)) ;;
      *)
        if timeout 60 "$bin" </dev/null >/tmp/hexad_chatrun.log 2>&1 \
           && grep -qE "$PASS_MARKER" /tmp/hexad_chatrun.log; then
          echo "  ✅ $f (entrypoint · bootstrapped toolchain · PASS_MARKER)"
          ep_pass=$((ep_pass+1))
        else
          echo "  ❌ $f (bootstrapped toolchain — run/marker)"
          grep -iE 'error:|redefinition' /tmp/hexad_chatrun.log 2>/dev/null | head -2
          ep_fail=$((ep_fail+1)); failed="$failed $f"
        fi ;;
    esac
    ep_total=$((ep_total+1))
  done
else
  for x in "${CHAT_LIBS[@]}" "${CHAT_ENTRYPOINTS[@]}"; do
    echo "  ⏭  SKIP $x (stale toolchain — needs hexa-lang ≥0fccac5c; set HEXA_BOOT, see header)"
    chat_skipped=$((chat_skipped+1))
  done
fi

echo "=== compiled: entrypoint ${ep_pass}/${ep_total} PASS · lib ${lib_ok}/${lib_total} build OK ==="
[ "$chat_skipped" -gt 0 ] && echo "=== NOTE: ${chat_skipped} CHAT target(s) SKIPPED (stale toolchain — NOT in denominator, NOT a failure; HEXA_BOOT to enable) ==="
if [ "$ep_pass" -eq "$ep_total" ] && [ "$lib_ok" -eq "$lib_total" ]; then
  if [ "$chat_skipped" -gt 0 ]; then
    echo "ALL GATED MODULES COMPILED-NATIVE PASS (CHAT skipped — stale toolchain, honest)."
  else
    echo "ALL COMPILED-NATIVE PASS — interp-deprecation safe."
  fi
  exit 0
fi
echo "FAILED:$failed"
exit 1
