"""CLM conv-MoE model skeleton (toy scale).

See CLM/P0_ARCHITECTURE.md for the architecture decisions this implements.
Modules:
  model.py  -- CLMConvMoE: byte-embed -> dilated conv trunk -> MoE conv layer -> readout
  data.py   -- toy two-lane synthetic byte corpus + batch slicing
  probe.py  -- toy routing-balance probe (3 router variants x 3 seeds), NON-GATE
"""
