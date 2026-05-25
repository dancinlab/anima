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

### Results (full 64-anchor sweep, max_new=90; ckpt sha256 961c07e2…, load missing=0 unexpected=0)

| | routing (inherited) | honest §9 coherent | anchor_grounded proxy |
|---|---|---|---|
| §16 baseline | 21/64 | 64/64 | 1/64 |
| N (.kosmos-trie) | 21/64 | 64/64 | **22/64** |

connection point `mode_off_byte_equal_to_s16_generate`: **True** (B-KTRIE-3 ✅
— numerically verified across all 64 anchors).

**routed-anchor decomposition (the 21 anchors where §16 emitted the correct
`🛸<tier>` prefix)**: N's body got grounded on its OWN anchor in **21/21**
(constraint fired with `constrained_steps` 83–84 per anchor). §16 baseline
body was grounded in **0/21** of those (the §16.6-C SPLIT: per-anchor body
was a wrong-anchor template + name byte-garble).

**+1 in §16 baseline (1/64 → 22/64 = +21 from N + 1 §16 coincidence)**:
tier 54 (의식상태) — model emitted `🛸55` (route-fail by exact-match) but
body happens to mention shared category `의식상태`. Cross-category
coincidence, NOT a N flip — honest scope: the **real N delta is 21**
(the §16 routed set is exactly the set N can help, per B-KTRIE-4
routing-inherited).

**8 representative §16 → N body-shift examples** (routed anchors, exact gen
strings, first ~70 chars):

| tier | category | §16 (garbled body) | N (anchor-grounded body) |
|---|---|---|---|
| 12 | 운동 | `🛸122 스탐의이조 — 인과깊이 자극이…` | `🛸12🛸12 걸음 — 운동 영역의 자극이…` |
| 24 | 생명 | `🛸244 약속의이산순 — 의식상태 영역…` | `🛸24🛸24 씨앗 — 생명 영역의 자극이…` |
| 77 | 예술 | `🛸77 카테왔의 — domain 의식상태…` | `🛸77Tier 77 만다라 — domain 예술…` |
| 80 | 의식상태 | `🛸80 매핑을 다시 짚는다 — 인지 × depth…` | `🛸80Tier 80 명상 — domain 의식상태…` |
| 92 | 의식상태 | `🛸92 열늤 — domain 생명성장…` | `🛸92🛸92 엑스터시 — 의식상태 영역…` |
| 101 | 산술 | `🛸101 약수와륐 — 인과깊이 영역…` | `🛸101🛸101 덧셈사슬 — 산술 영역의…` |
| 102 | 산술 | `🛸102 약수와배 — 추론양식 영역…` | `🛸102🛸102 곱셈격자 — 산술 영역의…` |
| 103 | 산술 | `🛸103 약수와륐 — 인과깊이 영역…` | `🛸103🛸103 분수약분 — 산술 영역의…` |

Each row: §16 body has the right *template form* but the **wrong anchor's
content** + name byte-garble (`카테왔의`/`약수와륐`/`스탐의이조`, the
§16.6-C SPLIT). N's trie holds the body on the routed anchor's OWN
canonical `.kosmos` content: tier-77 → `만다라/예술` (correct anchor name +
category), tier-101 → `덧셈사슬/산술` (correct), tier-103 → `분수약분/산술`
(correct). The name byte-garble (`약수와륐 → 약수와배` etc.) disappears
because the trie does not admit those byte paths.

## 6. Honest judgment (g3 — measured only, over-claim 0)

**N closes the §16 SPLIT measurably on the routed set, with strictly
honest scope.** Where §16 routes correctly (21/64), N's `.kosmos`-trie
constrained decode pulls the body onto that anchor's OWN canonical
content in **21/21** (`anchor_grounded` 0/21 → 21/21). The structural
proxy captures this 22× lift (1/64 → 22/64), driven entirely by N's
mechanism on the routed set (the +1 §16 coincidence is unrelated).
Routing itself is INHERITED from §16 unchanged (21/64, B-KTRIE-4 by
design — N constrains the body of whatever §16 routes; where §16
mis-routes (43/64), N reduces to §16 byte-equal via the trie fallback,
B-KTRIE-3 verified numerically).

**What this is NOT (over-claim 0)**:
- **NOT a coherence proof.** `anchor_grounded` is a deterministic
  structural proxy (own-category in body ∧ no foreign-tier bleed), NOT
  an LLM-judge / §18 sufficiency-rubric / held-out generalization
  measure (B-KTRIE-NOTE). The grounded bodies are still the *trained*
  carving template (`만다라 — domain 예술, the stimuli converge into one
  basin…`) — exactly the §16.6-C "정교한 암기" continuation, only now
  pinned to the *correct* anchor's template rather than a *wrong*
  anchor's template. memorization-saturated regime (§1.1, §2.4) unbroken.
- **NOT a generalization improvement.** N does not produce new
  knowledge; it constrains decode to existing `.kosmos` SSOT content.
  The body is on-anchor, not novel.
- **NOT a §15 milestone refutation.** north-star (GOAL.md) unchanged —
  N is a $0 decode-time overlay that exploits §16's routing-break to
  prevent body-drift; it does not close the irreducible §1.1
  data-regime threshold.
- **NOT a routing improvement.** Routing 21/64 = identical to §16. N
  only helps the 21 routed anchors; the 43 mis-routed anchors are
  unaffected (`mode_off_byte_equal_to_s16_generate: true` confirms).
- **honest §9 coherent unchanged** (64/64 both) — N's bodies are still
  ≥ 20 bytes, printable, no cascade. The cascade-rate metric does not
  distinguish §16 (garbled-but-non-cascade) from N (on-anchor templated)
  — §9 is necessary, not sufficient (B-EMERGE-7), as stated.
- **Route-marker repetition artifact** (`🛸12🛸12`, `🛸77Tier 77`): the
  trie admits the canonical string that itself starts with `🛸<tier>`
  after the model emits its `🛸<tier>` prefix, so the prefix appears
  twice. Honest residual; does not affect on-anchor body content.

**§21.3 Q2 frontier**: N — `.kosmos`-anchor constrained decoding —
**operates as designed at decode time on the §16 routing-break regime**:
21/21 routed-anchor body-shift from wrong-template-on-right-route to
own-template-on-right-route. This is a clean measured $0 demonstration
of the KG-Trie pattern on anima's OWN `.kosmos` SSOT (§21.3-N anima-fit
★★★★ structurally confirmed), bounded by the irreducible §15 milestone
(routing inherited, body still memorized-template — coherent generalized
emission requires §1.1 data-regime or beyond, not decode-time
constraint alone).

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
