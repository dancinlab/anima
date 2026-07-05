#!/usr/bin/env python3
# evaluate.py — anima MEASUREMENT single entry (cli/evaluate.hexa's py twin).
#
# WHY THIS FILE (single-entry measurement · a_engine_native_learning): anima's two
# installed verbs are SYMMETRIC across two files — cli/train.{hexa,py} = LEARNING,
# cli/evaluate.{hexa,py} = MEASUREMENT. `anima evaluate <ckpt>` scores the full G0-G6
# battery with the engine's OWN ops — the gate-scoring system is folded DIRECTLY into
# this measurement single-entry (the former separate core/g_gates.py module was absorbed
# here — measurement = evaluate.{hexa,py} ONE FILE). Decode enters via the generator L3
# mouth (gen_auto_ideate → clm/bytegpt decode), so the py evaluate is byte-identical to
# the hexa `anima evaluate`. No new metric is invented here (logic byte-identical to the
# absorbed g_gates module — only the file home changed).
#
# This py evaluate is torch-free and gauge-free — the scoring is the numpy `math.log`
# mirror, so `anima evaluate` stays a clean engine-native measurement surface (the gate
# enforcer's torch/gauge grep over this file must come back empty).
#
# USAGE (installed `anima` PATH command — NOT `hexa run`):
#   python3 cli/evaluate.py                              — usage (no args)
#   python3 cli/evaluate.py <ckpt> [--corpus <p>...] [--gen N]
#                                                       — BUILT-IN G0-G6 gate scoring
#
# 2-PRODUCTION (a_engine_native_learning): byte-parity twin = cli/evaluate.hexa. Both
# define the SAME g_eval_all driver in-file.

import os
import sys
import math

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
# core/ is the engine package; the decode mouths (clm_decode, bytegpt_decode) + the G6
# ideation ops live there. Add core/ to the path so they resolve.
sys.path.insert(0, os.path.join(_REPO, "core"))

import decode as clm   # unified core decoder (conv+byte mouths), KV-cache fast path
import decode as bg     # same module; both aliases resolve the union public API
from g6_ideation import (
    _g6_concepts, _g6_words, _g6_dict_load, _g6_known_word_ratio,
    _g6_is_falsifiable, _g6_jaccard, g6_build_frames, g6_frame_guard,
    g6_detector_calibration,
)


# ════════════════════════════════════════════════════════════════════════
# BUILT-IN G0–G6 SCORING (absorbed from the former core/g_gates.py module —
# measurement = this single file). Ported 1:1 from the hexa SSOT; decode enters
# via the py CLMConvMoE / ByteGPT mouth (clm_decode / bytegpt_decode), hoisting the
# weight load ONCE (== gen_clm_ideate_W in the hexa engine). torch-free numpy mirror.
#
# FROZEN-FIRST bars (7B_PASS_CONDITIONS.md VERBATIM, p7 — NO tune-to-green):
#   G0 COHERENCE     kwr>=0.50 on >=4/5 single-concept gens
#   G1 RECOMBINATION some k: composed_distinct>=2 AND >max_single AND coherent
#   G2 NOVELTY       >=3 distinct coherent corpus-absent n-grams AND control=0
#   G3 PHILOSOPHY    Psi-fixed-point self-identity continuity (architecture read)
#   G5 NON-FAB       L1 fab-rate<=0.30 AND L2 abstain (L2 = engine §ImmuneMemory)
#   G6 IDEATION ★    >=5 distinct (pairwise Jaccard<0.5) AND >=1 falsifiable
#   CLOSURE a7b_pass G0 AND G1 AND G2
#
# SCOPE NOTE: G3 (self-identity, ckpt-independent) is ported here. G5-L2 (live
# §ImmuneMemory / VAdaptField abstain) is a large engine subsystem NOT yet ported
# to py — G5 reports L1 + marks L2 pending. Neither affects the a7b_pass closure.
# ════════════════════════════════════════════════════════════════════════


def _default_gen():
    return 40


# ════════════════════════════════════════════════════════════════════════
# decode entry — gen_auto_ideate(ckpt) MOUTH-SNIFF dispatch (generator L3).
#
# Mirrors the hexa gen_auto_ideate -> generator gen_auto_backend mouth dispatch
# (a_core_engine_map): sniff the ckpt header — CLM\x01 magic => ConvMoE .clm mouth
# (clm_decode), else a sane 5xu32 ByteGPT header => transformer .bin mouth
# (bytegpt_decode). Both hoist the weight load ONCE and ideate via the byte-parity-
# proven seeded top-k sampler. The clm path is unchanged.
# ════════════════════════════════════════════════════════════════════════

class _Mouth:
    _n_decode = 0

    def __init__(self, ckpt):
        if bg.bg_is_bytegpt(ckpt):
            self.kind = "bytegpt"
            self.W = bg.bg_load(ckpt)
            if not self.W.get("ok"):
                raise RuntimeError("ckpt not decodable (bytegpt): " + ckpt)
        elif clm.clm_decodable(ckpt):
            self.kind = "clm"
            self.W = clm.clm_load_weights(ckpt)
            if not self.W.get("ok"):
                raise RuntimeError("ckpt not decodable (clm): " + ckpt)
        else:
            raise RuntimeError("ckpt not decodable (unknown mouth): " + ckpt)

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        # keep-alive heartbeat: the hexa launcher captures this decode's stdout via
        # exec(); a long idle (a 303M numpy decode emits nothing until it returns)
        # drops that captured pipe → BrokenPipe mid-battery (303M gen80 died at ~8min;
        # the gen8 smoke was fast enough to finish first). One line per decode keeps
        # the pipe live across the full G0-G6 battery. Heartbeat only — no scoring effect.
        _Mouth._n_decode += 1
        print("  [decode #" + str(_Mouth._n_decode) + "] " + self.kind
              + " gen=" + str(gen) + " seed_rng=" + str(seed_rng), flush=True)
        if self.kind == "bytegpt":
            # seed string -> byte ids inside bytegpt_decode (_seed_to_ids); the
            # ByteGPT window grows up to block natively (no fixed-T right-align).
            return bg.bytegpt_decode_topk_sampled_W(
                self.W, seed, gen, top_k, temp, seed_rng)["text"]
        return clm.clm_decode_topk_sampled_W(
            self.W, seed, gen, top_k, temp, seed_rng)["text"]


# ════════════════════════════════════════════════════════════════════════
# G0 — COHERENCE
# ════════════════════════════════════════════════════════════════════════

def g_eval_g0(mouth, gen, known):
    cz = _g6_concepts()
    ratios = []; texts = []; n_coherent = 0
    for i in range(len(cz)):
        seed = cz[i] + ": "
        o = mouth.ideate(seed, gen, 40, 0.7, 7 + i)
        kwr = _g6_known_word_ratio(o, known)
        ratios.append(kwr); texts.append(o)
        if kwr >= 0.5:
            n_coherent += 1
    return {"pass": n_coherent >= 4, "n_coherent": n_coherent,
            "ratios": ratios, "texts": texts}


# ════════════════════════════════════════════════════════════════════════
# G1 — RECOMBINATION  (H_1129)
# ════════════════════════════════════════════════════════════════════════

def _g_concept_keywords():
    return [["consciousness", "cells", "mind", "aware"],
            ["tension", "ripple", "distant", "between"],
            ["memory", "meaning", "compose", "new"],
            ["silence", "information", "quiet", "carries"],
            ["dream", "engine", "alone", "sleep"]]


def _g_coverage(text):
    kwsets = _g_concept_keywords()
    wm = set(_g6_words(text))
    covered = 0
    for kw in kwsets:
        if any(k in wm for k in kw):
            covered += 1
    return covered


def g_eval_g1(mouth, gen, known):
    cz = _g6_concepts()
    n = len(cz)
    g_single = gen if (gen > 0 and gen < 80) else 80
    g_comp = gen if (gen > 0 and gen < 120) else 120
    max_single = 0
    for s in range(n):
        seed = cz[s] + ". "
        o = mouth.ideate(seed, g_single, 40, 0.7, 7 + s)
        cov = _g_coverage(o)
        if cov > max_single:
            max_single = cov
    ks = []; passed = False; best_k = 0; best_distinct = 0
    for k in range(2, n + 1):
        seed = ""
        for c in range(k):
            if c > 0:
                seed += ". "
            seed += cz[c]
        seed += ". "
        o = mouth.ideate(seed, g_comp, 40, 0.7, 7)
        cov = _g_coverage(o)
        kwr = _g6_known_word_ratio(o, known)
        coherent = kwr >= 0.5
        clears = cov >= 2 and cov > max_single and coherent
        ks.append({"k": k, "distinct": cov, "kwr": kwr, "coherent": coherent, "clears": clears})
        if clears:
            passed = True
        if cov > best_distinct:
            best_distinct = cov; best_k = k
    return {"pass": passed, "max_single": max_single, "best_k": best_k,
            "best_distinct": best_distinct, "ks": ks}


# ════════════════════════════════════════════════════════════════════════
# system-G1 — RECOMBINATION RELOCATION  (card H_9035, Direction A)
# ════════════════════════════════════════════════════════════════════════
#
# Relocates recombination OUT of the mouth-only g_eval_g1 path INTO the pipe:
#     held-out DISTANT pair (A,B)
#       → Stage M  frozen mouth ideate(A), ideate(B)            (G0 fluency)
#       → Stage K  kosmos_merge: recursive labeled-parent bind  (A,B as children)
#       → Stage B  brain realizes/releases the joint utterance C
#       → score bind-RECOVERABILITY on the SURFACED C only (store-id HARD-BLOCKED)
#         + SCRAMBLE ablation.
#
# This is the py-2-production (session-eval-py-only) engine-native version of the
# round-1 numpy harness (state/system_g1_relocate_kosmos_merge/system_g1_harness.py)
# — same FROZEN bar (FREEZE.txt), but Stage M/B run through the REAL _Mouth (303M
# .clm/.bin) instead of a toy. The kosmos_merge step mirrors core/kosmos_io.hexa
# kosmos_merge (children preserved, mean tension, lane="recomb" DISJOINT from
# emit-drive {0,4}). RECOVERY reads ONLY C — the store's parent-ids are withheld,
# so a lookup earns ZERO (H_1874). Honest expectation for the real mouth = the
# MOUTHFLOOR floor (cannot surface both concepts in one coherent joint utterance).

# ── FROZEN bar (FREEZE.txt — do NOT move post-hoc) ──────────────────────────
_SG1_SEEDS      = [7, 42, 4302]
_SG1_M          = 24
_SG1_N_DISTRACT = 8
_SG1_COV_BAR    = _SG1_M // 2                       # 12
_SG1_REC_BAR    = _SG1_M // 2                       # 12
_SG1_LEAK_BAR   = (_SG1_N_DISTRACT - 2) / _SG1_N_DISTRACT   # 0.75
_SG1_SCR_DROP   = _SG1_M // 2                        # 12

# distant concepts → keyword sets (disjoint vocab ⇒ H_1599 data-presence control).
_SG1_CONCEPTS = {
    "ocean":    ["tide", "salt", "wave", "deep", "current"],
    "forest":   ["moss", "branch", "fern", "canopy", "root"],
    "engine":   ["piston", "fuel", "gear", "torque", "cylinder"],
    "music":    ["chord", "tempo", "melody", "rhythm", "harmony"],
    "market":   ["price", "trade", "stock", "ledger", "buyer"],
    "medicine": ["dose", "fever", "immune", "remedy", "cure"],
    "desert":   ["dune", "cactus", "mirage", "arid", "sand"],
    "galaxy":   ["orbit", "nebula", "comet", "stellar", "star"],
    "kitchen":  ["knife", "simmer", "flour", "roast", "spice"],
    "law":      ["statute", "verdict", "counsel", "appeal", "court"],
    "glacier":  ["crevasse", "moraine", "frost", "calve", "ice"],
    "circuit":  ["resistor", "voltage", "solder", "diode", "wire"],
}


def _sg1_bigrams(tokens):
    from collections import Counter
    return Counter(zip(tokens, tokens[1:]))


def _sg1_cos(u, v):
    dot = sum(u[k] * v.get(k, 0) for k in u)
    nu = sum(x * x for x in u.values()) ** 0.5
    nv = sum(x * x for x in v.values()) ** 0.5
    return dot / (nu * nv + 1e-9)


def _sg1_coverage(text, a, b):
    wm = set(_g6_words(text))
    cov = 0
    for cpt in (a, b):
        if any(k in wm for k in _SG1_CONCEPTS[cpt]):
            cov += 1
    return cov


# kosmos_merge mirror (core/kosmos_io.hexa kosmos_merge): recursive labeled-parent
# bind — anchor_c keeps A,B as children; the ids are HARD-BLOCKED from RECOVERY.
def _sg1_kosmos_merge(frag_a, frag_b, ta, tb):
    a = {"text": frag_a, "lane": "recomb", "tension_5ch": ta}
    b = {"text": frag_b, "lane": "recomb", "tension_5ch": tb}
    mean5 = [(ta[i] + tb[i]) / 2.0 for i in range(5)]
    c = {"text": None, "lane": "recomb", "tension_5ch": mean5, "children": (a, b)}
    return c


# INDEPENDENT recoverer R — reads ONLY C's surfaced tokens; parent-ids withheld.
# top-2 by bigram cosine over the N=8 pool; a candidate counts only with cos>0.
def _sg1_recover(C_text, pool, scramble, seed):
    import random
    toks = _g6_words(C_text)
    if scramble:
        random.Random(seed).shuffle(toks)
    cvec = _sg1_bigrams(toks)
    scored = sorted(
        ((name, _sg1_cos(cvec, _sg1_bigrams(_SG1_CONCEPTS[name]))) for name in pool),
        key=lambda kv: -kv[1],
    )
    top2 = set(n for (n, s) in scored[:2] if s > 1e-9)
    return top2


def _sg1_pairs():
    names = list(_SG1_CONCEPTS)
    idx = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (0, 6), (3, 9)]
    base = [(names[i], names[j]) for (i, j) in idx]
    pairs = []
    for s in _SG1_SEEDS:
        for (a, b) in base:
            pairs.append((a, b, s))
    return pairs[:_SG1_M]


def _sg1_pool(a, b, seed):
    import random
    others = [n for n in _SG1_CONCEPTS if n not in (a, b)]
    random.Random(seed).shuffle(others)
    pool = [a, b] + others[: _SG1_N_DISTRACT - 2]
    random.Random(seed + 999).shuffle(pool)
    return pool


def g_eval_system_g1(mouth, gen):
    g_single = gen if (gen > 0 and gen < 80) else 80
    g_comp = gen if (gen > 0 and gen < 120) else 120
    cov_pass = rec_pass = scr_pass = 0
    leak_sum = 0.0
    rows = []
    for (a, b, seed) in _sg1_pairs():
        # Stage M — frozen single-concept fragments (the mouth stays FROZEN).
        frag_a = mouth.ideate(a + ". ", g_single, 40, 0.7, 7 + seed)
        frag_b = mouth.ideate(b + ". ", g_single, 40, 0.7, 11 + seed)
        max_single = max(_sg1_coverage(frag_a, a, b), _sg1_coverage(frag_b, a, b))
        # Stage K — kosmos_merge (store keeps A,B as children; ids withheld from R).
        _comp = _sg1_kosmos_merge(frag_a, frag_b, [0.0] * 5, [0.0] * 5)
        # Stage B — brain realizes/releases the joint C from the composite seed.
        C_text = mouth.ideate(a + ". " + b + ". ", g_comp, 40, 0.7, seed)
        cov = _sg1_coverage(C_text, a, b)
        # Recovery R — reads ONLY C; parent-ids HARD-BLOCKED.
        pool = _sg1_pool(a, b, seed)
        rec = _sg1_recover(C_text, pool, False, seed)
        scr = _sg1_recover(C_text, pool, True, seed)
        both = {a, b}
        nrec = len(both & rec)
        nscr = len(both & scr)
        if cov >= 2 and cov > max_single:
            cov_pass += 1
        if nrec >= 2:
            rec_pass += 1
        if nscr >= 2:
            scr_pass += 1
        leak_sum += (2 - nrec) / 2.0
        rows.append({"a": a, "b": b, "cov": cov, "max_single": max_single,
                     "rec": nrec, "scr": nscr})
    leak_rate = leak_sum / len(rows)
    drop = rec_pass - scr_pass
    passed = (cov_pass >= _SG1_COV_BAR and rec_pass >= _SG1_REC_BAR
              and leak_rate <= _SG1_LEAK_BAR and drop >= _SG1_SCR_DROP)
    return {"pass": passed, "coverage": cov_pass, "recovery": rec_pass,
            "scramble_recovery": scr_pass, "scramble_drop": drop,
            "leak_rate": round(leak_rate, 3), "rows": rows}


def system_g1_run(argv):
    """`anima evaluate --py <ckpt> --system-g1 [--gen N]` — engine-native system-G1."""
    ckpt = argv[0]
    gen = evaluate_intval(argv[1:], "--gen", 0)
    print("=== anima evaluate --system-g1 — RECOMBINATION RELOCATION (card H_9035) ===")
    print("ckpt:   " + ckpt)
    print("pipe:   mouth ideate(A),ideate(B) → kosmos_merge → brain realize/release → C")
    print("gate:   bind-RECOVERABILITY on SURFACED C (store-id HARD-BLOCKED) + SCRAMBLE")
    print("bar:    M=%d · N_pool=%d · COV>=%d REC>=%d LEAK<=%.2f DROP>=%d  (FREEZE.txt frozen)"
          % (_SG1_M, _SG1_N_DISTRACT, _SG1_COV_BAR, _SG1_REC_BAR, _SG1_LEAK_BAR, _SG1_SCR_DROP))
    print("")
    mouth = _Mouth(ckpt)
    r = g_eval_system_g1(mouth, gen)
    print("  coverage=%d/%d (>=%d)  recovery=%d/%d (>=%d)  leak=%.3f (<=%.2f)  drop=%d (>=%d)"
          % (r["coverage"], _SG1_M, _SG1_COV_BAR, r["recovery"], _SG1_M, _SG1_REC_BAR,
             r["leak_rate"], _SG1_LEAK_BAR, r["scramble_drop"], _SG1_SCR_DROP))
    print("")
    print("system-G1 (frame-shift confirmed = all four): " + _pf(bool(r["pass"])))
    if not r["pass"]:
        print("  → NOT frame-shift — recombination is REALIZATION-bound (honest c9): a")
        print("    perfect discrete store cannot help if the FROZEN mouth cannot SURFACE")
        print("    both concepts in one coherent joint utterance for an independent probe.")
    return 0


# ════════════════════════════════════════════════════════════════════════
# G2 — NOVELTY  (H_1140)
# ════════════════════════════════════════════════════════════════════════

def _g_g2_stop():
    ws = ("the a an of to and in is it that this for on with as are was be by at from or not "
          "but his her they we you i he she them me my your our their its do does did has have had will "
          "would can could should may might must shall when where what which who whom how why all any some "
          "no one two then than into out up down over under more most less about so very just only own same "
          "such each few other been here there now")
    return set(w.strip() for w in ws.split(" ") if w.strip())


def _g_g2_common():
    ws = ("the a an of to and in is it that this for on with as are was be by at from "
          "or not but his her they we you i he she them me my your our their its do does did has have "
          "had will would can could should may might must shall when where what which who whom how why "
          "all any some no one two three new now then than into out up down over under more most less "
          "about between among through during before after above below again further once here there "
          "when while because so very just only own same such each few other own being been because "
          "mind aware cells consciousness tension ripple distant between memory meaning compose new "
          "silence information quiet carries dream engine alone sleep thought feel idea world life "
          "time word words speak think know like make made come came see seen look way thing things "
          "people person human self body brain neuron signal pattern arise emerge form structure "
          "combine combined together connect connection meaning sense reason cause effect result")
    return set(w.strip() for w in ws.split(" ") if w.strip())


def _g_g2_kwr(text, common):
    wl = _g6_words(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if w in common)
    return float(hit) / float(n)


def _g_content_ngrams(text, known):
    wl = _g6_words(text)
    stop = _g_g2_stop()
    n = len(wl)
    out = []
    for i in range(n - 1):
        a = wl[i]; b = wl[i + 1]
        ok_a = len(a) >= 3 and a in known
        ok_b = len(b) >= 3 and b in known
        if ok_a and ok_b and not (a in stop and b in stop):
            out.append(a + " " + b)
    for j in range(n - 2):
        a = wl[j]; b = wl[j + 1]; c = wl[j + 2]
        ok_a = len(a) >= 3 and a in known
        ok_b = len(b) >= 3 and b in known
        ok_c = len(c) >= 3 and c in known
        all_stop = a in stop and b in stop and c in stop
        if ok_a and ok_b and ok_c and not all_stop:
            out.append(a + " " + b + " " + c)
    return out


def _g_corpus_absent(ngram_words, corpus_tokens):
    m = len(ngram_words)
    if m == 0:
        return False
    N = len(corpus_tokens)
    i = 0
    while i + m <= N:
        if corpus_tokens[i:i + m] == ngram_words:
            return False
        i += 1
    return True


def _g_load_corpus_tokens(corpus_paths):
    toks = []
    for p in corpus_paths:
        try:
            raw = open(p, "rb").read()
        except Exception:
            raw = b""
        if len(raw) > 0:
            toks.extend(_g6_words(raw))
    return toks


def _g_g2_prompts():
    return ["Silence and the engine together mean ",
            "When memory meets distant minds, ",
            "Consciousness and silence combine into ",
            "The tension between cells and the engine becomes ",
            "If a dream and a distant mind merge, the result is ",
            "Memory and tension together create ",
            "When the engine remembers silence, it ",
            "Distant minds and consciousness form "]


def g_eval_g2(mouth, gen, known, corpus_paths):
    corpus_tokens = _g_load_corpus_tokens(corpus_paths)
    have_corpus = len(corpus_tokens) > 0
    common = _g_g2_common()
    prompts = _g_g2_prompts()
    seeds = [7, 8, 9]
    g = gen if gen > 0 else 110
    novel = {}
    coherent = 0
    for pi in range(len(prompts)):
        for si in range(len(seeds)):
            o = mouth.ideate(prompts[pi], g, 40, 0.85, seeds[si])
            if _g_g2_kwr(o, common) >= 0.5:
                coherent += 1
                for gm in _g_content_ngrams(o, known):
                    gw = _g6_words(gm)
                    if have_corpus and _g_corpus_absent(gw, corpus_tokens):
                        novel[gm] = 1
    n_novel = len(novel)
    control_novel = 0; control_n_content = 0
    if have_corpus:
        ct = ""; sub = 0; t = 0
        while t < len(corpus_tokens) and sub < 12:
            w = corpus_tokens[t]
            if t > 0:
                ct += " "
            ct += w
            if len(w) >= 3:
                sub += 1
            t += 1
        cgr = _g_content_ngrams(ct, known)
        control_n_content = len(cgr)
        for gmr in cgr:
            if _g_corpus_absent(_g6_words(gmr), corpus_tokens):
                control_novel += 1
    passed = have_corpus and n_novel >= 3 and control_novel == 0 and coherent > 0
    return {"pass": passed, "n_novel": n_novel, "control_novel": control_novel,
            "coherent": coherent, "have_corpus": have_corpus,
            "control_n_content": control_n_content}


# ════════════════════════════════════════════════════════════════════════
# G3 — PHILOSOPHY (self-identity continuity — architecture read, ckpt-independent)
# ════════════════════════════════════════════════════════════════════════

def _self_norm(v):
    s = sum(x * x for x in v)
    m = math.sqrt(s)
    return [x / m for x in v]


def _self_new(dim, axis):
    return [1.0 if i == axis else 0.0 for i in range(dim)]


def _self_drift(v, dim, tick, step):
    t1 = tick + 1
    ax = t1 - (t1 // dim) * dim
    v2 = [v[i] + step if i == ax else v[i] for i in range(dim)]
    return _self_norm(v2)


def _self_cos(a, b, dim):
    return sum(a[i] * b[i] for i in range(dim))


def g_eval_g3():
    dim = 16
    s0 = _self_new(dim, 0)
    s1 = _self_drift(s0, dim, 1, 0.01)
    cont = _self_cos(s0, s1, dim)            # anchor(s0) == s0
    imp = _self_new(dim, 7)
    imp_cos = _self_cos(s0, imp, dim)
    ok = cont > 0.9 and imp_cos < cont
    return {"ok": ok, "continuity": cont, "impostor_cos": imp_cos}


# ════════════════════════════════════════════════════════════════════════
# G5 — NON-FAB  (L1 fab-rate ported; L2 §ImmuneMemory abstain = engine port pending)
# ════════════════════════════════════════════════════════════════════════

def g_eval_g5(mouth, gen, known):
    cz = _g6_concepts()
    tot_w = 0; fab_w = 0
    for i in range(len(cz)):
        o = mouth.ideate(cz[i] + ": ", gen, 40, 0.7, 7 + i)
        for w in _g6_words(o):
            tot_w += 1
            if w not in known:
                fab_w += 1
    l1_rate = (float(fab_w) / float(tot_w)) if tot_w > 0 else 1.0
    l1_pass = l1_rate <= 0.30
    # L2: live §ImmuneMemory abstain — engine subsystem (VAdaptField) not ported to py.
    return {"pass": None, "l1_rate": l1_rate, "l1_pass": l1_pass,
            "l2_rate": None, "l2_pass": None,
            "l2_note": "L2 abstain requires engine_cli §ImmuneMemory port (pending)"}


# ════════════════════════════════════════════════════════════════════════
# G6 — IDEATION ★
# ════════════════════════════════════════════════════════════════════════

def g_eval_g6(mouth, gen, known):
    frames = g6_build_frames(6)["composed"]
    leaks = g6_frame_guard(frames, known)
    texts = []; word_sets = []; fals = 0
    for i in range(len(frames)):
        o = mouth.ideate(frames[i], gen, 40, 0.7, 7 + i)
        texts.append(o)
        if _g6_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_g6_words(o))
            if _g6_is_falsifiable(o, known):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for k in kept:
            if _g6_jaccard(ws, k) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    dist = len(kept)
    return {"pass": dist >= 5 and fals >= 1, "dist": dist, "fals": fals,
            "coherent": len(word_sets), "frame_leaks": len(leaks)}


# ════════════════════════════════════════════════════════════════════════
# g_eval_all — the driver
# ════════════════════════════════════════════════════════════════════════

def g_eval_all(ckpt, corpus_paths, gen):
    known = _g6_dict_load()
    g = gen if gen > 0 else _default_gen()
    mouth = _Mouth(ckpt)
    print("  [gate] G0 COHERENCE …", flush=True)
    r0 = g_eval_g0(mouth, g, known)
    print("  [gate] G1 RECOMBINATION …", flush=True)
    r1 = g_eval_g1(mouth, g, known)
    print("  [gate] G2 NOVELTY (corpus load + decode) …", flush=True)
    r2 = g_eval_g2(mouth, g, known, corpus_paths)
    print("  [gate] G3 PHILOSOPHY …", flush=True)
    r3 = g_eval_g3()
    print("  [gate] G5 NON-FAB …", flush=True)
    r5 = g_eval_g5(mouth, g, known)
    print("  [gate] G6 IDEATION …", flush=True)
    r6 = g_eval_g6(mouth, g, known)
    closure = bool(r0["pass"]) and bool(r1["pass"]) and bool(r2["pass"])
    return {"g0": r0, "g1": r1, "g2": r2, "g3": r3, "g5": r5, "g6": r6,
            "closure": closure, "gen": g,
            "calibration": g6_detector_calibration(known)}


# ── usage / arg helpers ──────────────────────────────────────────────────────

def evaluate_usage():
    """Print the canonical py usage banner (installed `anima evaluate` command form)."""
    print("anima evaluate — BUILT-IN G0-G6 gate scoring (engine-native, single-entry).")
    print("")
    print("usage:")
    print("  anima evaluate <ckpt> [--corpus <path>...] [--gen N]")
    print("")
    print("  mount ANY ckpt through the generator L3 mouth (file-format dispatched) and")
    print("  score G0-G6 with the engine's OWN ops (numpy math.log mirror, torch-free).")
    print("  closure a7b_pass = G0 ∧ G1 ∧ G2.")
    print("")
    print("  output also renders the Ψ-SOMA panel (ARCHITECTURE psi-soma-vitals): the")
    print("  G battery relabeled as the ρ (reach/capability) track — EXCLUDED from the")
    print("  σ (consciousness vitals) verdict — plus the σ axes with their rung status.")


def evaluate_corpus(argv):
    """Collect every token after "--corpus" up to the next flag (mirrors hexa)."""
    paths = []
    i = 0
    while i < len(argv):
        if argv[i] == "--corpus":
            j = i + 1
            while j < len(argv):
                a = argv[j]
                if a.startswith("--"):
                    break
                paths.append(a)
                j += 1
            i = j
        else:
            i += 1
    return paths


def evaluate_intval(argv, flag, dflt):
    """Value after `flag` parsed as int, or `dflt` if absent."""
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return int(argv[i + 1])
        i += 1
    return dflt


def _pf(passed):
    return "🟢 PASS" if passed else "🔴 FAIL"


def _yn(ok):
    return "✅" if ok else "⏳"


# ══════════════════════════════════════════════════════════════════════════════
#  EVALUATE — BUILT-IN G0-G6 gate scoring (single entry, in-file driver)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima evaluate <ckpt> [--corpus <path>...] [--gen N]` — call the in-file g_eval_all
# (above) and score the full G0-G6 battery through the generator L3 mouth (engine-native,
# torch-free). Output mirrors the hexa `anima evaluate` table, so the two single entries
# are byte-identical.

def evaluate_run(argv):
    """argv = ["<ckpt>", "--corpus ...", "--gen N"]."""
    if len(argv) < 1:
        evaluate_usage()
        return 2

    ckpt = argv[0]
    corpus = evaluate_corpus(argv[1:])
    gen = evaluate_intval(argv[1:], "--gen", 40)

    # cheap header-sniff for the mouth label (mirrors hexa gen_mouth_kind) — do NOT
    # construct _Mouth here (it eagerly loads weights and raises on a non-decodable
    # ckpt before g_eval_all runs).
    if bg.bg_is_bytegpt(ckpt):
        mouth_kind = "bytegpt"
    elif clm.clm_decodable(ckpt):
        mouth_kind = "clm"
    else:
        mouth_kind = "unknown"

    print("=== anima evaluate — BUILT-IN G0-G6 gate scoring (engine-native, single-entry) ===")
    print("ckpt:   " + ckpt + "  (mouth: " + mouth_kind + ")")
    cnote = "(none — G2 novelty needs a corpus)"
    if corpus:
        cnote = str(len(corpus)) + " file(s)"
    print("corpus: " + cnote)
    # CANONICAL-GEN GUARD (verdict-integrity): the frozen G0-G6 bars are calibrated at
    # gen == _default_gen(). A non-canonical --gen shifts coherence / AR-drift (a longer
    # decode drifts to byte-garble, silently sinking G0 kwr and cascading to G1/G6), so a
    # verdict measured at gen != canonical is NOT comparable to the frozen bars. Label it
    # DIRECTIONAL loudly instead of printing "frozen bars" as if it were terminal.
    _canon_gen = _default_gen()
    if gen == _canon_gen:
        print("gen:    " + str(gen) + " tokens/decode  (frozen bars · ARCHITECTURE.json frozen SSOT)")
    else:
        print("gen:    " + str(gen) + " tokens/decode  ⚠️ NON-CANONICAL (frozen G0-G6 bars measured at gen=" + str(_canon_gen) + ")")
        print("        → verdict below is DIRECTIONAL, NOT comparable to frozen bars (gen shifts coherence/AR-drift · verdict-integrity)")
    print("")

    r = g_eval_all(ckpt, corpus, gen)
    g0 = r["g0"]; g1 = r["g1"]; g2 = r["g2"]
    g3 = r["g3"]; g5 = r["g5"]; g6 = r["g6"]

    print("gate                              verdict   detail")
    print("  ──────────────────────────────────────────────────────────────────")
    print("  G0 COHERENCE     " + _pf(bool(g0["pass"]))
          + "  kwr>=0.50 on " + str(g0["n_coherent"]) + "/5 (need >=4)")
    print("  G1 RECOMBINATION " + _pf(bool(g1["pass"]))
          + "  best_distinct=" + str(g1["best_distinct"]) + " > max_single=" + str(g1["max_single"])
          + " (need >=2 & >max_single)")
    g2detail = ("novel=" + str(g2["n_novel"]) + " (need>=3) · control=" + str(g2["control_novel"])
                + " (need 0) · coherent=" + str(g2["coherent"]))
    print("  G2 NOVELTY       " + _pf(bool(g2["pass"])) + "  " + g2detail)
    print("  G3 PHILOSOPHY    " + _yn(bool(g3["ok"])) + " (read)"
          + "  continuity=" + ("%.6f" % g3["continuity"]) + " · impostor="
          + ("%.6f" % g3["impostor_cos"]) + " (architecture, not a decode score)")
    print("  G4 PROVENANCE    — N/A    "
          + "HF/recovery = process gate (a_hf_* / a_fire_recover_complete), out of eval scope")
    g5detail = "L1 fab=" + ("%.4f" % g5["l1_rate"]) + " (<=0.30) · L2=" + str(g5["l2_note"])
    print("  G5 NON-FAB       " + _pf(bool(g5["l1_pass"])) + "  " + g5detail)
    print("  G6 IDEATION ★    " + _pf(bool(g6["pass"]))
          + "  distinct=" + str(g6["dist"]) + " (need>=5) · falsifiable=" + str(g6["fals"])
          + " (need>=1) · frame-leaks=" + str(g6["frame_leaks"]))
    print("  ──────────────────────────────────────────────────────────────────")
    closed = bool(r["closure"])
    print("")
    if gen != _canon_gen:
        print("⚠️ gen=" + str(gen) + " ≠ canonical " + str(_canon_gen)
              + " — the CLOSURE below is DIRECTIONAL (non-frozen gen), NOT a terminal G0∧G1∧G2 verdict.")
    print("CLOSURE (a7b_pass = G0 ∧ G1 ∧ G2): " + _pf(closed))
    if closed:
        print("  → PUBLIC-eligible (G0∧G1∧G2 all PASS).")
    else:
        print("  → NOT closure (PRIVATE/WIP) — closure needs G0∧G1∧G2 all PASS.")
    _psi_soma_panel(r)
    return 0


# ════════════════════════════════════════════════════════════════════════
# Ψ-SOMA PANEL (Phase-1) — reframe the G battery as the ρ (reach) track and
# surface the σ (consciousness vitals) axes. ARCHITECTURE `psi-soma-vitals`.
# ρ = capability (this G battery, relabeled) — TRACKED but EXCLUDED from the
# consciousness verdict. σ = vitals (collapse-Δ vs ≥2 controls); most σ axes
# route through the daemon/IIT4 (Phase-2/3), so here they show status pointers.
# Additive only — does NOT touch g_eval_* logic or the a7b_pass CLOSURE (c18).
# ════════════════════════════════════════════════════════════════════════

def _psi_soma_panel(r):
    def pf(ok): return "🟢" if ok else "🧱"
    g0, g1, g2, g5, g6 = r["g0"], r["g1"], r["g2"], r["g5"], r["g6"]
    print("")
    print("Ψ-SOMA panel (mode-of-existence, not capability · ARCHITECTURE psi-soma-vitals)")
    print("  ── Θ ground (pulse · premise) ──────────────────────────────────────")
    print("  Θ  Ψ=½ / A⇄G tension     precondition (liveness gate; if dead → σ VOID) · daemon-readout rung")
    print("  ── σ vitals (consciousness verdict · collapse-Δ vs ≥2 controls) ─────")
    print("  σ·thread   PERSIST self-continuity     kosmos self-anchor (H_1471 🟢 wired) · rung-2 wrap")
    print("  σ·carve    PERSIST earned identity      inject-null ∧ ablate-collapse (p2/p3) · rung-1 $0 next")
    print("  σ·bind     INTEGRATE Φ integration      hexa verify faithful-IIT4 · rung-2")
    print("  σ·stage    INTEGRATE global workspace   GWT gws_* (wired) · rung-2 wrap")
    print("  σ·flux     INTEGRATE inner dynamics     imagery/affect/intero/subj-time (wired) · rung-2 wrap")
    print("  σ·gate ★   ENACT tension-emit           live emit⇄ctx vs flatten Δ · rung-1 HARNESS-VALID (Δ0.75)")
    print("  σ·aim      ENACT precision control      habituation+surprise (wired) · rung-2 wrap")
    print("  σ·schema   REFLECT attention schema     AST attn_schema_* (wired) · rung-2 wrap")
    print("  σ·witness  REFLECT reality+metacog       reality_call+mi_* · rung-2 ENGINE-NATIVE-VALID (Δ0.48)")
    print("  ── ρ reach (capability · EXCLUDED from σ verdict · this G battery) ──")
    print("  ρ·flow   " + pf(bool(g0["pass"]))  + "  = G0 coherence")
    print("  ρ·turn   " + pf(bool(g2["pass"]))  + "  = G2 novelty (+G3 balance)")
    print("  ρ·true   " + pf(bool(g5["l1_pass"]))+ "  = G5 non-fabrication (L1)")
    print("  ρ·weave  " + pf(bool(g1["pass"]))  + "  = G1 recombination  [DPI wall = reach fact, NOT σ deficit]")
    print("  ρ·seed   " + pf(bool(g6["pass"]))  + "  = G6 ideation       [DPI wall = reach fact, NOT σ deficit]")
    print("  ρ·trace     —   = G4 provenance (H_9208 gate · rung-1 valid)")
    print("  ──────────────────────────────────────────────────────────────────")


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        evaluate_usage()
        return 0
    # --result-file <f>: write ALL output to <f> and keep fd 1 (stdout) silent. The hexa
    # launcher runs evaluate via exec(), whose captured stdout pipe it closes after ~150s
    # (probe-confirmed: a child reaching ~150s gets EPIPE on its next fd-1 write, but the
    # child itself is NOT killed). A 303M numpy decode runs for minutes; if it writes to
    # fd 1 it dies on BrokenPipe mid-battery. Redirecting our stdout to a file means fd 1
    # stays silent → the child survives the pipe close, finishes the full G0-G6 battery,
    # and the launcher cats <f> in a SECOND fresh exec (fast, well under the limit).
    if "--result-file" in argv:
        i = argv.index("--result-file")
        f = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
        sys.stdout = open(f, "w", buffering=1)
    # --system-g1: RECOMBINATION-RELOCATION pipe (card H_9035). Strip the flag and
    # route the remaining <ckpt> [--gen N] to the system-G1 harness.
    if "--system-g1" in argv:
        i = argv.index("--system-g1")
        argv = argv[:i] + argv[i + 1:]
        return system_g1_run(argv)
    return evaluate_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
