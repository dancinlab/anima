import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_303m_r4_full_ce_curriculum_2026_08_13"
SPEC = importlib.util.spec_from_file_location("r4_full_ce_curriculum", HERE / "run_curriculum.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_keeps_single_new_training_arm_and_blocked_release():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["bounded_work"]["maximum_new_training_arms"] == 1
    assert protocol["bounded_work"]["303m_training"] == "blocked"
    assert protocol["language_phase"]["objective"] == "full next-byte CE"
    assert protocol["turn_phase"]["chat_frame_alignment"] == "document"


def test_train_command_changes_only_curriculum_stage(tmp_path):
    broad = module.train_command(tmp_path / "broad", tmp_path / "train", tmp_path / "val",
                                 steps=2000, device="cpu")
    turn = module.train_command(tmp_path / "turn", tmp_path / "dialogue", tmp_path / "heldout",
                                steps=1875, device="cpu", init=tmp_path / "broad.bin",
                                dialogue=True)
    assert "--answer-ce-mode" not in broad
    assert turn[turn.index("--answer-ce-mode") + 1] == "turn-only"
    assert turn[turn.index("--chat-frame-alignment") + 1] == "document"
    assert turn[turn.index("--init") + 1].endswith("broad.bin")
    assert "--deterministic" in broad and "--deterministic" in turn
