# H5_001 G-0 — "[honored-noun]의/도 IS pos" counter-example: FIX STILL POSSIBLE — the noun channel needs ORBIT CLOSURE, not rates (Fable 5, 2026-07-18)

> **SSOT**: `ARCHITECTURE.json` → `defect-encoding.core-surfaces-both` (+ `.fixes`). Seed of record,
> read-only after ratification. Ruled against commit 5c4c93d (builder + counter-example) and fresh
> byte-level measurements on the COMMITTED `f2d_d1.json` (this doc cites them; rerunnable in-place).

## 0. The call in one paragraph

**FIX STILL POSSIBLE — inside the register lever, no panel change.** The counter-example's measurement
is real and correctly localized (posbin s7, support 96, pos-pure), but its irreducibility argument is
REFUTED by the committed corpus itself: `님의` occurs in **96/96 of the pos_5=2 f2d δ1 items**
(5–10×/sentence — the F-4 decoys already inject it), and those items did not thereby become pos=1,
because gold/pos are computed from the CORE SLOTS (`_emit_one` conjunct fields), not by byte-scan. "The
honored noun carrying 의 just IS honored-at-N1" conflates a role-indexed predicate with a location-free
byte string — the same conflation §1 of the first adjudication refuted for hp_k, now on the noun side.
What the measurement actually shows: the leak survives ONLY in keys whose support moves WITH the label
— (g, posbin) at the last core junction (`님의`∈s7 ⟺ pos_5=1 at 96/96 vs 0/96; `님도`∈s7 ⟺ pos_5=2 —
measured on committed f2d_d1), sub-m_min count tails (count(님의)∈{11,12} → pos_5=1 only), and the
junction grams F-4 itself named (committed verdict top: `b'\x98 \xec\xb2'` [의␣청-head] → pos_5=1,
`b'\x94 \xec\xb2'` [는␣청-head] → pos_5=2, support 96 each). Rate-based decoys can never pin those; an
involution can. **Concession first (§1), construction second (§2), sharpened fold criterion third (§3).**

## 1. Concession — where the first two gates over-claimed (the user's charge is partly right)

- SPEC §2.2 (님-side bullet) and ADJUDICATION F-4 prescribed **rates** ("rates set by the crossing so
  each such gram's support is exactly gold/pos-balanced"). F-4 even NAMED the junction family
  ("every noun⊗particle bridge AND every [는+space+noun-head] junction gram") — the requirement was
  stated, but the prescribed MECHANISM cannot meet it: a rate schedule uncorrelated with pos balances
  location-free presence (measured: ui_present 96/96 in BOTH halves — it worked), yet leaves every
  key whose support moves with the label (bins, count tails, junctions) to crossing coincidence. The
  builder implemented the spec as written; the census measured the mechanism's shortfall, not builder
  distance this time. **That is a design-gate error, conceded.**
- SPEC §5's involution is scoped to the 시 channel only ("exchanges the 시-assignment between contested
  and adverbial sites"); no involution was ever specified for the noun channel. Consequently §10.1's
  "census PINNED ≤ 0.5+ε at every δ ≥ 1 by construction" was **over-claimed as written** — it is true
  only once the orbit closes BOTH channels.
- What the counter-example got right beyond the numbers: flipping pos in the F-2 orbit indeed CANNOT
  balance the noun bridges, because the orbit as built moves the noun with the label (5c4c93d's finding
  is correct as far as it goes). What it got wrong: concluding no decoy can inject the gram. The
  committed corpus already does; the missing piece is making the injection ORBIT-PAIRED, not random.

## 2. F-5 — noun-channel orbit closure: region-complement (mirror) decoys

**Mechanism (extends F-2's involution ι to the noun channel):** in each conjunct region k, one adjunct
chunk is the MIRROR of that region's own core — same hon_k/plain_k lexemes, same adnominal-verb shape,
particles complement-assigned — so the region's chunk multiset is {core(pos), mirror(pos)} =
{[V-adn H의 P도], [V′-adn P의 H도]} (pos=1) or the same two strings with roles exchanged (pos=2).
ι_k := flip pos_k = exchange which of the two strings sits in the core slot; gold recomputed (F-2).

Why this pins every registered key exactly (support closed under ι_k ⇒ census = 0.5 by pairing):
- **bridges**: all four {H의, H도, P의, P도} occur exactly once per region in EVERY item ⇒ presence
  AND count keys constant (kills the {11,12} tails);
- **junctions**: {[는␣H-head], [는␣P-head], [의␣H-head], [의␣P-head]} all present per region in every
  item ⇒ the measured [의␣청]/[는␣청] family goes constant; the 도-boundary junction [도␣next-head]
  never spans back to the noun within n≤4 (noun-tail+도(3B)+space+head ≥ 6B);
- **bins**: 의/도 are both 3 bytes ⇒ ι preserves all byte offsets except the N1↔N2 length swap inside
  the frozen core (±3B typical) and the core-slot↔ADV-slot exchange (~30–40B, vs bin width ~80B on
  f2d: L≈655B ⇒ bin ≈ 82B; measured s7 window already CONTAINS ADV_5,2's decoy slot — offsets 573+,
  decoy at ~583 — so the last region closes too). Residual bin-boundary straddlers are gated by the
  per-(g,bin) A4 exact assert (re-run criterion §5 of the first adjudication) with frame/adjunct
  length-tuning; **if a fixed-order δ cannot satisfy per-(g,bin) exactly, that δ is BUILD-INFEASIBLE
  (discovered at $0) and the candidate window shifts to δ3–δ5 where scrambling makes slots
  exchangeable** — the consequence pre-registered in ADJUDICATION §4, unchanged.
- **anti-parity clause survives**: the mirror chunk carries an overt adjunct licensor ≤1 eojeol away
  (trailing frame word, e.g. "…모임에서"); the real core is the region-final chunk before the next
  region/tail. Role selection stays locally decidable; predicating 시/님 features OF a core slot across
  the contested edge stays the depth-2 task.
- **시-accounting**: the mirror's V′-adn(±시′) enters F-1's constant regional sum and F-2's 시-exchange
  orbit — one schedule, both channels.

**Register-lever check (the user's dichotomy, answered):** the honored noun stays 님-final; the core
string [V-adn N1의 N2도] is byte-untouched; pools, codebook, gold map untouched. Only ADJUNCT CONTENT
changes — the register. Panel-surface reuse of argument lexemes in decoy slots was already ruled
in-scope (ADJUDICATION §2: disjointness §6 scopes DRILL surfaces; 사장님 appears verbatim as an
argument in every f2d item). No second lever is crossed. The one genuine external gate: mirror-chunk
shapes must pass the carried native checklist ("[V′는 P의 H도] 모임에서"-family). **If the native pass
vetoes every mirror shape, that is a MEASURED bound on the register lever** — a legitimate fold path
(§3), not a construction failure to paper over.

## 3. Sharpened fold criterion (what would now be K-fold-1 evidence)

FOLD fires iff one of these MEASURED exits, none of which the current numbers reach:
1. After ι-closure on BOTH channels (F-1..F-5), some n≤4 family still at 1.0 — that gram, byte-decoded,
   would be a core-certifying window (first adjudication §4 said none exists in this grammar; F-5 is
   the constructive proof burden);
2. per-(g,bin) exact balance infeasible at EVERY δ including scrambled δ3–δ5;
3. native pass vetoes the entire mirror-decoy shape family (register lever bounded by Korean
   naturalness — a real, reportable bound);
4. G-0k: no ≥2-consecutive in-window δ (census green AND control in-sample ≥ 0.95, both seeds) — the
   gate's own referee, untouched by this ruling.

## 4. Record discrepancies (flagged for the re-run, honesty)

The committed g0_verdict.json (5c4c93d) does NOT yet match the message-level claims accompanying it:
f2d per-target still lists hp_0/hp_1/hp_2 at 1.0 (e.g. worst [presence n=2 b'\x90\xeb' → pos_2],
drill worst [count b'\xbc'=2 → hp_0]), and A4_gold_balance fails on f2d/f1d (0.5278/0.4167). "hp fully
balanced 96/96" currently holds for the per-conjunct si-constant check, not the full census. No ruling
rides on this — the re-run criterion is unchanged: **all 18 targets × full §5 key family (both-ends +
"=>"-relative posbin, per-sentence votes) ≤ 0.5+ε on drill+f2d+f1d, every δ ≥ 1, per-(g,bin) A4
asserts where order is fixed.** The census stamps it; nothing else does.
