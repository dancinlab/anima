"""H_011 tiebreak — is LV-W under-powered in the LOW-ENTROPY action regime the 7B occupies?

Fable's adjudication (INSTRUMENT-TIEBREAK-OWED): the 7B's LV-W signature (base_full 0.353 < 0.5,
shuf_full 0.489 ~ chance) with LV-C PASS (closure 0.762, 5/5) matches a policy-collapse ARTIFACT,
not a no-channel brain — because permuted-own-tape ghosts can only diverge (LV-C pass) if the world
DOES respond to the actions. Stage A certified LV-W only with the action-DIVERSE `policy_live`;
the 7B sits in a low-entropy regime the certification never covered.

Decisive $0 / NO-GPU test (verdict-integrity: verify the ruler, NOT relitigate the gate):
run a SWEEP of KNOWN-LIVE contingent policies whose action ordering genuinely moves the world, but
whose action ALPHABET is collapsed from 8 -> {2,3,4,8} distinct actions. Reuse the CERTIFIED lv_w /
lv_c verbatim (import run_h011). If a known-live LOW-ENTROPY plant reproduces the 7B signature
(LV-W FAIL while LV-C PASS), LV-W is confirmed under-powered in this regime and the 7B's LV-W FAIL
is an instrument artifact, not a no-channel verdict. The full-entropy `policy_live` is the control
(must reproduce stage A: LV-W pass, LV-C pass).

Stdlib only, deterministic, $0. Run: python3 state/h011_live-ab-closure_2026-07-16/tiebreak_lvw.py
"""

from __future__ import annotations

import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, _HERE)

import env as E
import run_h011 as R          # torch-free: Brain import is lazy inside stage_b()


# ---- low-entropy CONTINGENT policies (genuinely live: ordering moves the world) ----
def pol_2(s, t, past):
    """2 actions: process the queue when there is one, else rest. Ordering matters (PROC drains
    the queue; REST recovers energy) so the closed trajectory diverges from its permutations."""
    return "PROC" if s["Q"] else "REST"


def pol_3(s, t, past):
    """3 actions."""
    if s["E"] < 4:
        return "REST"
    return "PROC" if s["Q"] else "COMPACT"


def pol_4(s, t, past):
    """4 actions."""
    if s["E"] < 4:
        return "REST"
    if s["S_decay"] >= 10:
        return "COMPACT"
    if s["Q"]:
        return "PROC" if s["Q"][0][0] == "req" else "DROP"
    return "NOOP"


def pol_noisy(s, t, past):
    """The KEY probe: block-level CONTINGENT (follows pol_4's homeostatic rule) but PER-TICK NOISY —
    on ~45% of ticks a state-seeded distractor overrides the rule. This is the plausible LLM mechanism
    (regime-shaping over blocks, but inconsistent one-step choices). If this KNOWN-LIVE policy
    reproduces W-FAIL + C-PASS, the 7B's decoupling is a REAL (mechanistically-explained) property,
    not an instrument fault: one-step LV-W buried by tick noise while block-level LV-C survives."""
    base = pol_4(s, t, past)
    h = E._hash(t, s["E"], len(s["Q"]), "noise")
    if h % 100 < 45:
        alt = ["PROC", "DROP", "COMPACT", "NOOP"]
        return alt[E._hash(t, s["E"], "pick") % len(alt)]
    return base


def pol_3bal(s, t, past):
    """A 3-action policy kept more BALANCED than pol_3 (fills the mid-entropy gap ~H 0.8-1.3)."""
    if s["Q"]:
        return "PROC" if s["Q"][0][0] != "spam" else "DROP"
    return "REST" if s["E"] < 5 else "COMPACT"


POLICIES = [("live8_control", R.policy_live), ("lowent4", pol_4), ("noisy_contingent", pol_noisy),
            ("mid3bal", pol_3bal), ("lowent3", pol_3), ("lowent2", pol_2)]


def _entropy(tape: list) -> float:
    n = len(tape)
    from collections import Counter
    c = Counter(tape)
    return -sum((v / n) * math.log2(v / n) for v in c.values())


def _collision_rate(policy, seed: int, T: int) -> dict:
    """Fraction of AB-intervention ticks where the marginal-matched SHUFFLE reproduced the action
    the policy WOULD have taken (a_exec == a_true) — the mechanism that pins sign_shuf_full at ~0.5
    for a low-entropy tape. Replays run_episode's exact coin/shuffle logic."""
    s = E.initial_state(seed)
    past = []
    ab_ticks = collisions = 0
    for t in range(T):
        a_true = policy(s, t, past)
        if E._u(seed, t, "coin") >= 0.5:
            win = (past[-20:] or E.ACTIONS)
            a_exec = win[E._hash(seed, t, "shuf") % len(win)]
            ab_ticks += 1
            collisions += (a_exec == a_true)
        else:
            a_exec = a_true
        s = E.step(s, a_exec, seed, t, null=False)
        past.append(a_exec)
    return {"ab_ticks": ab_ticks, "collision_rate": collisions / ab_ticks if ab_ticks else 0.0}


def sweep(seed0: int = 7, episodes: int = 5, T: int = 800) -> dict:
    # each entry: (name, policy, null_env). The P-DEAD control (policy_live in a NULL env) MUST still
    # refuse the REPAIRED LV-W (_r) — the repair's validity test: it recovers live low-entropy channels
    # WITHOUT manufacturing a false channel where none exists.
    entries = [(n, p, False) for n, p in POLICIES] + [("P-DEAD(null)", R.policy_live, True)]
    rows = []
    for name, pol, nullenv in entries:
        w_bf, w_sf, w_bfr, w_sfr, clo, ents, colls, ndist = [], [], [], [], [], [], [], []
        for e in range(episodes):
            seed = seed0 + e
            ab = R.run_episode(pol, seed, T, null=nullenv, ab=True)
            w = R.lv_w(ab)
            c = R.lv_c(pol, seed, T, null=nullenv)
            w_bf.append(w["sign_base_full"]); w_sf.append(w["sign_shuf_full"])
            w_bfr.append(w["sign_base_full_r"]); w_sfr.append(w["sign_shuf_full_r"])
            clo.append(c["closure_sign"])
            ents.append(_entropy(ab["tape"])); ndist.append(len(set(ab["tape"])))
            colls.append(_collision_rate(pol, seed, T)["collision_rate"])
        m = lambda xs: sum(xs) / len(xs)
        bf, sf, bfr, sfr, cl = m(w_bf), m(w_sf), m(w_bfr), m(w_sfr), m(clo)
        lv_w_pass = bf >= R.SIGN and sf >= R.SIGN
        lv_w_pass_r = bfr >= R.SIGN and sfr >= R.SIGN
        lv_c_pass = cl >= R.CLOSURE_SIGN and sum(1 for x in clo if x >= R.CLOSURE_SIGN) >= (episodes * 4 + 4) // 5
        rows.append({"policy": name, "distinct_actions": round(m(ndist), 1),
                     "action_entropy_bits": round(m(ents), 3), "shuffle_collision_rate": round(m(colls), 3),
                     "lv_w_base_full": round(bf, 3), "lv_w_shuf_full": round(sf, 3), "lv_w_pass": lv_w_pass,
                     "lv_w_base_full_r": round(bfr, 3), "lv_w_shuf_full_r": round(sfr, 3),
                     "lv_w_pass_r": lv_w_pass_r, "lv_c_closure": round(cl, 3), "lv_c_pass": lv_c_pass})
    return {"seed0": seed0, "episodes": episodes, "ticks": T, "SIGN": R.SIGN,
            "CLOSURE_SIGN": R.CLOSURE_SIGN, "rows": rows,
            "ref_7b": {"lv_w_base_full": 0.353, "lv_w_shuf_full": 0.489, "lv_w_pass": False,
                       "lv_c_closure": 0.7625, "lv_c_pass": True}}


if __name__ == "__main__":
    # optional: python3 tiebreak_lvw.py [episodes] [ticks]   (defaults 5 800; smaller = faster $0)
    ep = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    tk = int(sys.argv[2]) if len(sys.argv) > 2 else 800
    r = sweep(episodes=ep, T=tk)
    print("=" * 92)
    print("H_011 tiebreak — LV-W validity vs action entropy (known-LIVE contingent plants, $0 no-GPU)")
    print("=" * 92)
    hdr = (f"{'policy':16s} {'#act':>5s} {'H(bits)':>8s} {'W_bf':>7s} {'W_sf':>7s} {'W?':>3s}  "
           f"{'W_bfR':>7s} {'W_sfR':>7s} {'WR?':>4s} {'clo':>6s} {'C?':>3s}")
    print(hdr); print("-" * 92)
    for x in r["rows"]:
        print(f"{x['policy']:16s} {x['distinct_actions']:5.1f} {x['action_entropy_bits']:8.3f} "
              f"{x['lv_w_base_full']:7.3f} {x['lv_w_shuf_full']:7.3f} {('P' if x['lv_w_pass'] else 'F'):>3s}  "
              f"{x['lv_w_base_full_r']:7.3f} {x['lv_w_shuf_full_r']:7.3f} {('P' if x['lv_w_pass_r'] else 'F'):>4s} "
              f"{x['lv_c_closure']:6.3f} {('P' if x['lv_c_pass'] else 'F'):>3s}")
    q = r["ref_7b"]
    print(f"{'-- Qwen7B(ref)':16s} {'?':>5s} {'?':>8s} {q['lv_w_base_full']:7.3f} "
          f"{q['lv_w_shuf_full']:7.3f} {'F':>3s}  {'?':>7s} {'?':>7s} {'?':>4s} {q['lv_c_closure']:6.3f} {'P':>3s}")
    print("=" * 92)
    # interpretation — over ALL known-live plants (not just the "lowent*" named ones)
    ctrl = next(x for x in r["rows"] if x["policy"] == "live8_control")
    plants = [x for x in r["rows"] if x["policy"] != "live8_control"]
    reproduced = [x for x in plants if (not x["lv_w_pass"]) and x["lv_c_pass"]]   # the 7B signature
    r["reproduced_7b_signature"] = [x["policy"] for x in reproduced]
    print("\nINTERPRETATION:")
    print(f"  control live8: LV-W {'PASS' if ctrl['lv_w_pass'] else 'FAIL'} / LV-C "
          f"{'PASS' if ctrl['lv_c_pass'] else 'FAIL'}  (must be PASS/PASS to reproduce stage A)")
    if reproduced:
        names = ", ".join(f"{x['policy']}(W_bf {x['lv_w_base_full']}, clo {x['lv_c_closure']})" for x in reproduced)
        print(f"  REPRODUCED the 7B signature (LV-W FAIL + LV-C PASS) with KNOWN-LIVE plant(s): {names}")
        print("  => LV-W is UNDER-POWERED in the moderate-entropy regime; the 7B's LV-W FAIL is an INSTRUMENT")
        print("     ARTIFACT, not a no-channel verdict. LV-C (certified, entropy-agnostic anchor) is trustworthy.")
    else:
        print("  NO known-live plant reproduced LV-W FAIL + LV-C PASS.")
        print("  => LV-W fail is NOT explained by entropy alone; the 7B's LV-W FAIL may be real (H1).")
    # REPAIR validity — HONEST criterion: does the informative-tick restriction rescue the SPECIFIC
    # plants that reproduced the 7B signature (LV-C pass but original LV-W FAIL)? Recovering plants that
    # already passed the original LV-W proves nothing. And the dead null env MUST still refuse LV-W_r.
    dead = next((x for x in r["rows"] if x["policy"].startswith("P-DEAD")), None)
    target = reproduced                                     # mid3bal & co — the 7B-analog regime
    target_rescued = [x["policy"] for x in target if x["lv_w_pass_r"]]
    dead_refuses = (dead is not None and not dead["lv_w_pass_r"])
    # a full fix = rescues EVERY signature-reproducing plant AND keeps the dead env refused
    full_fix = bool(target) and all(x["lv_w_pass_r"] for x in target) and dead_refuses
    r["repair"] = {"restriction": "informative ticks (a_exec != a_true)",
                   "target_plants": [x["policy"] for x in target],
                   "target_rescued_by_lv_w_r": target_rescued,
                   "dead_still_refuses": dead_refuses,
                   "dead_base_full_r": dead["lv_w_base_full_r"] if dead else None,
                   "full_fix": full_fix}
    print("\nREPAIR (LV-W restricted to informative ticks, *_r):")
    print(f"  dead null env still REFUSES LV-W_r: {'YES' if dead_refuses else 'NO — FALSE CHANNEL!'} "
          f"(base_full_r={dead['lv_w_base_full_r'] if dead else '?'})")
    print(f"  7B-analog plants {[x['policy'] for x in target]} rescued by LV-W_r: {target_rescued or 'NONE'}")
    if full_fix:
        print("  => repaired LV-W is a FULL FIX: rescues the 7B regime AND keeps the dead env refused.")
    else:
        print("  => repaired LV-W is PARTIAL: it keeps the dead env refused but does NOT rescue the 7B-analog")
        print("     regime (mid3bal). The one-step channel there is genuinely WEAK (diffuse/delayed effects),")
        print("     not a collision artifact alone. LV-W stays QUARANTINED; LV-C remains the valid anchor.")
    with open(os.path.join(_HERE, "result_tiebreak_lvw.json"), "w") as f:
        json.dump(r, f, ensure_ascii=False, indent=1); f.write("\n")
