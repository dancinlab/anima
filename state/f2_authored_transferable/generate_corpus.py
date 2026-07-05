#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F2 rule-structured transferable-form corpus GENERATOR (per CORPUS_DESIGN.md).

Production-form (anima-register) realization of the attribute-transfer rule corpus that the F2 poc
(#3035) proved enables held-out transfer. Distinct from the H_9206 ATD toy generator — this is the
anima-register (ko/en × general/sns) surface form for the eventual 303M retrain (a_chat_registers).

Rule: each concept has role_type in R and value_type in V. A fixed non-commutative lookup
  compose(role_type(a), rel, value_type(b)) -> result_type
determines the outcome C. Held-out (a,b) combos are DERIVABLE because compose is over ATTRIBUTES.
Shuffle-rule control corpus: same surface, C = rule-independent random (form-priming guard, H_9128).
$0, no model. Emits train / test(held-out combos) / shuffle-control.
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20260705
N_CONCEPT = 200
N_ROLE = 8
N_VALUE = 8
N_RESULT = 12
RELS = ["결합", "촉발", "변환", "억제"]           # non-commutative relations
HELDOUT_FRAC = 0.15                                # fraction of (a,b,rel) combos held out
N_TRAIN_SENT = 60000

rng = random.Random(SEED)

# concept names: anima-register-ish tokens (mix ko/en). placeholder vocab; swap for real 4-cell vocab.
def make_concepts():
    ko = ["빛", "결", "파동", "고요", "울림", "흐름", "매듭", "씨앗", "잔향", "무게",
          "온도", "그늘", "번짐", "여백", "층", "결정", "회로", "숨", "궤도", "farb"]
    concepts = []
    for i in range(N_CONCEPT):
        base = rng.choice(ko)
        name = f"{base}{i:03d}"
        concepts.append({"name": name, "role": rng.randrange(N_ROLE), "value": rng.randrange(N_VALUE)})
    return concepts

def compose_table():
    # fixed deterministic non-commutative rule: (role, rel, value) -> result_type
    tbl = {}
    for r in range(N_ROLE):
        for rel in range(len(RELS)):
            for v in range(N_VALUE):
                tbl[(r, rel, v)] = rng.randrange(N_RESULT)
    return tbl

RESULT_NAMES = [f"상태{k:02d}" for k in range(N_RESULT)]
ROLE_NAMES = [f"작용{r}" for r in range(N_ROLE)]
VALUE_NAMES = [f"성질{v}" for v in range(N_VALUE)]

# 4-cell register surface templates (ko/en × general/sns)
def attr_sentence(c):
    t = rng.choice([
        f"{c['name']}는 {ROLE_NAMES[c['role']]}의 작용을 지니고 {VALUE_NAMES[c['value']]}의 성질을 띤다.",
        f"{c['name']}: {ROLE_NAMES[c['role']]} 작용 · {VALUE_NAMES[c['value']]} 성질 ㅇㅇ",
        f"{c['name']} carries a {ROLE_NAMES[c['role']]} action and a {VALUE_NAMES[c['value']]} quality.",
        f"ngl {c['name']} is pure {ROLE_NAMES[c['role']]}-action w/ {VALUE_NAMES[c['value']]} vibe",
    ])
    return t

def compose_sentence(a, b, rel, result_name):
    t = rng.choice([
        f"{a['name']}가 {b['name']}를 {RELS[rel]}하면 {result_name}가 된다.",
        f"{a['name']} {RELS[rel]} {b['name']} → {result_name} 임 ㅋㅋ",
        f"When {a['name']} {RELS[rel]}s {b['name']}, it becomes {result_name}.",
        f"{a['name']}→{b['name']} ({RELS[rel]}) ends up {result_name} fr",
    ])
    return t

def gen(concepts, tbl):
    # split concepts into train/heldout to also test unseen-concept transfer
    idx = list(range(N_CONCEPT)); rng.shuffle(idx)
    tr_c = set(idx[:int(N_CONCEPT * 0.8)]); te_c = set(idx[int(N_CONCEPT * 0.8):])

    def result_of(a, b, rel):
        return RESULT_NAMES[tbl[(a["role"], rel, b["value"])]]

    # attribute statements for ALL concepts (both train & test concepts get their attrs stated)
    attr_lines = [attr_sentence(concepts[i]) for i in range(N_CONCEPT) for _ in range(3)]
    rng.shuffle(attr_lines)

    # compose sentences: train combos vs held-out combos
    train, test, shuf = [], [], []
    seen = set()
    # train: pairs among train concepts
    tr_list = list(tr_c)
    while len(train) < N_TRAIN_SENT:
        a, b = rng.choice(tr_list), rng.choice(tr_list); rel = rng.randrange(len(RELS))
        if a == b: continue
        key = (a, b, rel)
        if rng.random() < HELDOUT_FRAC:            # hold out some train-concept combos
            if key not in seen:
                seen.add(key)
                test.append(compose_sentence(concepts[a], concepts[b], rel, result_of(concepts[a], concepts[b], rel)))
                # shuffle-rule control: same pair, RANDOM result (rule-independent)
                shuf.append(compose_sentence(concepts[a], concepts[b], rel, rng.choice(RESULT_NAMES)))
            continue
        train.append(compose_sentence(concepts[a], concepts[b], rel, result_of(concepts[a], concepts[b], rel)))
    # test also: unseen-concept combos (stronger transfer)
    te_list = list(te_c)
    for _ in range(2000):
        a, b = rng.choice(te_list), rng.choice(te_list); rel = rng.randrange(len(RELS))
        if a == b: continue
        test.append(compose_sentence(concepts[a], concepts[b], rel, result_of(concepts[a], concepts[b], rel)))

    train_corpus = attr_lines + train; rng.shuffle(train_corpus)
    return train_corpus, test, shuf, len(tr_c), len(te_c)

def main():
    concepts = make_concepts(); tbl = compose_table()
    train_corpus, test, shuf, ntr, nte = gen(concepts, tbl)
    out = HERE
    open(os.path.join(out, "corpus_train.txt"), "w", encoding="utf-8").write("\n".join(train_corpus) + "\n")
    open(os.path.join(out, "corpus_heldout_test.txt"), "w", encoding="utf-8").write("\n".join(test) + "\n")
    open(os.path.join(out, "corpus_shuffle_control.txt"), "w", encoding="utf-8").write("\n".join(shuf) + "\n")
    meta = {"generator": "F2 rule-structured attribute-transfer (anima-register)",
            "n_concept": N_CONCEPT, "n_role": N_ROLE, "n_value": N_VALUE, "n_result": N_RESULT,
            "rels": RELS, "heldout_frac": HELDOUT_FRAC, "train_concepts": ntr, "test_concepts": nte,
            "train_lines": len(train_corpus), "heldout_test_lines": len(test), "shuffle_lines": len(shuf),
            "rule": "compose(role(a),rel,value(b))->result_type (fixed, non-commutative)",
            "held_out": "combos held out (train-concept combos + unseen-concept combos); attrs of ALL concepts stated in train",
            "control": "shuffle_control = same pairs with rule-independent random result (form-priming guard H_9128)",
            "measure": "byte-LM trained on corpus_train → held-out composed-C accuracy on corpus_heldout_test must beat corpus_shuffle_control (pre-reg kill); anima evaluate --py G1 ladder for TERMINAL."}
    json.dump(meta, open(os.path.join(out, "corpus_meta.json"), "w"), ensure_ascii=False, indent=1)
    print(f"train {len(train_corpus)} · heldout_test {len(test)} · shuffle {len(shuf)} lines")
    print("sample train:", train_corpus[0])
    print("sample heldout:", test[0])

if __name__ == "__main__":
    main()
