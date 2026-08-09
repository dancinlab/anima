#!/usr/bin/env python3
"""Install or inspect the canonical local anima chat broker on macOS."""

from __future__ import annotations

import os
import plistlib
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


LABEL = "com.dancinlab.anima-chat-broker"
HOST = "127.0.0.1"
PORT = 8000
ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv-runtime" / "bin" / "python"
BROKER = ROOT / "agent" / "domains" / "CHAT" / "broker.py"
STATIC = BROKER.parent / "static" / "index.html"
PLIST = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOG_DIR = ROOT / "logs"
DOMAIN = f"gui/{os.getuid()}"


def _check_files() -> None:
    missing = [str(path) for path in (PYTHON, BROKER, STATIC) if not path.is_file()]
    if missing:
        raise SystemExit("missing runtime file(s): " + ", ".join(missing))
    subprocess.run(
        [str(PYTHON), "-c", "import fastapi, uvicorn, websockets"],
        cwd=ROOT,
        check=True,
    )


def _payload() -> dict[str, object]:
    return {
        "Label": LABEL,
        "ProgramArguments": [str(PYTHON), "-u", str(BROKER)],
        "WorkingDirectory": str(ROOT),
        "EnvironmentVariables": {
            "HOST": HOST,
            "PORT": str(PORT),
            "PYTHONUNBUFFERED": "1",
        },
        "RunAtLoad": True,
        "KeepAlive": True,
        "ProcessType": "Background",
        "StandardOutPath": str(LOG_DIR / "chat-broker.out.log"),
        "StandardErrorPath": str(LOG_DIR / "chat-broker.err.log"),
    }


def _healthy(timeout: float = 15.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"http://{HOST}:{PORT}/health", timeout=2) as response:
                return response.status == 200
        except Exception:
            time.sleep(0.25)
    return False


def install() -> int:
    _check_files()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    tmp = PLIST.with_suffix(".plist.tmp")
    with tmp.open("wb") as handle:
        plistlib.dump(_payload(), handle, sort_keys=True)
    os.replace(tmp, PLIST)
    subprocess.run(["launchctl", "bootout", DOMAIN, str(PLIST)], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "bootstrap", DOMAIN, str(PLIST)], check=True)
    subprocess.run(["launchctl", "kickstart", "-k", f"{DOMAIN}/{LABEL}"], check=True)
    if not _healthy():
        raise SystemExit(f"broker failed health check; inspect {LOG_DIR}")
    print(f"healthy: http://{HOST}:{PORT}/health")
    return 0


def status() -> int:
    loaded = subprocess.run(
        ["launchctl", "print", f"{DOMAIN}/{LABEL}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    healthy = _healthy(timeout=1.0)
    print(f"loaded={str(loaded).lower()} healthy={str(healthy).lower()}")
    return 0 if loaded and healthy else 1


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in {"install", "status"}:
        print("usage: deploy_local_chat.py install|status", file=sys.stderr)
        return 2
    return install() if argv[0] == "install" else status()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
