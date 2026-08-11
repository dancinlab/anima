#!/usr/bin/env python3
"""Regression coverage for the live user-turn conversation gate."""
from staging_probe import _reply_contract


def test_reply_contract_rejects_whitespace_and_repetitive_language_drift():
    assert not _reply_contract("한글 가능해?", "   ")["passed"]
    assert not _reply_contract(
        "한글 가능해?",
        "en en el control de la construcción de la construcción de la construcción d",
    )["passed"]


def test_reply_contract_accepts_visible_language_aligned_response():
    result = _reply_contract("한글 가능해?", "네, 한글로 대화할 수 있어요.")
    assert result["passed"]
    assert result["language_aligned"]


def test_reply_contract_rejects_irrelevant_korean_answer():
    result = _reply_contract("한글 가능해?", "맞아요. 그래서 컨텍스트 길이가 중요해요.")
    assert result["language_aligned"]
    assert not result["semantic_alignment"]
    assert not result["passed"]


def test_reply_contract_requires_consciousness_semantics():
    bad = _reply_contract("What is consciousness?", "The weather is pleasant today.")
    good = _reply_contract(
        "What is consciousness?",
        "Consciousness is the subjective experience of awareness.",
    )
    assert not bad["passed"]
    assert good["passed"]
