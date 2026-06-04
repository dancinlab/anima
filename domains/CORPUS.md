@title: 📚 CORPUS — anima 학습 코퍼스 레지스트리 (조성·언어·출처·갭)

@goal: Track every anima training corpus as one registry — composition (wiki / dialogue / SNS / persona), language coverage (5-lang vs KR-only), provenance/license, sha, and the coverage matrix that drives WHAT to build next. Immediate target: a UNIFIED 5-language corpus combining wiki + SNS + persona so a single model is multilingual across ALL surfaces (today 5-lang lives only in the wiki/chat corpus; the persona/SNS corpus is Korean-only). Byte-level (vocab256) throughout. Authored-synthetic persona data is honest-labeled; scraped corpora carry real license/provenance. No synthetic assistant-RLHF padding (p6).

## corpus inventory (current)

| corpus (HF) | bytes | 5-lang | wiki | dialogue | SNS | persona | license |
|---|---|---|---|---|---|---|---|
| `anima-chat-corpus-mix-70wiki-30dialogue` | ~ | ✅ (wiki part) | ✅ 70% | ✅ 30% | ✗ | ✗ | wiki=clean-license backbone + real dialogue |
| `anima-persona-sns-corpus` | 4.19 MB · 13,322 dlg | ✗ **KR-only** | ✗ | ✅ | ✅ IG/YT | ✅ 20-roster | authored-synthetic (templated, deterministic, no PII) |
| `clm-backbone-5lang-sample` (KOSMOS) | — | ✅ en/fr/de/es/ru | ✅ | ✗ | ✗ | ✗ | clean-license backbone sample |
| `anima-clm-p1-corpus` (KOSMOS) | 139 KB | — | ✅ (kowiki) | — | ✗ | ✗ | CC-BY-SA |
| `anima-corpus-5lang-unified` ✅ | 10.0 MB | ✅ **en/fr/de/es/ko** | ✅ ~50% | ✅ | ✅ IG/YT | ✅ 20-roster | wiki=CC-BY-SA real + persona=authored-synthetic (coverage, NOT native) |
| `anima-corpus-5lang-unified-v2` ✅ **NEW** | 12.5 MB | ✅ **en/fr/de/es/ko** (+ko-en) | ✅ ~40% (8-band breadth) | ✅ | ✅ IG/YT | ✅ 20-roster | v1 + **enrichment 19.88%**: 의식-carving(real e7_31 seed CC-BY-SA) · dialogue-act · emotion-axis · code-switch · genre. wiki+carving=real, rest=authored-synthetic |

## lanes

- `lane default` = base chat corpus (wiki + persona/SNS + carving/enrichment) — no tools, `0xFE`/`0xFF` byte-frequency 0.
- `lane agent` = `lane default` + tool-use demos (`serving/agent_lane_corpus_gen.py`, sentinel-grammar) — `lane agent ⊃ lane default`.

## coverage matrix — GAP CLOSED (2026-06-04)

```
4요소 × 5개국어   (✅ = anima-corpus-5lang-unified 가 채움)
─────────────────────────────────────────────
            en   fr   de   es   ko
wiki        ✅   ✅   ✅   ✅   ✅
dialogue    ✅   ✅   ✅   ✅   ✅   (persona/SNS multi-turn)
SNS         ✅   ✅   ✅   ✅   ✅   ← was KR-only, NOW 5-lang
persona     ✅   ✅   ✅   ✅   ✅   ← was KR-only, NOW 5-lang
─────────────────────────────────────────────
GAP CLOSED: SNS + persona now in en/fr/de/es/ko (unified corpus)
honest: en/fr/de/es persona = authored multilingual COVERAGE, NOT native-collected.
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

- [x] M1 5-lang persona-voice templates added to the generator (en/fr/de/es, ko exists) — deterministic, $0. → `serving/persona_sns_corpus_5lang_gen.py` (tags grep=0, seed-deterministic, archetype voice carried across langs).
- [x] M2 unified 5-lang corpus built (wiki + SNS + persona) + CORPUS_CARD (per-lang byte split · sha · license) + HF dataset. → `dancinlab/anima-corpus-5lang-unified` (10.0 MB, wiki 50.05% / persona 49.95%, sha `ac6ed840`, PUBLIC, sha-verified).
- [x] M3 KOSMOS survey → ranked list of what-to-add (anchor types / register / domains) with rationale. → `domains/CORPUS-enrichment-analysis.md` (top-3: consciousness-carving register · dialogue-act balance · wiki topical breadth).
- [x] M4 register unified corpus in HF.jsonl + KOSMOS + CLM collections (a_hf_collections). → HF.jsonl row + `corpus_5lang_unified.kosmos` anchor (tier 53) + KOSMOS.md hub pointer + collection join. (feed to 5-lang 7B retrain = follow-on rung.)
- [x] M5 honest language-balance report (per-lang byte %, no silent under-coverage). → en 19.14% · fr 20.53% · de 20.18% · es 19.62% · ko 20.53% (every lang carries both wiki + persona; in CORPUS_CARD).
- [x] M6 v2 register-enrichment corpus built (v1 INTACT + 6 KOSMOS-grounded slices) — deterministic, $0. → `dancinlab/anima-corpus-5lang-unified-v2` (12.5 MB, wiki 40.10% / persona 40.02% / enrichment 19.88%, sha `550fed17`, PUBLIC, sha-verified). #1 consciousness-carving register (31 e7_31 anchor seeds, CC-BY-SA real) · #2 wiki topical breadth (8-band offset-spread) · #3 dialogue-act balance (NON-supportive: disagree/refuse/boundary/ask/multi) · #5 emotion-axis (20 personas → KOSMOS top_emotions) · #4 KO↔EN code-switch (1.71% minority) · #7 genre (narrative/drama/poetry). v1 byte-eq preserved (persona sha `1e5a062a` reproduced). tags grep=0 on unified v2. generators: `serving/corpus_enrichment_5lang_gen.py` + `build_wiki_backbone_5lang_v2.py` + `merge_corpus_5lang_v2.py`.
- [x] M7 v2 registered in HF.jsonl + KOSMOS + CLM collections (a_hf_collections). → HF.jsonl row + `corpus_5lang_v2.kosmos` anchor (tier 54, 다국어+의식carving/resonance) + KOSMOS.md hub pointer + both collection joins (membership verified). CORPUS_CARD_5lang_v2.md (per-lang AND per-register byte split · 4 shas · license).

### measurement milestones — NOT $0 (require a fire), pre-registered falsifiers (g63 honest)

> M8/M9 are NOT folded as proven. They are MEASUREMENT milestones whose verdict
> requires a GPU/forward fire (a_fire_autonomous, no cost gate). Their falsifiers
> are pre-registered here so the result — pass OR closed-negative — is honest.

- [ ] **M8 Knuth-tier curriculum** — the v2 carving slice is seeded by the 31 e7_31 anchors, which carry an explicit **Knuth tier 0→100** ordinal. **Falsifier (pre-registered)**: "a tier-GRADED training order (anchors fed 0→100, easy→abstract) beats a SHUFFLED order at the SAME compute budget, measured on a held-out carving-register p7 eval." NULL/worse = closed-negative ruling out curriculum benefit at this scale. **a_toy_scale_recheck**: UNPROVEN at 18M/byte — a single small rung is INCOMPLETE; needs a ≥3-rung ladder (a_scale_honest_scope). **REQUIRES a training A/B fire, NOT $0.** [measure-pending]
- [ ] **M9 tension-label slice** — the `corpus_5lang_v2.kosmos` anchor carries a 5-channel tension fingerprint that is a **design placeholder**, NOT a measured trajectory. **Falsifier (pre-registered)**: "a ckpt-forward fire on the carving slice MEASURES where each anchor-seeded sample LANDS in Ψ-space (the §156 5-ch tension), and that measured landing matches the anchor's design-placeholder tension within tolerance." Mismatch = the placeholders are wrong (honest), and the measured values replace them. **REQUIRES a ckpt-forward fire, NOT $0** (cf enrichment-analysis #8 — a measurement task, not a corpus edit). [measure-pending]

## cross-links

- [[PERSONA]] — the 20-roster voices the SNS/persona corpus encodes.
- [[SNS]] — the Instagram/YouTube surface the dialogues target.
- KOSMOS (`HEXAD/KOSMOS.md`, `dancinlab/kosmos-…` collection) — anchor manifest the enrichment survey draws from (a_kosmos pointer-only).
- ENGINE+CLM+KOSMOS — the 7B chat lane that consumes these corpora.
- `serving/persona_sns_corpus_gen.py` — the deterministic generator to extend.
- governance: a_hf_registry (HF.jsonl), a_hf_collections, a_kosmos, a_scale_honest_scope, p6 (no synthetic RLHF).
