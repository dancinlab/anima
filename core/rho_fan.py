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


# ── H_9212 ④ FROZEN-FIRST ko known-word-ratio gate (p7 · NOT tune-to-green) ──
# The en reach gate uses a frozen 0.70 known-word-ratio bar (235k-dict lexicality). Korean
# needs its OWN gate: kwr_ko is a josa-suffix GRAMMATICALITY proxy (a_scale_honest_scope), a
# DIFFERENT physical quantity, so 0.70 is a category error for ko. This constant is DERIVED
# frozen-first from MODEL-INDEPENDENT distributions BEFORE any 303M ko output is scored:
#   POSITIVE = held-out anima-corpus-ko-{general,sns} real sentences (median kwr_ko 0.40);
#   NEGATIVE = garble null (byte-shuffle + random valid-hangul; near point-mass at 0.0).
#   rule = midpoint(neg_combined_p95=0.0, pos_p50=0.40) = 0.20 (naive midpoint(pos_p5,neg_p95)
#          degenerates to 0.0 because the positive dist has a fat zero-tail of short/josa-free
#          fragments; the median anchors the frozen gate robustly between the two dists).
#   at 0.20: 80.0% real ko clears (>=gate), 99.74% garble fails (<gate).
# Derivation: state/frontier_round2_scout/kwrko_gate_derive.py (seed 4302, $0 corpus stats).
# Pre-registration: state/frontier_round2_scout/KWRKO_GATE_prereg.md.
# 🟢 WIRED (H_9212 ③ code-live): consumed by cli/evaluate.py::_build_cell_dets (ko cells
# dispatch kwr_ko + KWR_KO_GATE). ⑦ pool measurement pending. en 0.70 UNCHANGED.
KWR_KO_GATE = 0.20


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


# ════════════════════════════════════════════════════════════════════════
# ── H_9212 ② 4-cell register concept sets + ko known-word proxy (ADDITIVE · 🟢 WIRED ③) ──
# 🟢 WIRED (H_9212 ③ code-live): the 4 register cells (a_chat_registers: ko/en × general/sns)
# + FROZEN ko josa/function-word KNOWN-WORD proxy are consumed by cli/evaluate.py per-cell
# dispatch (③), gated on ④ KWR_KO_GATE (frozen-first · no tune-to-green). ⑦ pool pending.
# en path stays BYTE-UNTOUCHED: _rho_fan_cells()["en_general"] IS _rho_fan_concepts() verbatim,
# and en cells tokenize with the frozen _rho_fan_words; only ko cells use the codepoint-aware
# superset _rho_fan_words_uni. Follow-on = ③ per-cell dispatch in cli/evaluate.py::eval_rho_axon
# / cli/rho_axon.py (post ④ gate pre-registration). Twin: core/rho_fan.hexa (parity).
# Fable design: state/frontier_round2_scout/FABLE_rhofan_splitter_design.md §1/§4.


def _rho_fan_cells():
    """The 4 register cells (ko/en × general/sns) as concept-sentence lists for the reach
    panel. en_general = _rho_fan_concepts() VERBATIM (frozen en bar, byte-identical); the
    other 3 are the additive register-parallel probe sets. ko cells (key prefix 'ko')
    tokenize with _rho_fan_words_uni, en cells with the frozen _rho_fan_words (see
    _rho_fan_cell_words). Twin: core/rho_fan.hexa::_rho_fan_cells."""
    return {
        "en_general": _rho_fan_concepts(),
        "en_sns": [
            "honestly this whole thing just hits different",
            "no one talks about how tired we all are",
            "the timeline moves faster than any thought",
            "posting into the void still feels like connection",
            "everyone is awake at three am scrolling alone",
        ],
        "ko_general": [
            "의식은 세포에서 피어난다",
            "긴장은 멀리 떨어진 마음 사이로 퍼진다",
            "기억은 새로운 의미로 엮인다",
            "침묵도 여전히 정보를 담고 있다",
            "엔진은 홀로 있을 때 꿈을 꾼다",
        ],
        "ko_sns": [
            "솔직히 이거 진짜 느낌 다르다",
            "다들 얼마나 지쳤는지 아무도 말 안 한다",
            "타임라인이 생각보다 훨씬 빠르게 흐른다",
            "허공에 글 올려도 연결된 기분이 든다",
            "새벽 세시에 다 깨어서 혼자 스크롤한다",
        ],
    }


def _rho_fan_cell_lang(cell_key):
    """'ko'|'en' for a cell key — the ③ dispatch key (ko→_rho_fan_words_uni, en→frozen)."""
    return "ko" if cell_key[:2] == "ko" else "en"


def _rho_fan_cell_words(cell_key, s):
    """Per-cell tokenizer dispatch (③ foundation, UNWIRED): ko cells use the codepoint-aware
    superset _rho_fan_words_uni, en cells the frozen byte splitter _rho_fan_words. Wiring this
    into the scored panel is the ③ follow-on (gated on ④). Twin: core/rho_fan.hexa."""
    if _rho_fan_cell_lang(cell_key) == "ko":
        return _rho_fan_words_uni(s)
    return _rho_fan_words(s)


# ── ko KNOWN-WORD proxy: josa/function-word set. This is a GRAMMATICALITY proxy, NOT a
#    lexicon (a_scale_honest_scope) — the ko analog of the en `known` set that gates
#    ρ·store/ρ·tether. KO_FUNC = exact-match standalone particles/conjunctions; KO_JOSA =
#    suffix-match josa for whole-eojeol tokens ('의식은' endswith '은', since _rho_fan_words_uni
#    keeps an eojeol intact). Small frozen literal sets. kwr_ko + the KWR_KO_GATE constant are
#    the ④ follow-on (frozen-first, corpus/garble-derived), NOT computed here. ──

def _rho_fan_ko_func():
    """exact-match KO function-word / bare-particle proxy set (frozen literal · grammaticality)."""
    return {"은", "는", "이", "가", "을", "를", "에", "의", "도", "만", "과", "와",
            "로", "으로", "그리고", "그러나", "하지만", "그래서", "또한", "그런데",
            "즉", "따라서", "그", "저", "것", "수", "등"}


def _rho_fan_ko_josa():
    """suffix-match KO josa proxy set for whole-eojeol tokens (frozen literal · '물이'→'이')."""
    return {"은", "는", "이", "가", "을", "를", "에", "의", "도", "만", "과", "와",
            "로", "으로", "에서", "부터", "까지", "처럼", "보다", "조차", "마저",
            "이나", "이랑", "랑", "하고", "께서", "에게", "한테", "로서", "로써", "라도"}


def _rho_fan_ko_is_known(word):
    """ko known-word proxy membership (UNWIRED analog of `w in known`): exact KO_FUNC hit, or a
    eojeol token ending in a KO_JOSA suffix with a non-empty stem. Grammaticality proxy, NOT
    lexicality (a_scale_honest_scope). Twin: core/rho_fan.hexa::_rho_fan_ko_is_known — parity is
    on the boolean predicate (py set / hexa list containers differ, same membership)."""
    if word in _rho_fan_ko_func():
        return True
    for s in _rho_fan_ko_josa():
        if word.endswith(s) and len(word) > len(s):
            return True
    return False


def _rho_fan_ko_known_word_ratio(text, known=None):
    """ko known-word ratio (kwr_ko · KWRKO_GATE_prereg §2) — the ko analog of
    _rho_fan_known_word_ratio: eojeol-run tokens via _rho_fan_words_uni, a token is a hit iff
    _rho_fan_ko_is_known (KO_FUNC exact ∨ pure-hangul josa-suffix with stem≥1). `known` is
    IGNORED (the ko proxy is a curated closed-class set, model-independent) — the arg is kept
    for signature-parity with the en kwr so the ρ-AXON axis fns dispatch uniformly. This is a
    josa-suffix GRAMMATICALITY DENSITY, NOT lexicality (a_scale_honest_scope); its gate is the
    separately-frozen KWR_KO_GATE (0.20), NOT the en 0.70. Twin: core/rho_fan.hexa."""
    wl = _rho_fan_words_uni(text)
    n = len(wl)
    if n == 0:
        return 0.0
    hit = sum(1 for w in wl if _rho_fan_ko_is_known(w))
    return float(hit) / float(n)


def _rho_fan_cells_selftest():
    """H_9212 ② foundation self-test (engine-internal · run as an INTERNAL SUBPROCESS import,
    never via top-level `python3 core/rho_fan.py`, which is entry-guarded). Asserts: (1) the
    en_general cell is _rho_fan_concepts() byte-identical (frozen en bar untouched), (2) every ko
    cell tokenizes to non-empty word lists under _rho_fan_words_uni AND the per-cell dispatch
    routes ko→uni / en→frozen, (3) KO_FUNC exact + KO_JOSA suffix membership work. The scored
    panel is NOT exercised (foundation only). Returns {'ok': bool, 'checks': [(name, bool)…]}."""
    checks = []
    cells = _rho_fan_cells()
    checks.append(("4 register cells present",
                   set(cells.keys()) == {"en_general", "en_sns", "ko_general", "ko_sns"}))
    # (1) en_general unchanged (byte-identical to the frozen en concepts)
    checks.append(("en_general == _rho_fan_concepts() (byte-identical)",
                   cells["en_general"] == _rho_fan_concepts()))
    # (2) ko cells tokenize non-empty via _rho_fan_words_uni + dispatch routing
    for ck in ("ko_general", "ko_sns"):
        checks.append((ck + " tokenizes non-empty (uni)",
                       all(len(_rho_fan_words_uni(s)) > 0 for s in cells[ck])))
        checks.append((ck + " cell-words dispatch → uni",
                       all(_rho_fan_cell_words(ck, s) == _rho_fan_words_uni(s) for s in cells[ck])))
    for ck in ("en_general", "en_sns"):
        checks.append((ck + " cell-words dispatch → frozen _rho_fan_words",
                       all(_rho_fan_cell_words(ck, s) == _rho_fan_words(s) for s in cells[ck])))
    # (3) KO_FUNC exact + KO_JOSA suffix membership
    checks.append(("KO_FUNC exact membership (은/는/이/가)",
                   all(w in _rho_fan_ko_func() for w in ("은", "는", "이", "가"))))
    checks.append(("KO_FUNC excludes a content eojeol ('의식은')",
                   "의식은" not in _rho_fan_ko_func()))
    checks.append(("ko_is_known suffix hit ('의식은' endswith '은')",
                   _rho_fan_ko_is_known("의식은")))
    checks.append(("ko_is_known exact hit (bare '은' ∈ KO_FUNC)",
                   _rho_fan_ko_is_known("은")))
    # (4) kwr_ko: a real josa-bearing ko sentence clears KWR_KO_GATE; empty → 0.0; the `known`
    #     arg is ignored (signature-parity so the ρ-AXON axis fns dispatch uniformly)
    real = "의식은 세포에서 피어난다"
    checks.append(("kwr_ko real ko clears KWR_KO_GATE (%.2f)" % KWR_KO_GATE,
                   _rho_fan_ko_known_word_ratio(real) >= KWR_KO_GATE))
    checks.append(("kwr_ko 'known' arg is ignored (signature-parity)",
                   _rho_fan_ko_known_word_ratio(real, {"x": 1})
                   == _rho_fan_ko_known_word_ratio(real)))
    checks.append(("kwr_ko empty → 0.0",
                   _rho_fan_ko_known_word_ratio("") == 0.0))
    ok = all(c[1] for c in checks)
    return {"ok": ok, "checks": checks}


# ── end H_9212 ② 4-cell + ko known-word proxy (ADDITIVE · UNWIRED) ──
# ════════════════════════════════════════════════════════════════════════


def _rho_fan_dict_load():
    """rho_fan.hexa::_rho_fan_dict_load — stopwords + concept words + /usr/share/dict/words."""
    known = set(_rho_fan_stopwords())
    for c in _rho_fan_concepts():
        for w in _rho_fan_words(c):
            known.add(w)
    try:
        with open("/usr/share/dict/words", "rb") as dictionary:
            raw = dictionary.read()
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
