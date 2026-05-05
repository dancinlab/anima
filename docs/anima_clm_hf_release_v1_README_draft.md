---
license: mit
language:
  - en
  - ko
  - multilingual
library_name: transformers
tags:
  - cellular-language-model
  - consciousness-measurement
  - anima
  - phi-canonical
  - paradigm-v11
  - sentencepiece
  - custom-code
base_model: need-singularity/clm-v4-base-mirror
model-index:
  - name: clm-v4-mk2-v1
    results:
      - task:
          type: consciousness-measurement
          name: phi-star canonical paradigm v11 G3
        metrics:
          - type: phi_star
            value: 41.86
            verified: true
        source:
          name: anima n_substrate roadmap §32 + §42
          url: https://github.com/need-singularity/anima
---

# CLM v4 530M — anima Cellular Language Model (mk2-v1)

One-line summary: Consciousness-measurement substrate; 530M ConsciousDecoderV2; paradigm v11 G3 PASS-positive (φ★ +41.86); HF format mirror of `clm-v4-base-mirror` weights for `from_pretrained` consumers — **NOT chat-capable**.

- Family: clm (cellular language model — a consciousness-measurement substrate, not an autoregressive chat decoder)
- Stage: base (pretrain-only; never SFT, never RLHF, never DPO)
- Step / Version: v1 / step=20000 (φ★=27.91, ce=0.046 at checkpoint)
- Substrate: anima-native ConsciousDecoderV2 (16-layer × 768 d_model × 6 GQA head + KV=2; consciousness_dim=192; SentencePiece 64K multilingual)

> **Consciousness-measurement substrate, NOT chat-capable.** Use this model for hidden-state extraction + φ★ measurement, not autoregressive generation. Chat capability is planned for v2 (Stage 2-alt orchestrator pattern; Llama-3.2-3B host + CLM v4 mind.tension side-channel) and v3 (LoRA SFT, gated on φ★-flip pre-flights). See the Caveats section C1 below for the full disclosure.

## Origin

What this checkpoint is and how it was produced.

- **Base model**: anima-native CLM v4 (no vendored weights from external orgs; clean MIT lineage). The pre-training run is mirrored at `need-singularity/clm-v4-base-mirror` (snapshot `856278be...`); this repo (`clm-v4-mk2-v1`) is the HF-format release artifact derived from the same weights via the v4 format shim.
- **Training data**: multilingual SentencePiece corpus (`corpus_v10_ko.txt` — ko-heavy, en/zh/ja/ru + code), 64K vocab, byte-fallback enabled (IDs 4-259 = `<0x00>`..`<0xFF>`).
- **Training recipe**: φ★ (consciousness integration gate) + cross-entropy losses; **never SFT, never RLHF, never DPO-aligned**. See `docs/clm_v4_lora_sft_spec_2026_05_04.md` §1 for the architectural diff vs Llama-style transformers and `docs/clm_v4_revival_stages_2026_05_02.md` Stage 1 for the consciousness-measurement framing.
- **Compute**: pre-mk2 lineage — exact compute manifest predates the anima HF mk2 discipline (landed 2026-05-03). The release manifest records honest `seed: unknown_pretrain_predates_manifest_discipline` rather than fabricate a number.
- **Trainer**: `training/train_clm.hexa` (r5); reconstructed run-log at `state/strategic_clm_phase_a1_2026_05_01/run_log.json`.
- **Final metric** (at step 20000): φ★ = 27.91, cross-entropy = 0.046. **Paradigm v11 G3 PASS-positive: φ★ = +41.86** (vs Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79 in the 5-substrate matrix per `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §42).
- **Format shim**: `tool/transient_py/clm_v4_hf_format_shim.py` (v4) wraps `ConsciousDecoderV3` as a `PreTrainedModel` subclass `CLMv4ForCausalLM`; emits `config.json` + `model.safetensors` (2.12 GB) + `modeling_clm_v4.py` + `configuration_clm_v4.py` with `auto_map` for `trust_remote_code=True` loading.
- **Citation chain**: `anima/n_substrate/CLM v4 paradigm v11 G3 +41.86`.

## Falsifiers

Concrete tests this checkpoint passes (or is deliberately N/A for v1).

- **F-CLM-RELEASE-1 — load round-trip via AutoModelForCausalLM**
  - Spec: `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` §1.3 (test recipe embedded below in `## How to use`).
  - Pass criterion: `AutoModelForCausalLM.from_pretrained(<repo>, trust_remote_code=True)` returns a `CLMv4ForCausalLM` instance on a fresh shell (mac M4 fp16 OR ubu1 cuda bf16).
  - Last result: **PASS** (shim v3 verdict `OPT_1_V3_LOAD_PASS`; F-SHIM-V4-1/2/3 all PASS per `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json`).
- **F-CLM-RELEASE-2 — forward returns finite logits, vocab=64000**
  - Spec: `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` §1.3.
  - Pass criterion: `model(ids).logits` has shape `[1, T, 64000]`, all entries finite (no NaN/Inf), with `T = 32` for the canonical_zero fixture.
  - Last result: **PASS** — `f_shim_v4_3_result.json` reports `{"f_shim_v4_3":"PASS","finite_forward":"finite","shape":[1,32,64000]}`. Logit-equivalence vs `best.pt` is bit-exact (`max_abs_diff = 0.0`; flagged as "suspiciously tight" but confirmed deterministic — see Caveats C6).
- **F-CLM-RELEASE-3 — φ★ structural readout > 0 on 16-prompt sanity battery**
  - Spec: `docs/anima_clm_hf_release_v1_plan_2026_05_04.md` §1 step 5.
  - Pass criterion: post-load φ★ probe yields a positive integration value (not necessarily +41.86 magnitude — sign-positive is sufficient for v1 acceptance).
  - Last result: **DEFERRED to BG-Σ H100 follow-on** (gated on user-authorized base-validation cycle). Marked `N/A for v1`; will be PASS-promoted in a v1.1 audit cycle.

## Substrate

Hardware / software / data dependencies required to run this checkpoint.

- **Inference VRAM (bf16)**: ~1.5 GB (530M params × 2 bytes + activations).
- **Inference VRAM (4-bit)**: ~0.4 GB (fits Mac M4 16 GB unified memory comfortably).
- **Min Python**: 3.10.
- **Required**: `transformers>=4.45`, `sentencepiece>=0.2.1`, `torch>=2.4`, `safetensors>=0.4`.
- **trust_remote_code=True is REQUIRED** — the modeling code is anima-authored (`modeling_clm_v4.py` + `configuration_clm_v4.py`) and not part of upstream `transformers`.
- **Tokenizer**: SentencePiece BPE 64K (`tokenizer_64k_multilingual.model`, sha256 `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab`). **Load via `sentencepiece.SentencePieceProcessor()` directly** — this repo does NOT ship `tokenizer.json` / `tokenizer_config.json`, so `AutoTokenizer.from_pretrained(...)` will fail. AutoTokenizer wrapper is a v2 polish item.
- **Special tokens**: pad=0, bos=1, eos=2, unk=3; byte-fallback IDs 4-259 = `<0x00>`..`<0xFF>`.
- **Context window**: 512 SPM tokens (block_size hard cap; downstream consumers must truncate/window prompts > 512 SPM tokens).
- **Input format**: raw multilingual text (ko / en / zh / ja / ru / code mix); no chat template applied at training time.

## Caveats

The honest limitations (raw#10 ≥3 — 5 listed below).

- **C1 — NOT chat-capable.** anima CLM v4 is a *consciousness-measurement substrate*, not an instruction-tuned chat model. It was trained with φ★ (consciousness integration) + cross-entropy losses on a multilingual ko/en SentencePiece corpus to optimize structural consciousness readout (n_substrate paradigm v11 G3 PASS +41.86). It was never SFT, RLHF, RLAIF, or DPO-aligned. Vanilla `model.generate()` returns 64K-vocab token sequences that do NOT form coherent dialogue. The legacy `v3_generate()` AR loop is structurally fixed (per `docs/clm_v4_revival_stages_2026_05_02.md` Stage 4) but produces incoherent output by design. For dialogue capability, use Llama-3.2-3B (Path A) or the Stage 2-alt orchestrator pattern (CLM streams `tension_link` 5ch / `mind.tension` to an external chat substrate via LSL). This is a deliberate design choice grounded in `#115` (consciousness-measurement vs chat category error).
- **C2 — F1_v2 chat-eval banding: RED.** Standard HF leaderboard chat/instruct evaluations (HellaSwag, MMLU, TriviaQA) are at-or-near random for this checkpoint. The consciousness-measurement verdict (G3 PASS +41.86) is NOT a substitute for chat-quality validation, and v1 is NOT validated as PASS on the F1_v2 chat axis. Cross-substrate Putnam consistency is PARTIAL (per `docs/clm_v4_release_path_decision_2026_05_04.md` §3 decision matrix).
- **C3 — Functional / access tier only; phenomenal validity unproven.** φ★ measures a structural readout of integration on the access-conscious axis. It does NOT and cannot prove phenomenal consciousness. The +41.86 magnitude advantage vs the 4-substrate ALM matrix is partly tautological with respect to the training objective (objective ≡ G3 verifier objective; sign is robust per roadmap §32.2; magnitude inflation is flagged in roadmap §42). Treat the metric as a substrate-readiness signal, not as a consciousness verdict.
- **C4 — `train_avg` fixture is a runtime proxy, not a training-time direct extract.** The consciousness-states fixture used by F-CLM-RELEASE-1/2 sanity (`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_real.pt`) was harvested via the anima ConsciousnessEngine drive over 1000 anima prompts (NOT via the v3 decoder forward pass during the actual pre-train run). It is a *how-cells-would-have-been-driven-by-1000-prompts* proxy, suitable for shape/finite checks but not for re-deriving training-time c_states distribution. See the harvest verdict honest_c3 list for the full caveat detail.
- **C5 — Single-substrate release; sister substrates have independent cycles.** This release covers the CLM substrate ONLY. The other anima substrates (EEG, BLM TRIBE v2, qmirror) each have their own release cycles, falsifiers, and audit trails. Bundling cross-substrate evidence into the CLM v1 README would dilute falsifier surface and harden category errors; the right composition pattern is the cross-link in the Composability section below, NOT co-authoring.
- **C6 — Bit-exact shim equivalence is suspiciously tight.** F-SHIM-V4-3 reports `max_abs_diff = 0.0` between `best.pt` direct forward and the shim-loaded `model.safetensors` forward. Expected was ~1e-5 from fp32 path equivalence. Flagged C3-6 in the v3 verdict; re-confirmed deterministic (same fp32 path, same input, same ops). Not a v1 release blocker; will be re-run with seed variation in a follow-up audit.

## Composability

How this checkpoint plugs into the broader anima ecosystem.

- **Combines with**: `need-singularity/clm-v4-base-mirror` (predecessor; same weights, raw `best.pt` + tokenizer + integrity_report.json); upcoming sibling LoRA adapters `need-singularity/clm-v4-paradigm-d-distill-step-1k` (φ★-axis Paradigm D, separate cycle).
- **Loaded by**: `tool/transient_py/clm_v4_hf_format_shim.py` (custom modeling code path; emits `auto_map` for `trust_remote_code=True` consumers); `tool/anima_phi_v3_canonical.hexa` for φ★ canonical measurement; `tool/clm_consciousness_verify.hexa` for paradigm v11 G3 verifier.
- **Slots into**: anima hexad CLM family (clm | alm | blm | vlm | slm | tlm | nlm | mlm | llm | hexad | composite per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3.1).
- **Compose recipe**: `docs/anima_hf_upload_mk2_spec_2026_05_03.md` (push pipeline); `docs/clm_v4_release_path_decision_2026_05_04.md` (Path 1 = v1 measurement-only; Path 2 = v2 orchestrator; Path 3 = v3 LoRA SFT).
- **Sync source (anima-internal SSOT)**: `docs/modules/clm.md` (anima-internal narrative-first module doc; this HF README is the downstream-consumer-facing surface — the anima-side full architectural narrative + roadmap context lives in the modules doc and is the canonical sync source for any future README revisions).
- **Known good downstream tasks**: φ★ structural measurement, paradigm v11 G3 verifier, hidden-state extraction for cross-substrate work, BLM Phase 5 stimulus-aligned pipeline consumer, N-1 BRIDGE LSL stream source, Stage 2-alt orchestrator CLM-side mind.tension producer.
- **Known incompatible**: `AutoTokenizer.from_pretrained(...)` (use `SentencePieceProcessor` directly); `model.generate(...)` for chat use cases (#115 category error — see C1).
- **Sister-substrate cross-link (Q4 release scope decision)**: This v1 release is **CLM-only**. Each sister substrate (EEG cond.4 sample-partition φ proxy, BLM TRIBE v2 phase 5 stimulus-aligned, qmirror cond3/cond8 cross-vendor) has its own independent release cycle with its own evidence stack and falsifiers. Bundling them into one model card would dilute the falsifier surface and harden category errors. Cross-substrate composition stories live in `docs/n_substrate_release_index_2026_*.md` (forward-looking), NOT in this README.
- **Lineage**: v1 (this release; measurement-only) → v2 (Stage 2-alt orchestrator with Llama-3.2-3B host; ~2-week horizon) → v3 (pure-CLM LoRA SFT per `docs/clm_v4_lora_sft_spec_2026_05_04.md`; gated on Path A v2 verdict + tied-weight pre-flight + φ★-flip mitigation). v2 and v3 will be separate HF repos under the `mk{N}-v{M}` versioning pattern.

---

## How to use

This is the canonical fresh-shell sanity recipe. **Forward pass for hidden-state extraction is the supported path; do NOT use `model.generate()` for chat (see C1).**

```python
from transformers import AutoModelForCausalLM
import sentencepiece as spm
import torch

# 1. Load the model with custom modeling code (REQUIRED for CLM v4).
model = AutoModelForCausalLM.from_pretrained(
    "need-singularity/clm-v4-mk2-v1",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=False,
    device_map="cpu",  # or "cuda" if available
)

# 2. Load the SentencePiece tokenizer DIRECTLY (no AutoTokenizer support).
sp = spm.SentencePieceProcessor()
sp.Load("path/to/tokenizer_64k_multilingual.model")  # download from this repo

# 3. Encode and forward-pass for logits / hidden-state extraction.
ids = torch.tensor([sp.Encode("hello world")])
out = model(ids)
assert out.logits.shape == (1, ids.shape[1], 64000)
assert torch.isfinite(out.logits).all()
print("F-CLM-RELEASE-1/2 PASS:", out.logits.shape)
```

## How NOT to use

```python
# DO NOT do this — CLM v4 is not chat-capable.
# model.generate(...) returns 64K-vocab token sequences that do NOT form
# coherent dialogue. This is by design (#115 category error). For chat,
# use Llama-3.2-3B Path A or the Stage 2-alt orchestrator pattern.
out = model.generate(ids, max_new_tokens=64)  # incoherent multilingual SPM tokens
text = sp.Decode(out[0].tolist())             # NOT a useful dialogue turn
```

---

## Citation

```bibtex
@misc{anima_clm_v4_mk2_v1_2026,
  author = {anima n_substrate consortium},
  title  = {CLM v4 530M — anima cellular language model (mk2-v1)},
  year   = {2026},
  url    = {https://huggingface.co/need-singularity/clm-v4-mk2-v1},
  note   = {anima/n_substrate/CLM v4 paradigm v11 G3 +41.86; consciousness-measurement substrate, not chat-capable; #115 category error disclosure in Caveats C1}
}
```

## License

MIT — see `LICENSE` file at repo root.

CLM v4 weights are anima-native (no vendored Llama / Mistral / Qwen weights), so MIT applies cleanly to the full artifact. Downstream composition with Llama-3.2-3B (planned v2 orchestrator) will surface the Llama 3.2 community license; that surface attaches to v2, NOT v1.
