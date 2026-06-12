@V := "tape" :: spec [active]
  version = "1.0"

@H 1174 := "SELF-REPAIR — does damage->repair maintain function under sustained perturbation better than homeostasis alone? (life-criterion MISSING #4: self-repair)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Audit gap: homeostasis (SOC/Psi=1/2, H_931/1126) keeps the REGIME stable but does not REPAIR damaged components. Life repairs damage (DNA repair, wound healing). Distinct from homeostasis."
  substrate    = "toy $0 CPU. REUSE h1159b cells; INJECT damage = perturb a fraction f of cell centroids each step; REPAIR rule = nudge damaged cells back toward their recent assignment manifold. Compare REPAIR vs HOMEOSTASIS-ONLY (no repair) under the same damage."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 REPAIR-HELPS iff under sustained damage the repair arm holds lower error than homeostasis-only (Cohen's d>=0.8) AND recovers toward pre-damage error after a damage burst. 🔴 if repair ~= homeostasis (the regime self-heals already; repair is redundant) (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b; separates repair from homeostasis)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7."
  xref         = "h931_self_organized_criticality · 1126_psi_stability · h1159b_mitosis_capacity_self_tuning"
