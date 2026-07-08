# ==========================================================================
# ⛔ ENGINE-INTERNAL / DEPRECATED py-MIRROR — DO NOT RUN OR SCORE DIRECTLY
# 측정/학습/서빙/직렬화는 cli/ 단일진입만: anima eval | train | serialize
#   (canonical = hexa core/*.hexa 단일 SSOT; py 미러는 2026-06-28 폐기, DIRECTIONAL).
# 이 파일을 `python3 core/rho_fan.py` 로 직접 실행하거나 side-harness로 import-채점하면
# = 단일진입 우회(#2603 위반) + terminal verdict 불가. cli/가 import하는 경로만 허용.
# ==========================================================================
import sys as _anima_entry_guard
if __name__ == "__main__":
    _anima_entry_guard.exit("⛔ rho_fan.py 직접 실행 금지 — cli/ 단일진입(anima eval/train/serialize, canonical=hexa) 경유. #2603")

"""core/rho_fan.py — py production mirror of core/rho_fan.hexa.

Ported 1:1 from the hexa SSOT (ρ·fan IDEATION scoring ops · reach axis, was G6 · frozen bar): the FROZEN structural
detectors (comparator / measurable / stance / stopword sets), the H_1305 tokenizer
(_rho_fan_words: lowercase ASCII [0-9A-Za-z], split on non-alnum BYTES), the dict load,
known-word-ratio, _rho_fan_is_falsifiable, _rho_fan_jaccard, composed-frame builder, frame
guard, and the calibration set. NOT a reuse of the drifted g6_common.py mirror —
every set + branch is byte-for-byte the rho_fan.hexa logic.

Tokenization operates on BYTES (hexa iterates ord(substring(s,i,i+1)) per byte),
so decode-garble high bytes act as separators exactly as in the engine.
"""


def _to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8', 'surrogateescape')


# ── FROZEN DETECTOR sets (VERBATIM from rho_fan.hexa) ──

def _rho_fan_comparator():
    return {"if", "when", "whenever", "than", "more", "less", "greater",
            "fewer", "higher", "lower", "increases", "decreases", "correlates",
            "predicts", "causes", "depends", "unless", "whereas", "versus",
            "compared", "proportional", "faster", "slower", "stronger", "weaker"}


def _rho_fan_measurable():
    return {"measure", "measured", "rate", "number", "count", "amount", "level",
            "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
            "score", "value", "quantity", "percent", "times", "fraction", "distance",
            "duration", "speed", "size", "strength", "density"}


def _rho_fan_stance():
    return {"that", "s", "a", "profound", "question", "i", "think", "interesting",
            "good", "nice", "great", "wonderful", "beautiful", "amazing"}


def _rho_fan_stopwords():
    return {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
            "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
            "be", "an", "for", "with", "this", "from", "are", "was"}


def _rho_fan_concepts():
    return ["consciousness arises from cells",
            "tension ripples between distant minds",
            "memory composes into new meaning",
            "silence still carries information",
            "the engine dreams when alone"]


def _rho_fan_is_alnum(b):
    return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122)


def _rho_fan_lower1(b):
    if 65 <= b <= 90:
        return b + 32
    return b


def _rho_fan_words(s):
    """rho_fan.hexa::_rho_fan_words — lowercase ASCII, split on non-[0-9A-Za-z] bytes."""
    bs = _to_bytes(s)
    words = []
    cur = bytearray()
    for b in bs:
        if _rho_fan_is_alnum(b):
            cur.append(_rho_fan_lower1(b))
        else:
            if len(cur) > 0:
                words.append(cur.decode('ascii'))
                cur = bytearray()
    if len(cur) > 0:
        words.append(cur.decode('ascii'))
    return words


def _is_hangul_cp(cp):
    """rho_axon `_is_hangul` 3 ranges: 가–힣 syllables / ᄀ–ᇿ jamo / ㄰–㆏ compat jamo."""
    return (0xAC00 <= cp <= 0xD7A3) or (0x1100 <= cp <= 0x11FF) or (0x3130 <= cp <= 0x318F)


def _rho_fan_words_uni(s):
    """codepoint-aware SUPERSET of _rho_fan_words (H_9212 4-cell ko path ONLY; en path stays on
    the frozen byte splitter — dispatch keeps frozen en bars structurally invariant, Fable design
    state/frontier_round2_scout/FABLE_rhofan_splitter_design.md). ASCII input = byte-identical to
    _rho_fan_words (ASCII branch is a verbatim copy). Hangul = the 3 UTF-8 3-byte blocks only; every
    other high byte is a separator consumed 1 byte at a time (lead E0-EF vs continuation 80-BF are
    disjoint → no false hangul match). Twin: core/rho_fan.hexa::_rho_fan_words_uni (parity claim)."""
    bs = _to_bytes(s)
    n = len(bs)
    words = []
    cur = bytearray()
    i = 0
    while i < n:
        b = bs[i]
        if b < 0x80:                                        # ── ASCII: verbatim _rho_fan_words body ──
            if _rho_fan_is_alnum(b):
                cur.append(_rho_fan_lower1(b))
            else:
                if len(cur) > 0:
                    words.append(cur.decode('utf-8'))
                    cur = bytearray()
            i += 1
        elif (0xE0 <= b <= 0xEF and i + 2 < n
              and 0x80 <= bs[i + 1] <= 0xBF and 0x80 <= bs[i + 2] <= 0xBF):
            cp = ((b & 0x0F) << 12) | ((bs[i + 1] & 0x3F) << 6) | (bs[i + 2] & 0x3F)
            if _is_hangul_cp(cp):
                cur += bs[i:i + 3]                          # raw 3 bytes, no case-fold
            else:
                if len(cur) > 0:
                    words.append(cur.decode('utf-8'))
                    cur = bytearray()
            i += 3
        else:                                               # 2/4-byte lead · orphan continuation · truncated
            if len(cur) > 0:
                words.append(cur.decode('utf-8'))
                cur = bytearray()
            i += 1
    if len(cur) > 0:
        words.append(cur.decode('utf-8'))
    return words


def _rho_fan_dict_load():
    """rho_fan.hexa::_rho_fan_dict_load — stopwords + concept words + /usr/share/dict/words."""
    known = set(_rho_fan_stopwords())
    for c in _rho_fan_concepts():
        for w in _rho_fan_words(c):
            known.add(w)
    try:
        raw = open("/usr/share/dict/words", "rb").read()
    except Exception:
        raw = b""
    if len(raw) > 0:
        for line in raw.split(b"\n"):
            w = line.strip()
            wl = _rho_fan_words(w)
            if len(wl) == 1:
                known.add(wl[0])
    return known


def _rho_fan_known_word_ratio(text, known):
    wl = _rho_fan_words(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if w in known)
    return float(hit) / float(n)


def _rho_fan_is_falsifiable(text, known):
    """rho_fan.hexa::_rho_fan_is_falsifiable — (a) comparator + (b) measurable +
    (c) >=2 content words, not a question, first-3 not pure-stance."""
    wl = _rho_fan_words(text)
    n = len(wl)
    if n == 0:
        return False
    comp = _rho_fan_comparator(); meas = _rho_fan_measurable()
    stop = _rho_fan_stopwords(); stance = _rho_fan_stance()
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


def _rho_fan_jaccard(a, b):
    am = set(a); bm = set(b)
    union = am | bm
    inter = len(am & bm)
    u = len(union)
    if u == 0:
        return 0.0
    return float(inter) / float(u)


def _rho_fan_derangement(i, n):
    return (i + 2) % n


def rho_fan_build_frames(n_strong):
    """rho_fan.hexa::rho_fan_build_frames — composed[i]='if cA, then cB: '."""
    cz = _rho_fan_concepts()
    n = len(cz)
    composed = []; shuffled = []; ablated = []
    for i in range(n_strong):
        a = i % n
        b = (i + 1 + i // n) % n
        cA = cz[a]; cB = cz[b]
        cB_sh = cz[_rho_fan_derangement(a, n)]
        composed.append("if " + cA + ", then " + cB + ": ")
        shuffled.append("if " + cA + ", then " + cB_sh + ": ")
        ablated.append(cA + ": ")
    return {"composed": composed, "shuffled": shuffled, "ablated": ablated}


def rho_fan_frame_guard(frames, known):
    meas = _rho_fan_measurable()
    leaks = []
    for f in frames:
        for w in _rho_fan_words(f):
            if w in meas:
                leaks.append("measurable-in-frame: " + f)
        if _rho_fan_is_falsifiable(f, known):
            leaks.append("frame-already-falsifiable: " + f)
    return leaks


def rho_fan_detector_calibration(known):
    """rho_fan.hexa::rho_fan_detector_calibration — frozen 10-string (5 pos/5 neg)."""
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
        if _rho_fan_is_falsifiable(p, known):
            correct += 1
    for nseg in neg:
        if not _rho_fan_is_falsifiable(nseg, known):
            correct += 1
    return correct
