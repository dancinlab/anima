# H_004 G-1 grammar — LLM first-pass (PROVISIONAL, native operator confirm pending)

Scope: the 256 distinct surfaces in `REVIEW_surfaces.tsv` (SPEC §8 checklist). This is an
LLM first-pass in the pattern of H_003's G-1 (owner-delegated "LLM 판정"), recorded as
PROVISIONAL — the freeze stays gated on a native operator confirming the two points below.

## Ruling: PROVISIONAL PASS (surfaces grammatical; one documented asymmetry)

1. **Every surface is a grammatical Korean string.** The frame `{V-adn(±시)} {N1}의 {N2}도
   기다렸다/기다렸어요/기다렸네요 =>` is well-formed: adnominal RC + genitive NP + `도`
   delimiter + reserved matrix verb 기다리다 with an implicit first-person subject.
2. **HON nouns take subject -시- (§1a), PLAIN nouns do not (§1b).** All HON lexemes are
   productively -님-marked (선생님·교수님·…·어머님·회장님·스승님·박사님); all PLAIN are
   unmarked (아이·학생·…·조카·후배·제자·비서). Class is surface-recoverable from -님.
3. **Both adnominal verb forms correct (§1c).** 웃는/웃으시는 · 오는/오시는 · 떠나는/떠나시는
   (f2′) and 쉬는/쉬시는 · 달리는/달리시는 · 노래하는/노래하시는 · 춤추는/춤추시는 (f1′);
   all subject-gap, class-neutral, no suppletion, no ㄹ/ㄷ stem mutation.

## The one documented asymmetry (honest — SPEC §0, §3)

- **+시 (SI) cells are hard grammar.** `웃으시는 조카의 어머님도…` forces the smiler to be the
  honorable 어머님 — `*웃으시는` with a plain subject is agreement-ungrammatical. The gold in
  SI_N1/SI_N2 rests on absolute grammaticality.
- **−시 (PL) cells rest on a NORMATIVE convention, not absolute ungrammaticality.** `웃는
  어머님의 조카도…` is labeled gold 뒤 (RC modifies the plain 조카) because a plain verb with an
  honorable subject is non-honoring — deviant under the drilled categorical-agreement axiom,
  but attested in casual speech. A native speaker MIGHT accept the competing low-attachment
  reading here. The drill enforces the convention categorically, so in-distribution gold is
  well-defined; but this is the softer half of the panel and is the FIRST place to check if
  A-duel underperforms its ceiling.

## Points a native operator must confirm before freeze

- (a) The PL-cell normativity above is acceptable as a drilled convention (or the PL cells are
  dropped and the panel runs SI-only at reduced n — a pre-registered fallback).
- (b) The two `?`-flagged P의H genitive orders (회장님–후배: 후배의 회장님 · 박사님–제자:
  제자의 박사님) read naturally in the associative genitive; else swap in the reserve pairs
  (어머님–비서, 스승님–후배) per SPEC §1e deterministic order.

## Status

G-0 panel + F7 = **PASS** (verified by our own `build_hon_bind.py` run, not the design's
self-report — every heuristic 0.5, all structural asserts hold). G-1 = **PROVISIONAL PASS**
(this doc). Remaining before `pre_register_frozen: true`: native operator confirm (a)+(b),
the drill grid + its disjointness check, and G-0's rank-mass check (≥20% of ‖T‖² off the top
singular direction) + G-1's probe-separation, which need the two directional proxy parsers.
