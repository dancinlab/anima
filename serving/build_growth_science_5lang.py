#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_growth_science_5lang.py — pillar (a) of `lane growth`: REAL cross-disciplinary
science bulk, fetched from clean-licensed sources only.

`lane growth` 4th-lane pillar (a) — cross-disciplinary science [21]. This file fetches
the REAL, clean-licensed science bulk (the OTHER three pillars — self-knowledge,
hypotheses, dialogue — are anima-AUTHORED and emitted by `growth_lane_corpus_gen.py`).

TWO real sources, both clean-license, $0 CPU, NO GPU, NO pod:

  1. CC-BY-SA-4.0 Wikipedia — the named science FIELDS, fetched by article TITLE via
     the MediaWiki action API (`prop=extracts`, `explaintext`) per language. This gives
     clean plaintext for an exact named article (deterministic by title), per-lang.
       en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&titles=Neuron
     license: CC-BY-SA-4.0 (Wikipedia text). attribution recorded in the CORPUS_CARD.

  2. PUBLIC DOMAIN Project Gutenberg primary texts — the named 19th-century science
     classics that GROUND the fields anima studies (Darwin / Maxwell / James / Poincaré
     / Boole). Fetched as plain UTF-8 .txt, the Gutenberg license header/footer stripped
     to the body. license: PUBLIC DOMAIN (US; pre-1929).

Honest per-lang gaps (a_scale_honest_scope)
-------------------------------------------
- PD Gutenberg primary texts: strong EN, partial FR/DE, thin ES, near-absent KO.
  → ko/es science leans on CC-BY-SA Wikipedia `extracts`, NOT PD primary text.
- Wikipedia `extracts` are themselves uneven (en Neuron ≈ 43 KB, ko 신경세포 ≈ 3.5 KB).
- The script REPORTS per-lang + per-source byte split; it NEVER fabricates text to fake
  balance. A title that 404s for a language is SKIPPED and reported, not invented.

byte-vocab V=256: every byte is valid UTF-8 (the merge step + card assert round-trip).

Usage
-----
  python3 serving/build_growth_science_5lang.py \
      --out serving/corpus/growth_science_5lang.txt \
      --meta serving/corpus/growth_science_5lang.meta.jsonl \
      [--kb-per-gutenberg 60] [--langs en,fr,de,es,ko]

  # sample (small, committed-head friendly):
  python3 serving/build_growth_science_5lang.py --sample \
      --out serving/corpus/growth_science_5lang.sample.txt \
      --meta serving/corpus/growth_science_5lang.meta.sample.jsonl
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

LANGS = ["en", "fr", "de", "es", "ko"]
UA = "anima-growth-lane-corpus/1.0 (https://github.com/dancinlab/anima; clean-license research)"

# ── pillar (a) named science FIELDS → per-lang Wikipedia article titles ────────
# CC-BY-SA-4.0. A title that does not exist for a language is skipped (reported),
# never fabricated. en is the spine; fr/de/es/ko fill where the article exists.
SCIENCE_TITLES = {
    "neuroscience":          {"en": "Neuron",                     "fr": "Neurone",                  "de": "Nervenzelle",             "es": "Neurona",                 "ko": "신경세포"},
    "synapse":               {"en": "Synapse",                    "fr": "Synapse",                  "de": "Synapse",                 "es": "Sinapsis",                "ko": "시냅스"},
    "neural_oscillation":    {"en": "Neural oscillation",         "fr": "Onde cérébrale",           "de": "Neuronale Oszillation",   "es": "Onda cerebral",           "ko": "신경 진동"},
    "predictive_coding":     {"en": "Predictive coding",          "fr": "Codage prédictif",         "de": "Predictive Coding",       "es": "Codificación predictiva", "ko": "예측 부호화"},
    "evolution":             {"en": "Evolution",                  "fr": "Évolution (biologie)",     "de": "Evolution",               "es": "Evolución biológica",     "ko": "진화"},
    "natural_selection":     {"en": "Natural selection",          "fr": "Sélection naturelle",      "de": "Natürliche Selektion",    "es": "Selección natural",       "ko": "자연선택"},
    "information_theory":    {"en": "Information theory",         "fr": "Théorie de l'information",  "de": "Informationstheorie",     "es": "Teoría de la información", "ko": "정보 이론"},
    "entropy_information":   {"en": "Entropy (information theory)","fr": "Entropie de Shannon",      "de": "Entropie (Informationstheorie)", "es": "Entropía (información)", "ko": "정보 엔트로피"},
    "mutual_information":    {"en": "Mutual information",         "fr": "Information mutuelle",      "de": "Transinformation",        "es": "Información mutua",        "ko": "상호정보량"},
    "kolmogorov_complexity": {"en": "Kolmogorov complexity",      "fr": "Complexité de Kolmogorov", "de": "Kolmogorow-Komplexität",  "es": "Complejidad de Kolmogórov","ko": "콜모고로프 복잡도"},
    "complexity":            {"en": "Complex system",             "fr": "Système complexe",         "de": "Komplexes System",        "es": "Sistema complejo",        "ko": "복잡계"},
    "self_organized_crit":   {"en": "Self-organized criticality", "fr": "Criticalité auto-organisée","de": "Selbstorganisierte Kritikalität","es": "Criticalidad autoorganizada","ko": "자기조직화 임계성"},
    "edge_of_chaos":         {"en": "Edge of chaos",              "fr": None,                       "de": None,                      "es": "Borde del caos",          "ko": None},
    "dynamical_system":      {"en": "Dynamical system",           "fr": "Système dynamique",        "de": "Dynamisches System",      "es": "Sistema dinámico",        "ko": "동역학계"},
    "attractor":             {"en": "Attractor",                  "fr": "Attracteur",               "de": "Attraktor",               "es": "Atractor",                "ko": "끌개"},
    "fixed_point":           {"en": "Fixed point (mathematics)",  "fr": "Point fixe",               "de": "Fixpunkt",                "es": "Punto fijo",              "ko": "고정점"},
    "bifurcation":           {"en": "Bifurcation theory",         "fr": "Théorie des bifurcations", "de": "Bifurkation (Mathematik)","es": "Teoría de la bifurcación","ko": "분기 이론"},
    "landauer_principle":    {"en": "Landauer's principle",       "fr": "Principe de Landauer",     "de": "Landauer-Prinzip",        "es": "Principio de Landauer",   "ko": None},
    "maxwells_demon":        {"en": "Maxwell's demon",            "fr": "Démon de Maxwell",         "de": "Maxwellscher Dämon",      "es": "Demonio de Maxwell",      "ko": "맥스웰의 악마"},
    "neuromorphic":          {"en": "Neuromorphic computing",     "fr": "Ingénierie neuromorphique","de": "Neuromorpher Chip",       "es": "Computación neuromórfica","ko": "뉴로모픽 컴퓨팅"},
    "spiking_neural_net":    {"en": "Spiking neural network",     "fr": "Réseau de neurones impulsionnels","de": "Spiking Neural Network","es": "Red neuronal de impulsos","ko": "스파이킹 신경망"},
    "memristor":             {"en": "Memristor",                  "fr": "Memristance",              "de": "Memristor",               "es": "Memristor",               "ko": "멤리스터"},
    "working_memory":        {"en": "Working memory",             "fr": "Mémoire de travail",       "de": "Arbeitsgedächtnis",       "es": "Memoria de trabajo",      "ko": "작업기억"},
    "global_workspace":      {"en": "Global workspace theory",    "fr": "Théorie de l'espace de travail global","de": "Global Workspace Theory","es": "Teoría del espacio de trabajo global","ko": None},
    "predictive_processing": {"en": "Predictive coding",          "fr": "Codage prédictif",         "de": "Predictive Coding",       "es": "Codificación predictiva", "ko": "예측 부호화"},
    "qualia":                {"en": "Qualia",                     "fr": "Qualia",                   "de": "Qualia",                  "es": "Qualia",                  "ko": "감각질"},
    "hard_problem":          {"en": "Hard problem of consciousness","fr": "Problème difficile de la conscience","de": "Schweres Problem des Bewusstseins","es": "Problema difícil de la conciencia","ko": "의식의 어려운 문제"},
    "chinese_room":          {"en": "Chinese room",               "fr": "Chambre chinoise",         "de": "Chinesisches Zimmer",     "es": "Habitación china",        "ko": "중국어 방"},
    "iit":                   {"en": "Integrated information theory","fr": "Théorie de l'information intégrée","de": "Integrierte Informationstheorie","es": "Teoría de la información integrada","ko": "통합정보이론"},
    "attention_schema":      {"en": "Attention schema theory",    "fr": None,                       "de": None,                      "es": None,                      "ko": None},
    "higher_order":          {"en": "Higher-order theories of consciousness","fr": None,            "de": None,                      "es": None,                      "ko": None},
    "probability":           {"en": "Probability",                "fr": "Probabilité",              "de": "Wahrscheinlichkeit",      "es": "Probabilidad",            "ko": "확률"},
    "max_entropy":           {"en": "Principle of maximum entropy","fr": "Principe de maximum d'entropie","de": "Prinzip der maximalen Entropie","es": "Principio de máxima entropía","ko": None},
    "turing_machine":        {"en": "Turing machine",             "fr": "Machine de Turing",        "de": "Turingmaschine",          "es": "Máquina de Turing",       "ko": "튜링 기계"},
    "godel_incompleteness":  {"en": "Gödel's incompleteness theorems","fr": "Théorèmes d'incomplétude de Gödel","de": "Gödelscher Unvollständigkeitssatz","es": "Teoremas de incompletitud de Gödel","ko": "괴델의 불완전성 정리"},
    "lambda_calculus":       {"en": "Lambda calculus",            "fr": "Lambda-calcul",            "de": "Lambda-Kalkül",           "es": "Cálculo lambda",          "ko": "람다 대수"},
    "free_energy_principle": {"en": "Free energy principle",      "fr": "Principe d'énergie libre", "de": "Prinzip der freien Energie","es": "Principio de energía libre","ko": None},
    "active_inference":      {"en": "Active inference",           "fr": None,                       "de": None,                      "es": None,                      "ko": None},
    "abiogenesis":           {"en": "Abiogenesis",                "fr": "Abiogenèse",               "de": "Chemische Evolution",     "es": "Abiogénesis",             "ko": "화학진화설"},
    "autopoiesis":           {"en": "Autopoiesis",                "fr": "Autopoïèse",               "de": "Autopoiesis",             "es": "Autopoiesis",             "ko": "자기생성"},
    "strange_loop":          {"en": "Strange loop",               "fr": "Boucle étrange",           "de": "Seltsame Schleife",       "es": "Bucle extraño",           "ko": None},
    "self_reference":        {"en": "Self-reference",             "fr": "Autoréférence",            "de": "Selbstbezüglichkeit",     "es": "Autorreferencia",         "ko": "자기 언급"},
}

# ── pillar (a) PD primary texts — Project Gutenberg ebook ids ──────────────────
# PUBLIC DOMAIN. id → (label, author, lang). en strong; fr/de partial; es/ko absent.
GUTENBERG = [
    (1228,  "On the Origin of Species",          "Charles Darwin",   "en"),
    (2300,  "The Descent of Man",                 "Charles Darwin",   "en"),
    (15491, "Theory of Heat",                     "James Clerk Maxwell","en"),
    (57628, "The Principles of Psychology, Vol. 1","William James",   "en"),
    (37157, "Science and Hypothesis",             "Henri Poincaré",   "en"),
    (15114, "An Investigation of the Laws of Thought","George Boole", "en"),
]


def _wiki_extract(lang, title, timeout=30):
    """Fetch one Wikipedia article plaintext via the action API. CC-BY-SA-4.0.
    Returns (title_resolved, text) or (None, '') when the page is missing."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "extracts",
        "explaintext": "1", "exsectionformat": "plain",
        "titles": title, "redirects": "1",
    })
    url = f"https://{lang}.wikipedia.org/w/api.php?{q}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                d = json.load(r)
            pages = d.get("query", {}).get("pages", {})
            if not pages:
                return None, ""
            p = list(pages.values())[0]
            if "missing" in p or p.get("pageid", 0) == 0:
                return None, ""
            return p.get("title"), (p.get("extract") or "").strip()
        except Exception:
            if attempt == 3:
                return None, ""
            time.sleep(2 * (attempt + 1))
    return None, ""


def _strip_gutenberg(raw):
    """Strip the Project Gutenberg license header/footer, keep the PD body."""
    s = raw
    start_markers = ["*** START OF THE PROJECT GUTENBERG", "*** START OF THIS PROJECT GUTENBERG"]
    end_markers = ["*** END OF THE PROJECT GUTENBERG", "*** END OF THIS PROJECT GUTENBERG"]
    lo = 0
    for m in start_markers:
        i = s.find(m)
        if i != -1:
            nl = s.find("\n", i)
            lo = nl + 1 if nl != -1 else i
            break
    hi = len(s)
    for m in end_markers:
        i = s.find(m)
        if i != -1:
            hi = i
            break
    return s[lo:hi].strip()


def _gutenberg(eid, timeout=60):
    """Fetch a Gutenberg ebook plaintext (PUBLIC DOMAIN), body only."""
    for url in (f"https://www.gutenberg.org/cache/epub/{eid}/pg{eid}.txt",
                f"https://www.gutenberg.org/files/{eid}/{eid}-0.txt"):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode("utf-8", "replace")
            body = _strip_gutenberg(raw)
            if len(body) > 1000:
                return body
        except Exception:
            continue
    return ""


def build(langs, kb_per_gutenberg, sample):
    blocks = []   # list of (bytes, meta)
    title_cap = 6000 if sample else 0          # 0 = no cap (full article)
    gut_cap = (8 if sample else kb_per_gutenberg) * 1024
    title_keys = list(SCIENCE_TITLES.keys())
    if sample:
        title_keys = title_keys[:8]            # first 8 fields only for the sample

    # (a-wiki) — REAL CC-BY-SA-4.0 Wikipedia, by named title, per lang.
    for field in title_keys:
        per_lang = SCIENCE_TITLES[field]
        for lang in langs:
            title = per_lang.get(lang)
            if not title:
                continue
            resolved, text = _wiki_extract(lang, title)
            if not text or len(text) < 200:
                print(f"  [wiki] SKIP {lang}:{title} (missing/thin)", file=sys.stderr)
                continue
            if title_cap:
                text = text[:title_cap]
            blk = (text + "\n").encode("utf-8")
            blocks.append((blk, {
                "pillar": "a_science", "subsource": "wikipedia",
                "field": field, "lang": lang, "title": resolved,
                "license": "CC-BY-SA-4.0", "bytes": len(blk),
            }))
            print(f"  [wiki] {lang}:{resolved} {len(blk)}B", flush=True)
            time.sleep(0.3)

    # (a-gutenberg) — PUBLIC DOMAIN primary texts (en spine; honest per-lang note).
    for eid, label, author, lang in GUTENBERG:
        if lang not in langs:
            continue
        body = _gutenberg(eid)
        if not body:
            print(f"  [gutenberg] SKIP pg{eid} {label} (fetch failed)", file=sys.stderr)
            continue
        body = body[:gut_cap]
        # truncate on a valid UTF-8 boundary
        blk = (body + "\n").encode("utf-8")
        blk = blk.decode("utf-8", "ignore").encode("utf-8")
        blocks.append((blk, {
            "pillar": "a_science", "subsource": "gutenberg",
            "field": "primary_text", "lang": lang,
            "title": f"{label} — {author}", "gutenberg_id": eid,
            "license": "PUBLIC-DOMAIN", "bytes": len(blk),
        }))
        print(f"  [gutenberg] pg{eid} {label} {len(blk)}B", flush=True)
        time.sleep(0.3)

    data = b"\n".join(b for b, _ in blocks) + (b"\n" if blocks else b"")
    meta = [m for _, m in blocks]
    return data, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="serving/corpus/growth_science_5lang.txt")
    ap.add_argument("--meta", default="serving/corpus/growth_science_5lang.meta.jsonl")
    ap.add_argument("--langs", default="en,fr,de,es,ko")
    ap.add_argument("--kb-per-gutenberg", type=int, default=60,
                    help="bytes/1024 cap per PD primary text (full build)")
    ap.add_argument("--sample", action="store_true",
                    help="small sample (8 fields, capped excerpts) for the committed head")
    args = ap.parse_args()

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    for lg in langs:
        if lg not in LANGS:
            print(f"unknown lang {lg}", file=sys.stderr); sys.exit(2)

    data, meta = build(langs, args.kb_per_gutenberg, args.sample)

    # byte-vocab V=256 round-trip invariant.
    assert data.decode("utf-8"), "UTF-8 round-trip failed"
    assert b"\xfe" not in data and b"\xff" not in data, "0xFE/0xFF must be absent"

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(data)
    with open(args.meta, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    sha = hashlib.sha256(data).hexdigest()
    from collections import Counter
    by_lang = Counter()
    by_src = Counter()
    for m in meta:
        by_lang[m["lang"]] += m["bytes"]
        by_src[m["subsource"]] += m["bytes"]
    print(f"[growth-science] wrote {args.out} bytes={len(data)} blocks={len(meta)}")
    print(f"[growth-science] sha256={sha}")
    print(f"[growth-science] per_lang_bytes={dict(sorted(by_lang.items()))}")
    print(f"[growth-science] per_source_bytes={dict(sorted(by_src.items()))}")
    print(f"[growth-science] license: wikipedia=CC-BY-SA-4.0  gutenberg=PUBLIC-DOMAIN")


if __name__ == "__main__":
    main()
