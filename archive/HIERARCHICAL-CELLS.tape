#!/usr/bin/env tape

@V := "tape" :: spec [active]
  version = "1.2"

@I id001 := "hierarchical-cells" :: identity-claim [d=2026-05-15 active]
  kind = "anima 2-level cell substrate spec · declarative SSOT"
  brief = "direction γ hierarchical-cell architecture — L1 coarse / L2 fine spec · forward composition · loss · falsifier criteria · cost envelope"
  parent = "dancinlab/anima"
  sibling-log = "HIERARCHICAL-CELLS.log.tape"

# ══════════════════════════════════════════════════════════════
# HIERARCHICAL-CELLS.tape — direction γ paradigm shift
# 2-level cell pool: coarse category-gate × fine intra-category routing
# Carrier from STRICT-4A.step §2 direction γ
# ══════════════════════════════════════════════════════════════

# ── §1 motivation ─────────────────────────────────────────

@I motivation pscc_55_carry :: hierarchical [d=2026-05-14 ok]
  => "PSCC §55 § A6: 9 architectural variants tested across v3-routing class (top-K MoE + balance-aux + entropy-reg), all 4 paths (k Gumbel / l batch / m wider-d / n 5-seed) FALSIFIED for strict z>3.0. Routing differentiation 가 noise floor 와 동일 magnitude. Structural escape requires non-routing-axis innovation."

@I gap_in_current_arch :: hierarchical [d=2026-05-14 ok]
  => "v3-routing class flat cell pool — 64 cells, gradient stochasticity 가 routing direction 결정. 카테고리 5개 (self_definition/values/boundary/emotion/self_knowledge) 와 cell-pool 64 의 ratio (≈ 12.8) 가 학습-시 어떤 inductive bias 도 제공 안함. 2-level topology = 카테고리 수 일치 coarse layer (L1=5) + intra-category fine routing (L2=N per L1)"

# ── §2 architectural specification ─────────────────────────

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

# ── §9 cross-link ──────────────────────────────────────────

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
