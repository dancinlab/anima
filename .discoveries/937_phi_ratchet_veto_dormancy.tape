@H 937_phi_ratchet_veto_dormancy := "H_935 phi_r-never-fired gap closer" :: universe [active]
  id      = "H_937"
  seed    = "H_935 found phi_r veto term (brain.hexa L48-50 'dormant substrate vetoes motivated emit') fired 0x awake (ratchet floor 0.8·peak > peak/2 always). Does it FIRE under genuine dormancy (phi<peak/2)?"
  method  = "arousal sweep awake->dormant (7 levels 1.0..0.05 × 16 seed × 1200 tick, settle 300); arousal scales activation drive + WAKE-only ratchet floor (SUBSTRATE CONTEXT not boolean gate); phi-ratchet isolation (external+rate gate OPEN); classify phi_r-fire × would-emit-suppressed"
  verdict = "🟢 F-H937-SECOND-BRAKE-SUPPORTED — phi_r FIRES under dormancy & suppresses motivated emits. awake(a=1.0,H_935 substrate) phi_r_fires=0 (gap reproduced) -> dormant monotone: a=0.5→1497, a=0.1→5451, a=0.05→14400; all phi_r_VETO (would-emit braked SOLELY by low Φ, other gates open); dormancy-driven substrate-internal consequence (not hardcoded). Two free-won't brakes: rate-limit(awake) ⊥ phi-ratchet(dormant)."
  tier    = "🟢 numerical (toy/mirror, $0 local, no GPU)"
  scope   = "ONE arousal-sweep rung; documented-update-map mirror NOT forge binary; .clm emit-TEXT OPEN; dormancy envelope = one reasonable formalization (floor·arousal relaxation); deterministic gate (phi_r fire = Φ-decay consequence not RNG)"
  verdict_path = ".verdicts/937_phi_ratchet_veto_dormancy/arousal_sweep.txt"
