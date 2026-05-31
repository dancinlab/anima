879_clm_per_layer_edge — id-keyed backing dir for H_879 (per-layer incremental edge-learn · 부분부분학습)
=========================================================================================================
Hypothesis : UNIVERSE/H_879_clm_per_layer_edge.md
Verdict    : .verdicts/clm-per-layer-edge/F-CLM-PER-LAYER.txt (+ _prereg.txt + clm_per_layer_edge_result.json)
Driver     : CLM/model/h879_per_layer_edge.hexa (executable python harness; project hexa-native policy)
Backbone   : clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) — mid d512/L8/E8
Method     : W2 · adapt EXACTLY ONE trunk layer at a time (the rest frozen) on the H_865 adapter edge;
             per-layer (gain, z_drop) vs bf98c01-frozen thresholds (z_drop<1.0 ∧ gain>0).
Builds on  : H_861 (readout-only edge too shallow 🔴) · H_865 (trunk-adjacent adapter fixes BOUND 🟢)
             · H_872 (contiguous top-k freeze-depth sweep). H_879 is the orthogonal single-layer axis.
SW-sim of non-deterministic on-chip edge-learn accepted at the measurement rung (a_scale_honest_scope);
foundation H_679 established HW edge-learn is real.
