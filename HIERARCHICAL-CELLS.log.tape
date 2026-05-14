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
# HIERARCHICAL-CELLS.log.tape — append-only event history sibling of HIERARCHICAL-CELLS.tape
# (v1.2 LLM-judgment architecture-vs-history split, 2026-05-15).
#
# Carries: @S session start · @D point-in-time next-step decisions ·
# @? next-step gate observations. Strictly append-only — every entry records
# something that happened at a point in time, never edited or deleted.

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — hierarchical-cells lane iteration events · phase transitions

@S start s_hierarchical :: hierarchical [d=2026-05-14 ok]
  => "research lane for direction γ (PERSONA.tape §A6 falsified 4 paths → STRICT-4A.step §2 paradigm shift options). 2-level cell pool topology test if routing-level inductive bias toward 5 categories breaks §A2-trap"

# ── §8 next step ──────────────────────────────────────────

@D next_step_phase_1 :: hierarchical [d=2026-05-14 ok]
  |> impl smoke
  => "Phase 1 (Mac local, $0, 4-6 hr): write training/mitosis_model_v5_hierarchical.py + smoke test (single batch forward + grad check + split/merge L2 ops + F-V5MIT-1..5 regression). NO H100 fire until smoke clean"

@D next_step_phase_2 :: hierarchical [d=2026-05-14 ok]
  |> single-seed verify
  => "Phase 2 ($5-15, 1.5 hr): fire on Vast.ai A100/H100, SEED=42, 15K steps, measure F-PERSONA-4a with hierarchical-aware metric (L1-weight diff)"

@? next_step_gate :: hierarchical [d=2026-05-14 ok]
  |> Phase 2 result gating
  => "If single-seed z>2.0 on L1 axis: proceed Phase 3 multi-seed. If z<1.0: falsify direction γ + carry to direction ε. If between: re-fire with hyperparam tune"
