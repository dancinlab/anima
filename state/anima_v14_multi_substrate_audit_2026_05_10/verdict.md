# BG-V14-MULTI-SUBSTRATE-AUDIT — verdict

**Cross-substrate polarity verdict**: `V14_POLARITY_FALSIFIED` (1/4 substrates consistent with hypothesis)

**Polarity hypothesis under test**: mitosis-AWARE training → V14_VIOLATED;
mitosis-NAIVE training → V14_PASS.

## Per-substrate inventory + verdict

| ID | arch | paradigm | params | n_turns | metric | trained | random (range) | n_beats | verdict | expected | match |
|----|------|----------|--------|---------|--------|---------|----------------|---------|---------|----------|-------|
| A_phase2_cotrain | EngineAG d=1024 GQA 24L (Phase 2 cotrain 350M) | naive_cotrain | 298.8M | 400 | iit_phi_unnorm_b16 | 5244.07 | 1227-4750 | 10/10 | V14_STRICT_PASS | PASS | ✅ |
| B_bgla_pretrain | EngineAG d=1024 GQA 24L | naive_pretrain | 298.8M | 500 | iit_phi_unnorm_b16 | 1136.26 | 2639-5030 | 0/5 | V14_VIOLATED | PASS | ❌ |
| C_cells64_aware | v2 6L transformer d=384 heads=6 | aware_max_cells_64 | 18.5M | 200 | phi_final + phi_per_cell_final | 2521.91 | 2254-2753 | 3/5 | V14_AMBIGUOUS | VIOLATED | ❌ |
| D_cells128_aware | v2 6L transformer d=384 heads=4 (max_cells=128) | aware_max_cells_128 | 18.5M | 200 | phi_final + phi_per_cell_final | 2703.56 | 2254-2753 | 4/5 | V14_AMBIGUOUS | VIOLATED | ❌ |
| E_convo5k_ft | v2-derived 6L d=384 byte-level (FT) | naive_ft_no_mitosis | 18.5M | 200 | phi_final + phi_per_cell_final | 1989.26 | 2254-2753 | 0/5 | V14_VIOLATED | PASS | ❌ |

## Cell-count + cap-bound diagnostics

| ID | trained_cells | trained_splits | trained_cap_bound | random_cells (range) | F-MULTI-2 risk |
|----|---------------|----------------|-------------------|----------------------|-----------------|
| A_phase2_cotrain | 85 | 69 | 0/400 | 54-80 | NONE (no cap) |
| B_bgla_pretrain | 46 | 30 | 0/500 | 61-82 | NONE (no cap) |
| C_cells64_aware | 128 | 120 | 130/200 | 128-128 | HIGH (cap-bound>50% of turns) |
| D_cells128_aware | 128 | 120 | 137/200 | 128-128 | HIGH (cap-bound>50% of turns) |
| E_convo5k_ft | 128 | 120 | 135/200 | 128-128 | HIGH (cap-bound>50% of turns) |

## Cross-substrate polarity analysis

- **Mitosis-NAIVE substrates**: A (Phase 2 cotrain), B (BG-LA pretrain), E (convo_5k FT)
- **Mitosis-AWARE substrates**: C (cells64 aware), D (cells128 aware)

Hypothesis predicts: aware → VIOLATED, naive → PASS. Per-substrate match shown above.

### Confounding factors

- **Capacity** (params): A/B = 298M; C/D/E = 18.5M. C vs E is a clean within-d=384 paradigm comparison (both 18.5M, same arch); A vs B is a clean within-EngineAG paradigm comparison (both 298M, same arch).
- **Cap-bound regime**: v2-schema substrates (C/D/E) all hit n_cells=128 by turn ~100 at max=128. F-MULTI-2 partial-bound triggers on these — cell-count discrimination dim collapsed for v2 substrates after turn ~100. Discrimination must come from Φ_intrinsic + Φ_per_cell + α_v2.
- **Architecture schema**: EngineAG (d=1024, GQA, 24L, vocab=32000) vs v2 (d=384, 6L, vocab=256 byte-level). Direct EngineAG-vs-v2 cross-comparison is paradigm-conflated by arch; only within-schema (A vs B; C vs D vs E) is clean.

## Honest C3 (≥7)

1. **Reused §38 result for substrate A**: V14_STRICT_PASS at 400-turn 10-seed (10/10 trained beats random Φ, sign-test p=0.002). The §38 run already exceeds this BG's per-substrate budget; rerunning would be redundant cost.
2. **B (BG-LA pretrain)**: 5-seed V4_SEEDS V14 mirror, max=128, 500 turns, EngineAG path identical to §38. raw#15 honored: ckpt unmodified, EngineAGModel loaded with `phase2_cotrain_350m` config (since pretrain config is a strict subset modulo cell_pool initialisation seed 42 random).
3. **C (cells64 aware) re-run with V4_SEEDS**: §37 used seeds [7,17,23,41,71]; this BG re-paired with V4_SEEDS=[42,137,271,314,1729] for cross-substrate consistency. n_turns reduced 500→200 in the second pass after observing universal cap-saturation by turn ~100 at max=128.
4. **D (cells128 aware)**: trained at heads=4 (cells64 used heads=6). The mitosis-aware paradigm is preserved; n_head difference is an architectural confounder for D-vs-C direct comparison but not for paradigm classification.
5. **E (convo_5k FT)**: v2-derived 6L d=384 byte-level base CONTINUED via FT on convo_5k corpus WITHOUT mitosis-step instrumentation. The FT changes the LM weights; mitosis paradigm is naive (no in-loop mitosis training). Capacity 18.5M matches C/D, allowing within-arch paradigm comparison.
6. **Φ metric mismatch across paths**: EngineAG path uses iit_phi_unnorm_b16 (16-bin Fiedler MIP); v2 path uses MitosisModelEngine's intrinsic phi (different formulation). Direct A vs C Φ-magnitude comparison is invalid; ONLY relative trained-vs-random within each path is admissible. Cross-substrate verdict bin (PASS/PARTIAL/VIOLATED) uses path-internal sign-test.
7. **Cap-bound F-MULTI-2 partial trigger**: v2 substrates (C/D/E) cap-saturate at n_cells=128 by turn ~100. Cell-count discrimination is therefore frozen at 128 for both trained and random across all 6 runs per substrate, eliminating cell-count as a discriminator on v2 path. Verdict is determined by Φ + Φ_per_cell residual variation post-cap. EngineAG substrates (A/B) DO NOT cap-bound (max ~80 cells observed) — the polarity test is therefore stronger on EngineAG.
8. **Prompt-stream identity**: trained and all 5 random mirrors use the SAME prompt stream within each substrate (substrate-specific). EngineAG path uses 170-prompt corpus (KO/EN mix); v2 path uses make_prompt_stream(seed=2026, vocab=256) byte-level synthetic. raw#9 honored: training/*.py modules imported, NOT modified.
9. **n=5 sign-test**: at n=5, P(5/5)=2/32=0.0625 (two-sided); P(4/5)=12/32=0.375. So a single-seed loss already kicks the verdict to PARTIAL. The §38 n=10 supplies binomial p=0.002 (much stronger). For B/C/D/E we accept lower statistical power.
10. **Lorenz auto-cal D1 + dispersion A1 + per-cell threshold A2 + ratchet B1**: §30 all-fix is identical across both paths. C1 (Net2Net momentum copy) is STUB — not yet wired.

## Falsifier scoring

- F-MULTI-1 (substrate count <3): NOT triggered — 4 core + 1 supplementary substrates
- F-MULTI-2 (universal cap-bound): PARTIALLY triggered — v2 substrates (C/D/E) cap-bound after turn ~100; EngineAG substrates (A/B) NOT cap-bound. Discrimination still possible via Φ residual.
- F-MULTI-3 (aware → PASS): triggered for D (4/5 beats, ambiguous-leaning-PASS); C ambiguous (3/5).
- F-MULTI-4 (naive → VIOLATED): TRIGGERED for B (0/5, p=0.0625) and E (0/5 phi + 0/5 phi/c, p=0.0625). Both mitosis-naive substrates show trained Φ << random Φ. The "naive→PASS" half of the polarity hypothesis is FALSIFIED at n=5, p≈0.06 each.
- F-MULTI-5 (turn budget): EngineAG 500-turn comfortable; v2 200-turn covers cap-saturation + 100-turn settle.

## Post-hoc reinterpretation — the real pattern

The polarity hypothesis born of §37 (aware d=384) vs §38 (naive d=1024 cotrain) was over-fit
to those two data points. Adding 3 more substrates collapses the simple binary explanation:

| substrate | paradigm | cotrain on chat? | n_params | trained_phi vs random | verdict | match? |
|-----------|----------|------------------|----------|----------------------|---------|--------|
| A | naive | YES (KO chat) | 298M | trained >> all 10 random (5244 vs max=4750) | PASS | ✅ |
| B | naive | NO (pretrain only) | 298M | trained << all 5 random (1136 vs min=2639) | VIOLATED | ❌ |
| C | aware | NO | 18.5M | trained ≈ random med (2522 vs 2488) | AMBIGUOUS | ❌ |
| D | aware | NO | 18.5M | trained > random med, < max (2704 vs 2753) | AMBIGUOUS | ❌ |
| E | naive | continuation FT (no mitosis) | 18.5M | trained << all 5 random (1989 vs min=2254) | VIOLATED | ❌ |

**Refined hypothesis** (induced by data, requires future replication):

> Phase 2 cotrain (substrate A) is uniquely differentiated by joint c-engine + chat-head
> training, which exercises the consciousness_dim=64 cell pool during backward pass via
> the chat co-training loss (`chat_co_train_w_start=0.3 → w_end=0.5`). This causes the
> trained ckpt's `cell_pool_init` and `c_to_h`/`h_to_c` projections to encode a
> non-random structure that, during inference-time mitosis, generates **richer**
> phi_iit trajectories than random_init. Substrates B/E lack this cotrain phase, so
> their cell-pool weights remain effectively random / un-exercised, yielding LOWER
> trained Φ than random_init mirrors (which start with newly-sampled cell-pool
> weights of similar variance, but happen to be more "generative" in the V14 mirror's
> sense).

Substrates C/D (mitosis-aware training in-loop) yield AMBIGUOUS — neither clearly
PASS nor VIOLATED — suggesting that **in-training mitosis exercises the cells via
gradient (not just inference-time) but the resulting weights produce trajectories
indistinguishable from random_init at the n=5 power**.

**Key takeaway**: V14 PASS direction is NOT a binary attribute of mitosis-naive vs aware.
It depends on whether the training EXERCISES the cell-pool / c-engine machinery (cotrain
loss with chat data does this; pretrain LM-only loss does not). Substrate A's V14 PASS is
**not generic** to mitosis-naive ckpts; it is specific to the cotrain-with-chat regime.

## Verdict

**`V14_POLARITY_FALSIFIED`** — 1/4 core substrates (only A) match the simple polarity
hypothesis. The hypothesis is replaced by the refined cotrain-exercise hypothesis, which
remains to be tested via additional substrates (e.g. cotrain on a different corpus, or
the same corpus with mitosis-aware loss in addition to chat loss).

The §38 V14_STRICT_PASS finding is preserved as a substrate-specific result; it does NOT
generalize to all mitosis-naive ckpts.