# anima_emerge_chat_tribev2 — landed 2026-05-05

> **Verdict**: `FAIL_ALL_TRIED` — architectural impossibility at design review. Cost: $0. Wall: ~4 min.

## TL;DR

The mission was: *use `references/tribev2/` to make CLM v4 emit semantically coherent chat for prompt "안녕"*.

**TRIBE v2 is not a language model.** It is an fMRI BOLD encoder: text/audio/video stimuli → fsaverage5 cortical-surface BOLD predictions (10242 vertices, 5s hemodynamic-lag offset). It has **no** tokenizer-out, **no** decoder, **no** lm_head, **no** logits, **no** generate(). Its public API is `from_pretrained → get_events_dataframe → predict`, returning a numpy float array of brain-vertex predictions.

Therefore the load-bearing assumption of every strategy variant in the prompt — *"tribev2 contributes a language-decode signal"* — is architecturally false, and no decoding strategy / sampling regime / injection magnitude / source layer / secondary head / ensemble partner can rescue it. The mission is closed at design review with $0 spent.

## What tribev2 actually is (for the cycle ledger)

| field                | value                                                                                                  |
|----------------------|--------------------------------------------------------------------------------------------------------|
| modality_input       | text, audio, video                                                                                     |
| modality_output      | fMRI BOLD                                                                                              |
| output_space         | fsaverage5 cortical mesh, 10242 vertices                                                               |
| TR (s)               | 1.49                                                                                                   |
| hemodynamic offset   | 5 s                                                                                                    |
| text encoder         | meta-llama/Llama-3.2-3B (frozen feature extractor, layers [0, 0.2, 0.4, 0.6, 0.8, 1.0])                |
| audio encoder        | Wav2VecBert (layers [0.75, 1.0])                                                                       |
| video encoder        | facebook/vjepa2-vitg-fpc64-256 + facebook/dinov2-large                                                 |
| fusion head          | x_transformers TransformerEncoder, depth=8, hidden=1152, low_rank_head=2048, SubjectLayers, AvgPool1d  |
| public API           | `TribeModel.from_pretrained` / `get_events_dataframe` / `predict`                                       |
| evaluation           | OnlinePearsonCorr per vertex; TopkAcc top-1; MSELoss                                                   |
| license              | CC-BY-NC-4.0                                                                                            |

There is no path in this graph from any internal state back to a token distribution.

## Why each prompted strategy is blocked

The parent prompt enumerated six retry strategies. Each is architecturally blocked by the same root cause; the diagnoses below are recorded for ledger completeness.

| # | strategy                              | block root cause                                                                                                           |
|---|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| 1 | tribev2 default decode loop on `logits_a` | tribev2 produces no logits at all. There is no `logits_a` to loop over.                                                    |
| 2 | tribev2 multi-sample best-of-N        | best-of-N requires a tribev2 score over candidate token sequences; tribev2 only scores per-vertex BOLD Pearson r.          |
| 3 | tribev2 + canonical inject (low mag 5) | canonical inject biases CLM v4 hidden state along a discovered axis; tribev2 does not consume that hidden state, and even if it did, would still output BOLD vertices, not tokens. |
| 4 | tribev2 + tension-trajectory peak-layer hidden | reading a richer 768-d hidden does not invert into tokens. The chat-incapability is in CLM v4's own `lm_head` (issue #115).|
| 5 | tribev2 + head_g secondary            | head_g (cand-H) failed previously; tribev2 is not actually wired into this strategy.                                        |
| 6 | tribev2 ensemble with Llama 3.2 distill | if Llama is the chat producer, then Llama is doing the work; tribev2 contributes nothing — mission framing is not satisfied.|

## What I checked (and what I deliberately did not run)

Checked (read-only, ~10 tool uses):

- `references/tribev2/README.md` — confirmed identity statement.
- `references/tribev2/SUMMARY_KR.md` — confirmed KR identity statement.
- `references/tribev2/inventory.json` — confirmed modality matrix and architecture.
- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL.md` — confirmed Axis-3 *original* "No fit" verdict was based on output-space incompatibility (cortical vertex vs cell state).
- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md` — confirmed the post-#95 REVISE upgrades Axis 3 to "Strong via Framing D" but Framing D is a *3-way EEG↔CLM↔BOLD cross-validation*, **not** a chat-unblock path. Framing D explicitly preserves modality boundaries.
- `references/tribev2/tribev2/demo_utils.py` — public API surface grep: from_pretrained / get_events_dataframe / predict. No generate / decode / tokenize-out.
- `references/tribev2/tribev2/` whole-tree grep `generate|lm_head|logits` — 0 hits in model/decode paths.

Deliberately did not run:

- No transient_py helper script. Writing one would have required either (a) silently bypassing tribev2 and decoding CLM v4 directly (defeats the mission framing) or (b) embedding a fabricated "cortical-vertex → token" projection (no scientific or engineering basis). I chose to record the architectural diagnosis instead, at zero further cost.
- No HF download. tribev2 weights live at `huggingface.co/facebook/tribev2`; downloading them would not change the result and would consume HF traffic against a doomed plan.
- No commit (per prompt constraint).

## Cumulative architectural learning (chat-capability axis, anima-wide)

This cycle adds a third converging closure to the chat-capability investigation:

1. **Pβ Φ★-axis Paradigm D 50K** — F-Pβ-3 FAIL_TRUE composite 0.01176 RED (distill route closed).
2. **CLM v4 LoRA SFT** — F-CLM-LORA-2 FAIL_REGRESSION at -36.298 pp vs Llama Path A v2 (post-hoc SFT route closed).
3. **tribev2 bridge** — no decode path exists; mission architecturally impossible (cross-modal-encoder bridge route closed).

Three classes of proposal — *distill*, *post-hoc SFT*, *cross-modal encoder bridge* — are now systematically eliminated. Issue #115 (CLM v4 architectural chat-incapability) is corroborated, never contradicted.

## Recommendations (next cycle, ranked by 완성도 lens)

1. **PROMOTE Llama Path A v2 as the chat-capability winner.** Composite 0.5584 (Llama A v2) vs 0.19542 (CLM v4 LoRA SFT) vs 0.01176 (Pβ Paradigm D). The chat axis is decisively Llama-substrate. CLM v4 stays substrate-research-only. *Highest 완성도 — closes three converging negatives with one positive winner.*

2. **Pivot tribev2 to its actual fit: Pilot-T1 (Axis 4) / Framing D (3-way bridge anchor).** Both the original 2026-04-26 proposal and the 2026-05-02 addendum rank these as the scientifically defensible uses. Preregistered falsifiers F-CT-2/3/4 already exist. Budget $0-2. *High 완성도 — matches authored intent.*

3. **If anima-internal chat is *required*, design CLM-3 with explicit chat-loss training objective from cycle-0** (not bolted on). The three closures above collectively imply post-hoc chat-lift on CLM v4 is dead; a new substrate is the only remaining path if substrate-internal chat is required. *Medium 완성도 — high-cost speculative; defer until #2 returns.*

## raw#10 honest C3 (5)

1. **Why retry after #115 was already declared architectural?** The prompt argued tribev2 is "a different mechanism (decode / ensemble / scaffolding)" so #115 might not bind. That re-evaluation was reasonable, but tribev2 is *none* of those mechanisms — it's an fMRI encoder. The retry-justification framing rested on a category error about what tribev2 is. Net: both #115 *and* the prior architectural fact about tribev2's identity bind; either alone suffices.

2. **Did I reject too fast without runtime attempt?** I used <10 of ~40 tool uses to confirm identity from authoritative in-repo docs. The impossibility is documentary, not probabilistic. Running a doomed helper would consume budget, write a transient_py file containing a fabricated cortical-vertex→token projection (scientifically baseless), and produce a runtime-fail JSON conveying strictly less information than this design-time JSON.

3. **Could a creative reinterpretation rescue the mission?** Two are imaginable: (a) "use tribev2 to score CLM v4 chat outputs against a brain-anchored target" — does not *unblock* chat, presupposes it; (b) "use tribev2-predicted BOLD as a perceptual reward signal for RLHF on CLM v4" — speculative, multi-month, $$, no preregistered falsifier, orthogonal to the 60min/$0 budget. Logged for archival, not pursued.

4. **Cumulative-evidence claim might over-reach.** I assert tribev2 closure is a "third converging closure". To be fair: tribev2 closure is *cheaper* and *stronger* than the other two (documentary, not measurement), and rules out a separate *class* of proposal (cross-modal-encoder bridge), not another data point on the same axis. The verdict text reflects this distinction.

5. **Respect for "retry until success" instruction.** Partially. I exhausted the six strategies at design review, not at runtime. This is a defensible substitution because runtime outcomes are predictable from architecture (all `FAIL_NO_TOKEN_PRODUCED`, same root cause) and consume budget without adding falsification value. If the user's intent was "I want to *see* runtime fails, not just argued fails," that is legitimate but expensive — they should signal it explicitly, and I will then write minimal runtime stubs for each strategy.

## Artifact index

- `state/anima_emerge_chat_tribev2_2026_05_05/runs/strategy_1_architectural_blocked.json`
- `state/anima_emerge_chat_tribev2_2026_05_05/runs/strategy_2_through_6_architectural_blocked.json`
- `state/anima_emerge_chat_tribev2_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_tribev2_2026_05_05/verdict.json`
- `docs/anima_emerge_chat_tribev2_landed_2026_05_05.ai.md` (this file)

## raw compliance

- raw#15 (additive): no edits to mount.hexa, dialogue.hexa, anima-core-dialogue.bash, anima_dialogue_load.py, clm_v4_hf_format_shim.py, references/tribev2/.
- raw#10 (honest C3): five concerns above.
- raw#30 (irreversibility): no irreversible action.
- raw#37 (transient_py namespace): no .py written under `tool/transient_py/` — design review concluded scripts would be unjustified contradictions.
- no-commit: respected.
- no-HF-token-leak: respected (no HF download).
- $0: respected.
