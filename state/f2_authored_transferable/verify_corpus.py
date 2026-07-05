#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F2 generated-corpus verification — is the authored corpus transferable-sound (not degenerate)?

Parses the ACTUAL generated corpus (generate_corpus.py output): recovers each concept's (role,value)
from the attribute sentences, then trains a compose head (role x value x rel bilinear cross) on the
train composition sentences and tests held-out (train-concept + unseen-concept) combos vs the
shuffle-rule control. If held-out >> shuffle → the corpus carries held-out-derivable rule structure.

This is TERMINAL for "is the corpus transferable-sound data" (yes/no), DIRECTIONAL for the byte-LM claim
(a byte-LM must infer attributes from text + compose; this verification supplies the parsed attributes
directly). The byte-LM-learns-it-from-raw-text question is the H_9206 ATD crux (running on summer).
$0 numpy, mini-safe. Regenerate the corpus first: python3 generate_corpus.py
"""
import re, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROLE = re.compile(r'작용(\d+)'); VALUE = re.compile(r'성질(\d+)'); RESULT = re.compile(r'상태(\d+)')
NROLE, NVAL, NREL, NRES = 8, 8, 4, 12
RELS = ['결합', '촉발', '변환', '억제']
concept_attr = {}

def parse_attr(line):
    r = ROLE.search(line); v = VALUE.search(line); m = re.search(r'([^\s:]+\d{3})', line)
    if r and v and m:
        concept_attr[m.group(1)] = (int(r.group(1)), int(v.group(1)))

def parse_comp(line):
    names = re.findall(r'([^\s:]+\d{3})', line); res = RESULT.search(line)
    rel = next((i for i, x in enumerate(RELS) if x in line), None)
    if len(names) >= 2 and res and rel is not None:
        return names[0], rel, names[1], int(res.group(1))
    return None

def feat(a, rel, b):
    x = np.zeros(NROLE + NVAL + NREL)
    if a in concept_attr: x[concept_attr[a][0]] = 1
    if b in concept_attr: x[NROLE + concept_attr[b][1]] = 1
    x[NROLE + NVAL + rel] = 1
    ra = concept_attr.get(a, (0, 0))[0]; vb = concept_attr.get(b, (0, 0))[1]
    cross = np.zeros(NROLE * NVAL * NREL); cross[(ra * NVAL + vb) * NREL + rel] = 1
    return np.concatenate([x, cross])

def build(data):
    return np.array([feat(a, rel, b) for a, rel, b, c in data]), np.array([c for a, rel, b, c in data])

def main():
    for line in open(os.path.join(HERE, "corpus_train.txt"), encoding="utf-8"):
        parse_attr(line)
    load = lambda f: [t for t in (parse_comp(l) for l in open(os.path.join(HERE, f), encoding="utf-8")) if t]
    train, test, shuf = load("corpus_train.txt"), load("corpus_heldout_test.txt"), load("corpus_shuffle_control.txt")
    Xtr, ytr = build(train); Xte, yte = build(test); Xsh, ysh = build(shuf)
    Ytr = np.eye(NRES)[ytr]
    A = np.hstack([Xtr, np.ones((len(Xtr), 1))]); W = np.linalg.solve(A.T @ A + np.eye(A.shape[1]), A.T @ Ytr)
    acc = lambda X, y: float(np.mean((np.hstack([X, np.ones((len(X), 1))]) @ W).argmax(1) == y))
    rule_ho, shuf_ho, chance = acc(Xte, yte), acc(Xsh, ysh), 1.0 / NRES
    verdict = "CORPUS-SOUND-TRANSFERABLE" if rule_ho >= 0.7 and rule_ho - shuf_ho >= 0.3 else "CORPUS-DEGENERATE"
    out = {"probe": "F2 generated-corpus verification", "n_concept": len(concept_attr),
           "rule_heldout_acc": round(rule_ho, 4), "shuffle_control_acc": round(shuf_ho, 4),
           "chance": round(chance, 4), "delta": round(rule_ho - shuf_ho, 4), "verdict": verdict,
           "note": "held-out incl unseen-concept combos; TERMINAL for corpus-soundness, DIRECTIONAL for byte-LM (=H_9206 ATD)."}
    json.dump(out, open(os.path.join(HERE, "corpus_verify_RESULT.json"), "w"), ensure_ascii=False, indent=1)
    print(f"rule held-out={rule_ho:.3f} shuffle={shuf_ho:.3f} chance={chance:.3f} delta={rule_ho-shuf_ho:+.3f} -> {verdict}")

if __name__ == "__main__":
    main()
