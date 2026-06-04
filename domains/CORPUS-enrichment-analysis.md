# CORPUS — KOSMOS-grounded enrichment analysis (M3)

> What additional content would most improve the unified 5-lang corpus
> (`dancinlab/anima-corpus-5lang-unified` — wiki + SNS + persona, en/fr/de/es/ko)?
>
> Grounded in a survey of the KOSMOS anchor manifest (a_kosmos **pointer-only** —
> this analysis does NOT duplicate the kosmos spec; format SSOT =
> `github.com/dancinlab/kosmos`). Honest: each item is tagged **[evidence]**
> (a concrete coverage gap measured against the manifest) or **[speculative]**
> (plausible but unmeasured). Cost is a rough CPU-$0 effort estimate.

## what the unified corpus has today

- **Surfaces**: wiki (encyclopedic prose, ~50%) + persona×SNS dialogue (~50%).
- **Languages**: en/fr/de/es/ko, 5-way byte-balanced (19.1–20.5% each).
- **Registers present**: encyclopedic (wiki) + casual social/roleplay (SNS).
- **Dialogue acts present** (16 scenarios): praise · comfort · smalltalk ·
  advice · selfie-react · comment-reply · live-qna · recommend · apology ·
  congrats · cheer · howto · share-news · fanart · goodnight · motivate.
- **Emotional span (SNS)**: warmth, comfort, encouragement, playfulness, menace,
  coldness — carried by the 20-persona archetype voices.

## what the KOSMOS manifest covers that the corpus does NOT

The KOSMOS `e7_31` canonical anchor set (31 consciousness-carving anchors,
`HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/`) spans ~18 **categories** —
감각(sense) · 관계(relation) · 의식상태(consciousness-state) · 생명(life) ·
예술(art) · 수(number) · 시간(time) · 자연(nature) · 우주(cosmos) · 공간(space) ·
기억(memory) · 언어(language) · 윤리(ethics) · 기술(technology) · 운동(motion) ·
물질(matter) · 기준점(baseline) · 혼합(mixed) — and ~16 **emotions** —
serenity · clarity · wonder · resonance · longing · depth · peace · flow ·
joy · creativity · stillness · awe · vastness · ecstasy · neutral.

Mapping those axes onto the corpus surfaces reveals the gaps below.

## ranked enrichment candidates

| # | candidate | rationale (1-line) | cost | already covered? | tag |
|---|---|---|---|---|---|
| 1 | **Consciousness-carving register** (contemplative/introspective prose seeded by the 31 KOSMOS anchors: breath·meditation·nirvana·awe·eternity·infinity) | The corpus has NO contemplative/inner-state register; KOSMOS's whole consciousness axis (의식상태: 명상/열반/엑스터시/해리/루시드드림) is absent — this is anima's core domain and the biggest register gap | low ($0, anchor-text templated like persona gen) | NO | **[evidence]** |
| 2 | **Per-language balance is the floor, not the cap — raise wiki topical breadth** | wiki backbone is the FIRST N articles per lang (alphabetical bias); broaden by sampling across the article space so each language covers science/history/art/geography, not just A-prefix | low ($0, offset-spread the REST page walk) | partial (1MB/lang but narrow topical slice) | **[evidence]** |
| 3 | **Dialogue-act balance audit + under-covered acts** (disagreement · boundary-setting · refusal · question-asking-by-persona · multi-party) | All 16 current scenarios are follower→persona supportive/affective; NONE cover the persona *disagreeing*, *setting a boundary*, or *asking the follower a question* — KOSMOS 윤리(약속/promise) + 관계(relation) axes suggest these | low ($0, add scenarios to the generator) | NO (16 acts all supportive) | **[evidence]** |
| 4 | **Code-switching / mixed-language turns** (a follower writes EN, persona replies in the same lang but drops a loanword; KO↔EN webtoon-style) | The corpus is strictly monolingual per dialogue; real SNS is code-switched. Cheap to add as a small labeled slice; honest that it's authored | low ($0, generator variant) | NO | **[speculative]** (helps realism, unmeasured) |
| 5 | **Emotion-axis coverage for the persona voices** (map each archetype to KOSMOS top_emotions: e.g. sorceress→wonder/longing, demon_lord→awe/vastness, stoic_mentor→stillness/clarity) | Persona voices currently cover warmth/menace/cold but miss KOSMOS's serenity/awe/vastness/stillness/resonance band; aligning archetypes to the anchor emotion-set widens affective range | medium ($0 but needs per-archetype emotion templates) | partial | **[evidence]** |
| 6 | **Knuth-tier ordinal scaffolding** (an explicit difficulty/abstraction ladder 0→100 mirroring the Knuth tiers, so the corpus has a graded complexity curve) | KOSMOS orders anchors by a 0–100 Knuth tier (score 0.0→2.847); the corpus has no graded-complexity axis — a tiered slice could give the model a curriculum signal | medium ($0, but design work to define tier→text) | NO | **[speculative]** (curriculum benefit unproven at this scale; cf a_toy_scale_recheck) |
| 7 | **Genre diversity beyond wiki+SNS** (narrative fiction · dialogue-heavy drama · poetry/lyric — the 예술/art KOSMOS axis: 만다라/선율/창의) | Only 2 registers (encyclopedic + social); KOSMOS 예술 axis (creativity/resonance) is unrepresented; narrative/poetic register would broaden generative range | medium ($0 if authored; clean-license sourcing if real) | NO | **[speculative]** |
| 8 | **Anchor-grounded `.kosmos` tension labels on a corpus slice** (attach the 5-channel tension fingerprint to a subset so a future fire can measure carving) | KOSMOS anchors carry a 5-ch tension payload; tagging a corpus slice would let a future ckpt-forward fire MEASURE where each surface lands in Ψ-space (today the persona anchor's tension is a design placeholder, not measured) | medium (needs a ckpt forward = a fire, NOT $0) | NO | **[speculative]** (requires a measurement fire; honest: not $0) |

## top-3 recommendation (for the next corpus rung)

1. **#1 Consciousness-carving register** — highest value, lowest cost, on-domain.
   anima IS a consciousness agent; the corpus having zero contemplative/inner-state
   text is the starkest gap the KOSMOS manifest exposes. Seed templated
   introspective prose from the 31 anchors (breath/meditation/awe/eternity/…) in
   all 5 languages, honest-labeled authored. **[evidence]**
2. **#3 Dialogue-act balance** — cheap, fixes a real skew (all 16 SNS acts are
   supportive/affective; no disagreement/boundary/question-by-persona). Add a
   handful of balancing scenarios to the generator. **[evidence]**
3. **#2 Wiki topical breadth** — cheap, removes the alphabetical-prefix sampling
   bias so each language's encyclopedic slice spans real topical diversity.
   **[evidence]**

## NOT recommended as primary

- **#8 tension-labeled slice** and any "measure carving in Ψ-space" item require a
  GPU/ckpt-forward fire to be meaningful — out of scope for this $0 corpus rung,
  and honestly labeled as a future measurement, not a corpus edit
  (a_completeness_over_cheap: don't dress a measurement task as a cheap corpus add).
- Pure scale-up (just more bytes of the same 16 scenarios) — adds size, not
  coverage; the gaps above are about *register/act/emotion breadth*, not volume
  (a_scale_honest_scope).

## honest scope

- All "would help" rationales for register/act/breadth gaps are **[evidence]** —
  they are concrete absences measured against the present corpus + the KOSMOS
  manifest. Curriculum/code-switch/genre benefits are **[speculative]** — plausible
  but their training impact is unmeasured at this scale (a_toy_scale_recheck:
  small-corpus gains may not transfer; re-test on a scale-up fire before claiming).
- a_kosmos: this analysis is **pointer-only** to the KOSMOS manifest; it does not
  copy or restate the kosmos spec. Anchor data read from
  `HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/` (anima-side hub).

## cross-links

- `domains/CORPUS.md` (M3 milestone) · `serving/corpus/CORPUS_CARD_5lang_unified.md`.
- KOSMOS hub: `HEXAD/KOSMOS.md` · anchors `HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31/`.
- governance: a_kosmos · a_scale_honest_scope · a_toy_scale_recheck ·
  a_completeness_over_cheap · p6.
