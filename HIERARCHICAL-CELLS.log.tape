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
# HIERARCHICAL-CELLS.log.tape — append-only event history (v1.2 split)
# Sibling: HIERARCHICAL-CELLS.tape (architecture-current, editable)
# ══════════════════════════════════════════════════════════════

@V := "tape" :: spec [active]
  version = "1.2"

# §Log — entries chronological, oldest first.

@S start s_hierarchical :: hierarchical [d=2026-05-14 ok]
  => "research lane for direction γ (PERSONA.tape §A6 falsified 4 paths → STRICT-4A.step §2 paradigm shift options). 2-level cell pool topology test if routing-level inductive bias toward 5 categories breaks §A2-trap"

# ── §1 motivation ─────────────────────────────────────────


@D arch_l1_coarse :: hierarchical [d=2026-05-14 ok]
  |> Level-1 coarse category gate
  => "L1 = 5 cells (matches identity_probe category count). Router_L1 = Linear(d_model → 5). Soft-gate with annealed Gumbel-softmax to prevent winner-take-all on L1 (key — L1 monopoly = same §A2-trap)"


@D arch_l2_fine :: hierarchical [d=2026-05-14 ok]
  |> Level-2 fine intra-category routing
  => "Each L1 cell has M sub-cells (M=8 baseline). Router_L2[i] = Linear(d_model → M) per L1 cell. Hard top-K (k=2) selection on L2 → stochastic specialization within category"


@D arch_combined_forward :: hierarchical [d=2026-05-14 ok]
  |> Forward pass composition
  => "weights_L1 = gumbel_softmax(router_L1(x), τ_anneal). weights_L2[i] = topK(router_L2[i](x), k=2). combined_weight[i,j] = weights_L1[i] * weights_L2[i,j]. cell_outputs sum weighted by combined_weight"


@D arch_total_cells :: hierarchical [d=2026-05-14 ok]
  |> total parameter envelope
  => "L1=5 × L2=8 = 40 fine-cells vs flat 64. Each cell smaller (d=384 baseline → d_cell=128 with L1 specialization). Net params similar order (~25M total cell weights)"


@D arch_loss_composition :: hierarchical [d=2026-05-14 ok]
  |> training loss
  => "L = CE + α_aux_L1 * load_balance_L1 + α_aux_L2 * load_balance_L2 + λ_ent_L1 * entropy(weights_L1) + λ_ent_L2 * entropy(weights_L2). L1 entropy_reg prevents single-L1 monopoly (the critical mechanism)"

# ── §3 hypothesis ──────────────────────────────────────────


@D impl_trainer_fork :: hierarchical [d=2026-05-14 ok]
  |> training/mitosis_model_v5_hierarchical.py
  => "Fork mitosis_model_v5.py (current flat cell pool). Replace MitosisModelEngine.forward with 2-level routing. New: HierarchicalRouter class. Modify split/merge to operate on L2 sub-cells only (L1 fixed at 5). Estimated ~300 LoC fork"


@D impl_train_script :: hierarchical [d=2026-05-14 ok]
  |> state/anima_hier_2level_cells_<date>/train_hier.py
  => "Fork train_v5mitosis_cotrain_v3_routing.py with hierarchical engine + L1+L2 aux loss + entropy reg per level. ~150 LoC delta"


@D impl_falsifier_extend :: hierarchical [d=2026-05-14 ok]
  |> F-PERSONA-4a measurement update
  => "Existing measurement (per-prompt weights → cat-mean → pairwise KL → null permutation) operates on combined_weight[L1, L2]. Can also test L1-only weight space (5-dim) for cleaner diagnostic"

# ── §6 cost / wall envelope ────────────────────────────────


@K direction_gamma_cost = 15+80 = 9500 ucents-cents :: hierarchical [d=2026-05-14 ok]
  |> single fire envelope per STRICT-4A.step §4
  => "$15-80 H100 — biggest architectural rewrite among 5 directions. Includes ~300 LoC mitosis_model fork + dispatch + 3-seed verification ($15 × 3 ≈ $45 + dev time)"


@K cost_breakdown :: hierarchical [d=2026-05-14 ok]
  |> per-stage breakdown
  => "Phase 1 (impl + smoke) $0 Mac local 4-6 hr. Phase 2 (single-seed verify) $5-15 H100 1.5 hr. Phase 3 (3-seed §A2 robustness) $15-45 H100 4.5 hr. Phase 4 (24L scale-up if Phase 3 PASS) $50-150 H100 4-8 hr"

# ── §7 risk ────────────────────────────────────────────────


@? risk_l1_monopoly :: hierarchical [d=2026-05-14 ok]
  |> L1 winner-take-all risk
  => "Even with entropy_reg + load_balance_aux, L1 (only 5 cells) is SMALLER pool — winner-take-all easier than flat 64. Gumbel-softmax with high τ helps but kills determinism. If L1 entropy collapse occurs, hierarchical topology becomes effectively flat-with-5-survivors — possibly WORSE than flat-64"


@? risk_l2_routing_redundant :: hierarchical [d=2026-05-14 ok]
  |> L2 may be redundant
  => "If L1 fully separates categories, L2 within-category sub-cells may be unused (single L2 cell per L1 sufficient). Hierarchical overhead w/o gain. Mitigation: probe to L2 importance via gate entropy + active-cell count"


@? risk_more_seeds_more_a2 :: hierarchical [d=2026-05-14 ok]
  |> more architectural complexity = more seed-dependent
  => "Larger search space (L1 + L2 + 2-axis aux) — gradient noise compounds. Multi-seed variance may be EVEN HIGHER than flat v3-routing. n=3 verification mandatory; n=5 envelope recommended"


@? risk_mitosis_split_merge_break :: hierarchical [d=2026-05-14 ok]
  |> existing mitosis mechanism compat
  => "Current mitosis_model_v5 assumes flat cells list. Hierarchical adds 2-level nesting. split_cell / merge_cells need rewrite to handle L2 sub-cell ops within fixed L1 parent. F-V5MIT-1..5 falsifiers test this — risk: F-V5MIT-2 MERGE-WEIGHT may break if L1-L2 cross-merge attempted"

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

# ── §9 cross-link ──────────────────────────────────────────

