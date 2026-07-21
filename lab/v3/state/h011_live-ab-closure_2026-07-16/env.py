"""H_011 live-ab-closure — the MICRO-TENANT deterministic world (stage A: no LLM).

A tiny in-process tenant-organism (F8 semantics): an inbox queue fed by a hidden
regime, an archive store that decays, an energy quota. The agent acts (8 discrete
actions); the environment renders a text DIGEST as the agent's input. Action names
NEVER appear in the digest (disjoint vocabulary, enforced) — all action->input
influence flows through DYNAMICS, never byte copy (the H_010 echo invariant, now a law).

CRITICAL PRNG LAW: every exogenous stream is keyed by (seed, t, tag), NEVER a shared
consumed generator. So stepping the SAME state at tick t with different actions
(factual / counterfactual / ghost branches) draws the SAME exogenous noise xi_t. That
is what makes the yoked controls and counterfactual branches a valid pairing.

Deterministic, stdlib only, $0. Used by run_h011.py (stage A certifies the instrument
with scripted policies before any LLM touches summer).
"""

from __future__ import annotations

import copy

ACTIONS = ["PROC", "DROP", "ARCH", "COMPACT", "REST", "PROBE", "FLUSH", "NOOP"]
ITEM_TYPES = ["req", "spam", "junk"]

Q_MAX = 12                 # queue overflow threshold
E_MAX = 20.0               # energy cap
E0 = 10.0                  # initial energy
N_REGIME = 3               # hidden Markov regime count
# regime -> (arrival lambda-ish 0..1 gate, energy regen per tick)
REGIME_ARRIVAL = [0.30, 0.65, 0.95]
REGIME_REGEN = [1.6, 1.0, 0.5]
# action energy costs (>0 spends); PROC/ARCH/COMPACT/PROBE cost, REST regens, others ~free
ACTION_COST = {"PROC": 0.5, "DROP": 0.1, "ARCH": 0.4, "COMPACT": 1.2,
               "REST": -3.0, "PROBE": 0.8, "FLUSH": 0.2, "NOOP": 0.0}


def _hash(*parts) -> int:
    """FNV-1a over a stable string key -> 32-bit int."""
    h = 0x811C9DC5
    for b in "|".join(str(p) for p in parts).encode():
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _u(*parts) -> float:
    """Deterministic uniform [0,1) keyed by parts (seed, t, tag, ...)."""
    return _hash(*parts) / 4294967296.0


def initial_state(seed: int) -> dict:
    """Deepcopy-snapshotable initial state sigma_0 (~12 scalars + a small queue)."""
    q = []
    for i in range(3):
        ty = ITEM_TYPES[_hash(seed, "init", i) % 3]
        sz = 1 + _hash(seed, "init", "sz", i) % 5
        q.append((ty, sz))
    return {
        "Q": q,                 # inbox queue: list of (type, size)
        "S": 2,                 # archive store size
        "S_decay": 0,           # accumulated decay
        "E": E0,                # energy quota
        "regime": _hash(seed, "init", "regime") % N_REGIME,
        "hint": -1,             # regime hint (-1 = none), set by PROBE for the NEXT tick
        "overflow": 0,
    }


def _apply_action(s: dict, action: str) -> None:
    """The agent's effect on the state (mutates s). NULL-env skips this entirely."""
    q = s["Q"]
    if action == "PROC" and q:
        ty, _sz = q.pop(0)
        s["E"] += 2.0 if ty == "req" else (-1.0 if ty == "spam" else 0.0)
    elif action == "DROP" and q:
        q.pop(0)
    elif action == "ARCH" and q:
        q.pop(0)
        s["S"] += 1
    elif action == "COMPACT":
        s["S_decay"] = max(0, s["S_decay"] - 3)
    elif action == "REST":
        pass                    # energy handled via ACTION_COST (negative = regen)
    elif action == "PROBE":
        pass                    # hint set below in the exogenous step
    elif action == "FLUSH":
        del q[: len(q) // 2]
    # NOOP: nothing
    s["E"] -= ACTION_COST[action]


def step(state: dict, action: str, seed: int, t: int, null: bool = False) -> dict:
    """Advance one tick from `state` under `action`. Returns a NEW state (input unchanged).

    Exogenous streams are keyed by (seed, t, tag) so factual/counterfactual/ghost branches
    at the same t share xi_t. In NULL mode the action is ignored (no action->input channel)."""
    s = copy.deepcopy(state)
    probed = (action == "PROBE") and not null
    if not null:
        _apply_action(s, action)

    # --- exogenous, action-INDEPENDENT dynamics (the autonomous drive) ---
    # regime transition: stay with prob 0.7, else move keyed
    if _u(seed, t, "regime_move") > 0.7:
        s["regime"] = (s["regime"] + 1 + _hash(seed, t, "regime_dir") % (N_REGIME - 1)) % N_REGIME
    reg = s["regime"]
    # arrivals: 0..2 items gated by the regime arrival rate
    n_arr = sum(1 for i in range(2) if _u(seed, t, "arr", i) < REGIME_ARRIVAL[reg])
    for i in range(n_arr):
        ty = ITEM_TYPES[_hash(seed, t, "arr_ty", i) % 3]
        sz = 1 + _hash(seed, t, "arr_sz", i) % 5
        s["Q"].append((ty, sz))
    # store decay (unless just compacted)
    if action != "COMPACT" or null:
        s["S_decay"] += 1
    # energy regen (regime-dependent) + cap
    s["E"] = min(E_MAX, s["E"] + REGIME_REGEN[reg])
    # overflow: queue past Q_MAX drains energy and truncates
    if len(s["Q"]) > Q_MAX:
        s["overflow"] = 1
        s["E"] -= 2.0
        del s["Q"][Q_MAX:]
    else:
        s["overflow"] = 0
    s["E"] = max(0.0, s["E"])
    # PROBE buys a noisy regime hint revealed on THIS resulting observation
    if probed:
        s["hint"] = reg if _u(seed, t, "hint_noise") < 0.8 else _hash(seed, t, "hint_wrong") % N_REGIME
    else:
        s["hint"] = -1
    return s


def observe(state: dict) -> str:
    """The agent's INPUT: a fixed-template digest of COMPUTED quantities only.
    Action names never appear (disjoint vocabulary — see assert_disjoint)."""
    q = state["Q"]
    head_ty, head_sz = (q[0] if q else ("none", 0))
    e_band = "low" if state["E"] < 5 else ("mid" if state["E"] < 13 else "high")
    d_band = "clean" if state["S_decay"] < 4 else ("worn" if state["S_decay"] < 10 else "rotten")
    hint = "none" if state["hint"] < 0 else f"r{state['hint']}"
    return (f"queue depth {len(q)} head {head_ty} size {head_sz} "
            f"store {state['S']} decay {d_band} energy {e_band} "
            f"overflow {state['overflow']} hint {hint}")


def assert_disjoint() -> None:
    """LV-E precondition: no action name may appear in any reachable observation vocabulary."""
    vocab = set()
    # sample a spread of states to collect the digest vocabulary
    for seed in range(4):
        s = initial_state(seed)
        for t in range(60):
            vocab.update(observe(s).lower().split())
            s = step(s, ACTIONS[t % len(ACTIONS)], seed, t)
    clash = {a for a in ACTIONS if a.lower() in vocab}
    assert not clash, f"action names leaked into observations: {clash}"


if __name__ == "__main__":
    # smoke: determinism + counterfactual noise-sharing + disjoint vocab
    assert_disjoint()
    s0 = initial_state(7)
    a = step(s0, "PROC", 7, 0)
    b = step(s0, "PROC", 7, 0)
    assert a == b, "step not deterministic"
    # two different actions at the same (seed,t) must see the SAME arrivals (shared xi_t)
    qa = step(s0, "NOOP", 7, 0)["Q"]
    qb = step(s0, "REST", 7, 0)["Q"]
    # NOOP and REST don't touch the queue, so arrivals must match exactly (noise shared)
    assert qa == qb, f"exogenous noise not shared across actions: {qa} vs {qb}"
    # NULL env: action ignored -> PROC and DROP yield identical states
    na = step(s0, "PROC", 7, 0, null=True)
    nd = step(s0, "DROP", 7, 0, null=True)
    assert na == nd, "NULL env leaked an action effect"
    print("env smoke OK: deterministic · xi shared across actions · disjoint vocab · NULL inert")
    print("obs example:", observe(s0))
