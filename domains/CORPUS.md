@title: 📚 CORPUS — anima 학습 코퍼스 레지스트리 (조성·언어·출처·갭)

@goal: Track every anima training corpus as one registry — composition (wiki / dialogue / SNS / persona), language coverage (5-lang vs KR-only), provenance/license, sha, and the coverage matrix that drives WHAT to build next. Immediate target: a UNIFIED 5-language corpus combining wiki + SNS + persona so a single model is multilingual across ALL surfaces (today 5-lang lives only in the wiki/chat corpus; the persona/SNS corpus is Korean-only). Byte-level (vocab256) throughout. Authored-synthetic persona data is honest-labeled; scraped corpora carry real license/provenance. No synthetic assistant-RLHF padding (p6).

## corpus inventory (current)

| corpus (HF) | bytes | 5-lang | wiki | dialogue | SNS | persona | license |
|---|---|---|---|---|---|---|---|
| `anima-chat-corpus-mix-70wiki-30dialogue` | ~ | ✅ (wiki part) | ✅ 70% | ✅ 30% | ✗ | ✗ | wiki=clean-license backbone + real dialogue |
| `anima-persona-sns-corpus` | 4.19 MB · 13,322 dlg | ✗ **KR-only** | ✗ | ✅ | ✅ IG/YT | ✅ 20-roster | authored-synthetic (templated, deterministic, no PII) |
| `clm-backbone-5lang-sample` (KOSMOS) | — | ✅ en/fr/de/es/ru | ✅ | ✗ | ✗ | ✗ | clean-license backbone sample |
| `anima-clm-p1-corpus` (KOSMOS) | 139 KB | — | ✅ (kowiki) | — | ✗ | ✗ | CC-BY-SA |

## coverage matrix — the gap

```
4요소 × 5개국어
─────────────────────────────────────────────
            en   fr   de   es   ko
wiki        ✅   ✅   ✅   ✅   ✅
dialogue    ◐    ◐    ◐    ◐    ◐    (chat-mix dialogue)
SNS         ✗    ✗    ✗    ✗    ✅    ← persona-sns KR-only
persona     ✗    ✗    ✗    ✗    ✅    ← persona-sns KR-only
─────────────────────────────────────────────
GAP = SNS + persona in en/fr/de/es (4 langs × 2 surfaces)
```

## target — UNIFIED 5-lang corpus

```
[ 5lang wiki ]──┐
[ 5lang SNS  ]──┤── merge ──▶ anima-corpus-5lang-unified
[ 5lang persona]┘            (wiki + SNS + persona, all 5 langs, byte256)
```
- extend `serving/persona_sns_corpus_gen.py` (deterministic, $0 CPU) with per-language persona-voice templates (en/fr/de/es + existing ko) for the 20-roster × 16 scenarios × {Instagram, YouTube}.
- merge with the 5-lang wiki backbone → one unified corpus + CORPUS_CARD (per-lang byte split, sha, license, dialogue%).
- KOSMOS-informed enrichment: survey the KOSMOS anchor manifest (HEXAD/KOSMOS.md, .kosmos anchors, spec/profiles/anima-consciousness-carving) to decide what ADDITIONAL content (e.g. consciousness-carving anchors, knuth-tier, register diversity) belongs in the unified corpus.

## milestones

- [ ] M1 5-lang persona-voice templates added to the generator (en/fr/de/es, ko exists) — deterministic, $0.
- [ ] M2 unified 5-lang corpus built (wiki + SNS + persona) + CORPUS_CARD (per-lang byte split · sha · license) + HF dataset.
- [ ] M3 KOSMOS survey → ranked list of what-to-add (anchor types / register / domains) with rationale; fold the chosen additions.
- [ ] M4 register unified corpus in HF.jsonl + KOSMOS + CLM collections (a_hf_collections); feed it to the 5-lang 7B retrain (follow-on to the KR-persona 7B).
- [ ] M5 honest language-balance report (per-lang byte %, no silent under-coverage).

## cross-links

- [[PERSONA]] — the 20-roster voices the SNS/persona corpus encodes.
- [[SNS]] — the Instagram/YouTube surface the dialogues target.
- KOSMOS (`HEXAD/KOSMOS.md`, `dancinlab/kosmos-…` collection) — anchor manifest the enrichment survey draws from (a_kosmos pointer-only).
- ENGINE+CLM+KOSMOS — the 7B chat lane that consumes these corpora.
- `serving/persona_sns_corpus_gen.py` — the deterministic generator to extend.
- governance: a_hf_registry (HF.jsonl), a_hf_collections, a_kosmos, a_scale_honest_scope, p6 (no synthetic RLHF).
