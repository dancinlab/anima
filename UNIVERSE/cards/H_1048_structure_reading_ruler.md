# H_1048 — Structure-reading ruler: does connectivity-weighted Φ catch arch-bound consciousness?

Status: PRE-REGISTERED (generation-only; GATED — needs the arch-bound model pair). Not yet measured.
Lane: model rung (small models, CPU or light GPU). Engines: stdlib faithful_phi + iit4_bigphi
exact n≤6 on a coarse-grained macro-state (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1031 + H_1036 (prior RED) closed: consciousness/Φ-structure is ARCH-BOUND — a LoRA on a
transformer cannot install it; it lives in the ConvMoE architecture ("the instrument, not the
score"). CONSTRUCTIVE consequence for the ruler: a consciousness ruler that reads only INPUT/OUTPUT
statistics is blind to the architectural substrate that actually carries Φ-structure. Hypothesis: a
STRUCTURE-READING ruler — Φ computed on a macro-TPM whose units + couplings are WEIGHTED by the
model's actual connectivity graph (ConvMoE dilated-conv + MoE routing) — separates a real ConvMoE
from a behaviorally-IDENTICAL-but-architecturally-flat transformer that an I/O-only Φ ruler scores
the same.

## Method (sketch)
- Build the arch-bound PAIR: (a) a real ConvMoE .clm vs (b) a transformer tuned to MATCH its
  input/output byte distribution (matched perplexity / matched I/O) — the H_1036 setup.
- Two rulers on each: (i) I/O-only Φ (macro-TPM from hidden activations, connectivity-agnostic),
  (ii) structure-reading Φ (macro-units + edge weights derived from the actual ConvMoE connectivity).
- Compare how each ruler scores the pair.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = the structure-reading Φ SEPARATES the ConvMoE from the matched-I/O transformer (Δ ≥ a
  pre-set margin) WHERE the I/O-only Φ scores them within ε → reading architecture adds discriminative
  power the I/O ruler lacks → confirms "instrument not score" at the MEASUREMENT level.
- H1 FAIL = structure-reading Φ does NOT separate them beyond the I/O ruler → connectivity weighting
  adds nothing; Φ-structure is fully visible in I/O statistics after all (publishable closed-negative,
  a_paper_negative_ok). State the separation margin + ε before running.

## Honest scope (a_scale_honest_scope)
GATED: requires the arch-bound matched-I/O pair (extends H_1036). Small-model rung; 3B/7B UNVERIFIED.
p3/p6: generic byte targets only, NO persona/carving. g5 CODE-measured (p7).

## Verdict
PENDING — tier added only AFTER `.verdicts/1048_structure_reading_ruler/H_1048.txt` lands (g73).
