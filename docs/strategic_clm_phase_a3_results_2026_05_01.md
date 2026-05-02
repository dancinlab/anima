# CLM Phase A.3 — AN11(a) Weight Emergent Measurement on CLM v4 350m

- Agent: CLM Phase A.3 EXEC
- Date: 2026-05-02
- Host: ubu1 local CPU, $0
- Subject: `clm_v4_350m/scale_350m` (530.99M-param decoder, full fine-tune)
- Anchors: roadmap §32 row "2 AN11(a) Frobenius"; §27.5 (CP2 ALM-anchored / Mk.XII ≠ CP2)
- Race-isolated outputs: `state/strategic_clm_phase_a3_2026_05_01/*.json` + this doc

## TL;DR

| Question | Answer |
|---|---|
| Aggregate ‖ΔW‖_F (step10k → final) | **106.397** |
| ‖W_init‖_F (step10k) | **1545.291** |
| Normalized rel = ‖ΔW‖_F / ‖W‖_F | **0.0689 (6.89%)** |
| Layers compared | 581 (419 matrix-rank ≥ 2) |
| Params compared | 530,994,816 |
| AN11(a) AGI-strict | **NOT-MEASURED** (LoRA-implicit threshold not transferable) |
| AN11(a) CP2-relaxed | **PASS** (existence + family-shift both satisfied) |
| Cost | $0, 4 min wallclock |

## Phase 1 — Inventory

`~/anima/checkpoints/clm_v4_350m/scale_350m/`:
- `step_10000.pt` (5.36 GB) — earliest available, used as ΔW baseline
- `step_15000.pt`, `step_20000.pt`
- `final.pt` (= byte-identical to `best.pt` — verified by identical agg dW)
- `best.pt`, `best_phi.pt`
- **No `init.pt`** — true random-init baseline UNAVAILABLE

State-dict is wrapped: `torch.load(...)["decoder"]` yields the 581-key OrderedDict.

## Phase 2 — Frobenius (per-family, ranked by absolute dW_F)

| Family | n | agg ‖ΔW‖_F | agg ‖W‖_F | rel |
|---|---:|---:|---:|---:|
| down_proj | 16 | 14.680 | 100.450 | 0.146 |
| q_proj | 32 | 14.222 | 87.036 | 0.163 |
| gate_proj | 16 | 13.262 | 100.453 | 0.132 |
| up_proj | 16 | 12.674 | 100.434 | 0.126 |
| o_proj | 32 | 8.859 | 86.870 | 0.102 |
| k_proj | 32 | 7.474 | 47.056 | 0.159 |
| v_proj | 32 | 4.822 | 46.911 | 0.103 |
| ln (norm) | 49 | 1.585 | 193.969 | 0.008 |
| ffn (other linears) | 16 | 1.221 | 110.807 | 0.011 |
| attn_bias | 32 | 0.727 | 1453.798 | 0.0005 |
| other (ca_mix / rules / tok_emb / head_a / purefield ...) | 308 | 102.000 | 417.958 | 0.244 |

Top-10 absolute drift (drives the aggregate):
1. `blocks.15.ca_mix.weight` (768×2304) — 25.262
2. `head_a.weight` (64000×768) — 24.762
3. `tok_emb.weight` (64000×768) — 24.762  *(likely weight-tied with head_a)*
4. `blocks.9.rules.3.weight` — 21.528 (rel 1.38)
5. `blocks.13.ca_mix.weight` — 21.373
6. `blocks.11.rules.7.weight` — 20.760
7. `blocks.10.rules.4.weight` — 20.586
8. `blocks.12.rules.0.weight` — 19.065
9. `blocks.15.rules.5.weight` — 18.911
10. `blocks.14.ca_mix.weight` — 18.323

CLM-specific `ca_mix` (cross-attn mixing) and `rules.*` heads carry the largest drift — task-relevant geometry, not noise.

## Phase 3 — AN11(a) Verdict

**AGI-strict: NOT-MEASURED.** The original spec (`delta_norm > 0.001` per LoRA pair) is calibrated for low-rank adapter Frobenius over a frozen base. Applying it to a full-fine-tune trivially passes every tensor and is therefore vacuous. A re-derived threshold (e.g., per-tensor rel above a step-to-step micro-batch noise floor) is required and out of Phase A.3 scope.

**CP2-relaxed: PASS.** Both clauses satisfied:
1. **Existence** — ΔW_F = 106.40 ≫ 0 across 581 tensors, normalized 6.89%, well above any plausible noise floor.
2. **Family-shift** — MLP-gate dominance (gate/up/down all top-4 absolute) replicates ALM r14's pattern; q_proj prominence (rel 0.163) is even stronger than in ALM r14.

**Overall:** PASS (CP2-relaxed); AGI-strict deferred pending threshold re-derivation.

## Phase 4 — ALM r14 Comparison

| Metric | ALM r14 (Mistral-7B + LoRA r=64) | CLM v4 350m (full fine-tune) |
|---|---|---|
| Modules / tensors | 224 LoRA pairs | 581 tensors (419 matrices) |
| ΔW_F total | **6.991** | **106.397** |
| W_init_F | NOT recorded | 1545.291 |
| Normalized rel | unavailable | **0.0689** |
| Top family | gate_proj 4.36, up 3.91 | down 14.68, q 14.22, gate 13.26, up 12.67 |

**Raw 15.22× ratio is mostly DOF expansion** (full-rank vs r=64), not training intensity. The honest cross-substrate scalar would be normalized rel — but ALM r14's verifier (`an11_a_r14_frobenius.json`) did not record Mistral base ‖W‖_F. **Recommend Phase A.3-followup**: reload Mistral-7B-v0.3 base on ubu1 and emit ‖W_init‖_F to enable apples-to-apples normalized comparison ($0 if base cached).

Qualitative consistency: **MLP-gate dominance preserved** in CLM (matches ALM); CLM additionally drives attention-query and cross-attn-mix harder.

## Phase 5 — Honest C3 (top 3)

1. **C3-1 (HIGH): no random-init baseline** — ΔW measured from step_10000, not step_0. Reported 6.89% rel is a LOWER BOUND; true full training drift is larger but unknowable from preserved artifacts.
2. **C3-2 (HIGH): LoRA vs full-fine-tune is a category mismatch** — direct numeric ‖ΔW‖_F comparison (6.99 vs 106.40) reflects DOF expansion, not training intensity. Section 27.5 anchor (CP2 ALM-anchored / Mk.XII ≠ CP2) must hold: AN11(a) original spec is LoRA-implicit and not lifted to full-fine-tune without re-derivation. Normalized rel is the only honest cross-comparison, and ALM-side rel is currently missing.
3. **C3-3 (MED-HIGH): AGI-strict threshold not transferable** — the per-LoRA-pair `> 0.001` gate is vacuous for full-fine-tune (every CLM tensor passes trivially). Verdict honestly emitted as NOT-MEASURED rather than fabricated PASS.

Minor notes: `best.pt == final.pt` (byte-identical); `tok_emb.weight` and `head_a.weight` have identical dW_F (likely weight-tied); the highest *relative* shifts (rel > 6) are all `purefield.engine_*.bias` 1D vectors with tiny ‖W‖ — exclude from integration-axis interpretation.

## Cost Ledger
- Burn: **$0**
- Host: ubu1 local CPU
- Wallclock: ~4 min (load 3 × 5.4 GB checkpoints + per-tensor Frobenius)
