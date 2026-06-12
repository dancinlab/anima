@V := "tape" :: spec [active]
  version = "1.0"

# Lane A-multi LARGER RUNG — HYBRID branching-corpus held-out at WIDER branching (B=5) on the full NC ladder
# substrate=HYBRID (on-chip AKD1000 encoder ⊕ off-chip host-CPU Elman decode head; numpy BPTT, NO torch)
# a_lane_akida_gpu_split (NEVER Lane G) · a_scale_honest_scope (>=3-rung) · a_completeness_over_cheap.
# chip: live AKD1000 BC.00.000.002, akida 2.19.1, pi5-akida ($0); 8 trials/rung, enc_learned=True every trial.
# harness: AKIDA/onchip_xlm_branching.py with env LANE_A_DELTAS="1,7,13,19,29" (B=5) LANE_A_LADDER_NC="40,45,50".
# seed: the proven A-multi rung was B=3, NC{30,40,50}. Does the transferable OPERATOR hold at a LARGER rung
#   (wider branching B=5 + larger codebook ladder)? off-chip head trained on TRAIN-concept targets ONLY.

@D laneA_multi_branchwide := "HYBRID multi-step composition GENERALIZES at WIDER branching (B=5) on a 3-rung NC ladder (40/45/50) — transferable OPERATOR holds at the larger rung" :: discovery [d=2026-06-03 active]
  seed      = "does the transferable transition OPERATOR (proven B=3) survive a LARGER rung — wider branching B=5 (DELTAS 1,7,13,19,29) + larger codebook NC ladder {40,45,50}? substrate=HYBRID (on-chip encoder ⊕ off-chip Elman head), NEVER Lane G."
  falsifier = "F-BRANCH-1: held-out hop-2 AND hop-3 do NOT stay above shuffle-NULL on the branching set-membership metric -> REFUTED iff each ci_lo>NULL hi AND p<0.05. F-BRANCH-2: held-out hop-2 NOT within 2.0x of in-dist hop-2 -> REFUTED iff heldout>=train/2.0."
  claim     = "F-BRANCH-1 REFUTED + F-BRANCH-2 REFUTED, GENERALIZES=True on live AKD1000 BC.00.000.002 (akida 2.19.1, learn_all=True every rung). headline NC=50 (chance=0.1020): held-out decay [0.0617, 0.8683, 0.9267]; hop-2 ci_lo=0.8394>shufNULL hi=0.2213 (p=0.005), hop-3 ci_lo=0.9069>shufNULL hi=0.2234 (p=0.005); hop-2 within 2x of in-dist 0.9364. ladder held-out hop-2/3: NC=40 [0.9229,0.9208], NC=45 [0.8518,0.8964], NC=50 [0.8683,0.9267]. off-chip head composes on TEST concepts NEVER trained to emit = transferable offset operator, not per-concept lookup."
  scope     = "toy NC<=50 (a_scale_honest_scope); next rung = 3B. substrate=HYBRID (on-chip AKD1000 encoder ⊕ off-chip host-CPU Elman decode head, numpy BPTT NO torch), NOT pure-AKIDA, NOT Lane G."
  target    = ".verdicts/lane-a-multi-rung/F-BRANCH-WIDE.txt (verbatim host stdout, terminal 🟢)"
