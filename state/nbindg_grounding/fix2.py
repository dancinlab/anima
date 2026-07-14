"""Atom-level scoring, done correctly: undo the form flip before voting.

An atom appears in 6 surface forms and three of them (negL/negS/negE) INVERT its polarity, so an
atom's six item-labels are 3 positive and 3 negative by construction. Majority-voting the raw item
labels therefore returns 'negative' for every atom — which is what the previous pass did, making its
gold vector constant and every number on top of it meaningless (including the 0.659 and the wall).

The atom's polarity is the LATENT, and each form's flip is KNOWN. So the eval's own readout is:

    atom_pol_hat = majority over forms of ( item_pred XOR form_flip )

which is exactly the recombination the D-acc eval asks the model for. V-LIVE stays per item (n=120,
balanced 60/60, so 0.5 really is chance there).
"""
import json, math, os
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.expanduser("~/h9300")
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
FLIP = {"bare": 0, "int1": 0, "int2": 0, "negL": 1, "negS": 1, "negE": 1}
BAR, N_PERM, SEED = 0.65, 200, 7


def lr(Xtr, ytr, Xte):
    s = StandardScaler().fit(Xtr)
    m = LogisticRegression(max_iter=5000, C=0.1).fit(s.transform(Xtr), ytr)
    return m.predict(s.transform(Xte))


def live_item(X, y, st):
    hit = n = 0
    for a in np.unique(st):
        te = st == a
        p = lr(X[~te], y[~te].astype(float), X[te])
        hit += int((p == y[te]).sum()); n += int(te.sum())
    return hit / n, n


def atom_from_items(pred, flip, st, gold_atom):
    """Undo each form's flip, then vote. gold_atom = the atom's true base polarity."""
    ats = np.unique(st)
    hit = 0
    for a in ats:
        m = st == a
        votes = np.logical_xor(pred[m] > 0.5, flip[m] == 1)      # recovered atom polarity per form
        hit += int((votes.mean() > 0.5) == (gold_atom[a] > 0.5))
    return hit / len(ats), len(ats)


meta = json.load(open(os.path.join(HERE, "pos91_meta.json")))
base = {a["stem"]: a["pol"] for a in json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]}
print("H_9303 — certified instrument · atom polarity recovered by undoing the form flip\n")
out = {"bar": BAR, "arms": {}}
for arm in ARMS:
    Z = np.load(os.path.join(HERE, "hid", "pos91_%s.npz" % arm))
    rec = [(m, Z[m["id"] + "__last"]) for m in meta if m["id"] + "__last" in Z.files]
    X = np.array([v for _, v in rec], np.float64)
    y = np.array([m["pol"] for m, _ in rec])
    fl = np.array([FLIP[m["form"]] for m, _ in rec])
    sp = np.array([m["split"] for m, _ in rec]); st = np.array([m["stem"] for m, _ in rec])
    tr, te = sp == "train", sp == "heldout"

    live, n_live = live_item(X[tr], y[tr], st[tr])
    pred = lr(X[tr], y[tr].astype(float), X[te])
    acc, n_at = atom_from_items(pred, fl[te], st[te], base)
    sd = math.sqrt(0.25 / n_at)
    rng = np.random.default_rng(SEED)
    null = np.array([atom_from_items(lr(X[tr], rng.permutation(y[tr]).astype(float), X[te]),
                                     fl[te], st[te], base)[0] for _ in range(N_PERM)])
    pv = float((null >= acc).mean())
    out["arms"][arm] = {"V_LIVE_item": live, "heldout_atom_acc": acc, "n_atoms": n_at,
                        "perm_p": pv, "chance_sd": sd, "perm_p95": float(np.quantile(null, .95))}
    k = "EXPERIMENT" if arm.startswith("main") else "control  "
    print("  %s %13s | [V-LIVE item n=%d] %.3f   held-out ATOM %.3f (%+.2fσ) · perm p=%.3f · null p95 %.3f"
          % (k, arm, n_live, live, acc, (acc - .5) / sd, pv, np.quantile(null, .95)))

m7, m11 = out["arms"]["main_s7"], out["arms"]["main_s11"]
ctrl = out["arms"]["shuffle_grid"]["V_LIVE_item"]
live_ok = m7["V_LIVE_item"] > ctrl and m11["V_LIVE_item"] > ctrl
detect = all(a["heldout_atom_acc"] >= BAR and a["perm_p"] < .05 for a in (m7, m11))
partial = all(a["perm_p"] < .05 for a in (m7, m11)) and not detect
print("\n  n=%d held-out ATOMS · sd %.4f · bar 0.65 = %.2fσ · V-LIVE %s (%.3f/%.3f vs control %.3f)"
      % (m7["n_atoms"], m7["chance_sd"], (BAR-.5)/m7["chance_sd"],
         "PASS" if live_ok else "FAIL", m7["V_LIVE_item"], m11["V_LIVE_item"], ctrl))
v = ("⏳ INVALID — instrument not live; no tier." if not live_ok else
     "🔓 GROUNDED BUT NOT EMITTED — a never-taught atom's polarity IS in the representation at the answer point." if detect else
     "🟡 PARTIAL — above the permutation null but below the frozen bar." if partial else
     "🧱 GROUNDING WALL — EARNED at honest power on a certified instrument.")
print("\nVERDICT:", v)
out["verdict"] = v
json.dump(out, open(os.path.join(HERE, "probe91_atomfix.json"), "w"), ensure_ascii=False, indent=1)
