@V := "tape" :: spec [active]
  version = "1.0"

@H 1173 := "MEMBRANE / self<->non-self boundary — does a maintained boundary (reject/flag non-self inputs) improve OOD robustness vs no boundary? (life-criterion MISSING #3: boundary)" :: universe [⏳ QUEUED-LIFE-EVOL — pre-registered, not yet run]
  seed         = "Audit gap: a cell has a membrane defining inside (self) vs outside (non-self); the anima Psi=1/2 basin is an IMPLICIT boundary, not a maintained one. H_1143/1151 found the substrate has NO learned in/out familiarity handle — a membrane would supply it."
  substrate    = "toy $0 CPU. REUSE h1159b cells; ADD a maintained inclusion radius per cell (self = within radius of any cell centroid); inputs outside ALL radii = NON-SELF -> flagged/rejected (not assigned)."
  method       = "FROZEN FALSIFIER (pre-reg): 🟢 BOUNDARY-HELPS iff the boundary substrate (a) lowers in-distribution error vs no-boundary (d>=0.8) AND (b) flags non-self/OOD inputs with AUROC>=0.70 (a real self/non-self discriminator the dense substrate lacked, cf H_1143). 🔴 if the boundary gives no robustness gain nor OOD-flagging above chance (a_paper_negative_ok)."
  verdict_tier = "⏳ QUEUED-LIFE-EVOL (toy $0; reuses h1159b; ties to the H_1143 input-familiarity null)"
  scope        = "toy; live engine + scale UNVERIFIED (a_scale_honest_scope). p7, AUROC not perplexity."
  xref         = "h1143-hidden-ood-metacog · h1151-dg-pattern-separation · h1159b_mitosis_capacity_self_tuning · a_core_engine_map"
