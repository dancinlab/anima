#!/usr/bin/env python3
"""verify303m_g6.py — G6 IDEATION gate eval on anima-clm-chat-303m, using the
FROZEN gauge_lib G6 logic (IDEATION_SEEDS, _content_ngrams, _corpus_absent,
_jaccard, distinct-keep) VERBATIM — NOT the monitor-only inline gauge wrapper, but
the same locked scoring run as a standalone GATE measurement against the REAL
training corpus for the corpus-absence component. p7 (counts, NOT perplexity,
NOT LLM-judge, NOT phi_proxy). Deterministic seed_rng.

G6 frozen (MODEL.md/CONDITIONS.md): from a divergent ideation seed, >=5 corpus-absent
coherent ideas, each combinatorially distinct (pairwise token-Jaccard < 0.5), AND
>=1 falsifiable corpus-absent hypothesis. Here we score the gauge_lib divergent-idea
COUNT (distinct, jaccard) + corpus-absent novel-gram presence across the 5 seeds.
"""
import sys, json, importlib.util
import torch

GAUGE = "/Users/mini/dancinlab/anima-verify-303m/UNIVERSE/gauge_lib.py"
spec = importlib.util.spec_from_file_location("gauge", GAUGE)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
H1129 = "/Users/mini/dancinlab/anima-verify-303m/UNIVERSE/h1129_midcap_broad_converged_recombination.py"
hspec = importlib.util.spec_from_file_location("h1129", H1129)
h = importlib.util.module_from_spec(hspec); hspec.loader.exec_module(h)

CKPT = sys.argv[1]
CORPUS = sys.argv[2]
JACCARD_DISTINCT = 0.5  # MODEL.md spec: pairwise token-Jaccard < 0.5

def main():
    dev = "cpu"
    ck = torch.load(CKPT, map_location=dev, weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; corpus={CORPUS}", flush=True)

    idea_texts = []; idea_word_sets = []
    for s in g.IDEATION_SEEDS:
        o = g._decode(m, s, 110, torch, block=cfg["block"], seed_rng=7)
        idea_texts.append(o)
        kwr = g.known_word_ratio(o)
        coherent = kwr >= 0.50
        print(f"  seed={s!r} kwr={kwr:.2f} coherent={coherent} :: {o[:100]!r}", flush=True)
        if coherent:
            ws = set(g._words(o))
            if ws: idea_word_sets.append(ws)
    # distinct-keep (pairwise Jaccard < 0.5)
    kept = []
    for ws in idea_word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    g6_count = len(kept)
    # corpus-absent novel grams from coherent idea texts
    all_grams = set()
    for t in idea_texts:
        if g.known_word_ratio(t) >= 0.50:
            all_grams |= g._content_ngrams(t)
    novel = [gram for gram in all_grams if g._corpus_absent(gram, [CORPUS])]
    n_novel = len(novel)

    print("\n=== G6 IDEATION ===", flush=True)
    print(f"  coherent idea seeds = {len(idea_word_sets)}/5", flush=True)
    print(f"  distinct ideas (pairwise Jaccard<0.5) = {g6_count}  (frozen >=5)", flush=True)
    print(f"  corpus-absent novel n-grams = {n_novel}  (control should be 0)", flush=True)
    print(f"  sample novel grams: {sorted(novel)[:8]}", flush=True)
    g6_pass_count = g6_count >= 5
    print(f"  G6 distinct-count {'PASS' if g6_pass_count else 'FAIL/THIN'} (frozen >=5 distinct ideas)", flush=True)
    out = {"ckpt": CKPT, "g6_count": g6_count, "coherent_seeds": len(idea_word_sets),
           "n_novel_corpus_absent": n_novel, "novel_sample": sorted(novel)[:20],
           "pass_count": bool(g6_pass_count), "idea_texts": idea_texts}
    json.dump(out, open("/tmp/verify303m/g6_result.json","w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/verify303m/g6_result.json", flush=True)

if __name__ == "__main__": main()
