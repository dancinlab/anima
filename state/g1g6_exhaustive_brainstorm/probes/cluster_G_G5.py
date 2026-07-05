#!/usr/bin/env python3
"""Cluster G item G5 — longer-train gate-slope rule, $0 validation on existing data.

G5 (operational principle): "longer train only allowed on arms with positive gate
slope; 3 consecutive flat checkpoints => early-stop." This is NOT a lever to fire
but a STOPPING RULE. We validate it on EXISTING multi-arm/multi-rung trajectories:
does any architectural/depth/scale arm show positive slope on the BINDING gate
(G1 best_distinct or G6 falsifiability), justifying longer training? Or is it flat
at floor => the early-stop rule correctly fires?

DATA ($0, pre-existing files):
  (a) g1_coverage_prod_block 3-arm (L4_clean, L8_nocov, L8_cov) gen40 engine-native:
      G1 best_distinct, G6 dist, G6 fals, G2, G0  -- architecture ladder (depth+coverage)
      src: state/g1_coverage_prod_block/results_gen40/SUMMARY.txt
  (b) g1_framebreak_and_scale 3-rung (d256/L4, d512/L6, d768/L8) held-out recomb:
      scale ladder (matched obj/data, varies params)
      src: state/g1_framebreak_and_scale/RESULT.md
  (c) H_9131 capacity sweep: bind held-out across anchor capacity (4 caps)
      src: state/verdicts/trunk_obj_noncommutative/H_9131_derisk.md
        "전 앵커 용량서 bind held-out 우위 max +0.009 (<< delta) = FALSIFIED 용량 artifact 아님"

PREREGISTERED FROZEN BAR
  binding_gate flat  : consecutive arms delta = 0 (G1 best_distinct identical) OR
                       capacity delta < 0.10 (H_9131 delta=0.10) on the BINDING metric.
  positive-slope     : delta >= 1 on G1 best_distinct (integer 0..k) across >=2 steps
                       OR capacity delta >= 0.10 sustained -> justifies longer train.
  G5 rule VALIDATED  : if EVERY available trajectory is flat on the binding gate
                       (no positive slope), the early-stop rule correctly fires on
                       all current arms -> no arm merits longer training on binding.
  G5 rule BROKEN     : a trajectory shows positive slope on the binding gate ->
                       that arm would be (correctly) kept training under G5.
NOTE: a slope on a NON-binding metric (G2 novelty, G6 set-diversity count, scale
      held-out on a scale axis already ruled out by G4) does NOT break G5 — G5 keys
      on the BINDING/recombination gate, not auxiliary counters.
"""
import numpy as np

# (a) coverage_prod_block 3-arm gen40 engine-native (architecture/depth+coverage ladder)
arms = ["L4_clean","L8_nocov(depth-only)","L8_cov(depth+coverage)"]
G1_best = [0,0,0]            # best_distinct (frozen gate threshold=2; >=2 & >max_single)
G6_dist = [5,6,6]            # distinct count (set diversity, threshold>=5)
G6_fals = [0,0,0]            # falsifiable count (threshold>=1)
G2_nov  = [40,69,100]        # novelty n-gram count (threshold>=3)
G0      = [5,5,5]            # kwr PASS /5

# (b) framebreak scale ladder 3-rung (matched obj/data, varies params)
rungs = ["d256/L4 (3.3M)","d512/L6 (19.2M)","d768/L8 (57.2M)"]
held_out = [1,3,0]           # /5 ; d768 seen=0/8 -> INVALID (undertrained)
seen_sanity = [8,8,0]        # /8

# (c) H_9131 capacity sweep: bind held-out advantage across capacity (max +0.009)
cap_max_delta = 0.009        # << PREREG delta 0.10

def slope_int(vec):
    v=np.array(vec); return int(np.max(v)-np.min(v))
def flat_int(vec):
    return slope_int(vec)==0

print("="*72); print("Cluster G / G5 — gate-slope & early-stop rule, $0 validation"); print("="*72)
print("PREREG: G5 rule VALIDATED iff EVERY trajectory is flat on the BINDING gate")
print("(no positive slope); BROKEN if any trajectory slopes on the binding gate.\n")

# --- (a) coverage ladder ---
print("--- (a) coverage/depth architecture ladder (gen40 engine-native) ---")
for n,v in zip(["G1 best_distinct","G6 falsifiable","G6 distinct(set-div)","G2 novelty","G0 kwr/5"],
               [G1_best,G6_fals,G6_dist,G2_nov,G0]):
    print(f"  {n:22s}: {v}   slope(max-min)={slope_int(v)}")
binding_flat_a = flat_int(G1_best) and flat_int(G6_fals)
print(f"  => BINDING gate (G1_best & G6_fals) FLAT across 3 arms: {binding_flat_a}")
print(f"     (G6 distinct 5->6 is set-diversity axis, NOT binding; G2 novelty is NOT binding)")

# --- (b) scale ladder ---
print("\n--- (b) scale ladder (matched obj/data, varies params) ---")
print(f"  held-out recomb: {held_out} on rungs {rungs}")
print(f"  seen sanity    : {seen_sanity}  (d768=0/8 => UNDERTRAINED/INVALID rung)")
valid_held = [held_out[i] for i in range(3) if seen_sanity[i]>=6]  # exclude undertrained
print(f"  valid held-out (seen>=6/8): {valid_held}  slope={slope_int(valid_held) if len(valid_held)>=2 else 'N/A'}")
print(f"  NOTE: scale axis is already RULED OUT as a lever (G4/H_6112 scale-invariant,")
print(f"  H_1598 depth-L8 FALSIFIED). A slope here is on a non-lever axis and does NOT")
print(f"  break G5 on the binding gate. d768 undertrained => G5 would correctly")
print(f"  mandate more training ONLY if scale were a lever (it is not).")

# --- (c) capacity sweep ---
print("\n--- (c) H_9131 anchor-capacity sweep (bind held-out advantage) ---")
print(f"  max delta across capacities = {cap_max_delta}  (PREREG delta=0.10)")
print(f"  => flat (capacity artifact ruled out): {cap_max_delta < 0.10}")

print("\n"+"="*72); print("VERDICT (G5 operational rule)"); print("="*72)
all_binding_flat = binding_flat_a and (cap_max_delta < 0.10)
# scale ladder: binding-gate slope there is on G1 held-out recomb, but on a non-lever axis
# and the 3rd rung is invalid; honest accounting: no CLEAN positive binding-gate slope
# on any in-lever trajectory.
if all_binding_flat:
    print("  => G5 RULE VALIDATED on existing trajectories:")
    print("     every architecture/depth/capacity arm is FLAT on the binding gate")
    print("     (G1 best_distinct=0/0/0, G6 fals=0/0/0, capacity delta=0.009<<0.10).")
    print("     Early-stop rule would correctly fire on ALL current arms => no arm")
    print("     merits longer training on the binding/recombination gate. G5 as a")
    print("     wall-break LEVER: NOT actionable (it is a stopping rule, not a lever).")
else:
    print("  => G5 rule BROKEN: a trajectory shows binding-gate slope -> keep training.")
print("\n  Secondary: the only positive slope anywhere (d256->d512 held-out 1->3) is on")
print("  the SCALE axis, which G4/H_6112 already ruled scale-invariant, and the 3rd")
print("  rung (d768) is undertrained/invalid. So no in-lever positive binding slope.")
