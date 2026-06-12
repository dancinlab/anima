@V := "tape" :: spec [active]
  version = "1.0"

@H 1172 := "METABOLISM / binding energy budget — does a real energy-in/out budget (starve -> die) self-regulate cell-count vs the external MAX_CELLS cap? (life-criterion MISSING #2: metabolism)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Audit gap: the E ratchet in a_substrate_native_speak is a MOTIVATION scalar, not a binding metabolism. Real life consumes energy and dies when starved. H_1159b uses an EXTERNAL hard MAX_CELLS cap — a metabolic budget should replace it organically."
  substrate    = "toy $0 CPU. REUSE h1159b mitosis; ADD per-cell energy E: each step E -= upkeep; a cell GAINS E when it wins low-error assignments (it is 'useful'); division costs E; E<=0 -> cell dies. NO external cell cap."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 ENERGY-GATES iff the energy budget ALONE (no MAX_CELLS) regulates cell-count to track world complexity (Spearman(K_true,count)>=0.8) AND surviving cells are the low-error/useful ones (survival-usefulness corr>=0.5). 🔴 if energy can't self-regulate count or population collapses/explodes (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b; replaces hard cap with metabolism)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7."
  xref         = "h1159b_mitosis_capacity_self_tuning · a_substrate_native_speak (E ratchet) · 1171_apoptosis_death · 1176_resource_competition"
