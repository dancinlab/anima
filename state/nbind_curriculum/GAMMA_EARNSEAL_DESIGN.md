**YES — one genuinely new, narrowly-scoped angle survives. But it is a $0 decision probe whose most likely outcome is an EARNED terminal seal, and I give it only ~8–15% net odds of cracking F2. It is worth running anyway, because right now the measure-side terminal would be *declared*, not *earned*: NBIND-FC characterized the deficit (per-stem detector, no abstract NEG) but never tested whether a stem-invariant NEG feature exists in the substrate at all.** Ledger checked: no LOSO/cross-stem activation-invariance probe has ever been fired (H_9235 probed superposed *atom identity*, not operator surface-invariance; H_9261 probed XOR readout in the synthetic frame).

## The unmeasured fork NBIND-FC leaves open

The F2 stems (못, 아니) were abundantly present in wild pretraining with negation-like distribution. The drill nonetheless built **new per-stem detectors** instead of hooking anything pre-existing. Two disjoint explanations, currently undecided:

1. **No stem-invariant NEG feature exists** in the 303M byte substrate → measure-side is truly terminal; only architecture helps.
2. **The invariant exists, but CE-on-grid has zero pressure to route the flip through it** — a per-stem detector is the cheapest CE solution when k=4. Only this branch is measure-side addressable.

This fork is decidable for $0 on existing ckpts. That is the frozen gate.

## Frozen gate (both probes $0 numpy on existing ckpts, `--dump-hidden` path per #3177)

**Probe A — LOSO-NEG on the BASE ckpt.** Wild-text (not drill-corpus) negated-vs-plain contexts × 4 stems; leave-one-stem-out linear probe on frozen activations, 4 folds. Byte-confound guard: 안(EC 95 88)/않(EC 95 8A) share 2/3 UTF-8 bytes, so **the informative folds are 못 and 아니 held out**. Per probe-defect-census: paired stats (no max-of-controls), MDE precomputed, label-shuffle + surface-matched non-NEG morpheme-class control (detector-fairness), 4-cell where applicable.
**PASS (frozen now):** held-out acc ≥0.80 on BOTH 못 and 아니 folds · shuffle ≤0.55 · Δ vs surface-matched control ≥0.20 · paired-t p<0.05 · 2 seeds.

**Probe B — flip-vector geometry on the NBIND ckpt.** δ_s = mean h(neg,s) − mean h(plain,s) per drilled stem at Probe-A's layer/position; measure (i) cross-stem cosine among δ_s, (ii) cosine(δ_s, Probe-A direction).

**Decision tree (every leaf is closed):**
- **A FAIL** → no invariant NEG feature in-substrate → γ measure-side **TERMINAL, earned**. The real lever is architectural: representation granularity — learned morpheme-level latent chunking above bytes, which gives the operator a stem-invariant slot (with k≈4 Korean stems, byte level has nothing to abstract over). Explicitly NOT recurrence/retention (H_9259 killed) and NOT a bolt-on algebraic binder (H_9043: recoverability ✓, capability ✗).
- **A PASS ∧ B aligned** (drill flips already ride the invariant direction, yet F2 = chance) → present-but-unconsumed — the same law as the read-side earned-terminal → **TERMINAL**; forcing consumption re-enters the closed read-side lane = tune-to-green.
- **A PASS ∧ B orthogonal** → live mechanistic target; GPU fire justified.

## The fire (only if gate opens): γ-ANCHOR

NBIND training + auxiliary term tying per-stem flip deltas δ_s to the **frozen** Probe-A direction (cosine/InfoNCE across stems in-batch). Distinct from STEP-0 trunk-bake in kind: STEP-0 baked a generic output-bind loss with no verified in-substrate target (bind-add=−0.147); γ-anchor is *conditional on a pre-verified existing feature* and ties the operator representation, not the output. The verdict measure (F2 D-acc vs controls) stays untouched — no Goodhart.
**Pre-registered bars:** F2 (undrilled stem, both 못/아니 rotations) ≥0.65, 2 seeds · shuffle ≤0.55 · F1 non-regression ≥0.90× · Δ vs same-compute no-anchor retrain control (Δ is the signal, per the FORM-tunable/BIND-earned metalaw). FAIL → seal.

## Honest prediction

P(A pass) ≈ 0.5 · P(B orthogonal | A) ≈ 0.5 · P(fire cracks F2 | gate open) ≈ 0.3 → **net ≈ 8%**. The modal outcome is **A PASS ∧ B aligned → earned terminal** via the present-but-unconsumed law that already closed read-side. If the tree terminates, the honest seal reads: *surface-invariant operator binding is not a training-measure problem in a byte-granularity substrate with a k≈4-stem operator inventory; the residual lever is architectural (morpheme-level latent above bytes) — a substrate-identity decision for the owner, not a lever re-fire.* One noted-not-recommended residual: cross-operator factorization drill (many operator families × few stems, weight-level — distinct from killed in-context MLC) is technically unledgered, but corpus-heavy with a weak pre-gate; do not reach for it unless the owner reopens after a sealed tree.

Per the fable=design-only directive, this is the design; the probe pair itself belongs to the default execution path.