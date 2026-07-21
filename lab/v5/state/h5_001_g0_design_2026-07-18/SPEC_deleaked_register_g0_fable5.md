# H5_001 G-0 — constructed DELEAKED register: design adjudication + build spec (Fable 5, 2026-07-18)

> Status: DESIGN — absorbs as the G-0 build spec on ratification; distil into `ARCHITECTURE.json`
> (premise.window · lever · defect-encoding.*) and log in CHANGELOG at the implementation commit.
> Every inherited number cited with arm + source (G4). Named disagreements in §10.

## 0. Adjudication in one paragraph

The leak→unlearnable transition is **predicted to be a WINDOW, not a cliff — but only under a specific
construction**, because the census axis and the learnability axis decouple: A1 census is PINNED at exact
0.5 for every δ ≥ δ1 by an exact-balance (orbit/twin) construction, so it is not a graded quantity to be
tuned into band; what δ grades monotonically is REALIZATION VARIETY (identification pressure), and the
G-0k window criterion reduces in practice to "≥2 consecutive δ where the trained control still fits
in-sample ≥ 0.95". The task's minimal sufficient computation stays a depth-2 composition
(role-selection ∧ morpheme-read, then the drilled XOR) at every δ — no operator raises conjunction
order — which is the structural reason to expect graded degradation (window), unlike H_008's
arbitrary-pairing parity (cliff: control in-sample CHANCE at every budget while 16/16 audits green;
`anima-v4/HYPOTHESES/cards/H_008_supervision_budget_sample_efficiency.md`, A7 defect). Three naive
distractor schemes are REJECTED below by closed-form count arithmetic (census 0.75 / 1.0 / 1.0) — each
would have re-created a priced v4 trap; the surviving scheme is constant-시-count marking over
site-isomorphic verb sites with implicit-subject adverbial distractors, plus decoy 님-contexts for the
noun channel.

## 1. The defect, restated mechanically (what A1 must encode)

H_005 K3 (A-χ̂ f2″ 0.8242/0.7096 vs A-hand 1.0/1.0, F1a′ margins −0.1758/−0.2904; arms A-χ̂ / A-hand,
`anima-v4/state/h004_parser_duel_tension_rank_drill_2026-07-16/verdict_g3a.json`) was measured with
G3-0d probe φ→hon = 1.0 held-out n=1200 (frozen-post-CPT-trunk logistic probe, H_005 card:73). The
mechanism of the defect is a SOLUTION-SET failure, not a wrong-answer failure: on the templatic drill
(12 pairs × 9 verbs × 3 tails, `gen_drill_h004.py` predecessor grid), every accidental node-local
feature — lexeme identity, verb identity, template context, position — co-varies with the concord bit,
so MANY χ̂ fit the drill to 1.0 (s0 drill_dacc 1.0, same verdict_g3a.json) and the drill loss cannot
distinguish transferable (morpheme-in-role) solutions from non-transferable (lexical/positional table)
ones. SGD found partially non-transferable ones: 0.82/0.71 held-out. F1a still PASSED
(Δ(A-χ̂ − C-χ̂plc) = 0.2982/0.1914 ≥ 0.15, arms A-χ̂ vs C-χ̂plc, same file) — misidentified, not inert.

Two consequences that shape everything below:

1. **The morpheme channel is the mechanism, not the leak.** -시- on the contested verb and -님 on the
   honorable noun are the PRODUCTIVE channels the task composes (v4 SPEC §4 "drilled-blind disanalogy",
   `SPEC_hon_bind_panel_fable5.md`). They stay on the surface. What must die is every ACCIDENTAL
   correlate: sentence-level n-gram statistics, position, template context, lexical identity beyond 님.
2. **The probe will stay ≈ 1.0 under any deleak that keeps the morphemes** — φ_i pools node i's own
   bytes, and the contested verb node still contains ±시 verbatim. So A2's probe half (≥ 0.90) is
   expected structurally green and carries confirmation value only (consistent with the card's honest
   limit 3); the LIVE learnability conjunct at G-0k is the control in-sample fit ≥ 0.95. Named as a
   sharpening in §10.

Census target, therefore: **sentence-level n-gram features must not predict the binding bits**
(gold_k, hp_k, pos_k — 18 bit-targets per sentence), while node-indexed readability of hon(i) given the
node manifest remains 1.0 and is not audited as a leak. This is the defect-encoding form (standing G2):
a table-lookup fit of the drill becomes impossible, so every drill-fitting χ̂ must bind
morpheme-to-role — the identifying pressure H_005's register lacked.

## 2. The four operators, adjudicated (with the closed-form traps)

### 2.1 Paraphrase frames — REQUIRED, but not for the census (dilution theorem)

The census is CONDITIONAL: each n-gram g is scored majority-by-key over its OWN support. Spreading a
leaky gram across N frames leaves its per-support predictiveness UNCHANGED — if g occurs only in frame
f and is biased b within f, its census score is b at any N. **Paraphrase can never fix A1; only exact
balance within every gram's support can** (the arithmetic the prompt asked for: there is no N at which
dilution helps, because the census never marginalizes over frames). Paraphrase's real job is
identification pressure: it prunes template-keyed and context-keyed members of the χ̂ solution set.
Modest F (2–8 frames) suffices; balance-within-frame is asserted exactly (A4).

### 2.2 Distractor honorific material — REQUIRED; the census engine; three schemes REJECTED by count

Let hp = hp_k of the contested verb, gold_flip = 1 ⊕ hp ⊕ (pos−1) (gold formula,
`build_hon_bind.py` / SPEC §3). Distractor = an extra verb site carrying ±시. Exact-count results:

- **REJECTED (a): same-pair-licensed distractor** (an inner RC on N_k2, ±시 forced by N_k2's visible
  class under the categorical axiom). Then distractor-시 ⟺ pos=2, so per-conjunct 시-count
  c = hp + 1[pos=2] and gold_flip = 1[c ≠ 1] EXACTLY: c=0 → (0,N1) → 뒤; c=2 → (1,N2) → 뒤;
  c=1 → 앞. **The 시-count is a PERFECT gold predictor (census 1.0).** This is H_008's A7 shape —
  an audit-satisfying build whose only solution is pathological — re-created on the register axis.
- **REJECTED (b): independent balanced distractor** (own subject, class drawn 50/50 ⊥ hp). c = hp + B,
  B ~ Bernoulli(0.5): c=0 certifies hp=0, c=2 certifies hp=1, c=1 is uninformative — majority-by-count
  census = 0.25·1 + 0.25·1 + 0.5·0.5 = **0.75**. Fails A1 at any ε < 0.25. Generalizes: any
  independent-marking scheme leaks through count tails.
- **REJECTED (c): complementary marking with an overt distractor subject** (distractor-시 := ¬hp,
  licensed by giving it an honorable subject iff 시). The bit RELOCATES into the subject's visible
  class: the 4-byte gram [님(3 bytes) + first byte of the following particle] — 과(0xEA…) vs 이/의/도 —
  reads the distractor's class, hence ¬hp, at census **≈ 1.0**. Every deterministic scheme that
  licenses the distractor's 시 with a VISIBLE noun copies the bit to that noun's 님.

**ACCEPTED scheme — constant-count marking over site-isomorphic sites with implicit subjects:**

- 시-side distractors are **adverbial clauses with implicit (pro-dropped) subjects** — e.g.
  "쉬시는 동안" / "쉬는 동안" — where ±시 honors a discourse subject not on the surface. The drill
  grammar STIPULATES (axiom extension, §3): adverbial-clause ±시 is free, licensed either way, and
  never enters any gold bit. Truth conditions of the measured concord are untouched. Native reviewer
  confirms naturalness (G-1-style checklist carried).
- **Marking balance**: per conjunct region, total 시-count over {contested site} ∪ {D adverbial sites}
  is CONSTANT (pre-registered per δ), assigned by the deterministic crossing so that the distractor
  bit-vector is exchangeable across sites and jointly ⊥ (hp_k, pos_k) after conditioning on the
  constant sum. Count keys then have single-valued support (uninformative); presence keys are
  corpus-constant.
- **Site isomorphism**: the adverbial verb pool = drawn from the same morphological family as
  contested RC verbs (adnominal -는/-(으)시는 forms), so every ≤4-byte gram inside and at the
  junction of a 시-verb is realized at both site types with matched counts. The residual discriminator
  (the following eojeol's particle/frame word) sits ≥ 10 bytes downstream of the 시 bytes
  (는 3B + space 1B + noun/frame ≥ 6B) — beyond n≤4 reach. The census VERIFIES this rather than
  trusting it (that is A1's whole job).
- **님-side (pos_k) decoys**: the templatic register leaks pos_k at n=4 via [님 + 의-first-byte] vs
  [님 + 도-first-byte]. Balance by decoy 님-contexts inside adjunct material: decoy genitives
  ("사장님의 사무실에서") supplying [님의] with a plain head, and decoy 도-contexts (e.g. RC-framed
  "회장님도 아시는 모임에서") supplying [님도] — rates set by the crossing so each such gram's support
  is exactly gold/pos-balanced. Candidate strings go through the native pass; the census gates the
  result.

Learnability of the accepted scheme is NOT parity-shaped: role-selection (is this 시-verb the RC over
the contested edge, or an adverbial?) is decided by an OVERT LOCAL LICENSOR — the adverbial's frame
word (동안/때/후에…) immediately follows it; the contested RC immediately precedes the genitive pair.
**Anti-parity clause (binding, carried into the builder as an assert): every distractor/adjunct
carries an overt marker making its role deterministic from ≤ 1 adjacent eojeol.** H_008's parity had
no local cue by construction (arbitrary silent syllable pairing); this design keeps every predicate of
the depth-2 composition locally decidable — the composition itself (predicating the 시-feature OF a
noun slot across the contested edge) remains the task.

### 2.3 Licensed word-order alternation — RESTRICTED to adjunct placement

The contested core **[V-adn(±시) N_k1의 N_k2도] stays contiguous and order-frozen**: adnominal-before-
head is hard Korean grammar, and the H의P↔P의H within-pair swap IS the counterbalance machinery
(SPEC §2) — both survive untouched. The licensed alternation is ADJUNCT scrambling: adverbial/decoy
phrases permute among their allowed slots (before their conjunct's core; matrix-level adjuncts in
frame-defined positions). This kills position-indexed n-gram keys without breaking:
- **swap-alignment**: within-(pair, verb) the four cells still differ only in ±시 and noun order
  inside the frozen core;
- **the scoring machinery**: answer region is located per-item at base = len(surface bytes)
  (`train_h004.py _dacc_item`) — no fixed offsets anywhere in the metric;
- **the node machinery**, PROVIDED it is made manifest-driven (§6): v4 hard-codes n = 3K+2
  (`_hon_n`, `_node_of_byte` assert) and fixed head arithmetic (`build_tension._heads`: contested
  r→r+1 vs r→r+2). With adjunct eojeols, n varies per item ⇒ the generator emits `node_roles` +
  `support_edges` per item; the harness builds t_struct from the manifest; a closed-form audit
  re-derives edges from the surface and asserts equality.

### 2.4 Position jitter — REQUIRED but implemented as MEANINGFUL variation, not padding

Jitter = varying adjunct COUNT and LENGTH (and frame-varied matrix material incl. pre-tail adverbs),
never semantically empty filler (a native reviewer would flag padding; decoys already do the work).
It defeats the position-binned census family — which MUST include bins from the sentence END and
relative to the answer marker "=> " (v4's suffix lesson: H_003/H_004 read leaks from the end;
`SPEC_hon_bind_panel_fable5.md` §4.5). Length becomes variable ⇒ char-length is a live census key:
jitter level is a crossing dimension held exactly ⊥ gold (A4 asserts char-len majority ≤ 0.5+ε).

**Ranking**: 2.2 distractors+balance (census engine, required) > 2.1 frames (identification pressure,
required) > 2.4 jitter-as-variation (kills positional keys, cheap) > 2.3 adjunct scrambling (marginal
extra pressure, moderate machinery cost — included because the manifest refactor pays for it once).
께서-class material (founding design §2 mentions it) is EXCLUDED from v5's grammar: honorific
nominative on decoy subjects re-opens the (c)-relocation channel and complicates the axiom for no
census gain. Named in §10.

## 3. The register grammar (shape only; strings finalized in the builder + native pass)

Conjunct region k (K = 6, one answer slot each, answer convention 앞/뒤 unchanged):

```
[ADV_k,1 … ADV_k,D]  [V-adn(±시_k) N_k1의 N_k2도]        (core order-frozen; ADVs scramble at δ≥3)
```

- ADV = adverbial clause "V-adn(±시') FRAMEWORD" (implicit subject; ±시' free by axiom extension) or
  decoy-님 phrase (decoy genitive / decoy 도-context inside a clearly-adjunct PP).
- Matrix material: F paraphrase frames over the matrix verb region (기다리다-family register variants +
  pre-tail adverbs), drilled; one frame variant HELD OUT for the f1-analog liveness panel.
- **Axiom extension (pre-registered grammar stipulation)**: categorical -시- ⟺ honorable subject holds
  for every OVERT-subject clause (v4 axiom carried); adverbial clauses with implicit subjects carry
  free ±시, licensed either way, never entering gold. All decoy 님-nouns take only non-argument
  particles within their adjunct.
- Pools: argument HON/PLAIN pools and their drill/held-out split carried structurally from v4 SPEC §1
  (6+6 held-out, substring-disjoint — A3 verbatim); NEW pools (adverbial verbs, frame words, decoy
  nouns) are all DRILLED (register machinery is drilled; the recombination axis stays "argument noun
  lexemes only", matching v4's bet). A3 extended: no cross-pool stem-syllable sharing (님/시/는
  morphemes exempt — productive markers), pools non-corpus, verified by direct census.

## 4. The δ dial (≥5 spaced settings, monotone in variety; census pinned from δ1)

| δ | frames F | distractors | order | jitter | role |
|---|---|---|---|---|---|
| δ0 | 1 | none | fixed | none | templatic anchor — census FAILS by design; report-only; verifies the machinery reproduces v4-like control fit (expected ≈ 1.0 in-sample, cf. A-hand precond drill 1.0/1.0, `train_result_full.json`) |
| δ1 | 2 | D=2 sites/conjunct, constant 시-count, decoy-님 on | fixed | none | minimal census-clean point |
| δ2 | 4 | same | fixed | none | + paraphrase pressure |
| δ3 | 4 | same | adjunct scrambling ON | none | + positional decorrelation |
| δ4 | 4 | D ∈ {1..3} balanced | scrambling | adjunct count/length varies | + jitter |
| δ5 | 8 | D ∈ {1..3} | scrambling | full | max variety |

- **Monotonicity, honestly restated**: the GATED census (n ≤ 4) is ≤ 0.5+ε at every δ ≥ δ1 by
  construction — it does not "decrease". What decreases monotonically is the extended-radius leak
  profile (n = 5..8 census, REPORT-ONLY) and the exploitability of any fixed-position read; what
  increases is realization variety. G-0k's criterion applies verbatim: census green (structural),
  probe green (expected ≈ 1.0, confirmation), and the window is carved by in-sample fit.
- **Window prediction**: δ1 is designed to be the easiest fully-deleaked setting (small F, fixed
  order, no jitter — variety ≈ 4× templatic), and each step adds ONE operator increment. Since the
  composition order never rises and every added predicate is locally licensed, in-sample fit should
  degrade gradually if at all ⇒ ≥ 2 consecutive green settings expected. **Fold condition stays
  live**: if even δ1's control cannot fit in-sample ≥ 0.95, leak-freedom and learnability touch on
  this substrate ⇒ K-fold-1 at ~$0, exactly as pre-registered.
- **Named residual cliff risks** (what would make it a cliff despite the argument): (i) a
  marking-balance bug at one δ — census catches it at BUILD time (exit-blocking, all δ audited before
  any training), so it cannot masquerade as a physics cliff; (ii) drill-size-vs-variety memorization
  crunch — at fixed n_drill, δ5's variety may exceed what 3.7M fits by rule, producing a real knee
  between δ4/δ5: acceptable, that is what G-0k measures; (iii) role-licensor too weak (adverbial
  frame word rare in drill) — mitigated by frame words being high-frequency closed-class items
  appearing thousands of times.

## 5. A1 census — feature family + ε arithmetic (exact-balance, not sampling)

- **Targets** (per sentence, surface bytes only, answer region excluded): gold_k, hp_k, pos_k for
  k = 0..5 — 18 bits. Audited on drill grid AND both panels, per δ.
- **Keys**, for every byte n-gram g, n ∈ {1,2,3,4}: presence(g), count(g), and (g, position-bin) with
  8 bins computed from BOTH ends and relative to "=> ". Score = majority-by-key (max(s, 1−s) form —
  anti-correlated cues equally leaky, H_003 lesson).
- **Gate**: over all g with support m(g) ≥ m_min: score ≤ 0.5 + ε. Sub-m_min grams: REPORTED
  (top-20 deviations) and COVERED by the exact structural asserts (A4: per-lexeme, per-frame,
  per-adjunct-pattern, per-jitter-level, per-cell gold balance == 0.5 EXACT; this closure is what
  licenses the m_min cutoff — without it rare-gram families would be a hole).
- **ε derivation** (replaces the 0.05 placeholder): the corpus is generated as a deterministic
  mixed-radix crossing (rot × msg × frame × distractor-pattern × jitter-level …), closed under the
  involution that exchanges the 시-assignment between contested and adverbial sites with gold
  recomputed — so every gram's support is balanced by symmetry and deviations arise ONLY from
  odd-sized strata: |score − 0.5| ≤ 1/(2m). With m_min = 24 (the smallest designed crossing cell on
  the n=192 panel): **ε = 1/(2·24) ≈ 0.021** (panels); drill (min cell ≥ 64): **ε_drill = 1/128
  ≈ 0.008**. Pre-registered; the builder does NOT sample (H_008's first SWAP-XOR-B build failed A3 at
  worst-byte 0.677 from random sampling — the priced lesson), and stdlib determinism is v4's builder
  convention carried (no `random`, full nested loops).

## 6. Regenerated panel (nothing inherited; every number an audit OUTPUT)

- **Panel names**: `f2d` (verdict, held-out argument lexemes) and `f1d` (liveness, drilled lexemes ×
  held-out frame variant) — PANEL names per G4, chosen to avoid prime-stacking with v4's f2″.
  n(f2d) = 192 (48/cell; σ = √(.25/192) = 0.036 — v4's F3 arithmetic carries), n(f1d) = 64.
- **Codebook**: KEEP the [6,3] GF(4)-MDS strength-2 OA (`build_honbind_multi.py` `_codeword`) — it
  operates on cell assignments, orthogonal to surface realization; changing it would be a second
  lever. Cross-slot pairwise-dev audit re-run on emitted items (expect 0.0; cite fresh).
- **Free slots**: RECOMPUTED by `_panel_free_slots` logic run as a G-0 audit on the emitted gold
  patterns. Expected {0,1,2,4} (the gold map cell→bit is unchanged), but the set is an OUTPUT — if
  any realization coupling changes it, the audit says so before anything trains.
- **Field-blind ceiling**: RECOMPUTED closed-form from the recomputed free set: all-slot
  teacher-forced blind ceiling = (|free|·0.5 + |det|·1.0)/6 (expected 0.667 — cited fresh, never
  inherited); free-only scoring floor = 0.5 (the metric of record). GF(2)-rank + length-parity audit
  re-run (standing G3).
- **Realization ⊥ codeword**: frame/distractor/jitter coordinates are crossing dimensions enumerated
  independently of (rot, msg) — asserted by construction AND caught by census/pairwise audits if
  violated (a realization coupled to the codeword is a new determinism channel).
- **Node/support machinery (the one required harness change)**: items carry `node_roles`
  (eojeol index → {CONTESTED_V, N1, N2, ADV, DECOY, TAIL, ANS}) and `support_edges`
  (head_a/head_g per node; contested ONLY at the K RC edges; adjunct-internal edges agree in both
  parses). Harness builds t_struct and the hand χ from the manifest (hand field extends over adjunct
  nodes naturally — hon known at generation). Audit A-sup: re-derive edges from the surface
  deterministically and assert == emitted. Pre-run F4 off-top recomputed on sample T (v4 pre-run
  0.8333, `build_honbind_multi.py` header — recompute, expect same order).
- **Disjointness**: held-out argument lexemes + held-out frame variant absent (substring) from every
  drill surface — F7-style exit-blocking assert, extended over the new pools.

## 7. G-0 build spec — `state/h5_001_g0_deleaked_register_<date>/build_deleaked_register.py`

Stdlib-only, deterministic, no `random`, exit code = audit AND. Products, per δ ∈ {0..5}
(δ0 report-only, excluded from the pass conjunction):

- `grammar_d{δ}.json` — frames, pools, marking scheme, crossing dims (the frozen grammar of record)
- `drill_grid_d{δ}.json` · `panel_f2d_d{δ}.json` · `panel_f1d_d{δ}.json` — items with full schema:
  v4 keys carried (`surface`, `gold_pattern`, `gold_flips`, `cells`, `conjuncts`, `rot`, `msg`) +
  NEW `node_roles`, `support_edges`, `frame_id`, `distractor_pattern`, `jitter_level`, `char_len`
- `heldout_manifest.json` — pools + splits + reserve lists (gen_drill imports it; disjointness
  re-asserted downstream, v4 interface carried)
- `audit_report_d{δ}.json` + `REVIEW_surfaces_d{δ}.tsv` (native pass; one line per distinct surface
  with gloss + flags — G-1 checklist carried from v4 SPEC §8, extended: adverbial-시 naturalness,
  decoy-phrase naturalness, role-licensor overtness)
- top-level `g0_verdict.json` — verbatim-printable verdict

Exit-0 requires, for every δ ≥ 1, on drill + f2d + f1d:
A1 (18 targets × full key family, ε per §5) · A3 (pool construction, direct census) · A4 (exact
balance/liveness asserts incl. char-len, cell counts, answer-token absence, negator absence) ·
codebook GF(2)-rank + length-parity · free-slot recompute + ceiling recompute · A-sup manifest/edge
consistency · disjointness · anti-parity licensor assert (§2.2). The census code is unit-tested
against planted-leak fixtures (a known 0.75 count-leak corpus must FAIL it) BEFORE G-0k — the
collector-frozen discipline (H_008 pattern, anima-v4 commit e1b2a00).

## 8. G-0k measurement recipe (~5h MPS, $0; the mount/fold referee)

- **CPT: 2 total (seed 0/1), SHARED across all δ.** Deviation from the card's per-δ wording, argued:
  CPT is NSMC-only (`train_g3a.py:342` — `_nsmc_lines(120000)`, 512-window), byte-stream identical
  across δ; per-δ CPTs would add seed noise and ~2h for zero information. The φ-encoder of record is
  the frozen post-CPT trunk (train_g3a `phi_enc`), unchanged.
- Per (δ ∈ {1..5} × seed ∈ {0,1}), from the shared CPT checkpoint:
  1. **A1 census** — already computed at build; re-verified from the shipped JSONs (closed-form).
  2. **Probe** — logistic φ→hon per node over contested-verb + argument-noun nodes, held-out-lexeme
     split, n = 1200 nodes (G3-0d recipe, H_005 card:71); bar ≥ 0.90. Expected ≈ 1.0 (own-node
     bytes); its content is "pooling preserved the morpheme", i.e. build-gate confirmation.
  3. **Control in-sample** — C-scaf-configuration (struct channel present, T̂ ≡ 0 — the same config
     G-1's C-trained anchors) drilled from the CPT checkpoint on `drill_grid_d{δ}`, v4 drill recipe
     (answer-region up-weighted CE, `_drill_batch` amask lesson), early-stop permitted at sustained
     in-sample free-slot d_acc ≥ 0.98; bar: **in-sample ≥ 0.95**. ~25 min each × 10 runs ≈ 4.5h.
- **Decision (verbatim from the card, no amendment)**: window = ≥ 2 CONSECUTIVE δ with census ≤ 0.5+ε
  AND in-sample ≥ 0.95 AND probe ≥ 0.90, both seeds. δ* = the easier in-window setting. No window ⇒
  K-fold-1, v5 folds at ~$0. **No δ6, no midpoint insertion, no third seed** after seeing data.
- **Foreshadowed G-1 tension, recorded now**: a field-less control that fits the deleaked drill
  in-sample may ALSO generalize (H_007's saturation: C-scaf 0.8073/0.9531, C-dup 1.0000/0.9323,
  `state/h007_.../verdict_g2.json` via CAMPAIGN_RESULT §3) — if C-trained f2d > 0.80 at δ*, G-1's
  ceiling half fails and the single pre-registered retreat (other in-window δ) applies. G-0k does not
  and must not pre-tune against this; it is G-1's measurement.

## 9. Trap ledger (each entry: mistake → the v4 price it would repeat → the guard here)

1. Same-pair-licensed distractor → H_008 A7 parity/pathological-solution (control at CHANCE, 16/16
   audits green) → §2.2(a) arithmetic + A1 count keys + A2 co-certification.
2. Independent distractor marking → census 0.75 sentence-level shortcut (a NEW leak, H_005-shaped) →
   constant-count marking + count keys gated.
3. Complementary marking with overt licensor → bit relocation into [님+particle] 4-gram → implicit-
   subject adverbials + decoy-님 balancing + the census verifying, not assuming.
4. Inheriting free slots / ceiling / balance sets → H_004's 0.667 field-blind ceiling + H_007's
   frozen-anchor failure → §6: every metric object recomputed as an audit OUTPUT.
5. Fixed-offset assumptions (n = 3K+2, `_heads` arithmetic) surviving into the jittered register →
   silent mis-scored panels → manifest-driven nodes/support + A-sup equality audit.
6. Random sampling in the builder → H_008's first SWAP-XOR-B A3 failure (worst-byte 0.677) →
   deterministic mixed-radix crossing, orbit-closed; ε from odd-stratum arithmetic only.
7. Rare-gram census hole (m < m_min each perfectly predictive) → memorization leak invisible to the
   gate → exact per-stratum balance asserts (A4) close the family; top-deviation report.
8. Treating probe ≥ 0.90 as live learnability evidence under deleak → a green conjunct with no
   content → §1: in-sample carries A2; probe demoted to confirmation (card honest-limit 3, sharpened).
9. Realization coordinates coupled to the codeword → new determinism ceiling → crossing-independence
   assert + GF(2)/pairwise audits recomputed on emitted items.
10. δ-fishing after G-0k data → H_007 rescue-fragility / H_008 8-drill cap lessons → decision rule
    frozen verbatim in §8; retreat only as pre-registered in the card.

## 10. Named disagreements (no-unverified-average rule)

1. **Against "δ↑ ⇒ census ↓" as the dial's definition** (H5_001 card, Deliverable framing): a register
   whose gated census FALLS gradually with δ is build-defective at low δ (leaky settings can never be
   in-window, so they waste dial positions and G5 consecutiveness). The census must be PINNED ≤ 0.5+ε
   at every candidate δ by construction; δ dials variety/identification-pressure, with the n=5..8
   report-only census as the measurable monotone leak-profile. The card's G-0k criterion is satisfied
   verbatim either way — this changes what δ means, not what G-0k requires.
2. **Against probe ≥ 0.90 carrying learnability content here** (card A2 wording reads as a live
   conjunct): under any morpheme-preserving deleak the probe is structurally ≈ 1.0; the live A2 teeth
   are the control in-sample fit. Kept as a gate (it can still catch a pooling/build bug), scoped as
   confirmation.
3. **Against 께서-class distractor material** (founding design §2 lists it): honorific nominative on
   decoy subjects re-opens the §2.2(c) relocation channel and complicates the categorical axiom;
   excluded from v5's grammar. If a future card wants it, it is a new register variant, not a δ knob.
4. **Correction absorbed** (founding doc §6 carried): the H_008 en-route citation is k=96 =
   0.651/0.6875 (re-instrumented reads REPLACED phase-a's 0.7448; `verdict_g1_5.json`), never 0.74.
