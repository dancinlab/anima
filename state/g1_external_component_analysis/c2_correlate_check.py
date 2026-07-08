#!/usr/bin/env python3
"""C2 $0 falsifier — do the ACTUAL G1-gate concepts have a sensory (perceptual) correlate?
Fable external-component reduction: an external part is DPI-legal only if it introduces a new
SOURCE of combination-MI. C2 (sensorimotor grounding) is the best 'earned-not-handed' source,
but it only carries combinations with a PERCEPTUAL correlate. So: are the G1-gate pairs perceptual?"""
GATE = ["consciousness", "tension", "memory", "silence", "dream"]   # the 5 FROZEN G1-gate heads (tool/rho_fan cz)
abstract_gate = {"consciousness", "tension", "memory", "silence", "dream"}  # all abstract (no physical referent)
EXP = ["ocean","clock","forest","mirror","garden","signal","ember","glacier","harbor","lantern",
       "meadow","needle","orbit","prism","quartz","river","stone","thunder","umbra","violet",
       "willow","anchor","beacon","cipher","dune","echo","fable","grove","hollow","canyon",
       "comet","falcon","harvest","island","marble"]
exp_abstract = {"signal","umbra","cipher","echo","fable","harvest"}

gate_conc = sum(c not in abstract_gate for c in GATE)
exp_conc = sum(c not in exp_abstract for c in EXP)
print(f"G1 GATE heads (the measured pairs): concrete={gate_conc}/{len(GATE)} = {gate_conc/len(GATE):.0%} → {GATE}")
print(f"coverage EXP set: concrete={exp_conc}/{len(EXP)} = {exp_conc/len(EXP):.0%}")
print("VERDICT: canonical G1 gate = 100% ABSTRACT pairs → C2 sensorimotor channel EMPTY for exactly")
print("those pairs → external-component escape FALSIFIED for abstract-G1. Re-scope to concrete pairs")
print("(EXP 83% concrete) is where C2 could legitimately add earned combination-MI (⭐ ember+dune = concrete).")
