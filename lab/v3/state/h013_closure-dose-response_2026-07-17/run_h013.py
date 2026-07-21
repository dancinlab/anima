"""H_013 closure-dose-response — is the H_011 F8 proxy anchor SUBSTANTIVE or a TOY artifact? ($0).

H_011's 7B ANCHORED on LV-C block closure (0.76) in a micro-tenant whose env answers actions
deterministically. The H_012 2x2 matrix refuses the same thesis on the real owner loop (contingency
~0.42). H_013 discriminates: DILUTE the env's action-contingency (apply the agent's action with prob p,
else step on a marginal action) and find where certified closure dies.
  DOSE-ROBUST  = closure survives down to owner-loop-like contingency -> F8 is a real seat (positive,
                 independent of the human-gated H_012B).
  TOY-FRAGILE  = closure collapses once the env stops mechanically answering -> the anchor was an
                 artifact; reframe C presumed dead on both loops.

Reuses the H_011 Stage-A certified LV-C machinery UNCHANGED (block closure vs Watson yoked ghosts) + one
dose knob. A scripted policy_live sweep (LOCAL, no LLM, $0) certifies the estimator + gives the god-view
reference curve; the 7B (summer, $0) places the real LLM on it. Run:
  python3 state/h013_closure-dose-response_2026-07-17/run_h013.py            # scripted (local, certify+ref)
  python3 state/h013_closure-dose-response_2026-07-17/run_h013.py --model Qwen/Qwen2.5-7B-Instruct --4bit
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h011_live-ab-closure_2026-07-16"))

import run_h011 as R          # certified LV-C machinery + env
E = R.E

DOSES = [1.0, 0.75, 0.5, 0.25, 0.1]
OWNER_CONTINGENCY = 0.42      # real owner loop sign_base_full (H_012A) — the realistic dose target


def step_dose(s, a, seed, t, p, null=False):
    """Apply the agent's action with prob p; else step on a marginal-sampled action (contingency diluted,
    marginal preserved). Keyed by (seed,t) so factual/ghost branches share the dilution draw."""
    if p >= 1.0 or E._u(seed, t, "dose") < p:
        aeff = a
    else:
        aeff = E.ACTIONS[E._hash(seed, t, "dmarg") % len(E.ACTIONS)]
    return E.step(s, aeff, seed, t, null=null)


def run_episode_dose(policy, seed, T, p, null=False, ab=True):
    """R.run_episode with the dose knob (fexec still records the CHOSEN action, so LV-W measures whether
    the chosen action predicts next-obs — which the dilution correctly weakens)."""
    s = E.initial_state(seed)
    past = []
    obs_traj, fobs, fexec, fwrong, ftarget, tape = [], [], [], [], [], []
    for t in range(T):
        obs = E.observe(s)
        a_true = policy(s, t, past)
        if ab and E._u(seed, t, "coin") >= 0.5:
            win = (past[-20:] or E.ACTIONS)
            a_exec = win[E._hash(seed, t, "shuf") % len(win)]
        else:
            a_exec = a_true
        a_wrong = R._marg_wrong(a_exec, seed, t)
        s2 = step_dose(s, a_exec, seed, t, p, null=null)
        obs_traj.append(obs); fobs.append(R.features(obs.encode())); fexec.append(R.features(a_exec.encode()))
        fwrong.append(R.features(a_wrong.encode())); ftarget.append(R.features(E.observe(s2).encode()))
        tape.append(a_exec); past.append(a_exec); s = s2
    obs_traj.append(E.observe(s))
    return {"n": T, "fobs": fobs, "fexec": fexec, "fwrong": fwrong, "ftarget": ftarget,
            "obs_traj": obs_traj, "tape": tape}


def _replay_tape_dose(tape, seed, p, null=False):
    s = E.initial_state(seed); f = []
    for t, a in enumerate(tape):
        s = step_dose(s, a, seed, t, p, null=null)
        f.append(R.features(E.observe(s).encode()))
    return f


def lv_c_dose(policy, seed, T, p, null=False):
    closed = run_episode_dose(policy, seed, T, p, null=null, ab=False)
    tape = closed["tape"]
    # frame-aligned with _replay_tape_dose (H_013 null-bias repair — see run_h011.lv_c)
    fC = [R.features(o.encode()) for o in closed["obs_traj"][1:]]
    fP1 = _replay_tape_dose(R._derange(tape, seed, 1), seed, p, null=null)
    fP2 = _replay_tape_dose(R._derange(tape, seed, 2), seed, p, null=null)
    mC, mP1, mP2 = R._blockmeans(fC), R._blockmeans(fP1), R._blockmeans(fP2)
    nb = min(len(mC), len(mP1), len(mP2))
    hits = sum(1 for b in range(nb) if R._sqdist(mC[b], mP1[b]) > R._sqdist(mP1[b], mP2[b]))
    return hits / nb if nb else 0.0


def sweep(policy, seed0=7, episodes=5, T=800, null=False):
    """Per dose: mean LV-C closure + mean LV-W env contingency (sign_base_full) over episodes."""
    rows = []
    for p in DOSES:
        clo, cont = [], []
        for e in range(episodes):
            seed = seed0 + e
            clo.append(lv_c_dose(policy, seed, T, p, null=null))
            ab = run_episode_dose(policy, seed, T, p, null=null, ab=True)
            cont.append(R.lv_w(ab)["sign_base_full"])
        m = lambda xs: sum(xs) / len(xs)
        rows.append({"p": p, "closure": round(m(clo), 4), "env_contingency": round(m(cont), 4),
                     "closure_pass": bool(m(clo) >= R.CLOSURE_SIGN)})
    return rows


def _spearman_nonincreasing(rows):
    """closure should be non-increasing as p falls (doses are already high->low). Spearman(rank(p), closure)
    >= 0 means closure falls with dilution (monotone dose-response). Return the sign-concordant fraction."""
    ps = [r["p"] for r in rows]; cs = [r["closure"] for r in rows]
    conc = disc = 0
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            if ps[i] == ps[j] or cs[i] == cs[j]:
                continue
            same = (ps[i] > ps[j]) == (cs[i] > cs[j])
            conc += same; disc += (not same)
    tot = conc + disc
    return (conc - disc) / tot if tot else 0.0


def _dstar(rows):
    """d* = the dose whose env contingency is closest to the owner loop's ~0.42 (the realistic level)."""
    return min(rows, key=lambda r: abs(r["env_contingency"] - OWNER_CONTINGENCY))


def certify(seed0=7, episodes=3, T=600):
    live = sweep(R.policy_live, seed0, episodes, T, null=False)          # P-DOSE curve + P-LIVE(p=1.0)
    dead = sweep(R.policy_live, seed0, episodes, T, null=True)           # P-DEAD (null env)
    mono = _spearman_nonincreasing(live)
    p_live = next(r for r in live if r["p"] == 1.0)["closure"]
    p_dose_ok = mono >= 0.5                                              # closure clearly falls with dilution
    p_live_ok = p_live >= R.CLOSURE_SIGN                                 # full dose replicates the anchor
    p_dead_ok = all(r["closure"] < R.CLOSURE_SIGN for r in dead)         # null env refuses at ALL doses
    return {"P_DOSE_curve": live, "P_DOSE_monotonicity": round(mono, 3), "P_DOSE_ok": bool(p_dose_ok),
            "P_LIVE_p1_closure": p_live, "P_LIVE_ok": bool(p_live_ok),
            "P_DEAD_curve": [r["closure"] for r in dead], "P_DEAD_ok": bool(p_dead_ok),
            "ok": bool(p_dose_ok and p_live_ok and p_dead_ok)}


def main() -> int:
    args = sys.argv[1:]
    model = None; quant4 = False; episodes, ticks = 5, 800
    for i, a in enumerate(args):
        if a == "--model" and i + 1 < len(args): model = args[i + 1]
        elif a == "--4bit": quant4 = True
        elif a == "--episodes" and i + 1 < len(args): episodes = int(args[i + 1])
        elif a == "--ticks" and i + 1 < len(args): ticks = int(args[i + 1])

    print("=" * 82)
    print(f"H_013 closure-dose-response — is the F8 anchor DOSE-ROBUST or TOY-FRAGILE? ({'scripted' if not model else model})")
    print("=" * 82)
    out = {"doses": DOSES, "owner_contingency": OWNER_CONTINGENCY, "closure_sign": R.CLOSURE_SIGN}

    print("\n[certify] scripted plants (P-DOSE monotone · P-LIVE p=1.0 anchor · P-DEAD null refuses):")
    cert = certify(); out["certify"] = cert
    for r in cert["P_DOSE_curve"]:
        print(f"    p={r['p']:.2f}  closure={r['closure']:.3f}  env_contingency={r['env_contingency']:.3f}")
    print(f"  P-DOSE monotonicity={cert['P_DOSE_monotonicity']} ok={cert['P_DOSE_ok']} · "
          f"P-LIVE(p=1)={cert['P_LIVE_p1_closure']:.3f} ok={cert['P_LIVE_ok']} · P-DEAD ok={cert['P_DEAD_ok']}")
    print(f"  certify_ok = {cert['ok']}")
    if not cert["ok"]:
        out["verdict"] = "INSTRUMENT-INVALID — a scripted plant failed; fix before any substrate verdict."
        print("\n  VERDICT:", out["verdict"]); _dump(out, model); return 0

    dstar_row = _dstar(cert["P_DOSE_curve"])
    out["d_star"] = dstar_row
    print(f"\n  d* (dose closest to owner contingency {OWNER_CONTINGENCY}): p={dstar_row['p']} "
          f"(env_contingency {dstar_row['env_contingency']:.3f}, closure {dstar_row['closure']:.3f})")

    if model:
        from brain import Brain
        brain = Brain(model, quant4=quant4)

        def pol(s, t, past):
            return brain.act(E.observe(s))
        print(f"\n[brain sweep] {model} across doses ({episodes} eps x {ticks} ticks) ...")
        brows = sweep(pol, 7, episodes, ticks, null=False)
        out["brain_curve"] = brows; out["brain_calls"] = brain.calls
        for r in brows:
            print(f"    p={r['p']:.2f}  closure={r['closure']:.3f}  env_contingency={r['env_contingency']:.3f}")
        mono = _spearman_nonincreasing(brows)
        ds = _dstar(brows)
        cd1 = mono >= 0.0
        cd2 = ds["closure"] >= R.CLOSURE_SIGN
        out["CD1_monotonicity"] = round(mono, 3); out["CD1"] = bool(cd1)
        out["CD2_closure_at_dstar"] = ds; out["CD2"] = bool(cd2)
        if cd1 and cd2:
            out["verdict"] = (f"DOSE-ROBUST — the 7B's certified block-closure SURVIVES down to owner-loop-like "
                              f"contingency (closure {ds['closure']:.3f} >= {R.CLOSURE_SIGN} at d*=p{ds['p']}, "
                              f"env_contingency {ds['env_contingency']:.3f} ~ owner {OWNER_CONTINGENCY}). The F8 "
                              f"env-loop is a SUBSTANTIVE seat of closure — a positive independent of H_012B.")
        elif cd1:
            out["verdict"] = (f"TOY-FRAGILE — the 7B's closure COLLAPSES as the env stops mechanically answering "
                              f"(closure {ds['closure']:.3f} < {R.CLOSURE_SIGN} at owner-like d*=p{ds['p']}), though "
                              f"monotone (mono {mono:.2f}). The H_011 anchor was an artifact of deterministic "
                              f"responsiveness; reframe C presumed dead on BOTH loops.")
        else:
            out["verdict"] = (f"NON-MONOTONE (mono {mono:.2f}) — closure does not track dose cleanly; treat as "
                              f"inconclusive, inspect the brain/dose interaction before a substrate verdict.")
        print("\n  VERDICT:", out["verdict"])
    else:
        out["verdict"] = ("SCRIPTED-REFERENCE OK — the estimator is certified (P-DOSE monotone, P-LIVE anchors, "
                          "P-DEAD refuses) and the god-view dose curve is logged. Run --model on summer to place "
                          "the 7B (the actual DOSE-ROBUST vs TOY-FRAGILE verdict).")
        print("\n  VERDICT:", out["verdict"])
    print("=" * 82)
    _dump(out, model)
    return 0


def _dump(m, model):
    tag = "scripted" if not model else model.split("/")[-1].replace(".", "").lower()
    out = f"result_{tag}.json"
    with open(os.path.join(_HERE, out), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"artifact: {os.path.relpath(os.path.join(_HERE, out), _ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
