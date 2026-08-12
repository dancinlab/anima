from __future__ import annotations

import importlib.util
import math
import os
from pathlib import Path
import json
import subprocess
import sys

import pytest


TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None


def _import_train():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for part in (os.path.join(root, "core"), os.path.join(root, "cli")):
        if part in sys.path:
            sys.path.remove(part)
        sys.path.insert(0, part)
    sys.modules.pop("train", None)
    import train
    return train


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_legacy_answer_mask_keeps_only_last_newline_bounded_span():
    import torch

    train = _import_train()
    raw = b"x => first\ny => second\nz"
    targets = torch.tensor([list(raw)], dtype=torch.long)

    mask = train.answer_position_mask(targets)

    assert bytes(targets[0][mask[0]].tolist()) == b"second"


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_chat_answer_mask_selects_every_assistant_response_and_stops_at_newline():
    import torch

    train = _import_train()
    raw = (b"user: one\nassistant: first\n"
           b"user: two\nassistant: second\n"
           b"user: three")
    targets = torch.tensor([list(raw)], dtype=torch.long)

    mask = train.answer_position_mask(
        targets, marker=b"assistant: ", all_spans=True)

    assert bytes(targets[0][mask[0]].tolist()) == b"firstsecond"
    assert not mask[0][raw.index(b"user: two")]


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_chat_answer_ce_reports_exact_selected_position_count():
    import torch

    train = _import_train()
    raw = b"user: q\nassistant: answer\n"
    targets = torch.tensor([list(raw)], dtype=torch.long)
    logits = torch.zeros((1, 256, len(raw)), dtype=torch.float32, requires_grad=True)

    loss, count = train.answer_ce(
        logits, targets, 256, marker=b"assistant: ", all_spans=True)
    loss.backward()

    assert count == len(b"answer")
    assert float(loss.detach()) == pytest.approx(math.log(256), rel=1e-6)
    assert logits.grad is not None
    assert int(torch.count_nonzero(logits.grad)) == count * 256


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_answer_marker_must_not_be_empty():
    import torch

    train = _import_train()
    targets = torch.tensor([[1, 2, 3]], dtype=torch.long)

    with pytest.raises(ValueError, match="must not be empty"):
        train.answer_position_mask(targets, marker=b"", all_spans=True)


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_canonical_cli_records_chat_answer_telemetry(tmp_path):
    root = Path(__file__).resolve().parents[1]
    corpus = tmp_path / "dialogue.train.txt"
    validation = tmp_path / "dialogue.validation.txt"
    dialogue = ("user: one\nassistant: first\n"
                "user: two\nassistant: second\n") * 100
    corpus.write_text(dialogue, encoding="utf-8")
    validation.write_text(dialogue, encoding="utf-8")
    summary_path = tmp_path / "summary.json"
    checkpoint_path = tmp_path / "tiny.pt"

    completed = subprocess.run(
        [
            sys.executable, str(root / "cli" / "train.py"),
            "--arch", "bytegpt", "--d", "32", "--L", "1",
            "--seq-len", "64", "--steps", "2", "--batch-size", "2",
            "--device", "cpu", "--corpus", str(corpus),
            "--cell-label", "dialogue", "--require-cells", "1",
            "--validation-corpus", str(validation), "--val-every", "0",
            "--answer-ce-weight", "1.0", "--answer-ce-marker", "assistant: ",
            "--answer-ce-all-spans", "--ckpt-out", str(checkpoint_path),
            "--gauges-out", str(summary_path), "--skip-inline-rho",
            "--log-every", "2",
        ],
        cwd=root,
        env={**os.environ, "OMP_NUM_THREADS": "2", "MKL_NUM_THREADS": "2"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    telemetry = summary["answer_ce"]["telemetry"]
    assert summary["answer_ce"] == {
        "weight": 1.0,
        "marker_utf8": "assistant: ",
        "all_spans": True,
        "telemetry": telemetry,
    }
    assert telemetry["complete_trajectory"] is True
    assert telemetry["steps"] == 2
    assert telemetry["active_steps"] == 2
    assert telemetry["positions"] > 0
    assert telemetry["mean_ce"] is not None
