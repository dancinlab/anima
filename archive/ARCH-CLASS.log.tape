#!/usr/bin/env tape
# ARCH-CLASS.log.tape — append-only event history sibling of ARCH-CLASS.tape
# (v1.2 LLM-judgment architecture-vs-history split, 2026-05-15).
#
# Carries: @S session start · @D point-in-time next-step decisions ·
# @? next-step gate observations. Strictly append-only — every entry records
# something that happened at a point in time, never edited or deleted.

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — arch-class lane iteration events · phase transitions

@S start s_arch_class :: arch_class [d=2026-05-14 ok]
  => "research lane for direction ε — fundamental escape from soft/top-K continuous gate paradigm. Routing becomes discrete (hashing, VQ-VAE, or attention-head-level mixture). Null permutation may behave fundamentally differently for discrete routes than continuous weights"

# ── §11 next step ──────────────────────────────────────────

@D next_step_phase_1 eps2_smoke :: arch_class [d=2026-05-14 ok]
  |> Mac local Phase 1
  => "Phase 1 ($0, 2-3 hr): write hash-route variant + 100-step smoke on Mac CPU. Verify gradient flow + bucket distribution + F-V5MIT regression"

@D next_step_phase_2 eps2_fire :: arch_class [d=2026-05-14 ok]
  |> Vast.ai Phase 2
  => "Phase 2 ($5-15, 1.5 hr): A100 fire SEED=42, 15K steps, F-PERSONA-4a measurement"

@? next_step_gate eps2_verdict :: arch_class [d=2026-05-14 ok]
  |> Phase 2 outcome gating
  => "z > 3.0 strict pass: cond #3 strict-4a CLOSED via ε2. z 2.0-3.0: multi-seed Phase 3. z < 1.0: falsify ε2 → carry ε3 OR direction γ"
