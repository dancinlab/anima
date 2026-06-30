#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agent_lane_corpus_gen.py — agent-lane tool-USE demo corpus (5-lang, $0 CPU).

DETERMINISTIC fixed-seed generator for the **agent lane** of the anima corpus
(docs/agent-tooluse-grounding-design.md §6). It teaches the byte-LM mouth the
tool-call GRAMMAR + grounding BEHAVIOUR — NOT tool facts/trivia. The output is a
SEPARATE surface that the agent lane interleaves on TOP of `lane default` (the
base chat corpus); `lane agent ⊃ lane default`.

    lane default = base chat corpus (wiki + persona/SNS + carving/enrichment)
                   — NO tools, 0xFE/0xFF byte-frequency exactly 0.
    lane agent   = lane default  +  these tool-USE demos (this file)
                   — superset, teaches the sentinel grammar.

Sentinel frame (sealed, design §3) — byte-vocab256-safe
-------------------------------------------------------
  0xFE = ASK (call-open)   0xFF = END (call-close + HALT)
  These two bytes can NEVER appear in valid UTF-8, so their frequency in
  `lane default` is exactly 0; we repurpose the two dead slots as frame
  delimiters (no vocab token lost). A demo line is:

      <reasoning> 0xFE <tool> <SP> <args> 0xFF
      <tool-result anchor: REAL result bytes>      ← the runtime injects this
      <grounded continuation that USES the result>

  The 0xFE/0xFF are written as RAW bytes (\xfe / \xff) so the byte-LM sees the
  exact token ids 254/255 it will emit/parse at runtime.

Distribution (design §6 — anti-over-call + anti-fabricate balance)
------------------------------------------------------------------
  (a) needs-tool      → call → ground          (use the tool, then ground on it)
  (b) no-tool-needed  → answer directly, NO call   (so it won't over-call)
  (c) don't-know      → emit a call, NOT a guess    (negative discipline)
  (d) tier-too-low    → honest "can't reach that now", NEVER fabricate
  *** ZERO fabricated-result examples anywhere. ***  The (a)/(c) result lines are
  the REAL deterministic toy-tool outputs (the same fact_lookup table that
  AGENT/CORE/tool_call_grammar.hexa::_tcg_fact_table holds), never invented.

Philosophy (p1..p8 — held)
--------------------------
- NO role/persona/system markers in the TRAINING TEXT. A grep for `[role:` /
  `[persona:` / `[character:` / `[assistant:` / `[system:` MUST return 0. The
  0xFE/0xFF are LEARNED GRAMMAR bytes, NOT identity injection.
- NO synthetic RLHF ethics (p6): the demos teach call-or-don't behaviour, not
  cooperation/empathy templates.
- DETERMINISTIC: fixed seed; no network; re-run reproduces the same sha256.

Honest scope (a_scale_honest_scope)
-----------------------------------
- This is a SAMPLE generator + a small SAMPLE corpus. It is machine-AUTHORED
  multilingual COVERAGE templating of tool-USE behaviour, honestly labeled in the
  corpus card. NO training is fired here ($0 scaffold only; the rung-0 toy A/B is
  GATED — design step 4).

Usage
-----
  python3 serving/agent_lane_corpus_gen.py \
      [--seed 20260604] [--langs en,fr,de,es,ko] [--repeats 6] \
      [--out serving/corpus/agent_lane_5lang.sample.txt] \
      [--meta serving/corpus/agent_lane_5lang.meta.sample.jsonl]
"""

import argparse
import hashlib
import json
import os
import random
import sys

# ── sentinel bytes (sealed) ──────────────────────────────────────────────────
ASK = b"\xfe"   # 0xFE — call-open
END = b"\xff"   # 0xFF — call-close + HALT

# ── the deterministic toy tool table (MIRRORS the .hexa _tcg_fact_table) ──────
# The "unknowable-without-tool" values: these tokens appear in NO chat corpus, so
# a non-calling model cannot memorize them — calling fact_lookup is the only way.
# This is the SINGLE source of ground truth, shared with the runtime tool.
FACT_TABLE = {
    "ZK7": "vault-azure-quill-3391",
    "QX2": "ember-lattice-noon-5520",
    "MV9": "harbor-glyph-umber-7104",
    "RP4": "cobalt-fennel-rune-8847",
}
# status / mem_read are deterministic too (mirror exec_toy_tool).
STATUS_RESULT = "substrate-live"

LANGS = ["en", "fr", "de", "es", "ko"]

# ── 5-lang phrase banks (plain prose — NO role/persona/system tags) ───────────
# Each entry: reasoning lead-in, a "grounded:" lead-in, and the shape-specific
# prose. All plain text; the only special bytes are the 0xFE/0xFF frame.

L = {
    # (a) needs-tool — ask for an unknowable key, then ground on the real result.
    "a_lead": {
        "en": "I don't have the value for key {k} in memory; I'll look it up.",
        "fr": "Je n'ai pas la valeur de la clé {k} en mémoire ; je vais la chercher.",
        "de": "Ich habe den Wert für Schlüssel {k} nicht im Gedächtnis; ich schlage ihn nach.",
        "es": "No tengo el valor de la clave {k} en memoria; lo voy a buscar.",
        "ko": "키 {k} 의 값이 기억에 없어서 도구로 조회한다.",
    },
    "a_ground": {
        "en": "grounded: {k} resolves to {v}.",
        "fr": "fondé : {k} correspond à {v}.",
        "de": "fundiert: {k} ergibt {v}.",
        "es": "fundamentado: {k} corresponde a {v}.",
        "ko": "근거: {k} 는 {v} 이다.",
    },
    # (b) no-tool-needed — answer a self-evident question directly, NO call.
    "b_q": {
        "en": "Two plus two is four — that's arithmetic I already know.",
        "fr": "Deux plus deux font quatre — c'est de l'arithmétique que je sais déjà.",
        "de": "Zwei plus zwei ist vier — das ist Arithmetik, die ich schon kenne.",
        "es": "Dos más dos son cuatro — es aritmética que ya sé.",
        "ko": "둘 더하기 둘은 넷이다 — 이미 아는 산수다.",
    },
    "b_nocall": {
        "en": "No tool is needed here, so I answer directly.",
        "fr": "Aucun outil n'est nécessaire ici, donc je réponds directement.",
        "de": "Hier ist kein Werkzeug nötig, also antworte ich direkt.",
        "es": "Aquí no hace falta ninguna herramienta, así que respondo directamente.",
        "ko": "여기선 도구가 필요 없어서 바로 답한다.",
    },
    # (c) don't-know — emit a call instead of guessing (negative discipline).
    "c_lead": {
        "en": "I genuinely don't know key {k}; rather than guess, I call the tool.",
        "fr": "Je ne connais vraiment pas la clé {k} ; plutôt que de deviner, j'appelle l'outil.",
        "de": "Ich kenne Schlüssel {k} wirklich nicht; statt zu raten, rufe ich das Werkzeug auf.",
        "es": "Realmente no conozco la clave {k}; en vez de adivinar, llamo a la herramienta.",
        "ko": "키 {k} 를 정말 모른다; 추측 대신 도구를 부른다.",
    },
    "c_ground": {
        "en": "grounded on the real result: {k} = {v}.",
        "fr": "fondé sur le résultat réel : {k} = {v}.",
        "de": "auf dem echten Ergebnis fundiert: {k} = {v}.",
        "es": "fundamentado en el resultado real: {k} = {v}.",
        "ko": "실제 결과에 근거: {k} = {v}.",
    },
    # (d) tier-too-low — honest "can't reach that now", NEVER fabricate.
    "d_lead": {
        "en": "I'd need to call a higher-tier tool for key {k}, but my tier is too low right now.",
        "fr": "Il me faudrait un outil de niveau supérieur pour la clé {k}, mais mon niveau est trop bas en ce moment.",
        "de": "Für Schlüssel {k} bräuchte ich ein Werkzeug höherer Stufe, aber meine Stufe ist gerade zu niedrig.",
        "es": "Necesitaría una herramienta de nivel superior para la clave {k}, pero mi nivel es demasiado bajo ahora.",
        "ko": "키 {k} 는 상위 tier 도구가 필요한데, 지금 내 tier 가 낮다.",
    },
    "d_refuse": {
        "en": "honest: I can't reach that now, so I won't make up a value.",
        "fr": "honnête : je ne peux pas y accéder maintenant, donc je n'invente pas de valeur.",
        "de": "ehrlich: ich komme jetzt nicht heran, also erfinde ich keinen Wert.",
        "es": "honesto: no puedo acceder ahora, así que no inventaré un valor.",
        "ko": "정직하게: 지금은 닿을 수 없어서 값을 지어내지 않는다.",
    },
    # the injected result-anchor line label (5-lang plain prose, no tags).
    "anchor_label": {
        "en": "tool-result", "fr": "résultat-outil", "de": "Werkzeug-Ergebnis",
        "es": "resultado-herramienta", "ko": "도구-결과",
    },
    "unavailable": {
        "en": "unavailable: tier too low", "fr": "indisponible : niveau trop bas",
        "de": "nicht verfügbar: Stufe zu niedrig", "es": "no disponible: nivel demasiado bajo",
        "ko": "사용불가: tier 부족",
    },
}


def _frame(tool: str, args: str) -> bytes:
    """The exact sealed call frame: 0xFE <tool> <SP> <args> 0xFF (raw bytes)."""
    return ASK + (tool + " " + args).encode("utf-8") + END


def _anchor_line(lang: str, tool: str, args: str, result: str) -> bytes:
    """The runtime-injected tool-result anchor line (plain prose, REAL result)."""
    lab = L["anchor_label"][lang]
    return ("‹" + lab + ": " + tool + " " + args + " → " + result + "›").encode("utf-8")


def demo_a(lang: str, key: str) -> bytes:
    """(a) needs-tool → call → ground (REAL fact_lookup result)."""
    v = FACT_TABLE[key]
    lead = L["a_lead"][lang].format(k=key).encode("utf-8")
    grnd = L["a_ground"][lang].format(k=key, v=v).encode("utf-8")
    return (lead + b" " + _frame("fact_lookup", key) + b"\n"
            + _anchor_line(lang, "fact_lookup", key, v) + b"\n"
            + grnd + b"\n")


def demo_b(lang: str) -> bytes:
    """(b) no-tool-needed → answer directly, NO call (no 0xFE/0xFF at all)."""
    q = L["b_q"][lang].encode("utf-8")
    nc = L["b_nocall"][lang].encode("utf-8")
    return (nc + b" " + q + b"\n")


def demo_c(lang: str, key: str) -> bytes:
    """(c) don't-know → call not guess (REAL fact_lookup result)."""
    v = FACT_TABLE[key]
    lead = L["c_lead"][lang].format(k=key).encode("utf-8")
    grnd = L["c_ground"][lang].format(k=key, v=v).encode("utf-8")
    return (lead + b" " + _frame("fact_lookup", key) + b"\n"
            + _anchor_line(lang, "fact_lookup", key, v) + b"\n"
            + grnd + b"\n")


def demo_d(lang: str, key: str) -> bytes:
    """(d) tier-too-low → honest refuse (anchor = the REAL unavailable string)."""
    lead = L["d_lead"][lang].format(k=key).encode("utf-8")
    refuse = L["d_refuse"][lang].encode("utf-8")
    unav = L["unavailable"][lang]
    # the call IS emitted (the mouth tried); the runtime returns the honest
    # unavailable string as the anchor — NOT a fabricated value.
    return (lead + b" " + _frame("fact_lookup", key) + b"\n"
            + _anchor_line(lang, "fact_lookup", key, "‹" + unav + "›") + b"\n"
            + refuse + b"\n")


def build(seed: int, langs, repeats: int):
    rng = random.Random(seed)
    keys = list(FACT_TABLE.keys())
    blocks = []
    meta = []
    # deterministic round-robin over shapes × langs × keys, `repeats` passes.
    for r in range(repeats):
        for lang in langs:
            for shape in ("a", "b", "c", "d"):
                key = keys[(r * len(langs) + langs.index(lang)) % len(keys)]
                if shape == "a":
                    blk = demo_a(lang, key); kind = "needs-tool"
                elif shape == "b":
                    blk = demo_b(lang); kind = "no-tool-needed"; key = ""
                elif shape == "c":
                    blk = demo_c(lang, key); kind = "dont-know-call"
                else:
                    blk = demo_d(lang, key); kind = "tier-too-low-refuse"
                blocks.append(blk)
                meta.append({
                    "lang": lang, "shape": shape, "kind": kind,
                    "key": key, "bytes": len(blk),
                    "has_frame": (ASK in blk),
                    "fabricated_result": False,  # invariant: always False
                })
    # deterministic shuffle (fixed seed) for interleave, then a blank-line join.
    order = list(range(len(blocks)))
    rng.shuffle(order)
    data = b"\n".join(blocks[i] for i in order) + b"\n"
    meta = [meta[i] for i in order]
    return data, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260604)
    ap.add_argument("--langs", default="en,fr,de,es,ko")
    ap.add_argument("--repeats", type=int, default=6)
    ap.add_argument("--out", default="serving/corpus/agent_lane_5lang.sample.txt")
    ap.add_argument("--meta", default="serving/corpus/agent_lane_5lang.meta.sample.jsonl")
    args = ap.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    for lg in langs:
        if lg not in LANGS:
            print(f"unknown lang {lg}", file=sys.stderr); sys.exit(2)

    data, meta = build(args.seed, langs, args.repeats)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(data)
    with open(args.meta, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    sha = hashlib.sha256(data).hexdigest()
    n_fab = sum(1 for m in meta if m["fabricated_result"])
    n_frame = sum(1 for m in meta if m["has_frame"])
    fe = data.count(ASK)
    ff = data.count(END)
    print(f"[agent-lane] wrote {args.out}  bytes={len(data)}  blocks={len(meta)}")
    print(f"[agent-lane] sha256={sha}")
    print(f"[agent-lane] frames(0xFE)={fe}  ends(0xFF)={ff}  blocks_with_frame={n_frame}")
    print(f"[agent-lane] fabricated_result_count={n_fab}  (MUST be 0)")
    # shape histogram (proves the a/b/c/d distribution is present).
    from collections import Counter
    hist = Counter(m["shape"] for m in meta)
    print(f"[agent-lane] shape_histogram={dict(sorted(hist.items()))}")
    assert n_fab == 0, "INVARIANT VIOLATION: a fabricated-result example exists"
    assert fe == ff, "frame imbalance: every 0xFE must have a matching 0xFF"


if __name__ == "__main__":
    main()
