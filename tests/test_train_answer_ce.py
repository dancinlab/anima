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
def test_chat_turn_mask_keeps_internal_newline_and_boundary_not_user_content():
    import torch

    train = _import_train()
    raw = (b"user: first question\nassistant: first line\nsecond line\n"
           b"user: next question\nassistant: final\nuser: last question")
    targets = torch.tensor([list(raw)], dtype=torch.long)

    mask = train.chat_turn_position_mask(targets, b"assistant: ")

    assert bytes(targets[0][mask[0]].tolist()) == (
        b"first line\nsecond line\nuser: final\nuser: ")
    assert not mask[0][raw.index(b"next question")]
    assert not mask[0][raw.index(b"last question")]


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_answer_marker_must_not_be_empty():
    import torch

    train = _import_train()
    targets = torch.tensor([[1, 2, 3]], dtype=torch.long)

    with pytest.raises(ValueError, match="must not be empty"):
        train.answer_position_mask(targets, marker=b"", all_spans=True)


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_chat_framed_sampler_keeps_prompt_and_response_in_one_window(tmp_path):
    import torch

    train = _import_train()
    document = b"user: remember blue\nassistant: noted\nuser: what color?\nassistant: blue"
    corpus = tmp_path / "dialogue.txt"
    corpus.write_bytes(b"general text\n\n" + document + b"\n\nmore text\n\n")
    cell = train.ByteCell(str(corpus))
    try:
        cell.configure_chat_frames(96, b"assistant: ")
        start, framed = cell.framed_window_spec(
            96, torch.Generator().manual_seed(7))
        x, y = cell.materialize(start, 96)
        visible = bytes(x.tolist()) + bytes([int(y[-1])])
        assert framed
        assert len(cell.chat_frame_spans) == 1
        assert document in visible
    finally:
        cell.close()


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_bytegpt_bridge_metadata_uses_actual_step_and_validation_ce():
    train = _import_train()
    model = train.ByteGPT(train.ByteGPTConfig(
        vocab=256, d=16, n_layer=1, n_head=4, block=32))

    payload = train.bytegpt_bridge_payload(model, 2000, 1.234567, 123)

    assert payload["step"] == 2000
    assert payload["val_ce"] == 1.23457
    assert payload["nparam"] == 123


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_canonical_cli_records_chat_answer_telemetry(tmp_path):
    root = Path(__file__).resolve().parents[1]
    corpus = tmp_path / "dialogue.train.txt"
    validation = tmp_path / "dialogue.validation.txt"
    dialogue = ("user: one\nassistant: first\n\n"
                "user: two\nassistant: second\n\n") * 100
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
            "--answer-ce-all-spans", "--chat-framed-sampling",
            "--ckpt-out", str(checkpoint_path),
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
        "mode": "additive",
        "marker_utf8": "assistant: ",
        "all_spans": True,
        "chat_framed_sampling": True,
        "telemetry": telemetry,
    }
    assert telemetry["complete_trajectory"] is True
    assert telemetry["steps"] == 2
    assert telemetry["active_steps"] == 2
    assert telemetry["positions"] > 0
    assert telemetry["mean_ce"] is not None
    sampled = summary["sampling"]["per_cell"]["dialogue"]
    assert sampled["sampled_framed_windows"] == 4
    assert sampled["eligible_chat_documents"] > 0


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_response_only_ce_has_zero_prompt_gradient():
    import torch

    train = _import_train()
    raw = b"user: question\nassistant: answer\n"
    targets = torch.tensor([list(raw)], dtype=torch.long)

    class StubMouth(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.rows = torch.nn.Parameter(torch.zeros(1, 256, len(raw)))

        def forward(self, _x, y=None):
            logits = self.rows
            ce = torch.nn.functional.cross_entropy(
                logits.transpose(1, 2).reshape(-1, 256), targets.reshape(-1))
            return {"logits": logits, "ce_loss": ce,
                    "aux_loss": logits.new_zeros(())}

    mouth = StubMouth()
    shell = train.TrainShell(
        mouth, train.loss_ce_marginal, None, is_bytegpt=True, V=256,
        obj_needs_pen=False, dict_on=False, jamo_on=False, bf16=False,
        device="cpu")
    loss, _, aux = shell(
        targets, targets, torch.Generator().manual_seed(7), 0.0, 0.0,
        ans_w=1.0, ans_marker=b"assistant: ", ans_all_spans=True,
        ans_mode="only")
    loss.backward()

    mask = train.answer_position_mask(
        targets, marker=b"assistant: ", all_spans=True)
    prompt_grad = mouth.rows.grad.transpose(1, 2)[~mask]
    response_grad = mouth.rows.grad.transpose(1, 2)[mask]
    assert aux["ans_n"] == len(b"answer")
    assert int(torch.count_nonzero(prompt_grad)) == 0
    assert int(torch.count_nonzero(response_grad)) == len(b"answer") * 256


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_response_only_ce_fails_without_supervised_bytes():
    import torch

    train = _import_train()
    targets = torch.tensor([list(b"user: question only")], dtype=torch.long)

    class StubMouth(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.rows = torch.nn.Parameter(torch.zeros(1, 256, targets.shape[1]))

        def forward(self, _x, y=None):
            logits = self.rows
            ce = torch.nn.functional.cross_entropy(
                logits.transpose(1, 2).reshape(-1, 256), targets.reshape(-1))
            return {"logits": logits, "ce_loss": ce,
                    "aux_loss": logits.new_zeros(())}

    shell = train.TrainShell(
        StubMouth(), train.loss_ce_marginal, None, is_bytegpt=True, V=256,
        obj_needs_pen=False, dict_on=False, jamo_on=False, bf16=False,
        device="cpu")
    with pytest.raises(RuntimeError, match="no supervised assistant bytes"):
        shell(targets, targets, torch.Generator().manual_seed(7), 0.0, 0.0,
              ans_w=1.0, ans_marker=b"assistant: ", ans_all_spans=True,
              ans_mode="only")


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_turn_only_ce_has_no_following_user_content_gradient():
    import torch

    train = _import_train()
    raw = b"user: q\nassistant: answer\nuser: hidden prompt"
    targets = torch.tensor([list(raw)], dtype=torch.long)

    class StubMouth(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.rows = torch.nn.Parameter(torch.zeros(1, 256, len(raw)))

        def forward(self, _x, y=None):
            logits = self.rows
            ce = torch.nn.functional.cross_entropy(
                logits.transpose(1, 2).reshape(-1, 256), targets.reshape(-1))
            return {"logits": logits, "ce_loss": ce,
                    "aux_loss": logits.new_zeros(())}

    mouth = StubMouth()
    shell = train.TrainShell(
        mouth, train.loss_ce_marginal, None, is_bytegpt=True, V=256,
        obj_needs_pen=False, dict_on=False, jamo_on=False, bf16=False,
        device="cpu")
    loss, _, _ = shell(
        targets, targets, torch.Generator().manual_seed(7), 0.0, 0.0,
        ans_w=1.0, ans_marker=b"assistant: ", ans_all_spans=True,
        ans_mode="turn-only")
    loss.backward()

    mask = train.chat_turn_position_mask(targets, b"assistant: ")
    grad = mouth.rows.grad.transpose(1, 2)
    assert bytes(targets[0][mask[0]].tolist()) == b"answer\nuser: "
    assert int(torch.count_nonzero(grad[~mask])) == 0
    assert int(torch.count_nonzero(grad[mask])) == int(mask.sum()) * 256


@pytest.mark.skipif(not TORCH_AVAILABLE, reason="PyTorch training extra is not installed")
def test_chat_framed_sampling_is_available_to_base_ce_control(tmp_path):
    root = Path(__file__).resolve().parents[1]
    corpus = tmp_path / "dialogue.train.txt"
    dialogue = ("user: one\nassistant: first\n\n"
                "user: two\nassistant: second\n\n") * 20
    corpus.write_text(dialogue, encoding="utf-8")
    summary_path = tmp_path / "summary.json"

    completed = subprocess.run(
        [
            sys.executable, str(root / "cli" / "train.py"),
            "--arch", "bytegpt", "--d", "32", "--L", "1",
            "--seq-len", "64", "--steps", "1", "--batch-size", "2",
            "--device", "cpu", "--corpus", str(corpus),
            "--cell-label", "dialogue", "--require-cells", "1",
            "--chat-framed-sampling", "--answer-ce-marker", "assistant: ",
            "--val-every", "0",
            "--gauges-out", str(summary_path), "--skip-inline-rho",
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
    assert summary["answer_ce"] is None
    sampled = summary["sampling"]["per_cell"]["dialogue"]
    assert sampled["sampled_framed_windows"] == 2
    assert sampled["eligible_chat_documents"] > 0
