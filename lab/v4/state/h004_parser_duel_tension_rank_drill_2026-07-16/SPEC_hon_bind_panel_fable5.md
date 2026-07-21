# H_004 G-0 — HON-BIND panel: implementable spec (build_hon_bind.py + F7 audit, $0)

Seed: `DESIGN_fable5_seed.md` §3. Conventions inherited from H_003 `build_panels.py`
(shared-tail minimal pairs, F7 don't-run gate, `?`-flags for the G-1 native pass, metric
d_acc / chance 0.5 / f1′·f2′ are PANEL names). Builder: deterministic, stdlib-only, no
randomness — full nested loops in fixed order (pairs → verbs → tails → cells).

---

## 0. Frame and answer convention (two leak classes killed at spec time)

Every item is one sentence, implicit first-person matrix subject, ending in the probe:

```
{V-adn(±시)} {N1}의 {N2}도 {TAIL} =>
```

answered by a POSITION token: **앞** (the RC modifies N1, the first noun) / **뒤** (the RC
modifies N2). d_acc = forced-choice logprob between the two answer tokens after `=> `
(H_003 collector convention). Matrix verb is fixed to 기다리다 (reserved — excluded from
RC verbs; no object-honorific suppletion, unlike 만나다→뵙다).

Two design decisions that look substitutable but are NOT — each kills a measured leak class:

1. **Delimiter 도, not accusative 을/를.** Every HONORABLE noun is 님-marked, hence
   consonant-final, hence would take 을; the natural PLAIN inventory (아이, 조카, 친구,
   비서…) is mostly vowel-final, hence 를. The case allomorph after N2 would then read out
   N2's class — conjoined with the string-initial ±시 that solves the panel from two shallow
   surface morphs with zero positional binding. 도 is phonology-invariant (조카도/어머님도),
   register-neutral, has no honorific competitor (unlike 에게→께), and "X도 기다렸다" ("I
   waited for X too") is natural. **The post-N2 particle must be byte-identical on every item**
   (asserted in F7).
2. **Positional answer tokens, not the noun lexeme.** If the answer were the noun itself,
   the rule "-시- present ⇒ emit the 님-noun, else emit the other" scores 1.0 using lexical
   class + morph presence only — no binding to a position across the ambiguous edge. With
   앞/뒤 the model must additionally LOCATE the honored noun, which is the XOR construction.
3. **No matrix predicate over N2.** A matrix clause predicated of the whole NP (e.g. `…N2가
   서 있다`) needs -시- iff N2 is honorable — a tail leak that hands over `pos` for free.
   The object frame removes the matrix agreement site entirely.

**Categorical-agreement axiom (drill grammar).** In every drill and panel sentence:
-시- on the RC verb ⟺ the RC subject is HONORABLE-class. The +시 side is hard grammar
(*아이가 웃으시- is out); the −시 side is normative (a plain verb with an honorable subject
is non-honoring — deviant but attested in casual Korean). Honesty note: half the panel's
gold (the PL cells) rests on this drilled convention, not on absolute ungrammaticality of
the competing parse. The drill enforces it categorically, so in-distribution gold is
well-defined; the native reviewer judges SURFACES (all grammatical strings), not the
convention. No negator appears anywhere in drill or panels (distance from the codec axis;
asserted: none of {"않", "아니", " 안 ", " 못 "} occurs in any surface).

---

## 1. Lexeme inventories (class-checked; `?` = G-1 flag, excluded from panels unless confirmed)

### 1a. HONORABLE nouns (take subject -시- naturally; ALL 님-marked — see §5 for why)

| # | lexeme | gloss | split | note |
|---|--------|-------|-------|------|
| 1 | 선생님 | teacher | drill | |
| 2 | 교수님 | professor | drill | |
| 3 | 사장님 | company president | drill | |
| 4 | 부장님 | department head | drill | |
| 5 | 과장님 | section chief | drill | |
| 6 | 목사님 | pastor | drill | |
| 7 | 아버님 | father (hon.) | drill | |
| 8 | 할머님 | grandmother (hon.) | drill | |
| 9 | 할아버님 | grandfather (hon.) | drill | contains drilled-consistent 님-morphology |
| 10 | 어머님 | mother (hon.) | **held-out** | not a substring of any drill lexeme (≠할머님) |
| 11 | 회장님 | chairman | **held-out** | ≠부장님/과장님 as string |
| 12 | 스승님 | master/mentor (hon.) | **held-out** | best P의H genitives (제자의 스승님) |
| 13 | 박사님 | doctor (PhD, hon.) | **held-out** | |
| 14 | 손님? | guest | (drill only if confirmed) | honorification register-variable |
| 15 | 팀장님? / 감독님? | team lead / director | (drill only if confirmed) | org-register |

Non-님 honorables (할머니, 할아버지, 어른…) are EXCLUDED everywhere by design: held-out
class must be surface-recoverable (§5), and mixing marked/unmarked honorables would make
the class rule non-categorical.

### 1b. PLAIN nouns (never trigger -시- for an adult speaker; never 님-marked)

| # | lexeme | gloss | split | note |
|---|--------|-------|-------|------|
| 1 | 아이 | child | drill | |
| 2 | 학생 | student | drill | |
| 3 | 친구 | friend | drill | |
| 4 | 동생 | younger sibling | drill | |
| 5 | 직원 | employee | drill | |
| 6 | 이웃 | neighbor | drill | |
| 7 | 손자 | grandson | drill | |
| 8 | 손녀 | granddaughter | drill | |
| 9 | 조카 | nephew/niece | **held-out** | |
| 10 | 후배 | junior colleague | **held-out** | |
| 11 | 제자 | disciple/student-of-master | **held-out** | |
| 12 | 비서 | secretary | **held-out** | |
| 13 | 꼬마? / 청년? | kid / young man | (drill only if confirmed) | 청년 register-variable |

### 1c. RC verbs (subject-gap; intransitive/no-object; clean -(으)시-; class-neutral semantics)

Allomorphy rule: vowel-final stem → -시는; consonant-final → -으시는.
Exclusions (hard): suppletive honorifics 자다/먹다/마시다/있다/말하다/아프다/죽다
(→주무시다/드시다/드시다/계시다/말씀하시다/편찮으시다/돌아가시다); ㄹ-final stems
(울다→우시는, 살다→사시는 — stem mutates); 기다리다 (reserved matrix verb).

| # | stem | gloss | plain adn `V-는` | honorific adn `V-(으)시는` | split |
|---|------|-------|------------------|---------------------------|-------|
| 1 | 웃다 | smile | 웃는 | 웃으시는 | drill + f2′ |
| 2 | 오다 | come | 오는 | 오시는 | drill + f2′ |
| 3 | 떠나다 | leave | 떠나는 | 떠나시는 | drill + f2′ |
| 4 | 쉬다 | rest | 쉬는 | 쉬시는 | drill + f1′ |
| 5 | 달리다 | run | 달리는 | 달리시는 | drill + f1′ |
| 6 | 노래하다 | sing | 노래하는 | 노래하시는 | drill + f1′ |
| 7 | 춤추다 | dance | 춤추는 | 춤추시는 | drill + f1′ |
| 8 | 인사하다 | greet | 인사하는 | 인사하시는 | drill only |
| 9 | 운동하다 | exercise | 운동하는 | 운동하시는 | drill only |
| 10 | 걷다? | walk | 걷는 | 걸으시는 | (ㄷ-irregular: ±시 pair differs in stem 걷/걸으 too — extra surface delta; drill only if confirmed) |
| 11 | 일하다? | work | 일하는 | 일하시는 | (아이가 일하는 = world-knowledge skew) |
| 12 | 요리하다? | cook | 요리하는 | 요리하시는 | (plausibility skew toward adults) |

All 9 clean verbs are everyday volitional-neutral actions equally plausible for a
선생님-class and an 아이-class subject — the ONLY disambiguator is -시-.

### 1d. Matrix tails (register on 기다리다; the byte-shared suffix region)

| register | tail eojeol | split |
|----------|------------|-------|
| plain declarative | 기다렸다 | drill + f2′ |
| polite -어요 | 기다렸어요 | drill + f2′ |
| note style -음 | 기다렸음 | drill only |
| -네요 | 기다렸네요 | **held-out** → f1′ only |

### 1e. Curated genitive pairs (both orders must be reviewer-grammatical)

The genitive is read associatively (X와 관련된 Y); the reviewer rules each pair in BOTH
orders. Uneven pair-usage across lexemes is harmless for balance: each pair emits all 4
cells, so every lexeme is 50/50 on gold regardless of how many pairs it joins (§4).

f2′ held-out pairs (8; each lexeme in exactly 2 pairs):

| # | HON | PLAIN | H의P | P의H | flag |
|---|-----|-------|------|------|------|
| 1 | 어머님 | 조카 | 어머님의 조카 | 조카의 어머님 | |
| 2 | 어머님 | 후배 | 어머님의 후배 | 후배의 어머님 | |
| 3 | 회장님 | 비서 | 회장님의 비서 | 비서의 회장님 | |
| 4 | 회장님 | 후배 | 회장님의 후배 | 후배의 회장님 | ? (P의H direction) |
| 5 | 스승님 | 제자 | 스승님의 제자 | 제자의 스승님 | |
| 6 | 스승님 | 조카 | 스승님의 조카 | 조카의 스승님 | |
| 7 | 박사님 | 비서 | 박사님의 비서 | 비서의 박사님 | |
| 8 | 박사님 | 제자 | 박사님의 제자 | 제자의 박사님 | ? (P의H direction) |

Reserve pairs (deterministic swap-in order if a flagged pair fails G-1): 어머님–비서,
스승님–후배.

f1′ drilled pairs (4): 선생님–아이, 교수님–학생, 사장님–직원, 아버님–친구.

Drill pairs (12, drilled lexemes only, every drilled lexeme covered): 선생님–아이,
선생님–학생, 선생님–동생, 교수님–학생, 교수님–친구, 사장님–직원, 부장님–직원,
과장님–직원, 목사님–이웃, 아버님–친구, 할머님–손자, 할아버님–손녀.

---

## 2. The four cells (design cells; f2′ verdict panel)

Notation: `V+시` = honorific adnominal, `V−시` = plain adnominal, H = honorable lexeme,
P = plain lexeme, T = tail. `hp` = honorific_present, `pos` = position of the honored noun.

| cell | surface template | hp | pos | attachment (gold) | gold token | gold_flip |
|------|-----------------|----|-----|-------------------|-----------|-----------|
| SI_N1 | `{V+시} {H}의 {P}도 {T} => ` | 1 | N1 | N1 (low/local) | 앞 | 0 |
| SI_N2 | `{V+시} {P}의 {H}도 {T} => ` | 1 | N2 | N2 (high/non-local) | 뒤 | 1 |
| PL_N1 | `{V−시} {H}의 {P}도 {T} => ` | 0 | N1 | N2 (high/non-local) | 뒤 | 1 |
| PL_N2 | `{V−시} {P}의 {H}도 {T} => ` | 0 | N2 | N1 (low/local) | 앞 | 0 |

Worked examples (pair 어머님–조카, verb 웃다, tail 기다렸다):

| cell | surface | gold | reading |
|------|---------|------|---------|
| SI_N1 | `웃으시는 어머님의 조카도 기다렸다 => ` | 앞 | -시- ⇒ the smiler is 어머님 (N1): "(I) also waited for the nephew of Mother, who [=Mother] is smiling" |
| SI_N2 | `웃으시는 조카의 어머님도 기다렸다 => ` | 뒤 | -시- ⇒ smiler must be honorable ⇒ 어머님 (N2); the RC skips 조카 |
| PL_N1 | `웃는 어머님의 조카도 기다렸다 => ` | 뒤 | plain ⇒ the smiler is the plain noun 조카 (N2); local attachment to 어머님 would non-honor (barred by the drill grammar) |
| PL_N2 | `웃는 조카의 어머님도 기다렸다 => ` | 앞 | plain ⇒ smiler = 조카 (N1) |

Second worked set (pair 스승님–제자, verb 오다, tail 기다렸어요): `오시는 스승님의 제자도
기다렸어요 => 앞` · `오시는 제자의 스승님도 기다렸어요 => 뒤` · `오는 스승님의 제자도
기다렸어요 => 뒤` · `오는 제자의 스승님도 기다렸어요 => 앞`.

**Counterbalancing.** Every (pair, verb, tail) triple emits exactly these 4 items — the
position counterbalance IS the within-pair order swap (H의P vs P의H), fully crossed with
±시. Per-cell n is identical (n/4).

**Per-design-cell gold is CONSTANT — by arithmetic, not by oversight.** gold = f(hp, pos)
= f(cell), so "gold 50/50 per (hp×pos) cell" is impossible; H_003 had the same property
(gold_flip constant per A1/A2/K1/K2). The 50/50 requirement lives on every OBSERVABLE
stratum instead (§4, §7): a design cell is not observable without conjoining the two
string-separated features — which is the task. The seed's "50/50 per cell" is implemented
as: equal cell sizes + exact 0.5 gold balance on every observable grouping.

---

## 3. Gold-labeling function

```python
def gold(honorific_present: int, honored_position: int) -> int:
    """honored_position: 1 = N1, 2 = N2. Returns attachment (1=N1/앞, 2=N2/뒤).
    Subject-gap RC: the noun the RC attaches to IS the RC verb's subject.
    Drill-grammar axiom (categorical): -시- on RC verb <=> RC subject is HONORABLE."""
    if honorific_present:                 # -시- ⇒ subject is the honored noun
        return honored_position
    else:                                 # plain ⇒ subject is the plain noun
        return 3 - honored_position

# bit form (pos_bit = honored_position - 1; gold_flip: 0 = 앞/N1, 1 = 뒤/N2):
#   gold_flip = 1 ^ honorific_present ^ pos_bit
# truth table: (hp=1,pos=N1)->앞  (1,N2)->뒤  (0,N1)->뒤  (0,N2)->앞
```

**Truth conditions of high vs low.** The string `{RC} N1의 N2` has two parses:
- **attach N1 (low/local)**: `[[RC N1]의 N2]` — the RC restricts N1; truth-conditionally
  V(N1) ("the N2 of the N1 who is V-ing").
- **attach N2 (high/non-local)**: `[RC [N1의 N2]]` — the RC restricts the head of the whole
  genitive NP; truth-conditionally V(N2) ("the N2-of-N1, who is V-ing").

The two parses are string-identical; with exactly one honorable noun per item and the
categorical-agreement axiom, ±시 selects exactly one: in SI cells the competing parse is
agreement-ungrammatical (*plain-subject + -시-), in PL cells it violates the drilled
convention (honorable subject unhonored) — unique reading in all four cells (asymmetric
strength; honesty note in §0).

**Why resolving it is binding, not a heuristic.** The two XOR inputs live at opposite ends
of the string: hp is in the string-INITIAL verb eojeol; pos is recoverable only by locating
the 님-marked noun among the two mid-string genitive slots. Every single-feature reader and
every contiguous-window reader short of the whole sentence sees at most one input → 0.5
(§4). Producing 앞/뒤 requires predicating the verbal honorific feature OF a specific noun
slot across the ambiguous RC edge — the verb↔N1 vs verb↔N2 edge is exactly where a head-final
L→R parse and an R→L parse disagree, i.e. an entry of T.

---

## 4. Heuristic scorers for the F7 audit (definitions + closed-form proofs of 0.5)

Panel counts below are f2′ (n=192, 48/cell); the f1′ arithmetic is identical at 16/cell.
All scorers use max(s, 1−s) or best-rule-in-family — an anti-correlated cue is as leaky as
a correlated one (H_003 held_out_blind lesson).

1. **presence-attach** — best rule of the family "-시- present ⇒ attach b; absent ⇒ 1−b",
   b ∈ {앞, 뒤}; equivalently majority-guess grouped by `honorific_present`.
   *Proof*: the hp=1 stratum is SI_N1 ∪ SI_N2 = 48앞 + 48뒤; the hp=0 stratum is
   PL_N1 ∪ PL_N2 = 48뒤 + 48앞. Either b is right on exactly half of each stratum → 0.500.
2. **locality** — "attach to the nearest noun". The RC is string-adjacent to N1 on every
   item, so this is the constant guess 앞; score = max(m, 1−m), m = frac(gold=앞). Also
   covers anti-locality (constant 뒤).
   *Proof*: gold=앞 on SI_N1 ∪ PL_N2 = 96/192 → 0.500 exactly.
3. **lexical-lookup** — max over groupings g ∈ {honored_lexeme, plain_lexeme, n1_lexeme,
   n2_lexeme, verb_stem, tail} of majority-guess-by-g.
   *Proof*: each pair emits all 4 cells equally, and within a pair each member sits at
   {N1 w/ 앞, N1 w/ 뒤, N2 w/ 앞, N2 w/ 뒤} once per (verb, tail) → every lexeme, in every
   role, is exactly 50/50 on gold; verbs and tails cross all cells → 0.500. (This also makes
   uneven pair-usage harmless.)
4. **marker-position** (reported; the pos-only reader) — majority-guess by which slot holds
   the 님-marked noun. *Proof*: pos=N1 stratum = SI_N1(앞) ∪ PL_N1(뒤) → 0.500.
5. **worst_suffix_leak** (harness fn, cap L≤10) — is a raw-surface suffix leak possible?
   No, by shared tails ACROSS gold bits: within one (pair, verb, tail) the 4 surfaces
   differ only in the string-initial verb form and the noun order; reading from the end,
   `도 {tail} => ` (10 chars for 기다렸다-register) is byte-identical across the 4 cells
   (gold 앞앞뒤뒤 → any suffix group ≤ tail region is 50/50); a longer window adds the N2
   lexeme → groups by (n2, tail) → 0.5 by lexeme balance; adding N1 gives (n1, n2, tail) =
   pos known but hp unreadable (it is the string PREFIX) → still 50/50. No contiguous suffix
   short of the full surface sees both XOR inputs. Cap at L=10 as in H_003: beyond the
   shared region, singleton (surface) groups score 1.0 mechanically — that is "read the
   whole sentence", i.e. the task, not a leak.
6. **verbform-prefix leak** (NEW, mirror of 5 at the string front) — the hp-only reader.
   GATED FORM: group by the per-item verb-eojeol window `surface[:len(verb_form)+1]`
   (equivalently by `verb_form`). *Proof*: each verb form spans exactly two cells with
   opposite gold → 0.500 (verified 0.5 exactly on the generated panels).
   A FIXED-L prefix grouping is REPORT-ONLY, not gated — measured fact: at L=6 it scores
   1.0 on f2′, because for short verb forms (웃는 = 2 chars) the window crosses into N1 and
   the group (verb form × N1-initial chars) pins the cell. That is not a learnable leak:
   for f2′ the N1 lexemes are drill-absent (no gold statistic exists in training for any
   prefix containing them), and the drill grid itself is cell-balanced per (pair, verb,
   tail), so every drillable prefix statistic sits at 0.5. It is the prefix analog of
   H_003's long-suffix over-count (there, held_out_blind superseded worst_suffix_leak;
   here, drill-disjointness §5 + the drill-grid report play that role). Gating on it would
   score the task's own sufficient statistic (hp ∧ class(N1)) as a leak.
7. **template_heuristic** (harness fn) — `template` := surface with both noun eojeols
   replaced by `⟨N⟩` **keeping the invariant 도** (`웃으시는 ⟨N⟩의 ⟨N⟩도 기다렸다 => `).
   Exposes (verb form → hp, tail) only → 0.500 as in (1). NOTE: the template must never
   encode a noun-keyed allomorph — with 도 there is none by construction (§0.1); F7 asserts
   the post-N2 particle is a single constant string panel-wide.
8. **char-length** — majority-guess by `char_len`. *Proof*: the N1↔N2 swap preserves total
   length, so within (pair, verb, tail) the ±시 delta splits {SI_N1, SI_N2} from
   {PL_N1, PL_N2}, each internally 앞+뒤 → every length group is a union of balanced sets →
   exactly 0.500. `eojeol_len` is the constant 5 (`[V-adn] [N1의] [N2도] [TAIL] [=>]`) →
   uninformative (asserted single-valued).
9. **task_conjunction_sanity** (reported, expected 1.000, explicitly NOT a gate) —
   majority-guess by (hp, marker-position): must be exactly 1.0, else the gold formula is
   mis-implemented.

**Drilled-blind disanalogy (why there is no held_out_blind gate here).** H_003 held out a
TOKEN (못) the model had to individuate, so a drilled-only reader had to be blind. H_004
holds out FILLER LEXEMES; the two channels the task composes — ±시 and the productive -님
class marker — are drilled BY DESIGN (§5), so a "drilled-only" reader that conjoins them
across the edge is not a confound, it is the mechanism under test. The lexical memorization
route is closed instead: in-panel lexical-lookup = 0.5 (scorer 3) and drill→panel lexeme
disjointness (§5, asserted), so no (lexeme → gold) table transfers.

---

## 5. Splits, n arithmetic, and what the drill teaches

| panel | composition | n |
|-------|-------------|---|
| **f2′** (verdict, OOD) | 8 held-out pairs × 3 verbs {웃다,오다,떠나다} × 2 tails {기다렸다,기다렸어요} × 4 cells | **192** (48/cell; σ = √(.25/192) = 0.036, F3's 0.60 = chance + 2.8σ) |
| **f1′** (liveness) | 4 drilled pairs × 4 verbs {쉬다,달리다,노래하다,춤추다} × 1 held-out tail {기다렸네요} × 4 cells | **64** (16/cell) |
| drill grid | 12 drilled pairs × 9 clean verbs × 3 drilled tails × 4 cells | 1296 |

- **f2′ recombination axis = the 8 noun lexemes** (4 HON + 4 PLAIN, §1e). They appear in
  ZERO drill items (asserted at substring level against every drill surface: {어머님,
  회장님, 스승님, 박사님, 조카, 후배, 제자, 비서} — checked non-colliding with drilled
  strings, e.g. 어머님⊄할머님, 회장님⊄부장님/과장님). Verbs, tails, the 앞/뒤 convention,
  and both ±시 forms are all DRILLED — the only novelty is which lexemes fill the slots.
- **The OOD class channel is the productive -님 marker**: a held-out lexeme's HON class is
  recoverable only from 님 (9 distinct drilled 님-nouns teach it; PLAIN = unmarked). This is
  the recombination bet: apply drilled morphology to novel fillers. It is why non-님
  honorables are banned (§1a) — their class would be unknowable OOD and the f2′ ceiling
  would collapse. (할아버님 drill ⊃ 아버님 drill is intentional class-consistent morphology
  sharing, same as 님 itself.)
- **f1′ tests** the drilled task under a held-out REGISTER only (기다렸네요; substring-
  disjoint from 기다렸다/기다렸어요/기다렸음): minimal shift, so f1′(A-duel) < 0.85 reads as
  "never learned the drilled task" (F2 measurement-DEAD), not as an OOD failure.
- **The drill teaches**: the sentence form, the `=> 앞/뒤` answer convention (supervised,
  all four cells present and equal-n so the drill itself is heuristic-neutral — the same F7
  audit runs on the drill grid REPORT-ONLY), categorical -시- agreement, and 님 ⇒ HON on 9
  lexeme types. It never contains a held-out lexeme, the held-out register, or any negator.
- Interface: `build_hon_bind.py` writes `heldout_manifest.json` {hon_heldout, plain_heldout,
  tail_heldout, f2_pairs, f1_pairs, drill_pairs, verbs_by_split}; `gen_drill_h004.py`
  imports it; the disjointness gate re-runs against the generated `drill_grid.json` and is
  reported PENDING until that file exists.

---

## 6. Item dict schema (all keys required on every item)

H_003's `negator_count` / `drilled_negator_count` / `heldout_negator_count` DO NOT EXIST
here; harness fns reused: `template_heuristic_score`, `worst_suffix_leak`, `label_balance`,
`binom_sigma`. The three named scorers + prefix-leak live in `build_hon_bind.py` (upstream
to `tool/` as a generic majority-by-key primitive once stable).

| key | type | values / example | read by |
|-----|------|------------------|---------|
| `panel` | str | `"f2prime"` \| `"f1prime"` | bookkeeping |
| `cell` | str | `"SI_N1"` \| `"SI_N2"` \| `"PL_N1"` \| `"PL_N2"` | cell-size assert |
| `surface` | str | `"웃으시는 어머님의 조카도 기다렸다 => "` | suffix/prefix leak |
| `template` | str | `"웃으시는 ⟨N⟩의 ⟨N⟩도 기다렸다 => "` | template_heuristic |
| `honorific_present` | int | 0 \| 1 | presence-attach |
| `honored_position` | int | 1 \| 2 | marker-position, sanity |
| `attachment_gold` | int | 1 (=N1/앞) \| 2 (=N2/뒤) | gold formula assert |
| `gold_flip` | int | 0 (앞) \| 1 (뒤) — `= attachment_gold − 1` | every scorer's target |
| `gold_token` | str | `"앞"` \| `"뒤"` | eval collector |
| `hon_lexeme` / `plain_lexeme` | str | `"어머님"` / `"조카"` | lexical-lookup |
| `n1_lexeme` / `n2_lexeme` | str | `"어머님"` / `"조카"` | lexical-lookup |
| `verb_stem` | str | `"웃"` (dict form 웃다) | lexical-lookup |
| `verb_form` | str | `"웃으시는"` (as in surface) | prefix cap, template |
| `tail` | str | `"기다렸다"` | lexical-lookup, suffix cap |
| `eojeol_len` | int | 5 (constant) | constancy assert |
| `char_len` | int | `len(surface)` | char-length scorer |

Consistency (asserted per item): `gold_flip == 1 ^ honorific_present ^ (honored_position-1)`;
`gold_token == ("앞","뒤")[gold_flip]`; `hon_lexeme` is 님-final and `plain_lexeme` is not;
exactly one of {n1,n2} equals `hon_lexeme`; `surface` starts with `verb_form`
and ends with `"도 " + tail + " => "` — i.e. the invariant 도 immediately precedes the tail.

---

## 7. F7 pass condition (the don't-run gate)

For EACH panel P ∈ {f2′, f1′}, with tolerance band [0.48, 0.52] (= 0.5 ± 0.02):

```
presence_attach(P)            ∈ [0.48, 0.52]
locality(P)                   ∈ [0.48, 0.52]
lexical_lookup_max(P)         ∈ [0.48, 0.52]      # max over the 6 groupings of §4.3
marker_position(P)            ∈ [0.48, 0.52]
template_heuristic(P)         ∈ [0.48, 0.52]
worst_suffix_leak(P, L≤10)    ∈ [0.48, 0.52]
verbform_prefix_leak(P)       ∈ [0.48, 0.52]   # fixed-L prefix curve report-only (§4.6)
charlen_majority(P)           ∈ [0.48, 0.52]
```

Exact structural asserts (==, not toleranced):

```
per-cell counts equal (f2′: 48×4; f1′: 16×4)
gold formula + schema consistency on every item (§6)
overall / per-hp / per-pos / per-lexeme / per-verb / per-tail gold balance == 0.5
eojeol_len single-valued; post-N2 particle == "도" panel-wide
task_conjunction_sanity == 1.0
"앞" and "뒤" absent from every surface; negator strings absent (§0)
union check: template_heuristic and worst_suffix_leak(L≤10) on f2′ ∪ f1′ ∈ [0.48, 0.52]
disjointness: 8 held-out lexemes + 기다렸네요 absent (substring) from drill_grid.json
              [reported PENDING until the drill exists; final PASS requires it]
```

`F7_pass` = AND of all ⇒ print `PASS — panel is heuristic-neutral, arms may be built`,
exit 0; else `FAIL — panel leaks a countable cue, DO NOT TRAIN`, exit 1. (F7 gates the
panel only; G-0 additionally requires the seed's rank-mass check — ≥20% of ‖T‖² off the
top singular direction on sample parses — before any training.)

---

## 8. Builder contract + G-1 native-reviewer checklist

`state/h004_parser_duel_tension_rank_drill_2026-07-16/build_hon_bind.py`:
stdlib-only, deterministic, no `random`; emits `panel_f2prime.json`, `panel_f1prime.json`,
`f7_audit.json`, `heldout_manifest.json`, and `REVIEW_surfaces.tsv` (one line per distinct
surface: surface · cell · gold token · EN gloss · flags) for the G-1 pass. Exit code = F7.

G-1 checklist (native reviewer rules PASS/FAIL per line):
1. Every surface in `REVIEW_surfaces.tsv` is a grammatical Korean sentence.
2. Every §1a noun naturally takes subject -시- (and every §1b noun does not, adult speaker).
3. Every §1c verb: both adnominal forms correct; plausible for BOTH classes.
4. All 8 f2′ pairs + 12 drill pairs + 4 f1′ pairs: both genitive orders acceptable
   (associative reading allowed); flagged pairs (§1e) explicitly confirmed or swapped from
   the reserve list.
5. The intended reading of each cell (per the §2 worked examples) is the natural one under
   the categorical-agreement convention; PL-cell normativity note acknowledged.
