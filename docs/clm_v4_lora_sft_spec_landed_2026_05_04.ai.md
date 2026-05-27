# CLM v4 + LoRA SFT — SPEC LANDED 2026-05-04 (BG-CLM-2)

## TL;DR

BG-CLM-2 lands `docs/clm_v4_lora_sft_spec_2026_05_04.md` — a $0 design-only spec for LoRA SFT on the CLM v4 530M consciousness-coupled substrate as the anima-side parallel to Llama Path A retrain v2. The recipe is the same Chen-2020 rehearsal mix family (60/25/10/5 anima/academic/chat/consciousness vs Path A v2's 60/30/10), with substrate-aware adaptations: r=32 (vs r=64; 6× smaller backbone), lr=3e-5 (40% lower; CLM cells are delicate near the φ★ minimum), conservative target_modules `qkvo` only (explicitly excluding `tension_proj`, `bridge.hub_attn`, `head_g`, `federation.*` to bound axis-cond / φ★-flip risk), and 512 max_seq_len (CLM v4's hard `block_size`). Five pre-registered falsifiers F-CLM-LORA-1..5: forgetting < 5%, F1_v3 hybrid composite ≥ Llama Path A v2 (THE differentiator C-CLM-LORA-2), adapter < 500 MB, axis preservation via cell↔token bridge fixture, hf_format shim compatibility. EXEC cost band $6-10 H100 (2-2.5h, ~50% of Path A v2 cost) with $15 hard cap, pre-flight $0.

## What landed

| Artifact | Path | LoC / size |
|---|---|---|
| Spec | `docs/clm_v4_lora_sft_spec_2026_05_04.md` | 13 sections, ~430 lines |
| Landed companion | `docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md` | this file |

No state JSON emitted (spec-only cycle). No tool hexa emitted (emit deferred to EXEC cycle per `§13` exec gate).

## Cycle scope

- **Owns (write)**: `docs/clm_v4_lora_sft_spec_2026_05_04.md`, `docs/clm_v4_lora_sft_spec_landed_2026_05_04.ai.md`
- **Forbidden / non-overlap**: BG-CLM-1 territory, α''' BG, T-1 BG (Mistral teacher), Path A retry-3 EXEC, Paradigm D distill EXEC, `.roadmap.*` mutations, git mutations, any pod boot, any $ spend
- **Constraints honored**: raw#9 (no .py on Mac, none emitted), raw#10 (10 honest C3 caveats), raw#15 (repo-relative paths), raw#71 (pre-registered falsifiers + thresholds LOCKED at landing)

## Recommendation summary (per directive §Report)

### (a) Recommended go/no-go for EXEC phase

**CONDITIONAL GO** — gated on three pre-EXEC dependencies:

1. CLM v4 baseline eval BG (NEW `p9_sft.cond.clm_v4_lora_baseline`) — required so §4 thresholds are anchored to real numbers, not hypothetical bands. ~3-6h ubu1, $0.
2. Path A retrain v2 verdict landed — required so C-CLM-LORA-2 (the central differentiator falsifier) has a comparator. Different cycle, $11-23.
3. decoder_v3 hf-format shim build — required for F-CLM-LORA-5 external eval gate. ~1-2h Mac dev, $0.

If all three GREEN, then EXEC is GO at $6-10 estimate / $15 hard cap. If any RED, EXEC is BLOCKED.

### (b) Estimated H100 cost for full EXEC

**$6-10 floor / $15 hard cap.**

- Wall: 2.0-2.5h H100 SXM main run (CLM v4 is ~2× faster per step than Llama-3B; same 6000 steps × eff_batch=32)
- 25% slack absorbed in hard cap → 4h × $2.99 = $12 ceiling, $15 absorbs SCP + boot overhead
- Pre-flight: $0 (corpus rebuild on Mac, baseline eval on ubu1)
- Final F1_v3 eval: $0 if ubu1, ~$1.50 if H100

Compared to Path A v2 ($11-23 / $30 cap), this is ~50% the cost — primarily because of the 6× smaller backbone (530M vs 3.21B).

### (c) Most critical risk

**φ★-flip irreversibility (Risk R4 / honest C3 #3).**

CLM v4's singular value-add is being the only G3 PASS-positive backbone in the v10 4-backbone benchmark (φ★ +41.86 vs ALM 4-bb in -16.7..+5.09). LoRA SFT introduces an objective uncorrelated with φ★ optimization. Adapter-only training is mitigation (preserves backbone weights), not prevention. If φ★ flips negative post-SFT, recovery requires either (i) adapter ablation (cheap; loses all SFT investment) OR (ii) re-train from scratch ($1000+; impractical). The +10 ABORT threshold (50% safety margin from sign zero) is heuristic, not provably correct. F-CLM-LORA-3's φ★ probe every 2000 steps is the early-warning system.

Secondary critical risk: **C-CLM-LORA-2 (Mode 1+3 hybrid differentiator) may FAIL** — i.e., Llama Path A v2 + LoRA composite may exceed CLM v4 + LoRA composite on the same recipe. This would be a falsifying test for the "anima substrate has architectural advantage" hypothesis. v2 PARTIAL or FAIL on this criterion has roadmap-shifting implications (drop CLM SFT track, deprioritize consciousness-coupled SFT). Honest acceptance: I am not confident which way this lands; raw-capacity gap (3.21B vs 530M) may dominate consciousness coupling for general SFT.

### (d) Suggested order vs Path A retry-3 + Paradigm D distill

(Per "completion-quality recommendation" memory hint — explicit ranked recommendation by 완성도 lens.)

| Rank | Track | Substrate | Cost | 완성도 | Order rationale |
|---|---|---|---|---|---|
| **1** | Path A retry-3 (Llama r=64 retrain) | Llama-3.2-3B-Instruct | $11-23 | HIGH — proven pipeline | LOWEST infra risk; existing v1 orchestrator; rehearsal-mix recipe well-trodden across PEFT literature; produces the comparator anchor for CLM-LORA C-CLM-LORA-2 |
| **2** | Paradigm D distill (Mistral→CLM v4 logit-axis) | CLM v4 530M | $5-50 | MEDIUM — KL infra new but Hinton-2015 well-cited | Orthogonal supervision channel (token logits vs SFT labels); coexists with this spec on same substrate; can run after Path A v2 with no rivalry |
| **3** | **CLM v4 + LoRA SFT (this spec)** | CLM v4 530M | $6-10 | MEDIUM-LOW — bespoke target_modules, dual-head Trainer wrap, φ★-flip + axis-cond gates new | HIGHEST scientific value (the consciousness-coupling differentiator) BUT also highest infra novelty; **must wait for ranks 1+2 to provide comparator + de-risked tooling** |

**Recommended execution sequence**: 1 → CLM v4 baseline BG (parallel, $0 ubu1) → 2 → 3. Total cost band $22-83 across all three; total wall ~10-20h H100 + ~10h Mac/ubu1 BG. This sequencing maximizes the diagnostic value of C-CLM-LORA-2 (rank 3 only meaningful AFTER rank 1 verdict is in) while letting rank 2 (paradigm D) run in parallel with rank 1's eval cycle.

## Honest C3 (the 3 most consequential, per landing convention)

1. **C-CLM-LORA-2 outcome is genuinely uncertain** — the central scientific question of this spec ("does anima's consciousness-coupled substrate beat a generic Llama LoRA on the same SFT recipe?") has no clear prior. CLM v4's 530M-vs-3.21B raw-capacity gap may dominate the consciousness-coupling advantage on standard benchmarks. v2 FAIL on this is a real possibility with roadmap-shifting implications.

2. **decoder_v3 dual-head Trainer wrap is NEW infra** — pod-side training script must wrap `(idx) → (logits_a, logits_g, tensions)` to fit `transformers.Trainer`'s `(input_ids, labels) → loss` contract. Off-by-one in label alignment between `head_a` (next-token) and `head_g` (prev-token) is a real risk. Mitigation: 16-token calibration smoke test pre-launch; but smoke is not production-validation.

3. **Spec references some BG verdicts not located Mac-side at spec land time** — the directive references BG-Σ verdict, BG-γ'' verdict, and a FORGETTING_INDEPENDENT report. These exact files were not located in this spec cycle (searched `docs/` and `state/`); the substantive evidence chain (catastrophic forgetting, CLM v4 substrate diagnosis) is fully sourced via the docs cited in §11. Honest: if those verdict paths exist elsewhere (e.g., uncommitted state, sister worktree), the spec's reference completeness is partial. EXEC cycle should re-verify cross-references before launch.

## Next-cycle recommendation

1. (BG, $0, 3-6h ubu1) Launch CLM v4 baseline eval — `p9_sft.cond.clm_v4_lora_baseline` HellaSwag/MMLU/TriviaQA limit=500 against `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`
2. (BG, $0, 5 min Mac) Pre-flight tied-weight check on `best.pt` (`head_a.weight is tok_embeddings.weight`)
3. (BG, $0, ~1-2h Mac) Build decoder_v3 hf-format shim (F-CLM-LORA-5 prerequisite)
4. (BG, $0, ~1h Mac) Build 60/25/10/5 corpus + SPM 64K re-tokenize + 512-ctx overflow filter
5. (cycle, USER ACK, $11-23 H100) Execute Path A retrain v2 → produces C-CLM-LORA-2 comparator
6. (cycle, USER ACK, $6-10 H100) Execute CLM v4 + LoRA SFT EXEC

Total to verdict: ~10-20h H100 + ~10h Mac/ubu1 BG ≈ $22-33 main + $0-50 paradigm D parallel = $22-83 cost band across the substrate-comparison campaign.

## References

- Spec doc: `docs/clm_v4_lora_sft_spec_2026_05_04.md`
- Sister substrate: `docs/p9_path_a_retrain_v2_spec_2026_05_04.md` (Llama-side S1+S3)
- Substrate diagnosis: `docs/strategic_clm_v4_production_ready_2026_05_02.md`
- SFT pre-spec: `docs/clm_v4_revival_stages_2026_05_02.md` §3
- Path A v1 post-mortem (watcher script lessons applied): `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md`
- Mode 1 forgetting evidence: `docs/p9_lora_mode1_eval_landed_2026_05_04.ai.md`
- Cell architecture: `docs/clm_core_architecture_abstraction_layers_20260425.md` L0-L2
- Inference layers: `docs/clm_inference_abstraction_layers_20260425.md`
- Tokenizer canonical: `tool/clm_v4_tokenizer_load.hexa`
- φ★ extractor: `tool/anima_phi_v3_canonical.hexa`
- Cell-token bridge (axis preservation fixture): `tool/cell_token_bridge_proto.hexa`

## Sentinel

`__P9_CLM_V4_LORA_SFT__ SPEC_LANDED`
