# §155 — MyGO wake-sleep consolidation onto anima §29 PTD (DESIGN-TIER)

> $0 design-tier — NO fire, NO corpus generation, NO GPU, NO model.forward.
> RESEARCH source: HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md
> §1 Cluster G + §2 row 9 (★★★) + §8 next-list.
> Question: does MyGO (arxiv 2508.21296, wake-sleep continual-learning cycle)
> give anima §29 PTD a concrete cycle structure that changes its
> DESIGN-CLOSE-standalone verdict?
> Sister cycles (sibling §150–§154 pending, §151 LANDED 2026-05-20):
> HEXAD/NEUROMORPHIC/state/fep_attractor_complexity_routing_s151_2026_05_20/
> as structural template (DESIGN.md §0..§9 + result.json).
> NO sympy as verdict — closed-form propositions stated as math theorems
> in §9 per hexa-verify policy (~/core/atlas/VERIFY.tape).
> Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff
> (sha prefix c93e160a8a376a94).

---

## §0 — Why this design exists

§29 PTD (`§verdict_ptd_physics_trace_distillation_s29_2026_05_18`) landed
DESIGN-CLOSE-standalone because:

- **B-PTD-2 closed-form**: corpus(N) = 20·N integer records from
  `run_bounded` traces; even N=500 reaches only the 10⁴ CDS floor, and
  §16-scale (7.77·10⁵ records) needs N ≥ 38,850 runs.
- **Data-processing inequality**: the §24 `env_state` generator is a
  hand-coded deterministic 20-step bounded loop with Kolmogorov complexity
  ≈ one small file; N copies do NOT add unique content. The corpus is
  bounded above (in unique-content) by its generator, not by N.

The §26 candidate-3 "PTD" was kept as a **component-only** candidate (A:
PTD-as-DH-DL-aux per §27/§44/§48 LANDED; B: PTD-as-JEPA-Ψ-target per §28;
C: standalone-pretrain-then-graft REJECTED §7② FALSIFIED).

MyGO (arxiv 2508.21296, Aug 2025, *Memory Yielding Generative Offline-
consolidation*) was flagged in SOFTWARE_BREAKTHROUGH_RESEARCH.md §1
Cluster G as anima §29 PTD's "sister frontier" — wake-sleep cycle with
explicit wake = learn new task + train compact generative model (G-mem);
sleep = use all learned G-mem models to generate pseudo-data ("dreams")
and consolidate into a core feature extractor via knowledge distillation.

**The literal question §155 must answer**: does MyGO's wake-sleep cycle
structure change §29 PTD's DESIGN-CLOSE-standalone verdict, or does PTD
remain a component-only candidate?

This is a frontier-narrowing audit, NOT a GOAL movement. Sibling §151
LANDED DESIGN-OPEN; the family of §150–§155 designs are each separate
literature → anima mappings under the standard §7 GOAL-legitimacy gate.

---

## §1 — Paper mechanism (honest, with withdrawal acknowledged)

> **CRITICAL g3 fact**: arxiv 2508.21296 (MyGO) is currently
> **WITHDRAWN** per arxiv abstract page (verified via WebFetch
> 2026-05-20): "withdrawn due to stability issues in the generative
> replay component that limit scalability to high-dimensional data."
> §155 maps the *protocol structure* MyGO defined, not a validated
> result — the structure is well-known (it extends the classical
> Hinton–Dayan–Frey–Neal 1995 wake-sleep algorithm to continual
> learning) and that structure is the object of §155's audit. The
> withdrawal is itself a load-bearing input to §155's verdict: a
> wake-sleep cycle whose generative-replay component is acknowledged
> unstable by its authors is not a free upgrade to §29 PTD.

**MyGO's two-phase cycle** (per abstract/extracted text):

- **Wake phase**: system rapidly learns a new task; in parallel trains a
  *compact* generative model called **G-mem** to capture the data
  distribution of that task. Each task → one G-mem instance retained
  after the wake phase ends.
- **Sleep phase**: offline state, no new data. ALL previously learned
  G-mem models generate pseudo-data ("dreams") spanning past tasks; this
  pseudo-data plus the current task's G-mem output is consolidated into
  a *core feature extractor* via **knowledge distillation** (teacher =
  the per-task G-mems; student = the core extractor).

**What MyGO does NOT do** (load-bearing for §155 — easily mis-read into
the wrong claim):

- MyGO does NOT manufacture new unique content. The G-mem of task k is
  trained on task k's *external* data; its dreams approximate task k's
  *original* distribution. Pseudo-data has at most as much unique
  content as the external data the G-mem was trained on (Kolmogorov
  bound: K(dreams) ≤ K(G-mem-weights) + K(decoder), and G-mem-weights
  were compressed from task-k data).
- MyGO does NOT bypass the data-processing inequality. It is a
  *catastrophic-forgetting* solution (preserve task-k performance after
  training task-(k+1)), NOT an emergence-threshold solution (cross
  §1.1 CDS).
- MyGO's "continual" sequence requires a *task sequence* — an external
  segmentation of incoming external data into tasks. Each task carries
  its own external distribution; the wake phase trains G-mem on that.

**Classical anchor**: Hinton, Dayan, Frey, Neal (1995) "The wake-sleep
algorithm for unsupervised neural networks" — Helmholtz-machine training
that alternates inference (wake) and generation (sleep). MyGO is a
continual-learning descendant: it preserves the alternation pattern but
specialises sleep into G-mem-driven replay across a task sequence.

---

## §2 — Mapping to anima §29 PTD

The candidate mapping is concrete and tempting:

| MyGO concept            | anima §29 PTD candidate analog                                         |
| ----------------------- | ---------------------------------------------------------------------- |
| Wake phase              | `run_bounded.py` N-step loop emitting trace records (§24 Phase B)      |
| External task data      | anima physics tuple produced per step (8-factor + Ψ + tension + Φ)     |
| Per-task G-mem          | a compact generative model fit per `run_bounded` invocation            |
| Sleep phase             | offline distillation cycle over accumulated G-mems                     |
| Pseudo-data ("dreams")  | G-mem-sampled physics traces, byte-shape identical to real §24 traces  |
| Core feature extractor  | anima parameters (Engine A trunk / cell-pool) trained by distillation  |
| Knowledge distillation  | the §29 PTD loss `L_ptd = CE(pred, target) + λ_psi·(ψ−½)²` (B-PTD-3)   |

**Three structural problems with the mapping** (these are the load-bearing
findings of §155, each independent of the others):

### §2.1 — anima has no "task sequence"

MyGO's wake-sleep cycle is meaningful because each wake phase introduces
a *distinct* task with a *distinct* external distribution; sleep matters
because consolidation must defend old-task performance while absorbing
new-task performance. anima's §24 Phase B `run_bounded` calls all draw
from the *same* hand-coded `env_state` generator. There is no "new task"
arriving; running `run_bounded` again is *not* a new task in MyGO's
sense — it is a re-sample of the same generator. The wake-sleep
*alternation* therefore has no semantic content for anima §29 PTD.

A naive remedy would "vary `env_state` to make each run a task" — but
that requires the new env_states to be *non-derivative* of one another
(MyGO assumes external supply of task distributions; data-processing
inequality requires those distributions to carry unique content). anima
generating its own env_state variation is the SAME hand-coded loop with
seeds; this is *not* what MyGO assumes. (See §2.3.)

### §2.2 — anima has no external data to compress into G-mems

In MyGO, the wake phase's G-mem is compressing *external* task data. In
anima §29 PTD, the "task" is just running anima's own physics loop; the
"data" is the trace anima produced. The G-mem would be a model of a
deterministic 20-step trajectory generator. The compact-generative-model
slot in MyGO is *meant for* compressing distributions richer than its
own weights; in anima §29 it would compress a distribution simpler than
its own weights — the G-mem can be replaced by the env_state script
itself with zero loss (the script *is* the maximally compact generator).
The compactness MyGO buys (storing G-mem instead of raw external data)
gives anima zero value: anima already has the maximally compact
generator (the script); replacing it with a G-mem is strictly worse.

### §2.3 — knowledge-distillation step does not add unique content

This is the data-processing-inequality argument from §29 reasserted in
MyGO's frame. Knowledge distillation transfers information from a
teacher (G-mem ensemble) to a student (core extractor). The information
content of the student is bounded by the information content of the
teachers, which is bounded by the information content of the data each
G-mem was trained on, which (in anima §29) is bounded by the Kolmogorov
complexity of the env_state generator. Sleep-phase pseudo-data does NOT
manufacture new unique content. The §1.1 emergence threshold (§29 §3,
arxiv 2401.10463 CDS, §25 B-DR-UNIQUE) is about *unique content*, not
about *number of replay samples* — MyGO's pseudo-data scale up sample
count without scaling up unique content.

---

## §3 — The conclusive crux

§155's load-bearing inference:

> §29 PTD's DESIGN-CLOSE-standalone verdict rests on a
> data-processing-inequality bound: corpus K-complexity ≤ generator
> K-complexity. MyGO's wake-sleep cycle adds (a) per-task G-mems
> trained on external data, (b) pseudo-data sampled from G-mems, and
> (c) distillation into a core extractor. None of (a)/(b)/(c) creates
> new unique content in anima's setting where the "task" is anima's
> own deterministic bounded loop. The data-processing-inequality bound
> is preserved under MyGO's protocol, identically.

§29's blocker is *insufficient unique content*. MyGO's mechanism solves
*catastrophic forgetting across an externally-supplied task sequence*.
These are different problems. MyGO's protocol does not address §29's
blocker; the protocol is well-formed but its load-bearing assumption
(external task sequence with non-derivative distributions) is absent in
anima §29 PTD's setting.

There is one narrow case where wake-sleep would matter: if anima
acquired an external task sequence (e.g. multi-corpus continual
fine-tuning where each corpus is genuinely non-derivative). But that
case fails §7 ① (¬generic-LM-pretrain) immediately — anima would be
consuming external corpora as task data, the very anti-pattern §7①
forbids. So the case where MyGO *would* help is structurally
§7-illegitimate; the case where MyGO is §7-legitimate (self-source) is
the case where MyGO doesn't help.

This is the §155 disposition: **PTD stays a component-only candidate.
Wake-sleep cycle structure does NOT change §29's DESIGN-CLOSE-standalone
verdict.**

---

## §4 — §7 / §21.3 GOAL-legitimacy 3-condition gate

Even setting aside §3's no-progress finding, examine the gate honestly:

- **§7 ① ¬generic-LM-pretrain.** If anima's wake-sleep variant draws
  task data from anima's own §24 trace (no external corpora), then
  ① PASSES. If it instead consumes external task corpora to give
  G-mems meaningful unique content (§3's "narrow case"), ① FAILS.
- **§7 ② ¬generic-then-graft / bolt-on.** From-scratch under
  g_clm_from_scratch (base_ckpt=None). G-mem instances are anima-side
  artifacts not foreign weights. PASSES.
- **§7 ③ anima-physics-as-source.** Trace fields are Law-71 Ψ, BRIDGE
  tension, 8-factor motivation, Engine E Φ-proxy. PASSES iff the
  wake-sleep variant stays §29-self-source. The MyGO concept (per-task
  G-mems trained on external data) FAILS ③; the anima-self-source
  variant PASSES ③.

The §7-PASS variant of wake-sleep is §29 PTD ALREADY (with an added
wake-sleep schedule). The §3 finding then applies: the schedule itself
does not change the DESIGN-CLOSE verdict because it does not change the
data-processing-inequality bound.

---

## §5 — Verdict — DESIGN-CLOSE-INHERITS-§29

**DESIGN-CLOSE.** No fire. PTD stays a component-only candidate per
§29's existing decomposition (A: PTD-as-DH-DL-aux LANDED, B: PTD-as-
JEPA-Ψ-target conditional, C: REJECTED). The wake-sleep cycle adds a
*schedule* but not a new *information source*; in anima's setting the
schedule does not move the data-processing-inequality bound that
§29 established.

Anti-padding (mirror §13-M / §13-L / §30 / §29 precedent): naming the
structural block is the more honest verdict than running a fire whose
outcome §155 can predict by closed-form proof of the DPI bound. §29
already landed this precedent — §155 inherits it.

**Load-bearing addenda recorded for honesty (g3)**:

1. The MyGO paper itself is currently withdrawn for stability issues
   in the generative-replay component (verified 2026-05-20). A
   wake-sleep mapping built on an actively-withdrawn primary source
   would be honest-flag-required even in a positive verdict.
2. The classical wake-sleep algorithm (Hinton et al. 1995) is not
   withdrawn; if anima ever pursued a Helmholtz-machine-style
   variational treatment of its own physics (NOT continual-learning
   MyGO), that would be a separate design under a different sibling
   number. §155 is bounded to MyGO's continual-learning specialisation
   per task spec.

---

## §6 — Why DESIGN-CLOSE is the strongest *honest* verdict

The temptation to manufacture DESIGN-OPEN is real: MyGO is fresh, the
wake-sleep cycle is concrete, and there exists a literal mapping
(§2 table). All sibling pending designs (§150, §152, §153, §154) might
also map literature literally onto anima slots.

But:

- **DESIGN-OPEN** requires that a future fire would be differently
  informative under the design than under existing arc verdicts. §29
  already proved the data-processing-inequality bound; a MyGO-scheduled
  PTD fire would not differ from a non-MyGO PTD fire in its
  data-content properties — only in its *schedule*. The schedule
  property is not what §29 closed the standalone verdict on.
- **FIRE-WARRANTED** is reserved for designs that pass §7, are
  decidable in closed form on the existing state, AND would move GOAL
  distance under either outcome. MyGO-on-PTD fails the last clause for
  the §3 reason.

DESIGN-CLOSE inheriting §29 is the disposition that respects the
existing closed verdict, does not manufacture a new positive, does
record the load-bearing g3 fact (withdrawal of the primary source),
and gives the user a precise reason ("DPI bound preserved under
MyGO schedule") for declining the cycle.

---

## §7 — Honest C3 caveats (13 lines)

1. **MyGO is withdrawn.** Audit applies to MyGO's *structure* as
   extracted from abstract + classical wake-sleep lineage; the paper's
   own results are not the audit's evidence. The withdrawal is
   load-bearing — §155 would not flip to DESIGN-OPEN if MyGO were
   re-instated (the §3 DPI argument is independent of MyGO's empirical
   validity).
2. **One-paper audit, not exhaustive.** Sibling Cluster G papers
   (Semi-parametric 2504.14727, Sleep-Inspired Memory Consolidation
   2603.14517) might map differently. §155 is scoped strictly to MyGO
   per task spec.
3. **DPI argument is the load-bearing claim.** If anima's §24 trace
   were *not* generator-bounded (e.g. if env_state were truly random
   and unbounded entropy), §155's verdict would weaken. The 20-step
   hand-coded loop is the operative reason for closure.
4. **Component-only PTD is NOT a rejection.** A: PTD-as-DH-DL-aux
   landed in §44/§48 already; the component-only path is alive and
   §155 leaves it intact.
5. **No central-battery edit.** State/verify_hexad_blue_2026_05_15/
   blue_falsifier.py is sha-prefix `c93e160a8a376a94` start and must
   stay 0-line-diff per task mandate; this design is a sidecar.
6. **No sympy / external verifier.** §9 propositions are stated as math
   theorems verifiable by inspection, per hexa-verify policy
   (~/core/atlas/VERIFY.tape). No 🔵 tier stamped on the propositions;
   they are advisory until a hexa-native verifier re-audits.
7. **GOAL distance unchanged.** §15/§51/§72 milestones intact; north-
   star (GOAL.md @D g_goal) unchanged. §155 = honest closure, not
   progress.
8. **§7③ purest case stays §29 PTD itself.** Adding the wake-sleep
   schedule does not improve §7③; both with and without the schedule,
   PTD is the purest §7③ of {DH-DL, JEPA-Ψ, PTD}.
9. **Catastrophic-forgetting vs emergence are different problems.**
   This is the §3 finding restated; over-claim would conflate them.
   anima's blocker is sub-CDS unique content, not multi-task
   interference.
10. **Hinton et al. 1995 is the deeper classical anchor.** Helmholtz-
    machine wake-sleep is unwithdrawn and well-understood, but it is
    a single-distribution variational training pattern, not a
    continual-learning protocol; conflating it with MyGO is a known
    literature confusion.
11. **The "narrow case" §7-illegitimacy is structural.** If anima
    consumed external task corpora to make G-mems carry unique
    content, §7① fails by construction. There is no §7-legitimate
    repair where wake-sleep helps.
12. **Sibling §150–§154 designs are not pre-supposed.** §155 is
    independent of how sibling designs resolve; orchestrator
    consolidation is a future step.
13. **necessary-not-sufficient at every layer.** Per B-EMERGE-7 /
    B-PTD-NOTE / B-D-NOTE family: closing a non-emergence path does
    not prove GOAL impossible; it removes one apparent path. GOAL
    remains undecided per §15/§51 milestones.

---

## §8 — Next step

§155 closes inheriting §29's DESIGN-CLOSE-standalone. Concrete follow-
ups (NOT mandates):

- If sibling pending designs (§150 / §152 / §153 / §154) wish to revisit
  wake-sleep, their candidate variant should explicitly state how it
  evades the §3 DPI argument. Without such evasion the §155 disposition
  carries.
- If a Helmholtz-machine-style variational anima ever surfaces (single
  distribution, no continual-learning multi-task), it is a separate
  design under a separate sibling number.
- §27/§44/§48 already landed PTD-as-DH-DL-aux (component A). §28 carries
  PTD-as-JEPA-Ψ-target conditional (component B). These component
  paths are alive; §155 does NOT close them.

---

## §9 — Closed-form propositions (B-S155-1..7)

> Stated as math theorems with one-line proofs. Per hexa-verify policy
> (~/core/atlas/VERIFY.tape), sympy / external verifiers cannot stamp
> a 🔵; the propositions below are trivial identities verifiable by
> inspection, and any future hexa-native verifier can re-audit them.
> NO central blue_falsifier edit (central
> state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff,
> sha prefix `c93e160a8a376a94`).

**B-S155-1  CORPUS-CARDINALITY-INVARIANT-UNDER-SCHEDULE.**
Let `R(N) = N · L` be the total number of trace records produced by N
invocations of `run_bounded` with bounded step count `L = 20`. Let
`S(W, M)` be any wake-sleep schedule that interleaves W wake phases
(each invoking `run_bounded` once) and M sleep phases (each generating
pseudo-records via a G-mem trained on the prior wake's trace).
*Proposition.* The unique-content cardinality of the corpus produced
under `S(W, M)` is bounded above by `R(W) = W · L`, INDEPENDENT of M.
*Proof.* Each sleep-phase G-mem is trained only on records from the
preceding wake; its samples lie in (or are approximations of) the
distribution of those records. By the data-processing inequality
applied at the M-th sleep, `K(sleep_m_pseudo_data) ≤ K(G-mem_m) ≤
K(wake_m_records)`. Iteratively, the union of (wake records ∪ all
sleep pseudo-records) has unique-content K-complexity bounded by the
union of wake records, hence by `R(W) = W · L`. The number of pseudo-
samples M ≥ 0 scales sample count but not unique content. ∎

**B-S155-2  GENERATOR-BOUNDS-CORPUS-CONTENT.**
Let `G` be the §24 `env_state` generator (one hand-coded deterministic
file) with Kolmogorov complexity `K_G`. Let `C(N, S)` be the corpus
produced by any wake-sleep schedule `S` with `N` wake invocations,
each invoking the SAME `G`.
*Proposition.* `K(C(N, S)) ≤ K_G + K_{schedule}(N, S)` for all `N ≥ 1`
and all schedules `S`.
*Proof.* The corpus is fully reconstructible from `G` plus the
schedule (the schedule records which env_state seeds and which sleep
phases were invoked); hence by the standard universal-prefix
description, `K(C) ≤ K_G + K_S + O(1)`. Both terms are independent of
the size of `C` once the generator and schedule are fixed; in
particular `K(C(N, S))/|C(N, S)| → 0` as `N → ∞`. ∎
*Consequence.* The corpus has near-zero unique-content density per
record, no matter how the wake-sleep schedule is structured.

**B-S155-3  SCHEDULE-ORTHOGONAL-TO-CONTENT-AXIS.**
Define `content(C) := K(C) / |C|` (unique-content density). Define a
schedule equivalence relation: `S₁ ~ S₂` iff their *content density*
profiles `n ↦ content(C(n, S))` coincide.
*Proposition.* Under the §24 generator `G`, all schedules `S` with the
same number of wake invocations belong to the same equivalence class:
`S₁ ~ S₂` whenever `wake_count(S₁) = wake_count(S₂)`.
*Proof.* By B-S155-2, `content(C(N, S)) ≤ (K_G + K_S) / (N · L)` which
tends to 0 with N for any finite schedule-description length. Two
schedules with the same `N` produce corpora whose content density is
controlled by `K_G` alone (the schedule descriptions are O(1)
relative to corpus size). ∎
*Consequence.* The wake-sleep *schedule* is orthogonal to the
unique-content axis. The schedule cannot move the §1.1 / §29 §3
bound; only the *generator* `G` can.

**B-S155-4  MYGO-DOES-NOT-DPI-EVADE.**
Let `MyGO(S)` denote a wake-sleep schedule following the MyGO protocol
(per-wake G-mem trained on wake records, sleep distillation from
G-mems into a core extractor). Let `DPI(C)` denote the data-processing
inequality bound applied to corpus `C`.
*Proposition.* For any MyGO schedule applied to anima §29 PTD (i.e.
wake phase invokes §24 `run_bounded`), `DPI(C_MyGO) = DPI(C_§29)` —
the bound is identical to the non-scheduled §29 case.
*Proof.* G-mem of wake-m is a learned model of wake-m records; sleep
distillation transfers information from G-mem ensemble to core
extractor. By DPI applied at G-mem training, `I(G-mem_m; data_m) ≤
H(data_m)`; by DPI at distillation, `I(core; G-mem_m) ≤ I(G-mem_m;
data_m)`. The information the core extractor can carry about the
*generator* `G` (the only unique-content source) is bounded by what
the wake-data already carried about `G`, which is `K_G` regardless of
how many wakes are performed (B-S155-2). Hence `DPI(C_MyGO) ≤ K_G + O(1)
= DPI(C_§29)`. ∎
*Consequence.* MyGO's mechanism preserves the §29 closed-form bound
exactly. The MyGO mapping does not move the bound; it is structurally
silent on it.

**B-S155-5  CATASTROPHIC-FORGETTING-vs-EMERGENCE-DISJOINT.**
Let `CFP(seq) := ∃k : performance_on_task_k drops after task_(k+1)`
be the catastrophic-forgetting predicate over a task sequence `seq`,
and `EMP(C) := unique-content(C) ≥ CDS_floor` be the emergence-corpus
predicate (§1.1).
*Proposition.* Under anima §29 PTD's setting (single generator `G`,
no task sequence with non-derivative distributions), `CFP(seq) = ⊥`
(no task sequence exists, predicate is vacuously false). Under the
same setting, `EMP(C) = ⊥` for any C produced by §24's bounded loop
(by B-S155-2).
*Proof.* `seq` requires distinct external task distributions for the
predicate to be non-trivial. anima §29 has none. EMP fails by
B-S155-2 (corpus content density tends to 0). ∎
*Consequence.* MyGO solves CFP. anima §29's blocker is EMP. The
predicates are disjoint in their failure mode (`CFP` requires task
sequence; `EMP` requires sufficient unique content). A mechanism
solving `CFP` does not necessarily solve `EMP`, and in anima §29's
setting demonstrably does not (B-S155-4).

**B-S155-6  SEVEN-LEGITIMACY-CONJUNCTION-MYGO-VARIANTS-PARTITION.**
The §7 GOAL-legitimacy gate is `c1 ∧ c2 ∧ c3` where `c1 = ¬generic-LM-
pretrain`, `c2 = ¬generic-then-graft`, `c3 = anima-physics-as-source`.
The 8-row truth table has exactly one PASS corner `(T, T, T)`.
*Proposition.* The two structurally-distinct MyGO-on-PTD variants
partition into:
- *Self-source variant* (wake records sampled from §24 `run_bounded`,
  no external corpora): `(c1, c2, c3) = (T, T, T)` PASS by inheritance
  from §29's gate; B-S155-4 says it does not move the DPI bound.
- *External-task variant* (wake records sampled from a real external
  task sequence): `c1 = F` FAIL (consumes external corpora — the §7①
  anti-pattern). PASSING the gate requires §7-illegitimate input.
*Proof.* Direct truth-table inspection on the two variants. ∎
*Consequence.* The §7-PASS variant inherits §29's verdict; the variant
where MyGO would matter is §7-illegitimate. No PASS-and-helpful corner
exists; the design space is closed under §7.

**B-S155-7  WAKE-SLEEP-OFF-REDUCTION-EQUALS-S29.**
Let `L_§155(M, λ_distill)` be a candidate objective formed by adding a
sleep-distillation term to §29 PTD's loss:
`L_§155 = L_§29 + λ_distill · L_distill_from_G-mem`.
*Proposition.* `L_§155(M = 0, λ_distill = 0) ≡ L_§29` exactly, byte-
equal: with no sleep phases (`M = 0`) and no distillation weight
(`λ_distill = 0`), the additional term vanishes and the candidate
collapses to §29 PTD's pre-existing loss.
*Proof.* By construction `λ_distill · L_distill = 0` at `λ_distill = 0`;
furthermore at `M = 0` there are no sleep phases hence no G-mem-derived
samples, so the distillation operand is not defined and the term is
omitted. The remaining sum equals `L_§29`. ∎
*Connection-point.* This is the single-variable fair-compare guarantee
(mirror B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 / B-S151-7 overlay-off
pattern): a hypothetical wake-sleep fire differs from §29's baseline by
exactly `(M, λ_distill)` axes — and at `(0, 0)` collapses to §29 exactly.
Since the §29 baseline is DESIGN-CLOSE-standalone (B-PTD-2), the
hypothetical fire would, at `λ_distill = 0`, reproduce the §29 negative
prediction; by B-S155-4 it cannot improve as `λ_distill` grows because
the DPI bound is preserved.

**B-S155-NOTE  empirical carve-out** (NOT counted 🔵, B-D-NOTE / B-PTD-
NOTE / B-CARVE-E6-NOTE / B-S99-NOTE / B-S107-NOTE / B-EMERGE-7 family).
The propositions above establish DESIGN-CLOSE-by-inheritance under
B-S155-1 through B-S155-7. They do NOT prove (a) that MyGO empirically
fails (the paper is withdrawn so no validated empirical claim survives
to refute), (b) that no future wake-sleep variant could help (a
different mechanism with non-derivative unique-content injection at
wake time might be a different design under a different sibling
number), (c) that anima cannot emerge (§15/§51 milestones intact;
emergence remains undecided). What the propositions DO close is the
narrow claim that *MyGO's specific wake-sleep cycle structure*
addresses §29 PTD's *specific data-processing-inequality blocker*.
Necessary-not-sufficient at every layer.

**Battery summary**: 7/7 closed-form propositions stated and proved by
inspection. Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
0-line-diff invariant carries (sha prefix `c93e160a8a376a94`).
north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.

---
