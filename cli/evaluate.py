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
    print("  anima evaluate <ckpt> --route-audit <manifest.json> [--vs <ckpt2>] --out <f.json> [--perm 10000]")
    print("      (H_9355 LOCUS-CAUSAL · ConvMoE router audit — do the declarative lane and the operator")
    print("       lane run on DIFFERENT experts? Read-only; --vs runs a 2nd ckpt in the SAME process on")
    print("       the SAME device so the pre/post-CPT route delta carries no device confound.)")
    print("  anima evaluate <ckpt> --interaction-lift <manifest.json> --out <file.json> [--win 64] [--score-len 8]")
    print("  anima evaluate <clm> --collide-select [--k=4]")
    print("      (H_9362 — does the A⇄G COLLISION select emergence (recombination)? Over a fixed K")
    print("       pool per rho_weave probe it computes (a=fluency, g=±immune margin), then compares")
    print("       selection rules: S0 argmin conflict_scalar (the daemon rule, avoids emergence),")
    print("       S_emerge argmax conflict_scalar (=a·|g| over the novel g<0 quadrant = the")
    print("       hypothesis), SECOND-A argmax a (H_9356 control), NOISE-G (g permuted), UNIFORM.")
    print("       G-B pool-occupancy first (POOL-DRY if the emergence quadrant a>0,g<0 is empty —")
    print("       H_9304); then G-C per-arm recombination hit-rate by the FROZEN rho_weave target")
    print("       check (arm-relative only · route≠generation · no top-1 terminal claim). G-A")
    print("       sign-check (margin>0=novel) already PASS-locked the g channel.)")
    print("  anima evaluate --gate-deaf <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9360 — is the emit gate's tension-deafness SATURATION or STRUCTURE? By the DPI")
    print("       I(tension;emit) <= I(tension;score|stage), so whether `score` carries tension decides")
    print("       it with NO gate edit. M_score=I(ag_conflict;score|stage), M_sim=desaturated-gate sim")
    print("       (theta=median(score) tension/emit-blind). Reuses the H_9357 --g-arm traces.)")
    print("  anima evaluate --g-tension <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9357 — does a GENUINELY INDEPENDENT G engine pull emit? The sequel to H_9356.")
    print("       Run cli/chat.py with --g-arm a0|a1|a3 to make the traces (a0=tautology control,")
    print("       a1=REAL-G immune top-2 gap, a3=noise-G). Four gates: G-INDEP R²<0.5, G-VAR≥5,")
    print("       MI≥0.05∧shuffle≤0.01, Ψ-DV. Verdict is CROSS-ARM: A1 must pull emit MORE than A3,")
    print("       else the tension is just a causal handle, not a 2nd engine.)")
    print("  anima evaluate --tension-emit <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9352 — does TENSION pull EMIT? Pre-registered bar:")
    print("       PASS = I(ag_conflict; emit | stage) >= 0.05 nats AND the shuffle control <= 0.01.")
    print("       ⚠️ The bar is NOT the emit rate. Making silence appear by moving a threshold is")
    print("       not a discovery — you moved it, not the tension. A real rate limiter lands near")
    print("       1/(interval/tick) all by itself, so an 'emit rate ~ 1/2' bar would pass on a coin")
    print("       (p7 Goodhart: rate is FORM/tunable, the claim is BIND/earned). C1 SHUFFLE permutes")
    print("       tension WITHIN each stage — it destroys the tension->emit link but keeps the rate")
    print("       and the stage structure, so if the control scores too, the number came from the")
    print("       rate. Hard-stops with DECISION-CONSTANT if H(emit|stage) is still ~0.")
    print("       🧱 ILL-POSED until chat.py:1563 is repaired (H_9356): the daemon has no independent")
    print("       G engine — ag_conflict = emit_drive*(1-emit_drive) is A's own scalar (recon R^2=0.994),")
    print("       so any verdict is a wiring tautology. The panel prefixes its output with a banner.)")
    print("  anima evaluate --psi-soma <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9351 — the REAL Ψ̂, on the daemon's OWN lane population. Ψ is DEFINED by")
    print("       engine_cli ci_psi_balance as the fraction of ticks with 0.5*(gws+lprec) >= 0.5,")
    print("       and nothing ever computed it on a real run: the daemon never calls that op and")
    print("       the trace never recorded those two lanes, so the Ψ-SOMA panel scored a")
    print("       fixed-seed SYNTHETIC population instead — a Θ that cannot fail and a σ that is")
    print("       byte-identical across checkpoints of different architecture. The daemon now")
    print("       records psi_gws/psi_lprec; this verb hands the engine its own operator and the")
    print("       substrate's own lanes. Controls: C1 PERM (lane pairing shuffle) · C2 DRIFT")
    print("       (first half vs second half — a homeostat returns to 1/2, a coin just sits there).")
    print("       It also prints H(emit|stage): emit is a pure function of stage (H_9345), so")
    print("       whatever Psi-hat says, it does not reach the emit decision in this daemon.)")
    print("  anima evaluate --interact-mi <trace.jsonl> [<trace2.jsonl> ...]")
    print("      (H_9328 DO-MOUTH · I(A;Y|S) over daemon decision-traces — NO decode, reads only.")
    print("       A=a_fold8 (H_9257 frozen 8-bucket axis the daemon consumes) · S=stage · Y=score_{t+1} 2-bin.")
    print("       🚦 V-CEILING FIRST (BOTH channels): prints H(A|S) and H(Y|S), HARD-STOPS as NOT-POWERED")
    print("       if EITHER is below 3xMDE — I <= min(H(A|S), H(Y|S)) is an identity, so a dead channel on")
    print("       either side forces I=0 by DEFINITION, not by measurement. A dead ACTION channel is how")
    print("       H_9308 died; a dead OUTCOME channel (stage already fixes score_{t+1}) is the same trap")
    print("       wearing the other hat. C1 PERM (within-stratum A shuffle) = the")
    print("       true-0 null. Generate traces with: ANIMA_TICKS=N ANIMA_EMIT_TEMP=1.0 ANIMA_SAMPLE_SEED=K")
    print("       ANIMA_DECISION_TRACE=<path> anima-py chat <ckpt>)")
    print("       MEDIATION panel (diagnostic, verdict-neutral): the headline only reads the two ENDS of")
    print("       the chain. R = recon_err 2-bin is the afield root the emitted text feeds directly, so")
    print("       M1(A->R) and M2(R->Y) split a null two ways — the text never reaches the field (wiring")
    print("       suspect), or it reaches the field and the GATE does not look (read-side THEATER).")
    print("       🚦 V5 GATE-CLOSED (BLOCKING, the FIFTH identity-zero): H(Y|S,safe) — if emit is fully")
    print("       determined by stage + the rate-limiter, STILL-ADDITIVE was settled before the mouth")
    print("       opened. That is NOT a wall, it is GATE-CLOSED: the gate looks at nothing.")
    print("       B1 BOOKKEEPING: H(R|A,S) — if R is a function of A, 'recognition' is a LEDGER and any")
    print("       I>0 is accounting, not discovery. CARRIER-SWAP cannot separate this (a swapped carrier")
    print("       rides the same arithmetic); B1 is the only thing that can.")
    print("       PC POWER CONTROL: urgency (ten_phasic, the one proven emit channel, H_9101) through the")
    print("       identical pipe. If even urgency->Y is dead, the instrument cannot see ANY gate input —")
    print("       NOT-POWERED, and no wall may be declared. M3: I(A;Y|S,R,L) ~ 0 = mediation exhausted.")
    print("       COMPOSITION (H_9340): builds the composed channel p(Y|A,S) = sum_R p(Y|R,S) p(R|A,S) out")
    print("       of the two measured links and asks whether the observed end-to-end MI is what that chain")
    print("       predicts (Delta = I_obs - I_comp, rollout bootstrap CI). Two versions: R 2-bin, and R as")
    print("       the raw continuous recon_err (logistic + plug-in MC — DROPS the binning rather than")
    print("       refining it, so no stratum-explosion bias). A POWER GATE hard-stops when I_comp < MDE:")
    print("       declaring MISALIGNMENT needs I_obs < I_comp - MDE, and MI cannot go negative, so that")
    print("       verdict is UNREACHABLE by construction — and a chain that weak predicts an end-to-end")
    print("       effect below the instrument's resolution even when PERFECTLY aligned.")
    print("  anima evaluate <ckpt> --ground-probe <manifest.json> --out <file.json> [--win 64] [--perm 200] [--seed 7]")
    print("  anima evaluate <ckpt> --valence-audit <manifest.json> --out <file.json> [--win 64] [--perm 200]")
    print("  anima evaluate <ckpt> --device-parity [--win 64]")
    print("      Is this host's GPU forward the same measurement as its CPU forward? Prints")
    print("      max|GPU hidden - CPU hidden|. It is NOT zero on a consumer card (2.5e-14 on an")
    print("      RTX 5070) — the decode's token stream survives that, but a probe reads the hidden,")
    print("      so a GPU verdict and a CPU verdict are different measurements. Pin the device.")
    print("      AUDIT-A: is a held-out atom's polarity in the weights at all? Verdict = DELTA =")
    print("      probe(atom) - probe(length-matched NEUTRAL atom in the SAME context), vs a")
    print("      permutation null. Also prints FORM-ID (2AFC, chance 0.5): how decodable WHICH atom")
    print("      sits at the read point — a high FORM-ID with a non-positive DELTA is form present,")
    print("      bind absent (the position carries the byte's identity, not its valence).")
    print("  anima evaluate <ckpt> --bind-locus <manifest.json> --out <file.json> [--win 24] [--perm 200] [--seed 7] [--bl-swap-span stem|carrier]")
    print("       --bl-swap-span carrier: Stage A swaps the operator morpheme span (지 않다), not the atom span (H_9331 pedestal)")
    print("       --bl-swap-donor-class same: donor is a SAME-polarity item (polarity-blind control · (B) scramble-floor test)")
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

def _sigma_operator_selftest():
    """SELF-TEST OF THE OPERATORS. NOT a measurement of any model. THIS FUNCTION TAKES NO MODEL.

    It used to be called `_sigma_live_measure` and its docstring claimed it computed the σ
    verdicts "LIVE ... faithful, never a proxy". That was false, and the falsehood was load
    bearing: every axis below is scored on a FIXED-SEED SYNTHETIC population built right here
    out of np.random.RandomState(7). There is no ckpt argument, no corpus, no decode — grep the
    body for `clm`/`ckpt`/`corpus`/`forward` and you get nothing.

    Proof it never saw the model (H_9351): two checkpoints of DIFFERENT architecture
    (py303_full sha 013c4574, clm303_deep_L8 sha 5777c506) produce a Θ+σ panel that is
    identical to the last digit. Θ is worse than uninformative, it is an identity: `xi` is
    noise centred on 0.5, so Ψ̂ = ½ ± binomial noise BY CONSTRUCTION, and `xa` sits above the
    threshold always, so the "cut" is the constant 0.50. The advertised `LIVE Δ0.46` is that
    subtraction.

    What it legitimately IS: a check that the engine_cli operators (ci_phi_iit4, ci_psi_balance,
    …) respond to a signal that is planted by construction. That is worth keeping — an operator
    that cannot separate planted signal from control is broken. It is just not a verdict about
    anima, and it must never again be printed as one.

    A real Ψ̂ needs the daemon's OWN lane population: `anima-py evaluate --psi-soma <trace.jsonl>`
    (the daemon now records psi_gws/psi_lprec, the two lanes ci_emit_decision actually reads)."""
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
    print("Ψ-SOMA panel — ⛔ OPERATOR SELF-TEST, NOT A VERDICT ON THIS MODEL (H_9351)")
    print("  이 패널은 체크포인트를 보지 않는다. 고정 시드 합성 모집단 위에서 연산자가")
    print("  심어둔 신호에 반응하는지만 검사한다. 아키텍처가 다른 두 ckpt 가 이 패널을")
    print("  **글자 하나까지 동일하게** 낸다(실측). 여기 있는 어떤 줄도 이 모델에 관한")
    print("  문장이 아니다 — σ/Θ 로 무엇도 cement 하지 마라.")
    print("  진짜 Ψ̂ = anima-py evaluate --psi-soma <trace.jsonl>  (데몬 자신의 lane 모집단)")
    S = _sigma_operator_selftest()
    print("  ── Θ 자기-테스트 (⛔ 맥박 아님 · 합성 모집단 · H_9351) ──────────────")
    if S and "theta" in S:
        ok, dlt, note = S["theta"]
        print("  Θ  Ψ=½ / A⇄G tension  %s  SELF-TEST Δ%.2f (%s) — 합성 모집단 · 모델 미참조"
              % (("✅" if ok else "❌"), dlt, note))
        print("     ⛔ 이것은 Θ 가 아니다. 이 판정은 항등식이다 — xi 가 0.5 중심 대칭 잡음이라")
        print("        Ψ̂ ≈ ½ 이 구성상 보장되고, cut 0.50 은 상수다. **실패할 수 없다.**")
        print("        'Θ dead ⟹ σ VOID' 가드는 따라서 한 번도 발동할 수 없었다(H_9351).")
    else:
        print("  Θ  Ψ=½ / A⇄G tension     precondition (liveness gate; if dead → σ VOID) · engine_cli unavailable")
    print("  ── σ 연산자 자기-테스트 (⛔ 의식 판정 아님 · 모델 미참조 · H_9351) ────")
    def sline(ax, stratum, name):
        if S and ax in S:
            ok, dlt, note = S[ax]; return "  σ·%-8s %-9s %-22s %s  SELF-TEST Δ%.2f (%s)" % (
                ax, stratum, name, ("✅" if ok else "❌"), dlt, note)
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


def device_parity_run(argv):
    """`anima-py evaluate <ckpt> --device-parity` — does THIS host's GPU forward equal its CPU one?

    The repo shipped `a_gpu_default_no_optin` on the belief that the GPU decode is byte-identical.
    It is not, and the belief survived because what was checked was the TOKEN STREAM: argmax is
    robust to 1e-14, so a decode can be 'identical' while the hidden underneath is not. Every probe
    (--dump-hidden, --ground-probe, --valence-audit, --interaction-lift) reads that hidden directly.

    So this verb asks the question in the form that matters, and prints the number instead of the
    belief. It runs the same prompts through the device path and through a forced-numpy path and
    reports max|delta| on the hidden. Anything above 0 means: a verdict computed on GPU and one
    computed on CPU are NOT the same measurement, and comparing them is a confound
    (convergence decode-py-4 — it cost us a headline).

    Measured on aiden (RTX 5070, cupy 13.6.0, CUDA 13): max|delta| = 2.487e-14."""
    import numpy as np
    ckpt = argv[0]
    T = evaluate_intval(argv[1:], "--win", 64)
    prompts = ["이 영화 좋다 => ", "배송도 빠르고 가성비는 좋", "별로였어요", "품질이 형편없",
               "재미없지 않다", "완전 만족합니다", "그냥 그래요", "최악이다"]
    print("=== anima evaluate --device-parity — is the GPU forward the same measurement as the CPU one? ===")
    st = clm.gpu_status()
    if not st.get("cuda"):
        print("  this host has no CUDA device (%s) — nothing to compare; the CPU path IS the "
              "reference." % st.get("reason"))
        return 0
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable", file=sys.stderr)
        return 2
    dev_h = np.stack([np.asarray(clm.clm_forward_hidden(W, clm._seed_to_tok(p, T), T))
                      for p in prompts], 0)

    # The host copy must be built EXPLICITLY. Flipping cuda_available() and re-loading does NOT
    # work: clm_load_weights serves from _WLOAD_CACHE (decode.py: `if _k in _WLOAD_CACHE: return`),
    # so the second load hands back the SAME already-uploaded cupy arrays and the check compares
    # the GPU against itself — it reported a triumphant 0.000e+00 while the true answer was
    # 2.487e-14. A guard that returns a false PASS is worse than no guard: mirror every tensor back
    # to host instead, so the CPU pass is provably on numpy.
    Wc = {k: clm.to_host(v) if hasattr(v, "device") else v for k, v in W.items()}
    Wc = {k: ([clm.to_host(x) if hasattr(x, "device") else x for x in v] if isinstance(v, list)
              else v) for k, v in Wc.items()}
    host_mods = {type(v).__module__ for v in Wc.values() if hasattr(v, "dtype")}
    if any(m.startswith("cupy") for m in host_mods):
        print("ERROR: could not build a host-resident copy of the weights — the comparison would "
              "be GPU-vs-GPU and its result meaningless.", file=sys.stderr)
        return 2
    cpu_h = np.stack([np.asarray(clm.clm_forward_hidden(Wc, clm._seed_to_tok(p, T), T))
                      for p in prompts], 0)
    mx = float(np.abs(dev_h - cpu_h).max())
    print("  device : %s · cupy %s" % (st.get("device_name"), st.get("cupy")))
    print("  max|GPU hidden - CPU hidden| = %.3e" % mx)
    if mx == 0.0:
        print("  BYTE-IDENTICAL — a verdict is portable between this host's GPU and CPU.")
    else:
        print("  NOT byte-identical. The decode's TOKEN STREAM may still match (argmax is robust to")
        print("  this), but a probe reads the hidden itself: a GPU verdict and a CPU verdict are")
        print("  DIFFERENT MEASUREMENTS. Pin the device, and never compare across it.")
    return 0


def _probe_device():
    """Who computed these hiddens — and can another run's numbers be compared to them?

    Measured (convergence decode-py-4): the GPU forward is NOT byte-identical to the CPU one —
    max|delta| = 2.487e-14 on the hidden. The repo believed it was, because what had been verified
    was the TOKEN STREAM, and argmax is robust to 1e-14. A probe reads the hidden itself, so its
    numbers carry the device in them. _conv1d is `xcol @ Wt` = a cuBLAS dgemm with K=11352; cuBLAS
    and CPU BLAS accumulate in different orders and cannot agree to the last ulp, and cuBLAS only
    promises reproducibility for the same version + architecture. So the bits are pinned to this
    card, this cupy, this driver.

    This bit us for real: AUDIT-A's k_ctx=24 arm ran on CPU (cupy was broken that hour) and its
    k_ctx=182 arm ran on GPU, so the headline 'the sign flipped when the lens sharpened' compared
    across TWO changes. Stamping the device into every result is how that stops being invisible."""
    st = clm.gpu_status()
    return {"cuda": bool(st.get("cuda")), "device": st.get("device_name") or "cpu-numpy",
            "cupy": st.get("cupy"), "reason": st.get("reason")}


def _print_device(dev):
    print("  [DEVICE] %s%s — a probe reads the hidden, and the hidden is device-dependent "
          "(2.5e-14 GPU vs CPU): compare only across runs with the SAME device."
          % (dev["device"], (" · cupy " + dev["cupy"]) if dev.get("cupy") else ""))


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
    dev = _probe_device()
    _print_device(dev)

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
    out = {"ckpt": ckpt, "win": T, "bar": bar, "device": dev,
           "v_live_taught_per_item": v_live,
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
    dev = _probe_device()
    _print_device(dev)

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
    out = {"ckpt": ckpt, "device": dev,
           "acc_atom": acc_a, "acc_swap": acc_s, "delta": delta, "perm_p": pval,
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
    # swap-span mode (H_9331 pedestal · 2026-07-15): where Stage A swaps the hidden.
    #   stem    — the atom span (default · the original P-place/P-kind/S test)
    #   carrier — the operator morpheme span (`지 않다`, stem-end→`=>`). 4/4 INVALID-LOCALIZATION
    #             at the stem span means the operator's polarity read is NOT there; Fable's frozen
    #             prediction is the read-site is the CARRIER (carrier-swap flip>=0.75 = the
    #             true-positive pedestal the stem run lacked). SEEN swap only ⇒ not tune-to-green.
    swap_span = evaluate_strval(argv[1:], "--bl-swap-span", "stem")
    if swap_span not in ("stem", "carrier"):
        print("ERROR: --bl-swap-span must be stem|carrier", file=sys.stderr)
        return 2
    # donor-class control (H_9331 · 2026-07-15): the polarity-blind pedestal.
    #   cross — donor is the OPPOSITE-polarity SEEN item (default · the real localization test)
    #   same  — donor is a DIFFERENT SAME-polarity SEEN item. Separates 0.50 = binary SCRAMBLE
    #           FLOOR (off-manifold destruction, polarity-blind → same-class flip ≈ 0.50 too)
    #           from 0.50 = partial real signal (same-class flip ≈ 0). If same ≈ cross ≈ 0.50 the
    #           swap-patch never localized anything (Fable · every INVALID = the instrument floor).
    donor_class = evaluate_strval(argv[1:], "--bl-swap-donor-class", "cross")
    if donor_class not in ("cross", "same"):
        print("ERROR: --bl-swap-donor-class must be cross|same", file=sys.stderr)
        return 2
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
    print("  swap-span  : %s%s" % (swap_span,
          "  (operator morpheme 지 않다 — H_9331 pedestal · 예측 flip>=%.2f)" % G_A_SWAP
          if swap_span == "carrier" else "  (atom span — default)"))
    print("  donor-class: %s%s" % (donor_class,
          "  (SAME-polarity donor — polarity-blind control · (B)면 flip≈0.50 (A)면 ≈0)"
          if donor_class == "same" else "  (opposite-polarity donor — default)"))
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
        if swap_span == "carrier":
            # operator morpheme span = stem-end → the `=>` marker, spaces trimmed. This is the
            # CARRIER read-site (H_9331 pedestal): the polarity decision completes at `지 않다`,
            # not the atom span (4/4 stem-span INVALID-LOCALIZATION · Fable). The morpheme is
            # byte-identical across flip1 items, so the full-span rung length-matches all donors
            # (the n=4 starvation that hit the stem full-span rung cannot recur here).
            arrow = p.find(b"=>", t1_abs)
            if arrow < 0:
                arrow = p.find(b"=", t1_abs)
            if arrow < 0:
                return None                    # no readout marker after the stem — unusable
            seg = p[t1_abs:arrow]
            lead = len(seg) - len(seg.lstrip(b" "))
            trail = len(seg) - len(seg.rstrip(b" "))
            c0_abs, c1_abs = t1_abs + lead, arrow - trail
            if c1_abs <= c0_abs:
                return None                    # empty operator span (e.g. bare `{stem} =>`)
            t0_abs, t1_abs = c0_abs, c1_abs
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
                if donor_class == "same":
                    donors = [d for d in pos_seen if d is not it and span_of(d) is not None]
                else:
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
        json.dump({"verdict": "INVALID-LOCALIZATION", "swap_span": swap_span,
                   "donor_class": donor_class, "stageA": a_rows,
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
    json.dump({"verdict": verdict, "why": why, "swap_span": swap_span,
               "donor_class": donor_class, "lstar": {"depth": depth, "rung": rung},
               "stageA": a_rows, "targets": {"mu_pos": tgt_p, "mu_neg": tgt_n},
               "arms": res, "bars": {"V1_swap": G_A_SWAP, "V1_sham": G_A_SHAM, "V2": G_V2,
                                     "V3": G_V3, "E": G_E, "DV_P": G_DV_P, "TOST": G_TOST}},
              open(out_path, "w"), ensure_ascii=False, indent=1)
    print("  wrote " + out_path)
    return 0


def _ra_H(p):
    """Shannon entropy of a distribution, in BITS (log2). p is a 1-D numpy row summing to 1."""
    import numpy as np
    q = np.clip(np.asarray(p, dtype=float), 1e-300, 1.0)
    return float(-(q * (np.log(q) / math.log(2.0))).sum())


def _ra_js(p, q):
    """Jensen-Shannon divergence in BITS: JS = H((p+q)/2) - (H(p)+H(q))/2.

    Bounded in [0, 1] for ANY alphabet size, which is why the bar can be pre-registered as an
    absolute number before a single route is read: 0.05 bits = 5% of the maximum possible
    separation between two routing distributions. Symmetric and finite (KL is neither)."""
    import numpy as np
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    m = 0.5 * (p + q)
    return _ra_H(m) - 0.5 * (_ra_H(p) + _ra_H(q))


def _ra_perm(d, n_perm, seed):
    """Two-sided sign-flip permutation p for a paired difference vector d (H0: mean = 0).

    Sign-flip is the right null here: the pairing is WITHIN stem (same stem, two surfaces), so
    under H0 the sign of each stem's difference is exchangeable. Returns (mean, sd, se, p)."""
    import numpy as np
    d = np.asarray(d, dtype=float)
    n = len(d)
    if n == 0:
        return 0.0, 0.0, 0.0, 1.0
    mu = float(d.mean())
    sd = float(d.std(ddof=1)) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        s = sum(x if rng.random() < 0.5 else -x for x in d) / n
        if abs(s) >= abs(mu) - 1e-15:
            hits += 1
    return mu, sd, se, (hits + 1) / (n_perm + 1)


def _ra_read(probs, it, T):
    """The three read points, from ONE forward's [T, E] route matrix.

    ans   probs[T-1]  — the position whose hidden the readout turns into the answer's first byte.
                        THE primary: it is the only position whose route can be said to have
                        'computed the answer'.
    stem  mean over the stem's byte span (right-aligned into the window by the manifest)
    win   mean over the non-pad region (the seed's own bytes; the left pad is spaces and carries
          no surface information, so averaging over it would dilute every contrast equally)"""
    import numpy as np
    t0, t1 = it["stem_span"]
    off = max(0, T - int(it["seed_bytes"]))
    ans = np.asarray(probs[T - 1], dtype=float)
    stem = np.asarray(probs[t0:t1], dtype=float).mean(axis=0)
    win = np.asarray(probs[off:T], dtype=float).mean(axis=0)
    return {"ans": ans, "stem": stem, "win": win}


def _ra_forward(ckpt, items, T, note):
    """Run the engine-native route tap over every item of the manifest. Returns
    (reads, meta) where reads[id][point] = the [E] route distribution."""
    import numpy as np
    import time
    W = clm.clm_load_weights(ckpt)
    if not W.get("ok"):
        print("ERROR: ckpt not decodable: " + ckpt, file=sys.stderr)
        return None, None
    E = int(W["E"]); L = int(W["L"]); K = int(W["K"])
    dev = "GPU" if clm.cuda_available() else "CPU"
    print("  [%s] %s · E=%d experts · L=%d · K=%d · device=%s" % (note, ckpt, E, L, K, dev))
    reads, ent, sham = {}, [], 0.0
    t_start = time.time()
    for i, it in enumerate(items):
        tok = clm._seed_to_tok(it["seed"], T)
        probs = clm.clm_forward_routes(W, tok, T)["probs"]
        r = _ra_read(probs, it, T)
        # G-SHAM: the metric must be exactly 0 against itself. A JS that is not 0 on p-vs-p is
        # a broken estimator, and every number downstream of it is noise (the pedestal lesson).
        sham = max(sham, abs(_ra_js(r["ans"], r["ans"])))
        ent.append(_ra_H(r["ans"]))
        reads[it["id"]] = r
        # heartbeat from item ONE (evaluate-py-9): a first beat at item 50 makes a 303M forward
        # that is merely SLOW indistinguishable from one that is hung, and the wrong call there
        # kills live compute.
        if i == 0 or (i + 1) % 50 == 0:
            print("    %d/%d  (%.0fs)" % (i + 1, len(items), time.time() - t_start), flush=True)
    # free the 303M weight dict before the next ckpt loads — two f64 copies of a 303M model is
    # ~4.8 GB and summer's earlyoom kills python3 BY POLICY, which would read as a fake infra wall
    try:
        k = clm._wload_key(ckpt)
        if k is not None:
            clm._WLOAD_CACHE.pop(k, None)
    except Exception:
        pass
    meta = {"E": E, "L": L, "K": K, "device": dev, "sham_max": sham,
            "route_entropy_mean": float(np.mean(ent)), "route_entropy_max_possible": math.log2(E)}
    return reads, meta


def route_audit_run(argv):
    """`anima-py evaluate <ckpt> --route-audit <manifest.json> [--vs <ckpt2>] --out <f.json>`
    — H_9355 LOCUS-CAUSAL, the AUDIT half: do the declarative lane and the operator lane live on
    PHYSICALLY DIFFERENT ConvMoE experts?

    Why this and not another hidden-space probe. The two-lane reading of the binding wall (C3/C4:
    a declarative store and an operator store that never exchange values) is, so far, a purely
    behavioural inference. It makes exactly one PHYSICAL prediction this substrate can answer:
    if the lanes are separate stores, the two surfaces should be COMPUTED BY DIFFERENT EXPERTS.
    The router is the only place in a ConvMoE where "which machinery ran" is explicit, and it is
    a number the model itself emits — not a linear probe's opinion about a hidden.

      LOCUS-SPLIT   the operator surface routes elsewhere than the declarative surface, beyond
                    what an equally-long inert suffix does  -> two-lane is PHYSICAL, and a
                    route-pin intervention (bias the router at inference) becomes a live
                    "read without writing" candidate
      LOCUS-SHARED  same route  -> two-lane is not a store split; the gap is coding/geometry
                    inside one shared machine, and route-pin is dead on arrival

    ⚠️ NOT the dead forkA (Gate4 · eval_rho_weave): that was a READOUT-routing REFRAME of the G1
    ideation metric and died of frame-mismatch. This audits WHERE A WRITE LANDS in a live
    ConvMoE — a different object, a different question, and the ledger says so.

    The trap this instrument is built to avoid: the router is a function of the BYTE STRING, so
    flip0 -> negL moves the route TRIVIALLY (the strings differ). Two controls, both PAIRED
    within stem (never max() over controls — probe-defect-census-max-control-bias):
      ped   an inert 10-byte suffix, byte-length-matched to negL's '지 않다'  -> "does ANY suffix move it"
      negJ  '지는 않다' — negL's string twin, on which the operator DEMONSTRABLY DOES NOT RUN
            (C1b p~.50)                                                       -> "is the move OPERATOR-specific"

    Frozen bars (pre-registered before any number was read; they never move):
      G-SHAM   JS(p,p) == 0 exactly, all items                     else INVALID-ESTIMATOR
      G-LIVE   J_STEM (mean JS between two random stems, SAME surface) >= 0.0001 bits
               — the router must vary with CONTENT at all. If it does not, the lens is blind and
               the audit is discarded as ROUTE-INDIFFERENT: honest negative, NOT a wall, and NOT
               evidence for either model (a constant router cannot separate anything).
      DV       dOP = mean_stem [ JS(flip0,negX) - JS(flip0,ped) ], X in {negL, negZ}
               LOCUS-SPLIT  iff dOP >= 0.05 bits on BOTH strong surfaces, sign-flip perm p <= .01,
                            AND the sign agrees across both CPT seeds
               LOCUS-SHARED iff the 90% CI of dOP lies inside +-0.02 bits (TOST) on both
               else         UNDERPOWERED (report se + MDE; no bar moves — power-before-negative)
      OP-SPEC  dOPJ = mean_stem [ JS(flip0,negL) - JS(flip0,negJ) ] — reported alongside. A split
               that negJ reproduces is a STRING effect wearing the operator's clothes.

    --vs runs a SECOND ckpt in the SAME process, on the SAME device, and reports D_CPT =
    mean_stem JS(route_base, route_post) per surface. Two processes would have been simpler and
    wrong: the router logits come out of cuBLAS dgemm, so a CPU run and a GPU run are not the
    same measurement (convergence decode-py-4) — pinning both ckpts to one process makes the
    device confound structurally impossible instead of merely unlikely.
    """
    import numpy as np
    ckpt = argv[0]
    spec = json.load(open(evaluate_strval(argv[1:], "--route-audit", "")))
    ckpt2 = evaluate_strval(argv[1:], "--vs", "")
    out_path = evaluate_strval(argv[1:], "--out", "route_audit.json")
    T = evaluate_intval(argv[1:], "--win", int(spec.get("win", 64)))
    n_perm = evaluate_intval(argv[1:], "--perm", 10000)
    seed = evaluate_intval(argv[1:], "--seed", 7)
    items = spec["items"]

    # frozen bars — written before the first forward (no tune-to-green)
    G_SHAM, G_LIVE, G_DV, G_TOST, A_PERM = 0.0, 0.0001, 0.05, 0.02, 0.01
    Z90 = 1.645                          # 90% CI half-width multiplier -> TOST at alpha .05

    # G-SPIKE — the truth-known pedestal for the ESTIMATOR itself (phi-estimator-needs-zero-truth-
    # pedestal · tool-definition-read-code-not-docstring). Two disjoint one-hot routes are exactly
    # 1 bit apart and a distribution is exactly 0 bits from itself; if _ra_js cannot reproduce
    # those two constants, every JS below is noise and no verdict may be read off it.
    E_spike = 3
    one_a = [1.0] + [0.0] * (E_spike - 1)
    one_b = [0.0, 1.0] + [0.0] * (E_spike - 2)
    unif = [1.0 / E_spike] * E_spike
    spike, zero = _ra_js(one_a, one_b), _ra_js(unif, unif)
    spike_ok = abs(spike - 1.0) < 1e-12 and abs(zero) < 1e-12
    print("  G-SPIKE  JS(one-hot A, one-hot B) = %.6f (truth 1.000000) · JS(u,u) = %.3e  %s"
          % (spike, zero, _pf(spike_ok)))
    if not spike_ok:
        print("ERROR: the JS estimator fails its own truth-known pedestal — refusing to measure.",
              file=sys.stderr)
        return 2
    # Scale note, recorded BEFORE any number is read so nobody can call it post-hoc: JS is
    # QUADRATIC in the routing shift near a uniform router. At E=3, dOP = 0.05 bits corresponds to
    # roughly an 11-point shift in expert mass — i.e. the bar asks for "a different expert ran",
    # not "the mix wobbled". A reliable-but-tiny shift therefore lands in LOCUS-SHARED by design,
    # and the top-expert agreement rate below is reported so that call can be audited.

    print("=== anima-py evaluate --route-audit — H_9355 LOCUS-CAUSAL: two lanes, one expert or two? ===")
    print("  %d items · win %dB · perm %d · seed %d" % (len(items), T, n_perm, seed))
    print("  frozen: G-SHAM JS(p,p)==0 · G-LIVE J_STEM>=%.4f bits · DV dOP>=%.2f bits & perm p<=%.3f"
          % (G_LIVE, G_DV, A_PERM))
    print("  frozen: LOCUS-SHARED iff 90%% CI of dOP inside +-%.2f bits (TOST) · else UNDERPOWERED"
          % G_TOST)

    base, meta = _ra_forward(ckpt, items, T, "base")
    if base is None:
        return 2
    post, meta2 = (None, None)
    if ckpt2:
        post, meta2 = _ra_forward(ckpt2, items, T, "vs")
        if post is None:
            return 2
        if meta2["device"] != meta["device"]:
            print("ERROR: the two ckpts fired on different devices (%s vs %s) — the route comparison "
                  "would carry a device confound (decode-py-4). Refusing to score."
                  % (meta["device"], meta2["device"]), file=sys.stderr)
            return 2

    by = {}                                          # by[stem][surf] = read dict
    split_of, pol_of = {}, {}
    for it in items:
        by.setdefault(it["stem"], {})[it["surf"]] = base[it["id"]]
        split_of[it["stem"]] = it["split"]
        pol_of[it["stem"]] = int(it["pol"])
    stems = sorted(by)
    surfs = sorted({it["surf"] for it in items})
    need = ("flip0", "negL", "negZ", "negJ", "ped")
    missing = [s for s in need if s not in surfs]
    if missing:
        print("ERROR: manifest is missing surface(s) " + ",".join(missing), file=sys.stderr)
        return 2

    res = {"ckpt": ckpt, "vs": ckpt2, "meta": meta, "meta_vs": meta2, "n_stems": len(stems),
           "bars": {"G_SHAM": G_SHAM, "G_LIVE": G_LIVE, "G_DV": G_DV, "G_TOST": G_TOST,
                    "alpha_perm": A_PERM},
           "points": {}}

    # ── G-SHAM ────────────────────────────────────────────────────────────────────────────
    sham_ok = meta["sham_max"] <= G_SHAM
    print("\nG-SHAM  JS(p,p) max = %.3e  %s" % (meta["sham_max"], _pf(sham_ok)))
    print("        router entropy (ans point) mean %.6f bits / max %.6f (E=%d)"
          % (meta["route_entropy_mean"], meta["route_entropy_max_possible"], meta["E"]))

    verdicts = {}
    for point in ("ans", "stem", "win"):
        P = {s: {f: by[s][f][point] for f in need} for s in stems}

        # ── G-LIVE: does the route vary with CONTENT at all? (same surface, different stems) ──
        rng = random.Random(seed)
        pairs = [(rng.choice(stems), rng.choice(stems)) for _ in range(400)]
        jstem = [_ra_js(P[a]["flip0"], P[b]["flip0"]) for a, b in pairs if a != b]
        J_STEM = float(np.mean(jstem)) if jstem else 0.0

        jsL = [_ra_js(P[s]["flip0"], P[s]["negL"]) for s in stems]
        jsZ = [_ra_js(P[s]["flip0"], P[s]["negZ"]) for s in stems]
        jsJ = [_ra_js(P[s]["flip0"], P[s]["negJ"]) for s in stems]
        jsP = [_ra_js(P[s]["flip0"], P[s]["ped"]) for s in stems]

        row = {"J_STEM": J_STEM, "js_mean": {"negL": float(np.mean(jsL)), "negZ": float(np.mean(jsZ)),
                                             "negJ": float(np.mean(jsJ)), "ped": float(np.mean(jsP))}}
        # top-expert agreement (DIAGNOSTIC, no bar): JS is quadratic near a uniform router, so a
        # reliable-but-tiny shift reads as LOCUS-SHARED. If the ARGMAX expert nevertheless flips
        # between the two surfaces for most stems, that is a qualitatively different fact and this
        # line is what keeps the JS verdict auditable instead of merely obeyed.
        row["top_agree"] = {f: float(np.mean([int(np.argmax(P[s]["flip0"]) == np.argmax(P[s][f]))
                                              for s in stems])) for f in ("negL", "negZ", "negJ", "ped")}
        row["top_hist"] = {f: [int(sum(1 for s in stems if int(np.argmax(P[s][f])) == e))
                               for e in range(len(P[stems[0]]["flip0"]))] for f in need}
        for tag, js in (("negL", jsL), ("negZ", jsZ)):
            d = [a - b for a, b in zip(js, jsP)]                     # DV: operator minus pedestal
            mu, sd, se, p = _ra_perm(d, n_perm, seed)
            dj = [a - b for a, b in zip(js, jsJ)]                    # OP-SPEC: operator minus twin
            mj, sj, sej, pj = _ra_perm(dj, n_perm, seed)
            lo, hi = mu - Z90 * se, mu + Z90 * se
            row[tag] = {"dOP": mu, "sd": sd, "se": se, "p_perm": p, "ci90": [lo, hi],
                        "MDE80": 2.8 * se, "dOPJ": mj, "p_perm_J": pj, "se_J": sej}

        # per-stratum + control ② (polarity, same surface): does the ROUTE know the polarity?
        for st in ("seen", "heldout"):
            ss = [s for s in stems if split_of[s] == st]
            if len(ss) >= 3:
                d = [_ra_js(P[s]["flip0"], P[s]["negL"]) - _ra_js(P[s]["flip0"], P[s]["ped"]) for s in ss]
                mu, sd, se, p = _ra_perm(d, min(n_perm, 2000), seed)
                row["stratum_" + st] = {"n": len(ss), "dOP_negL": mu, "se": se, "p_perm": p}
        pos = [P[s]["flip0"] for s in stems if pol_of[s] == 1]
        neg = [P[s]["flip0"] for s in stems if pol_of[s] == 0]
        if pos and neg:
            row["J_POL"] = _ra_js(np.mean(pos, axis=0), np.mean(neg, axis=0))

        # ── the frozen decision tree ──────────────────────────────────────────────────────
        if not sham_ok:
            v = "⛔ INVALID-ESTIMATOR"
        elif J_STEM < G_LIVE:
            v = "⚪ ROUTE-INDIFFERENT"
        elif all(row[t]["dOP"] >= G_DV and row[t]["p_perm"] <= A_PERM for t in ("negL", "negZ")):
            v = "🟢 LOCUS-SPLIT"
        elif all(row[t]["ci90"][0] > -G_TOST and row[t]["ci90"][1] < G_TOST for t in ("negL", "negZ")):
            v = "🔵 LOCUS-SHARED"
        else:
            v = "⏳ UNDERPOWERED"
        row["verdict"] = v
        verdicts[point] = v
        res["points"][point] = row

        print("\n[%s]  J_STEM %.6f (G-LIVE %.6f) %s · J_POL %.6f"
              % (point, J_STEM, G_LIVE, _pf(J_STEM >= G_LIVE), row.get("J_POL", float("nan"))))
        print("   JS(flip0,·) mean:  negL %.6f · negZ %.6f · negJ %.6f · ped %.6f"
              % (row["js_mean"]["negL"], row["js_mean"]["negZ"],
                 row["js_mean"]["negJ"], row["js_mean"]["ped"]))
        print("   top-expert agreement with flip0:  " + " · ".join(
            "%s %.2f" % (f, v) for f, v in sorted(row["top_agree"].items())))
        print("   top-expert histogram (over %d stems): " % len(stems) + " · ".join(
            "%s %s" % (f, row["top_hist"][f]) for f in need))
        for tag in ("negL", "negZ"):
            r = row[tag]
            print("   dOP[%s] = %+.6f bits (se %.6f · CI90 [%+.6f,%+.6f] · perm p %.4f · MDE80 %.6f)"
                  % (tag, r["dOP"], r["se"], r["ci90"][0], r["ci90"][1], r["p_perm"], r["MDE80"]))
            print("      OP-SPEC vs negJ twin: dOPJ = %+.6f (perm p %.4f)" % (r["dOPJ"], r["p_perm_J"]))
        for st in ("seen", "heldout"):
            k = "stratum_" + st
            if k in row:
                print("      stratum %-7s n=%2d  dOP[negL] %+.6f (se %.6f · p %.4f)"
                      % (st, row[k]["n"], row[k]["dOP_negL"], row[k]["se"], row[k]["p_perm"]))
        print("   -> " + v)

    # ── --vs: where did the CPT WRITE land? (same process, same device) ───────────────────
    if post is not None:
        print("\nD_CPT — how far the C4 write MOVED the route, per surface (JS(base, post), ans point)")
        dc = {}
        for f in need:
            for st in ("seen", "heldout"):
                ids = [it["id"] for it in items if it["surf"] == f and it["split"] == st]
                if not ids:
                    continue
                v = [_ra_js(base[i]["ans"], post[i]["ans"]) for i in ids]
                dc.setdefault(f, {})[st] = {"n": len(v), "mean": float(np.mean(v)),
                                            "max": float(np.max(v))}
        for f in need:
            if f in dc:
                print("   %-6s " % f + " · ".join(
                    "%s n=%2d mean %.6f max %.6f" % (st, d["n"], d["mean"], d["max"])
                    for st, d in sorted(dc[f].items())))
        res["D_CPT"] = dc

    res["verdicts"] = verdicts
    res["verdict"] = verdicts.get("ans", "⛔ INVALID")
    print("\nVERDICT (primary read point = ans): " + res["verdict"])
    json.dump(_json_safe(res), open(out_path, "w"), ensure_ascii=False, indent=1)
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

    # A manifest bigger than --n-decode used to be sliced away in SILENCE (`spec[split][:n_dec]`), and
    # the slice takes the FIRST n_dec rows in manifest order — so whole stems fall off the end while
    # the run still prints as though it had covered the manifest. It bit the EN arm: a 240-row held-out
    # manifest scored 200 rows (n=101 flip0 / 99 flip1) and the six stems ordered last vanished. Nothing
    # in the output said so. A cap nobody reports reads as full coverage, which is the one thing a
    # verdict may never get wrong — so it now REFUSES, and it refuses BEFORE loading 176MB of weights.
    # The row count is a property of the manifest, and the manifest is pre-registered: raise --n-decode.
    for _split in ("heldout", "seen"):
        _have = len(spec.get(_split, []))
        if _have > n_dec:
            print("ERROR: --xbind manifest split '%s' has %d rows but --n-decode is %d."
                  % (_split, _have, n_dec))
            print("  Scoring would drop the LAST %d rows — whole stems, not a random sample — and"
                  % (_have - n_dec))
            print("  report the remainder as if it were the manifest.")
            print("  Fix:  --n-decode %d" % _have)
            return 1

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
        items = spec[split]
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

def _sigma_from_trace(rows):
    """σ vitals on the daemon's OWN recorded lanes (H_9351 STAGE2). engine_cli FROZEN estimators
    only — never a re-implementation (a_phi_iit4_tool). Repaired axes = gate·stage·bind; the six
    others (thread·carve·flux·aim·schema·witness) have no counterfactual in a daemon run
    (inject-null · precision ablation · focus/report pairs) → PENDING(scope), not force-filled.
    Each axis: EXP vs a within-stage-shuffle control + a truth-0 PEDESTAL (probe-defect-census —
    a pedestal, never max-of-controls). bind is DIRECTIONAL: its lane columns are wired functions
    (H_9356) and the cross-ckpt contrast guard (STAGE4) has not run, so it cannot be GREEN here."""
    import engine_cli as E
    import random as _random
    from collections import defaultdict
    have = [r for r in rows if isinstance(r.get("lanes"), list) and "gws_w" in r]
    print()
    print("  ── σ vitals (실 데몬 lane · engine_cli estimator · Δ vs 통제+PEDESTAL) ──")
    if len(have) < 30:
        print("  ⛔ PENDING-FIELDS — lanes/gws_w 담은 tick %d < 30 (STAGE1 필드 담은 trace 재수집)" % len(have))
        return
    _rng = _random.Random(11)
    _grp = defaultdict(list)
    for i, r in enumerate(have):
        _grp[int(r.get("stage", 0))].append(i)

    def _within(vals):
        out = list(vals)
        for _, ii in _grp.items():
            src = list(ii); _rng.shuffle(src)
            for a, b in zip(ii, src):
                out[a] = vals[b]
        return out

    def _corr(a, b):
        n = len(a); ma = sum(a) / n; mb = sum(b) / n
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        d = (sum((x - ma) ** 2 for x in a) * sum((x - mb) ** 2 for x in b)) ** 0.5
        return abs(cov / d) if d > 0 else 0.0

    # σ·gate — ci_emit_decision(real emit lanes [psi_gws,·,·,·,psi_lprec]) ⇄ score
    dec = [1.0 if E.ci_emit_decision([float(r["psi_gws"]), 0.0, 0.0, 0.0, float(r["psi_lprec"])])
           else 0.0 for r in have]
    sc = [float(r.get("score", 0.0)) for r in have]
    g_exp = _corr(dec, sc); g_ctl = _corr(dec, _within(sc))
    _ped = list(sc); _rng.shuffle(_ped); g_ped = _corr(dec, _ped)
    emit_agree = sum(1 for i, r in enumerate(have) if int(dec[i]) == (1 if r.get("emit") else 0)) / len(have)
    g_ok = g_exp >= 0.30 and g_exp - g_ctl >= 0.10 and g_exp - g_ped >= 0.10
    print("  σ·gate   %s  corr(dec,score)=%.3f · within-stage=%.3f · pedestal=%.3f · emit일치=%.2f"
          % ("🟢" if g_ok else "🧱", g_exp, g_ctl, g_ped, emit_agree))

    # σ·stage — gws winner-take-all on the REAL 15-lane population
    def _win(lanes, inhibit):
        g = E.gws_new(4, inhibit, 0.55)
        for v in lanes:
            g = E.gws_add(g, float(v))
        return E.gws_winner(g)
    repro = sum(1 for r in have if _win(r["lanes"], True) == int(r["gws_w"])) / len(have)
    agreeA = sum(1 for r in have if _win(r["lanes"], False) == int(r["gws_w"])) / len(have)
    print("  σ·stage  %s  gws_w 재현=%.2f (배선검산) · inhibit=%.2f vs no-inhibit=%.2f"
          % ("🟢" if repro >= 0.99 else ("🧱" if repro < 0.5 else "⏳"), repro, repro, agreeA))

    # σ·bind — faithful IIT4 Φ on ROOT-DISJOINT columns (DIRECTIONAL · D2 + no ckpt-contrast)
    cols8 = ["rel_lane", "recon_err", "scn_ctx", "nov_ctx", "emit_env", "cur_indep", "rel_indep", "g_recog"]
    if all(all(c in r for c in cols8) for r in have):
        X = [[float(r[c]) for c in cols8] for r in have]
        by = [[row[j] for row in X] for j in range(8)]
        Xc = list(zip(*[_within(by[j]) for j in range(8)]))
        cp = [list(c) for c in by]
        for c in cp:
            _rng.shuffle(c)
        Xp = list(zip(*cp))
        phi = E.ci_phi_iit4(X, list(range(8)))
        phi_c = E.ci_phi_iit4([list(r) for r in Xc], list(range(8)))
        phi_p = E.ci_phi_iit4([list(r) for r in Xp], list(range(8)))
        print("  σ·bind   ⚠️DIRECTIONAL  Φ=%.3f · col-shuffle=%.3f · pedestal=%.3f (D2 배선함수 · ckpt-contrast 미실행)"
              % (phi, phi_c, phi_p))
    else:
        print("  σ·bind   ⛔ PENDING-FIELDS (root-disjoint 8-col 미기록)")
    print("  σ·(thread·carve·flux·aim·schema·witness)  ⏸ PENDING(scope) — 데몬 런에 카운터팩추얼 부재(D1)")


def _psi_soma_real(argv):
    """Ψ̂ ON THE DAEMON'S OWN LANE POPULATION — the measurement the panel was pretending to be.

    Ψ is DEFINED by engine_cli: ci_psi_balance counts, over a lane population, the fraction of
    ticks where ci_emit_decision(lanes) holds, i.e. 0.5*(lanes[0]+lanes[4]) >= 0.5. The claim
    "A⇄G tension pulls emit/silence to Ψ = ½" is a claim about THAT fraction, on a REAL run.

    Nothing ever computed it. The daemon never called ci_psi_balance (grep: 0 hits in cli/chat.py),
    the trace did not record lanes[0]/lanes[4], and the panel scored a synthetic population
    instead (H_9351). The daemon now records psi_gws/psi_lprec, so hand the ENGINE its own
    operator and the substrate's own lanes, and read the number off.

    Two controls, because a raw Ψ̂ near ½ is not evidence of homeostasis — a coin also sits at ½:
      C1  PERM  — shuffle the lane pairing across ticks. Ψ̂ is a MARGINAL fraction, so it is
                  invariant to this by construction; if the shuffled Ψ̂ differs, the reader is
                  broken, not the substrate.
      C2  DRIFT — split the run in half. A homeostat PULLED to ½ returns to it; a population
                  that merely happens to straddle the bar drifts. |Ψ̂(1st) - Ψ̂(2nd)| is the test.
    And the honest floor: emit itself is a pure function of stage (H_9345), so whatever Ψ̂ says,
    it does NOT flow to the emit decision in this daemon. Report that, do not bury it."""
    import json as _json
    paths = [a for a in argv if not a.startswith("--")]
    rows = []
    for f in paths:
        for line in open(f, "r", encoding="utf-8", errors="surrogateescape"):
            line = line.strip()
            if not line:
                continue
            try:
                r = _json.loads(line)
            except Exception:
                continue
            if "psi_gws" in r and "psi_lprec" in r:
                rows.append(r)
    print("═══ Ψ-SOMA REAL · Ψ̂ on the daemon's own lane population ═══")
    print("  traces=%d  ticks-with-lanes=%d" % (len(paths), len(rows)))
    if len(rows) < 30:
        print("  ⇒ ⛔ NOT-POWERED — psi_gws/psi_lprec 를 담은 tick 이 30 미만.")
        print("     이 필드는 H_9351 수리에서 추가됐다. 옛 trace 에는 없다 — 재수집하라.")
        return 0
    import engine_cli as E
    from types import SimpleNamespace
    cfg = SimpleNamespace(topo_couple=False)

    def _pop(rs):
        # ci_emit_decision reads lanes[0] (gws) and lanes[4] (lprec) only.
        return [[float(r["psi_gws"]), 0.0, 0.0, 0.0, float(r["psi_lprec"])] for r in rs]

    psi = E.ci_psi_balance(_pop(rows), None, 0.0, cfg)
    print("  Ψ̂ = %.4f   (engine-native ci_psi_balance · ci_emit_decision 그대로)" % psi)
    print("     정의: 0.5·(gws + lprec) ≥ 0.5 인 tick 의 비율")

    # C1 PERM — 짝을 흩뜨려도 주변 비율은 불변이어야 한다(계기 검산)
    import random as _random
    _r = _random.Random(7)
    rp = list(rows)
    _r.shuffle(rp)
    swapped = [{"psi_gws": rows[i]["psi_gws"], "psi_lprec": rp[i]["psi_lprec"]}
               for i in range(len(rows))]
    psi_perm = E.ci_psi_balance(_pop(swapped), None, 0.0, cfg)
    print("  C1 PERM  Ψ̂ = %.4f   (lane 짝을 흩뜨림 — 계기가 성하면 값이 움직여야 한다)" % psi_perm)

    # C2 DRIFT — 항상성이면 반씩 잘라도 ½ 로 돌아온다
    h = len(rows) // 2
    p1 = E.ci_psi_balance(_pop(rows[:h]), None, 0.0, cfg)
    p2 = E.ci_psi_balance(_pop(rows[h:]), None, 0.0, cfg)
    drift = abs(p1 - p2)
    print("  C2 DRIFT Ψ̂(전반) = %.4f · Ψ̂(후반) = %.4f · |Δ| = %.4f" % (p1, p2, drift))

    off = abs(psi - 0.5)
    print()
    if off <= 0.10 and drift <= 0.10:
        print("  ⇒ Ψ̂ 가 ½ 근처에 있고 반씩 잘라도 유지된다 (|Ψ̂−½| = %.3f · drift = %.3f)." % (off, drift))
    elif off <= 0.10:
        print("  ⇒ Ψ̂ 는 ½ 근처이나 **표류한다**(drift %.3f) — 당겨진 게 아니라 걸쳐 있을 뿐이다." % drift)
    else:
        print("  ⇒ **Ψ̂ 가 ½ 이 아니다** (|Ψ̂−½| = %.3f). A⇄G 항상성 주장은 이 런에서 성립하지 않는다." % off)

    # 그리고 절대 묻지 말아야 할 것
    em = [r.get("emit") for r in rows if "emit" in r and "stage" in r]
    if em:
        st = [(int(r["stage"]), 1 if r.get("emit") else 0) for r in rows if "stage" in r]
        hE = _im_h_given_S([e for _, e in st], [g for g, _ in st])
        print()
        print("  🚦 그런데 H(emit|stage) = %.6f nats — emit 은 stage 의 순수 함수다(H_9345)." % hE)
        if hE < 0.030:
            print("     ⇒ **Ψ̂ 가 무엇이든, 그것은 emit 결정으로 흐르지 않는다.** 데몬은")
            print("        ci_psi_balance 를 한 번도 부르지 않는다. 'tension 이 emit 을 Ψ=½ 로")
            print("        당긴다' 는 두 개의 무관한 사실을 이어붙인 것이다(H_9351 · H_9352).")

    # H_9356 Θ-SCOPE banner: on a0 wiring, ag_g_drive = -(1-emit_drive) = A's own complement,
    # so Θ is A's solo pulse, not A⇄G. The panel must say so — this repair swaps the population
    # (synthetic → real A-lanes), it does not swap A-solo → A⇄G.
    _garm = next((r.get("g_arm") for r in rows if r.get("g_arm")), "a0")
    if _garm == "a0":
        print()
        print("  ⚠️ Θ-SCOPE (H_9356 · g_arm=a0): ag_g_drive = A 의 여함수 ⇒ Θ 는 A⇄G 가 아니라 A 단독 맥박.")
    _sigma_from_trace(rows)
    return 0



def _tension_emit(argv):
    """DOES TENSION PULL EMIT? — the pre-registered bar for H_9352, and the trap it must dodge.

    H_9345 measured H(emit|stage) = 0.000000 over 2198 ticks: emit was a pure function of stage.
    H_9352 found why — the gate's `seconds_since_last` slot was fed a synthetic (stage, urgency)
    envelope, not elapsed time, so the one live term in the whole comparator was a stage clock.
    Plugging in the real clock makes emit vary again.

    ⚠️ AND THAT ALONE PROVES NOTHING. Making silence appear by moving a threshold is not a
    discovery — I moved it, not the tension. A rate limiter with a real clock will produce an
    emit rate near 1/(interval/tick) all by itself, and if the bar were "emit rate ≈ 1/2" it
    would pass on a coin. That is the p7 Goodhart shape exactly: an emit rate is FORM (tunable),
    the claim is BIND (must be earned).

    So the bar is conditional information, not rate:
        PASS  =  I(ag_conflict ; emit | stage)  >=  0.05 nats
                 AND  the tension-shuffle control  <=  0.01 nats
    C1 SHUFFLE permutes ag_conflict WITHIN each stage, which destroys the tension→emit link but
    preserves the emit rate and the stage structure. If the shuffled arm scores too, the number
    is coming from the rate, not from the tension, and the lever is theatre.

    🧱 ILL-POSED UNTIL chat.py:1563 IS REPAIRED (H_9356). The daemon has no independent G engine:
    ag_a_drive = emit_drive and ag_g_drive = -(1 - emit_drive) [chat.py:1562-1564], so
    ag_conflict = emit_drive * (1 - emit_drive) is a deterministic PARABOLA of the single scalar
    emit_drive. On a real clock-fixed trace, reconstructing ten_phasic from the emit_drive
    trajectory alone gives R^2 = 0.994. So `tension` here is A's OWN function measured against A's
    OWN emit gate — BOTH a PASS and a STILL-STAGE are wiring tautologies (engine-independent
    information = 0), not substrate facts. This panel prints its verdict but PREFIXES it with an
    ILL-POSED banner until ag_g_drive is fed an independent reverse observation (recon_err /
    pending_rel). Do not cement any tension→emit claim off this number while the banner stands."""
    import json as _json
    import random as _random
    paths = [a for a in argv if not a.startswith("--")]
    rows = []
    for f in paths:
        for line in open(f, "r", encoding="utf-8", errors="surrogateescape"):
            line = line.strip()
            if not line:
                continue
            try:
                r = _json.loads(line)
            except Exception:
                continue
            if "tick" in r and "stage" in r and "emit" in r and "agloop_ctx" in r:
                rows.append(r)
    mde = 0.05
    ctrl_bar = 0.01
    print("═══ TENSION→EMIT · I(ag_conflict ; emit | stage) ═══")
    print("  🧱 ILL-POSED (H_9356): 데몬에 독립 G 엔진이 없다 — ag_conflict = emit_drive·(1−emit_drive)")
    print("     [chat.py:1562-1564] = A 스칼라 하나의 결정론적 함수(재구성 R²=0.994). 여기 tension 은")
    print("     A 자신의 함수를 A 자신의 emit 게이트에 대고 재는 것 ⇒ 아래 판정은 🟢든 🧱든 배선")
    print("     tautology(engine-독립 정보량 0)이지 substrate 사실이 아니다. chat.py:1563 이 ag_g_drive")
    print("     를 독립 reverse 관측(recon_err/pending_rel)에서 받기 전엔 이 숫자로 cement 금지.")
    print("  traces=%d  ticks=%d" % (len(paths), len(rows)))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (tick < 200)")
        return 0
    S = [int(r["stage"]) for r in rows]
    E_ = [1 if r.get("emit") else 0 for r in rows]
    rate = sum(E_) / float(len(E_))
    hE = _im_h_given_S(E_, S)
    print("  발화율 = %.1f%%   H(emit|stage) = %.6f nats" % (100.0 * rate, hE))
    if hE < 0.030:
        print("  ⇒ ⛔ DECISION-CONSTANT — emit 이 아직 stage 의 순수 함수다. 시계가 안 꽂혔거나")
        print("     비교기가 여전히 포화다. tension 을 물을 수 없다(항등식으로 0).")
        return 0
    # ag_conflict 는 trace 에 직접 없다 — agloop_ctx 가 그 유래다(chat.py:1545-1550).
    # 데몬이 실제로 게이트에 흘려보내는 tension 축을 그대로 쓴다.
    tv = sorted(float(r["agloop_ctx"]) for r in rows)
    tmed = tv[len(tv) // 2]
    T = [1 if float(r["agloop_ctx"]) > tmed else 0 for r in rows]
    hT = _im_h_given_S(T, S)
    i_te = _im_cmi(T, E_, S)
    print("  H(tension|S) = %.4f nats   (tension = agloop_ctx 2-bin · ag_conflict 유래)" % hT)
    if hT < 0.030:
        print("  ⇒ ⛔ tension 채널이 죽어 있다 — 물을 수 없다.")
        return 0
    # C1 SHUFFLE — stage 안에서 tension 만 흩뜨린다(발화율·stage 구조는 보존)
    _r = _random.Random(7)
    null = []
    for _ in range(200):
        Tp = list(T)
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        for idx in st.values():
            vals = [Tp[k] for k in idx]
            _r.shuffle(vals)
            for j, k in enumerate(idx):
                Tp[k] = vals[j]
        null.append(_im_cmi(Tp, E_, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= i_te) + 1.0) / 201.0
    earned = i_te - nm
    print("  EXP  I(tension;emit|S) = %.5f nats" % i_te)
    print("  C1 SHUFFLE null = %.5f · perm-p = %.4f · EARNED = %+.5f nats" % (nm, pv, earned))
    print("     (stage 안에서 tension 만 흩뜨림 — 발화율과 stage 구조는 그대로 남는다.")
    print("      이 통제가 같이 점수를 내면 그 숫자는 tension 이 아니라 **발화율**에서 온 것이다.)")
    print()
    print("  🔒 사전등록 bar: EARNED ≥ %.2f nats ∧ C1 SHUFFLE ≤ %.2f nats" % (mde, ctrl_bar))
    if earned >= mde and nm <= ctrl_bar and pv < 0.005:
        print("  ⇒ 🟢 TENSION-PULLS-EMIT — 기질의 긴장이 발화 결정을 민다.")
    elif nm > ctrl_bar:
        print("  ⇒ ⛔ INVALID — 통제군이 bar 를 넘었다(%.5f > %.2f). 숫자가 발화율에서 온다." % (nm, ctrl_bar))
    elif abs(earned) < mde:
        print("  ⇒ 🧱 STILL-STAGE — 게이트가 다시 움직이긴 하나 **tension 은 안 민다**.")
        print("     시계를 꽂은 것은 emit 을 stage 에서 풀었을 뿐, tension 에 묶지는 않았다.")
        print("     (발화율이 ½ 근처여도 그건 레이트 리미터의 산술이지 항상성이 아니다 · p7)")
    else:
        print("  ⇒ 미달 · 판정 보류")
    return 0


def _gt_r2_indep(target, covs):
    """R2 of OLS target ~ [1, covs, covs^2]. High R2 = target is (a function of) the covariates =
    wiring-degenerate. Used by G-INDEP: ag_g_drive must NOT be reconstructable from emit_drive and
    the other lanes that already feed emit_drive, or the 'G engine' is just a second A (H_9356)."""
    import numpy as np
    y = np.asarray(target, dtype=float)
    n = len(y)
    if n < 8:
        return float("nan")
    cols = [np.ones(n)]
    for c in covs:
        a = np.asarray(c, dtype=float)
        cols.append(a)
        cols.append(a * a)
    X = np.column_stack(cols)
    beta, _res, _rk, _sv = np.linalg.lstsq(X, y, rcond=None)
    yh = X.dot(beta)
    ss_res = float(np.sum((y - yh) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0.0:
        return 1.0
    return max(0.0, 1.0 - ss_res / ss_tot)


def _gt_arm_panel(rows, mde, ctrl_bar):
    """Compute the four gates for one arm's rows. Returns a dict of measured quantities + PASS flags."""
    import random as _random
    S = [int(r["stage"]) for r in rows]
    E_ = [1 if r.get("emit") else 0 for r in rows]
    n = len(rows)
    rate = sum(E_) / float(n)
    hE = _im_h_given_S(E_, S)
    gd = [float(r.get("ag_g_drive", 0.0)) for r in rows]
    # G-VAR: min distinct(ag_g_drive) across source rollouts (a store with a constant key is dead).
    per_src = {}
    for r in rows:
        per_src.setdefault(r.get("_src", "?"), set()).add(round(float(r.get("ag_g_drive", 0.0)), 6))
    gvar_min = min(len(v) for v in per_src.values()) if per_src else 0
    # G-INDEP: reconstruct ag_g_drive from emit_drive + the lanes that feed emit_drive.
    covs = []
    for key in ("emit_drive", "phi", "rel_lane", "recon_err", "emit_env"):
        if all(key in r for r in rows):
            covs.append([float(r[key]) for r in rows])
    r2 = _gt_r2_indep(gd, covs) if covs else float("nan")
    # MI: I(ag_conflict; emit | stage), ag_conflict binarised at its median.
    cv = sorted(float(r.get("ag_conflict", 0.0)) for r in rows)
    cmed = cv[len(cv) // 2]
    C = [1 if float(r.get("ag_conflict", 0.0)) > cmed else 0 for r in rows]
    mi = _im_cmi(C, E_, S)
    _r = _random.Random(7)
    null = []
    for _ in range(200):
        Cp = list(C)
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        for idx in st.values():
            vals = [Cp[k] for k in idx]
            _r.shuffle(vals)
            for j, k in enumerate(idx):
                Cp[k] = vals[j]
        null.append(_im_cmi(Cp, E_, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= mi) + 1.0) / 201.0
    earned = mi - nm
    # Psi-hat on the daemon's OWN gws/lprec lanes (H_9351).
    psi = None
    if all(("psi_gws" in r and "psi_lprec" in r) for r in rows):
        emith = [1 if 0.5 * (float(r["psi_gws"]) + float(r["psi_lprec"])) >= 0.5 else 0 for r in rows]
        psi = sum(emith) / float(n)
    return dict(n=n, rate=rate, hE=hE, gvar=gvar_min, r2=r2, mi=mi, nm=nm, pv=pv,
                earned=earned, psi=psi, indep=(r2 == r2 and r2 < 0.5))


def _g_tension(argv):
    """DOES A GENUINELY-INDEPENDENT G ENGINE PULL EMIT? — H_9357, the sequel to H_9356.

    H_9356 proved the daemon's A⇄G tension was A alone: ag_g_drive = -(1-emit_drive), so
    ag_conflict was a deterministic parabola of one scalar, and --tension-emit was ill-posed.
    H_9357 wires ag_g_drive (behind cli/chat.py --g-arm) to the immune store's top-2 affinity
    GAP (d2, the one reverse quantity NOT already an input to emit_drive) and asks whether THAT
    2-engine tension pulls emit — with the controls MI alone cannot supply.

    Four arms (run cli/chat.py --g-arm a0|a1|a3; a2 is derived here by shuffling a1):
      A0  current wiring (the H_9356 tautology)      — MUST FAIL G-INDEP (proves the gate can fail)
      A1  REAL-G   = immune top-2 gap                — must PASS G-INDEP+G-VAR+MI
      A3  NOISE-G  = seeded per-tick PRNG            — the 'causal handle vs 2nd engine' separator

    Four gates:
      G-INDEP  R2(ag_g_drive ~ emit_drive + lanes + squares) < 0.5   (else INVALID-SECOND-A)
      G-VAR    min distinct(ag_g_drive) per rollout >= 5             (else INVALID-CONSTANT)
      MI       I(ag_conflict; emit | stage) >= 0.05 AND shuffle <= 0.01
      Psi-DV   |Psi_hat - 1/2| vs the H_9351 baseline 0.9167, and vs NOISE-G

    ⚠️ The verdict is CROSS-ARM, not a single number: A1 pulling emit MORE than A3 (noise wired
    the same causal way) is the only thing that separates 'a real second engine' from 'any handle
    on the conflict knob'. A1 ≈ A3 leaves the tension claim dead — that is the falsification."""
    paths = [a for a in argv if not a.startswith("--")]
    rows = _im_rows(paths)
    rows = [r for r in rows if ("tick" in r and "stage" in r and "emit" in r and "ag_g_drive" in r)]
    mde = 0.05
    ctrl_bar = 0.01
    print("═══ A⇄G INDEPENDENT-G TENSION → EMIT · H_9357 ═══")
    print("  rows=%d  traces=%d" % (len(rows), len(paths)))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200) — collect more chat --g-arm rollouts.")
        return 0
    by_arm = {}
    for r in rows:
        by_arm.setdefault(str(r.get("g_arm", "?")), []).append(r)
    print("  arms present: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(by_arm.items())))
    res = {}
    for arm in sorted(by_arm):
        res[arm] = _gt_arm_panel(by_arm[arm], mde, ctrl_bar)
    print()
    print("  arm | n    | rate | H(e|S) | G-VAR | G-INDEP R2 | MI(earned) perm-p | Ψ̂  |Ψ̂-½|")
    for arm in sorted(res):
        d = res[arm]
        psi_s = ("%.3f %.3f" % (d["psi"], abs(d["psi"] - 0.5))) if d["psi"] is not None else "  —"
        print("  %-3s | %4d | %.2f | %.4f | %5d | %.4f %-4s | %+.4f %.3f  | %s"
              % (arm, d["n"], d["rate"], d["hE"], d["gvar"], (d["r2"] if d["r2"] == d["r2"] else -1),
                 "OK" if d["indep"] else "FAIL", d["earned"], d["pv"], psi_s))
    print()
    # ── cross-arm verdict ──
    a0 = res.get("a0"); a1 = res.get("a1"); a3 = res.get("a3")
    if a0 is not None and a0["indep"]:
        print("  ⇒ ⛔ INVALID — the A0 (tautology) arm PASSED G-INDEP; the independence gate is broken.")
        return 0
    if a1 is None:
        print("  ⇒ ⛔ INCOMPLETE — no a1 (REAL-G) arm present. Run cli/chat.py --g-arm a1.")
        return 0
    if a1["gvar"] < 5:
        print("  ⇒ ⛔ INVALID-CONSTANT — a1 ag_g_drive has < 5 distinct values/rollout (dead store).")
        return 0
    if not a1["indep"]:
        print("  ⇒ 🧱 INVALID-SECOND-A — a1 ag_g_drive is reconstructable from emit_drive (R²≥0.5).")
        print("     I did not build an independent G; I built a second A. (H_9356 unbroken.)")
        return 0
    a1_pulls = (a1["earned"] >= mde and a1["nm"] <= ctrl_bar and a1["pv"] < 0.005)
    sep = None
    if a3 is not None:
        sep = a1["earned"] - a3["earned"]
    print("  🔒 prereg: A0 FAIL G-INDEP (gate live) ∧ A1 G-INDEP OK ∧ A1 MI≥%.2f/shuf≤%.2f ∧ A1≠A3" % (mde, ctrl_bar))
    if a1_pulls and (sep is None or sep > mde):
        print("  ⇒ 🟢 INDEPENDENT-TENSION-PULLS-EMIT — a genuine 2nd engine (immune d2) moves emit,")
        print("     and it moves it MORE than noise wired the same way (A1−A3 = %s)."
              % ("%.4f" % sep if sep is not None else "no A3"))
    elif a1["indep"] and not a1_pulls:
        print("  ⇒ 🧱 G-INERT — the independent G is wired and varies, but emit does NOT consume it")
        print("     (MI earned %.4f < %.2f). The wiring is real; the tension is not. Separate follow-on H." % (a1["earned"], mde))
    elif sep is not None and sep <= mde:
        print("  ⇒ 🧱 CAUSAL-HANDLE-ONLY — a1 pulls emit no more than noise-G (A1−A3=%.4f ≤ %.2f)." % (sep, mde))
        print("     ag_conflict is causally wired to emit, so ANY G signal lifts MI. Not a 2nd engine.")
    else:
        print("  ⇒ 미달 · 판정 보류")
    return 0


def _gd_cmi_bin(Xv, Yv, S, seed=7, nperm=200):
    """I(X;Y|stage) with median-binarized X and Y, plus a within-stage shuffle null on X
    (perm-debias). Returns (mi, null_mean, perm_p, earned). Y may already be 0/1 (emit_sim)."""
    import random as _random
    xs = sorted(Xv); xm = xs[len(xs) // 2]
    Xb = [1 if v > xm else 0 for v in Xv]
    ys = sorted(set(Yv))
    if len(ys) <= 2:
        Yb = [1 if v else 0 for v in Yv]
    else:
        ym = sorted(Yv)[len(Yv) // 2]
        Yb = [1 if v > ym else 0 for v in Yv]
    mi = _im_cmi(Xb, Yb, S)
    r = _random.Random(seed)
    null = []
    for _ in range(nperm):
        st = {}
        for k, g in enumerate(S):
            st.setdefault(g, []).append(k)
        Xp = list(Xb)
        for idx in st.values():
            vals = [Xp[k] for k in idx]
            r.shuffle(vals)
            for j, k in enumerate(idx):
                Xp[k] = vals[j]
        null.append(_im_cmi(Xp, Yb, S))
    nm = sum(null) / len(null)
    pv = (sum(1 for v in null if v >= mi) + 1.0) / (nperm + 1.0)
    return mi, nm, pv, mi - nm


def _gate_deaf(argv):
    """H_9360 GATE-DEAF SPLIT — is the emit gate's deafness to tension SATURATION (tunable) or
    STRUCTURE (the upstream mixing layer never loads tension onto the gate input)?

    H_9357 proved an independent G is wired but emit does NOT consume it (G-INERT). WHY? By the
    data-processing inequality, emit = should_emit(score) ∧ safe with safe ≡ clock (core/brain.py),
    so I(tension; emit) ≤ I(tension; score | stage). Therefore whether `score` already carries
    tension DECIDES saturation-vs-structure — with NO gate edit ($0, on the existing traces).

    M_score = I(ag_conflict ; score | stage)      does the gate INPUT carry tension?
    M_sim   = I(ag_conflict ; emit_sim | stage)   desaturated-gate offline sim: θ = median(score)
              on the CALIBRATION rollouts (score marginal only — tension- and emit-blind), then
              emit_sim = 1[score > θ] ∧ (secs_since_emit ≥ 30) on the JUDGMENT rollouts.
    Spike-in control: I(score ; emit_sim | stage) MUST be large (emit_sim ≡ f(score)); if it is
    not, the estimator is broken and the whole panel is INVALID.

    Verdict is on arm a1 (the real independent G), gated on a1 > a3 (else instrument INVALID):
      M_score ≥0.05 ∧ M_sim ≥0.05  → (a)  SATURATION — info reaches the gate input; threshold 0.3
                                          saturates and discards it. Fix is live recalibration.
      M_score ≥0.05 ∧ M_sim ≤0.01  → (a′) BINARY-FORM bottleneck — no threshold can carry it; a
                                          graded gate is needed (structure, but LOCAL to the gate).
      M_score ≤0.01 (TOST equiv)   → (b)  STRUCTURE — the mixing layer never loads tension onto the
                                          gate input; the gate is INNOCENT and no rewire helps (DPI).
      0.01 < M_score < 0.05        → PENDING — report MDE, extend n; never declare 'none'.
    """
    mde = 0.05
    ctrl_bar = 0.01
    rows = _im_rows(argv)
    rows = [r for r in rows if all(k in r for k in ("stage", "score", "ag_conflict", "secs_since_emit", "g_arm"))]
    print("═══ GATE-DEAF SPLIT · H_9360 · DPI: I(tension;emit) ≤ I(tension;score|stage) ═══")
    print("  rows=%d" % len(rows))
    if len(rows) < 200:
        print("  ⇒ ⛔ NOT-POWERED (rows < 200)")
        return 0
    by = {}
    for r in rows:
        by.setdefault(str(r["g_arm"]), []).append(r)
    print("  arms: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in sorted(by.items())))
    res = {}
    for arm, ar in sorted(by.items()):
        S = [int(r["stage"]) for r in ar]
        AC = [float(r["ag_conflict"]) for r in ar]
        SC = [float(r["score"]) for r in ar]
        # M_score
        m_sc, m_sc_nm, m_sc_pv, m_sc_e = _gd_cmi_bin(AC, SC, S, seed=7)
        # desaturated-gate sim: split rollouts into calibration / judgment halves
        srcs = sorted({r.get("_src", "?") for r in ar})
        half = max(1, len(srcs) // 2)
        calib = set(srcs[:half])
        cal_scores = [float(r["score"]) for r in ar if r.get("_src") in calib]
        cs = sorted(cal_scores)
        theta = cs[len(cs) // 2] if cs else 0.0
        # The desaturation question is only meaningful on CLOCK-PERMITTED ticks (secs≥30): on
        # clock-blocked ticks emit is forced silent regardless of score, so tension cannot move it
        # (that is the rate limiter, not the gate). Condition M_sim + the spike-in on secs≥30 so
        # emit_sim = 1[score>θ] purely — otherwise the clock gate masks score and the spike-in
        # (which must be large since emit_sim ≡ f(score) here) reads ~0 and the panel self-INVALIDs.
        jr = [r for r in ar if r.get("_src") not in calib and float(r.get("secs_since_emit", 0.0)) >= 30.0]
        Sj = [int(r["stage"]) for r in jr]
        ACj = [float(r["ag_conflict"]) for r in jr]
        SCj = [float(r["score"]) for r in jr]
        emit_sim = [1 if float(r["score"]) > theta else 0 for r in jr]
        m_sim, m_sim_nm, m_sim_pv, m_sim_e = _gd_cmi_bin(ACj, emit_sim, Sj, seed=11) if len(jr) >= 40 else (0.0, 0.0, 1.0, 0.0)
        # spike-in: I(score; emit_sim | stage) must be large (emit_sim = 1[score>θ] by construction)
        spike = _gd_cmi_bin(SCj, emit_sim, Sj, seed=13)[0] if len(jr) >= 40 else 0.0
        rate_sim = sum(emit_sim) / float(len(emit_sim)) if emit_sim else 0.0
        res[arm] = dict(n=len(ar), n_clk=len(jr), m_sc=m_sc_e, m_sc_pv=m_sc_pv, m_sim=m_sim_e,
                        m_sim_pv=m_sim_pv, spike=spike, theta=theta, rate_sim=rate_sim, rows=ar)
    print()
    print("  arm | n   | n_clk | M_score(earn) p | M_sim(earn) p | spike I(sc;sim|S) | θ")
    for arm in sorted(res):
        d = res[arm]
        print("  %-3s | %3d | %5d | %+.4f %.3f    | %+.4f %.3f   | %.4f            | %.3f"
              % (arm, d["n"], d["n_clk"], d["m_sc"], d["m_sc_pv"], d["m_sim"], d["m_sim_pv"], d["spike"], d["theta"]))
    print()
    a1 = res.get("a1"); a3 = res.get("a3")
    if a1 is None:
        print("  ⇒ ⛔ INCOMPLETE — no a1 (REAL-G) arm.")
        return 0
    if a1["n_clk"] < 40:
        print("  ⇒ ⏳ PENDING — a1 clock-permitted rows n_clk=%d < 40; M_sim/spike underpowered." % a1["n_clk"])
        print("     M_score=%.4f is still readable; extend traces (more rollouts) for the M_sim leg." % a1["m_sc"])
        return 0
    if a1["spike"] < 0.05:
        print("  ⇒ ⛔ INVALID — spike-in control failed (I(score;emit_sim|stage)=%.4f < 0.05):" % a1["spike"])
        print("     emit_sim is a function of score by construction; a dead spike-in = broken estimator.")
        return 0
    if a3 is not None and a3["m_sc"] >= a1["m_sc"] and a1["m_sc"] >= mde:
        print("  ⇒ ⛔ INVALID — noise arm a3 M_score ≥ a1 (%.4f ≥ %.4f); instrument not selective." % (a3["m_sc"], a1["m_sc"]))
        return 0
    # ── PEDESTAL-CORRECTED Δ_G (H_9360 · Fable-designed) ──────────────────────────────────────
    # The estimator's zero-point is NOT 0: the noise arm a3 reads M_score>0 too, because a3's
    # ag_conflict still carries A-side info (a3 only replaces the G pole with noise). So the signal
    # is Δ vs the control (measurement meta-law), not raw: Δ_G = M_score(a1) − M_score(a3) = the
    # INDEPENDENT-G component loaded onto score. Read it with a rollout-level df (tick permutation
    # is anti-conservative — ticks within a rollout autocorrelate; the replication unit is rollout).
    import math as _math

    def _msc(rws):
        return _gd_cmi_bin([float(r["ag_conflict"]) for r in rws], [float(r["score"]) for r in rws],
                           [int(r["stage"]) for r in rws], seed=7)[3]

    def _jackknife(rws):
        by_r = {}
        for r in rws:
            by_r.setdefault(r.get("_src", "?"), []).append(r)
        keys = sorted(by_r)
        k = len(keys)
        if k < 4:
            return 0.0, k
        loo = []
        for i in range(k):
            sub = [r for j, kk in enumerate(keys) if j != i for r in by_r[kk]]
            loo.append(_msc(sub))
        mbar = sum(loo) / k
        var = (k - 1.0) / k * sum((v - mbar) ** 2 for v in loo)
        return _math.sqrt(max(0.0, var)), k

    def _block_floor(rws, seed=29, nperm=200):
        # true-0 pedestal: reassign ag_conflict by WHOLE ROLLOUT (preserve within-rollout
        # autocorrelation, break only the a1↔score pairing). earned≈0 is the artifact floor.
        import random as _random
        by_r = {}
        for r in rws:
            by_r.setdefault(r.get("_src", "?"), []).append(r)
        keys = sorted(by_r)
        blocks_ac = [[float(r["ag_conflict"]) for r in by_r[kk]] for kk in keys]
        base_sc = [[float(r["score"]) for r in by_r[kk]] for kk in keys]
        base_st = [[int(r["stage"]) for r in by_r[kk]] for kk in keys]
        rr = _random.Random(seed)
        vals = []
        for _ in range(nperm):
            perm = list(range(len(keys)))
            rr.shuffle(perm)
            A, Sc, St = [], [], []
            for i in range(len(keys)):
                m = min(len(blocks_ac[perm[i]]), len(base_sc[i]))
                A += blocks_ac[perm[i]][:m]
                Sc += base_sc[i][:m]
                St += base_st[i][:m]
            vals.append(_gd_cmi_bin(A, Sc, St, seed=31)[3])
        return sum(vals) / len(vals)

    se1, k1 = _jackknife(a1["rows"])
    se3, k3 = _jackknife(a3["rows"]) if a3 is not None else (0.0, 0)
    dg = a1["m_sc"] - (a3["m_sc"] if a3 is not None else 0.0)
    se_dg = _math.sqrt(se1 * se1 + se3 * se3)
    floor = _block_floor(a1["rows"])
    # full-resolution C (channel ceiling · report only, not a gate input)
    C = _gd_cmi_bin([float(r["ag_conflict"]) for r in a1["rows"]],
                    [round(float(r["score"]), 4) for r in a1["rows"]],
                    [int(r["stage"]) for r in a1["rows"]], seed=17)[3]
    eq = 0.01                         # equivalence limit (pedestal-referenced Δ, registered pre-look)
    ci_lo, ci_hi = dg - 1.645 * se_dg, dg + 1.645 * se_dg    # 90% CI for TOST
    print("  🔒 prereg (Δ_G = M_score(a1)−M_score(a3) · rollout-df · TOST ±%.2f · a3 = pedestal):" % eq)
    print("     Δ_G = %+.4f · SE_jk = %.4f (k=%d) · 90%%CI [%+.4f, %+.4f]" % (dg, se_dg, min(k1, k3), ci_lo, ci_hi))
    print("     block-perm true-0 floor = %+.4f (must be ≈0) · C=I(conflict;score|S) full-res = %.4f · M/C=%.2f" % (floor, C, (a1["m_sc"] / C if C > 0 else 0.0)))
    if abs(floor) > eq:
        print("  ⇒ ⛔ INVALID — block-perm floor |%.4f| > %.2f: the estimator has an artifact floor above the equivalence limit." % (floor, eq))
    elif ci_hi <= eq and ci_lo >= -eq:
        print("  ⇒ 🧱 (b)-for-G — the independent G's tension does NOT pass the score bottleneck")
        print("     (Δ_G equivalent to 0 within ±%.2f · TOST). This IS the mechanism of H_9357 G-INERT:" % eq)
        print("     score barely carries G, so emit has nothing to consume. Frontier = the ag_conflict→score")
        print("     mixer (ag_budget∈{4..6} integer-ratio ×0.10 quantization), NOT the gate.")
    elif ci_lo > 0.0:
        print("  ⇒ 🟢 weak-(a) — Δ_G = %+.4f > 0 (90%%CI excludes 0): the independent G IS loaded onto" % dg)
        print("     score, weakly. NEXT = Stage-1 desaturation lane (anima-py chat --gate-calib).")
    else:
        mde = (1.645 + 1.28) * se_dg * _math.sqrt(2.0)
        print("  ⇒ ⏳ PENDING — Δ_G=%+.4f neither equivalent-to-0 nor >0. MDE≈%.4f." % (dg, mde))
        print("     %s" % ("MDE > eq: n underpowered → regenerate arms." if mde > eq else "MDE ≤ eq: shape ambiguous → re-examine."))
    return 0


def _collide_select(ckpt, argv):
    """DOES A⇄G COLLISION SELECT EMERGENCE? — H_9362, the generation-selection sequel to H_9357.

    H_9357 asked whether tension pulls EMIT (the 1-bit shadow) and got G-INERT. H_9362 moves to
    the SELECTION axis: over a fixed pool of K candidates per recombination probe, does the A⇄G
    collision pick the recombination target better than fluency-alone or noise?

    The drives (generator.py conflict_drives_live): a = clip01(1-CE/5) fluency, g = ±immune margin.
    G-A (H_9362, engine_cli.py:643 margin=recon_err-recall_thr, >0=abstain) locked the sign:
    novel -> margin>0 -> g<0; recognized -> margin<=0 -> g>0. So the emergence candidate
    (fluent AND novel) is (a>0, g<0), and conflict_scalar (opposite-sign -> a*|g|) is exactly the
    "fluent AND novel" product -- HIGH for emergence, 0 for echo (a>0,g>0), ~0 for garbage (a~0).
    The daemon's live path uses argMIN conflict_scalar (generator.py:815) -> it DISCARDS emergence.

    Arms (same fixed pool, K fixed, selection rule only differs):
      S0        argmin conflict_scalar  (the current daemon rule -- avoids emergence)
      S_emerge  argmax conflict_scalar  (the hypothesis: A*G collision selects emergence)
      SECOND-A  argmax a                (fluency alone -- the H_9356 "second A" control)
      NOISE-G   argmax conflict_scalar with g permuted across candidates (causal-handle control)
      UNIFORM   candidate 0             (floor)

    Gates: G-B pool occupancy (how many candidates land in the emergence quadrant a>0,g<0 -- if ~0
    the pool is DRY and no selector can find what is not there, H_9304 prediction) then G-C the
    per-arm recombination hit-rate scored by the FROZEN rho_weave target check (arm-relative judge
    only, recomb-gate4: route != generation, no top-1 terminal claim)."""
    import random as _random
    sys.path.insert(0, "core")
    import generator as _gen
    from engine_cli import (immune_memory_new_text, immune_memory_bind_text,
                            conflict_scalar as _cs, EngineConfig)
    import rho_axon as _rx
    K = 4
    for a in argv:
        if a.startswith("--k="):
            K = int(a.split("=", 1)[1])
    mouth = _Mouth(ckpt)
    cfg = EngineConfig(True, "conv", False, False)
    # G-store: bind the compose CUES as "seen context" (H_9337 recognition-first). The composed
    # TARGET is never bound, so a real recombination candidate reads as novel (g<0).
    pairs = _rx._WEAVE
    mem = immune_memory_new_text(pairs[0][0], 0.5, 256)
    for cue, tgt, sw, bs, lang in pairs:
        mem = immune_memory_bind_text(mem, cue[:64], cue, cfg)
    print("=== A\u21c4G COLLISION-SELECTS-EMERGENCE \u00b7 H_9362 \u00b7 --collide-select ===")
    print("  ckpt=%s  probes=%d  K=%d" % (ckpt.split("/")[-1], len(pairs), K))
    # build the shared candidate pool per probe + drives
    perm_rng = _random.Random(7)
    rows = []          # per (probe, cand): dict(a, g, cs, retr)
    occ = {"emerge": 0, "echo": 0, "garbage": 0, "other": 0}
    for i, (cue, tgt, sw, bs, lang) in enumerate(pairs):
        pool = []
        for k in range(K):
            txt = mouth.ideate(cue + " ", 24, 8, 0.7, _rx.SEEDS[0] + 17 * i + k)
            d = _gen.conflict_drives_live(ckpt, txt, mem)
            a, g = float(d[0]), float(d[1])
            retr = 1 if _rx._retrieved(txt, tgt) else 0
            pool.append(dict(txt=txt, a=a, g=g, cs=_cs(a, g), retr=retr))
            q = ("emerge" if (a > 0.05 and g < -0.05) else "echo" if (a > 0.05 and g > 0.05)
                 else "garbage" if a <= 0.05 else "other")
            occ[q] += 1
        rows.append(pool)
    npool = sum(len(p) for p in rows)
    # ── G-B pool occupancy ──
    print()
    print("  \u2500\u2500 G-B \ud480 \uc810\uc720 (\ucc3d\ubc1c \uc0ac\ubd84\uba74 a>0,g<0) \u2500\u2500")
    print("    emergence(a>0,g<0)=%d  echo(a>0,g>0)=%d  garbage(a\u22480)=%d  other=%d  / %d cand"
          % (occ["emerge"], occ["echo"], occ["garbage"], occ["other"], npool))
    emerge_frac = occ["emerge"] / float(npool) if npool else 0.0
    if occ["emerge"] == 0:
        print("    \u21d2 \U0001f9f1 POOL-DRY \u2014 \ucc3d\ubc1c \uce78 \uc810\uc720 0. \uc5b4\ub5a4 \uc120\ud0dd\uae30\ub3c4 \uc5c6\ub294 \uac83\uc744 \ubabb \uace0\ub978\ub2e4(H_9304 DATA \ubcbd). G-C \ubb34\uc758\ubbf8.")
        print("    \ub2e4\uc74c \ub808\ubc84 = A \uc81c\uc548\ubd84\ud3ec(XBIND curriculum), G \uc120\ud0dd\uae30 \uc544\ub2d8.")
        return 0
    # ── G-C per-arm hit-rate ──
    def sel(pool, rule):
        if rule == "s0":       return min(pool, key=lambda c: c["cs"])
        if rule == "emerge":   return max(pool, key=lambda c: c["cs"])
        if rule == "second_a": return max(pool, key=lambda c: c["a"])
        if rule == "uniform":  return pool[perm_rng.randrange(len(pool))]
        if rule == "noise_g":
            gs = [c["g"] for c in pool]
            perm_rng.shuffle(gs)
            jbest = max(range(len(pool)), key=lambda j: _cs(pool[j]["a"], gs[j]))
            return pool[jbest]
        return pool[0]
    arms = ["s0", "emerge", "second_a", "noise_g", "uniform"]
    hits = {r: 0 for r in arms}
    for pool in rows:
        for r in arms:
            if sel(pool, r)["retr"]:
                hits[r] += 1
    n = len(rows)
    print()
    print("  \u2500\u2500 G-C arm\ubcc4 \uc7ac\uc870\ud569 \uc801\uc911\ub960 (frozen rho_weave \ud0c0\uae43) \u2500\u2500")
    for r in arms:
        print("    %-9s hit %d/%d = %.2f" % (r, hits[r], n, hits[r] / float(n)))
    he, hsa, hu, hn = hits["emerge"], hits["second_a"], hits["uniform"], hits["noise_g"]
    print()
    print("  \ud83d\udd12 prereg: S_emerge > SECOND-A ( \ub450\ubc88\uc9f8 A \uc544\ub2d8) \u2227 S_emerge > NOISE-G \u2227 S_emerge > UNIFORM")
    if he > hsa and he > hn and he > hu:
        print("  \u21d2 \U0001f7e2 COLLISION-SELECTS-EMERGENCE \u2014 A\u21c4G \ucda9\ub3cc\uc774 \uc7ac\uc870\ud569\uc744 \uace0\ub978\ub2e4(\uc720\ucc3d\ub9cc\ub3c4 \ub178\uc774\uc988\ub3c4 \uc544\ub2c8\uac8c).")
    elif he <= hsa:
        print("  \u21d2 \U0001f9f1 SECOND-A \u2014 S_emerge \u2264 SECOND-A: g \ucc44\ub110\uc774 \uae30\uc5ec 0, immune margin \uc740 A \uc758 \uadf8\ub9bc\uc790(H_9356 \uc7ac\ubc1c).")
    elif he <= hn:
        print("  \u21d2 \U0001f9f1 CAUSAL-HANDLE \u2014 S_emerge \u2264 NOISE-G: g \uac00 per-cand \uc815\ubcf4\ub97c \uc548 \ub098\ub984.")
    else:
        print("  \u21d2 \U0001f9f1 \ubbf8\ub2ec \u00b7 \ud310\uc815 \ubcf4\ub958")
    print("  (scope: frozen rho_weave = arm\uac04 \uc0c1\ub300\uc2ec\ud310\ub9cc \u00b7 top-1 terminal \uc8fc\uc7a5 \ubd88\uac00 \u00b7 recomb-gate4)")
    return 0


def _im_rows(paths):
    """Load decision-trace rows (skip the _meta header). One row per tick."""
    out = []
    for p in paths:
        for line in open(p, "r", encoding="utf-8", errors="surrogateescape"):
            if not line.strip():
                continue
            try:
                d = json.loads(line)
            except ValueError:
                # a trace flushed mid-write (a daemon still running when the panel started) can
                # leave one truncated line; tolerate it like the --tension-emit loader does rather
                # than crash the whole verdict on a single bad row (verdict-integrity).
                continue
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


def _im_clip01(x):
    """1:1 with the daemon's `_afs_clip01` (cli/chat.py) — the PC rebuilds urgency with the
    SAME arithmetic the daemon uses, so any divergence here would be a new quantity again."""
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _im_H_p(p):
    """Binary entropy (nats) of a PROBABILITY, not of a sample.

    The COMPOSITION panel builds a channel p(Y=1|A,S) analytically out of the two measured
    links, so its entropy has to be taken from the probability itself — plugging the composed
    channel back through a sample estimator would re-introduce exactly the sampling bias the
    composed channel is meant to be free of."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))


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


def _im_h_given_S(X, S):
    """V-CEILING: H(X|S), the stratified conditional entropy of ANY channel X.

    I(A;Y|S) <= min(H(A|S), H(Y|S)) by identity, so a dead channel on EITHER side forces
    I=0 by definition, not by measurement. H_9308 died on the ACTION side (H(A|S)=0). The
    OUTCOME side is the same trap wearing the other hat: if the stage already determines
    the next-tick score, then Y is a function of S and I is 0 no matter what the mouth
    says. Gate BOTH before reading I (convergence interact-mi-py-2)."""
    n = len(S)
    if n == 0:
        return 0.0
    strata = {}
    for i in range(n):
        strata.setdefault(S[i], []).append(i)
    return sum((float(len(idx)) / n) * _im_H([X[i] for i in idx]) for idx in strata.values())


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
    nxt_gate = {}
    for src, rs in by_src.items():
        rs.sort(key=lambda r: int(r["tick"]))
        for i in range(len(rs) - 1):
            nxt[(src, int(rs[i]["tick"]))] = float(rs[i + 1]["score"])
            # V5 needs the bookkeeping of the tick that PRODUCED Y, not the one that spoke.
            nxt_gate[(src, int(rs[i]["tick"]))] = (int(rs[i + 1]["stage"]),
                                                   rs[i + 1].get("safe"))
    use = [r for r in emits if (r["_src"], int(r["tick"])) in nxt]
    if len(use) < 30:
        print("  ⇒ NOT-POWERED (next-tick score 있는 emit-tick < 30)")
        return 0
    ys = sorted(nxt[(r["_src"], int(r["tick"]))] for r in use)
    med = ys[len(ys) // 2]
    A = [int(r["a_fold8"]) for r in use]
    S = [int(r["stage"]) for r in use]
    Y = [1 if nxt[(r["_src"], int(r["tick"]))] > med else 0 for r in use]
    # ── V-CEILING · BOTH channels (BLOCKING · before any I is read) ────────────────
    # I(A;Y|S) <= min(H(A|S), H(Y|S)) is an IDENTITY. A dead channel on either side pins
    # I to 0 by definition. Gating only the action side (as this did until interact-mi-py-2)
    # leaves the outcome side wide open: if the stage already fixes the next-tick score,
    # a null reads as "the loop carries no information" when it actually reads "we asked a
    # question whose answer was already written". Both, or neither.
    hA = _im_h_given_S(A, S)
    hY = _im_h_given_S(Y, S)
    print("  🚦 V-CEILING  H(A|S) = %.4f nats · H(Y|S) = %.4f nats   (floor %.3f = 3×MDE)"
          % (hA, hY, hfloor))
    if hA < hfloor:
        print("  ⇒ NOT-POWERED — 행동 채널이 죽어 있다. I 는 정의상 0 이지 측정된 0 이 아니다.")
        print("     (H_9308 이 정확히 여기서 죽었다 · convergence interact-mi-py-1)")
        return 0
    if hY < hfloor:
        print("  ⇒ NOT-POWERED — 결과 채널이 죽어 있다(다음-tick score 가 stage 로 이미 결정됨).")
        print("     I 는 정의상 0 — 입이 무엇을 말했든 물을 수 있는 질문이 아니었다.")
        print("     (같은 항등식의 반대쪽 축 · convergence interact-mi-py-2)")
        return 0
    # ── V5 · GATE-CLOSED (the FIFTH identity-zero · BLOCKING · H_9337 frozen bar) ──────
    # H(Y|S) alive is NOT enough. The gate's own inputs are stage AND the rate-limiter
    # (`safe`). If emit is fully determined by (stage, safe), then Y is a function of the
    # gate's own bookkeeping and STILL-ADDITIVE is settled BEFORE the mouth opens — again
    # by definition, not by measurement. That is a different claim from "the loop carries
    # no information": it says THE GATE LOOKS AT NOTHING. H_9100 (motivation saturated at
    # floor ~0.7, always clearing the 0.3 threshold) and H_9209/9225/9230 (every read-side
    # emit wiring = THEATER, ΔEff 0/120) predict exactly this shape, so it must be its own
    # verdict, not folded into the wall.
    #
    # ⚠️ CONDITION ON THE TICK THAT PRODUCED Y, NOT THE ONE THAT SPOKE. Y is score_{t+1}, so
    # the gate bookkeeping that could already have written it is (stage_{t+1}, safe_{t+1}).
    # Stratifying by the SPEAKING tick's (stage, safe) is a different question and cannot
    # detect the trap — a synthetic arm with Y := f(stage_{t+1}, safe_{t+1}) sailed straight
    # through that version of the gate. Conditioning here is safe from the mediator trap
    # because `safe` is a rate-limiter over WHETHER/WHEN the daemon spoke — it is not a
    # descendant of A, which is WHAT it said (the H_9257 content axis).
    sf = [nxt_gate[(r["_src"], int(r["tick"]))][1] for r in use]
    if all(v is not None for v in sf):
        svals = sorted(float(v) for v in sf)
        smed = svals[len(svals) // 2]
        SG = [(nxt_gate[(r["_src"], int(r["tick"]))][0],
               1 if float(nxt_gate[(r["_src"], int(r["tick"]))][1]) > smed else 0) for r in use]
        hYg = _im_h_given_S(Y, SG)
        print("  🚦 V5 GATE     H(Y|S,safe) = %.4f nats   (floor %.3f · safe = rate-limit lane)"
              % (hYg, hfloor))
        if hYg < hfloor:
            print("  ⇒ ⛔ GATE-CLOSED — 게이트가 **아무것도 안 본다**(emit 이 stage+safe 로 완전결정).")
            print("     이건 🧱 가 아니다. '폐루프가 정보를 안 나른다'가 아니라 '게이트에 물어볼 수")
            print("     있는 질문이 없다' — STILL-ADDITIVE 는 입이 열리기 전에 이미 확정돼 있었다.")
            print("     다음 물음은 '루프가 나르는가'가 아니라 '게이트가 무엇을 보게 할 수 있는가'다.")
            return 0
    else:
        print("  🚦 V5 GATE     safe 미기록 trace ⇒ SKIP (구 포맷 · GATE-CLOSED 를 배제할 수 없음)")
    # ── V6 · DECISION-CHANNEL (the SIXTH identity-zero · H_9345) ──────────────────────
    #
    # Every gate above asks whether the PROXY (score) has room. None of them asks whether the
    # DECISION does. Measured on 70 rollouts x 2198 ticks: H(emit|stage) = 0.000000 EXACTLY —
    # stages 0/1/4 emit 100% of the time, stages 2/3 are silent 100% of the time, and the
    # silence lands on ticks 9-10 in every single rollout. emit/silence is a PURE FUNCTION OF
    # STAGE. So I(anything ; emit | stage) = 0 BY IDENTITY, and the question "does what the
    # substrate says inform its next DECISION" has no decision to inform.
    #
    # This does not invalidate a score-based readout — score genuinely varies. It BOUNDS it:
    # a verdict on `score` is a verdict on a lane the gate consumes, NOT on the gate's output.
    # Say so, or you will write "the loop does not inform the next decision" when what you
    # measured was a proxy and the decision was a clock.
    emx = [r.get("emit") for r in rows]
    if all(v is not None for v in emx):
        Sall = [int(r["stage"]) for r in rows]
        hEmit = _im_h_given_S([1 if v else 0 for v in emx], Sall)
        rate = sum(1 for v in emx if v) / float(len(emx))
        print("  🚦 V6 DECISION H(emit|S) = %.6f nats   (발화율 %.1f%% · n=%d tick 전수)"
              % (hEmit, 100.0 * rate, len(emx)))
        if hEmit < hfloor:
            print("     ⇒ ⛔ **DECISION-CONSTANT** — emit/침묵이 stage 의 **순수 함수**다.")
            print("        I(무엇이든 ; emit | S) ≤ H(emit|S) ≈ 0 ⇒ **어떤 변수도 결정에 정보를**")
            print("        **나를 수 없다 — 측정 이전에, 정의상.** 게이트는 게이트가 아니라 시계다(H_9345).")
            print("        아래 판정은 **대리변수(score)에만 스코프**된다 — 게이트의 출력이 아니라")
            print("        게이트가 소비하는 lane 에 대한 것이다. '다음 결정에' 로 확장하지 마라.")
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

    # ── MEDIATION · 사슬을 열어본다 (진단 · 헤드라인 아님) ──────────────────────────
    # 헤드라인 I(A;Y|S) 는 사슬의 두 끝만 잰다. 그 사이에는 실제 배선이 있다:
    #
    #     [기질이 뱉은 말] ──▶ [afield] ──▶ [ score ] ──▶ [emit 게이트]
    #        A (a_fold8)      recon_err      Y (2-bin)
    #
    # emit tick 에서 g_text 는 afield step 에 들어가고 그 결과가 recon_err 다. 즉 recon_err
    # 는 "말이 장(場)을 밀었는가"의 직접 관측이고, 데몬이 tick 마다 이미 기록한다.
    # A→Y 가 0 일 때 두 세계가 갈린다:
    #   ① M1(A→recon_err) 도 0  ⇒ 말이 장조차 못 민다. 주입이 무효 = 계기/배선 문제.
    #   ② M1 은 살고 M2(recon_err→Y) 가 0  ⇒ 말은 장을 미는데 **게이트가 그걸 안 본다**.
    #      이건 H_9209/H_9225/H_9230 이 read-side 배선에서 반복해 만난 THEATER 그림과 합류한다
    #      (emit = stage + rate-limit 지배). 그렇다면 null 은 고립된 사실이 아니라 그 벽의 목격이다.
    # 둘 다 같은 C1 순열 귀무(실측 단위) 위에서 잰다. 진단이므로 verdict 를 바꾸지 않는다.
    #
    # ⏱️ THE LAG IS PART OF THE WIRING — take the mediators from the tick that PRODUCED Y.
    # The daemon reads a 1-tick-lagged prediction error (chat.py: `pending_recon` is written
    # at the emit site of tick t and READ at tick t+1), so the causal chain is
    #     A_t ──▶ recon_err_{t+1} ──▶ score_{t+1} (= Y)
    # A row's OWN `recon_err` is the error of the PREVIOUS utterance A_{t-1}, and it feeds
    # score_t, not Y. Reading the same row's mediator therefore misses by exactly one tick in
    # BOTH links: M1 would compare A_t against A_{t-1}'s error, and M2 would ask a mediator
    # that already spent itself on score_t to explain score_{t+1}. A synthetic arm with
    # score := f(recon_err) at the same tick read M2 as DEAD under that version — the
    # instrument could not see a channel that was planted by construction. The headline
    # I(A_t; score_{t+1}|S) had the lag right; the whole diagnostic panel had it wrong, and a
    # null would have read as "the text never even reaches the field".
    # NB: `by_src` is rebound to an index map by the autocorrelation block above — rebuild
    # the row map under its own name rather than reusing a name the code already spent.
    rows_by_src = {}
    for r in rows:
        rows_by_src.setdefault(r["_src"], []).append(r)
    nxt_lane = {}
    for src, rs in rows_by_src.items():
        rs.sort(key=lambda r: int(r["tick"]))
        for i in range(len(rs) - 1):
            nxt_lane[(src, int(rs[i]["tick"]))] = rs[i + 1]
    rec = [nxt_lane[(r["_src"], int(r["tick"]))].get("recon_err") for r in use]
    if any(v is None for v in rec):
        print("  ── MEDIATION: recon_err 미기록 trace ⇒ SKIP (구 trace 포맷)")
        return 0
    rs = sorted(float(v) for v in rec)
    rmed = rs[len(rs) // 2]
    R = [1 if float(v) > rmed else 0 for v in rec]
    hR = _im_h_given_S(R, S)
    print("  ── MEDIATION (진단 · verdict 불변) ─────────────────────────────")
    print("     H(R|S) = %.4f nats   R = recon_err 2-bin (afield 뿌리 · g_text 가 직접 민다)" % hR)
    if hR < hfloor:
        print("     ⇒ 매개 채널 자체가 죽어 있다 — M1/M2 는 정의상 0. 사슬을 못 연다.")
    for nm, X, Z in ((("M1  A→R (말이 장을 미는가)", A, R), ("M2  R→Y (장이 게이트를 미는가)", R, Y))
                     if hR >= hfloor else ()):
        i_xz = _im_cmi(X, Z, S)
        null = []
        for _ in range(perm):
            Xp = list(X)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Xp[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Xp[k] = vals[j]
            null.append(_im_cmi(Xp, Z, S))
        nm_ = sum(null) / len(null)
        pv = (sum(1 for v in null if v >= i_xz) + 1.0) / (perm + 1.0)
        earned = i_xz - nm_
        tag = "🔗 LIVE" if (earned >= mde and pv < 0.005) else ("· 등가(0)" if abs(earned) <= mde else "· 미달")
        print("     %-28s EARNED = %+.5f nats · perm-p = %.4f   %s" % (nm, earned, pv, tag))
    print("     ⇒ M1 살고 M2 죽으면: 말은 장을 밀지만 **게이트가 안 본다**(read-side THEATER 합류).")
    print("        M1 도 죽으면: 주입 자체가 장에 안 닿는다(배선/계기 의심 — 기질 주장 금지).")
    print("     ⚠️ 사다리의 한계 둘: (a) R 은 2-bin ⇒ M2 죽음의 스코프는 '게이트가 R 을 1-bit")
    print("        해상도에서 안 읽는다'까지다. (b) M1·M2 가 **둘 다 살아도** end-to-end I=0 일 수")
    print("        있다 — 쌍별 MI 는 합성되지 않는다(나르는 성분 ≠ 쓰는 성분).")

    # ── B1 · BOOKKEEPING (H_9337 frozen bar · guards the 🟢 강한 독법) ────────────────
    # If R is a deterministic function of (A, S), then "recognition error" is not a percept
    # at all — it is a LEDGER, an arithmetic restatement of what the mouth just said. Then
    # I(A;Y|S) > 0 is not a discovery, it is ACCOUNTING: the daemon's own bookkeeping is the
    # wire. This is the general form of the trap already hit once ("query the store with the
    # last utterance" → constant 1.15, because you asked about what you just filed).
    #
    # ⚠️ C2 CARRIER-SWAP CANNOT SEPARATE THIS. A swapped carrier rides the SAME arithmetic,
    # so a pure-ledger system emits EXACTLY the same C2 signature as a real one (both die
    # under swap). C2 separates a COMMON-CAUSE drift (latent state driving A and Y together);
    # bookkeeping is separated by B1 and by nothing else.
    hRA = _im_h_given_S(R, [(a, s) for a, s in zip(A, S)])
    print("  ── B1 BOOKKEEPING (🟢 의 강한 독법을 지키는 게이트) ─────────────")
    print("     H(R|A,S) = %.4f nats   (floor %.3f — R 이 A 로 완전결정이면 재인식이 아니라 장부)"
          % (hRA, hfloor))
    if hRA < hfloor:
        print("     ⇒ ⛔ 장부다 — R 은 A 의 산술적 재진술일 뿐, 새 지각의 분산을 싣지 않는다.")
        print("        I > 0 이 나와도 그건 발견이 아니라 **회계**다. 🟢 의 강한 독법 무효.")
    else:
        print("     ⇒ ✅ R 은 A 너머의 분산을 싣는다 — 재인식이 장부로 붕괴하지 않았다.")

    # ── PC · POWER POSITIVE CONTROL (🧱 선언의 전제조건 · memory power-before-negative-verdict)
    # Before any wall is declared, prove the INSTRUMENT can see a channel that is KNOWN to be
    # live. H_9101 earned exactly one proven emit channel: urgency = phasic Δ tension
    # (`ten_phasic`). Run it through the identical I(·;Y|S) pipe:
    #   urgency→Y ALIVE  ∧  R→Y dead  ⇒ the gate is SELECTIVELY blind. A real 🧱.
    #   urgency→Y DEAD               ⇒ the instrument cannot see ANY gate input. That is
    #                                  ⛔ NOT-POWERED, and a 🧱 declared here would be a
    #                                  statement about my measurement, not the substrate.
    # ⚠️ THE POSITIVE CONTROL MUST MEASURE THE QUANTITY IT NAMES.
    # This block used `ten_phasic` and called it "urgency". It is NOT urgency. chat.py:1878:
    #     urgency = clip01(0.4*agloop_ctx + 0.3*cur_phasic + 0.3*ten_phasic)
    #     cur_phasic = clip01(0.5 + 3.0*(cur_ctx - cur_ema))
    # ten_phasic is ONE of three terms, weighted 0.3. So the control was reading 30% of the
    # channel it claimed to certify, and when it read DEAD that told us nothing about urgency.
    # The name matched; the thing did not (tool-definition-read-code-not-docstring). All three
    # terms are in the trace, so rebuild urgency EXACTLY as the daemon does and use THAT.
    def _urgency(r):
        cur_ph = _im_clip01(0.5 + 3.0 * (float(r["cur_ctx"]) - float(r["cur_ema"])))
        return _im_clip01(0.4 * float(r["agloop_ctx"]) + 0.3 * cur_ph + 0.3 * float(r["ten_phasic"]))

    need = ("agloop_ctx", "cur_ctx", "cur_ema", "ten_phasic")
    have = all(all(k in nxt_lane[(r["_src"], int(r["tick"]))] for k in need) for r in use)
    tp = [_urgency(nxt_lane[(r["_src"], int(r["tick"]))]) for r in use] if have else [None]
    print("  ── PC 검정력 양성대조 (🧱 선언의 전제조건) ─────────────────────")
    print("     U = clip01(0.4·agloop_ctx + 0.3·cur_phasic + 0.3·ten_phasic)  ← chat.py:1878 그대로")
    if any(v is None for v in tp):
        print("     urgency 항 미기록 ⇒ SKIP — 양성대조 없이 🧱 선언 금지")
    else:
        ts = sorted(float(v) for v in tp)
        tmed = ts[len(ts) // 2]
        U = [1 if float(v) > tmed else 0 for v in tp]
        hU = _im_h_given_S(U, S)
        i_uy = _im_cmi(U, Y, S)
        null = []
        for _ in range(perm):
            Up = list(U)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, Y, S))
        nmu = sum(null) / len(null)
        pvu = (sum(1 for v in null if v >= i_uy) + 1.0) / (perm + 1.0)
        eu = i_uy - nmu
        live = (eu >= mde and pvu < 0.005)
        print("     urgency→Y  EARNED = %+.5f nats · perm-p = %.4f · H(U|S) = %.4f   %s"
              % (eu, pvu, hU, "🔗 LIVE (H_9101 유일 proven 채널)" if live else "💀 DEAD"))
        if not live:
            print("     ⇒ ⛔ 검정력 부재 — 계기가 **알려진 살아있는 채널조차** 못 본다.")
            print("        여기서 🧱 를 선언하면 그건 기질이 아니라 내 측정에 관한 문장이다.")
        else:
            print("     ⇒ ✅ 계기는 게이트 입력을 볼 수 있다 — R→Y 가 죽으면 그건 **선택적** 실명이다.")
        # ── PC-SCOPE · urgency 가 죽은 것은 계기 탓인가, urgency 의 성질인가 (H_9340) ────
        #
        # The PC bar says "urgency->Y dead => the instrument is blind => no wall may be
        # declared". That inference has a premise, and the premise is CHECKABLE IN THE SAME
        # RUN: if M2 (R->Y) came back LIVE, then the ->Y detector demonstrably sees a gate
        # input, and the instrument is NOT blind. Then urgency's death is a fact about
        # URGENCY, not about the measurement — and the bar's warrant is void even though the
        # bar itself still stands (re-reading a rule after seeing the number is tune-to-green).
        #
        # What remains is a scope question. H_9101 earned urgency as the one proven channel
        # for emit SHADE — what the mouth says at tick t, same tick. This panel asks about
        # the next tick's SCORE. Those are different targets, and urgency colouring the mouth
        # at t while not reaching the gate at t+1 makes both facts true at once. Measure it:
        # the SAME urgency, the SAME stage conditioning, against the SAME-TICK action.
        #
        # NOTE THE TICK. PC's U is the urgency of the tick that PRODUCED Y (t+1) — that is the
        # right one for a ->Y question. The shade question is about the urgency that coloured
        # the MOUTH, and the mouth spoke at t. Reusing PC's U here would ask whether the NEXT
        # tick's urgency explains THIS tick's utterance, which is a question about the future.
        Uc_raw = [_urgency(r) for r in use]
        ucs = sorted(Uc_raw)
        ucmed = ucs[len(ucs) // 2]
        Uc = [1 if v > ucmed else 0 for v in Uc_raw]
        i_ua = _im_cmi(Uc, A, S)
        null = []
        for _ in range(perm):
            Up = list(Uc)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, A, S))
        nma = sum(null) / len(null)
        pva = (sum(1 for v in null if v >= i_ua) + 1.0) / (perm + 1.0)
        ea = i_ua - nma
        shade_live = (ea >= mde and pva < 0.005)
        print("     urgency→A  EARNED = %+.5f nats · perm-p = %.4f   %s   ← same-tick (H_9101 축)"
              % (ea, pva, "🔗 LIVE" if shade_live else "💀 DEAD"))
        # ── URGENCY-CHANNEL · 코드가 말하는 하류를 직접 잰다 (chat.py:1881) ──────────
        #
        # `urgency` does not flow into the score directly. It sets the tick interval:
        #     idle = 5.0 + 55.0 * clip01(stage_env * (0.5 + urgency))
        # and `idle` is passed straight into brain_emit(). So urgency's channel is the
        # EMIT DECISION — whether/when the substrate speaks, not what it says. Measure the
        # target the wiring names, not the one the panel happens to have around.
        em = [1 if nxt_lane[(r["_src"], int(r["tick"]))].get("emit") else 0 for r in use]
        i_ue = _im_cmi(U, em, S)
        null = []
        for _ in range(perm):
            Up = list(U)
            st = {}
            for k, s in enumerate(S):
                st.setdefault(s, []).append(k)
            for idx in st.values():
                vals = [Up[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Up[k] = vals[j]
            null.append(_im_cmi(Up, em, S))
        nme = sum(null) / len(null)
        pve = (sum(1 for v in null if v >= i_ue) + 1.0) / (perm + 1.0)
        ee = i_ue - nme
        emit_live = (ee >= mde and pve < 0.005)
        hE = _im_h_given_S(em, S)
        print("     urgency→emit EARNED = %+.5f nats · perm-p = %.4f · H(emit|S) = %.4f   %s"
              % (ee, pve, hE, "🔗 LIVE" if emit_live else "💀 DEAD"))
        print("        (코드가 말하는 하류: urgency → idle → brain_emit · chat.py:1881)")
        # The CONCLUSION must key on the axis the WIRING names — emit — not on whichever axis
        # the panel happened to have lying around. Keying it on urgency->Y read "both dead" on
        # a synthetic arm where urgency drove the emit decision by construction.
        decision_live = emit_live or live
        if hE < hfloor:
            print("     ⇒ ⚠️ emit 채널 자체가 죽어 있다(거의 항상 말하거나 항상 침묵) — 판독 불가.")
        elif decision_live and not shade_live:
            print("     ⇒ ✅ **urgency 는 결정-채널이지 내용-채널이 아니다.** 언제/여부를 밀되")
            print("        발화의 내용축은 물들이지 않는다. H_9101(emit 의 유일 proven 채널)과")
            print("        **정합**한다 — 그리고 이것은 '내용이 게이트에 못 닿는다'는 헤드라인과")
            print("        **같은 그림**이다: 게이트는 읽되, 읽는 것이 내용이 아니다.")
        elif shade_live and not decision_live:
            print("     ⇒ urgency 가 입은 물들이나 결정으로는 안 간다(스코프 분리).")
        elif not shade_live and not decision_live:
            print("     ⇒ ⚠️ urgency 가 **어느 축으로도** 안 간다 — 이 양이 H_9101 의 urgency 와")
            print("        **같은지 코드에서 diff** 하라(docstring 금지 · tool-definition-read-code-not-docstring).")
            print("        선례: 이 패널이 ten_phasic 을 urgency 라 부르다 30%만 재고 있었다.")
        else:
            print("     ⇒ urgency 가 결정과 내용을 **둘 다** 민다 — 채널이 분리되지 않는다.")

    # ── M3 · MEDIATION EXHAUSTED (진단) ──────────────────────────────────────────────
    # If roots ① and ② carry the whole path, then conditioning on them should EXHAUST the
    # mediation: I(A;Y|S,R,L) ≈ 0. A residual > 0 says there is an UNACCOUNTED path from the
    # mouth to the gate — which is itself a finding, not a nuisance.
    lan = [nxt_lane[(r["_src"], int(r["tick"]))].get("rel_lane") for r in use]
    if not any(v is None for v in lan):
        ls_ = sorted(float(v) for v in lan)
        lmed = ls_[len(ls_) // 2]
        L = [1 if float(v) > lmed else 0 for v in lan]
        SRL = [(s, r_, l_) for s, r_, l_ in zip(S, R, L)]
        i_res = _im_cmi(A, Y, SRL)
        # The RAW residual cannot be read against MDE. Conditioning on (S,R,L) shatters the
        # sample into ~12x more strata, and plug-in CMI is POSITIVELY BIASED in small strata —
        # every synthetic arm with NO residual path still read 0.019-0.037 nats here. Reading
        # that against a 0.010 bar would MANUFACTURE an "unaccounted path" out of thin air, the
        # same class of defect as an order-statistic bar (probe-defect-census). The bias lives
        # in the null too, so subtract the null: EARNED, never the raw value.
        null = []
        for _ in range(perm):
            Ap2 = list(A)
            st = {}
            for k, z in enumerate(SRL):
                st.setdefault(z, []).append(k)
            for idx in st.values():
                vals = [Ap2[k] for k in idx]
                rnd.shuffle(vals)
                for j, k in enumerate(idx):
                    Ap2[k] = vals[j]
            null.append(_im_cmi(Ap2, Y, SRL))
        nm3 = sum(null) / len(null)
        pv3 = (sum(1 for v in null if v >= i_res) + 1.0) / (perm + 1.0)
        e3 = i_res - nm3
        print("  ── M3 매개 소진 (진단) ─────────────────────────────────────────")
        print("     I(A;Y | S,R,L) = %.5f · null = %.5f ⇒ EARNED = %+.5f nats · perm-p = %.4f"
              % (i_res, nm3, e3, pv3))
        if e3 >= mde and pv3 < 0.005:
            print("     ⇒ 잔차 EARNED > MDE — **미계상 경로가 있다**(뿌리①② 밖으로 말이 게이트에 닿는다).")
        else:
            print("     ⇒ 잔차 ≈ 0 — 뿌리①② 가 말→게이트 경로를 설명한다(소진).")

    # ── AXIS · 내가 잰 축이 루프가 나르는 축인가 (진단 · 헤드라인 아님) ───────────────
    # 헤드라인의 A = a_fold8 = penult_fold8(pooled) — 입이 **표상한** 축이다.
    # 그런데 루프가 물리적으로 나르는 것은 _afs_byte_feature(g_text, 8) — 평균·분산·고바이트·
    # 공백·숫자·구두점 같은 **8개 바이트-모양 스칼라**다(chat.py:240). 내용은 거기서 이미 버려진다.
    # 두 축이 직교하면, 나는 **루프가 나르지 않는 축**을 재고 "정보가 없다"고 말한 셈이 된다.
    #
    # A′ = penult_fold8(byte_feat8) — 같은 FROZEN reducer(H_9257), 물리적으로 소비되는 입력,
    # 새 자유도 0. bar 도 추가하지 않는다(진단이므로 verdict 불변).
    #
    # A SKIP HERE MUST NOT RETURN. This panel used to `return 0` when gtext_b64 was absent,
    # which silently swallowed every panel below it — the same defect already fixed once when
    # a dead mediation channel ate this very AXIS block. A diagnostic that cannot run is a
    # diagnostic that prints SKIP, not one that ends the readout (convergence evaluate-py-14).
    gt = [r.get("gtext_b64") for r in use]
    Ap = None
    if any(g is None for g in gt):
        print("  ── AXIS: gtext_b64 미기록 ⇒ SKIP (구 trace 포맷)")
    else:
        try:
            import base64
            Ap = [clm.penult_fold8(_im_byte_feat8(
                base64.b64decode(g).decode("utf-8", "surrogateescape"))) for g in gt]
        except Exception as e:  # pragma: no cover
            print("  ── AXIS: SKIP (" + str(e) + ")")
            Ap = None
    if Ap is not None:
        hAp = _im_h_given_S(Ap, S)
        i_axes = _im_cmi(A, Ap, S)
        print("  ── AXIS (진단 · verdict 불변) ──────────────────────────────────")
        print("     A  = penult_fold8(pooled)     — 입이 표상한 축      H(A|S)  = %.4f nats" % hA)
        print("     A′ = penult_fold8(byte_feat8) — 루프가 나르는 축    H(A′|S) = %.4f nats" % hAp)
        print("     I(A;A′|S) = %.4f nats   (두 축이 같은 것을 보는가)" % i_axes)
        if hAp < hfloor:
            print("     ⇒ A′ 자체가 죽어 있다 — 루프 입력이 상수. 축 문제 이전에 경로 문제.")
        elif i_axes < mde:
            print("     ⇒ ⚠️ 두 축이 **거의 직교**하다. 나는 루프가 나르지 않는 축을 쟀다 —")
            print("        헤드라인의 '정보 없음'은 **이 축 위에서만** 벌어진 것이다(축 재선택이")
            print("        아니라, A′ 로 재판독해야 use-claim 이 선다).")
        else:
            print("     ⇒ 두 축이 상당히 겹친다 — 헤드라인 축 선택은 방어된다.")

    # ── COMPOSITION · 사슬이 안 이어붙는가, 아니면 그냥 좁은가 (H_9340 · 사전등록) ──────
    #
    # H_9337 read M1 (A->R) LIVE, M2 (R->Y) LIVE, and A->Y below MDE, and I called that a
    # COMPOSITION FAILURE — "the component the mouth pushes is not the component the gate
    # reads". That is the story I want to be true, and the data I already had ARGUES AGAINST
    # IT. A weak-channel Markov chain predicts multiplicative attenuation:
    #     rho1 ~ sqrt(2*0.0202) = 0.20 · rho2 ~ sqrt(2*0.0902) = 0.42
    #     I_comp ~ 0.5*(rho1*rho2)^2 = 0.0036 nats     vs     I_obs = 0.0061
    # The observation sits ABOVE the composition prediction. A real misalignment would put it
    # BELOW (a mismatched component leaks MORE than the product, not less), and the DPI bound
    # min(0.020, 0.090) = 0.020 is not violated either. The picture is not a contradiction —
    # it is attenuation. So test the chain directly instead of narrating it.
    #
    # Build the COMPOSED channel from the two measured links and ask whether the observed
    # end-to-end MI is what that chain predicts:
    #     p_comp(Y|A,S) = sum_R p(Y|R,S) p(R|A,S)      Delta = I_obs - I_comp
    # Two versions. The 2-bin one uses the same R the headline used. The CONTINUOUS one uses
    # the raw recon_err scalar the trace already carries (logistic p(Y|r,S), then a plug-in
    # Monte-Carlo average over the r's actually observed in each (A,S) cell — no density
    # estimate). Note the continuous version DROPS the binning rather than refining it, so it
    # carries none of the stratum-explosion bias that forced M3 onto a permutation null.
    lan_c = [nxt_lane[(r["_src"], int(r["tick"]))].get("rel_lane") for r in use]
    print("  ── COMPOSITION (H_9340 · 사슬이 안 이어붙는가 vs 그냥 좁은가) ────")

    def _comp_mi(pY_given_R, R_of_i):
        """I_comp(A;Y|S) for the composed channel p(Y|A,S) = E_{R|A,S}[ p(Y|R,S) ]."""
        cell = {}
        for i, a in enumerate(A):
            cell.setdefault((S[i], a), []).append(pY_given_R[i])
        pa_s, ns = {}, {}
        for i, a in enumerate(A):
            pa_s[(S[i], a)] = pa_s.get((S[i], a), 0) + 1
            ns[S[i]] = ns.get(S[i], 0) + 1
        tot = float(len(A))
        out = 0.0
        for s in ns:
            keys = [k for k in cell if k[0] == s]
            if not keys:
                continue
            wsum = float(ns[s])
            pbar = sum(pa_s[k] / wsum * (sum(cell[k]) / len(cell[k])) for k in keys)
            hbar = _im_H_p(pbar)
            hcond = sum(pa_s[k] / wsum * _im_H_p(sum(cell[k]) / len(cell[k])) for k in keys)
            out += (wsum / tot) * (hbar - hcond)
        return out

    def _pY_given_Rbin(idx):
        tab = {}
        for i in idx:
            tab.setdefault((S[i], R[i]), [0, 0])
            tab[(S[i], R[i])][Y[i]] += 1
        return [((tab.get((S[i], R[i]), [1, 1])[1] + 0.5)
                 / (sum(tab.get((S[i], R[i]), [1, 1])) + 1.0)) for i in range(len(A))]

    def _pY_given_Rcont(idx):
        # per-stage logistic on the raw scalar, 200 steps of plain gradient ascent
        out = [0.5] * len(A)
        for s in set(S):
            tr = [i for i in idx if S[i] == s]
            if len(tr) < 10:
                continue
            xs = [rc[i] for i in tr]
            mu = sum(xs) / len(xs)
            sd = (sum((v - mu) ** 2 for v in xs) / len(xs)) ** 0.5 or 1.0
            w = b = 0.0
            for _ in range(200):
                gw = gb = 0.0
                for i in tr:
                    z = w * ((rc[i] - mu) / sd) + b
                    p = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
                    e = Y[i] - p
                    gw += e * ((rc[i] - mu) / sd)
                    gb += e
                w += 0.5 * gw / len(tr)
                b += 0.5 * gb / len(tr)
            for i in range(len(A)):
                if S[i] != s:
                    continue
                z = w * ((rc[i] - mu) / sd) + b
                out[i] = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))
        return out

    rc = [float(nxt_lane[(r["_src"], int(r["tick"]))]["recon_err"]) for r in use]
    allidx = list(range(len(A)))
    i_c2 = _comp_mi(_pY_given_Rbin(allidx), R)
    i_cc = _comp_mi(_pY_given_Rcont(allidx), rc)
    print("     I_obs(A;Y|S)      = %.5f nats" % I)
    print("     I_comp [R 2-bin]  = %.5f   Δ = %+.5f" % (i_c2, I - i_c2))
    print("     I_comp [R 연속]    = %.5f   Δ = %+.5f  ← 사전등록 판독축" % (i_cc, I - i_cc))
    print("     (b) 게이트  I_comp[연속] − I_comp[2bin] = %+.5f  (>%.3f 이면 2-bin 이 정보를 버렸다)"
          % (i_cc - i_c2, mde))
    # bootstrap over ROLLOUTS (the exchangeable unit, evaluate-py-13) for a CI on Delta
    src_l = [r["_src"] for r in use]
    roll = sorted(set(src_l))
    byr = {}
    for i, s_ in enumerate(src_l):
        byr.setdefault(s_, []).append(i)
    deltas = []
    for _ in range(200):
        pick = [roll[rnd.randrange(len(roll))] for _ in range(len(roll))]
        idx = [i for r_ in pick for i in byr[r_]]
        Ab = [A[i] for i in idx]; Yb = [Y[i] for i in idx]; Sb = [S[i] for i in idx]
        io = _im_cmi(Ab, Yb, Sb)
        pv = _pY_given_Rcont(idx)
        cell = {}
        for i in idx:
            cell.setdefault((S[i], A[i]), []).append(pv[i])
        cnt = {}
        for i in idx:
            cnt[(S[i], A[i])] = cnt.get((S[i], A[i]), 0) + 1
        nsb = {}
        for i in idx:
            nsb[S[i]] = nsb.get(S[i], 0) + 1
        ic = 0.0
        for s in nsb:
            keys = [k for k in cell if k[0] == s]
            wsum = float(nsb[s])
            pbar = sum(cnt[k] / wsum * (sum(cell[k]) / len(cell[k])) for k in keys)
            ic += (wsum / float(len(idx))) * (
                _im_H_p(pbar) - sum(cnt[k] / wsum * _im_H_p(sum(cell[k]) / len(cell[k])) for k in keys))
        deltas.append(io - ic)
    deltas.sort()
    lo, hi = deltas[int(0.025 * len(deltas))], deltas[int(0.975 * len(deltas)) - 1]
    print("     Δ[연속] 95%% CI (rollout bootstrap) = [%+.5f, %+.5f]" % (lo, hi))
    # ── POWER GATE on the (a)-vs-(c) contrast (BLOCKING) ─────────────────────────────
    # A verdict that cannot be reached is as broken as a guard that cannot fail. Declaring
    # (a) MISALIGNMENT requires I_obs < I_comp - MDE, and mutual information cannot go below
    # zero — so when I_comp itself sits under MDE, (a) is UNREACHABLE BY CONSTRUCTION and the
    # test can only ever land on (c). That is not evidence for (c); it is the bar quietly
    # deciding in advance. Worse, it says something stronger about the whole question: a chain
    # this weak predicts an end-to-end MI BELOW THE INSTRUMENT'S RESOLUTION even when it is
    # PERFECTLY aligned — so the observed A->Y is exactly what a working chain looks like, and
    # there is no "composition failure" left to explain.
    if i_cc < mde:
        print("     ⇒ ⛔ (a)/(c) 판별 **NOT-POWERED** — 합성 예측 자체가 MDE 아래다"
              " (I_comp=%.5f < %.3f)." % (i_cc, mde))
        print("        (a) 는 I_obs < I_comp − MDE 를 요구하는데 상호정보는 음수가 못 된다 ⇒")
        print("        이 bar 로 (a) 는 **원리적으로 도달 불가**. (c) 로만 갈 수 있는 검정이다.")
        print("        더 중요한 함의: **완벽히 정렬된 사슬조차 측정 불가능한 효과를 예측한다.**")
        print("        ⇒ 관측된 A→Y 는 정상 작동하는 약한 사슬이 내놓을 바로 그 값이다.")
        print("        '합성 실패'는 설명할 것이 없다 — 두 링크가 약한 것이 전부다.")
        return 0
    if lo > mde:
        print("     ⇒ 직통로 — R 밖의 A→Y 경로가 있다. M3 소진과 모순 ⇒ L-조건화 재점검.")
    elif hi < -mde:
        print("     ⇒ (a) **정렬 실패 실재** — 실측이 합성 예측보다 유의하게 **낮다**.")
        print("        말이 미는 R 의 성분과 게이트가 읽는 성분이 어긋난다.")
    elif lo > -mde and hi < mde:
        print("     ⇒ (c) **감쇠다 — 합성 실패 아님.** 사슬은 곱셈으로 이어진다, 좁을 뿐.")
        print("        H_9337 의 '정렬 실패' 헤드라인은 **정정된다**.")
    else:
        print("     ⇒ 판정 보류 — CI 가 등가역과 한쪽 꼬리에 걸친다(검정력 부족).")
    return 0


def _im_byte_feat8(s):
    """cli/chat.py::_afs_byte_feature(s, 8) 의 판독-측 쌍둥이 — 루프가 실제로 나르는 8 스칼라.

    데몬은 emit 마다 이 8개(평균·분산·고바이트·저바이트·공백·숫자·구두점·짧은바이트 비율)만
    afield 에 넣는다. 내용은 여기서 소각된다. 판독기가 이 축을 못 보면, '정보가 없다'는 결론은
    기질이 아니라 **내 축 선택**에 관한 것이 된다. reference-match: chat.py:240 과 1:1."""
    b = s.encode("utf-8", "surrogateescape")
    n = len(b)
    if n == 0:
        return [0.0] * 8
    fn = float(n)
    total = sumsq = 0.0
    n_hi = n_low = n_sp = n_dig = n_pun = n_lt64 = 0
    for byte in b:
        bf = float(byte)
        total += bf
        sumsq += bf * bf
        if byte >= 128:
            n_hi += 1
        if byte < 32:
            n_low += 1
        if byte == 32:
            n_sp += 1
        if 48 <= byte <= 57:
            n_dig += 1
        if byte in (33, 44, 46, 58, 59, 63):
            n_pun += 1
        if byte < 64:
            n_lt64 += 1
    mean = total / fn
    var = sumsq / fn - mean * mean
    return [mean / 255.0, var / 65025.0, n_hi / fn, n_low / fn,
            n_sp / fn, n_dig / fn, n_pun / fn, n_lt64 / fn]


_KNOWN_FLAGS = frozenset((
    "--arm", "--bind-locus", "--bl-swap-span", "--bl-swap-donor-class", "--consult", "--consult-format", "--corpus", "--dump-hidden", "--earned", "--gen",
    "--help", "--ground-probe", "--interact-mi", "--gate-deaf", "--g-tension", "--tension-emit", "--psi-soma", "--interaction-lift", "--k-perm", "--kappa", "--kernel", "--kosmos", "--min-occ", "--null",
    "--device-parity", "--n-decode", "--n-sampled", "--valence-audit",
    "--out", "--perm", "--probe", "--seed",
    "--result-file", "--collide-select", "--k", "--rho-axon", "--route-audit", "--score-len", "--seeds", "--selftest-rho-cells",
    "--slot-off",
    "--slot-shuffle", "--system-g1", "--vs", "--win", "--with-logits", "--xbind", "--xfan",
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
    if "--collide-select" in argv:
        _ck = [a for a in argv if not a.startswith("--")]
        return _collide_select(_ck[0] if _ck else "", [a for a in argv if a.startswith("--")])
    if len(argv) >= 2 and argv[0] == "--gate-deaf":
        return _gate_deaf(argv[1:])
    if len(argv) >= 2 and argv[0] == "--g-tension":
        return _g_tension(argv[1:])
    if len(argv) >= 2 and argv[0] == "--tension-emit":
        return _tension_emit(argv[1:])
    if len(argv) >= 2 and argv[0] == "--psi-soma":
        return _psi_soma_real(argv[1:])
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
    # --route-audit <manifest.json>: H_9355 LOCUS-CAUSAL — the ConvMoE router's per-surface expert
    # distribution. Asks the one question a hidden-space probe cannot: not what is represented, but
    # WHICH EXPERT COMPUTED IT. A route split (beyond a byte-matched inert suffix) makes the
    # two-lane model PHYSICAL; a shared route kills route-pin before it is fired.
    if "--route-audit" in argv:
        return route_audit_run(argv)
    if "--bind-locus" in argv:
        return bind_locus_run(argv)
    if "--valence-audit" in argv:
        return valence_audit_run(argv)
    # --device-parity: is this host's GPU forward the same measurement as its CPU forward? The probes
    # read hiddens, and the hidden is NOT byte-identical across devices (decode-py-4).
    if "--device-parity" in argv:
        return device_parity_run([a for a in argv if a != "--device-parity"])
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
