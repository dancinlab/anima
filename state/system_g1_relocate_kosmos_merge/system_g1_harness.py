#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# system-G1 relocation harness (Direction A) — RUNNABLE numpy DIRECTIONAL smoke.
#
#   Relocates recombination OUT of the mouth-only path (g_eval_g1 @
#   cli/evaluate.py:155 calls ONLY mouth.ideate) INTO the pipe:
#       held-out DISTANT pair (A,B)
#         → Stage M   frozen mouth ideate(A), ideate(B)            (G0 fluency)
#         → Stage K   kosmos_merge: recursive labeled-parent bind  (A,B as children)
#         → Stage B   brain vbasal_select realize + release        (selection)
#         → output C_text / C_tension
#
#   THE anti-artifact gate = bind-RECOVERABILITY on the SURFACED output C:
#   an independent recoverer R reads ONLY C (the merge-store parent ids are
#   HARD-BLOCKED from R) and must recover both parents as top-2 of an N=8 pool.
#   Reading the store instead would be a 24/24 by-construction lookup = ZERO
#   credit (H_1874 / H_6152 lesson).  SCRAMBLE ablation proves R reads
#   compositional STRUCTURE (bigrams), not bag-of-words.
#
#   numpy ⇒ DIRECTIONAL only (a_engine_native_learning).  A GREEN verdict needs
#   the rung(2)-(4) engine-native ladder (see FREEZE.txt / card).  The mouth here
#   is a TOY (small vocab/dim) — NOT the 303M .clm (that is a pool follow-on).
# ═══════════════════════════════════════════════════════════════════════════
import random
from collections import Counter

# ── frozen bar (see FREEZE.txt — do NOT move post-hoc) ──────────────────────
SEEDS         = [7, 42, 4302]
M             = 24          # held-out DISTANT concept pairs (8 base × 3 seeds)
N_DISTRACT    = 8           # recoverer pool size (2 parents + 6 distractors)
COV_BAR       = M // 2      # 12
REC_BAR       = M // 2      # 12
LEAK_BAR      = (N_DISTRACT - 2) / N_DISTRACT   # random distractor-fraction floor = 0.75
SCRAMBLE_DROP = M // 2      # 12

# ── toy concept lexicon: disjoint vocabularies (DISTANT by construction) ─────
# each concept = an ordered signature phrase; disjointness ⇒ H_1599 data control.
CONCEPTS = {
    "ocean":    ["tide", "salt", "wave", "deep"],
    "forest":   ["moss", "branch", "fern", "canopy"],
    "engine":   ["piston", "fuel", "gear", "torque"],
    "music":    ["chord", "tempo", "melody", "rhythm"],
    "market":   ["price", "trade", "stock", "ledger"],
    "medicine": ["dose", "fever", "immune", "remedy"],
    "desert":   ["dune", "cactus", "mirage", "arid"],
    "galaxy":   ["orbit", "nebula", "comet", "stellar"],
    "kitchen":  ["knife", "simmer", "flour", "roast"],
    "law":      ["statute", "verdict", "counsel", "appeal"],
    "glacier":  ["crevasse", "moraine", "frost", "calve"],
    "circuit":  ["resistor", "voltage", "solder", "diode"],
}
GLUE = ["and", "then", "with", "so"]     # register glue — shared across concepts


# ── Stage M: TOY frozen mouth ───────────────────────────────────────────────
# A real mouth = cli/evaluate.py::_Mouth(ckpt).ideate(seed, gen, top_k, temp, rng).
# The toy surfaces a concept's ordered signature phrase; `arm` selects behaviour
# for the JOINT realization only (Stage B), the mouth-floor arm being the honest
# model of the real 303M mouth.
class ToyMouth:
    def __init__(self, arm):
        self.arm = arm                      # "compositional" | "mouthfloor"

    def ideate_single(self, concept, seed):
        toks = list(CONCEPTS[concept])
        g = GLUE[seed % len(GLUE)]
        # ordered phrase: tok0 GLUE tok1 tok2 GLUE tok3  → internal signature bigrams
        return [toks[0], g, toks[1], toks[2], g, toks[3]]

    # Stage B realization: mouth conditioned on the merged composite → joint C.
    def realize_joint(self, frag_a, frag_b, seed):
        if self.arm == "compositional":
            # block-concat both parent fragments (each parent's internal bigrams
            # preserved) + a joint connector → C surfaces BOTH concepts.
            return frag_a + ["then"] + frag_b
        # mouthfloor: surface only the dominant (first) concept — models the real
        # g_eval_g1 floor where composed coverage never exceeds max_single.
        return frag_a


# ── Stage K: kosmos_merge — recursive labeled-parent bind (A,B as children) ──
# rung(2): core/kosmos_io.hexa fn kosmos_merge(anchor_a, anchor_b) -> anchor_c.
# lane "recomb" is DISJOINT from emit-drive lanes {0,4} (a_substrate_disjoint).
def kosmos_merge(frag_a, frag_b):
    a = {"text": frag_a, "lane": "recomb"}
    b = {"text": frag_b, "lane": "recomb"}
    c = {"text": None, "lane": "recomb", "children": (a, b)}   # store keeps ids
    return a, b, c


# ── embeddings: BIGRAM feature vector (order-sensitive ⇒ scramble is meaningful)
def embed_bigrams(tokens):
    return Counter(zip(tokens, tokens[1:]))

def cos(u, v):
    dot = sum(u[k] * v.get(k, 0) for k in u)
    nu = sum(x * x for x in u.values()) ** 0.5
    nv = sum(x * x for x in v.values()) ** 0.5
    return dot / (nu * nv + 1e-9)


# ── coverage (mirrors _g_coverage @ cli/evaluate.py:144): #concepts touched ──
def coverage(tokens, concepts):
    tokset = set(tokens)
    return sum(1 for cpt in concepts if any(t in tokset for t in CONCEPTS[cpt]))


# ── INDEPENDENT recoverer R — reads ONLY C, parent ids HARD-BLOCKED ──────────
def recover_parents(C_tokens, pool, scramble=False, seed=0):
    toks = list(C_tokens)
    if scramble:
        random.Random(seed).shuffle(toks)      # destroy bigram structure
    cvec = embed_bigrams(toks)
    scored = sorted(
        ((name, cos(cvec, embed_bigrams(CONCEPTS[name]))) for name in pool),
        key=lambda kv: -kv[1],
    )
    return {scored[0][0], scored[1][0]}         # top-2


# ── build the M held-out DISTANT pairs (disjoint-vocab by construction) ──────
def build_pairs():
    names = list(CONCEPTS)
    # 8 distinct cross-concept pairs (any two distinct concepts = disjoint vocab)
    idx = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (0, 6), (3, 9)]
    base = [(names[i], names[j]) for (i, j) in idx]
    pairs = []
    for s in SEEDS:                                                  # ×3 = M=24
        for (a, b) in base:
            pairs.append((a, b, s))
    return pairs[:M]


def distractor_pool(a, b, seed):
    others = [n for n in CONCEPTS if n not in (a, b)]
    random.Random(seed).shuffle(others)
    pool = [a, b] + others[: N_DISTRACT - 2]
    # shuffle the FULL pool so zero-cosine ties do NOT resolve to the parents
    # (else parent identity leaks via list order, not via C's structure).
    random.Random(seed + 999).shuffle(pool)
    return pool


# ── run one arm over all M pairs ────────────────────────────────────────────
def run_arm(arm):
    mouth = ToyMouth(arm)
    results = []
    for (a, b, seed) in build_pairs():
        # Stage M — frozen single-concept fragments
        frag_a = mouth.ideate_single(a, seed)
        frag_b = mouth.ideate_single(b, seed)
        max_single = max(coverage(frag_a, [a, b]), coverage(frag_b, [a, b]))  # = 1
        # Stage K — kosmos merge (store keeps A,B as children)
        _pa, _pb, comp = kosmos_merge(frag_a, frag_b)
        # Stage B — brain realizes/releases joint C from the composite
        ca, cb = comp["children"]
        C = mouth.realize_joint(ca["text"], cb["text"], seed)
        cov = coverage(C, [a, b])
        # Recovery R — reads ONLY C; pool = 2 parents + 6 distractors
        pool = distractor_pool(a, b, seed)
        rec = recover_parents(C, pool, scramble=False, seed=seed)
        rec_scr = recover_parents(C, pool, scramble=True, seed=seed)
        both = {a, b}
        results.append({
            "cov": cov, "max_single": max_single,
            "recovered": len(both & rec),           # 0..2
            "recovered_scrambled": len(both & rec_scr),
            "distractor_frac": (2 - len(both & rec)) / 2.0,   # frac of top-2 that are wrong
        })
    return results


def score(results):
    cov = sum(1 for r in results if r["cov"] >= 2 and r["cov"] > r["max_single"])
    rec = sum(1 for r in results if r["recovered"] >= 2)
    scr = sum(1 for r in results if r["recovered_scrambled"] >= 2)
    leak_rate = sum(r["distractor_frac"] for r in results) / len(results)
    passed = (cov >= COV_BAR and rec >= REC_BAR
              and leak_rate <= LEAK_BAR and (rec - scr) >= SCRAMBLE_DROP)
    return {"coverage": cov, "recovery": rec, "scramble_recovery": scr,
            "leak_rate": round(leak_rate, 3), "scramble_drop": rec - scr,
            "PASS": passed}


def _fmt(tag, s):
    return (f"  {tag:14s} coverage={s['coverage']:2d}/{M} (bar>={COV_BAR})  "
            f"recovery={s['recovery']:2d}/{M} (bar>={REC_BAR})  "
            f"leak_rate={s['leak_rate']} (bar<={LEAK_BAR})  "
            f"scramble_rec={s['scramble_recovery']:2d}/{M}  "
            f"drop={s['scramble_drop']:2d} (bar>={SCRAMBLE_DROP})  "
            f"=> {'PASS' if s['PASS'] else 'FAIL'}")


if __name__ == "__main__":
    print("═" * 78)
    print("system-G1 relocation harness — numpy DIRECTIONAL smoke (TOY mouth)")
    print(f"  M={M} distant pairs · seeds={SEEDS} · N_pool={N_DISTRACT} · "
          f"bars: cov>={COV_BAR} rec>={REC_BAR} leak<={LEAK_BAR} drop>={SCRAMBLE_DROP}")
    print("═" * 78)
    sc = score(run_arm("compositional"))
    sf = score(run_arm("mouthfloor"))
    print(_fmt("COMPOSITIONAL", sc))
    print(_fmt("MOUTHFLOOR", sf))
    print("─" * 78)
    # harness is VALID iff it credits composition AND rejects the mouth-only floor
    harness_valid = sc["PASS"] and not sf["PASS"]
    print(f"  HARNESS-VALID (credits composition ∧ rejects mouth-floor): {harness_valid}")
    print("  VERDICT: DIRECTIONAL (numpy toy) — GREEN needs rung(2)-(4) engine-native")
    print("           (core/kosmos_io.hexa kosmos_merge + anima evaluate --system-g1,")
    print("            real 303M mouth on pool GPU; mini=OOM).  See FREEZE.txt / card.")
    print("═" * 78)
