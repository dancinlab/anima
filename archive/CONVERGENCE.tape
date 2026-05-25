#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "anima.convergence" :: identity-claim [d=2026-05-15 active]
  kind = "anima convergence-cycle milestone projection · architecture SSOT"
  brief = "honesty-triad C3-closure precondition + Ψ=1/2 fixed-point target. Live records in ~/core/anima/convergence/*.convergence."
  parent = "dancinlab/anima"
  sibling-log = "CONVERGENCE.log.tape"

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
