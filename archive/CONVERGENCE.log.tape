#!/usr/bin/env tape
# CONVERGENCE.log.tape — append-only event history sibling of CONVERGENCE.tape
# (v1.2 architecture-vs-history split, 2026-05-15).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — append events below this line, chronological (oldest first).

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
