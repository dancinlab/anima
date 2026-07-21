"""anima_v4 — shared runnable harness for HYPOTHESES hypothesis cards.

Deterministic, dependency-free (stdlib only) primitives for the anima-v4 problem.
HYPOTHESES cards reference these functions from their per-hypothesis run scripts
under `state/<hX>/` (shared machinery lives in repo-root `tool/`, per-hypothesis
runs live in `state/`).

Every function is a closed-form public relation — no fitting, no hidden constants
beyond documented defaults. All inputs are explicit so a card's falsifiers can be
evaluated against the returned numbers. Replace the placeholder primitives below
with the domain relations this campaign actually needs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# --- domain constants (explicit, no hidden fitting) ---------------------------

# `d_acc` (the anima v1 MORPH-ATOM metric) is forced-choice discrimination
# accuracy: NLL(seed+gold) < NLL(seed+counterfactual) over a 2-way choice.
# It is an accuracy over a binary forced choice, so it is bounded and its
# chance floor is exactly 1/2. Both bounds are definitional, not measured.
D_ACC_MAX = 1.0
D_ACC_CHANCE = 0.5


# --- generic closed-form primitives -------------------------------------------

def ratio(value: float, baseline: float) -> float:
    """Improvement factor of a measured value vs a baseline: value / baseline."""
    if baseline == 0:
        raise ValueError("baseline must be non-zero")
    return value / baseline


def headroom(current: float, floor: float) -> float:
    """Reduction factor between a current value and a theoretical floor:
    current / floor (>1 means there is room to improve toward the floor)."""
    if floor <= 0:
        raise ValueError(f"floor must be > 0: {floor}")
    return current / floor


def log_ratio(x: float) -> float:
    """Natural-log primitive kept as a worked example of using `math` (a
    thermodynamic-style floor is often R·T·ln(1/x)). Replace as needed."""
    if not (0.0 < x < 1.0):
        raise ValueError(f"x must be in (0,1): {x}")
    return math.log(1.0 / x)


# --- falsifier-reachability primitives ----------------------------------------
#
# A pre-registered falsifier of the form "delta(mechanism, control) < T => DEAD"
# is only a test of the mechanism if T is arithmetically attainable. When the
# control already scores near a bounded metric's ceiling, no mechanism can clear
# T and the falsifier returns DEAD for reasons that have nothing to do with the
# mechanism. These primitives decide that question in closed form.

def max_attainable_delta(control: float, ceiling: float = D_ACC_MAX) -> float:
    """The largest delta any mechanism could possibly show over `control` on a
    metric bounded above by `ceiling`. Closed form: ceiling - control."""
    if control > ceiling:
        raise ValueError(f"control {control} exceeds ceiling {ceiling}")
    return ceiling - control


def falsifier_reachable(threshold: float, control: float,
                        ceiling: float = D_ACC_MAX) -> bool:
    """True when a pre-registered `delta >= threshold` verdict is arithmetically
    attainable against `control` on a metric bounded by `ceiling`. False means
    the falsifier is VACUOUS: it triggers DEAD for every possible mechanism, so
    running it measures nothing."""
    return threshold <= max_attainable_delta(control, ceiling)


def saturation(arm: float, leak_ceiling: float) -> float:
    """Distance from a measured arm to the panel's LEAK CEILING — the score the
    panel yields when the answer is handed to the model outright (anima v1's C3
    'V1 liveness' arm). A value near 0 means the panel is saturated: the arm is
    already scoring what a model gets for free, so the panel can no longer
    resolve anything above it. Negative means the arm beat the leak ceiling."""
    return leak_ceiling - arm


def bpe_merge_reachable(pair_count: int, min_pair_count: int) -> bool:
    """Closed-form reachability of a frequency-BPE merge. Greedy BPE only ever
    merges a symbol pair whose corpus count reaches `min_pair_count` (anima v1
    `morph2b.py` used 5). A pair below that floor is never merged at ANY vocab
    size K — enlarging K adds rarer merges from the eligible pool, it does not
    lower the eligibility floor. So atomicity of a sub-threshold morpheme is
    unreachable for frequency BPE by construction, not by tuning."""
    if min_pair_count < 1:
        raise ValueError(f"min_pair_count must be >= 1: {min_pair_count}")
    return pair_count >= min_pair_count


# --- panel-audit primitives (closed-form, pre-training) -----------------------
#
# A recombination panel is only a valid test if a strategy that does NOT do the
# thing being tested scores chance on it. H_003's panel is built to pin the two
# cheap strategies — "any negator flips polarity" (presence) and "read the
# template shape" — to exactly 0.5, so that beating 0.5 requires individuating
# the negator token. These primitives verify that BY CONSTRUCTION, before any
# GPU spend (F7 · the don't-run gate). Panel items are dicts carrying at least
# {"gold_flip": int (0/1 = net parity), "negator_count": int, "template": str}.

def presence_heuristic_score(items: list) -> float:
    """Score of the strategy 'any negator present => flip polarity' against the
    panel's own gold. Returns the fraction of items where (negator_count > 0)
    matches gold_flip. A well-built recombination panel pins this to 0.5: depth-2
    items carry two negators (net no-flip) yet the heuristic still flips, so it is
    wrong exactly on them. Deviation from 0.5 means the panel leaks a countable
    cue and beating chance no longer requires the mechanism under test."""
    if not items:
        raise ValueError("empty panel")
    hits = sum(1 for it in items if int(it["negator_count"] > 0) == it["gold_flip"])
    return hits / len(items)


def template_heuristic_score(items: list) -> float:
    """Score of the best strategy that reads ONLY the template shape, ignoring
    which tokens fill it. For each distinct template it predicts that template's
    majority gold_flip; the score is how often that majority is right. If two
    depths share a template tail (H_003's D1/D2 minimal pairs), the template is
    50/50 and this returns 0.5 — the panel cannot be solved by shape alone."""
    if not items:
        raise ValueError("empty panel")
    from collections import defaultdict

    by_t = defaultdict(list)
    for it in items:
        by_t[it["template"]].append(it["gold_flip"])
    correct = 0
    for flips in by_t.values():
        maj = 1 if sum(flips) * 2 >= len(flips) else 0
        correct += sum(1 for f in flips if f == maj)
    return correct / len(items)


def worst_suffix_leak(items: list, max_len: int = 24) -> dict:
    """The strongest surface-suffix shortcut available on the panel. For every
    suffix length L up to max_len, group items by the last L characters of their
    `surface` string and score the best majority-guess strategy over those groups
    (as template_heuristic does, but on REAL surface suffixes rather than an
    assigned template field). Returns the worst (highest) such score and the L that
    achieves it. A heuristic-neutral panel keeps this at 0.5: no suffix of any
    length may correlate with the parity bit, or a model can read it instead of
    individuating the negator. This is the honest, assignment-free version of
    template_heuristic — a panel passes F7 only if BOTH sit at 0.5."""
    if not items:
        raise ValueError("empty panel")
    from collections import defaultdict

    best = 0.0
    best_len = 0
    for L in range(1, max_len + 1):
        by_suf = defaultdict(list)
        for it in items:
            s = it["surface"]
            by_suf[s[-L:]].append(it["gold_flip"])
        correct = 0
        for flips in by_suf.values():
            maj = 1 if sum(flips) * 2 >= len(flips) else 0
            correct += sum(1 for f in flips if f == maj)
        score = correct / len(items)
        if score > best:
            best, best_len = score, L
    return {"worst_suffix_score": round(best, 4), "suffix_len": best_len}


def held_out_blind_score(items: list) -> float:
    """The semantically correct F7 check. A panel is admissible only if a strategy
    that sees everything EXCEPT it cannot individuate the held-out negator token —
    i.e. it counts only the DRILLED negators and predicts flip from their parity —
    is pinned to chance. Each item carries `drilled_negator_count`. The strategy is
    correct when (drilled_count % 2) == gold_flip, which happens exactly when the
    held-out negator count is even. Returns max(score, 1 - score): a score of 0.25
    is as leaky as 0.75, because the model can invert an anti-correlated cue. Only
    0.5 means the held-out token carries information no drilled-only reader can
    recover — which is what forces the model to detect it. This supersedes
    worst_suffix_leak, whose raw-surface grouping both over-counts singleton verb
    groups AND scores detecting the target token (the mechanism) as a leak."""
    if not items:
        raise ValueError("empty panel")
    hits = sum(1 for it in items if (it["drilled_negator_count"] % 2) == it["gold_flip"])
    s = hits / len(items)
    return max(s, 1.0 - s)


def label_balance(items: list, cell_key: str = "cell") -> dict:
    """Per-cell fraction of gold_flip==1. A recombination panel must be 50/50 per
    cell or a constant-guess strategy beats chance on the imbalanced cell. Returns
    {cell: fraction_positive}."""
    from collections import defaultdict

    by_c = defaultdict(list)
    for it in items:
        by_c[it[cell_key]].append(it["gold_flip"])
    return {c: sum(v) / len(v) for c, v in by_c.items()}


def binom_sigma(p: float, n: int) -> float:
    """Standard error of a binomial proportion — sqrt(p(1-p)/n). Used to state a
    falsifier threshold in sigma above chance so 'reachable only by a real effect,
    not luck' is arithmetic, not assertion."""
    if n <= 0:
        raise ValueError(f"n must be > 0: {n}")
    return math.sqrt(p * (1.0 - p) / n)


# --- falsifier harness --------------------------------------------------------

@dataclass
class Falsifier:
    """One pre-registered, measurable falsifier. `predicate(metrics) -> bool`
    returns True when the falsifier is TRIGGERED (hypothesis component refuted)."""

    name: str
    predicate: object  # callable(dict) -> bool
    desc: str = ""


def evaluate(metrics: dict, falsifiers: list) -> dict:
    """Run each falsifier against the measured metrics. A falsifier PASSes when
    it is NOT triggered. Returns a verdict ledger (all-stdlib, JSON-safe)."""
    results = []
    for f in falsifiers:
        triggered = bool(f.predicate(metrics))
        results.append(
            {"name": f.name, "triggered": triggered, "status": "FAIL" if triggered else "PASS"}
        )
    n_pass = sum(1 for r in results if r["status"] == "PASS")
    return {
        "metrics": metrics,
        "falsifiers": results,
        "n_pass": n_pass,
        "n_total": len(results),
        "all_pass": n_pass == len(results),
    }
