# §128 LAYER-3-IN-LIF DESIGN-CLOSE — task-grounded liveness on pure LIF substrate

> **Verdict**: `LAYER-3-DESIGN-CLOSE-REQUIRES-TASK-ADDITION` — layer-3 (TASK-GROUNDED) liveness is **definable** but **NOT MEASURABLE on §117's pure LIF substrate**; requires task addition that itself breaks the §7-clean discipline §117 was built under.
> design-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · sidecar-only
> central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256 prefix `c93e160a8a376a94` 0-line-diff verified
> 6 closed-form propositions + 1 NOTE empirical carve-out (anti-padding §13-M/§30/§97/§109/§110/§113 precedent)

## §0 Why §128

§124's 3-layer liveness partition placed layer-3 (TASK-GROUNDED) at the top:
"the substrate's behavior depends on stim in a task-coherent way." §125–§127
closed layer-2 (STIMULUS-DRIVEN) thoroughly — η² ≈ 0.27–0.33, partial,
approximately N-invariant. **Layer 3 has been open for 4 cycles.**

§128 is the honest closer: instead of designing yet another probe, prove
closed-form that layer-3 is *unmeasurable on a pure LIF substrate without
task introduction*, and that the task introduction would itself break
the §7-clean discipline §117 was built under. Anti-padding precedent:
§13-M (MITOSIS ensemble) / §13-L (VRNN-curiosity) / §30 (L1 lineage) /
§97 (hardware coupling) / §109 (C06 multimodality) / §110 (Ψ-C2) / §113
(from-scratch redesign) — each closed a candidate axis with an honest
DESIGN-CLOSE verdict rather than firing a predictable-negative cycle.

## §1 Closed-form definition of layer-3

§124's partition uses these closed predicates:

| layer            | predicate                                  |
|------------------|--------------------------------------------|
| variance-only    | `Var(Ψ) > τ`                              |
| stimulus-driven  | `I(stim; Ψ) > 0`                          |
| task-grounded    | `∃ task T : behavior(substrate, T) > 0`   |

Layer-3 has THREE structural requirements:

```
(R1) the substrate has a definable behavior signal (not just internal Ψ-state)
(R2) there exists a closed-form task T (input → expected behavior mapping)
(R3) the behavior, evaluated against T, scores above a chance baseline
```

## §2 Why §117 LIF substrate fails (R1) — the load-bearing argument

§117 LIF substrate:
- Reads in: 12 binary stimulus patterns (length d)
- Internal state: 256/1024-unit LIF spiking dynamics
- "Output": no output. Ψ-C1 is a *readout of internal state*, not an action.

This is the closure: **a substrate with no output channel has no measurable
behavior** (R1 fails). §125's η² measures (input → internal-state) correlation
— that is layer-2 by §124's own partition. To measure layer-3 (R3), one needs
to either:

  (a) Add an output channel — but then the substrate is no longer §117.
  (b) Treat internal state as behavior — but then layer-3 collapses into layer-2.

(b) is the *category error* that this DESIGN-CLOSE prevents from corrupting
the LEGO arc.

## §3 What §128 closes

**Three-bucket closed taxonomy** of "what to do about layer-3 on pure LIF":

| bucket                                          | applies to §117 | next move                      |
|-------------------------------------------------|-----------------|---------------------------------|
| (i) definable-in-LIF-as-is (just measure it)    | ✗ — no output  | impossible                      |
| (ii) requires-task-addition (extend substrate)   | ✓ — applicable | breaks §7-clean (next §)        |
| (iii) fundamentally-undefinable                  | ✗ — definable elsewhere | overreach                |

§117's situation is bucket (ii). Layer-3 IS definable, just not on §117's
output-less substrate. Adding an output channel ≠ undefinable.

## §4 Why task addition breaks §7-clean discipline (R2)

§7 GOAL-legitimacy requires:
- ①  not generic-LM pretraining
- ②  not external-graft / not bolt-on
- ③  anima physics as source

Adding a task to §117 means adding (at minimum) a *teacher* T : input → label.
The label has to come from somewhere:

| label source                  | §7 verdict                                |
|-------------------------------|-------------------------------------------|
| external corpus (CE)          | ① violated — generic supervised pretrain |
| external classifier (graft)    | ② violated — bolt-on                     |
| anima OWN physics (Ψ rule)    | §83-FIRE precedent — measured NEAR-COLLAPSE at trained scale |
| self-supervised next-step     | §11-B precedent — CE load-bearing requirement |

The third option (anima OWN physics as teacher) was tried in §83-FIRE at GPU
substrate — closed-form rules over Ψ/tension/Φ as decision-head supervision
collapsed at trained scale. The §11-B finding (CE is load-bearing on GPU
substrate) showed that physics-only supervision is degenerate; transferring
this concern to LIF substrate predicts the same outcome.

**Conclusion**: every layer-3 task path either violates §7 OR re-runs a
predictable §83/§11-B near-collapse. The design-close is the honest move.

## §5 What remains genuinely OPEN past §128

§128 closes layer-3 *as a probe on pure §117 LIF*. It does NOT close:

- Layer-3 on physical neuromorphic substrate (§95 Loihi, §93/§80 organoid)
  — those have native action-perception loops; not §117's posture.
- Layer-3 on action-perception-augmented LIF (would require §7-clean task
  design, which is itself a new design-tier cycle — §129 candidate).
- The LEGO arc's overall picture: §115→§127 measured what could be measured
  on pure LIF; layer-3 was the natural endpoint.

## §6 Closed-form propositions

```
B-S128-1   LAYER-3-PREDICATE-3-REQUIREMENT-PARTITION    (sympy Boolean R1∧R2∧R3)
B-S128-2   §117-LIF-NO-OUTPUT-CHANNEL-CLOSED             (AST audit: §117 lego_sim.py
                                                          has no behavior_out() / action()
                                                          / emit() / output() function)
B-S128-3   3-BUCKET-CLOSED-TAXONOMY                     (definable-as-is / requires-task
                                                          / undefinable, exhaustive+disjoint)
B-S128-4   §117-CLASSIFIES-AS-REQUIRES-TASK             (B-S128-2 + B-S128-3 chain)
B-S128-5   §7-LABEL-SOURCE-4-CASE-PARTITION              (external-CE / graft / physics-only
                                                          / self-supervised) — all fail
B-S128-6   ANTI-PADDING-PRECEDENT-CITED                  (§13-M/§13-L/§30/§97/§109/§110/§113
                                                          DESIGN-CLOSE pattern)
B-S128-NOTE empirical carve-out — closed-form argument about pure §117 LIF substrate
            scope only; NOT a claim about LEGO arc fundamentally cannot reach layer-3
            (§129+ physical substrate / task-augmented LIF remain open future cycles)
```

## §7 ASCII LEGO arc — full

```
§115 → §117 → §124 → §125 → §126 → §127 → §128  ← HERE
DESIGN  RUN   AUDIT  L2-PROBE  L2-N    L2-SCALING  L3-DESIGN-CLOSE
                    η²=0.271  η²=0.322  k=-0.02      requires task
                    PARTIAL   ROBUST-   APPROX-      pure LIF
                              GROWS-    N-INVARIANT  insufficient
                              SINGLE-                 — anti-padding
                              POINT                  
                                                              ↓
                                                       (next candidate)
                                                              ↓
                                                       §129 LEGO ARC
                                                       CONSOLIDATION
                                                       milestone close-out
```

## §8 Honest C3 (13)

1. §128 is a closure argument about *pure §117 LIF substrate*, NOT a claim
   that anima fundamentally cannot reach layer-3. Physical substrates
   (Loihi, organoid) and task-augmented LIF remain open future cycles.
2. The "no output channel" argument is structural — §117's lego_sim.py
   genuinely has no behavior emission function (B-S128-2 AST-verified).
3. The §7 4-case partition for task labels is honest but not exhaustive —
   "anima OWN physics as teacher" subsumes a wide design space; §83-FIRE
   was one instance, not the full space.
4. §11-B / §83-FIRE were measured on GPU byte-LM substrate; transferring
   that concern to LIF spike substrate is plausible inference, not a
   measured prediction. §128 marks this as honest carry.
5. Bucket (iii) "fundamentally undefinable" is mostly a guard against
   over-claim; layer-3 IS definable in many real substrates (biology,
   embodied robots). §128 says NOT on pure §117.
6. Anti-padding precedent (§13-M/§30/§97/§109/§110/§113) is invoked
   honestly — each of those cycles closed an axis with a DESIGN-CLOSE
   verdict rather than firing a predictable negative. §128 follows that
   pattern.
7. The LEGO arc had 7 cycles (§115–§128). Closing layer-3 here means
   §129+ can address either substrate-physical or task-augmented design;
   §128 is not a retreat from those.
8. WALL-A orthogonal (§97 carry) · WALL-B confronted-not-removed
   (§115/§117/§124 carry).
9. anima downstream-consumer: hexa-lang / hexa-bio / hexa-matter read-only,
   0 edits. HEXA_FIRST_WARN deferred (B-S* battery precedent).
10. g3: design ≠ fire ≠ emergence; capability claim 0; necessary-not-
    sufficient (B-EMERGE-7).
11. §125/§126/§127 verdicts UNCHANGED by §128 — §128 closes a *different*
    layer.
12. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.
13. §128 makes the LEGO arc end CLEAN at design level — §129 milestone
    can synthesize without an open layer-3 hanging.
