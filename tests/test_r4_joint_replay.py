import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_303m_r4_joint_replay_2026_08_13"
SPEC = importlib.util.spec_from_file_location("r4_joint_replay", HERE / "run_joint.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_matches_dialogue_exposure_and_blocks_release():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    recipe = protocol["fixed_recipe"]
    assert recipe["steps"] * recipe["rows_per_step_per_cell"] == 1875 * 8
    assert recipe["sample"] == "roundrobin"
    assert protocol["bounded_work"]["maximum_new_training_arms"] == 1
    assert protocol["bounded_work"]["production"] == "blocked"


def test_joint_command_uses_native_two_cell_additive_path(tmp_path):
    command = module.joint_command(
        tmp_path / "out", tmp_path / "broad.train", tmp_path / "broad.val",
        tmp_path / "dialogue.train", tmp_path / "dialogue.val",
        tmp_path / "language.bin", "cpu")
    assert command[command.index("--sample") + 1] == "roundrobin"
    assert command[command.index("--answer-ce-mode") + 1] == "additive"
    assert command[command.index("--chat-frame-alignment") + 1] == "document"
    assert command.count("--cell-label") == 2
    assert command[command.index("--steps") + 1] == "3750"
