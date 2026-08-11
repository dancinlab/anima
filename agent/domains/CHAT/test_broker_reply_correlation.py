#!/usr/bin/env python3
"""Multi-user reply ownership regression for the chat broker."""
from __future__ import annotations

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import broker  # noqa: E402


def test_anima_reply_is_bound_to_existing_user_turn():
    broker.STATE.user_turns.clear()
    turn = {
        "id": "turn-1", "kind": "user", "sender": "alice",
        "sender_id": "user-1", "text": "한글 가능해?",
    }
    broker.STATE.user_turns[turn["id"]] = turn

    assert broker.resolve_reply_turn("turn-1") is turn


def test_anima_cannot_spoof_unknown_reply_target():
    broker.STATE.user_turns.clear()

    assert broker.resolve_reply_turn("missing-turn") is None
    assert broker.resolve_reply_turn(None) is None
