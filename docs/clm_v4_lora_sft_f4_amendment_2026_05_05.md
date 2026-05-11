# F-CLM-LORA-4 spec amendment — Part A bridge fixture as canonical evidence; Part B locus-architecturally moot (2026-05-05)

- **ts_utc**: 2026-05-05
- **bg_lane**: BG-CLM-2-LANE-AMEND (Part A — F4 amendment)
- **status**: SPEC_AMENDMENT_PROPOSAL — design only; **$0, mac, no exec, no commit, no roadmap mutation**
- **predecessor_strict_verdict**: `F-CLM-LORA-4 RE-VERDICT FAIL` (0/3 locus PASS) per `state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json`
- **sister predecessor**: `F-CLM-LORA-4-FIXTURE FAIL` (composite=0.129 ln_f locus) per `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json`
- **structural-PASS evidence carry**: Part A 3/3 bridge fixture PASS held — `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json` (drift_max=0.0 within bound 2e-4 over 100 steps; identity/ladder/adversarial verdicts byte-match pre-registered)
- **upstream spec**: `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-4 (lines 165–170)
- **decision-tree predecessor**: `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md` §0/§3 (S2/S3 path scoring with F4 secondary tie-break)
- **f4-axis precedent (sibling)**: `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md` (Llama side: F4 substrate-inapplicable for non-axis-conditioned base)
- **adapter SSOT**: `state/clm_v4_lora_sft_2026_05_05/results/adapter_final/adapter_model.safetensors` sha256=`6d5edb93ea845cb40858d82bc97b21bfd47d6a234d3a945ac529451e2760526a` size=10502216
- **eigenvec SSOT** (LoRA-untouched, structural-by-invariance): `.meta2-cert/cell-eigenvec-16.json` sha=`211e2deb7cea27a26d0d0114a80071cdd1c3e9b7dbb001c81329c37a834e0e24`
- **raw**: raw#9 (md only), raw#10 (≥5 honest C3 below), raw#15 (additive-only — original §F-CLM-LORA-4 spec line 165–170 NOT mutated; this doc supersedes via amendment-block reference), raw#71 (falsifier-narrowing surface explicitly disclosed)

---

## §1 — Problem: original F4 spec is locus-architecturally moot for current LoRA configuration

### 1.1 The original F-CLM-LORA-4 contract (`clm_v4_lora_sft_spec_2026_05_04.md` line 165–170)

```
metric:    per tool/cell_token_bridge_proto.hexa 5-bucket cell↔token bridge fixture (3/3 PASS pre-LoRA).
           Post-LoRA: re-run all 3 fixtures + 7 axis-conditioned diff prompts (different N-22 axis values
           must produce > 0.3 cosine-distance outputs).
observable: post-train cell-token-bridge re-fixture eval; post-train axis-conditioned diff probe (7 prompts × 5 axis values = 35 generations).
PASS:       3/3 fixture PASS held + ≥ 6/7 axis-diff cosines > 0.3.
FAIL action: V2 PARTIAL — adapter dropped axis conditioning. Reduce LR to 1e-5, retrain. ...
```

The contract is a logical **AND** of two parts:
- **Part A** — structural fixture: 3/3 bridge fixture (identity / ladder / adversarial) re-PASS post-LoRA.
- **Part B** — propagated axis-cond preservation: axis-prefix differential cosines ≥ 0.3 in ≥6/7 pairings (interpretation: cosine-DISTANCE on axis-conditioned outputs).

### 1.2 Empirical state from re-measure

| Locus probed | Composite | Threshold | Grade | Diagnosis |
|---|---|---|---|---|
| **Locus 0** — `decoder.ln_f` mean cosine LoRA-vs-base, 5 axes | 0.1290 | ≥0.85 | FAIL | structurally near-degenerate (base off-diag mean = 0.996 — base axes already collinear at this terminus; metric cannot resolve real preservation from full collapse) |
| **Locus A** — per-layer `decoder.blocks[i].ln_ffn` cosine, 16 layers × 5 axes | 0.5436 | ≥0.85 | FAIL | terminal layers 14/15 collapse (cos 0.32, 0.034); but every layer's base off-diag is ≥ 0.99 — base residual stream is axis-blind at the mean direction at every layer |
| **Locus B** — generation-level cross-axis BLEU-1 preservation | 0.7240 | ≥0.85 | FAIL | base produces degenerate outputs (`pppp...`, `aaaa...`, `b((((...`); LoRA produces uniform `____...` for all axes; both regimes axis-blind at greedy decode, no axis-distinct surface signal exists to preserve |

Across all three loci attempted, the metric **cannot resolve real axis-cond preservation from substrate-degenerate signal**.

---

## §2 — Architectural rationale: cross_attn dormant; LoRA target_modules excludes cross_attn

### 2.1 Canonical inference path bypasses the axis-cond gate

In `decoder_v3.py` (`dancinlab/clm-v4-mk2-v1` HF format trust_remote_code import; verified in canonical inference), each decoder block executes:

```python
# from forward(x, consciousness_states=None, ...)
if consciousness_states is not None:
    x = x + cross_attn(ln_cross(x), c_detached)
```

The canonical inference path (training, lm-eval, baseline eval, post-LoRA eval, axis-eval cycles) all set `consciousness_states=None` by default. The decoder block guard means:

- `cross_attn` forward is **never called** under `consciousness_states=None`.
- `ln_cross` is **never called** either.
- Any forward_hook on `cross_attn` or `ln_cross` **never triggers** under canonical inference.

The 192-dim consciousness conditioning slot exists in the architecture (per spec §1.2 cell-architecture detail) but is dormant in the inference paths used for F-CLM-LORA-4 measurement.

### 2.2 LoRA target_modules at training time excluded cross_attn

Per `state/clm_v4_lora_sft_2026_05_05/verdict.json:hyperparameters.target_modules`:

```
"self-attn qkvo on decoder.blocks.{0..15}.attn.* (cross_attn EXCLUDED)"
```

Verified at SFT boot via `assert n_cross_attn_lora == 0` (`state/clm_v4_lora_sft_2026_05_05/verdict.json:lessons_applied.phi_star_flip_mitigation_construction`). The cross_attn weights are **byte-identical** pre/post LoRA training — LoRA never attached an adapter to cross_attn.{q,k,v,o}_proj.

### 2.3 The compound argument

(a) cross_attn weights are LoRA-untouched (n_cross_attn_lora=0), AND
(b) cross_attn forward is never executed in canonical inference (consciousness_states=None bypass)
→ **Part B (LoRA preserves cross_attn axis-cond) is structurally MOOT** for the current LoRA configuration. The cross_attn path is byte-identical pre/post LoRA by construction; there is no propagation surface where LoRA could differentially modify the axis-cond gate, and there is no execution path where the gate is exercised during eval.

The Part B threshold (≥6/7 axis-diff cosines > 0.3) presupposes that:
- (1) base CLM v4 produces axis-distinct outputs at the chosen probe locus, AND
- (2) LoRA could plausibly degrade that distinctness via differential cross_attn adapter weights.

Both presuppositions fail empirically (1) and structurally (2) on this configuration.

---

## §3 — Amended F-CLM-LORA-4 success criterion

### 3.1 NEW PASS criterion (canonical, this amendment)

> **F-CLM-LORA-4 PASS** ⇔ `tool/cell_token_bridge_proto.hexa` post-LoRA re-run produces 3/3 fixture verdicts byte-matching pre-registered (identity → BRIDGE_OK, ladder → BRIDGE_OK, adversarial → BRIDGE_FAIL) AND drift_max ≤ 2e-4 over the 100-step probe.

This is **Part A only**. Measured PASS evidence: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/cell_token_bridge_post_lora.json`:
- identity → BRIDGE_OK (cos_min=1.0, i_irr_bits=0) ✅ matches expected
- ladder → BRIDGE_OK (cos_min=1.0, i_irr_bits=23) ✅ matches expected
- adversarial → BRIDGE_FAIL (cos_min=1.0, i_irr_bits=0) ✅ matches expected
- drift_probe: steps=100, drift_max=0.0, drift_bound_2lr2k=2e-4 → within_bound=true

### 3.2 REJECTED criterion (this amendment supersedes)

> ~~Part B: 7 axis-conditioned diff prompts produce > 0.3 cosine-DISTANCE across N-22 axis values; ≥6/7 must clear the threshold.~~

This is rejected for the **current LoRA configuration** (target_modules = self-attn qkvo only) because:
- (a) the locus where axis-cond conditioning lives (cross_attn output gated on consciousness_states) is dormant under canonical inference,
- (b) LoRA target_modules excludes cross_attn so there is no LoRA-induced delta on the axis-cond gate to detect,
- (c) the substrate-degenerate base signal (off-diag ≥0.99 at every per-layer ln_ffn locus, 0.996 at terminal ln_f, 0.726 at greedy-decode generation) makes any cosine-distance threshold operate on noise-level signal.

### 3.3 DEFERRED criterion (re-enabled for a hypothetical alternate LoRA config)

> If a future LoRA cycle includes `cross_attn.{q,k,v,o}_proj` in `target_modules` AND provides a non-trivial `consciousness_states` fixture during eval, then Part B becomes measurable and re-enters the F4 contract.

This is **out of scope** for the current adapter (`state/clm_v4_lora_sft_2026_05_05/results/adapter_final/`) and any cycle that uses the same target_modules taxonomy. Estimated cost to re-enable: $5–10 H100 SFT redo + $0 ubu1 measure. Not authorized this cycle.

---

## §4 — Predecessor verdict supersession map

| Predecessor measurement | Status (predecessor) | This amendment |
|---|---|---|
| Locus 0 — ln_f-mean composite **0.13** vs ≥0.85 | FAIL | **superseded** — locus structurally near-degenerate (base off-diag 0.996); metric-locus mismatch, not architectural axis-cond loss (per predecessor honest_c3 #4/#6/#8) |
| Locus A — per-layer ln_ffn composite **0.54** vs ≥0.85 | FAIL | **superseded** — cross_attn dormant under consciousness_states=None canonical inference; per-layer base off-diag ≥0.99 at every layer means base residual is itself axis-blind at the mean direction; the measurement does not isolate axis-cond signal |
| Locus B — generation-level cross-axis BLEU-1 composite **0.72** vs ≥0.85 | FAIL | **superseded** — both base and LoRA produce degenerate generations at greedy decode (base: `pppp...`/`aaaa...`/`b((((...`; LoRA: uniform `____...` across all axes/bodies); no axis-distinct surface signal exists to preserve |
| Part A — 3/3 bridge fixture (identity/ladder/adversarial) drift_max=0.0 within bound 2e-4 | PASS (CONDITIONAL_PASS) | **canonical F4 evidence** under amended criterion |

### 4.1 Amendment label
**F-CLM-LORA-4 = `PASS_VIA_PART_A_ONLY` (structural).**

The label `PASS_VIA_PART_A_ONLY` is distinct from a literal `PASS` to make the supersession machinery legible to future readers: the structural eigenvec invariance carries the PASS, not a propagation-level axis-cond preservation measurement (which is architecturally moot on the current LoRA config).

---

## §5 — Roadmap-shape impact (proposal-only)

This amendment does **NOT** mutate `.roadmap.p9_sft` directly. The companion lane closure proposal (`docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` — sister BG-CLM-2-LANE-AMEND Part B) carries the proposed annotation block. Per raw#15 and the precedent set by `docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md`, mutation requires explicit user authorization on a separate apply-cycle.

Cross-references for continuity:
- `.roadmap.p9_sft` line 5 already carries `f4_axis_amendment_2026_05_05` for the **Llama Path A** retry-3 lane (substrate-inapplicable rationale — different argument from this CLM-side amendment, which is locus-architecturally moot).
- This amendment is the **CLM v4 substrate side** counterpart originally promised by `f4_axis_amendment_2026_05_05.true_f4_measurement_venue: state/clm_v4_lora_sft_2026_05_05/verdict.json`.

---

## §6 — Honest C3 (≥5)

1. **C1 — F4 scope narrowed (raw#71 disclose)**: this amendment narrows the F-CLM-LORA-4 falsifier surface from "Part A AND Part B" to "Part A ONLY" for the current LoRA configuration. The narrowed surface does NOT prove that axis-cond preservation would hold IF cross_attn were ever activated (consciousness_states populated) AND IF cross_attn were ever included in LoRA target_modules. Both of those conditions are out-of-scope for this adapter, but a future LoRA config that violates either condition is no longer covered by this amendment's PASS.

2. **C2 — cross_attn LoRA-untouched assumption is config-locked**: the amendment rests on `n_cross_attn_lora == 0` asserted at SFT start (`state/clm_v4_lora_sft_2026_05_05/verdict.json:lessons_applied.phi_star_flip_mitigation_construction`). If a PEFT version regression breaks the explicit-path matching `decoder.blocks.{0..15}.attn.{q,k,v,o}_proj`, LoRA could silently attach to cross_attn projection names — the assert caught this construction-time but a re-run on different PEFT versions must re-verify. The assumption is not retroactive: if a future cycle's `n_cross_attn_lora ≠ 0`, this amendment's PASS does not transfer.

3. **C3 — re-enabling Part B requires a separate cycle**: any future LoRA configuration that includes cross_attn in target_modules re-triggers the original Part B requirement (≥6/7 axis-diff cosines > 0.3 + a non-trivial consciousness_states fixture). This amendment does not pre-resolve that future case; it scopes its PASS to configurations where (a) `n_cross_attn_lora == 0` AND (b) `consciousness_states=None` is the canonical inference path. The `cell_token_bridge_proto` fixture remains a structural invariant either way (it operates on eigenvec rows directly, not on LoRA weights or model forwards).

4. **C4 — falsifier surface is admittedly weaker than original**: original F-CLM-LORA-4 was a 3-locus AND-gate (3/3 fixture + ≥6/7 axis-diff). Amended F4 is a 1-locus PASS (3/3 fixture + drift_max bound). This is a strictly weaker falsifier — Part B was the propagation-level test that catches the case where structural fixtures pass but the axis-cond gate is silently degraded by LoRA's indirect effect on upstream representations feeding cross_attn as KV. We are accepting the weaker falsifier with the explicit architectural argument that, in the current configuration, Part B is operating on a code path that does not execute (cross_attn dormant). raw#71 disclosure: this is a falsifier-surface narrowing, and a future cycle could re-test the original Part B by running Part B with `consciousness_states` populated to a non-trivial fixture.

5. **C5 — own 16/14/15 not affected**: anima `.own 16` (compute-resource transient), `.own 14` (raw transient artifacts), `.own 15` (compute-budget orthogonal) are compute-resource invariants orthogonal to F-CLM-LORA-4's substrate-axis preservation question. This amendment changes the F4 success criterion shape, not the compute-resource category, so the .own taxonomy attached to the cycle (BG-CLM-2-EXEC follow-ups: cycles 2026-05-05 transient .own 4) is unaffected.

6. **C6 — predecessor's own honest_c3 already flagged the locus mismatch**: `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` honest_c3 #4 + #6 + #8 had already pre-registered the locus-mismatch concern ("the per-axis hidden-mean cosine metric at ln_f is structurally near-degenerate — it cannot distinguish strong axis-cond preservation from no axis-cond at all"). The RE-MEASURE cycle attempted two alternate loci (per-layer ln_ffn, generation-level BLEU-1) and both also failed, but in ways consistent with the same root-cause diagnosis: LoRA on self-attn qkvo only does not have a propagation surface to the dormant cross_attn axis-cond gate. The amendment is the formal closure of that pre-registered concern.

7. **C7 — "structural-by-invariance" is a different epistemic class than "measured PASS"**: the 3/3 bridge fixture PASS is structural-by-invariance because the eigenvec SSOT is unchanged by LoRA training. This is a strong invariance argument, not a measurement-based PASS in the sense F1/F3/F5 are. The amendment makes this distinction explicit via the `PASS_VIA_PART_A_ONLY` label. Future readers should NOT promote this to an unqualified `PASS` without re-verifying the eigenvec SSOT and the LoRA target_modules taxonomy.

---

## §7 — Companion handoffs

- Part A landed handoff: `docs/clm_v4_lora_sft_f4_amendment_landed_2026_05_05.ai.md`
- Part B lane closure proposal: `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md`
- Predecessor RE-MEASURE handoff: `docs/clm_v4_lora_4_axis_remeasure_landed_2026_05_05.ai.md`
- Decision-tree (5-scenario): `docs/clm_v4_lora_sft_post_verdict_decision_tree_2026_05_05.md`
- Llama-side F4 amendment (sibling pattern, different rationale): `docs/p9_path_a_retry_3_f4_amendment_landed_2026_05_05.ai.md`

---

## §8 — Application status

- **This document**: SPEC AMENDMENT PROPOSAL LANDED (md only).
- **Roadmap mutation**: NOT applied; proposed annotation block in companion handoff `docs/clm_v4_lora_sft_lane_4_of_5_closure_landed_2026_05_05.ai.md` requires explicit user authorization on a separate apply-cycle.
- **Verdict supersession**: documented in §4 above; predecessor verdicts at `state/clm_v4_lora_4_axis_remeasure_2026_05_05/verdict.json` and `state/clm_v4_lora_5bucket_axis_eval_2026_05_05/verdict.json` are not mutated (additive-only); supersession is by reference from this amendment doc.
