"""AUDIT-A manifest — the atom in its REAL contexts, and the same contexts with a NEUTRAL atom.

The O channel bets that the natural corpus DID form the atom's valence somewhere in the weights and
that the answer slot simply never had a gradient reason to consume it. If the valence was never
formed, there is nothing to bridge and the $21 fire is wasted. So read the atom's own contextualised
position in its real corpus sentences and probe for gold polarity.

But a sentiment review is FULL of sentiment words, so a probe that reads the NEIGHBOURHOOD rather
than the atom would score just as well and we would fire on an illusion. Hence the control that IS
the measurement: every context appears twice —

    arm "atom"  ...배송도 빠르고 가성비는 <ATOM>          (the real atom)
    arm "swap"  ...배송도 빠르고 가성비는 <NEUTRAL>       (a length-matched neutral atom, SAME context)

and the verdict is Delta = probe(atom) - probe(swap) against a permutation null, never a raw value.

NEUTRAL atoms are mined from the corpus itself: frequent stems whose occurrences are polarity-
balanced (|p(pos) - 0.5| < NEUTRAL_TOL), so they carry exposure but no valence. They are drawn ONLY
from non-held-out stems, so nothing about the held-out split leaks.
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "nbind_curriculum"))
sys.path.insert(0, HERE)
import gen_nbindg_n2 as GN2

K_CTX = 24            # contexts per atom (both arms use the SAME contexts)
CTX_BYTES = 64        # left context kept before the atom
NEUTRAL_TOL = 0.05    # |p(positive) - 0.5| must be under this for a stem to count as neutral
MIN_OCC = 200
SEED = 7


def main() -> int:
    import random
    rng = random.Random(SEED)
    rows = GN2.load_corpora()
    meta = [a for a in json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
            if a["split"] == "heldout"]
    held = {a["stem"] for a in meta}

    # neutral inventory: exposed but polarity-balanced, and never a held-out atom
    tot, pos = collections.Counter(), collections.Counter()
    for t, lab in rows:
        for w in set(t.split()):
            if 2 <= len(w) <= 6:
                tot[w] += 1
                pos[w] += int(lab == 1)
    neutral = [w for w, n in tot.items()
               if n >= MIN_OCC and w not in held
               and not any(h in w for h in held)
               and abs(pos[w] / n - 0.5) < NEUTRAL_TOL]
    if not neutral:
        print("ERROR: no neutral inventory", file=sys.stderr)
        return 1
    by_len = collections.defaultdict(list)
    for w in neutral:
        by_len[len(w)].append(w)

    items = []
    for a in meta:
        stem = a["stem"]
        hits = [t for (t, _l) in rows if stem in t]
        rng.shuffle(hits)
        used = 0
        for t in hits:
            i = t.find(stem)
            frag = t[:i][-CTX_BYTES:]                  # the left context, atom excluded
            if not frag.strip():
                continue
            # length-matched neutral: same character length as the atom, so the only thing that
            # moved is WHICH word sits at the read position
            cands = by_len.get(len(stem)) or by_len.get(min(by_len, key=lambda L: abs(L - len(stem))))
            swap = rng.choice(cands)
            items.append({"id": "A_%s_%d" % (stem, used), "prompt": frag + stem,
                          "stem": stem, "pol": int(a["pol"]), "arm": "atom"})
            items.append({"id": "S_%s_%d" % (stem, used), "prompt": frag + swap,
                          "stem": stem, "pol": int(a["pol"]), "arm": "swap"})
            used += 1
            if used >= K_CTX:
                break

    out = os.path.join(HERE, "valence_manifest.json")
    json.dump({"win": 64, "items": items}, open(out, "w"), ensure_ascii=False)
    n_at = len({i["stem"] for i in items})
    print("wrote %s · %d prompts (%d atoms x %d contexts x 2 arms)"
          % (out, len(items), n_at, K_CTX))
    print("neutral inventory: %d stems (occ>=%d · |p(pos)-0.5|<%.2f · non-held-out)"
          % (len(neutral), MIN_OCC, NEUTRAL_TOL))
    print("e.g. atom: %r" % items[0]["prompt"][-28:])
    print("     swap: %r" % items[1]["prompt"][-28:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
