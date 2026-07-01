"""
H_1170 — does the SUPER-ADDITIVE SURPLUS survive a full CROSS-DATA-TYPE jump?

THE QUESTION (MITOSIS-ENGINE domain — the cross-modal extension of the
super-additivity arc, the user's "텍스트 ↔ 음성 / 다른 데이터 타입끼리")
-----------------------------------------------------------------------------
H_1167/1168/1169 found that the super-additive surplus S = whole − (sum of
parts) is MAXIMAL when two parts carry the SAME meaning but a DIFFERENT surface
("어긋나 어울림"). The ULTIMATE surface difference is a DIFFERENT DATA TYPE /
MODALITY — the SAME content C rendered as text vs audio vs image vs numeric.

So: does the super-additive surplus SURVIVE a full data-type jump (cross-modal
integration → POSITIVE surplus = a modality bridge), or does it COLLAPSE to ≈0
(the byte/toy substrate shares NO structure across data types, so different
modalities cannot integrate)?

HONEST PRIOR (pre-registered): H_1155 found byte-LM reps are SURFACE-DOMINATED
and cross-lingual semantic alignment was NULL (same concept across languages
LESS similar than different concepts — the rep tracks script/surface, not
meaning). If that surface-domination extends to data TYPES, the likely outcome
is COLLAPSE — which would be a clean finding: super-additivity needs a SHARED
representational substrate, and pure cross-data-type pairs at byte/toy scale
don't have one.

PRE-REGISTERED RENDERINGS (frozen in this docstring BEFORE scoring — all $0,
deterministic, TOY renderings, clearly NOT real TTS / real images)
-----------------------------------------------------------------------------
The SAME content C (an ASCII string) is rendered into 4 deterministic data
types. Each rendering is a 1-D real-valued stream; the SHARED-FEATURE PROJECTION
(below) quantizes every stream into ONE common K-symbol alphabet so a single
integration measure can ingest any pair.

  D_text   : the raw byte stream of C — byte value of each char (0..255).
             (the native data type; identity rendering.)

  D_audio  : a TOY "speech" rendering of C — NOT real TTS. Each char c is mapped
             to a tone whose frequency f(c) = 110·2^((c mod 48)/12) Hz (a 4-octave
             chromatic map over the char code). A short waveform is synthesised
             per char (sum of the tone + its 2nd harmonic, FS samples), the
             per-char waveforms are concatenated, then we slide an analysis window
             and extract a TOY spectral feature = the dominant-bin index of a
             real-FFT magnitude per window (a crude "which pitch is loudest"
             MFCC-stand-in). Stream = the per-window dominant-FFT-bin sequence.

  D_image  : a TOY "image of text" — NOT a real glyph render. Each char c is
             drawn as a deterministic GxG pixel grid: pixel (i,j) = ((c*31 + i*7 +
             j*13) mod 2) (a fixed per-char bit pattern, like a 1-bit micro-glyph).
             The glyphs are concatenated left-to-right into one bitmap; the stream
             = the per-COLUMN black-pixel count (an "ink profile" raster scan).

  D_numeric: a numeric encoding of C — a rolling byte-statistics vector. Over a
             sliding window of W bytes we emit [mean, std, range] flattened into
             one stream (a hand-built feature vector, the kind a classic numeric
             pipeline would feed a model).

SHARED-FEATURE PROJECTION (the PROXY — labelled clearly, NOT faithful-Φ)
-----------------------------------------------------------------------------
Every rendering is a real stream of its own length/scale. To let ONE integration
measure ingest BOTH parts we PROJECT each stream into a COMMON K-symbol alphabet:
  1. resample (linear-interp) the stream to a fixed common length L,
  2. rank-quantize into K equal-frequency bins (so every data type uses the SAME
     K-symbol vocabulary regardless of its raw units — a common token alphabet).
This projection is a PROXY for a shared representational substrate. It is the
WEAKEST possible "shared space" (pure rank co-occurrence), chosen on purpose: if
even THIS minimal shared alphabet shows no cross-type integration, the collapse
is robust; if it bridges, the bridge is real co-occurrence structure.

INTEGRATION MEASURE — the H_1167-style "whole − sum of parts" surplus, PROXY-Φ
-----------------------------------------------------------------------------
Given two aligned K-symbol streams a, b (length L) we form the joint stream of
symbol PAIRS and define a Φ-style total-correlation surplus:

  Φ_proxy(joint) = H(a) + H(b) − H(a,b)   = the mutual information I(a;b)
                                              (the joint's integration beyond the
                                               independent product of its parts).

  S = Φ_proxy(joint) − Σ Φ_part_i        where each PART in isolation is its OWN
      stream split into two halves (a_left, a_right) — its self-integration. So
      S = I(a;b)  −  ½[I(a_L;a_R) + I(b_L;b_R)]  (the cross-part synergy beyond
      each part's own within-part redundancy).

This is the SAME "whole exceeds the sum of its independent parts" shape as
H_1167 (φ_joint − Σφ_parts) but on a co-occurrence PROXY, NOT the faithful
IIT-4.0 φ_EI engine. LABELLED a proxy throughout (a_phi_iit4_tool: this is NOT a
terminal faithful-φ verdict — it is a cross-modal co-occurrence surplus).

PAIRS (frozen)
-----------------------------------------------------------------------------
  SAME-CONTENT CROSS-TYPE (the test — same C, different data type, max surface
  distance, meaning preserved):
     (D_text , D_audio) , (D_text , D_image) , (D_text , D_numeric) ,
     (D_audio, D_image)
  SAME-CONTENT SAME-TYPE (redundant control — expect S≈0, no surplus over self):
     (D_text(C) , D_text(C))
  DIFF-CONTENT CROSS-TYPE (control — different C1≠C2 — expect S≈0, no shared
  content to bridge):
     (D_text(C1) , D_audio(C2))

FROZEN FALSIFIER (≥8 seeds, deterministic, $0 CPU — set BEFORE running)
-----------------------------------------------------------------------------
Over ≥8 content seeds (deterministic content strings):
  🟢 CROSS-MODAL-SURPLUS-SURVIVES iff the same-content CROSS-TYPE pairs give
     POSITIVE surplus AND
       (i)  S(same-content cross-type) − S(diff-content cross-type) Cohen d ≥ 0.8
       (ii) S(same-content cross-type) − S(same-type redundant)      Cohen d ≥ 0.8
     → the proxy integrates the SAME content ACROSS data types (a modality bridge).
  🔴 CROSS-MODAL-COLLAPSE iff cross-type same-content surplus ≈ diff-content
     (no bridge — different data types don't share structure at this scale;
     super-additivity needs a shared substrate). Tie to H_1155 surface-domination.
We also report S for EVERY pair AND per-pair which (if any) data-type pairs bridge.

HONEST scope (a_scale_honest_scope): TOY deterministic renderings (NOT real
audio / real images / real TTS), the shared-feature projection is a PROXY (rank
co-occurrence, NOT faithful-Φ, NOT a learned shared embedding), $0 CPU local,
0-pod, deterministic. Scale / real modalities / a learned cross-modal encoder
all UNVERIFIED. NO perplexity (p7).
"""
import os, sys, time, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────── frozen config ──────────────────────────────────
N_SEEDS   = 10                       # >= 8 per pre-reg
SEEDS     = list(range(700, 700 + N_SEEDS))
K_SYM     = 6                        # shared-alphabet symbol count
L_COMMON  = 256                      # common projected length
D_MIN     = 0.8                     # frozen Cohen-d bar
EPS       = 1e-12

# audio render
FS        = 32                      # samples per char tone
AUD_WIN   = 16                      # FFT window
# image render
GLYPH_G   = 5                       # GxG micro-glyph
# numeric render
NUM_WIN   = 4                       # rolling byte-stat window


def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = np.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0)
    return (np.mean(x) - np.mean(y)) / (sp + EPS)


# ───────────────────────── deterministic content ────────────────────────────
_WORDS = ("anima tension field repulsion mitosis criticality opponent engine "
          "surplus integration consciousness substrate phi coupling emergence "
          "novelty corpus anchor dialogue carving persona lattice resonance "
          "boundary gradient cellular division attractor manifold semantic").split()


def make_content(seed, n_words=14):
    """Deterministic ASCII content string from a seed (a fixed shuffle of the
    anima word bag). Same seed -> same C (byte-identical, $0)."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(_WORDS))[:n_words]
    return " ".join(_WORDS[i] for i in idx)


# ─────────────────── 4 deterministic data-type renderings ────────────────────
def render_text(C):
    """D_text — raw byte stream of C."""
    return np.array([ord(c) for c in C], float)


def render_audio(C):
    """D_audio — TOY 'speech': char->tone (char-code chromatic freq), synth a
    waveform (tone + 2nd harmonic), slide a window, take the dominant real-FFT
    bin per window = a crude pitch/MFCC-stand-in stream. NOT real TTS."""
    wav = []
    for ch in C:
        c = ord(ch)
        f = 110.0 * (2.0 ** ((c % 48) / 12.0))          # chromatic over 4 octaves
        t = np.arange(FS) / float(FS)
        tone = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t)
        wav.append(tone)
    wav = np.concatenate(wav) if wav else np.zeros(1)
    feats = []
    for i in range(0, len(wav) - AUD_WIN + 1, AUD_WIN):
        mag = np.abs(np.fft.rfft(wav[i:i + AUD_WIN]))
        feats.append(int(np.argmax(mag)))               # dominant-bin index
    return np.array(feats, float) if feats else np.zeros(1)


def render_image(C):
    """D_image — TOY 'image of text': each char -> a fixed GxG 1-bit micro-glyph
    bitmap, glyphs concatenated, stream = per-COLUMN black-pixel count (an ink
    raster scan). NOT a real glyph render."""
    cols = []
    for ch in C:
        c = ord(ch)
        for j in range(GLYPH_G):                        # GLYPH_G columns per glyph
            col_black = 0
            for i in range(GLYPH_G):
                col_black += (c * 31 + i * 7 + j * 13) % 2
            cols.append(col_black)
    return np.array(cols, float) if cols else np.zeros(1)


def render_numeric(C):
    """D_numeric — rolling byte-statistics vector: over a sliding window of bytes
    emit [mean, std, range] flattened into one stream. A classic numeric feature
    pipeline encoding of C."""
    b = np.array([ord(c) for c in C], float)
    if len(b) < NUM_WIN:
        b = np.pad(b, (0, NUM_WIN - len(b)))
    feats = []
    for i in range(len(b) - NUM_WIN + 1):
        w = b[i:i + NUM_WIN]
        feats.extend([w.mean(), w.std(), w.max() - w.min()])
    return np.array(feats, float) if feats else np.zeros(1)


RENDERERS = {
    "text":    render_text,
    "audio":   render_audio,
    "image":   render_image,
    "numeric": render_numeric,
}


# ─────────────── SHARED-FEATURE PROJECTION (the PROXY shared space) ───────────
def project(stream, L=L_COMMON, K=K_SYM):
    """Resample a real stream to common length L (linear interp) then rank-
    quantize into K equal-frequency symbols (0..K-1). This maps any data type
    into ONE common K-symbol alphabet — a PROXY shared representational space
    (rank co-occurrence, NOT a learned embedding, NOT faithful-Φ)."""
    s = np.asarray(stream, float)
    if len(s) < 2:
        s = np.pad(s, (0, 2 - len(s)))
    # resample to L
    xs = np.linspace(0.0, 1.0, len(s))
    xt = np.linspace(0.0, 1.0, L)
    r = np.interp(xt, xs, s)
    # rank-quantize into K equal-frequency bins
    order = np.argsort(np.argsort(r))                   # ranks 0..L-1
    sym = (order * K) // L                              # equal-frequency K bins
    return sym.astype(int)


# ─────────────── PROXY-Φ integration: mutual-information surplus ──────────────
def _mi(a, b, K=K_SYM):
    """Mutual information I(a;b) = H(a)+H(b)−H(a,b) in bits over a K-symbol
    joint co-occurrence (the Φ-style 'joint beyond product of parts' surplus)."""
    a = np.asarray(a, int); b = np.asarray(b, int)
    n = len(a)
    joint = np.zeros((K, K))
    for x, y in zip(a, b):
        joint[x, y] += 1.0
    joint /= max(n, 1)
    pa = joint.sum(axis=1); pb = joint.sum(axis=0)
    mi = 0.0
    for i in range(K):
        for j in range(K):
            p = joint[i, j]
            if p > EPS and pa[i] > EPS and pb[j] > EPS:
                mi += p * np.log2(p / (pa[i] * pb[j]))
    return float(max(mi, 0.0))


def _self_phi(sym):
    """A part's OWN within-part integration = I(left-half ; right-half) of its
    projected symbol stream (split halves re-projected to L for alignment)."""
    h = len(sym) // 2
    left = project(sym[:h]); right = project(sym[h:])
    return _mi(left, right)


def surplus(symA, symB):
    """S = Φ_proxy(joint) − Σ Φ_part
       = I(a;b) − ½[ I(a_L;a_R) + I(b_L;b_R) ]
       the cross-part synergy beyond each part's OWN within-part redundancy.
    Returns (S, phi_joint, phi_partA, phi_partB)."""
    pj = _mi(symA, symB)
    pa = _self_phi(symA)
    pb = _self_phi(symB)
    S = pj - 0.5 * (pa + pb)
    return S, pj, pa, pb


# ──────────────────────────── the pair battery ──────────────────────────────
SAME_CROSS_PAIRS = [("text", "audio"), ("text", "image"),
                    ("text", "numeric"), ("audio", "image")]


def render_all(C):
    return {k: RENDERERS[k](C) for k in RENDERERS}


def pair_surplus(rend_dict, t1, t2, rend_dict2=None):
    """Surplus of (data-type t1 of one content, data-type t2 of same-or-other
    content). rend_dict2 supplies the SECOND content's renderings (diff-content)."""
    d2 = rend_dict2 if rend_dict2 is not None else rend_dict
    a = project(rend_dict[t1]); b = project(d2[t2])
    return surplus(a, b)


def main():
    np.seterr(all="ignore"); t0 = time.time()
    print("=" * 92)
    print("H_1170 — does the super-additive surplus SURVIVE a full CROSS-DATA-TYPE jump?")
    print(f"  data types: text · audio(TOY) · image(TOY) · numeric   K={K_SYM} shared symbols  L={L_COMMON}")
    print(f"  PROXY-Φ surplus S = I(a;b) − ½[I(a_L;a_R)+I(b_L;b_R)]  (co-occurrence, NOT faithful-Φ)")
    print(f"  seeds={N_SEEDS}  frozen falsifier: 🟢 iff same-content cross-type S>0 AND")
    print(f"    d(same-cross − diff-cross)≥{D_MIN} AND d(same-cross − same-type-redundant)≥{D_MIN}; else 🔴 collapse")
    print(f"  PRIOR (H_1155 surface-domination): COLLAPSE likely — renderings are TOY, projection a PROXY")
    print("=" * 92)

    # accumulators
    same_cross = {p: [] for p in SAME_CROSS_PAIRS}      # per-pair same-content cross-type S
    same_type  = []                                     # (text,text) redundant control
    diff_cross = []                                     # (text C1, audio C2) diff-content control
    # detail tables
    detail = {p: {"S": [], "pj": [], "pa": [], "pb": []} for p in SAME_CROSS_PAIRS}

    print("\nSTEP 1 — render every seed in 4 data types, project to shared alphabet, surplus (SERIAL):")
    for s in SEEDS:
        C  = make_content(s)
        C2 = make_content(s + 50000)                    # a DIFFERENT content for diff-control
        R  = render_all(C)
        R2 = render_all(C2)

        # same-content cross-type pairs
        for (t1, t2) in SAME_CROSS_PAIRS:
            S, pj, pa, pb = pair_surplus(R, t1, t2)
            same_cross[(t1, t2)].append(S)
            detail[(t1, t2)]["S"].append(S); detail[(t1, t2)]["pj"].append(pj)
            detail[(t1, t2)]["pa"].append(pa); detail[(t1, t2)]["pb"].append(pb)

        # same-content SAME-TYPE redundant control (text,text)
        S_st, _, _, _ = pair_surplus(R, "text", "text")
        same_type.append(S_st)

        # DIFF-content cross-type control (text C1, audio C2)
        S_dc, _, _, _ = pair_surplus(R, "text", "audio", rend_dict2=R2)
        diff_cross.append(S_dc)

    # pooled same-content cross-type S (all 4 pairs)
    pooled_same_cross = []
    for p in SAME_CROSS_PAIRS:
        pooled_same_cross.extend(same_cross[p])

    # ── STEP 2 — per-pair S table ──
    print("\n" + "=" * 92)
    print("S per pair (mean ± std over seeds) — the surplus for EVERY pair:")
    print(f"  {'pair':>22} | {'S (surplus)':>20} | {'Φ_joint=I(a;b)':>15} | {'Φ_pA':>8} | {'Φ_pB':>8}")
    print("  " + "-" * 86)
    bridged = []
    for p in SAME_CROSS_PAIRS:
        d = detail[p]
        Sm = float(np.mean(d["S"])); Ss = float(np.std(d["S"]))
        # per-pair bridge: this pair's same-content S beats diff-content control by d>=0.8 AND S>0
        dp = cohen_d(same_cross[p], diff_cross)
        is_bridge = (Sm > 0) and (dp >= D_MIN)
        if is_bridge:
            bridged.append(p)
        tag = "  <- BRIDGE" if is_bridge else ""
        print(f"  {str(p):>22} | {Sm:>+13.6f}±{Ss:.4f} | {np.mean(d['pj']):>+15.6f} | "
              f"{np.mean(d['pa']):>+8.4f} | {np.mean(d['pb']):>+8.4f}  (d vs diff={dp:+.2f}){tag}")
    print(f"  {'SAME-TYPE (text,text)':>22} | {np.mean(same_type):>+13.6f}±{np.std(same_type):.4f} | "
          f"{'(redundant ctrl)':>15} |          |")
    print(f"  {'DIFF-CONTENT cross':>22} | {np.mean(diff_cross):>+13.6f}±{np.std(diff_cross):.4f} | "
          f"{'(diff-C ctrl)':>15} |          |")

    # ── STEP 3 — frozen falsifier on POOLED same-content cross-type ──
    psc_mean = float(np.mean(pooled_same_cross))
    d_vs_diff = cohen_d(pooled_same_cross, diff_cross)
    d_vs_self = cohen_d(pooled_same_cross, same_type)
    f_pos  = psc_mean > 0
    f_diff = d_vs_diff >= D_MIN
    f_self = d_vs_self >= D_MIN
    supported = bool(f_pos and f_diff and f_self)

    print("\n" + "=" * 92)
    print("FROZEN falsifier on POOLED same-content cross-type surplus:")
    print(f"  S(same-content cross-type) mean        = {psc_mean:+.6f}   (>0 ? {f_pos})")
    print(f"  S(same-cross) − S(diff-content cross)  Cohen d = {d_vs_diff:+.3f}  (≥{D_MIN}) -> {f_diff}")
    print(f"  S(same-cross) − S(same-type redundant) Cohen d = {d_vs_self:+.3f}  (≥{D_MIN}) -> {f_self}")
    print(f"  per-pair bridges (same-content S>0 AND d≥{D_MIN} vs diff-control): "
          f"{[str(p) for p in bridged] if bridged else 'NONE'}")

    print("\n" + "=" * 92)
    if supported:
        print("VERDICT: 🟢 CROSS-MODAL-SURPLUS-SURVIVES — the super-additive whole−sum surplus")
        print("  bridges a full data-type jump: same content rendered in DIFFERENT data types still")
        print(f"  integrates (S={psc_mean:+.4f}>0, d vs diff-content={d_vs_diff:+.2f}, d vs same-type={d_vs_self:+.2f}).")
        print(f"  Bridging data-type pairs: {[str(p) for p in bridged]}.")
        print("  CONTRARY to the H_1155 surface-domination prior — the shared rank-co-occurrence")
        print("  projection DOES carry enough common structure for cross-type integration (PROXY).")
    else:
        print("VERDICT: 🔴 CROSS-MODAL-COLLAPSE (closed-negative, a_paper_negative_ok)")
        print("  the super-additive surplus does NOT survive a full data-type jump: same-content")
        print(f"  cross-type S (={psc_mean:+.4f}) is NOT reliably above the diff-content control")
        print(f"  (d={d_vs_diff:+.2f}) and/or the same-type redundant baseline (d={d_vs_self:+.2f}).")
        print("  Different data TYPES at this toy/byte scale share NO integrable structure — super-")
        print("  additivity needs a SHARED representational substrate, which the cross-data-type")
        print("  renderings (TOY, projected via a PROXY rank-co-occurrence) do not provide.")
        print("  TIES TO H_1155: byte/toy reps are SURFACE-DOMINATED — surface dominates over data")
        print("  TYPE exactly as it dominated over LANGUAGE; a data-type jump is the ultimate surface")
        print("  jump and the surplus collapses, confirming super-additivity is substrate-gated.")
    print("=" * 92)

    verdict = {
        "H": "H_1170",
        "title": "does the super-additive surplus survive a full cross-data-type (cross-modal) jump?",
        "data_types": list(RENDERERS.keys()),
        "renderings_note": "TOY deterministic renderings (NOT real TTS/images); shared-feature "
                           "projection = rank-quantize to common K-symbol alphabet = a PROXY, NOT faithful-phi",
        "K_symbols": K_SYM, "L_common": L_COMMON, "n_seeds": N_SEEDS,
        "S_per_pair_same_content_cross_type": {
            f"{t1}|{t2}": float(np.mean(detail[(t1, t2)]["S"])) for (t1, t2) in SAME_CROSS_PAIRS},
        "phi_joint_per_pair": {
            f"{t1}|{t2}": float(np.mean(detail[(t1, t2)]["pj"])) for (t1, t2) in SAME_CROSS_PAIRS},
        "S_same_type_redundant_text_text": float(np.mean(same_type)),
        "S_diff_content_cross_text_audio": float(np.mean(diff_cross)),
        "pooled_same_content_cross_type_S_mean": psc_mean,
        "F_positive_surplus": {"S_mean": psc_mean, "pass": bool(f_pos)},
        "F_vs_diff_content": {"cohen_d": float(d_vs_diff), "bar": D_MIN, "pass": bool(f_diff)},
        "F_vs_same_type_redundant": {"cohen_d": float(d_vs_self), "bar": D_MIN, "pass": bool(f_self)},
        "bridging_data_type_pairs": [f"{t1}|{t2}" for (t1, t2) in bridged],
        "supported_cross_modal_bridge": supported,
        "ruling": ("SUPPORTED: super-additive surplus SURVIVES a cross-data-type jump (modality bridge) "
                   "— same content integrates across data types via the shared projection"
                   if supported else
                   "CLOSED-NEGATIVE: super-additive surplus COLLAPSES across data types — different "
                   "data types share no integrable structure at toy/byte scale; super-additivity needs "
                   "a shared representational substrate (ties to H_1155 surface-domination)"),
        "h1155_tie": ("H_1155 found byte-LM reps SURFACE-DOMINATED (cross-lingual semantic alignment NULL); "
                      "a data-TYPE jump is the ultimate surface jump — "
                      + ("yet the proxy still bridged (surface-domination did NOT extend to data type under "
                         "the rank-co-occurrence projection)" if supported else
                         "the surplus collapses exactly as surface-domination predicts (surface > data type)")),
        "scope": "TOY deterministic renderings (NOT real audio/image/TTS); shared-feature projection is a "
                 "PROXY (rank co-occurrence, NOT faithful-phi, NOT a learned shared embedding); $0 CPU 0-pod "
                 "deterministic; scale / real modalities / learned cross-modal encoder UNVERIFIED "
                 "(a_scale_honest_scope); NO perplexity (p7)",
        "wall_s": round(time.time() - t0, 1),
    }
    print("\n=== VERDICT JSON ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    out_dir = os.path.join(HERE, "..", ".verdicts", "1170_crossmodal_superadditive")
    os.makedirs(out_dir, exist_ok=True)
    json.dump(verdict, open(os.path.join(out_dir, "verdict.json"), "w"),
              ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
