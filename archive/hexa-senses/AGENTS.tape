#!/usr/bin/env tape
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
