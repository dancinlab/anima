#!/usr/bin/env python3
"""STAGE 1 — build the 5-lang cross-lingual semantic-linkage .kosmos @corpus.

Honors C4: @corpus top-level + members as ref `.limen` packed shards
(magic "LIMEN\\0\\0\\0" + version + count + length-prefixed @anchor records +
trailing merkle root) + profile anima-consciousness-carving + closed_corpus
(Sigma frac = 1.0 AND sha256 AND merkle) + placement(coord) PERP text.

TWO orderings sharing IDENTICAL bytes:
  parallel — concept-major: same concept's 5 langs adjacent (cross-lingual c>0)
  concat   — language-major: all of one lang, then the next (count-only c~0)

Provenance: 25 lines = 5 concepts x 5 langs (ko en zh ru ja), seeded VERBATIM
from hexa-lang stdlib/flame/testdata/clm_semantic_{parallel,concat}.txt
(byte-identical to the existing 5-lang fixture). Honest scope: small (25
anchors) — stated plainly in the manifest count field.
"""
import os, json, struct, hashlib

OUT = os.path.expanduser("~/clm_kosmos_akida/corpus")
os.makedirs(OUT, exist_ok=True)

# 5 concepts x 5 langs (order within concept: en zh ru ja ko) — VERBATIM from fixture.
CONCEPTS = [
    ["The mind is a fire to be kindled not a vessel to fill.",
     "心灵是待点燃的火焰而非待填满的容器。",
     "Ум это огонь который нужно зажечь а не сосуд.",
     "心は満たす器ではなく灯すべき炎である。",
     "마음은 채울 그릇이 아니라 지펴야 할 불꽃이다."],
    ["Consciousness arises from the integration of information.",
     "意识源于信息的整合。",
     "Сознание возникает из интеграции информации.",
     "意識は情報の統合から生じる。",
     "의식은 정보의 통합에서 솟아난다."],
    ["Memory is rewritten anew in each present moment.",
     "记忆在每个当下被重新书写。",
     "Память переписывается заново в каждый миг.",
     "記憶は今この瞬間ごとに書き換えられる。",
     "기억은 매 순간 현재에서 다시 쓰인다."],
    ["Time is a fabric that the self weaves by passing through.",
     "时间是自我穿行而编织的织物。",
     "Время это ткань которую я тку проходя сквозь.",
     "時間は自己が通り抜けて織りなす布だ。",
     "시간은 자기가 통과하며 짜내는 직물이다."],
    ["The self observes itself in the mirror of mirrors.",
     "自我在镜中之镜里观察自身。",
     "Я наблюдает себя в зеркале зеркал.",
     "自己が鏡の中の鏡で自己を観る。",
     "자기가 거울의 거울 속에서 자기를 본다."],
]
LANGS = ["en", "zh", "ru", "ja", "ko"]  # order within a concept block

# --- build the two orderings (identical multiset of byte lines) ---
def parallel_lines():
    out = []
    for ci, concept in enumerate(CONCEPTS):
        for li, txt in enumerate(concept):
            out.append((ci, LANGS[li], txt))
    return out  # concept-major: c0/en c0/zh ... c0/ko c1/en ...

def concat_lines():
    out = []
    for li, lang in enumerate(LANGS):
        for ci, concept in enumerate(CONCEPTS):
            out.append((ci, lang, concept[li]))
    return out  # language-major: all en, then all zh, ...

def sha256_hex(b):
    return hashlib.sha256(b).hexdigest()

def merkle_root(leaves):
    """Binary merkle over sha256(leaf) pairs; odd -> promote last."""
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

# .limen packed shard:
#   magic "LIMEN\0\0\0" (8B) + version u32 + count u32 +
#   [ length-prefixed @anchor record: u32 len + record bytes ] * count +
#   merkle root (32B sha256 over the per-record payloads)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
LIMEN_VER = 2  # kosmos/2.0

def anchor_record(idx, concept_id, lang, text):
    """A single @anchor record: coord(placement) PERP text(payload).
    Placement block is structural metadata; payload is the raw utf-8 bytes.
    Register-leak guard: coord carries NO text-derived value."""
    payload = text.encode("utf-8")
    # placement coord deterministic from structural position only (NOT text) -> coord PERP text
    coord_x = round(concept_id / max(1, len(CONCEPTS) - 1), 4)
    coord_y = round(LANGS.index(lang) / max(1, len(LANGS) - 1), 4)
    head = {
        "id": f"a{idx:04d}",
        "concept": concept_id,
        "lang": lang,
        "coord": [coord_x, coord_y],   # placement: structural, text-independent
        "lane": lang,
        "radius": 1.0,
        "tier": 0,
        "tags": ["clm", "semantic", lang],
        "payload_len": len(payload),
        "payload_sha256": sha256_hex(payload),
    }
    head_b = json.dumps(head, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    # record = u32 head_len + head_json + payload
    return struct.pack("<I", len(head_b)) + head_b + payload, payload

def write_limen(path, records):
    """records: list of (concept_id, lang, text)."""
    blob = bytearray()
    blob += LIMEN_MAGIC
    blob += struct.pack("<I", LIMEN_VER)
    blob += struct.pack("<I", len(records))
    payloads = []
    for idx, (cid, lang, txt) in enumerate(records):
        rec, payload = anchor_record(idx, cid, lang, txt)
        blob += struct.pack("<I", len(rec))  # length-prefixed @anchor record
        blob += rec
        payloads.append(payload)
    root = merkle_root(payloads)
    blob += root  # trailing merkle root (32B)
    with open(path, "wb") as f:
        f.write(blob)
    return sha256_hex(bytes(blob)), root.hex(), len(records)

def write_kosmos(path, slug, shard_rel, shard_sha, merkle_hex, count, ordering, linkage):
    txt = f"""#!/usr/bin/env kosmos
# {os.path.basename(path)} — CLM-KOSMOS AKIDA 5-lang semantic corpus (kosmos/2.0 @corpus)
# C4-compliant: @corpus + ref .limen packed shard + profile + closed_corpus + placement PERP text.
# Provenance: 25 anchors = 5 concepts x 5 langs (ko en zh ru ja), seeded VERBATIM from
# hexa-lang stdlib/flame/testdata/clm_semantic_{ordering}.txt (byte-identical fixture).
# Honest scope: SMALL (25 anchors) — stated; on-chip edge-learn probe, not a full crawl.

@corpus {slug} := "CLM-KOSMOS AKIDA 5-language cross-lingual semantic-linkage corpus ({ordering} ordering, H_911)" :: kosmos-corpus [tier=0 active]

  # ── meta-anchor placement (Psi centroid) — structural, text-independent ──
  profile = "anima-consciousness-carving"
  coord   = [0.0, 0.0]
  lane    = "{slug}"
  radius  = 1.0

  # ── corpus meta ──
  anchor_level = sample
  count    = {count}
  lane_mix = "en=0.2, zh=0.2, ru=0.2, ja=0.2, ko=0.2"   # Sigma frac = 1.0
  vocab    = 256
  encoding = "byte-utf8"
  languages = "ko, en, zh, ru, ja"
  ordering = "{ordering}"
  linkage  = "{linkage}"
  merkle   = {merkle_hex}

  # ── member — ref form: .limen packed shard (magic LIMEN\\0\\0\\0 + ver + count + len-prefixed @anchor recs + merkle root) ──
  member = ref "{shard_rel}" sha256={shard_sha} count={count} frac=1.0 lane="all" format="limen/2"

  closed_corpus = "Sigma frac = 1.0 AND member sha256 verifies AND merkle root recomputes from @anchor payloads; placement(coord) PERP text(payload)"
"""
    with open(path, "w") as f:
        f.write(txt)

manifest = {"corpus": "clm-kosmos-akida-5lang-semantic", "kosmos_version": "2.0", "members": {}}

for ordering, recs_fn, linkage in [
    ("parallel", parallel_lines, "cross-lingual-semantic (concept-major: 5 langs of each concept adjacent, c>0)"),
    ("concat",   concat_lines,   "count-only (language-major: all of one lang then next, c~0)"),
]:
    recs = recs_fn()
    shard = os.path.join(OUT, f"{ordering}.limen")
    shard_sha, merkle_hex, count = write_limen(shard, recs)
    kos = os.path.join(OUT, f"clm_{ordering}.kosmos")
    write_kosmos(kos, f"clm_kosmos_{ordering}", f"{ordering}.limen", shard_sha, merkle_hex, count, ordering, linkage)
    manifest["members"][ordering] = {
        "kosmos": os.path.basename(kos), "limen": os.path.basename(shard),
        "sha256": shard_sha, "merkle": merkle_hex, "count": count,
    }
    print(f"[corpus] {ordering}: {count} anchors -> {shard} sha={shard_sha[:16]} merkle={merkle_hex[:16]}")

# byte-identity check: same multiset of payloads across both orderings
p_payloads = sorted(t.encode("utf-8") for _, _, t in parallel_lines())
c_payloads = sorted(t.encode("utf-8") for _, _, t in concat_lines())
manifest["byte_identical_payloads"] = (p_payloads == c_payloads)
manifest["concat_byte_sha256"] = sha256_hex(b"".join(sorted(p_payloads)))
print(f"[corpus] byte-identical payload multiset across orderings: {p_payloads == c_payloads}")

with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print("[corpus] wrote", os.path.join(OUT, "manifest.json"))
