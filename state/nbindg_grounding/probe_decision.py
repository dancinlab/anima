"""H_9303 — the lane's original question, asked for the first time at the position that answers it.

H_9302 certified the instrument and, in doing so, invalidated every negative this lane ever read:
the probes were reading the hidden at the ATOM's last byte, where a causal LM has had no reason to
commit to anything. Move the read to the DECISION POINT (right after the arrow, where the model was
taught to emit the polarity and answers at SEEN 0.950) and the same probe goes from 0.390/0.325
(below chance) to 0.633/0.673, while the untaught shuffle_grid control stays at 0.408.

So the question this lane has been trying to ask for three years — and never actually asked — is:

    Does the DECISION-POINT representation carry the polarity of a HELD-OUT NATURAL atom,
    one the model was never taught, whose polarity its own input context determines
    (H_9291's oracle recovers it 29/29 from that very context)?

  reads   -> the polarity IS in the representation at the point of use, but the model does not EMIT
             it (H_9286: held-out D-acc = chance). The wall is then the COMMIT / output channel, not
             grounding — a lever nobody has touched.
  chance  -> now, and only now, an honest grounding wall: the representation genuinely does not carry
             an untaught atom's polarity at the moment it must answer. THEN the O/C channel is the
             right spend.

Prompts: the H_9297 natural contexts with " => " appended — the exact query form the D-acc eval uses,
so this is the probe moved to the eval's own position, not a new task invented for the probe.

Gates (frozen; V-LENGTH and V-CV inherited from H_9300's amendment II, V-LIVE new from H_9302):
  V-LIVE    the TRAIN (grid-taught) atoms must read above the shuffle_grid control at this position.
            Without it we are back to reading a negative off an uncertified instrument.
  V-PERM    200-draw label-permutation null (percentile, never a band).
  V-LENGTH  a one-feature prompt-byte-length probe reads 0.648 on this split — AT the frozen 0.65
            bar. Any arm that does not BEAT that floor, and does not survive regressing length out,
            has read length, not polarity.
  V-BASE    base_only stays below bar.
  bar 0.65  UNMOVED (n=91, chance sd 0.0524 -> 2.86 sigma).
"""

from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
BAR = 0.65
N_PERM = 200
SEED = 7


def logreg(Xtr, ytr, Xte):
    s = StandardScaler().fit(Xtr)
    m = LogisticRegression(max_iter=5000, C=0.1).fit(s.transform(Xtr), ytr)
    return m.predict_proba(s.transform(Xte))[:, 1], m.predict_proba(s.transform(Xtr))[:, 1]


def load(arm):
    npz = np.load(os.path.join(HERE, "hid", f"dec64_{arm}.npz"))
    meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
    prompts = {i["id"]: i["prompt"]
               for i in json.load(open(os.path.join(HERE, "gt_prompts_n92.json")))["items"]}
    pooled, y, split, blen = [], [], [], []
    for a in meta:
        ids = [i for i in a["ids"] if i + "__last" in npz.files]
        if not ids:
            continue
        pooled.append(np.stack([npz[i + "__last"] for i in ids], 0).astype(np.float64).mean(0))
        blen.append(np.mean([len(prompts[i].encode()) for i in ids if i in prompts]))
        y.append(a["pol"]); split.append(a["split"])
    return (np.stack(pooled, 0), np.array(y), np.array(split), np.array(blen))


def v_live(arm):
    """The grid-TAUGHT atoms, read at this same decision position, contexts as samples,
    leave-one-ATOM-out. This is the gate H_9289..H_9300 never had."""
    npz = np.load(os.path.join(HERE, "hid", f"dec64_{arm}.npz"))
    meta = [a for a in json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
            if a["split"] == "train"]
    X, y, at = [], [], []
    for ai, a in enumerate(meta):
        for i in a["ids"]:
            if i + "__last" in npz.files:
                X.append(npz[i + "__last"]); y.append(a["pol"]); at.append(ai)
    X, y, at = np.array(X, np.float64), np.array(y), np.array(at)
    hit, n = 0, 0
    for a in np.unique(at):
        te = at == a
        p, _ = logreg(X[~te], y[~te].astype(float), X[te])
        hit += int(((p > 0.5) == y[te]).sum()); n += int(te.sum())
    return hit / n


def main() -> int:
    out = {"bar": BAR, "position": "decision-point (after the arrow)", "arms": {}}
    print("H_9303 — the G-PROBE, moved to the position the model answers at")
    print(f"  bar {BAR} FROZEN · held-out n=91 · chance sd 0.0524 = {(BAR-0.5)/0.0524:.2f}σ\n")
    for arm in ARMS:
        X, y, split, blen = load(arm)
        tr, te = split == "train", split == "heldout"
        n_te = int(te.sum()); sd = math.sqrt(0.25 / n_te)

        pte, _ = logreg(X[tr], y[tr].astype(float), X[te])
        acc = float(((pte > 0.5) == y[te]).mean())

        rng = np.random.default_rng(SEED)
        null = np.array([float(((logreg(X[tr], rng.permutation(y[tr]).astype(float), X[te])[0] > 0.5)
                                == y[te]).mean()) for _ in range(N_PERM)])
        pval = float((null >= acc).mean())

        lx = blen[:, None]
        lfloor = float((((logreg(lx[tr], y[tr].astype(float), lx[te])[0] > 0.5) == y[te]).mean()))
        b = np.c_[np.ones(len(blen)), blen]
        coef, *_ = np.linalg.lstsq(b[tr], X[tr], rcond=None)
        R = X - b @ coef
        rte, _ = logreg(R[tr], y[tr].astype(float), R[te])
        acc_res = float(((rte > 0.5) == y[te]).mean())

        live = v_live(arm)
        out["arms"][arm] = {"P_LIN": acc, "perm_p": pval, "perm_p95": float(np.quantile(null, .95)),
                            "length_floor": lfloor, "P_LIN_length_residual": acc_res,
                            "V_LIVE_taught_atoms": live, "n_heldout": n_te, "chance_sd": sd,
                            "exact_p": float(stats.binom.sf(round(acc*n_te)-1, n_te, 0.5))}
        kind = "EXPERIMENT" if arm.startswith("main") else "control  "
        print(f"  {kind} {arm:>13} | held-out P-LIN {acc:.3f} ({(acc-0.5)/sd:+.2f}σ) · perm p={pval:.3f}")
        print(f"  {'':>24}| [V-LIVE taught atoms] {live:.3f}   [V-LENGTH] floor {lfloor:.3f} · "
              f"residual {acc_res:.3f}")

    m = [out["arms"][a] for a in ("main_s7", "main_s11")]
    ctrl = out["arms"]["shuffle_grid"]["V_LIVE_taught_atoms"]
    v_live_ok = all(a["V_LIVE_taught_atoms"] > ctrl for a in m)
    v_base = out["arms"]["base_only"]["P_LIN"] < BAR
    v_len = all(a["P_LIN"] > a["length_floor"] and a["P_LIN_length_residual"] >= BAR for a in m)
    detect = all(a["P_LIN"] >= BAR and a["perm_p"] < 0.05 for a in m)
    partial = all(a["perm_p"] < 0.05 for a in m) and not detect

    print(f"\n  V-LIVE: {'PASS' if v_live_ok else 'FAIL'} (taught atoms read above the untaught "
          f"control {ctrl:.3f})   V-BASE: {'PASS' if v_base else 'FAIL'}")
    if not v_live_ok:
        v = ("⏳ INVALID — the instrument is not live at this position either; no tier.")
    elif detect and v_len:
        v = ("🔓 REPRESENTATION HAS IT — the polarity of a held-out, never-taught atom IS in the "
             "representation at the moment the model must answer. It just does not EMIT it "
             "(H_9286: held-out D-acc = chance). The wall is the COMMIT/output channel, not "
             "grounding — and the O/C objective was aimed at the wrong thing.")
    elif (detect or partial) and not v_len:
        v = ("⏳ LENGTH-CONFOUND — the arms rise but do not clear the length-only floor / do not "
             "survive residualising length. No tier.")
    elif partial:
        v = ("🟡 PARTIAL — some polarity is readable at the decision point but it does not clear the "
             "frozen bar. Report the effect size; the bar does not move.")
    else:
        v = ("🧱 GROUNDING WALL — EARNED, at last on a certified instrument: with the probe at the "
             "position the model answers at, and with the taught atoms proving it can read there, "
             "an untaught atom's polarity is NOT in the representation. This is the honest grounding "
             "wall the lane thought it had, and the O/C channel is now the justified spend.")
    print(f"\nVERDICT: {v}")
    out["verdict"] = v
    json.dump(out, open(os.path.join(HERE, "probe_decision.json"), "w"), ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
