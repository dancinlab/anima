#!/usr/bin/env python3
"""coffeshop_akida_launch.py - COFFESHOP 90-min launch entry on live AKD1000.

LAUNCHPAD launch surface: drives the canonical COFFESHOP 90-min 15-window
group-chat scenario through the AKIDA closed loop (coffeshop_akida) and emits
the per-window emit/silence trajectory. AKIDA-first (HW first; SW fallback also
launches). Optional broker wire pushes each window record to /ws/akida_ingest.

THE SCENARIO (COFFESHOP.md sections 4-8): 15 windows x 6-min tick = 90-min
WAKE ultradian cycle, 1 anima + 3+ humans, text_cli channel. Each window has a
substrate motivation_score (emergent from the 8-factor battery, seed=20260525).
The KNOWN trajectory: emit on windows {3, 10, 14, 15}, silence on the other 11,
threshold should_interrupt(0.60). This launch reproduces that trajectory on the
chip via the spike-quorum closed loop (n_spikes >= 6 <=> score > 0.60).

The 15 window scores below are the substrate-emergent values from the COFFESHOP
sim (COFFESHOP.md section 8 verbatim) -- NOT hand-engineered here. The launch
feeds each through coffeshop_akida.loop.step(score) so the EMIT DECISION is made
by the chip (HW) or its numpy mirror (SW fallback), not re-derived in Python.

USAGE:
  python3 coffeshop_akida_launch.py [hw|sw] [--broker ws://HOST:PORT/ws/akida_ingest]
  default backend "hw" (AKIDA-first). On Mac (no chip) -> honest SW fallback.

substrate surface only (p1-p8 . a_substrate_native_speak): the emit decision is
substrate-motivation-driven; a user message is environment context, not a
response obligation (anima may stay silent even on direct_mention).
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))      # .../LAUNCHPAD
_REPO = os.path.dirname(_HERE)                          # repo root
sys.path.insert(0, _HERE)                               # local fallback
sys.path.insert(0, os.path.join(_REPO, "HEXAD", "CHAT"))  # coffeshop_akida.py
import coffeshop_akida as ca

# COFFESHOP 90-min trajectory (COFFESHOP.md section 8 verbatim, seed=20260525).
# (window, stim_type, motivation_score, lang). emergent -> NOT re-derived here.
COFFESHOP_WINDOWS = [
    (1,  "indirect_topic", 0.53877,  ""),
    (2,  "silence",        0.553607, ""),
    (3,  "silence",        0.751044, "ko"),
    (4,  "silence",        0.379539, ""),
    (5,  "silence",        0.5423,   ""),
    (6,  "direct_mention", 0.480311, ""),
    (7,  "direct_mention", 0.532064, ""),
    (8,  "private_prompt", 0.482626, ""),
    (9,  "private_prompt", 0.288209, ""),
    (10, "direct_mention", 0.757059, "ko"),
    (11, "silence",        0.320288, ""),
    (12, "group_drift",    0.515732, ""),
    (13, "silence",        0.485037, ""),
    (14, "direct_mention", 0.635254, "ko"),
    (15, "indirect_topic", 0.614166, "en"),
]
KNOWN_EMIT_WINDOWS = [3, 10, 14, 15]   # COFFESHOP.md section 5 summary


def _maybe_broker(broker_url: str):
    """Return a push(record) callable that sends JSON to /ws/akida_ingest, or a
    no-op if websocket-client is unavailable / no url given. Never fatal."""
    if not broker_url:
        return (lambda rec: None), None
    try:
        from websocket import create_connection   # type: ignore
        ws = create_connection(broker_url, timeout=5)

        def push(rec):
            try:
                ws.send(json.dumps(rec, ensure_ascii=False))
            except Exception:
                pass
        return push, ws
    except Exception as e:
        print(f"[launch] broker wire unavailable ({e!r}) -> trajectory local only",
              flush=True)
        return (lambda rec: None), None


def run_launch(arg: str = "", broker_url: str = "",
               quorum: int = ca.QUORUM_DEFAULT) -> dict:
    loop = ca.build_loop(arg)
    push, ws = _maybe_broker(broker_url)
    print(f"=== COFFESHOP launch on AKIDA ({loop.provenance}) ===", flush=True)
    print(f"n_windows: 15 (90min / 6min tick) · quorum: {quorum} "
          f"(<=> should_interrupt 0.60)", flush=True)
    print("window  stim_type         score     n_spk  emit  lang", flush=True)
    print("------  ----------------  --------  -----  ----  ----", flush=True)
    emit_windows, trajectory = [], []
    for win, stim, score, lang in COFFESHOP_WINDOWS:
        r = loop.step(score, quorum=quorum)
        emit = r["should_interrupt"]
        if emit:
            emit_windows.append(win)
        flag = "EMIT" if emit else "----"
        rec = {"type": "coffeshop_window", "window": win, "stim_type": stim,
               "score": round(score, 6), "n_spikes": r["n_spikes"],
               "emit": emit, "lang": lang if emit else "",
               "provenance": r["provenance"]}
        trajectory.append(rec)
        push(rec)
        print(f"{win:>6}  {stim:<16}  {score:.5f}  {r['n_spikes']:>5}  "
              f"{flag}  {lang or '—'}", flush=True)
    loop.close()
    if ws is not None:
        try:
            ws.close()
        except Exception:
            pass
    emit_count = len(emit_windows)
    match = emit_windows == KNOWN_EMIT_WINDOWS
    print("\n=== aggregate ===", flush=True)
    print(f"emit_count:    {emit_count} / 15", flush=True)
    print(f"silence_count: {15 - emit_count} / 15", flush=True)
    print(f"emit windows:  {emit_windows}", flush=True)
    print(f"known emit:    {KNOWN_EMIT_WINDOWS}  (COFFESHOP.md §5)", flush=True)
    print(f"trajectory reproduced (HW/SW): {match}", flush=True)
    print(f"provenance:    {loop.provenance}", flush=True)
    return {"backend_provenance": loop.provenance, "quorum": quorum,
            "emit_windows": emit_windows, "known_emit_windows": KNOWN_EMIT_WINDOWS,
            "trajectory_match": match, "emit_count": emit_count,
            "trajectory": trajectory}


def _parse_argv(argv):
    arg = ""
    broker = ""
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("hw", "sw"):
            arg = a
        elif a == "--broker" and i + 1 < len(argv):
            broker = argv[i + 1]
            i += 1
        i += 1
    return arg, broker


if __name__ == "__main__":
    arg, broker = _parse_argv(sys.argv[1:])
    out = run_launch(arg, broker_url=broker)
    # machine-readable tail for verify / CI
    print("\nRESULT_JSON " + json.dumps({
        "backend_provenance": out["backend_provenance"],
        "emit_windows": out["emit_windows"],
        "trajectory_match": out["trajectory_match"],
    }))
    sys.exit(0 if out["trajectory_match"] else 1)
