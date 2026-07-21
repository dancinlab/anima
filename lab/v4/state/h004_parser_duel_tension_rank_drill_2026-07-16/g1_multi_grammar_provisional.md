# H_004 MULTI-BIND G-1 grammar — LLM first-pass (PROVISIONAL, native operator confirm pending)

Scope: the `panel_f2doubleprime.json` surfaces (n=192, K=6 stacked HON-BIND conjuncts). LLM
first-pass in the H_003 "LLM 판정" pattern, recorded PROVISIONAL — freeze stays gated on a
native operator confirming the flagged points below.

## Ruling: PROVISIONAL PASS (grammatical), with two flagged classes for the native operator

1. **Each conjunct is well-formed.** `[V-adn(±시) N1의 N2도]` = a relative-clause-modified genitive
   NP marked with 도. E.g. `웃으시는 조카의 어머님도` = "also the mother of the nephew, who [=mother]
   smiles(HON)". Grammatical.
2. **The 6-fold 도-stack is grammatical.** `A도 B도 … F도 기다렸다` lists six "also"-objects of the
   matrix verb 기다리다 ("(I) waited for A too, B too, … F too"). Korean allows arbitrary-length 도
   object stacking; six is stylistically heavy (a probe artifact, acceptable as in H_003's synthetic
   frames) but not ungrammatical.
3. **±시 concord holds per conjunct** exactly as in single-bind: +시 forces the honorable (님-marked)
   noun as the RC subject (hard grammar); −시 rests on the drilled categorical-agreement convention
   (the honorable noun un-honored is normative-deviant, not absolutely ungrammatical).
4. **The 4 new pool lexemes are class-correct**: 원장님 (director) · 총장님 (chancellor) take subject
   -시- naturally (님-marked, honorable); 조수 (assistant) · 신입 (newcomer) are plain, un-marked.

## Flagged for the native operator (freeze gate)

- (a) **PL-cell normativity** (same as single-bind) — acceptable as a drilled convention, or drop PL
  cells and run SI-only at reduced n (pre-registered fallback).
- (b) **Loose associative P의H genitives** with the new lexemes: `신입의 총장님` ("the chancellor of
  the newcomer"), `조수의 원장님` ("the director of the assistant") read as associative but are
  semantically loose. Confirm acceptable, or restrict the new lexemes to the H의P order / swap from a
  reserve pool. (The MDS panel construction is order-agnostic; a lexeme-order restriction re-runs
  build_honbind_multi.py + F7″ unchanged.)
- (c) **6-stack naturalness** — confirm the length is acceptable for the drill register, or reduce K
  (K=6 is the minimal K clearing probe(rank-1) ≤ 0.60, so K cannot drop without re-opening G-1).

## Status

G-0 (F7″) + G-1 core (rank-mass + probe separation + F6) all PASS on the BUILT MULTI-BIND panel
(build_tension.json, cross-validated). G-1 grammar = **PROVISIONAL LLM PASS** (this doc). The ONLY
remaining pre-freeze gate is native-operator confirmation of (a)+(b)+(c). On confirm →
`pre_register_frozen: true` → build the drill grid (+ disjointness) → G-2 d=384 arms
(A-duel/A-rank1/C-plc/C-scaf/C-perm ×2 seed, local MPS ~5h — a multi-session compute endpoint).
