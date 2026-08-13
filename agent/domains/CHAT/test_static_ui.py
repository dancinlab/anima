from pathlib import Path


STATIC_INDEX = Path(__file__).with_name("static") / "index.html"


def test_mobile_chat_input_does_not_trigger_focus_zoom():
    html = STATIC_INDEX.read_text(encoding="utf-8")

    assert "interactive-widget=resizes-content" in html
    assert "button, input { touch-action: manipulation; }" in html
    assert ".controls input[type=text], .controls input[type=number]" in html
    assert "font-size: 16px;" in html


def test_mobile_zoom_accessibility_is_not_disabled():
    html = STATIC_INDEX.read_text(encoding="utf-8")

    assert "user-scalable=no" not in html
    assert "maximum-scale=1" not in html
