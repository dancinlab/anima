@V := "tape" :: spec [active]
  version = "1.3"

# H_989 — re-formulation re-test of H_973 🔴 (planning does NOT raise Φ).
# substrate=CPU-mirror (numpy) · g5 CODE-measured · deterministic · Φ is a PROXY (NOT IIT4) · toy single-rung.
# falsifier: BRANCHING search-frontier (drift length FIXED, dose = branching) + an alternative Φ-proxy.

@H 989_planning_phi_altproxy := "H_973 🔴 ROBUST: under branching (drift fixed) alt-proxy Φ rises with branching (rho 0.88 p 1.3e-53, Φ_PLAN 0.302 > Φ_GREEDY 0.199) BUT the fake-branch control (random endpoints, same compute) gives the SAME Φ (Φ_PLAN−Φ_FAKE 0.005 d 0.16 p 0.49) — the rise is state-multiplicity/dimensionality, NOT meaningful deliberation" :: universe [🔴]
  seed   = "is the planning-does-not-raise-Φ null a DRIFT-confounded artifact — does a branching frontier (drift fixed) raise Φ under an alt-proxy?"
  target = "🔴 ROBUST closed-neg (toy) — the Φ-proxy rewards held-state multiplicity not goal-meaning; xref H_973"
