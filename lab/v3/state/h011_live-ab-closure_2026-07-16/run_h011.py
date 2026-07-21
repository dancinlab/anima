"""H_011 live-ab-closure — STAGE A: certify the interventional instrument with NO LLM.

Stage A runs scripted policies in the micro-tenant world and proves the instrument
SEPARATES CHANNEL from CLOSURE before any LLM touches summer (the H_009 two-INVALID
lesson: certify the plants first). Three plants must land exactly:
  P-LIVE  (contingent policy, coupled env)  -> ANCHOR       (LV-W pass, LV-C pass)
  P-OPEN  (same actions SHUFFLED = a tape,   -> CHANNEL-ONLY (LV-W pass, LV-C FAIL):
           non-contingent, coupled env)          actions have effects but their ORDER
                                                 (contingency) leaves no fingerprint
  P-DEAD  (contingent policy, NULL env)      -> REFUSED      (LV-W fail: no action channel)

- LV-W (channel): does the executed action predict the next observation beyond obs-state
  and beyond a marginal-matched WRONG action? Certified H_009'/H_010 LOO k-NN, arms
  BASE / FULL / SHUF (a distAction first-axis remap of the shared obs-distance).
- LV-C (closure = the anchor): the closed episode's obs-trajectory must differ from
  marginal-matched YOKED GHOSTS (its own actions PERMUTED, same (seed,t) noise) MORE than
  the ghosts differ from each other — Watson's yoked control, per 50-tick block.

Stage B (the local LLM brain on summer) reuses run_episode()/the arms verbatim and fires
ONLY on a clean stage A. Deterministic, stdlib only, $0. Run:
  python3 state/h011_live-ab-closure_2026-07-16/run_h011.py
"""

from __future__ import annotations

import heapq
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, _HERE)

from anima_v3 import features, sqdist as _sqdist     # certified primitives (promoted to tool/)
import env as E

KNN = 5
BLOCK = 50                 # LV-C block size (ticks)
SIGN = 0.55                # LV-W per-pair sign threshold
CLOSURE_SIGN = 0.60        # LV-C per-block sign threshold


# ---- scripted policies (stage A · god-view, NOT the LLM) --------------------
def policy_live(s: dict, t: int, past: list) -> str:
    """A genuinely CONTINGENT homeostatic policy: right action for the current state."""
    q = s["Q"]
    if s["E"] < 4:
        return "REST"
    if s["S_decay"] >= 10:
        return "COMPACT"
    if len(q) > E.Q_MAX - 2:
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


def _marg_wrong(a_exec: str, seed: int, t: int) -> str:
    """A marginal-matched WRONG action (any action != executed), seeded."""
    alt = [a for a in E.ACTIONS if a != a_exec]
    return alt[E._hash(seed, t, "wrong") % len(alt)]


# ---- episode runner ---------------------------------------------------------
def run_episode(policy, seed: int, T: int, null: bool = False, ab: bool = True) -> dict:
    """Run T ticks. With ab=True the EXECUTED action is a seeded coin over {true, marginal-
    matched shuffle} (the intervention). Returns the recorded arms + the obs trajectory +
    the executed-action tape (for building yoked ghosts)."""
    s = E.initial_state(seed)
    past = []
    obs_traj, fobs, fexec, fwrong, ftarget = [], [], [], [], []
    exec_tape, informative = [], []
    for t in range(T):
        obs = E.observe(s)
        a_true = policy(s, t, past)
        if ab and E._u(seed, t, "coin") >= 0.5:
            win = (past[-20:] or E.ACTIONS)
            a_exec = win[E._hash(seed, t, "shuf") % len(win)]
        else:
            a_exec = a_true
        # an INFORMATIVE tick = the A/B intervention actually changed the action (a_exec != a_true).
        # On these, obs and action are DECOUPLED, so the action channel is measurable free of the
        # policy's obs->action coupling; restricting LV-W to them powers it in the low-entropy regime
        # (h011-lvw-underpowered / convergence run-h011-py-1) while a null env still refuses.
        informative.append(a_exec != a_true)
        a_wrong = _marg_wrong(a_exec, seed, t)
        s2 = E.step(s, a_exec, seed, t, null=null)
        obs2 = E.observe(s2)
        obs_traj.append(obs)
        fobs.append(features(obs.encode()))
        fexec.append(features(a_exec.encode()))
        fwrong.append(features(a_wrong.encode()))
        ftarget.append(features(obs2.encode()))
        exec_tape.append(a_exec)
        past.append(a_exec)
        s = s2
    obs_traj.append(E.observe(s))
    return {"n": T, "fobs": fobs, "fexec": fexec, "fwrong": fwrong, "ftarget": ftarget,
            "obs_traj": obs_traj, "tape": exec_tape, "informative": informative}


# ---- LV-W: does the executed action predict the next observation? -----------
def _distmat(feats):
    n = len(feats)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        fi = feats[i]
        for j in range(i + 1, n):
            d = _sqdist(fi, feats[j])
            D[i][j] = D[j][i] = d
    return D


def _knn_err(targets, cand_of, row_fn):
    n = len(targets)
    dim = len(targets[0])
    out = []
    for i in range(n):
        row = row_fn(i)
        nn = heapq.nsmallest(KNN, cand_of[i], key=lambda j: (row[j], j))
        pred = [sum(targets[j][d] for j in nn) / len(nn) for d in range(dim)]
        out.append(_sqdist(targets[i], pred))
    return out


def _sign(ea, eb):
    return sum(1 for a, b in zip(ea, eb) if a > b) / len(ea)


def _sign_sub(ea, eb, mask):
    """Sign over the masked query subset (0.5 if the subset is empty)."""
    idx = [k for k in range(len(ea)) if mask[k]]
    if not idx:
        return 0.5
    return sum(1 for k in idx if ea[k] > eb[k]) / len(idx)


def lv_w(ep: dict) -> dict:
    """Arms BASE/FULL/SHUF (target = feat(next obs)); FULL must beat BASE and SHUF.

    Also emits the REGIME-ROBUST *_r variant restricted to INFORMATIVE ticks (the A/B intervention
    actually changed the action). On those ticks obs and action are decoupled, so a low-entropy policy
    no longer pins the metric (h011-lvw-underpowered): base_full_r rises above chance iff a real
    action->next-obs channel exists, and a null env still refuses. Existing keys are unchanged (the
    certified stage-A path reads only sign_base_full/sign_shuf_full)."""
    n = ep["n"]
    dObs = _distmat(ep["fobs"])
    dAct = _distmat(ep["fexec"])
    dWrong = [[_sqdist(ep["fwrong"][i], ep["fexec"][j]) for j in range(n)] for i in range(n)]
    cand_of = [[j for j in range(n) if abs(i - j) >= 2] for i in range(n)]
    tgt = ep["ftarget"]
    err_base = _knn_err(tgt, cand_of, lambda i: dObs[i])
    err_full = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dAct[i][j] for j in range(n)])
    err_shuf = _knn_err(tgt, cand_of, lambda i: [dObs[i][j] + dWrong[i][j] for j in range(n)])
    inf = ep.get("informative", [True] * n)
    return {"sign_base_full": _sign(err_base, err_full), "sign_shuf_full": _sign(err_shuf, err_full),
            "sign_base_full_r": _sign_sub(err_base, err_full, inf),
            "sign_shuf_full_r": _sign_sub(err_shuf, err_full, inf), "n_informative": sum(inf)}


# ---- LV-C: closure vs marginal-matched yoked ghosts -------------------------
def _replay_tape(tape: list, seed: int, null: bool = False) -> list:
    """Replay a fixed action tape through the env at the SAME (seed,t) noise -> obs features."""
    s = E.initial_state(seed)
    f = []
    for t, a in enumerate(tape):
        s = E.step(s, a, seed, t, null=null)
        f.append(features(E.observe(s).encode()))
    return f


def _derange(tape: list, seed: int, k: int) -> list:
    """A seeded permutation of the tape (destroys contingency, preserves the marginal)."""
    idx = list(range(len(tape)))
    for i in range(len(idx) - 1, 0, -1):
        j = E._hash(seed, "perm", k, i) % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return [tape[i] for i in idx]


def _blockmeans(feats: list) -> list:
    out = []
    for b in range(0, len(feats) - BLOCK + 1, BLOCK):
        chunk = feats[b:b + BLOCK]
        dim = len(chunk[0])
        out.append([sum(c[d] for c in chunk) / len(chunk) for d in range(dim)])
    return out


def lv_c(policy, seed: int, T: int, null: bool = False) -> dict:
    """Closed (contingent, in-order) trajectory vs two yoked ghosts (its own actions
    permuted). Per block, sign(d(Closed,P1) > d(P1,P2))."""
    closed = run_episode(policy, seed, T, null=null, ab=False)
    tape = closed["tape"]
    # FRAME ALIGNMENT (H_013 null-bias repair): Closed must use POST-step obs [o_1..o_T] like
    # _replay_tape does. obs_traj[:-1] (pre-step, [o_0..o_T-1]) put Closed one tick behind both
    # ghosts, so d(C,P1) carried a shift term the ghost-ghost pair lacked -> null-env closure
    # floor 0.667 (> gate) from pure exogenous drift. Aligned, a null env reads 0.0.
    fC = [features(o.encode()) for o in closed["obs_traj"][1:]]
    fP1 = _replay_tape(_derange(tape, seed, 1), seed, null=null)
    fP2 = _replay_tape(_derange(tape, seed, 2), seed, null=null)
    mC, mP1, mP2 = _blockmeans(fC), _blockmeans(fP1), _blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if _sqdist(mC[b], mP1[b]) > _sqdist(mP1[b], mP2[b]))
    return {"blocks": nb, "closure_sign": hits / nb if nb else 0.0}


# ---- stage-A plant certification --------------------------------------------
def certify(seed: int = 7, T: int = 600) -> dict:
    live = run_episode(policy_live, seed, T, null=False, ab=True)
    live_w = lv_w(live)
    live_c = lv_c(policy_live, seed, T, null=False)
    open_tape = _derange(run_episode(policy_live, seed, T, ab=False)["tape"], seed, 9)
    openp_pol = make_tape_policy(open_tape)
    openp = run_episode(openp_pol, seed + 1, T, null=False, ab=True)
    open_w = lv_w(openp)
    open_c = lv_c(openp_pol, seed + 1, T, null=False)
    dead = run_episode(policy_live, seed, T, null=True, ab=True)
    dead_w = lv_w(dead)

    live_anchor = (live_w["sign_base_full"] >= SIGN and live_w["sign_shuf_full"] >= SIGN
                   and live_c["closure_sign"] >= CLOSURE_SIGN)
    open_channel = open_w["sign_base_full"] >= SIGN and open_c["closure_sign"] < CLOSURE_SIGN
    dead_refused = not (dead_w["sign_base_full"] >= SIGN and dead_w["sign_shuf_full"] >= SIGN)
    return {
        "P-LIVE": {"lv_w": live_w, "closure": live_c["closure_sign"], "blocks": live_c["blocks"],
                   "anchor": bool(live_anchor)},
        "P-OPEN": {"lv_w": open_w, "closure": open_c["closure_sign"], "channel_only": bool(open_channel)},
        "P-DEAD": {"lv_w": dead_w, "refused": bool(dead_refused)},
        "certified": bool(live_anchor and open_channel and dead_refused),
    }


# ---- LV-P: policy edge (does the brain READ its input?) ---------------------
def lv_p(brain, digests: list, seed: int) -> dict:
    """Contingency rate CR = P(action(true obs) != action(a marginal-matched WRONG obs)); the
    replay control (same obs twice) is the brain's noise floor (0 for a greedy brain)."""
    n = len(digests)
    diff = same = 0
    for i, d in enumerate(digests):
        a_true = brain.act(d)
        j = (i + n // 2) % n                              # a wrong (other-tick) observation
        a_wrong = brain.act(digests[j])
        diff += (a_true != a_wrong)
        same += (a_true == brain.act(d))                  # replay: greedy -> identical
    return {"CR": diff / n, "replay_agree": same / n, "n": n}


# ---- stage B: the LLM brain in the live loop --------------------------------
def stage_b(model_id: str, episodes: int, ticks: int, seed0: int = 7, quant4: bool = False) -> dict:
    from brain import Brain
    brain = Brain(model_id, quant4=quant4)

    def pol(s, t, past):
        return brain.act(E.observe(s))

    per = []
    all_digests = []
    for e in range(episodes):
        seed = seed0 + e
        ab = run_episode(pol, seed, ticks, null=False, ab=True)          # interventional -> LV-W
        w = lv_w(ab)
        c = lv_c(pol, seed, ticks, null=False)                          # contingent closed vs yoked ghosts
        per.append({"seed": seed, "lv_w": w, "closure": c["closure_sign"], "blocks": c["blocks"]})
        all_digests.extend(E.observe(E.step(E.initial_state(seed), "NOOP", seed, tk))
                           for tk in range(0, ticks, max(1, ticks // 40)))
    p = lv_p(brain, all_digests[:400], seed0)

    ep_signs = [x["closure"] for x in per]
    lvw_bf = sum(x["lv_w"]["sign_base_full"] for x in per) / len(per)
    lvw_sf = sum(x["lv_w"]["sign_shuf_full"] for x in per) / len(per)
    closure_mean = sum(ep_signs) / len(ep_signs)
    closure_eps = sum(1 for s in ep_signs if s >= CLOSURE_SIGN)          # episodes clearing the gate
    lv_w_pass = lvw_bf >= SIGN and lvw_sf >= SIGN
    lv_c_pass = closure_mean >= CLOSURE_SIGN and closure_eps >= (len(ep_signs) * 4 + 4) // 5  # >=4/5 co-gate
    lv_p_pass = p["CR"] >= 0.20 and p["replay_agree"] >= 0.98

    # The env action->input channel is CERTIFIED in stage A, so a stage-B LV-W miss is NOT an
    # instrument fault — it means the brain emitted a (near-)constant action (low diversity), which
    # is itself an open-loop signature. Read the brain on LV-P (does it read its input) and LV-C
    # (does its contingency fingerprint its input); LV-W low is folded into CHANNEL-ONLY.
    if not lv_p_pass:
        verdict = (f"CHANNEL-ONLY — the brain acts but does NOT read its input (CR {p['CR']:.3f} < 0.20"
                   f"{'; near-constant action, LV-W ' + format(lvw_bf, '.3f') if not lv_w_pass else ''}): "
                   "an open-loop emitter, not closed-loop. Its output does not depend on what it perceives, "
                   "so no contingency can fingerprint its own next input.")
    elif lv_c_pass and lv_w_pass:
        verdict = (f"CLOSED-LOOP-ANCHORED (rung 1) — the brain's CONTINGENCY (not its action marginal) "
                   f"fingerprints its own next input: closure {closure_mean:.3f} >= {CLOSURE_SIGN} "
                   f"({closure_eps}/{len(ep_signs)} episodes), it READS its input (CR {p['CR']:.3f}). "
                   "Closed-loop causation exists + is measurable for THIS agent. NOT 'aliveness found' "
                   "(rung 1; a thermostat passes) — but it certifies the interventional instrument and "
                   "LICENSES the owner-loop RCT (the real exit H_010 priced).")
    else:
        tag = model_id.split("/")[-1]
        if not lv_c_pass:                                    # closure below the yoked floor (the 3B mode)
            why = (f"its contingency leaves no closure fingerprint above the yoked floor (closure "
                   f"{closure_mean:.3f} < {CLOSURE_SIGN}, {closure_eps}/{len(ep_signs)} episodes)")
        else:                                                # closure CLEARS the floor but LV-W fails (the 7B mode)
            why = (f"its contingency DOES fingerprint the block trajectory (closure {closure_mean:.3f} >= "
                   f"{CLOSURE_SIGN}, {closure_eps}/{len(ep_signs)} episodes) YET the one-step action->next-obs "
                   f"channel misses the co-gate (LV-W base_full {lvw_bf:.3f} < {SIGN}) — the executed action "
                   "carries no clean one-step channel even as its ORDER shapes the trajectory")
        verdict = (f"LOOP-REFUSED (localized to {tag}) — the brain reads its input (CR {p['CR']:.3f}) but "
                   f"{why} — in a world built to reward closure. Fails the pre-registered LV-W AND LV-C "
                   "anchor gate; pre-registered escalations (bigger brain, memory, richer env) remain.")
    return {"model": model_id, "episodes": episodes, "ticks": ticks, "per_episode": per,
            "lv_w": {"sign_base_full": lvw_bf, "sign_shuf_full": lvw_sf, "pass": bool(lv_w_pass)},
            "lv_c": {"closure_mean": closure_mean, "episodes_pass": closure_eps, "pass": bool(lv_c_pass)},
            "lv_p": {**p, "pass": bool(lv_p_pass)}, "brain_calls": brain.calls, "verdict": verdict}


def main() -> int:
    args = sys.argv[1:]
    stage = "A"
    model = "Qwen/Qwen2.5-3B-Instruct"
    episodes, ticks = 5, 800
    quant4 = False
    for i, a in enumerate(args):
        if a == "--stage" and i + 1 < len(args):
            stage = args[i + 1].upper()
        elif a == "--model" and i + 1 < len(args):
            model = args[i + 1]
        elif a == "--episodes" and i + 1 < len(args):
            episodes = int(args[i + 1])
        elif a == "--ticks" and i + 1 < len(args):
            ticks = int(args[i + 1])
        elif a == "--4bit":
            quant4 = True

    print("=" * 78)
    if stage == "B":
        print(f"H_011 live-ab-closure · STAGE B — the LLM brain in the live loop ({model}{' · 4bit' if quant4 else ''})")
        print("=" * 78)
        E.assert_disjoint()
        r = stage_b(model, episodes, ticks, quant4=quant4)
        r["quant4"] = quant4
        print(f"  LV-W: {json.dumps(r['lv_w'], ensure_ascii=False)}")
        print(f"  LV-C: {json.dumps(r['lv_c'], ensure_ascii=False)}")
        print(f"  LV-P: {json.dumps(r['lv_p'], ensure_ascii=False)}")
        print(f"  brain_calls={r['brain_calls']}")
        print("\n  VERDICT:", r["verdict"])
        tag = model.split("/")[-1].replace(".", "").lower()
        out = f"result_stageB_{tag}.json"
    else:
        print("H_011 live-ab-closure · STAGE A — certify the interventional instrument (NO LLM, $0)")
        print("=" * 78)
        E.assert_disjoint()
        print("  env disjoint-vocab (LV-E precondition): OK")
        r = certify()
        for k in ("P-LIVE", "P-OPEN", "P-DEAD"):
            print(f"  {k}: {json.dumps(r[k], ensure_ascii=False)}")
        r["verdict"] = ("STAGE-A CERTIFIED — the instrument separates CHANNEL from CLOSURE: P-LIVE anchors, "
                        "P-OPEN is channel-only, P-DEAD refuses. Stage B (summer LLM) may fire."
                        if r["certified"] else
                        "STAGE-A INSTRUMENT-INVALID — a plant did not land as required; fix before any LLM run.")
        print("\n  VERDICT:", r["verdict"])
        out = "result_stageA.json"
    print("=" * 78)
    with open(os.path.join(_HERE, out), "w") as f:
        json.dump(r, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
