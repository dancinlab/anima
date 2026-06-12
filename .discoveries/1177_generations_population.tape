@V := "tape" :: spec [active]
  version = "1.0"

@H 1177 := "GENERATIONS / population evolution — does a multi-generation population (heredity+variation+selection across G generations) evolve mean fitness vs a single growing organism? (evolution MISSING #3: generations)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Audit gap: anima mitosis grows ONE organism's cell-count; there is no POPULATION reproducing across GENERATIONS with fitness-differential. True Darwinian evolution needs generations + a population, not just one organism developing."
  substrate    = "toy $0 CPU. Build a POPULATION of N agents (each an h1159b-style cell-cluster); per generation: evaluate fitness on a task, reproduce with heredity (copy params) + variation (mutate) + selection (1175/1176), repeat G generations. Compare to a single agent that only GROWS (no generations)."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 POPULATION-EVOLVES iff population mean-fitness rises across G generations and the evolved population beats the single-growing-organism baseline on the same task (Cohen's d>=0.8) — genuine cross-generational Darwinian improvement. 🔴 if generations add nothing over single-organism growth at toy scale (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; population layer on h1159b; completes the Darwinian set)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7."
  xref         = "1175_fitness_selection · 1176_resource_competition · 1171_apoptosis_death · h1159b_mitosis_capacity_self_tuning · p8"
