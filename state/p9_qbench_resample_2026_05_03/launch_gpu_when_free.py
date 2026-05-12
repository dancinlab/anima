#!/usr/bin/env python3
"""F-QBENCH-1: queue HellaSwag full eval on ubu1 GPU.
Waits for GPU memory to free up (other P9 jobs running) then launches.
raw#10: NO preemption — we wait, never kill. Polling interval 5 min.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

LOG = Path("/home/aiden/anima/state/p9_qbench_resample_2026_05_03/launch.log")
OUT = "/home/aiden/anima/state/p9_qbench_resample_2026_05_03/full_hellaswag_per_example.json"
EVAL = "/home/aiden/anima/state/p9_qbench_resample_2026_05_03/eval_hellaswag_full.py"
PYTHON = "/home/aiden/venv_orchestrator/bin/python"

LOG.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    line = f"[{time.strftime('%FT%TZ', time.gmtime())}] {msg}"
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def gpu_used_mib():
    out = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        text=True).strip().splitlines()[0]
    return int(out)


def n_compute_apps():
    out = subprocess.check_output(
        ["nvidia-smi", "--query-compute-apps=pid", "--format=csv,noheader,nounits"],
        text=True).strip()
    return 0 if not out else len([x for x in out.splitlines() if x.strip()])


def main():
    log("launcher starting (waiting for GPU)")
    deadline = time.time() + 8 * 3600
    while True:
        used = gpu_used_mib()
        napps = n_compute_apps()
        log(f"gpu_used_mib={used} n_compute_apps={napps}")
        if used < 4096 and napps <= 0:
            log("GPU free, launching eval")
            break
        if time.time() > deadline:
            log("DEADLINE reached without GPU free, abort")
            sys.exit(2)
        time.sleep(300)

    log(f"starting eval; output={OUT}")
    rc = subprocess.call([PYTHON, EVAL, "--output", OUT, "--limit", "0"])
    log(f"eval finished rc={rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
