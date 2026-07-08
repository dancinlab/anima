**Verdict: (b) falsification.** No task can satisfy all three conditions simultaneously — the requirements form a closed squeeze — and stage-1's B≫C was a superposition-capacity result, not a transfer result. The framebreak is not a G1 lever. Argument, then a cheap kill-shot control if you want this engine-cemented rather than essay-cemented.

## The squeeze (why conditions 1–3 are jointly unsatisfiable)

**Well-posedness first.** For held-out accuracy to measure anything, g on the 30 held-out combos must be *uniquely determined* by the 150 training combos. An arbitrary lookup table isn't — held-out failure would be information-theoretic, everyone (resonator included) sits at chance, and the "wall" is vacuous. So g must have committed compositional structure. That forces g into one of two branches, and both kill the framebreak:

**Branch 1: g ∈ the VSA-expressible class** (bilinear bind, role-indexed permutation, group operation — anything a fixed bind/unbind/permute/cleanup pipeline can compute).
- The resonator win is circular *by necessity, not by accident*: a fixed operator computes exactly its own algebra and nothing else. Any g it generalizes was, by selection, in that algebra. The only non-circular escape would be independent evidence that anima's actual G1 target function is in this class — and your own ledger is counter-evidence: H_1816 (PC binding NOT-SUP) and H_9131 ② (bind objective can't beat strong additive baseline) both say imposing binding structure on the trunk doesn't help. A toy with g ∈ VSA imports an unproven premise, so its GREEN wouldn't transfer regardless.
- Worse, the wall itself likely evaporates in this branch: bilinear maps, modular arithmetic, and group compositions with dense marginal coverage are the *canonical grokking successes* — CE transformers do reach held-out generalization on them at convergence. Keeping the LM red would require undertraining, undersizing, or starving coverage — tune-to-red, the mirror image of tune-to-green, and disqualified anyway because the real wall is established scale- and convergence-invariant.

**Branch 2: g is a genuine, literature-established transfer wall** (SCAN/COGS-style systematic splits — real, reproducible transformer failures). Here a VSA system *does* beat the transformer — but only when handed the ground-truth role/filler factorization and atom codebook (Smolensky-style: the compositional parse is injected as prior knowledge). That's the rig in its purest form, because **the G1 wall is precisely the absence of a learned factorization**. Handing the resonator the factorization solves the hard part offline. In anima, nothing hands the trunk the role/filler parse of natural bytes.

**Why stage-1 masked this.** In superposition-partner-recall, the pairs format gives the factorization for free; the difficulty is interference in a superposed trace — HRR's designed-for home turf. That is a *memory-capacity* property. Held-out transfer's difficulty is *inducing the factorization from data* — a thing HRR does not do at all (it presupposes atoms and roles). So the operator escape can't even in principle be a transfer lever; it was only ever a capacity/interference lever. This is the same trap shape as H_1835: in-context/superposition competence mistaken for transfer competence.

## Point 4 (atom geometry) independently confirms the kill

- B in-dist = 0.06 and B0 > B means CE training *actively destroys* the quasi-orthogonality HRR needs (anisotropic cone collapse toward task-correlated directions). This isn't a wiring bug to fix; it's the gradient's inductive bias working against the algebra.
- Fixed random projection cannot fix it: JL-type maps approximately preserve inner products, so anisotropy passes straight through. Garbage geometry in, garbage geometry out.
- A dedicated atom space with a frozen random codebook + a *trained* encoder into it is viable — but that is a trained binding front-end, i.e. it collapses into γ (H_1840, trained constructive bind), not a fixed-algebra framebreak. Whitening is banned as fit-on-data.
- Honest conclusion: LM hiddens can't host HRR, and every repair path converges onto the one lever your ledger already holds open (γ).

## Kill-shot control, if you want it measured (cheap, CPU-pool, frozen bars)

The handed-factorization control quantifies the circularity directly:

- **Task**: one Branch-2 wall instance (SCAN-style split, or conjunctive bilinear g with the structure class committed in the card), 150 train / 30 held-out, r≡f mod6 kept, answer never in context.
- **Arms**: A = CE byte-LM to convergence, plus a 4×-steps grokking guard (if 4× breaks the wall, the instance is disqualified as not-a-wall). B_handed = fixed HRR with ground-truth atoms + roles. B_blind = fixed HRR with atoms derived without ground truth (LM hiddens or frozen random projection; no whitening). C = trained readout.
- **Frozen predictions, registered before firing**: A ≈ chance; B_handed high iff g ∈ VSA-class; **B_blind ≈ chance**. The framebreak survives only if B_blind clears the wall bar. The B_handed − B_blind margin *is* the measured circularity.

I predict the kill. Either way the verdict is decision-grade: B_blind at chance cements "operator escape = structure-specific to stage-1 superposition recall; framebreak 🧱 FALSIFIED as a G1 lever," and the residual live levers remain exactly what the ledger says — γ trained-constructive-bind (H_1840, cost-gated) and coverage-density. Per your execution-default policy this spec is handoff-ready; I haven't run anything.