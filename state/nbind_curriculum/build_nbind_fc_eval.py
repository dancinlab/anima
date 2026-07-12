#!/usr/bin/env python3
"""build_nbind_fc_eval.py — NBIND-FC K=6 form-novel eval harness (H_next · Fable spec).

Reconstructs the FROZEN K=6 training grid (gen_nbind.build seed 4302) -> pol[p], plist, preds.
The K=6 grid drilled negation forms: negL(지 않다)/negS(안 V)/negE(전혀 …지 않다) [flip1] + bare/정말/너무 [flip0].
Emits two HELD-OUT-FORM eval manifests (all flip1, predicates trained-known, only the negation SURFACE is novel):
  F1 (conjugation-novel): unseen conjugations of the SAME 지-않- stem (않아요/않았다/않네) — shares neg-stem byte 않.
  F2 (lexeme-novel):      wholly untrained neg lexeme 못+V — ZERO shared neg-stem bytes with 않/안/전혀.
gold_word = label[pol(p) ^ 1] (flip1). Tests whether the flip operator abstracts over negation SURFACE.
Item schema = nbind-eval-v1 xbind (a=p, b=F1|F2, gold_word, seed, gold, counterfactual). b encodes the panel.
Run co-located with gen_nbind.py. Output nbind_fc_{f1,f2}_manifest.json for `anima-py evaluate --xbind`.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
sys.path.insert(0, HERE)
import gen_nbind as G

SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 4302
OUTDIR = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else HERE

# F1: novel conjugations of the trained 지-않- stem (trained form = stem+"지 않다").
F1_SUFFIXES = ["지 않아요", "지 않았다", "지 않네"]
# F2: untrained neg lexeme — 못 + eojeol (ability-negation surface; zero shared bytes with 않/안/전혀).
def f2_render(span_eojeol):
    return "못 " + span_eojeol


def main():
    rows_tr = G.load_nsmc(None)
    B = G.build(rows_tr, SEED)
    pol, plist, preds = B["pol"], B["plist"], B["preds"]

    def emit(tag, render_fn):
        items = []
        for p in plist:
            spans = preds[p]["spans"]
            carrier, ej = (spans[0] if spans else (None, p))
            # F1 uses the STEM (p) for the 지-않- conjugation; F2 uses the eojeol surface.
            if tag == "f1":
                if G.is_past_stem(p):     # 지 않- ungrammatical on a ㅆ-past stem (gen_nbind rule)
                    continue
                surfs = [p + suf for suf in F1_SUFFIXES]
            else:
                surfs = [render_fn(ej)]
            bit = pol[p] ^ 1              # flip1
            gold_word = "긍정" if bit else "부정"
            for surf in surfs:
                seed_s = "이 영화 " + surf + " => "
                if gold_word in seed_s:          # echo-guard
                    continue
                items.append({"p": p, "form": tag, "a": p, "b": tag,
                              "pol": pol[p], "flip": 1, "xor": bit,
                              "surf": surf, "seed": seed_s,
                              "gold": ("긍정." if bit else "부정."),
                              "counterfactual": ("부정." if bit else "긍정."),
                              "gold_word": gold_word})
        man = {"format": "nbind-eval-v1",
               "note": "NBIND-FC K=6 %s form-novel flip1 (predicate trained·negation surface novel). "
                       "gold=frozen training-grid pol^1." % tag,
               "gen": 8, "win": 64, "heldout": items, "seen": []}
        path = os.path.join(OUTDIR, "nbind_fc_%s_manifest.json" % tag)
        json.dump(man, open(path, "w", encoding="utf-8"), ensure_ascii=False)
        pol_bal = sum(1 for it in items if it["pol"] == 1)
        print("[%s] n=%d pol1=%d pol0=%d -> %s" % (tag, len(items), pol_bal, len(items) - pol_bal, path))
        return len(items)

    print("frozen grid: |plist|=%d pol-balance=%d/%d" % (len(plist), sum(pol.values()), len(plist)))
    n1 = emit("f1", None)
    n2 = emit("f2", f2_render)
    print("FC-EVAL-BUILD-DONE f1=%d f2=%d" % (n1, n2))


if __name__ == "__main__":
    main()
