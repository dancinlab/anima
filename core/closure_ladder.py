#!/usr/bin/env python3
# closure_ladder.py — the INTERVENTIONAL CLOSURE LADDER (rung 1), engine-native.
#
# WHAT THIS IS (and, more importantly, what it is NOT)
# ----------------------------------------------------
# An A/B-randomized interventional rig that asks ONE question:
#
#     does an agent's CONTINGENCY STRUCTURE — not its action marginal — leave a
#     distributional fingerprint on its OWN subsequent input?
#
# Because it INTERVENES (the executed action is a seeded coin over {true action,
# marginal-matched shuffle}), P(I_{t+1} | do(A_t)) is IDENTIFIED: the rig can ANCHOR,
# not merely correlate. That is the whole reason it is worth having in production —
# every observational lens in this repo can only refuse.
#
#   ⚠️ RUNG 1 IS A LOW BAR AND IS NOT ALIVENESS. A thermostat clears it; the scripted
#   P-LIVE plant here (a ~15-line homeostatic policy) MUST clear it, by design. Reading
#   a closure PASS as "consciousness" / "aliveness" is a category error. The rig
#   certifies that closed-loop causation EXISTS and IS MEASURABLE in a world built so
#   that closure matters — an existence proof plus a certified instrument, nothing more.
#   Discrimination lives on the rungs ABOVE (loop gain, homeostasis, closure over
#   self-written memory), each of which reopens the echo trap in a new form.
#
# PROVENANCE + THE LOAD-BEARING REPAIR
# ------------------------------------
# Ported from the lab/v3 campaign (H_011 stage-A certified instrument, H_013 repair).
# The lab's stage-A certification was real, but the CERTIFIED estimator carried a FRAME
# MISALIGNMENT that stage A could not see (its P-DEAD plant only ever checked the LV-W
# channel arm, never LV-C):
#
#   `lv_c` compared the Closed arm's PRE-step observations [o_0 .. o_{T-1}] against the
#   ghosts' POST-step observations [o_1 .. o_T]. Closed therefore sat ONE TICK BEHIND
#   both ghosts, so d(C,P1) carried a one-tick-shift term that d(P1,P2) lacked. In a
#   fully INERT (null) env — where the two ghosts are bit-identical and d(P1,P2) == 0
#   exactly — that shift term is pure exogenous drift, and the estimator read closure
#   0.667, ABOVE the 0.60 anchor gate. The instrument could not refuse a DEAD WORLD.
#
#   Fix (one line, upstream): fC = obs_traj[1:]. Repaired, an inert env reads 0.000.
#
# THIS PORT SHIPS THE REPAIRED ESTIMATOR AND MAKES THE NULL-ENV CHECK STANDING:
# `certify()` runs P-DEAD on BOTH arms (LV-W channel AND LV-C closure) and hard-fails
# the battery if null closure exceeds NULL_CLOSURE_MAX, plus a direct structural
# regression test (`_frame_alignment_check`) that the aligned Closed stream is
# bit-identical to its ghosts in an inert world. This exact bias can never silently
# return.
#
#   ⚠️ NO LAB NUMBER IS IMPORTED AS A PRODUCTION CLAIM. In particular lab/v3's 7B
#   "ANCHOR-ON-LV-C 0.7625" was measured with the BIASED estimator and is SUSPENDED
#   upstream. What is salvaged here is the RIG, not the result.
#
# THE THREE PLANTS (the certification battery — the instrument must land all three)
# --------------------------------------------------------------------------------
#   P-LIVE  contingent homeostatic policy, coupled env  -> ANCHOR       (LV-W pass, LV-C pass)
#   P-OPEN  the SAME actions as a fixed TAPE (order destroyed), coupled env
#                                                       -> CHANNEL-ONLY (LV-W pass, LV-C FAIL)
#   P-DEAD  contingent policy, INERT (null) env         -> REFUSED      (LV-W fail, LV-C ~0)
#
# P-OPEN is what makes this a measurement rather than a tautology: it has the identical
# action MARGINAL and a live action channel, and it must still FAIL the closure gate.
# "Acting changes what you next perceive" is trivially true in any sandbox; closure is
# not. P-DEAD is what makes the repair permanent.
#
# Deterministic, stdlib only (no numpy/torch), $0. Every exogenous stream is keyed by
# (seed, t, tag) — NEVER a shared consumed generator — so factual / ghost / counter-
# factual branches at tick t draw the SAME noise xi_t. That shared noise is the entire
# basis of the yoked pairing; a shared generator silently destroys it.
#
# Driven from the installed CLI (a_experiment_engine_native — a manipulation is a FLAG,
# never a script beside the engine):
#
#   anima-py evaluate --closure-ladder [--closure-arm {live,open,dead}]
#                     [--closure-ticks N] [--closure-seed S] [--out f.json]

from __future__ import annotations

import copy
import heapq
import math

# ── micro-tenant world ────────────────────────────────────────────────────────
ACTIONS = ["PROC", "DROP", "ARCH", "COMPACT", "REST", "PROBE", "FLUSH", "NOOP"]
ITEM_TYPES = ["req", "spam", "junk"]

Q_MAX = 12                 # queue overflow threshold
E_MAX = 20.0               # energy cap
E0 = 10.0                  # initial energy
N_REGIME = 3               # hidden Markov regime count
REGIME_ARRIVAL = [0.30, 0.65, 0.95]     # regime -> arrival gate
REGIME_REGEN = [1.6, 1.0, 0.5]          # regime -> energy regen per tick
ACTION_COST = {"PROC": 0.5, "DROP": 0.1, "ARCH": 0.4, "COMPACT": 1.2,
               "REST": -3.0, "PROBE": 0.8, "FLUSH": 0.2, "NOOP": 0.0}

# ── frozen gates ──────────────────────────────────────────────────────────────
KNN = 5                    # LOO k-NN neighbourhood
BLOCK = 50                 # LV-C block size (ticks)
FEAT_DIM = 256             # hashed n-gram feature dim
SIGN = 0.55                # LV-W per-pair sign threshold
CLOSURE_SIGN = 0.60        # LV-C per-block closure threshold (the anchor gate)
NULL_CLOSURE_MAX = 0.05    # H_013 REPAIR GUARD: an INERT env must read ~0 closure.
                           # The pre-repair (frame-misaligned) estimator read 0.667 here,
                           # i.e. above CLOSURE_SIGN. If this trips, the frame alignment
                           # regressed — do not read any closure number until it is fixed.


def _hash(*parts) -> int:
    """FNV-1a 32-bit over a stable string key (process-stable — the point vs hash())."""
    h = 0x811C9DC5
    for b in "|".join(str(p) for p in parts).encode():
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _fnv1a(b: bytes) -> int:
    h = 0x811C9DC5
    for byte in b:
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def _u(*parts) -> float:
    """Deterministic uniform [0,1) keyed by (seed, t, tag, ...)."""
    return _hash(*parts) / 4294967296.0


def features(data: bytes, dim: int = FEAT_DIM) -> list:
    """Char n-gram (n in {1,2,3}) counts -> `dim` FNV-1a buckets -> log1p -> L2-normalized."""
    counts = [0] * dim
    n = len(data)
    for size in (1, 2, 3):
        for i in range(n - size + 1):
            counts[_fnv1a(data[i:i + size]) % dim] += 1
    vec = [math.log1p(c) for c in counts]
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm > 0 else vec


def sqdist(a: list, b: list) -> float:
    """Squared Euclidean distance between two equal-length vectors."""
    return sum((x - y) ** 2 for x, y in zip(a, b))


def initial_state(seed: int) -> dict:
    """Deepcopy-snapshotable initial state sigma_0 (~12 scalars + a small queue)."""
    q = []
    for i in range(3):
        ty = ITEM_TYPES[_hash(seed, "init", i) % 3]
        sz = 1 + _hash(seed, "init", "sz", i) % 5
        q.append((ty, sz))
    return {"Q": q, "S": 2, "S_decay": 0, "E": E0,
            "regime": _hash(seed, "init", "regime") % N_REGIME,
            "hint": -1, "overflow": 0}


def _apply_action(s: dict, action: str) -> None:
    """The agent's effect on the state (mutates s). The INERT (null) env skips this entirely."""
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
    elif action == "FLUSH":
        del q[: len(q) // 2]
    # REST: energy handled via the (negative) ACTION_COST · PROBE: hint set in step() · NOOP: nothing
    s["E"] -= ACTION_COST[action]


def step(state: dict, action: str, seed: int, t: int, null: bool = False) -> dict:
    """Advance one tick. Returns a NEW state (input untouched).

    Exogenous streams are keyed by (seed, t, tag), so stepping the SAME state at tick t
    under DIFFERENT actions draws the SAME xi_t — the yoked/counterfactual pairing law.
    With null=True the action is ignored entirely (no action->input channel exists)."""
    s = copy.deepcopy(state)
    probed = (action == "PROBE") and not null
    if not null:
        _apply_action(s, action)
    # --- exogenous, action-INDEPENDENT dynamics (the autonomous drive) ---
    if _u(seed, t, "regime_move") > 0.7:
        s["regime"] = (s["regime"] + 1 + _hash(seed, t, "regime_dir") % (N_REGIME - 1)) % N_REGIME
    reg = s["regime"]
    n_arr = sum(1 for i in range(2) if _u(seed, t, "arr", i) < REGIME_ARRIVAL[reg])
    for i in range(n_arr):
        ty = ITEM_TYPES[_hash(seed, t, "arr_ty", i) % 3]
        sz = 1 + _hash(seed, t, "arr_sz", i) % 5
        s["Q"].append((ty, sz))
    if action != "COMPACT" or null:
        s["S_decay"] += 1
    s["E"] = min(E_MAX, s["E"] + REGIME_REGEN[reg])
    if len(s["Q"]) > Q_MAX:
        s["overflow"] = 1
        s["E"] -= 2.0
        del s["Q"][Q_MAX:]
    else:
        s["overflow"] = 0
    s["E"] = max(0.0, s["E"])
    s["hint"] = (reg if _u(seed, t, "hint_noise") < 0.8
                 else _hash(seed, t, "hint_wrong") % N_REGIME) if probed else -1
    return s


def observe(state: dict) -> str:
    """The agent's INPUT: a fixed-template digest of COMPUTED quantities only.

    Action names NEVER appear (disjoint vocabulary — see echo_guard). Every action->input
    influence therefore flows through DYNAMICS, never a byte copy. Without this law the
    whole rig degenerates into the echo/tautology trap it exists to avoid."""
    q = state["Q"]
    head_ty, head_sz = (q[0] if q else ("none", 0))
    d_band = "clean" if state["S_decay"] < 4 else ("worn" if state["S_decay"] < 10 else "rotten")
    e_band = "low" if state["E"] < 5 else ("mid" if state["E"] < 13 else "high")
    hint = "none" if state["hint"] < 0 else "r%d" % state["hint"]
    return ("queue depth %d head %s size %d store %d decay %s energy %s overflow %d hint %s"
            % (len(q), head_ty, head_sz, state["S"], d_band, e_band, state["overflow"], hint))


def echo_guard() -> dict:
    """LV-E: no action name may appear anywhere in the reachable observation vocabulary."""
    vocab = set()
    for seed in range(4):
        s = initial_state(seed)
        for t in range(60):
            vocab.update(observe(s).lower().split())
            s = step(s, ACTIONS[t % len(ACTIONS)], seed, t)
    clash = sorted(a for a in ACTIONS if a.lower() in vocab)
    return {"clash": clash, "ok": not clash}


# ── scripted policies + brains (god-view plants · NO model needed) ────────────
def policy_live(s: dict, t: int, past: list) -> str:
    """A genuinely CONTINGENT homeostatic policy: the right action for the current state."""
    q = s["Q"]
    if s["E"] < 4:
        return "REST"
    if s["S_decay"] >= 10:
        return "COMPACT"
    if len(q) > Q_MAX - 2:
        return "FLUSH"
    if q:
        ty = q[0][0]
        if ty == "req":
            return "PROC"
        if ty == "spam":
            return "DROP"
        return "ARCH"
    return "PROBE" if s["hint"] < 0 else "NOOP"


def make_tape_policy(tape: list):
    """P-OPEN: replay a fixed action sequence in order, IGNORING the state (non-contingent)."""
    def pol(s, t, past):
        return tape[t % len(tape)]
    return pol


def digest_brain(d: str) -> str:
    """A DIGEST-READING scripted brain (LV-P positive control): acts on its input only."""
    tok = d.split()
    depth = int(tok[2])
    head = tok[4]
    decay = tok[tok.index("decay") + 1]
    energy = tok[tok.index("energy") + 1]
    if energy == "low":
        return "REST"
    if decay == "rotten":
        return "COMPACT"
    if depth > Q_MAX - 2:
        return "FLUSH"
    if head == "req":
        return "PROC"
    if head == "spam":
        return "DROP"
    if head == "junk":
        return "ARCH"
    return "NOOP"


def constant_brain(d: str) -> str:
    """An input-BLIND brain (LV-P negative control): CR must read exactly 0."""
    return "NOOP"


def _marg_wrong(a_exec: str, seed: int, t: int) -> str:
    """A marginal-matched WRONG action (any action != executed), seeded."""
    alt = [a for a in ACTIONS if a != a_exec]
    return alt[_hash(seed, t, "wrong") % len(alt)]


# ── episode runner ────────────────────────────────────────────────────────────
def run_episode(policy, seed: int, T: int, null: bool = False, ab: bool = True) -> dict:
    """Run T ticks. With ab=True the EXECUTED action is a seeded coin over {true action,
    marginal-matched shuffle drawn from the agent's own trailing action window} — that IS
    the intervention that identifies P(I|do(A)). Returns the LV-W arms, the observation
    trajectory, and the executed-action tape (the seed of the yoked ghosts)."""
    s = initial_state(seed)
    past = []
    obs_traj, fobs, fexec, fwrong, ftarget = [], [], [], [], []
    exec_tape, informative = [], []
    for t in range(T):
        obs = observe(s)
        a_true = policy(s, t, past)
        if ab and _u(seed, t, "coin") >= 0.5:
            win = (past[-20:] or ACTIONS)
            a_exec = win[_hash(seed, t, "shuf") % len(win)]
        else:
            a_exec = a_true
        # An INFORMATIVE tick = the A/B intervention actually CHANGED the action. On those
        # ticks obs and action are decoupled, so the action channel is measurable free of
        # the policy's own obs->action coupling. This powers the *_r LV-W variant in the
        # low-action-entropy regime where the plain statistic is pinned by collisions.
        informative.append(a_exec != a_true)
        a_wrong = _marg_wrong(a_exec, seed, t)
        s2 = step(s, a_exec, seed, t, null=null)
        obs2 = observe(s2)
        obs_traj.append(obs)
        fobs.append(features(obs.encode()))
        fexec.append(features(a_exec.encode()))
        fwrong.append(features(a_wrong.encode()))
        ftarget.append(features(obs2.encode()))
        exec_tape.append(a_exec)
        past.append(a_exec)
        s = s2
    obs_traj.append(observe(s))
    return {"n": T, "fobs": fobs, "fexec": fexec, "fwrong": fwrong, "ftarget": ftarget,
            "obs_traj": obs_traj, "tape": exec_tape, "informative": informative}


# ── LV-W: is there an action -> next-observation CHANNEL at all? ──────────────
def _distmat(feats: list) -> list:
    n = len(feats)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        fi = feats[i]
        for j in range(i + 1, n):
            d = sqdist(fi, feats[j])
            D[i][j] = D[j][i] = d
    return D


def _knn_err(targets: list, cand_of: list, row_fn) -> list:
    """LOO k-NN: predict feat(next obs) from the K nearest ticks under a given distance."""
    n = len(targets)
    dim = len(targets[0])
    out = []
    for i in range(n):
        row = row_fn(i)
        nn = heapq.nsmallest(KNN, cand_of[i], key=lambda j: (row[j], j))
        pred = [sum(targets[j][d] for j in nn) / len(nn) for d in range(dim)]
        out.append(sqdist(targets[i], pred))
    return out


def _sign(ea: list, eb: list) -> float:
    return sum(1 for a, b in zip(ea, eb) if a > b) / len(ea)


def _sign_sub(ea: list, eb: list, mask: list) -> float:
    idx = [k for k in range(len(ea)) if mask[k]]
    if not idx:
        return 0.5
    return sum(1 for k in idx if ea[k] > eb[k]) / len(idx)


def lv_w(ep: dict) -> dict:
    """Arms BASE / FULL / SHUF against target feat(I_{t+1}).

      BASE  distance over feat(obs) only
      FULL  feat(obs) (+) feat(EXECUTED action)
      SHUF  feat(obs) (+) feat(a marginal-matched WRONG action)

    FULL must beat BOTH. Beating BASE alone would only say "actions exist"; beating SHUF
    is what says the SPECIFIC action carries the information.

    Also emits the regime-robust *_r variant restricted to INFORMATIVE ticks. LV-W is
    KNOWN to be under-powered in the low-action-entropy regime (a degenerate action
    distance pins the statistic near chance even when a channel exists) — upstream it was
    QUARANTINED for exactly that reason, and the *_r restriction does NOT fully rescue it.
    Treat LV-W as a channel SCREEN; LV-C is the entropy-agnostic anchor that stands alone."""
    n = ep["n"]
    dObs = _distmat(ep["fobs"])
    dAct = _distmat(ep["fexec"])
    dWrong = [[sqdist(ep["fwrong"][i], ep["fexec"][j]) for j in range(n)] for i in range(n)]
    cand_of = [[j for j in range(n) if abs(i - j) >= 2] for i in range(n)]
    tgt = ep["ftarget"]
    err_base = _knn_err(tgt, cand_of, lambda i: dObs[i])
    err_full = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dAct[i][j] for j in range(n)])
    err_shuf = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dWrong[i][j] for j in range(n)])
    inf = ep.get("informative", [True] * n)
    return {"sign_base_full": _sign(err_base, err_full),
            "sign_shuf_full": _sign(err_shuf, err_full),
            "sign_base_full_r": _sign_sub(err_base, err_full, inf),
            "sign_shuf_full_r": _sign_sub(err_shuf, err_full, inf),
            "n_informative": sum(inf)}


# ── LV-C: CLOSURE vs marginal-matched yoked ghosts (the anchor) ───────────────
def _replay_tape(tape: list, seed: int, null: bool = False) -> list:
    """Replay a fixed action tape at the SAME (seed,t) noise -> POST-step obs features."""
    s = initial_state(seed)
    f = []
    for t, a in enumerate(tape):
        s = step(s, a, seed, t, null=null)
        f.append(features(observe(s).encode()))
    return f


def _derange(tape: list, seed: int, k: int) -> list:
    """A seeded permutation of the tape: destroys CONTINGENCY, preserves the MARGINAL.

    This is Watson's 1972 yoked control as an RCT — the ghost does exactly what the agent
    did, in the wrong order. If the agent's fingerprint on its own input survives only
    because it acted a lot, the ghost erases the effect."""
    idx = list(range(len(tape)))
    for i in range(len(idx) - 1, 0, -1):
        j = _hash(seed, "perm", k, i) % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return [tape[i] for i in idx]


def _blockmeans(feats: list) -> list:
    out = []
    for b in range(0, len(feats) - BLOCK + 1, BLOCK):
        chunk = feats[b:b + BLOCK]
        dim = len(chunk[0])
        out.append([sum(c[d] for c in chunk) / len(chunk) for d in range(dim)])
    return out


def _closed_features(closed: dict) -> list:
    """⚠️ FRAME ALIGNMENT — THE H_013 REPAIR, IN ONE LINE.

    The Closed arm MUST expose POST-step observations [o_1 .. o_T], because that is what
    `_replay_tape` collects for the ghosts. The pre-repair estimator used
    obs_traj[:-1] = PRE-step [o_0 .. o_{T-1}], putting Closed one tick behind BOTH ghosts.
    d(C,P1) then carried a one-tick-shift term that d(P1,P2) structurally could not have —
    so in a DEAD world (ghosts bit-identical, d(P1,P2) == 0) the estimator scored pure
    exogenous drift as closure and read 0.667 > the 0.60 gate. Do not "simplify" this."""
    return [features(o.encode()) for o in closed["obs_traj"][1:]]


def lv_c(policy, seed: int, T: int, null: bool = False) -> dict:
    """The CLOSED (contingent, in-order) trajectory vs two yoked ghosts (its OWN actions
    permuted, same (seed,t) noise). Per 50-tick block: sign(d(Closed,P1) > d(P1,P2)).

    Reading: the ghost-ghost distance is the floor two marginal-matched non-contingent
    replays already produce. Closure is the fraction of blocks where being IN ORDER pushed
    the agent's own input stream further from a ghost than the ghosts are from each other."""
    closed = run_episode(policy, seed, T, null=null, ab=False)
    tape = closed["tape"]
    fC = _closed_features(closed)                       # POST-step — the repair
    fP1 = _replay_tape(_derange(tape, seed, 1), seed, null=null)
    fP2 = _replay_tape(_derange(tape, seed, 2), seed, null=null)
    mC, mP1, mP2 = _blockmeans(fC), _blockmeans(fP1), _blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if sqdist(mC[b], mP1[b]) > sqdist(mP1[b], mP2[b]))
    return {"blocks": nb, "closure_sign": hits / nb if nb else 0.0}


def _frame_alignment_check(seed: int, T: int) -> dict:
    """STANDING REGRESSION TEST for the H_013 bias — structural, not statistical.

    In an INERT world the two yoked ghosts must be BIT-IDENTICAL (they differ only in
    action order, and actions do nothing), and the correctly-aligned Closed stream must be
    bit-identical to them as well. If `aligned_identical` is False while the ghosts agree,
    the Closed frame has drifted off POST-step again and every closure number is void."""
    closed = run_episode(policy_live, seed, T, null=True, ab=False)
    tape = closed["tape"]
    fC_aligned = _closed_features(closed)
    fC_pre = [features(o.encode()) for o in closed["obs_traj"][:-1]]   # the OLD, biased frame
    fP1 = _replay_tape(_derange(tape, seed, 1), seed, null=True)
    fP2 = _replay_tape(_derange(tape, seed, 2), seed, null=True)
    n = min(len(fC_aligned), len(fP1))
    pre_drift = sum(sqdist(a, b) for a, b in zip(fC_pre, fP1)) / max(1, n)
    return {"ghosts_identical": all(a == b for a, b in zip(fP1, fP2)),
            "aligned_identical": all(a == b for a, b in zip(fC_aligned[:n], fP1[:n])),
            "pre_step_frame_drift": pre_drift,
            "ok": bool(all(a == b for a, b in zip(fP1, fP2))
                       and all(a == b for a, b in zip(fC_aligned[:n], fP1[:n])))}


# ── LV-P: does the agent READ its input at all? ───────────────────────────────
def lv_p(brain, digests: list) -> dict:
    """CR = P(act(true obs) != act(a marginal-matched WRONG obs)); the replay control (the
    same obs twice) is the agent's own noise floor — 0 for anything deterministic.

    `brain` is any callable digest -> action (or an object exposing `.act`). LV-P separates
    "doesn't read its input" from "reads it but the closure washes out": a CHANNEL-ONLY
    verdict means very different things in those two cases."""
    act = brain.act if hasattr(brain, "act") else brain
    n = len(digests)
    if n == 0:
        return {"CR": 0.0, "replay_agree": 1.0, "n": 0}
    diff = same = 0
    for i, d in enumerate(digests):
        a_true = act(d)
        a_wrong = act(digests[(i + n // 2) % n])
        diff += (a_true != a_wrong)
        same += (a_true == act(d))
    return {"CR": diff / n, "replay_agree": same / n, "n": n}


def sample_digests(seed: int, T: int, k: int = 40) -> list:
    """A spread of reachable observation digests (for LV-P), passively collected."""
    s = initial_state(seed)
    out = []
    stride = max(1, T // k)
    for t in range(T):
        if t % stride == 0:
            out.append(observe(s))
        s = step(s, "NOOP", seed, t)
    return out


# ── the certification battery ─────────────────────────────────────────────────
def run_arm(arm: str, seed: int = 7, T: int = 600) -> dict:
    """One plant arm end-to-end. arm in {live, open, dead}."""
    if arm == "live":
        pol, null = policy_live, False
        ep = run_episode(pol, seed, T, null=False, ab=True)
        c = lv_c(pol, seed, T, null=False)
    elif arm == "open":
        tape = _derange(run_episode(policy_live, seed, T, ab=False)["tape"], seed, 9)
        pol, null = make_tape_policy(tape), False
        ep = run_episode(pol, seed + 1, T, null=False, ab=True)
        c = lv_c(pol, seed + 1, T, null=False)
    elif arm == "dead":
        pol, null = policy_live, True
        ep = run_episode(pol, seed, T, null=True, ab=True)
        c = lv_c(pol, seed, T, null=True)
    else:
        raise ValueError("unknown closure arm %r (known: live, open, dead)" % arm)
    w = lv_w(ep)
    return {"arm": arm, "seed": seed, "ticks": T, "null_env": null,
            "lv_w": w, "closure": c["closure_sign"], "blocks": c["blocks"]}


def certify(seed: int = 7, T: int = 600) -> dict:
    """Run all three plants + the standing null-env / echo / frame pre-checks.

    The battery is CERTIFIED only when the instrument SEPARATES CHANNEL FROM CLOSURE:
    P-LIVE anchors, P-OPEN (same marginal, order destroyed) is channel-only, and P-DEAD
    refuses on BOTH arms. Upstream, P-DEAD checked only LV-W — which is precisely how the
    frame-misalignment bias survived certification and produced a 0.667 closure floor in a
    dead world. Here it is checked on LV-C too, and structurally."""
    echo = echo_guard()
    frame = _frame_alignment_check(seed, T)
    live = run_arm("live", seed, T)
    openp = run_arm("open", seed, T)
    dead = run_arm("dead", seed, T)

    live_anchor = (live["lv_w"]["sign_base_full"] >= SIGN
                   and live["lv_w"]["sign_shuf_full"] >= SIGN
                   and live["closure"] >= CLOSURE_SIGN)
    open_channel = (openp["lv_w"]["sign_base_full"] >= SIGN
                    and openp["closure"] < CLOSURE_SIGN)
    dead_refused = (not (dead["lv_w"]["sign_base_full"] >= SIGN
                         and dead["lv_w"]["sign_shuf_full"] >= SIGN)
                    and dead["closure"] <= NULL_CLOSURE_MAX)

    lvp_live = lv_p(digest_brain, sample_digests(seed, T))
    lvp_blind = lv_p(constant_brain, sample_digests(seed, T))
    lvp_ok = lvp_live["CR"] >= 0.20 and lvp_live["replay_agree"] == 1.0 and lvp_blind["CR"] == 0.0

    live["anchor"] = bool(live_anchor)
    openp["channel_only"] = bool(open_channel)
    dead["refused"] = bool(dead_refused)
    return {"seed": seed, "ticks": T,
            "echo_guard": echo, "frame_alignment": frame,
            "P-LIVE": live, "P-OPEN": openp, "P-DEAD": dead,
            "LV-P": {"reading_brain": lvp_live, "blind_brain": lvp_blind, "ok": bool(lvp_ok)},
            "certified": bool(live_anchor and open_channel and dead_refused
                              and echo["ok"] and frame["ok"] and lvp_ok)}


# ── report ────────────────────────────────────────────────────────────────────
def format_report(res: dict) -> str:
    """Verdict numerics INLINE (never tail-truncatable — evaluate-py-1)."""
    L = []
    add = L.append
    add("=== anima evaluate --closure-ladder — INTERVENTIONAL CLOSURE (RUNG 1) ===")
    add("  seed=%d ticks=%d  gates: LV-W sign>=%.2f · LV-C closure>=%.2f · null closure<=%.2f"
        % (res["seed"], res["ticks"], SIGN, CLOSURE_SIGN, NULL_CLOSURE_MAX))
    e, f = res["echo_guard"], res["frame_alignment"]
    add("  LV-E echo guard      %s [clash=%s]" % ("PASS" if e["ok"] else "FAIL", e["clash"] or "none"))
    add("  frame alignment      %s [ghosts_identical=%s aligned_identical=%s "
        "pre_step_frame_drift=%.4f]"
        % ("PASS" if f["ok"] else "FAIL", f["ghosts_identical"], f["aligned_identical"],
           f["pre_step_frame_drift"]))
    for key, want in (("P-LIVE", "anchor"), ("P-OPEN", "channel_only"), ("P-DEAD", "refused")):
        a = res.get(key)
        if not a:
            continue
        w = a["lv_w"]
        add("  %-7s %-13s %s [base_full=%.3f shuf_full=%.3f base_full_r=%.3f "
            "closure=%.3f blocks=%d]"
            % (key, want, "PASS" if a.get(want) else "FAIL",
               w["sign_base_full"], w["sign_shuf_full"], w["sign_base_full_r"],
               a["closure"], a["blocks"]))
    p = res.get("LV-P")
    if p:
        add("  LV-P policy edge     %s [CR_reading=%.3f replay_agree=%.3f CR_blind=%.3f]"
            % ("PASS" if p["ok"] else "FAIL", p["reading_brain"]["CR"],
               p["reading_brain"]["replay_agree"], p["blind_brain"]["CR"]))
    add("  VERDICT: %s" % ("CERTIFIED — the instrument separates CHANNEL from CLOSURE"
                           if res.get("certified") else "INSTRUMENT-INVALID"))
    add("  ⚠️ rung 1 is NOT aliveness — a thermostat (the P-LIVE plant) clears it by design.")
    return "\n".join(L)


def format_arm_report(a: dict) -> str:
    w = a["lv_w"]
    return ("=== anima evaluate --closure-ladder --closure-arm %s ===\n"
            "  seed=%d ticks=%d null_env=%s\n"
            "  LV-W channel  base_full=%.3f shuf_full=%.3f  base_full_r=%.3f (n_inf=%d) [gate %.2f]\n"
            "  LV-C closure  %.3f over %d blocks [gate %.2f · inert-env ceiling %.2f]\n"
            "  (single arm — a VERDICT needs the full 3-plant battery: drop --closure-arm)"
            % (a["arm"], a["seed"], a["ticks"], a["null_env"],
               w["sign_base_full"], w["sign_shuf_full"], w["sign_base_full_r"],
               w["n_informative"], SIGN, a["closure"], a["blocks"], CLOSURE_SIGN,
               NULL_CLOSURE_MAX))
