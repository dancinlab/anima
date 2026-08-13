import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_303m_r4_exposure_ladder_2026_08_13"
SPEC = importlib.util.spec_from_file_location("r4_exposure_ladder", HERE / "run_exposure.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_changes_only_exposure_on_one_trajectory():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    assert protocol["fixed_data"]["documents"] == 3500
    assert protocol["fixed_recipe"]["parameters"] == 891648
    assert protocol["trajectory"]["evaluated_steps"] == [3750, 7500, 15000, 30000]
    assert protocol["trajectory"]["dialogue_row_exposure"] == [15000, 30000, 60000, 120000]
    assert protocol["trajectory"]["primary_step"] == 30000
    assert protocol["bounded_work"]["maximum_new_training_trajectories"] == 1
    assert protocol["bounded_work"]["vast_ai_allowed"] is False


def test_command_reuses_native_joint_recipe(tmp_path):
    command = module.exposure_command(
        tmp_path / "out", tmp_path / "broad", tmp_path / "broad-val",
        tmp_path / "dialogue", tmp_path / "dialogue-val", tmp_path / "init", "cpu")
    assert command[command.index("--steps") + 1] == "30000"
    assert command[command.index("--ckpt-every") + 1] == "3750"
    assert command[command.index("--answer-ce-mode") + 1] == "additive"
    assert command[command.index("--cell-label") + 1:command.index("--require-cells")] == [
        "broad", "dialogue"]
    assert "--deterministic" in command


def test_control_reproduction_is_fail_closed():
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    good = {
        "broad_validation": {"ce": protocol["control_reproduction"]["prior_broad_ce"]},
        "dialogue_validation": {
            "assistant_turn": {"ce": protocol["control_reproduction"]["prior_heldout_assistant_ce"]}
        },
        "conversation": {"summary": {"by_language": {"en": {
            "semantic_passes": 0, "structural_passes": 0}}}},
    }
    assert module.control_reproduced(good, protocol["control_reproduction"])
    bad = json.loads(json.dumps(good))
    bad["dialogue_validation"]["assistant_turn"]["ce"] += 0.031
    assert not module.control_reproduced(bad, protocol["control_reproduction"])


def test_recorded_endpoint_cannot_promote_failed_conversation():
    result = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
    endpoint = next(point for point in result["points"] if point.get("primary_endpoint"))
    assert result["control_reproduced"] is True
    assert endpoint["dialogue_rows"] == 120000
    assert endpoint["semantic"] == "0/7"
    assert endpoint["conversation_pass"] is False
    assert result["gate"] is False
    assert result["verdict"] == "FAIL-FIXED-CAPACITY-AFTER-EXPOSURE"
    assert result["hf_custody"]["sha256_mismatches"] == 0
