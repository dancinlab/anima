@V := "tape" :: spec [active]
  version = "1.0"

@H 1176 := "RESOURCE COMPETITION — does a scarce shared resource create the selection pressure pure mitosis lacks? (evolution MISSING #2: competition)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Audit gap: grep found 'competition' = 0 in the CORE engine. Selection (H_1175) only BITES when cells compete for a scarce resource (carrying capacity). Without scarcity, fitness-differential reproduction has no teeth."
  substrate    = "toy $0 CPU. REUSE h1159b cells; ADD a scarce shared resource pool R with carrying capacity K_cap; cells draw R proportional to assignment share; when total demand > R, the lowest-fitness cells starve/die (competition). Compare COMPETITION vs unconstrained growth."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 COMPETITION-DRIVES-SELECTION iff scarcity yields a population whose composition TRACKS fitness (high-fitness cells dominate, corr(fitness,survival)>=0.5) AND total population is bounded by K_cap, vs no-competition unbounded equal-survival growth. 🔴 if competition does not produce fitness-tracking selection (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b; makes selection bite)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7."
  xref         = "1175_fitness_selection · 1171_apoptosis_death · 1172_metabolism_energy_budget · h1159b_mitosis_capacity_self_tuning"
