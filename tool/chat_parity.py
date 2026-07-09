#!/usr/bin/env python3
"""tool/chat_parity.py — anima chat 2-production parity harness (P0 · zero-hexa self-impl).

The end-to-end closure gate for the py chat daemon self-implementation (owner directive
2026-07-09 "py 자체구현 · 언어간 상호의존 0"): the py channel `anima-py chat <ckpt>` transcript +
`.kosmos` writes must be BYTE-IDENTICAL to the hexa `anima <ckpt>` reference (deterministic
12-tick session: stage = dr_stage_at(tick*8), greedy argmax mouth, no RNG on the verdict path).
The ONLY non-deterministic surface is wall-clock — `emitted_at` in written anchors + the volatile
kosmos dir prefix in transcript paths — which this harness MASKS before diffing.

Reuses the archive/state/core_2prod_py_parity/compare.py contract (byte-identical strings) but at
the whole-transcript + kosmos-tree level (not just key=value fields).

Modes:
  chat_parity.py selftest '<hexa chat cmd>'   — run the SAME cmd twice, assert 0 diff
                                                 (proves the golden itself is deterministic — the
                                                 Phase-0 acceptance check; if this fails the golden
                                                 is unusable and no py comparison is meaningful).
  chat_parity.py compare '<hexa cmd>' '<py cmd>'  — golden hexa vs py twin: 0 diff = PARITY.

The kosmos root is the HARDCODED `/tmp/anima_kosmos` (cli/anima.hexa:627 `let kdir =
"/tmp/anima_kosmos"`, `rm -rf`+`mkdir` wiped per session) — NOT env-configurable. So the harness
does NOT inject a dir; it pre-wipes that fixed path, runs the cmd (which wipes+writes it too), then
captures it. The P6 py chat (`cli/chat.py`) MUST write to the SAME hardcoded `/tmp/anima_kosmos`
for a byte-parity comparison. The fixed path means the transcript's kosmos paths are identical on
both sides, so only `emitted_at` + UTC timestamps need masking (the path prefix mask below is then
a harmless no-op kept for robustness). `$ANIMA_KOSMOS_DIR` is still exported (forward-compat: a
future env-aware py chat can honor it), but the hexa reference ignores it.
"""
import os
import re
import shutil
import subprocess
import sys

# hardcoded chat kosmos root (cli/anima.hexa:627 · wiped per session). Both twins write here.
KOSMOS_DIR = "/tmp/anima_kosmos"

# wall-clock masks — the only non-deterministic bytes in a det-clock chat session.
_UTC_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")          # ISO-8601 UTC (emitted_at, _ki_utc_now)
_EMITTED_AT_RE = re.compile(r"(emitted_at\s*=\s*).*$", re.MULTILINE)   # anchor emitted_at line body


def _mask(text, kosmos_dir):
    """Replace the volatile kosmos dir prefix + any wall-clock timestamp with stable tokens."""
    if kosmos_dir:
        text = text.replace(kosmos_dir, "<KOSMOS_DIR>")
    text = _EMITTED_AT_RE.sub(r"\1<EMITTED_AT>", text)
    text = _UTC_RE.sub("<UTC>", text)
    return text


def capture(cmd, kosmos_dir=KOSMOS_DIR):
    """Pre-wipe the fixed kosmos dir, run the chat cmd (it wipes+writes there too), then capture it.
    Returns (masked_stdout, {relpath: masked_bytes}, returncode). Runs are sequential (shared dir)."""
    if os.path.isdir(kosmos_dir):
        shutil.rmtree(kosmos_dir)
    os.makedirs(kosmos_dir, exist_ok=True)
    env = dict(os.environ)
    env["ANIMA_KOSMOS_DIR"] = kosmos_dir          # forward-compat; hexa ignores it (hardcoded path)
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    stdout = _mask(proc.stdout, kosmos_dir)
    kfiles = {}
    for root, _dirs, files in os.walk(kosmos_dir):
        for fn in sorted(files):
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, kosmos_dir)
            with open(full, "r", errors="replace") as fh:
                kfiles[rel] = _mask(fh.read(), kosmos_dir)
    return stdout, kfiles, proc.returncode


def diff(cap_a, cap_b, label_a="A", label_b="B"):
    """Byte-diff two captures (stdout + kosmos tree). Return list of divergence strings ([] = parity)."""
    (out_a, kf_a, rc_a) = cap_a
    (out_b, kf_b, rc_b) = cap_b
    problems = []
    if rc_a != 0:
        problems.append(f"{label_a} exit={rc_a} (nonzero)")
    if rc_b != 0:
        problems.append(f"{label_b} exit={rc_b} (nonzero)")
    if out_a != out_b:
        # locate first differing line for a readable message
        la, lb = out_a.splitlines(), out_b.splitlines()
        first = next((i for i in range(min(len(la), len(lb))) if la[i] != lb[i]), None)
        if first is not None:
            problems.append(f"stdout diff @line {first}: {label_a}={la[first]!r} {label_b}={lb[first]!r}")
        else:
            problems.append(f"stdout length diff: {label_a}={len(la)}L {label_b}={len(lb)}L")
    only_a = sorted(set(kf_a) - set(kf_b))
    only_b = sorted(set(kf_b) - set(kf_a))
    if only_a:
        problems.append(f"kosmos files only in {label_a}: {only_a}")
    if only_b:
        problems.append(f"kosmos files only in {label_b}: {only_b}")
    for rel in sorted(set(kf_a) & set(kf_b)):
        if kf_a[rel] != kf_b[rel]:
            problems.append(f"kosmos byte diff: {rel}")
    return problems


def _run_pair(cmd_a, cmd_b, label_a, label_b):
    # sequential: both write the SAME hardcoded KOSMOS_DIR, so capture A fully before running B.
    ca = capture(cmd_a)
    cb = capture(cmd_b)
    problems = diff(ca, cb, label_a, label_b)
    if problems:
        print(f"❌ PARITY FAIL ({label_a} vs {label_b}) — {len(problems)} divergence(s):")
        for p in problems[:40]:
            print("   · " + p)
        return 1
    print(f"✅ PARITY PASS ({label_a} vs {label_b}) — transcript + kosmos byte-identical (wall-clock masked)")
    return 0


def main(argv):
    if len(argv) >= 3 and argv[1] == "selftest":
        # golden determinism: same cmd twice → 0 diff
        return _run_pair(argv[2], argv[2], "hexa#1", "hexa#2")
    if len(argv) >= 4 and argv[1] == "compare":
        return _run_pair(argv[2], argv[3], "hexa", "py")
    print(__doc__)
    print("usage: chat_parity.py selftest '<hexa cmd>' | compare '<hexa cmd>' '<py cmd>'")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
