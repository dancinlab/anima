#!/usr/bin/env python3
"""H_9235 H2-lite — frozen probe-prompt spec generator (procedural · torch-free · FREEZE before dump).
32 concepts (12 ρ·weave-gate + 20 common nouns, mutually distinct) · 16 content-matched paraphrases each,
each prompt ENDS with the concept word so the T=24 last-position penultimate hidden = the concept ATOM.
Zero-unary-MI 5-bit codes assigned by seeded permutation(seed 7) → XOR operator target (bit-marginal 0.5,
MI(bit;atom)=0) — matches operator_test.py (H_9234) verbatim so its harness/bars transfer.
Emits: concepts.json (code+paraphrases), unary_prompts.json (32×16=512 items, 8/8 train/test split),
pair_prompts.json (seeded pair subset, per-position dumped for rung b). NO answer in any prompt (evaluate-py-2)."""
import json, hashlib
# 32 concepts — first 5 = ρ·weave gate (rho_fan cz-aligned), rest = common perceptual/abstract nouns
CONCEPTS = ["consciousness", "tension", "memory", "silence", "dream",
            "ocean", "fire", "mountain", "river", "forest",
            "city", "music", "light", "shadow", "wind",
            "stone", "bird", "tree", "star", "moon",
            "sun", "cloud", "rain", "snow", "storm",
            "mirror", "clock", "door", "window", "bridge",
            "garden", "flame"]
assert len(CONCEPTS) == 32 and len(set(CONCEPTS)) == 32
# 16 content-matched templates, each ENDS with the concept (last-pos hidden = atom)
TEMPLATES = ["The {c}", "I think about the {c}", "She spoke of the {c}", "A story about the {c}",
             "There was only {c}", "Deep inside the {c}", "They found the {c}", "He dreamed of the {c}",
             "The idea of the {c}", "Far beyond the {c}", "Words about the {c}", "The meaning of the {c}",
             "We remember the {c}", "Nothing but the {c}", "The nature of the {c}", "Close to the {c}"]
assert len(TEMPLATES) == 16

def seeded_perm(n, seed):
    """deterministic LCG permutation (torch/numpy-free, reproducible)."""
    idx = list(range(n)); s = seed & 0xFFFFFFFF
    for i in range(n - 1, 0, -1):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        j = s % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return idx

# 5-bit codes: permute 0..31 (seed 7) → each concept a distinct code → all 32 codes present (bit-marginal 0.5)
perm = seeded_perm(32, 7)
codes = {CONCEPTS[i]: [(perm[i] >> b) & 1 for b in range(4, -1, -1)] for i in range(32)}
# verify zero-unary-MI: every bit-position marginal == 0.5 over the 32 atoms
import statistics
for b in range(5):
    m = statistics.mean(codes[c][b] for c in CONCEPTS)
    assert abs(m - 0.5) < 1e-9, (b, m)

concepts_out = {c: {"idx": i, "code": codes[c],
                    "paraphrases": [t.format(c=c) for t in TEMPLATES]}
                for i, c in enumerate(CONCEPTS)}

# unary prompts: 32×16, split 8 train / 8 test paraphrases (held-out paraphrase generalization)
unary = []
for i, c in enumerate(CONCEPTS):
    for k, t in enumerate(TEMPLATES):
        unary.append({"id": "%s__p%d" % (c, k), "prompt": t.format(c=c),
                      "concept": c, "cidx": i, "split": "train" if k < 8 else "test"})

# pair prompts: mirror operator_test held-out split (150 held-out of 32*31). per-position dump for rung b.
pairs_all = [(a, b) for a in range(32) for b in range(32) if a != b]
pperm = seeded_perm(len(pairs_all), 7)
held = []
seen_set = set()
for k in pperm:
    ab = pairs_all[k]
    if len(held) < 150 and ab not in seen_set:
        held.append(ab); seen_set.add(ab)
train_pairs = [p for p in pairs_all if p not in seen_set]
# pair prompt: "The {A} and the {B}" (both concepts present, NO xor answer — target is synthetic code)
def pair_prompt(a, b): return "The %s and the %s" % (CONCEPTS[a], CONCEPTS[b])
pair_items = []
for tag, plist in (("train", train_pairs), ("held", held)):
    for (a, b) in plist:
        pair_items.append({"id": "%s_%d_%d" % (tag, a, b), "prompt": pair_prompt(a, b),
                           "a": a, "b": b, "split": tag})

def dump(obj, name):
    s = json.dumps(obj, ensure_ascii=False, indent=1)
    open(name, "w").write(s)
    return hashlib.sha256(s.encode()).hexdigest()[:12]

sha_c = dump(concepts_out, "concepts.json")
sha_u = dump({"n_items": len(unary), "items": unary, "concepts_sha": sha_c}, "unary_prompts.json")
sha_p = dump({"n_items": len(pair_items), "n_train": len(train_pairs), "n_held": len(held),
              "items": pair_items, "concepts_sha": sha_c}, "pair_prompts.json")
print("FROZEN concepts.sha=%s unary(%d).sha=%s pairs(%d train=%d held=%d).sha=%s" %
      (sha_c, len(unary), sha_u, len(pair_items), len(train_pairs), len(held), sha_p))
