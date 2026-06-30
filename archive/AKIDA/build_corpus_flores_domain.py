#!/usr/bin/env python3
"""H_861 METASTASIS corpus — FLORES-200 ordered by SOURCE DOMAIN for a controlled domain-boundary transfer test.

WHY (H_861 falsifier, controlled): does a learned transition operator transfer ACROSS a domain boundary, or is it
corpus-axis-bound? The branching harness holds out the LAST N_TEST_FRAC concepts as TEST. To make TEST a genuine
DISTANT domain we order concepts by FLORES source domain. BUT a contiguous TEST block + small ring offsets can hit
the PR#1694 structural-0 artifact (a TEST concept's successors are mostly other TEST concepts the head never emits).
To control for that, we emit TWO corpora with IDENTICAL split GEOMETRY (same last-30% holdout):
  - corpus_flores_domain   : concepts ordered [wikinews, wikibooks, wikivoyage] -> TEST(last 320)=wikivoyage (REAL distant domain)
  - corpus_flores_shuffled : SAME concepts, domain labels PERMUTED -> TEST(last 320)=domain-mixed (WITHIN-dist control)
Running the SAME harness (NC=1012, N_TEST_FRAC=0.3162) on both: any structural-0 artifact affects BOTH equally, so
the held-out hop-2/3 DIFFERENCE (domain vs shuffled) cleanly isolates the DOMAIN-BOUNDARY effect.
  domain held >= shuffled held  -> operator is domain-AGNOSTIC = METASTASIS (F-861 REFUTED)
  domain held << shuffled held  -> corpus-axis-bound (F-861 CONFIRMED, closed-negative — corpus-axis ⊥ register)

LIMEN format byte-identical to build_corpus_flores_gold.py. substrate note: HOST-side prep; chip rungs run on
live AKD1000 enc ⊕ off-chip head (HYBRID) per a_lane_akida_gpu_split.
"""
import os, json, struct, hashlib, random

LANGS = ["en", "zh", "ru", "ja", "ko"]
FLORES_CODES = {"en": "eng_Latn", "zh": "zho_Hans", "ru": "rus_Cyrl", "ja": "jpn_Jpan", "ko": "kor_Hang"}
FLORES_DIR = os.environ.get("FLORES_DEVTEST_DIR", "/tmp/flores200_dataset/devtest")
META = os.environ.get("FLORES_META", "/tmp/flores200_dataset/metadata_devtest.tsv")
OUT_DOMAIN = os.path.expanduser("~/clm_kosmos_akida/corpus_flores_domain")
OUT_SHUF = os.path.expanduser("~/clm_kosmos_akida/corpus_flores_shuffled")
# order domains so the SMALLER-index domains are TRAIN and the last domain is the held-out distant domain
DOMAIN_ORDER = ["wikinews", "wikibooks", "wikivoyage"]  # TEST(last ~30%) = wikivoyage (320)
SEED = 20260603
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"; LIMEN_VER = 2


def read_lang(code):
    with open(os.path.join(FLORES_DIR, f"{code}.devtest"), encoding="utf-8") as f:
        return [ln.rstrip("\n") for ln in f]


def read_domains():
    doms = []
    with open(META, encoding="utf-8") as f:
        next(f)  # header
        for ln in f:
            parts = ln.rstrip("\n").split("\t")
            doms.append(parts[1] if len(parts) > 1 else "unknown")  # domain column
    return doms


def sha256_hex(b): return hashlib.sha256(b).hexdigest()


def merkle_root(leaves):
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer: return b"\x00"*32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i+1] if i+1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a+b).digest())
        layer = nxt
    return layer[0]


def anchor_record(idx, cid, lang, text, nc):
    payload = text.encode("utf-8")
    head = {"id": f"a{idx:04d}", "concept": cid, "lang": lang,
            "coord": [round(cid/max(1, nc-1), 4), round(LANGS.index(lang)/4, 4)],
            "lane": lang, "radius": 1.0, "tier": 0, "tags": ["clm", "semantic", lang],
            "payload_len": len(payload), "payload_sha256": sha256_hex(payload)}
    hb = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(hb)) + hb + payload, payload


def write_limen(path, concepts):
    nc = len(concepts); recs = []
    for ci, c in enumerate(concepts):
        for li, txt in enumerate(c):
            recs.append((ci, LANGS[li], txt))
    blob = bytearray(); blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER); blob += struct.pack("<I", len(recs))
    pays = []
    for idx, (cid, lang, txt) in enumerate(recs):
        rec, p = anchor_record(idx, cid, lang, txt, nc); blob += struct.pack("<I", len(rec)) + rec; pays.append(p)
    blob += merkle_root(pays)
    open(path, "wb").write(blob)
    return sha256_hex(bytes(blob)), len(recs)


def emit(out_dir, concepts, label, domain_seq):
    os.makedirs(out_dir, exist_ok=True)
    sha, cnt = write_limen(os.path.join(out_dir, "parallel.limen"), concepts)
    from collections import Counter
    nc = len(concepts)
    # domain block boundaries (for the harness N_TEST_FRAC pin)
    manifest = {"corpus": f"clm-kosmos-akida-{label}", "n_concepts": nc, "n_anchors": cnt, "langs": LANGS,
                "domain_order": DOMAIN_ORDER, "domain_counts": dict(Counter(domain_seq)),
                "test_domain": DOMAIN_ORDER[-1], "test_n": dict(Counter(domain_seq)).get(DOMAIN_ORDER[-1], 0),
                "n_test_frac_for_clean_domain_split": round(dict(Counter(domain_seq)).get(DOMAIN_ORDER[-1], 0)/nc, 4),
                "provenance": "FLORES-200 devtest gold, ordered by source domain (metadata_devtest.tsv)", "sha256": sha}
    json.dump(manifest, open(os.path.join(out_dir, "manifest.json"), "w"), indent=2, ensure_ascii=False)
    print(f"[{label}] {cnt} anchors / {nc} concepts -> {out_dir}  sha256={sha}")
    print(f"[{label}] domain_counts={dict(Counter(domain_seq))} test_domain={DOMAIN_ORDER[-1]} n_test_frac={manifest['n_test_frac_for_clean_domain_split']}")
    return manifest


def main():
    cols = {l: read_lang(FLORES_CODES[l]) for l in LANGS}
    doms = read_domains()
    n = min(len(cols[l]) for l in LANGS); n = min(n, len(doms))
    # build (concept_tuple, domain) list, dedup by EN
    items = []; seen = set()
    for i in range(n):
        row = tuple(cols[l][i].strip() for l in LANGS)
        if any(not c for c in row) or row[0] in seen:
            continue
        seen.add(row[0]); items.append((row, doms[i]))
    # DOMAIN-ordered: sort by domain rank (wikinews, wikibooks, wikivoyage), stable
    rank = {d: i for i, d in enumerate(DOMAIN_ORDER)}
    dom_items = sorted(items, key=lambda it: rank.get(it[1], 99))
    dom_concepts = [it[0] for it in dom_items]; dom_seq = [it[1] for it in dom_items]
    emit(OUT_DOMAIN, dom_concepts, "flores-domain", dom_seq)
    # SHUFFLED control: same concepts, random order (TEST block = domain-mixed)
    rng = random.Random(SEED)
    shuf_items = items[:]; rng.shuffle(shuf_items)
    shuf_concepts = [it[0] for it in shuf_items]; shuf_seq = [it[1] for it in shuf_items]
    emit(OUT_SHUF, shuf_concepts, "flores-shuffled", shuf_seq)


if __name__ == "__main__":
    main()
