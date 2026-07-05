#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_6163 pre-gate v2 — MINIMAL-PAIR surface-controlled falsifiability probe.

The v1 pre-gate found the naive falsifiability signal (rep held-out 0.759) was a SURFACE-LEXICAL
artifact (char-3gram baseline 0.894 > rep). v2 removes the surface confound with MINIMAL PAIRS: each
pair shares the same subject noun phrase and uses a qualitative (no-number) predicate, so falsifiable
vs unfalsifiable differ mainly in the TESTABILITY of the claim, not concrete/quantitative vocabulary.

Runs BOTH in one pass:
  - 303M rep probe (whitened final-LN hidden, held-out linear).
  - char-3gram SURFACE baseline (no model) on the SAME statements.
Decision (pre-registered):
  GENUINE-REP-SIGNAL  <=> rep held-out >= 0.65 AND (rep - surface) >= 0.08  (rep beats surface).
  SURFACE-ONLY / 🧱   <=> rep - surface <= 0.05 (rep no better than raw surface).
  If BOTH drop to chance on minimal pairs -> the v1 signal was purely the concrete/abstract vocab axis.
Honest scope: falsifiability partly correlates with concreteness, so a residual surface gap may remain;
the test is whether the 303M rep adds signal ABOVE tightened surface. Measurement = bg_forward_last_hidden
(py-canonical numpy, engine-native). Pool (summer) for the 303M forwards.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decode as D
CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")

# 28 minimal pairs: (falsifiable, unfalsifiable) — shared subject, qualitative predicate, no numbers
PAIRS = [
    ("The treatment lowers blood pressure.", "The treatment restores inner balance."),
    ("The diet reduces body weight.", "The diet aligns the body with its rhythm."),
    ("The training raises test scores.", "The training awakens true potential."),
    ("The vaccine prevents the infection.", "The vaccine strengthens the will to heal."),
    ("The medicine relieves the pain.", "The medicine releases trapped energy."),
    ("The supplement raises iron levels.", "The supplement nourishes the spirit."),
    ("The therapy reduces anxiety.", "The therapy reunites the self."),
    ("The fertilizer increases the crop yield.", "The fertilizer honors the ancient soil."),
    ("The filter removes the particles.", "The filter purifies the essence of air."),
    ("The policy lowers unemployment.", "The policy restores lost purpose."),
    ("The plan reduces the costs.", "The plan returns dignity to workers."),
    ("The route shortens the commute.", "The route leads toward destiny."),
    ("The update fixes the crash.", "The update brings peace to the code."),
    ("The paint dries on the wall.", "The paint breathes life into the wall."),
    ("The seed germinates in the soil.", "The seed holds the dream of a forest."),
    ("The pump moves water through the pipe.", "The pump gives the garden a heartbeat."),
    ("The sensor detects the motion.", "The sensor feels the presence of life."),
    ("The battery powers the device.", "The battery gives the device a soul."),
    ("The bridge carries the load.", "The bridge connects distant hearts."),
    ("The engine burns the fuel.", "The engine embodies the open road."),
    ("The material resists the heat.", "The material carries the earth's memory."),
    ("The course improves the typing speed.", "The course unlocks the writer within."),
    ("The app increases daily activity.", "The app brings mindfulness to life."),
    ("The drug slows the tumor growth.", "The drug realigns the body's fate."),
    ("The lamp brightens the room.", "The lamp fills the room with warmth of being."),
    ("The exercise strengthens the muscles.", "The exercise frees the trapped spirit."),
    ("The signal reaches the receiver.", "The signal touches the listening soul."),
    ("The rain wets the ground.", "The rain blesses the waiting earth."),
]

def rep(W, text):
    ids = list(text.encode("utf-8"))
    return np.asarray(D.bg_forward_last_hidden(W, ids, len(ids)), dtype=np.float64)

def kfold_acc(X, y, k=8, seed=0):
    n = len(y); idx = np.arange(n); rng = np.random.RandomState(seed); rng.shuffle(idx)
    correct = 0
    for f in np.array_split(idx, k):
        te = set(f.tolist()); tr = np.array([i for i in range(n) if i not in te])
        t = np.where(y[tr] == 1, 1.0, -1.0); A = np.hstack([X[tr], np.ones((len(tr), 1))])
        w = np.linalg.solve(A.T @ A + 1.0 * np.eye(A.shape[1]), A.T @ t)
        Ate = np.hstack([X[f], np.ones((len(f), 1))]); pred = (Ate @ w) > 0
        correct += int(np.sum(pred == (y[f] == 1)))
    return correct / n

def surface_feats(texts):
    grams = set()
    for t in texts:
        s = t.lower()
        for i in range(len(s) - 2): grams.add(s[i:i+3])
    grams = sorted(grams); gi = {g: i for i, g in enumerate(grams)}
    X = np.zeros((len(texts), len(grams)))
    for r, t in enumerate(texts):
        s = t.lower()
        for i in range(len(s) - 2): X[r, gi[s[i:i+3]]] += 1
    return (X - X.mean(0)) / (X.std(0) + 1e-8)

def main():
    texts = [f for f, u in PAIRS] + [u for f, u in PAIRS]
    y = np.array([1] * len(PAIRS) + [0] * len(PAIRS))
    print(f"[1/3] load 303M · {len(texts)} minimal-pair statements ...", flush=True)
    W = D.bg_load(CKPT)
    print("[2/3] 303M reps ...", flush=True)
    R = np.stack([rep(W, t) for t in texts])
    Rw = (R - R.mean(0)) / (R.std(0) + 1e-8)
    rep_acc = float(np.mean([kfold_acc(Rw, y, k=8, seed=s) for s in range(5)]))
    print("[3/3] surface char-3gram baseline ...", flush=True)
    Xs = surface_feats(texts)
    surf_acc = float(np.mean([kfold_acc(Xs, y, k=8, seed=s) for s in range(5)]))
    rng = np.random.RandomState(20260705); sh = []
    for s in range(5):
        yp = y.copy(); rng.shuffle(yp); sh.append(kfold_acc(Rw, yp, k=8, seed=s))
    shuf = float(np.mean(sh))
    delta = rep_acc - surf_acc
    if rep_acc >= 0.65 and delta >= 0.08: verdict = "GENUINE-REP-SIGNAL"
    elif delta <= 0.05: verdict = "SURFACE-ONLY"
    else: verdict = "AMBIGUOUS"
    out = {"probe": "H_6163 minimal-pair surface-controlled falsifiability pre-gate", "n": len(texts),
           "rep_heldout": round(rep_acc, 4), "surface_heldout": round(surf_acc, 4),
           "rep_minus_surface": round(delta, 4), "shuffle": round(shuf, 4), "verdict": verdict,
           "bar": "GENUINE iff rep>=0.65 AND rep-surface>=0.08; SURFACE-ONLY iff rep-surface<=0.05"}
    json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"    rep={rep_acc:.3f} surface={surf_acc:.3f} delta={delta:+.3f} shuffle={shuf:.3f} -> {verdict}", flush=True)

if __name__ == "__main__":
    main()
