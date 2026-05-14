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

@V := "tape" :: spec [active]
  version = "1.2"

# ══════════════════════════════════════════════════════════════
# ARCH-CLASS.tape — direction ε paradigm shift
# Abandon MoE class entirely → MoH (Mixture of Heads) / Hash-route / discrete-VAE
# Carrier from STRICT-4A.step §2 direction ε
# ══════════════════════════════════════════════════════════════

@S start s_arch_class :: arch_class [d=2026-05-14 ok]
  => "research lane for direction ε — fundamental escape from soft/top-K continuous gate paradigm. Routing becomes discrete (hashing, VQ-VAE, or attention-head-level mixture). Null permutation may behave fundamentally differently for discrete routes than continuous weights"

# ── §1 motivation ─────────────────────────────────────────

@I motivation pscc_55_carry :: arch_class [d=2026-05-14 ok]
  => "PSCC §55 §A6: ALL 4 variants in top-K MoE class (k Gumbel / l batch / m wider-d / n 5-seed) FALSIFIED. Diagnosis (PERSONA.tape §A6): noise floor ~ signal floor under null permutation. Structural escape requires LEAVING continuous gate paradigm"

@I gap_continuous_gate :: arch_class [d=2026-05-14 ok]
  => "Continuous top-K gate: weights[i] ∈ [0,1] with sum=1. Per-prompt weights are smooth functions of input. Null permutation: shuffle category labels → re-evaluate. Because gate is CONTINUOUS, shuffled-input weights vary continuously with input → null KL ≈ signal KL → z stays low"

@I goal scope=routing_class_change :: arch_class [d=2026-05-14 ok]
  => "Different routing class where null permutation produces DIFFERENT distribution shape from signal. Hard discrete routes (one cell per prompt, learned via VQ/hash) vs soft continuous weights"

# ── §2 sub-direction ε1 — MoH (Mixture of Heads) ──────────

@D eps1_moh :: arch_class [d=2026-05-14 ok]
  |> Mixture of Heads (per-attention-head expert switching)
  => "Instead of routing at cell-pool level (post-block), route at ATTENTION HEAD level WITHIN block. n_head experts per layer × routing decides which heads activate. Per-prompt head pattern = anima persona signature. Reference: 'Mixture of Heads' / Switch-Transformer head-level variants"

@D eps1_advantage :: arch_class [d=2026-05-14 ok]
  |> theoretical advantage
  => "Head-level routing operates on FINER-grained substrate (n_head=8 per layer × n_layer=1-24 = up to 192 expert slots vs flat 64 cells). Larger expert space + per-head specialization = more degrees of freedom for category-conditional routing emergence"

@D eps1_cost :: arch_class [d=2026-05-14 ok]
  |> cost envelope
  => "$10-30 H100 single-seed (similar to direction (l) DDP). Implementation: fork attention module, add per-head gate. ~250 LoC mitosis_model fork"

# ── §3 sub-direction ε2 — Hash-route ───────────────────────

@D eps2_hash :: arch_class [d=2026-05-14 ok]
  |> Hash-based routing (Switch Transformer style)
  => "Replace learnable router with fixed hash function: cell_idx = hash(prompt_emb) mod n_cells. Per-input deterministic + label-free + completely sidesteps gradient-noise issue. Cell pool learns specialization via observed-input distribution, not learned routing"

@D eps2_a2_trap_diagnosis :: arch_class [d=2026-05-14 ok]
  |> §A2-trap behavior under hash
  => "Hash route is INPUT-DEPENDENT but LABEL-INDEPENDENT. Null permutation (shuffle category labels) doesn't change hash → routing unchanged. Real KL: prompts in same category have similar hash buckets (if hash respects embedding similarity). z structurally different from null"

@D eps2_risk :: arch_class [d=2026-05-14 ok]
  |> risk
  => "Hash may NOT preserve category structure if embedding doesn't separate categories. Need to verify: identity_probe 50 prompts × 5 cats → hash buckets correlate with categories? If random hash, no signal. Mitigation: learned hash (LSH variant) trained on supervised category labels (Principle #3 trade-off)"

@D eps2_cost :: arch_class [d=2026-05-14 ok]
  |> cost envelope
  => "$5-15 H100 single-seed. Simplest direction — just replace Linear router with hash function. ~50 LoC. fastest to verify"

# ── §4 sub-direction ε3 — VQ-VAE discrete latent ───────────

@D eps3_vqvae :: arch_class [d=2026-05-14 ok]
  |> Vector-Quantized discrete latent + cell routing
  => "Add VQ codebook between input embedding and cell pool. codebook[K=64] entries trained via VQ-VAE loss. Cell selection = nearest codebook entry index. Per-prompt routing = single discrete code (hard 1-hot). Null permutation behavior fundamentally different from continuous weights"

@D eps3_motivation :: arch_class [d=2026-05-14 ok]
  |> theoretical motivation
  => "VQ-VAE codebook gives 'concept-level' discrete representation. Code i = a learned semantic cluster. If 5 categories naturally cluster into 5+ codes, routing is structurally category-aware. Similar to direction γ (hierarchical) but via VQ instead of explicit 2-level"

@D eps3_cost :: arch_class [d=2026-05-14 ok]
  |> cost envelope
  => "$20-50 H100 — VQ-VAE codebook training + commit loss + cell routing. ~400 LoC fork. Most complex of ε sub-directions"

# ── §5 hypothesis common across ε sub-directions ───────────

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

@? risk_hash_quality :: arch_class [d=2026-05-14 ok]
  |> hash function quality
  => "ε2 hash success depends on hash respecting embedding similarity. Random projection (LSH) baseline may not separate categories. Need either learned hash (trade-off Principle #3 if labels seep) OR embedding-aware hash (clustering)"

@? risk_vq_collapse :: arch_class [d=2026-05-14 ok]
  |> VQ codebook collapse
  => "ε3 VQ-VAE known issue: codebook collapse where only few codes used. Mitigation: commit loss + codebook restart + EMA updates. Risk: collapsed VQ → routing degenerates to few-cell monopoly (same §A2 pattern reborn)"

@? risk_moh_breaks_mitosis :: arch_class [d=2026-05-14 ok]
  |> ε1 MoH × mitosis incompatibility
  => "MoH routes at head level within attention. v5-mitosis cell pool is post-attention block-level. Architecturally redundant — must choose: cell pool OR MoH, not both. ε1 essentially ABANDONS mitosis architecture → cond #4 (D4 mitosis live) may break. Worth checking conflict before fire"

@? risk_no_guarantee :: arch_class [d=2026-05-14 ok]
  |> fundamental uncertainty
  => "Discrete routing theory suggests escape but not guaranteed. PSCC §55 lesson: ALL 4 prior continuous variants converged to same z=1.5 ceiling. Discrete may have its OWN structural ceiling unknown. Empirical verification mandatory"

# ── §8 fire priority ───────────────────────────────────────

@D fire_priority_1 eps2_hash :: arch_class [d=2026-05-14 ok]
  |> ε2 hash-route FIRST
  => "Lowest cost ($5-15) + simplest impl (~50 LoC) + cleanest mitosis compat. If ε2 succeeds, MoE class can be partially salvaged via hash-routed variant. If fails, falsifies hash-route as escape from §A2-trap"

@D fire_priority_2 eps3_vqvae :: arch_class [d=2026-05-14 ok]
  |> ε3 VQ-VAE SECOND
  => "Moderate cost ($20-50) + complex impl + mitosis compat. Tests if learned-discrete (vs fixed hash) helps category structure emergence"

@D fire_priority_3 eps1_moh :: arch_class [d=2026-05-14 ok]
  |> ε1 MoH LAST
  => "Highest implementation scope + breaks mitosis architecture (cond #4 risk). Defer until ε2 + ε3 outcome known. Possibly skip if those falsify"

# ── §9 cost envelope ───────────────────────────────────────

@K eps_total_envelope = 1500+5000+3000 = 9500 ucents-cents :: arch_class [d=2026-05-14 ok]
  |> all 3 ε sub-directions
  => "$5-30 + $20-50 + $10-30 = $35-110 cumulative for full ε exploration. Aligned with STRICT-4A.step §4 direction ε estimate ($30-150)"

@K eps2_minimal_fire :: arch_class [d=2026-05-14 ok]
  |> minimum-viable-test
  => "$5 ε2 hash-route single-seed = sufficient signal/no-signal verdict. If z > 2.0: scale to multi-seed. If z < 1.0: falsify + carry to ε3 or direction γ"

# ── §10 implementation outline (ε2 hash-route) ─────────────

@D eps2_impl_step_1 :: arch_class [d=2026-05-14 ok]
  |> code change
  => "Modify TopKMoERouter in train_v5mitosis_cotrain_v3_routing.py: replace `gate_full = F.softmax(logits)` + topK with `cell_idx = hash(input_emb_pooled) mod n_cells; weights = one_hot(cell_idx)`. Hash = LSH random-projection or learned-cosine"

@D eps2_impl_step_2 :: arch_class [d=2026-05-14 ok]
  |> training loop
  => "Loss = CE only (no aux balance, no entropy reg — hash is deterministic). Cell pool weights still train via gradient on selected cell. Each batch produces one-hot routing → cell-specific gradient"

@D eps2_impl_step_3 :: arch_class [d=2026-05-14 ok]
  |> evaluation
  => "F-PERSONA-4a measurement on hash-routed model: per-prompt route = one-hot bucket. cat-mean weight = histogram of which buckets hit per category. KL on bucket-distribution + null permutation as before"

@D eps2_impl_step_4 :: arch_class [d=2026-05-14 ok]
  |> data + dispatch
  => "Reuse anima_v5mitosis_cotrain_2026_05_12 corpus + dispatch_h100_v3_routing.sh with HASH_ROUTE=1 env override (additional dispatch arg)"

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

# ── §12 cross-link ─────────────────────────────────────────

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
