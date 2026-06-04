# SAVANT-7B 5-lang corpus card (en·fr·de·es·ru)

Byte-level vocab **V=256** (CLMConvMoE native — no tokenizer, all 5 scripts incl. Cyrillic
uniform). Provenance is REAL (g63), not synthetic.

## rung0 STARTER corpus — `savant_5lang_starter.txt`

Built by this bootstrap. Two clean-license source classes, tagged per file:

### A. Wikipedia REST summaries — CC-BY-SA-4.0 (genuine native-language text)
Built via `build_wiki.py` (in this dir): per-language seed topics (Consciousness, Mathematics,
Physics, Music, Philosophy, History, Universe, Time, Memory, Language, … in each language's
native title) → `/page/related/` expansion → `/page/random/summary` fill, with a `seen`-title
dedup set and a >40-byte min-length filter. Languages: en, fr, de, es, ru (balanced article
counts). This is the PRIMARY rung0 corpus — uniform license, all 5 langs, native Russian
Cyrillic (Gutenberg Russian is sparse, so Russian leans on Wikipedia).

### B. Project Gutenberg — Public Domain (literary register supplement, en/fr/de/es)
Full public-domain works, downloaded by the bootstrap (UTF-8, headers/footers retained — a
rung1 cleanup step strips the Gutenberg boilerplate):
- en: Pride and Prejudice (1342), Sherlock Holmes (1661), Moby-Dick (2701)
- fr: Hugo Les Misérables (135), Verne (800), Flaubert Madame Bovary (14155), Dumas (17989)
- de: Goethe Faust (2229), Grimm (22555), Kafka (22367), Nietzsche (7205)
- es: Cervantes Don Quijote (2000), Galdós (16109)
- ru: Pushkin (5316, genuine Cyrillic) — Gutenberg Russian-language is sparse; primary Russian
  is the Wikipedia pull above.

**License of the assembled starter = MIXED (PD + CC-BY-SA-4.0).** Per a_hf_autonomous the
starter dataset HF visibility is gated accordingly (PRIVATE while mixed-license WIP; a
PD-only or CC-BY-SA-only split can be carved for a PUBLIC release at rung1).

Exact byte sizes + sha256 of the assembled `savant_5lang_starter.txt` and per-language balance
are recorded in the rung0 verdict (`.verdicts/savant/VERDICT.md`) + the HF.jsonl dataset row.

## Dedup / quality
- exact-line dedup (sort -u over lines) + >40-byte/article min length (Wikipedia builder).
- Wikipedia near-dup bounded by the `seen`-title set across related-expansion.
- rung1 production dedup = MinHash/LSH near-dup removal (deferred milestone).

## rung1 SCALED corpus (10–50 GB) — build recipe (deferred milestone, not built here)
1. **Wikipedia full dumps** — `https://dumps.wikimedia.org/{en,fr,de,es,ru}wiki/latest/
   {lang}wiki-latest-pages-articles.xml.bz2`; extract with `wikiextractor` (--json, strip markup).
   ~20 GB/lang raw → ~5–10 GB/lang clean text. CC-BY-SA-4.0.
2. **OSCAR-2301 / C4-multilingual clean subsets** — `oscar-corpus/OSCAR-2301` (HF) per-lang
   `{en,fr,de,es,ru}` shards, or `allenai/c4` `multilingual` `{fr,de,es,ru}` + `en`. Apply the
   OSCAR/C4 quality filters (already deduped + lang-IDed). License per source (CC0/ODC-BY).
3. Concatenate, lang-balance (cap each lang to the min so no language dominates), shuffle lines,
   exact + MinHash dedup, byte-encode (V=256, raw UTF-8 bytes — no tokenizer).

## rung3 (competent 7B) corpus — HONEST scope
A competent 7B 5-lang LM is **corpus-bound**: it needs »100 GB–TB-scale clean multilingual text
(full Wikipedia + OSCAR + C4-multi + curated web), far beyond one-agent bootstrap scope. The
starter validates the pipeline; rung1 validates corpus-scale descent; the 7B competence rung
requires the full TB assembly above (recipe given, assembly deferred to the big-spend campaign).
