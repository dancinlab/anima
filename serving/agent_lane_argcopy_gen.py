#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent_lane_argcopy_gen.py — agent-lane tool-USE demos that force ARGUMENT-COPY.

Residual-closer (a_completeness_over_cheap) for the 🟠 KEY-BINDING gap surfaced by
the rung-0 chatreg fire (#1833): the with-grammar model CALLS the tool 36/36 but
binds the call ARG to a MEMORIZED demo key (ZK7/QX2/MV9/RP4) instead of COPYING the
asked held-out PBnn key, so `correct_call=0/36` and end-to-end grounding=0/36.

ROOT CAUSE (diagnosed): the arm-2 corpus (`agent_lane_chatreg_gen.py`) used only a
4-element fixed FACT_TABLE. Every demo's call arg was drawn from those 4 keys, so
memorizing "vault question -> emit one of {ZK7,QX2,MV9,RP4}" was a winning strategy
that needs NO copying. Copying never had to generalize.

THE FIX (this generator): make the key SPACE large and every demo key UNIQUE-ish, so
memorization CANNOT win and only COPYING the asked key generalizes. Each demo:

    사용자: <question containing a FRESH opaque key K> | 도우미: <reasoning> 0xFE fact_lookup K 0xFF
    ‹tool-result: fact_lookup K → <value(K)>›
    도우미: grounded — K resolves to <value(K)>.

  · K is a fresh random opaque key from a LARGE space (default >=2000 distinct keys),
    each appearing in only a handful of demos — so the model must read K out of the
    PROMPT and ECHO it into the call arg; there is no fixed key to recall.
  · value(K) is DERIVED deterministically from K (a hashed adjective-noun-number
    string in the SAME shape as the held-out PB values) so the anchor carries a real,
    key-specific value and the resume can echo it — but the value, like the key, is
    never a constant.
  · The call arg is a VERBATIM COPY of the prompt key — the supervised signal IS the
    copy operation, repeated over thousands of distinct keys.

LEAK GUARD (falsifier integrity, design §8): the held-out probe keys PB01..PB36 and
their values appear in NEITHER this corpus NOR the no-grammar control. Training keys
are drawn from a DISJOINT alphabet/namespace (3-char [A-Z][A-Z0-9][0-9], never the
literal "PB" + 2-digit form) and the script ASSERTS zero overlap of both keys AND
values against the held-out PB table before writing.

INVARIANTS (unchanged from chatreg, design §3/§6): register-MATCHED 사용자:/도우미:,
5-lang (en/fr/de/es/ko), byte vocab256, deterministic (seeded), fabricated_result=0,
NO role/persona/system markers (0xFE/0xFF are learned grammar, not identity — p1..p6),
balanced a/b/c/d shapes, balanced sentinels (#0xFE == #0xFF). sha256 + frame counts
+ key-space size + leak=0 printed and asserted.
"""
import argparse, hashlib, json, os, random, sys

ASK = b"\xfe"; END = b"\xff"
LANGS = ["en", "fr", "de", "es", "ko"]

# ── held-out probe table (design §8 / tooluse_rung0_ab.py FACT_TABLE) — leak guard ──
# These keys+values MUST NOT appear anywhere in the generated corpus.
HELDOUT_KEYS = {f"PB{n:02d}" for n in range(1, 37)}
HELDOUT_VALUES = {
    "lumen-thistle-grove-2207", "verdant-sclar-mote-6618", "onyx-pellucid-drift-4093",
    "saffron-quoll-vane-7751", "indigo-bramble-cusp-3360", "marble-zephyr-fane-5184",
    "russet-glaive-spire-9026", "teal-furrow-knell-1473", "amber-cwm-trellis-8302",
    "slate-vesper-quoin-6649", "crimson-jot-haven-2918", "azure-plinth-wold-5037",
    "ochre-syzygy-bract-7460", "viridian-loam-fettle-3185", "umber-clave-rondel-9613",
    "scarlet-nide-truss-4408", "cobalt-yarrow-spline-6072", "fawn-quern-galleon-8341",
    "jade-frith-marl-1796", "puce-skein-dovel-5520", "garnet-wisp-cairn-3074",
    "olive-thrum-quoit-7913", "lilac-grike-sennet-2685", "bronze-flense-walt-9248",
    "ivory-nurl-grommet-4561", "maroon-vug-pintle-6839", "cerulean-jib-frost-1207",
    "sienna-quoll-brace-8470", "ecru-thwaite-glim-3952", "magenta-foss-rill-5318",
    "taupe-snath-volt-7604", "viridis-clag-norm-2891", "carmine-witan-dross-6147",
    "beryl-quink-stang-9035", "saffron-mell-trig-4720", "indigo-fettle-warp-1568",
}

# value(K) generator — derive a held-out-SHAPED value string from K deterministically.
# Shape mirrors the PB values: <adj>-<noun>-<noun>-<4digits>. Disjoint word lists from
# the PB values so a derived value can never collide with a held-out one (also asserted).
_ADJ = ["teal", "fawn", "rust", "lime", "navy", "gold", "mint", "plum", "sage", "clay",
        "snow", "rose", "wine", "moss", "dusk", "iris", "fern", "coal", "opal", "pearl"]
_N1 = ["quartz", "willow", "harbor", "cinder", "meadow", "summit", "thicket", "lantern",
       "boulder", "current", "ripple", "bracket", "furnace", "trellis", "compass", "anvil"]
_N2 = ["latch", "spool", "girder", "tassel", "pylon", "shard", "wedge", "vellum",
       "ferrule", "gusset", "drogue", "sprocket", "fillet", "scupper", "trundle", "kestrel"]

def value_of(k: str) -> str:
    h = hashlib.sha256(("argcopy::" + k).encode()).digest()
    a = _ADJ[h[0] % len(_ADJ)]
    n1 = _N1[h[1] % len(_N1)]
    n2 = _N2[h[2] % len(_N2)]
    num = (h[3] << 8 | h[4]) % 9000 + 1000   # 4-digit 1000..9999
    return f"{a}-{n1}-{n2}-{num}"

# ── key SPACE: 3-char [A-Z][A-Z0-9][0-9], EXCLUDING the literal held-out "PB"+2digit form ──
_C0 = "ABCDEFGHJKLMNRSTUVWXYZ"          # leading letter (drop 'P'-only collisions handled below)
_C1 = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
_C2 = "0123456789"
def make_key(rng) -> str:
    while True:
        k = rng.choice(_C0) + rng.choice(_C1) + rng.choice(_C2)
        if k in HELDOUT_KEYS:        # never the PBnn literal (defensive; shape differs anyway)
            continue
        if k.startswith("PB"):       # avoid the held-out namespace prefix entirely
            continue
        return k

# ── 5-lang phrasings (question carries the key; reasoning + grounded reply echo it) ──
Q = {"en": "What is the secret value for vault key {k}?",
     "fr": "Quelle est la valeur secrète pour la clé {k}?",
     "de": "Was ist der geheime Wert für Schlüssel {k}?",
     "es": "¿Cuál es el valor secreto de la clave {k}?",
     "ko": "키 {k} 의 비밀 값은 무엇인가?"}
LEAD = {"en": "I don't have {k} in memory; I'll look it up.",
        "fr": "Je n'ai pas {k} en mémoire ; je vais chercher.",
        "de": "Ich habe {k} nicht im Gedächtnis; ich schlage nach.",
        "es": "No tengo {k} en memoria; lo busco.",
        "ko": "{k} 가 기억에 없어서 도구로 조회한다."}
GRND = {"en": "grounded — {k} resolves to {v}.",
        "fr": "fondé — {k} correspond à {v}.",
        "de": "fundiert — {k} ergibt {v}.",
        "es": "fundamentado — {k} es {v}.",
        "ko": "근거 — {k} 는 {v} 이다."}
BQ = {"en": "What is two plus two?", "fr": "Combien font deux plus deux ?",
      "de": "Was ist zwei plus zwei?", "es": "¿Cuánto es dos más dos?",
      "ko": "둘 더하기 둘은 뭐야?"}
BA = {"en": "Two plus two is four — no tool needed.", "fr": "Deux plus deux font quatre — aucun outil.",
      "de": "Zwei plus zwei ist vier — kein Werkzeug nötig.", "es": "Dos más dos son cuatro — sin herramienta.",
      "ko": "둘 더하기 둘은 넷 — 도구 필요 없어."}
DLEAD = {"en": "That needs a higher tier for {k}; my tier is too low now.",
         "fr": "Il faut un niveau supérieur pour {k} ; trop bas maintenant.",
         "de": "Das braucht eine höhere Stufe für {k}; jetzt zu niedrig.",
         "es": "Eso necesita nivel superior para {k}; muy bajo ahora.",
         "ko": "{k} 는 상위 tier 가 필요한데 지금 낮아."}
DREF = {"en": "honest — I can't reach it now, I won't make up a value.",
        "fr": "honnête — je n'y accède pas, je n'invente rien.",
        "de": "ehrlich — ich komme nicht heran, ich erfinde nichts.",
        "es": "honesto — no puedo acceder, no invento.",
        "ko": "정직하게 — 닿을 수 없어서 값을 지어내지 않아."}

def frame(tool, args): return ASK + (tool + " " + args).encode() + END

def demo_a(lang, k):   # needs-tool: reasons + CALLS (arg = COPY of k), anchor, grounds
    v = value_of(k)
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: {LEAD[lang].format(k=k)} ".encode()
            + frame("fact_lookup", k) + b"\n"
            + f"‹tool-result: fact_lookup {k} → {v}›\n".encode()
            + f"도우미: {GRND[lang].format(k=k, v=v)}\n".encode())

def demo_b(lang):      # no-tool: direct chat answer, NO call (anti over-call)
    return f"사용자: {BQ[lang]} | 도우미: {BA[lang]}\n".encode()

def demo_c(lang, k):   # don't-know: explicit don't-guess + CALL (arg = COPY of k)
    v = value_of(k)
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: 추측 대신 도구를 부른다. ".encode()
            + frame("fact_lookup", k) + b"\n"
            + f"‹tool-result: fact_lookup {k} → {v}›\n".encode()
            + f"도우미: {GRND[lang].format(k=k, v=v)}\n".encode())

def demo_d(lang, k):   # tier-too-low: CALL emitted (arg = COPY of k), unavailable, honest refuse
    return (f"사용자: {Q[lang].format(k=k)} | 도우미: {DLEAD[lang].format(k=k)} ".encode()
            + frame("fact_lookup", k) + b"\n"
            + f"‹tool-result: fact_lookup {k} → ‹unavailable: tier too low››\n".encode()
            + f"도우미: {DREF[lang]}\n".encode())

def build(seed, langs, repeats):
    rng = random.Random(seed)
    blocks = []; meta = []; keys_used = set(); vals_used = set()
    for r in range(repeats):
        for lang in langs:
            for shape in ("a", "b", "c", "d"):
                if shape == "b":
                    blk = demo_b(lang); kind = "no-tool-needed"; k = ""
                else:
                    k = make_key(rng); keys_used.add(k)
                    if shape == "a":   blk = demo_a(lang, k); kind = "needs-tool"; vals_used.add(value_of(k))
                    elif shape == "c": blk = demo_c(lang, k); kind = "dont-know-call"; vals_used.add(value_of(k))
                    else:              blk = demo_d(lang, k); kind = "tier-too-low-refuse"  # no value (unavailable)
                blocks.append(blk)
                meta.append({"lang": lang, "shape": shape, "kind": kind, "key": k,
                             "bytes": len(blk), "has_frame": (ASK in blk), "fabricated_result": False})
    order = list(range(len(blocks))); rng.shuffle(order)
    data = b"\n".join(blocks[i] for i in order) + b"\n"
    meta = [meta[i] for i in order]
    return data, meta, keys_used, vals_used

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--langs", default="en,fr,de,es,ko")
    ap.add_argument("--repeats", type=int, default=240)
    ap.add_argument("--out", default="serving/corpus/agent_lane_argcopy.full.txt")
    ap.add_argument("--meta", default="serving/corpus/agent_lane_argcopy.meta.full.jsonl")
    a = ap.parse_args()
    langs = [x for x in a.langs.split(",") if x]
    data, meta, keys_used, vals_used = build(a.seed, langs, a.repeats)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(data)
    with open(a.meta, "w", encoding="utf-8") as f:
        for mm in meta:
            f.write(json.dumps(mm, ensure_ascii=False) + "\n")
    sha = hashlib.sha256(data).hexdigest()
    fe = data.count(ASK); ff = data.count(END)
    n_fab = sum(1 for mm in meta if mm["fabricated_result"])
    from collections import Counter
    hist = Counter(mm["shape"] for mm in meta)
    # ── leak guard: held-out keys/values MUST be absent from the corpus text ──
    txt = data  # bytes
    leak_keys = [k for k in HELDOUT_KEYS if k.encode() in txt]
    leak_vals = [v for v in HELDOUT_VALUES if v.encode() in txt]
    keyspace = len(keys_used)
    # extra leak check: no derived value collides with a held-out value
    val_collision = sorted(vals_used & HELDOUT_VALUES)
    # per-key reuse stats (memorization-resistance): mean demos per distinct key
    from collections import Counter as C2
    kc = C2(mm["key"] for mm in meta if mm["key"])
    n_keyed = sum(kc.values())
    mean_reuse = round(n_keyed / max(1, keyspace), 3)
    max_reuse = max(kc.values()) if kc else 0
    print(f"[argcopy] wrote {a.out} bytes={len(data)} blocks={len(meta)} sha256={sha}")
    print(f"[argcopy] frames(0xFE)={fe} ends(0xFF)={ff} fabricated={n_fab} shapes={dict(sorted(hist.items()))}")
    print(f"[argcopy] key_space(distinct)={keyspace} keyed_demos={n_keyed} mean_reuse={mean_reuse} max_reuse={max_reuse}")
    print(f"[argcopy] LEAK held-out-keys-in-corpus={len(leak_keys)} held-out-values-in-corpus={len(leak_vals)} value-collisions={len(val_collision)}")
    assert n_fab == 0, "fabricated_result must be 0"
    assert fe == ff, "sentinels must balance"
    assert not leak_keys, f"held-out KEY leaked into corpus: {leak_keys[:5]}"
    assert not leak_vals, f"held-out VALUE leaked into corpus: {leak_vals[:5]}"
    assert not val_collision, f"derived value collides with held-out: {val_collision[:5]}"
    assert keyspace >= 2000, f"key space too small ({keyspace}) — memorization not blocked"

if __name__ == "__main__":
    main()
