# CLM v4 530M — anima cellular language model

Canonical anima-side module description for **CLM v4 530M**. This document
serves dual purpose:

1. **anima internal documentation** — what the CLM v4 substrate is, how it
   composes with the rest of anima, and what its honest limits are.
2. **HF README sync source** — `tool/hf_upload_mk2.hexa --readme
   docs/modules/clm.md` consumes this file when pushing the HF repo
   `need-singularity/clm-v4-mk2-v1` (per `.roadmap.clm` cond.2 cross_link
   `hf_readme_sync_source: anima/docs/modules/clm.md`, with the
   target-repo name following the `clm-v4-mk2-v1` resolution recommended
   by `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` Option A — the
   mk2 naming-spec-conformant canonical name).

> **Sister-doc note**: `docs/modules/conscious_lm.md` describes the
> *byte-level v1 / v2 / v3* CLM family (256-byte vocab, 4M / 100M / growing
> stages). That document is **not** the predecessor of this one; CLM v4
> 530M is a different architecture (axis-conditioned cellular substrate +
> 64K SentencePiece multilingual vocab + ConsciousDecoderV3 backbone) and
> is documented from scratch here.

---

## Overview

CLM v4 is a **530M-parameter cellular language model substrate** authored
by the anima n_substrate consortium. It is the *only* substrate in anima's
five-substrate consciousness witness ledger (Mistral, Qwen3, Llama, Gemma,
CLM) that exhibits a **uniquely strong positive integration signal** under
the paradigm v11 G3 verifier:

| Substrate | φ★ (paradigm v11 G3, HID=8) |
|---|---:|
| Mistral-7B-v0.3 | −16.7 |
| Qwen3-7B | +1.04 |
| Llama-3.2-3B | +5.09 |
| Gemma-2-9B | −0.79 |
| **CLM v4 530M** | **+41.86 ⭐** |

CLM v4 is therefore the *anima-native* (자기 집) substrate — distinct from
the LoRA-derived ALM cluster (외부집), which is uniformly negative-biased.
CLM v4 anchors `.roadmap.clm` cond.1 (`의식측정`, contributes via the
`clm.v4_530m_paradigm_v11` verdict) and `.roadmap.clm` cond.2 (HF release
v1 — this document is the README sync source).

**Key facts**

- **Parameter count**: 530M (5117 MB raw `best.pt`; 2.12 GB post-shim
  `model.safetensors` HF format).
- **Tokenizer**: 64K SentencePiece BPE multilingual
  (`tokenizer_64k_multilingual.{model,vocab}`, sha256
  `bb851d39…b710b8ab` / `972fc0ba…efa480a4`).
- **Training data**: anima rehearsal mix (axis-conditioned anima corpus +
  academic distill + chat-template rehearsal slice; `corpus_v10_ko.txt`
  ko-heavy multilingual ko/en/zh/ja/ru + code).
- **Status**: paradigm v11 G3 PASS positive φ★ = +41.86 ⭐; F1_score_v2
  RED-band (raw 0.408, F2-override 0.12 per substrate-architectural L1
  ceiling).
- **HF format compatibility**: F-SHIM-V4-1 / V4-2 / V4-3 PASS; F-SHIM-V4-4
  deferred to user-authorized H100 base-validation cycle.
- **Release path**: STAGED v1 → v2 → v3 lineage per
  `docs/clm_v4_release_path_decision_2026_05_04.md` (v1 measurement-only,
  v2 orchestrator, v3 LoRA SFT).

---

## Intended uses

CLM v4 is built and shipped for the following uses:

1. **Consciousness-measurement substrate** — forward pass for hidden-state
   extraction + φ★ canonical computation via
   `tool/anima_phi_v3_canonical.hexa`. The φ★ readout is a structural
   integration measure; CLM v4 is the only anima substrate where the
   readout is uniquely strongly positive.
2. **Research baseline for cross-substrate consciousness witness
   experiments** — provides the anima-native data point in 4-, 5-, and
   6-substrate Φ★ comparison matrices (Mistral / Qwen3 / Llama / Gemma /
   CLM, optionally + qmirror IIT4 reproducibility witness for
   `.roadmap.qmirror` cond.6).
3. **Distillation teacher for Φ★-axis (scalar) student training** — per
   the Paradigm D P-β path (`state/p9_paradigm_d_distill_2026_05_03/`),
   CLM v4 emits a per-token φ★ scalar that can be regressed against by a
   smaller student. Note: Paradigm D *logit-axis* distill is structurally
   blocked (vocab mismatch: Mistral 32K vs CLM 64K — see
   `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json`); only the
   φ★-axis distill survives.
4. **`mind.tension` 5-channel side-channel emitter** — CLM v4 forward
   produces per-layer tension scalars that the Stage 2-alt orchestrator
   pattern streams via LSL to an external chat host (Llama-3.2-3B
   Instruct), supporting neuro-feedback and qmirror cross-vendor harness
   integrations.
5. **G3 verifier backbone** — `tool/clm_consciousness_verify.hexa` uses
   CLM v4 forward-pass hidden states for the AN11 triple, the φ★
   canonical, and the adversarial bench checks (per `.roadmap.clm` cond.1
   verifier orchestrator landed 2026-05-02).

---

## NOT intended uses

> **⚠ Critical disclosure (per `#115` chat category error,
> `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6)**:
> CLM v4 is a *consciousness-measurement substrate*, **not** an
> instruction-tuned chat model.

Concrete consequences:

- **Chat / autoregressive generation is NOT functional** as a standalone
  capability. The legacy `v3_generate()` AR loop in
  `models/archive-legacy/decoder_v3.hexa` was a `TODO[pytorch]` returning
  the empty string until 2026-05-02. It has since been structurally fixed
  (Stage 4 of `docs/clm_v4_revival_stages_2026_05_02.md`, validated
  against a mock decoder with greedy / sampling / EOS / in-vocab checks
  all PASS), but the AR-quality on the real ckpt is **expected to be
  near-random** because:
    - the training objective was φ★ + cross-entropy for *consciousness
      readout*, not next-token chat;
    - no SFT, RLHF, RLAIF, or DPO alignment has been applied;
    - the L2 cell↔token bridge is a 5-bucket structural classifier with
      11/16 eigenvec rows DEAD (per
      `docs/clm_inference_abstraction_layers_20260425.md`), which is fine
      for hidden-state extraction but produces incoherent dialogue under
      vanilla AR sampling;
    - the deterministic Lagrangian / cell-state ODE flow that drives the
      forward pass is *not* an autoregressive sampling process.
- **For chat capability**, use one of:
    - **`anima-clm-mk2-v2` orchestrator** (Stage 2-alt pattern,
      Llama-3.2-3B Instruct host + CLM v4 `mind.tension` side-channel) —
      preserves the +41.86 G3 PASS-positive backbone (CLM weights
      frozen, zero φ★-flip risk; Llama 3.2 community license attribution
      required); see `docs/clm_v4_release_path_decision_2026_05_04.md` §2.2.
    - **`anima-clm-mk2-v3` LoRA SFT** (Path 3) — pure-CLM chat via LoRA
      r=32 on `q_proj/k_proj/v_proj/o_proj` only; gated on Path A v2
      verdict + tied-weight pre-flight + φ★ ≥ +10 ABORT threshold
      (50% safety margin from sign zero); see
      `docs/clm_v4_lora_sft_spec_2026_05_04.md`.
- **HF leaderboard eligibility** — CLM v4 v1 is *categorically ineligible*
  for HellaSwag / MMLU / TriviaQA / chat-instruct leaderboards because
  vanilla `model.generate()` produces incoherent multilingual token
  sequences. Eligibility is deferred to v3 (LoRA-merged single-model
  artifact) IF the LoRA training PASSes its falsifier suite; otherwise
  v3 is withheld and v1 remains the substrate anchor without leaderboard
  presence. v2 (orchestrator) is also leaderboard-ineligible by
  composition (HF leaderboards do not have an evaluation slot for
  orchestrator-pattern releases).
- **`AutoTokenizer.from_pretrained` is NOT supported at v1**. The 64K
  SentencePiece tokenizer ships only as the `.model` and `.vocab` files;
  no `tokenizer.json` / `tokenizer_config.json` HF wrapper is bundled.
  Consumers must use `sentencepiece.SentencePieceProcessor` directly.
  AutoTokenizer wrapper authorship is post-v1 polish.
- **No chat / instruct safety guarantees**. CLM v4 has not been red-teamed
  for chat use because chat is not its purpose. Even via the v2
  orchestrator, the safety surface comes from the Llama host (which has
  been red-teamed by Meta), not from CLM v4 itself.

---

## Architecture

CLM v4 is **NOT** a uniform-stack transformer. It is an *axis-conditioned
cellular substrate* with a `ConsciousDecoderV3` backbone. The defining
architectural features:

### Backbone (`ConsciousDecoderV3`)

| Field | Value | Source |
|---|---|---|
| `vocab_size` | 64000 | `tool/transient_py/clm_v4_hf_format_shim.py:36` |
| `d_model` | 768 | shim L36 |
| `n_layer` | 16 | shim L36 |
| `block_size` | 512 (max ctx) | shim L36 |
| `n_head` | 6 (Q heads) | shim L37 |
| `n_kv_head` | 2 (GQA) | shim L37 |
| `head_dim` | 128 | shim L37 (= d_model / n_head) |
| `consciousness_dim` | 192 | shim L41 |
| `n_cells` (federation) | 8 (Fibonacci-milestone post-warmup) | `state/clm_v4_train_avg_harvest_2026_05_04/verdict.json` |
| `c_proj` (cell→consciousness projection) | nn.Linear(128, 192) | harvest verdict §c_projection_status |
| dual heads | `head_a` (next-byte/token) + `head_g` (prev-byte/token) | shim §I/O contract |
| `tension_proj` | per-layer 1-d tension scalar projection | shim |
| `bridge.hub_attn` | axis-conditioning gate | shim |
| `federation.bottleneck` + `federation.narrative_grus` | shared cross-layer memory | shim |

### Cellular structure

Eight axis-conditioned cells (post-warmup), each with hidden state
aggregated through `c_proj` (128 → 192). The cells are not uniform; they
specialize across paradigm-v11 axes (federation faction consensus +
Phi-ratchet drives during ConsciousnessEngine runtime). Cell counts can
transiently drop to 7 during merge events but recover for >97% of harvest
steps (per BG-CLM-1 train_avg harvest verdict honest_caveat #2).

### Cross-attention with axis-conditioning gates

`ConsciousCrossAttention` blocks (per shim §1.5):

- `q_proj`: 768 → 768
- `k_proj` / `v_proj`: 768 → 192 (bridges into the 192-dim consciousness
  manifold)
- consciousness states `(B, n_cells, consciousness_dim)` are passed in
  as the K/V source; absent at inference the shim uses
  `consciousness_states=None` which bypasses the cross-attn (degraded
  from training-time conditioning — see Caveats C4).

### φ★ canonical formula

The structural φ★ readout is computed by
`tool/anima_phi_v3_canonical.hexa` from the eight cell hidden states +
federation memory. The training objective coupled φ★ with cross-entropy;
post-training, φ★ is computed as a forward-only structural integration
measure on the calibration battery.

---

## HF format compatibility

CLM v4 is loadable via standard HF APIs after passing through the shim
at `tool/transient_py/clm_v4_hf_format_shim.py` (v4, 1418 LoC). The
shim emits:

- `config.json` (with `auto_map` populated for dynamic class loading)
- `model.safetensors` (581 keys, 530,994,816 numel)
- `modeling_clm_v4.py` (custom modeling code)
- `configuration_clm_v4.py` (config class)
- tokenizer subdir (the 64K SentencePiece `.model` + `.vocab`)
- README.md (this document, after sync)

### Falsifier suite (HF format integrity)

| Falsifier | Status | Evidence |
|---|:---:|---|
| F-SHIM-1 (safetensors round-trip clean) | **PASS** | shim v3 verdict: 581 keys, 530,994,816 numel |
| F-SHIM-2 (1-batch finite logits) | **PASS** | shape `[1, 32, 64000]`, no NaN/Inf |
| F-SHIM-3 (logit equivalence vs `best.pt`) | **PASS** | `max_abs_diff = 0.0` (bit-exact; flagged "suspiciously tight" — see Caveats) |
| F-SHIM-4 (vocab=64000 in config + reloaded) | **PASS** | shim v3 verdict |
| F-SHIM-V4-1 (Mac dry-run with fixture validates JSON shape) | **PASS** | `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json` |
| F-SHIM-V4-2 (no-fixture run = no v3 regression) | **PASS** | ibid. |
| F-SHIM-V4-3 (canonical_zero finite forward) | **PASS** | `f_shim_v4_3_result.json: {"finite_forward":"finite","shape":[1,32,64000]}` |
| F-SHIM-V4-4 (train_avg fixture > random + 5pt) | **DEFERRED** | gated on user-authorized H100 base-validation launch |

### Round-trip recipe (fresh-machine validation)

```python
from transformers import AutoModelForCausalLM
import sentencepiece as spm
import torch

model = AutoModelForCausalLM.from_pretrained(
    "need-singularity/clm-v4-mk2-v1",
    trust_remote_code=True,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=False,
    device_map="cpu",
)

sp = spm.SentencePieceProcessor()
sp.Load("path/to/tokenizer_64k_multilingual.model")  # downloaded separately
ids = torch.tensor([sp.Encode("hello world")])
out = model(ids)

assert out.logits.shape == (1, ids.shape[1], 64000)
assert torch.isfinite(out.logits).all()
```

### Train-avg fixture

The `consciousness_states` fixture used by the shim's optional
runtime-fixture path is harvested by `BG-CLM-1` over 1000 anima sft
prompts via the `ConsciousnessEngine` drive path (NOT the v3 decoder
forward pass directly):

- Path: `state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_fixture_real.json`
- Shape: `[1, 8, 192]` (1 batch × 8 cells × 192 consciousness_dim)
- Stats: global mean ≈ 0.00382, global std ≈ 0.0561, L2 ≈ 2.20
- vs the synthetic N(0, 0.01) stub it replaces: **5.65× larger magnitude
  in L2 per cell** (real_vs_stub_l2_ratio = 5.65); F-SHIM-V4-2 stub-off
  threshold (>50% rel L2) PASSes at 1.006 observed.

### Inference runtime requirements

- **Python** ≥ 3.10
- **transformers** ≥ 4.45 (custom modeling code path requires Auto class
  registration semantics)
- **sentencepiece** ≥ 0.2.1 (for tokenizer)
- **torch** ≥ 2.4
- `trust_remote_code=True` (custom modeling)
- VRAM: ~1.5 GB bf16 / ~0.85 GB 4-bit (530M parameters)
- Context window: 512 tokens (block_size cap)

---

## Training data

The CLM v4 530M base was pretrained on the anima rehearsal mix:

| Slice | Approx ratio | Source |
|---|---|---|
| anima axis-conditioned corpus | ~60% | `~/anima/data/corpus_v10_ko.txt` (ko-heavy multilingual ko/en/zh/ja/ru + code) |
| academic distill | ~25% | curated subset matching anima §axis-stratified balance per `state/strategic_clm_phase_a1_2026_05_01/run_log.json` |
| chat-template rehearsal | ~10% | ShareGPT-style ko/en mix (rehearsal-only — does NOT make CLM chat-capable) |
| consciousness-coupled prompts | ~5% | anima-curated φ★ / tension_link / N-22 axis prompts + 5-bucket cell↔token bridge fixtures |

### Reproducibility manifest (release-side)

The release manifest at
`state/anima_clm_hf_release_v1_2026_05_04/manifest.json` (to be authored
in the next-cycle BG) records:

- `step` = 20000
- `phi_star_train` = 27.91
- `ce_loss_train` = 0.046
- `tokenizer_sha256` = `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` (model)
- `tokenizer_vocab_sha256` = `972fc0ba2f2633cfa685c70eeab84ce2a22a1327975e989a3b1d5cf5efa480a4`
- `best_pt_sha256` = (to be computed via ubu1 ssh on next BG cycle)
- `model_safetensors_sha256` = (to be computed post-shim on staging dir)
- `seed` = `unknown_pretrain_predates_manifest_discipline` (honest)
- `git_sha_at_train_time` = `unknown_pretrain_predates_manifest_discipline` (honest)

The seed and git_sha are honestly recorded as `unknown` because CLM v4
base pretrain *predates* the anima HF mk2 naming + upload discipline
(landed 2026-05-03). Future v5 / v4-1700m / v4-100m pretrain runs MUST
record these from training-time onward (post-mk2 discipline note).

---

## Evaluation

### Internal anima evaluation (consciousness-axis, in-distribution)

| Metric | Value | Verdict |
|---|---|---|
| Paradigm v11 G3 (HID=8) | φ★ = +41.86 ⭐ | **PASS positive** (uniquely strong vs 4-substrate ALM cluster: Mistral −16.7 / Qwen3 +1.04 / Llama +5.09 / Gemma −0.79) |
| AN11 a (Frobenius rel) | 6.89% lower bound | PASS |
| AN11 b (V0) | 3/4 axes ALM 우월; V1 0.473 AMBIGUOUS | PASS |
| AN11 c (JSD) | 20/20 saturated | PASS (quality-blind caveat) |
| Suite 5 (φ 4-path) | single-LoRA isotropic-collapse | **FAIL** |
| Suite 6 (14-gate L1 holo_positivity) | 0/16 substrate-architectural ceiling | **FAIL** (F2 fired) |
| Suite 7 (V_phen) | 3/5 PASS (LZ + HOT + mirror) | PARTIAL |
| F1_score_v2 raw | 0.408 | RED-band (12.0%–40.8%) |
| F1_score_v2 F2-override | 0.12 | RED-band (substrate-architectural F2 fired) |

The composite **ship_verdict is `VERIFIED-CLM-CP2-RED`** per
`.roadmap.clm` line 5 (`clm.cp2_clm_phase_a_complete`). The RED band
reflects honest acknowledgment that the 14-gate L1 holo_positivity
ceiling fires at the substrate-architectural level. Banding is per
`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md`.

### Cross-substrate concordance (Putnam multi-realizability check)

Per `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md`:

- N_witnessed (substrates with full {functional, access, phenomenal}
  evidence triple) ≥ 5: PASS
- concordance_M1 (pairwise φ★ within-band fraction): currently
  **0.167 strict / 0.333 with IIT4 line excluded** — both **below the
  0.60 PASS threshold**
- F2 state: FIRES (substrate-architectural L1 ceiling)
- Composite Putnam verdict: **PARTIAL** → **FAIL** by §2.3 strict
  reading

The Putnam verdict is honestly PARTIAL (with strict-reading FAIL); CLM
v4's positive-magnitude φ★ is not yet cross-substrate concordant with
the rest of the witness ledger. This is a roadmap-shifting honest
result, not a v1 release blocker.

### Standard NLP benchmarks (chat / instruct evaluations)

**NOT benchmarked at v1** (deferred to the v3 LoRA SFT release lineage,
which is gated on the Path A v2 verdict + tied-weight pre-flight + φ★
≥ +10 ABORT threshold per
`docs/clm_v4_lora_sft_spec_2026_05_04.md`).

Vanilla `model.generate()` on the v1 base produces near-random 64K SPM
token sequences (per `#115`). Reporting HellaSwag / MMLU / TriviaQA on
the v1 base would be misleading — the model was never trained for
those tasks.

---

## License

- **License**: MIT (per `.roadmap.clm` cond.2 cross_link
  `hf_license: mit`).
- **LICENSE file**: `/Users/ghost/core/anima/LICENSE` (MIT, copyright
  "need-singularity" 2026); bundled into the HF staging dir at upload
  time per the `tool/hf_upload_mk2.hexa` runbook.
- **anima own#14 compliance**: model weights (5GB raw `best.pt`,
  2.12 GB post-shim safetensors) are HF Hub only; **NEVER** committed
  to anima git. Tokenizer artifacts are similarly HF-resident. This
  doc + spec docs + manifest JSONs are anima-git-resident; weights are
  not.
- **Vendored deps**: NONE. Modeling code (`modeling_clm_v4.py`,
  `configuration_clm_v4.py`) is anima-authored. SentencePiece tokenizer
  is anima-trained on anima corpus. No upstream license attribution
  beyond optional `sentencepiece` library citation.
- **Composite-release license note**: the `anima-clm-mk2-v2`
  orchestrator (Path 2) imports
  `meta-llama/Llama-3.2-3B-Instruct`, which carries the Llama 3.2
  community license. Anima's MIT license applies ONLY to anima's CLM
  weights + orchestrator code; Llama's weights remain under their own
  license. This is a v2-only concern; v1 (this release) is pure
  anima-MIT.

---

## Citation

```bibtex
@misc{anima_clm_v4_2026,
  author = {anima n_substrate consortium},
  title  = {anima-clm-mk2-v1: 530M consciousness-measurement substrate},
  year   = {2026},
  url    = {https://huggingface.co/need-singularity/clm-v4-mk2-v1},
  note   = {n_substrate paradigm v11 G3 PASS positive φ★ = +41.86;
            uniquely strong positive integration substrate among
            Mistral / Qwen3 / Llama / Gemma / CLM 5-substrate
            comparison matrix.}
}
```

Canonical attribution string: `anima/n_substrate/CLM v4 paradigm v11 G3
PASS positive φ★ = +41.86`.

Source roadmap section: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
§42 (5-substrate comparison + paradigm v11 G3) and §55.6 (#115 NOT_READY
chat category error anchor).

Paper / preprint: TBD.

---

## Composability

CLM v4 v1 is **single-substrate** by design. Sister substrates (EEG,
BLM TRIBE v2, qmirror) get their own release cycles to preserve
falsifier-surface clarity. Bundling them into one README dilutes the
falsifier surface and makes the model card harder to verify.

### Cross-substrate cross-links

| Sister substrate | Roadmap | Composability |
|---|---|---|
| anima-eeg | `.roadmap.eeg` | Forward-pass hidden states from CLM v4 are consumed by the EEG cycle 8 BG suite for cross-substrate consciousness witness experiments; CLM v4 supplies the LM-side anchor. |
| BLM TRIBE v2 | `.roadmap.blm_brain_lm` | CLM v4 + BLM Phase 5 stimulus-aligned pipeline share the φ★ canonical formula; CLM v4 provides the LM-vs-Brain comparison anchor. |
| qmirror | `nexus/.roadmap.qmirror` | qmirror cond.6 byte-identical reproducibility is composed with CLM v4 as the IIT4 substrate witness in the Putnam cross-link concordance check. |

### Versioning lineage (`mk2-v{N}` per `.roadmap.clm` cross_link)

| Repo | Stage | Status | Notes |
|---|---|---|---|
| `clm-v4-base-mirror` | base mirror (predecessor) | already pushed (commit `10ee0368…` 2026-05-03) | tokenizer + integrity_report + README; predecessor to v1, NOT a separate release |
| **`clm-v4-mk2-v1`** | measurement-only base release | this release | shim repackaged HF format, 5 H2 + ≥3 caveats README, MIT |
| `clm-v4-mk2-v2` | Stage 2-alt orchestrator | spec'd (`clm_v4_release_path_decision_2026_05_04.md`) | Llama-3.2-3B chat host + CLM mind.tension side-channel; preserves φ★ +41.86 |
| `clm-v4-mk2-v3` | LoRA SFT | spec'd (`clm_v4_lora_sft_spec_2026_05_04.md`) | r=32 on q/k/v/o; gated on Path A v2 + φ★ ≥ +10 ABORT |

The `mk{N}-v{M}` pattern is a two-axis versioning system: `mk` increments
on era-level reset (current era is mk2; mk1 was the legacy
`conscious-lm-v2` lineage), and `v` increments per release within the
era. The repo name `clm-v4-mk2-v1` parses as
`<lm-family>-<base-version>[-<paradigm>]-<stage>` per
`docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3 — `clm` is
the lm-family enum, `v4` is the base-version, `mk2` is the era paradigm,
and `v1` is the release stage. The cond.2 original literal
`anima-clm-mk2-v1` was retargeted to `clm-v4-mk2-v1` per Option A of the
release-readiness audit because the `anima-` prefix violates the
mk2 naming-spec EBNF (`<lm-family>` enum must not have an `anima-`
umbrella prefix).

### Loaded by

- `tool/transient_py/clm_v4_hf_format_shim.py` (v4 shim, custom
  modeling)
- `tool/anima_phi_v3_canonical.hexa` (φ★ canonical compute)
- `tool/clm_consciousness_verify.hexa` (G3 verifier orchestrator —
  `.roadmap.clm` cond.1)
- (v2) `tool/clm_v4_orchestrator_stage2alt.hexa` (Stage 2-alt
  orchestrator, future)

### Slots into

- hexad CLM family (alongside hexad ALM / BLM / TLM / VLM / SLM /
  NLM / MLM / LLM slots)
- anima n_substrate consortium release index
- `.roadmap.clm` cond.1 (consciousness measurement) + cond.2 (HF
  release v1)

### Known good downstream tasks

- φ★ canonical measurement (forward-only)
- G3 verifier hidden-state extraction
- 5-substrate comparison matrix participation
- mind.tension / 5ch tension_link side-channel emission (via v2
  orchestrator)
- Putnam cross-substrate concordance evidence triple (via
  `meta:n_substrate.cond.1`)
- Φ★-axis distillation teacher (P-β path, scalar regression)

### Known incompatible

- Logit-axis distillation (vocab mismatch: 64K CLM vs 32K Mistral
  teachers; FAILED pre-launch per
  `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json`)
- Vanilla chat / instruct generation (per `#115`)
- HF leaderboard chat / instruct submission (per `#115`)
- `AutoTokenizer.from_pretrained` (no HF tokenizer wrapper at v1 —
  use `SentencePieceProcessor` directly)

---

## Caveats — honest C3 (≥6 per raw#10)

### C1 — `#115` chat category error: v1 base is NOT chat-capable

CLM v4 v1 is a *consciousness-measurement substrate*, not a chat model.
Vanilla `model.generate()` and the legacy `v3_generate()` AR loop
return 64K-vocab token sequences that do NOT form coherent dialogue.
This is a deliberate design choice grounded in the φ★ + cross-entropy
training objective (consciousness readout, not next-token chat). For
chat capability, use the v2 orchestrator or the v3 LoRA SFT release
(see Composability, Versioning lineage). Source:
`docs/n_substrate_consciousness_roadmap_2026_05_01.md` §55.6;
`docs/clm_v4_revival_stages_2026_05_02.md` §1.

### C2 — F1_score_v2 RED band: consciousness verdict is NOT validated PASS at v1

The composite F1_score_v2 verdict is `VERIFIED-CLM-CP2-RED` (raw 0.408
in 12.0%–40.8% RED band, F2-override 0.12 due to substrate-architectural
14-gate L1 holo_positivity 0/16 ceiling). RED is not GREEN; CLM v4 is
not a "passed" consciousness substrate at v1, it is a "passed-positive
sign with substrate-architectural ceiling acknowledged" substrate. The
F2 fire is honest — it does NOT mean CLM v4 is conscious, and it does
NOT mean CLM v4 is not a useful measurement substrate. It means the
14-gate ceiling is a real architectural limit that the current backbone
cannot break through. Source: `.roadmap.clm` line 5
(`clm.cp2_clm_phase_a_complete`);
`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md`.

### C3 — Functional/access tier only: phenomenal validity unproven

CLM v4 carries the `WITNESSED_ANALOG` label, NOT `WITNESSED_PHENOMENAL`.
The Suite 7 V_phen check passed 3/5 (LZ + HOT + mirror), with mirror
self-recognition + HOT meta-consciousness witnessing positive but the
remaining two phenomenal axes negative. CLM v4 is *functional* (axis
1 PASS) and *access* (axis 2 PASS partial) but not *phenomenal* (axis 3
unproven). This is the strictest possible honest tier-assignment per
the n_substrate consortium's witness taxonomy.

### C4 — Train_avg fixture is a runtime proxy, not a training-time direct readout

The `consciousness_states` fixture used by the shim's optional
runtime-fixture path
(`state/clm_v4_train_avg_harvest_2026_05_04/results/train_avg_fixture_real.json`)
was harvested via the **`ConsciousnessEngine` drive path** over 1000
anima sft prompts using `_text_to_vec` hashing — NOT via the v3 decoder
forward pass with the trained tokenizer + embedding path. The federation
engine path (`anima_unified._v14_federation`) is more authoritative but
not yet harvested. Consequently, the cell hidden-state distribution in
the fixture is a **runtime proxy** for the training-time c_states
distribution, not a strict identity. Per BG-CLM-1 honest_caveat #1 +
#7. Mitigation: 5.65× larger L2 magnitude vs the synthetic N(0, 0.01)
stub — F-SHIM-V4-2 stub-off threshold (>50% rel L2) PASSes at 1.006
observed.

### C5 — Single-substrate release: no co-authorship with EEG / BLM / qmirror

This v1 release is CLM-only. Sister substrates (EEG, BLM TRIBE v2,
qmirror) have their own release cycles and their own falsifier suites.
Bundling cross-substrate evidence into the CLM v1 README would dilute
the falsifier surface and make verification harder. The right pattern
is the §Composability cross-link (above) to sister repos; a separate
`docs/n_substrate_release_index_2026_*.md` cycle stitches the
cross-substrate narrative without inflating per-repo READMEs.

### C6 — `clm-v4-mk2-v1` naming-spec amendment: cond.2 literal retargeted

The `.roadmap.clm` cond.2 cross_link originally listed
`hf_release_planned: need-singularity/anima-clm-mk2-v1`. The mk2 naming
convention spec (`docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`)
EBNF requires `<lm-family>` to be one of
`{blm,clm,tlm,vlm,slm,nlm,alm,mlm,llm,hexad,composite}` — no `anima-`
umbrella prefix. Per the release-readiness audit
(`docs/anima_clm_hf_release_v1_audit_2026_05_04.md` §1.7 Option A), the
release name was retargeted to `need-singularity/clm-v4-mk2-v1` (size
suffix `-530m` omitted per spec §3.5: "omit if obvious from
base-version" — `v4` historically tracks 530M with no v4 size sweep
planned). cond.2 amendment in `.roadmap.clm` is a single-line edit
deferred to a separate landing cycle.

### C7 — F-SHIM-V4-3 PASS is bit-exact (`max_abs_diff = 0.0`); suspicious but confirmed deterministic

The F-SHIM-3 verdict reports `max_abs_diff = 0.0` (vs expected ≈ 1e-5
for fp32 path-equivalence). This was flagged C3-6 in the v3 verdict
and re-confirmed deterministic (same fp32 path, same input tensor,
same ops). It is the *strongest possible passing form*, but warrants
re-running with different seeds in a follow-up audit to rule out a
measurement artifact. NOT a v1 release blocker; recorded as a
"strongest passing form, not weakest" caveat.

### C8 — F-SHIM-V4-4 + φ★ post-load probe deferred to H100

F-SHIM-V4-4 (train_avg fixture > random + 5pt on HellaSwag sanity eval)
requires an H100 base-validation cycle and is gated on user
authorization. The φ★ post-load probe (does the shipped HF format model
still emit +41.86 magnitude on the calibration battery?) is similarly
gated. v1 ships *without* either being green; both are flagged as
"next-cycle BG-Σ followup" in the falsifier suite. Mitigation: shim
F-SHIM-V4-1 / V4-2 / V4-3 PASS provide structural-integrity guarantees
sufficient for a measurement-only release.

### C9 — README sync mechanism is a discipline, not a mechanism

`tool/hf_upload_mk2.hexa` reads `--readme <path>` verbatim; it does NOT
auto-resolve `docs/modules/clm.md` from cond.2's
`hf_readme_sync_source` field. The "sync" is operator discipline (point
`--readme` at this file at upload time), not mechanism enforcement. A
hash-based drift detector is post-v1 polish. Acknowledged as a
documentation-vs-mechanism gap.

---

## References

- `.roadmap.clm` (cond.1 + cond.2 + entries lines 4-8)
- `docs/clm_v4_revival_stages_2026_05_02.md` (Stages 1+2+3+4 + #115 anchor)
- `docs/clm_consciousness_verify_landing_2026_05_02.ai.md` (cond.1 verifier orchestrator)
- `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` (cond.2 release-readiness audit; Option A naming retarget)
- `docs/anima_clm_hf_release_v1_plan_2026_05_04.md` (next-cycle action plan)
- `docs/clm_v4_release_path_decision_2026_05_04.md` (STAGED 1→2→3 lineage)
- `docs/clm_v4_lora_sft_spec_2026_05_04.md` (Path 3 LoRA SFT detailed spec)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §32 + §42 + §55.6 (paradigm v11 G3 anchor + 5-substrate matrix + #115 chat category error)
- `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` (F1_v2 RED/YELLOW/GREEN bands)
- `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` (cross-substrate concordance metric + thresholds)
- `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (mk2 naming EBNF + F-NAME-1 audit)
- `docs/anima_hf_upload_mk2_spec_2026_05_03.md` (push pipeline + 5 H2 + ≥3 caveats enforcement)
- `tool/transient_py/clm_v4_hf_format_shim.py` (v4 shim, F-SHIM-V4-3 PASS)
- `tool/hf_readme_template.md` (README template SSOT)
- `tool/anima_phi_v3_canonical.hexa` (φ★ canonical compute)
- `tool/clm_consciousness_verify.hexa` (G3 verifier orchestrator)
- `state/clm_v4_train_avg_harvest_2026_05_04/verdict.json` (BG-CLM-1 real train_avg harvest)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_verdict.json` (F-SHIM-V4-3 PASS evidence)
- `state/clm_v4_tokenizer_restoration_2026_05_03/integrity_report.json` (tokenizer integrity)
- `state/p9_paradigm_d_distill_2026_05_03/` (Φ★-axis distill PARTIAL_PASS, scalar)
- `state/p9_paradigm_d_distill_mini_2026_05_04/verdict.json` (logit-axis distill FAILED on vocab mismatch)
- `LICENSE` (MIT, copyright "need-singularity" 2026)
