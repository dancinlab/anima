#!/usr/bin/env python3
"""B-1 FALS-precursor 분해 게이지 (H_9128 STEP-0, DIRECTIONAL).

탐지기 core/g6_ideation.py::_g6_is_falsifiable 의 5-conjunct 를 개별로 재채점한다.
목적: 어느 conjunct 가 병목(dead)인지 지도화. 예측: measurable(b) 단독.

★DIRECTIONAL: 입력 continuation 은 bytegpt303 h1129 BYTE mouth py numpy decode
  (state/g6_targeted_corpus/results/{base,targeted,shuf}.json 의 comp_texts/shuf_texts).
  텍스트 스캔 자체도 numpy/torch 아닌 순수 py 이지만 303M engine-native decode 아님
  → a_engine_native_learning 상 DIRECTIONAL. 수치 verbatim, tune-to-green 없음.

frozen 세트/토크나이저/predicate 는 core/g6_ideation.py 에서 verbatim 복제(import-우회 회피).
"""
import json, os

# ── FROZEN DETECTOR sets — VERBATIM from core/g6_ideation.py (g6_ideation.hexa SSOT) ──
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater",
              "fewer", "higher", "lower", "increases", "decreases", "correlates",
              "predicts", "causes", "depends", "unless", "whereas", "versus",
              "compared", "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}
STOPWORDS = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
             "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
             "be", "an", "for", "with", "this", "from", "are", "was"}
CONCEPTS = ["consciousness arises from cells",
            "tension ripples between distant minds",
            "memory composes into new meaning",
            "silence still carries information",
            "the engine dreams when alone"]


def _to_bytes(s):
    if isinstance(s, bytes):
        return s
    return s.encode('utf-8', 'surrogateescape')


def _is_alnum(b):
    return (48 <= b <= 57) or (65 <= b <= 90) or (97 <= b <= 122)


def _lower1(b):
    return b + 32 if 65 <= b <= 90 else b


def g6_words(s):
    """g6_ideation.hexa::_g6_words — lowercase ASCII [0-9A-Za-z], split on non-alnum BYTES."""
    bs = _to_bytes(s)
    words = []
    cur = bytearray()
    for b in bs:
        if _is_alnum(b):
            cur.append(_lower1(b))
        else:
            if cur:
                words.append(cur.decode('ascii')); cur = bytearray()
    if cur:
        words.append(cur.decode('ascii'))
    return words


def dict_load():
    known = set(STOPWORDS)
    for c in CONCEPTS:
        for w in g6_words(c):
            known.add(w)
    try:
        raw = open("/usr/share/dict/words", "rb").read()
    except Exception:
        raw = b""
    for line in raw.split(b"\n"):
        wl = g6_words(line.strip())
        if len(wl) == 1:
            known.add(wl[0])
    return known


def known_word_ratio(text, known):
    wl = g6_words(text)
    if not wl:
        return 0.0
    return sum(1 for w in wl if w in known) / len(wl)


def conjuncts(text, known):
    """5-conjunct + kwr coherence gate 를 개별 채점. True=그 조건 통과.

    실 엔진(core/g6_ideation.hexa g6_decode_best_of_k L278)은 fals 판정 전
    `kwr >= 0.5 && _g6_is_falsifiable(o)` — kwr≥0.5 coherence gate 가 0번째 전제.
    """
    wl = g6_words(text)
    n = len(wl)
    kwr = known_word_ratio(text, known)
    g = kwr >= 0.5                                            # (g) coherence gate kwr>=0.5
    if n == 0:
        return dict(g=g, a=False, b=False, c=False, d=True, e=True, n=0, content=0, kwr=kwr)
    a = any(w in COMPARATOR for w in wl)                      # (a) comparator >=1
    b = any(w in MEASURABLE for w in wl)                      # (b) measurable  >=1
    content = sum(1 for w in wl if len(w) >= 3 and w in known and w not in STOPWORDS)
    c = content >= 2                                          # (c) content >=2
    tr = _to_bytes(text).strip()
    d = not (len(tr) > 0 and tr[-1] == 63)                    # (d) not trailing '?'
    nf = 3 if n >= 3 else n
    allstance = all(wl[f] in STANCE for f in range(nf)) if nf > 0 else False
    e = not allstance                                        # (e) first-3 not pure-stance
    return dict(g=g, a=a, b=b, c=c, d=d, e=e, n=n, content=content, kwr=kwr)


def is_falsifiable(cj):
    # 순수 5-conjunct (탐지기 _g6_is_falsifiable 본체). kwr gate 는 호출측(g)이라 분리.
    return cj['a'] and cj['b'] and cj['c'] and cj['d'] and cj['e']


def is_fals_gated(cj):
    # 실 엔진 fals=1 조건 (kwr>=0.5 AND 5-conjunct).
    return cj['g'] and is_falsifiable(cj)


def lam_ascii(text):
    """continuation ASCII-영어 비율 = printable-ascii-letter/space 바이트 / 전체 바이트."""
    bs = _to_bytes(text)
    if not bs:
        return 0.0
    good = sum(1 for x in bs if (65 <= x <= 90) or (97 <= x <= 122) or x == 32)
    return good / len(bs)


def digit_rate(text):
    bs = _to_bytes(text)
    if not bs:
        return 0.0
    return sum(1 for x in bs if 48 <= x <= 57) / len(bs)


CONJ = ['g', 'a', 'b', 'c', 'd', 'e']
NAMES = {'g': 'kwr>=0.5(coherence)', 'a': 'comparator>=1', 'b': 'measurable>=1',
         'c': 'content>=2', 'd': 'not-question', 'e': 'not-pure-stance'}


def score_group(texts_meta, known):
    """texts_meta: list of (arm,kind,seed,i,text). Return per-conjunct fail map + rows."""
    N = len(texts_meta)
    fail = {k: 0 for k in CONJ}
    fals_gated = 0
    lam_sum = 0.0; dig_sum = 0.0; kwr_sum = 0.0
    blocker = {k: 0 for k in CONJ}
    sole = {k: 0 for k in CONJ}
    rows = []
    for (arm, kind, seed, i, t) in texts_meta:
        cj = conjuncts(t, known)
        fg = is_fals_gated(cj)
        la = lam_ascii(t); dr = digit_rate(t)
        lam_sum += la; dig_sum += dr; kwr_sum += cj['kwr']
        if fg:
            fals_gated += 1
        for k in CONJ:
            if not cj[k]:
                fail[k] += 1
        if not fg:
            failing = [k for k in CONJ if not cj[k]]
            for k in failing:
                blocker[k] += 1
            if len(failing) == 1:
                sole[failing[0]] += 1
        rows.append(dict(arm=arm, kind=kind, seed=seed, frame=i,
                         **{k: cj[k] for k in CONJ},
                         content=cj['content'], kwr=round(cj['kwr'], 4), n=cj['n'],
                         fals=fg, lam_ascii=round(la, 4), digit=round(dr, 4), text=t))
    dead = max(CONJ, key=lambda k: fail[k])
    return dict(
        n=N, n_fals_gated=fals_gated, p_fals=round(fals_gated / N, 4) if N else 0.0,
        fail_count={f"{k}:{NAMES[k]}": fail[k] for k in CONJ},
        fail_rate={f"{k}:{NAMES[k]}": round(fail[k] / N, 4) for k in CONJ} if N else {},
        blocker_count={f"{k}:{NAMES[k]}": blocker[k] for k in CONJ},
        sole_blocker_count={f"{k}:{NAMES[k]}": sole[k] for k in CONJ},
        mean_lam_ascii=round(lam_sum / N, 4) if N else 0.0,
        mean_digit_rate=round(dig_sum / N, 4) if N else 0.0,
        mean_kwr=round(kwr_sum / N, 4) if N else 0.0,
        dead_conjunct=f"{dead}:{NAMES[dead]}",
        dead_fail_rate=round(fail[dead] / N, 4) if N else 0.0,
    ), rows


def main():
    known = dict_load()
    src_dir = os.path.join(os.path.dirname(__file__), "..", "..", "g6_targeted_corpus", "results")
    src_dir = os.path.normpath(src_dir)
    by_arm = {a: [] for a in ['base', 'targeted', 'shuf']}
    allmeta = []
    for arm in ['base', 'targeted', 'shuf']:
        d = json.load(open(os.path.join(src_dir, f"{arm}.json")))
        for s in d.get('per_seed', []):
            seed = s['seed']
            for kind in ('comp_texts', 'shuf_texts'):
                for i, t in enumerate(s.get(kind, [])):
                    by_arm[arm].append((arm, kind, seed, i, t))
                    allmeta.append((arm, kind, seed, i, t))

    per_arm = {}
    all_rows = []
    for arm in ['base', 'targeted', 'shuf']:
        summ, rows = score_group(by_arm[arm], known)
        per_arm[arm] = summ
        all_rows += rows
    agg, _ = score_group(allmeta, known)

    out = dict(
        probe="H_9128 B-1 FALS-precursor decompose gauge",
        verdict_axis="DIRECTIONAL (bytegpt303 h1129 BYTE mouth py-numpy decode, NOT 303M engine-native)",
        source="state/g6_targeted_corpus/results/{base,targeted,shuf}.json comp_texts(continuation-only)",
        note=("scored text = continuation ALONE (=`o` from g6_decode_best_of_k), byte-reproduces "
              "stored fals_per_seed exactly. 6 precursors incl. kwr>=0.5 coherence gate (hexa L278). "
              "BASE arm = wall condition (untrained mouth); TARGETED/SHUF = corpus-injected condition."),
        detector_ref="core/g6_ideation.hexa g6_decode_best_of_k L278 + _g6_is_falsifiable (frozen sets verbatim)",
        dict_words="/usr/share/dict/words (235976)",
        per_arm=per_arm,
        aggregate=agg,
        rows=all_rows,
    )
    with open(os.path.join(os.path.dirname(__file__), "b1_result.json"), "w") as fp:
        json.dump(out, fp, indent=1, ensure_ascii=False)

    for arm in ['base', 'targeted', 'shuf']:
        s = per_arm[arm]
        tag = 'WALL (untrained mouth)' if arm == 'base' else 'corpus-injected'
        print(f"\n== {arm.upper()}  [{tag}]  N={s['n']}  P(fals_gated)={s['p_fals']}  "
              f"mean_kwr={s['mean_kwr']}  lam_ascii={s['mean_lam_ascii']}  digit={s['mean_digit_rate']}")
        print("   precursor FAIL rate (higher=deader):")
        for k in CONJ:
            print(f"     {k} {NAMES[k]:20s} fail {s['fail_count'][f'{k}:{NAMES[k]}']:2d}/{s['n']} "
                  f"= {s['fail_rate'][f'{k}:{NAMES[k]}']:.3f}   sole={s['sole_blocker_count'][f'{k}:{NAMES[k]}']}")
        print(f"   DEAD = {s['dead_conjunct']} ({s['dead_fail_rate']})")


if __name__ == "__main__":
    main()
