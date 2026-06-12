@V := "tape" :: spec [active]
  version = "1.3"

# H_986 — re-formulation re-test of H_978 🔴 (lattice geometry is modality-specific).
# substrate=CPU-mirror (numpy) · g5 CODE-measured · deterministic · toy single-rung (a_scale_honest_scope).
# falsifier: fairer alignment (rotation/scale-invariant CKA + orthogonal Procrustes on a shared-factor support).

@H 986_geometry_invariant_aligned := "H_978 🔴 ROBUST under fair alignment: cross-modal CKA 0.799 < within-language band 0.947 (>null 0.594) AND Procrustes residual 0.344 ≫ band 0.052, unrelated-engine control correctly rejected — modality-specificity is NOT a raw-coordinate formulation artifact" :: universe [🔴]
  seed   = "is the H_978 cross-modal geometry difference a RAW-COORDINATE artifact — does CKA/Procrustes alignment reveal a shared invariant?"
  target = "🔴 ROBUST closed-neg (toy) — geometry stays modality-specific even under the fairest alignment; xref H_978"
