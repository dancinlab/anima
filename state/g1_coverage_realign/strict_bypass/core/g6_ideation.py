# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/g6_ideation.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ g6_ideation.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

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
