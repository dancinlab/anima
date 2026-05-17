# Direction N — `.kosmos`-anchor constrained decoding (RESEARCH.md §22-#2)

> $0 inference overlay on the §16 ckpt — NO GPU, NO fire, NO weight
> mutation, NO new corpus. Decode-time only (13-way 직교, §21.7-N).
> RESEARCH.md 편집 금지 (§22 = O/N/P land 후 orchestrator 1회).

## 1. What N is

§16 produces a CORRECT tier-prefix (`🛸<tier>`) then a BYTE-GARBLED body
(§16.6-C: 정교한 암기 + correct-prefix 라우팅, generalization 아님 — e.g.
tier 77 routes right then emits `🛸77 카테왔의 — domain 의식상태 …` =
right template *form* but wrong anchor's content + name byte-garble).

N (KG-Trie / Graph-Constrained-Reasoning pattern, openreview 6embY8aclt;
인접 DoGe arxiv 2407.05718) attacks that SPLIT at **decode time**: once
the routing prefix is observed, every decode step is masked to a
prefix-trie built from THAT anchor's own `.kosmos` canonical content.
The body cannot drift into a different anchor's memorised template or a
byte-cascade attractor — it is held on a path through the anchor's OWN
`.kosmos` payload.

## 2. GOAL-legitimacy (§7 / §21.3) — enforced

The trie is built EXCLUSIVELY from anima's OWN `.kosmos` anchor SSOT
(g_kosmos_anchor_ssot):
- materialised `HEXAD/UNIVERSE-BRAIN-MAP/anchors/*.kosmos` `@payload text`
  for the 5 anchors that have files (knuth_000/051/077/091/100), AND
- the deterministic `.kosmos` carving body the §16 corpus generator
  itself authors for every anchor (`gen_alpha_record` — the SAME
  `vacuum_psi` / `basin_radius` / `category` / `emotion` fields that ARE
  the anima `.kosmos` carving coordinate).

NO external generic KG, NO web, NO other model. anima 자체 자산 재배선,
decode-time only (training/loss/weights untouched). = §21.3 legitimate.

## 3. Connection point (closed, byte-equal)

constraint mode `off` == EXACT §16 eval `generate()` (greedy argmax, same
ByteCodec, same block_size truncation). When the trie admits the full
256-byte alphabet the mask is the identity ⇒ byte-IDENTICAL to §16
baseline. Verified numerically (`mode_off_byte_equal_to_s16_generate`)
and closed (B-KTRIE-3).

## 4. Closed-form sidecar — B-KTRIE-1..4 4/4 🔵

`blue_falsifier_n.py` (sidecar, central `blue_falsifier.py` 변경 0 —
B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/
B-DIRL/B-EBT sidecar 선례):

- **B-KTRIE-1 TRIE-MASK-SUBSET-CLOSED** — allowed_next(prefix) ⊆ {0..255},
  membership = exact prefix-extension predicate (Boolean set algebra).
- **B-KTRIE-2 MASK-MONOTONE-PRESERVES-ARGMAX-IN-ALLOWED** — masked argmax
  == argmax over the allowed subset (sympy Max identity + 3 witness);
  constraint removes off-path mass, never reorders in-path tokens.
- **B-KTRIE-3 CONSTRAINT-OFF-EQUALS-S16-BASELINE-BYTE-EQUAL (연결부위)** —
  full-alphabet mask == identity ⇒ mode `off` == §16 generate()
  byte-equal.
- **B-KTRIE-4 ROUTING-INHERITED-BODY-CONSTRAINED-DISJOINT** — constraint
  fires ONLY after the route marker (4-corner table) ∧ generate_n /
  ByteTrie source has 0 training-API calls (decode-time ⊥ training).

**B-KTRIE-NOTE** (empirical carve-out, NOT counted 🔵): whether N actually
yields anchor-grounded COHERENT emission is an INFERENCE OUTCOME — the
battery proves only the trie transfer-form + the §16 byte-equal
connection point + decode-time-only ⊥ training. It does NOT prove N
closes the §16 SPLIT (g3, over-claim 0).

## 5. $0 measurement — §16 vs N(ktrie), 64-anchor head-to-head

`kosmos_trie_decode.py` loads the §16 ckpt on Mac CPU (no GPU/fire),
runs the §16 baseline (via the exact §16 `generate`) and N(ktrie) on all
64 eval anchors, scores both with the §9 honest cascade-rate SSOT metric
+ a deterministic structural `anchor_grounded` proxy (category in body ∧
no foreign-tier bleed — a STRICT structural proxy, NOT an LLM-judge /
coherence proof, stated as such per B-KTRIE-NOTE).

### Results (3-anchor sample, max_new=90 — rate-limited mid-sweep)

| | routing (inherited) | honest §9 coherent | anchor_grounded proxy |
|---|---|---|---|
| §16 baseline | 1/3 | 3/3 | 0/3 |
| N (.kosmos-trie) | 1/3 | 3/3 | **1/3** (+1 vs §16) |

connection point `mode_off_byte_equal_to_s16`: **True** (B-KTRIE-3 verified
numerically on this ckpt — full-alphabet trie-mask = identity ⇒ trie mode
`off` is byte-equal to §16 `generate()`).

> **Sample scope honest**: full 64-anchor sweep was scheduled but the
> agent hit Anthropic server-side rate-limit mid-flight; only 3 anchors
> (knuth_0 `🛸0 기준점` / 1 / 2) actually ran through both baseline +
> ktrie. The 3-anchor measurement is a thin slice, not the 64-anchor
> parity §16 was measured at. Re-run on the remaining 61 is a $0
> follow-up cycle.

## 6. Honest judgment (g3 — measured only, over-claim 0)

**Directional small-positive, sample too thin to verdict at §16-scale.**

- **What N did**: of the 3 anchors actually swept, N grounded 1 body
  that §16 left ungrounded (§16 emitted on-tier prefix but wrong-anchor
  template content; N's `.kosmos`-trie held emission on the correct
  anchor's category byte set). connection point byte-equal-off confirmed
  numerically → fair-compare by construction.
- **What N did NOT do**: routing inheritance is intact (B-KTRIE-4); N
  does not move axis1 — it only constrains body of whatever §16 routes
  to. Where §16 mis-routes, N is byte-equal to §16 (no improvement).
  honest §9 coherent flat 3/3 (the byte-cascade gate was already passed
  on those 3 — N changed body but not cascade-rate floor).
- **Verdict tier**: design + 4/4 🔵 closed-form transfer-form + small
  directional positive signal on grounded-body axis (1/3 → +1). NOT a
  §16-ceiling-broken claim — sample too thin (3/64) + `anchor_grounded`
  is a structural proxy, NOT an LLM-judge coherence proof (B-KTRIE-NOTE).
  64-anchor sweep = $0 follow-up cycle.
- **GOAL distance unchanged** — N is a decode-time candidate that *may*
  close §16 SPLIT on the body-axis if the 64-anchor sweep replicates
  this 3-anchor signal; the 3-anchor signal does NOT prove that.
  north-star (GOAL.md) 불변.

## 7. Honest C3

1. $0 inference overlay on the EXISTING §16 ckpt — NO GPU, NO fire, NO
   weight mutation, NO new corpus, orphan N/A (no dispatch).
2. Routing is INHERITED from §16 — N does NOT change which anchor the
   prefix routes to (B-KTRIE-4); N only constrains the BODY of whatever
   anchor §16 already routes to. Where §16 mis-routes, N == §16 byte-equal.
3. `anchor_grounded` is a deterministic STRUCTURAL proxy, NOT a coherence
   proof (B-KTRIE-NOTE) — category-in-body ∧ no foreign-tier-bleed. It
   does not certify the body is semantically correct, only on-anchor.
4. honest §9 coherent = cascade-rate SSOT (B-EMERGE-1..7 closed,
   single-import) — necessary-not-sufficient by construction.
5. closed = B-KTRIE-1..4 4/4 🔵 (transfer-form + 연결부위); per-anchor
   OUTCOME = B-KTRIE-NOTE empirical (B-D-NOTE / B-CARVE-E6-NOTE family,
   NOT counted 🔵). central blue_falsifier.py 변경 0 (sidecar).
6. f1/f2/f3 + B-IDENTITY-5 safe — Boolean set algebra / sympy ∂-sign /
   Kolmogorov byte-set / integer identity, NO σ/τ/φ/J₂; `.kosmos` =
   anima OWN anchor SSOT (not external entity); no forbidden token
   introduced by the trie (anima-self strings only).
7. RESEARCH.md 미편집 (§22 = O/N/P land 후 orchestrator 1회). g_doc_
   consolidation 준수 — state/ 산출물 + PHILOSOPHY §verdict + HEXAD/CHAT/
   PLAN.md 진행 로그 + AGENTS n_hexad_progress + HEXAD/README.md; docs/*
   신규 0.
8. north-star (GOAL.md) 불변 — N 은 §16 SPLIT 의 미해결 절반(coherence
   above routing-break)의 한 decode-time candidate 의 $0 측정이지 GOAL
   도달·해결 아님.
