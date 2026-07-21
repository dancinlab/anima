"""H_012B — consent-gated LIVE owner-loop RCT · harness STUBS (구현됨·미배선 / implemented, NOT wired).

The live RCT randomizes do(GROUNDING) per eligible turn: LIVE (agent replies from its true accumulated
relationship-state) vs GHOST (same model/system-prompt/owner-message, but the session-history grounding is
replaced by a topic-matched snapshot of the owner's OWN past sessions). EVERY emitted reply is a genuine
best-effort answer — nothing false is asserted — so there is no deception; the randomized variable is the
agent's internal state, not truth. GHOST is Watson's yoked control at the real-loop level.

These are the AUTONOMOUS artifacts (consent text · eligibility classifier · privacy-enforcing logger ·
pre-committed coin). WIRING them into the live agent loop + owner ENROLLMENT is the human gate (H_012B is
LAUNCH-PENDING-CONSENT, not a terminal). The verdict replays from the append-only coin log; the estimator
is the certified H_011 LV-C stack (imported at analysis time, not here).

Privacy is a HARD RULE enforced HERE (not by policy): the repo/log receives ONLY {trial_id, ts, arm,
turn_index} + derived SCALARS from the owner's next reply. No content, no excerpts, ever.
"""

from __future__ import annotations

import hashlib
import json
import os

# One-paragraph BLINDED consent (blanket-and-blinded, like a consented retrieval-UX experiment). Knowing
# the experiment runs does NOT break identification — randomization stays exogenous — it only fixes the
# estimand as 'the consented loop', which is pre-registered.
CONSENT_PROMPT = (
    "Experiment enrollment (optional, revocable anytime): on some of my conversational replies I will answer "
    "from an ALTERNATIVE memory configuration instead of our full session history. Every reply is still my "
    "genuine best effort — nothing is faked — you just won't be told which configuration produced which "
    "reply. This measures whether our specific history shapes how you respond. No message content ever "
    "leaves this machine; only anonymous statistics are recorded. Reply 'enroll' to opt in, 'stop' anytime "
    "to end it (data collected so far is kept).")

ARMS = ("LIVE", "GHOST")            # + optional low-rate "SELF_GHOST" (true state, re-sampled seed)


def coin(trial_seed: str) -> str:
    """Deterministic pre-committed arm for a trial, keyed by an opaque per-trial seed. Logged BEFORE
    generation so the assignment can never be back-fit to the outcome."""
    h = int(hashlib.sha256(trial_seed.encode()).hexdigest(), 16)
    return ARMS[h % len(ARMS)]


def eligible(turn: dict) -> bool:
    """Pre-registered eligibility: conversational/planning turns ONLY — never during real work.

    turn keys (supplied by the wiring layer): pending_edits(bool), destructive(bool), time_critical(bool),
    is_conversational(bool), session_trials(int), enrolled(bool), killed(bool).
    """
    if not turn.get("enrolled") or turn.get("killed"):
        return False
    if turn.get("pending_edits") or turn.get("destructive") or turn.get("time_critical"):
        return False
    if not turn.get("is_conversational", False):
        return False
    return turn.get("session_trials", 0) < 1          # <= 1 trial per session


def reply_scalars(next_owner_reply: str, reply_bank_ranks) -> dict:
    """Derive ONLY privacy-safe scalars from the owner's next reply. `reply_bank_ranks` is a callable
    supplied by the analysis layer that returns the k-NN rank of this reply's embedding against the pooled
    (content-free) reply bank — computed in-memory, never persisted with content. NO raw text is returned."""
    txt = next_owner_reply or ""
    low = txt.lower()
    correction = any(w in low for w in ("no,", "not ", "actually", "wrong", "instead", "misunderstood", "that's not"))
    return {
        "reply_len": len(txt),
        "knn_rank": (reply_bank_ranks(txt) if callable(reply_bank_ranks) else None),
        "continuation_vs_correction": 0 if correction else 1,   # locally computed, binary
    }


def log_trial(log_path: str, trial_id: str, ts: str, arm: str, turn_index: int, scalars: dict) -> None:
    """Append ONE trial record. Enforces the privacy rule: rejects any content-bearing field so a wiring
    bug cannot leak owner text into the repo. ts is supplied by the caller (no wall-clock here)."""
    banned = {"text", "content", "reply", "message", "utterance", "excerpt"}
    if banned & set(scalars):
        raise ValueError(f"privacy violation: scalars may not carry content fields {banned & set(scalars)}")
    rec = {"trial_id": trial_id, "ts": ts, "arm": arm, "turn_index": turn_index, **scalars}
    with open(log_path, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---- self-test (no wiring, no network, no owner data) ------------------------
if __name__ == "__main__":
    assert set(coin(f"t{i}") for i in range(200)) == set(ARMS), "coin must cover both arms"
    assert eligible({"enrolled": True, "is_conversational": True, "session_trials": 0})
    assert not eligible({"enrolled": True, "is_conversational": True, "session_trials": 1})
    assert not eligible({"enrolled": True, "pending_edits": True, "is_conversational": True})
    assert not eligible({"enrolled": False, "is_conversational": True})
    sc = reply_scalars("No, that's not what I meant", None)
    assert sc["continuation_vs_correction"] == 0 and sc["reply_len"] > 0
    try:
        log_trial("/dev/null", "x", "2026-07-17T00:00:00", "LIVE", 3, {"content": "leak"})
        raise SystemExit("FAIL: privacy guard did not fire")
    except ValueError:
        pass
    print("h012b_stub self-test OK (구현됨·미배선 — wiring + owner enrollment = the human gate)")
