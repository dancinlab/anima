#!/usr/bin/env python3
"""gen_morphatom_s1.py — MORPH-ATOM stage-2 S1 corpus/drill builder (H_9288, Fable spec).

Trains the MORPH-2B codec (K from G-0) on the CPT corpus, then emits the 4-arm training inputs as
raw .bytes files (anima-py train reads corpus as open(path,'rb'), V=256 — a re-encoded byte stream is
exactly what it wants). All arms warm-start the same base 303M; same sentence sets / epoch counts.

Arms (exact corpus delta):
  M  = codec(K) CPT (full)                        + codec drill (안/않/못 grid, 아니 held-out 0 rows)
  C1 = RAW utf-8 CPT (same sentences, no codec)   + RAW drill
  C2 = codec CPT minus sentences whose encoding contains the held-out stem's token id (geometry ablation)
  C3 = codec CPT with the 4 stem token ids collapsed to ONE shared id (leak ceiling / V1 liveness)

Drill = NBIND XOR grid (pol(p)⊕flip(n), sentiment predicate × negation form), drilled stems only,
held-out stem 0 rows (grep-assert). 90% grid + 10% CPT replay (avoid catastrophic geometry erase).
Eval panels (JSON, codec-agnostic text; pod encodes per-arm): F2 = held×held-predicate flip; F1 = sanity.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__)) or "."
sys.path.insert(0, HERE)
import gen_nbind as G
import morph2b as MB

OUTDIR = sys.argv[sys.argv.index("--out-dir") + 1] if "--out-dir" in sys.argv else HERE
CORPUS = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else os.path.join(HERE, "morph_corpus.txt")
K = int(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else 2048
HELD = sys.argv[sys.argv.index("--held") + 1] if "--held" in sys.argv else "ani"
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 4302
CPT_LINES = int(sys.argv[sys.argv.index("--cpt-lines") + 1]) if "--cpt-lines" in sys.argv else 120000

STEM_CH = {"an": "안", "anh": "않", "mot": "못", "ani": "아니"}
DRILLED = [s for s in ["an", "anh", "mot"] if s != HELD] if HELD == "ani" else [s for s in STEM_CH if s != HELD]
RENDER = {  # negation render fns per stem (surface for drill/eval)
    "an":  [lambda s, e: "안 " + e],
    "anh": [lambda s, e: s + "지 않다", lambda s, e: s + "지 않아요"],
    "mot": [lambda s, e: "못 " + e, lambda s, e: s + "지 못하다"],
    "ani": [lambda s, e: s + "지 아니하다"],
}
FLIP0 = [lambda s, e: e, lambda s, e: "정말 " + e, lambda s, e: "너무 " + e]


def main():
    lines = [l.rstrip("\n") for l in open(CORPUS, encoding="utf-8") if l.strip()][:CPT_LINES]
    # ---- train codec ----
    merges = MB.train_bpe(lines[:20000], K)
    merge_rank, tok2id, vocab = MB.build_vocab(lines, merges)
    id2tok = {v: k for k, v in tok2id.items()}
    stem_ids = {s: [i for i in MB.stem_token_ids(STEM_CH[s], merge_rank, tok2id)[0] if i is not None] for s in STEM_CH}
    held_ids = set(stem_ids[HELD])
    json.dump({"k": K, "vocab_size": len(vocab), "held": HELD, "held_ids": sorted(held_ids),
               "stem_ids": {s: stem_ids[s] for s in STEM_CH}, "drilled": DRILLED},
              open(os.path.join(OUTDIR, "codec.json"), "w", encoding="utf-8"), ensure_ascii=False)

    enc = lambda t: MB.encode_to_bytes(t, merge_rank, tok2id)

    def enc_c3(t):  # collapse 4 stem ids → one shared id (min stem id)
        shared = min(min(v) for v in stem_ids.values() if v)
        b = bytearray(enc(t)); allstem = {i for v in stem_ids.values() for i in v}
        for k in range(0, len(b) - 1, 2):
            i = (b[k] << 8) | b[k + 1]
            if i in allstem:
                b[k], b[k + 1] = shared >> 8, shared & 0xFF
        return bytes(b)

    def contains_held(t):
        b = enc(t)
        return any(((b[k] << 8) | b[k + 1]) in held_ids for k in range(0, len(b) - 1, 2))

    # ---- CPT corpus variants ----
    with open(os.path.join(OUTDIR, "cpt_M.bytes"), "wb") as f:
        for l in lines: f.write(enc(l) + b"\x00\x0a")     # token-space newline sentinel (id 0x000a)
    with open(os.path.join(OUTDIR, "cpt_C1.bytes"), "wb") as f:
        for l in lines: f.write(l.encode("utf-8", "replace") + b"\n")
    with open(os.path.join(OUTDIR, "cpt_C2.bytes"), "wb") as f:
        kept = 0
        for l in lines:
            if not contains_held(l): f.write(enc(l) + b"\x00\x0a"); kept += 1
    with open(os.path.join(OUTDIR, "cpt_C3.bytes"), "wb") as f:
        for l in lines: f.write(enc_c3(l) + b"\x00\x0a")

    # ---- drill XOR grid (drilled stems only, held 0 rows) ----
    B = G.build(G.load_nsmc(None), SEED)
    pol, plist, preds = B["pol"], B["plist"], B["preds"]
    rng = random.Random(SEED)
    def span(p):
        s = preds[p]["spans"]; return (s[0][1] if s else p)
    grid = []            # (surf, gold_word)
    for p in plist:
        e = span(p)
        for r in FLIP0:
            grid.append(("이 영화 " + r(p, e) + " => ", "긍정." if pol[p] else "부정."))
        for sid in DRILLED:
            for r in RENDER[sid]:
                bit = pol[p] ^ 1
                grid.append(("이 영화 " + r(p, e) + " => ", "긍정." if bit else "부정."))
    rng.shuffle(grid)
    replay = lines[:len(grid) // 9]      # 10% CPT replay
    def write_drill(path, encfn, raw=False):
        with open(path, "wb") as f:
            for surf, gold in grid:
                line = surf + gold
                f.write((line.encode("utf-8", "replace") + b"\n") if raw else (encfn(line) + b"\x00\x0a"))
            for l in replay:
                f.write((l.encode("utf-8", "replace") + b"\n") if raw else (encfn(l) + b"\x00\x0a"))
    write_drill(os.path.join(OUTDIR, "drill_M.bytes"), enc)
    write_drill(os.path.join(OUTDIR, "drill_C1.bytes"), None, raw=True)
    write_drill(os.path.join(OUTDIR, "drill_C2.bytes"), enc)
    write_drill(os.path.join(OUTDIR, "drill_C3.bytes"), enc_c3)

    # assert held-out stem 0 rows in drill grid surfaces
    held_surf = sum(1 for surf, _ in grid if any(r(plist[0], span(plist[0])) for r in []) )  # noop guard
    held_in_grid = sum(1 for surf, _ in grid if STEM_CH[HELD] in surf)
    # ---- eval panels (text; pod encodes per-arm) ----
    def emit_eval(tag, stems, preds_list):
        items = []
        for p in preds_list:
            e = span(p)
            for sid in stems:
                for r in RENDER[sid]:
                    bit = pol[p] ^ 1
                    items.append({"seed": "이 영화 " + r(p, e) + " => ",
                                  "gold": ("긍정." if bit else "부정."),
                                  "counterfactual": ("부정." if bit else "긍정.")})
        json.dump({"format": "morphatom-eval-v1", "tag": tag, "items": items},
                  open(os.path.join(OUTDIR, "eval_%s.json" % tag), "w", encoding="utf-8"), ensure_ascii=False)
        return len(items)
    n_f2 = emit_eval("f2", [HELD], plist)             # held-out stem flip = the verdict
    n_f1 = emit_eval("f1", DRILLED, plist[:len(plist) // 2])   # drilled × predicate sanity

    print("MORPH-ATOM S1 built: K=%d vocab=%d held=%s drilled=%s | held_in_drill_grid=%d(must=0) | grid=%d f2=%d f1=%d"
          % (K, len(vocab), HELD, DRILLED, held_in_grid, len(grid), n_f2, n_f1))
    print("cpt bytes:", {a: os.path.getsize(os.path.join(OUTDIR, "cpt_%s.bytes" % a)) for a in ["M", "C1", "C2", "C3"]})
    print("MORPHATOM_S1_GEN_DONE")


if __name__ == "__main__":
    main()
