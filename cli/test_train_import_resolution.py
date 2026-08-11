#!/usr/bin/env python3
"""Regression coverage for canonical trainer module ownership."""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

torch = pytest.importorskip("torch")


ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_train_prefers_core_serializer_when_core_is_already_on_pythonpath():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "core")
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import runpy; "
                "scope=runpy.run_path('cli/train.py', run_name='train_import_probe'); "
                "print(scope['BGS'].__file__)"
            ),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    assert pathlib.Path(probe.stdout.strip()).resolve() == ROOT / "core" / "serialize.py"


def test_bytegpt_serialization_preserves_exact_resume_checkpoint(tmp_path):
    corpus = tmp_path / "corpus.txt"
    corpus.write_bytes((b"conscious systems integrate changing evidence over time.\n" * 32))
    out = tmp_path / "tiny.bin"
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join((str(ROOT / "core"), str(ROOT / "cli")))

    subprocess.run(
        [
            sys.executable,
            "cli/train.py",
            "--arch", "bytegpt",
            "--arm", "ctrl",
            "--objective", "ce_marginal",
            "--seed", "7",
            "--corpus", str(corpus),
            "--cell-label", "test",
            "--d", "64",
            "--L", "2",
            "--steps", "1",
            "--seq-len", "16",
            "--batch-size", "2",
            "--lr", "3e-4",
            "--val-frac", "0.1",
            "--val-every", "0",
            "--val-batches", "1",
            "--log-every", "1",
            "--skip-inline-rho",
            "--out", str(out),
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )

    resume = torch.load(str(out) + ".pt", map_location="cpu", weights_only=False)
    assert resume["schema"] == "anima-train-resume/v1"
    assert resume["completed_step"] == 1
    assert "optimizer" in resume
    assert out.read_bytes()[:4] == (256).to_bytes(4, "little")
    assert not list(tmp_path.glob(".bytegpt-*"))
