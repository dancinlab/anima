import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_303m_r4_low_lr_sft_2026_08_13"
SPEC = importlib.util.spec_from_file_location("r4_low_lr_sft", HERE / "run_low_lr.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_changes_only_turn_lr_and_keeps_release_blocked():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["fixed_turn_change"] == {
        "control_peak_lr": 0.001, "treatment_peak_lr": 0.0001, "ratio": 0.1}
    assert protocol["bounded_work"]["maximum_new_training_arms"] == 1
    assert protocol["bounded_work"]["production"] == "blocked"


def test_shared_command_accepts_preregistered_transfer_lr(tmp_path):
    command = module.curriculum.train_command(
        tmp_path / "out", tmp_path / "train", tmp_path / "val", steps=1875,
        device="cpu", init=tmp_path / "language.bin", dialogue=True, peak_lr=0.0001)
    assert command[command.index("--lr") + 1] == "0.0001"
    assert command[command.index("--answer-ce-mode") + 1] == "turn-only"
    assert command[command.index("--chat-frame-alignment") + 1] == "document"
