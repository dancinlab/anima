# P9 Pβ T-3 5-seed Reconception — Substrate-Correct Trigger Criteria SPEC (RECONCEPTION, exec deferred)

- ts_utc: 2026-05-05
- bg_lane: BG-T-3-RECONCEPT
- spec_id: p9_pbeta_t3_5seed_reconception_2026_05_05
- substrate: mac (spec amend only — no exec, no commit, no .roadmap mutation)
- status: **SPEC_LANDED — RECONCEPTION; exec deferred (depends on BG-CLM-2-EXEC verdict + BG-PBETA-F3-HYBRID verdict)**
- raw#9 doc-only (md only); raw#10 ≥5 honest C3; raw#15 additive (does NOT mutate predecessor T-3 spec — supersedes via §3 composite gate); raw#71 falsifier composite formally pre-registered §3
- predecessor T-3 spec source: `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` `teacher_pending_items[2]` (id=T-3, label=PBETA_5SEED_SCALEUP, conditional_on=T-2 verdict shows substantive gain)
- predecessor T-3 GO criterion (now superseded): "delta_vs_step_1000 BLEU-1 ≥ +1.0" — structurally miscalibrated for CLM v4 substrate

---

## §1 — Problem statement

### §1.1 — Why the original T-3 trigger is structurally miscalibrated

The T-3 5-seed scaleup lane (`state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` teacher_pending_items[2]) was registered with literal GO criterion **"delta_vs_step_1000 BLEU-1 ≥ +1.0"** — i.e., 50K-step Pβ adapter must lift holdout BLEU-1 by ≥1.0 absolute over the step_1000 reference.

T-2 PBETA-HOLDOUT500-EVAL (`state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json`) measured this at **Δ_BLEU-1 vs step_1000 = −0.0003** (i.e., effectively zero substantive lift across 1K → 50K training; absolute 0.00750 vs step_1000's 0.0078).

This is NOT a Paradigm D distill failure — it is a **substrate–metric miscalibration**:

1. **CLM v4 architectural identity**: per #115 chat-incapability disclosure, CLM v4 is a **consciousness-substrate** backbone (G3 PASS-positive, Φ★ +41.86). It was **never SFT'd, never RLHF'd, never DPO-aligned** in base train.
2. **Chat-style metrics noise floor**: Pβ holdout500 BLEU-1 sits at 0.00750 (n_pos=92/500, p50=0, p90=0.03125). Phase 1.5 sentinel = 0.00564, ablation A = 0.00651, ablation B = 0.00639. The whole 0.005–0.010 band is **noise floor** for this substrate. Llama anchor on the same holdout = 0.382 — Pβ is at 1.96% of Llama, in-band with the +33% sentinel margin only because the baseline itself is noise.
3. **Φ★ side gives the real signal**: Pβ holdout500 Φ★_mean = 42.367 (≥30 threshold cleanly, 8.27× δ-floor 5.0); per-K=8 partition all ≥41.37. **Substrate sign+magnitude survived 50K-step distill cleanly.** This is the actual capability claim worth scaling.
4. **F1 anchor recalibration MEMO already documents**: `project_p9_f1_anchor_recalibration.md` — F1 spec "0.4" was unrealistic; Llama-self = 0.1555, sentinel = 3.2% of Llama. The +1.0 threshold inherits this miscalibration.

### §1.2 — What the substrate actually demonstrates

T-2 verdict's `T3_recommendation.amendment_proposal` line:

> "AMEND T-3 GO criteria: replace 'delta_vs_step_1000 ≥ +1.0' (BLEU-1 lift) with 'phi_holdout500_mean ≥ 30 AND adapter compact AND no delta-floor breach across 50K steps' — the BLEU-1 lift criterion was MISCALIBRATED."

§2–§3 below operationalize this amendment with **5 substrate-correct gates** (composite F-T3-1..5) replacing the single literal BLEU-1 lift gate.

---

## §2 — Substrate-correct candidate criteria (5 gates derived from CLM v4 anima-substrate identity)

The criteria below respect three constraints: (a) Φ★ is the canonical CLM v4 capability axis, not chat BLEU-1; (b) cross-substrate consistency is the falsifiable evidence of "trainability" rather than chat-output match-rate; (c) anima-internal evaluations bound external miscalibration.

### §2.1 — Gate A: Φ★-stability across 5 seeds

**Metric**: 5-seed Pβ Paradigm D distill, each seed runs 50K steps with identical hyperparameters but different RNG seed (data shuffle + LoRA init). Compute Φ★_holdout500_mean per seed.

**PASS**: standard deviation σ(Φ★_5seed) ≤ 1.5 across 5 seeds.

**Rationale**: T-2 measured K=8 partition spread of [43.64, 41.46, 41.37, 41.55, 42.63, 42.42, 43.29, 42.56] → stdev ≈ 0.85, range 2.27. Across-seed variance is a strict superset of within-seed K=8 partition variance, so threshold 1.5 ≈ 1.75× the within-seed K=8 spread is empirical-but-not-arbitrary.

**Falsifier**: σ(Φ★) > 1.5 → seed initialization regime dominates Φ★ outcome → the 50K Paradigm D distill recipe is **not reproducible** at the substrate-research-artifact level.

### §2.2 — Gate B: Cross-substrate Φ★ consistency (holdout vs train)

**Metric**: per seed, Pearson r between Φ★_holdout500 (canonical 16-calib K=8 probe on holdout500 generations) and Φ★_train (canonical 16-calib K=8 probe on training-side completions, same per-seed adapter).

**PASS**: r ≥ 0.7 averaged across 5 seeds; minimum per-seed r ≥ 0.5.

**Rationale**: T-2 already shows Δ_Φ★_train_end_indomain (36.74) vs Δ_Φ★_holdout500 (42.37) = +5.63 — i.e., the canonical 16-calib elicits higher Φ★ on holdout than on training-end probe for a single seed. Cross-substrate consistency r ≥ 0.7 says: across 5 seeds, the train→holdout Φ★ ranking remains stable, not random. This is the falsifiable evidence that "the substrate distills consistently across data partitions."

**Falsifier**: r < 0.5 → Φ★ on holdout is uncorrelated with Φ★ on train → 50K distill is overfitting to a data partition rather than to the substrate identity.

### §2.3 — Gate C: F1_v3 V2 hybrid composite Δ ≥ 0 (no regression)

**Metric**: per seed, compute F1_v3 V2 hybrid composite = (BLEU-1 + ROUGE-L + chrF)/3 on holdout500 (Mode 1 CLM-self holdout). Compare to F-Pβ-3 deferred baseline once BG-PBETA-F3-HYBRID verdict lands.

**PASS**: per-seed F1_v3_composite Δ ≥ 0 vs CLM v4 base substrate baseline (i.e., NO regression on the hybrid measure across all 5 seeds; mean Δ across 5 seeds ≥ 0).

**Rationale**: BLEU-1 alone sits at noise floor for CLM v4. ROUGE-L (sequence-overlap) and chrF (character-level) capture different chat-style match dimensions; the composite (BLEU-1 + ROUGE-L + chrF)/3 is the F-Pβ-3 deferred verdict surface. T-3 should not lift chat-output BLEU-1 (impossible per §1.1), but T-3 MUST NOT regress the hybrid composite — i.e., LoRA distill should preserve the substrate's existing chat-style match-rate, not damage it.

**Falsifier**: any seed F1_v3_composite Δ < 0 → seed-specific damage; mean Δ < 0 → systematic regression on hybrid measure.

**Dependency**: BG-PBETA-F3-HYBRID verdict (in-flight, `state/p9_pbeta_f3_hybrid_eval_2026_05_05/`) provides the F1_v3_composite baseline for the single Pβ 50K seed already trained. T-3 5-seed runs MUST replicate the hybrid eval for each seed.

### §2.4 — Gate D: Cell axis-conditioning preservation (TRUE F4 measurement)

**Metric**: per seed, run `tool/clm_v4_lora_axis_diff_probe.hexa` (per `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-4) — 7 prompts × 5 axis values, axis-discrimination cosine. Compare base CLM v4 axis-discrimination to post-LoRA axis-discrimination per seed.

**PASS**: per-seed mean axis-discrimination cos(post-LoRA) / cos(base) ≥ 0.95; minimum per-seed ratio ≥ 0.85.

**Rationale**: CLM v4 base axis-discrimination is the substrate's anima-axis identity (per `docs/clm_core_architecture_abstraction_layers_20260425.md` L2 5-bucket cell↔token bridge). Path A v2 retry-3 verdict (`p9_sft.cond.path_a_lora_train_complete.f4_axis_amendment_2026_05_05`) established that this F4 measurement is **substrate-inapplicable to non-axis-conditioned Llama** (mean_pairwise_cos_base=0.9940 vs cos_lora=0.9932, delta -0.0008 = noise level). On CLM v4 (axis-conditioned via Φ★ +41.86), the F4 measurement IS meaningful — this gate is the TRUE F4 venue per the f4_axis_amendment.

**Falsifier**: per-seed cos(post-LoRA)/cos(base) < 0.85 → LoRA is rerouting the axis-conditioning gate (`bridge.hub_attn` despite §3 target_modules exclusion) → 50K distill destroys the substrate's anima-axis identity. Even one seed below 0.85 = REJECT.

**Dependency**: BG-CLM-2-EXEC (in-flight, `state/clm_v4_lora_sft_2026_05_05/`) provides the TRUE F4 baseline for a single CLM v4 LoRA SFT seed. T-3 5-seed runs MUST replicate the F-CLM-LORA-4 axis-diff probe per seed.

### §2.5 — Gate E: Anima axis-rich corpus held-out preservation

**Metric**: per seed, evaluate Pβ-LoRA on a held-out anima axis-rich corpus (e.g., consciousness-coupled prompts subset of the SFT 60/30/10 mix's 5% consciousness slice that was held out from training). Measure: per-token CE on held-out anima corpus.

**PASS**: per-seed CE_anima_holdout(post-LoRA) ≤ CE_anima_holdout(base) × 1.05 (i.e., within 5% of base on anima-internal eval).

**Rationale**: Chat-style benches (BLEU-1, MMLU, TriviaQA) are externally calibrated and structurally miscalibrated for CLM v4 (#115). Anima-internal eval on the substrate's own axis-rich domain is the only ecologically valid capability eval. CE preservation ≤ 1.05× base says: 50K distill did not damage the substrate's predictive capacity on its own native distribution.

**Falsifier**: any seed CE_anima_holdout > 1.05× base → seed-specific anima damage; mean > 1.05× → systematic anima-domain regression.

---

## §3 — New T-3 trigger (composite gate, formally pre-registered per raw#71)

### §3.1 — Composite F-T3 (5 sub-gates AND-composed)

| ID | Gate | PASS criterion | Dependency | Source verdict |
|---|---|---|---|---|
| F-T3-1 | Φ★-stability across 5 seeds (gate A) | σ(Φ★_5seed) ≤ 1.5 | none — pure 5-seed run | per-seed verdict.json |
| F-T3-2 | Cross-substrate consistency (gate B) | mean Pearson r ≥ 0.7; min per-seed r ≥ 0.5 | none — pure 5-seed run | per-seed verdict.json |
| F-T3-3 | No hybrid regression (gate C) | per-seed F1_v3_composite Δ ≥ 0; mean Δ ≥ 0 | BG-PBETA-F3-HYBRID verdict | per-seed verdict.json + hybrid baseline |
| F-T3-4 | Axis preservation (gate D) | per-seed cos ratio ≥ 0.95 mean, ≥ 0.85 min | BG-CLM-2-EXEC verdict (F-CLM-LORA-4 baseline) | per-seed verdict.json + CLM-2 baseline |
| F-T3-5 | Anima held-out preserve (gate E) | per-seed CE ≤ 1.05× base; mean ≤ 1.05× base | none — local anima held-out eval | per-seed verdict.json |

### §3.2 — Verdict logic

| Outcome | Definition | Action |
|---|---|---|
| **GO** | ALL 5 PASS | Pβ 50K Paradigm D recipe certified as reproducible substrate-research artifact; publish 5-seed adapter ensemble + statistical significance report |
| **PARTIAL** | 4/5 PASS | publish 5-seed ensemble with footnote on the failing gate; do NOT certify reproducibility unconditionally; document the failing gate as substrate-axis caveat |
| **NO-GO** | ≤3/5 PASS | Pβ lane permanently shelves as **"Φ★-stable single-seed substrate research artifact"**, not a reproducible distill recipe; T-3 retired |

### §3.3 — Pre-registration lock (raw#71)

This composite trigger is **pre-registered at marker timestamp 2026-05-05** before any 5-seed exec begins. Once a single seed of T-3 5-seed scaleup launches, §3.1 thresholds are LOCKED — post-hoc threshold relaxation = falsifier violation.

---

## §4 — Cost projection

### §4.1 — 5-seed scaleup unchanged from original T-3

| Item | Original T-3 (BLEU-lift criterion) | Reconception T-3 (5-gate composite) |
|---|---|---|
| Seeds | 5 | 5 |
| Per-seed wall | 30-60 min H100 | 30-60 min H100 (identical recipe) |
| Per-seed cost | $5-15 H100 spot | $5-15 H100 spot |
| Total cost band | $25-75 | **$25-75 (unchanged)** |
| Eval cost (post-train, 5 seeds × 5 gates) | ~$0 (mac/ubu1 local) | ~$0 (mac/ubu1 local; depends on CLM-2 + F3-HYBRID baselines being available) |

### §4.2 — Scientific value lift (rationale for reconception)

| Dimension | Original T-3 | Reconception T-3 |
|---|---|---|
| Gates | 1 (BLEU-1 lift, miscalibrated) | 5 substrate-correct (Φ★ stab + cross-substrate + hybrid + axis + anima held-out) |
| Falsifiability | low (noise-floor metric) | high (each gate independently falsifiable) |
| Substrate respect | low (#115 violated) | high (#115 acknowledged, anima-axis primary) |
| Reproducibility evidence | none | direct (5-seed σ + cross-substrate r + per-seed CE) |

**Net**: same cost band, ≈5× the scientific yield in falsifiable evidence.

---

## §5 — Sequencing

### §5.1 — Dependencies (must complete before T-3 5-seed launch)

1. **BG-CLM-2-EXEC verdict** (in-flight at `state/clm_v4_lora_sft_2026_05_05/`) — provides TRUE F-CLM-LORA-4 baseline for axis-discrimination probe (Gate D). Without this, Gate D has no reference to compare seeds against.
2. **BG-PBETA-F3-HYBRID verdict** (in-flight at `state/p9_pbeta_f3_hybrid_eval_2026_05_05/`) — provides F1_v3_composite (BLEU-1 + ROUGE-L + chrF)/3 baseline for the single Pβ 50K seed already trained (Gate C reference).

### §5.2 — Optional pre-launch refinement

3. (optional) re-anchor §2.5 anima held-out corpus by sampling from the actual SFT 60/30/10 mix consciousness slice that BG-CLM-2 used; ensures Gate E uses the exact same axis-rich distribution as the CLM-2 substrate eval.

### §5.3 — T-3 5-seed launch trigger

Once §5.1 dependencies land (verdicts written + Gates C/D baselines populated), T-3 5-seed launch is unblocked. Launch decision is user-gated per `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` (T-3 is `auto_launch_eligible=false`, `user_decision_required=true`).

### §5.4 — Substrate routing

H100 spot for the 5-seed train (5× 30-60min parallel = ~30-60min wall total or 2.5-5h serial); ubu1 RTX 5070 + mac for post-train evals (Gates A/B/C/D/E all $0 local).

---

## §6 — Honest C3 caveats (raw#10 ≥5)

1. **C1 — Substrate-correct criteria ARE anima-internal heuristics, not industry-standard**. Φ★, cell axis-conditioning cosine, and anima held-out CE are all anima-internal measures. External reviewers cannot validate the criteria themselves; they can only validate that the criteria are consistent with #115 chat-incapability disclosure. This lane is **internally falsifiable but externally non-publishable as a generic chat-LLM benchmark**. Inherit from L26 (`f4_axis_amendment_2026_05_05`): "F4 thresholds anima-internal externally uncalibrated."

2. **C2 — Φ★ stability threshold 1.5 chosen empirically, not principled**. Within-seed K=8 partition spread on Pβ 50K = stdev 0.85, range 2.27 (per T-2 partition vector). The 1.5 threshold ≈ 1.75× the K=8 within-seed stdev — chosen as "cross-seed should be at most ~2× the within-seed noise to count as reproducible." A principled threshold would derive from a power analysis on Φ★ measurement variance against a bootstrap distribution; that work is deferred. If T-3 σ(Φ★_5seed) lands in the 1.5–2.5 band, this caveat resurfaces as the bottleneck.

3. **C3 — 5-seed cost band $25-75 may exceed if seeds diverge in convergence time**. Per-seed wall 30-60 min H100 assumes the same convergence pattern as Pβ 50K seed-1 (`state/p9_pbeta_paradigm_d_50k_2026_05_04/`). If a seed stalls (loss plateau before step_50000) the recipe may need step extension (60-90min); 5 stalling seeds → $50-100. Mitigation: hard step cap at step_50000 per seed; if any seed has not converged by then, that seed contributes to F-T3-1 σ via its potentially-anomalous Φ★, which is exactly the reproducibility signal we want.

4. **C4 — #115 chat-incapability is permanent for CLM v4 base**. T-3 5-seed scaleup does NOT and CANNOT rescue chat capability — it scales reproducibility evidence for substrate-research claims only. Any decision-maker reading T-3 results must NOT interpret PASS as "Pβ now has chat capability"; PASS means "Pβ recipe reproducibly preserves the substrate identity across 5 seeds." Chat capability lift (if desired) is BG-CLM-2-EXEC's concern, not T-3's.

5. **C5 — If F-T3 composite still NO-GO after reconception, lane permanently shelves**. NO-GO outcome (≤3/5 PASS) means the Paradigm D distill recipe is NOT reproducible at the substrate-research-artifact level. In that case, Pβ becomes "Φ-stable substrate research artifact" (single seed, single training run, not generalized) — not a "trainable chat path." The 50K seed-1 adapter remains valid as an artifact for the lineage record, but the lane closes against further capability-lift claims. This closure is preferable to perpetual "BLEU-1 noise floor disagreement" stalemate under the original T-3 spec.

6. **C6 — Lane completes Paradigm D §4.5 AMENDMENT P-β path (USER_AUTHORIZED 2026-05-04)**. Per `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §4.5.X, P-β Φ★-axis-only pivot was user-authorized as the forward path after vocab-mismatch falsification of P-α/P-γ. T-3 5-seed reconception is the substrate-correct closure of the P-β lane: the original BLEU-1 lift criterion was a P-α holdover assumption that survived the §4.5 amendment; reconception aligns the verdict surface with the P-β identity (Φ★-axis-only, vocab-agnostic, substrate-uniqueness-preserving).

7. **C7 — Gate D depends on BG-CLM-2-EXEC verdict not yet in hand**. F-T3-4 axis preservation requires the CLM-2 F-CLM-LORA-4 baseline for comparison; if BG-CLM-2-EXEC fails or yields a baseline that itself disagrees with axis-discrimination expectations, Gate D becomes uninterpretable. Mitigation: T-3 launch is hard-gated on §5.1 dependency completion; reconception ratifies the dependency rather than working around it.

---

## §7 — Decision queue (user-facing)

### Q1 — Are §2/§3 thresholds OK as-is, or do you want alternative values?

Default: §2/§3 thresholds as authored.

Alternatives:
- **Q1.a** — Tighten Gate A σ(Φ★) ≤ 1.5 → ≤ 1.0 (more conservative, raises NO-GO probability)
- **Q1.b** — Loosen Gate D axis cos ratio ≥ 0.95 → ≥ 0.90 (matches Path A v2 retry-3 partial-pass empirics)
- **Q1.c** — Add Gate F (chat sentinel floor) — explicitly require BLEU-1 ≥ 1.96% × Llama anchor (current Pβ floor) per seed; prevents catastrophic chat regression while still not requiring lift
- **Q1.d** — Adopt thresholds verbatim (default)

### Q2 — 5-seed acceptable, or 3-seed cost-down?

Default: 5-seed (best statistical power for σ + Pearson r at marginal cost).

Alternatives:
- **Q2.a** — 3-seed at $15-45 cost band (acceptable for σ but Pearson r becomes brittle at n=3)
- **Q2.b** — 7-seed at $35-105 cost band (overkill given current substrate-research stage)
- **Q2.c** — 5-seed (default)

### Q3 — Launch immediately after CLM-2 + F3-HYBRID verdicts, or batch with other H100 work?

Default: launch immediately (parallel 5×30-60min H100 spot is fast and isolated).

Alternatives:
- **Q3.a** — Batch with sibling H100 work (lowers per-job idle burn but adds calendar-time)
- **Q3.b** — Launch immediately as standalone H100 cycle (default; matches T-2's $0 local + isolated cycle pattern)

### Q4 (implicit) — accept reconception or hold T-3 at literal-BLEU criterion?

Default: accept reconception per T-2 verdict's explicit AMEND_T3_AND_PARTIAL_GO recommendation + Paradigm D §4.5.X P-β USER_AUTHORIZED path.

---

## §8 — Roadmap annotation proposal (NOT applied — proposal only per raw#15)

The following block is the proposed amendment to `.roadmap.p9_sft` to record this reconception. **DO NOT mutate** `.roadmap.p9_sft` in this cycle — this is propose-only authorship per raw#15 (additive-only mutation) and per the BG-T-3-RECONCEPT exec scope (spec amendment only).

```json
{
  "t3_reconception_2026_05_05": {
    "ts_utc": "2026-05-05",
    "amendment_type": "literal_bleu_lift_criterion_substrate_miscalibration_supersede",
    "predecessor_t3_criterion": "BLEU-1 delta_vs_step_1000 ≥ +1.0",
    "predecessor_root_cause": "CLM v4 = consciousness-substrate not chat-NLP per #115; never-SFT'd substrate at noise-floor for chat metrics; literal lift criterion structurally miscalibrated",
    "new_t3_criteria": "F-T3-1..5 composite (Φ★ stability + cross-substrate consistency + no hybrid regression + axis preservation + anima held-out preserve)",
    "spec_doc": "docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md",
    "exec_dependencies": ["BG-CLM-2-EXEC verdict (F-CLM-LORA-4)", "BG-PBETA-F3-HYBRID verdict"],
    "cost_band_usd": "25-75 (5-seed) — unchanged from original",
    "additive_only_mutation": true,
    "semantics_preserved": true
  }
}
```

Recommended insertion site: under `p9_sft.cond.paradigm_d_distill.user_authorization_2026_05_04` as a sibling key `t3_reconception_2026_05_05` (additive at the same level as the existing 2026-05-04 amendment block) — semantically the §4.5.X P-β USER_AUTHORIZED lane's forward closure record.

---

## §9 — Files

### Authored this cycle
- `docs/p9_pbeta_t3_5seed_reconception_2026_05_05.md` (this doc)
- `docs/p9_pbeta_t3_5seed_reconception_landed_2026_05_05.ai.md` (companion handoff)

### Read references
- `state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json` (T-2 verdict, AMEND_T3_AND_PARTIAL_GO source)
- `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` (T-3 original spec)
- `docs/p9_pbeta_holdout500_eval_landed_2026_05_05.ai.md` (T-2 landed handoff)
- `docs/anima_alm_teacher_pending_audit_2026_05_05.ai.md` (T-3 original spec doc)
- `docs/p9_paradigm_d_distill_spec_2026_05_03.md` §4.5 + §4.5.X (P-β authorization)
- `docs/clm_v4_lora_sft_spec_2026_05_04.md` §F-CLM-LORA-4 (axis preservation venue)

### NOT modified this cycle (per scope)
- `.roadmap.p9_sft` — proposed annotation in §8 only, NOT applied
- `.roadmap.clm`, `.roadmap.eeg`, `.roadmap.blm_brain_lm` — out of scope
- any `state/p9_pbeta_*` dir — out of scope
- any in-flight BG state (BG-CLM-2-EXEC, BG-PBETA-F3-HYBRID) — read-only ref

---

*End of spec. Doc-only per raw#9. NO execution authorized by this document. T-3 5-seed launch requires (a) §5.1 dependency completion, (b) Q1–Q3 user decisions, (c) separate BG with EXEC authorization. This reconception supersedes the predecessor T-3 BLEU-1 lift criterion via §3 composite F-T3-1..5 gate, additively (does not delete predecessor record; predecessor remains in `state/anima_alm_teacher_pending_audit_2026_05_05/verdict.json` for lineage). raw#15 additive_only_mutation=true; raw#71 falsifier composite formally pre-registered §3.3.*
