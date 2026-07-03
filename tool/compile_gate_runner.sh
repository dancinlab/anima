#!/usr/bin/env bash
# anima compile-gate runner — per-module fast gate for the engine entrypoints.
# Delegates to hexa-lang's tool/compile_gate.py (landed in hexa-lang #4461):
# body-only edits gate in ~1.4s (changed-module transpile + clang -fsyntax-only
# against a generated sibling-interface skeleton) instead of a ~10s+ full
# `hexa build`; interface/closure changes and stale anchors fall back to the
# full build inside the tool itself (no weakened check — the tool decides).
# Resolution order: installed toolchain src -> sibling checkout. No silent skip:
# if the tool is missing entirely, this check FAILS loudly (exit 2).
set -euo pipefail

CG=""
for cand in "$HOME/.hx/src/tool/compile_gate.py" \
            "/Users/mini/dancinlab/hexa-lang/tool/compile_gate.py"; do
    if [ -f "$cand" ]; then CG="$cand"; break; fi
done
# Sibling checkout may be held on a stale branch by another session (never touch
# it) — extract the tool from its origin/main ref into the hexa cache instead.
if [ -z "$CG" ] && [ -d "/Users/mini/dancinlab/hexa-lang/.git" ]; then
    mkdir -p "$HOME/.hexa-cache/cgate"
    if git -C /Users/mini/dancinlab/hexa-lang fetch -q origin main 2>/dev/null && \
       git -C /Users/mini/dancinlab/hexa-lang show origin/main:tool/compile_gate.py \
           > "$HOME/.hexa-cache/cgate/compile_gate.py" 2>/dev/null && \
       [ -s "$HOME/.hexa-cache/cgate/compile_gate.py" ]; then
        CG="$HOME/.hexa-cache/cgate/compile_gate.py"
    fi
fi
if [ -z "$CG" ]; then
    echo "compile-gate: compile_gate.py not found (install hexa >= the #4461 release or clone dancinlab/hexa-lang as a sibling)" >&2
    exit 2
fi

REPO="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$CG" --repo "$REPO" \
    --entry cli/anima.hexa --entry cli/train.hexa \
    --changed --base origin/main "$@"
