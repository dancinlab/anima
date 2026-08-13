import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_303m_r4_dialogue_scale_2026_08_13"
SPEC = importlib.util.spec_from_file_location("r4_dialogue_scale", HERE / "run_scale.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_changes_only_nested_dialogue_support():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["arms"] == [500, 1500, 3500]
    assert protocol["primary_endpoint"] == 3500
    assert protocol["fixed_recipe"]["parameters"] == 891648
    assert protocol["fixed_recipe"]["dialogue_row_exposure"] == 15000
    assert protocol["bounded_work"]["maximum_new_training_arms"] == 3
    assert protocol["bounded_work"]["vast_ai_allowed"] is False


def test_recorded_primary_endpoint_cannot_promote_failed_conversation():
    result = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
    endpoint = next(arm for arm in result["arms"] if arm.get("primary_endpoint"))
    assert endpoint["documents"] == 3500
    assert endpoint["semantic"] == "0/7"
    assert endpoint["conversation_pass"] is False
    assert result["gate"] is False
    assert result["verdict"] == "FAIL-DIALOGUE-SUPPORT-SCALE"
    assert result["research_reference"]["effect"] == "interpretation constraint only"
    assert result["research_reference"]["consciousness_claim"] is False


def test_scale_reuses_canonical_joint_command(tmp_path):
    command = module.joint.joint_command(
        tmp_path / "out", tmp_path / "broad", tmp_path / "broad-val",
        tmp_path / "dialogue", tmp_path / "dialogue-val", tmp_path / "init", "cpu")
    assert command[command.index("--arch") + 1] == "bytegpt"
    assert command[command.index("--steps") + 1] == "3750"
    assert command[command.index("--answer-ce-mode") + 1] == "additive"
    assert command[command.index("--cell-label") + 1:command.index("--require-cells")] == [
        "broad", "dialogue"]
    assert "--deterministic" in command


def test_runtime_compatible_selector_preserves_source_order(tmp_path):
    source = tmp_path / "dialogue.txt"
    source.write_text(
        "user: first\nassistant: short\n\n"
        "user: second\nassistant: " + "x" * 193 + "\n\n"
        "user: third\nassistant: retained\n",
        encoding="utf-8")
    selected = module.runtime_compatible_documents(source)
    assert selected == [
        "user: first\nassistant: short",
        "user: third\nassistant: retained\n",
    ]
