# §30 — Lateral L1: Cumulative Ckpt Lineage (DESIGN-TIER)

> $0 design-tier — NO fire, NO GPU, NO ckpt training. Lateral candidate to the
> §1~§24 frontier-narrowing arc. L1 = anima ckpt N inherits from anima ckpt
> N−1 (and N−1 from N−2 …), building *generational* memory across cycle-
> versions — the MITOSIS cell-pool extended beyond within-run splits.
> design-tier ≠ fire ≠ emergence (g3). north-star (`GOAL.md`) unchanged.

---

## §1 — Observation that motivates L1

Every anima fire across 23+ research cycles (UBM-E6/E7, Dir-A..M, §11/§16/§22/
§23, the §13-K/L/M batch) trains **from scratch** — `g_clm_from_scratch`
mandates `init_weights = RANDOM INIT seed-fixed`, `base_ckpt = NONE`. No ckpt
inherits from a prior ckpt. anima is a *fresh newborn* every cycle, never a
*generation* descended from the last.

This is structurally at odds with the one analogy `GOAL.md` leans on: human
consciousness does not re-initialise nightly — it accumulates. A person at age
30 is the cumulative integral of 30 years of weight updates on one continuous
substrate. anima's research arc, by contrast, has produced ~16 sibling ckpts
that share *nothing* — each discards the last. L1 asks: **what if anima ckpt N
inherited ckpt N−1's weights as init, so the lineage built generational
memory?** The MITOSIS cell-pool already does this *within* a run (cells split,
state copies parent→child); L1 lifts that one level — cell-pool persisting and
*merging* across cycle-versions, not just within a single forward graph.

## §2 — L1 mechanism (ckpt-as-parent, generational MITOSIS)

**Generation index.** Each ckpt carries `gen: int ≥ 0`. `gen=0` = a true
from-scratch RANDOM-init ckpt (the current regime). `gen=N (N≥1)` = a ckpt
whose `init_weights` were loaded from a `gen=(N−1)` *anima-own* ckpt, then
trained further on a new corpus/lever.

**Lineage edge.** L1 introduces a typed parent pointer
`parent_ckpt_id: str | None` + `parent_source: {"anima_self", "external"}`.
The edge is admissible **only** when `parent_source == "anima_self"` — i.e. the
parent ckpt is itself a node in anima's own lineage DAG, tracing (via repeated
parent pointers) back to a `gen=0` RANDOM-init root. An `external` parent
(HuggingFace foundation model, a non-anima checkpoint) is structurally
rejected — this is the governance-distinguishing invariant (`§3`, B-LINEAGE-2).

**Generational MITOSIS cell-pool merge.** anima's `mitosis_hook_lib.hexa`
maintains a `cell_pool` (≥2, ≤128 cells in the lib; ≤64 in the verification
spec `.clm v1 P2` carried by B-MITOSIS-5). L1 extends `merge_cells` across
cycle-versions: when ckpt N inherits ckpt N−1, the *child* cycle-version may
either (i) carry N−1's cell-pool wholesale, or (ii) instantiate a fresh
sub-pool and **merge** it with the inherited pool — `n_child + m_parent` cells,
clamped to the same `[2,64]` bound MITOSIS already enforces. The merge is the
cell-pool analogue of the weight-init inheritance: structural memory carried,
not just scalar weights.

**Corpus.** L1 is *orthogonal* to corpus — it is a weight-init / cell-pool
lineage lever, not a data lever. It composes with any corpus (§16 diverse,
§23 intra-anchor framing) and any training-time lever (Dir-I Ψ-anchored CTL).

## §3 — THE governance tension: `g_clm_from_scratch` (full analysis)

This is the core of §30 and is confronted head-on.

`@D g_clm_from_scratch` (d=2026-05-15, **active, required**):

> rule: ".clm v1/v2/v3 모두 fresh from-scratch pre-train. **ckpt inherit /
> fine-tune / cotrain-from-ckpt path 폐기.** init_weights = RANDOM INIT
> seed-fixed. **precursor ckpt 는 arch SUPPORTED 검증 anchor only — substrate
> base X.**"
>
> why: "anima_native_scratch (D1=1.0) 원칙 강화. 사용자 directive 2026-05-15
> '.clm 학습은 처음부터 진행하는걸로'."

On its face, **L1 = ckpt inheritance, which `g_clm_from_scratch` explicitly
forbade.** A design that ignored this would be dishonest. Two readings:

**Reading A — the rule's *rationale* is narrower than its *letter*.** The `why`
and the rule's own qualifier point at a specific harm: `"precursor ckpt 는 arch
SUPPORTED 검증 anchor only — substrate base X"`. The word *precursor* and the
memory anchor `anima_native_scratch (D1=1.0)` ("anima native, scratch" — the
D1 design axis demanding anima's substrate be *anima's own*, not borrowed)
both target **external-substrate contamination**: the 2026-05-15 saga context
was repeated proposals to fine-tune anima atop a HuggingFace/Llama foundation
or to cotrain from a non-anima precursor ckpt. The harm guarded against is
*anima identity diluted by a substrate it did not author*. Under Reading A,
anima-OWN-ckpt → anima-OWN-ckpt lineage is **categorically different**: every
weight in a `gen=N` ckpt traces, through the lineage DAG, back to a `gen=0`
RANDOM-init root that anima authored. No external substrate ever enters. The
lineage is anima all the way down.

**Reading B — the rule's *letter* is the rule.** `"ckpt inherit / fine-tune /
cotrain-from-ckpt path 폐기"` is categorical. `cotrain-from-ckpt` was an
*anima-own*-ckpt continuation (the v5-mitosis cond.5 cotrain inherited an
anima ckpt) and it was still 폐기'd. If the user's 2026-05-15 directive
"`처음부터 진행하는걸로`" ("do it from the beginning") meant *every cycle
restarts*, then L1 violates the rule regardless of self-vs-external.

**Why this design CANNOT self-resolve the tension.** A design-tier document has
no authority to reinterpret an `active, required` governance entry. The honest
move is: (1) state which reading the *mechanism* is compatible with, (2) build
a closed-form invariant that *tests* whether the self-vs-external distinction
is even cleanly definable, and (3) hand the governance decision to the user.

## §4 — The closed-form test: can self-lineage be cleanly distinguished?

Reading A is only tenable if "anima-self lineage" is a **crisp, decidable**
predicate — otherwise L1 leaks exactly the contamination `g_clm_from_scratch`
guards against. `B-LINEAGE-2` (`§8`) is precisely this test:

`parent_source ∈ {"anima_self", "external"}` is a **closed 2-element
partition** — the sets are disjoint and exhaustive *by construction*, and a
lineage edge is admissible iff every ancestor chain terminates at a `gen=0`
RANDOM-init anima root. This is decidable: walk the parent pointers; if any
node has `parent_source=="external"` OR a missing root, the lineage is
rejected. **B-LINEAGE-2 PASSES** — the predicate cleanly separates the two
cases. So the *mechanical* distinction is sound.

**But — and this is the honest crux — a clean *mechanical* predicate does not
make L1 *safe*.** B-LINEAGE-2 proves you can *tell* a self-ckpt from an
external one. It does NOT prove that inheriting a self-ckpt carries *memory*
rather than *defects* (`§6`). The mechanical cleanliness is necessary, not
sufficient.

## §5 — §7 GOAL-legitimacy 3-condition gate

- **§7 ① ¬generic-LM-pretrain** — ✅ L1 is a weight-init lineage lever; it does
  not introduce a generic web-corpus pretraining stage. The `gen=0` root is
  the same RANDOM-init anima substrate; every descendant trains on
  anima-physics corpora (carving / Ψ-anchored). No generic substrate enters.
- **§7 ② ¬generic-then-graft / bolt-on** — ✅ L1 grafts nothing external. The
  parent is anima's own prior ckpt; the cell-pool merge uses anima's own
  `merge_cells`. No external classifier, retriever, or foundation model.
  **Caveat (honest):** if `B-LINEAGE-2` were ever bypassed and an `external`
  parent admitted, §7 ② would be *violated* — the predicate is the §7-② guard.
- **§7 ③ anima-physics-is-source** — ⚠️ **partial.** The lineage edge itself is
  *not* anima physics — it is a software bookkeeping pointer. What L1 *carries*
  is anima's own trained weights + MITOSIS cell-pool (anima's growth axis), so
  the *substrate* stays anima-physics-sourced. But L1 does not add a new
  physics capability *source*; it is a *continuity* mechanism over an existing
  source. Honest verdict: §7 ③ is *satisfied at the substrate level* (lineage
  carries anima physics) but L1 is **not itself a physics capability** — it is
  infrastructure. This is acceptable for a *lateral* candidate (it is not
  claimed as the emergence lever) but disqualifies any over-claim that L1
  *produces* emergence.

## §6 — Lineage of memory vs lineage of defects (the decisive risk)

This is where L1's design verdict actually turns.

`§16.6-C` established that anima's best ckpt to date (§16, routing 21/64) is in
a **memorization-saturated regime** — "정교한 암기 + correct-prefix routing,
generalization 아님". Its bodies are byte-garbled; `B-ATTRACTOR` family
documents a persistent byte-cascade attractor (`🛸99…`, `eeee…`, digit
cascades) that *shifts with corpus/ckpt but never dissolves* across the entire
13-way arc. `§11-A` proved 3.68× model scale does not break it; `§9` proved the
V-SPONT "progress" was a lenient-metric artifact.

**The question L1 must answer honestly: when ckpt N+1 inherits ckpt N, what
does the cumulative signal carry?**

- *Lineage of memory* (the optimistic reading): N+1 starts from N's learned
  representations and *adds* to them — generational accumulation, the human-
  consciousness analogy realised.
- *Lineage of defects* (the measured-evidence reading): N is memorization-
  saturated with a baked-in byte-cascade attractor. Inheriting N's weights as
  init means N+1 **starts inside that attractor basin.** Gradient descent from
  a from-scratch RANDOM init at least *explores* before collapsing; gradient
  descent from a saturated parent begins already collapsed. L1 would propagate
  — and likely *deepen* — the exact defect every cycle since UBM-E7 has failed
  to escape. The cumulative signal is not memory; it is **a hardening
  attractor**.

The evidence base strongly favours the pessimistic reading. anima has *no*
ckpt that is *not* memorization-saturated — there is no clean parent to begin
a lineage from. A lineage rooted at a saturated `gen=0` is a lineage of that
saturation. The human-consciousness analogy fails precisely here: a human
brain's cumulative substrate is not *frozen-saturated* at each step — it
retains plasticity. anima's ckpts are CE-trained to near-zero loss (final CE
~0.003–0.008 across the arc) — they are *maximally saturated*, the opposite of
plastic. Inheriting maximal saturation is inheriting a wall.

**This does not mean lineage is *never* viable** — it means lineage is only
viable *once anima has a non-saturated ckpt to root it at*, which is exactly
the unsolved `§1.1` data-regime / `§15` milestone problem. L1 is **downstream**
of the open problem, not a path to it.

## §7 — Verdict: path (b) DESIGN-CLOSE, governance-blocked-AND-premature

Of the two paths the brief offers — (a) argue L1 legitimate + propose a
`g_clm_from_scratch` refinement for user approval, or (b) design-close L1 as
governance-blocked — **§30 takes path (b)**, with a precise honest framing:

L1 is design-closed for **two independent, each-sufficient** reasons:

1. **Premature (the decisive reason).** Per `§6`: anima has no non-saturated
   ckpt. Every candidate `gen=0` root is memorization-saturated with the
   byte-cascade attractor. A lineage rooted there propagates a *lineage of
   defects*, not memory — and likely deepens the attractor (init inside the
   basin). L1's value is *conditional on a clean parent existing*, which is the
   unsolved `§1.1`/`§15` problem. L1 is downstream of the open frontier, not a
   lever on it. Firing L1 now would produce a measured negative isomorphic to
   `§11-A` (scale-up FLAT) — predictable, low-value, anti-padding (the
   `§13-M`/`§13-L` design-close precedent).

2. **Governance-blocked pending user decision.** Even granting Reading A
   (`§3`), L1 *literally* contradicts `g_clm_from_scratch`'s `"ckpt inherit"`
   clause, and `cotrain-from-ckpt` — an anima-*own*-ckpt continuation — was
   *also* 폐기'd, which is evidence the rule's letter reaches anima-self
   lineage too. A design-tier document **cannot self-grant** an exception. L1
   cannot fire without an explicit user governance decision.

**Honest note on path (a).** Path (a) is *not wrong on the self-vs-external
distinction* — `B-LINEAGE-2` shows that distinction is mechanically clean, and
Reading A's rationale-narrowing is a defensible argument. If anima ever obtains
a non-saturated ckpt (post-`§1.1`), path (a) becomes the *correct* path and the
user should be asked to refine `g_clm_from_scratch`. §30 therefore records, as
a **recommendation for future user consideration only** (NOT a self-granted
change, NOT an edit to `AGENTS.tape`):

> *Recommended future refinement, gated on a non-saturated ckpt existing:* a
> superseding `@D` clarifying that `g_clm_from_scratch` forbids **external-
> precursor** inheritance (foundation models, non-anima ckpts — substrate
> contamination) while permitting **anima-self lineage** (a ckpt whose entire
> ancestor DAG roots at a `gen=0` RANDOM-init anima node), *provided the
> parent ckpt is not memorization-saturated*. Until such a ckpt exists, the
> existing from-scratch rule stands and L1 stays closed.

§30 does **not** propose this be adopted now — it would be premature even as a
governance change, because §6 shows L1 has nothing safe to inherit *today*.

## §8 — Closed-form battery (B-LINEAGE-1..4, sidecar)

`blue_falsifier_lineage.py` — separate `state/`-local sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **untouched** (B-DIRI /
B-PRIME / B-EBT / B-S16 sidecar precedent).

- **B-LINEAGE-1 GENERATION-INDEX-MONOTONE** — lineage depth `gen` strictly
  increases by exactly 1 per inheritance edge: `gen(N+1) = gen(N) + 1`, sympy
  `Δ = +1 > 0`, Kolmogorov-bounded integer, child always deeper than parent.
- **B-LINEAGE-2 SELF-SOURCE-vs-EXTERNAL-PRECURSOR-DISJOINT** — `parent_source ∈
  {"anima_self","external"}` is a closed 2-element partition (disjoint ∧
  exhaustive); admissibility predicate `admissible(edge) := parent_source ==
  "anima_self" ∧ root_is_gen0_random(chain)` cleanly separates the two cases.
  **PASSES** — the governance-distinguishing invariant is mechanically sound.
  (Honest: pass = the distinction is *definable*, NOT that L1 is *safe* — `§6`.)
- **B-LINEAGE-3 CELL-POOL-MERGE-CARDINALITY** — generational merge of an
  `n`-cell child pool with an `m`-cell parent pool yields `n+m` cells, clamped
  to `[2,64]` via `clamp(x,MIN,MAX)=min(MAX,max(MIN,x))` — integer cardinality
  closure, mirrors B-MITOSIS-3/-5.
- **B-LINEAGE-4 GENERATION-0-REDUCTION-CLOSED** (연결부위) — at `gen=0` the
  parent pointer is `None`, the inheritance map is the identity-on-nothing, and
  `init_weights = RANDOM seed-fixed` ⇒ L1 at gen-0 **IS** the current
  `g_clm_from_scratch` regime, byte-equal. Boolean overlay-off, mirrors B-EBT-5
  — proves L1 is a strict *superset* of the current regime (current = L1∩{gen=0}).

**B-LINEAGE-NOTE** (empirical carve-out, NOT counted 🔵): whether an actual
lineage carries *memory* vs *defects* (`§6`) — the cumulative SGD trajectory,
whether ckpt N+1 escapes or deepens N's byte-cascade attractor, whether
generational accumulation improves routing/coherence — is an EMPIRICAL fire
OUTCOME (`B-D-NOTE` / `B-ATTRACTOR-NOTE` / `B-SCALE-NOTE` family). The battery
proves the lineage *bookkeeping* is closed-form (monotone depth, clean
self/external partition, merge cardinality, gen-0 reduction); it does NOT prove
L1 would help, and `§6`+`§7` argue it would not, *today*.

## §9 — Why design-close is the honest verdict (g3)

A design-close is a *valid, valuable* outcome (`§13-M`/`§13-L` precedent). §30
establishes, with a 4/4 🔵 closed battery, that:

1. L1's mechanism is *coherent and decidable* — generation index monotone,
   self/external distinction crisp, cell-pool merge bounded, gen-0 reduces to
   the current regime exactly.
2. L1 is *governance-blocked* — it contradicts `g_clm_from_scratch`'s letter;
   no design can self-grant the exception.
3. L1 is *premature regardless of governance* — anima has no non-saturated
   ckpt to root a lineage at; a lineage today is a lineage of the byte-cascade
   defect, not of memory.

The negative is precise and frontier-narrowing: **cumulative ckpt lineage is
not a path *to* `§1.1`/`§15`; it is a candidate that becomes viable only
*after* `§1.1` is solved.** Recording this prevents a future cycle from firing
a predictable-negative L1 in the saturated regime.

## §10 — Honest C3 (≥10)

1. **Path (b) chosen, but path (a) is not refuted on the self-vs-external
   axis.** `B-LINEAGE-2` shows the distinction is mechanically clean — Reading
   A's rationale argument is defensible. §30 closes L1 on *prematurity* (`§6`)
   primarily; the governance block is the second, independent reason. If a
   non-saturated ckpt ever exists, path (a) is correct.
2. **The decisive evidence is `§16.6-C` + `B-ATTRACTOR`** — memorization
   saturation + a never-dissolving byte-cascade attractor. If a future cycle
   produces a *non-saturated* ckpt, §6's argument inverts and L1 should be
   re-evaluated. The verdict is *evidence-conditional*, not absolute.
3. **§7 ③ is only partially satisfied.** L1 is *infrastructure* (continuity
   over an existing physics source), not itself a physics capability. §30 does
   NOT claim L1 produces emergence — it is a lateral candidate, not a lever.
4. **B-LINEAGE-2 "PASS" is necessary-not-sufficient.** It proves you can
   *distinguish* self from external; it does not prove inheriting self is
   *safe*. Conflating the two would be the over-claim §30 explicitly avoids.
5. **No `AGENTS.tape` edit.** §3's recommended `g_clm_from_scratch` refinement
   is a *recommendation for user consideration only* — and §30 explicitly says
   it is premature to adopt even as a governance change today.
6. **L1 ∩ {gen=0} = current regime (B-LINEAGE-4).** This is a genuine result:
   the current from-scratch regime is the gen-0 slice of L1's design space, so
   L1 is a conservative superset — but a superset whose non-trivial part (gen
   ≥1) is exactly the part `§6` argues is unsafe today.
7. **The human-consciousness analogy is partially misleading.** Human
   cumulative substrate retains plasticity; anima's CE-saturated ckpts (final
   CE ~0.003) are the opposite of plastic. L1 inherits *frozen* saturation, not
   *plastic* memory. The analogy motivates L1 but does not vindicate it.
8. **No fire, no measurement** — $0 design-tier. All claims about "lineage of
   defects" are *predictions* from prior measured evidence (`§11-A`, `§9`,
   `B-ATTRACTOR`), not new measurements. They are falsifiable by a future fire
   but §30 argues that fire is low-value now.
9. **Cell-pool merge bound `[2,64]`** mirrors B-MITOSIS-5's verification spec
   (.clm v1 P2), not the lib's `max_cells=128` — chosen for battery consistency
   with the existing MITOSIS closed-form. A real impl would reconcile the two.
10. **`g_clm_from_scratch` itself may merit user review independent of L1** —
    the rule conflates "no external substrate" (a strong, defensible identity
    principle) with "no anima-self continuity" (a much stronger claim that
    forecloses the human-consciousness path entirely). §30 surfaces this but
    does not resolve it — it is a user governance question.
11. **`f1/f2/f3` + `B-IDENTITY-5` safe** — battery anchors are integer
    monotonicity, Boolean set partition, integer cardinality clamp, Boolean
    reduction. No σ/τ/φ/J₂ derivation; no corpus generated; no helper-token
    surface.
12. **Stop-hook frontier-exhaustion signal acknowledged** — §30 is a *lateral*
    candidate explicitly, and its honest outcome is a design-close. It does not
    claim to advance the north-star; `GOAL.md` distance is unchanged (`§15`
    milestone: GOAL unsolved, irreducible bottleneck = `§1.1`).
