# G1 REAL-SUBSTRATE concept-feature probe — RESULT (2026-07-02, H_6167 → real-model bridge)

**TIER: 🟢 SUBSTRATE NOT THE BOTTLENECK (real 303M concept features are distinct/recoverable).** py mirror
= DIRECTIONAL (a_engine_native_learning; `core/decode.py` penultimate hook on py303_full.clm, d=3784 L=4 E=3).
aiden CPU $0.

## Question
H_6166/H_6167 (toy): recombination is achievable when the target has learnable structure; random targets
are unlearnable artifacts. Bridge to the REAL model: does the real 303M trunk's penultimate feature carry
the INGREDIENTS for recombination (distinct concept encoding), or is it feature-degenerate (substrate wall)?

## Result
- **[TEST1 · decisive] concept-identity held-out acc = 0.917** (chance 0.083; 12 concepts × 6 contexts,
  linear probe trained on 4 ctx, tested on 2 held-out ctx). The real trunk's penultimate feature DISTINCTLY
  encodes concept identity, recoverable from unseen contexts. (mean off-diag cosine 0.970 = strong anisotropy,
  but concepts are linearly separable in the residual — id-acc 0.917 proves it.) → substrate is NOT
  feature-degenerate.
- **[TEST2 · non-discriminating] structured recomb (ridge readout): REAL=RANDOM=SHUFFLE=0.583** (chance 0.167).
  The three arms are IDENTICAL because a LINEAR ridge readout cannot capture the nonlinear factored target
  y=T2[a%K,b%K] — it extracts the same limited signal from ANY distinct features. This is a readout-ceiling
  artifact, NOT feature-carried recombination evidence. Not re-run with a trained MLP because it is
  non-discriminating BY DESIGN: H_6167 already established distinct-features + structured-target + trained
  readout → recombination for ANY consistent distinct per-concept features (real or random alike); so TEST2
  cannot add information beyond TEST1.

## Reading (honest, scoped)
The real 303M substrate carries the necessary INGREDIENT for recombination — distinct, context-invariant
concept representations (TEST1, 0.917). Combined with the toy law (H_6167: distinct features + learnable
structure → held-out recombination), the substrate is NOT the recombination bottleneck. Therefore the
real-text G1=0 (H_1218/clm303) is most consistent with a DOWNSTREAM cause — the generation objective/metric
does not elicit recombination in the byte-output, even though the trunk represents the concepts distinctly —
rather than a substrate incapability. (Scope: DIRECTIONAL py-mirror; a full engine-native generation-side
re-test of what elicits recombination in output is the follow-on.)

## Provenance
real_struct_probe.py (imports core/decode.py, penultimate=yn pre-readout), run.log, result.json.
aiden CPU, py303_full.clm (303M, 176MB), $0.
