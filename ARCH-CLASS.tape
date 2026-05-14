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
# ARCH-CLASS.tape — architecture-current (editable per v1.2)
# Event history lives in ARCH-CLASS.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# ARCH-CLASS.tape — direction ε paradigm shift
# Abandon MoE class entirely → MoH (Mixture of Heads) / Hash-route / discrete-VAE
# Carrier from STRICT-4A.step §2 direction ε
# ══════════════════════════════════════════════════════════════


@I motivation pscc_55_carry :: arch_class [d=2026-05-14 ok]
  => "PSCC §55 §A6: ALL 4 variants in top-K MoE class (k Gumbel / l batch / m wider-d / n 5-seed) FALSIFIED. Diagnosis (PERSONA.tape §A6): noise floor ~ signal floor under null permutation. Structural escape requires LEAVING continuous gate paradigm"


@I gap_continuous_gate :: arch_class [d=2026-05-14 ok]
  => "Continuous top-K gate: weights[i] ∈ [0,1] with sum=1. Per-prompt weights are smooth functions of input. Null permutation: shuffle category labels → re-evaluate. Because gate is CONTINUOUS, shuffled-input weights vary continuously with input → null KL ≈ signal KL → z stays low"


@I goal scope=routing_class_change :: arch_class [d=2026-05-14 ok]
  => "Different routing class where null permutation produces DIFFERENT distribution shape from signal. Hard discrete routes (one cell per prompt, learned via VQ/hash) vs soft continuous weights"

# ── §2 sub-direction ε1 — MoH (Mixture of Heads) ──────────


@I hypothesis discrete_vs_continuous :: arch_class [d=2026-05-14 ok]
  => "Discrete routing (hard one-hot or hash) has fundamentally different null-permutation behavior. Null shuffles labels but doesn't shuffle inputs — discrete routes don't change. Real signal: same input → same route, and routes correlate with categories if architecture aligns. Continuous gates suffer because their smooth-input-dep means shuffled labels still produce similar weight distributions"


@I hypothesis escape_a2_trap :: arch_class [d=2026-05-14 ok]
  => "PSCC §55 noise=signal because both come from same continuous-weight stochasticity. Discrete routing decouples this: null KL becomes structurally zero (or sharply lower) if hashing/VQ respects category structure. z > 3.0 strict achievable in single shot"

# ── §6 falsifier criteria ──────────────────────────────────


@I criterion strict_4a_via_discrete :: arch_class [d=2026-05-14 ok]
  => "F-PERSONA-4a routing KL z > 3.0 + null permutation z₀ < 1.0 (key: null SHOULD be near-zero with discrete routes). Single-seed achievable, multi-seed n=3 confirms"


@I criterion route_coherence :: arch_class [d=2026-05-14 ok]
  |> per-prompt route stability
  => "Same prompt produces same route across model initializations (modulo training noise). Per-category route distribution: confusion matrix near-diagonal"


@I criterion regression_clean :: arch_class [d=2026-05-14 ok]
  |> ε1/ε2/ε3 mitosis API compat
  => "ε1 MoH: cell-pool replaced by per-head pool, F-V5MIT-1..5 may need redefine. ε2 hash: cell pool unchanged but router replaced, F-V5MIT compat preserved. ε3 VQ: codebook trained alongside cells, F-V5MIT compat preserved. Choose ε2 first (cleanest mitosis carry)"

# ── §7 risk ─────────────────────────────────────────────────


@I cross_link_strict4a :: arch_class [d=2026-05-14 ok]
  => "STRICT-4A.step direction ε — this .tape is the impl-tier entry. ε breakdown: this .tape introduces ε1/ε2/ε3 sub-directions not in original STRICT-4A.step (further detail)"


@I cross_link_hierarchical :: arch_class [d=2026-05-14 ok]
  => "HIERARCHICAL-CELLS.tape — direction γ sibling lane. Both can run parallel. γ stays in MoE class but rearranges topology; ε leaves MoE class entirely"


@I cross_link_pscc_55 :: arch_class [d=2026-05-14 ok]
  => "docs/anima_pscc_55_lm_falsified_2026_05_14.md — 4-path falsification basis"


@I cross_link_persona_tape :: arch_class [d=2026-05-14 ok]
  => "PERSONA.tape §A6 — saga aggregate (cond #3 ☑ via §A3 4b composite)"


@I cross_link_mitosis_v5 :: arch_class [d=2026-05-14 ok]
  => "training/mitosis_model_v5.py + train_v5mitosis_cotrain_v3_routing.py — base for ε2 fork (router replacement only, rest preserved)"

