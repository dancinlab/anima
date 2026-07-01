880_clm_adapter_stack — id-keyed backing dir for H_880 (adapter-stack accumulation · per-context switch)
========================================================================================================
Hypothesis : UNIVERSE/H_880_clm_adapter_stack.md
Verdict    : .verdicts/clm-adapter-stack/F-CLM-ADAPTER-STACK.txt (+ _prereg.txt + clm_adapter_stack_result.json)
Driver     : CLM/model/h880_adapter_stack.hexa (contract surface; project hexa-native policy)
Runtime    : h880_adapter_stack_runtime.py.txt (the executable measurement harness, reuses H_865
             AdapterEdge / make_lane_bytes / infer_config_and_load verbatim; stored as .py.txt because
             the repo blocks new .py — the .hexa is the source-of-truth contract)
Backbone   : clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) — mid d512/L8/E8, FROZEN core
Method     : W2 · stack K=4 thin H_865 adapters (one per context) between FROZEN norm_out and FROZEN
             readout; train ONE AT A TIME (param isolation); per-context switch at inference. Three frozen
             gates: NEW-GAIN min_k gain_k>0 ∧ OLD-Z-DROP z_drop_old<1.0 (bf98c01) ∧ INTERFERENCE own
             adapter strictly best (max_{i≠j}(-interf)<0).
Builds on  : H_679 (PLASTICITY HW edge-learn, foundation) · H_865 (thin adapter edge, BOUND 🟢).
Execution  : GPU (RTX 5070, aiden) · device cuda · cuDNN disabled (torch-nightly sublibrary mismatch;
             native CUDA conv path, numerically identical). Device-bug fix: eval batches moved to device.
SW-sim of non-deterministic on-chip edge-learn accepted at the measurement rung (a_scale_honest_scope);
foundation H_679 established HW edge-learn is real. post-tuning 0 · a_paper_negative_ok.
