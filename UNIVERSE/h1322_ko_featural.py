#!/usr/bin/env python3
# h1322_ko_featural.py — does decomposing ONE LEVEL DEEPER than jamo — to the FEATURAL VECTOR that
# Hangul's DESIGN encodes — drop held-out KO next-symbol CE BELOW the jamo floor (H_1316 = 2.51335)?
#
# THE PRIOR RESULT (H_1316 🟢): NFD jamo composition (초성 L / 중성 V / 종성 T) dropped held-out KO
# next-symbol CE from the raw-byte ceiling 2.95342 to 2.51335 nats/UTF-8-byte; shuffle-jamo control
# rose to 2.74306 → the lift is COMPOSITIONAL structure. But jamo is only the FIRST decomposition.
#
# THE NEW ANGLE: Hangul is — uniquely among major scripts — a DELIBERATELY DESIGNED *featural*
# writing system (Sejong 1443). Each jamo's SHAPE encodes articulatory/phonological FEATURES:
# consonants = articulator base (velar/alveolar/bilabial/sibilant/glottal) + added strokes
# (aspiration) + doubling (tense); vowels = ·/ㅡ/ㅣ combos with yang/yin polarity + iotation.
# So ㄱ and ㅋ are ONE FEATURE apart, not two opaque symbols. NO organically-evolved script has this.
#
# THIS LANE: keep the LABEL alphabet + byte-accounting IDENTICAL to H_1316 (Vj = 256 + distinct
# jamo). The ONLY change = the mitosis PARTITION geometry X: instead of opaque symbol-id columns
# (H_1316: [last_sym/Vj, second_sym/Vj, cont_depth/3]), X is built from the previous symbols'
# DESIGN FEATURE COLUMNS, so two jamo one feature apart land NEAR each other in partition space and
# the gradient-free mitosis can exploit the designed systematicity. CE is convertible to the SAME
# nats/UTF-8-byte axis → directly comparable to jamo 2.51335 and raw 2.95342.
#
# FROZEN-FIRST bars (.verdicts/1322_ko_featural/H_1322_FREEZE.txt; NOT moved — c9/p7):
#   F1 DEEPER  featural CE < jamo 2.51335 by >=0.03 (mean 3 seeds)  AND  < raw 2.95342.
#   F2 EARNED  featural beats SHUFFLE-feature-map by >=0.05 (decisive: the lift is the DESIGN,
#              not extra dims/vocab). If F2 fails → gain is dims-not-design (honest negative, c9).
#   F3 LINEARITY (non-gating)  linear-predictability in feature space better than in jamo-symbol
#              space by >=0.02 nats/byte (the design's mathematical signature).
#   GREEN iff F1 ∧ F2. If F1 fails → jamo is the decomposition FLOOR (honest 🧱).
#
# REAL Korean only (NO synthetic, p1-p8): SAME anima-7b R2 web corpus as H_1307 RUN A / H_1316
# (r2://phanes/anima-7b/web/{kor,eng}/shard0000.bytes); KO/EN window sha256 ASSERTED == the H_1307
# RUN A manifest hashes so the corpus is provably identical. R2 keys env-only at fetch time (c7).
# SCALE-HONEST: toy/DIRECTIONAL; engine-transfer to live hexa = follow-on; NO fluency claim.

import argparse
import hashlib
import json
import os
import sys
import time
import unicodedata

import numpy as np

try:
    import torch
except Exception as e:  # pragma: no cover
    print("FATAL: torch import failed:", e)
    sys.exit(2)

# ── FROZEN knobs (verbatim from H_1306 / H_1307 / H_1316) ──────────────────────
GROW_MAX = 40
SPLIT_THRESH_CE = 0.05
MIN_OWNED = 8
LAPLACE = 1.0
H1307_CEILING_KO_CE = 2.95342     # in-run G0 raw-byte ceiling (H_1316 reproduced)
H1316_JAMO_CE = 2.51335           # the jamo floor this lane must beat
F1_MARGIN = 0.03                  # F1: featural must beat the jamo floor by >= this
F2_MARGIN = 0.05                  # F2: featural must beat shuffle-feature-map by >= this
F3_MARGIN = 0.02                  # F3 (non-gating): linearity advantage margin
H1307_KO_SHA = "c47b6808308d2f73cb92d74f8fdb15c64e6c96e8ed58ae2ef91a7c57fe5dc6ca"
H1307_EN_SHA = "31b4a5430441cfdbb496b59f392150e4aa748cde2ed1b7cedad10960f0bcaf73"

R2_KO_KEY = "anima-7b/web/kor/shard0000.bytes"
R2_EN_KEY = "anima-7b/web/eng/shard0000.bytes"

HANGUL_LO, HANGUL_HI = 0xAC00, 0xD7A3   # precomposed Hangul syllable block


def log(*a):
    print(*a, flush=True)


# ── REAL corpus fetch from R2 (boto3 range GET; secrets env-only, never logged) ─
def fetch_r2_range(key, nbytes):
    import boto3
    from botocore.config import Config
    acct = os.environ["R2_ACCOUNT_ID"]
    bucket = os.environ["R2_BUCKET"]
    s3 = boto3.client(
        "s3",
        endpoint_url=f"https://{acct}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}),
    )
    obj = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes=0-{nbytes - 1}")
    return obj["Body"].read()


def trim_utf8(b):
    for cut in range(0, 4):
        try:
            b[: len(b) - cut].decode("utf-8")
            return b[: len(b) - cut]
        except Exception:
            continue
    return b


# ════════════════════════════════════════════════════════════════════════════════════════════
#  HANGUL FEATURAL DESIGN MAP  (documented Hunminjeongeum featural scheme — encoded, NOT invented)
#  NFD conjoining-jamo codepoints:
#    Initial (choseong) L : U+1100..U+1112   (consonants)
#    Medial   (jungseong) V: U+1161..U+1175   (vowels)
#    Final    (jongseong) T: U+11A8..U+11C2   (consonant clusters; reuse articulator families)
#  Each jamo → a 5-int feature vector [f_artic, f_manner, f_nasal_or_polar, f_liquid_or_iota, f_round]
#  Columns are SHARED slots (consonants populate the consonant meaning, vowels the vowel meaning).
# ════════════════════════════════════════════════════════════════════════════════════════════
# articulator classes: 0 none, 1 velar, 2 alveolar, 3 bilabial, 4 sibilant/dental, 5 glottal, 6 zero-ㅇ, 7 vowel
# manner: 0 plain, 1 aspirated, 2 tense
# -- INITIAL consonants U+1100.. --
#   ㄱ1100 ㄲ1101 ㄴ1102 ㄷ1103 ㄸ1104 ㄹ1105 ㅁ1106 ㅂ1107 ㅃ1108 ㅅ1109 ㅆ110A
#   ㅇ110B ㅈ110C ㅉ110D ㅊ110E ㅋ110F ㅌ1110 ㅍ1111 ㅎ1112
# Feature vector = [artic, manner, nasal, liquid, round]   (round unused for consonants → 0)
CONS_FEAT = {
    0x1100: [1, 0, 0, 0, 0],  # ㄱ velar plain
    0x1101: [1, 2, 0, 0, 0],  # ㄲ velar tense
    0x1102: [2, 0, 1, 0, 0],  # ㄴ alveolar nasal
    0x1103: [2, 0, 0, 0, 0],  # ㄷ alveolar plain
    0x1104: [2, 2, 0, 0, 0],  # ㄸ alveolar tense
    0x1105: [2, 0, 0, 1, 0],  # ㄹ alveolar liquid
    0x1106: [3, 0, 1, 0, 0],  # ㅁ bilabial nasal
    0x1107: [3, 0, 0, 0, 0],  # ㅂ bilabial plain
    0x1108: [3, 2, 0, 0, 0],  # ㅃ bilabial tense
    0x1109: [4, 0, 0, 0, 0],  # ㅅ sibilant plain
    0x110A: [4, 2, 0, 0, 0],  # ㅆ sibilant tense
    0x110B: [6, 0, 0, 0, 0],  # ㅇ zero/null onset
    0x110C: [4, 0, 0, 0, 0],  # ㅈ sibilant/affricate plain
    0x110D: [4, 2, 0, 0, 0],  # ㅉ sibilant tense
    0x110E: [4, 1, 0, 0, 0],  # ㅊ sibilant aspirated
    0x110F: [1, 1, 0, 0, 0],  # ㅋ velar aspirated
    0x1110: [2, 1, 0, 0, 0],  # ㅌ alveolar aspirated
    0x1111: [3, 1, 0, 0, 0],  # ㅍ bilabial aspirated
    0x1112: [5, 0, 0, 0, 0],  # ㅎ glottal
}
# -- FINAL consonant clusters U+11A8.. → fold to the articulator family of the base consonant --
#   We map each jongseong codepoint to its primary consonant feature. Clusters take the family of
#   their FIRST element (standard simplification; the design systematicity lives in the base shape).
FINAL_FEAT = {
    0x11A8: [1, 0, 0, 0, 0],  # ㄱ
    0x11A9: [1, 2, 0, 0, 0],  # ㄲ
    0x11AA: [1, 0, 0, 0, 0],  # ㄳ (ㄱ+ㅅ) → velar family
    0x11AB: [2, 0, 1, 0, 0],  # ㄴ
    0x11AC: [2, 0, 1, 0, 0],  # ㄵ (ㄴ+ㅈ)
    0x11AD: [2, 0, 1, 0, 0],  # ㄶ (ㄴ+ㅎ)
    0x11AE: [2, 0, 0, 0, 0],  # ㄷ
    0x11AF: [2, 0, 0, 1, 0],  # ㄹ liquid
    0x11B0: [2, 0, 0, 1, 0],  # ㄺ (ㄹ+ㄱ)
    0x11B1: [2, 0, 0, 1, 0],  # ㄻ (ㄹ+ㅁ)
    0x11B2: [2, 0, 0, 1, 0],  # ㄼ (ㄹ+ㅂ)
    0x11B3: [2, 0, 0, 1, 0],  # ㄽ (ㄹ+ㅅ)
    0x11B4: [2, 0, 0, 1, 0],  # ㄾ (ㄹ+ㅌ)
    0x11B5: [2, 0, 0, 1, 0],  # ㄿ (ㄹ+ㅍ)
    0x11B6: [2, 0, 0, 1, 0],  # ㅀ (ㄹ+ㅎ)
    0x11B7: [3, 0, 1, 0, 0],  # ㅁ
    0x11B8: [3, 0, 0, 0, 0],  # ㅂ
    0x11B9: [3, 0, 0, 0, 0],  # ㅄ (ㅂ+ㅅ)
    0x11BA: [4, 0, 0, 0, 0],  # ㅅ
    0x11BB: [4, 2, 0, 0, 0],  # ㅆ
    0x11BC: [1, 0, 1, 0, 0],  # ㅇ (ng — velar nasal)
    0x11BD: [4, 0, 0, 0, 0],  # ㅈ
    0x11BE: [4, 1, 0, 0, 0],  # ㅊ
    0x11BF: [1, 1, 0, 0, 0],  # ㅋ
    0x11C0: [2, 1, 0, 0, 0],  # ㅌ
    0x11C1: [3, 1, 0, 0, 0],  # ㅍ
    0x11C2: [5, 0, 0, 0, 0],  # ㅎ
}
# -- MEDIAL vowels U+1161.. → [artic=7(vowel), vbase, polar, iota, round] --
#   ㅏ1161 ㅐ1162 ㅑ1163 ㅒ1164 ㅓ1165 ㅔ1166 ㅕ1167 ㅖ1168 ㅗ1169 ㅘ116A ㅙ116B
#   ㅚ116C ㅛ116D ㅜ116E ㅝ116F ㅞ1170 ㅟ1171 ㅠ1172 ㅡ1173 ㅢ1174 ㅣ1175
#   vbase: 1 vertical-axis, 2 horizontal-axis, 3 combined
#   polar: 0 neutral, 1 yang/bright, 2 yin/dark
#   iota : 0 plain, 1 iotated (y-glide)
#   round: 0 simple, 1 compound (has a horizontal + vertical merge)
VOWEL_FEAT = {
    0x1161: [7, 1, 1, 0, 0],  # ㅏ vertical yang
    0x1162: [7, 1, 1, 0, 0],  # ㅐ (ㅏ+ㅣ)
    0x1163: [7, 1, 1, 1, 0],  # ㅑ iotated yang
    0x1164: [7, 1, 1, 1, 0],  # ㅒ
    0x1165: [7, 1, 2, 0, 0],  # ㅓ vertical yin
    0x1166: [7, 1, 2, 0, 0],  # ㅔ
    0x1167: [7, 1, 2, 1, 0],  # ㅕ iotated yin
    0x1168: [7, 1, 2, 1, 0],  # ㅖ
    0x1169: [7, 2, 1, 0, 0],  # ㅗ horizontal yang
    0x116A: [7, 3, 1, 0, 1],  # ㅘ compound (ㅗ+ㅏ)
    0x116B: [7, 3, 1, 0, 1],  # ㅙ
    0x116C: [7, 3, 1, 0, 1],  # ㅚ
    0x116D: [7, 2, 1, 1, 0],  # ㅛ horizontal iotated yang
    0x116E: [7, 2, 2, 0, 0],  # ㅜ horizontal yin
    0x116F: [7, 3, 2, 0, 1],  # ㅝ compound
    0x1170: [7, 3, 2, 0, 1],  # ㅞ
    0x1171: [7, 3, 2, 0, 1],  # ㅟ
    0x1172: [7, 2, 2, 1, 0],  # ㅠ horizontal iotated yin
    0x1173: [7, 2, 0, 0, 0],  # ㅡ horizontal neutral (earth)
    0x1174: [7, 3, 0, 0, 1],  # ㅢ compound (ㅡ+ㅣ)
    0x1175: [7, 1, 0, 0, 0],  # ㅣ vertical neutral (human)
}
N_FEAT_COLS = 5
# per-column number of distinct values for normalization (max+1)
FEAT_DIVISORS = [8.0, 3.0, 3.0, 2.0, 2.0]   # artic 0..7, manner/polar 0..2, nasal/iota 0..1, liquid/round? see below
# NOTE column meaning is shared: col0=artic(0..7), col1=manner|vbase, col2=nasal|polar, col3=liquid|iota, col4=round.
# vbase ranges 0..3 so col1 divisor must cover 3 → use 4. Fix divisors:
FEAT_DIVISORS = [8.0, 4.0, 3.0, 2.0, 2.0]


def jamo_feature_vec(cp):
    """Return the 5-int design feature vector for an NFD jamo codepoint, else None."""
    if cp in CONS_FEAT:
        return CONS_FEAT[cp]
    if cp in VOWEL_FEAT:
        return VOWEL_FEAT[cp]
    if cp in FINAL_FEAT:
        return FINAL_FEAT[cp]
    return None


# ── B-style NO-CHEAT: NFD→NFC round-trip + byte accounting (same as H_1316) ─────
def roundtrip_and_accounting(text):
    bad = 0
    n_syll = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            n_syll += 1
            nfd = unicodedata.normalize("NFD", ch)
            nfc = unicodedata.normalize("NFC", nfd)
            if nfc.encode("utf-8") != ch.encode("utf-8"):
                bad += 1
    return {"hangul_syllables": n_syll, "roundtrip_fail": bad, "ok": bad == 0}


# ── SYMBOL + FEATURE stream builders ────────────────────────────────────────────
def build_jamo_vocab(text):
    jset = set()
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            for jc in unicodedata.normalize("NFD", ch):
                jset.add(ord(jc))
    jamo_sorted = sorted(jset)
    jamo_to_id = {cp: 256 + i for i, cp in enumerate(jamo_sorted)}
    return jamo_to_id, jamo_sorted


def syll_jamo_nbytes(njamo):
    if njamo == 3:
        return [1, 1, 1]
    if njamo == 2:
        return [2, 1]
    if njamo == 1:
        return [3]
    out = [1] * njamo
    out[0] += (3 - njamo) if njamo < 3 else 0
    return out


def make_streams(text, jamo_to_id, jamo_feat_map):
    """Build aligned arrays in ONE pass:
       syms[int64]   = jamo-symbol id (256+rank) or raw byte id (0..255)  — the LABEL alphabet (== H_1316)
       feats[int8 N×5] = the design feature vector per symbol (raw bytes → byte-derived columns)
       nby[int64]    = UTF-8 bytes each symbol accounts for (lossless axis)
       depth[int64]  = continuation depth (jamo-inside-syllable / UTF-8 continuation-byte)
       jamo_feat_map: dict jamo-codepoint → 5-int feature vector (INTACT design map, or a SHUFFLED
                      bijection of it for the control)."""
    syms, feats, nby, depth = [], [], [], []
    d = 0
    for ch in text:
        cp = ord(ch)
        if HANGUL_LO <= cp <= HANGUL_HI:
            nfd = unicodedata.normalize("NFD", ch)
            nb = syll_jamo_nbytes(len(nfd))
            for j, jc in enumerate(nfd):
                jcp = ord(jc)
                syms.append(jamo_to_id[jcp])
                fv = jamo_feat_map.get(jcp)
                if fv is None:
                    fv = [0, 0, 0, 0, 0]
                feats.append(fv)
                nby.append(nb[j])
                d = 0 if j == 0 else d + 1
                depth.append(d)
        else:
            for b in ch.encode("utf-8"):
                syms.append(int(b))
                # raw byte → byte-derived feature columns (kept small & ASCII-identical across arms):
                # col0 = high nibble (0..15→scaled later), col1 = low nibble, rest 0. ASCII structure
                # preserved identically in every arm (intact/shuffle), so only Hangul rep varies.
                feats.append([b >> 4, b & 0xF, 0, 0, 0])
                nby.append(1)
                if 0x80 <= b <= 0xBF:
                    d = d + 1
                else:
                    d = 0
                depth.append(d)
    return (np.asarray(syms, dtype=np.int64),
            np.asarray(feats, dtype=np.int64),
            np.asarray(nby, dtype=np.int64),
            np.asarray(depth, dtype=np.int64))


# ── engine-native mitosis (BYTE-FAITHFUL to H_1306/H_1307/H_1316) ───────────────
def assign_all(centers_t, X_t):
    d2 = torch.cdist(X_t, centers_t, p=2)
    return torch.argmin(d2, dim=1)


def all_heads(Y_t, owner, K, ntr, vj, dev):
    Hmat = torch.full((K, vj), LAPLACE, dtype=torch.float64, device=dev)
    own = owner[:ntr]
    y = Y_t[:ntr]
    flat = own * vj + y
    ones = torch.ones(flat.shape[0], dtype=torch.float64, device=dev)
    Hmat.view(-1).index_add_(0, flat, ones)
    Hmat = Hmat / Hmat.sum(dim=1, keepdim=True)
    return Hmat


def owned_ce(Y_t, owner, k, ntr, p_row):
    mask = (owner[:ntr] == k)
    if not mask.any():
        return -1.0
    yk = Y_t[:ntr][mask]
    return -torch.log(p_row[yk] + 1e-12).mean().item()


def grow_on(centers, X_tr, Y_tr, ntr, vj, dev, grow_max):
    centers = [list(c) for c in centers]
    while len(centers) < grow_max:
        ct = torch.tensor(centers, dtype=torch.float64, device=dev)
        owner = assign_all(ct, X_tr)
        K = len(centers)
        owntr = owner[:ntr]
        owned_n = torch.bincount(owntr, minlength=K).cpu().numpy()
        Hmat = all_heads(Y_tr, owner, K, ntr, vj, dev)
        local_ce = np.full(K, -1.0)
        for k in range(K):
            if owned_n[k] > 0:
                local_ce[k] = owned_ce(Y_tr, owner, k, ntr, Hmat[k])
        elig = [k for k in range(K) if owned_n[k] >= MIN_OWNED and local_ce[k] > SPLIT_THRESH_CE]
        if not elig:
            break
        pick = elig[0]
        bestce = local_ce[elig[0]]
        for k in elig[1:]:
            if local_ce[k] > bestce:
                bestce = local_ce[k]
                pick = k
        if len(centers) + 1 > grow_max:
            break
        pmask = (owntr == pick)
        pts = X_tr[:ntr][pmask]
        if pts.shape[0] == 0:
            break
        var = pts.var(dim=0, unbiased=False)
        ax = int(torch.argmax(var).item())
        col = pts[:, ax]
        m = col.shape[0]
        scol, _ = torch.sort(col)
        if m % 2 == 1:
            med = scol[m // 2].item()
        else:
            med = ((scol[m // 2 - 1] + scol[m // 2]) / 2.0).item()
        lo_mask = col <= med
        hi_mask = col > med
        if int(lo_mask.sum().item()) == 0 or int(hi_mask.sum().item()) == 0:
            break
        c_lo = pts[lo_mask].mean(dim=0).cpu().numpy().tolist()
        c_hi = pts[hi_mask].mean(dim=0).cpu().numpy().tolist()
        centers = [centers[i] for i in range(len(centers)) if i != pick] + [c_lo, c_hi]
    return centers


def split_even_odd(X, Y, NB, stride):
    X, Y, NB = X[::stride], Y[::stride], NB[::stride]
    idx = np.arange(X.shape[0])
    e = idx % 2 == 0
    o = idx % 2 == 1
    return X[e], Y[e], NB[e], X[o], Y[o], NB[o]


def per_byte_ce(centers_t, X_tr_t, Y_tr_t, ntr, X_te_t, Y_te_t, NB_te, vj, dev):
    owner_tr = assign_all(centers_t, X_tr_t)
    Hmat = all_heads(Y_tr_t, owner_tr, centers_t.shape[0], ntr, vj, dev)
    owner_te = assign_all(centers_t, X_te_t)
    p = Hmat[owner_te, Y_te_t]
    nll = -torch.log(p + 1e-12)
    nb_t = torch.tensor(NB_te, dtype=torch.float64, device=dev)
    total_nats = nll.sum().item()
    total_bytes = float(nb_t.sum().item())
    return total_nats / total_bytes, total_nats, total_bytes, len(nll)


# ── partition feature builders ──────────────────────────────────────────────────
def feat_norm(feats):
    """Normalize the 5 int columns to ~[0,1] by their divisors (raw-byte cols use 16)."""
    out = feats.astype(np.float64).copy()
    out[:, 0] /= 16.0   # col0 spans 0..15 (byte hi-nibble) or 0..7 (artic) → scale by 16 (consistent)
    out[:, 1] /= 16.0   # col1 spans 0..15 (byte lo-nibble) or 0..3 (manner/vbase)
    out[:, 2] /= 3.0
    out[:, 3] /= 2.0
    out[:, 4] /= 2.0
    return out


def build_X_jamo(syms, depth, vj):
    """H_1316 opaque-id partition geometry (BASELINE re-port): [last/Vj, second/Vj, depth/3]."""
    n = len(syms)
    idx = np.arange(4, n - 1)
    last = syms[idx - 1].astype(np.float64) / float(vj)
    second = syms[idx - 2].astype(np.float64) / float(vj)
    cdep = depth[idx - 1].astype(np.float64) / 3.0
    X = np.stack([last, second, cdep], axis=1)
    Y = syms[idx].astype(np.int64)
    return X, Y, idx


def build_X_featural(syms, feats, depth, vj):
    """FEATURAL partition geometry: previous-2 symbols' DESIGN feature columns + cont_depth.
       X dim = 5 (last feats) + 5 (second feats) + 1 (depth) = 11. Label Y = same jamo-symbol id."""
    n = len(syms)
    idx = np.arange(4, n - 1)
    fn = feat_norm(feats)
    last_f = fn[idx - 1]
    second_f = fn[idx - 2]
    cdep = (depth[idx - 1].astype(np.float64) / 3.0)[:, None]
    X = np.concatenate([last_f, second_f, cdep], axis=1)   # N×11
    Y = syms[idx].astype(np.int64)
    return X, Y, idx


def arm_ce(X, Y, idx, nbytes, vj, stride, dev, grow_max, seed_centers):
    NB_lab = nbytes[idx]
    Xtr, Ytr, NBtr, Xte, Yte, NBte = split_even_odd(X, Y, NB_lab, stride)
    Xtr_t = torch.tensor(Xtr, dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Xte_t = torch.tensor(Xte, dtype=torch.float64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    c = grow_on(seed_centers, Xtr_t, Ytr_t, Xtr.shape[0], vj, dev, grow_max)
    ct = torch.tensor(c, dtype=torch.float64, device=dev)
    ce_b, tot_nats, tot_bytes, nsym = per_byte_ce(ct, Xtr_t, Ytr_t, Xtr.shape[0], Xte_t, Yte_t, NBte, vj, dev)
    if dev.type == "cuda":
        torch.cuda.synchronize()
    return {"cells": len(c), "ce_per_byte": round(ce_b, 5),
            "train_sym": int(Xtr.shape[0]), "test_sym": int(Xte.shape[0]),
            "test_bytes": int(tot_bytes), "vocab": vj}


def seed_centers_dim(dim):
    """Midpoint seed-center pattern lifted to `dim` (H_1307 [[0.3,...,0.0],[0.7,...,0.5]] family)."""
    a = [0.3] * dim
    b = [0.7] * dim
    a[-1] = 0.0
    b[-1] = 0.5
    return [a, b]


# ── F3 LINEARITY probe (closed-form ridge; held-out next-symbol CE in feature vs jamo-id space) ──
def linearity_ce(Xdesign, Y, idx, nbytes, vj, stride, dev, lam=1.0):
    """Fit a closed-form multinomial-ish LINEAR predictor: ridge-regress one-hot(Y) on Xdesign(+bias),
       softmax the held-out scores, report per-byte CE. Same train/test even/odd split. This measures
       how LINEARLY predictable the next symbol is from the given representation."""
    NB_lab = nbytes[idx]
    Xtr, Ytr, NBtr, Xte, Yte, NBte = split_even_odd(Xdesign, Y, NB_lab, stride)
    # restrict label space to symbols seen in train (others get a floor prob)
    Xtr_t = torch.tensor(np.concatenate([Xtr, np.ones((Xtr.shape[0], 1))], axis=1), dtype=torch.float64, device=dev)
    Xte_t = torch.tensor(np.concatenate([Xte, np.ones((Xte.shape[0], 1))], axis=1), dtype=torch.float64, device=dev)
    Ytr_t = torch.tensor(Ytr, dtype=torch.int64, device=dev)
    Yte_t = torch.tensor(Yte, dtype=torch.int64, device=dev)
    d = Xtr_t.shape[1]
    # one-hot targets over vj
    Yoh = torch.zeros((Xtr_t.shape[0], vj), dtype=torch.float64, device=dev)
    Yoh[torch.arange(Xtr_t.shape[0], device=dev), Ytr_t] = 1.0
    A = Xtr_t.t() @ Xtr_t + lam * torch.eye(d, dtype=torch.float64, device=dev)
    B = Xtr_t.t() @ Yoh
    W = torch.linalg.solve(A, B)                 # d×vj
    logits = Xte_t @ W                           # N×vj
    logits = logits - logits.max(dim=1, keepdim=True).values
    probs = torch.softmax(logits, dim=1)
    p = probs[torch.arange(Xte_t.shape[0], device=dev), Yte_t].clamp_min(1e-12)
    nll = -torch.log(p)
    nb_t = torch.tensor(NBte, dtype=torch.float64, device=dev)
    return (nll.sum().item() / float(nb_t.sum().item()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ko-window", type=int, default=30_000_000)
    ap.add_argument("--en-window", type=int, default=10_000_000)
    ap.add_argument("--ko-stride", type=int, default=300)
    ap.add_argument("--grow-max", type=int, default=GROW_MAX)
    ap.add_argument("--seeds", default="4322,4323,4324")
    ap.add_argument("--out", default="/tmp/h1322_out")
    ap.add_argument("--ko-cache", default="/tmp/h1311_ko_raw.bytes")
    ap.add_argument("--en-cache", default="/tmp/h1311_en_raw.bytes")
    ap.add_argument("--cpu", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if args.cpu or not torch.cuda.is_available():
        dev = torch.device("cpu")
        log("=== H_1322 — FEATURAL decomposition vs the jamo 2.51335 floor (CPU) ===")
    else:
        dev = torch.device("cuda")
        cap = torch.cuda.get_device_capability(0)
        log(f"=== H_1322 — FEATURAL decomposition vs the jamo 2.51335 floor (sm_{cap[0]}{cap[1]}) ===")
        log(f"device={torch.cuda.get_device_name(0)} cap={cap} torch={torch.__version__}")
        _t = (torch.randn(512, 512, device=dev) @ torch.randn(512, 512, device=dev)).sum().item()
        torch.cuda.synchronize()
        log(f"kernel launch OK (sentinel {_t:.1f})")

    t0 = time.time()
    # ── REAL corpus, BYTE-IDENTICAL to H_1307 RUN A / H_1316 ──
    if os.path.exists(args.ko_cache) and os.path.getsize(args.ko_cache) >= args.ko_window:
        ko_raw = open(args.ko_cache, "rb").read()[: args.ko_window + 8]
        log(f"[corpus] KO from cache {args.ko_cache}")
    else:
        log(f"[corpus] fetching {args.ko_window} REAL KO bytes from r2://{os.environ.get('R2_BUCKET','?')}/{R2_KO_KEY}")
        ko_raw = fetch_r2_range(R2_KO_KEY, args.ko_window + 8)
        open(args.ko_cache, "wb").write(ko_raw)
    ko_win = trim_utf8(ko_raw[: args.ko_window])
    ko_sha = hashlib.sha256(ko_win).hexdigest()
    same_ko = (ko_sha == H1307_KO_SHA)
    log(f"[corpus] KO {len(ko_win)}B sha={ko_sha[:16]}…  identical-to-H_1307-RUN-A={same_ko}")
    if not same_ko:
        log("FATAL: KO corpus sha != H_1307 RUN A — REFUSING to run (provenance gate, REAL-only). STOP.")
        sys.exit(3)
    ko_text = ko_win.decode("utf-8")

    # ── NO-CHEAT round-trip + accounting ──
    rt = roundtrip_and_accounting(ko_text)
    log(f"[nocheat] hangul_syllables={rt['hangul_syllables']} roundtrip_fail={rt['roundtrip_fail']} ok={rt['ok']}")

    # ── vocab + intact design feature map ──
    jamo_to_id, jamo_sorted = build_jamo_vocab(ko_text)
    n_jamo = len(jamo_sorted)
    VJ = 256 + n_jamo
    log(f"[jamo] distinct jamo codepoints={n_jamo}  jamo-symbol vocab Vj={VJ}")
    # coverage check: which jamo lack a design feature vector (would fall back to zero)
    intact_map = {}
    missing = []
    for cp in jamo_sorted:
        fv = jamo_feature_vec(cp)
        if fv is None:
            missing.append(cp)
            intact_map[cp] = [0, 0, 0, 0, 0]
        else:
            intact_map[cp] = fv
    log(f"[featmap] design-feature coverage: {n_jamo - len(missing)}/{n_jamo} jamo mapped; "
        f"missing={[hex(m) for m in missing][:20]}")

    # ── G0 raw-byte re-port (sanity: opaque-id, vocab 256) ──
    ko_bytes = np.frombuffer(ko_win, dtype=np.uint8).astype(np.int64)
    raw_depth = np.zeros(len(ko_bytes), dtype=np.int64)
    d = 0
    is_cont = (ko_bytes >= 0x80) & (ko_bytes <= 0xBF)
    for i in range(len(ko_bytes)):
        d = d + 1 if is_cont[i] else 0
        raw_depth[i] = d
    raw_nbytes = np.ones(len(ko_bytes), dtype=np.int64)
    Xr, Yr, idxr = build_X_jamo(ko_bytes, raw_depth, 256)
    g0 = arm_ce(Xr, Yr, idxr, raw_nbytes, 256, args.ko_stride, dev, args.grow_max, seed_centers_dim(3))
    log(f"[G0 raw-byte] {json.dumps(g0)}  (H_1316 reproduced 2.95342)")

    # ── G1 jamo opaque-id re-port (BASELINE = H_1316 jamo floor) ──
    syms_i, feats_i, nby_i, depth_i = make_streams(ko_text, jamo_to_id, intact_map)
    acct_ok = (int(nby_i.sum()) == len(ko_win))
    log(f"[nocheat] byte-accounting: Σ n_bytes={int(nby_i.sum())} corpus_bytes={len(ko_win)} close={acct_ok}")
    Xj, Yj, idxj = build_X_jamo(syms_i, depth_i, VJ)
    g1jamo = arm_ce(Xj, Yj, idxj, nby_i, VJ, args.ko_stride, dev, args.grow_max, seed_centers_dim(3))
    log(f"[G1 jamo opaque-id] {json.dumps(g1jamo)}  (H_1316 floor=2.51335)")

    # ── G2 FEATURAL (intact design map) + G2c SHUFFLE-feature-map control ──
    seeds = [int(s) for s in args.seeds.split(",") if s.strip()]
    per_seed = []
    # intact featural X (deterministic; same across seeds)
    Xf, Yf, idxf = build_X_featural(syms_i, feats_i, depth_i, VJ)
    g2_intact = arm_ce(Xf, Yf, idxf, nby_i, VJ, args.ko_stride, dev, args.grow_max, seed_centers_dim(Xf.shape[1]))
    log(f"[G2 featural intact] {json.dumps(g2_intact)}")

    # F3 LINEARITY: feature space vs jamo-id space (intact, deterministic)
    # jamo-id space design = one-hot-ish low-dim id columns (the H_1316 opaque-id X)
    lin_feat = linearity_ce(Xf, Yf, idxf, nby_i, VJ, args.ko_stride, dev)
    lin_jamo = linearity_ce(Xj, Yj, idxj, nby_i, VJ, args.ko_stride, dev)
    log(f"[F3 linearity] feature-space CE={round(lin_feat,5)}  jamo-id-space CE={round(lin_jamo,5)}  "
        f"Δ(jamo−feat)={round(lin_jamo-lin_feat,5)}")

    for sd in seeds:
        # SHUFFLE-feature-map control: bijection over the jamo set → reassign each jamo's feature
        # vector to a DIFFERENT jamo's vector (destroys ㄱ/ㅋ one-apart systematicity; same #vectors).
        rng = np.random.default_rng(sd)
        perm = rng.permutation(len(jamo_sorted))
        shuf_map = {}
        for i, cp in enumerate(jamo_sorted):
            shuf_map[cp] = intact_map[jamo_sorted[perm[i]]]
        syms_s, feats_s, nby_s, depth_s = make_streams(ko_text, jamo_to_id, shuf_map)
        Xfs, Yfs, idxfs = build_X_featural(syms_s, feats_s, depth_s, VJ)
        g2c = arm_ce(Xfs, Yfs, idxfs, nby_s, VJ, args.ko_stride, dev, args.grow_max, seed_centers_dim(Xfs.shape[1]))
        rec = {"seed": sd,
               "g0_raw_ce": g0["ce_per_byte"],
               "g1_jamo_ce": g1jamo["ce_per_byte"],
               "g2_featural_ce": g2_intact["ce_per_byte"], "g2_cells": g2_intact["cells"],
               "g2c_shuffle_feat_ce": g2c["ce_per_byte"], "g2c_cells": g2c["cells"]}
        log(f"[seed {sd}] " + json.dumps(rec))
        per_seed.append(rec)

    # ── means ──
    g0_mean = g0["ce_per_byte"]
    g1jamo_mean = g1jamo["ce_per_byte"]
    g2_mean = g2_intact["ce_per_byte"]
    g2c_mean = float(np.mean([r["g2c_shuffle_feat_ce"] for r in per_seed]))

    # compare against the LOCKED H_1316 jamo floor AND the in-run jamo re-port (report both)
    jamo_floor = H1316_JAMO_CE

    # ── FROZEN bars ──
    f1_vs_jamo = (g2_mean < (jamo_floor - F1_MARGIN))
    f1_vs_raw = (g2_mean < H1307_CEILING_KO_CE)
    f1 = bool(f1_vs_jamo and f1_vs_raw)
    f2 = bool((g2c_mean - g2_mean) >= F2_MARGIN)
    f3 = bool((lin_jamo - lin_feat) >= F3_MARGIN)
    green = bool(f1 and f2)
    if green:
        verdict = ("🟢 GREEN — Hangul's DESIGNED featural systematicity gives KO a measurable DEPTH "
                   "advantage BELOW jamo (deeper featural decomposition is the right representation)")
    elif (not f1):
        verdict = ("🧱 HONEST-FLOOR — F1 fails: featural does NOT beat the jamo floor by the bar → "
                   "jamo is the decomposition FLOOR for this mechanism (bounds the depth, c9)")
    elif f1 and (not f2):
        verdict = ("🟠 DIMS-NOT-DESIGN — F1 holds but F2 fails: the featural gain is dimensionality, "
                   "NOT the designed systematicity (shuffle ties featural; honest negative, c9)")
    else:
        verdict = "🔴 mixed-fail"

    total_wall = time.time() - t0
    summary = {
        "id": "H_1322",
        "device": (torch.cuda.get_device_name(0) if dev.type == "cuda" else "cpu"),
        "torch": torch.__version__,
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "corpus_identical_to_H1307_runA": bool(same_ko),
        "ko_stride": args.ko_stride, "grow_max": args.grow_max,
        "jamo_vocab_Vj": VJ, "distinct_jamo": n_jamo,
        "design_feature_coverage": f"{n_jamo - len(missing)}/{n_jamo}",
        "raw_ceiling_ko_ce": H1307_CEILING_KO_CE,
        "jamo_floor_ko_ce_locked": jamo_floor,
        "g0_raw_byte_ce_inrun": g0_mean,
        "g1_jamo_opaque_id_ce_inrun": g1jamo_mean,
        "g2_featural_ce": g2_mean,
        "g2c_shuffle_feature_ce_mean": round(g2c_mean, 5),
        "delta_featural_vs_jamo_floor": round(g2_mean - jamo_floor, 5),
        "delta_featural_vs_jamo_inrun": round(g2_mean - g1jamo_mean, 5),
        "delta_featural_vs_raw": round(g2_mean - H1307_CEILING_KO_CE, 5),
        "delta_shuffle_minus_featural": round(g2c_mean - g2_mean, 5),
        "linearity_feature_ce": round(lin_feat, 5),
        "linearity_jamo_id_ce": round(lin_jamo, 5),
        "linearity_advantage": round(lin_jamo - lin_feat, 5),
        "seeds": seeds, "per_seed": per_seed,
        "nocheat_roundtrip": rt, "nocheat_byte_accounting_close": acct_ok,
        "F1_deeper": f1, "F1_vs_jamo": bool(f1_vs_jamo), "F1_vs_raw": bool(f1_vs_raw),
        "F2_earned": f2, "F3_linearity": f3,
        "GREEN": green, "verdict": verdict,
        "total_wall_s": round(total_wall, 2),
    }
    with open(os.path.join(args.out, "h1322_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    manifest = {
        "ko_source": f"r2://{os.environ.get('R2_BUCKET','phanes')}/{R2_KO_KEY} bytes[0:{args.ko_window}] trimmed[:{len(ko_win)}]",
        "ko_window_bytes": len(ko_win), "ko_window_sha256": ko_sha,
        "identical_to_H1307_runA": bool(same_ko),
        "ko_stride": args.ko_stride, "grow_max": args.grow_max, "jamo_vocab": VJ,
        "feature_cols": N_FEAT_COLS, "design_feature_coverage": f"{n_jamo - len(missing)}/{n_jamo}",
    }
    with open(os.path.join(args.out, "h1322_manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log("-------------------------------------------------------------------------------")
    log(f"CE LADDER (nats/UTF-8-byte):")
    log(f"  raw-byte ceiling   = {H1307_CEILING_KO_CE}  (in-run G0 {g0_mean})")
    log(f"  jamo floor (H_1316)= {jamo_floor}           (in-run jamo re-port {g1jamo_mean})")
    log(f"  FEATURAL (intact)  = {g2_mean}              Δvs_jamo_floor={round(g2_mean-jamo_floor,5)}  Δvs_raw={round(g2_mean-H1307_CEILING_KO_CE,5)}")
    log(f"  SHUFFLE-feat ctrl  = {round(g2c_mean,5)} (mean {len(seeds)} seeds)  Δ(shuf−feat)={round(g2c_mean-g2_mean,5)}")
    log(f"F1 DEEPER   (feat < jamo {jamo_floor}−{F1_MARGIN} AND < raw): {f1}  (vs_jamo={f1_vs_jamo} vs_raw={f1_vs_raw})")
    log(f"F2 EARNED   (feat < shuffle-feat by >={F2_MARGIN}): {f2}")
    log(f"F3 LINEARITY(feat-space more linear by >={F3_MARGIN}): {f3}  (Δ={round(lin_jamo-lin_feat,5)})")
    log(f"VERDICT: {verdict}")
    log(f"total wall={total_wall:.1f}s")
    log("  engine-transfer to live hexa DIRECTIONAL (re-confirm on CORE/*.hexa = follow-on). NO fluency claim.")
    log("[done]")


if __name__ == "__main__":
    main()
