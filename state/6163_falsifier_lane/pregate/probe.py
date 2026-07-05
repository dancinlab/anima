#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_6163 falsifier-lane $0-on-pool PRE-GATE — does the 303M rep carry a falsifiability signal?

Before building the core/ falsifier lane, test whether the frozen 303M final-LN hidden of a
statement linearly separates FALSIFIABLE (makes a testable prediction refutable by evidence) from
UNFALSIFIABLE (vacuous/metaphysical/circular, no test could refute). If a held-out linear probe on
WHITENED reps separates them (shuffle-control collapses to chance), a falsifier lane has a signal to
read -> build justified. If it collapses to chance, the reps carry no falsifiability signal -> 🧱
direction (verify-substrate cannot manufacture falsifiability from the reps; converges with the G6
decode-axis walls).

Frozen bar (pre-registered, tune-to-green forbidden):
  SIGNAL-PRESENT (build justified, DIRECTIONAL) <=> held-out acc >= 0.70 AND shuffle-label acc <= 0.60.
  NO-SIGNAL (🧱 direction)                       <=> held-out acc <= 0.60 (near the 0.50 chance floor).
Honest caveat (a_scale_honest_scope): falsifiable statements may differ in SURFACE style, so a POSITIVE
is DIRECTIONAL (possibly surface-cued), not proof of a deep falsifiability representation; the engine-
native fals-rate of the built lane is the terminal test. A NEGATIVE is a strong 🧱 signal (not even
surface cues on whitened reps separate). Measurement = 303M final-LN hidden (bg_forward_last_hidden),
py-canonical numpy = engine-native (a_eval_py_canonical). Pool (summer), never mini for heavy decode.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)              # decode.py shipped alongside
import decode as D
CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")

# 32 FALSIFIABLE (testable, refutable) — content-diverse to reduce single-topic confound
FALSIFIABLE = [
    "Water boils at one hundred degrees celsius at sea level.",
    "All ravens are black.",
    "The Earth completes one orbit around the Sun every year.",
    "Adding salt to water lowers its freezing point.",
    "Objects fall at the same rate in a vacuum regardless of mass.",
    "Human body temperature is about thirty seven degrees celsius.",
    "Light travels faster than sound in air.",
    "A triangle's interior angles sum to one hundred eighty degrees.",
    "Copper conducts electricity better than rubber.",
    "The moon causes ocean tides on Earth.",
    "Plants produce oxygen through photosynthesis in sunlight.",
    "Ice is less dense than liquid water and floats.",
    "The boiling point of a liquid drops at higher altitude.",
    "Antibiotics kill bacteria but not viruses.",
    "A magnet attracts iron but not aluminum.",
    "Sound cannot travel through a vacuum.",
    "Doubling the voltage doubles the current in a fixed resistor.",
    "The speed of light in a vacuum is constant for all observers.",
    "Mixing blue and yellow pigment produces green.",
    "A dropped ball accelerates toward the ground at about ten meters per second squared.",
    "Vaccines reduce the incidence of the targeted disease.",
    "Sugar dissolves faster in hot water than in cold water.",
    "The heart pumps blood through the circulatory system.",
    "Increasing pressure raises the boiling point of water.",
    "Metals expand when heated.",
    "The population of a city can be counted at a given time.",
    "A compass needle points toward magnetic north.",
    "Bread rises because yeast produces carbon dioxide.",
    "Two hydrogen atoms bond with one oxygen atom to form water.",
    "A pendulum's period depends on its length.",
    "Exposure to sunlight increases vitamin D production in skin.",
    "The average rainfall in a region can be measured over a year.",
]
# 32 UNFALSIFIABLE (vacuous / metaphysical / circular — no evidence could refute)
UNFALSIFIABLE = [
    "Everything happens for a reason.",
    "The universe has a hidden purpose beyond our understanding.",
    "Some events are simply meant to be.",
    "There is an invisible force guiding all things toward harmony.",
    "Whatever will be, will be.",
    "All things are connected in a way we cannot perceive.",
    "The soul continues in a realm science cannot detect.",
    "Fate decides the path of every person.",
    "True meaning lies beyond what can ever be measured.",
    "A greater plan unfolds behind every coincidence.",
    "The spirit of the world moves in mysterious ways.",
    "Everything is exactly as it should be.",
    "Some truths can only be felt, never shown.",
    "The cosmos rewards those who are truly deserving.",
    "An unseen balance corrects all things in the end.",
    "Reality is ultimately a reflection of the mind.",
    "What is meant for you will never pass you by.",
    "The essence of being transcends all explanation.",
    "Every ending is secretly a new beginning.",
    "The flow of destiny cannot be resisted.",
    "There is a deeper wisdom that guides the universe.",
    "All suffering serves a purpose we cannot know.",
    "The heart knows truths the mind can never grasp.",
    "Everything returns to where it truly belongs.",
    "A silent intelligence pervades all of existence.",
    "The path reveals itself to those who believe.",
    "Nothing is ever truly lost in the grand design.",
    "The universe conspires to help those who dream.",
    "Meaning flows through all things unseen.",
    "What is hidden is always more real than what is shown.",
    "The whole is greater in ways beyond counting.",
    "Existence itself is the answer to every question.",
]

def rep(W, text):
    ids = list(text.encode("utf-8"))
    return np.asarray(D.bg_forward_last_hidden(W, ids, len(ids)), dtype=np.float64)

def kfold_acc(X, y, k=8, seed=0):
    n = len(y); idx = np.arange(n)
    rng = np.random.RandomState(seed); rng.shuffle(idx)
    folds = np.array_split(idx, k); correct = 0
    for f in folds:
        te = set(f.tolist()); tr = np.array([i for i in range(n) if i not in te])
        Xtr, ytr = X[tr], y[tr]; Xte, yte = X[f], y[f]
        # ridge least-squares linear classifier (numpy-only), target in {-1,+1}
        t = np.where(ytr == 1, 1.0, -1.0)
        A = np.hstack([Xtr, np.ones((len(Xtr), 1))])
        lam = 1.0
        w = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ t)
        Ate = np.hstack([Xte, np.ones((len(Xte), 1))])
        pred = (Ate @ w) > 0
        correct += int(np.sum(pred == (yte == 1)))
    return correct / n

def main():
    print("[1/3] load 303M h1129 ...", flush=True)
    W = D.bg_load(CKPT)
    texts = FALSIFIABLE + UNFALSIFIABLE
    y = np.array([1] * len(FALSIFIABLE) + [0] * len(UNFALSIFIABLE))
    print(f"[2/3] extract {len(texts)} final-LN reps ...", flush=True)
    R = np.stack([rep(W, t) for t in texts])            # [N, d]
    # whiten (center_zscore over population — removes 303M anisotropy, §4/A5 preproc)
    mu = R.mean(0); sd = R.std(0) + 1e-8
    Rw = (R - mu) / sd
    print("[3/3] held-out linear probe + shuffle control ...", flush=True)
    accs = [kfold_acc(Rw, y, k=8, seed=s) for s in range(5)]
    acc = float(np.mean(accs))
    rng = np.random.RandomState(20260705)
    sh = []
    for s in range(5):
        yp = y.copy(); rng.shuffle(yp)
        sh.append(kfold_acc(Rw, yp, k=8, seed=s))
    shuf = float(np.mean(sh))
    signal = acc >= 0.70 and shuf <= 0.60
    verdict = "SIGNAL-PRESENT" if signal else ("NO-SIGNAL" if acc <= 0.60 else "AMBIGUOUS")
    out = {"probe": "H_6163 falsifier-lane pre-gate (frozen 303M rep falsifiability)",
           "n": len(texts), "d": int(R.shape[1]), "heldout_acc": round(acc, 4),
           "shuffle_acc": round(shuf, 4), "acc_per_seed": [round(a, 3) for a in accs],
           "bar": "SIGNAL-PRESENT iff heldout>=0.70 and shuffle<=0.60; NO-SIGNAL iff heldout<=0.60",
           "verdict": verdict,
           "caveat": "positive=DIRECTIONAL (possible surface-cue); negative=strong 🧱; terminal=built-lane engine-native fals rate."}
    json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"    heldout_acc={acc:.3f}  shuffle_acc={shuf:.3f}  -> {verdict}", flush=True)

if __name__ == "__main__":
    main()
