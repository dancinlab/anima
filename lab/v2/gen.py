"""lab/v2/gen.py — synthetic operator x store-fact stream.

@canonical-ok — 'v2' is not a version bump of anima/; it is a parallel toy research
substrate that coexists permanently with core/ (owner-named, 2026-07-16).

The task is the minimal mirror of the BINDING wall (H_9327/H_9359): the FACT lives only in
the store, the OPERATOR lives only in the text, and the answer requires binding the two.

    store: {lumo: good, vipek: bad, ...}   (8 slots, one is the queried entity)
    text : "is lumo => good"   (identity)
           "not lumo => bad"   (negation)

Both operators are FREE and PRE-POSED at the same slot, so operator identity is never
confounded with position (the EN discriminator, CLAUDE.md EN-FIRST).

THE HEART — per-example rotation: every example re-draws every polarity in its store.
An entity's polarity is therefore inconsistent ACROSS examples, so the expected return of
memorising entity->polarity into the weights is exactly 0.5 (chance). Every point above
chance must have come through the bridge. Any slower schedule pays partial credit for
in-window memorisation and dilutes the pressure to learn to query; SLOWROT (bars.json)
isolates that.
"""

import hashlib

import numpy as np

CONSONANTS = "bdfgklmnprstvz"
VOWELS = "aeiou"

OP_IS = 0
OP_NOT = 1
POL_GOOD = 0
POL_BAD = 1

ANSWER_BYTES = {POL_GOOD: b"good", POL_BAD: b"bad"}


def entity_pool(n_total, name_len=5):
    """Deterministic CVCVC pool. Sorted + sliced => the train/eval split is a pure
    function of (n_total, name_len), independent of any run seed."""
    if name_len != 5:
        raise ValueError("name_len is pinned to 5 (bars.json task.entity_bytes)")
    names = []
    for c0 in CONSONANTS:
        for v0 in VOWELS:
            for c1 in CONSONANTS:
                for v1 in VOWELS:
                    for c2 in CONSONANTS:
                        names.append(c0 + v0 + c1 + v1 + c2)
    names = sorted(set(names))
    if len(names) < n_total:
        raise ValueError("pool too small")
    # stride-sample so train/eval share the same character distribution
    idx = np.linspace(0, len(names) - 1, n_total).astype(int)
    return [names[i] for i in idx]


def split_pool(n_total, n_train, n_eval):
    """Disjoint train/eval entity sets. Interleaved (every k-th name is held out) so both
    halves are drawn from the same region of the name space — novelty must be 'a new key
    built from seen bytes', not 'a different distribution'."""
    if n_train + n_eval != n_total:
        raise ValueError("split must exhaust the pool")
    pool = entity_pool(n_total)
    ratio = n_total // n_eval  # e.g. 512/128 = 4 -> every 4th name is held out
    train, ev = [], []
    for i, nm in enumerate(pool):
        (ev if i % ratio == ratio - 1 else train).append(nm)
    if len(train) != n_train or len(ev) != n_eval:
        raise ValueError(f"split arithmetic: got {len(train)}/{len(ev)}")
    if set(train) & set(ev):
        raise ValueError("train/eval overlap")
    return train, ev


def render(op, entity):
    """Prompt bytes. The query position is the LAST prompt byte — the hidden there is what
    predicts the first answer byte, so that is where the bridge forms its query."""
    op_s = "is" if op == OP_IS else "not"
    return f"{op_s} {entity} => ".encode("ascii")


def truth(op, polarity):
    if op == OP_IS:
        return polarity
    return POL_BAD if polarity == POL_GOOD else POL_GOOD


class Stream:
    """Seeded example stream. No corpus file — examples are generated on the fly and the
    stream is reproducible from (seed, entities, n_slots)."""

    def __init__(self, seed, entities, n_slots, rotate_every=1):
        self.rng = np.random.default_rng(seed)
        self.entities = list(entities)
        self.n_slots = n_slots
        self.rotate_every = rotate_every  # 1 = per-example (COTRAIN); >1 = SLOWROT
        self._held = None
        self._held_age = 0

    def _draw_store(self):
        """Pick n_slots distinct entities and a FRESH polarity for each."""
        idx = self.rng.choice(len(self.entities), size=self.n_slots, replace=False)
        names = [self.entities[i] for i in idx]
        pols = self.rng.integers(0, 2, size=self.n_slots)
        return names, pols

    def example(self):
        if self._held is None or self._held_age >= self.rotate_every:
            self._held = self._draw_store()
            self._held_age = 0
        names, pols = self._held
        self._held_age += 1

        slot = int(self.rng.integers(0, self.n_slots))
        op = int(self.rng.integers(0, 2))
        entity = names[slot]
        polarity = int(pols[slot])
        return {
            "store_names": names,
            "store_pols": np.asarray(pols, dtype=np.int64),
            "slot": slot,
            "op": op,
            "polarity": polarity,
            "prompt": render(op, entity),
            "answer": ANSWER_BYTES[truth(op, polarity)],
        }

    def batch(self, n):
        return [self.example() for _ in range(n)]


def stream_sha(seed, entities, n_slots, n=2000):
    """Determinism witness (C0-c): the same seed must reproduce the same stream bytes."""
    s = Stream(seed, entities, n_slots)
    h = hashlib.sha256()
    for ex in s.batch(n):
        h.update(ex["prompt"])
        h.update(ex["answer"])
        h.update(bytes(ex["store_pols"].tolist()))
        h.update("".join(ex["store_names"]).encode())
    return h.hexdigest()


def assert_no_eval_leak(seed, train_entities, eval_entities, n_slots, n_probe=100_000):
    """C0-a: an eval entity must NEVER appear in the training stream — not as a store key,
    not as a prompt substring. A gate that scores a stratum the corpus reinforces is a
    forgery that always passes (cpt-destroys-what-corpus-omits); this is the opposite —
    the judged stratum must be 0-shot. Hard-assert: a leak aborts the build."""
    ev = set(eval_entities)
    s = Stream(seed, train_entities, n_slots)
    hits = 0
    for ex in s.batch(n_probe):
        if ev.intersection(ex["store_names"]):
            hits += 1
            continue
        text = ex["prompt"].decode("ascii")
        if any(name in text for name in ev):
            hits += 1
    if hits > 0:
        raise AssertionError(f"C0-a EVAL KEY LEAK: {hits} hits in {n_probe} examples")
    return hits


if __name__ == "__main__":
    import json
    import os
    import sys

    bars = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bars.json")))
    t = bars["task"]
    train, ev = split_pool(t["entity_pool"], t["entity_train"], t["entity_eval"])
    print(f"pool={t['entity_pool']} train={len(train)} eval={len(ev)} disjoint=True")
    print(f"  train[:4]={train[:4]}  eval[:4]={ev[:4]}")

    s = Stream(7, train, t["store_slots"])
    ex = s.example()
    print(f"  example prompt={ex['prompt']!r} answer={ex['answer']!r} op={ex['op']} pol={ex['polarity']}")

    print("C0-a checking eval-key leak over 100k training examples ...")
    hits = assert_no_eval_leak(7, train, ev, t["store_slots"])
    print(f"  C0-a PASS: leak hits = {hits}")

    a = stream_sha(7, train, t["store_slots"])
    b = stream_sha(7, train, t["store_slots"])
    print(f"C0-c determinism: {a[:16]} == {b[:16]} -> {a == b}")
    sys.exit(0 if (hits == 0 and a == b) else 1)
