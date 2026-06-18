#!/usr/bin/env python3
"""H_911 TRAINING-SET BUILDER — 5-language (ko·en·zh·ru·ja) parallel .kosmos corpus.

Scales the canonical 25-anchor reference builder
(.verdicts/clm-akida-multiling-semantic/scripts/build_corpus.py) to a LARGE
real-data set sourced from FLORES-200 (CC-BY-SA-4.0, true 5-way line-aligned
parallel; 997 dev + 1012 devtest = 2009 concepts × 5 langs = 10045 anchors).

Honors C4 (kosmos/2.0): @corpus top-level + members as ref `.limen` packed
shards (magic "LIMEN\\0\\0\\0" + version + count + length-prefixed @anchor
records + trailing merkle root) + profile anima-consciousness-carving +
closed_corpus (Σ frac = 1.0 AND sha256 AND merkle) + placement(coord) PERP text.

TWO orderings sharing IDENTICAL anchor payload bytes (differ ONLY in member
ordering inside the .limen shard):
  parallel — concept-major: the 5 langs of each concept are adjacent (c>0)
  concat   — language-major: all of one language, then the next (c~0)

Provenance is recorded HONESTLY in the manifest: real (FLORES-200) vs synthetic
(claude-CLI gap-fill) counts + ratio. FLORES is true 5-way parallel so the
default build is 100% real; synthetic augmentation is OFF unless --synth-fill N
is passed to top up toward a larger anchor target when real data is exhausted.

Usage:
  build_trainset.py --raw DIR --out DIR --concepts N [--synth-fill M] [--split both]
"""
import os, sys, json, struct, hashlib, argparse, subprocess, time

LANGS = ["en", "zh", "ru", "ja", "ko"]      # order WITHIN a concept block (matches reference)
FLORES = {                                   # our lang -> FLORES-200 code
    "en": "eng_Latn", "zh": "zho_Hans", "ru": "rus_Cyrl",
    "ja": "jpn_Jpan", "ko": "kor_Hang",
}
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
LIMEN_VER = 2                                # kosmos/2.0


def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()


def merkle_root(leaves):
    """Binary merkle over sha256(leaf); odd -> promote last. (verbatim from reference)"""
    layer = [hashlib.sha256(l).digest() for l in leaves]
    if not layer:
        return b"\x00" * 32
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]
            b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    return layer[0]


def load_flores(raw_dir, split):
    """Return list of concepts; each concept = {lang: text} for all 5 langs.
    split in {dev, devtest, both}. Rows are line-aligned across languages."""
    splits = ["dev", "devtest"] if split == "both" else [split]
    concepts = []
    for sp in splits:
        cols = {}
        n = None
        for lg, code in FLORES.items():
            p = os.path.join(raw_dir, f"{code}.{sp}")
            with open(p, encoding="utf-8") as f:
                lines = [ln.rstrip("\n") for ln in f]
            cols[lg] = lines
            n = len(lines) if n is None else min(n, len(lines))
        for i in range(n):
            concepts.append({lg: cols[lg][i] for lg in LANGS})
    return concepts


def synth_concept(idx, claude_bin):
    """Gap-fill ONE 5-lang concept via the subscription claude CLI (NO API key).
    Backoff 30/60/120/240s. Returns {lang:text} or None on persistent failure."""
    prompt = (
        "Output ONLY a single JSON object, no prose, with keys en,zh,ru,ja,ko whose "
        "values are the SAME short declarative sentence (about mind/consciousness/time) "
        "translated faithfully into English, Chinese(simplified), Russian, Japanese, "
        "Korean respectively. The five must be exact translations of one concept."
    )
    for attempt, wait in enumerate([0, 30, 60, 120, 240]):
        if wait:
            time.sleep(wait)
        try:
            r = subprocess.run([claude_bin, "-p"], input=prompt, capture_output=True,
                               text=True, timeout=180)
            out = r.stdout.strip()
            s = out.find("{"); e = out.rfind("}")
            if s >= 0 and e > s:
                obj = json.loads(out[s:e + 1])
                if all(obj.get(lg) for lg in LANGS):
                    return {lg: str(obj[lg]).strip() for lg in LANGS}
        except Exception:
            pass
    return None


def parallel_records(concepts):
    """concept-major: c0/en c0/zh c0/ru c0/ja c0/ko c1/en ... -> (cid, lang, text)."""
    out = []
    for ci, c in enumerate(concepts):
        for lg in LANGS:
            out.append((ci, lg, c[lg]))
    return out


def concat_records(concepts):
    """language-major: all en, then all zh, ... -> (cid, lang, text)."""
    out = []
    for lg in LANGS:
        for ci, c in enumerate(concepts):
            out.append((ci, lg, c[lg]))
    return out


def anchor_record(idx, concept_id, lang, text, n_concepts):
    """A single @anchor record: coord(placement) PERP text(payload).
    coord is structural-position-derived ONLY (register-leak guard)."""
    payload = text.encode("utf-8")
    coord_x = round(concept_id / max(1, n_concepts - 1), 6)
    coord_y = round(LANGS.index(lang) / max(1, len(LANGS) - 1), 6)
    head = {
        "id": f"a{idx:05d}",
        "concept": concept_id,
        "lang": lang,
        "coord": [coord_x, coord_y],
        "lane": lang,
        "radius": 1.0,
        "tier": 0,
        "tags": ["clm", "semantic", lang],
        "payload_len": len(payload),
        "payload_sha256": sha256_hex(payload),
    }
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head_b)) + head_b + payload, payload


def write_limen(path, records, n_concepts):
    blob = bytearray()
    blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER)
    blob += struct.pack("<I", len(records))
    payloads = []
    for idx, (cid, lang, txt) in enumerate(records):
        rec, payload = anchor_record(idx, cid, lang, txt, n_concepts)
        blob += struct.pack("<I", len(rec))
        blob += rec
        payloads.append(payload)
    root = merkle_root(payloads)
    blob += root
    with open(path, "wb") as f:
        f.write(blob)
    return sha256_hex(bytes(blob)), root.hex(), len(records)


KOSMOS_TMPL = """#!/usr/bin/env kosmos
# {fname} — H_911 TRAINING-SET: 5-lang cross-lingual semantic-linkage .kosmos @corpus (kosmos/2.0)
# C4-compliant: @corpus + ref .limen packed shard + profile + closed_corpus + placement PERP text.
# Provenance: {count} anchors = {n_concepts} concepts x 5 langs (ko en zh ru ja).
#   real(FLORES-200, CC-BY-SA-4.0)={n_real_c} concepts ; synthetic(claude-CLI)={n_synth_c} concepts.
# Honest scope: real 5-way line-aligned parallel; ordering differs only in .limen member sequence.

@corpus {slug} := "H_911 training-set — 5-language cross-lingual semantic-linkage corpus ({ordering} ordering)" :: kosmos-corpus [tier=0 active]

  # -- meta-anchor placement (Psi centroid) -- structural, text-independent --
  profile = "anima-consciousness-carving"
  coord   = [0.0, 0.0]
  lane    = "{slug}"
  radius  = 1.0

  # -- corpus meta --
  anchor_level = sample
  count    = {count}
  lane_mix = "en=0.2, zh=0.2, ru=0.2, ja=0.2, ko=0.2"   # Sigma frac = 1.0
  vocab    = 256
  encoding = "byte-utf8"
  languages = "ko, en, zh, ru, ja"
  ordering = "{ordering}"
  linkage  = "{linkage}"
  source   = "FLORES-200 (CC-BY-SA-4.0) real={n_real_c}c + synthetic(claude-CLI)={n_synth_c}c"
  merkle   = {merkle_hex}

  # -- member -- ref form: .limen packed shard --
  member = ref "{shard_rel}" sha256={shard_sha} count={count} frac=1.0 lane="all" format="limen/2"

  closed_corpus = "Sigma frac = 1.0 AND member sha256 verifies AND merkle root recomputes from @anchor payloads; placement(coord) PERP text(payload)"
"""


def write_kosmos(path, **kw):
    with open(path, "w") as f:
        f.write(KOSMOS_TMPL.format(**kw))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--split", default="both", choices=["dev", "devtest", "both"])
    ap.add_argument("--concepts", type=int, default=0, help="cap real concepts (0=all)")
    ap.add_argument("--synth-fill", type=int, default=0, help="add M synthetic concepts via claude CLI")
    ap.add_argument("--claude-bin", default="claude")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    real = load_flores(args.raw, args.split)
    if args.concepts and args.concepts < len(real):
        real = real[:args.concepts]
    n_real_c = len(real)

    synth = []
    if args.synth_fill > 0:
        for i in range(args.synth_fill):
            c = synth_concept(n_real_c + i, args.claude_bin)
            if c:
                synth.append(c)
            # flush-early: persist partial synth so a CLI stall never loses prior work
            with open(os.path.join(args.out, "synth_partial.json"), "w", encoding="utf-8") as f:
                json.dump(synth, f, ensure_ascii=False)
    n_synth_c = len(synth)
    concepts = real + synth
    n_concepts = len(concepts)

    manifest = {
        "corpus": "clm-h911-trainset-5lang-parallel",
        "kosmos_version": "2.0",
        "source": "FLORES-200 (dl.fbaipublicfiles.com/nllb/flores200_dataset.tar.gz)",
        "license": "CC-BY-SA-4.0 (FLORES-200); synthetic gap-fill via subscription claude CLI",
        "split": args.split,
        "concepts_total": n_concepts,
        "concepts_real_flores": n_real_c,
        "concepts_synthetic_claude": n_synth_c,
        "real_fraction": round(n_real_c / n_concepts, 6) if n_concepts else 0.0,
        "anchors_total": n_concepts * 5,
        "members": {},
    }

    for ordering, recs_fn, linkage in [
        ("parallel", parallel_records, "cross-lingual-semantic (concept-major: 5 langs of each concept adjacent, c>0)"),
        ("concat",   concat_records,   "count-only (language-major: all of one lang then next, c~0)"),
    ]:
        recs = recs_fn(concepts)
        shard = os.path.join(args.out, f"{ordering}.limen")
        shard_sha, merkle_hex, count = write_limen(shard, recs, n_concepts)
        kos = os.path.join(args.out, f"clm_{ordering}.kosmos")
        write_kosmos(kos, fname=os.path.basename(kos), slug=f"clm_h911_{ordering}",
                     count=count, n_concepts=n_concepts, n_real_c=n_real_c, n_synth_c=n_synth_c,
                     ordering=ordering, linkage=linkage, shard_rel=f"{ordering}.limen",
                     shard_sha=shard_sha, merkle_hex=merkle_hex)
        manifest["members"][ordering] = {
            "kosmos": os.path.basename(kos), "limen": os.path.basename(shard),
            "sha256": shard_sha, "merkle": merkle_hex, "count": count,
        }
        print(f"[corpus] {ordering}: {count} anchors -> sha={shard_sha[:16]} merkle={merkle_hex[:16]}")

    # byte-identity: same MULTISET of payloads across both orderings
    p_pl = sorted(t.encode("utf-8") for _, _, t in parallel_records(concepts))
    c_pl = sorted(t.encode("utf-8") for _, _, t in concat_records(concepts))
    manifest["byte_identical_payloads"] = (p_pl == c_pl)
    manifest["concat_byte_sha256"] = sha256_hex(b"".join(p_pl))
    print(f"[corpus] byte-identical payload multiset across orderings: {p_pl == c_pl}")

    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"[corpus] real={n_real_c}c synth={n_synth_c}c total={n_concepts}c ({n_concepts*5} anchors) "
          f"real_frac={manifest['real_fraction']}")
    print("[corpus] wrote", os.path.join(args.out, "manifest.json"))


if __name__ == "__main__":
    main()
