# Emerge Candidate F — F-CAND-F-1-v2 rule_outputs cosine pairwise probe spec (2026-05-05)

Spec for the v2 falsifier extension of emerge candidate F (CA-rule cells × 5-axis vote). Closes the C2 mode (c) gap explicitly deferred by the v1 spec: detection of `rule_outputs` convergence collapse where 8 rule cells emit different `rule_logits` (so v1's flatten-std and max-row-std checks PASS) but produce near-identical `rule_outputs` vectors (effective rules = 1). This document is **doc + spec only**: zero source change, zero retrain, zero new helper Python file, zero commit. Read-only on `ready/models/conscious_decoder.py:466,499-503,538-542`.

Lineage:

- `docs/anima_emerge_candidate_f_ca_rule_5axis_vote_spec_2026_05_05.md` (BG-H land — F-CAND-F-1 v1 spec) — §7 C2 explicitly defers mode (c) detection: "F-CAND-F-1 detects (a) and (b) but NOT (c) — for (c), `rule_probs` variance is high but content variance is zero. A v2 falsifier would compare per-rule output `r(ca_out)` cosine pairwise; out-of-scope for Stage 1."
- `ready/models/conscious_decoder.py:466,499-503,538-542` — CA-rule cells implementation: `n_ca_rules=8`, `rule_weights = nn.Linear(d_model, 8)`, `rules = nn.ModuleList([nn.Linear(d_model, d_model, bias=False) for _ in range(8)])`, forward stacks `rule_outputs = torch.stack([r(ca_out) for r in self.rules], dim=2)` into shape `[B, T, 8, D]`.
- `state/anima_axis_eval_set_2026_05_05/prompts.jsonl` (5×20 = 100 axis-bucket eval prompts) — neutral 5-prompt subset reused for v2 validation.

---

## §1 Concept — three CA-rule collapse modes

<!-- [Hc_015 ca-rule-convergence-collapse — moved to hypotheses_candidates/Hc_015_ca_rule_convergence_collapse.md on 2026-05-11] -->

---

## §2 F-CAND-F-1-v2 falsifier definition (3-state)

### §2.1 Captured tensor

Per-block, after forward, the helper captures `rule_outputs` of shape `[B, T, 8, D]` from each of the 16 `DecoderBlockV2` instances. The capture uses a forward hook on each block's `nn.ModuleList` `rules` (or, equivalently, on the `meta_ca_out` computation site by intercepting `rule_outputs` before the `* rule_probs.unsqueeze(-1)` multiply). v2 reduces:

```text
rule_outputs[B, T, 8, D]
  → mean over (B, T)        → per-block per-rule vector  [8, D]
  → cosine pairwise          → per-block similarity matrix [8, 8]
```

For 16 blocks, the helper emits a stack `cosine_pairwise_per_block` of shape `[16, 8, 8]`. v2 falsifier reads this stack.

### §2.2 Pairwise cosine compute

Per block (D = d_model, fp32):

```python
# rule_outputs_mean: [8, D]
norm = rule_outputs_mean / (rule_outputs_mean.norm(dim=-1, keepdim=True) + 1e-9)  # [8, D]
cos_matrix = norm @ norm.T                                                         # [8, 8]
# diagonal == 1.0 by construction; off-diagonal = pairwise cosine
```

Off-diagonal aggregates per block:

```python
# off_diag_mean: scalar
off_diag_sum  = cos_matrix.sum() - cos_matrix.diag().sum()
off_diag_mean = off_diag_sum / (8 * 7)        # 56 ordered off-diagonal entries → 56 / 56 normalization
off_diag_max  = cos_matrix.fill_diagonal_(-inf).max()  # pairwise max (i ≠ j)
```

Aggregate across 16 blocks:

```python
mean_off_diag_mean   = mean(off_diag_mean over 16 blocks)
mean_off_diag_max    = mean(off_diag_max  over 16 blocks)
worst_block_off_diag = max(off_diag_max   over 16 blocks)
```

### §2.3 PASS / FAIL_TRUE / FAIL_FALSE criteria

**Statement:** Under `mode=auto` on a neutral prompt set (5 prompts from `state/anima_axis_eval_set_2026_05_05/prompts.jsonl`, one per axis), the captured per-block `rule_outputs` cosine pairwise matrices `[16, 8, 8]` MUST satisfy BOTH:

- (i) **off-diagonal mean cosine** — across all 16 blocks, the mean of the 56 off-diagonal entries averaged across blocks: `mean_off_diag_mean ≤ 0.7`. Interpreted as: on average, each pair of rule outputs has cosine similarity ≤ 0.7 (≥ 45.6° angle).
- (ii) **off-diagonal max cosine (per block)** — for EVERY block, no single off-diagonal entry exceeds 0.85: `worst_block_off_diag ≤ 0.85`. Interpreted as: no two rules within any block are near-identical.

**PASS:** (i) AND (ii) both hold across all 5 prompts (or, per-prompt PASS rate ≥ 4 of 5 — matching v1 F-CAND-F-3 prompt-pass-count semantics).

**FAIL_TRUE:** (i) violated (`mean_off_diag_mean > 0.7`) OR (ii) violated (`worst_block_off_diag > 0.85`) on ≥ 2 of 5 prompts → rule_outputs convergence collapse confirmed. The 8-cell META-CA mechanism is content-collapsed; even if `rule_probs` selector varies, the selected rules produce near-identical content. Implication for emerge candidate F: the v2 vote-matrix [8, 5] is rank-1 in CONTENT space regardless of routing-space variance; cell-level "axis specialization" framing is hollow. Cell `i` and cell `j` may receive different selector mass but emit the same vector — the user-visible `ca_consensus_axis` is determined by an arbitrary `P` projection on a content-degenerate substrate. CLM v5 redesign should split rules either by topology (different subnet shapes per rule) or by hard mixture-of-experts gating that prevents weight convergence during training.

**FAIL_FALSE:** hook capture returns NaN / inf / empty dict / shape mismatch on any layer; OR `rule_outputs_mean.norm` < 1e-6 on any block (degenerate zero output, cosine undefined); OR fewer than 16 blocks captured → measurement pipeline crash, falsifier deferred.

### §2.4 Cascade with v1 F-CAND-F-1

v2 is CONDITIONED on v1 PASS. If v1 reports FAIL_TRUE (mode (a) or (b)), v2 cascade-defers because `rule_outputs` mean over a uniform or single-winner `rule_probs` distribution becomes ill-conditioned for the convergence framing. Reporting precedence:

1. v1 FAIL_TRUE → v2 emits `state: "DEFERRED_V1_FAIL_TRUE"`, `cosine_data: null`.
2. v1 FAIL_FALSE → v2 emits `state: "DEFERRED_V1_FAIL_FALSE"`, `cosine_data: null`.
3. v1 PASS → v2 evaluates per §2.3 and emits PASS / FAIL_TRUE / FAIL_FALSE with full cosine data.

This cascade is symmetric to v1 F-CAND-F-3's deferral when F-CAND-F-1 fails.

---

## §3 Hypothesis + 4 scenarios + gate_strength implication

### §3.1 4 scenarios

Predicted `mean_off_diag_mean` distribution over 16 blocks under different training pathologies:

| scenario | mean_off_diag_mean | per-block max cosine | F-1-v2 verdict | substrate state |
|---|---|---|---|---|
| **healthy** | ≈ 0.0 to 0.3 | ≤ 0.5 | PASS | 8 rules learned 8 distinct transformations; META-CA architecturally functional |
| **mild collapse** | ≈ 0.4 to 0.6 | 0.6 to 0.75 | PASS (borderline) or ambiguous | 2-3 rule clusters; effective rules ≈ 3-5 — function preserved with some redundancy |
| **strong collapse** | ≈ 0.7 to 0.85 | 0.8 to 0.9 | FAIL_TRUE | rules near-identical with scale/direction perturbation; effective rules ≈ 1-2 — META-CA architecturally vestigial |
| **complete collapse** | ≈ 0.85 to 1.0 | ≥ 0.9 | FAIL_TRUE | 8 W_i indistinguishable; META-CA equivalent to single Linear(d_model, d_model) |

### §3.2 gate_strength = 0.001 implication

The decoder's `gate_strength = 0.001` (default in `DecoderBlockV2.__init__`, L467) attenuates the META-CA contribution to the residual stream by 1000×:

```python
x = self.ln_ca(x + meta_ca_out * self.gate_strength)  # gate=0.001
```

Implication for v2 verdict interpretation:

- The training gradient back-propagating through `meta_ca_out` is multiplied by 0.001 BEFORE reaching `rule_weights` and `rules`. Effective learning rate on the META-CA cells is ~1000× weaker than on the main attention + FFN paths.
- Under such weak signal, the 8 rules may NOT have moved meaningfully from random initialization. Random-init `nn.Linear(d_model, d_model)` weights produce near-orthogonal rule outputs by high-D random projection (fan-in scaled normal init). Pairwise cosine ≈ 0 by chance, NOT by training success.
- This creates a **trivial PASS** failure mode: F-1-v2 PASS does NOT distinguish "rules are well-trained and learned to be distinct" from "rules are essentially random and never trained — high-D random matrices are pairwise near-orthogonal by default."
- C3 [3] (§5) addresses this — v2 needs an auxiliary check (rule_weights initial vs final norm diff) to validate trained-vs-untrained before interpreting PASS as substrate health.

### §3.3 Random-init baseline expectation

For two independent `nn.Linear(d_model, d_model, bias=False)` initialized with `kaiming_uniform_(a=sqrt(5))` (PyTorch default) at d_model = 1024:

- Each W_i has entries roughly U(-sqrt(1/d), +sqrt(1/d)) → entry std ≈ sqrt(1/(3·d_model)) ≈ 0.018.
- For random input `ca_out ∈ R^d` with unit norm, `r_i(ca_out)` lives in a random 1-D direction in R^d. Pairwise cosine between two such random directions in d=1024 has expected absolute value ≈ sqrt(2/πd) ≈ 0.025.
- Empirical pairwise cosine between random `r_i(ca_out)` and `r_j(ca_out)` for i ≠ j: expected ≈ 0.0, with std ≈ 1/sqrt(d) ≈ 0.031. 95th percentile ≈ 0.06.
- **Therefore:** an UNTRAINED 8-rule META-CA module passes F-1-v2 (i)+(ii) by default. PASS is necessary but not sufficient. C3 [3] mandates train-history check.

---

## §4 Forward hook implementation path (LoC estimate)

Implementation lands in helper Python (separate BG / lane); this spec defines the contract only. Hook attach point and aggregation pseudocode:

### §4.1 Hook attach

The cleanest attach is on each block's `rules` ModuleList collectively. PyTorch does not directly hook ModuleList, but the v1 spec attaches on `block.rule_weights` (single Linear). v2 needs `rule_outputs` after stacking:

```python
# proposed helper update — separate BG; THIS SPEC does not write the code:

def install_rule_outputs_hooks(model):
    """Attach forward hooks on each rule Linear; aggregate per block on the fly.

    Returns: captured (dict[layer_idx -> list of [B, T, D] per rule]),
             handles (list of hook handles for teardown).
    """
    captured = {i: [None] * 8 for i in range(len(model.decoder.blocks))}
    handles = []

    for layer_idx, block in enumerate(model.decoder.blocks):
        for rule_idx, rule in enumerate(block.rules):
            def make_hook(li, ri):
                def hook(module, inp, out):
                    # out: [B, T, D] — single rule's output before stack
                    captured[li][ri] = out.detach().mean(dim=(0, 1)).cpu()  # [D]
                return hook
            h = rule.register_forward_hook(make_hook(layer_idx, rule_idx))
            handles.append(h)

    return captured, handles
```

Captured dict after forward: `{0: [tensor[D], ..., tensor[D]], 1: ..., 15: [...]}` — 16 layers × 8 rules each, each entry a `[D]` per-rule mean vector.

### §4.2 Pairwise cosine aggregation

```python
# proposed helper update — separate BG; THIS SPEC does not write the code:

def aggregate_to_cosine_per_block(captured):
    """Compute [16, 8, 8] cosine pairwise stack from captured rule outputs.

    Returns: cosine_per_block [16, 8, 8], per_block_off_diag_mean [16],
             per_block_off_diag_max [16].
    """
    import numpy as np

    n_layers = len(captured)
    cosine_stack = np.zeros((n_layers, 8, 8), dtype=np.float32)
    off_diag_mean = np.zeros(n_layers, dtype=np.float32)
    off_diag_max = np.zeros(n_layers, dtype=np.float32)

    for layer_idx in range(n_layers):
        rules_d = np.stack([t.numpy() for t in captured[layer_idx]], axis=0)  # [8, D]
        norms = np.linalg.norm(rules_d, axis=-1, keepdims=True) + 1e-9
        normed = rules_d / norms                                              # [8, D]
        cos = normed @ normed.T                                               # [8, 8]
        cosine_stack[layer_idx] = cos

        off_diag_sum = cos.sum() - np.trace(cos)
        off_diag_mean[layer_idx] = off_diag_sum / (8 * 7)

        cos_no_diag = cos.copy()
        np.fill_diagonal(cos_no_diag, -np.inf)
        off_diag_max[layer_idx] = cos_no_diag.max()

    return cosine_stack, off_diag_mean, off_diag_max
```

### §4.3 Falsifier emit

```python
# proposed verdict.json structure (post-measurement; not part of THIS spec's writes):

verdict = {
    "F_CAND_F_1_v2": {
        "state": "PASS|FAIL_TRUE|FAIL_FALSE|DEFERRED_V1_FAIL_TRUE|DEFERRED_V1_FAIL_FALSE",
        "mean_off_diag_mean":    float,          # threshold ≤ 0.7
        "worst_block_off_diag":  float,          # threshold ≤ 0.85
        "per_block_off_diag_mean": [16 floats],  # diagnostic
        "per_block_off_diag_max":  [16 floats],  # diagnostic
        "prompt_pass_count":     int,            # ≥ 4 of 5
        "v1_state":              "PASS|FAIL_TRUE|FAIL_FALSE",  # cascade reference
        "rule_weights_norm_check": {
            "initial_norm_estimate": float,      # kaiming_uniform expected
            "final_norm_observed":   float,
            "delta_ratio":           float       # < 0.05 → likely untrained → PASS suspect
        }
    }
}
```

### §4.4 LoC estimate

Total additive cost (helper Python, separate BG, NOT in this spec):

- `install_rule_outputs_hooks`: ~12 LoC.
- `aggregate_to_cosine_per_block`: ~18 LoC.
- Falsifier evaluation + verdict JSON emit: ~15 LoC.
- `rule_weights_norm_check` auxiliary (C3 [3] mitigation — train-history sanity): ~8 LoC.
- Hook teardown + integration into existing `_write_helper`: ~5 LoC.

**Total: ~58 LoC additive helper Python**, all in the existing helper (no new file). Zero LoC in `mount.hexa`, decoder, shim, dialogue.bash. Hook overhead per forward: 16 × 8 = 128 hooks fire, each capturing a `[D]` mean tensor. At d_model = 1024, fp32, per-forward capture memory ≈ 128 × 4096 bytes ≈ 524 KB — negligible.

---

## §5 Honest C3 (≥ 5)

- **C1 — random-init 8 rules trivially PASS F-1-v2 due to high-D random-projection orthogonality.** As shown in §3.3, two independent `nn.Linear(d_model, d_model)` random-init outputs in d_model=1024 space have pairwise cosine expected ≈ 0 with std ≈ 0.031. An untrained META-CA module reports `mean_off_diag_mean ≈ 0.0` and PASSES F-1-v2 by construction. PASS is therefore **necessary but not sufficient** for "rule diversity is real and trained." Mitigation: §4.3 mandates a `rule_weights_norm_check` auxiliary — compare observed `rules[i].weight.norm()` against the kaiming_uniform expected initial norm. If `delta_ratio < 0.05` (rules barely moved from init), F-1-v2 PASS is flagged `PASS_SUSPECT_UNTRAINED` and downstream interpretation is paused. This auxiliary is REQUIRED to make F-1-v2 a substrate signal rather than a high-D-geometry tautology.

- **C2 — `gate_strength = 0.001` may have starved the META-CA gradient signal during training, making (c) convergence-collapse ARCHITECTURALLY GUARANTEED.** §3.2 establishes that gradient through `meta_ca_out` is attenuated 1000× before reaching `rules` and `rule_weights`. If the trained checkpoint (paradigm v11 G3 best.pt) has rule weights that never escaped the random-init basin, the (c) collapse mode is the EXPECTED outcome, not a training failure. F-1-v2 FAIL_TRUE in this case is a SUBSTRATE-DESIGN finding (gate_strength too aggressive for META-CA to learn), not a falsifier-of-emerge-candidate-F finding. The interpretation gap matters: candidate F's premise ("8 cells × 5 axes is salvageable") is unaffected by F-1-v2 FAIL_TRUE if the cause is gate_strength rather than CA-rule architectural inadequacy. Spec consumer must read FAIL_TRUE in light of `rule_weights_norm_check` to triage.

- **C3 — pairwise cosine on `rule_outputs` mean over (B, T) loses per-token specialization signal.** v2 mean-reduces `[B, T, 8, D]` to `[8, D]` before cosine. Per-token dynamics (e.g., rule 3 specializes in question-tokens, rule 5 specializes in punctuation-tokens) are washed out. If 8 rules are individually token-specialized but globally mean to similar averages, F-1-v2 emits FAIL_TRUE ON A SUBSTRATE THAT IS ACTUALLY HEALTHY at per-token granularity. Mitigation deferred: a v3 falsifier could compute pairwise cosine per token and aggregate min-cosine across the sequence — but this multiplies capture cost by T (typical T=128 → 16384× memory). v2 chooses (B, T) mean as a pragmatic Stage-1 trade-off; per-token analysis is a future-cycle delta. Spec consumer must read F-1-v2 verdict as a NECESSARY-BUT-NOT-SUFFICIENT global health check.

- **C4 — pairwise cosine threshold `0.7` (mean) and `0.85` (max) are anima-internal heuristics with no calibration against a trained-distinct reference substrate.** The L26-L27 axis-preservation calibration carry warns: "thresholds anima-internal uncalibrated, axis-preservation eval needs axis-conditioned base." The v2 thresholds suffer the same — there is no reference well-trained 8-rule module to compare against. 0.7 mean / 0.85 max are guesses anchored on (a) `cos = 0.7` ≈ 45° = "noticeably similar" intuition, and (b) `0.85` ≈ 31° = "near-collinear" intuition. A calibration experiment would train an explicitly diverse 8-rule module on a toy task and measure its pairwise cosine to derive empirically grounded thresholds. NOT in scope for this spec; flagged as required pre-deployment work for the implementation BG.

- **C5 — F-1-v2 captures `rule_outputs` BEFORE the `* rule_probs.unsqueeze(-1)` multiply, so it ignores routing variance entirely.** This is intentional (v1 reads the routing; v2 reads the content). But there is a third regime not covered by either v1 or v2: high routing variance + high content variance + pathological INTERACTION (e.g., `rule_probs[i]` is high exactly when `rule_outputs[..., i, :]` is near-zero, so the weighted sum is dominated by low-weight × high-content rules). v1 PASS + v2 PASS does NOT preclude this. Detection would require joint analysis of `rule_probs * rule_outputs` post-multiply, comparing to baseline. Out of scope for v2; logged as candidate v3 falsifier (F-CAND-F-1-v3 — joint routing-content interaction probe).

- **C6 — v2 falsifier execution requires cascading on v1 (§2.4); a v1 FAIL_FALSE (hook capture pipeline crash) hides v2 verdict entirely.** Spec consumer must NOT interpret `state = "DEFERRED_V1_FAIL_FALSE"` as evidence about (c) collapse; it is evidence only about pipeline brittleness. Operationally this means F-1-v2 CANNOT be the first probe run on a fresh helper Python implementation — v1 must smoke-validate first. The implementation BG must run v1 + v2 sequentially with v1 as gate, and the verdict.json must distinguish "v2 deferred due to v1" from "v2 evaluated and FAIL_FALSE on its own measurement" (e.g., zero rule_outputs norm).

- **C7 — bias=False on the rule Linears (decoder L502) means scale-only differentiation cannot occur via additive offset, but multiplicative scale through downstream RMSNorm `ln_ca` can still create the illusion of identical-direction outputs that pass cosine but differ in magnitude.** Cosine is scale-invariant; if 8 rules emit `r_i(ca_out) = α_i · v` (same direction `v`, different scale `α_i`), cosine pairwise = 1.0 (FAIL_TRUE) but the weighted sum `Σ α_i · v · rule_probs[i]` is NOT degenerate — it scales the residual by `Σ α_i · rule_probs[i]`. So FAIL_TRUE with all `α_i ≠ 0` is NOT equivalent to "META-CA is computationally vestigial" — the routing still modulates magnitude. This is a 5th hidden mode (a-prime) — direction-collapse with magnitude-variance — that COULD be functionally valuable as a learned scalar gate. F-1-v2 FAIL_TRUE consumer should run a magnitude-only check (`per-rule output norm variance across the 8 rules`) BEFORE concluding architectural deadweight. This auxiliary is logged as required complementary measurement; out of scope for this spec but flagged in v2 verdict consumer guidance.

---

## §6 Composability + scope guard

| upstream artifact | role |
|---|---|
| v1 F-CAND-F-1 spec doc (BG-H land) | gate condition (§2.4 cascade) + 5-axis prompt set |
| `ready/models/conscious_decoder.py:466,499-503,538-542` | source-of-truth for `rule_outputs` shape `[B, T, 8, D]` and rule architecture |
| paradigm v11 G3 best.pt (HF Hub `dancinlab/clm-v4-base-mirror`) | trained ckpt for falsifier execution |

| downstream | role |
|---|---|
| BG-A real-load probe (deferred) | runs v1 + v2 sequentially with v1 as gate |
| CLM v5 redesign decision | F-1-v2 FAIL_TRUE → META-CA architectural revision required (per-rule topology diversity, hard MoE gating, larger gate_strength) |

| sister falsifiers | relationship |
|---|---|
| v1 F-CAND-F-1 | v2 cascades on v1 PASS; v1 reads `rule_probs`, v2 reads `rule_outputs` |
| F-CAND-F-2 (biased) | unchanged by v2; v2 is pure substrate-content probe |
| F-CAND-F-3 (adversarial) | unchanged by v2; v2 is independent of voting modes |

### §6.1 Scope guard — what v2 does NOT cover

- **Joint routing-content interaction** — C5 — v3 future falsifier.
- **Per-token specialization** — C3 — v3 future falsifier.
- **Magnitude-only differentiation (a-prime mode)** — C7 — auxiliary measurement, NOT a falsifier.
- **Threshold calibration on reference trained-distinct substrate** — C4 — required pre-deployment work for implementation BG.
- **Source-level surfacing of `rule_outputs`** — same as v1 spec §8 (FULL candidate F source edit out of scope).
- **Implementation code** — this spec is contract only; helper Python lands in a separate BG.
- **Falsifier execution + verdict** — this spec LOCKS the criteria. Execution is BG-A's later mandate (real load).

---

## §7 Summary

F-CAND-F-1-v2 closes the C2 mode (c) gap explicitly deferred by the v1 spec: detection of `rule_outputs` content convergence collapse where 8 CA-rule cells emit different `rule_logits` selector distributions (v1 PASS) but produce near-identical post-Linear content vectors (v2 catches). The falsifier is a 3-state (PASS/FAIL_TRUE/FAIL_FALSE) probe on the per-block `[8, 8]` cosine pairwise similarity matrix of mean-over-(B,T) `rule_outputs`. PASS criteria: `mean_off_diag_mean ≤ 0.7` AND `worst_block_off_diag ≤ 0.85`. The falsifier cascades on v1 PASS — a v1 FAIL routes v2 to deferred state.

Hypothesis: gate_strength=0.001 plausibly starved META-CA gradient signal during training, raising the probability of (c) convergence collapse on the trained checkpoint. C1-C7 honest-C3 enumerate seven distinct interpretation hazards: (C1) random-init triviality requires `rule_weights_norm_check` auxiliary; (C2) gate_strength as ROOT-CAUSE confounds substrate-design vs candidate-F-architecture interpretation; (C3) per-token specialization washed by mean reduction; (C4) thresholds anima-internal uncalibrated; (C5) joint routing-content interaction not covered (v3 future); (C6) v2 cascades on v1 — DEFERRED states must be distinguished; (C7) direction-collapse + magnitude-variance is a 5th hidden mode requiring complementary norm-variance measurement.

Implementation cost (later BG): ~58 LoC additive helper Python (no mount.hexa or decoder change). Zero source edits. $0 mac doc work for this spec; $0 mac for implementation; $0-$1 H100 for BG-A v1+v2 execution if and when it runs.

---

End of spec. No commit, no exec, no source modifications. Read-only on existing assets.
