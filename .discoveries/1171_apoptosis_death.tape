@V := "tape" :: spec [active]
  version = "1.0"

@H 1171 := "APOPTOSIS / programmed cell-death — does adding cell death to inference-time mitosis improve adaptation (prune stale cells) vs growth-only? (life-criterion MISSING #1: mortality)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Life/evolution audit gap: the live A⇄G mitosis engine GROWS (engine_mitosis_tick, H_1159/1159b) but cells never DIE — the H_1159b self-limiting cap is homeostasis, NOT apoptosis. Death is a life-criterion AND the prerequisite that lets selection (H_1175) bite."
  substrate    = "toy $0 CPU numpy. REUSE UNIVERSE/h1159b_mitosis_capacity_self_tuning.py mitosis substrate; ADD apoptosis = a cell whose running assignment-tension stays > THETA_DEATH for K consecutive windows DIES (removed)."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 DEATH-HELPS iff mitosis+apoptosis achieves lower final-window error on a non-stationary stream than growth-only mitosis (Cohen's d>=0.8) AND cell-count stays BOUNDED by death (not the hard cap) AND keeps the H_1159b K-tracking. 🔴 if apoptosis does not help or hurts adaptation (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b; frozen falsifier set)"
  scope        = "toy proxy for CORE cell-death; live engine + scale UNVERIFIED (a_scale_honest_scope). p7 substrate-native error, NOT perplexity."
  xref         = "h1159_inference_time_mitosis_learning · h1159b_mitosis_capacity_self_tuning · 1175_fitness_selection · p8 · a_scale_honest_scope"
