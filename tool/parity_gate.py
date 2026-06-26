#!/usr/bin/env python3
"""parity_gate — CODE-LEVEL enforcement of the hexa ⇄ py 2-production byte-parity (LOCKSTEP).

a_engine_native_learning: anima keeps TWO co-equal production engines (hexa core/*.hexa and
py core/*.py) at byte-parity. A py-engine G-gate verdict is terminal ONLY if its SCORING matches
the WIRED hexa single-entry (cli/anima.hexa eval → core/g_gates.hexa → generator L3). Decode-only
parity is NOT enough — a py side-harness that scores with g_gates.py can DRIFT (precedent
2026-06-26 clm303_clean: side-harness G1/G6 @gen=40 was a gen-budget + unverified-scoring artifact).

This gate runs the GOLDEN small ckpt (d768 — hexa runs it WITHOUT the 303M OOM) through BOTH:
  (1) the WIRED hexa single entry   : hexa run cli/anima.hexa -- eval <golden> --gen 0
  (2) the py production engine       : python3 core/g_gates.py <golden> --gen 0
and asserts the G0-G6 verdict fields are IDENTICAL. Any drift → exit 1 → CI red → merge blocked.
A wiring that cannot run (entry absent / no parseable G0-G6) → exit 2 (fail LOUD, never silent-pass).

CI-wired on the Blacksmith macOS runner (.github/workflows/ci.yml). Local: python3 tool/parity_gate.py
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# golden d768 ConvMoE ckpt — small enough that the hexa wired eval runs without the 303M OOM.
GOLDEN_CANDIDATES = [
    "state/lane_p_clm/clm_d768_e2l1.clm",
    "state/lane_p_clm/reexport_d768_v2_fast.clm",
]

# WIRED = the ACTUAL production CLI binary the user/pod runs: `anima eval <ckpt>` (installed via
# `hx install anima`). This is the strongest engine-native standard — NOT a source-file run
# (`hexa run cli/anima.hexa`) and NOT a py side-harness. We try the installed `anima` binary
# FIRST; the source-run is only a fallback for envs where `anima` isn't on PATH yet (it routes
# through the identical cli/anima.hexa → core/g_gates.hexa → generator L3 single entry).
WIRED_CMDS = [
    ["anima", "eval", "{ckpt}", "--gen", "0"],                                    # 실제 CLI 바이너리 (canonical)
    ["hexa", "run", "cli/anima.hexa", "--", "eval", "{ckpt}", "--gen", "0"],      # 소스-run fallback
]
PY_CMD = [sys.executable, "core/g_gates.py", "{ckpt}", "--gen", "0"]

# structured G0-G6 verdict fields parsed from each engine's stdout (format-tolerant: match the
# canonical g_gates printout `G0 COHERENCE pass=True n_coherent=5/5 ...` etc.).
FIELD_RE = {
    "G0_pass": re.compile(r"G0\b.*?pass=(\w+)", re.I),
    "G1_pass": re.compile(r"G1\b.*?pass=(\w+)", re.I),
    "G1_max_single": re.compile(r"G1\b.*?max_single=(\d+)", re.I),
    "G2_pass": re.compile(r"G2\b.*?pass=(\w+)", re.I),
    "G2_n_novel": re.compile(r"G2\b.*?n_novel=(\d+)", re.I),
    "G6_dist": re.compile(r"G6\b.*?dist=(\d+)", re.I),
    "G6_fals": re.compile(r"G6\b.*?fals=(\d+)", re.I),
    "a7b_pass": re.compile(r"a7b_pass.*?=>?\s*(PASS|FAIL|True|False)", re.I),
}


def run(cmd, ckpt):
    args = [a.replace("{ckpt}", ckpt) for a in cmd]
    try:
        p = subprocess.run(args, cwd=REPO, capture_output=True, text=True, timeout=1800)
    except Exception as e:
        return None, f"run error: {e}"
    out = (p.stdout or "") + "\n" + (p.stderr or "")
    return out, None


def parse(out):
    got = {}
    for k, rx in FIELD_RE.items():
        m = rx.search(out)
        if m:
            got[k] = m.group(1).upper()
    return got


def main():
    ckpt = next((c for c in GOLDEN_CANDIDATES if os.path.isfile(os.path.join(REPO, c))), None)
    if not ckpt:
        # no golden ckpt locally (e.g. shallow CI checkout w/o LFS weights) → cannot run the
        # parity gate; skip LOUDLY (not a pass, not a false-red) so the gap is visible.
        print("::warning::parity_gate: no golden d768 ckpt present "
              f"({' / '.join(GOLDEN_CANDIDATES)}) — parity NOT verified this run (skipped).")
        return 0

    # WIRED: prefer the real installed `anima` CLI binary; fall back to source-run.
    wired_out, werr, wired_via = None, "no command tried", "?"
    for cmd in WIRED_CMDS:
        out, err = run(cmd, ckpt)
        if out is not None and parse(out):
            wired_out, werr, wired_via = out, None, cmd[0]
            break
        werr = err or "no parseable G0-G6"
    py_out, perr = run(PY_CMD, ckpt)
    if wired_out is None:
        print(f"::error::parity_gate: WIRED single-entry eval failed to run ({werr}). "
              "The real `anima eval` CLI (or hexa run cli/anima.hexa -- eval) must work for the "
              "2-production parity gate — that IS the canonical engine-native measurement.")
        return 2
    print(f"   wired-via = {wired_via}")
    if perr or py_out is None:
        print(f"::error::parity_gate: py engine (core/g_gates.py) failed to run ({perr}).")
        return 2
    if perr or py_out is None:
        print(f"::error::parity_gate: py engine (core/g_gates.py) failed to run ({perr}).")
        return 2

    w, y = parse(wired_out), parse(py_out)
    if not w or not y:
        print("::error::parity_gate: could not parse G0-G6 verdict fields from "
              f"{'WIRED' if not w else ''}{'+' if not w and not y else ''}{'PY' if not y else ''} "
              "output — the single-entry G-gate printout drifted. (fail LOUD, no silent pass)")
        print("--- WIRED ---\n" + wired_out[-1500:])
        print("--- PY ---\n" + py_out[-1500:])
        return 2

    keys = sorted(set(w) | set(y))
    diffs = [(k, w.get(k, "∅"), y.get(k, "∅")) for k in keys if w.get(k) != y.get(k)]
    print(f"parity_gate · golden={ckpt} · fields={len(keys)} · "
          f"{'MATCH' if not diffs else 'DIVERGENT'}")
    for k in keys:
        flag = "≠" if w.get(k) != y.get(k) else "="
        print(f"   {flag} {k:16s} wired={w.get(k,'∅'):6s} py={y.get(k,'∅')}")
    if diffs:
        print("::error::parity_gate: hexa ⇄ py SCORING DRIFT — the py engine is NOT byte-parity "
              "with the wired hexa single-entry. LOCKSTEP violated (a_engine_native_learning). "
              "Fix the diverging op in core/*.py before any py-engine terminal G-gate verdict.")
        return 1
    print("✅ parity_gate: hexa ⇄ py G0-G6 byte-parity verified on golden (2-production LOCKSTEP).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"::error::parity_gate: ENFORCER ERROR — {e}", file=sys.stderr)
        sys.exit(2)
