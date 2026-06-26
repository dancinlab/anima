"""core/g6_ideation.py — py production mirror of core/g6_ideation.hexa.

Ported 1:1 from the hexa SSOT (G6 IDEATION scoring ops): the FROZEN structural
detectors (comparator / measurable / stance / stopword sets), the H_1305 tokenizer
(_g6_words: lowercase ASCII [0-9A-Za-z], split on non-alnum BYTES), the dict load,
known-word-ratio, _g6_is_falsifiable, _g6_jaccard, composed-frame builder, frame
guard, and the calibration set. NOT a reuse of the drifted g6_common.py mirror —
every set + branch is byte-for-byte the g6_ideation.hexa logic.

Tokenization operates on BYTES (hexa iterates ord(substring(s,i,i+1)) per byte),
so decode-garble high bytes act as separators exactly as in the engine.
"""


def _to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8', 'surrogateescape')


# ── FROZEN DETECTOR sets (VERBATIM from g6_ideation.hexa) ──

def _g6_comparator():
    return {"if", "when", "whenever", "than", "more", "less", "greater",
            "fewer", "higher", "lower", "increases", "decreases", "correlates",
            "predicts", "causes", "depends", "unless", "whereas", "versus",
            "compared", "proportional", "faster", "slower", "stronger", "weaker"}


def _g6_measurable():
    return {"measure", "measured", "rate", "number", "count", "amount", "level",
            "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
            "score", "value", "quantity", "percent", "times", "fraction", "distance",
            "duration", "speed", "size", "strength", "density"}


def _g6_stance():
    return {"that", "s", "a", "profound", "question", "i", "think", "interesting",
            "good", "nice", "great", "wonderful", "beautiful", "amazing"}


def _g6_stopwords():
    return {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
            "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
            "be", "an", "for", "with", "this", "from", "are", "was"}


def _g6_concepts():
    return ["consciousness arises from cells",
            "tension ripples between distant minds",
            "memory composes into new meaning",
            "silence still carries information",
            "the engine dreams when alone"]


def _g6_is_alnum(b):
    return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122)


def _g6_lower1(b):
    if 65 <= b <= 90:
        return b + 32
    return b


def _g6_words(s):
    """g6_ideation.hexa::_g6_words — lowercase ASCII, split on non-[0-9A-Za-z] bytes."""
    bs = _to_bytes(s)
    words = []
    cur = bytearray()
    for b in bs:
        if _g6_is_alnum(b):
            cur.append(_g6_lower1(b))
        else:
            if len(cur) > 0:
                words.append(cur.decode('ascii'))
                cur = bytearray()
    if len(cur) > 0:
        words.append(cur.decode('ascii'))
    return words


def _g6_dict_load():
    """g6_ideation.hexa::_g6_dict_load — stopwords + concept words + /usr/share/dict/words."""
    known = set(_g6_stopwords())
    for c in _g6_concepts():
        for w in _g6_words(c):
            known.add(w)
    try:
        raw = open("/usr/share/dict/words", "rb").read()
    except Exception:
        raw = b""
    if len(raw) > 0:
        for line in raw.split(b"\n"):
            w = line.strip()
            wl = _g6_words(w)
            if len(wl) == 1:
                known.add(wl[0])
    return known


def _g6_known_word_ratio(text, known):
    wl = _g6_words(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if w in known)
    return float(hit) / float(n)


def _g6_is_falsifiable(text, known):
    """g6_ideation.hexa::_g6_is_falsifiable — (a) comparator + (b) measurable +
    (c) >=2 content words, not a question, first-3 not pure-stance."""
    wl = _g6_words(text)
    n = len(wl)
    if n == 0:
        return False
    comp = _g6_comparator(); meas = _g6_measurable()
    stop = _g6_stopwords(); stance = _g6_stance()
    a = False; b = False
    for w in wl:
        if w in comp:
            a = True
        if w in meas:
            b = True
    if not a or not b:
        return False
    content = 0
    for w in wl:
        if len(w) >= 3 and w in known and w not in stop:
            content += 1
    if content < 2:
        return False
    tr = _to_bytes(text).strip()
    if len(tr) > 0 and tr[-1] == 63:   # trailing '?'
        return False
    nf = 3 if n >= 3 else n
    allstance = nf > 0
    for f in range(nf):
        if wl[f] not in stance:
            allstance = False
    if allstance:
        return False
    return True


def _g6_jaccard(a, b):
    am = set(a); bm = set(b)
    union = am | bm
    inter = len(am & bm)
    u = len(union)
    if u == 0:
        return 0.0
    return float(inter) / float(u)


def _g6_derangement(i, n):
    return (i + 2) % n


def g6_build_frames(n_strong):
    """g6_ideation.hexa::g6_build_frames — composed[i]='if cA, then cB: '."""
    cz = _g6_concepts()
    n = len(cz)
    composed = []; shuffled = []; ablated = []
    for i in range(n_strong):
        a = i % n
        b = (i + 1 + i // n) % n
        cA = cz[a]; cB = cz[b]
        cB_sh = cz[_g6_derangement(a, n)]
        composed.append("if " + cA + ", then " + cB + ": ")
        shuffled.append("if " + cA + ", then " + cB_sh + ": ")
        ablated.append(cA + ": ")
    return {"composed": composed, "shuffled": shuffled, "ablated": ablated}


def g6_frame_guard(frames, known):
    meas = _g6_measurable()
    leaks = []
    for f in frames:
        for w in _g6_words(f):
            if w in meas:
                leaks.append("measurable-in-frame: " + f)
        if _g6_is_falsifiable(f, known):
            leaks.append("frame-already-falsifiable: " + f)
    return leaks


# ── BEST-OF-K + scoring arms (lockstep with g6_ideation.hexa — 2-production parity) ──
# These 4 pub fns were ABSENT from this py mirror (a89a F3 2-production drift); ported here
# byte-for-byte from g6_ideation.hexa. Decode enters via the SAME generator L3 mouth as the
# hexa engine: the hexa g6_* fns call gen_clm_ideate / gen_clm_ideate_W / gen_auto_ideate;
# the py twins take the corresponding decode primitives from core/clm_decode.py /
# core/bytegpt_decode.py (the byte-parity-proven ports) — so the SCORING logic (kwr-gate,
# is_falsifiable, greedy jaccard distinctness) is identical, only the decode binding differs
# by the language's native mouth handle. (a_core_engine_map: still the ONE typed slot.)

def _clm_ideate(ckpt, frame, gen, top_k, temp, seed_rng):
    """g6_ideation.hexa::gen_clm_ideate twin — CLM-only seeded top-k (core/clm_decode.py)."""
    import clm_decode as _clm
    return _clm.clm_decode_topk_sampled(ckpt, frame, gen, top_k, temp, seed_rng)["text"]


def _clm_ideate_W(W, frame, gen, top_k, temp, seed_rng):
    """g6_ideation.hexa::gen_clm_ideate_W twin — loaded-W seeded top-k (core/clm_decode.py)."""
    import clm_decode as _clm
    return _clm.clm_decode_topk_sampled_W(W, frame, gen, top_k, temp, seed_rng)["text"]


def _auto_ideate(ckpt, frame, gen, top_k, temp, seed_rng):
    """g6_ideation.hexa::gen_auto_ideate twin — MOUTH-SNIFF dispatch (.clm OR ByteGPT)."""
    import clm_decode as _clm
    import bytegpt_decode as _bg
    if _bg.bg_is_bytegpt(ckpt):
        return _bg.bytegpt_decode_topk_sampled_ranged(ckpt, frame, gen, top_k, temp, seed_rng)["text"]
    return _clm.clm_decode_topk_sampled(ckpt, frame, gen, top_k, temp, seed_rng)["text"]


def g6_decode_best_of_k(ckpt, frame, gen, k, base_seed, known):
    """g6_ideation.hexa::g6_decode_best_of_k — best-of-K (offsets [0,101,202]) by (fals,kwr).
    Decode = CLM-only gen_clm_ideate twin (H_1381 best-of-K study)."""
    offsets = [0, 101, 202]
    best = ""; best_fals = -1; best_kwr = -1.0
    kk = k if k < 3 else 3
    for oi in range(kk):
        o = _clm_ideate(ckpt, frame, gen, 40, 0.7, base_seed + offsets[oi])
        kwr = _g6_known_word_ratio(o, known)
        fals = 1 if (kwr >= 0.5 and _g6_is_falsifiable(o, known)) else 0
        if fals > best_fals or (fals == best_fals and kwr > best_kwr):
            best_fals = fals; best_kwr = kwr; best = o
    return best


def g6_decode_best_of_k_W(W, frame, gen, k, base_seed, known):
    """g6_ideation.hexa::g6_decode_best_of_k_W — loaded-W twin (load .clm ONCE for the arm)."""
    offsets = [0, 101, 202]
    best = ""; best_fals = -1; best_kwr = -1.0
    kk = k if k < 3 else 3
    for oi in range(kk):
        o = _clm_ideate_W(W, frame, gen, 40, 0.7, base_seed + offsets[oi])
        kwr = _g6_known_word_ratio(o, known)
        fals = 1 if (kwr >= 0.5 and _g6_is_falsifiable(o, known)) else 0
        if fals > best_fals or (fals == best_fals and kwr > best_kwr):
            best_fals = fals; best_kwr = kwr; best = o
    return best


def g6_score_arm(ckpt, frames, gen, k, base_seed, best_of_k, known):
    """g6_ideation.hexa::g6_score_arm — CLM-only DIST/FALS arm. dist = greedy jaccard<=0.5."""
    texts = []; word_sets = []; fals = 0
    for f in frames:
        if best_of_k:
            o = g6_decode_best_of_k(ckpt, f, gen, k, base_seed, known)
        else:
            o = _clm_ideate(ckpt, f, gen, 40, 0.7, base_seed)
        texts.append(o)
        if _g6_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_g6_words(o))
            if _g6_is_falsifiable(o, known):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for kk in kept:
            if _g6_jaccard(ws, kk) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "texts": texts}


def g6_score_arm_auto(ckpt, frames, gen, base_seed, known, ideate=None):
    """g6_ideation.hexa::g6_score_arm_auto — CANONICAL mouth-agnostic G6 scoring op.
    IDENTICAL DIST/FALS/coherent logic to g6_score_arm, decode via the single typed entry
    gen_auto_ideate (sniffs .clm OR ByteGPT) — the op g_gates.g_eval_g6 calls (no dead inline
    duplicate). base_seed parameterizes the per-frame RNG (seeded base_seed+i; base_seed=7
    reproduces the old inline g_eval_g6 path frame-for-frame). `ideate` lets the g_gates _Mouth
    pass its pre-loaded-weight ideate (== gen_*_ideate_W: load ONCE for the arm); default =
    _auto_ideate (per-call sniff). The scoring is byte-identical either way."""
    if ideate is None:
        ideate = lambda f, g, sr: _auto_ideate(ckpt, f, g, 40, 0.7, sr)
    texts = []; word_sets = []; fals = 0
    for i in range(len(frames)):
        o = ideate(frames[i], gen, base_seed + i)
        texts.append(o)
        if _g6_known_word_ratio(o, known) >= 0.5:
            word_sets.append(_g6_words(o))
            if _g6_is_falsifiable(o, known):
                fals += 1
    kept = []
    for ws in word_sets:
        ok = True
        for kk in kept:
            if _g6_jaccard(ws, kk) > 0.5:
                ok = False
        if ok:
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "texts": texts}


def g6_sampler_selftest():
    """g6_ideation.hexa::g6_sampler_selftest -> generator.hexa::gen_g6_sampler_selftest.
    Exercise the engine's seeded top-k sampler on a SYNTHETIC peaked logits vector (NO model
    forward — fast, deterministic, smoke-safe). Returns {deterministic, diverse, in_topk}
    proving the best-of-K DEPTH lever. Uses the byte-parity clm_decode.py sampler primitives
    (_topk_sample / _mix32) — the py twin of clmd_topk_sample_pub / clmd_mix32_pub."""
    import numpy as _np
    import clm_decode as _clm
    v = 6
    lg = _np.array([1.0, 3.0, 2.0, 0.5, 5.0, 4.0], dtype=_np.float64)
    a, _ = _clm._topk_sample(lg, v, 3, 0.7, _clm._mix32(7))
    b, _ = _clm._topk_sample(lg, v, 3, 0.7, _clm._mix32(7))
    deterministic = (a == b)
    offs = [0, 101, 202]
    draws = []
    for o in offs:
        t, _ = _clm._topk_sample(lg, v, 5, 0.7, _clm._mix32(7 + o))
        draws.append(t)
    diverse = not (draws[0] == draws[1] and draws[1] == draws[2])
    in_topk = True
    s = _clm._mix32(11)
    for _ in range(40):
        t, s = _clm._topk_sample(lg, v, 3, 0.7, s)
        if t != 1 and t != 4 and t != 5:
            in_topk = False
    return {"deterministic": deterministic, "diverse": diverse, "in_topk": in_topk}


def g6_detector_calibration(known):
    """g6_ideation.hexa::g6_detector_calibration — frozen 10-string (5 pos/5 neg)."""
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
    correct = 0
    for p in pos:
        if _g6_is_falsifiable(p, known):
            correct += 1
    for nseg in neg:
        if not _g6_is_falsifiable(nseg, known):
            correct += 1
    return correct
