from __future__ import annotations

import json
import pathlib
import sys

import pytest


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


def test_semantic_keywords_inside_contradiction_do_not_pass():
    panel = evaluate._conversation_panel_load(str(PANEL))
    item, turn = _turn(panel, "en_ice")

    result = evaluate.score_conversation_response(
        turn["user"],
        "Ice does not melt in sunlight, although water and heat are words here.",
        turn, item["lang"], panel["bars"])

    assert not result["semantic_pass"]
    assert not result["pass"]


def test_korean_required_term_is_not_an_arbitrary_substring():
    assert not evaluate._conversation_term_present("자동차입니다.", "차")
    assert evaluate._conversation_term_present("차가 있습니다.", "차")


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


def test_panel_retains_invalid_bytes_across_multiturn_seed(monkeypatch, tmp_path):
    raw = b"broken byte: \xeb".decode("utf-8", "surrogateescape")

    class InvalidByteMouth:
        def __init__(self, _checkpoint):
            self.kind = "test-byte-mouth"

        def chat(self, _seed, _max_new, _stop_markers):
            return {"text": raw, "raw_text": raw, "stopped": False,
                    "stop_marker": None}

    monkeypatch.setattr(evaluate, "_Mouth", InvalidByteMouth)
    output = tmp_path / "conversation.json"
    checkpoint = tmp_path / "unused.bin"
    checkpoint.write_bytes(b"test checkpoint")

    status = evaluate.conversation_panel_run([
        str(checkpoint), "--conversation-panel", str(PANEL), "--out", str(output)])
    result = json.loads(output.read_text(encoding="utf-8"))

    assert status == 1
    assert len(result["responses"]) == 14
    memory_rows = [row for row in result["responses"] if row["item_id"] == "en_memory"]
    assert len(memory_rows) == 2
    assert memory_rows[1]["seed_bytes"] > memory_rows[0]["seed_bytes"]
    assert all(not row["score"]["structural"]["utf8"] for row in memory_rows)


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


@pytest.mark.parametrize("marker", ["\n USER :", "\n사용자 :", "\n<|USER|> :"])
def test_runtime_turn_parser_rejects_role_spacing_and_case_variants(marker):
    raw = "A clear answer." + marker + " fabricated next turn"

    result = generator.gen_chat_turn_text(raw)

    assert result["text"] == "A clear answer."
    assert result["stopped"]


def test_panel_template_must_match_runtime_ssot(tmp_path):
    panel = json.loads(PANEL.read_text(encoding="utf-8"))
    panel["template"]["assistant_prefix"] = "도우미: "
    changed = tmp_path / "changed.json"
    changed.write_text(json.dumps(panel, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match="canonical SSOT"):
        evaluate._conversation_panel_load(str(changed))


def test_panel_sha_mismatch_fails_before_checkpoint_load(tmp_path):
    output = tmp_path / "result.json"

    status = evaluate.conversation_panel_run([
        str(tmp_path / "missing.bin"), "--conversation-panel", str(PANEL),
        "--conversation-panel-sha256", "0" * 64, "--out", str(output)])

    assert status == 4
    assert not output.exists()


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
