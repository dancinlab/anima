"""5-verb spec inventory tests."""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


VERB_FILES = [
    ("dream",  "dream/hexa-dream.md"),
    ("ear",    "ear/hexa-ear.md"),
    ("empath", "empath/hexa-empath.md"),
    ("olfact", "olfact/hexa-olfact.md"),
    ("voice",  "voice/hexa-voice.md"),
]


@pytest.mark.auto
@pytest.mark.parametrize("verb,relpath", VERB_FILES, ids=[v for v, _ in VERB_FILES])
def test_each_verb_spec_present_with_canonical(verb, relpath):
    path = ROOT / relpath
    assert path.exists(), f"missing: {relpath}"
    head = path.read_text(encoding="utf-8")[:1024]
    assert "@canonical" in head, f"{relpath}: no @canonical"
    assert "canon@" in head


@pytest.mark.auto
def test_total_count_is_5():
    assert len(VERB_FILES) == 5


@pytest.mark.auto
def test_voice_renamed_marker():
    """voice/hexa-voice.md must declare its hexa-speak rename + formulaic constraint."""
    p = ROOT / "voice/hexa-voice.md"
    text = p.read_text(encoding="utf-8")[:2048]
    assert "@renamed" in text
    assert "FORBIDDEN" in text


@pytest.mark.auto
def test_voice_canonical_points_to_hexa_speak():
    """The upstream canonical should still resolve to hexa-speak (rename is local)."""
    p = ROOT / "voice/hexa-voice.md"
    head = p.read_text(encoding="utf-8")[:512]
    assert "hexa-speak" in head
