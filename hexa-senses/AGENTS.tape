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
# AGENTS.tape for `anima/hexa-senses` subfolder
# Inherits LATTICE_POLICY governance from anima/AGENTS.tape; adds
# hexa-senses-specific identity.

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "hexa-senses" :: identity-claim [d=2026-05-14 active]
  kind = "anima sub-project · 5-verb sensory substrate"
  parent = "dancinlab/anima"
  axis = "5 sensory channels (matter / DNA / RNA / antibody / ligand modality)"

# Parent governance applies — inherit from anima/AGENTS.tape
@D g_inherit := "inherits-parent-governance" :: governance [required]
  rule = "All anima/AGENTS.tape governance rules (g1..g8) apply here unchanged."
  apply-list = "real-limits-first · lattice-is-tool · verification-anchor-real-limit · no-artificial-ceilings · honesty-obligation-external · philosophy-ledger-append-only · commit conventions"
  authority = "[@x_anima_agents]"
  @> AGENTS.md

@X x_anima_agents := "anima/AGENTS.tape" :: parent-governance [active]
  url = "https://github.com/dancinlab/anima/blob/main/AGENTS.tape"
  scope = "parent governance — LATTICE_POLICY + philosophy pipeline + commit conventions"

@X x_lattice_policy := "anima/LATTICE_POLICY.md" :: policy [d=2026-05-12 active]
  url = "https://github.com/dancinlab/anima/blob/main/LATTICE_POLICY.md"
  scope = "dancinlab-wide real-limits-first standard"

@X x_tape_spec := "tape v1.2 spec" :: spec [d=2026-05-14 active]
  url = "https://github.com/dancinlab/tape/blob/main/spec/tape.md"

@H h1 := "agents-md-replaced" :: generator [active]
  note = "AGENTS.md (53-line LATTICE_POLICY wrapper, identical to anima root template) replaced by this AGENTS.tape — governance inherited from parent anima/AGENTS.tape."

@H h2 := "claude-md-symlink" :: generator [active]
  rule = "CLAUDE.md → AGENTS.tape symlink"
  command = `ln -sf AGENTS.tape CLAUDE.md`
