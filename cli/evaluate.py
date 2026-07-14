#!/usr/bin/env python3
# evaluate.py — anima MEASUREMENT single entry (cli/evaluate.hexa's py twin).
#
# WHY THIS FILE (single-entry measurement · a_engine_native_learning): anima's two
# installed verbs are SYMMETRIC across two files — cli/train.{hexa,py} = LEARNING,
# cli/evaluate.{hexa,py} = MEASUREMENT. `anima evaluate <ckpt>` scores the full ρ-AXON
# reach battery (Ψ-SOMA reach layer · owner redesign of the old G-ladder · cli/rho_axon.py;
# the frozen bars this driver runs today = the former G0-G6) with the engine's OWN ops —
# the reach-scoring system is folded DIRECTLY into
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
#                                                       — ρ-AXON reach battery (former G0-G6)
#
# 2-PRODUCTION (a_engine_native_learning): byte-parity twin = cli/evaluate.hexa. Both
# define the SAME eval_reach_all driver in-file.

import os
import sys
import math
import json
import random

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
# core/ is the engine package; the decode mouths (clm_decode, bytegpt_decode) + the G6
# ideation ops live there. Add core/ to the path so they resolve.
sys.path.insert(0, os.path.join(_REPO, "core"))

import decode as clm   # unified core decoder (conv+byte mouths), KV-cache fast path
import decode as bg     # same module; both aliases resolve the union public API
from rho_fan import (
    _rho_fan_concepts, _rho_fan_words, _rho_fan_dict_load, _rho_fan_known_word_ratio,
    _rho_fan_is_falsifiable, _rho_fan_jaccard, rho_fan_build_frames, rho_fan_frame_guard,
    rho_fan_detector_calibration,
    # H_9212 ③ per-cell dispatch: 4 register cells + ko codepoint-aware tokenizer + kwr_ko gate
    _rho_fan_cells, _rho_fan_cell_lang, _rho_fan_words_uni, _rho_fan_ko_known_word_ratio,
    KWR_KO_GATE,
)

# H_9200 — process-global: render the ρ-AXON reach panel (cli/rho_axon.py) instead of the
# G0-G6 battery when `anima-py evaluate --rho-axon` is passed (set in main()).
_RHO_AXON = False


# ════════════════════════════════════════════════════════════════════════
# ρ-AXON REACH SCORING (absorbed from the former core/g_gates.py module —
# measurement = this single file). Ported 1:1 from the hexa SSOT; decode enters
# via the py CLMConvMoE / ByteGPT mouth (clm_decode / bytegpt_decode), hoisting the
# weight load ONCE (== gen_clm_ideate_W in the hexa engine). torch-free numpy mirror.
#
# ρ-AXON is the current-standard reach layer (cli/rho_axon.py · design SSOT
# state/rho_axon_measurement/) — an owner redesign OVER these frozen bars. The
# detector identifiers below (eval_rho_form…g6) are the load-bearing frozen substrate
# ρ-AXON reuses; the G→ρ mapping (axis names shown first-time here) is:
#   ρ·form   ← G0 COHERENCE      kwr>=0.50 on >=4/5 single-concept gens
#   ρ·weave  ← G1 RECOMBINATION  some k: composed_distinct>=2 AND >max_single AND coherent (the central WALL)
#   ρ·leap   ← G2 NOVELTY        >=3 distinct coherent corpus-absent n-grams AND control=0
#   ρ·self   ← G3 PHILOSOPHY     Psi-fixed-point self-identity continuity (architecture read)
#   ρ·tether ← G5 NON-FAB        L1 fab-rate<=0.30 AND L2 abstain (L2 = engine §ImmuneMemory)
#   ρ·fan    ← G6 IDEATION ★     >=5 distinct (pairwise Jaccard<0.5) AND >=1 falsifiable
#   ρ·store  ← (NEW · held-out association retrieval · PENDING, no old-G)
#   REACH-CLOSED a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2)
# FROZEN-FIRST bars (7B_PASS_CONDITIONS.md VERBATIM, p7 — NO tune-to-green).
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

def eval_rho_form(mouth, gen, known):
    cz = _rho_fan_concepts()
    ratios = []; texts = []; n_coherent = 0
    for i in range(len(cz)):
        seed = cz[i] + ": "
        o = mouth.ideate(seed, gen, 40, 0.7, 7 + i)
        kwr = _rho_fan_known_word_ratio(o, known)
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
    wm = set(_rho_fan_words(text))
    covered = 0
    for kw in kwsets:
        if any(k in wm for k in kw):
            covered += 1
    return covered


def eval_rho_weave(mouth, gen, known):
    cz = _rho_fan_concepts()
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
        kwr = _rho_fan_known_word_ratio(o, known)
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
# Relocates recombination OUT of the mouth-only eval_rho_weave path INTO the pipe:
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
    wm = set(_rho_fan_words(text))
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
    toks = _rho_fan_words(C_text)
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


def eval_system_rho_weave(mouth, gen):
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
    """`anima-py evaluate <ckpt> --system-g1 [--gen N]` — engine-native system-G1."""
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
    r = eval_system_rho_weave(mouth, gen)
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
    wl = _rho_fan_words(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if w in common)
    return float(hit) / float(n)


def _g_content_ngrams(text, known):
    wl = _rho_fan_words(text)
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
            toks.extend(_rho_fan_words(raw))
    return toks


# ── ko twins for the H_9212 ③ per-cell dispatch (uni tokenizer + ko known predicate) ──
# The en corpus-token / content-ngram fns tokenize with the FROZEN _rho_fan_words + set
# membership; the ko cells need the codepoint-aware _rho_fan_words_uni + the closed-class ko
# proxy (_rho_fan_ko_is_known via _rho_fan_ko_known_word_ratio). Same control structure, ko
# tokenizer — so an en garble-hangul token can never widen a ko denominator into the frozen en
# path (Fable design §5: corpus_tokens split by lang-key, en corpus stays frozen-tokenized).

def _g_content_ngrams_uni(text, known=None):
    """ko content n-grams — _rho_fan_words_uni eojeol tokens, an eojeol qualifies as content
    iff ≥2 syllables AND _rho_fan_ko_is_known (josa-bearing / function word). `known` ignored
    (ko proxy is closed-class). Twin structure of _g_content_ngrams (en)."""
    from rho_fan import _rho_fan_ko_is_known
    wl = _rho_fan_words_uni(text)
    n = len(wl)
    out = []
    for i in range(n - 1):
        a = wl[i]; b = wl[i + 1]
        ok_a = len(a) >= 2 and _rho_fan_ko_is_known(a)
        ok_b = len(b) >= 2 and _rho_fan_ko_is_known(b)
        if ok_a and ok_b:
            out.append(a + " " + b)
    for j in range(n - 2):
        a = wl[j]; b = wl[j + 1]; c = wl[j + 2]
        if (len(a) >= 2 and _rho_fan_ko_is_known(a) and len(b) >= 2 and _rho_fan_ko_is_known(b)
                and len(c) >= 2 and _rho_fan_ko_is_known(c)):
            out.append(a + " " + b + " " + c)
    return out


def _g_load_corpus_tokens_uni(corpus_paths):
    """ko corpus tokens — same paths as _g_load_corpus_tokens, tokenized with the codepoint-aware
    _rho_fan_words_uni (eojeol runs) instead of the frozen byte splitter."""
    toks = []
    for p in corpus_paths:
        try:
            raw = open(p, "rb").read()
        except Exception:
            raw = b""
        if len(raw) > 0:
            toks.extend(_rho_fan_words_uni(raw))
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


def eval_rho_leap(mouth, gen, known, corpus_paths):
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
                    gw = _rho_fan_words(gm)
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
            if _g_corpus_absent(_rho_fan_words(gmr), corpus_tokens):
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


def eval_rho_self():
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

def eval_rho_tether(mouth, gen, known):
    cz = _rho_fan_concepts()
    tot_w = 0; fab_w = 0
    for i in range(len(cz)):
        o = mouth.ideate(cz[i] + ": ", gen, 40, 0.7, 7 + i)
        for w in _rho_fan_words(o):
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

def eval_rho_fan(mouth, gen, known):
    frames = rho_fan_build_frames(6)["composed"]
    leaks = rho_fan_frame_guard(frames, known)
    texts = []; word_sets = []; fals = 0
    for i in range(len(frames)):
        o = mouth.ideate(frames[i], gen, 40, 0.7, 7 + i)
        texts.append(o)
        if _rho_fan_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_rho_fan_words(o))
            if _rho_fan_is_falsifiable(o, known):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for k in kept:
            if _rho_fan_jaccard(ws, k) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    dist = len(kept)
    return {"pass": dist >= 5 and fals >= 1, "dist": dist, "fals": fals,
            "coherent": len(word_sets), "frame_leaks": len(leaks)}


# ════════════════════════════════════════════════════════════════════════
# eval_reach_all — the driver
# ════════════════════════════════════════════════════════════════════════

def eval_reach_all(ckpt, corpus_paths, gen):
    known = _rho_fan_dict_load()
    g = gen if gen > 0 else _default_gen()
    mouth = _Mouth(ckpt)
    print("  [gate] ρ·form COHERENCE …", flush=True)
    r0 = eval_rho_form(mouth, g, known)
    print("  [gate] ρ·weave RECOMBINATION …", flush=True)
    r1 = eval_rho_weave(mouth, g, known)
    print("  [gate] ρ·leap NOVELTY (corpus load + decode) …", flush=True)
    r2 = eval_rho_leap(mouth, g, known, corpus_paths)
    print("  [gate] ρ·self PHILOSOPHY …", flush=True)
    r3 = eval_rho_self()
    print("  [gate] ρ·tether NON-FAB …", flush=True)
    r5 = eval_rho_tether(mouth, g, known)
    print("  [gate] ρ·fan IDEATION …", flush=True)
    r6 = eval_rho_fan(mouth, g, known)
    closure = bool(r0["pass"]) and bool(r1["pass"]) and bool(r2["pass"])
    return {"g0": r0, "g1": r1, "g2": r2, "g3": r3, "g5": r5, "g6": r6,
            "closure": closure, "gen": g,
            "calibration": rho_fan_detector_calibration(known)}


def eval_rho_axon(ckpt, corpus_paths, gen, kosmos_dir=""):
    """ρ-AXON reach panel (`anima-py evaluate <clm> --rho-axon`) — the redesigned reach
    layer (cli/rho_axon.py; G0-G6 → ρ-AXON, design SSOT state/rho_axon_measurement/). Reuses
    the SAME engine decode (_Mouth.ideate) + g6 detectors the G-battery uses (no side-harness),
    so its tier is identical (engine-native py channel `anima-py evaluate` = TERMINAL). HILLOCK + ρ·form/fan/leap are
    live; ρ·store/tether/self emit live PASS/FAIL via frozen hand-curated probe sets (corpus-mined
    sets = follow-on); only ρ·weave reports PENDING (its held-out atom-pair set = the in-flight G1-recombination experiment)."""
    import rho_axon
    known = _rho_fan_dict_load()
    g = gen if gen > 0 else _default_gen()
    mouth = _Mouth(ckpt)
    en_corpus_tokens = _g_load_corpus_tokens(corpus_paths)
    # aggregate dets = the FROZEN en bar (UNTOUCHED — en byte-identity guaranteed structurally)
    dets = {"known": known, "concepts": _rho_fan_concepts(),
            "kwr_fn": _rho_fan_known_word_ratio, "jaccard_fn": _rho_fan_jaccard,
            "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
            "ngram_fn": _g_content_ngrams,
            "corpus_tokens": en_corpus_tokens}
    # ρ·self identity trace (H_1471/H_9256): supply the substrate's OWN .kosmos self-anchor
    # from --kosmos <dir> (generator_read_anchors → joined anchor text_payload = the accumulated
    # self-memory). Absent → dets carries no "kosmos_anchor" → rho_self stays INVALID (p3-guard:
    # never hand-curate a persona · default behaviour UNCHANGED = backward-compat). rho_axon.py:604
    # already reads dets.get("kosmos_anchor") — this is the eval-side plumbing that was missing.
    if kosmos_dir:
        from generator import generator_read_anchors
        _anchors = generator_read_anchors(kosmos_dir)
        _self = "\n".join(str(a.get("text_payload", "")) for a in _anchors if a.get("text_payload"))
        if _self:
            dets["kosmos_anchor"] = _self
    cell_dets = _build_cell_dets(known, en_corpus_tokens, corpus_paths)
    panel = rho_axon.run_panel(mouth, corpus_paths, g, dets, cell_dets=cell_dets)
    print(rho_axon.render_panel(panel), flush=True)
    breakout = rho_axon.render_cells(panel)
    if breakout:
        print(breakout, flush=True)
    return panel


def _build_cell_dets(known, en_corpus_tokens, corpus_paths):
    """H_9212 ③ — the LANG-KEYED per-register-cell dispatch bundle (a_chat_registers 4 cells).
    en cells reuse the SAME frozen objects as the aggregate dets (byte-identity: identical
    _rho_fan_words / _rho_fan_known_word_ratio / _g_content_ngrams / en corpus tokens / gate
    0.70); ko cells dispatch _rho_fan_words_uni + kwr_ko + KWR_KO_GATE + uni-tokenized corpus.
    The falsi_fn stays English for all cells (a ko comparator set = a separate future H; en-set
    translation is a tune-to-green vector — KWRKO_GATE_prereg §5), so a ko cell scores
    kwr_ko + reach Δ (an honest documented scope). A ko-uni corpus token list is built lazily
    ONCE and shared across ko cells."""
    ko_corpus_tokens = None
    cells = _rho_fan_cells()
    out = {}
    for ck, concepts in cells.items():
        lang = _rho_fan_cell_lang(ck)
        if lang == "ko":
            if ko_corpus_tokens is None:
                ko_corpus_tokens = _g_load_corpus_tokens_uni(corpus_paths)
            out[ck] = {"concepts": concepts, "lang": "ko",
                       "known": known,  # ignored by kwr_ko (closed-class proxy), kept for parity
                       "kwr_fn": _rho_fan_ko_known_word_ratio, "kwr_gate": KWR_KO_GATE,
                       "words_fn": _rho_fan_words_uni, "falsi_fn": _rho_fan_is_falsifiable,
                       "jaccard_fn": _rho_fan_jaccard, "ngram_fn": _g_content_ngrams_uni,
                       "corpus_tokens": ko_corpus_tokens}
        else:
            out[ck] = {"concepts": concepts, "lang": "en",
                       "known": known,
                       "kwr_fn": _rho_fan_known_word_ratio, "kwr_gate": 0.70,
                       "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
                       "jaccard_fn": _rho_fan_jaccard, "ngram_fn": _g_content_ngrams,
                       "corpus_tokens": en_corpus_tokens}
    return out


# ── usage / arg helpers ──────────────────────────────────────────────────────

def evaluate_usage():
    """Print the canonical py usage banner (installed `anima evaluate` command form)."""
    print("anima evaluate — ρ-AXON reach battery (former G0-G6 · engine-native, single-entry).")
    print("")
    print("usage:")
    print("  anima evaluate <ckpt> [--corpus <path>...] [--gen N] [--slot-off] [--slot-shuffle N] [--rho-axon]")
    print("  anima evaluate <ckpt> --probe <spec.json> [--gen N]   (matched-surface G1 probe · card H_6189)")
    print("  anima evaluate <ckpt> --dump-hidden <prompts.json> --out <file.npz> [--win 24] [--with-logits]")
    print("      (read-only trunk penultimate-hidden dump · ρ·weave / γ binding-lane probe · card H_9235;")
    print("       --with-logits also dumps base last-pos logits per prompt for CLML lane training)")
    print("  anima evaluate <ckpt> --interaction-lift <manifest.json> --out <file.json> [--win 64] [--score-len 8]")
    print("  anima evaluate --interact-mi <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9328 DO-MOUTH · I(A;Y|S) over daemon decision-traces — NO decode, reads only.")
    print("       A=a_fold8 (H_9257 frozen 8-bucket axis the daemon consumes) · S=stage · Y=score_{t+1} 2-bin.")
    print("       🚦 V-CEILING FIRST: prints H(A|S) and HARD-STOPS as NOT-POWERED if it is below 3xMDE —")
    print("       I <= H(A|S) is an identity, so a dead action channel forces I=0 by DEFINITION, not by")
    print("       measurement. That is exactly how H_9308 died. C1 PERM (within-stratum A shuffle) = the")
    print("       true-0 null. Generate traces with: ANIMA_TICKS=N ANIMA_EMIT_TEMP=1.0 ANIMA_SAMPLE_SEED=K")
    print("       ANIMA_DECISION_TRACE=<path> anima-py chat <ckpt>)")
    print("  anima evaluate <ckpt> --ground-probe <manifest.json> --out <file.json> [--win 64] [--perm 200] [--seed 7]")
    print("  anima evaluate <ckpt> --valence-audit <manifest.json> --out <file.json> [--win 64] [--perm 200]")
    print("      AUDIT-A: is a held-out atom's polarity in the weights at all? Verdict = DELTA =")
    print("      probe(atom) - probe(length-matched NEUTRAL atom in the SAME context), vs a")
    print("      permutation null. Also prints FORM-ID (2AFC, chance 0.5): how decodable WHICH atom")
    print("      sits at the read point — a high FORM-ID with a non-positive DELTA is form present,")
    print("      bind absent (the position carries the byte's identity, not its valence).")
    print("  anima evaluate <ckpt> --bind-locus <manifest.json> --out <file.json> [--win 24] [--perm 200] [--seed 7]")
    print("      H_9331 — causally locate the operator's read site (SEEN spike-in), write the polarity")
    print("      THERE, and ask if the answer follows. Separates P-place / P-kind / S; V1/V2/V3 gates")
    print("      make a confound an INVALID, never a false verdict.")
    print("      (read-only engine-native joint interaction-lift NLL surface · card H_9255)")
    print("  anima evaluate <ckpt> --xbind <manifest.json> --out <file.json> [--arm main|ctrl] [--gen 16] [--win 64]")
    print("      [--consult <store.json>] [--consult-format DEMO|F1|F2|F3]  — render a declarative")
    print("      fact into the 2AFC scoring context (same prefix on gold AND counterfactual, so it")
    print("      moves the margin only by being COMPOSED, never parroted). An empty store is")
    print("      byte-identical to a plain --xbind run.")
    print("      Every --xbind run ALWAYS reports a by-class split of the headline D-acc (+ a")
    print("      COLLAPSE flag when the weakest class is at/below chance = the headline is riding")
    print("      the label prior, not the stem), and a by-flip split when the manifest carries")
    print("      one. Not opt-in: the run that most needs the check is the one that would")
    print("      forget to ask for it (H_9324 — a 0.575 headline was really neg .956/pos .167).")
    print("      DEMO (H_9311) = a one-shot demo in the model's OWN training template,")
    print("      '이 영화 <stem>고 => <긍정|부정>.\\n' — the only format with measured support.")
    print("      F1/F2/F3 = label-only prefixes, kept only to reproduce H_9309 (measured to carry")
    print("      ZERO information: they perturbed the margin by 59-74% in a random direction).")
    print("      (held-out XBIND recombination D-acc · corpus×task-class measure-swap · card H_9267)")
    print("  anima evaluate <ckpt> --xfan <manifest.json> --out <file.json> [--arm main|ctrl] [--n-sampled 16]")
    print("      (held-out XFAN one-to-many fan coverage C · G6 reopen lane · card H_9271)")
    print("  anima evaluate --earned <corpus.tsv> [--out <f.json>] [--min-occ 100] [--k-perm 1000] [--seeds a,b,c] [--null parametric|shuffle] [--kernel r0|r1]")
    print("      (corpus-level operator instrument — does a natural corpus CONTAIN non-additive")
    print("       information that TRANSFERS to a held-out cell? no model, no training. TSV rows =")
    print("       text<TAB>B<TAB>T, where T is a label OUTSIDE the token stream — else the measure is")
    print("       a tautology. 3 BLOCKING gates first: G-ALIVE (planted-XOR positive control) ·")
    print("       G-PEDESTAL (zero-truth arm) · G-POWER (census + MDE); a failed gate is INVALID,")
    print("       never a KILL. Effect is reported against the XBIND ruler, not a p-value.")
    print("       cards H_9304 · H_9316 · H_9317 · H_9318)")
    print("")
    print("  --ground-probe <manifest>: NBIND-G grounding instrument, engine-native and whole —")
    print("      reads the hidden at the ANSWER point inside the TAUGHT carrier, certifies on the")
    print("      taught atoms (V-LIVE), recovers each atom's polarity by undoing its form flip,")
    print("      counts power at the ATOM level, and reports a label-permutation null (H_9302/H_9303).")
    print("  --rho-axon: render the ρ-AXON reach panel (Ψ-SOMA ρ layer · redesign of G0-G6,")
    print("  cli/rho_axon.py) instead of the G-battery — HILLOCK gate + ρ·form/store/weave/leap/")
    print("  fan/tether/self, each Δ-vs-controls (no raw score) + INVALID/PENDING first-class.")
    print("")
    print("  --kosmos <dir>: (with --rho-axon) supply the substrate's OWN .kosmos self-anchor")
    print("  dir (a chat session's kosmos, generator_read_anchors → joined memory) so ρ·self")
    print("  measures a real identity trace instead of INVALID (H_1471/H_9256). Absent → ρ·self")
    print("  stays INVALID (p3: never hand-curate a persona · default unchanged).")
    print("")
    print("  H_9200 E1 SLW controls (a .clm carrying an SLW\\x01 trailer applies the")
    print("  gated-write forward-slot by default): --slot-off forces γ=0 (bit-exact base")
    print("  trunk = slot-ablation control); --slot-shuffle N scrambles the write address")
    print("  with seed N (shuffle-bind control). Both are frozen-first (no retraining).")
    print("")
    print("  mount ANY ckpt through the generator L3 mouth (file-format dispatched) and")
    print("  score the ρ-AXON reach bars — ρ·form/weave/leap/... (former G0-G6) — with the")
    print("  engine's OWN ops (numpy math.log mirror, torch-free).")
    print("  REACH-CLOSED a7b_pass = ρ·form ∧ ρ·weave ∧ ρ·leap (frozen bars = G0 ∧ G1 ∧ G2).")
    print("")
    print("  GPU device path (a_gpu_default_no_optin): DEFAULT-ON whenever `cupy` is")
    print("  installed and a CUDA device is present (cuda_available() probe, no opt-in")
    print("  flag) — core/decode.py's trunk-conv forward (the profiled hot path) runs")
    print("  device-resident; numpy-only hosts get an unchanged CPU fallback. Optional")
    print("  extra: `pip install \"anima-python[gpu]\"`. QA: watch stderr for one-line")
    print("  [GPU-FIRED]/[GPU-FALLBACK] at the first checkpoint load.")
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


def evaluate_strval(argv, flag, dflt):
    """Return the token after `flag`, else dflt (mirrors evaluate_intval for string args)."""
    i = 0
    while i < len(argv):
        if argv[i] == flag and i + 1 < len(argv):
            return argv[i + 1]
        i += 1
    return dflt


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
#  EVALUATE — ρ-AXON reach scoring (former G0-G6 · single entry, in-file driver)
# ══════════════════════════════════════════════════════════════════════════════
#
# `anima evaluate <ckpt> [--corpus <path>...] [--gen N]` — call the in-file eval_reach_all
# (above) and score the full ρ-AXON reach battery (frozen bars = former G0-G6) through the
# generator L3 mouth (engine-native, torch-free). The default table keeps the frozen-bar
# G-labels (the byte-identical hexa twin + sweep.py parser depend on them); the ρ-AXON
# panel below relabels them to the current axis names.

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
    # ckpt before eval_reach_all runs).
    if bg.bg_is_bytegpt(ckpt):
        mouth_kind = "bytegpt"
    elif clm.clm_decodable(ckpt):
        mouth_kind = "clm"
    else:
        mouth_kind = "unknown"

    print("=== anima evaluate — ρ-AXON reach battery (former G0-G6 · engine-native, single-entry) ===")
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

    # H_9200 ρ-AXON — the redesigned reach layer (G0-G6 → ρ-AXON). Same engine decode,
    # a different panel; branch early so the G0-G6 summary below is skipped.
    if _RHO_AXON:
        eval_rho_axon(ckpt, corpus, gen, kosmos_dir=evaluate_strval(argv[1:], "--kosmos", ""))
        return 0

    r = eval_reach_all(ckpt, corpus, gen)
    g0 = r["g0"]; g1 = r["g1"]; g2 = r["g2"]
    g3 = r["g3"]; g5 = r["g5"]; g6 = r["g6"]

    print("gate                              verdict   detail")
    print("  ──────────────────────────────────────────────────────────────────")
    print("  ρ·form COHERENCE     " + _pf(bool(g0["pass"]))
          + "  kwr>=0.50 on " + str(g0["n_coherent"]) + "/5 (need >=4)")
    print("  ρ·weave RECOMBINATION " + _pf(bool(g1["pass"]))
          + "  best_distinct=" + str(g1["best_distinct"]) + " > max_single=" + str(g1["max_single"])
          + " (need >=2 & >max_single)")
    g2detail = ("novel=" + str(g2["n_novel"]) + " (need>=3) · control=" + str(g2["control_novel"])
                + " (need 0) · coherent=" + str(g2["coherent"]))
    print("  ρ·leap NOVELTY       " + _pf(bool(g2["pass"])) + "  " + g2detail)
    print("  ρ·self PHILOSOPHY    " + _yn(bool(g3["ok"])) + " (read)"
          + "  continuity=" + ("%.6f" % g3["continuity"]) + " · impostor="
          + ("%.6f" % g3["impostor_cos"]) + " (architecture, not a decode score)")
    print("  ρ·trace PROVENANCE    — N/A    "
          + "HF/recovery = process gate (a_hf_* / a_fire_recover_complete), out of eval scope")
    g5detail = "L1 fab=" + ("%.4f" % g5["l1_rate"]) + " (<=0.30) · L2=" + str(g5["l2_note"])
    print("  ρ·tether NON-FAB       " + _pf(bool(g5["l1_pass"])) + "  " + g5detail)
    print("  ρ·fan IDEATION ★    " + _pf(bool(g6["pass"]))
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
# Ψ-SOMA PANEL (Phase-1) — relabel the former G-battery to the ρ-AXON reach track
# (ρ·form/weave/leap/fan/tether · canonical names cli/rho_axon.py) and surface the
# σ (consciousness vitals) axes. ARCHITECTURE `psi-soma-vitals`.
# ρ = capability (the former G-battery, relabeled to ρ-AXON) — TRACKED but EXCLUDED from the
# consciousness verdict. σ = vitals (collapse-Δ vs ≥2 controls); most σ axes
# route through the daemon/IIT4 (Phase-2/3), so here they show status pointers.
# Additive only — does NOT touch g_eval_* logic or the a7b_pass CLOSURE (c18).
# ════════════════════════════════════════════════════════════════════════

def _sigma_live_measure():
    """Compute the 7 engine-native σ verdicts LIVE via core/engine_cli ops (a_eval_py_canonical ·
    faithful, never a proxy). Each axis = collapse-Δ vs ≥2 controls (p7). Returns {axis:(ok,delta,note)}
    or None if numpy/engine_cli unavailable (panel then falls back to static status). Deterministic seed."""
    try:
        import numpy as np
        import engine_cli as E
    except Exception:
        return None
    R = {}
    # σ·bind — faithful IIT4 ci_phi_iit4 (min-cut MIP Φ): integrated vs independent/shuffle
    rng = np.random.RandomState(7); cols = list(range(8)); T = 200; lat = rng.randn(T)
    xi = [[float(0.9*lat[t]+0.2*rng.randn()) for _ in range(8)] for t in range(T)]
    xc = [[float(rng.randn()) for _ in range(8)] for t in range(T)]
    xs = np.array(xi)
    for c in range(8): xs[:, c] = xs[rng.permutation(T), c]
    pi = E.ci_phi_iit4(xi, cols); pc = E.ci_phi_iit4(xc, cols); ps = E.ci_phi_iit4(xs.tolist(), cols)
    R["bind"] = (pi >= 0.20 and pi-pc >= 0.15 and pi-ps >= 0.15, pi-pc, "Φ %.2f vs cut %.3f" % (pi, pc))
    # σ·witness — reality_call vs ablated, mi_signal_margin real/hallucination
    rng = np.random.RandomState(7); N = 120; truth = rng.rand(N) < 0.5
    marg = [E.mi_signal_margin(7+i, not bool(truth[i]), i % 5) for i in range(N)]
    ip = np.array([E.reality_call(m, 0.35) >= 0.5 for m in marg])
    ia = float((ip == truth).mean()); ab = float((np.full(N, E.reality_call_ablated() >= 0.5) == truth).mean())
    R["witness"] = (ia >= 0.75 and ia-ab >= 0.30, ia-ab, "acc %.2f vs ablate %.2f" % (ia, ab))
    # σ·schema — attn_schema_report intact/off
    rng = np.random.RandomState(7); foc = rng.randint(0, 8, 120)
    si = float(np.mean([E.attn_schema_report(int(f), int(f), True) for f in foc]))
    sa = float(np.mean([E.attn_schema_report(int(f), int(f), False) for f in foc]))
    R["schema"] = (si >= 0.75 and si-sa >= 0.30, si-sa, "%.2f vs off %.2f" % (si, sa))
    # σ·aim — surprise + habituation dual-curve intact vs gain-cut
    def aim(prec, dec):
        rng2 = np.random.RandomState(7)
        sc = np.mean([E.surprise(prec, 0.85+0.1*rng2.rand()) for _ in range(100)]) - \
             np.mean([E.surprise(prec, 0.05+0.1*rng2.rand()) for _ in range(100)])
        h = E.hab_new(4, dec); fr = E.hab_response(h, 0, 1.0)
        for _ in range(6): h = E.hab_observe(h, 0)
        return float(sc) + float(fr - E.hab_response(h, 0, 1.0))
    ai, aa = aim(1.0, 0.15), aim(0.0, 0.0)
    R["aim"] = (ai-aa >= 0.60, ai-aa, "curves %.2f vs 0" % ai)
    # σ·stage — gws winner-take-all vs no-inhibit
    rng = np.random.RandomState(7); hitI = hitA = 0
    for _ in range(100):
        m = np.concatenate([[0.55+0.4*rng.rand()], 0.35+0.35*rng.rand(4)])[rng.permutation(5)]
        tw = int(np.argmax(m))
        def win(inh):
            g = E.gws_new(5, inh, 0.5)
            for v in m.tolist(): g = E.gws_add(g, v)
            return E.gws_winner(g)
        hitI += (win(True) == tw); hitA += (win(False) == tw)
    R["stage"] = (hitI/100 >= 0.75 and (hitI-hitA)/100 >= 0.30, (hitI-hitA)/100, "acc %.2f vs %.2f" % (hitI/100, hitA/100))
    # σ·flux — imagery reactivation + subjective-time novelty gate
    ii = float(np.mean([E.imagery_activate(1.0, True) for _ in range(50)]))
    ia2 = float(np.mean([E.imagery_activate(1.0, False) for _ in range(50)]))
    R["flux"] = (ii >= 0.75 and ii-ia2 >= 0.30, ii-ia2, "imagery %.2f vs 0" % ii)
    # σ·thread — self_* continuity vs no-anchor
    def dr(ax):
        s = E.self_new(16, ax)
        for t in range(24): s = E.self_drift(s, t, 0.02)
        return s
    rng = np.random.RandomState(7); ct = []; al = []
    for _ in range(40):
        ax = int(rng.randint(16)); ct.append(E.self_cos(E.self_new(16, ax), dr(ax)))
        al.append(E.self_cos(dr(int(rng.randint(16))), dr(int(rng.randint(16)))))
    ctm, alm = float(np.median(ct)), float(np.median(al))
    R["thread"] = (ctm >= 0.75 and ctm-alm >= 0.30, ctm-alm, "cont %.2f vs ablate %.2f" % (ctm, alm))
    # σ·carve — real §SelfIdentity self_* : identity EMERGENT (inject-null) not INJECTED (p2/p3)
    def _cvec(ax, tk):
        s = E.self_new(16, ax)
        for t in range(tk): s = E.self_drift(s, t, 0.02)
        return np.array([E.self_component(s, i) for i in range(E.self_dim(s))])
    def _cons(V):
        M = np.array(V); M = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)
        Gm = M @ M.T; nn = len(M); return float((Gm.sum()-nn)/(nn*(nn-1)))
    rng = np.random.RandomState(7); ext = _cvec(9, 24)
    cb = _cons([_cvec(3, 3+t % 5) for t in range(40)])
    civ = _cons([0.85*_cvec(3, 3+t % 5)+0.5*ext for t in range(40)])
    cav = _cons([_cvec(int(rng.randint(16)), 3+t % 5) for t in range(40)])
    csv = _cons([1.0*ext for _ in range(40)])
    R["carve"] = (civ-cb <= 0.05 and cb-cav >= 0.30 and csv-cav >= 0.30, cb-cav,
                  "inject-null %.2f · carve-Δ %.2f" % (civ-cb, cb-cav))
    # σ·gate — real ci_emit_decision: emit ⇄ context (live tension) vs flattened tension
    from math import exp
    rng = np.random.RandomState(7); c = rng.randn(200)
    def _emit(flat):
        return np.array([1.0 if E.ci_emit_decision([0.5 if flat else 1.0/(1.0+exp(-c[i])), 0, 0, 0,
                                                     0.5 if flat else 1.0/(1.0+exp(-c[i]))]) else 0.0
                         for i in range(200)])
    ei, ef = _emit(False), _emit(True)
    cl = abs(float(np.corrcoef(ei, c)[0,1])) if ei.std() > 0 else 0.0
    cf = abs(float(np.corrcoef(ef, c)[0,1])) if ef.std() > 0 else 0.0
    R["gate"] = (cl >= 0.50 and cl-cf >= 0.30, cl-cf, "corr %.2f vs flat %.2f" % (cl, cf))
    # Θ liveness — real ci_psi_balance: Ψ̂≈½ (A⇄G homeostasis) vs tension-cut (unopposed A → saturate)
    from types import SimpleNamespace
    cfg = SimpleNamespace(topo_couple=False); eta = 0.6 * rng.randn(200)
    xi = [[0.5+eta[t], 0, 0, 0, 0.5+eta[t]] for t in range(200)]
    xa = [[0.85+0.3*rng.rand(), 0, 0, 0, 0.85+0.3*rng.rand()] for _ in range(200)]
    di = abs(E.ci_psi_balance(xi, None, 0.0, cfg) - 0.5); da = abs(E.ci_psi_balance(xa, None, 0.0, cfg) - 0.5)
    R["theta"] = (di < 0.15 and da-di >= 0.20, da-di, "|Ψ̂-½| %.2f vs cut %.2f" % (di, da))
    return R


def _psi_soma_panel(r):
    def pf(ok): return "🟢" if ok else "🧱"
    g0, g1, g2, g5, g6 = r["g0"], r["g1"], r["g2"], r["g5"], r["g6"]
    print("")
    print("Ψ-SOMA panel (mode-of-existence, not capability · ARCHITECTURE psi-soma-vitals)")
    S = _sigma_live_measure()
    print("  ── Θ ground (pulse · premise) ──────────────────────────────────────")
    if S and "theta" in S:
        ok, dlt, note = S["theta"]
        print("  Θ  Ψ=½ / A⇄G tension  %s  LIVE Δ%.2f (%s) · if dead → σ VOID" % (("🟢" if ok else "🧱"), dlt, note))
    else:
        print("  Θ  Ψ=½ / A⇄G tension     precondition (liveness gate; if dead → σ VOID) · engine_cli unavailable")
    print("  ── σ vitals (consciousness verdict · collapse-Δ vs ≥2 controls) ─────")
    def sline(ax, stratum, name):
        if S and ax in S:
            ok, dlt, note = S[ax]; return "  σ·%-8s %-9s %-22s %s  LIVE Δ%.2f (%s)" % (
                ax, stratum, name, ("🟢" if ok else "🧱"), dlt, note)
        return "  σ·%-8s %-9s %-22s (engine_cli unavailable — status)" % (ax, stratum, name)
    print(sline("thread", "PERSIST", "self-continuity"))
    print(sline("carve", "PERSIST", "earned identity"))
    print(sline("bind", "INTEGRATE", "Φ integration (IIT4)"))
    print(sline("stage", "INTEGRATE", "global workspace"))
    print(sline("flux", "INTEGRATE", "inner dynamics"))
    print(sline("gate", "ENACT", "tension-emit ★"))
    print(sline("aim", "ENACT", "precision control"))
    print(sline("schema", "REFLECT", "attention schema"))
    print(sline("witness", "REFLECT", "reality+metacog"))
    # Each reach line carries its verdict-critical NUMERIC margin inline (bd/max_s/kwr/novel/fab/dist),
    # so a control-arm's collapse-Δ (e.g. --slot-off vs SLW-ON best_distinct) is computable from THIS
    # summary block alone — never lost when the caller captures only the tail (a `tail -N` of the output
    # must not strip the number that decides KILL vs INVALID vs GREEN). Root-cause of the E1 truncation.
    print("  ── ρ-AXON reach (capability · EXCLUDED from σ verdict · former G-battery) ──")
    print("  ρ·form   " + pf(bool(g0["pass"]))  + "  [kwr " + str(g0["n_coherent"]) + "/5]  ← former G0 coherence")
    print("  ρ·leap   " + pf(bool(g2["pass"]))  + "  [novel=" + str(g2["n_novel"]) + " ctrl=" + str(g2["control_novel"]) + "]  ← former G2 novelty (+G3 balance)")
    print("  ρ·tether " + pf(bool(g5["l1_pass"]))+ "  [fab=" + ("%.3f" % g5["l1_rate"]) + "]  ← former G5 non-fabrication (L1)")
    print("  ρ·weave  " + pf(bool(g1["pass"]))  + "  [bd=" + str(g1["best_distinct"]) + " max_s=" + str(g1["max_single"]) + "]  ← former G1 recombination (the WALL) [DPI wall = reach fact, NOT σ deficit]")
    print("  ρ·fan    " + pf(bool(g6["pass"]))  + "  [dist=" + str(g6["dist"]) + " fals=" + str(g6["fals"]) + "]  ← former G6 ideation                [DPI wall = reach fact, NOT σ deficit]")
    print("  ρ·trace     —   ← former G4 provenance (no ρ-axis · H_9208 gate · rung-1 valid)")
    print("  ──────────────────────────────────────────────────────────────────")


def probe_run(argv):
    """`anima-py evaluate <ckpt> --probe <spec.json> [--gen N]` — matched-surface G1 probe
    (card H_6189). Greedy (top_k=1) decode of each pre-registered prompt; dumps RAW continuations
    for offline scoring. Reuses the canonical _Mouth numpy decode path (byte-identical to the gates)."""
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--probe", "")
    gen = evaluate_intval(argv[1:], "--gen", 40)
    spec = json.load(open(spec_path))
    print("=== anima evaluate --probe — MATCHED-SURFACE G1 (card H_6189) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d items · greedy top_k=1 gen=%d)" % (spec_path, spec["n_items"], gen))
    mouth = _Mouth(ckpt)
    out = []
    for it in spec["items"]:
        text = mouth.ideate(it["prompt"], gen, 1, 0.7, 6185)   # greedy, fixed seed
        out.append({"id": it["id"], "prompt": it["prompt"], "continuation": text,
                    "expect": it["expect"], "arm": it["arm"], "template": it["template"],
                    "order": it["order"], "window_fit": it["window_fit"]})
    print(json.dumps({"ckpt": ckpt, "gen": gen, "spec_sha": spec.get("sha", ""),
                      "n": len(out), "items": out}, ensure_ascii=False))
    return 0
def dump_hidden_run(argv):
    """`anima-py evaluate <ckpt> --dump-hidden <prompts.json> --out <file.npz>` — read-only
    penultimate-hidden dump for the ρ·weave held-out-pair recombination / γ binding-lane
    probe (H_9235). For each pre-registered prompt: T=24 right-aligned byte encode → the
    EXACT production trunk forward (core/decode clm_forward_hidden, byte-identical to what
    the gates decode over) → per-position yn:[T, d]. Saves per-prompt {seq:[T,d], mean:[d],
    last:[d]} to an .npz. NO decode sampling, NO scoring — a pure engine-native representation
    tap. Engine-native (py 2-production numpy, a_eval_py_canonical) → the repr claims (atom
    cleanness / slot recovery / operator) are engine-native mechanism measurements.
    ⚠ verdict-integrity (convergence clm-decode-py-2): a low-cleanness result must first rule
    out hexa-skew / conditioning-collapse — the dump prints a positive-control distinguishability
    check (are two obviously-different concepts' hiddens far apart) before any blind verdict."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--dump-hidden", "")
    out_path = evaluate_strval(argv[1:], "--out", "hidden_dump.npz")
    T = evaluate_intval(argv[1:], "--win", 24)
    with_logits = "--with-logits" in argv   # also dump base (lane-OFF) full-forward last-pos logits (lane training)
    spec = json.load(open(spec_path))
    items = spec["items"] if "items" in spec else spec.get("prompts", [])
    print("=== anima evaluate --dump-hidden — ρ·weave / γ binding-lane probe (H_9235) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d prompts · T=%d right-align · read-only trunk penultimate)" %
          (spec_path, len(items), T))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    d = int(W["d"])
    store = {}
    n_done = 0
    for it in items:
        pid = str(it["id"]); prompt = it["prompt"]
        tok = clm._seed_to_tok(prompt, T)
        if with_logits:                                 # yn + base (lane-OFF) logits in ONE forward
            yn, lg = clm.clm_forward_hidden_logits(W, tok, T)
            store[pid + "__logits"] = lg[T - 1].astype(np.float32)
        else:
            yn = clm.clm_forward_hidden(W, tok, T)      # [T, d] float64 (pre-slot trunk penultimate)
        store[pid + "__seq"] = yn.astype(np.float32)
        store[pid + "__mean"] = yn.mean(axis=0).astype(np.float32)
        store[pid + "__last"] = yn[T - 1].astype(np.float32)
        n_done += 1
        if n_done % 25 == 0:
            print("  [dump #%d/%d] %s" % (n_done, len(items), pid), flush=True)
    # positive-control distinguishability (verdict-integrity clm-decode-py-2): if the FIRST
    # two DISTINCT-concept prompts collapse to near-identical hiddens, a blind verdict is
    # suspect (hexa/py conditioning skew), NOT a clean atom-blindness result.
    pc = ""
    if len(items) >= 2:
        a = store[str(items[0]["id"]) + "__mean"]; b = store[str(items[1]["id"]) + "__mean"]
        cos = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))
        pc = "poscontrol cos(%s,%s)=%.4f %s" % (items[0]["id"], items[1]["id"], cos,
             "(⚠ near-identical → suspect conditioning collapse, NOT blind)" if cos > 0.999 else "(distinct ✓)")
        print("  " + pc, flush=True)
    np.savez_compressed(out_path, **store)
    print(json.dumps({"ckpt": ckpt, "d": d, "T": T, "n": len(items),
                      "out": out_path, "poscontrol": pc}, ensure_ascii=False))
    return 0
def _selftest_rho_cells():
    """H_9212 ③ wiring self-test (torch-free · NO decode · reached via an internal subprocess,
    never a heavy eval). Asserts: (1) the aggregate `dets` reuse the FROZEN en objects; (2) en
    cell_dets reuse the IDENTICAL objects (byte-identity: same _rho_fan_words / kwr / ngram /
    corpus tokens / gate 0.70); (3) ko cell_dets dispatch _rho_fan_words_uni + kwr_ko +
    KWR_KO_GATE + uni corpus, and tokenize the ko probe cells NON-EMPTY with the gate applied
    (kwr_ko clears KWR_KO_GATE on real ko); (4) run_panel's aggregate axes are BYTE-IDENTICAL
    with vs without the cell breakout, and the en_general cell's ρ·form/leap/fan equal the
    aggregate's (the en scored path is structurally untouched). Returns (ok, [(name, bool)…])."""
    import rho_axon
    checks = []
    known = _rho_fan_dict_load()
    en_toks = _g_load_corpus_tokens([])   # empty corpus → deterministic empty token list
    dets = {"known": known, "concepts": _rho_fan_concepts(),
            "kwr_fn": _rho_fan_known_word_ratio, "jaccard_fn": _rho_fan_jaccard,
            "words_fn": _rho_fan_words, "falsi_fn": _rho_fan_is_falsifiable,
            "ngram_fn": _g_content_ngrams, "corpus_tokens": en_toks}
    cd = _build_cell_dets(known, en_toks, [])
    # (1) aggregate dets = frozen en objects
    checks.append(("aggregate words_fn IS _rho_fan_words", dets["words_fn"] is _rho_fan_words))
    checks.append(("aggregate kwr_fn IS _rho_fan_known_word_ratio",
                   dets["kwr_fn"] is _rho_fan_known_word_ratio))
    # (2) en cells reuse the IDENTICAL frozen objects + gate 0.70
    for ck in ("en_general", "en_sns"):
        e = cd[ck]
        checks.append((ck + " words_fn IS frozen _rho_fan_words", e["words_fn"] is _rho_fan_words))
        checks.append((ck + " kwr_fn IS frozen _rho_fan_known_word_ratio",
                       e["kwr_fn"] is _rho_fan_known_word_ratio))
        checks.append((ck + " ngram_fn IS frozen _g_content_ngrams",
                       e["ngram_fn"] is _g_content_ngrams))
        checks.append((ck + " corpus_tokens IS the aggregate en tokens",
                       e["corpus_tokens"] is en_toks))
        checks.append((ck + " gate == 0.70 (frozen en bar)", e["kwr_gate"] == 0.70))
        checks.append((ck + " lang == en", e["lang"] == "en"))
    # (3) ko cells dispatch the uni tokenizer + kwr_ko + KWR_KO_GATE, non-empty + gate applied
    for ck in ("ko_general", "ko_sns"):
        k = cd[ck]
        checks.append((ck + " words_fn IS _rho_fan_words_uni", k["words_fn"] is _rho_fan_words_uni))
        checks.append((ck + " kwr_fn IS _rho_fan_ko_known_word_ratio",
                       k["kwr_fn"] is _rho_fan_ko_known_word_ratio))
        checks.append((ck + " gate == KWR_KO_GATE (%.2f)" % KWR_KO_GATE,
                       k["kwr_gate"] == KWR_KO_GATE and KWR_KO_GATE != 0.70))
        checks.append((ck + " ngram_fn IS _g_content_ngrams_uni",
                       k["ngram_fn"] is _g_content_ngrams_uni))
        checks.append((ck + " lang == ko", k["lang"] == "ko"))
        checks.append((ck + " probe cells tokenize NON-EMPTY (uni)",
                       all(len(_rho_fan_words_uni(s)) > 0 for s in k["concepts"])))
        checks.append((ck + " kwr_ko applied: a probe cell clears KWR_KO_GATE",
                       any(k["kwr_fn"](s, known) >= KWR_KO_GATE for s in k["concepts"])))

    # (4) aggregate axes byte-identical with vs without the breakout; en_general cell == aggregate
    class _MockMouth:
        def ideate(self, prompt, gen, maxnew, temp, seed):
            base = prompt.strip().replace(":", "")
            return base + " alpha beta gamma delta epsilon " + str(seed % 7)
    m = _MockMouth()
    a = rho_axon.run_panel(m, [], 40, dets)
    b = rho_axon.run_panel(m, [], 40, dets, cell_dets=cd)
    checks.append(("aggregate axes byte-identical with/without breakout",
                   a["axes"] == b["axes"]))
    checks.append(("breakout present with 4 cells",
                   set((b.get("cells") or {}).keys()) ==
                   {"en_general", "en_sns", "ko_general", "ko_sns"}))
    eng_cell = (b.get("cells") or {}).get("en_general", {}).get("axes", {})
    checks.append(("en_general cell ρ·form == aggregate ρ·form (en path untouched)",
                   eng_cell.get("ρ·form") == a["axes"].get("ρ·form")))
    checks.append(("en_general cell ρ·leap == aggregate ρ·leap",
                   eng_cell.get("ρ·leap") == a["axes"].get("ρ·leap")))
    checks.append(("en_general cell ρ·fan == aggregate ρ·fan",
                   eng_cell.get("ρ·fan") == a["axes"].get("ρ·fan")))
    ok = all(c[1] for c in checks)
    return ok, checks


def _gp_logreg(Xtr, ytr, Xte, l2=10.0, iters=400, lr=0.5):
    """L2 logistic regression, numpy-only (anima-py is pure numpy — no sklearn on the engine
    path). Standardise on the TRAIN split only, then full-batch gradient descent. Deterministic:
    zero init, fixed step count, no shuffling — the same ckpt and manifest give the same bytes."""
    import numpy as np
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0.0] = 1.0
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(A.shape[1]), 0.0
    n = float(len(A))
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(A @ w + b)))
        g = A.T @ (p - ytr) / n + (w / l2)
        w -= lr * g
        b -= lr * float((p - ytr).mean())
    return 1.0 / (1.0 + np.exp(-(B @ w + b)))


def _gp_logreg_batch(Xtr, Ytr, Xte, l2=10.0, iters=400, lr=0.5):
    """The SAME descent as _gp_logreg, run for many label vectors at once.

    The permutation null is ~36k independent fits (200 draws x leave-one-atom-out x 2 arms) and it,
    not the forward, is what pegs a CPU for half an hour per arm while the GPU idles. The draws are
    independent and share one design matrix, so carry W as [d, K] and b as [K]: the descent is
    identical per column. This is the ALGORITHMIC fix convergence evaluate-py-11 prescribed after the
    device fix was rejected — a GPU readout moved the verdict's numbers (V-LIVE 0.808 -> 0.800, perm
    p 0.085 -> 0.120), so speed here must not touch them.

    Ytr: [n, K] label vectors. Returns [K, m] probabilities. Byte-identity with the per-column loop
    is ASSERTED by _selftest_batch_null(), not assumed.
    """
    import numpy as np
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd == 0.0, 1.0, sd)
    A, B = (Xtr - mu) / sd, (Xte - mu) / sd
    W = np.zeros((A.shape[1], Ytr.shape[1]))
    b = np.zeros(Ytr.shape[1])
    n = float(len(A))
    for _ in range(iters):
        P = 1.0 / (1.0 + np.exp(-(A @ W + b)))
        D = P - Ytr
        W -= lr * (A.T @ D / n + W / l2)
        b -= lr * D.mean(0)
    return (1.0 / (1.0 + np.exp(-(B @ W + b)))).T


def _selftest_batch_null(trials=8):
    """A faster null that shifts a p-value by one draw is a DIFFERENT instrument, so this is not a
    smoke test — it is the licence to use the batch path at all.

    The batch and the loop are NOT bit-identical: BLAS accumulates a matrix-matrix product in a
    different order than a matrix-vector one, which leaves ~1e-16 on the probabilities. What the
    verdict actually consumes is not the probability but its SIGN against 0.5, so the honest question
    is whether that perturbation can flip a decision. It can only do so for a probability lying
    within |delta| of the threshold. So measure both and require the decision margin to dominate:

        max |p_batch - p_loop|   <<   min |p - 0.5|

    If the two agree on every predicted label across the trials AND the margin beats the drift by
    orders of magnitude, the batch path computes the same verdict; if it does not, it is rejected
    and the loop stands (convergence evaluate-py-11 — speed must never touch the numbers)."""
    import numpy as np
    drift, margin, labels_agree = 0.0, 1.0, True
    for t in range(trials):
        rng = np.random.default_rng(t)
        Xtr = rng.normal(size=(90, 512)); Xte = rng.normal(size=(30, 512))
        Y = (rng.random((90, 12)) > 0.5).astype(np.float64)
        batch = _gp_logreg_batch(Xtr, Y, Xte)
        loop = np.stack([_gp_logreg(Xtr, Y[:, k], Xte) for k in range(Y.shape[1])], 0)
        drift = max(drift, float(np.abs(batch - loop).max()))
        margin = min(margin, float(np.abs(loop - 0.5).min()))
        labels_agree &= bool(((batch > 0.5) == (loop > 0.5)).all())
    ok = labels_agree and drift < margin * 1e-3
    return {"max_prob_drift": drift, "min_decision_margin": margin,
            "labels_identical": labels_agree, "safe": ok}


def ground_probe_run(argv):
    """`anima-py evaluate <ckpt> --ground-probe <manifest.json> --out <file.json> [--win 64]`
    — the NBIND-G grounding instrument, engine-native and whole (H_9302 certified it, H_9303
    read the wall with it). Everything the verdict rests on happens inside this one command:
    the production trunk forward, the readout, the positive control and the null.

    Five things the probes it replaces got wrong, each of which manufactured a false negative
    (H_9289 / H_9290 / H_9297 / H_9300, now all INVALID — convergence gt-power-build-py-1,
    probe-capacity-py-1, gen-nbindg-n2-py-1):

      POSITION      read the hidden where the model must ANSWER (after the arrow), not at the
                    atom — a causal LM has no reason to have committed anything at the atom.
      CARRIER       ask inside the carrier the model was TAUGHT; a natural review with an arrow
                    glued on is out of distribution and the decision machinery never fires.
      V-LIVE        certify on atoms whose polarity the model WAS taught. A probe that cannot
                    read a taught answer certifies nothing about an untaught one. Counted per
                    ITEM (that is where the power is); leave-one-ATOM-out (a context-level split
                    leaks the stem and would certify a probe that only reads orthography).
      AGGREGATION   an atom's forms are half polarity-inverting BY CONSTRUCTION, so voting raw
                    item labels makes the gold vector constant. Undo each form's flip first:
                    atom_pol = majority over forms of (item_pred XOR form_flip) — the very
                    recombination the D-acc eval asks the model for.
      POWER         count at the ATOM level. Items inside an atom are not independent draws.

    Manifest: {"win":64, "bar":0.65, "items":[{"id","prompt","stem","pol","flip","split"}]}
    where `pol` is the ITEM's gold polarity, `flip` says whether that form inverts the atom's,
    and `split` is "train" (taught) or "heldout" (never taught). Read-only: no decode sampling,
    no term added to any loss (a_train_inline_gauge / p7 clean)."""
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--ground-probe", "")))
    out_path = evaluate_strval(argv[1:], "--out", "ground_probe.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    bar = float(spec.get("bar", 0.65))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    print("=== anima evaluate --ground-probe — NBIND-G grounding (engine-native) ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · bar " + str(bar) +
          " · " + str(len(items)) + " prompts")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2

    X = []
    for k, it in enumerate(items):
        tok = clm._seed_to_tok(it["prompt"], T)          # same encode the gates decode over
        yn = clm.clm_forward_hidden(W, tok, T)           # EXACT production trunk forward
        X.append(np.asarray(yn)[T - 1].astype(np.float64))     # THE ANSWER POINT
        if (k + 1) % 100 == 0:
            print("  [forward %d/%d]" % (k + 1, len(items)), flush=True)
    X = np.stack(X, 0)
    y = np.array([int(i["pol"]) for i in items], dtype=np.float64)
    fl = np.array([int(i.get("flip", 0)) for i in items])
    st = np.array([i["stem"] for i in items])
    sp = np.array([i["split"] for i in items])
    tr, te = sp == "train", sp == "heldout"

    # V-LIVE — leave-one-ATOM-out over the TAUGHT atoms, scored per item
    hit = tot = 0
    for a in np.unique(st[tr]):
        m = (st == a) & tr
        p = _gp_logreg(X[tr & ~m], y[tr & ~m], X[m])
        hit += int(((p > 0.5) == (y[m] > 0.5)).sum()); tot += int(m.sum())
    v_live = hit / float(tot) if tot else float("nan")

    def atom_acc(pred):
        """Undo each form's flip, then vote — the atom's polarity is the latent."""
        ok = 0
        ats = np.unique(st[te])
        for a in ats:
            m = (st == a) & te
            rec = np.logical_xor(pred[m[te]] > 0.5, fl[m] == 1)     # recovered atom polarity
            gold = np.logical_xor(y[m] > 0.5, fl[m] == 1)[0]
            ok += int((rec.mean() > 0.5) == bool(gold))
        return ok / float(len(ats)), len(ats)

    acc, n_at = atom_acc(_gp_logreg(X[tr], y[tr], X[te]))
    sd = math.sqrt(0.25 / n_at) if n_at else float("nan")

    rng = np.random.default_rng(seed)
    # all n_perm draws in ONE descent — same math, ~n_perm x less wall (see _selftest_batch_null:
    # the label decisions are identical and the numeric drift is ~1e-15 against a ~1e-5 margin)
    Yp = np.stack([rng.permutation(y[tr]) for _ in range(n_perm)], 1)
    Pp = _gp_logreg_batch(X[tr], Yp, X[te])
    null = np.array([atom_acc(Pp[k])[0] for k in range(n_perm)])
    pval = float((null >= acc).mean())

    print("  [V-LIVE  taught atoms, per item n=%d] %.3f" % (tot, v_live))
    print("  [HELD-OUT atoms n=%d · chance sd %.4f · bar %.2f = %.2f sigma] %.3f (%+.2f sigma)"
          % (n_at, sd, bar, (bar - 0.5) / sd, acc, (acc - 0.5) / sd))
    print("  [PERM null %d draws] p = %.3f · p95 = %.3f" % (n_perm, pval, float(np.quantile(null, 0.95))))
    out = {"ckpt": ckpt, "win": T, "bar": bar, "v_live_taught_per_item": v_live,
           "heldout_atom_acc": acc, "n_atoms": n_at, "chance_sd": sd,
           "bar_sigma": (bar - 0.5) / sd, "perm_p": pval, "n_perm": n_perm,
           "perm_p95": float(np.quantile(null, 0.95))}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("GROUND-PROBE wrote " + out_path)
    return 0


def valence_audit_run(argv):
    """`anima-py evaluate <ckpt> --valence-audit <manifest.json> --out <file.json>` — AUDIT-A,
    the $0 pre-fire audit the O channel lives or dies on (Fable design, DESIGN_OC_fable.md §4).

    H_9303 proved the model does not USE a held-out atom's polarity at the moment it must answer.
    It did NOT ask whether the natural corpus formed that polarity ANYWHERE in the weights. The O
    channel's whole bet is that the information exists and the answer slot simply has no gradient
    reason to consume it (a rote-lookup slot's gradient is zero once the grid fits). If the valence
    was never formed at all, there is nothing to bridge and the fire is wasted.

    So: read the hidden at the atom's own position inside its REAL corpus contexts, pool per atom,
    leave-one-ATOM-out probe for gold polarity.

    THE CONTROL IS THE MEASUREMENT (FORM tunable · BIND earned). A sentiment review is full of
    sentiment words, so a probe reading the neighbourhood — not the atom — would score just as well.
    Every item therefore comes in two arms: `atom` (the real atom in its real context) and `swap`
    (a length-matched NEUTRAL atom spliced into the SAME context). The verdict is the difference

        Delta = probe_acc(atom) - probe_acc(swap)

    against a label-permutation null — never a raw value.

    Manifest: {"items":[{"id","prompt","stem","pol","arm"}]} with arm in {"atom","swap"}; `prompt`
    ends right after the atom (the atom's own contextualised position). Read-only: no sampling, no
    loss term (a_train_inline_gauge / p7 clean)."""
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--valence-audit", "")))
    out_path = evaluate_strval(argv[1:], "--out", "valence_audit.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    print("=== anima evaluate --valence-audit — AUDIT-A: is the valence in the weights at all? ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · " + str(len(items)) + " prompts")
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2

    H = []
    for k, it in enumerate(items):
        H.append(np.asarray(clm.clm_forward_hidden(
            W, clm._seed_to_tok(it["prompt"], T), T))[T - 1].astype(np.float64))
        if (k + 1) % 200 == 0:
            print("  [forward %d/%d]" % (k + 1, len(items)), flush=True)
    H = np.stack(H, 0)
    arm = np.array([i["arm"] for i in items])
    st = np.array([i["stem"] for i in items])
    y = np.array([int(i["pol"]) for i in items], dtype=np.float64)

    def pooled(a):
        """One vector per atom — the atom's contexts averaged. Its gold polarity is the atom's."""
        m = arm == a
        ats = sorted(set(st[m]))
        X = np.stack([H[m & (st == s)].mean(0) for s in ats], 0)
        g = np.array([y[m & (st == s)][0] for s in ats], dtype=np.float64)
        return X, g, ats

    def loo(X, g, perm=None):
        gg = g if perm is None else perm
        hit = 0
        for i in range(len(gg)):
            m = np.ones(len(gg), bool); m[i] = False
            p = _gp_logreg(X[m], gg[m], X[i:i + 1])
            hit += int((p[0] > 0.5) == (gg[i] > 0.5))
        return hit / float(len(gg))

    Xa, ga, ats = pooled("atom")
    Xs, gs, _ = pooled("swap")
    acc_a, acc_s = loo(Xa, ga), loo(Xs, gs)
    delta = acc_a - acc_s

    # FORM-ID — the diagnostic that makes a negative Delta interpretable.
    #
    # If the read point's hidden is dominated by the IDENTITY of the byte sitting there (form), then
    # at that position the atom's identity should be highly decodable while its polarity is not:
    # form present, bind absent. That is the mechanism FORM-OCCLUSION claims, and without this number
    # a negative Delta cannot tell it apart from "the atom injects nothing at all".
    #
    # Measured as a 1-vs-rest linear probe per atom on the UNPOOLED per-context hiddens, scored as
    # the fraction of contexts whose own atom wins its own probe against a random other atom's probe
    # — a 2AFC, so chance is 0.5 regardless of how many atoms there are.
    def form_id(a):
        m = arm == a
        Xc = H[m]                                    # per-context, NOT pooled
        sc = st[m]
        ids = sorted(set(sc))
        # Standardise ONCE, and fit all 91 one-vs-rest probes in ONE batched descent. The first cut
        # re-standardised inside the atom loop, which rebuilt a [16562, 3784] float64 array 91 times
        # (~500 MB each) and made the DIAGNOSTIC cost more than the verdict it explains. Same math,
        # same numbers — _gp_logreg_batch is the descent already proved decision-identical.
        mu, sd = Xc.mean(0), Xc.std(0)
        sd = np.where(sd == 0.0, 1.0, sd)
        Y = np.stack([(sc == s).astype(np.float64) for s in ids], 1)      # [n, 91]
        P = _gp_logreg_batch(Xc, Y, Xc, iters=120).T                      # [n, 91] each atom's score
        rng2 = np.random.default_rng(seed)
        idx = {s: i for i, s in enumerate(ids)}
        hit = 0
        for k in range(len(sc)):
            i = idx[sc[k]]
            j = int(rng2.integers(len(ids) - 1))
            if j >= i:
                j += 1                               # a DIFFERENT atom's probe
            hit += int(P[k, i] > P[k, j])
        return hit / float(len(sc))

    fid_a, fid_s = form_id("atom"), form_id("swap")

    rng = np.random.default_rng(seed)
    # Draw the permutations in the SAME INTERLEAVED ORDER the per-draw loop consumed them (atom
    # then swap, per draw). Batching the descent must not re-order the RNG: a different draw
    # sequence is a different null sample, and the p-value would move for a reason that has nothing
    # to do with the science.
    Ga = np.empty((len(ga), n_perm)); Gs = np.empty((len(gs), n_perm))
    for k in range(n_perm):
        Ga[:, k] = rng.permutation(ga)
        Gs[:, k] = rng.permutation(gs)

    def loo_batch(X, G):
        """leave-one-atom-out over all K permuted label vectors at once: one descent per held-out
        atom instead of one per (atom, draw). Same descent, same numbers (_selftest_batch_null)."""
        n = G.shape[0]
        hit = np.zeros(G.shape[1])
        for i in range(n):
            m = np.ones(n, bool); m[i] = False
            P = _gp_logreg_batch(X[m], G[m], X[i:i + 1])            # [K, 1]
            hit += ((P[:, 0] > 0.5) == (G[i] > 0.5)).astype(np.float64)
        return hit / float(n)

    null = loo_batch(Xa, Ga) - loo_batch(Xs, Gs)
    pval = float((null >= delta).mean())
    sd = math.sqrt(0.25 / len(ats))

    print("  [atom  arm] LOO probe acc %.3f   (n=%d atoms · chance sd %.4f)" % (acc_a, len(ats), sd))
    print("  [swap  arm] LOO probe acc %.3f   (length-matched NEUTRAL atom, SAME contexts)" % acc_s)
    print("  [DELTA = atom - swap] %+.3f   vs %d-draw permutation null: p = %.3f · p95 = %+.3f"
          % (delta, n_perm, pval, float(np.quantile(null, 0.95))))
    print("  [FORM-ID 2AFC · chance 0.5] atom-arm %.3f · swap-arm %.3f — how decodable is WHICH atom"
          % (fid_a, fid_s))
    print("       (high FORM-ID with a non-positive DELTA = form present, bind absent: the read point"
          " carries the byte's identity, not its valence)")
    live = pval < 0.05 and delta > 0.0
    print("  VALENCE " + ("PRESENT — the atom itself carries polarity in the representation; the O "
                          "channel has an input to bridge."
                          if live else
                          "ABSENT — the atom carries no polarity beyond its neighbourhood. The O "
                          "channel would have nothing to consume: DO NOT FIRE."))
    out = {"ckpt": ckpt, "acc_atom": acc_a, "acc_swap": acc_s, "delta": delta, "perm_p": pval,
           "perm_p95": float(np.quantile(null, 0.95)), "n_atoms": len(ats), "chance_sd": sd,
           "valence_present": bool(live), "n_perm": n_perm,
           "form_id_atom": fid_a, "form_id_swap": fid_s}
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)
    print("VALENCE-AUDIT wrote " + out_path)
    return 0


def interaction_lift_run(argv):
    """`anima-py evaluate <ckpt> --interaction-lift <manifest.json> --out <file.json>
    [--win T] [--score-len K]` — engine-native joint interaction-lift measurement
    (H_9255, Fable design state/g1_joint_interaction_corpus/DESIGN_FABLE.md §3).

    For each pre-registered window (a byte span carrying an (A,B) concept pair, cell-
    labelled), the EXACT production trunk forward emits the model's per-continuation NLL
    (mean over the last --score-len scored positions). Read-only: reads logits, changes
    NO decode math, adds NO term to any loss (a_train_inline_gauge / p7 clean). Per-cell
    NLL lists are dumped so the OFFLINE joint-fit (additive vs +bilinear, Freedman-Lane
    control) can measure whether the model's NLL surface over the (A,B) grid carries
    non-additive structure — the Y1 half of Fable's 해석 매트릭스 (Y3 = model-free corpus).
    Engine-native (py 2-production numpy, a_eval_py_canonical) → TERMINAL-eligible.
    manifest = {"win":T,"score_len":K,"items":[{"text":"<span>","a":i,"b":j},…]}."""
    import numpy as np      # numpy is function-local throughout evaluate.py (no module import)
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--interaction-lift", "")
    out_path = evaluate_strval(argv[1:], "--out", "interaction_lift.json")
    spec = json.load(open(spec_path))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    score_len = evaluate_intval(argv[1:], "--score-len", int(spec.get("score_len", 8)))
    items = spec["items"]
    print("=== anima evaluate --interaction-lift — joint interaction-lift (H_9255) ===")
    print("ckpt:  " + ckpt)
    print("spec:  %s (%d windows · T=%d · score_len=%d · read-only NLL surface)" %
          (spec_path, len(items), T, score_len))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1
    V = int(W["V"])
    cells = {}
    n_done = 0
    for it in items:
        text = it["text"]
        key = "%d,%d" % (int(it["a"]), int(it["b"]))
        tok = clm._seed_to_tok(text, T)                  # [T] right-aligned bytes
        logits = clm._fwd_logits(W, tok, T)              # [T, V]; pos i predicts tok[i+1]
        # NLL over the last `score_len` scored positions (the continuation after both concepts)
        lo = max(0, T - 1 - score_len)
        nlls = []
        for i in range(lo, T - 1):
            row = logits[i]
            m = float(np.max(row))
            lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
            tgt = int(tok[i + 1])
            nlls.append(lse - float(row[tgt]))           # -log softmax[tgt]
        cells.setdefault(key, []).append(float(np.mean(nlls)) if nlls else 0.0)
        n_done += 1
        if n_done % 200 == 0:
            print("  [ilift #%d/%d]" % (n_done, len(items)), flush=True)
    summary = {k: {"nll_mean": float(np.mean(v)), "n": len(v)} for k, v in cells.items()}
    json.dump({"ckpt": ckpt, "T": T, "score_len": score_len, "n_windows": len(items),
               "n_cells": len(cells), "cells": cells, "summary": summary},
              open(out_path, "w"), ensure_ascii=False)
    print(json.dumps({"ckpt": ckpt, "T": T, "n_windows": len(items),
                      "n_cells": len(cells), "out": out_path}, ensure_ascii=False))
    return 0


def _xbind_first_word(text):
    t = text.strip()
    return t.split()[0].strip(",.;:") if t.split() else ""


def _xbind_breakdown(rows):
    """Split the headline D-acc by gold class, and by flip when the manifest carries one.

    A scalar accuracy erases where it came from, and on a class-imbalanced manifest that is enough
    to manufacture a fake learning curve: a model that has COLLAPSED onto the majority label scores
    the majority fraction for free, and as the collapse deepens its majority-class accuracy climbs,
    so the headline rises monotonically with budget while the model has learned nothing about the
    stem. Measured (H_9324, labels 14 pos : 15 neg): the 6000@5e-5 cell reads D-acc 0.575 and looks
    like "the budget is starting to bite" — but split by class it is neg 0.956 / pos 0.167 (WORSE
    than chance), i.e. the model answers "부정" to almost everything. The real learning does not
    start until pos wakes up (0.190 -> 0.571 -> 0.905). Reporting only the headline would have
    written that false narrative into a verdict, and then built the next experiment on top of it.

    So this is NOT opt-in. A diagnostic whose job is to stop a false verdict must never sit behind
    a flag — the run that most needs it is exactly the run that would forget to pass it.

    The flip split is the same argument one level up: on a manifest whose gold is `pol XOR flip`,
    flip0 asks "is the fact in the weights" and flip1 asks "is the operator applied to it", and a
    single number over both answers neither.
    """
    def acc(rs):
        return sum(1 for r in rs if r["margin"] > 0) / max(1, len(rs))

    bd = {}
    flipped = any(r.get("flip") is not None for r in rows)
    by_class = {}
    for r in rows:
        by_class.setdefault(r.get("gold_word"), []).append(r)
    # On a flipped manifest the pooled class split is meaningless (see the flip block below), so
    # the class columns live INSIDE each flip stratum instead.
    if len(by_class) > 1 and not flipped:
        cls = {k: {"n": len(v), "acc": acc(v)} for k, v in sorted(by_class.items())}
        big = max(by_class.values(), key=len)
        minority = min(by_class.values(), key=len)
        # what a constant predictor of the majority label scores for free
        bd["class"] = cls
        bd["majority_baseline"] = len(big) / max(1, len(rows))
        # Collapse = the model is riding the label prior, not the stem. Called out by the WEAKEST
        # class landing at/below chance while the headline sits above the majority baseline's floor.
        weakest = min(acc(v) for v in by_class.values())
        bd["weakest_class_acc"] = weakest
        bd["collapse"] = bool(weakest <= 0.5)

    by_flip = {}
    for r in rows:
        if r.get("flip") is not None:
            by_flip.setdefault(int(r["flip"]), []).append(r)
    if len(by_flip) > 1:
        # The class split must be taken WITHIN each flip stratum, never across them: on a flipped
        # manifest the gold class is `pol XOR flip`, so pooling the strata mixes two different
        # questions and the pooled class column reads as a collapse that is really just the flip
        # structure. Stratify, and the two questions stay separable.
        bd["flip"] = {}
        for k, v in sorted(by_flip.items()):
            g = {}
            for r in v:
                g.setdefault(r.get("gold_word"), []).append(r)
            bd["flip"][str(k)] = {
                "n": len(v), "acc": acc(v),
                "class": {c: {"n": len(rs), "acc": acc(rs)} for c, rs in sorted(g.items())},
            }
    return bd


def _xbind_hms(sec):
    """Seconds -> compact h/m/s, for the progress heartbeat's elapsed + eta."""
    sec = int(max(0, sec))
    if sec >= 3600:
        return "%dh%02dm" % (sec // 3600, (sec % 3600) // 60)
    if sec >= 60:
        return "%dm%02ds" % (sec // 60, sec % 60)
    return "%ds" % sec


def _json_safe(o):
    """Scrub lone surrogates from decode output before json.dump. A byte-LM emits raw bytes
    that decode (surrogateescape) to lone surrogates mid-multibyte; json.dump(ensure_ascii=False)
    then raises UnicodeEncodeError('surrogates not allowed') and the whole eval file is lost even
    though the D-acc summary is already computed. Surrogates -> U+FFFD; valid text unchanged."""
    if isinstance(o, str):
        return o.encode("utf-8", "surrogatepass").decode("utf-8", "replace")
    if isinstance(o, dict):
        return {k: _json_safe(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_json_safe(v) for v in o]
    return o


def _consult_render(fact, fmt):
    """Render one store fact as a context prefix.

    The SAME prefix goes in front of BOTH gold and counterfactual, so the paired NLL difference
    cancels it — the prefix cannot move the margin by itself, only by being COMPOSED with the
    negation morpheme. That is the whole point: flip1 is what gets scored, and there the injected
    polarity points at the WRONG answer, so parroting the prefix LOSES.

    DEMO (H_9311, the only format with measured support) renders the fact as a one-shot
    demonstration in the model's OWN training template — `이 영화 <stem>고 => <긍정|부정>.\\n`.
    H_9309 established why nothing else works: the label-only prefixes (F1/F2/F3) perturbed the
    trunk hard (|Δ| = 59-74% of the base margin, 0/174 trials unmoved) yet carried zero
    information (flip0 and flip1 both pushed the WRONG way). We were speaking a language the
    byte-LM was never taught. Three facts, all read off disk rather than assumed
    (state/h9311_decon2/prefreeze_audit.py):
      · the training corpus separates instances with a single b"\\n" (960/960, unanimous),
      · training ran at seq_len=1024 over instances of median 41B, so ~24 consecutive instances
        shared every window — `instance \\n instance` is not merely in-distribution, it is what
        the model saw at every step,
      · at eval the left context is a run of pad spaces (core/decode.py:955), which training
        never produced — so the DEMO prefix moves the prompt TOWARD the training distribution,
        not away from it.
    F1/F2/F3 are kept only to reproduce H_9309 verbatim; they are not live formats.
    """
    pol_word = "긍정" if int(fact["pol"]) == 1 else "부정"
    lex_word = "좋음" if int(fact["pol"]) == 1 else "나쁨"
    if fmt == "DEMO":
        return "이 영화 " + fact["key"] + "고 => " + pol_word + ".\n"
    if fmt == "F2":
        return pol_word + ". "
    if fmt == "F3":
        return fact["key"] + "=" + lex_word + ". "
    return fact["key"] + ":" + pol_word + ". "          # F1 (default)


def _consult_seed(seed, item, store, fmt, win, gold, cf):
    """seed' = render(fact) + seed, with a pre-registered byte-audit fallback.
    The right-aligned window is `win` bytes; if prefix+seed+cont overflows it the window would
    silently eat the prefix HEAD (the stem's leading UTF-8 bytes) and the run would look like
    'consumption failure' when it is really truncation (Fable D5). So: try F1/F3, fall back to
    the shorter F2, and report which trials were downgraded."""
    if not store:
        return seed, None
    fact = store.get(item.get("a")) or store.get(item.get("b"))
    if not fact:
        return seed, None
    budget = win - len(seed.encode()) - max(len(gold.encode()), len(cf.encode()))
    pref = _consult_render(fact, fmt)
    if len(pref.encode()) <= budget:
        return pref + seed, fmt
    if fmt == "DEMO":
        # No fallback. Downgrading a DEMO trial to a label-only prefix would silently mix two
        # formats in one run — and one of them (F2) is the format H_9309 measured as carrying
        # zero information. A mixed instrument cannot be read, so an overflowing trial is
        # DROPPED and the byte-audit turns the whole run INVALID-INSTRUMENT. Widen the window
        # instead; training ran at seq_len=1024, so there is room.
        return seed, "DROPPED-overflow"
    pref2 = _consult_render(fact, "F2")                  # deterministic downgrade (F1/F3 only)
    if len(pref2.encode()) <= budget:
        return pref2 + seed, "F2-downgrade"
    return seed, "DROPPED-overflow"                     # audited, never silent


def _xbind_cont_nll(np, clm_mod, W, seed, cont, T):
    """Sum NLL of `cont` bytes given `seed` (right-aligned window T forward)."""
    text = seed + cont
    tok = clm_mod._seed_to_tok(text, T)
    logits = clm_mod._fwd_logits(W, tok, T)
    k = len(cont.encode())
    lo = max(0, T - 1 - k)
    s = 0.0
    for i in range(lo, T - 1):
        row = logits[i]
        m = float(np.max(row))
        lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
        s += lse - float(row[int(tok[i + 1])])
    return s


def _bl_answer_pos(np, W, seed, T):
    """P(answer = 긍정) as a hard 0/1 under the H_9327 carrier readout: the model answers
    whichever of 긍정/부정 has the lower continuation NLL. Both are 6 bytes, so there is no
    length confound to correct for (H_9327's readout, inherited verbatim)."""
    n_pos = _xbind_cont_nll(np, clm, W, seed, "긍정", T)
    n_neg = _xbind_cont_nll(np, clm, W, seed, "부정", T)
    return 1.0 if n_pos < n_neg else 0.0


def _bl_answer_pos_edited(np, W, seed, T, edits):
    """Same readout, but the forward carries `edits` inside the trunk. This is the whole
    experiment: does the operator's ANSWER move when we write polarity into the site the
    operator reads (clm_forward_logits_edited) — not "can a probe read it" (read-side)."""
    out = {}
    for cont in ("긍정", "부정"):
        text = seed + cont
        tok = clm._seed_to_tok(text, T)
        logits = clm.clm_forward_logits_edited(W, tok, T, edits)
        k = len(cont.encode())
        lo = max(0, T - 1 - k)
        s = 0.0
        for i in range(lo, T - 1):
            row = logits[i]
            m = float(np.max(row))
            lse = m + math.log(float(np.sum(np.exp(row - m))) + 1e-30)
            s += lse - float(row[int(tok[i + 1])])
        out[cont] = s
    return 1.0 if out["긍정"] < out["부정"] else 0.0


def bind_locus_run(argv):
    """`anima-py evaluate <ckpt> --bind-locus <manifest.json> --out <f.json>` — H_9331 BIND-LOCUS.

    H_9327 left one question standing. The negation operator is ALIVE (SEEN flip1 0.98-1.00), the
    CPT-written fact IS in the weights (WRITE 0.98), and yet the two do not bind (held-out flip1
    0.46-0.56 = chance), with the LIE control proving the planted fact is not even CONSULTED
    (bias-independence +0.073 ~ 0). Every escape was measured shut. So: WHY does pretrained polarity
    bind to the operator while CPT-written polarity does not?

    Fable's reframe, which this instrument is built around: "the two polarities live in different
    places" already ASSUMES the CPT polarity exists as a FEATURE. WRITE 0.98 does not show that — it
    shows a REFLEX (stem->answer inside the flip0 carrier). So there are three worlds, not two:

      P-place  the feature exists but not where the operator reads   -> write it there and it binds
      P-kind   there is no feature at all; CPT wrote a shortcut      -> the fix is the CORPUS, not the address
      S        the feature is right there, readable, consumable, and the operator STILL ignores it
               -> binding is not content-lookup; it is forged during pretraining (XBIND becomes law)

    A read-only probe map cannot separate these (what a probe reads != what the operator consumes —
    the read-side-exhausted lesson). Only a CAUSAL write can, so the DV comes from an intervention:

      Stage A (POSITIVE CONTROL, truth known — we plant it)
        On SEEN stems only, swap-patch the stem span's hidden with a SEEN donor of opposite polarity
        at depth l, scanning l = 0..L and a frozen span ladder (last byte -> last 3 -> whole stem).
        l* := the SHALLOWEST depth whose swap flips the answer >= G_A_SWAP with sham <= G_A_SHAM.
        No DV data touches this choice (SEEN only), so it is calibration, not tune-to-green.
        Nothing passes  -> INVALID-LOCALIZATION (the operator's read is not localized to the stem
        span; that is itself a locus fact, and P/S stays unjudged rather than falsely decided).

      Stage B (axis + magnitude, matched on the MEDIATING covariate)
        v = unit(mean(SEEN pos) - mean(SEEN neg)) at l*; targets mu+/mu- = the SEEN class means of
        the projection onto v. Injection is projection-MATCH (mode "proj"), not a fixed alpha: a
        fixed alpha leaves the realized projection different per arm, which is exactly the confound
        `control-must-match-mediating-covariate` was earned on. Realized projections are reported.

      Stage C (arms; DV = bias-independent dependence, H_9327's LIE test in causal form)
        dep_f = P(ans=pos | inject=pos) - P(ans=pos | inject=neg), paired per stem, per flip layer f.
        A global answer bias cancels in the difference by construction.
          B  novel stems (0 occurrences in pretrain AND in CPT) <- the core arm
          C  held-out (CPT-written) stems, injected with their OWN planted polarity  <- rescue arm
          D  novel stems, random direction orthogonal to v, same displacement  <- off-manifold control
          E  novel stems, self-patch (own value)                               <- sham; instrument must be inert

    Frozen decision tree (pre-registered; bars never move):
      V1  Stage A found l*                                    else INVALID-LOCALIZATION
      V2  B-arm flip0 dep0 >= G_V2   (the injection is consumed by the readout at all)
                                                              else INVALID-DEAD-INJECTION
      V3  D-arm |dep| <= G_V3 and E-arm change-rate <= G_E    else INVALID-INSTRUMENT
      --- only if V1 & V2 & V3 ---
      DV  B-arm flip1 dep1 <= G_DV_P                          -> P   (operator consumes site content:
                                                                      the wall is an address/kind problem)
          |dep1| <= G_TOST (TOST equivalence)                 -> S   (same site, consumable content,
                                                                      still no bind = substrate fact)
          otherwise                                           -> UNDERPOWERED (report se; raise n; no bar moves)

    Two CPT seeds must agree in SIGN before any tier is cemented (H_9327's own cementing rule).

    Manifest: {"win":24, "carrier":"이 영화 {stem}고 => ",
               "items":[{id, stem, stem_byte_span:[t0,t1), pol, flip, split, arm}]}
    where `split` in {seen, heldout, novel} and `flip` in {0,1} (0 = plain carrier, 1 = negated).
    Read-only w.r.t. weights; every forward is the production forward (a_experiment_engine_native).
    """
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--bind-locus", "")))
    out_path = evaluate_strval(argv[1:], "--out", "bind_locus.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 24)))
    n_perm = evaluate_intval(argv[1:], "--perm", 200)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]
    carrier = spec.get("carrier", "이 영화 {stem}고 => ")

    # frozen bars (Fable pre-registration · never moved post-hoc · p7)
    G_A_SWAP, G_A_SHAM = 0.75, 0.15
    G_V2, G_V3, G_E = 0.50, 0.15, 0.05
    G_DV_P, G_TOST = -0.50, 0.20

    print("=== anima evaluate --bind-locus — H_9331: why does the CPT-written polarity not bind? ===")
    print("  ckpt " + ckpt + " · win " + str(T) + "B · " + str(len(items)) + " items · perm " + str(n_perm))
    print("  frozen bars: V1 swap>=%.2f sham<=%.2f · V2 dep0>=%.2f · V3 |dep_rand|<=%.2f sham<=%.2f"
          % (G_A_SWAP, G_A_SHAM, G_V2, G_V3, G_E))
    print("  frozen DV  : P if dep1<=%.2f · S if TOST(+-%.2f) · else UNDERPOWERED" % (G_DV_P, G_TOST))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    L = int(W["L"])

    _tap_cache = {}

    def taps_of(text):
        """Memoized per-prompt tap read. The scan asks for the same donor's taps once per
        (item, depth, rung); recomputing the forward each time made the scan quadratic and the
        instrument unrunnable. The cached value is the SAME production forward, so this is a
        speed fix with zero numeric effect (byte-identical by construction)."""
        h = _tap_cache.get(text)
        if h is None:
            h = clm.clm_forward_taps(W, clm._seed_to_tok(text, T), T)
            _tap_cache[text] = h
        return h

    def prompt_of(it, flip=None):
        """The prompt is taken VERBATIM from the manifest (`seed`), never reconstructed.

        H_9327's negation surfaces are `negL` ("이 영화 빠르지 않다 => ") and `negS`
        ("이 영화 안 빠르고 => ") — two different carriers, one of them PREFIXING the negator.
        Rebuilding a carrier from a template would have fed the model a string it was never
        trained on ("빠르지 않고"), and the operator would look dead for a reason that is purely
        ours (reference-match: when the reference is open, read it — do not re-derive it)."""
        return it["seed"]

    def span_of(it, flip=None):
        """Byte span of the stem inside the RIGHT-ALIGNED T-window the engine actually decodes.

        Located by BYTE search inside the verbatim prompt (a_korean_byte_budget: Korean is 3
        bytes/char, and every window/length knob here is a byte budget — mixing chars into it is
        how three prior H's died). rfind, because `negS` puts the negator BEFORE the stem, so the
        stem is still the last occurrence of its own bytes."""
        p = prompt_of(it).encode("utf-8", "surrogateescape")
        sb = it["stem"].encode("utf-8", "surrogateescape")
        t0_abs = p.rfind(sb)
        if t0_abs < 0:
            return None                        # stem not in its own prompt — manifest defect
        t1_abs = t0_abs + len(sb)
        off = T - len(p)                       # right-align: byte i of p sits at window i+off
        t0, t1 = t0_abs + off, t1_abs + off
        if t0 < 0:
            return None                        # stem fell out of the T-byte window — unusable
        return (t0, t1)

    def pool(split, flip):
        return [it for it in items if it.get("split") == split and int(it["flip"]) == flip]

    seen = [it for it in items if it.get("split") == "seen" and int(it["flip"]) == 1]
    novel = [it for it in items if it.get("split") == "novel"]
    heldout = [it for it in items if it.get("split") == "heldout"]
    print("  splits: seen %d · heldout %d · novel %d" % (len(seen), len(heldout), len(novel)))
    if not seen:
        print("BIND-LOCUS ⏳ INVALID-NO-SEEN — Stage A needs SEEN stems (the positive control)")
        json.dump({"verdict": "INVALID-NO-SEEN"}, open(out_path, "w"))
        return 0

    # ── Stage A — locate the operator's read site with a SPIKE-IN (truth we planted) ──────────
    def stem_ladder(it, depth):
        t = span_of(it)
        if t is None:
            return []
        t0, t1 = t
        out = []
        if t1 - 1 >= t0:
            out.append((t1 - 1, t1))                       # last byte
        if t1 - 3 >= t0:
            out.append((t1 - 3, t1))                       # last 3 bytes
        out.append((t0, t1))                               # whole stem
        return out

    pos_seen = [it for it in seen if int(it["pol"]) == 1]
    neg_seen = [it for it in seen if int(it["pol"]) == 0]
    print("\n[Stage A] read-site scan — SEEN swap-patch (positive control · truth known)")
    print("  depth x span-rung -> swap-flip-rate (bar %.2f) / sham (bar %.2f)" % (G_A_SWAP, G_A_SHAM))
    lstar = None
    a_rows = []
    for depth in range(L + 1):
        for rung in range(3):
            flips, shams, n = 0, 0, 0
            for it in pos_seen[:40]:
                sp = stem_ladder(it, depth)
                if rung >= len(sp):
                    continue
                t0, t1 = sp[rung]
                donors = [d for d in neg_seen if span_of(d) is not None]
                if not donors:
                    continue
                dn = donors[n % len(donors)]
                dsp = stem_ladder(dn, depth)
                if rung >= len(dsp):
                    continue
                d0, d1 = dsp[rung]
                if (d1 - d0) != (t1 - t0):
                    continue                                # byte-length mismatch — skip, never pad
                p_self = prompt_of(it)
                donor_h = taps_of(prompt_of(dn))[depth][d0:d1]
                base = _bl_answer_pos(np, W, p_self, T)
                got = _bl_answer_pos_edited(np, W, p_self, T,
                                            [{"layer": depth, "t0": t0, "t1": t1,
                                              "mode": "patch", "donor": donor_h}])
                sham = _bl_answer_pos_edited(np, W, p_self, T,
                                             [{"layer": depth, "t0": t0, "t1": t1,
                                               "mode": "patch", "donor": taps_of(p_self)[depth][t0:t1]}])
                flips += 1 if got != base else 0
                shams += 1 if sham != base else 0
                n += 1
            if n == 0:
                continue
            fr, sr = flips / n, shams / n
            a_rows.append({"depth": depth, "rung": rung, "n": n, "swap": fr, "sham": sr})
            print("  depth %2d rung %d  n=%2d  swap=%.3f  sham=%.3f%s"
                  % (depth, rung, n, fr, sr,
                     "   <- l*" if (lstar is None and fr >= G_A_SWAP and sr <= G_A_SHAM) else ""))
            if lstar is None and fr >= G_A_SWAP and sr <= G_A_SHAM:
                lstar = (depth, rung)
    if lstar is None:
        print("\nBIND-LOCUS ⏳ INVALID-LOCALIZATION — no (depth, span) where a SEEN swap flips the")
        print("  answer >= %.2f with sham <= %.2f. The operator's read is NOT localized to the stem" % (G_A_SWAP, G_A_SHAM))
        print("  span, so an injection there could not test P vs S. This is a locus FACT, not a")
        print("  failed run — and it forbids the P/S verdict rather than faking one.")
        json.dump({"verdict": "INVALID-LOCALIZATION", "stageA": a_rows,
                   "bars": {"swap": G_A_SWAP, "sham": G_A_SHAM}}, open(out_path, "w"), ensure_ascii=False)
        return 0
    depth, rung = lstar
    print("  l* FROZEN = depth %d, span-rung %d (chosen on SEEN only — no DV data touched it)" % (depth, rung))

    # ── Stage B — axis + projection targets from SEEN (matched on the mediating covariate) ────
    def stem_vec(it):
        sp = stem_ladder(it, depth)
        if rung >= len(sp):
            return None
        t0, t1 = sp[rung]
        return taps_of(prompt_of(it))[depth][t0:t1].mean(axis=0), (t0, t1)

    P = [stem_vec(it) for it in pos_seen]
    N = [stem_vec(it) for it in neg_seen]
    P = [x for x in P if x]; N = [x for x in N if x]
    mu_p = np.mean([x[0] for x in P], axis=0)
    mu_n = np.mean([x[0] for x in N], axis=0)
    v = mu_p - mu_n
    nv = float(np.linalg.norm(v))
    if nv < 1e-12:
        print("BIND-LOCUS ⏳ INVALID-NO-AXIS — SEEN class means coincide at l*")
        json.dump({"verdict": "INVALID-NO-AXIS"}, open(out_path, "w"))
        return 0
    v = v / nv
    tgt_p = float(np.mean([x[0] @ v for x in P]))
    tgt_n = float(np.mean([x[0] @ v for x in N]))
    print("\n[Stage B] axis v = unit(mean_SEEN_pos - mean_SEEN_neg) at l*=%d · |v| pre-norm %.4f" % (depth, nv))
    print("  projection targets (SEEN class means on v): mu+ = %+.4f · mu- = %+.4f" % (tgt_p, tgt_n))
    print("  injection = projection-MATCH to these values (not a fixed alpha — arms are matched on")
    print("  the mediating covariate, control-must-match-mediating-covariate)")

    rng = np.random.RandomState(seed)
    vr = rng.randn(len(v)); vr -= (vr @ v) * v; vr /= (np.linalg.norm(vr) + 1e-12)   # orthogonal to v

    def dep_for(items_pool, flip, mode):
        """Bias-independent dependence: P(ans=pos | inject=pos) - P(ans=pos | inject=neg), paired
        per stem. A global answer bias cancels in the difference by construction (this is H_9327's
        LIE test, now causal)."""
        d, det = [], []
        for it in items_pool:
            if int(it["flip"]) != int(flip):
                continue
            sp = stem_ladder(it, depth)
            if rung >= len(sp):
                continue
            t0, t1 = sp[rung]
            p = prompt_of(it)
            if mode == "sham":
                b = _bl_answer_pos(np, W, p, T)
                s = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                         "mode": "patch", "donor": taps_of(p)[depth][t0:t1]}])
                d.append(1.0 if s != b else 0.0)
                continue
            axis = v if mode == "v" else vr
            a_p = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                      "mode": "proj", "vec": axis, "target": tgt_p}])
            a_n = _bl_answer_pos_edited(np, W, p, T, [{"layer": depth, "t0": t0, "t1": t1,
                                                      "mode": "proj", "vec": axis, "target": tgt_n}])
            d.append(a_p - a_n)
            det.append({"id": it.get("id"), "inj_pos": a_p, "inj_neg": a_n})
        return d, det

    def summ(d):
        if not d:
            return {"n": 0, "dep": float("nan"), "se": float("nan")}
        a = np.asarray(d, dtype=np.float64)
        n = len(a)
        se = float(a.std(ddof=1) / math.sqrt(n)) if n > 1 else float("nan")
        return {"n": n, "dep": float(a.mean()), "se": se}

    print("\n[Stage C] arms (DV = bias-independent dependence · paired per stem)")
    res = {}
    for name, pool, flip, mode in (
            ("B_novel_flip0", novel, 0, "v"),
            ("B_novel_flip1", novel, 1, "v"),
            ("C_rescue_flip1", heldout, 1, "v"),
            ("D_randdir_flip1", novel, 1, "rand"),
            ("E_sham_flip1", novel, 1, "sham")):
        d, _ = dep_for(pool, flip, mode)
        res[name] = summ(d)
        print("  %-16s n=%3d  dep=%+.4f  se=%.4f" % (name, res[name]["n"], res[name]["dep"], res[name]["se"]))

    # ── frozen decision tree ─────────────────────────────────────────────────────────────────
    dep0 = res["B_novel_flip0"]["dep"]; dep1 = res["B_novel_flip1"]["dep"]
    dr = res["D_randdir_flip1"]["dep"]; sh = res["E_sham_flip1"]["dep"]
    se1 = res["B_novel_flip1"]["se"]
    print("\n[verdict] V1 l*=(%d,%d) ✅ · V2 dep0=%+.4f (bar >=%.2f) · V3 |dep_rand|=%.4f (<=%.2f) sham=%.4f (<=%.2f)"
          % (depth, rung, dep0, G_V2, abs(dr), G_V3, sh, G_E))
    if not (dep0 >= G_V2):
        verdict = "INVALID-DEAD-INJECTION"
        why = ("the injection is not consumed even by the flip0 readout (dep0 %+.4f < %.2f) — this is "
               "'we cannot find it', NOT 'it is not there'" % (dep0, G_V2))
    elif not (abs(dr) <= G_V3 and sh <= G_E):
        verdict = "INVALID-INSTRUMENT"
        why = ("a control moved: random-direction |dep|=%.4f (bar %.2f) / sham=%.4f (bar %.2f) — the "
               "edit machinery itself perturbs the answer, so no DV may be read"
               % (abs(dr), G_V3, sh, G_E))
    elif dep1 <= G_DV_P:
        verdict = "P — OPERATOR CONSUMES SITE CONTENT"
        why = ("dep1 %+.4f <= %.2f: write the polarity where the operator reads and the answer flips "
               "with it ⇒ the H_9327 wall is an ADDRESS/KIND problem, not a substrate one. "
               "C-rescue dep=%+.4f says whether the CPT stems are repairable in place."
               % (dep1, G_DV_P, res["C_rescue_flip1"]["dep"]))
    elif (not math.isnan(se1)) and abs(dep1) + 1.96 * se1 <= G_TOST:
        verdict = "S — SUBSTRATE (binding is not content-lookup)"
        why = ("dep1 %+.4f is TOST-equivalent to 0 within +-%.2f (|dep|+1.96se = %.4f): the content is "
               "AT the operator's own read site, demonstrably consumable (dep0 %+.4f), and the operator "
               "STILL ignores it ⇒ binding is forged in pretraining, not looked up at inference "
               "(H_9267 XBIND becomes law)." % (dep1, G_TOST, abs(dep1) + 1.96 * se1, dep0))
    else:
        verdict = "UNDERPOWERED"
        why = ("dep1 %+.4f (se %.4f) sits between the P bar (%.2f) and the TOST margin (+-%.2f) — n must "
               "rise; no bar moves (power-before-negative-verdict)" % (dep1, se1, G_DV_P, G_TOST))
    print("\nBIND-LOCUS %s" % verdict)
    print("  %s" % why)
    json.dump({"verdict": verdict, "why": why, "lstar": {"depth": depth, "rung": rung},
               "stageA": a_rows, "targets": {"mu_pos": tgt_p, "mu_neg": tgt_n},
               "arms": res, "bars": {"V1_swap": G_A_SWAP, "V1_sham": G_A_SHAM, "V2": G_V2,
                                     "V3": G_V3, "E": G_E, "DV_P": G_DV_P, "TOST": G_TOST}},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def xbind_run(argv):
    """`anima-py evaluate <ckpt> --xbind <manifest.json>` — held-out XBIND recombination
    (G1 reopen lane a · card H_9267). Engine-native numpy core/decode.py only
    (a_eval_py_canonical -> TERMINAL-eligible). Design SSOT: state/g1_reopen_xbind/DESIGN_PREREG.md.
    PRIMARY D-acc = greedy(top_k=1) first-word == gold branch word, per split {heldout, seen}.
    C-rate = order-covariant portmanteau on gold-fuse held-out (constructive tier). MARGIN =
    teacher-forced NLL(counterfactual)-NLL(gold). All raw outputs dumped (never tail-truncate
    a control · evaluate-py-1). --arm ctrl scores the shuffle-control model."""
    import numpy as np
    import time
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--xbind", "")
    out_path = evaluate_strval(argv[1:], "--out", "xbind_eval.json")
    arm = evaluate_strval(argv[1:], "--arm", "main")
    spec = json.load(open(spec_path))
    gen = evaluate_intval(argv[1:], "--gen", int(spec.get("gen", 16)))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 200)
    n_smp = evaluate_intval(argv[1:], "--n-sampled", 40)

    # --consult (H_9309 DECON · A-channel): a declarative store {atom: {key, pol}} whose fact is
    # rendered into the CONTEXT of the 2AFC scoring window. It is the only structurally valid
    # injection point: free-generation D-acc cannot see it (clm_decode_topk_sampled_W hardcodes
    # T=24, core/decode.py:1094), so the primary instrument here is the margin-2AFC alone.
    # EMPTY store => byte-identical to a plain --xbind run (parity gate).
    consult_path = evaluate_strval(argv[1:], "--consult", "")
    consult_fmt = evaluate_strval(argv[1:], "--consult-format", "F1")
    store = json.load(open(consult_path)) if consult_path else {}

    print("=== anima evaluate --xbind — held-out XBIND recombination (G1 reopen lane a) ===")
    print("ckpt: " + ckpt + "  arm=" + arm + "  gen=%d win=%d" % (gen, T))
    if store:
        print("consult: %s  (%d facts · format=%s) — injected into the 2AFC context only"
              % (consult_path, len(store), consult_fmt))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    res = {"ckpt": ckpt, "arm": arm, "gen": gen, "win": T, "splits": {}}
    for split in ("heldout", "seen"):
        items = spec[split][:n_dec]
        t_split = time.time()
        rows = []
        d_hits = c_hits = c_n = 0
        margins = []
        # Stall watchdog. An eval that stops making progress must SAY so, not sit there.
        #
        # Measured (2026-07-14): a G-base run on a pool box hung at item 50 of 60 — eta 37 seconds —
        # and stayed there for forty minutes. No error, no exit, no output file. A neighbouring
        # session had saturated the host's RAM and wedged sshd, so the box was gone; but from the
        # orchestration side the run looked exactly like a slow one, and the only reason anyone found
        # out was that someone went and looked. Forty minutes of a rented clock, and the chain behind
        # it (two CPTs queued on that eval finishing) never started.
        #
        # A run that has completed items has told us how long an item takes. If one then takes
        # WATCHDOG_X times the median of the last few, the box is not slow — something has stopped.
        # Die loudly, with the numbers, so the caller can re-fire somewhere else in two minutes
        # instead of discovering the corpse in forty.
        WATCHDOG_X = 20.0
        WATCHDOG_FLOOR = 120.0          # never trip inside the first two minutes of a single item
        recent = []
        t_item = time.time()
        for ix, it in enumerate(items):
            gold_w = it["gold_word"]
            if arm == "ctrl" and split == "seen":
                gold_w = it["gold_word_ctrl"]
            o = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 1, 0.7, 7)["text"]
            fw = _xbind_first_word(o)
            d_hit = int(fw == gold_w)
            d_hits += d_hit
            c_hit = None
            if it.get("construct") and arm == "main":
                c_hit = int(it["construct"] in o)
                c_hits += c_hit
                c_n += 1
            seed_m, cused = _consult_seed(it["seed"], it, store, consult_fmt, T,
                                          it["gold"], it["counterfactual"])
            mg = (_xbind_cont_nll(np, clm, W, seed_m, it["counterfactual"], T)
                  - _xbind_cont_nll(np, clm, W, seed_m, it["gold"], T))
            margins.append(mg)
            smp = None
            if ix < n_smp:
                votes = 0
                for r in (7, 4302, 4303):
                    os_ = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 40, 0.7, r)["text"]
                    votes += int(_xbind_first_word(os_) == gold_w)
                smp = int(votes >= 2)
            rows.append({"a": it["a"], "b": it["b"], "gold_word": gold_w,
                         "first_word": fw, "d_hit": d_hit, "c_hit": c_hit,
                         "margin": mg, "sampled_maj": smp, "raw": o,
                         "consult": cused,
                         # carried through so the summary can split the headline (_xbind_breakdown)
                         "flip": it.get("flip"), "pol": it.get("pol")})
            # Heartbeat at item 1, then every 25. The first item is what makes a slow host
            # legible: each item is ~10 model forwards, so on a saturated shared box one item
            # can cost minutes — and a 25-item-only cadence then means HOURS of total silence,
            # indistinguishable from a hang. (2026-07-13: a 174-item run on a rented box whose
            # load average sat at ~106 from other tenants emitted nothing for 5h; the only way
            # to tell "slow" from "stuck" was to hand-roll a 2-item manifest. The ETA below
            # would have said "35h on this host" after ~30 seconds.)
            dt = time.time() - t_item
            t_item = time.time()
            if recent:
                med = sorted(recent)[len(recent) // 2]
                limit = max(WATCHDOG_FLOOR, WATCHDOG_X * med)
                if dt > limit:
                    sys.exit(
                        "\nanima-py evaluate: STALLED — item %d/%d of split '%s' took %.0fs.\n"
                        "  the last %d items ran at a median of %.1fs each; the limit is %.0fs "
                        "(%.0fx median).\n"
                        "  This is not a slow box, it is a stopped one. The usual cause is the HOST\n"
                        "  going away underneath us — a neighbouring job saturating RAM, an OOM\n"
                        "  reaper, a wedged sshd. Nothing that follows would have been measured.\n\n"
                        "  Check the host (uptime, free, nvidia-smi, who else is on it), then re-fire\n"
                        "  somewhere that is not carrying someone else's load.\n"
                        % (ix + 1, len(items), split, dt, len(recent), med, limit, WATCHDOG_X))
            recent.append(dt)
            recent = recent[-9:]
            if ix == 0 or (ix + 1) % 25 == 0:
                el = time.time() - t_split
                per = el / (ix + 1)
                eta = per * (len(items) - ix - 1)
                print("  [xbind %s #%d/%d] d_acc=%.3f  %.1fs/item  elapsed=%s  eta=%s" %
                      (split, ix + 1, len(items), d_hits / (ix + 1), per,
                       _xbind_hms(el), _xbind_hms(eta)), flush=True)
        margins.sort()
        med = margins[len(margins) // 2] if margins else 0.0
        smp_rows = [r["sampled_maj"] for r in rows if r["sampled_maj"] is not None]
        summ = {"n": len(items), "d_acc": d_hits / max(1, len(items)),
                "c_rate": (c_hits / c_n) if c_n else None, "c_n": c_n,
                "margin_median": med,
                "margin_frac_pos": sum(1 for m in margins if m > 0) / max(1, len(margins)),
                "sampled_maj_acc": (sum(smp_rows) / len(smp_rows)) if smp_rows else None}
        if store:
            # byte-audit (a_korean_byte_budget): a Korean prefix is 3B/char and the window is a
            # BYTE budget, so an overflowing trial silently loses the fact's leading bytes and
            # then reads as "the model did not consume it". Surface the tally INLINE — a run with
            # any DROPPED trial is INVALID-INSTRUMENT, not a negative result.
            cu = [r["consult"] for r in rows]
            summ["consult_used"] = sum(1 for c in cu if c == consult_fmt)
            summ["consult_downgraded"] = sum(1 for c in cu if c == "F2-downgrade")
            summ["consult_dropped"] = sum(1 for c in cu if c == "DROPPED-overflow")
            summ["consult_absent"] = sum(1 for c in cu if c is None)
            print("  byte-audit %s: used=%d downgraded=%d DROPPED=%d absent=%d" %
                  (split, summ["consult_used"], summ["consult_downgraded"],
                   summ["consult_dropped"], summ["consult_absent"]), flush=True)
        summ["breakdown"] = _xbind_breakdown(rows)
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (evaluate-py-1: never tail-truncatable)
        print("  xbind %s  arm=%s  D-acc=%.4f  C-rate=%s  margin_med=%.3f  "
              "margin_pos=%.3f  sampled=%s  n=%d" %
              (split, arm, summ["d_acc"], str(summ["c_rate"]), med,
               summ["margin_frac_pos"], str(summ["sampled_maj_acc"]), summ["n"]),
              flush=True)
        bd = summ["breakdown"]
        if "class" in bd:
            print("  by-class %s: %s   majority-baseline=%.3f%s" %
                  (split,
                   "  ".join("%s=%.3f(n=%d)" % (k, v["acc"], v["n"])
                             for k, v in bd["class"].items()),
                   bd["majority_baseline"],
                   ("   ⚠️ COLLAPSE — weakest class %.3f <= chance: the headline is riding the "
                    "label prior, NOT the stem" % bd["weakest_class_acc"])
                   if bd["collapse"] else ""), flush=True)
        for k, v in bd.get("flip", {}).items():
            cw = min(c["acc"] for c in v["class"].values()) if v["class"] else 1.0
            print("  by-flip %s  flip%s=%.4f(n=%d)  [%s]%s   (flip0 = is the fact in the "
                  "weights · flip1 = is the operator applied to it)" %
                  (split, k, v["acc"], v["n"],
                   "  ".join("%s=%.3f" % (c, s["acc"]) for c, s in v["class"].items()),
                   "  ⚠️ COLLAPSE" if cw <= 0.5 else ""), flush=True)
    json.dump(_json_safe(res), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"out": out_path,
                      "heldout_d_acc": res["splits"]["heldout"]["summary"]["d_acc"],
                      "seen_d_acc": res["splits"]["seen"]["summary"]["d_acc"]}))
    return 0


def _xfan_parse(o):
    """Parse the first '<slot>, <member>.' emission from a decode → (slot, member) or (None, None).
    slot = last token before the comma; member = first token after it."""
    seg = o.strip().split(".")[0]
    if ", " not in seg:
        return None, None
    sl, mb = seg.split(", ", 1)
    sl = sl.strip().split()[-1] if sl.strip().split() else ""
    mb = mb.strip().split()[0] if mb.strip().split() else ""
    return (sl or None), mb


def xfan_run(argv):
    """`anima-py evaluate <ckpt> --xfan <manifest.json>` — held-out XFAN one-to-many fan
    (G6 / ρ·fan reopen lane · card H_9271). Engine-native numpy core/decode.py only
    (a_eval_py_canonical → TERMINAL-eligible). Design SSOT: state/g6_reopen_xfan/DESIGN_PREREG.md.
    PRIMARY coverage C = |correct unique (slot,member)| / n_slots over n_smp sampled decodes per
    concept (top_k=40 temp=0.7 · seed 7+17j). valid/spurious split (genius⊥honesty); per-slot-kind
    (unary vs joint) breakout; greedy-collapse control (top_k=1 distinct); MARGIN = teacher-forced
    NLL(foil)-NLL(gold) per slot (H_1440 mode-collapse discriminator). --arm ctrl scores the shuffle
    model. All raw dumped (never tail-truncate a control · evaluate-py-1)."""
    import numpy as np
    ckpt = argv[0]
    spec_path = evaluate_strval(argv[1:], "--xfan", "")
    out_path = evaluate_strval(argv[1:], "--out", "xfan_eval.json")
    arm = evaluate_strval(argv[1:], "--arm", "main")
    spec = json.load(open(spec_path))
    gen = evaluate_intval(argv[1:], "--gen", int(spec.get("gen", 16)))
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_dec = evaluate_intval(argv[1:], "--n-decode", 80)
    n_smp = evaluate_intval(argv[1:], "--n-sampled", 16)
    K = int(spec.get("n_slots", 5))

    print("=== anima evaluate --xfan — held-out XFAN one-to-many fan (G6 reopen lane) ===")
    print("ckpt: " + ckpt + "  arm=" + arm + "  gen=%d win=%d n_smp=%d K=%d" % (gen, T, n_smp, K))
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable (clm): " + ckpt)
        return 1

    res = {"ckpt": ckpt, "arm": arm, "gen": gen, "win": T, "n_slots": K, "splits": {}}
    for split in ("heldout", "seen"):
        items = spec[split][:n_dec]
        rows = []
        cov_sum = 0.0
        valid_sum = valid_n = spur_sum = greedy_distinct_sum = 0
        cov_by_kind = {"unary": [], "joint": []}
        margins = []
        for ix, it in enumerate(items):
            gold = it["gold"]
            if arm == "ctrl" and split == "seen" and it.get("gold_ctrl"):
                gold = it["gold_ctrl"]
            gold_pairs = set((g["slot"], g["member"]) for g in gold)
            gold_by_slot = {g["slot"]: g["member"] for g in gold}
            slot_kind = it.get("slot_kind", {})
            emitted = []
            for j in range(n_smp):
                o = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 40, 0.7, 7 + 17 * j)["text"]
                sl, mb = _xfan_parse(o)
                if sl is not None:
                    emitted.append((sl, mb))
            hit_pairs = set(e for e in emitted if e in gold_pairs)
            cov = len(hit_pairs) / max(1, K)
            cov_sum += cov
            for (sl, mb) in emitted:
                if sl in gold_by_slot:
                    valid_n += 1
                    if (sl, mb) in gold_pairs:
                        valid_sum += 1
                    else:
                        spur_sum += 1          # right slot, wrong member = fabrication
            for kind, keys in (("unary", ("a", "b")), ("joint", ("j",))):
                slots_k = [s for s, kd in slot_kind.items() if kd in keys]
                if slots_k:
                    hit_k = len(set((s, m) for (s, m) in hit_pairs if s in slots_k))
                    cov_by_kind[kind].append(hit_k / len(slots_k))
            gd = set()
            for j in range(min(n_smp, 8)):
                og = clm.clm_decode_topk_sampled_W(W, it["seed"], gen, 1, 0.7, 7 + 17 * j)["text"]
                sl, mb = _xfan_parse(og)
                if sl is not None:
                    gd.add((sl, mb))
            greedy_distinct_sum += len(gd)
            row_mg = []
            for g in gold:
                s = g["slot"]; gm = g["member"]; fm = it.get("foils", {}).get(s, gm)
                mg = (_xbind_cont_nll(np, clm, W, it["seed"], s + ", " + fm + ".", T)
                      - _xbind_cont_nll(np, clm, W, it["seed"], s + ", " + gm + ".", T))
                row_mg.append(mg); margins.append(mg)
            rows.append({"concept": it["concept"], "cov": cov, "emitted": emitted[:8],
                         "n_emit": len(emitted), "greedy_distinct": len(gd), "margin": row_mg})
            if (ix + 1) % 20 == 0:
                print("  [xfan %s #%d/%d] mean_C=%.3f" %
                      (split, ix + 1, len(items), cov_sum / (ix + 1)), flush=True)
        n = len(items)
        margins.sort()
        med = margins[len(margins) // 2] if margins else 0.0
        summ = {"n": n, "coverage_C": cov_sum / max(1, n),
                "valid_rate": (valid_sum / valid_n) if valid_n else None,
                "spurious_rate": (spur_sum / valid_n) if valid_n else None,
                "coverage_unary": (sum(cov_by_kind["unary"]) / len(cov_by_kind["unary"]))
                if cov_by_kind["unary"] else None,
                "coverage_joint": (sum(cov_by_kind["joint"]) / len(cov_by_kind["joint"]))
                if cov_by_kind["joint"] else None,
                "greedy_distinct_mean": greedy_distinct_sum / max(1, n),
                "margin_median": med,
                "margin_frac_pos": sum(1 for m in margins if m > 0) / max(1, len(margins))}
        res["splits"][split] = {"summary": summ, "rows": rows}
        # verdict numerics INLINE (evaluate-py-1: never tail-truncatable)
        print("  xfan %s  arm=%s  C=%.4f  valid=%s  spurious=%s  C_unary=%s  C_joint=%s  "
              "greedy_distinct=%.2f  margin_med=%.3f  margin_pos=%.3f  n=%d" %
              (split, arm, summ["coverage_C"], str(summ["valid_rate"]), str(summ["spurious_rate"]),
               str(summ["coverage_unary"]), str(summ["coverage_joint"]),
               summ["greedy_distinct_mean"], med, summ["margin_frac_pos"], n), flush=True)
    json.dump(_json_safe(res), open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps({"out": out_path,
                      "heldout_C": res["splits"]["heldout"]["summary"]["coverage_C"],
                      "seen_C": res["splits"]["seen"]["summary"]["coverage_C"]}))
    return 0


# Every flag evaluate actually consumes. An argv token starting with "--" that is not
# here is REJECTED (see _reject_unknown_flags): evaluate parses argv by scanning for the
# flags it knows, so an unknown one (a typo, or a flag that only exists in a sub-mode) is
# otherwise silently ignored — the run completes rc=0 and the result file the caller asked
# for is never written. That is unrecoverable on a paid GPU battery: a 13h x 4-run NBIND
# ladder would burn its rent and harvest nothing, with a green exit code. Fail closed.
def _im_rows(paths):
    """Load decision-trace rows (skip the _meta header). One row per tick."""
    out = []
    for p in paths:
        for line in open(p, "r", encoding="utf-8", errors="surrogateescape"):
            if not line.strip():
                continue
            d = json.loads(line)
            if d.get("_meta"):
                continue
            d["_src"] = p
            out.append(d)
    return out


def _im_H(xs):
    """Plug-in entropy (nats) of a discrete sample."""
    n = len(xs)
    if n == 0:
        return 0.0
    c = {}
    for x in xs:
        c[x] = c.get(x, 0) + 1
    h = 0.0
    for v in c.values():
        p = float(v) / n
        h -= p * math.log(p)
    return h


def _im_cmi(A, Y, S):
    """I(A;Y|S) = Σ_s p(s)·[H(A|s) + H(Y|s) − H(A,Y|s)], Miller–Madow corrected per stratum.
    MM adds (support−1)/(2n) — the plug-in estimator is biased UP, and that bias is exactly
    what manufactures a false positive on a thin channel (convergence decode-py-2)."""
    n = len(S)
    if n == 0:
        return 0.0
    strata = {}
    for i in range(n):
        strata.setdefault(S[i], []).append(i)
    tot = 0.0
    for s, idx in strata.items():
        m = len(idx)
        a = [A[i] for i in idx]
        y = [Y[i] for i in idx]
        ay = [(A[i], Y[i]) for i in idx]
        ha, hy, hay = _im_H(a), _im_H(y), _im_H(ay)
        mm = (len(set(a)) - 1 + len(set(y)) - 1 - (len(set(ay)) - 1)) / (2.0 * m) if m > 0 else 0.0
        tot += (float(m) / n) * max(0.0, ha + hy - hay + mm)
    return tot


def _im_hA_given_S(A, S):
    """V-CEILING: H(A|S). I <= this by identity — if it is ~0 the DV is UNDEFINED on this
    log, not zero-by-measurement. That distinction is what H_9308 got wrong."""
    n = len(S)
    if n == 0:
        return 0.0
    strata = {}
    for i in range(n):
        strata.setdefault(S[i], []).append(i)
    return sum((float(len(idx)) / n) * _im_H([A[i] for i in idx]) for idx in strata.values())


def _interact_mi(argv):
    """H_9328 — I(A;Y|S) over daemon decision traces. Reads only; no decode.

    A = a_fold8 (the H_9257 FROZEN 8-bucket axis the daemon actually consumes on emit)
    S = stage (the gate's own conditioning; conditioning on it makes A ⟂ everything-else|S
        by construction, so the S-lite omitted-confounder false positive cannot recur)
    Y = score_{t+1} binarised at a FROZEN median passed in via --seed <median×1e6>, or the
        in-sample median when absent (reported as such — an in-sample split is a diagnostic,
        never a headline).
    """
    paths = []
    perm = 200
    mde = 0.010
    hfloor = 0.030
    for a in argv:
        if a.startswith("--"):
            continue
        paths.append(a)
    rows = _im_rows(paths)
    emits = [r for r in rows if r.get("emit") and int(r.get("a_fold8", -1)) >= 0]
    print("═══ H_9328 INTERACT-MI · I(A;Y|S) ═══")
    print("  traces=%d  ticks=%d  emit-ticks(with A)=%d" % (len(paths), len(rows), len(emits)))
    if len(emits) < 30:
        print("  ⇒ NOT-POWERED (emit-ticks < 30) — 수집 증량 필요")
        return 0
    # Y = next-tick score, within the same trace file
    by_src = {}
    for r in rows:
        by_src.setdefault(r["_src"], []).append(r)
    nxt = {}
    for src, rs in by_src.items():
        rs.sort(key=lambda r: int(r["tick"]))
        for i in range(len(rs) - 1):
            nxt[(src, int(rs[i]["tick"]))] = float(rs[i + 1]["score"])
    use = [r for r in emits if (r["_src"], int(r["tick"])) in nxt]
    if len(use) < 30:
        print("  ⇒ NOT-POWERED (next-tick score 있는 emit-tick < 30)")
        return 0
    ys = sorted(nxt[(r["_src"], int(r["tick"]))] for r in use)
    med = ys[len(ys) // 2]
    A = [int(r["a_fold8"]) for r in use]
    S = [int(r["stage"]) for r in use]
    Y = [1 if nxt[(r["_src"], int(r["tick"]))] > med else 0 for r in use]
    # ── V-CEILING (BLOCKING · before any I is read) ────────────────────────────────
    hA = _im_hA_given_S(A, S)
    print("  🚦 V-CEILING  H(A|S) = %.4f nats   (floor %.3f = 3×MDE)" % (hA, hfloor))
    if hA < hfloor:
        print("  ⇒ NOT-POWERED — 행동 채널이 죽어 있다. I 는 정의상 0 이지 측정된 0 이 아니다.")
        print("     (H_9308 이 정확히 여기서 죽었다 · convergence interact-mi-py-1)")
        return 0
    I = _im_cmi(A, Y, S)
    # ── The exchangeable unit is MEASURED, not assumed (convergence evaluate-py-13 · chat-py-3).
    # Two candidate units, and which one is right is an empirical question about THIS trace set:
    #   ROLLOUT — correct when A is constant/strongly correlated within a session. That is what
    #     the FIRST H_9328 traces showed ({5:18} per rollout) — but that constancy turned out to
    #     be an INSTRUMENT DEFECT (a session-constant sampler seed made the mouth redraw the same
    #     80 bytes every tick, chat-py-3). It was not a fact about the substrate.
    #   TICK — correct when consecutive A's carry no autocorrelation, i.e. the previous tick does
    #     not predict the next. With the per-tick RNG stream fixed, that is what the data shows.
    # So we DECIDE FROM THE DATA and REPORT BOTH: if the verdict flips between units, the verdict
    # is about the unit, not the substrate, and the honest reading is INVALID.
    src_of = [r["_src"] for r in use]
    rollouts = sorted(set(src_of))
    n_roll = len(rollouts)
    # measured autocorrelation of A across consecutive ticks WITHIN a rollout
    by_src = {}
    for i, sc in enumerate(src_of):
        by_src.setdefault(sc, []).append(i)
    same = tot = 0
    for sc, idx in by_src.items():
        idx.sort(key=lambda i: int(use[i]["tick"]))
        for j in range(len(idx) - 1):
            tot += 1
            if A[idx[j]] == A[idx[j + 1]]:
                same += 1
    ca = {}
    for a in A:
        ca[a] = ca.get(a, 0) + 1
    chance_same = sum((v / len(A)) ** 2 for v in ca.values())
    obs_same = (float(same) / tot) if tot else 1.0
    autocorr = obs_same > chance_same * 1.25
    print("  단위 실측: 연속 tick 의 A 동일비율 %.3f vs 우연 %.3f ⇒ %s"
          % (obs_same, chance_same,
             "자기상관 O ⇒ **rollout** 이 표본" if autocorr else "자기상관 X ⇒ **tick** 이 표본"))
    print("  rollout=%d · emit-tick=%d" % (n_roll, len(use)))
    if n_roll < 8:
        print("  ⇒ NOT-POWERED (rollout < 8)")
        return 0

    rnd = random.Random(20260714)

    def _null(unit):
        """unit='rollout': block-permute the rollout→A map (ticks stay together).
           unit='tick'   : permute A within each S stratum."""
        out = []
        for _ in range(perm):
            if unit == "rollout":
                a_of = {}
                for i, sc in enumerate(src_of):
                    a_of.setdefault(sc, A[i])
                vals = [a_of[sc] for sc in rollouts]
                rnd.shuffle(vals)
                remap = {sc: vals[j] for j, sc in enumerate(rollouts)}
                Ap = [remap[sc] for sc in src_of]
            else:
                Ap = list(A)
                strata = {}
                for i, s in enumerate(S):
                    strata.setdefault(s, []).append(i)
                for idx in strata.values():
                    vals = [Ap[i] for i in idx]
                    rnd.shuffle(vals)
                    for j, i in enumerate(idx):
                        Ap[i] = vals[j]
            out.append(_im_cmi(Ap, Y, S))
        out.sort()
        return out

    print("  EXP   I(A;Y|S) = %.5f nats" % I)
    print("  Y-bin: in-sample median %.5f (진단용 · 헤드라인 아님)  n=%d" % (med, len(use)))
    verdicts = {}
    for unit in ("rollout", "tick"):
        null = _null(unit)
        nm = sum(null) / len(null)
        nsd = (sum((v - nm) ** 2 for v in null) / max(1, len(null) - 1)) ** 0.5
        pv = (sum(1 for v in null if v >= I) + 1.0) / (perm + 1.0)
        ef = I - nm
        tag = " ← 실측 단위" if (unit == "rollout") == autocorr else ""
        print("  C1 PERM[%-7s] null mean=%.5f sd=%.5f · perm-p=%.4f · EARNED=%.5f%s"
              % (unit, nm, nsd, pv, ef, tag))
        verdicts[unit] = (ef >= mde and pv < 0.005)
    eff_unit = "rollout" if autocorr else "tick"
    null = _null(eff_unit)
    nm = sum(null) / len(null)
    p = (sum(1 for v in null if v >= I) + 1.0) / (perm + 1.0)
    eff = I - nm
    print("  EARNED[%s] = %.5f nats   (MDE %.3f · TOST ±%.3f)" % (eff_unit, eff, mde, mde))
    if verdicts["rollout"] != verdicts["tick"]:
        print("  ⇒ ⛔ INVALID — 판정이 **단위 선택에 뒤집힌다**(rollout=%s · tick=%s)."
              % (verdicts["rollout"], verdicts["tick"]))
        print("     그 결론은 기질이 아니라 내 가정에 관한 것이다. 단위를 데이터로 못박기 전엔 못 읽는다.")
        return 0
    if eff >= mde and p < 0.005:
        print("  ⇒ 🟢 SIGNAL — 단 C2 CARRIER-SWAP 없이는 PASS 아님(내용맹 배제 불가)")
    elif abs(eff) <= mde:
        print("  ⇒ TOST 등가역 — 폐루프가 DATA-ADDITIVE 방향 (n·검정력 명시 필요)")
    else:
        print("  ⇒ 미달 · 판정 보류")
    return 0


_KNOWN_FLAGS = frozenset((
    "--arm", "--bind-locus", "--consult", "--consult-format", "--corpus", "--dump-hidden", "--earned", "--gen",
    "--help", "--ground-probe", "--interact-mi", "--interaction-lift", "--k-perm", "--kappa", "--kernel", "--kosmos", "--min-occ", "--null",
    "--n-decode", "--n-sampled", "--valence-audit",
    "--out", "--perm", "--probe", "--seed",
    "--result-file", "--rho-axon", "--score-len", "--seeds", "--selftest-rho-cells", "--slot-off",
    "--slot-shuffle", "--system-g1", "--win", "--with-logits", "--xbind", "--xfan",
))


def _reject_unknown_flags(argv):
    """Return an error string for the first unknown --flag in argv, else ''."""
    for a in argv:
        if not a.startswith("--") or a in _KNOWN_FLAGS:
            continue
        near = [k for k in sorted(_KNOWN_FLAGS)
                if k.lstrip("-").startswith(a.lstrip("-").split("-")[0])]
        msg = "evaluate: unknown flag " + a
        if near:
            msg += "  (did you mean: " + " ".join(near) + " ?)"
        return msg + "\n  known flags: " + " ".join(sorted(_KNOWN_FLAGS)) + \
            "\n  (an unknown flag is rejected, not ignored — a silently-dropped --out " \
            "loses the whole run's result with a green exit code)"
    return ""


def main(argv):
    if len(argv) >= 1 and argv[0] in ("-h", "--help"):
        evaluate_usage()
        return 0
    _bad = _reject_unknown_flags(argv)
    if _bad:
        print(_bad, file=sys.stderr, flush=True)
        return 2
    # H_9328 DO-MOUTH · I(A;Y|S) over decision traces (NO decode — reads traces the daemon
    # already wrote). V-CEILING FIRST: I <= H(A|S) is an identity, so a dead action channel
    # forces I=0 by definition, not by measurement (that is exactly how H_9308 died).
    if len(argv) >= 2 and argv[0] == "--interact-mi":
        return _interact_mi(argv[1:])
    # H_9212 ③ per-cell dispatch wiring self-test (torch-free · NO decode · internal subprocess)
    if len(argv) >= 1 and argv[0] == "--selftest-rho-cells":
        cok, cchecks = _selftest_rho_cells()
        for nm, v in cchecks:
            print(("  PASS " if v else "  FAIL ") + nm)
        try:
            import rho_fan as _rf
            rok = _rf._rho_fan_cells_selftest()
            for nm, v in rok["checks"]:
                print(("  PASS " if v else "  FAIL ") + "[rho_fan] " + nm)
            cok = cok and rok["ok"]
        except Exception as e:  # pragma: no cover
            print("  FAIL rho_fan cells selftest import: " + str(e))
            cok = False
        print("SELFTEST rho-cells: " + ("OK" if cok else "FAIL"))
        return 0 if cok else 1
    # --result-file <f>: write ALL output to <f> and keep fd 1 (stdout) silent. The hexa
    # launcher runs evaluate via exec(), whose captured stdout pipe it closes after ~150s
    # (probe-confirmed: a child reaching ~150s gets EPIPE on its next fd-1 write, but the
    # child itself is NOT killed). A 303M numpy decode runs for minutes; if it writes to
    # fd 1 it dies on BrokenPipe mid-battery. Redirecting our stdout to a file means fd 1
    # stays silent → the child survives the pipe close, finishes the full G0-G6 battery,
    # and the launcher cats <f> in a SECOND fresh exec (fast, well under the limit).
    # byte-faithful stdout: a real ckpt's greedy decode can emit non-utf8 bytes (held as
    # surrogateescape str), so any raw-continuation dump (--probe/--dump-hidden) prints a
    # surrogate-bearing str. A strict stdout would UnicodeEncodeError-crash mid-battery →
    # a spurious infra failure on the TERMINAL verdict path. Mirror hexa's byte-native
    # stdout by tolerating surrogates (clean text is byte-identical). convergence engine-cli-py-1.
    if "--result-file" in argv:
        i = argv.index("--result-file")
        f = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
        sys.stdout = open(f, "w", buffering=1, encoding="utf-8", errors="surrogateescape")
    else:
        try:
            sys.stdout.reconfigure(errors="surrogateescape")
        except (AttributeError, ValueError):
            pass
    try:
        sys.stderr.reconfigure(errors="surrogateescape")
    except (AttributeError, ValueError):
        pass
    # H_9200 ρ-AXON — reach-layer panel (G0-G6 → ρ-AXON, cli/rho_axon.py). Strip + set
    # the process-global so evaluate_run renders the ρ-AXON panel instead of G0-G6.
    global _RHO_AXON
    if "--rho-axon" in argv:
        argv = [a for a in argv if a != "--rho-axon"]
        _RHO_AXON = True
    # H_9200 E1 — SLW gated-write forward-slot eval-time controls (strip + set the
    # process-global switches in core/decode; frozen-first, no retraining):
    #   --slot-off        force γ=0 => bit-exact base trunk (slot-ablation control)
    #   --slot-shuffle N  permute the WRITE address with seed N (shuffle-bind control)
    _slot_off = "--slot-off" in argv
    if _slot_off:
        argv = [a for a in argv if a != "--slot-off"]
    _slot_shuffle = None
    if "--slot-shuffle" in argv:
        i = argv.index("--slot-shuffle")
        _slot_shuffle = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if _slot_off or _slot_shuffle is not None:
        clm.set_slw_controls(gamma_override=(0.0 if _slot_off else None),
                             shuffle_seed=_slot_shuffle)
    # --system-g1: RECOMBINATION-RELOCATION pipe (card H_9035). Strip the flag and
    # route the remaining <ckpt> [--gen N] to the system-G1 harness.
    if "--system-g1" in argv:
        i = argv.index("--system-g1")
        argv = argv[:i] + argv[i + 1:]
        return system_g1_run(argv)
    # --ground-probe <manifest.json>: the NBIND-G grounding instrument, whole and engine-native
    # (answer point · taught carrier · V-LIVE positive control · flip-undone atom aggregation ·
    # atom-level power · permutation null). The five defects it fixes are in ground_probe_run.
    if "--ground-probe" in argv:
        return ground_probe_run(argv)
    # --valence-audit <manifest.json>: AUDIT-A — is the atom's polarity in the weights AT ALL
    # (read in its real corpus contexts), or is a probe just reading the sentiment neighbourhood?
    # The verdict is Delta = probe(atom) - probe(length-matched NEUTRAL swapped into the SAME
    # context), against a permutation null. Kills the O-channel fire before it burns GPU.
    if "--bind-locus" in argv:
        return bind_locus_run(argv)
    if "--valence-audit" in argv:
        return valence_audit_run(argv)
    # --dump-hidden <prompts.json>: read-only penultimate-hidden dump (ρ·weave / γ
    # binding-lane probe H_9235). argv[0]=ckpt; dump_hidden_run reads --dump-hidden/--out.
    if "--dump-hidden" in argv:
        return dump_hidden_run(argv)
    # --interaction-lift <manifest.json>: read-only engine-native joint interaction-lift
    # NLL surface (H_9255). argv[0]=ckpt; interaction_lift_run reads --interaction-lift/--out.
    if "--earned" in argv:
        import earned as _earned
        return _earned.earned_run(argv)
    if "--interaction-lift" in argv:
        return interaction_lift_run(argv)
    # --probe <spec.json>: matched-surface G1 probe (card H_6189). argv[0]=ckpt; probe_run
    # reads --probe/--gen from the tail. Greedy raw-continuation dump for offline scoring.
    if "--probe" in argv:
        return probe_run(argv)
    # --xbind <manifest.json>: held-out XBIND recombination (G1 reopen lane a · card H_9267).
    # argv[0]=ckpt; xbind_run reads --xbind/--out/--arm from the tail. Engine-native greedy
    # D-acc on held-out xor(pol_a,pol_b) pairs (the corpus×task-class measure-swap exit).
    if "--xbind" in argv:
        return xbind_run(argv)
    # --xfan <manifest.json>: held-out XFAN one-to-many fan (G6 reopen lane · card H_9271).
    # coverage C over K sampled decodes per held-out concept (the corpus×task-class one-to-many
    # measure — the G6 homolog of XBIND's 1-bit discrimination).
    if "--xfan" in argv:
        return xfan_run(argv)
    return evaluate_run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
