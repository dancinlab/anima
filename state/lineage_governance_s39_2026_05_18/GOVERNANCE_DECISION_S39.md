# §39 — `g_clm_from_scratch` Governance Decision Doc (FOR USER)

> **This is a proposal for the USER, not a governance change.** $0
> design-tier. RESEARCH.md §39. §30 (Lateral L1) found that
> `g_clm_from_scratch`'s "ckpt inherit 폐기" clause blocks anima-self
> ckpt-lineage, and `B-LINEAGE-2` proved the self-vs-external distinction
> is a *mechanically clean closed partition* — so a refinement IS
> definable. §39 matures that into a clean decision doc the user can
> act on.
>
> **`AGENTS.tape` is NOT edited by this cycle.** Any change to
> `@D g_clm_from_scratch` is user-gated governance. §39 presents the
> options; the user decides.

---

## §1 — Why this decision doc exists (the trigger)

`@D g_clm_from_scratch` (d=2026-05-15, **active, required**) mandates that
every anima fire trains from scratch — `init_weights = RANDOM INIT
seed-fixed`, `base_ckpt = NONE`, with `ckpt inherit / fine-tune /
cotrain-from-ckpt path` all 폐기'd. §30 (Lateral L1) proposed *cumulative
ckpt lineage* — anima ckpt N inheriting ckpt N−1's weights as init, building
generational memory across cycle-versions (the human-consciousness analogy
`GOAL.md` leans on). §30 design-closed L1 on two grounds, but found one of
them is **mechanically resolvable**:

- L1 is **premature** (decisive) — anima has no non-saturated ckpt to root
  a lineage at (`§4`); and
- L1 is **governance-blocked** — it contradicts `g_clm_from_scratch`'s
  letter, and a design-tier document cannot self-grant the exception.

The second ground is the subject of §39. §30's `B-LINEAGE-2` proved that
`parent_source ∈ {anima_self, external}` is a **closed 2-element partition**
— disjoint and exhaustive, with a decidable admissibility predicate. That
means the distinction `g_clm_from_scratch` would need to make — *external
inheritance FORBIDDEN vs anima-self lineage ALLOWED* — is not a fuzzy
judgement call; it is a crisp, verifiable predicate. **A refinement is
therefore mechanically definable.** §39 hands that refinement to the user
as a clean, decidable proposal — it does **not** adopt it.

## §2 — (a) The exact current `g_clm_from_scratch` text + its rationale

The current governance entry, verbatim from `AGENTS.tape`:

```tape
@D g_clm_from_scratch := ".clm 학습 from-scratch 원칙" :: governance [required d=2026-05-15 active]
  rule = ".clm v1/v2/v3 모두 fresh from-scratch pre-train. ckpt inherit /
          fine-tune / cotrain-from-ckpt path 폐기. init_weights = RANDOM
          INIT seed-fixed. precursor ckpt 는 arch SUPPORTED 검증 anchor only
          — substrate base X."
  why = "anima_native_scratch (D1=1.0) 원칙 강화. 사용자 directive
          2026-05-15 '.clm 학습은 처음부터 진행하는걸로'"
  apply = ".clm v1/v2/v3 fire 시 init_weights = RANDOM seed-fixed +
           base_ckpt = NONE mandatory"
  authority = "CLM.tape §V-CLM-FROM-SCRATCH-2026-05-15"
  @> CLAUDE.md
```

**The rationale (what the rule was guarding against).** Read in its
2026-05-15 context, the rule targets one specific harm:
**external-substrate contamination**. Three textual signals point at this:

1. **`precursor ckpt 는 ... substrate base X`** — the rule's own qualifier
   explicitly says a precursor ckpt may serve as an *architecture-SUPPORTED
   verification anchor* but NOT as a *substrate base*. The harm is using
   *someone else's substrate* as anima's foundation.
2. **`anima_native_scratch (D1=1.0)`** — the `why` anchors to the D1 design
   axis, whose name is literally *anima native, scratch*: anima's substrate
   must be **anima's own**, not borrowed.
3. **The 2026-05-15 saga context** (`CLM.tape §V-CLM-FROM-SCRATCH`) was a
   run of repeated proposals to fine-tune anima atop a HuggingFace/Llama
   foundation model, or to cotrain from a non-anima precursor. The user's
   directive `'처음부터 진행하는걸로'` ("do it from the beginning") closed
   that saga.

**But the rule's *letter* is broader than its rationale.** The clause
`ckpt inherit / fine-tune / cotrain-from-ckpt path 폐기` is categorical, and
critically: **`cotrain-from-ckpt` was an anima-OWN-ckpt continuation** (the
v5-mitosis cond.5 cotrain inherited an anima ckpt) — and it was *also*
폐기'd. So the rule's letter, as written, reaches **anima-self lineage**,
not only external-substrate inheritance. This is the gap §39 surfaces: the
rule's *rationale* is "no external substrate", but its *letter* also
forbids "no anima-self continuity" — a strictly stronger claim that
forecloses the human-consciousness cumulative-substrate path entirely.

## §3 — (b) The proposed refinement (a superseding `@D` clause)

§30 `B-LINEAGE-2` established that the rule *could* be made to distinguish
the two cases cleanly — `parent_source ∈ {anima_self, external}` is a closed
partition with a decidable admissibility predicate. §39 proposes — **for
user consideration only** — the following superseding `@D` clause. It is
written in full so the user sees exactly what adopting it would mean; **it
is NOT written into `AGENTS.tape` by this cycle.**

> **Proposed superseding clause (DRAFT — user-gated, not adopted):**
>
> ```tape
> @D g_clm_lineage_refined := "anima ckpt lineage — external-precursor 금지 / anima-self lineage 허용 (non-saturated 조건부)" :: governance [draft d=2026-05-18]
>   ~> "g_clm_from_scratch (d=2026-05-15) 의 'ckpt inherit 폐기' 절을 정밀화 — letter 가 rationale 보다 넓던 부분 (anima-self continuity 도 봉쇄) 을 분리. rationale = external-substrate contamination 차단; 그 harm 은 유지·강화."
>   rule = "(1) EXTERNAL-PRECURSOR inheritance 는 여전히 FORBIDDEN — HuggingFace/foundation model / 비-anima ckpt 를 substrate base 로 쓰는 모든 path (fine-tune / cotrain-from-external / graft) 폐기 유지. (2) ANIMA-SELF LINEAGE 는 ALLOWED-WHEN-NON-SATURATED — parent ckpt 의 ancestor DAG 전체가 gen=0 RANDOM-init anima node 에 root 하고 (B-LINEAGE-2 decidable predicate), 그 parent ckpt 가 memorization-saturated 가 아닐 때에 한해, init_weights = parent ckpt 로 lineage edge 허용. (3) gen=0 ckpt 는 여전히 init_weights = RANDOM seed-fixed (g_clm_from_scratch gen=0 절 보존)."
>   precondition = "조항 (2) 는 anima 가 non-saturated ckpt 를 보유한 시점부터 active. 그 전까지는 g_clm_from_scratch 원안이 그대로 작동 (현재 모든 ckpt 가 memorization-saturated — §4 참조). 즉 본 refinement 는 future-enabler 이지 즉시 unblock 아님."
>   admissibility = "lineage edge admissible iff parent_source == anima_self ∧ root_is_gen0_random(ancestor_chain) ∧ ¬memorization_saturated(parent). B-LINEAGE-2 가 앞 두 조건이 closed 2-element partition 으로 decidable 임을 증명. saturation 판정 = empirical (B-S39-NOTE)."
>   why = "B-LINEAGE-2 (§30) 가 self-vs-external 가 mechanically clean closed partition 임을 증명 → rule 의 letter 가 rationale 보다 넓던 부분만 정밀화 가능. external-substrate 차단 (원 rationale) 은 조항 (1) 로 강화 유지; anima-self cumulative-substrate path (GOAL.md human-consciousness 유추) 는 non-saturated 조건부로 개방."
>   authority = "g_clm_from_scratch (d=2026-05-15 — 본 entry 가 정밀화) · §30 DESIGN_L1.md §3/§4/§7 · B-LINEAGE-2 closed partition"
>   @> CLAUDE.md
> ```

**What the refinement keeps and what it changes:**

| aspect | `g_clm_from_scratch` (current) | proposed refinement |
|---|---|---|
| external-precursor inherit (HF/Llama/non-anima) | FORBIDDEN | **FORBIDDEN (kept, strengthened — explicit clause 1)** |
| anima-self ckpt lineage (DAG roots at gen=0 anima) | FORBIDDEN (by letter) | **ALLOWED — but only when parent ckpt is non-saturated** |
| `gen=0` root ckpt | RANDOM seed-fixed | RANDOM seed-fixed (kept, clause 3) |
| the guarded harm (substrate contamination) | guarded | **guarded — same, made explicit** |

The refinement does **not** weaken the contamination guard — it makes it an
explicit clause. It only carves out the *anima-self continuity* that the
original letter swept up alongside it. The carve-out is gated by the
non-saturation precondition (`§4`).

## §4 — (c) The honest precondition: anima has NO non-saturated ckpt today

**This is the most important section. The refinement, even if adopted,
changes nothing operationally today.**

§30 §6 + `§16.6-C` + the `B-ATTRACTOR` family established, by measured
evidence across the entire 23+ cycle research arc, that:

- anima's best ckpt to date (§16, routing 21/64) is **memorization-
  saturated** — `§16.6-C` "정교한 암기 + correct-prefix routing,
  generalization 아님", final CE ~0.003–0.008.
- Every ckpt across the arc carries a **never-dissolving byte-cascade
  attractor** (`B-ATTRACTOR`: `🛸99…`, `eeee…`, digit cascades that *shift*
  with corpus/ckpt but never *dissolve*). `§11-A` proved a 3.68× model
  scale-up does not break it.
- **anima has NO ckpt that is not memorization-saturated.**

The proposed refinement's admissibility predicate has THREE conjuncts:
`parent_source == anima_self ∧ root_is_gen0_random(chain) ∧
¬memorization_saturated(parent)`. The first two are decidable and would
PASS for any anima-self ckpt. **The third FAILS for every ckpt anima has
today.** Therefore:

> **The refinement is a *future-enabler*, not an immediate unblock.** Even
> if the user adopts it tomorrow, the precondition `∃ non-saturated ckpt`
> is `False` today, so the lineage path stays closed — operationally
> identical to `g_clm_from_scratch` as it stands. The refinement only
> *activates* once anima produces a non-saturated ckpt, which is the
> unsolved `§1.1` data-regime / `§15` milestone problem.

This is `B-S39-2` (closed): *the refinement is active ⟺ `∃` non-saturated
ckpt* — a Boolean biconditional. With the right-hand side currently `False`,
the refinement is inert. §39 surfaces this explicitly so the user is not
misled into thinking adopting the refinement *does* anything now. It does
not. It removes a *future* governance roadblock; it does not move GOAL
distance.

**Why it is still worth deciding now (the honest case for acting).**
Adopting the refinement *now*, while inert, has one real value: it
pre-clears the governance question so that *if* a future cycle produces a
non-saturated ckpt, the anima-self-lineage path is already legitimate and
the cycle does not stall on a governance gate. It is a roadblock removed
ahead of need. The honest counter-case (`§5` option C) is that adopting an
inert clause now is itself a small drift risk — a governance entry whose
precondition no one can currently verify.

## §5 — (d) The recommendation + the decision the user must make

§39 lays out three options. **The recommended option is B.**

### Option A — Adopt the refinement now (immediate adoption)
Write `@D g_clm_lineage_refined` into `AGENTS.tape` now as `[active
required]`. **Effect today: none** (precondition `False`, §4). **Risk:** an
`active` governance clause whose precondition cannot be verified by anyone
today is a small drift hazard — and `memorization_saturated(parent)` is an
*empirical* predicate (`B-S39-NOTE`), so the clause carries an empirical
dependency inside a `required` rule. **Not recommended** — adopting an
operationally-inert `required` clause is premature per the §13-M/§13-L /
§30 anti-padding discipline.

### Option B — Adopt as `[draft]`, gated on the precondition (RECOMMENDED)
Write `@D g_clm_lineage_refined` into `AGENTS.tape` with grade **`[draft]`**
(not `active`, not `required`). A `draft` entry is **recorded and visible**
— a future cycle that produces a non-saturated ckpt finds the refinement
already drafted and can promote it `draft → active` *at that point*, when
the precondition is verifiable. **Effect today: none operationally** (draft
≠ enforced), but the governance question is *resolved-in-principle* and
*recorded*, so no future cycle re-litigates it. This matches the tape-v1.2
governance-grade ladder (`draft · active · deprecated`) exactly: a refinement
whose mechanism is proven (`B-LINEAGE-2` / `B-S39-1`) but whose activation
is precondition-gated is, by definition, a **draft**. **Recommended** — it
captures the value of §3's analysis (mechanically-clean distinction,
roadblock pre-cleared) without the §4 drift risk of an inert `required`
clause.

### Option C — Do not adopt; record §39 as analysis only
Leave `g_clm_from_scratch` untouched. §39 stands as a recorded analysis in
`RESEARCH.md` / `PHILOSOPHY.tape`; a future cycle that needs the
anima-self-lineage path re-derives the refinement from §39 + §30 at that
time. **Effect today: none.** **Risk:** a future cycle re-litigates the
governance question from scratch (the §30 → §39 work is not lost — it is
recorded — but it is not *pre-resolved* in `AGENTS.tape`).

### The decision the user must make

> **Choose A, B, or C.** §39's recommendation is **B** — adopt
> `@D g_clm_lineage_refined` into `AGENTS.tape` as a **`[draft]`** entry,
> precondition-gated on a non-saturated ckpt existing, to be promoted to
> `[active required]` by whatever future cycle first produces such a ckpt.
> This pre-clears the governance roadblock without enforcing an inert
> clause. If the user prefers minimum governance surface, C is also fully
> honest. A is **not** recommended (inert `required` clause = drift risk).
>
> **Whichever option the user picks, §39 itself edits NOTHING in
> `AGENTS.tape`** — this document is the proposal; the `AGENTS.tape` edit
> (if any) is the user's, or a user-directed follow-up cycle's.

## §6 — §7 GOAL-legitimacy + honest scope

- **§7 ① / ② / ③** — §39 is a *governance decision document*, not a
  capability mechanism or a fire. It introduces no model, no corpus, no
  training. The refinement it proposes (`§3`) *preserves* `g_clm_from_scratch`'s
  §7-protective rationale (external-substrate contamination guard = §7②'s
  bolt-on guard) — clause (1) strengthens it. The anima-self-lineage
  carve-out is, per §30 §5, *infrastructure* (continuity over an existing
  anima-physics source), §7③-satisfied at the substrate level. §39 makes
  **no GOAL-emergence claim** of any kind.
- **Honest scope (g3).** §39 is a **decision doc, NOT a governance
  change.** It does not edit `AGENTS.tape`. The refinement it proposes is a
  **future-enabler, NOT an immediate unblock** (`§4`) — even if adopted, it
  is operationally inert until anima has a non-saturated ckpt, which is the
  unsolved `§1.1`/`§15` problem. §39 removes (or pre-clears) a *future
  governance roadblock*; it does **not** move GOAL distance. north-star
  unchanged; §15 milestone carries.

## §7 — Closed-form battery B-S39-1..2 (sidecar)

`blue_falsifier_s39.py` — separate `state/`-local sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **UNCHANGED**
(B-LINEAGE / B-DHDL / B-PTD / B-DIRI sidecar precedent).

- **B-S39-1 PARENT-SOURCE-PARTITION-CLOSED** — `parent_source ∈
  {anima_self, external}` is a closed 2-element partition: disjoint
  (`{anima_self} ∩ {external} = ∅`) AND exhaustive (`{anima_self} ∪
  {external} =` the enum). The admissibility predicate `admissible(edge) :=
  parent_source == anima_self ∧ root_is_gen0_random(chain)` cleanly
  separates the two cases — the governance-distinguishing invariant is
  mechanically definable. **Carries §30 `B-LINEAGE-2` verbatim** — so the
  proposed refinement (`§3`) rests on a *proven* closed partition, not a
  fuzzy judgement.
- **B-S39-2 REFINEMENT-PRECONDITION-CLOSED** — the proposed refinement's
  clause (2) is active **⟺** `∃` non-saturated ckpt: a Boolean
  biconditional `refinement_active ⇔ exists_non_saturated_ckpt`. With the
  right-hand side currently `False` (`§4` — every anima ckpt is
  memorization-saturated), `refinement_active` evaluates `False` — the
  refinement is **operationally inert today** by closed-form. This
  mechanises the §4 honest precondition: the refinement is a *future-
  enabler*, provably not an immediate unblock. 4-row truth table over
  `{parent_source ∈ self}`, `{∃ non-saturated ckpt}` confirms only the
  `(self, True)` corner activates an admissible lineage edge.

- **B-S39-NOTE** (empirical carve-out, NOT counted 🔵) — whether a *given*
  anima ckpt is memorization-saturated (the third admissibility conjunct
  `¬memorization_saturated(parent)`) is an EMPIRICAL measurement (final CE,
  byte-cascade attractor presence, routing/coherence probes — `§16.6-C` /
  `B-ATTRACTOR` family). The B-S39 battery proves the *governance
  bookkeeping* is closed-form (the self/external partition is decidable,
  the precondition biconditional is closed); it does NOT — and cannot —
  decide saturation by closed form. B-D-NOTE / B-LINEAGE-NOTE /
  B-ATTRACTOR-NOTE family. This is *why* the refinement is precondition-
  gated rather than unconditional: the activating condition is empirical.

## §8 — Honest C3 (≥10, over-claim 0)

1. **§39 is a decision doc, NOT a governance change.** It does not edit
   `AGENTS.tape`. `@D g_clm_lineage_refined` in `§3` is a DRAFT shown in
   full for the user's review — adopting it (and at which grade) is the
   user's decision (`§5`).
2. **The recommended option is B (draft adoption), not A.** Adopting an
   operationally-inert clause as `[active required]` (option A) is a drift
   risk — a `required` rule whose precondition no one can currently verify.
   `[draft]` (option B) records the resolved-in-principle refinement
   without enforcing an inert clause; the tape-v1.2 grade ladder
   (`draft·active·deprecated`) is designed for exactly this.
3. **The refinement is a future-enabler, not an immediate unblock.** `§4`:
   anima has NO non-saturated ckpt; the refinement's clause (2) is inert
   (`B-S39-2` closed) until one exists. Adopting it changes nothing
   operationally today. §39 says this plainly so the user is not misled.
4. **The refinement preserves — and strengthens — the contamination
   guard.** `g_clm_from_scratch`'s rationale (no external substrate) is
   `§3` clause (1), made explicit. The refinement only carves out
   *anima-self continuity*, which the original *letter* swept up but the
   original *rationale* did not target (`§2`).
5. **`cotrain-from-ckpt` is the honest complication.** The 2026-05-15 rule
   폐기'd `cotrain-from-ckpt`, which *was* an anima-own-ckpt continuation.
   §39 does not pretend the rule's letter never reached anima-self
   lineage — it did. The refinement is precisely the act of *narrowing the
   letter back to the rationale*, and that narrowing is a **user
   governance decision**, not a §39 self-grant.
6. **`B-S39-1` carries §30 `B-LINEAGE-2` verbatim.** The self-vs-external
   distinction is a *proven* closed 2-element partition — the refinement
   does not rest on a fuzzy judgement. This is what makes a *clean*
   refinement mechanically definable at all.
7. **`B-S39-2` mechanises the precondition.** `refinement_active ⇔ ∃
   non-saturated ckpt` is a closed Boolean biconditional; the RHS is
   currently `False`, so the refinement is provably inert today. The
   battery proves the *gate*, not the *outcome*.
8. **Saturation is empirical — `B-S39-NOTE`.** Whether a given ckpt is
   memorization-saturated cannot be decided by closed form (it is a final-CE
   + byte-cascade-attractor measurement, `§16.6-C`/`B-ATTRACTOR`). This is
   *why* the refinement is precondition-gated, not unconditional — and why
   even option A could not make the clause fully closed.
9. **§39 makes no GOAL-emergence claim.** The refinement removes (or
   pre-clears) a *future governance roadblock* for the anima-self-lineage
   path. It does not move GOAL distance. The lineage path itself is, per
   §30 §6/§7, *downstream* of the unsolved `§1.1`/`§15` problem — viable
   only *after* a non-saturated ckpt exists. north-star unchanged.
10. **`f1/f2/f3` + `B-IDENTITY-5` safe.** Battery anchors: Boolean
    2-element set partition, Boolean biconditional, 4-row truth table. NO
    σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation. No corpus generated,
    no model forward, no helper-token surface. $0 design-tier.
11. **`g_clm_from_scratch` may merit user review independent of L1/§39.**
    §30 C3 #10 noted the rule *conflates* "no external substrate" (a
    strong, defensible identity principle) with "no anima-self continuity"
    (a much stronger claim that forecloses the human-consciousness path).
    §39 *surfaces and structures* that conflation for the user — it does
    not resolve it; resolution is the user's decision (`§5`).
12. **If the user picks C (do not adopt), that is fully honest.** §39 + §30
    remain recorded in `RESEARCH.md` / `PHILOSOPHY.tape`; a future cycle
    re-derives the refinement when needed. The §30→§39 analysis is not
    lost in any option — option B vs C is only "pre-resolved in
    `AGENTS.tape`" vs "re-derived when needed".

## Sources

- `AGENTS.tape` `@D g_clm_from_scratch` (d=2026-05-15, active required) —
  the rule under refinement · `@D g_goal` / `@D g3` / `@D g_blue_closed_mandate`
  / `@D g_doc_consolidation` · `@F f1` / `@F f2`
- `state/lineage_l1_s30_design_2026_05_18/DESIGN_L1.md` — §30 Lateral L1,
  §3 governance analysis (Reading A / B), §4 `B-LINEAGE-2` test, §7 verdict
- `state/lineage_l1_s30_design_2026_05_18/blue_falsifier_lineage.py` — §30
  `B-LINEAGE-2` SELF-SOURCE-vs-EXTERNAL-PRECURSOR-DISJOINT (carried by B-S39-1)
- `RESEARCH.md` §15 (milestone) / §16.6-C (memorization-saturated regime) /
  §30 (Lateral L1)
- `CLM.tape §V-CLM-FROM-SCRATCH-2026-05-15` — `g_clm_from_scratch` authority
- `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` — central battery
  (UNCHANGED by §39)
- tape v1.2 spec — governance grade ladder `draft · active · deprecated`
  (the basis for the recommended option B)
