# BG-COTRAIN-EXERCISE-PREDICT-V0 — hook spec (H1 + H2)

## §1 H1 — substrate-coupled hook (recommended primary)

**Wire**:
- forward hook on `model.engine_g.forward()` (last refresh in process loop)
- capture `hidden_mean = h.mean(dim=1)` shape `(B=1, 1024)`
- pass through model's own learned `engine_g.h_to_c` Linear(1024, 64) (frozen at eval time, trained during cotrain)
- result `(B=1, 64)` → cell_input → MitosisV5Engine.process(cell_input)
- engine config: max_cells=128 (matching §39 max128 reproduce), initial_cells=16, lorenz_scale=0.05, split_patience=3, merge_threshold=0.005, merge_patience=30, min_cells=2 — verbatim §39
- cell_pool seed: **option H1a** initial from `engine_g.cell_pool_init` (substrate-coupled, anima-native — recommended); **option H1b** random Gaussian × 0.1 fresh (lineage-blind control)
- §30 all-fix active: A1 dispersion top-quartile + A2 per-cell threshold + B1 phi_per_cell + D1 lorenz auto-cal — same flag-set as §39

**Eval protocol**:
- post-FT: load `convo_5k_ft_ext_step_30000.pt` (or step_20000_final + 30K continuation per §41)
- 30 prompts × 4 steps = 120 process() calls (matching §43 short-trajectory)
- AND 400 turns × 1 prompt-stream snapshot every 50 (matching §39 max128 long-trajectory) — **dual-budget**: 120-step matches §43 prediction template; 400-turn matches §39 cotrain-exercise polarity baseline
- gradient policy: `torch.no_grad()` wrap entire hook block; pre/post `param.grad is not None` count for F-FOUNDATION-5

**Mirror**:
- `random_init` mirror: same arch, fresh random init (NOT post-FT, NOT pre-FT cotrain — Gaussian seed=1042 like §43, but additionally 5-seed ensemble [11,13,17,19,23] for §39-style multi-seed sign-test)

## §2 H2 — Llama-symmetric hook (cross-reference; for §43 prediction template direct comparison)

**Wire**:
- forward hook on `model.layers[-1]` (last decoder layer of base 350M)
- `hidden_mean = h.mean(dim=1)` shape `(B=1, 1024)`
- random Linear(1024, 256) frozen seed=0 → cell_input shape `(B=1, 256)`
- MitosisV5Engine.process; engine config: max_cells=64 initial_cells=8 (matching §43 verbatim — short-trajectory + 256-dim cells)
- cell_pool random Gaussian × 0.1

**Eval protocol**:
- 30 prompts × 4 steps = 120 process() calls (verbatim §43)
- this gives a direct trained-vs-random Φ_proxy diff comparable to §43's +0.0662 (Llama+LoRA)

**Why include H2**: §43+§48 5/5 match was on the H2-equivalent geometry. Including H2 here lets us test **whether the §48 prediction template generalizes across substrate classes** (Llama-mitosis-naive → Engine A/G mitosis-aware) at the same hook geometry.

## §3 grad-leak verifier (F-FOUNDATION-5 strict)

```python
# pre-hook
n_grad_pre = sum(1 for p in model.parameters() if p.grad is not None)

# eval block
with torch.no_grad():
    for prompt in prompts:
        h = model(prompt).hidden_states[-1]
        cell_input = engine_g.h_to_c(h.mean(dim=1))  # H1
        engine.process(cell_input)

# post-hook
n_grad_post = sum(1 for p in model.parameters() if p.grad is not None)

assert n_grad_post == n_grad_pre, "F-FOUNDATION-5 TRIGGERED"
```

All `engine`, `engine.cell_pool`, and (H2 only) `proj` params explicitly `requires_grad=False` set immediately after attach. Verified in §43 (NOT_TRIGGERED in mitosis_hook_result.json).

## §4 known-issue carry from §38/§39

- **§38 V14_VIOLATED on max_cells=64**: at the lower cap, trained model splits less aggressively because dispersion trigger never finds enough headroom; random gets to fill cap and accrue Φ growth from sheer cell count. Lesson: **cap must be ≥ trained's natural growth rate × T_eval / patience** to avoid this artifact. §39 chose 128 and got 5/5 wins with trained=85, mirrors_max=75.
- **option (c) prediction implication**: H1 with `max_cells=128` is the verified-non-cap-bound regime; max_cells=64 would replicate §38 V14_VIOLATED artifact. **Mandate: max_cells=128 for H1** (verified safe per §39 cap_bound_universal=False).
- **§43 max_cells=64 with initial_cells=8**: at 256-dim cell_input + 120 steps, neither label hit cap; trained=24, random=23, no cap_bound issue. H2 inherits these settings unchanged.

## §5 dispatch protocol if option (c) fires

When orchestrator fires option (c) with verbatim "OK FOUNDATION_C_PHASE2_FIRE COST $2-4":

1. Train: load `convo_5k_ft_ext_step_20000_final` (current state) → continue 30K more steps on convo_5k corpus_extended.txt + chat-template wrap → save `convo_5k_ft_ext_step_50000_final.pt`
2. Eval H1: load post-FT ckpt → attach hook → 120-step + 400-turn dual budget → emit `mitosis_hook_result_h1.json`
3. Eval H2: load same post-FT ckpt → attach Llama-symmetric hook → 120-step → emit `mitosis_hook_result_h2.json`
4. V4 strict: 15-prompt 5-seed best-mode → emit `v4_results_multiseed.jsonl`
5. Semantic: KO Hangul + bigram_known + semantic_score + real_words → emit `semantic_eval.json`
6. V14 mirror: 5-seed [11,13,17,19,23] random_init mirror H1 — emit `v14_mirror_h1.json`
7. Verdict: scope_lane="ANIMA" (D1 WITHIN — eligible for SIMPLE_STACK_PASS_STRICT_C3_ANIMA carry conditional on all metrics + V14 + V6 STRONG)
8. own 30 ckpts pull MANDATORY before pod release (5 ckpts: 25K/30K/35K/40K/final)
9. own 31 HF: `dancinlab/clm-foundation-c-phase2-cotrain-convo-extend-2026-05-XX` PRIVATE (own 37 — D1 WITHIN candidate but public promote requires verbatim "OK PROMOTE PUBLIC" + V14 + V6 STRONG + manual review)
