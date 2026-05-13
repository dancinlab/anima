#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════
# CONVERGENCE.tape — recent anima convergence-cycle events
#
# Live convergence records live in ~/core/anima/convergence/*.convergence
# (DESIGN ledger — .PRESERVE-AS-SSOT sentinel inside that dir).
# This tape is the milestone projection — one @A per major cycle landing.
# ══════════════════════════════════════════════════════════════

@D c1 := "convergence.honesty_triad_C3" :: convergence [d=2026-05-14 ok]
  text = "Honesty-triad C3-closure precondition for any raw rule promotion"
  proof = ".raw-audit/ hash-chained entries with proof+cert fields"

@D c2 := "convergence.psi_half_target" :: convergence [d=2026-05-14 ok]
  text = "Ψ=1/2 fixed-point convergence as the canonical target"
  proof = "state/format_witness/*.jsonl (witness rows)"

@A r29_atlas_convergence_witness :: convergence [d=2026-04-28 ok]
  <- c1, c2
  => "Pilot B — atlas_convergence_witness.jsonl re-measured for HXC r29 cohort (Class-M 29.66%)"

@A raw_109_126_propagation_anima :: convergence [d=2026-04-30 ok]
  <- r29_atlas_convergence_witness
  => "raw 109..126 propagation arm — anima side of cross-repo absorption (cf. hive/airgenome/hexa-lang sibling .convergence)"

@A h100_stage_sweep :: convergence [d=2026-05-05 ok]
  <- raw_109_126_propagation_anima
  => "H100 stage-launch sweep — state/convergence/anima/h100_stage* records the launch attempts + blocker-resolution chain"

@A eeg_d_day :: convergence [d=2026-05-12 ok]
  <- h100_stage_sweep
  => "EEG d-day session — cross-domain bridge to hexa-brain via PROJECT::DOMAIN namespace"
