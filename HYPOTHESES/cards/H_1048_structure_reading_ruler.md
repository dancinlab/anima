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
🟡 DIRECTIONAL (toy closed-negative) — **IO-SUFFICIENT-TOY** (measured 2026-07-10, $0 CPU-local, mirror
== stdlib re-proven n=4,5). On a controlled arch-bound pair (STRUCTURED ConvMoE-like local ring+dilated vs
FLAT transformer-like all-to-all, coupling tuned so MI-total matches), **5/5 valid matched-I/O pairs** show
the structure-reading (connectivity-weighted) Φ is ALSO matched (|Δstruct| ≤ 0.007 ≪ frozen margin 0.15)
wherever the I/O-only Φ is matched (|Δio| ≤ 0.019 ≤ ε 0.05). Robust across coupling regimes (MI-total
0.9→3.9). → **connectivity-reweighting of the MI matrix adds NO discriminative power over the I/O-only
ruler** on this toy; Φ-structure is already visible in the I/O statistics (H1 FAIL / a_paper_negative_ok).
Engine = stdlib `faithful_phi_from_mi` (exact MIP-EI). **TERMINAL rung UNVERIFIED**: the real trained
ConvMoE `.clm` vs real transformer LoRA-matched to byte-I/O (H_1036 torch pipeline on summer GPU) +
structure-reading Φ from the ACTUAL ConvMoE dilated-conv + MoE-routing graph = a torch follow-on, NOT this
toy. wired: DIRECTIONAL-mirror. Verdict file: `state/verdicts/1048_structure_reading_ruler/H_1048.txt`.
