from __future__ import annotations

import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
for path in (ROOT / "cli", ROOT / "core"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import evaluate  # noqa: E402
import generator  # noqa: E402


PANEL = (ROOT / "state" / "anima_303m_r0_conversation_2026_08_12" /
         "conversation_panel.json")


def _turn(panel: dict, item_id: str, turn_index: int = 0):
    return evaluate._conversation_find_turn(panel, item_id, turn_index)


def test_registered_scorer_controls_certify_before_model_read():
    panel = evaluate._conversation_panel_load(str(PANEL))

    result = evaluate.conversation_scorer_controls(panel)

    assert result["pass"]
    assert len(result["rows"]) == 4
    assert all(row["pass"] for row in result["rows"])


def test_meaningful_answer_passes_relevance_and_surface_checks():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "en_ice")

    result = evaluate.score_conversation_response(
        turn["user"],
        "The ice melts into water because sunlight transfers heat to it.",
        turn,
        item["lang"],
        panel["bars"],
    )

    assert result["pass"]
    assert result["structural_pass"]
    assert result["semantic_pass"]


def test_repetitive_wrong_language_output_is_rejected():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "en_consciousness")

    result = evaluate.score_conversation_response(
        turn["user"],
        "en en el control de la construcción de la construcción de la construcción.",
        turn,
        item["lang"],
        panel["bars"],
    )

    assert not result["pass"]
    assert not result["semantic_pass"]
    assert (not result["structural"]["language"] or
            not result["structural"]["repetition"])


def test_unrelated_generic_korean_output_is_rejected():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "ko_ice")

    result = evaluate.score_conversation_response(
        turn["user"],
        "맞아요. 그래서 컨텍스트 길이가 중요해요.",
        turn,
        item["lang"],
        panel["bars"],
    )

    assert result["structural_pass"]
    assert not result["semantic_pass"]
    assert not result["pass"]


def test_invalid_byte_output_is_retained_but_fails_utf8():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "en_ice")
    raw = b"ice melts from heat.\xff".decode("utf-8", "surrogateescape")

    result = evaluate.score_conversation_response(
        turn["user"], raw, turn, item["lang"], panel["bars"], raw_text=raw)

    assert not result["structural"]["utf8"]
    assert not result["pass"]


def test_correction_rejects_stale_fact():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "en_correction", 1)

    stale = evaluate.score_conversation_response(
        turn["user"], "Your favorite color is green.", turn, item["lang"], panel["bars"])
    corrected = evaluate.score_conversation_response(
        turn["user"], "Your favorite color is purple.", turn, item["lang"], panel["bars"])

    assert not stale["pass"]
    assert stale["forbidden_hits"] == ["green"]
    assert corrected["pass"]


def test_runtime_turn_framing_stops_before_synthetic_next_user():
    raw = "A clear answer.\nuser: a synthetic next turn"

    result = generator.gen_chat_turn_text(raw)

    assert result["text"] == "A clear answer."
    assert result["stopped"]
    assert result["stop_marker"] == "\nuser:"
    assert result["raw_text"] == raw


def test_panel_json_is_stable_and_has_expected_response_counts():
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    counts = {lang: 0 for lang in ("en", "ko")}
    finals = 0
    for item in panel["items"]:
        counts[item["lang"]] += len(item["turns"])
        finals += sum(bool(turn.get("multiturn_final")) for turn in item["turns"])

    assert counts == {"en": 7, "ko": 7}
    assert finals == 4
    assert panel["template"]["system_prompt"] is False
