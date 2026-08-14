import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_native_303m_replay_recovery_2026_08_14"
SPEC = importlib.util.spec_from_file_location("native_replay_recovery", HERE / "run_recovery.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_is_single_mixed_replay_arm_and_blocks_release():
    protocol = module.load_protocol()
    recipe = protocol["fixed_recipe"]
    assert recipe["maximum_training_arms"] == 1
    assert recipe["source_mode"] == "mixed"
    assert recipe["general_fraction"] + recipe["dialogue_fraction"] == 1.0
    assert recipe["endpoint_step"] - recipe["base_step"] == recipe["new_optimizer_steps"]
    assert protocol["bounded_work"]["result_dependent_extension"] is False
    assert protocol["bounded_work"]["participant_mount"].startswith("blocked")
    assert protocol["bounded_work"]["production"] == "blocked"


def test_instrument_controls_reject_contradiction_and_korean_substring():
    controls = module.conversation_scorer_controls_result(module.load_protocol())
    assert controls["pass"] is True
    assert len(controls["rows"]) == 8
    assert all(row["pass"] for row in controls["rows"])


def test_training_command_reuses_mixed_response_path(tmp_path: Path):
    protocol = module.load_protocol()
    model = tmp_path / "model"
    data = tmp_path / "data"
    target = data / "data-conversation-target"
    model.mkdir(); target.mkdir(parents=True)
    (data / "manifest.json").write_text(json.dumps({"splits": {
        "train_general": ["general.train"],
        "validation_general": ["general.validation"],
    }}), encoding="utf-8")
    (target / "manifest.json").write_text(json.dumps({"splits": {
        "train_dialogue": ["dialogue.train"],
        "validation_dialogue": ["dialogue.validation"],
    }}), encoding="utf-8")
    command = module.training_command(protocol, model, data, tmp_path / "out", "python")
    assert "--response-only" in command
    assert "--dialogue-only" not in command
    assert command[command.index("--steps") + 1] == "40000"
    assert command.count("--train-general") == 1
    assert command.count("--train-dialogue") == 1
