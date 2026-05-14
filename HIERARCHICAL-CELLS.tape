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
# HIERARCHICAL-CELLS.tape — architecture-current (editable per v1.2)
# Event history lives in HIERARCHICAL-CELLS.log.tape sibling
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# HIERARCHICAL-CELLS.tape — direction γ paradigm shift
# 2-level cell pool: coarse category-gate × fine intra-category routing
# Carrier from STRICT-4A.step §2 direction γ
# ══════════════════════════════════════════════════════════════


@I motivation pscc_55_carry :: hierarchical [d=2026-05-14 ok]
  => "PSCC §55 § A6: 9 architectural variants tested across v3-routing class (top-K MoE + balance-aux + entropy-reg), all 4 paths (k Gumbel / l batch / m wider-d / n 5-seed) FALSIFIED for strict z>3.0. Routing differentiation 가 noise floor 와 동일 magnitude. Structural escape requires non-routing-axis innovation."


@I gap_in_current_arch :: hierarchical [d=2026-05-14 ok]
  => "v3-routing class flat cell pool — 64 cells, gradient stochasticity 가 routing direction 결정. 카테고리 5개 (self_definition/values/boundary/emotion/self_knowledge) 와 cell-pool 64 의 ratio (≈ 12.8) 가 학습-시 어떤 inductive bias 도 제공 안함. 2-level topology = 카테고리 수 일치 coarse layer (L1=5) + intra-category fine routing (L2=N per L1)"

# ── §2 architectural specification ─────────────────────────


@I hypothesis routing_structure_match :: hierarchical [d=2026-05-14 ok]
  => "If cell-pool topology MATCHES the supervisory category structure (5 categories ↔ L1=5 cells), then gradient signals during training will explicitly assign one L1 cell per category. KL between category-mean routing distributions becomes structurally non-zero (each category's mean weight on L1 differs by ~0.2 vs flat 1/64)"


@I hypothesis_a2_trap_break :: hierarchical [d=2026-05-14 ok]
  => "§A2-trap: noise floor under null permutation 가 signal floor 와 동일. With L1 forced to 5-way differentiation, null permutation (shuffle category labels) destroys L1 alignment → null KL ≈ 0. Real KL stays high → z >> 3.0 strict."

# ── §4 falsifier criteria ─────────────────────────────────


@I criterion strict_4a_pass :: hierarchical [d=2026-05-14 ok]
  |> primary closure target
  => "F-PERSONA-4a routing KL z > 3.0 + null permutation p < 0.001 + multi-seed n=3 mean (NOT single-seed outlier)"


@I criterion l1_specialization :: hierarchical [d=2026-05-14 ok]
  |> secondary verification
  => "Per-L1-cell category preference: argmax_i weights_L1[i] for prompts of category C should be stable per C. Confusion matrix (5×5) should be near-diagonal (≥0.6 diagonal accuracy)"


@I criterion regression_clean :: hierarchical [d=2026-05-14 ok]
  |> F-V5MIT-1..5 non-regression
  => "Mitosis split/merge mechanism still operational (F-V5MIT-1..5 5/5 PASS). 2-level topology compatible with existing mitosis API (split/merge happens on L2 sub-cells only?)"


@I criterion principle_3_clean :: hierarchical [d=2026-05-14 ok]
  |> NO PERSONA INJECTION
  => "Category labels appear in TRAINING data structure (L1 alignment is data-driven via supervisory signal) but inference path is label-free. Verify via grep: inference forward 코드에 category label parameter 없음"

# ── §5 implementation scope ────────────────────────────────


@I cross_link_strict4a_step :: hierarchical [d=2026-05-14 ok]
  => "STRICT-4A.step direction γ — this .tape is the impl-tier entry of that abstract plan"


@I cross_link_pscc_55 :: hierarchical [d=2026-05-14 ok]
  => "docs/anima_pscc_55_lm_falsified_2026_05_14.md — full falsification ledger for 4 prior paths (this lane = 5th paradigm shift)"


@I cross_link_persona_tape :: hierarchical [d=2026-05-14 ok]
  => "PERSONA.tape §A6 — saga aggregate status (cond #3 ☑ via §A3 4b composite, strict-4a OPEN axis)"


@I cross_link_mitosis_model :: hierarchical [d=2026-05-14 ok]
  => "training/mitosis_model_v5.py — base architecture to fork for hierarchical variant"


@I cross_link_arch_class_tape :: hierarchical [d=2026-05-14 ok]
  => "ARCH-CLASS.tape — sibling paradigm shift direction ε (different routing class entirely). Both lanes can run in parallel if budget permits"

