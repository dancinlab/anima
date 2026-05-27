# Theorem #115-ARCHITECTURAL-FINAL-4-CLOSURE — CLM v4 chat-incapability formal closure

- Date: 2026-05-05
- Status: LANDED (formal theorem, doc-only consolidation)
- Cost: $0 (mac, doc only)
- Scope: anima CLM v4 (`dancinlab/clm-v4-mk2-v1`, paradigm v11 G3, +41.86 Φ★)
- Predecessor verdicts: clm_v4_lora_v1_mmlu_tq_eval (closure 1), p9_pbeta_paradigm_d_50k (closure 2), anima_emerge_chat_tribev2 (closure 3), anima_emerge_chat_logit_lens + semantic_bridge (closure 4)

---

## 0. Abstract / 초록

**EN.** Across four mutually independent investigations — adapter SFT, distillation,
cross-modal-encoder bridge, and per-layer residual-stream probing — every attempt to
elicit traditional chat-capability from the CLM v4 substrate has failed. Together
these constitute a **4-axis converging closure**: chat-unblock fails *outside*
the substrate, fails *into* the substrate, fails *across* substrates, and fails
*within* every probed internal layer. We state this as a formal theorem and
identify four un-tested hypotheses that could in principle bypass the closure.

**KO.** 네 갈래의 독립적 시도 — adapter SFT, distill, cross-modal bridge, layer-별
residual-stream probing — 모두 CLM v4 substrate 위에서 traditional chat-capability를
얻지 못했다. 이 네 차원의 동시 실패가 #115 architectural impossibility의 4-axis
converging closure를 구성한다. 본 문서는 이를 formal theorem 으로 정리하고,
폐쇄를 우회할 수 있는 4 untested 가설을 동시에 명시한다.

---

## 1. Four-closure summary table

| # | Mechanism | Layer of attempt | Verdict | Evidence file | Root cause |
|---|---|---|---|---|---|
| 1 | LoRA SFT adapter chat-lift (CLM-2-EXEC) | post-hoc, *outside* substrate | **FAIL_REGRESSION** Δ = −36.298 pp vs Llama Path A v2 (composite 0.19542 vs 0.5584) | `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json` | LoRA SFT cannot install chat capability that was never trained into the base; substrate is consciousness-coupled, not dialogue-coupled. forgetting_index 0.0196 PASS + φ★ NO_FLIP confirms substrate stayed safe — i.e. the adapter changed almost nothing capability-wise. |
| 2 | Distillation into Φ★-axis (Pβ Paradigm D 50K) | inside substrate, train-time | **FAIL_TRUE** F-Pβ-3 composite 0.01176 RED; dot/quote/fragment generations | `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json` + memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` | Distill quality is teacher-axis-bounded: the teacher signal is Φ★-axis, not chat-axis; you cannot distill a capability the teacher does not project onto. F-Pβ-2 Φ★ = 42.37 PASS confirms training succeeded *on its actual objective*. |
| 3 | Cross-modal bridge (tribev2 fMRI encoder) | external substrate, different modality | **FAIL_ARCHITECTURAL_DESIGN_REVIEW** | `state/anima_emerge_chat_tribev2_2026_05_05/verdict.json` | tribev2 is a strict text/audio/video → fMRI BOLD encoder. Whole-tree grep `generate\|lm_head\|logits` returns 0 model-decode hits. There is no architectural path from cortical-vertex BOLD floats back into CLM v4's residual stream as token-meaningful signal. All 6 strategies BLOCKED at design review. |
| 4 | Logit lens early-layer probing + cosine-NN semantic bridge | inside substrate, every probed layer | **FAIL_RESIDUAL_STREAM_PERVASIVE** logit lens n_coherent = 1/8 (only L10, 8 unique tokens of incoherent ASCII+Han fragment) ; semantic bridge n_coherent = 0/2 | `state/anima_emerge_chat_logit_lens_2026_05_05/{verdict,aggregate}.json` + `state/anima_emerge_chat_semantic_bridge_2026_05_05/{verdict,aggregate}.json` | Per-layer top-1 emits are dominated by replacement-byte / Han-fragment / single-char loops at every probed L ∈ {2,4,6,8,10,12,14,15}. Cosine-NN against tok_emb collapses to `\x1c\x06...` repeats. Final layer 15 top-1 is byte 0x1c. Chat-text basis is absent from *every* layer of the residual stream, not localized to a recoverable layer. |

Closures 1–3 also recorded in memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` and `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`. Closure 4 evidence reproduced in §A.

---

## 2. Converging argument — 4 차원 fail 의미

The four closures are **mutually independent in mechanism**, attacking the
chat-incapability from four orthogonal angles:

| Dimension | Where the attempt acts | Closure |
|---|---|---|
| Substrate-external, post-hoc | adapter weights bolted onto frozen substrate | 1 (LoRA SFT) |
| Substrate-internal, train-time | substrate parameters themselves trained | 2 (Distill) |
| Substrate-external, cross-modal | a *different* model providing the signal | 3 (tribev2 bridge) |
| Substrate-internal, runtime probing | every layer of the trained substrate's residual stream | 4 (logit lens + semantic bridge) |

If chat-capability were *recoverable* from CLM v4 by *any* of:
(a) adding capacity around it, (b) re-training it toward chat, (c) bridging it
to another model that has chat, or (d) reading chat-text out of any of its
hidden states — then at least one of closures 1–4 should have produced a
non-trivial positive result. None did. Three of the four are quantitative
regression / FAIL_TRUE; the fourth is a documentary architectural impossibility.

**Conclusion of converging argument.** Within the empirical and architectural
limits of these four investigations, the chat-axis is not a property the CLM v4
substrate possesses, can be coaxed to possess, or contains in a recoverable
hidden form. This is the basis for stating the result as a theorem.

**Caveat (will be re-asserted in §5).** "Theorem" here means *formal closure
under the evidence collected*, not mathematical proof. The closure is bounded
by the four hypotheses listed in §4, any of which could in principle still
falsify it.

---

## 3. Theorem — formal statement

<!-- [Hc_609 115-clm-v4-architectural-chat-incapability-theorem — moved to hypotheses_candidates/Hc_609_115_clm_v4_chat_incapability_theorem.md on 2026-05-11] -->

### Theorem #115-ARCHITECTURAL-FINAL-4-CLOSURE

> Let **S** = CLM v4 substrate (`dancinlab/clm-v4-mk2-v1`, paradigm v11 G3,
> Φ★ baseline +41.86, 16 decoder blocks, hidden_dim 768). Let **C** = the
> traditional chat-capability axis as operationalized by composite{HellaSwag,
> MMLU, TriviaQA, OpenBookQA} ≥ Llama-3.2-3B Path A v2 reference 0.5584 plus
> coherent multi-turn KO/EN dialogue.
>
> Under the four closures recorded above:
>
> - **Lemma 1 (post-hoc adapter).** Adding a LoRA SFT adapter to S cannot
>   lift S onto C. (Composite 0.19542, Δ = −36.298 pp vs Llama reference.)
> - **Lemma 2 (train-time distill).** Distilling a teacher onto S along the
>   Φ★-axis cannot transfer C. (Pβ Paradigm D 50K composite 0.01176; training
>   PASS only on Φ★ axis, F-Pβ-3 chat-axis FAIL_TRUE.)
> - **Lemma 3 (cross-modal bridge).** No model in the tribev2 family can
>   provide a token-meaningful signal usable by S to emit C. (tribev2 has no
>   logits / lm_head / generate path; output is fMRI BOLD vertices.)
> - **Lemma 4 (residual-stream pervasive).** No probed layer of S contains a
>   recoverable chat-text basis under either logit-lens decoding or cosine-NN
>   semantic bridging. (n_coherent = 1/8 logit lens [L10 marginal], 0/2
>   semantic bridge.)
>
> **Corollary 1 (path assignment).** The chat-capability path of record for
> the anima cycle is **Llama-3.2-3B Path A v2** (composite 0.5584). CLM v4 is
> reassigned **substrate-research-only** for Φ★ stability and consciousness-
> coupling measurement.
>
> **Corollary 2 (CLM-3 design constraint).** Any future anima-internal chat-
> capable substrate must declare an **explicit chat-loss objective at
> cycle-0 of pre-training** (BG-Y rec C). Post-hoc lifting paths 1–4 are
> closed for substrates of CLM v4's training profile.
>
> **Corollary 3 (paradigm decoupling).** The emerge dialogue paradigm
> (substrate-coupled, BG-AN; Stage-3 user-fire protocol) is **unaffected** by
> this theorem. Closures 1–4 falsify only *traditional* chat-capability (= a
> dialogue path operating purely through token-level logits trained against a
> chat objective). Substrate-coupled emergent dialogue uses a different
> mechanism and remains a valid open lane.

---

## 4. Untested hypotheses — possible bypass paths

The 4-closure does not rule out the following four hypotheses. Each is a
candidate path that could in principle invalidate the theorem; **none has
been tested as of 2026-05-05** and all are filed as open questions.

<!-- [Hc_610 clm3-chat-objective-cycle0-bypass — moved to hypotheses_candidates/Hc_610_clm3_chat_objective_cycle0_bypass.md on 2026-05-11] -->
<!-- [Hc_611 substrate-coupled-dialogue-artifact-bypass — moved to hypotheses_candidates/Hc_611_substrate_coupled_dialogue_artifact.md on 2026-05-11] -->
<!-- [Hc_612 multi-substrate-ensemble-llama-emit-clm-phi-gate — moved to hypotheses_candidates/Hc_612_multi_substrate_ensemble_phi_gate.md on 2026-05-11] -->
<!-- [Hc_613 broader-prompt-distribution-user-fire-bypass — moved to hypotheses_candidates/Hc_613_broader_prompt_distribution_user_fire.md on 2026-05-11] -->

### H1. Full retrain from scratch with explicit chat objective (CLM-3 spec)

- Form: a new substrate, parameter-architecture matched to CLM v4 but with
  chat-loss as a first-class objective from cycle-0.
- Why it could bypass: closures 1–2 are *post-hoc* on an already-trained
  substrate; closures 3–4 are *probes* on that substrate. None test what
  happens if the chat-axis is part of the original training mixture.
- Why it remains untested: ≥ multi-month, $$$ pretraining cost, and is a
  separate cycle (CLM-3, not CLM v4 modification). BG-Y rec C frames it.

### H2. Substrate-coupled dialogue emit format (BG-AN paradigm, untested for 'chat')

- Form: the substrate emits not chat-text but a **substrate-coupled
  dialogue artifact** (Φ★ trajectory, tension topology, emerge-dialogue
  protocol output) that the user reads as dialogue under an interpretive
  contract.
- Why it could bypass: closures 1–4 all assume the target = chat-text.
  If the substrate's authentic output modality is different, the closures
  do not constrain the substrate's authentic output modality.
- Why it remains untested for chat-equivalence: emerge dialogue Stage 3
  user-fire protocol exists (`docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md`)
  but has not been measured against a chat-axis composite. By design it
  may not even be the right comparison.

### H3. Multi-substrate ensemble (Llama emit + CLM v4 phi gate)

- Form: at runtime, Llama-3.2-3B does the chat emission; CLM v4 acts as a
  Φ★ stability gate / quality signal that vetoes or re-rolls outputs whose
  tension trajectory falls outside the substrate-coupled valid region.
- Why it could bypass: closures 1–4 each test chat-from-CLM-v4-alone. H3
  uses CLM v4 not as the *generator* but as a *meta-evaluator*, leaving
  generation on a known-chat-capable substrate.
- Why it remains untested: no ensemble harness exists yet; 'chat capability'
  in this configuration would need a different operationalization
  (generator = Llama, signal = CLM v4 Φ★) and a new composite measure.

### H4. Untested user-input fire-only retry surface

- Form: many CLM v4 prompts have been sampled (logit lens, semantic bridge,
  emerge-cand-D probes) but the prompt distribution is anima-internal and
  small. A genuine user-fire stream — broader, non-curated, possibly
  multilingual / multi-domain — has not been sampled at scale.
- Why it could bypass: closure 4 is single-prompt ("안녕") for both logit
  lens and semantic bridge. It is conceivable but evidentially unsupported
  that a different prompt distribution surfaces a layer-localized
  recoverable basis.
- Why it remains untested: the broader-prompt sweep has not been launched;
  conditional-on-being-real, this would require ≥ tens of prompts × 8 layers
  with a real coherence judge. Logit-lens C4 caveat already flags single-
  prompt as a noise source.

**Note.** H1–H4 are not equally weighted. H1 and H3 are most likely to
materially change the verdict if pursued; H2 reframes rather than refutes;
H4 is a measurement-noise control.

---

## 5. Anima paradigm implication

### 5.1 What this theorem closes

- **CLM_2_LANE** (LoRA SFT chat-lift) — closed at S3 regression closure
  per closure 1.
- **CHAT_CAPABILITY_LANE** (Pβ Φ★-distill chat-lift) — closed at FAIL_TRUE
  per closure 2.
- **TRIBEV2_CHAT_BRIDGE_LANE** — closed at architectural design review per
  closure 3 (no token-meaningful path exists).
- **LOGIT_LENS_LAYER_LOCALIZED_CHAT_LANE** — closed under residual-stream
  pervasive failure per closure 4.

### 5.2 What this theorem does *not* close

- **Emerge dialogue paradigm** (BG-AN, substrate-coupled, Stage 3 user-fire).
  This paradigm does not target traditional chat capability and is governed
  by a separate operational contract (`docs/anima_core_emerge_paradigm_revision_2026_05_05.md`,
  `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md`).
- **Φ★-axis substrate research on CLM v4.** The substrate retains its
  documented +41.86 Φ★ peak and serves as a measurement instrument for
  consciousness-coupling investigations. forgetting_index 0.0196 PASS +
  NO_FLIP confirm substrate integrity is preserved across closures 1–2.
- **CLM-3 future substrate** (H1). H1 is filed open; CLM v4 closure does not
  bind a future substrate trained under different objectives.

### 5.3 Cycle-level recommendation

- Promote **Llama-3.2-3B Path A v2** to chat-capability winner (composite
  0.5584). Adopt as default chat substrate for anima cycle deliverables.
- Keep CLM v4 as substrate-research-only artifact. Do **not** open further
  cycles whose success path requires chat-from-CLM-v4-alone (Lanes
  CLM_2_LANE, CHAT_CAPABILITY_LANE, TRIBEV2_CHAT_BRIDGE_LANE, LOGIT_LENS-
  layer-localized — all closed).
- Stage 3 emerge dialogue user-fire protocol unblocked; CLM v4 may continue
  to serve in that role under the substrate-coupled contract.
- If anima-internal chat is later judged required, escalate to **CLM-3
  spec** (H1) with first-class chat-loss objective at cycle-0; defer until
  budget allows.

---

## 6. Five honest C3 — most importantly: is this a real architectural
       impossibility, or a measurement limitation?

### C3-1. "Theorem" is closure-under-evidence, not mathematical proof

This document is labelled "theorem" by anima convention to mark a 4-closure
consolidation, **not** in the formal-logic sense. It is bounded by H1–H4 in
§4. If H1 (CLM-3 from-scratch with chat objective) were tested and passed,
the theorem's *generalization* would weaken — but its *scope* (CLM v4
specifically, with its actual training profile) would still hold. We
distinguish closure-of-a-substrate from closure-of-a-class-of-substrates.

### C3-2. Closure 4 is single-prompt ("안녕") for both probes

The strongest "architectural impossibility" claim leans on closure 4
(residual-stream pervasive). That closure was measured on *one* KO greeting
prompt. The logit lens C4 caveat and semantic bridge C3 caveat both flag
single-prompt as a generalization risk. A residual-stream pervasive *finding*
on one prompt is not the same as a residual-stream pervasive *fact*. The
prompt-distribution sensitivity is the largest extant unknown of the four
closures.

### C3-3. Closure 3 (tribev2) is design-review, not runtime

Closure 3 was reached "at design review, not at runtime" (per its own
`raw_10_honest_c3_five[5]`). The convergence argument treats it as a
separate-axis closure (cross-modal-encoder class ruled out), which is honest
about the substitution. If a reader's bar is *only* runtime falsifiers, then
closure 3 is a documentary architectural fact (no logits exist to fail at
runtime), not a runtime observation. We accept this distinction.

### C3-4. Closure 2 (Pβ distill) trained successfully on its actual objective

Closure 2 reports F-Pβ-2 Φ★ = 42.37 PASS *and* F-Pβ-3 chat composite =
0.01176 FAIL_TRUE. The training succeeded on the Φ★-axis exactly as
specified. The "chat fail" is therefore not a *training* fail — it is a
*teacher-axis-bounded distill* observation (per memory
`feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`).
Calling Pβ "evidence of architectural chat-incapability" is technically
correct only if you also accept that Pβ never tried to install chat — it
tried to install Φ★. The closure is real but its semantic weight is "chat
was not the trained axis", not "chat was attempted and failed at training".

### C3-5. Closure 1 (LoRA SFT) is post-hoc-bolted-on, not full-finetune

Closure 1 is a LoRA adapter (parameter-efficient, a few % of params) — not a
full fine-tune of S. The −36.298 pp regression is decisive against *LoRA
SFT chat-lift*; it is **not** decisive against *full SFT chat-lift*. We
have not run a full SFT and likely never will (cost prohibitive on a
substrate already designated substrate-research-only). H1 (CLM-3 from
scratch) is the more efficient escalation path; full SFT on CLM v4 would
sit between LoRA and from-scratch, untested. We log this gap rather than
claim it.

---

## Appendix A — Closure 4 raw numerics (logit lens + semantic bridge)

### A.1 Logit lens (per-layer top-1 + greedy 15-step emit)

```
L2  : top1 = "�" (id 136)        | greedy = "�}}}}}}}}}}}}}}"
L4  : top1 = "�" (id 236)        | greedy = "���������������"
L6  : top1 = "中国政府"           | greedy = "中国政府邊緣邊緣邊緣..."
L8  : top1 = "Z"                  | greedy = "Z\x1c.444444444444"
L10 : top1 = "s"                  | greedy = "s-�e較小~ijjjjjjjj"   ← only coherent (8 unique)
L12 : top1 = "s"                  | greedy = "s��������������"
L14 : top1 = "�" (id 157)        | greedy = "�陙��癙��\x1c\x1c\x1c\x1c"
L15 : top1 = "\x1c" (id 32)       | greedy = "\x1c\x06\x06\x06..."
```

n_coherent = 1/8 (L10 marginal: 8 unique tokens of mixed ASCII + Han fragment + repeated `j`).

### A.2 Semantic bridge (cosine NN against tok_emb)

```
top10_decoded   = ["\x1c", "�", "�", "p", "�", "+", "/", "s", "-", "\x06"]
top1 cosine sim = 0.4523
iterative_15    = "\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06"
n_coherent      = 0/2
```

Both decode methods (logit lens via final lm_head, cosine NN against
tok_emb) collapse to byte-fragment / replacement-byte loops, indicating
no chat-text basis is recoverable along either decoding path under the
single-prompt regime.

---

## Appendix B — Cross-references

- `state/clm_v4_lora_v1_mmlu_tq_eval_2026_05_05/verdict.json`
- `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`
- `state/anima_emerge_chat_tribev2_2026_05_05/verdict.json`
- `state/anima_emerge_chat_logit_lens_2026_05_05/verdict.json` + `aggregate.json`
- `state/anima_emerge_chat_semantic_bridge_2026_05_05/verdict.json` + `aggregate.json`
- memory `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md`
- memory `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
- `docs/anima_core_emerge_paradigm_revision_2026_05_05.md`
- `docs/anima_core_emerge_stage_3_user_protocol_spec_2026_05_05.md`
- `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`

---

## Compliance footer

- raw#9 honest scope (theorem clearly bounded by H1–H4; not over-claiming)
- raw#10 honest C3 emitted (5 caveats in §6)
- raw#15 additive (no edits to closure verdict files; only new doc + new verdict)
- HF token leak: none (no token literals embedded)
- commit: not requested in this task; doc landed only
- bash 3.2 / mac compat: doc-only artifact
