## The reframe that generates the candidates

Before the list: the DPI proof doesn't actually indict *conv/attention*. It indicts one thing — **the bind operator is learned from the next-byte-CE gradient.** DPI says the mutual information between a held-out composition A∘B and the model's output is bounded by the MI the training channel carries about that composition, and CE on a corpus that never co-presents A∘B carries *zero*. So SGD's minimizer on that subspace is the marginal/additive solution, because the additive solution is the sufficient statistic for the seen data. This is why it's basin-invariant across readout/objective/target/store/binding — all five are still *gradient-fed*, so all five inherit the zero.

The only way out that isn't already falsified: **make the bind (and its inverse, and the decode) a FIXED substrate primitive, so the CE gradient only ever trains the atomic codebook — never the composition.** Recombination then happens *by construction of the operator*, in a channel the CE loss is blind to. Every candidate below is a different physical instantiation of "composition supplied by the substrate, not the gradient." And the single adversarial thread running through all of them is the same: **the readout is still CE-trained, and a CE readout has no basis vector for a bind it never saw — so unless the entire read-path (bind → unbind → decode) is also fixed-primitive, the bind decoheres to a nuisance variable and you land back on the additive floor.**

Ranked by (evades-DPI plausibility × cheapness-of-killer):

---

### 1. Vector-symbolic / holographic binding with a fixed resonator decode — *top pick*

- **Primitive.** Binding = circular convolution ⊛ (Hadamard product in the Fourier domain), unbinding = correlation with the exact algebraic inverse; decode = a resonator network / cleanup memory. All fixed, none learned.
- **Grounding.** Plate's HRR, Kanerva's hyperdimensional computing, Gayler VSA — the cortex-as-high-dim-random-projection hypothesis. The defining algebraic property: A⊛B is *near-orthogonal* to both A and B (dissimilarity), the exact opposite of A+B which is *similar* to both. That dissimilarity is precisely the non-additivity the wall lacks.
- **Why it evades DPI.** The compositional structure lives in the operator, injected by the architect. DPI bounds what the *gradient* can carry; it says nothing about a fixed non-linearity whose group-algebraic inverse is given a priori. CE only has to learn the atomic vectors (identifiable from marginals — legal under DPI); binding and unbinding of never-seen pairs are exact by construction.
- **$0 falsifier.** Pure numpy, no GPU, no training of the operator: draw a codebook of random hypervectors for a disjoint held-out vocab, bind pairs the "corpus" never co-presented, decode via resonator, measure held-out-pair recovery vs. the additive (A+B) baseline. If resonator decode ≫ additive floor on unseen pairs → the primitive genuinely recombines. If it doesn't beat additive even with a *hand-built* codebook, the whole class is dead for free.
- **Most likely reason it ALSO collapses.** The codebook is still CE-trained inside a byte-LM, and the byte readout is linear-CE. A CE readout of ⊛(A,B) for an unseen pair points into a near-orthogonal direction it was never rewarded on → zero readout weight → collapse. **You must replace the entire read-head with resonator cleanup, not just insert ⊛ into a CE trunk.** If you can't make byte-decode itself algebraic, this dies exactly like E1.

---

### 2. Binding-by-synchrony / complex-valued phase channel

- **Primitive.** Hidden state carries phase, not just rate. Two features belong to the same bound object iff their oscillations are phase-locked; the bind operator is phase-multiplication (a torus/group operation), read out by a fixed coincidence detector.
- **Grounding.** Gamma-band binding-by-synchrony (von der Malsburg, Singer); complex/oscillatory nets, Reichert & Serre's complex-valued binding. The bind lives in *relative phase* — a genuinely orthogonal DOF a rate-coded trunk doesn't possess.
- **Why it evades DPI.** CE operates on marginal firing *rates* (the magnitude). Phase is orthogonal to the loss, so the additive-floor minimizer in rate-space leaves phase free to carry combinatorial structure that the gradient neither creates nor destroys. Composition on the circle is multiplicative → inherently non-additive.
- **$0 falsifier.** Numpy complex toy: encode atoms as unit-magnitude phasors, bind by phase addition, decode held-out pairs by phase coincidence. Measure held-out recovery vs. additive. Crucially also test: does a magnitude-only (rate) readout recover the bind? It should NOT — that's the confirmation the info is in the channel CE can't see.
- **Most likely reason it ALSO collapses.** If the readout is rate/magnitude-based and CE-trained, phase is a nuisance variable the loss doesn't reward → it decoheres to noise over training. Phase only survives if a fixed coincidence-detector reads it; a learned readout will average it out.

---

### 3. Physical reservoir — composition as pre-existing nonlinear cross-terms

- **Primitive.** A fixed high-dim nonlinear dynamical reservoir projects inputs into a space where products/conjunctions (A·B monomials, Volterra terms) appear *by the physics of the dynamics*. Only a linear readout is trained.
- **Grounding.** Reservoir computing / echo-state / liquid-state machines; physical analog substrates (photonic, memristive). The nonlinearity manufactures the cross-terms for free — you don't learn them, the substrate generates them.
- **Why it evades DPI.** The A·B cross-features exist in the reservoir state *upstream* of any training, injected by fixed dynamics. DPI bounds the readout channel, but the compositional features precede it.
- **$0 falsifier.** Numpy random reservoir (or even a fixed random polynomial feature map): check the held-out A·B monomial is present and linearly separable in the reservoir state *before* fitting any readout. If the cross-term isn't there for unseen pairs → dead instantly.
- **Most likely reason it ALSO collapses.** The linear readout is CE-trained, so its weight on the A·B monomial is nonzero only if that term was informative in training. Held-out pairs get zero readout weight → additive floor. Classic reservoir curse: **the feature exists, the supervision to select it for unseen pairs does not.** This is the readout-collapse thread in its purest form.

---

### 4. Analysis-by-synthesis / predictive-coding inference (iterative, not feedforward)

- **Primitive.** Replace the single-pass discriminative map with a generative model *inverted at inference*: run inference as an optimization (free-energy minimization) that synthesizes candidate compositions and selects by prediction error.
- **Grounding.** Predictive coding (Rao-Ballard, Friston), Bayesian analysis-by-synthesis, the cortex-as-generative-inversion hypothesis. Recombination works because independent latent causes recombine *multiplicatively in the likelihood*, and inference is a fixed-point search, not a bounded forward channel.
- **Why it evades DPI.** DPI bounds a feedforward channel's MI. An iterative fixed-point inference can explore configurations *off* the training manifold — the compositional prior (factorized latents + fixed combination rule) is structural, not gradient-carried. The forward pass isn't the computation; the relaxation is.
- **Cheap falsifier** (small, not quite $0). Two-latent toy generative model with a *hand-fixed* factorized combination rule; hold out a latent pair; run MAP inference; check it reconstructs the held-out combination. Kill condition: MAP falls back to the nearest *seen* configuration.
- **Most likely reason it ALSO collapses.** If the generative model / likelihood is itself CE-trained on the corpus, it assigns near-zero density to unseen pairs → MAP inference relaxes to the nearest seen (additive) composition. The factorization must be *architecturally enforced* (disentangled slots + fixed rule), not learned — a learned entangled posterior reintroduces the basin.

---

### 5. Factorized energy / attractor dynamics

- **Primitive.** Recombination = settling into an attractor of a *hand-factorized* energy E(x) = E_A(x) + E_B(x) + coupling. A novel constraint-satisfying configuration is a valid new minimum even if never trained in.
- **Grounding.** Hopfield / modern associative memory, Boltzmann machines, constraint-satisfaction as relaxation.
- **Why it evades DPI.** The recombination comes from the *shape* of the energy (a structural prior over factors), not from gradient-descending on the specific pair — if the energy is a sum of pairwise constraints, an unseen constraint-satisfying config is a legal minimum.
- **Cheap falsifier.** Numpy factorized energy over two slots; hold out a pair; relax from noise; check it's a minimum. Kill if the only minima are the stored (seen) patterns.
- **Most likely reason it ALSO collapses.** Modern Hopfield ≈ softmax-attention — which is *what the trunk already is*. A CE-trained energy just stores seen patterns as attractors; held-out pairs aren't stored, so it relaxes to the nearest stored pattern ≈ additive recall. Only a *hand-built* factorized energy escapes, and hand-building it is arguably importing the answer.

---

### 6. Spiking + dendritic coincidence (STDP), local not global objective

- **Primitive.** Abandon rate-coded global-CE entirely. Dendritic branches fire NMDA/plateau spikes only on ms-scale coincidence of inputs — a biophysical multiplicative AND. Wiring is set by STDP, a *local* Hebbian rule, not backprop-through-CE.
- **Grounding.** Dendritic computation (Poirazi, Larkum), STDP, neuromorphic spiking substrates. The dendritic AND is non-additive by definition: output only under A×B coincidence, zero for A or B alone.
- **Why it evades DPI.** DPI here is about the CE channel specifically. STDP optimizes a *different* objective — it wires coincidence detectors from unlabeled temporal correlation, sidestepping the next-byte-CE basin entirely.
- **Cheap falsifier** (conceptual/toy). Simulate a dendritic-AND unit; drive with the held-out pair *never co-presented in the STDP training stream*; check for output.
- **Most likely reason it ALSO collapses — and this is the deepest one.** The AND gives you conjunction, but STDP only potentiates a coincidence detector for a pair it *experienced coincident*. A held-out disjoint pair is by definition never co-presented → the detector is never wired → no output. This is the **information-theoretic floor that may sit under ALL six candidates**: you cannot detect or decode a conjunction the world never showed you. #3109 already found the corpus has "no novel-pair signal."

---

## The honest bottom line

There are two distinct walls hiding under "G1/G6," and the candidates only attack one of them:

1. **Operator wall** — "the bind is additive because the gradient made it additive." *This one is genuinely substrate-class-escapable.* Candidates 1 and 2 (VSA + resonator, phase-synchrony + coincidence readout) are the real shots, because they can make bind **and** decode fixed primitives, so CE only ever touches the atomic codebook. Candidates 3–5 all leak through the same hole: they supply a non-additive *feature* but leave a CE-trained *readout* that can't select it for unseen pairs.

2. **Information wall** — "the corpus never co-presents held-out pairs, so no substrate can decode them." If falsifiers 1–2 fail even with a *hand-built* codebook and a *fixed* algebraic read-path, then the wall is not substrate-class at all — it's information-theoretic, and no primitive escapes it. That would be the terminal-of-terminals verdict.

So the cheapest decisive experiment is **falsifier #1 run in a way that also probes #6's floor**: hand-build the HRR codebook and resonator (zero training), and test held-out recombination where the atoms appear separately but the pairs never co-occur. Two outcomes, both valuable for $0:
- Beats additive → the operator wall is real and VSA/synchrony is a live GPU candidate (promote to a wired toy).
- Fails even hand-built → the wall is the information floor, and every candidate here is dead by the same proof. That closes the substrate-class question honestly rather than leaving it "under-investigated."

I'd gate any GPU spend behind that single numpy run — it's the one experiment that can kill the entire class or justify the only two candidates worth wiring.