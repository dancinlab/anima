@H 997_cross_modal_dynamics_transfer := "Does latent DYNAMICS transfer across modalities even though GEOMETRY doesn't (reconcile H_960🟢 + H_978🔴)?" :: universe [🟢]
  seed     = "H_960🟢 modality-agnostic encode vs H_978🔴 geometry modality-specific — is DYNAMICS the invariant?"
  target   = "🟢 PASS — frozen-A transition forecasts modality B (err 0.16) ≪ shuffled 66.4 (p=8.1e-06); cross-modal CKA 0.79 ≪ same-modal 1.00"
  probe    = "CWM/probes2/h997_dynamics_transfer.py · shared oscillator, A=raw B=rotated+nonlinear, 24 seeds"
  verdict  = ".verdicts/997_cross_modal_dynamics_transfer/h997_dynamics_transfer.txt"
  scope    = "TOY single rung (a_scale_honest_scope), ladder OPEN"
