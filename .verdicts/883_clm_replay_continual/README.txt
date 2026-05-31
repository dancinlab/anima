883_clm_replay_continual — id-keyed backing dir for H_883 (replay-buffer continual learning)
=========================================================================================================
Hypothesis : UNIVERSE/H_883_clm_replay_continual.md
Verdict    : .verdicts/clm-replay-continual/F-CLM-REPLAY.txt (+ _prereg.txt + clm_replay_continual_result.json)
Driver     : CLM/model/h883_replay_continual.hexa (executable python harness; project hexa-native policy)
Backbone   : clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) — mid d512/L8/E8 (13,653,768 params)
Method     : W2 · interleave a SMALL replay buffer of OLD ("web" base-ability) batches into the SAME
             edge-only Adam stream (REPLAY_RATIO=0.25, every 4th step a replay step; core trunk FROZEN)
             vs a no_replay edge-learn run on the identical backbone/edge/seeds/step budget.
             Primary verdict read at S=300: PASS 🟢 iff z_drop(replay) < z_drop(no_replay) ∧ gain(replay) > 0.
Builds on  : H_861 (readout-only edge too shallow 🔴) · H_865 (trunk-adjacent adapter fixes BOUND 🟢, the
             edge that actually moves) · H_872/H_879 (freeze-depth / per-layer edge) · H_875 (forgetting
             curve — the no_replay arm IS the side-by-side baseline). Foundation H_679 (HW edge-learn real).
Execution  : CPU-LOCAL on this Mac (no runpod/cloud); SW-sim of the non-deterministic on-chip edge-learn
             accepted at the measurement rung (a_scale_honest_scope); replay does NOT trigger a
             deterministic full-retrain — it only mixes a few old batches into the edge-only stream (@L1).
Thresholds : F-CLM-REPLAY_prereg.txt VERBATIM (frozen 2026-05-31, post-tuning 0). a_paper_negative_ok.
