# CORPUS — log

Append-only history sister of `CORPUS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — UNIFIED 5-lang corpus SHIPPED (M1–M5 closed)

- [x] **M1** — `serving/persona_sns_corpus_5lang_gen.py`: 20-roster × 16 scenario × {IG,YT} extended to en/fr/de/es (ko delegated to KR module → ko slice byte-identical). Per-tone BODY banks (praise/comfort/smalltalk, all 20 tones) + 13 long-tail GENERIC + scenario user-lines + voice rules per lang. Archetype voice carried across langs (knight=formal/archaic, ice_queen=cold). DETERMINISTIC (seed 20260604 rerun sha identical). p2/p3/p4 clean (role/persona/character tags grep=0). p6 no-RLHF.
- [x] **M2** — built clean wiki backbone (`build_wiki_backbone_5lang.py`: wikimedia/wikipedia 20231101 en/fr/de/es/ko, CC-BY-SA-4.0, HF datasets-server REST, $0 CPU no-GPU, 1MB/lang) + merged ~50/50 with persona (`merge_corpus_5lang_unified.py` block-interleave) → `persona_sns_corpus_5lang_unified.txt` 10.0 MB sha `ac6ed840`. NOT reusing `clm-backbone-5lang-sample` (off-axis ko/en/zh/ru/ja + NSFW/spam ko C4 → clean rebuild per a_completeness_over_cheap). CORPUS_CARD_5lang_unified.md (per-lang split · sha · license · dialogue%). HF `dancinlab/anima-corpus-5lang-unified` PUBLIC, 6 files, sha-verified via authed re-download, private=False verified.
- [x] **M3** — `domains/CORPUS-enrichment-analysis.md`: KOSMOS e7_31 31-anchor manifest survey (18 categories × 16 emotions) → ranked 8-candidate what-to-add list. TOP-3: (1) consciousness-carving register [evidence, biggest gap — corpus has zero contemplative/inner-state text yet that's anima's core domain] (2) dialogue-act balance [evidence — all 16 SNS acts supportive, none disagree/boundary/persona-asks] (3) wiki topical breadth [evidence — alphabetical-prefix sampling bias]. Honest [evidence] vs [speculative] tags. a_kosmos pointer-only.
- [x] **M4** — HF.jsonl row + `corpus_5lang_unified.kosmos` anchor (tier 53, 다국어/resonance, text+manifest+tension 5ch) + KOSMOS.md hub pointer + a_hf_collections join (KOSMOS + CLM). 5-lang 7B retrain = follow-on rung (separate from KR-persona 7B).
- [x] **M5** — per-lang byte balance: en 19.14% · fr 20.53% · de 20.18% · es 19.62% · ko 20.53% (5-way balanced; every lang carries BOTH wiki + persona; no silent under-coverage). In CORPUS_CARD.

## 2026-06-04 — domain created

- [x] CORPUS domain seeded (snapshot `CORPUS.md` + this log + DOMAINS.tape row).
- [x] inventory recorded: `anima-chat-corpus-mix-70wiki-30dialogue` (5-lang wiki + dialogue), `anima-persona-sns-corpus` (KR-only, 20-roster IG/YT, 4.19MB/13,322 dlg), `clm-backbone-5lang-sample`, `anima-clm-p1-corpus`.
- [x] coverage GAP identified: SNS + persona are Korean-only; 5-lang lives only in wiki/chat. → unified 5-lang corpus is the target.
- [ ] M1 5-lang persona-voice templates (en/fr/de/es) added to `serving/persona_sns_corpus_gen.py`.
- [ ] M2 unified 5-lang corpus (wiki+SNS+persona) + CORPUS_CARD + HF.
- [ ] M3 KOSMOS survey → what-to-add ranked list.
- [ ] M4 HF.jsonl + KOSMOS/CLM collections + feed 5-lang 7B retrain.
- [ ] M5 honest per-lang byte-balance report.
