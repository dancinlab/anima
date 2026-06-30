#!/usr/bin/env python3
"""Lane A GOLD scale-ceiling corpus — FLORES-200 devtest, 5 langs, byte-for-byte REAL GOLD.

WHY (a_completeness_over_cheap primary path): rung4 (corpus_real250) stopped at NC=250 because the
honest real ceiling was AUTHORING quality — Tier-3 (concepts 100..249) were model-authored aligned
propositions, and pushing past 250 with MORE authored padding would CONFOUND the scale science
(is a ci_lo drop the CHIP ceiling, or just lower corpus quality?). The clean fix is NOT more authored
padding (a_completeness_over_cheap dont: merge-of-failures) — it is SOURCING genuine professional GOLD
parallel data so every rung is the same provenance. FLORES-200 devtest = 1012 professionally-translated
parallel sentences across 200 langs (ungated fbaipublicfiles tarball). Using the SAME 5 langs as the
prior rungs (en/zh/ru/ja/ko), each parallel sentence = one real GOLD concept -> a clean codebook up to
NC=1012 with ZERO authored or synthetic padding. This lets the A-single (AKIDA) single-step generation
ladder and the A-multi (HYBRID) branching ladder run >=3 rungs PAST 250 (250/500/1000) on uniform gold,
so the anchor-count at which 1-bit/256-unit on-chip generation crosses the shuffle-NULL is a CLEAN
quantified real-semantic ceiling (a_scale_honest_scope), not a corpus-quality artifact.

PROVENANCE (single tier, all gold): flores200_devtest_gold — FLORES-200 devtest, byte-preserved from the
official facebookresearch/flores release. NOT model-authored. NOT synthetic. NOT hand-authored.

OUTPUT: corpus_flores_gold/parallel.limen + manifest.json — LIMEN format byte-identical to
build_corpus_real250.py so onchip_xlm_gen_scale_flores.py / onchip_xlm_branching_flores.py consume it
UNCHANGED (the harness subsets the first N sorted concepts x 5 langs per rung).

substrate note: this builder is HOST-side corpus prep (CPU). The chip rungs that CONSUME it run on live
AKD1000 (A-single=AKIDA) / on-chip enc + off-chip head (A-multi=HYBRID) per a_lane_akida_gpu_split.
"""
import os, json, struct, hashlib, sys

LANGS = ["en", "zh", "ru", "ja", "ko"]
# FLORES-200 file codes, in the SAME order as LANGS (concept tuple order must match LANGS).
FLORES_CODES = {"en": "eng_Latn", "zh": "zho_Hans", "ru": "rus_Cyrl", "ja": "jpn_Jpan", "ko": "kor_Hang"}

FLORES_DIR = os.environ.get("FLORES_DEVTEST_DIR", os.path.expanduser("/tmp/flores200_dataset/devtest"))
OUT_DIR = os.environ.get("FLORES_OUT_DIR", os.path.expanduser("~/clm_kosmos_akida/corpus_flores_gold"))
MAX_NC = int(os.environ.get("FLORES_MAX_NC", "1012"))  # FLORES devtest has 1012 parallel sentences

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"; LIMEN_VER = 2


def read_flores_lang(code):
    path = os.path.join(FLORES_DIR, f"{code}.devtest")
    with open(path, "r", encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f]


def load_concepts():
    cols = {lang: read_flores_lang(FLORES_CODES[lang]) for lang in LANGS}
    n = min(len(cols[lang]) for lang in LANGS)
    concepts = []
    seen_en = set()
    for i in range(n):
        row = tuple(cols[lang][i].strip() for lang in LANGS)
        if any(not cell for cell in row):
            continue  # skip any incomplete parallel row (gold data should have none)
        if row[0] in seen_en:
            continue  # dedup by EN sentence (FLORES sentences are distinct; defensive)
        seen_en.add(row[0])
        concepts.append(row)
        if len(concepts) >= MAX_NC:
            break
    return concepts


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def merkle_root(leaves):
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer:
        return b"\x00" * 32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0]


def anchor_record(idx, concept_id, lang, text, n_concepts):
    payload = text.encode("utf-8")
    coord_x = round(concept_id / max(1, n_concepts - 1), 4)
    coord_y = round(LANGS.index(lang) / max(1, len(LANGS) - 1), 4)
    head = {"id": f"a{idx:04d}", "concept": concept_id, "lang": lang,
            "coord": [coord_x, coord_y], "lane": lang, "radius": 1.0, "tier": 0,
            "tags": ["clm", "semantic", lang],
            "payload_len": len(payload), "payload_sha256": sha256_hex(payload)}
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head_b)) + head_b + payload, payload


def write_limen(path, concepts):
    n_concepts = len(concepts)
    records = []
    for ci, concept in enumerate(concepts):
        for li, txt in enumerate(concept):
            records.append((ci, LANGS[li], txt))
    blob = bytearray(); blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER); blob += struct.pack("<I", len(records))
    payloads = []
    for idx, (cid, lang, txt) in enumerate(records):
        rec, payload = anchor_record(idx, cid, lang, txt, n_concepts)
        blob += struct.pack("<I", len(rec)); blob += rec; payloads.append(payload)
    root = merkle_root(payloads); blob += root
    with open(path, "wb") as f:
        f.write(blob)
    return sha256_hex(bytes(blob)), root.hex(), len(records)


def byte_len_stats(concepts):
    import math
    lens = [len(concepts[ci][li].encode("utf-8")) for ci in range(len(concepts)) for li in range(5)]
    n = len(lens); mean = sum(lens) / n
    var = sum((x - mean) ** 2 for x in lens) / n
    return {"n_anchors": n, "mean_bytes": round(mean, 2), "sd_bytes": round(math.sqrt(var), 2),
            "min": min(lens), "max": max(lens)}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    concepts = load_concepts()
    nc = len(concepts)
    # source-file checksums so the gold provenance is auditable end-to-end
    src_sha = {}
    for lang in LANGS:
        with open(os.path.join(FLORES_DIR, f"{FLORES_CODES[lang]}.devtest"), "rb") as f:
            src_sha[FLORES_CODES[lang]] = sha256_hex(f.read())
    shard = os.path.join(OUT_DIR, "parallel.limen")
    sha, merkle, count = write_limen(shard, concepts)
    manifest = {
        "corpus": "clm-kosmos-akida-flores-gold", "kosmos_version": "2.0",
        "n_concepts": nc, "n_anchors": count, "langs": LANGS,
        "tiers": {
            "flores200_devtest_gold": {
                "concepts": f"0..{nc-1}", "count": nc,
                "provenance": ("FLORES-200 devtest parallel sentences (facebookresearch/flores official "
                               "ungated release), 5 langs en/zh/ru/ja/ko byte-preserved — REAL PROFESSIONAL "
                               "GOLD, NOT model-authored, NOT hand-authored, NOT synthetic"),
                "flores_codes": FLORES_CODES,
                "source_file_sha256": src_sha}},
        "byte_len_stats": byte_len_stats(concepts),
        "sha256": sha, "merkle": merkle}
    json.dump(manifest, open(os.path.join(OUT_DIR, "manifest.json"), "w"), indent=2, ensure_ascii=False)
    print(f"[flores-gold] {count} anchors / {nc} concepts -> {shard}")
    print(f"[flores-gold] sha256={sha}")
    print(f"[flores-gold] merkle={merkle}")
    print(f"[flores-gold] byte-len: {json.dumps(byte_len_stats(concepts))}")
    print(f"[flores-gold] source_file_sha256={json.dumps(src_sha)}")
    if nc < 1000:
        print(f"[flores-gold] WARN only {nc} gold concepts available (<1000) — top rung will cap at NC={nc}")


if __name__ == "__main__":
    main()
