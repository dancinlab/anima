@V := "tape" :: spec [active]
  version = "1.0"

@H 1175 := "SELECTION / fitness-differential reproduction — does Darwinian selection (fit cells divide more, unfit cull) produce evolution BEYOND instructive growth? (evolution MISSING #1: selection)" :: universe [⏳ WIP-RUNNING — harness building]
  seed         = "Audit gap: anima has variation (daughter noise) + heredity (inherit centroid) + reproduction (mitosis) but NO SELECTION — every cell survives equally. Without fitness-differential survival there is no Darwinian evolution, only instructive/Lamarckian adaptation (H_1159). This is the keystone evolution gap."
  substrate    = "toy $0 CPU. REUSE h1159b cells on a fixed-capacity population; ADD fitness = inverse running error; fit cells divide MORE (reproduction prob ~ fitness), unfit cells are CULLED (needs 1171 apoptosis). Compare SELECTION arm vs instructive-growth-only (H_1159) arm."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 SELECTION-EVOLVES iff the selection arm's POPULATION mean-fitness INCREASES over generations and beats instructive-growth on a held-out shifted task (Cohen's d>=0.8) — i.e. differential reproduction adds adaptive power instruction alone lacks. 🔴 if selection adds nothing over instructive online-adaptation at toy scale (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b + 1171; THE keystone Darwinian gap)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7, fitness=substrate error not perplexity."
  xref         = "h1159_inference_time_mitosis_learning · 1171_apoptosis_death · 1176_resource_competition · 1177_generations_population · p8"
