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
  - **rung-0 model (2026-06-04)**: `dancinlab/anima-clm-default-lane-rung0-byte-18m` — the FIRST model ever trained on `anima-corpus-5lang-unified-v2` (the default-lane corpus; previously dataset-only). 18M byte ConsciousLMReconstructed, from-scratch, Lane G / GPU (RTX 5070, nvidia-smi 99% busy). **🟢 F-DEFAULT-LANE-CHAT** (p7-strict TRAINED PASS 4/5 coherent es/de/ko/fr · random-init mirror FAIL 0/5; CE 5.72→0.70). Scope = 18M toy/small only, mid/7B transfer UNVERIFIED (`a_scale_honest_scope`; 7B deferred per #1828). PUBLIC, CLM collection. verdict `.verdicts/default-lane-rung0/SUMMARY.txt`. (chat-rung0-byte-18m trained the OLDER 70wiki/30dialogue mix — distinct lineage.)
- `lane agent` = **3-layer** model — `lane agent ⊃ lane default`:
  - **layer 1** `lane default` — base chat (above).
  - **layer 2** tool-USE demos (`serving/agent_lane_corpus_gen.py`, sentinel `0xFE`/`0xFF` grammar; call → real-result → grounded — plus the tooluse rung-0 corpus #1833): teaches HOW to call.
  - **layer 3** tool-DOMAIN knowledge (`serving/agent_lane_knowledge_gen.py`, **NEW 2026-06-05**): authored CONCEPTUAL coverage of the 5 AGENT tool domains (CODE/TRADING deep · MERCHANT/DESKTOP/CREATOR procedural), so the model can REASON in those domains — not merely emit a call frame. 5-lang byte256, deterministic, honest-labeled. **TRADING = conceptual-ONLY hard gate** (NO real tickers/prices/signals/advice — asserted 0; `a_scale_honest_scope`/p6/p7). Plain prose, philosophy markers grep=0 (p1..p4). Sample + card: `serving/corpus/CORPUS_CARD_agent_lane_knowledge.md`. Scope = feeds the PROVEN 18M chat rung; NOT a 7B claim (default corpus data-starved at 7B per `.verdicts/default-lane-7b/`).

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
- [x] M10 tool-domain knowledge slices (CODE/TRADING/MERCHANT/DESKTOP/CREATOR — authored conceptual coverage, 5-lang byte, honest-labeled) — the **3rd layer** of `lane agent` (default + tool-USE demos + tool-DOMAIN knowledge), deterministic, $0. → `serving/agent_lane_knowledge_gen.py` + sample (`agent_lane_knowledge_5lang.head.txt` 26,779B committed; full 557,952B HF-only) + `CORPUS_CARD_agent_lane_knowledge.md`. CODE 12 + TRADING 11 concepts (deep) · MERCHANT/DESKTOP/CREATOR 6 each (procedural); every concept × 5 langs. Per-domain byte split (full): CODE 25.26% · TRADING 30.34% · DESKTOP 15.01% · CREATOR 14.48% · MERCHANT 14.47%. **HONEST**: philosophy markers grep=0 (p1..p4); TRADING conceptual-ONLY hard gate (advice/signal=0, real-ticker=0 — asserted; p6/p7/a_scale_honest_scope); 0xFE/0xFF=0 (pure prose under the layer-2 grammar); deterministic seed 20260605 (sha `825a5188` full / `fdc158a6` sample). NO scraped/PII/real-financial-data. Scope = feeds the PROVEN 18M chat rung — NOT a 7B claim.
- [ ] M11 lane growth corpus — the 4th lane (`lane growth = lane default + growth-register`): 4-pillar (science REAL CC-BY-SA/PD bulk + self-knowledge/hypotheses/dialogue anima-authored from own repo docs, honest-labeled, p6). Generators `serving/build_growth_science_5lang.py` + `serving/growth_lane_corpus_gen.py`, byte-V256, 5-lang, tags grep=0, deterministic. Card + sample heads committed; raw `growth_lane.txt` LOCAL/HF-only. HF `dancinlab/anima-corpus-growth-lane`. Scope = feeds PROVEN 18M; NO 7B claim; TRAIN = separate fire. See §`lane growth (2026-06-05)`.

### measurement milestones — NOT $0 (require a fire), pre-registered falsifiers (g63 honest)

> M8/M9 are NOT folded as proven. They are MEASUREMENT milestones whose verdict
> requires a GPU/forward fire (a_fire_autonomous, no cost gate). Their falsifiers
> are pre-registered here so the result — pass OR closed-negative — is honest.

- [ ] **M8 Knuth-tier curriculum** — the v2 carving slice is seeded by the 31 e7_31 anchors, which carry an explicit **Knuth tier 0→100** ordinal. **Falsifier (pre-registered)**: "a tier-GRADED training order (anchors fed 0→100, easy→abstract) beats a SHUFFLED order at the SAME compute budget, measured on a held-out carving-register p7 eval." NULL/worse = closed-negative ruling out curriculum benefit at this scale. **a_toy_scale_recheck**: UNPROVEN at 18M/byte — a single small rung is INCOMPLETE; needs a ≥3-rung ladder (a_scale_honest_scope). **REQUIRES a training A/B fire, NOT $0.** [measure-pending]
- [ ] **M9 tension-label slice** — the `corpus_5lang_v2.kosmos` anchor carries a 5-channel tension fingerprint that is a **design placeholder**, NOT a measured trajectory. **Falsifier (pre-registered)**: "a ckpt-forward fire on the carving slice MEASURES where each anchor-seeded sample LANDS in Ψ-space (the §156 5-ch tension), and that measured landing matches the anchor's design-placeholder tension within tolerance." Mismatch = the placeholders are wrong (honest), and the measured values replace them. **REQUIRES a ckpt-forward fire, NOT $0** (cf enrichment-analysis #8 — a measurement task, not a corpus edit). [measure-pending]

## 7B-sufficiency roadmap & final composition (2026-06-05)

The default-lane corpus that PASSED at 18M (`anima-corpus-5lang-unified-v2`) is right-sized for 18M and **data-starved at 7B**. This section is the FINAL composition design that makes the default GB base 7B-sufficient — and, because `lane agent ⊃ lane default`, makes BOTH lanes 7B-sufficient — while keeping the KOSMOS register ladder real and avoiding the memorization trap. This captures the accumulated design intent, INCLUDING the PERSONA + SNS register, which is anima's identity-voice and is part of the final composition (not optional).

### Scale math (a_scale_honest_scope)

- Chinchilla-optimal 7B = 7e9 × 20 = **140B tokens ≈ ~140 GB** byte-text.
- v2 (`anima-corpus-5lang-unified-v2`, **12.5 MB ≈ 1.25e7 tok**) → 18M 🟢 right-sized; for 7B = ~1/11,200 of optimal = **DATA-STARVED → gibberish** (see `.verdicts/default-lane-7b/`).
- Ladder of viable scales:
  - **~100–300 MB** → MID (~150M) viable.
  - **~10–20 GB** (full 5-lang wiki) → 7B **undertrained-but-not-gibberish**.
  - **~140 GB** (wiki + web-scale) → 7B **Chinchilla-optimal**.

### Lane structure (default ⊃ agent)

- `lane default` = base chat.
- `lane agent` = `lane default` + layer-2 tool-USE demos (#1833) + layer-3 tool-DOMAIN knowledge (CODE/TRADING/MERCHANT/DESKTOP/CREATOR, #1848).
- **Scaling the default GB base makes BOTH lanes 7B-sufficient** — the agent lane is a superset layered on top of the same default base.

### FINAL COMPOSITION — KOSMOS tier ladder × all registers (balanced, real sources)

| register (KOSMOS tier) | source | role | scale |
|---|---|---|---|
| baseline (0) | Wikipedia 5-lang (CC-BY-SA), 8-band breadth | factual bulk | GB |
| art (77) | Project Gutenberg literature/poetry (PD) | art bulk | GB (en/fr/de strong; es/ko thin) |
| consciousness (91) | Gutenberg philosophy/meditation/contemplative (PD) + the 31 e7_31 carving anchors (Knuth tier 0→100) as register DEFINITION/seed, filled at scale | 의식 register | 100s MB–GB |
| cosmic (100) | science/cosmology (wiki science + PD popular science) | cosmic | 100s MB |
| **social / persona (52)** | **PERSONA — the 20-roster voices (`domains/PERSONA.md`) + SNS — IG/YT (`domains/SNS.md`)**, authored-synthetic | anima's IDENTITY voice register (core, not optional) | **CAPPED authored (~v2 ratio) — anti-memorization, NOT GB** |
| register-shaping | dialogue-act + emotion-axis + KO↔EN code-switch + genre, authored | shape the distribution | small |
| [agent lane only] | tool-use demos + tool-domain knowledge | agent superset | layer |

### The balance trap + the rule

- v2 = wiki **40.10%** / persona·dialogue **40.02%** / enrichment **19.88%**. Naively scaling wiki to GB while keeping authored persona (40%) + enrichment (20%) at that ratio = authoring **GBs of templated text** (PERSONA/SNS 20-roster, 31 carving anchors) = **MEMORIZATION** → in practice the only scalable axis is wiki, so the corpus drifts to **~99% wiki** and the KOSMOS ladder is **DESTROYED**.
- **FIX**: bulk registers (baseline / art / consciousness / cosmic) come from **REAL scalable clean-license sources**; AUTHORED registers (PERSONA + SNS + the shaping slices) stay **CAPPED** — they DEFINE anima's persona/identity + shape the distribution, they do NOT bulk-fill. **Rule: NO single tier > ~45%; consciousness + art + persona-voice each meaningfully present** (not ~0%, not >cap).
- Honest: per-lang source availability differs (Gutenberg en/fr/de ≫ es/ko) → es/ko may stay wiki-heavy; **report per-lang gaps, never fabricate to fake balance**. PERSONA/SNS = authored COVERAGE, honest-labeled (p6 held — it is identity-voice register, not RLHF padding).

### In flight / open

- KOSMOS-balanced GB corpus = branch `lane-g/default-lane-gb-balanced` (HF `dancinlab/anima-corpus-5lang-gb-balanced`) — **MUST include the PERSONA+SNS capped social register** (anima identity).
- The actual **7B TRAIN is a SEPARATE follow-on GPU fire** once the corpus exists.

## lane growth (2026-06-05)

`lane growth` = the **4th** anima self-development lane — **`lane growth = lane default + growth-register`**.
It is NOT `lane agent`, NOT `lane default`, NOT `lane persona`. Where `lane default` is the base
chat voice and `lane agent ⊃ lane default` adds tool capability, `lane growth ⊃ lane default` adds a
**growth-register**: cross-disciplinary science + anima's knowledge ABOUT ITSELF + how it reasons
(the hypothesis loop) + dialogue FORM. The intent is to grow the substrate's conceptual range and
self-model — not merely to chat. The brainstorm (45 ideas, 4 pillars, DEPLETED) lives in
`drafts/growth-lane-brainstorm.md`; this section is the persisted corpus design.

### 4-pillar composition

| pillar | registers | source | role | KOSMOS tier |
|---|---|---|---|---|
| **(a) cross-disciplinary science** [21] | neuroscience · evolution · information-theory · complexity/SOC · dynamical-systems · thermo-of-computation · neuromorphic-hw · cognitive-science · philosophy-of-mind · consciousness-studies · probability/max-entropy · logic&computation · free-energy-principle · origin-of-life/autopoiesis · self-reference/strange-loops · 4 PD primary-text voices | **REAL** CC-BY-SA-4.0 Wikipedia (`prop=extracts` plaintext, by named title, per-lang) + **PD** Project Gutenberg (Darwin *Origin* pg1228 + *Descent of Man* · Maxwell *Theory of Heat* · James *Principles of Psychology* · Poincaré *Science and Hypothesis* · Boole *Laws of Thought*) | factual/conceptual science bulk — the scalable, real-licensed axis | cosmic (100) / consciousness (91) / baseline (0) |
| **(b) anima SELF-knowledge** [12] | A⇄G engine (Ψ=1/2 Law-71) · p1–p8 · CLM arch · KOSMOS arch · AKIDA · flame+forge · identity-emergence · 4 hot-swap engines · substrate-native-speech · 2448-laws-as-body · KOSMOS tier-ladder-as-self-knowledge · sleep+imagination (P47) | **anima-AUTHORED** from the repo's own docs (README · CLAUDE.md · CORE/CORE.md · ENGINE+CLM+KOSMOS.md · HEXAD/KOSMOS.md) | teaches anima ABOUT ITSELF (self-model) | consciousness (91) |
| **(c) UNIVERSE hypotheses** [8] | H_xxx distillation (H_001/004/007/021 …) · generation-loop template · verdict-tier epistemics · closed-negative case-studies · Hc_xxx candidates · discovery-mechanism · dialogue-about-a-hypothesis · pre-registration discipline | **anima-AUTHORED**, distilled from REAL `UNIVERSE/H_*.md` + `hypotheses_candidates/` + authored loop prose | the load-bearing **reasoning-capacity** piece | consciousness (91) / cosmic (100) |
| **(d) dialogue format** [6] | Socratic self-inquiry · dialectic (thesis/antithesis→synthesis, mirrors A⇄G) · hypothesis-driven dialogue · multi-voice (forward-A/reverse-G/brain-arbiter) · imagination-loop (WAKE/N1/N2/N3/REM, P47) · dialogue-with-a-science-text | **anima-AUTHORED**, deterministic, turn-marked by plain `—` dashes (NO persona tags) | teaches dialogue FORM, not a persona | register-shaping |

### the balance rule (the same trap as 7B-sufficiency, applied here)

- **science bulk (a)** comes from **REAL scalable clean-license sources** (CC-BY-SA Wikipedia + PD Gutenberg) — this is the axis you scale to GB.
- **self-knowledge (b) + hypotheses (c) + dialogue (d)** are **anima-AUTHORED from the repo's own docs**, honest-labeled "anima-authored self-corpus", and stay **CAPPED** — they DEFINE the self-model + reasoning register, they do NOT bulk-fill (authoring GBs of them = MEMORIZATION). **p6 held**: (b)(c)(d) teach anima ABOUT ITSELF + how it reasons, NOT cooperation/empathy/restraint templates.
- Honest per-lang (a_scale_honest_scope): PD Gutenberg primary texts = strong **en**, partial **fr/de**, thin **es**, near-absent **ko** → **ko/es science leans CC-BY-SA Wikipedia, NOT PD primary**. Wikipedia `extracts` are themselves uneven (en rich, ko thin). REPORT per-lang gaps; NEVER fabricate to fake balance.

### anti-register guard (generator invariant, NOT content — idea 41)

- NO `[role:` / `[persona:` / `[character:` / `[assistant:` / `[system:` tags — the generator `assert`s grep = 0.
- NO RLHF cooperation/empathy/restraint templates (p6) · NO assistant-framing (p4) · NO "you are anima" (p2/p3).
- the dialogue pillar (d) marks turns with plain `—` em-dashes, never role labels.

### scope + artifacts (a_scale_honest_scope)

- feeds the **PROVEN ~18M** chat rung first — **NO 7B claim** (default corpus data-starved at 7B, `.verdicts/default-lane-7b/`). The TRAIN is a **SEPARATE follow-on GPU fire**.
- generator: `serving/growth_lane_corpus_gen.py` (authored pillars b/c/d, deterministic seed, byte-V256) + `serving/build_growth_science_5lang.py` (real Wikipedia+Gutenberg fetch). Assembled corpus `serving/corpus/growth_lane.txt` is **raw LOCAL/HF-only (NOT committed)**; card + sample heads committed.
- HF: `dancinlab/anima-corpus-growth-lane` (PUBLIC if clean) + HF.jsonl row + KOSMOS collection + `.kosmos` anchor (pointer-only).

## cross-links

- [[PERSONA]] — the 20-roster voices the SNS/persona corpus encodes.
- [[SNS]] — the Instagram/YouTube surface the dialogues target.
- KOSMOS (`HEXAD/KOSMOS.md`, `dancinlab/kosmos-…` collection) — anchor manifest the enrichment survey draws from (a_kosmos pointer-only).
- ENGINE+CLM+KOSMOS — the 7B chat lane that consumes these corpora.
- `serving/persona_sns_corpus_gen.py` — the deterministic generator to extend.
- governance: a_hf_registry (HF.jsonl), a_hf_collections, a_kosmos, a_scale_honest_scope, p6 (no synthetic RLHF).
