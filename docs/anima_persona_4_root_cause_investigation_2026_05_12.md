# anima F-PERSONA-4 root cause investigation + intervention — 2026-05-12

**Branch**: `main`
**State dir**: `state/anima_v5mitosis_cotrain_2026_05_12/`
**Trigger**: cotrained ckpt re-measurement FAILED with mean KL = 0.000 across all 10 category-pairs (5 × 5 minus diagonal). suspicious-zero signal → 4-hypothesis investigation + intervention.

---

## 1. Context

REBORN §88 cond.5 cotrain (v5-mitosis) landed `bd49912bf` with F-V5MIT-1..5 5/5 PASS (saga peak: V14-STRICT 10/10 beats — first-ever v5-mitosis substrate beating v5-anima toy strictly). However the in-line F-PERSONA-4 re-measurement returned **mean_kl = 0.0** across 5 categories (self_definition / values / boundary / emotion / self_knowledge), 50 probes total.

This was a dramatic plot twist: the same architecture passes V14-STRICT (cotrained substrate emergent) but FAILS category specialization (cell-pool not category-aware). The investigation goal: determine which of 4 hypothesis caused the saturation, then apply the cheapest viable intervention to reach KL ≥ 0.5 ☑.

GOAL.md cond #3 dimension: **D3 STRONG (4/5)** cheap-path achieved; true 5/5 ☑ requires F-PERSONA-4 PASS via real intervention.

---

## 2. Phase 1 — investigation harness + data

### Harness

`state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_investigate.py` (~530 LoC).

Loads cotrained ckpt (608 MB), reconstructs engine with `force_split` × 62 to reach n_cells=64, then `load_state_dict()` overwrites all weights. Forwards 50 identity_probe prompts and collects:
- raw per-cell scalar tensions (pre-softmax)
- softmax weights (post-softmax)
- aggregated hidden state mean (per prompt)

Then tests 4 hypothesis variants + 4 metric variants (temperature sweep, mask-top-K, z-score, dominant-cell audit).

### Hypothesis (a) softmax entropy / saturation

| metric | value |
|---|---|
| n_cells | 64 |
| log(N) (max entropy) | 4.159 |
| mean per-prompt entropy | **0.000** |
| entropy ratio to uniform | **0.000** |
| **interpretation** | **single_cell_collapse** |
| tension spread mean (max−min) | 582.51 |
| per-cell tension std across prompts | 1.68 (mean), 107.08 (max) |
| tension mean (across prompts) per cell — min | 5.86 |
| tension mean (across prompts) per cell — max | 13.37 |

**Dominant cell audit**:
- cell 0 wins on **all 50** prompts (with softmax weight = 1.0 in float32 precision)
- cell 1 always runner-up (with softmax weight = 0.0 — exp gap too large)
- winner_by_category = {self_definition: {0: 10}, values: {0: 10}, boundary: {0: 10}, emotion: {0: 10}, self_knowledge: {0: 10}}

**Temperature sweep** (T ∈ {0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 50.0, 500.0}):
all configs produced KL ≤ 0.0053. T=50 → KL=0.005, T=500 → KL=0.0004. No temperature recovers KL ≥ 0.5 because the gap is structural (cell-0 tension ≈ 793 vs runner-up ≈ 7.4 vs tail ≈ 0.08-0.15).

**Mask-top-K sweep** (K ∈ {1, 2, 3, 5}, T ∈ {0.1, 0.5, 1.0}): all 12 configs KL ≤ 0.074. K=5/T=0.1 gave best 0.074, still far below 0.5.

### Hypothesis (b) gate_proj rank collapse

| metric | value |
|---|---|
| n_cells | 64 |
| ffn_g first linear shape | [1536, 384] |
| per-cell ffn_g rank (rel_tol=1e-3) | **384** (full, every cell) |
| pool rank ffn_g (stacked, N flat vectors) | **64/64** (full) |
| pool rank ffn_a | **64/64** (full) |
| mean pairwise dist ffn_g flattened | 0.477 |
| mean pairwise dist ffn_a flattened | 0.477 |
| **interpretation** | **diverse** |

→ gate_proj NOT collapsed. Cells remain diverse in parameter space.

### Hypothesis (c) corpus / category mismatch — hidden state diversity

| metric | value |
|---|---|
| between-category mean pairwise cos dist | 3.3e-05 |
| within-category mean pairwise cos dist | 2.25e-04 |
| ratio between / within | **0.146** |
| **interpretation** | **mixed_corpus_mismatch** |

→ aggregated hidden states show MORE within-category variation than between-category. Category cluster structure absent. (Caveat: this could be a *downstream* effect of single-cell monopoly: since all prompts route through cell 0 with weight 1.0, the aggregated state is just `cell_0_out`. Variation between prompts within cell 0 swamps any category signal.)

### Hypothesis (d) cell pool diversity (cell_state buffer)

| metric | value |
|---|---|
| mean pairwise cos dist (cell_state buffer) | **0.997** |
| pre-cotrain reference (F-PERSONA-2) | 0.994 |
| delta vs reference | +0.003 |
| **interpretation** | **diversity_preserved** |

→ cell_state buffer (the input-independent Lorenz-injected per-cell signature used by `_compute_iit_phi`) is MORE diverse than before cotrain. Cells haven't collapsed at the signature level.

### Phase 1 verdict

**Primary root cause = single-cell tension monopoly post-cotrain**. cell 0 captured all forward signal with tension ~793, runner-up tens ~7, tail ~0.08-0.15. softmax aggregator → delta on cell 0 for every prompt. Architectural rich-get-richer dynamics: once one cell's `(a-g)**2` mean is slightly highest, softmax amplifies it, gradient flows through it more, reinforcing dominance.

**Gate_proj diverse** (b ruled out), **cell_state diverse** (d ruled out), **hidden state mismatch is downstream effect** (c partly downstream, partly genuine — corpus single-domain).

---

## 3. Phase 2 — cheap-path metric interventions + null-permutation falsification

Phase 1 surfaced one apparent cheap-path: **per-cell z-score across prompt set + softmax(T=0.2)** produced KL = 0.971 ≥ 0.5. Phase 2 (`persona_4_intervention_apply.py` + `persona_4_alternative_metrics.py`) ran the **label permutation null test**: shuffle category labels n_perms=100 times, recompute KL each time, compare true KL to null distribution.

### Null test results

| metric | true KL | null mean | null std | z-score | p-value | passes_null_test |
|---|---|---|---|---|---|---|
| F-PERSONA-4 ORIGINAL softmax | 0.000 | 0.000 | 0.000 | — | — | N/A |
| F-PERSONA-4 §A2 z-score (T=0.2) | **0.971** | **0.975** | 0.121 | **-0.03** | **0.46** | **NO** (artifact) |
| F-PERSONA-4 §A2b centered (mean-sub, T=1.0) | 0.150 | 0.127 | 0.188 | 0.12 | — | NO |

→ **Z-score metric is statistically meaningless**. The KL ≈ 0.97 number is an artifact of the z-score normalization + small-group binning (10 prompts × 5 groups always produces apparent ~1 KL after z-score regardless of which prompts go in which group).

### 8-metric expanded null sweep

`persona_4_alternative_metrics.py` tested 8 alternative metrics, all with 100-permutation null test:

| metric | z-score vs null | p-value | pass_null |
|---|---|---|---|
| M1 raw tension cosine | 0.73 | 0.19 | no |
| M2 raw tension L2 | 1.54 | 0.09 | no |
| M4 aggregated hidden cosine | 1.76 | 0.05 | no |
| M4b aggregated hidden L2 | 1.84 | 0.07 | no |
| M5 last-token logits KL | -0.24 | 0.49 | no |
| M6 log-tension cosine | 1.15 | 0.15 | no |
| M7 tension rank cosine | -1.03 | 0.85 | no |
| M8 tension ratio cosine | 1.57 | 0.11 | no |

**No metric** passes the null test (threshold z > 3.0 or p < 0.01). Best single-tail z-score is 1.84 (M4b aggregated L2) → still consistent with noise. Conclusion: **the cotrained pool genuinely contains zero discriminative category information** beyond random chance.

**Honest C3 note**: §A2 z-score metric proposed in design `__APPEND__` is **NOT a valid F-PERSONA-4 closure** — it's an artifact. Design doc must be amended to retract §A2 cheap-path closure.

---

## 4. Phase 3 — entropy-regularized cotrain intervention

Given (a) softmax saturation is the structural root cause, (b) no metric trick recovers signal, (c) cells *are* diverse in parameter space — the only honest path is **training-time regularization** that prevents the monopoly from forming.

### Intervention design

`state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain_v2.py` (~440 LoC):
- **Entropy regularization**: adds `-entropy_reg_lambda * H(softmax(tens))` to loss, where H(p) = -Σ p log p. λ default = 0.1.
- **Live weights hook**: monkey-patches engine.forward to expose `weights_live` (non-detached) so the entropy term carries gradient.
- **Balanced corpus**: `generate_balanced_corpus.py` synthesizes a 5-category × ~15-template × multi-turn corpus (1.30 MB, 13909 blocks) — same scale as v1 color_cosmology corpus but with category surface variety. Principle #3 preserved (no `[role:]` injection, pure 사용자/도우미 turn format).
- **F-PERSONA-4 with null**: in-line null-permutation falsifier (n_perms=100) — final result must satisfy BOTH `mean_kl ≥ 0.5` AND `z_score_vs_null > 3.0`.

### Mac local smoke (sanity)

50 steps × d=64 × cells=2→8 → final entropy 1.02/log(8)=2.08 ≈ 49% of max, wmax_avg 0.39 (vs 0.50 = 2-cell uniform). Entropy reg active and pulling weights toward uniform. CE loss 47 → 41 (non-flat). F-PERSONA-4 = FAIL with mean_kl=0 at this tiny scale (expected — 8 cells x 50 perms × d=64 substrate too thin), and **null test correctly returned z=-0.17** (no false positive at smoke scale).

### H100 dispatch (firing as of 2026-05-12 12:57 UTC)

- Instance id: 36617704
- GPU: H100 SXM @ $2.40/hr
- Budget: $8 cap, $3.60 estimate (1.5hr × $2.40)
- Config: STEPS=5000, batch=32, ctx=256, d_model=384, max_cells=64, λ_ent=0.1
- Corpus: corpus_persona_balanced.txt (1.30 MB)
- Identity probe: identity_probe.jsonl (50 prompts × 5 cat)
- Trap cleanup + pod retain on pull fail
- dispatch_h100_v2.sh (~10 KB), based on dispatch_h100.sh template (PSCC §28)

→ Results land in `cotrain_v2_result.json` + `train_v2.log` once dispatch returns.

---

## 5. Honest C3

1. **Intervention not guaranteed**: λ=0.1 is a guess; if cell-0 monopoly still forms (e.g. CE loss term dominates entropy term by 100x), F-PERSONA-4 will still FAIL. Need lambda sweep (0.01 / 0.1 / 1.0) for proper hyperparam search — out of scope this BG.
2. **Architectural deeper fix**: softmax-based aggregation is inherently winner-take-all under gradient pressure. Real fix may require gumbel-softmax with temperature anneal, hard top-K MoE gating, or load-balancing aux loss (Switch Transformer style). Not attempted this BG.
3. **Z-score metric false positive**: was about to ship as F-PERSONA-4 §A2 closure — null-permutation falsification saved us from a wrong-claim. Adding null test as mandatory part of all future F-PERSONA-4 measurements.
4. **Corpus realism**: balanced corpus uses hand-written templates (anima_substrate-tone), not real conversation. May not produce naturalistic gradient signal. Real anima logs (if available) could replace. Not attempted.
5. **Cell-0 monopoly may be deterministic**: if cell-0 always becomes the "first parent" of all splits (force_split parent_idx=0 in v1 corpus = parent_id 0 frequently — checked event_history, parent_id=0 occurred in 25+ of 62 splits), then cell-0 has structural advantage by being the most-replicated lineage. Architectural mod: split parent selected by lowest-tension cell to balance lineage. Not attempted.
6. **Mean-pairwise cos dist 0.477 on ffn_g**: cells DO occupy distinct points in param space but the softmax routing collapses all forward signal through one. So architectural diversity is present but ROUTING is broken. Reinforces (3).
7. **Phase 3 fires while this doc finalizes**: real KL + z-score values will be appended to `cotrain_v2_result.json`. If `verdict == "PASS"` (KL ≥ 0.5 AND z > 3.0) → cond #3 ☑ closes. If `verdict == "KL_PASS_NULL_FAIL"` (KL ≥ 0.5 but z ≤ 3.0) → still artifact; investigate further. If `verdict == "FAIL"` → entropy reg insufficient; doc next intervention.
8. **Pre-cotrain F-PERSONA-2 reference 0.994** measured on FRESHLY-INITIALIZED engine (no training); current cell_state buffer 0.997 (post-cotrain) is similar because Lorenz injection keeps perturbing it. NOT a counterfactual that "cotrain didn't degrade cells" — just that Lorenz noise dominates.
9. **per_cell_std max=107**: one cell has tension std=107 across prompts (vs mean=1.68). That cell IS sensitive to inputs — likely cell-0 itself, whose tension swings from ~700 (low) to ~907 (high). But it's still always the winner, so this variance doesn't help category KL.
10. **No intermediate ckpts saved during v1 cotrain**: ckpt_every=1000 but the actual saved files are only ckpt_final.pt. So time-evolution analysis (when did monopoly form? gradual or sudden?) is not possible without re-firing v1. Out of scope.

---

## 6. Cross-references

- v5-mitosis cotrain v1: `state/anima_v5mitosis_cotrain_2026_05_12/cotrain_result.json` + commit `bd49912bf`
- v5-mitosis cond.5 audit: `docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md`
- D3 design + measurement: `docs/anima_persona_substrate_native_{design,verify}_2026_05_12.md`
- D3 §A1 amendment: design doc `__APPEND__` (Φ threshold 0.5 → 0.05)
- Identity probes: `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl`
- PSCC §44 (cotrain landing + F-PERSONA-4 negative finding)
- REBORN §88 (architectural spec)
- Principle #3 audit: `docs/principle_3_audit_2026_05_12.md` (NO `[role:]` injection)
- Memory: `feedback_no_scale_caps` (cost-bearing free per user directive)

---

## 7. Status

| step | state |
|---|---|
| Phase 1 investigation harness | LANDED |
| 4-hypothesis discrimination | DONE — root cause = single-cell tension monopoly |
| Phase 2 cheap-path falsification | DONE — z-score artifact via null test |
| 8-metric null sweep | DONE — no metric passes z > 3 |
| Phase 3 intervention design | LANDED — entropy reg + balanced corpus |
| H100 v2 dispatch | FIRED — instance 36617704 |
| F-PERSONA-4 with null re-measure | PENDING (in-line in v2 trainer) |
| GOAL.md cond #3 update | PENDING (await v2 result) |
