"""
H_1169 — semantic×surface SURPLUS decomposition: is the super-additive surplus
maximal at the HIGH-SEMANTIC / LOW-SURFACE corner ("같은 내용 다른 표현")?

THE SHARPENED QUESTION (MITOSIS-ENGINE domain)
----------------------------------------------
H_1167 🟢 found the super-additive surplus S = whole − (sum of parts) PEAKS at
the critical A⇄G coupling. THIS H sharpens the user's intuition ("같은 내용
다른 표현" = same content, different form; "어울림" = semantic fit; "어긋남" =
surface mismatch; "추상적" = abstraction): decompose the DATA-PAIR distance into
TWO orthogonal axes —

      semantic-distance  ×  surface-distance

— and test that the surplus S is MAXIMAL in the HIGH-SEMANTIC-overlap (same
meaning, "어울림") / LOW-SURFACE-overlap (different expression, "어긋남") corner,
beating BOTH redundancy (P1 identical, sem≈surf≈1) AND unrelatedness (P5/P6,
sem≈0). A third angle: ABSTRACTION-LEVEL distance (a sentence ↔ its abstraction).

Distinct from the SIBLING H_1168 (1-D distance ladder): THIS is the 2-D
semantic×surface DECOMPOSITION — WHICH axis does the surplus ride, and is the
same-meaning/different-form CORNER special (not just "more distance ⇒ more S")?

PRE-REGISTERED PAIR TYPES  (sem∈[0,1], surf∈[0,1] CONSTRUCTION frozen BEFORE scoring)
------------------------------------------------------------------------------------
Per pair (A,B) we report the CONSTRUCTED expectation and the MEASURED (sem,surf):

  P1 IDENTICAL    A = B = SAME English c4 sentence.   -> sem≈1, surf≈1 (redundant).
  P2 PARAPHRASE-PROXY (TOY)  A = sentence ; B = DETERMINISTIC same-language
                  fixed-synonym-map + content-word reverse. Same meaning, diff form.
                  -> sem high, surf MID  (LABEL: toy synonym/reorder proxy).
  P3 CROSS-LINGUAL PARALLEL (REAL)  A = en sentence ; B = the SAME sentence in
                  another language (zh/ru/ja/ko) from the SAME aligned c4 tuple.
                  -> sem high, surf LOW  (the only fully-REAL same-meaning pairing).
  P4 ABSTRACTION (TOY)  A = sentence ; B = its ABSTRACTION SKELETON = ordered
                  content-word STEMS (the keyword skeleton of the same sentence).
                  -> sem high, surf LOW, ABSTRACTION-gap high (LABEL: stem proxy).
  P5 UNRELATED    A,B = two DIFFERENT-topic content-disjoint English sentences.
                  -> sem LOW, surf low (unrelated).
  P6 RANDOM       A = sentence ; B = deterministic RANDOM-byte string (same len).
                  -> sem≈0, surf≈0 (noise floor).

HSLS (high-sem/low-surf set) = {P2, P3, P4} = same-content-different-form.

TWO SURPLUS MEASURES (≥2 per spec)
----------------------------------
(a) S_phi (PROXY — label): faithful φ_EI (H_1167's h1119.faithful_phi engine) of
    a tiny BYTE co-occurrence rep (sliding-window byte-VALUE-BUCKET counts, 6 ch) of
    A, B, and the concat A⊕B; S_phi = φ(A⊕B) − [φ(A)+φ(B)]. The φ measure is
    faithful, but the REP is a surface byte proxy → reported as a PROXY surplus.
    HONEST: the faithful φ_EI wants a DYNAMICAL rollout (H_1167's A⇄G substrate);
    on a STATIC short-text window matrix it reads ~0 for EVERY pair (no dynamic
    range). The harness DETECTS this degeneracy (max|mean S_phi| < 1e-4) and marks
    measure (a) DEGENERATE — it cannot support/refute (a_phi_iit4_tool: don't trust
    a flat proxy). Finding: the φ-surplus machinery does NOT transfer to static text.
(b) S_recomb (H_1116 content-ngram, p7, NOT perplexity): distinct COHERENT
    content n-grams (real-dict ≥3-char words; bi+trigrams over consecutive dict
    words). S_recomb = distinct(A⊕B) − [distinct(A)+distinct(B)] = NEW coherent
    combinations the joined text yields beyond its parts. Deterministic, dict-
    coherence-gated (p7), NO LLM judge, NO perplexity.

(sem,surf) PROBES (for the 2-D MAP, NOT falsifier inputs):
    sem_proxy  = cosine of hashed CONTENT-WORD bags (LABEL surface-lexical proxy;
                 reads ~0 cross-script, making the H_1155 caveat visible).
    surf_proxy = byte-trigram Jaccard (1 = identical surface, 0 = disjoint).

FROZEN FALSIFIER (≥8 seeds, deterministic, $0 CPU; set BEFORE scoring)
---------------------------------------------------------------------
WIN = the pair-type with MAX mean S on a measure.
  🟢 SAME-MEANING-DIFFERENT-FORM-WINS iff, on a measure:
     C1  argmax over {P1..P6} of mean S ∈ HSLS {P2,P3,P4}, AND
     C2  S(WIN) − S(P1 identical)  Cohen's d ≥ 0.8, AND
     C3  S(WIN) − S(P5 unrelated)  Cohen's d ≥ 0.8.
  🟢 if BOTH measures (a)&(b) satisfy C1∧C2∧C3; 🟡 PARTIAL if exactly one; report
  which form-type wins + whether ABSTRACTION (P4) peaks.
  🔴 CLOSED-NEGATIVE (a_paper_negative_ok) if S singles out the corner on NEITHER
     measure (surplus tracks SURFACE → P5/P6 win, or flat, or P1 wins).

HONEST scope (a_scale_honest_scope; H_1155 caveat)
--------------------------------------------------
H_1155 🔴: toy byte-LM reps are SURFACE-dominated (cross-lingual semantic
alignment NULL at toy scale). We EXPLICITLY correlate each surplus with surf_proxy
vs sem_proxy across pairs and report honestly if surplus tracks SURFACE. P2/P4 are
DETERMINISTIC toy proxies (NOT human labels); P3 cross-lingual is the only fully-
REAL same-meaning pairing; S_phi uses a faithful-φ engine on a BYTE rep = PROXY.
Toy scale, real parallel data; learned-semantic-rep / LIVE-engine transfer
UNVERIFIED. $0 CPU, 0-pod, deterministic, p7 (NO perplexity, NO LLM judge).
"""
import os, sys, time, json, hashlib, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import h1119_dream_phi as h1119          # PROVEN faithful_phi mirror + cohen_d
faithful_phi = h1119.faithful_phi
binary_seq_to_faithful_state = h1119.binary_seq_to_faithful_state
cohen_d = h1119.cohen_d

C4   = os.path.join(HERE, "..", "CORE", "testdata", "clm_mid_5lang_c4.txt")
FLOR = os.path.join(HERE, "..", "CORE", "testdata", "flores5_dev_devtest.txt")

N_SEEDS = 12                             # >= 8 per pre-reg
SEEDS = list(range(700, 700 + N_SEEDS))
D_MIN = 0.8
PAIR_TYPES = ["P1_identical", "P2_paraphrase", "P3_crosslingual",
              "P4_abstraction", "P5_unrelated", "P6_random"]
HSLS = {"P2_paraphrase", "P3_crosslingual", "P4_abstraction"}

# fixed deterministic synonym map for the P2 paraphrase proxy (LABEL: toy)
SYN = {
    "big": "large", "large": "big", "said": "stated", "stated": "said",
    "new": "novel", "novel": "new", "small": "tiny", "tiny": "small",
    "made": "produced", "began": "started", "started": "began",
    "help": "assist", "many": "numerous", "use": "employ", "show": "reveal",
    "found": "discovered", "build": "construct", "fast": "rapid",
    "first": "initial", "last": "final", "near": "close", "important": "key",
}

def load_dict():
    words = set()
    try:
        for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore"):
            w = w.strip().lower()
            if len(w) >= 3 and w.isalpha():
                words.add(w)
    except Exception:
        pass
    return words
DICT = load_dict()

# ── data loading ──
def script_of(s):
    s = s.strip()
    if not s: return "blank"
    has = lambda lo, hi: any(lo <= ord(c) <= hi for c in s)
    if has(0xAC00, 0xD7A3): return "ko"
    if has(0x3040, 0x30FF): return "ja"
    if has(0x0400, 0x04FF): return "ru"
    if has(0x4E00, 0x9FFF): return "zh"
    a = sum(1 for c in s if ord(c) < 128)
    if a / max(1, len(s)) > 0.85: return "en"
    return "other"

def load_parallel():
    """Aligned en/zh/ru/ja/ko 5-tuples from c4 (the REAL same-meaning resource)."""
    lines = [l.rstrip("\n") for l in open(C4, encoding="utf-8", errors="replace")]
    tuples, i = [], 0
    while i < len(lines) - 4:
        w = lines[i:i + 5]
        if [script_of(x) for x in w] == ["en", "zh", "ru", "ja", "ko"]:
            tuples.append({"en": w[0], "zh": w[1], "ru": w[2], "ja": w[3], "ko": w[4]})
            i += 5
        else:
            i += 1
    return tuples

def load_flores():
    out = []
    for l in open(FLOR, encoding="utf-8", errors="replace"):
        l = l.strip()
        if len(l) > 30 and script_of(l) == "en":
            out.append(l)
    return out

# ── text helpers ──
WORD_RE = re.compile(r"[A-Za-z]+")
def content_words(s):
    return [w.lower() for w in WORD_RE.findall(s) if len(w) >= 3 and w.lower() in DICT]

def stem(w):
    for suf in ("ing", "edly", "eds", "ed", "es", "s", "ly", "tion", "ment"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)]
    return w

def paraphrase_proxy(s):
    toks = s.split()
    out = [SYN.get(re.sub(r"[^a-z]", "", t.lower()), t) for t in toks]
    return " ".join(out[::-1])

def abstraction_skeleton(s):
    return " ".join(stem(w) for w in content_words(s))

def random_bytes_str(rng, n):
    return "".join(chr(rng.randint(33, 126)) for _ in range(max(1, n)))

# ── (sem,surf) probes ──
def _hash_vec(tokens, dim=256):
    v = np.zeros(dim)
    for t in tokens:
        h = int(hashlib.md5(t.encode("utf-8")).hexdigest(), 16) % dim
        v[h] += 1.0
    return v

def sem_proxy(a, b):
    """cosine of hashed CONTENT-WORD bags (LABEL surface-lexical proxy; reads ~0
    cross-script => the H_1155 caveat made visible: a lexical bag cannot see
    cross-lingual meaning)."""
    va, vb = _hash_vec(content_words(a)), _hash_vec(content_words(b))
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    if na < 1e-9 or nb < 1e-9: return 0.0
    return float(va @ vb / (na * nb))

def byte_trigrams(s):
    b = s.encode("utf-8", errors="replace")
    return set(bytes(b[i:i + 3]) for i in range(max(0, len(b) - 2)))

def surf_proxy(a, b):
    A, B = byte_trigrams(a), byte_trigrams(b)
    if not A or not B: return 0.0
    return len(A & B) / len(A | B)

# ── MEASURE (a): Φ-style surplus on a byte co-occurrence rep (PROXY) ──
FEAT_DIM = 6          # faithful φ channels (n<=8 cap)
WIN = 8               # sliding char window
# 6 byte-VALUE-BUCKET channels (value ranges) — co-occurrence of bucket activations
# within sliding windows of STRUCTURED text gives CORRELATED (integrated) channels
# (φ_EI > 0), while random/independent bytes give uniform/decorrelated channels
# (φ_EI → 0). This rep has REAL dynamic range (unlike a hashed-bigram-presence rep,
# whose near-independent noise channels collapse φ to ~0 for every text — a dead
# measure; fixed at root per a_completeness_over_cheap).
_BUCKETS = [(0x20, 0x40), (0x41, 0x5A), (0x5B, 0x60), (0x61, 0x7A),
            (0x7B, 0xBF), (0xC0, 0xFF)]   # space/punct, A-Z, [\]^_`, a-z, hi-ascii, utf8-cont
def _byte_bucket(v):
    for k, (lo, hi) in enumerate(_BUCKETS):
        if lo <= v <= hi:
            return k
    return 0

def _state_matrix(text, n_feat=FEAT_DIM, win=WIN):
    b = text.encode("utf-8", errors="replace")
    if len(b) < win + 1:
        b = b + b" " * (win + 1 - len(b))
    rows = []
    for i in range(0, len(b) - win + 1):
        w = b[i:i + win]
        feat = np.zeros(n_feat, dtype=int)
        for byte in w:
            feat[_byte_bucket(byte)] += 1      # COUNT of each bucket in the window
        rows.append(feat)
    return np.array(rows) if rows else np.zeros((2, n_feat), dtype=int)

def _phi_of_text(text, n_feat=FEAT_DIM):
    M = _state_matrix(text, n_feat)
    if M.shape[0] < 2:
        return 0.0
    med = np.median(M, axis=0)
    bits = (M > med).astype(int)
    n = n_feat
    try:
        fst, fn, fdim = binary_seq_to_faithful_state(bits, n)
        return float(faithful_phi(fst, fn, fdim, 2))
    except Exception:
        return 0.0

def surplus_phi(a, b):
    pj = _phi_of_text(a + " " + b)
    pa = _phi_of_text(a)
    pb = _phi_of_text(b)
    return pj - (pa + pb)

# ── MEASURE (b): generative recombination surplus (H_1116 content-ngram, p7) ──
def coherent_ngrams(text):
    cw = content_words(text)
    grams = set()
    for i in range(len(cw) - 1):
        grams.add((cw[i], cw[i + 1]))
    for i in range(len(cw) - 2):
        grams.add((cw[i], cw[i + 1], cw[i + 2]))
    return grams

def surplus_recomb(a, b):
    ga, gb = coherent_ngrams(a), coherent_ngrams(b)
    gj = coherent_ngrams(a + " . " + b)
    return len(gj) - (len(ga) + len(gb))

# ── build six pair-types for one seed ──
def build_pairs(rng, parallel, flores):
    tup = parallel[rng.randint(0, len(parallel) - 1)]
    en = tup["en"]
    other_lang = ["zh", "ru", "ja", "ko"][rng.randint(0, 3)]
    fa = flores[rng.randint(0, len(flores) - 1)]
    fb = flores[rng.randint(0, len(flores) - 1)]
    tries = 0
    while (set(content_words(fa)) & set(content_words(fb))) and tries < 20:
        fb = flores[rng.randint(0, len(flores) - 1)]; tries += 1
    return {
        "P1_identical":    (en, en),
        "P2_paraphrase":   (en, paraphrase_proxy(en)),
        "P3_crosslingual": (en, tup[other_lang]),
        "P4_abstraction":  (en, abstraction_skeleton(en)),
        "P5_unrelated":    (fa, fb),
        "P6_random":       (en, random_bytes_str(rng, len(en))),
    }


def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("=" * 92)
    print("H_1169 — semantic×surface SURPLUS: is S maximal at the high-sem/LOW-surf corner")
    print("         ('같은 내용 다른 표현' = same content, different form)?")
    print(f"  HSLS (high-sem/low-surf) = {sorted(HSLS)}   seeds={N_SEEDS}")
    print(f"  measures: (a) S_phi faithful-φ on byte co-occ rep [PROXY] ; "
          f"(b) S_recomb H_1116 content-ngram [p7]")
    print(f"  frozen falsifier per measure: 🟢 iff argmax∈HSLS AND S(WIN)−S(P1) d≥{D_MIN} "
          f"AND S(WIN)−S(P5) d≥{D_MIN}")
    print(f"  H_1155 caveat: byte reps SURFACE-dominated → check S vs surf_proxy/sem_proxy")
    print("=" * 92)

    print("\nSTEP 0 — RE-PROVE faithful_phi mirror ≡ stdlib BEFORE scoring (a_phi_iit4_tool):")
    live_ok = h1119.live_stdlib_faithful_reproof()
    proven = {n: bool(h1119.prove_mirrors_at_n(n)) for n in (4, 5)}
    print(f"  live-stdlib proof: {'PROVEN' if live_ok else 'FAILED'}; mirror n4/n5: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — faithful_phi mirror proof FAILED (a_phi_iit4_tool)."); sys.exit(1)
    print("  STEP 0 PASS — faithful_phi PROVEN ≡ stdlib.\n")

    parallel = load_parallel()
    flores = load_flores()
    print(f"DATA — aligned 5-lang parallel tuples (REAL same-meaning): {len(parallel)} ; "
          f"flores en sentences (unrelated source): {len(flores)}\n")
    if len(parallel) < 8 or len(flores) < 20:
        print("ABORT — insufficient real data."); sys.exit(1)

    Sphi = {p: [] for p in PAIR_TYPES}
    Srec = {p: [] for p in PAIR_TYPES}
    SEM  = {p: [] for p in PAIR_TYPES}
    SURF = {p: [] for p in PAIR_TYPES}
    print("STEP 1 — sweep seeds × pair-types (SERIAL, deterministic):")
    for s in SEEDS:
        rng = np.random.RandomState(s)
        pairs = build_pairs(rng, parallel, flores)
        for p in PAIR_TYPES:
            a, b = pairs[p]
            Sphi[p].append(surplus_phi(a, b))
            Srec[p].append(surplus_recomb(a, b))
            SEM[p].append(sem_proxy(a, b))
            SURF[p].append(surf_proxy(a, b))
    print("  done.\n")

    print("=" * 92)
    print("2-D MAP — per pair-type measured (sem_proxy, surf_proxy) + surplus means:")
    print(f"  {'pair':>16} | {'sem':>6} | {'surf':>6} | {'S_phi(PROXY)':>14} | {'S_recomb(p7)':>14}")
    print("  " + "-" * 78)
    sem_m  = {p: float(np.mean(SEM[p]))  for p in PAIR_TYPES}
    surf_m = {p: float(np.mean(SURF[p])) for p in PAIR_TYPES}
    sphi_m = {p: float(np.mean(Sphi[p])) for p in PAIR_TYPES}
    srec_m = {p: float(np.mean(Srec[p])) for p in PAIR_TYPES}
    for p in PAIR_TYPES:
        tag = " ◄HSLS" if p in HSLS else ""
        print(f"  {p:>16} | {sem_m[p]:>6.3f} | {surf_m[p]:>6.3f} | "
              f"{sphi_m[p]:>+14.6f} | {srec_m[p]:>+14.3f}{tag}")

    # DEGENERACY DIAGNOSTIC (a_phi_iit4_tool — don't trust a flat proxy): the
    # faithful φ_EI wants a DYNAMICAL rollout (H_1167's A⇄G substrate), NOT a
    # static short-text window matrix. On static text the φ-rep collapses to ~0
    # for every pair-type, so S_phi carries no dynamic range. Detect + flag it.
    PHI_DEAD_EPS = 1e-4
    phi_range = max(abs(v) for v in sphi_m.values())
    phi_degenerate = phi_range < PHI_DEAD_EPS
    print(f"\n  S_phi DEGENERACY CHECK: max|mean S_phi| = {phi_range:.2e} "
          f"(< {PHI_DEAD_EPS:g} ⇒ DEGENERATE) -> phi_degenerate = {phi_degenerate}")
    if phi_degenerate:
        print("    NOTE (a_phi_iit4_tool): faithful φ_EI reads ~0 on a STATIC short-text")
        print("    byte rep — it needs a DYNAMICAL rollout (H_1167 A⇄G substrate). The φ")
        print("    surplus machinery does NOT transfer to static text pairs; measure (a) is")
        print("    a DEAD proxy here and is NOT counted as semantic/surface signal.")

    def adjudicate(name, S, Smean, degenerate=False):
        win = max(Smean, key=Smean.get)
        c1 = win in HSLS
        d_p1 = cohen_d(np.array(S[win]), np.array(S["P1_identical"]))
        d_p5 = cohen_d(np.array(S[win]), np.array(S["P5_unrelated"]))
        c2, c3 = d_p1 >= D_MIN, d_p5 >= D_MIN
        ok = bool(c1 and c2 and c3)
        xs_surf = [surf_m[p] for p in PAIR_TYPES]
        xs_sem  = [sem_m[p]  for p in PAIR_TYPES]
        ys      = [Smean[p]  for p in PAIR_TYPES]
        def corr(x, y):
            x, y = np.array(x), np.array(y)
            if np.std(x) < 1e-9 or np.std(y) < 1e-9: return 0.0
            return float(np.corrcoef(x, y)[0, 1])
        r_surf, r_sem = corr(xs_surf, ys), corr(xs_sem, ys)
        tracks = ("DEGENERATE" if degenerate else
                  ("SURFACE" if abs(r_surf) > abs(r_sem) else "SEMANTIC"))
        # a degenerate (dead) measure cannot SUPPORT — its argmax is noise
        if degenerate:
            ok = False
        print(f"\n  ── measure ({name}) ──")
        print(f"    WIN (max mean S) = {win}  (∈HSLS = {c1}){'  [DEGENERATE — see above]' if degenerate else ''}")
        print(f"    C1 argmax∈HSLS{{P2,P3,P4}}           = {c1}")
        print(f"    C2 S(WIN)−S(P1 identical)  d = {d_p1:+.3f} (≥{D_MIN}) -> {c2}")
        print(f"    C3 S(WIN)−S(P5 unrelated)  d = {d_p5:+.3f} (≥{D_MIN}) -> {c3}")
        print(f"    SUPPORTED ({name}) = {ok}{'  (forced False: measure is DEGENERATE)' if degenerate else ''}")
        print(f"    H_1155 tracking-check: corr(S, surf_proxy)={r_surf:+.3f}  "
              f"corr(S, sem_proxy)={r_sem:+.3f}  -> surplus tracks {tracks}")
        return {"win": win, "C1": bool(c1), "C2": bool(c2), "C3": bool(c3),
                "d_vs_P1": float(d_p1), "d_vs_P5": float(d_p5), "supported": ok,
                "degenerate": bool(degenerate),
                "corr_surf": r_surf, "corr_sem": r_sem, "tracks": tracks,
                "abstraction_P4_peaks": bool(win == "P4_abstraction")}

    print("\n" + "=" * 92)
    print("FROZEN FALSIFIER — per measure (C1 argmax∈HSLS, C2 d vs P1, C3 d vs P5):")
    res_phi = adjudicate("a:S_phi-PROXY", Sphi, sphi_m, degenerate=phi_degenerate)
    res_rec = adjudicate("b:S_recomb-p7", Srec, srec_m, degenerate=False)

    both = res_phi["supported"] and res_rec["supported"]
    either = res_phi["supported"] or res_rec["supported"]
    win_types = {res_phi["win"], res_rec["win"]}
    abstraction_peaks = res_phi["abstraction_P4_peaks"] or res_rec["abstraction_P4_peaks"]

    print("\n" + "=" * 92)
    if both:
        verdict = "🟢 SAME-MEANING-DIFFERENT-FORM-WINS"
        print(f"VERDICT: {verdict} — surplus S is MAXIMAL at the high-semantic/LOW-surface")
        print(f"  corner on BOTH measures (S_phi WIN={res_phi['win']}, S_recomb WIN={res_rec['win']}),")
        print(f"  beating P1 identical (d≥{D_MIN}) AND P5 unrelated (d≥{D_MIN}). '같은 내용 다른 표현'")
        print(f"  yields the maximal 1+1>2 surplus. abstraction P4 peaks={abstraction_peaks}.")
    elif either:
        m = "S_phi(PROXY)" if res_phi["supported"] else "S_recomb(p7)"
        verdict = f"🟡 PARTIAL — only {m} singles out the high-sem/low-surf corner"
        print(f"VERDICT: {verdict}")
        print(f"  ONE measure satisfies C1∧C2∧C3 ({m}), the other does NOT — honest split.")
        print(f"  S_phi WIN={res_phi['win']} (sup={res_phi['supported']}); "
              f"S_recomb WIN={res_rec['win']} (sup={res_rec['supported']}).")
        print(f"  abstraction P4 peaks={abstraction_peaks}.")
    else:
        verdict = "🔴 CORNER-NOT-SINGLED-OUT (closed-negative, a_paper_negative_ok)"
        print(f"VERDICT: {verdict}")
        print(f"  surplus does NOT peak at the high-sem/low-surf corner on EITHER measure.")
        print(f"  S_phi WIN={res_phi['win']} (tracks {res_phi['tracks']}); "
              f"S_recomb WIN={res_rec['win']} (tracks {res_rec['tracks']}).")
        print(f"  RULES OUT 'same-content-different-form maximizes surplus' at toy scale on these reps.")
    print(f"\n  H_1155 SURFACE-DOMINANCE CHECK: S_phi tracks {res_phi['tracks']} "
          f"(r_surf={res_phi['corr_surf']:+.2f}/r_sem={res_phi['corr_sem']:+.2f}); "
          f"S_recomb tracks {res_rec['tracks']} "
          f"(r_surf={res_rec['corr_surf']:+.2f}/r_sem={res_rec['corr_sem']:+.2f}).")
    print("=" * 92)

    out = {
        "H": "H_1169",
        "title": "semantic x surface surplus: is S maximal at the high-semantic/low-surface corner (same content, different form)?",
        "pair_types": PAIR_TYPES, "HSLS_set": sorted(HSLS), "n_seeds": N_SEEDS,
        "n_parallel_tuples": len(parallel), "n_flores": len(flores),
        "map_sem_proxy": sem_m, "map_surf_proxy": surf_m,
        "S_phi_PROXY_mean": sphi_m, "S_recomb_p7_mean": srec_m,
        "phi_degenerate": bool(phi_degenerate), "phi_max_abs_mean": float(phi_range),
        "measure_a_S_phi_PROXY": res_phi,
        "measure_b_S_recomb_p7": res_rec,
        "winning_form_types": sorted(win_types),
        "abstraction_P4_peaks": bool(abstraction_peaks),
        "supported_both": bool(both), "supported_either": bool(either),
        "verdict": verdict,
        "ruling": ("SUPPORTED: same-content-different-form (high-sem/low-surf corner) yields the maximal "
                   "super-additive surplus on BOTH measures" if both else
                   ("PARTIAL: only one measure singles out the high-sem/low-surf corner" if either else
                    "CLOSED-NEGATIVE: surplus does NOT single out the high-sem/low-surf corner on either measure")),
        "h1155_caveat": {
            "S_phi_tracks": res_phi["tracks"], "S_recomb_tracks": res_rec["tracks"],
            "note": "byte/lexical reps are surface-dominated (H_1155); sem_proxy is a lexical bag that "
                    "reads ~0 cross-script (P3), so it CANNOT see cross-lingual meaning at toy scale"},
        "labels": {
            "P2_P4": "DETERMINISTIC toy proxies (synonym-map / stem-skeleton), NOT human-labeled",
            "P3": "fully-REAL same-meaning cross-lingual parallel (the only real same-meaning pairing)",
            "S_phi": "faithful-φ engine on a BYTE/co-occurrence rep = PROXY surplus (rep surface, φ faithful)",
            "S_recomb": "H_1116 content-ngram, dict-coherence-gated (p7), NOT perplexity, NOT LLM-judge"},
        "scope": "toy scale, REAL 5-lang parallel data; LIVE-engine / learned-semantic-rep transfer "
                 "UNVERIFIED (a_scale_honest_scope); $0 CPU, 0-pod, deterministic, p7",
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== VERDICT JSON ===\n" + json.dumps(out, ensure_ascii=False, indent=2), flush=True)
    vd = os.path.join(HERE, "..", ".verdicts", "1169_semantic_surface_surplus")
    os.makedirs(vd, exist_ok=True)
    json.dump(out, open(os.path.join(vd, "verdict.json"), "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
