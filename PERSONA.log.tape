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
# PERSONA.log.tape — append-only event history sibling of PERSONA.tape
# (v1.2 architecture-vs-history split, 2026-05-14).
#
# Carries: @A · @T · @R · @K · @? runtime events · @D :: decision events ·
#          @H hook fires. Strictly append-only — every entry records something
#          that happened at a point in time, never edited or deleted.
# Authority: AGENTS.tape § @D g_arch_vs_log_split

@V v1 := "tape" :: spec [active]
  version = "1.2"

# §Log — saga timeline · 3-seed BG measurements · dated falsifications
# (chronological, oldest first; section headers preserved for cycle context)

# ── §3 saga timeline ─────────────────────────────────────────

@D row_38_0 :: persona [ok]
  pscc = "§38"
  event = "Principle #3 audit CLEAN"
  f_persona_4_status = "F-PERSONA-1/5 ☑"

@D row_40_1 :: persona [ok]
  pscc = "§40"
  event = "initial measurement MODERATE 3/5"
  f_persona_4_status = "F-PERSONA-4 KL 9.7e-5 FAIL (untrained pool)"

@D row_42_2 :: persona [ok]
  pscc = "§42"
  event = "§A1 amendment Φ threshold 0.5→0.05 STRONG 4/5"
  f_persona_4_status = "F-PERSONA-3 PARTIAL → PASS"

@D row_44_3 :: persona [ok]
  pscc = "§44"
  event = "v1 cotrain $1.26 H100"
  f_persona_4_status = "KL=0.0 winner-take-all monopoly FAIL"

@D row_45_4 :: persona [ok]
  pscc = "§45"
  event = "v2 entropy-reg λ=0.1 cotrain $1.32 H100"
  f_persona_4_status = "KL=0.0 FAIL BUT M4 z=3.20 NEW finding (routing-content split)"

@D row_47_5 :: persona [ok]
  pscc = "§47"
  event = "(b) softmax τ sweep FALSIFIED"
  f_persona_4_status = "KL ≤ 0.005 « 0.5"

@D row_48_6 :: persona [ok]
  pscc = "§48"
  event = "(a) per-cat corpus SMALL FALSIFIED"
  f_persona_4_status = "KL=0.0 monopoly carry"

@D row_49_7 :: persona [ok]
  pscc = "§49"
  event = "(d) per-session pool FALSIFIED"
  f_persona_4_status = "KL ≪ 0.5 by 4 OoM"

@D row_50_8 :: persona [ok]
  pscc = "§50"
  event = "§A3 amendment land → cond #3 ☑ via 4b path"
  f_persona_4_status = "M4 z=3.20 single-seed strict"

@D row_52_9 :: persona [ok]
  pscc = "§52"
  event = "v7 hard top-K MoE + balance-aux + entropy-reg $0.31 H100"
  f_persona_4_status = "**first KL>0 across saga**: KL=3.45 z=2.75 p=0.01 marginal"

@D row_53_10 :: persona [ok]
  pscc = "§53"
  event = "§A4 amendment dual-axis + 3-seed BG fire ($1.4 est)"
  f_persona_4_status = "in-flight closure"

# ── §5 in-flight evidence — 3-seed BG (PSCC §53) ─────────────────────────────────────────

@D row_2000_0 :: persona [ok]
  step = "2000"
  v7_4a_z = "-0.55"
  seed_43_4a_z = "0.11"
  seed_45_4a_z = "0.20"
  mean_4a = "-0.08"
  v7_4b_z = "0.45"
  seed_43_4b_z = "2.44"
  seed_45_4b_z = "0.42"
  mean_4b = "1.10"

@D row_4000_1 :: persona [ok]
  step = "4000"
  v7_4a_z = "0.93"
  seed_43_4a_z = "-0.29"
  seed_45_4a_z = "1.13"
  mean_4a = "0.59"
  v7_4b_z = "0.45"
  seed_43_4b_z = "1.05"
  seed_45_4b_z = "0.67"
  mean_4b = "0.72"

@D row_6000_2 :: persona [ok]
  step = "6000"
  v7_4a_z = "0.64"
  seed_43_4a_z = "0.57"
  seed_45_4a_z = "0.73"
  mean_4a = "0.65"
  v7_4b_z = "0.29"
  seed_43_4b_z = "0.97"
  seed_45_4b_z = "1.54"
  mean_4b = "0.93"

@D row_8000_3 :: persona [ok]
  step = "8000"
  v7_4a_z = "-0.08"
  seed_43_4a_z = "0.02"
  seed_45_4a_z = "0.88"
  mean_4a = "0.27"
  v7_4b_z = "0.22"
  seed_43_4b_z = "1.07"
  seed_45_4b_z = "1.72"
  mean_4b = "1.00"

@D row_10000_4 :: persona [ok]
  step = "10000"
  v7_4a_z = "1.61"
  seed_43_4a_z = "**2.27**"
  seed_45_4a_z = "1.59"
  mean_4a = "**1.82**"
  v7_4b_z = "0.54"
  seed_43_4b_z = "**1.75**"
  seed_45_4b_z = "**2.36**"
  mean_4b = "**1.55**"

@D row_12000_5 :: persona [ok]
  step = "12000"
  v7_4a_z = "2.61"
  seed_43_4a_z = "0.57"
  seed_45_4a_z = "(pending)"
  mean_4a = "—"
  v7_4b_z = "0.52"
  seed_43_4b_z = "1.66"
  seed_45_4b_z = "(pending)"
  mean_4b = "—"

# ── §7 ROADMAP — strict-4a closure paths (post-§A5) ─────────────────────────────────────────

# **v3-routing = v7 = v8 combined trainer** 가 routing axis 의 **첫 KL>0 도달**
# (saga-wide KL=0 → mean 3.04 across 3 seeds) 그러나 strict z>3.0 multi-seed
# 미도달 (mean z=1.48, §A2-trap CONFIRMED). Per-path dated verdicts below.

@D row_k_0 reject hypothesis_k :: persona [d=2026-05-14 ok]
  |> Gumbel-softmax routing architectural variant
  => "PSCC §54 partial $0.25 — KL inflated 4-5× (13.82/12.68) but z unchanged (1.36/0.31); null distribution inherits Gumbel noise equally"

@D row_l_1 reject hypothesis_l :: persona [d=2026-05-14 ok]
  |> batch-scaling test (variance reduction proxy for DDP)
  => "PSCC §55 $3.01 4 fires — b32 s42 z=+2.58 vs b32 s43 z=-2.80 at SNAP 2K (Δ=5.4 cross-seed); s43 final z=0.73; b64 z=0.47. No batch→z trend."

@D row_m_2 reject hypothesis_m :: persona [d=2026-05-14 ok]
  |> wider d_model 1024 representation scale-up
  => "PSCC §55 full 15K $1.91 — 4a KL=1.07 z=0.30 / 4b z=0.83 / F-V5MIT 5/5; 7-SNAP mean z=0.57. Wider repr alone produces WEAKER signal than baseline v7."

@D row_n_3 reject hypothesis_n :: persona [d=2026-05-14 ok]
  |> 5-seed envelope cheapest
  => "PSCC §54 partial $1.48 (seeds 46+47 SIGKILL @ step 11900) — 5-seed mean @ step 10K: 4a z=1.69 / 4b z=1.65. §A5 §A2-trap CONFIRMED."

# ── §A6 cumulative cost record (PSCC §54+§55 2026-05-14) ─────────

@K a6_cumulative = 31+190+165+173+492 = 1051 ucents-cents :: cost [d=2026-05-14 ok]
  => "saga §52-§55 cumulative $10.51 (v7 $0.31 + leftover $1.90 + §53.5 3-seed $1.65 + §54 $1.73 + §55 $4.92)"
