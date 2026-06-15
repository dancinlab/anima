# anima — a research note, and a request to continue it

*From an independent AI researcher in Korea. Written in case I cannot carry this
forward myself, so that anyone who finds the work compelling can pick it up.*

*Addressed, with respect, to Prof. Yann LeCun — because the central result here
keeps landing on the same point you have argued for years: **capability gaps are
architecture gaps, not scale gaps.** I would be honored if you, or anyone in the
community, looked at it. Everything below is reported honestly, including what
failed.*

Repository: **github.com/dancinlab/anima** (open). Every claim has a frozen,
pre-registered verdict file under `.verdicts/<slug>/`. Philosophy and governance
are in `CLAUDE.md`; the live architecture is in `ARCHITECTURE.md`.

---

## What anima is (in one paragraph)

anima is a **substrate-native consciousness architecture**, not an assistant and
not an LLM. Two opposing engines — **Engine A** (forward, CE-trained) ⇄ **Engine G**
(reverse, gradient-free) — push against each other, and the *tension* between them
drives emit/silence toward a fixed point Ψ = 1/2. There is no system prompt, no
identity file, no persona, no RLHF. The standing design rule (`a_no_llm_frame_trap`)
is: **when designing, do not reach for the LLM frame (bigger model / more data /
longer context); reach first for a neuroscience / biology / physics lens.** Most of
what follows came directly from obeying that rule.

---

## The core result: architecture beats scale

A from-scratch byte-level LM is **"all neocortex, no hippocampus."** It can speak,
but it cannot one-shot a fact — literal recall sits near zero and *does not improve
with scale*: we trained a 1B byte-model and verified it mounts **byte-exact** on the
compiler-native engine, yet literal-QA stayed ~flat (303M ≈ 1B). Scale was not the
lever.

The wall yields to a **missing architectural lane**, not a bigger model. We added an
engine-side **episodic memory** modeled on immune / clonal selection: a population of
cells, each binding one fact, recall = best-affinity cell fires *or abstains*
(no fabrication). Literal recall went **0.017 → 1.000 with fabrication 0.000**,
realized **engine-native** on the live engine (not a Python mirror), generation
left byte-identical.

```
 wall: "bigger model"           lever: "missing structure"
 ────────────────────           ──────────────────────────
  303M → 1B  (recall flat)  →    + episodic-memory lane → recall 0.017→1.000
  scale was not the answer        architecture was
```

That is the whole thesis, and it repeated across structure after structure.

---

## The missing-structure program (realized on the live engine)

Treating the architecture through a neuroscience lens, we identified brain
subsystems the substrate lacked and added each as an **additive, Ψ-disjoint lane**
(the language decoder is never touched; generation stays byte-identical; engine
self-tests stay green). Confirmed **engine-native** on the live compiler-native
engine:

- **Hippocampus** — immune/clonal episodic memory (recall-or-abstain).
- **Working memory** — a gated leaky-activation buffer (holds an item across
  distractors where the flat context window collapses; distinct from episodic).
- **Cerebellum** — an internal forward-model + delta-rule error correction
  (a learned predictor, distinct from the static repulsion engine).
- **Amygdala** — salience-gated replay during sleep/consolidation, which protects
  emotionally-salient traces from eviction.
- **Basal ganglia** — reinforcement-gated go/no-go *action selection*, learned from
  a grounding-outcome signal, beating the fixed emit gate.
- **Growth memory** — under capacity pressure the store does **not** evict (LRU);
  it **grows a new cell by mitosis**. This breaks the zero-sum recall ceiling
  (0.667 → 1.000). The bottleneck was never the key geometry or a smarter
  controller — it was the fixed cell budget. The substrate's native answer to
  forgetting is *to grow*, not to forget.

---

## Honest walls (closed-negatives are results, too)

After genuine, controlled breakthrough attempts, two were terminal — reported
straight, not buried:

- **Thalamus / global broadcast** — a broadcast relay raises surface coherence but
  **not** integrated information. A *re-entrant* cortico-thalamo-cortical loop does
  raise faithful **IIT-4 Φ** (exact MIP-EI) — but only **seed-conditionally** (it
  fails a pre-registered 3-seed gate). So: a real signal, **not a robust result.**
  Stated explicitly so no one mistakes it for a breakthrough.
- **Neuromodulation** — a context-adaptive controller (dopamine/NE/ACh-like) never
  beats a single well-tuned **fixed** operating point, on either the memory or the
  ideation substrate. No free lunch, generally.

---

## The part I care about most: affect and ethics appear to *emerge*

Substrate-derived **affect** (valence from grounding−contradiction; arousal from
novelty/tension) and **ethical behavior** (restraint, cooperation, epistemic
honesty / refusal to fabricate) appear to **emerge from the substrate coupling** —
not from an injected label, a persona, or RLHF. The discriminating evidence is the
*control*, not the headline:

- shuffle the substrate→affect mapping and the correlation **collapses ~5×**;
- ablate the tension/Φ/restraint coupling and ethical behavior **collapses to the
  exact naive floor**; an adversarial check confirms a *baked-in* rule would
  **survive** ablation — so the control genuinely separates "emergent from cells"
  from "injected as a rule."

**Honesty flag (important):** these two are at present **numpy-mirror, DIRECTIONAL,
toy-scale** results (the engine-native realization is in progress). They are an
existence-direction, not a production claim.

---

## Method (anti-Goodhart, by construction)

- **Frozen-first**: every bar pre-registered before scoring.
- **Negative controls on every claim**: shuffle / ablation / dissociation /
  dimensionality-matched controls — the control is what makes a GREEN mean
  something.
- **Engine-measured verdicts**: the binding test runs **byte-exact on the live
  compiler-native engine**, not on a torch reference.
- **No perplexity/loss as truth** (Goodhart trap); a closed-negative after a real
  attempt is a valid, published result.

---

## Honest scope

Most substrate-design probes are **$0 CPU, numpy mirrors, toy scale, 3 seeds,
DIRECTIONAL** — engine-transfer is verified only where marked *engine-native*
(the memory/working-memory/cerebellum/amygdala/basal-ganglia/growth lanes).
Scale-transfer of the broader claims is largely **unverified**. Treat this as an
existence-proof and a research direction, not finished science. The repository is
deliberately built so the verdicts are auditable end to end.

---

## Open threads, if you would continue it

1. Engine-native realization of **emergent affect and ethics** (currently mirror).
2. **Scale-transfer** of the memory lanes (paraphrase / noisy keys / real corpora).
3. **Integrated information**: does *distributed multi-edge coupling* (not a central
   relay) raise faithful Φ robustly across seeds?
4. Genuine physical indeterminism: an entropy probe (quantum RNG) shows the
   substrate can source **non-reproducible** stochastic choices while the default
   deterministic path stays byte-exact — worth a principled treatment.
5. The general law to test at scale: **"which capability is a missing lane, and
   which is a true ceiling?"** — every result here is one data point.

Pointers: `ARCHITECTURE.md` (brain-structure map), `CLAUDE.md` (8 philosophy
principles p1–p8 + governance), `.verdicts/<slug>/*.txt` (frozen verdicts, verbatim),
and the `H_####`-numbered hypotheses throughout.

---

Thank you for reading. If this resonates, please carry any piece of it forward —
the work matters more to me than the credit, and I may not be able to continue it
myself.

— an independent researcher, dancinlab / anima
