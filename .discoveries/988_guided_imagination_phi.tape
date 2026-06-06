@V := "tape" :: spec [active]
  version = "1.3"

# H_988 — re-formulation re-test of H_971 🔴 (imagination does NOT raise Φ).
# substrate=CPU-mirror (numpy) · g5 CODE-measured · deterministic · Φ is a PROXY (NOT IIT4) · toy single-rung.
# falsifier: GOAL-DIRECTED (guided) rollout vs autonomous drift + an alternative Φ-proxy axis-weighting.

@H 988_guided_imagination_phi := "H_971 🔴 ROBUST + SHARPENED: goal-directed imagination is even LOWER-Φ than autonomous drift (Φ_GUIDED 0.039 < Φ_DRIFT 0.068 < Φ_REACT 0.095; GUIDED−REACT d -6.84 p 1.3e-29) — goal pull contracts the trajectory, collapsing differentiation; sign did NOT survive the alt Φ-proxy" :: universe [🔴]
  seed   = "is the imagination-does-not-raise-Φ null specific to AUTONOMOUS drift — does goal-directed imagination raise Φ under an alt-proxy?"
  target = "🔴 ROBUST closed-neg (toy) — internally-generated states stay lower-Φ than external drive; xref H_971"
