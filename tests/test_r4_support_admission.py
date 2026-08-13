import json
from pathlib import Path

from core import generator


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (ROOT / "state/anima_303m_r4_support_admission_2026_08_13" /
            "protocol.json")


def test_support_admission_protocol_is_single_axis_and_bounded():
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    arms = protocol["admission_arms"]

    assert [arm["label"] for arm in arms] == [
        "CONTROL-3500", "SHORT-COMPLETE", "ALL-COMPLETE"]
    assert [arm["multiturn"] for arm in arms] == [0, 1010, 1194]
    assert sum(bool(arm.get("primary")) for arm in arms) == 1
    assert protocol["fixed_model"]["parameters"] == 2817024
    assert protocol["fixed_recipe"]["dialogue_rows"] == 120000
    assert protocol["bounded_work"]["maximum_new_joint_trajectories"] == 3
    assert protocol["bounded_work"]["h100_allowed"] is False
    assert protocol["bounded_work"]["303m_training"] == "blocked"


def test_canonical_parser_exposes_last_exchange_without_dropping_history():
    turns = [
        ("user", "Remember red."),
        ("assistant", "Noted."),
        ("user", "What should you remember?"),
        ("assistant", "Red."),
    ]
    document = generator.gen_chat_render_turns(turns)
    parsed = generator.gen_chat_parse_turns(document)

    assert parsed == turns
    assert len(parsed) == 4
    assert parsed[-2:] == turns[-2:]
