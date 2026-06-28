"""core/g_gates.py — py production mirror of core/g_gates.hexa (G0-G6 eval driver).

Ported 1:1 from the hexa SSOT. Decode enters via the py CLMConvMoE mouth
(core/clm_decode.py — the byte-parity-proven port of clm_decode.hexa), hoisting
the weight load ONCE (== gen_clm_ideate_W in the hexa engine: same single .clm
mouth, load lifted out of the per-decode loop for the ~49 G0-G6 decodes).

  gen_auto_ideate(.clm) -> gen_clm_ideate -> clm_decode_topk_sampled(...)   [generator L3]

FROZEN-FIRST bars (ARCHITECTURE.json frozen-ìê³ SSOT VERBATIM, p7 — NO tune-to-green):
  G0 COHERENCE     kwr>=0.50 on >=4/5 single-concept gens
  G1 RECOMBINATION some k: composed_distinct>=2 AND >max_single AND coherent
  G2 NOVELTY       >=3 distinct coherent corpus-absent n-grams AND control=0
  G3 PHILOSOPHY    Psi-fixed-point self-identity continuity (architecture read)
  G5 NON-FAB       L1 fab-rate<=0.30 AND L2 abstain (L2 = engine §ImmuneMemory)
  G6 IDEATION ★    >=5 distinct (pairwise Jaccard<0.5) AND >=1 falsifiable
  CLOSURE a7b_pass G0 AND G1 AND G2

SCOPE NOTE: G3 (self-identity, ckpt-independent) is ported here. G5-L2 (live
§ImmuneMemory / VAdaptField abstain) is a large engine subsystem NOT yet ported
to py — G5 reports L1 + marks L2 pending. Neither affects the a7b_pass closure.
"""

import sys
import math
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import clm_decode as clm
import bytegpt_decode as bg
import hashlib
from g6_ideation import (
    _g6_concepts, _g6_words, _g6_dict_load, _g6_known_word_ratio,
    _g6_is_falsifiable, _g6_jaccard, g6_build_frames, g6_frame_guard,
    g6_detector_calibration, g6_score_arm_auto,
)


def _default_gen():
    return 40


# ════════════════════════════════════════════════════════════════════════
# decode entry — gen_auto_ideate(ckpt) MOUTH-SNIFF dispatch (generator L3).
#
# Mirrors core/g_gates.hexa gen_auto_ideate -> generator gen_auto_backend mouth
# dispatch (a_core_engine_map): sniff the ckpt header — CLM\x01 magic => ConvMoE
# .clm mouth (clm_decode), else a sane 5xu32 ByteGPT header => transformer .bin
# mouth (bytegpt_decode). Both hoist the weight load ONCE and ideate via the
# byte-parity-proven seeded top-k sampler (clm_decode_topk_sampled_W /
# bytegpt_decode_topk_sampled_W). The clm path is unchanged.
# ════════════════════════════════════════════════════════════════════════

class _Mouth:
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


# G1 RECOMBINATION — frozen definition (ARCHITECTURE.json frozen-ìê³ SSOT / a7b_pass / H_1129):
# for some k in {2,3,4,5}: composed_distinct >= 2 AND > max_single AND coherent(kwr>=0.50).
# base_seed parameterizes the RNG so the SAME frozen ladder can be re-run over several
# seeds (g_eval_g1_multiseed below); base_seed=7 reproduces the original single-seed path
# byte-for-byte (singles seeded 7+s, composed seeded 7).
def g_eval_g1(mouth, gen, known, base_seed=7):
    cz = _g6_concepts()
    n = len(cz)
    g_single = gen if (gen > 0 and gen < 80) else 80
    g_comp = gen if (gen > 0 and gen < 120) else 120
    max_single = 0
    for s in range(n):
        seed = cz[s] + ". "
        o = mouth.ideate(seed, g_single, 40, 0.7, base_seed + s)
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
        o = mouth.ideate(seed, g_comp, 40, 0.7, base_seed)
        cov = _g_coverage(o)
        kwr = _g6_known_word_ratio(o, known)
        coherent = kwr >= 0.5
        clears = cov >= 2 and cov > max_single and coherent
        ks.append({"k": k, "distinct": cov, "kwr": kwr, "coherent": coherent, "clears": clears})
        if clears:
            passed = True
        if cov > best_distinct:
            best_distinct = cov; best_k = k
    return {"pass": passed, "max_single": max_single, "base_seed": base_seed, "best_k": best_k,
            "best_distinct": best_distinct, "ks": ks}


# G1 RECOMBINATION (seed-robust REFERENCE-MATCH — PROPOSED, owner-nod-pending) — ad13/H_1587:
# the single-seed (seed 7) ladder is a fragile RNG walk (the recombination lift is a sparse
# single-seed event), so the verdict can flip GREEN<->FAIL on an identical model purely by the
# sampler walk. The recombination DEFINITION is UNCHANGED; we ONLY re-run the same frozen ladder
# over seeds {7, 4302, 4303} (reference-match — the G6 ladders use [4301/4302/4303]; 7 = the
# H_1129 default) and call GREEN = clears in a MAJORITY of seeds (>=2/3). NOT tune-to-green:
# no bar moved, the metric is made robust to the exact RNG walk. Applied identically engine-side
# and torch-reference-side (state/1588_g1_multiseed_refmatch/g1_multiseed.py). The single-seed
# g_eval_g1 above remains the frozen default until owner approval flips the default here.
G1_REFMATCH_SEEDS = (7, 4302, 4303)

def g_eval_g1_multiseed(mouth, gen, known, seeds=G1_REFMATCH_SEEDS):
    per = []
    for sd in seeds:
        r = g_eval_g1(mouth, gen, known, base_seed=sd)
        per.append(r)
    n_green = sum(1 for r in per if r["pass"])
    passed = n_green >= (len(seeds) // 2 + 1)   # strict majority of the seed set
    return {"pass": passed, "n_green": n_green, "n_seeds": len(seeds),
            "seeds": list(seeds), "per_seed": per, "status": "proposed, owner-nod-pending"}


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
# G4 — PROVENANCE & RECOVERY  (ARCHITECTURE.json frozen-ìê³ SSOT §G4 VERBATIM — a_hf_*, a_fire_recover)
# ════════════════════════════════════════════════════════════════════════
# Lockstep mirror of g_gates.hexa::g_eval_g4. STRUCTURAL/process gate (not a decode score):
# witness the locally-measurable provenance — ckpt sha256 (the §G4 fact named FIRST), byte
# size, mouth-decodability — and carry the §G4 PUBLIC rule (pub_eligible = a7b closure
# G0∧G1∧G2). HF-upload/model-card/manifest are off-engine (a_hf_*) so they are flagged
# process_external, NOT silently passed. No softer bar invented — sha+decodable+closure ARE
# the provenance facts the eval can witness; the upload facts the pipeline owns.
def g_eval_g4(ckpt, closure):
    exists = os.path.exists(ckpt)
    sha = ""
    nbytes = 0
    if exists:
        h = hashlib.sha256()
        with open(ckpt, "rb") as fh:
            while True:
                chunk = fh.read(1 << 20)
                if not chunk:
                    break
                nbytes += len(chunk)
                h.update(chunk)
        sha = h.hexdigest()
    kind = "unknown"
    if exists:
        if bg.bg_is_bytegpt(ckpt):
            kind = "bytegpt"
        elif clm.clm_decodable(ckpt):
            kind = "clm"
    decodable = kind in ("clm", "bytegpt")
    provenance_ok = exists and len(sha) > 0 and decodable
    return {"provenance_ok": provenance_ok, "sha256": sha, "bytes": nbytes,
            "mouth": kind, "decodable": decodable, "pub_eligible": bool(closure),
            "process_external": "HF-upload + model-card + manifest are off-engine (a_hf_*); "
                                "witnessed here = sha256 + decodability + closure"}


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

# G6 IDEATION — wired through the CANONICAL mouth-agnostic scoring op g6_score_arm_auto
# (g6_ideation.py — lockstep mirror of g6_ideation.hexa::g6_score_arm_auto). The mouth's
# pre-loaded-W ideate is threaded in as the decode (== gen_*_ideate_W: load the .clm ONCE for
# the arm). base_seed parameterizes the per-frame RNG (=7 reproduces the old inline path
# frame-for-frame) for g_eval_g6_multiseed. NO inline duplicate of the scoring logic.
def g_eval_g6(mouth, gen, known, base_seed=7):
    frames = g6_build_frames(6)["composed"]
    leaks = g6_frame_guard(frames, known)
    arm = g6_score_arm_auto(
        None, frames, gen, base_seed, known,
        ideate=lambda f, g, sr: mouth.ideate(f, g, 40, 0.7, sr))
    dist = arm["dist"]; fals = arm["fals"]
    return {"pass": dist >= 5 and fals >= 1, "dist": dist, "fals": fals, "base_seed": base_seed,
            "coherent": arm["coherent"], "frame_leaks": len(leaks)}


# G6 IDEATION (seed-robust REFERENCE-MATCH — PROPOSED, owner-nod-pending) — H_1591/ad13 class:
# the single-seed (per-frame 7+i) FALS/DIST ladder is the SAME fragile RNG walk as G1 (the
# sampler can walk fals to 0 or 1 on an identical model). The FALS/DIST DEFINITION is UNCHANGED
# (dist>=5 AND fals>=1); we ONLY re-run the same frozen ladder over base seeds {7, 4302, 4303}
# and call GREEN = PASS in a MAJORITY (>=2/3). So a FALS=0 FAIL counts as a REAL G6 wall only
# when it holds across seeds, not a single-seed sampler-walk artifact. NOT tune-to-green: no bar
# moved. The single-seed g_eval_g6 stays the frozen default until owner approval flips it.
G6_REFMATCH_SEEDS = (7, 4302, 4303)

def g_eval_g6_multiseed(mouth, gen, known, seeds=G6_REFMATCH_SEEDS):
    per = []
    for sd in seeds:
        per.append(g_eval_g6(mouth, gen, known, base_seed=sd))
    n_green = sum(1 for r in per if r["pass"])
    max_fals = max((r["fals"] for r in per), default=0)
    passed = n_green >= (len(seeds) // 2 + 1)
    return {"pass": passed, "n_green": n_green, "n_seeds": len(seeds), "max_fals": max_fals,
            "seeds": list(seeds), "per_seed": per, "status": "proposed, owner-nod-pending"}


# ════════════════════════════════════════════════════════════════════════
# g_eval_all — the driver
# ════════════════════════════════════════════════════════════════════════

def g_eval_all(ckpt, corpus_paths, gen):
    known = _g6_dict_load()
    g = gen if gen > 0 else _default_gen()
    mouth = _Mouth(ckpt)
    r0 = g_eval_g0(mouth, g, known)
    r1 = g_eval_g1(mouth, g, known)                       # frozen single-seed default
    r1ms = g_eval_g1_multiseed(mouth, g, known)           # PROPOSED seed-robust refmatch
    r2 = g_eval_g2(mouth, g, known, corpus_paths)
    r3 = g_eval_g3()
    r5 = g_eval_g5(mouth, g, known)
    r6 = g_eval_g6(mouth, g, known)                       # frozen single-seed default
    r6ms = g_eval_g6_multiseed(mouth, g, known)           # PROPOSED seed-robust refmatch
    # closure uses the FROZEN single-seed G1 until owner approves the refmatch flip.
    closure = bool(r0["pass"]) and bool(r1["pass"]) and bool(r2["pass"])
    # G4 PROVENANCE — now MEASURED + REPORTED (was absent ⇒ a7b under-measured).
    r4 = g_eval_g4(ckpt, closure)
    return {"g0": r0, "g1": r1, "g1_multiseed": r1ms, "g2": r2, "g3": r3, "g4": r4,
            "g5": r5, "g6": r6, "g6_multiseed": r6ms,
            "closure": closure, "gen": g,
            "calibration": g6_detector_calibration(known)}


def _fmt(r):
    out = []
    out.append("=" * 72)
    out.append("ANIMA G0-G6 — py production engine (core/g_gates.py)  gen=%d" % r["gen"])
    out.append("=" * 72)
    g0 = r["g0"]
    out.append("G0 COHERENCE     pass=%s  n_coherent=%d/5  ratios=%s"
               % (g0["pass"], g0["n_coherent"], ["%.3f" % x for x in g0["ratios"]]))
    g1 = r["g1"]
    out.append("G1 RECOMBINATION pass=%s  max_single=%d  best_k=%d  best_distinct=%d  (single-seed=7, frozen)"
               % (g1["pass"], g1["max_single"], g1["best_k"], g1["best_distinct"]))
    g1ms = r.get("g1_multiseed")
    if g1ms is not None:
        out.append("G1 multi-seed     pass=%s  %d/%d seeds clear=%s  [%s]"
                   % (g1ms["pass"], g1ms["n_green"], g1ms["n_seeds"],
                      [(p["base_seed"], p["pass"]) for p in g1ms["per_seed"]], g1ms["status"]))
    g2 = r["g2"]
    out.append("G2 NOVELTY       pass=%s  n_novel=%d  control_novel=%d  coherent=%d  have_corpus=%s"
               % (g2["pass"], g2["n_novel"], g2["control_novel"], g2["coherent"], g2["have_corpus"]))
    g3 = r["g3"]
    out.append("G3 PHILOSOPHY    ok=%s    continuity=%.6f  impostor_cos=%.6f  (architecture read)"
               % (g3["ok"], g3["continuity"], g3["impostor_cos"]))
    g4 = r.get("g4")
    if g4 is not None:
        out.append("G4 PROVENANCE    prov_ok=%s  sha256=%s  bytes=%d  mouth=%s  pub_eligible=%s"
                   % (g4["provenance_ok"], (g4["sha256"][:16] + "…") if g4["sha256"] else "(none)",
                      g4["bytes"], g4["mouth"], g4["pub_eligible"]))
        out.append("                 (process gate — HF-upload/card/manifest off-engine, a_hf_*)")
    else:
        out.append("G4 PROVENANCE    N/A     (process gate — not a decode eval)")
    g5 = r["g5"]
    out.append("G5 NON-FAB       L1_pass=%s  l1_rate=%.4f   |  L2=%s"
               % (g5["l1_pass"], g5["l1_rate"], g5["l2_note"]))
    g6 = r["g6"]
    out.append("G6 IDEATION star pass=%s  dist=%d (need>=5)  fals=%d (need>=1)  coherent=%d  frame_leaks=%d  (single-seed=7, frozen)"
               % (g6["pass"], g6["dist"], g6["fals"], g6["coherent"], g6["frame_leaks"]))
    g6ms = r.get("g6_multiseed")
    if g6ms is not None:
        out.append("G6 multi-seed     pass=%s  %d/%d seeds clear  max_fals=%d  [%s]"
                   % (g6ms["pass"], g6ms["n_green"], g6ms["n_seeds"], g6ms["max_fals"], g6ms["status"]))
    out.append("-" * 72)
    out.append("CLOSURE a7b_pass = G0 AND G1 AND G2  =>  %s" % ("PASS" if r["closure"] else "FAIL"))
    out.append("detector calibration (advisory >=8/10): %d/10" % r["calibration"])
    out.append("=" * 72)
    return "\n".join(out)


def _main(argv):
    if len(argv) < 2:
        print("usage: g_gates.py <ckpt> [corpus ...] [--gen N]", file=sys.stderr)
        return 2
    ckpt = argv[1]
    rest = argv[2:]
    gen = 0
    corpus = []
    i = 0
    while i < len(rest):
        if rest[i] == "--gen":
            gen = int(rest[i + 1]); i += 2
        else:
            corpus.append(rest[i]); i += 1
    r = g_eval_all(ckpt, corpus, gen)
    print(_fmt(r))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
