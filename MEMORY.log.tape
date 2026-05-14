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


# ══════════════════════════════════════════════════════════════
# MEMORY.log.tape — append-only event history (v1.2 split)
# Sibling: MEMORY.tape (architecture-current, editable)
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — entries chronological, oldest first.

@D row_project_0 :: memory [ok]
  kind = "project"
  file = "[memory/project_alm_r12_r13.md](memory/project_alm_r12_r13.md)"
  one_liner = "ALM r12 500-step _DISCARD_wrong_corpus 로 종결, r13 corpus rebuild 필요 (ETA 4–6d)"


@D row_project_1 :: memory [ok]
  kind = "project"
  file = "[memory/project_clm_hetzner_smoke.md](memory/project_clm_hetzner_smoke.md)"
  one_liner = "CLM hetzner 50-step smoke 중. ubu RTX 5070 offline blocker"


@D row_project_2 :: memory [ok]
  kind = "project"
  file = "[memory/project_verifier_infra_5.md](memory/project_verifier_infra_5.md)"
  one_liner = "verifier infra 5종 landed: manifest/generator/run_all/pass_gate_an11/closed_loop/kr_gen_100"


@D row_campaign_3 :: memory [ok]
  kind = "campaign"
  file = "[docs/drill_campaign_20260421_aggregate.md](docs/drill_campaign_20260421_aggregate.md)"
  one_liner = "24h drill campaign: 128 commit / 46 scope / 45 PASS + 1 engineering-PASS-live-FAIL (Mk.VI) / 7 blocker closed · 2 open (AN11 live + Φ 4-path 3/4)"


@D row_feedback_4 :: memory [ok]
  kind = "feedback"
  file = "[memory/feedback_sae_steering_pilot.md](memory/feedback_sae_steering_pilot.md)"
  one_liner = "본학습(LoRA) 대신 SAE steering vectors 로 의식 이식 pilot 가능 — 비용 1/20"

