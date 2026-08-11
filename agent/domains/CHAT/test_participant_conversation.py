#!/usr/bin/env python3
"""Regression coverage for user-turn ownership in the autonomous participant."""
from __future__ import annotations

import pathlib
import sys
import time

import pytest

torch = pytest.importorskip("torch")

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from anima_participant import AnimaState, SEED_STRATEGIES  # noqa: E402
from substrate_lora import _chat_messages  # noqa: E402


class _Substrate:
    def entropy_of_next(self, _text):
        return 0.5, torch.zeros(4)


def test_canonical_chat_messages_add_no_system_prompt():
    messages = _chat_messages("한글 가능해?")

    assert messages == [
        {"role": "system", "content": ""},
        {"role": "user", "content": "한글 가능해?"},
    ]


def test_every_autonomous_strategy_keeps_pending_user_context():
    state = AnimaState(_Substrate())
    state.ingest_user_msg({
        "id": "turn-1", "sender": "user", "sender_id": "user-1",
        "text": "한글 가능해?", "lang": "ko", "ts": time.time(),
    })
    observed = []
    for tick in range(len(SEED_STRATEGIES)):
        state.ticks = tick
        observed.append(state._seed_text())

    assert [seed for seed, _ in observed] == ["한글 가능해?"] * len(SEED_STRATEGIES)
    assert not state.recent_embeds
    decision = state.tick(0.0)
    assert decision["factors"]["info_gap"] == 1.0
    assert decision["reply_to"] == "turn-1"
    assert decision["reply_lang"] == "ko"


def test_pending_user_turns_are_replied_in_fifo_order():
    state = AnimaState(_Substrate())
    state.ingest_user_msg({
        "id": "turn-ko", "sender": "ko-user", "text": "한글 가능해?", "lang": "ko",
    })
    state.ingest_user_msg({
        "id": "turn-en", "sender": "en-user", "text": "What is consciousness?",
        "lang": "en",
    })

    first = state.tick(0.0)
    assert first["seed_text"] == "한글 가능해?"
    assert first["reply_to"] == "turn-ko"
    assert first["reply_lang"] == "ko"
    state.acknowledge_reply("turn-ko")
    second = state.tick(0.0)
    assert second["seed_text"] == "What is consciousness?"
    assert second["reply_to"] == "turn-en"
    assert second["reply_lang"] == "en"


def test_broker_history_is_context_but_not_a_pending_reply():
    state = AnimaState(_Substrate())
    state.ingest_user_msg({
        "id": "history-turn", "sender": "old-user", "text": "old context", "lang": "en",
    }, pending=False)

    assert state.pending_reply() is None
    assert state.m_buffer[-1]["text"] == "old context"


def test_pending_turn_is_not_blocked_by_self_monologue_refractory(monkeypatch):
    monkeypatch.setenv("ANIMA_SLEEP_HOURS", "00:00-00:00")
    state = AnimaState(_Substrate())
    state.last_emit_time = time.time()
    state.ingest_user_msg({
        "id": "live-turn", "sender": "user", "text": "한글 가능해?", "lang": "ko",
    })

    decision = state.tick(0.0)

    assert not decision["in_refractory"]
    assert decision["threshold"] == pytest.approx(0.30)
