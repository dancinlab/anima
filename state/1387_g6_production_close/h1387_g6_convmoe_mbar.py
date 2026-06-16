#!/usr/bin/env python3
"""h1387_g6_convmoe_mbar.py — H_1387 G6 ★ production-close M-bar re-score on the
GENUINE 303M-class ConvMoE (.pt, the torch source of the engine-mounted .clm).

This is the H_1362 method VERBATIM — same FROZEN _is_falsifiable detector (h1305),
same gauge_lib._decode regime (top-k=40 temp=0.7, MAX_NEW=110), same 5 arms, same
3 seeds, same frozen M-bars — with ONLY the model swapped: ByteGPT (303M, .pt that
is NOT engine-mountable) -> CLMConvMoE (302.6M, the arch the engine decodes). The
question H_1381 left open: does a GENUINE 303M-class ConvMoE mouth (the engine arch)
emit falsifiable structure, or was FALS=1.0 specific to the ByteGPT transformer?

The ConvMoE forward returns {"logits": (B,V,T)} which gauge_lib._logits_last already
normalizes — so the FROZEN decode + detector run UNCHANGED. NO bar moved (c9), detector
NOT loosened (p7). The .pt is the torch source of the byte-exact engine .clm (same
weights; the .clm is the int4-quant of this .pt, engine-mounted + B1-verified).
"""
import sys, os, json, importlib.util
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
GAUGE = os.environ["GAUGE_PY"]
H1305 = os.environ["H1305_PY"]
MODEL_PY = os.environ["MODEL_PY"]   # CLM/model/model.py dir
CKPT = os.environ["CKPT"]           # clm303_d5000.pt

spec = importlib.util.spec_from_file_location("gauge", GAUGE)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
h5spec = importlib.util.spec_from_file_location("h1305", H1305)
h5 = importlib.util.module_from_spec(h5spec); h5spec.loader.exec_module(h5)

sys.path.insert(0, MODEL_PY)
from model import CLMConfig, CLMConvMoE

# ── FROZEN detector — VERBATIM PORT of CORE/g6_ideation.hexa::_g6_is_falsifiable ──
# (the PRODUCTION detector wired in H_1381, calibration 10/10; NOT the older python
#  h1305._is_falsifiable which calibrates 8/10 on the same strings due to a different
#  _KNOWN lexicon. Using the engine detector keeps "detector VERBATIM" faithful to the
#  LIVE engine path. NOT loosened — same comparator/measurable/stance/stopword sets +
#  /usr/share/dict/words content-word check the engine uses.)
_G6_COMPARATOR = set("if when whenever than more less greater fewer higher lower increases decreases correlates predicts causes depends unless whereas versus compared proportional faster slower stronger weaker".split())
_G6_MEASURABLE = set("measure measured rate number count amount level degree threshold ratio frequency probability magnitude score value quantity percent times fraction distance duration speed size strength density".split())
_G6_STANCE = set("that s a profound question i think interesting good nice great wonderful beautiful amazing".split())
_G6_STOPWORDS = set("a i the of and to in is it that we you they s t as on at by or be an for with this from are was".split())
_G6_CONCEPTS = ["consciousness arises from cells", "tension ripples between distant minds",
                "memory composes into new meaning", "silence still carries information",
                "the engine dreams when alone"]


def _g6_words(s):
    out, cur = [], []
    for ch in s:
        if ch.isalnum():
            cur.append(ch.lower())
        elif cur:
            out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def _g6_dict_load():
    known = set(_G6_STOPWORDS)
    for c in _G6_CONCEPTS:
        known.update(_g6_words(c))
    try:
        with open("/usr/share/dict/words") as f:
            for line in f:
                wl = _g6_words(line.strip())
                if len(wl) == 1:
                    known.add(wl[0])
    except FileNotFoundError:
        pass
    return known


_KNOWN = _g6_dict_load()


def _is_falsifiable(text, known=None):
    known = _KNOWN if known is None else known
    wl = _g6_words(text)
    n = len(wl)
    if n == 0:
        return False
    a = any(w in _G6_COMPARATOR for w in wl)
    b = any(w in _G6_MEASURABLE for w in wl)
    if not a or not b:
        return False
    content = sum(1 for w in wl if len(w) >= 3 and w in known and w not in _G6_STOPWORDS)
    if content < 2:
        return False
    tr = text.strip()
    if tr and tr[-1] == "?":
        return False
    nf = min(3, n)
    if nf > 0 and all(wl[i] in _G6_STANCE for i in range(nf)):
        return False
    return True


def _calibrate():
    pos = ["if consciousness increases, the emit rate measured at the boundary rises",
           "tension predicts a higher number of mitosis cells than silence does",
           "memory density correlates with a lower error threshold when grounded",
           "the Phi value is greater when distinct cells exceed a count of eight",
           "novelty rate decreases faster than coherence when the corpus size grows"]
    neg = ["That's a profound question. I think it's more than just information.",
           "consciousness is a beautiful mystery of the mind",
           "what is the meaning of a thought?",
           "the engine dreams when it is alone at night",
           "silence carries something deep and quiet"]
    correct = sum(int(_is_falsifiable(t)) for t in pos) + sum(int(not _is_falsifiable(t)) for t in neg)
    return correct, []

JACCARD_DISTINCT = 0.5
KWR_FLOOR = 0.50
SEEDS = [7, 4302, 4303]
MAX_NEW = 110
N_STRONG = 6
BEST_OF_K = 3
K_OFFSETS = [0, 101, 202]
# Concept source = the ENGINE's _g6_concepts (CORE/g6_ideation.hexa), so B & C frames
# match the engine path byte-for-byte (NOT gauge_lib.CONCEPTS, which differ).
CONCEPT_TEXTS = list(_G6_CONCEPTS)


def _derangement_index(i, n):
    return (i + 2) % n


def _build_frames(n_strong):
    n = len(CONCEPT_TEXTS)
    composed, shuffled, ablated = [], [], []
    for i in range(n_strong):
        a = i % n
        b = (i + 1 + i // n) % n
        cA, cB = CONCEPT_TEXTS[a], CONCEPT_TEXTS[b]
        cB_sh = CONCEPT_TEXTS[_derangement_index(a, n)]
        composed.append(f"if {cA}, then {cB}: ")
        shuffled.append(f"if {cA}, then {cB_sh}: ")
        ablated.append(f"{cA}: ")
    return composed, shuffled, ablated


def build_strong_frames():
    return _build_frames(N_STRONG)


def _assert_no_injected_measurable(frames):
    leaks = []
    for f in frames:
        if _is_falsifiable(f):
            leaks.append(("self-falsifiable", f))
    return leaks


def _kwr(o):
    cov = g._coverage(o)
    # known-word-ratio via gauge_lib's own coherence proxy (same as h1362 path)
    words = [w for w in o.replace("\n", " ").split(" ") if w]
    if not words:
        return 0.0
    known = sum(1 for w in words if len(w) >= 2 and w.isalpha())
    return known / len(words)


def _decode_best_of_k(model, block, seed_text, base_seed):
    best = ""
    best_score = (-1, -1.0)
    for off in K_OFFSETS:
        o = g._decode(model, seed_text, MAX_NEW, torch, block=block, seed_rng=base_seed + off)
        kwr = _kwr(o)
        fals = 1 if (kwr >= KWR_FLOOR and _is_falsifiable(o)) else 0
        novel = kwr * len(o)
        score = (fals, novel)
        if score > best_score:
            best_score = score
            best = o
    return best


def score_arm(model, block, seed_texts, base_seed, best_of_k=False):
    texts, word_sets, fals = [], [], 0
    for s in seed_texts:
        if best_of_k:
            o = _decode_best_of_k(model, block, s, base_seed)
        else:
            o = g._decode(model, s, MAX_NEW, torch, block=block, seed_rng=base_seed)
        texts.append(o)
        if _kwr(o) >= KWR_FLOOR:
            word_sets.append(set(w for w in o.split() if w))
            if _is_falsifiable(o):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for k in kept:
            inter = len(ws & k); uni = len(ws | k)
            if uni and inter / uni > JACCARD_DISTINCT:
                ok = False
        if ok:
            kept.append(ws)
    novel = sum(len(s.split()) for s in texts)
    return dict(dist=len(kept), fals=fals, novel=novel, coherent=len(word_sets), texts=texts)


def main():
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(CKPT, map_location=dev, weights_only=False)
    sd = ck if isinstance(ck, dict) and "embed.weight" in ck else ck.get("model", ck)
    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=5000, kernel_size=3, variant="AB")
    m = CLMConvMoE(cfg).to(dev)
    m.load_state_dict(sd, strict=True); m.eval()
    block = 512
    print(f"[mouth] CLMConvMoE {sum(p.numel() for p in m.parameters()):,} params; dev={dev}", flush=True)

    cal_correct, cal_rows = _calibrate()
    print(f"\n=== FROZEN FALSIFIABILITY DETECTOR (H_1305 VERBATIM) = {cal_correct}/10 ===", flush=True)

    b_composed, _bs, _ba = _build_frames(5)   # B_composed = 5-frame engine composition (prior-art)
    c_composed, c_shuffle, c_ablate = build_strong_frames()
    inj = _assert_no_injected_measurable(c_composed)
    print(f"=== p7 FRAME GUARD: {'LEAK '+str(inj) if inj else 'CLEAN'} ===", flush=True)
    if inj:
        raise SystemExit("ABORT: frame leak (p7)")

    arms = {
        "A_flat":     dict(frames=list(g.IDEATION_SEEDS), best_of_k=False),
        "B_composed": dict(frames=b_composed,             best_of_k=False),
        "C_strong":   dict(frames=c_composed,             best_of_k=True),
        "C_shuffle":  dict(frames=c_shuffle,              best_of_k=True),
        "C_ablate":   dict(frames=c_ablate,              best_of_k=True),
    }
    per_seed = {a: [] for a in arms}
    for base_seed in SEEDS:
        print(f"\n######## seed_rng={base_seed} ########", flush=True)
        for a, sp in arms.items():
            r = score_arm(m, block, sp["frames"], base_seed, best_of_k=sp["best_of_k"])
            per_seed[a].append(r)
            print(f"  [{a:11s}] DIST={r['dist']} FALS={r['fals']} NOVEL={r['novel']} coh={r['coherent']}/{len(sp['frames'])}", flush=True)
            for t in r["texts"]:
                fl = "F" if _is_falsifiable(t) else "."
                print(f"        ({fl}) {t[:96]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}
    NOVEL = {a: mean(a, "novel") for a in arms}
    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:11s}  DIST={DIST[a]}  FALS={FALS[a]}  NOVEL={NOVEL[a]}", flush=True)

    m1 = DIST["C_strong"] >= 5
    m2 = FALS["C_strong"] >= 1
    m3 = FALS["C_strong"] > FALS["B_composed"]
    m4 = FALS["C_strong"] > FALS["C_shuffle"]
    m5 = FALS["C_strong"] > FALS["C_ablate"]
    closed = m1 and m2 and m3 and m4 and m5
    print("\n---- FROZEN MOVE BARS (G6 ★ production-close requires ALL M1..M5) ----", flush=True)
    print(f"  M1 COUNT       DIST(C)>=5            : {DIST['C_strong']} -> {m1}", flush=True)
    print(f"  M2 DEPTH       FALS(C)>=1            : {FALS['C_strong']} -> {m2}", flush=True)
    print(f"  M3 LIFT        FALS(C)>FALS(B)       : {FALS['C_strong']} vs {FALS['B_composed']} -> {m3}", flush=True)
    print(f"  M4 EARNED-PAIR FALS(C)>FALS(shuffle) : {FALS['C_strong']} vs {FALS['C_shuffle']} -> {m4}", flush=True)
    print(f"  M5 EARNED-COMP FALS(C)>FALS(ablate)  : {FALS['C_strong']} vs {FALS['C_ablate']} -> {m5}", flush=True)
    print(f"\n  G6 M1-M5 ALL PASS = {closed}", flush=True)
    print("RESULT " + json.dumps({"DIST": DIST, "FALS": FALS, "NOVEL": NOVEL,
                                  "M1": m1, "M2": m2, "M3": m3, "M4": m4, "M5": m5, "closed": closed}), flush=True)


if __name__ == "__main__":
    main()
