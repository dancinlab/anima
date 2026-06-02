#!/usr/bin/env python3
"""Lane A SYNTHETIC-CAPACITY corpus — distinguishable byte-pattern anchors for the 256-unit / 524K on-chip
CODE-CAPACITY ceiling probe. substrate=AKIDA (the chip pipeline is unchanged) · a_scale_honest_scope honesty.

WHY THIS EXISTS (honest, NOT a fabricated semantic green):
  The REAL cross-lingual corpus (corpus_big) caps at 50 FLORES concepts / 250 anchors. The A-single rung+1 question
  ("does single-step on-chip GENERATION hold above-NULL as the anchor count GROWS, OR does it hit the 256-unit /
  524K chip-capacity ceiling — find WHERE it breaks") CANNOT be answered with 250 anchors: the corpus is the ceiling,
  not the chip. To reach the CHIP-CAPACITY frontier we build a SYNTHETIC corpus of distinguishable byte-pattern
  anchors that flows through the BYTE-IDENTICAL on-chip pipeline (enc_whitened over byte-histograms -> bind -> 256-unit
  AkidaUnsupervised FC -> open-vocab decode). This is a CODE-CAPACITY probe, explicitly labelled synthetic — NOT a
  semantic/cross-lingual claim, NOT a fabricated PUBLIC. The successor structure is the same index ring used by the
  proven rungs; only the ANCHOR PAYLOADS are synthetic (so we can grow NC past the real-corpus ceiling and see the
  256-unit code saturate / collapse — finding-either-direction valid, a_paper_negative_ok).

DESIGN (distinguishable-but-overlapping, so the 256-unit code is the binding constraint, not trivial separability):
  - NC concepts x L=5 "langs". Each concept c gets a concept-specific byte-frequency profile theta_c (a sparse
    random multinomial over the 256 byte-vocab, ACTIVE_BYTES nonzero bytes). Each (c,l) anchor = a length-PAYLOAD_LEN
    byte string sampled from a per-(c,l) noisy mixture (1-LANG_NOISE)*theta_c + LANG_NOISE*theta_lang, so the 5
    langs of a concept share theta_c (cross-anchor structure exists) yet differ (5 realizations), exactly mirroring
    the real corpus's "5 langs of one concept adjacent" structure. As NC grows the theta_c profiles crowd the
    256-byte simplex -> the 256-unit 1-bit code must resolve more, harder neighbours -> the chip-capacity ceiling.
  - Deterministic seed -> byte-reproducible. .limen format byte-identical to build_corpus.py (LIMEN\\0\\0\\0 + ver +
    count + len-prefixed @anchor recs + 32B merkle root); concept/lang headers match corpus_big so the harnesses
    (which subset by concept) consume it UNCHANGED.

USAGE: LANE_A_SYNTH_NC=500 python build_corpus_synth_capacity.py  (default NC=500 -> 2500 anchors)
       writes ~/clm_kosmos_akida/corpus_synth/parallel.limen
"""
import os, json, struct, hashlib
import numpy as np

OUT = os.path.expanduser("~/clm_kosmos_akida/corpus_synth")
os.makedirs(OUT, exist_ok=True)

NC          = int(os.environ.get("LANE_A_SYNTH_NC", "500"))   # number of distinguishable concepts
LANGS       = ["en", "zh", "ru", "ja", "ko"]                   # 5 "langs" = 5 noisy realizations per concept
L           = len(LANGS)
PAYLOAD_LEN = int(os.environ.get("LANE_A_SYNTH_PLEN", "120"))  # bytes per anchor (~ real-corpus line length scale)
ACTIVE_BYTES= int(os.environ.get("LANE_A_SYNTH_ACT", "40"))    # nonzero bytes in a concept profile (simplex crowding)
LANG_NOISE  = float(os.environ.get("LANE_A_SYNTH_LNOISE", "0.35"))  # per-lang deviation from the shared concept profile
SEED        = int(os.environ.get("LANE_A_SYNTH_SEED", "20260603"))
VOCAB       = 256

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
LIMEN_VER   = 2

def sha256_hex(b): return hashlib.sha256(b).hexdigest()
def merkle_root(leaves):
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer: return b"\x00" * 32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0]

rng = np.random.default_rng(SEED)
# per-LANG base profile (shared across concepts so a "lang" is a real shared axis, like a script's byte stats)
lang_theta = []
for li in range(L):
    p = np.zeros(VOCAB)
    act = rng.choice(VOCAB, size=ACTIVE_BYTES, replace=False)
    p[act] = rng.random(ACTIVE_BYTES); p = p / p.sum()
    lang_theta.append(p)
# per-CONCEPT profile (the cross-lingual structure the encoder must learn; crowds the simplex as NC grows)
concept_theta = []
for c in range(NC):
    p = np.zeros(VOCAB)
    act = rng.choice(VOCAB, size=ACTIVE_BYTES, replace=False)
    p[act] = rng.random(ACTIVE_BYTES); p = p / p.sum()
    concept_theta.append(p)

def make_payload(c, li):
    mix = (1.0 - LANG_NOISE) * concept_theta[c] + LANG_NOISE * lang_theta[li]
    mix = mix / mix.sum()
    draw = rng.choice(VOCAB, size=PAYLOAD_LEN, p=mix)
    return bytes(int(x) for x in draw)

def anchor_record(idx, concept_id, lang, payload):
    coord_x = round(concept_id / max(1, NC - 1), 4)
    coord_y = round(LANGS.index(lang) / max(1, L - 1), 4)
    head = {"id": f"a{idx:04d}", "concept": concept_id, "lang": lang,
            "coord": [coord_x, coord_y], "lane": lang, "radius": 1.0, "tier": 0,
            "tags": ["clm", "synthetic-capacity", lang],
            "payload_len": len(payload), "payload_sha256": sha256_hex(payload)}
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head_b)) + head_b + payload, payload

# parallel ordering: concept-major (5 langs of each concept adjacent) — matches corpus_big
records = []
for c in range(NC):
    for li, lang in enumerate(LANGS):
        records.append((c, lang, make_payload(c, li)))

blob = bytearray(); blob += LIMEN_MAGIC
blob += struct.pack("<I", LIMEN_VER); blob += struct.pack("<I", len(records))
payloads = []
for idx, (cid, lang, payload) in enumerate(records):
    rec, pl = anchor_record(idx, cid, lang, payload)
    blob += struct.pack("<I", len(rec)); blob += rec; payloads.append(pl)
root = merkle_root(payloads); blob += root
path = os.path.join(OUT, "parallel.limen")
with open(path, "wb") as f: f.write(blob)
print("[synth] NC=%d langs=%d -> %d anchors  plen=%d active=%d lnoise=%.2f seed=%d"
      % (NC, L, len(records), PAYLOAD_LEN, ACTIVE_BYTES, LANG_NOISE, SEED))
print("[synth] wrote %s sha256=%s merkle=%s" % (path, sha256_hex(bytes(blob))[:16], root.hex()[:16]))
# sanity: concept distinguishability (mean pairwise L1 between concept byte-hists should be > 0, < 2)
H = np.zeros((min(NC, 60), VOCAB))
for c in range(min(NC, 60)):
    cnt = np.zeros(VOCAB)
    for li in range(L):
        for b in records[c * L + li][2]: cnt[b] += 1
    H[c] = cnt / cnt.sum()
d = []
for i in range(H.shape[0]):
    for j in range(i + 1, H.shape[0]):
        d.append(np.abs(H[i] - H[j]).sum())
print("[synth] concept byte-hist mean pairwise L1 (first 60c) = %.4f (0=identical, 2=disjoint)" % float(np.mean(d)))
