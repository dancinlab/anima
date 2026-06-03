882_clm_region_gated — id-keyed backing dir for H_882 (region-gated plasticity · 영역별 학습 게이트)
==================================================================================================
Hypothesis : UNIVERSE/H_882_clm_region_gated.md
Verdict    : .verdicts/clm-region-gated/F-CLM-REGION-GATED.txt (+ _prereg.txt + clm_region_gated_result.json)
Driver     : CLM/model/h882_region_gated.hexa (executable harness; project hexa-native policy)
Runtime    : h882_region_gated_runtime.py.txt (reproducibility copy of the executed harness)
Backbone   : clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) — mid d512/L8/E8, FROZEN core
Method     : W2 · two arms identical except the OUTPUT-LOGIT region gate (E5 variable-ablation). UNGATED =
             H_865 adapter affects all 256 logits; GATED masks the adapter logit contribution to R_new
             (≥99% new-context TRAIN target mass), R_base = FROZEN-readout pass-through. Two frozen gates:
             RETAIN z_drop_gated<z_drop_ungated ∧ GAIN gain_gated>=gain_ungated.
Builds on  : H_679 (PLASTICITY HW edge-learn, foundation) · H_861 (readout-only forgets 🔴) · H_865
             (additive adapter fixes BOUND 🟢) · H_872 (freeze-depth). H_882 is the region-gate lever.
Result     : 🔴 CLOSED-NEGATIVE — RETAIN FAILs on all 5 seeds (gated z_drop ~+142..+150 ≫ ungated ~-12..-15);
             the output-logit gate makes forgetting WORSE (softmax couples masked R_base logits to the
             adaptation-driven R_new logits, starving the frozen base mass). GAIN passes on all 5.
Execution  : GPU (RTX 5070, aiden) · device cuda · cuDNN disabled (torch-nightly sublibrary mismatch;
             native CUDA conv path, numerically identical). Device-bug fix: eval batches moved to device.
SW-sim of non-deterministic on-chip edge-learn accepted at the measurement rung (a_scale_honest_scope);
foundation H_679 established HW edge-learn is real. post-tuning 0 · a_paper_negative_ok.
