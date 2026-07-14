"""H_9309 DECON — build the declarative store + the PC-NONCE launch gate manifests.

WHY THIS EXPERIMENT EXISTS (measured, not assumed):

  operator   LEARNED    — SEEN flip1 (negation applied to a mastered atom): D-acc 0.950,
                          frac(margin>0) 0.975.  The model composes negation fine.
  polarity   ABSENT     — held-out flip0: frac(margin>0) 0.5057, z=+0.11 (H_9308).  It does not
                          even BET on a held-out atom's polarity.
  polarity   RECOVERABLE— an ideal reader restores it from the very context the model saw:
                          MASKED 29/29 = 1.000, SHUFFLE 0.5172 (H_9291 ORACLE).

So exactly one input is missing, and it is sitting in the data.  DECON hands that one input to
the model through an external declarative store and asks whether the ALREADY-LEARNED operator
can consume it.  This is the A channel — the only one of O/C/A/I/D that survives M1 (the model
never wrote the variable), because it does not need the trunk to hold the variable at all.

THE ANTI-PARROT DESIGN (why flip1 is the primary DV, not flip0):
  The store says "빠르 = 긍정".  On a flip0 trial the gold answer IS 긍정 — so a model that merely
  ECHOES the injected token scores 100% while composing nothing.  On a flip1 trial ("빠르지 않다")
  the gold answer is 부정 — the injected fact points at the WRONG answer.  Parroting LOSES there.
  Only fact ⊗ negation wins.  Hence: flip0 = consumption, flip1 = composition, and the verdict
  rides on flip1.

THE LAUNCH GATE (PC-NONCE) — held-out is not touched until the mechanism is proven to work at all.
  Nonce stems the model cannot know, with a truth we declare.  Two arms:
    NONCE-NOSTORE : empty store.  MUST read chance.  This is the absence proof — measured on the
                    model itself rather than grepped from a corpus we no longer hold.  (It is also
                    the byte-identical parity gate: an empty store must not perturb scoring.)
    NONCE-STORE   : the store carries each nonce's declared polarity.  flip0 proves consumption,
                    flip1 proves composition.
  PC-NONCE fails ⟹ INVALID-MECHANISM ⟹ DO NOT FIRE held-out (its one-shot contact budget is
  preserved).  A probe that fails its own positive control decides nothing — this is the lesson
  that killed H_9303 (sign-acc 0.554), H_9307 (LOO 0.750) and GEN-DIR before it.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")

# The 6 surface forms, verbatim from the n2_eval_manifest construction (nbind-eval-v1).
# flip = does the form invert the atom's base polarity.
FORMS = [
    ("bare", "{s}고",            0),
    ("int1", "정말 {s}고",        0),
    ("int2", "너무 {s}다",        0),
    ("negL", "{s}지 않다",        1),
    ("negS", "안 {s}고",          1),
    ("negE", "전혀 {s}지 않다",    1),
]
TMPL = "이 영화 {surf} => "

# 29 nonce stems — Korean-phonotactic but not words.  We do NOT rely on this being true by
# inspection: the NONCE-NOSTORE arm measures it directly (a nonce carrying a real prior would
# read above chance there, and we would swap it).  That is a stronger claim than a corpus grep,
# and it survives the fact that the 450k CPT corpus is no longer on disk.
NONCE = [
    "뽀길", "츄람", "끄뷔", "삠돌", "웨긋", "쟈쿠", "펄뭇", "힝졸", "꼬뷁", "댕류",
    "쁘칸", "톄묵", "샤긜", "뭉퀄", "흐뎁", "뾰찰", "칵쥬", "튤겅", "붐켸", "쎄퐁",
    "얄믭", "쥐낑", "훠딱", "낍뽀", "먀둥", "겅츨", "빡쉬", "돌캬", "윰챠",
]
# Declared truth, balanced 15/14 to mirror the held-out atom polarity distribution exactly.
NONCE_POL = [i % 2 for i in range(len(NONCE))]


def rows_for(stems, pols):
    out = []
    for stem, pol in zip(stems, pols):
        for form, pat, flip in FORMS:
            gold_pol = pol ^ flip
            gw = "긍정" if gold_pol == 1 else "부정"
            cw = "부정" if gold_pol == 1 else "긍정"
            surf = pat.format(s=stem)
            out.append({"p": stem, "form": form, "a": stem, "b": form, "pol": pol,
                        "flip": flip, "xor": gold_pol, "surf": surf,
                        "seed": TMPL.format(surf=surf),
                        "gold": gw + ".", "counterfactual": cw + ".", "gold_word": gw})
    return out


def main():
    atoms = json.load(open(os.path.join(KEEP, "gt_atoms.json")))["atoms"]
    held = [a for a in atoms if a["split"] == "heldout"]
    assert len(held) == 29, len(held)

    # ---- the real store: the 29 held-out atoms' TRUE polarity.
    # Provenance is the H_9291 ORACLE, which recovered exactly these 29/29 from the model's own
    # left-context.  We are not smuggling in an answer the data did not contain — we are handing
    # over a fact the data fully determines but the trunk declined to write.
    store = {a["stem"]: {"key": a["stem"], "pol": a["pol"]} for a in held}
    json.dump(store, open(os.path.join(HERE, "store_heldout.json"), "w"),
              ensure_ascii=False, indent=1)

    # ---- PC-NONCE: manifest + its store.  Same 6 forms, same template, same 29×6 = 174 shape,
    # so the power of the launch gate equals the power of the test it gates.
    nrows = rows_for(NONCE, NONCE_POL)
    man = {"format": "nbind-eval-v1", "task": "H_9309 DECON PC-NONCE (consumption+composition)",
           "gen": 8, "win": 64, "heldout": nrows, "seen": []}
    json.dump(man, open(os.path.join(HERE, "pc_nonce_manifest.json"), "w"),
              ensure_ascii=False, indent=1)
    nstore = {s: {"key": s, "pol": p} for s, p in zip(NONCE, NONCE_POL)}
    json.dump(nstore, open(os.path.join(HERE, "pc_nonce_store.json"), "w"),
              ensure_ascii=False, indent=1)

    # ---- byte audit, up front.  The window is 64 BYTES and Korean is 3 B/char
    # (a_korean_byte_budget — this exact confusion has cost three experiments).  If a prefix does
    # not fit, the right-aligned window eats its HEAD and the trial silently becomes a no-op that
    # then reads as "the model did not consume the fact".
    real = json.load(open(os.path.join(KEEP, "n2_eval_manifest.json")))["heldout"]
    print("=" * 78)
    print("H_9309 DECON — store + PC-NONCE built")
    print("=" * 78)
    print("store_heldout.json   : %d facts (pol 1=%d 0=%d)"
          % (len(store), sum(1 for v in store.values() if v["pol"] == 1),
             sum(1 for v in store.values() if v["pol"] == 0)))
    print("pc_nonce_manifest    : %d rows / %d nonce atoms (flip0=%d flip1=%d)"
          % (len(nrows), len(NONCE), sum(1 for r in nrows if r["flip"] == 0),
             sum(1 for r in nrows if r["flip"] == 1)))

    print("\n[byte-audit] win=64 · budget = 64 − len(seed) − len(gold), all in BYTES")
    for tag, rows, st in (("heldout", real, store), ("pc-nonce", nrows, nstore)):
        worst = 999
        over_f1 = over_f2 = 0
        for r in rows:
            b = 64 - len(r["seed"].encode()) - max(len(r["gold"].encode()),
                                                   len(r["counterfactual"].encode()))
            worst = min(worst, b)
            f = st[r["p"]]
            pw = "긍정" if f["pol"] == 1 else "부정"
            f1 = len((f["key"] + ":" + pw + ". ").encode())
            f2 = len((pw + ". ").encode())
            over_f1 += int(f1 > b)
            over_f2 += int(f2 > b)
        print("  %-8s n=%-4d tightest budget=%2dB · F1 overflows %d/%d · F2 overflows %d/%d"
              % (tag, len(rows), worst, over_f1, len(rows), over_f2, len(rows)))
    print("\n  F1 = '<stem>:<긍정|부정>. '  F2 = '<긍정|부정>. ' (8B — the deterministic downgrade)")
    print("  A DROPPED trial (neither fits) makes the run INVALID-INSTRUMENT, not a negative.")
    print("\n→ store_heldout.json · pc_nonce_manifest.json · pc_nonce_store.json")


if __name__ == "__main__":
    main()
