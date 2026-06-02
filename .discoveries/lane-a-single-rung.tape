@V := "tape" :: spec [active]
  version = "1.0"

# Lane A-single SCALE-TRANSFER RUNG — single-step open-vocab GENERATION across an ANCHOR-COUNT ladder
# substrate=AKIDA (on-chip 1-bit Hebbian) · a_lane_akida_gpu_split · a_scale_honest_scope (>=3-rung ladder)
# chip: live AKD1000 BC.00.000.002, akida 2.19.1, pi5-akida ($0); 8 trials/rung, encoder_learned per trial.
# harness: AKIDA/onchip_xlm_gen_scale.py (byte-match onchip_xlm_generation enc/bind/FC/decode; concept subset varies).

@D laneA_single_genscale := "single-step on-chip GENERATION SCALE-SURVIVES across a 3-rung anchor-count ladder (50/100/250) on live AKD1000" :: discovery [d=2026-06-03 active]
  seed      = "does the proven single-step open-vocab generation (one scale point, 250 anchors, gen_ci_lo=0.4096) hold ABOVE shuffle-NULL as the codebook/anchor count grows? substrate=AKIDA, NEVER merged with Lane G."
  falsifier = "F-GEN-SCALE-1: single-step gen does NOT hold above shuffle-NULL as anchors grow -> REFUTED iff EVERY rung gen ci_lo>NULL hi AND p<0.05. F-GEN-SCALE-2: gen collapses toward chance -> REFUTED iff largest-rung ci_lo>NULL hi AND >=2x chance."
  claim     = "F-GEN-SCALE-1 REFUTED + F-GEN-SCALE-2 REFUTED on live AKD1000 BC.00.000.002 (akida 2.19.1, learn_all_hw=True every rung). NC=10/50anch: gen ci_lo=0.6237 vs shufNULL hi=0.2794 (p=0.005); NC=20/100anch: 0.4761 vs 0.1228 (p=0.005); NC=50/250anch: 0.4131 vs 0.0431 (p=0.005) AND >identity-NULL 0.4009 (produces not echo at full scale). all aboveShuf + >=2x chance. single-step A-single ceiling is SCALE-ROBUST, not a single-point artefact; gen-vs-echo gap widens in favor of produce as anchors grow."
  scope     = "toy vocab (a_scale_honest_scope); production full-LM ladder separate. substrate=AKIDA (on-chip 1-bit Hebbian), NOT HYBRID, NOT Lane G."
  target    = ".verdicts/lane-a-single-rung/F-GEN-SCALE.txt (verbatim on-chip stdout, terminal 🟢)"
