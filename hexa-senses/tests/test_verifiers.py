"""Smoke tests for verify/*.py."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"


@pytest.mark.auto
@pytest.mark.parametrize("script,expected", [
    ("n6_arithmetic.py",  r"\d+/\d+ PASS  —  n=6 arithmetic identity"),
    ("spec_inventory.py", r"5/5 verb specs present"),
])
def test_verifier_runs_clean(script, expected):
    rc = subprocess.run([sys.executable, str(VERIFY / script)],
                        capture_output=True, text=True, cwd=str(ROOT))
    assert rc.returncode == 0, f"{script}: {rc.stdout}\n{rc.stderr}"
    assert re.search(expected, rc.stdout)


@pytest.mark.auto
def test_cli_dispatcher_all_pass():
    rc = subprocess.run([sys.executable, str(VERIFY / "cli.py"), "all", "--quiet"],
                        capture_output=True, text=True, cwd=str(ROOT))
    assert rc.returncode == 0
    m = re.search(r"(\d+)/(\d+) checks PASS", rc.stdout)
    assert m
    n_ok, total = int(m.group(1)), int(m.group(2))
    assert n_ok == total
