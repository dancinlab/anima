#!/usr/bin/env python3
"""gen_nbind_kform.py — NBIND-FC K-form-coverage corpus (H_next · form-coverage sweep).

Extends gen_nbind's negation inventory to DISTINCT-STEM families and drills K stems (fixed data
budget), holding out the (K+1)-th stem's family for the F2 verdict. Korean has few grammatical
negation stems on sentiment adjectives, so K is bounded — that bound is itself a finding.

flip1 negation STEM families (ordered; each = a distinct-byte negation mechanism on an adj/desc stem):
  1. 안   : "안 " + eojeol
  2. 않   : stem + "지 않다"        (+ conjugation variants for F1)
  3. 못   : "못 " + eojeol           (zero shared bytes with 안/않)
  4. 아니 : stem + "지 아니하다"      (archaic-but-grammatical; zero shared with 안/않/못)
flip0 (polarity-preserving, always present): bare / "정말 "+e / "너무 "+e.

--k-stems K drills the first K stems (all flip1 variants of those stems) + the 3 flip0 forms.
Held-out F2 panel = the (K+1)-th stem family (novel negation MECHANISM, never trained → tests
whether the flip operator abstracts across negation stems, not just conjugations of a drilled one).
F1 panel = novel conjugations of the LAST DRILLED 않-stem (already generalizes at K>=2 per K=6).

out_bit = pol(p) ^ 1 (all eval items flip1). Balanced pol. Item schema = nbind-eval-v1 xbind.
Total train rows fixed via REP scaling (rows ~= constant across K).
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
sys.path.insert(0, HERE)
import gen_nbind as G

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 4302
K = int(sys.argv[sys.argv.index("--k-stems") + 1]) if "--k-stems" in sys.argv else 2
OUTDIR = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else HERE
TARGET_ROWS = 8000        # fixed data budget across K

# STEM families: (stem_id, [train render fns], needs_non_past). render fn: (stem, eojeol) -> surface
STEMS = [
    ("an",   [lambda s, e: "안 " + e], False),
    ("anh",  [lambda s, e: s + "지 않다", lambda s, e: "전혀 " + s + "지 않다"], True),
    ("mot",  [lambda s, e: "못 " + e, lambda s, e: s + "지 못하다"], False),
    ("ani",  [lambda s, e: s + "지 아니하다"], True),
]
FLIP0 = [lambda s, e: e, lambda s, e: "정말 " + e, lambda s, e: "너무 " + e]
# F1 (conjugation-novel of the drilled 않-stem) + F2 (held-out next stem)
F1_ANH = [lambda s, e: s + "지 않아요", lambda s, e: s + "지 않았다", lambda s, e: s + "지 않네"]


def render_ok(stem, needs_non_past):
    return not (needs_non_past and G.is_past_stem(stem))


def main():
    rows_tr = G.load_nsmc(None)
    B = G.build(rows_tr, SEED)
    pol, plist, preds = B["pol"], B["plist"], B["preds"]
    rng = random.Random(SEED + K)

    drilled = STEMS[:K]
    heldout_stem = STEMS[K] if K < len(STEMS) else None

    def span(p):
        s = preds[p]["spans"]
        return (s[0][1] if s else p)

    # ---- training corpus (main = pol^flip, ctrl = shuffled) ----
    cells = []                      # (p, render, flip)
    for p in plist:
        e = span(p)
        for r in FLIP0:
            cells.append((p, r(p, e), 0))
        for sid, rens, npast in drilled:
            if not render_ok(p, npast):
                continue
            for r in rens:
                cells.append((p, r(p, e), 1))
    REP = max(1, TARGET_ROWS // max(1, len(cells)))
    main_lines, ctrl_lines = [], []
    crng = random.Random(SEED + 1000 + K)
    inst = [c for c in cells for _ in range(REP)]
    rng.shuffle(inst)
    for (p, surf, flip) in inst:
        bit = pol[p] ^ flip
        main_lines.append("이 영화 " + surf + " => " + ("긍정." if bit else "부정."))
        cb = 1 if crng.random() < 0.5 else 0
        ctrl_lines.append("이 영화 " + surf + " => " + ("긍정." if cb else "부정."))
    open(os.path.join(OUTDIR, "kform_train.txt"), "w", encoding="utf-8").write("\n".join(main_lines) + "\n")
    open(os.path.join(OUTDIR, "kform_shuffle_train.txt"), "w", encoding="utf-8").write("\n".join(ctrl_lines) + "\n")

    # ---- eval panels ----
    def emit(tag, render_list):
        items = []
        for p in plist:
            e = span(p)
            for r in render_list:
                surf = r(p, e)
                bit = pol[p] ^ 1
                gw = "긍정" if bit else "부정"
                seed_s = "이 영화 " + surf + " => "
                if gw in seed_s:
                    continue
                items.append({"p": p, "form": tag, "a": p, "b": tag, "pol": pol[p], "flip": 1,
                              "xor": bit, "surf": surf, "seed": seed_s,
                              "gold": ("긍정." if bit else "부정."), "counterfactual": ("부정." if bit else "긍정."),
                              "gold_word": gw})
        json.dump({"format": "nbind-eval-v1", "note": "NBIND-FC K=%d %s" % (K, tag),
                   "gen": 8, "win": 64, "heldout": items, "seen": []},
                  open(os.path.join(OUTDIR, "kform_eval_%s.json" % tag), "w", encoding="utf-8"),
                  ensure_ascii=False)
        return len(items)

    n_f1 = emit("f1", F1_ANH) if K >= 2 else 0     # 않-conjugation novel (needs 않 drilled)
    n_f2 = 0
    if heldout_stem:
        sid, rens, npast = heldout_stem
        n_f2 = emit("f2", [rens[0]])               # held-out next stem = novel negation mechanism
    print("K=%d drilled=%s heldout=%s | train_rows=%d(REP=%d) f1=%d f2=%d" %
          (K, [s[0] for s in drilled], heldout_stem[0] if heldout_stem else None,
           len(main_lines), REP, n_f1, n_f2))
    print("KFORM_GEN_DONE")


if __name__ == "__main__":
    main()
