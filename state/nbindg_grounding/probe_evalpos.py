"""H_9303-EVALPOS — the probe at the position AND in the carrier the eval itself uses.

H_9303's first firing appended " => " to a NATURAL review context and the instrument died there
(V-LIVE: taught atoms 0.419/0.362 vs the untaught control 0.477). Reference-matching the eval
manifest explains why: the eval NEVER shows the model a natural context. Its query is

    seed = "이 영화 빠르고 => "        (the TAUGHT carrier, carrying the held-out atom)

so " => " glued onto a review is out of distribution, and the model's decision machinery — which
H_9302 proved fires inside the taught carrier (0.633/0.673 vs control 0.408) — never engages.

That reference-match also dissolves the contrast the whole lane was built on:

    ORACLE (H_9291)  is GIVEN the natural context and reads the polarity out of it   (evidence in
                                                                                      the query)
    MODEL  (the eval) is GIVEN "이 영화 <atom> => " with NO context and must emit the polarity
                                                                     (evidence must be IN THE WEIGHTS)

These are different tasks. "The information is in the input but not in the representation" was never
a coherent sentence: at the eval's query the information is not in the input at all.

So the question that is actually on the table, asked in the eval's own carrier:

    Does the model's representation, at the moment it must answer, carry the polarity of a held-out
    atom it was never taught — i.e. did the natural distribution GROUND that atom in the weights?

  reads   -> grounding happened; the polarity is there but the model does not EMIT it (held-out
             D-acc = chance). The wall is COMMIT, not grounding.
  chance  -> the first honest grounding wall, on a certified instrument.

V-LIVE (in-distribution now): the 20 taught atoms in this same carrier must read above the untaught
shuffle_grid control. Without that, no number is read.
"""
import json, math, os, subprocess
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.expanduser("~/h9300")
ANIMA = os.path.expanduser("~/.local/bin/anima-py")
CKPT = os.path.expanduser("~/anima-weights/natem_n2")
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
BAR, N_PERM, SEED = 0.65, 200, 7


def lr(Xtr, ytr, Xte):
    s = StandardScaler().fit(Xtr)
    m = LogisticRegression(max_iter=5000, C=0.1).fit(s.transform(Xtr), ytr)
    return m.predict(s.transform(Xte))


def loo_by_atom(X, y, stem):
    hit = n = 0
    for a in np.unique(stem):
        te = stem == a
        p = lr(X[~te], y[~te].astype(float), X[te])
        hit += int((p == y[te]).sum()); n += int(te.sum())
    return hit / n


def main():
    meta = json.load(open(os.path.join(HERE, "evalpos_meta.json")))
    out = {"bar": BAR, "arms": {}}
    print("H_9303-EVALPOS — the probe in the carrier the EVAL itself queries with")
    print("  taught atoms (in-distribution positive control) + 174 held-out eval items\n")
    for arm in ARMS:
        npz_p = os.path.join(HERE, "hid", "evalpos_%s.npz" % arm)
        if not os.path.exists(npz_p):
            subprocess.run([ANIMA, "evaluate", os.path.join(CKPT, "natem_n2_%s.clm" % arm),
                            "--dump-hidden", os.path.join(HERE, "evalpos_prompts.json"),
                            "--out", npz_p, "--win", "64"], check=True, capture_output=True)
        Z = np.load(npz_p)
        rec = [(m, Z[m["id"] + "__last"]) for m in meta if m["id"] + "__last" in Z.files]
        X = np.array([v for _, v in rec], np.float64)
        y = np.array([m["pol"] for m, _ in rec])
        sp = np.array([m["split"] for m, _ in rec])
        st = np.array([m["stem"] for m, _ in rec])
        tr, te = sp == "train", sp == "heldout"

        live = loo_by_atom(X[tr], y[tr], st[tr])                     # V-LIVE, in-distribution
        acc = float((lr(X[tr], y[tr].astype(float), X[te]) == y[te]).mean())
        n_te = int(te.sum()); sd = math.sqrt(0.25 / n_te)
        rng = np.random.default_rng(SEED)
        null = np.array([float((lr(X[tr], rng.permutation(y[tr]).astype(float), X[te]) == y[te]).mean())
                         for _ in range(N_PERM)])
        p = float((null >= acc).mean())
        out["arms"][arm] = {"V_LIVE_taught": live, "heldout_P_LIN": acc, "perm_p": p,
                            "n_heldout": n_te, "chance_sd": sd}
        kind = "EXPERIMENT" if arm.startswith("main") else "control  "
        print("  %s %13s | [V-LIVE taught] %.3f   held-out %.3f (%+.2fσ) · perm p=%.3f"
              % (kind, arm, live, acc, (acc - 0.5) / sd, p))

    m7, m11 = out["arms"]["main_s7"], out["arms"]["main_s11"]
    ctrl = out["arms"]["shuffle_grid"]["V_LIVE_taught"]
    live_ok = m7["V_LIVE_taught"] > ctrl and m11["V_LIVE_taught"] > ctrl
    detect = all(a["heldout_P_LIN"] >= BAR and a["perm_p"] < 0.05 for a in (m7, m11))
    partial = all(a["perm_p"] < 0.05 for a in (m7, m11)) and not detect
    print("\n  V-LIVE: %s (taught %.3f/%.3f vs untaught control %.3f)"
          % ("PASS" if live_ok else "FAIL", m7["V_LIVE_taught"], m11["V_LIVE_taught"], ctrl))
    if not live_ok:
        v = "⏳ INVALID — the instrument is not live even in the eval's own carrier; no tier."
    elif detect:
        v = ("🔓 GROUNDED BUT NOT EMITTED — a held-out atom's polarity IS in the representation at "
             "the moment the model must answer, yet held-out D-acc is chance. The natural "
             "distribution DID ground the atom; the wall is the COMMIT/output channel, not "
             "grounding — and the O/C objective was aimed at the wrong stage.")
    elif partial:
        v = ("🟡 PARTIAL — some of the held-out polarity is readable at the answer point but it does "
             "not clear the frozen bar. Effect size reported; the bar does not move.")
    else:
        v = ("🧱 GROUNDING WALL — EARNED on a certified instrument: with the probe in the eval's own "
             "carrier, and the taught atoms proving it reads there, an untaught atom's polarity is "
             "NOT in the representation when the model must answer. The natural distribution did not "
             "ground it. NOW the O/C channel is the justified spend.")
    print("\nVERDICT:", v)
    out["verdict"] = v
    json.dump(out, open(os.path.join(HERE, "probe_evalpos.json"), "w"), ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
