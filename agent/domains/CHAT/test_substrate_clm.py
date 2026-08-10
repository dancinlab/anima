#!/usr/bin/env python3
"""Regression coverage for the canonical CLM chat substrate adapter."""
from __future__ import annotations

import pathlib
import sys

import pytest

pytest.importorskip("torch")

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from substrate_clm import CLMSubstrate, _websocket_text  # noqa: E402


FIXTURE = ROOT / "archive" / "state" / "lane_p_clm_gen" / "clm_d768_gen.clm"


def test_clm_substrate_uses_real_decode_path():
    substrate = CLMSubstrate(str(FIXTURE))
    entropy, embedding = substrate.entropy_of_next("the mind")
    text = substrate.generate("the mind", max_new=4)

    assert substrate.name == "clm"
    assert substrate.vocab_size == 256
    assert substrate.param_count() > 0
    assert 0.0 <= entropy <= 1.0
    assert embedding.ndim == 1
    assert isinstance(text, str)
    text.encode("utf-8", "strict")


def test_clm_substrate_rejects_missing_or_unknown_checkpoint(tmp_path):
    with pytest.raises(ValueError, match="ANIMA_CLM_CKPT"):
        CLMSubstrate("")
    with pytest.raises(FileNotFoundError):
        CLMSubstrate(str(tmp_path / "missing.clm"))
    bad = tmp_path / "bad.clm"
    bad.write_bytes(b"not-a-clm")
    with pytest.raises(ValueError, match="not a decodable"):
        CLMSubstrate(str(bad))


def test_websocket_text_replaces_only_invalid_utf8_bytes():
    raw = b"ok\xff\xed\xa0\x80"
    surrogate_text = raw.decode("utf-8", "surrogateescape")
    safe = _websocket_text(surrogate_text)
    assert safe.startswith("ok")
    assert "\ufffd" in safe
    safe.encode("utf-8", "strict")
