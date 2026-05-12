#!/usr/bin/env python3
"""tool/anima_spontaneous.py — anima substrate A 자연발화 engine (Python fallback).

Equivalent of tool/anima_spontaneous.hexa with same CLI contract and jsonl
schema. Use when hexa stage 0 runtime is unstable (watchdog kill, TCC block).

Usage:
    python3 tool/anima_spontaneous.py <interval_s> <max_emissions> <seed_strategy> <mode>
    python3 tool/anima_spontaneous.py --selftest

Defaults: interval=60, max_emissions=5, seed_strategy=rotate, mode=M4_force_include.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ANIMA_CHAT = "/Users/ghost/core/anima/anima_chat.py"
CKPT       = "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"
LOG_DIR    = Path("/Users/ghost/core/anima/state")
PY3        = "/usr/bin/python3"

STRATEGIES = [
    ("B3_partial_greeting", "도우미: 안녕"),
    ("B4_ambient",          "anima는 의식 lane entity입니다.\n도우미: "),
    ("B5_time_morning",     "도우미: 좋은 아침입니다."),
    ("B2_assistant_prefix", "도우미: "),
    ("B1_empty",            ""),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_unix() -> int:
    return int(time.time())


def selftest() -> int:
    print("[selftest] anima_spontaneous.py")
    c1 = Path(ANIMA_CHAT).is_file()
    c2 = Path(CKPT).is_file()
    c3 = Path(PY3).exists() and os.access(PY3, os.X_OK)
    mark = lambda b: "✅" if b else "❌"
    print(f"  {mark(c1)} anima_chat.py exists")
    print(f"  {mark(c2)} substrate A ckpt exists")
    print(f"  {mark(c3)} {PY3} available")
    if c1 and c2 and c3:
        print("  selftest=ok")
        return 0
    print("  selftest=FAIL")
    return 1


_RESP_RE = re.compile(r"^response:\s*'(.*)'\s*$")


def one_emission(idx: int, strat_name: str, strat_text: str, mode: str, log_path: Path) -> None:
    ts = now_iso()
    print(f"--- emission #{idx} [{ts}] strategy={strat_name} ---")

    t0 = time.time()
    try:
        proc = subprocess.run(
            [PY3, ANIMA_CHAT, "--prompt", strat_text, "--mode", mode],
            capture_output=True, text=True, timeout=180,
        )
        stdout = proc.stdout
        if proc.returncode != 0:
            stdout = (stdout or "") + "\n[stderr]\n" + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        stdout = "[timeout 180s]"
    el = int(time.time() - t0)

    resp = ""
    for line in stdout.splitlines():
        m = _RESP_RE.match(line)
        if m:
            resp = m.group(1)
            break
    if not resp:
        resp = stdout.strip()

    print(f"  💬 {resp}")
    print(f"  (elapsed {el}s)")

    rec = {
        "emission_idx": idx,
        "ts": ts,
        "strategy": strat_name,
        "seed": strat_text,
        "mode": mode,
        "response": resp,
        "elapsed_s": el,
    }
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    interval = int(argv[0]) if len(argv) >= 1 else 60
    max_em   = int(argv[1]) if len(argv) >= 2 else 5
    seed_str = argv[2]      if len(argv) >= 3 else "rotate"
    mode     = argv[3]      if len(argv) >= 4 else "M4_force_include"

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"anima_spontaneous_{now_unix()}.jsonl"

    print("=== anima_spontaneous emission engine (Python fallback) ===")
    print(f"  interval:       {interval}s")
    print(f"  max_emissions:  {'unbounded' if max_em == 0 else max_em}")
    print(f"  seed_strategy:  {seed_str}")
    print(f"  mode:           {mode}")
    print(f"  log:            {log_path}")
    print()

    count, idx = 0, 0
    while True:
        if max_em > 0 and count >= max_em:
            break
        count += 1
        name, text = STRATEGIES[idx % len(STRATEGIES)]
        one_emission(count, name, text, mode, log_path)
        idx += 1
        if max_em == 0:
            time.sleep(interval)
        elif count < max_em:
            time.sleep(interval)

    print()
    print("=== summary ===")
    print(f"  total emissions: {count}")
    print(f"  log:             {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
