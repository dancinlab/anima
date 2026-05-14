#!/usr/bin/env tape
# ══════════════════════════════════════════════════════════════════════
# .tape v1.2 — grammar primer (cold-read by any LLM / agent / human)
# ══════════════════════════════════════════════════════════════════════
# Form: each entry is `@<type> <id> := "<subject>" :: <kind> [<grades>]`
#       optionally followed by body lines (2-space indent) — key=value,
#       edges (<- -> => …), or quoted prose.
#
# ENTRY TYPES (17):
#   Runtime (10): @S session  @U user  @A assistant  @T tool-call  @R result
#                 @H hook  @D decision  @K cost  @P provider  @? anomaly
#   Foundation:   @I identity-claim
#   Declarative:  @X external-citation  @F forbidden-pattern  @N note
#                 @C config  @L layout  @V spec-version
#
# EDGES (12, on body lines, 2-space indent):
#   Causal:     <- caused-by   -> triggers   == continues
#               ~> supersedes  !! aborts     |> verified-by
#   Effect:     => produces (followed by quoted natural-language)
#   Structural: <: specializes  :> generalizes  ?> soft-depends
#               !> conflicts-with  @> projects-to (e.g. @> AGENTS.md)
#
# GRADE TAGS (in [...] on entry header):
#   Delivery:   ok · err · denied · cancelled · partial · superseded
#   Governance: required · recommended · optional · draft · active · deprecated
#   Scoped:     allow:<x> · deny:<x>
#   Time/index: T<n> (turn)  N<n> (wall-sec)  d=<YYYY-MM-DD>
#
# PAYLOAD SYNTAX (body lines):
#   key = "value"           single-line string
#   key = [a, b, c]         array literal
#   key <<~EOF              heredoc (multi-line; ends with EOF on own line)
#     multi-line text
#   EOF
#   "see [@x1] §3"          inline citation by entry id
#   `cmd or path`           backtick code-span (inline only)
#
# Full spec: ~/core/tape/spec/tape.md (or github.com/dancinlab/tape)
# ══════════════════════════════════════════════════════════════════════
#
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
