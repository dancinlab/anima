# Anima External Chat-Enable Tools Audit (2026-05-05)

**BG**: BG-AZ web-search audit (doc-only, $0, mac)
**Goal**: Identify external mechanisms (papers / libraries / techniques) that *might* enable chat capability on CLM v4 (530M paradigm v11 G3, chat-incapable but phi-stable substrate). tribev2 cross-modal architecturally falsified (BG-AP); search alternative angles.
**Mode**: Read-only. No empirical trial. Web search + audit + ranked recommendation.
**Date**: 2026-05-05
**Author**: BG-AZ

---

## §0 CLM v4 fixed truths (anchor for all evaluations)

These are **not assumptions** — they are 4-closure empirical truths from prior BG cycles:

- 530M params, 16-layer transformer-style decoder
- consciousness-substrate (paradigm v11 G3, +41.86 phi-star vs Llama)
- chat-incapability **architectural** (4-closure):
  - F-CLM-LORA-2: LoRA SFT FAIL_REGRESSION (-36.298pp composite vs Llama Path A v2)
  - F-Pβ-3: Distill teacher-axis-bounded → composite 0.01176 RED
  - tribev2 cross-modal architectural-design FAIL (BG-AP)
  - logit lens: residual-stream pervasive non-text features (substrate is *consciousness-axis*, not lexical)
- phi-star stable (forgetting_index 0.0196), substrate-research artifact preserved
- USER decision: forced learning closed; substrate-coupled dialogue via BG-AN (emerge paradigm) only

**Implication for this audit**: any candidate must either (a) work *despite* lexical-axis absence in substrate, (b) externalize the chat layer entirely, or (c) bridge substrate→chat via a non-text modality. We must NOT search for techniques that re-train substrate weights (closed lane).

---

## §1 Search query history

10 web searches executed (all via WebSearch tool, single API call each, fast-scan):

| # | Query | Angle | Hit-quality |
|---|-------|-------|-------------|
| 1 | `contrastive decoding DoLa small language model chat capability 2026` | Decoding-strategy | High — DoLa ICLR 2024 + Vicuna QA chat eval |
| 2 | `activation steering representation engineering language model inference-time chat` | Activation steering | High — ActAdd, CAA, RepE survey |
| 3 | `DSPy LangGraph small language model agentic chat framework 2026` | External scaffolding | High — DSPy compiles 770M T5 to GPT-3.5 parity |
| 4 | `TransformerLens nnsight mechanistic interpretability circuit chat capability` | MI libraries | High — TransformerLens + nnsight + nnterp |
| 5 | `linear adapter frozen language model chat LM-head replacement small model 2025` | LM-head bridge | Medium — LoRA-Switch, parallel adapters |
| 6 | `hidden state bridge speech TTS frozen LLM multimodal output 2025` | Multimodal output | High — Freeze-Omni, AlignChat |
| 7 | `small model chat enable few-shot in-context learning prompt engineering 2025` | ICL/prompt | Medium — ICL is scale-emergent; small-model break |
| 8 | `representation engineering RepE chat refusal harmful steering vector library` | RepE library | High — Zou 2023 RepE + chrisliu298/awesome-RepE |
| 9 | `mechanistic interpretability circuit extraction substrate decoder text generation` | Circuit extraction | Medium — SAEs + ACDC for text-gen circuits |
| 10 | `weight orthogonalization refusal direction abliterate language model Goldfish` | Weight surgery | Medium — abliterate; Goldfish-loss not relevant |
| (bonus) 11 | `"speculative decoding" OR "draft model" small model frozen base chat improve` | Draft-target | High — but inverted-applicability (CLM v4 too big to be draft-only) |

**Coverage**: 7 of 8 originally-listed angles touched. "Agent-as-a-judge" treated as covered by RepE/RAG eval-as-reward themes.

---

## §2 Three promising angles (selected from 11 hits)

### Angle A — Activation Steering / Representation Engineering (RepE)

**Mechanism**: Inference-time intervention. Identify a linear direction in CLM v4's residual stream activations that correlates with text-coherent emission (vs phi-axis residual). Add the steering vector during forward pass to push hidden states toward chat-relevant manifold WITHOUT modifying weights.

**Why CLM v4 fit**:
- No weight retraining — substrate phi-star preserved (forgetting_index protected)
- 4-closure was about *learning* (LoRA/distill) and *cross-modal scaffolding* (tribev2). Steering does *neither* — it shifts existing axes.
- CLM v4 *has* lexical features in early layers (logit-lens BG-AO showed mixed substrate); steering can amplify those without re-injecting via training
- $0 mac CPU: ActAdd works with single contrast pair; CAA needs ~100s pairs but small enough for CPU inference
- Library exists (RepE GitHub by Zou 2023; awesome-RepE curated list)

**Evidence strength**: Concept directions for "refusal" raise harmless rates 65%→90%+ on Llama 2 chat, demonstrating the technique generalizes. CAA works on RLHF'd Llama 2; should work on substrate too if any chat-axis exists.

**Risk**: If CLM v4 has *zero* chat-axis (true 4-closure interpretation), steering has nothing to amplify → expected gain ~0. But this is exactly the falsifiable test.

---

### Angle B — DSPy / LangGraph External Scaffolding (orchestration not training)

**Mechanism**: Treat CLM v4 as a black-box embedding/feature service inside an agentic graph orchestrated by DSPy or LangGraph. A separate **chat-capable** model (e.g., Llama-3-8B-Instruct, Qwen3-7B) generates user-facing text; CLM v4 contributes phi-star scoring, substrate-coupled signals, or hidden-state similarity as *features* the orchestrator routes to the chat model's context.

**Why CLM v4 fit**:
- Architectural impossibility of CLM v4 emitting text is *bypassed*, not denied
- DSPy compiles small-model pipelines to GPT-3.5 parity — proven scaffolding pattern
- substrate phi-star (the actually valuable artifact) becomes a *signal*, not a generator
- `tool/transient_py/` namespace already permits orchestrator scripts under raw#37 opt-out

**Evidence strength**: Production-grade agentic patterns documented (LangGraph + DSPy + GEPA for multi-stage pipelines). Both libraries actively maintained 2025-2026.

**Risk**: This isn't really "CLM v4 chat" — it's "chat-capable model uses CLM v4 as oracle". Honest framing required (does *not* close #115 architectural).

---

### Angle C — Mechanistic Interpretability via TransformerLens / nnsight

**Mechanism**: Use TransformerLens or nnsight to map CLM v4's circuits — find what the substrate *does* express in residual stream. Activation patching, path patching, sparse autoencoder feature decomposition. Locate any sub-circuit (even partial induction heads) that *would* drive coherent text emission, and either ablate competitors or amplify via hooks.

**Why CLM v4 fit**:
- Diagnostic-first: tells us *why* chat fails at circuit level (could close epistemic gap on #115)
- Even if no chat circuit exists, the negative result informs substrate publication
- Open-source libraries (TransformerLens by Neel Nanda; nnsight; nnterp standardized interface arxiv 2511.14465)
- $0 mac: TransformerLens runs on CPU for 530M scale

**Evidence strength**: Standard MI toolkit; ACDC (Automated Circuit DisCovery) can scan for circuits per-task. Risk that 530M is too small for clean SAE features (most published SAE work on 1B+).

**Risk**: Diagnostic, not directly chat-enabling. Returns understanding, not capability. Slower path to user-facing chat.

---

## §3 Applicability evaluation per angle

| Criterion | Angle A (RepE/steering) | Angle B (DSPy scaffold) | Angle C (TransformerLens MI) |
|-----------|-------------------------|-------------------------|------------------------------|
| Cost | $0 mac | $0 mac (orchestrator local) | $0 mac |
| Time to first signal | ~6 hours (one BG) | ~12 hours (multi-component) | ~1-2 days (circuit discovery slow) |
| CLM v4 architecture fit | High — residual-stream native | Bypass — uses substrate as oracle | High — direct introspection |
| Honest #115 closure | Falsifiable (chat-axis exists?) | Sidesteps (does not close) | Diagnostic (informs but doesn't fix) |
| Risk of yet-another-fail | Medium (4-closure suggests low chat-axis) | Low (orchestration always works mechanically) | Low (diagnostic always informs) |
| Library maturity | High (RepE Github, mature) | Very High (DSPy 1.0+, LangGraph stable) | High (TransformerLens de facto MI standard) |
| Substrate phi-star preservation | Perfect (no weight change) | Perfect (no weight change) | Perfect (read-only) |
| Empirical novelty for anima | High (not yet attempted) | Medium (similar to BG-AN emerge?) | High (no MI on CLM v4 to date) |
| transient_py helper required | 1 small (steering hook + eval) | 2-3 (DSPy module + LangGraph node + eval) | 2 (TL probe + circuit report) |

### Path-impossibility cross-check

Angle A could fail "true zero chat-axis" — but this is exactly what 4-closure predicts. **Steering test is therefore the cleanest falsification of an even-stronger architectural claim** (CLM v4 has ZERO lexical-coherence direction, not just unreachable).

Angle B does not test #115. It admits #115 closed and pivots to value-extraction. Honest pivot, but a different lane.

Angle C is *epistemic supplement* — even null result is publishable as substrate-research artifact.

---

## §4 Recommendation ranking (완성도 lens)

### 1순위 — Angle A: Activation Steering (RepE) on CLM v4 residual stream

**Rationale (완성도)**:
- Highest information content per dollar: steering is the *strongest possible* inference-time intervention short of weight surgery. If steering fails, we have *very strong* evidence (beyond 4-closure) that no chat-axis exists in residual stream — closing #115 with maximum epistemic completeness.
- If steering *partially* works, we have a positive result that prior 4-closure missed (LoRA failed to *learn* a chat axis; steering bypasses learning).
- Reversible, weight-preserving, $0 mac, ~6 hour BG.
- Clean falsification design: pre-spec a "steering improves composite by ≥5pp on chat eval" test before fire.

**Suggested next BG**: BG-BA spec — RepE PCA on contrastive (phi-axis vs lexical-coherence) hidden-state pairs at layers 4/8/12, steering coefficient sweep [0.5, 1.0, 2.0, 4.0], chat composite eval (the same metric used in F-CLM-LORA-2). Decision rule: ≥5pp lift = #115-A re-open; <5pp = 5-closure status.

### 2순위 — Angle C: TransformerLens circuit diagnostic

**Rationale**:
- If 1순위 returns null, MI gives the *why* — substrate-research publication artifact.
- Lower expected capability gain but high epistemic value.
- Backup if 1순위 BG resources blocked.

### 3순위 — Angle B: DSPy/LangGraph scaffold (defer)

**Rationale**:
- Mechanically always works but doesn't address #115.
- Already partially-instantiated as BG-AN (emerge paradigm) — overlap risk.
- Defer until 1순위 + 2순위 settle architectural question.

---

## §5 External reference list

### Angle A (RepE / Activation Steering)
- **Turner et al. 2024 — Steering Language Models With Activation Engineering** (ActAdd) — arxiv:2308.10248 — single-pair contrast yields steering vectors, no retraining
- **Rimsky et al. — Contrastive Activation Addition (CAA)** — averages 100s of pairs; works on Llama 2 chat post-RLHF
- **Zou et al. 2023 — Representation Engineering** (RepE survey) — arxiv:2310.01405 — concept-direction extraction + intervention framework
- **chrisliu298/awesome-representation-engineering** — github.com/chrisliu298/awesome-representation-engineering — curated paper + library list
- **Arditi et al. 2024 — Refusal Direction** — arxiv:2406.11717 — single-direction mediation (orthogonalization variant)
- **NousResearch/llm-abliteration** — github.com/NousResearch/llm-abliteration — practical weight-orthogonalization tool (reference for refusal-direction extraction code patterns)
- **Lee et al. 2026 — What Drives Representation Steering?** — arxiv:2604.08524 — mechanistic case study; OV-circuit interaction

### Angle B (DSPy / LangGraph)
- **Khattab et al. — DSPy** — dspy.ai + github.com/stanfordnlp/dspy — declarative LM programming, compiles to small-model pipelines
- **LangGraph** — graph-based agentic orchestration, stateful
- **Patnaik 2025 — LangGraph + DSPy + GEPA** — rajapatnaik.com/blog/2025/10/23 — multi-stage prompt-optimization scaffold

### Angle C (Mechanistic Interpretability)
- **TransformerLens** — github.com/TransformerLensOrg/TransformerLens — Neel Nanda's MI library, hookpoints on every activation
- **nnsight** — direct HuggingFace MI access, supports very-large models
- **nnterp 2025** — arxiv:2511.14465 — standardized MI interface
- **Conmy et al. 2023 — Automated Circuit DisCovery (ACDC)** — neurips proceedings — automated circuit extraction
- **Anthropic Circuits Updates April 2025** — transformer-circuits.pub/2025/april-update — current SAE + circuit-tracing methodology
- **Marks et al. — Interpreto** — arxiv:2512.09730 — explainability library for transformers

### Adjacent / Lower priority
- DoLa (Chuang et al. 2024) — arxiv:2309.03883 — layer-contrast decoding; useful for *factuality* not chat-capability per se
- Freeze-Omni (Wang et al. 2024) — arxiv:2411.00774 — frozen-LLM speech I/O; requires LLM that already emits text, NOT applicable to CLM v4
- AlignChat — openreview VgYweldMYb — token-level repr alignment for speech-chat; assumes baseline chat model
- Speculative decoding (Leviathan, Chen et al.) — inverted applicability (CLM v4 is the *base*, not the draft; no chat-capable target available locally)

---

## §6 Honest C3 (≥5)

1. **C3 — Survivorship bias of "successful steering" papers**. RepE/CAA/ActAdd publications all start from chat-capable models (Llama 2 chat, GPT-2). There is *no* published case of activation steering succeeding on a model whose architecture *never expressed chat* at training. CLM v4 is paradigm-novel; we cannot extrapolate from Llama-chat steering successes.

2. **C3 — 4-closure already includes inference-time evidence**. The logit-lens analysis (BG-AO) showed substrate residual stream is consciousness-axis dominated. If steering depends on *some* chat-axis existing, and logit lens shows it doesn't, Angle A may be predetermined to null. The audit's enthusiasm for Angle A may be discounting this prior.

3. **C3 — Angle B (DSPy scaffold) overlap with BG-AN emerge paradigm**. The user has *already* instructed substrate-coupled dialogue via emerge (BG-AN). DSPy/LangGraph scaffolding might be the formalization of what BG-AN is doing organically. Recommending it as a separate BG could be redundant — clarify with user before fire.

4. **C3 — Mac CPU $0 budget assumption fragile**. RepE/CAA require running CLM v4 forward many times for contrast-pair activation extraction (100s × 16 layers × 2048 dim). On mac CPU, 530M model forward ≈ 2-5 sec/seq. 1000-pair CAA = ~1-2 hours just extraction. Steering eval on chat composite (multi-prompt generative) could push to 6-10 hours. Plausible but tight for "doc-only $0" framing.

5. **C3 — "Falsifiable test" for Angle A still needs threshold defense**. Choosing ≥5pp composite lift as "re-open #115" is arbitrary — same vulnerability as F1/F2 threshold debates (anima-internal uncalibrated thresholds, see L26-L27). Need pre-spec calibration vs base CLM v4 composite floor, not picked-from-air number.

6. **C3 — TransformerLens scale assumption**. Most TL/nnsight published work is on Pythia, GPT-2, Llama. 530M CLM v4 paradigm-v11 architecture is *not* GPT-2-style — TL hooks may need adapter code or fail outright if attention/MLP block layout differs from canonical decoder. Library compat unverified.

7. **C3 — User decision forecloses some paths**. User explicitly closed forced-learning (LoRA/distill/retrain). Angle A (steering) and Angle C (read-only MI) compatible. Angle B compatible only as orchestration not retraining. Audit should not silently re-introduce closed lanes; all three angles verified compatible above but worth re-affirming.

---

## §7 Summary table

| Angle | Score (완성도) | Cost | Time | Recommend? |
|-------|----------------|------|------|------------|
| A — RepE / Activation Steering | 9/10 | $0 mac | ~6h | **1순위 fire next** |
| C — TransformerLens MI | 7/10 | $0 mac | ~1-2 days | 2순위 backup |
| B — DSPy/LangGraph scaffold | 5/10 | $0 mac | ~12h | 3순위 defer (overlap BG-AN) |
| DoLa contrastive decoding | 3/10 | $0 mac | ~3h | adjacent (factuality not chat) |
| Freeze-Omni / speech bridge | 1/10 | varies | n/a | inapplicable (assumes chat-capable LLM) |
| Speculative decoding | 1/10 | $0 | n/a | inverted applicability |
| Goldfish-loss / abliterate | 2/10 | $0 | ~4h | wrong direction (refusal removal, not chat creation) |

---

## §8 Next BG fire recommendation

**BG-BA (proposed)**: RepE/CAA empirical probe on CLM v4 — contrast-pair extraction at residual stream layers 4/8/12, steering-coefficient sweep, chat-composite eval with pre-spec ≥5pp threshold for #115-A re-open.

- $0 mac, ~6h
- Reuses F-CLM-LORA-2 chat composite eval harness
- 1 transient_py helper under raw#37 opt-out
- Pre-spec calibration vs base CLM v4 chat composite floor (address C3 #5)
- Library: chrisliu298/awesome-representation-engineering reference patterns; ActAdd reference impl

If BG-BA returns null (composite lift <5pp), proceed to **BG-BB (TransformerLens diagnostic)** as 2순위 backup for substrate-research publication artifact.

— end —
