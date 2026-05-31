883_clm_replay_continual — id-keyed backing dir for H_883 (replay-buffer continual learning)
============================================================================================
Hypothesis : UNIVERSE/H_883_clm_replay_continual.md
Verdict    : .verdicts/clm-replay-continual/F-CLM-REPLAY.txt (+ _prereg.txt + clm_replay_continual_result.json)
Driver     : CLM/model/h883_replay_continual.hexa (executable python harness; project hexa-native policy)
Backbone   : clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) — mid d512/L8/E8, FROZEN core trunk
Edge       : H_865 trunk-adjacent thin adapter (rank=64, identity@step0) → FROZEN readout
Method     : W2 · interleave a SMALL replay buffer (REPLAY_RATIO=0.25, deterministic every-4th step)
             of OLD base-ability ("web" lane) samples into the edge-only on-chip adaptation stream;
             read z_drop(replay) vs z_drop(no_replay) and gain(replay) at the S=300 endpoint vs the
             F-CLM-REPLAY_prereg-frozen falsifier (R) z_drop(replay)<z_drop(no_replay) ∧ (G) gain(replay)>0.
Builds on  : H_861 (readout-only edge too shallow 🔴) · H_865 (adapter edge fixes BOUND 🟢) ·
             H_875 (forgetting curve — this is its follow-on SAFETY DEVICE). The no_replay arm IS the
             H_875 no-replay baseline, measured side-by-side in the same run.
SW-sim of non-deterministic on-chip edge-learn accepted at the measurement rung (a_scale_honest_scope);
foundation H_679 established HW edge-learn is real. post-tuning 0 · a_paper_negative_ok.
