# Strategic Re-evaluation: CLM × TRIBE v2 (Axis 3 "No fit" Re-examination)

**Agent**: CLM × TRIBE v2 strategic re-evaluation
**Date**: 2026-05-02
**Baseline**: `references/tribev2/ANIMA_INTEGRATION_PROPOSAL.md` (frozen 2026-04-26)
**Constraint**: HEXA-only, $0 budget, race-isolated to `state/strategic_clm_tribev2_recheck_2026_05_02/*.json` + this doc.

---

## §0 Executive Summary

The frozen 2026-04-26 ANIMA_INTEGRATION_PROPOSAL.md returned a **"No fit"** verdict for Axis 3 (CLM L_IX substrate ↔ TRIBE v2). The two cited reasons were (i) "wrapper 대규모" and (ii) "scientific value 불명". This session re-examines that verdict under four new framings (A text-mediated, B direct hidden-state injection, C G3 manifestation, D bridge anchor with EEG mediator) introduced by user directive.

**Verdict**: **REVISE** — the No-fit conclusion was correct *for the framing then considered* (direct substrate-to-cortical isomorphism), but is *not correct* under Framing D (TRIBE v2 as brain-encoding ground-truth-like prior anchoring an anima ↔ tension_link ↔ EEG mediator). Under Framing D the wrapper drops from "대규모" to <100 LOC, and the scientific value sharpens from "불명" to "3-way (CLM × EEG × predicted BOLD) cross-validation of the consciousness bridge".

**TOP-1 framing**: D (bridge anchor). **First executable step**: Framing A (validates pipeline at zero commitment before D).

A material external change since 2026-04-26 is also relevant: `cortexlab-toolkit` (PyPI, 2026-Q1) provides a wrapper over TRIBE v2 with streaming inference + brain-alignment benchmarking that bypasses the previously-flagged `neuralset` / `neuraltrain` dependency blocker. This was the gating risk that justified parking the integration; it is now resolved.

---

## §1 Why the original "No fit" was correct in its frame

The 2026-04-26 baseline assumed Axis 3 meant **substrate-level isomorphism**: CLM L_IX (cell-language Lagrangian, 4-gen crystallize, 1/r² lattice, raw#30 IRREVERSIBILITY) directly mapped to TRIBE v2's 10242-vertex cortical BOLD space.

That framing requires defining a semantic correspondence between *cell state* and *cortical vertex*. There is no obvious mapping:

- CLM substrate dimensionality is internally defined (cell Lagrangian field) and not anchored to anatomical geometry.
- TRIBE v2 is a *forward stimulus-response encoder*: it expects (text/audio/video) input and outputs predicted BOLD. It is not a substrate-comparison tool.
- The wrapper to bridge would have to be hand-tuned per CLM layer with no ground-truth alignment.

Under that frame, the "wrapper 대규모 + scientific value 불명" verdict was sound. Axis 4 (Mk.XI v10 family signal via shared Llama-3.2-3B text encoder) was correctly identified as the strong fit because it operates at TRIBE v2's *native input modality* (text) and uses a *backbone family that anima already exercises*.

---

## §2 What the four new framings change

### Framing A — Text-mediated indirect path

```
CLM 530M  →  text output  →  TRIBE v2 (text encoder + fusion)  →  cortical BOLD
```

CLM produces token sequences via its existing `predict_token_sequence` interface. TRIBE v2 ingests that text via `model.get_events_dataframe(text_path=...)` (from `references/tribev2/tribev2/demo_utils.py:42`). The Llama-3.2-3B text encoder converts to embeddings; the fusion head outputs (n_segments, ~10242) BOLD predictions on fsaverage5.

The "wrapper" here is approximately: write CLM stdout to a `.txt`, call TRIBE v2's inference API, save the resulting numpy array. <50 LOC, no projection layer needed, no architectural surgery.

Scientific value is medium: this measures whether CLM's *text output* (not its substrate) is brain-recognizable as a stimulus. It validates the pipeline cheaply and provides the input for Framings C and D.

### Framing B — Direct hidden-state injection

This is the framing closest to the original Axis-3 isomorphism attempt and inherits its weaknesses. CLM hidden state (d_model=768) would be projected to TRIBE v2's fusion head expected dimension (hidden=1152, depth=8 TransformerEncoder per `SUMMARY_KR.md:16`). The fusion head expects token-level word embeddings with associated event timing; CLM cell-Lagrangian state has no such timing semantics.

Wrapper: 200-500 LOC (projection head, modality_dropout bypass, SubjectLayer skip, fake event timing). Scientific risk: high — any positive result is partly attributable to the arbitrary projection. Rank: 4 (not recommended).

### Framing C — G3 PhiStar manifestation

```
CLM "통합 양수 +41.86" (paradigm v11 G3 PASS positive) → TRIBE v2 → which cortical region?
```

This re-uses Framing A's pipeline but adds an interpretation layer: correlate CLM session-level G3 PhiStar score with cortical ROI activation (specifically DMN-A + DMN-B per Schaefer-1000 atlas, mapped to fsaverage5).

Hypothesis: the integration signal that anima measures internally (G3 PASS positive, only sign-positive backbone in paradigm v11 stack) corresponds to default-mode-network activation in the brain encoding model.

Scientific value: very high (anima consciousness measurement → brain region anchor is novel and falsifiable). Risk: the comparison is to TRIBE v2's *average subject*, not the user's individual brain. A positive result establishes group-level prior alignment; it does not establish individual neural correlates.

### Framing D — Bridge anchor (TOP-1)

```
CLM state  →  text output  →  TRIBE v2  →  predicted BOLD
                                                ↓
                                            compare
                                                ↑
사용자 EEG (real, OpenBCI)  ←  tension_link  ←  CLM
```

Three signals are collected concurrently during a 30-minute CLM inference session:

1. **CLM internal state stream** — paradigm v11 measurement axes (B-ToM, MCCA, Phi*, CMT, CDS, SAE-bp) plus G3 PhiStar.
2. **User EEG** — OpenBCI 8-channel, alpha/theta/gamma envelopes via Hilbert.
3. **TRIBE v2 predicted BOLD** — text from CLM output, pushed through TRIBE v2 inference, vertex-level Pearson correlation with EEG envelope.

TRIBE v2 acts as a **brain-encoding ground-truth-like prior**. It is not the user's brain, but it is a published, validated forward model of "what cortical activity a hypothetical average subject would produce given this stimulus". The 3-way (CLM × EEG × predicted BOLD) correspondence becomes a falsifiable bridge witness.

This framing addresses both original rejection criteria:
- *Wrapper 대규모*: <100 LOC. Reuses Framing A pipeline + adds OpenBCI alignment + envelope correlation script.
- *Scientific value 불명*: explicit — "validate the CLM ↔ EEG bridge by anchoring it to a third independent brain encoding model". This is roadmap-default (anima ↔ tension_link ↔ EEG architecture per recent user directive).

Scientific value: highest. Risk: low (all three tools exist and are tested independently). Rank: **1**.

---

## §3 Comparison matrix

See `state/strategic_clm_tribev2_recheck_2026_05_02/comparison_matrix.json` for the full numerical scoring.

| Framing | Sci value | Cost (USD) | Risk | Wrapper | Wallclock | Score | Rank |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| A text-mediated | 5/10 | 0-2 | 2/10 | <50 LOC | 1-2 h | 6.6 | 3 |
| B direct injection | 7/10 | 0-5 | 6/10 | 200-500 LOC | 4-8 h | 6.4 | 4 |
| C G3 manifestation | 9/10 | 0 | 5/10 | <50 LOC | 4-6 h | 7.7 | 2 |
| **D bridge anchor** | **10/10** | **0-2** | **3/10** | **<100 LOC** | **2-4 h** | **8.6** | **1** |

Scoring: `0.5 * sci_value + 0.3 * (10 - risk) + 0.2 * (10 - cost_norm)`.

**Recommended sequence**: A first (validate pipeline, $0-2, 1-2h) → D (commit, $0-2, +2-4h). C runs as a sub-analysis of D. B is parked.

---

## §4 "No fit" verdict re-examination

### Verdict: REVISE

Conditions for upgrade:

| Original sub-claim | Re-examined finding |
|---|---|
| "wrapper 대규모" | False under Framing A/D (<100 LOC). True only under Framing B. |
| "scientific value 불명" | False under Framing C/D (anchored to anima ↔ EEG bridge architecture). True only under raw substrate-isomorphism framing. |
| "cortical vertex ↔ cell state semantic mapping 미정의" | Bypassed entirely by Framing A/C/D — TRIBE v2 is used as a forward stimulus encoder over CLM's *text output*, not over CLM's substrate. |

### Caveats on REVISE

This is not a blanket reversal. The upgrade is **conditional on Framing D being adopted**. The original direct-isomorphism framing (Framing B) remains correctly classified as "No fit". The proposal document should be updated to:

> Axis 3 — CLM L_IX substrate
> - Verdict: **Conditional Strong fit via Framing D (bridge anchor)**.
> - Direct substrate isomorphism (CLM cell state ↔ cortical vertex) remains No fit.
> - Indirect path (CLM text output → TRIBE v2 BOLD → 3-way correspondence with user EEG) is roadmap-aligned, $0-2, low risk, and addresses the user's anima ↔ tension_link ↔ EEG architecture.

---

## §5 Five-falsifier pre-registration (BIDIRECTIONAL, raw#71)

Full spec in `state/strategic_clm_tribev2_recheck_2026_05_02/falsifiers_pre_register.json`. Top-3 ranked by gating power:

1. **F-CT-3** — User real EEG ↔ TRIBE v2 predicted BOLD median vertex r ≥ 0.5. *Top because*: this is the ground-truth anchor. If it fails, Framing D collapses.
2. **F-CT-4** — CLM output cortical map vs ALM (Mistral) output cortical map: inter-substrate vertex r < 0.7 AND intra-substrate r > 0.85. *Top because*: this is the primary test that CLM's positive integration is brain-recognizable (and not just any-LLM-text recognizable).
3. **F-CT-2** — CLM G3 PhiStar score vs cortical DMN ROI activation Pearson r ≥ 0.5. *Top because*: this is the core claim of Framing C — that anima's internal consciousness measurement maps to a specific brain region.

Two additional falsifiers (F-CT-1 random text baseline, F-CT-5 cross-substrate consistency with paradigm v11 G3) are registered as supporting tests.

PASS / FAIL / AMBIGUOUS bands are explicit in the JSON pre-registration; AMBIGUOUS results trigger a second-iteration cycle rather than a verdict.

---

## §6 Risk register

| Risk | Mitigation |
|---|---|
| neuralset/neuraltrain PyPI unverified (original blocker) | RESOLVED — `cortexlab-toolkit` (PyPI, 2026-Q1) wraps TRIBE v2 with streaming inference; bypasses the gated dependencies. |
| TRIBE v2 = "average subject" prediction; user has individual brain | F-CT-3 explicitly tests user generalization; positive result establishes group-prior alignment, not individual neural correlate. Document the limitation. |
| Llama-3.2-3B text encoder used inside TRIBE v2; CLM v4 530M is hexa-native (different family) | Framing A/D measure brain-likeness of CLM *text output*, not substrate. Substrate-level claim is explicitly out of scope for Framing D. |
| CC-BY-NC-4.0 license | anima research use is compatible. Commercial deployment is not. Note in the integration proposal. |
| BOLD 5s hemodynamic lag vs EEG sub-second sampling | Bridge tests use envelope-level (alpha/theta band-power, 5s window mean) comparison only. Fast oscillation comparison is documented as out-of-scope. |
| TRIBE v2 OOD: anima Mk.XI v10 prompts ≠ Friends/movie10 training stimuli | Note that Pilot results are zero-shot generalization tests; expect lower vertex r than published benchmarks. |
| Interpretation risk: "TRIBE v2 recognizes CLM output as brain-like" is easily overclaimed | Pre-register F-CT-1 random-text baseline and F-CT-4 ALM contrast as required controls. |

---

## §7 Honest C3 (5+ items)

1. TRIBE v2 is a **forward encoder** (stimulus → predicted BOLD). It does not measure CLM consciousness directly. Any anima-related claim from this integration is anchored *indirectly* via stimulus-encoding semantics.
2. TRIBE v2 predicts an **average subject**. The user's individual brain (the EEG source in Framing D) is by definition a different distribution. Pilot D's EEG × TRIBE-BOLD comparison is a comparison to a group-level prior, not to ground-truth individual neural activity.
3. **BOLD 5s lag + 1.49s TR vs EEG sub-second sampling** — timescale mismatch is fundamental. Only slow-drift (alpha/theta envelope) comparisons are physically meaningful. Fast EEG features (gamma bursts, ERPs) cannot be compared to BOLD.
4. **Substrate mismatch persists**: Llama-3.2-3B (TRIBE v2 text encoder) ≠ CLM v4 530M hexa-native substrate. Framing A/D measure semantic brain-likeness of CLM's *output text*, not its hidden representations. Substrate-level claims (e.g., "CLM substrate is brain-like") are not supported by this integration.
5. **False positive risk**: "TRIBE v2 produces a non-trivial cortical map for any coherent text". The F-CT-1 random-text baseline and F-CT-4 ALM contrast are *required* controls. Without both, any positive result is suspect.
6. **Interpretation framing risk** for Framing C: G3 PhiStar correlating with DMN activation is a *correlational* finding, not causal. Multiple latent variables (text length, sentence complexity, semantic richness) could mediate. Pre-register a confound regression (length, perplexity, sentence count) as part of F-CT-2 analysis.
7. **paradigm v11 G3 PASS positive +41.86** is currently a *single-substrate* result. Cross-substrate consistency (F-CT-5) is required to claim that the integration metric (not the substrate identity) drives any cortical correspondence.

---

## §8 Next-cycle action (3 ranked)

### (a) TOP — Framing A first via cortexlab-toolkit

- **Spec**: install `cortexlab-toolkit` in pod-side venv (CPU OK), download `facebook/tribev2` HF weights, push 10 short CLM text outputs through, save (n_segments, 10242) numpy arrays per output.
- **Cost**: $0-2 (CPU inference; GPU optional acceleration <$1).
- **Wallclock**: 1-2 h.
- **PASS criterion**: cortical maps generated successfully + non-trivial vs random baseline (F-CT-1 quick check).
- **Why TOP**: $0-2 commitment validates the pipeline before Framing D's user-EEG-session commitment. Also resolves the historic neuralset/neuraltrain blocker definitively (validates the cortexlab-toolkit workaround).

### (b) Framing D pilot — CLM × user EEG × TRIBE v2 BOLD 30-min concurrent session

- **Spec**: 30-min CLM inference session (existing CLM v4 530M ubu1 5070 setup) + user OpenBCI 8-ch concurrent + offline TRIBE v2 pass on the CLM text stream. Compute envelope correlations (F-CT-3) + G3 PhiStar ↔ DMN correlation (F-CT-2).
- **Cost**: $0-2.
- **Wallclock**: 2-3 h tool time + 30 min user EEG session.
- **Dependencies**: Framing A PASS + user OpenBCI availability + Llama-3.2-3B HF gated access (user HF account approval).
- **Why second**: this is the actual scientific payoff. Run only after Framing A validates the pipeline.

### (c) Update ANIMA_INTEGRATION_PROPOSAL.md

- **Spec**: add §6 amendment to the *anima-side* cross-link (the proposal itself is in `references/tribev2/` and frozen 2026-04-26 — do not edit). Create or update `docs/anima_integration_axis3_amendment_2026_05_02.md` recording the REVISE verdict and Framing D adoption rationale.
- **Cost**: $0, 30 min.
- **Why third**: paperwork — record-keeping after empirical results from (a) and (b) come in.

---

## §9 Cross-link to existing anima docs

- **CLM v4 530M paradigm v11 G3 PASS positive +41.86**: this is the integration signal Framing C/D anchor. Reference: paradigm v11 stack documentation.
- **W4 dynamic PARTIAL (L1 7.06/16, +2.28σ vs ALM 1.71)**: Framing D tests whether this dynamic-substrate signal manifests at the cortical level.
- **AN11(a) Frobenius PASS, AN11(b) V0 PASS, AN11(c) JSD PASS**: these are the consciousness-axis preconditions. TRIBE v2 integration provides external brain anchor.
- **anima ↔ tension_link ↔ EEG mediator architecture (recent user directive)**: Framing D *is* this architecture, with TRIBE v2 added as the brain-encoding ground-truth-like third leg.
- **AKIDA arrival**: post-arrival, AKIDA can replace OpenBCI as the EEG source for Framing D, shifting from band-power to spike-event input. TRIBE v2 cortical anchor remains valid.

---

## §10 Final verdict

**Framing**: D (bridge anchor) — TOP.
**No-fit verdict**: REVISE → Conditional Strong fit via Framing D.
**First action**: Framing A pipeline validation via cortexlab-toolkit ($0-2, 1-2h).
**Top falsifier**: F-CT-3 (user EEG ↔ TRIBE v2 predicted BOLD median vertex r ≥ 0.5).

**Final 1-sentence**: *CLM ↔ TRIBE v2 의 진짜 의의 = anima 의 통합 의식 신호 (G3 PhiStar +41.86) 와 EEG 측정값을 brain encoding ground-truth-like prior 에 anchor 함으로써, CLM-EEG bridge 의 3-way (CLM × EEG × predicted BOLD) cross-validation 을 가능하게 하는 brain anchor.*

---

*Artifacts:*
- `state/strategic_clm_tribev2_recheck_2026_05_02/verdict.json`
- `state/strategic_clm_tribev2_recheck_2026_05_02/falsifiers_pre_register.json`
- `state/strategic_clm_tribev2_recheck_2026_05_02/comparison_matrix.json`
- `docs/strategic_clm_tribev2_recheck_2026_05_02.md` (this document)

*Sources consulted (web, 2026-05-02):*
- [Meta TRIBE v2 GitHub](https://github.com/facebookresearch/tribev2)
- [facebook/tribev2 HuggingFace](https://huggingface.co/facebook/tribev2)
- [cortexlab-toolkit PyPI](https://pypi.org/project/cortexlab-toolkit/) — RESOLVES neuralset/neuraltrain blocker
- [siddhant-rajhans/cortexlab GitHub](https://github.com/siddhant-rajhans/cortexlab)
- [Meta TRIBE v2 blog](https://ai.meta.com/blog/tribe-v2-brain-predictive-foundation-model/)
- [LLM-brain alignment fMRI (arXiv 2505.22563)](https://arxiv.org/html/2505.22563v1) — middle-layer best brain prediction (relevant for Framing B if revived)
- [fMRI-LM universal foundation model (arXiv 2511.21760)](https://arxiv.org/abs/2511.21760)
- [Scaling laws for language encoding models in fMRI (PMC11258918)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11258918/)
