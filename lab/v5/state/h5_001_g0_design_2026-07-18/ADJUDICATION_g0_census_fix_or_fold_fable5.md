# H5_001 G-0 — census 1.0 on hp_k/pos_k: FIX POSSIBLE, builder-side (Fable 5, 2026-07-18)

> **SSOT**: `ARCHITECTURE.json` → `defect-encoding` · `lever.g0-construction`. Seed of record for the
> G-0 census fix (read-only); the build outcome distils into the tree, not this doc.

> Status: ADJUDICATION against the measured per-target census (g0-build,
> `state/h5_001_g0_deleaked_register_2026-07-18/g0_verdict.json`: A1 worst=1.0 all δ, per-target max 1.0
> on hp_k and pos_k, drill+f2d+f1d). Binary call requested: FIX POSSIBLE vs FOLD (K-fold-1-analog).

## 0. The call in one paragraph

**FIX POSSIBLE — and the fix is in the BUILDER, not the census key family.** Neither of the offered
horns is right: the key family is not over-powered (keep presence, count, (g,posbin) exactly as
SPEC §5 registers them — each encodes a priced lesson), and the leak is not irreducible Korean
morphology. The measured 1.0s are the census doing its job on a builder that implements **none of the
three balance mechanisms its own SPEC §2.2/§5 requires**: the constant-시-count invariant is computed
over adverbial sites ONLY (excluding the contested site — directly against §2.2's "total 시-count over
{contested site} ∪ {D adverbial sites} is CONSTANT"), the §5 orbit/involution closure ("closed under
the involution that exchanges the 시-assignment between contested and adverbial sites with gold
recomputed") is entirely absent (`use_si = (j < (d+1)//2)` — a fixed pattern, never crossed against
hp_k), and site isomorphism is partial (ADV_VERBS ∩ VERBS = {웃}; 오/떠나's ±시 forms occur ONLY at
contested sites; the contested verb and the hon noun are deterministic functions of k). The census did
not discover a wall in the lever's reach; it measured the builder's distance from the SPEC. Do not
fold on this number. Implement F-1..F-4 below, re-run, and let the census stamp it.

## 1. Ruling on question 1 (hp_k): "the gram IS the label" — REFUTED at the byte level

The argument conflates a **site-indexed label** with a **location-free byte string**. hp_k=1 is defined
as "시 on the CONTESTED verb of conjunct k" — a role-indexed predicate. The census key cannot condition
on "contested": that predicate is role-selection, which is exactly the node-indexed read SPEC §1
declares NOT-a-leak ("node-indexed readability of hon(i) given the node manifest remains 1.0 and is
not audited"), and exactly one conjunct of the depth-2 composition (role-selection ∧ morpheme-read,
§0) the register exists to force. The measured gram — the stem⊗(으)시 bridge, e.g. 웃으시는 vs 웃는
= 4-gram [9B 83 EC 9C] (웃-tail + 으-head) vs [9B 83 EB 8A] (웃-tail + 는-head) — is label-equivalent
ONLY because the build makes the byte string site-unique:

- `ADV_VERBS = [보이, 웃, 살]` vs contested `VERBS = [웃, 오, 떠나]` (builder :74/:77): 오시는/떠나시는
  can never occur at an adverbial site, so their bridge grams have hp-pure support;
- `use_si` fixed in j (:141): even for the shared stem 웃, no item ever plants 웃으시는 at an adverbial
  site as the orbit partner of an hp=0 contested 웃는 in the same stratum;
- `verb = VERBS[k % 3]`, `hon = hon_pool[k % 6]` (:164-166): site content deterministic in k, so
  (g,posbin) localizes what variety should have smeared.

Under §2.2's site-isomorphism requirement, "no sentence has 시 on the contested verb with hp=0" stays
true but becomes **census-irrelevant**: the balancing sentences realize the SAME bytes at an ADVERBIAL
site (±시 free there by the §3 axiom), and no n≤4 window can tell the two sites apart — the site
discriminator (the following eojeol) is ≥5 bytes from the last 시-byte (는 3B + space 1B; §2.2's own
arithmetic), so no 4-gram contains both a 시-byte and a next-word byte. What DOES certify core-ness is
a conjunction of ≥2 windows across a >4-byte span — outside A1's per-gram family by construction, and
precisely the composition the task wants to leave as the only route to the bit. **Verb-local 시 is the
mechanism, not an irreducible leak (§1); the build failed to camouflage it per its own spec.**

Sub-ruling: **no census key is over-powered.** Count keys guard the §2.2(b) 0.75 trap; posbin guards
H_003/H_004's positional/suffix reads. "Verb-adjacent" keys are NOT in the §5 family and must not be
added — adjacency-to-the-contested-verb presupposes the parse. The n≤4 byte window is the honest,
pre-registered locality notion. (Two census-implementation gaps found while auditing — the shipped
posbin is start-relative only, where §5 registers bins from BOTH ends and relative to "=> ", and the
posbin accumulator votes per occurrence rather than per sentence — both should be fixed with the
builder: the census gets STRONGER, never weaker.)

## 2. Ruling on question 2 (pos_k): the leaking gram CAN be injected by a drilled decoy

"Decoys are DRILLED" (SPEC §3) scopes the register MACHINERY — the phrase shapes, frame words,
adverbial verbs, the decoy-PP constructions. The noun FILLER of a decoy slot is not the recombination
axis; §3's bet is "argument noun lexemes only" as the axis of NOVEL ARGUMENT BINDINGS. And the
disjointness gate (§6) bans held-out lexemes from every DRILL surface — it says nothing about panel
surfaces, where 사장님 already appears verbatim as an argument in every f2d item. Therefore:

- **drill**: balance [X님의]/[X님도] and [P의]/[P도] bridges with decoy PPs whose noun slots draw from
  the DRILLED argument pools (HON6/PLAIN6) — fully allowed today;
- **f2d/f1d**: balance the held-out bridges with decoy PPs on the PANELS' OWN surfaces using the
  held-out lexemes (non-argument outer particles / adjunct positions per §3's axiom). No drill
  exposure is added; the drilled machinery stays drilled; the novel lexeme stays novel in the argument
  role. The census is per-corpus, so per-corpus balance is what A1 requires.

The current builder cannot do this because its decoy pool is the disjoint `DECOY_NIM = [손님, 귀빈,
내빈, 고객, 단골, 행인]` (:80) — of which only 손님 is even 님-final, so the [님의]/[님도] balancing
§2.2 planned barely fires at all, and the argument-noun⊗particle bridges ([사장님의] support 96 = the
pos-half of n=192; the plain-noun [P의]/[P도] bridges likewise) have NO balancer. That is an
incomplete decoy inventory + a pool-scoping choice — not an impossibility. The un-balanceable reading
("decoy slots may only contain DECOY_NIM") is a constraint the SPEC never states.

## 3. The four named build defects → fixes (F-1..F-4)

- **F-1 constant-sum scope**: compute the constant 시-count over {contested site} ∪ {ADV sites} per
  conjunct region (§2.2 letter). Today `si_count_adv` excludes the contested site, so per-conjunct and
  per-sentence 시-counts equal const + hp_k — count keys read hp directly. (The shipped
  `anti_parity_si_count` check passes at 0.0625 because it audits the adv-only invariant — the wrong
  one.)
- **F-2 orbit closure (§5)**: pair every item with its involution partner — exchange the contested
  site's ±시 (and stem, see F-3) with an adverbial site in the SAME conjunct, gold recomputed. This is
  the mechanism that PINS the census at exact 0.5 (§10.1); ε = 1/(2m) covers odd strata only, it never
  covers a missing symmetry.
- **F-3 full site isomorphism**: adverbial verb slots draw from the SAME stem pool as contested RC
  verbs (identical stems ⇒ identical allomorphy, 으시/시). **A3-extended amendment (named)**: "no
  cross-pool stem-syllable sharing" is scoped to the defect it encodes — silent pairing across
  DISTINCT lexemes (A7′). Same-lexeme-across-site-types is not that defect; pool-DISJOINT stems
  actively CREATE an accidental role-selection correlate (stem→site lookup table — H_005's exact
  shape, the thing §1 says must die). Role selection then rests solely on the overt licensor
  (frame word ≤1 eojeol away) — the anti-parity clause §2.2 is untouched.
- **F-4 decoy noun slots = argument lexemes, per corpus**: decoy genitive/도/RC-framed contexts
  (§2.2's own shapes, e.g. "…시는 X님도 아는 모임에서" family) with noun slots drawn from the corpus's
  OWN argument lexeme sets (drilled on drill; held-out on f2d/f1d surfaces only), rates set by the
  crossing so every noun⊗particle bridge AND every [는+space+noun-head] junction gram is
  pos/gold-balanced over its support. Recommended alongside: rotate the hon assignment across k (kill
  `hon_pool[k % 6]` determinism) so each noun's argument support is a proper subset of the corpus and
  decoy placements can sit in argument-free sentences (naturalness; native pass gates).

## 4. What would have been FOLD — and what fold evidence now looks like

FOLD would be correct iff some core n≤4 window is **core-certifying**: a ≤4-byte string that cannot
occur in licensed adjunct space under the opposite label. No such window exists in this grammar:
verb-complex windows are plantable on adverbial/decoy verbs (±시 free by axiom), noun-complex windows
([noun+의/도], [noun+님]) in decoy PPs, junction windows ([시는] bridges, [는_+noun-head]) in decoy
RC-framed contexts — and the verb-side discriminator sits beyond any 4-gram (5-byte gap). The honest
residual risk is **(g,posbin) at fixed-order δ1/δ2**: the involution moves bytes intra-conjunct, and a
bin boundary can split orbit partners. Per-(g,bin) balance is a build-time constraint; if a
fixed-order δ cannot pin, that δ is BUILD-INFEASIBLE (discovered at $0), the candidate window shifts
toward the scrambled settings (δ3–δ5, where site positions are exchangeable), and K-fold-1 fires only
if G-0k then finds no ≥2-consecutive window — the gate's measurement, not this adjudication's.
**If, after F-1..F-4, the census still shows a family at 1.0, THAT gram is real fold evidence** —
bring it back with its byte decode and support, and it gets ruled on. The current 1.0s are not: they
measure builder-vs-SPEC distance. gold_k needs no separate mechanism — gold_0's 1.0 rides the same
per-conjunct determinism, no single n≤4 gram computes hp⊕pos across the ≥10-byte junction span, and
gold stays gated as its own target (18 targets unchanged).

## 5. Re-run criterion (what "stamps it" means)

All 18 targets × full §5 key family (with the posbin census corrected to both-ends + "=>"-relative,
per-sentence votes) ≤ 0.5 + ε (ε = 1/(2m) per §5) on drill + f2d + f1d for every δ ≥ 1, with the A4
exact-balance asserts extended per-(g,bin) where fixed order applies. δ0 stays report-only-FAIL by
design. Nothing in this adjudication touches G-0k's decision rule (§8) — no new δ, no new seed.
