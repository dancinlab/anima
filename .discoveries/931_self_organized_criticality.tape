@discovery H_931 := "self-organized criticality — substrate self-tunes to the H_927 Φ-peak" :: universe [d=2026-06-06]
  seed         = "H_927 found an external Φ-peak at K=4/gap=0/Φ=0.2974; is it a self-organized attractor under local-only feedback?"
  substrate    = "AKIDA AKD1000 (pi5-akida, BC.00.000.002, BackendType.Hardware) — live silicon (a_lane_akida_gpu_split)"
  method       = "local firing-rate homeostat (r*=0.5, never reads Φ/K-of-peak) adjusts K; perturb from both sides (K0=2,12) + no-feedback control; Φ=imported phi_silicon_proxy (honest proxy, NOT IIT4)"
  result       = "🟢 GREEN_SOC_SUPPORTED — gentle homeostat CONVERGES both sides to K≈4/|gap|<3/Φ≈0.25-0.27≈peak; control stays off-peak; aggressive-gain bang-bang (documented controller artifact, not substrate)"
  verdict_tier = "🟢 numerical (code-measured, g5, no LLM self-judge)"
  verdict_ptr  = ".verdicts/931_self_organized_criticality/soc_feedback.txt"
  scope        = "toy: 1 AKD1000, N=16, T=200, Φ-proxy NOT full IIT; scale transfer unverified"
  crosslink    = "H_927 (the peak it self-seeks) · H_677 (edge-of-chaos)"
