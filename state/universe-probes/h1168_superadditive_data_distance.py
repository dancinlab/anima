"""
H_1168 — does the super-additive surplus S = φ_joint − Σφ_parts ("the 1+1>2
advantage") have an OPTIMAL-OFFSET sweet spot on a DATA-DISTANCE axis, on REAL
parallel multilingual data? — "어긋나 어울림" (offset-but-harmonious).

H_1167 (toy substrate) showed the surplus PEAKS at the critical COUPLING γ
(inverted-U over an interaction knob). The user sharpens: on REAL DATA, which
DATA-PAIRINGS produce that super-additive harmony? Hypothesis — map the H_1167
inverted-U onto a DATA-DISTANCE axis: two parts A,B that are IDENTICAL are
redundant (no surplus), two parts that are UNRELATED don't integrate (no
surplus), but two parts at a JUST-RIGHT intermediate offset (predicted: SAME
meaning, DIFFERENT script = cross-lingual parallel) maximize the whole-minus-sum.

REAL DATA (parallel multilingual, line-aligned by block):
  CORE/testdata/flores5_dev_devtest.txt — 5 language blocks of 997 lines each
     (en[0:997] zh[997:1994] ru[1994:2991] ja[2991:3988] ko[3988:4985]); line i
     in each block is the SAME sentence (same meaning, different script) = the
     natural "어긋나 어울림" point.
  CORE/testdata/clm_mid_5lang_c4.txt — 5-lang corpus for related/unrelated sampling.

DATA-DISTANCE LADDER (pre-registered, exact, FROZEN — operationalize distance
between the two parts A,B; B is constructed relative to A at each rung):
  d0 IDENTICAL          : B = A                          (same text twice — redundant)
  d1 PARAPHRASE/NEAR    : B = a lightly byte-perturbed A (same lang, high overlap)
  d2 CROSS-LINGUAL PARALLEL : A,B = the SAME flores sentence in two DIFFERENT langs
                             (same meaning, different script) — PREDICTED PEAK
  d3 TOPICAL            : A,B = different sentences, SAME language/block (related)
  d4 UNRELATED          : A,B = different sentences, DIFFERENT far-apart source
  d5 RANDOM             : B = random bytes (no harmony)

We measure SURPLUS S(d) = M_joint(A⊕B) − [M(A) + M(B)] at each rung, on TWO
distinct DATA TYPES / measures so the result is not measure-specific:

  (a) FAITHFUL-Φ-STYLE INTEGRATION surplus (REUSES the H_1119 PROVEN faithful
      IIT-4.0 mirror ≡ stdlib, n=6 exact MIP-EI, re-proved BEFORE scoring per
      a_phi_iit4_tool). Each part is rendered as a 6-channel binary time-series by
      a DETERMINISTIC byte-bigram feature hash; φ(part) = within-part integration;
      φ_joint = integration of the 6-channel system whose channels 0..2 carry A's
      features and 3..5 carry B's features at matched time-steps. S_a = φ_joint −
      [φ(A) + φ(B)]. This IS faithful φ (NOT a proxy) on a byte representation of
      the pair; the byte→channel rendering is a representation choice, labelled.

  (b) GENERATIVE-RECOMBINATION surplus (REUSES the H_1116 content-ngram metric:
      real-dict coherence-gated bigrams over consecutive ≥3-char dict words, p7,
      NOT perplexity / NOT LLM-judge). distinct(X) = # of coherent content-bigrams
      in X. S_b = distinct(A⊕B) − [distinct(A) + distinct(B)] = the EXTRA distinct
      coherent combinations the joined pair yields beyond the two parts apart.

FROZEN FALSIFIER (≥8 seeds, deterministic, $0 CPU):
  🟢 OPTIMAL-OFFSET iff, on a measure, S(d) has an INTERIOR argmax at an
     intermediate distance (NOT d0/identical, NOT d5/random) AND
     S(peak) − S(d0) Cohen's d ≥ 0.8 AND S(peak) − S(d5) Cohen's d ≥ 0.8.
  SUPPORTED iff this holds on BOTH measures (a) AND (b); report honestly if only
  one holds. Report WHICH distance wins (is it d2 cross-lingual, as predicted?).
  🔴 CLOSED-NEGATIVE iff S is monotone / peaks at an endpoint / flat on both →
     super-additivity has NO data-distance sweet spot at this scale
     (a_paper_negative_ok).

SCOPE: real-data SAMPLE, toy faithful-φ n=6 + byte rendering, a_scale_honest_scope.
Measure (a) IS faithful φ (proven mirror); the byte→6ch rendering is labelled a
representation choice, not a proxy-Φ. Measure (b) is deterministic content-ngram,
NOT perplexity (p7).
"""
import os, sys, time, json, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import h1119_dream_phi as h1119          # PROVEN faithful_phi mirror + reproof helpers

CH = h1119.CH                            # = 6 (n=6 exact MIP-EI joint system)
faithful_phi = h1119.faithful_phi
binary_seq_to_faithful_state = h1119.binary_seq_to_faithful_state

REPO = os.path.join(HERE, "..")
FLORES = os.path.join(REPO, "CORE", "testdata", "flores5_dev_devtest.txt")
C4 = os.path.join(REPO, "CORE", "testdata", "clm_mid_5lang_c4.txt")

# flores block layout (verified by script-transition scan): 5 blocks × 997 lines.
BLOCK = 997
LANGS = ["en", "zh", "ru", "ja", "ko"]
BLOCKS = {lg: (i * BLOCK, (i + 1) * BLOCK) for i, lg in enumerate(LANGS)}

N_SEEDS = 12
SEEDS = list(range(700, 700 + N_SEEDS))
T_STEPS = 600            # time-steps per part rendering (byte-bigram walk)
D_MIN = 0.8

LADDER = ["d0_identical", "d1_paraphrase", "d2_xling_parallel",
          "d3_topical", "d4_unrelated", "d5_random"]

# ───────────────────────── real-data loaders ──────────────────────────────
def load_flores():
    lines = open(FLORES, encoding="utf-8", errors="ignore").read().splitlines()
    return {lg: lines[a:b] for lg, (a, b) in BLOCKS.items()}

def load_c4():
    return [l for l in open(C4, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]

# ───────────── measure (a): faithful-φ on a byte rendering ─────────────────
def text_to_channels(text, n_ch, t_steps, seed_salt):
    """DETERMINISTIC byte-bigram feature hash → (t_steps × n_ch) real activations.
    Walks the UTF-8 byte stream; each byte-bigram is hashed (sha256, stable) into a
    channel index and a ±sign, accumulated into a leaky channel state sampled at
    t_steps evenly. No model, no randomness beyond the fixed seed_salt. This renders
    a TEXT as a multi-channel signal so the PROVEN faithful φ can be applied to it."""
    b = text.encode("utf-8", errors="ignore")
    if len(b) < 2:
        b = (b + b"\x00\x00")
    st = np.zeros(n_ch)
    W = np.empty((t_steps, n_ch))
    L = max(1, len(b) - 1)
    salt = seed_salt.encode()
    for t in range(t_steps):
        # cover the bigram stream, looping deterministically across t_steps
        i = (t * 7919) % L            # 7919 prime stride for spread
        bg = bytes([b[i], b[i + 1]]) if len(b) >= 2 else b"\x00\x00"
        hh = hashlib.sha256(salt + bg).digest()
        ch = hh[0] % n_ch
        sign = 1.0 if (hh[1] & 1) else -1.0
        mag = 0.5 + (hh[2] / 255.0)   # 0.5..1.5
        st *= 0.85                    # leaky
        st[ch] += sign * mag
        W[t] = st
    return W

def phi_of_W(W):
    """faithful φ of a (T×CH) activation matrix — median-binarize per channel then
    the PROVEN mirror (≡ stdlib, BITS/log2), identical recipe to h1119.phi_stage."""
    med = np.median(W, axis=0)
    bits = (W > med).astype(int)
    fst, fn, fdim = binary_seq_to_faithful_state(bits, CH)
    return faithful_phi(fst, fn, fdim, 2)

def surplus_phi(A, B, seed):
    """S_a = φ_joint(A⊕B) − [φ(A)+φ(B)]. Parts rendered on all 6 channels each;
    JOINT = 6-ch system with channels 0..2 from A's 3-ch render + 3..5 from B's."""
    salt = f"s{seed}"
    WA = text_to_channels(A, CH, T_STEPS, salt + "A")
    WB = text_to_channels(B, CH, T_STEPS, salt + "B")
    phiA = phi_of_W(WA)
    phiB = phi_of_W(WB)
    # joint 6-ch system: 3 channels carrying A's features, 3 carrying B's, matched t
    WA3 = text_to_channels(A, 3, T_STEPS, salt + "Aj")
    WB3 = text_to_channels(B, 3, T_STEPS, salt + "Bj")
    WJ = np.concatenate([WA3, WB3], axis=1)   # (T × 6)
    phiJ = phi_of_W(WJ)
    return phiJ - (phiA + phiB)

# ───────────── measure (b): content-ngram recombination (H_1116) ──────────
import re as _re
_DICT = None
def dictwords():
    global _DICT
    if _DICT is None:
        try:
            _DICT = set(w.strip().lower() for w in open("/usr/share/dict/words")
                        if len(w.strip()) >= 3)
        except Exception:
            _DICT = set()
    return _DICT

def words(s):
    return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())

def content_bigrams(text):
    """coherence-gated content bigrams: CONSECUTIVE real-dict (≥3 char) words, the
    H_1116/H_1140 p7 metric (deterministic, NOT perplexity). For non-Latin scripts
    that don't hit the en dict, fall back to ≥2-char token bigrams so cross-lingual
    parts still contribute (a coherent surface combination)."""
    d = dictwords()
    w = words(text)
    cw = [x for x in w if (x in d and len(x) >= 3)]
    bg = set(zip(cw, cw[1:]))
    if not bg:
        # non-Latin / dict-miss fallback: surface token bigrams (≥2 char)
        tw = [x for x in w if len(x) >= 2]
        bg = set(zip(tw, tw[1:]))
    return bg

def distinct(text):
    return len(content_bigrams(text))

def surplus_recomb(A, B):
    """S_b = distinct(A⊕B) − [distinct(A) + distinct(B)]. The joined pair's EXTRA
    coherent content-bigrams beyond the two parts measured apart (cross-boundary +
    de-dup). Identical parts → A⊕B has ~the same set → surplus ≈ −distinct(A) (very
    negative, redundant); offset parts that share boundary structure → positive."""
    joint = distinct(A + " " + B)
    return joint - (distinct(A) + distinct(B))

# ─────────────────────── pair construction per rung ───────────────────────
def perturb(text, rng):
    """light byte-level perturbation: flip ~5% of byte positions to a neighbor
    (same-language near-paraphrase proxy; preserves most surface, small offset)."""
    b = bytearray(text.encode("utf-8", errors="ignore"))
    n = max(1, int(len(b) * 0.05))
    for _ in range(n):
        if not b:
            break
        i = int(rng.integers(0, len(b)))
        b[i] = (b[i] + 1) % 256
    return b.decode("utf-8", errors="ignore")

def build_pair(rung, flores, c4, rng):
    """Return (A,B) for the given distance rung, drawn deterministically from rng."""
    en = flores["en"]
    li = int(rng.integers(0, BLOCK))
    A = en[li].strip()
    while len(A) < 8:
        li = int(rng.integers(0, BLOCK)); A = en[li].strip()
    if rung == "d0_identical":
        return A, A
    if rung == "d1_paraphrase":
        return A, perturb(A, rng)
    if rung == "d2_xling_parallel":
        # SAME flores sentence (same line index), two DIFFERENT languages
        lg = LANGS[1 + int(rng.integers(0, 4))]   # zh/ru/ja/ko
        B = flores[lg][li].strip()
        return A, B
    if rung == "d3_topical":
        # different sentence, SAME (en) block — related domain, not parallel
        lj = int(rng.integers(0, BLOCK))
        while lj == li:
            lj = int(rng.integers(0, BLOCK))
        return A, en[lj].strip()
    if rung == "d4_unrelated":
        # different sentence from the c4 corpus (different source/topic)
        cj = int(rng.integers(0, len(c4)))
        B = c4[cj].strip()
        while len(B) < 8:
            cj = int(rng.integers(0, len(c4))); B = c4[cj].strip()
        return A, B
    if rung == "d5_random":
        nbytes = max(8, len(A.encode("utf-8")))
        B = bytes(int(rng.integers(0, 256)) for _ in range(nbytes)).decode("utf-8", errors="ignore")
        if len(B) < 4:
            B = "".join(chr(33 + int(rng.integers(0, 90))) for _ in range(nbytes))
        return A, B
    raise ValueError(rung)

def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = np.sqrt((x.std() ** 2 + y.std() ** 2) / 2.0)
    return float((x.mean() - y.mean()) / (sp + 1e-12))

# ───────────────────────────────── main ───────────────────────────────────
def evaluate(measure_fn, flores, c4):
    """Return dict rung -> list of S over seeds, using a per-(rung,seed) pre-seeded
    rng so the SAME line/lang draws are reused identically across both measures."""
    S = {r: [] for r in LADDER}
    for r in LADDER:
        for s in SEEDS:
            rng = np.random.default_rng(abs(hash((r, s))) % (2**32))
            A, B = build_pair(r, flores, c4, rng)
            S[r].append(measure_fn(A, B, s))
    return S

def judge(S):
    means = {r: float(np.mean(S[r])) for r in LADDER}
    peak = max(means, key=means.get)
    pidx = LADDER.index(peak)
    interior = 0 < pidx < len(LADDER) - 1
    d0 = cohen_d(S[peak], S["d0_identical"])
    d5 = cohen_d(S[peak], S["d5_random"])
    f_interior = interior
    f_d0 = d0 >= D_MIN
    f_d5 = d5 >= D_MIN
    supported = bool(f_interior and f_d0 and f_d5)
    return {"means": means, "peak": peak, "interior": bool(interior),
            "d_vs_d0": d0, "d_vs_d5": d5,
            "f_interior": bool(f_interior), "f_d0": bool(f_d0), "f_d5": bool(f_d5),
            "supported": supported}

def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("=" * 90)
    print("H_1168 — OPTIMAL-OFFSET on a DATA-DISTANCE axis? (super-additive surplus")
    print("  S=phi_joint-Sum phi_parts; '어긋나 어울림' = offset-but-harmonious). REAL parallel data.")
    print(f"  ladder: {LADDER}")
    print(f"  seeds={N_SEEDS} T_STEPS={T_STEPS} CH={CH}  D_MIN={D_MIN}")
    print("  GREEN iff INTERIOR argmax (not d0/d5) AND d(peak,d0)>=0.8 AND d(peak,d5)>=0.8")
    print("     on BOTH (a) faithful-phi surplus AND (b) recombination surplus.")
    print("=" * 90)

    # STEP 0 — mirror ≡ stdlib re-proof BEFORE scoring (a_phi_iit4_tool)
    print("\nSTEP 0 — RE-PROVE faithful_phi mirror == stdlib BEFORE scoring (a_phi_iit4_tool):")
    try:
        live_ok = h1119.live_stdlib_faithful_reproof()
    except Exception as e:
        print(f"  live stdlib reproof errored: {e}"); live_ok = False
    proven = {}
    for n in (4, 5):
        try:
            proven[n] = bool(h1119.prove_mirrors_at_n(n))
        except Exception as e:
            print(f"  prove_mirrors_at_n({n}) errored: {e}"); proven[n] = False
    print(f"  live-stdlib proof: {'PROVEN' if live_ok else 'FAILED'}; mirror n4/n5: {proven}")
    if not (live_ok and all(proven.values())):
        print("\nABORT — faithful_phi mirror == stdlib proof FAILED. NOT scoring (a_phi_iit4_tool).")
        sys.exit(1)
    print("  STEP 0 PASS — faithful_phi mirror PROVEN == stdlib.\n")

    flores = load_flores()
    c4 = load_c4()
    print("[data] flores blocks: " + ", ".join(f"{lg}={len(flores[lg])}" for lg in LANGS)
          + f"  | c4 lines={len(c4)}")

    # measure (a) — faithful-φ integration surplus
    print("\n── MEASURE (a): FAITHFUL-phi integration surplus  S_a = phi_joint - [phi(A)+phi(B)] ──")
    Sa = evaluate(lambda A, B, s: surplus_phi(A, B, s), flores, c4)
    for r in LADDER:
        arr = np.array(Sa[r])
        print(f"  {r:18s}: S_a = {arr.mean():+.6f} ± {arr.std():.6f}", flush=True)
    Ja = judge(Sa)

    # measure (b) — recombination surplus
    print("\n── MEASURE (b): RECOMBINATION surplus  S_b = distinct(A⊕B) - [distinct(A)+distinct(B)] ──")
    Sb = evaluate(lambda A, B, s: surplus_recomb(A, B), flores, c4)
    for r in LADDER:
        arr = np.array(Sb[r])
        print(f"  {r:18s}: S_b = {arr.mean():+.4f} ± {arr.std():.4f}", flush=True)
    Jb = judge(Sb)

    both_supported = Ja["supported"] and Jb["supported"]
    any_supported = Ja["supported"] or Jb["supported"]
    d2_wins_a = Ja["peak"] == "d2_xling_parallel"
    d2_wins_b = Jb["peak"] == "d2_xling_parallel"

    if both_supported:
        ruling = ("SUPPORTED GREEN OPTIMAL-OFFSET: super-additive surplus has an INTERIOR "
                  "data-distance sweet spot on BOTH measures — "
                  f"(a)phi peak={Ja['peak']}, (b)recomb peak={Jb['peak']}. "
                  "'어긋나 어울림' confirmed: identical=redundant, random=no-integration, "
                  "intermediate offset maximizes whole-minus-sum.")
    elif any_supported:
        which = "(a) faithful-phi" if Ja["supported"] else "(b) recombination"
        ruling = (f"PARTIAL (honest): OPTIMAL-OFFSET holds on {which} ONLY "
                  f"(a-peak={Ja['peak']} sup={Ja['supported']}; b-peak={Jb['peak']} "
                  f"sup={Jb['supported']}) — measure-specific, NOT both (a_paper_negative_ok).")
    else:
        ruling = ("CLOSED-NEGATIVE RED: NO data-distance sweet spot — surplus is "
                  f"monotone/endpoint/flat on BOTH measures (a-peak={Ja['peak']} "
                  f"interior={Ja['interior']} d0={Ja['f_d0']} d5={Ja['f_d5']}; "
                  f"b-peak={Jb['peak']} interior={Jb['interior']} d0={Jb['f_d0']} "
                  f"d5={Jb['f_d5']}). Super-additivity has no data-distance optimum "
                  "at this scale (a_paper_negative_ok).")

    verdict = {
        "H": "H_1168",
        "title": "optimal-offset on a data-distance axis for super-additive surplus (어긋나 어울림)",
        "ladder": LADDER,
        "predicted_peak": "d2_xling_parallel",
        "measure_a_faithful_phi": {
            "S_mean": Ja["means"], "peak": Ja["peak"], "interior_argmax": Ja["interior"],
            "d_vs_d0": Ja["d_vs_d0"], "d_vs_d5": Ja["d_vs_d5"],
            "F_interior": Ja["f_interior"], "F_d0_ge_0.8": Ja["f_d0"], "F_d5_ge_0.8": Ja["f_d5"],
            "supported": Ja["supported"], "d2_xling_wins": bool(d2_wins_a)},
        "measure_b_recombination": {
            "S_mean": Jb["means"], "peak": Jb["peak"], "interior_argmax": Jb["interior"],
            "d_vs_d0": Jb["d_vs_d0"], "d_vs_d5": Jb["d_vs_d5"],
            "F_interior": Jb["f_interior"], "F_d0_ge_0.8": Jb["f_d0"], "F_d5_ge_0.8": Jb["f_d5"],
            "supported": Jb["supported"], "d2_xling_wins": bool(d2_wins_b)},
        "both_measures_supported": bool(both_supported),
        "any_measure_supported": bool(any_supported),
        "winning_distance_a": Ja["peak"], "winning_distance_b": Jb["peak"],
        "d2_cross_lingual_predicted_and_won": bool(d2_wins_a and d2_wins_b),
        "ruling": ruling,
        "scope": ("REAL-data sample (flores 5-lang parallel + c4); measure (a) IS "
                  "faithful IIT-4.0 phi (PROVEN mirror == stdlib, n=6 exact MIP-EI) on a "
                  "DETERMINISTIC byte-bigram channel rendering (rendering=representation "
                  "choice, labelled — NOT a proxy-Phi); measure (b) is deterministic "
                  "content-ngram recombination (p7, NOT perplexity). toy faithful-phi n=6 "
                  "+ real-data sample, a_scale_honest_scope."),
        "reuse": "H_1119 faithful_phi mirror (a) · H_1116 content-ngram metric (b)",
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    outdir = os.path.join(REPO, ".verdicts", "1168_superadditive_data_distance")
    os.makedirs(outdir, exist_ok=True)
    json.dump(verdict, open(os.path.join(outdir, "verdict.json"), "w"),
              ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
