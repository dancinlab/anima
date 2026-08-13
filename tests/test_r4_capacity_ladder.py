import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state/anima_303m_r4_capacity_ladder_2026_08_13"


def _load_runner():
    spec = importlib.util.spec_from_file_location("r4_capacity", STATE / "run_capacity.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_capacity_protocol_changes_only_registered_shape():
    protocol = json.loads((STATE / "protocol.json").read_text())
    assert protocol["fixed_data"]["documents"] == 3500
    assert protocol["fixed_recipe"]["joint_phase"]["dialogue_rows"] == 120000
    assert protocol["bounded_work"]["h100_allowed"] is False
    assert [arm["parameters"] for arm in protocol["capacity_arms"]] == [2817024, 10110080, 29316224]
    assert sum(bool(arm.get("primary")) for arm in protocol["capacity_arms"]) == 1


def test_capacity_commands_share_recipe_and_native_head_geometry(tmp_path):
    runner = _load_runner()
    protocol = json.loads((STATE / "protocol.json").read_text())
    paths = [tmp_path / name for name in ("bt", "bv", "dt", "dv", "init")]
    for arm in protocol["capacity_arms"]:
        language = runner.language_command(tmp_path / "language", paths[0], paths[1], arm,
                                           protocol["fixed_recipe"], "cpu")
        joint = runner.joint_command(tmp_path / "joint", paths[0], paths[1], paths[2], paths[3],
                                     paths[4], arm, protocol["fixed_recipe"], "cpu")
        for command in (language, joint):
            assert command[command.index("--d") + 1] == str(arm["d"])
            assert command[command.index("--L") + 1] == str(arm["layers"])
            assert "--canon" in command
        assert language[language.index("--steps") + 1] == "2000"
        assert joint[joint.index("--steps") + 1] == "30000"
        assert joint[joint.index("--lr-decay-steps") + 1] == "3750"
        assert arm["d"] // arm["heads"] == protocol["fixed_recipe"]["head_dimension"]
