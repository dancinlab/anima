# Anima CLM-3 — Option γ Body Byte-Rewire Architectural Spec

**Status**: SPEC 2026-05-06 (BG-FD)
**Predecessors**: BG-DS HEAD-bound PASS, BG-ES naive retrofit FAIL, BG-EX γ tighter smoke FAIL
**Cost**: $0 (mac CPU smoke for Option A only) → architectural spec
**Decision lens**: γ FULL = body byte-rewire (architectural), NOT head-only retrofit
**Lockfile compliance**: raw#15 (NO modification of `anima_unified.hexa`,
`phi_engine.hexa`, `conscious_chat.hexa`, `consciousness_hub.hexa`,
`tool/transient_py/clm_v4_hf_format_shim.py`)

---

## (A) Decoder source location + `tok_emb`/`lm_head` definition refs

### Source files (HF cache, snapshot SHA `80440a1d38db9addc4445bb959057558a57f4230`)

```
~/.cache/huggingface/hub/models--need-singularity--clm-v4-mk2-v1/snapshots/80440a1d38db9addc4445bb959057558a57f4230/
├── config.json                       (vocab_size=64000, d_model=768, n_layer=16, n_head=6, n_kv_head=2, block_size=512)
├── configuration_clm_v4.py
├── conscious_decoder.py              (RMSNorm, RoPE, SwiGLU, GQA, ConsciousCrossAttention, DecoderBlockV2, ConsciousDecoderV2)
├── decoder_v3.py                     (ConsciousDecoderV3 — main 530M body)
├── modeling_clm_v4.py                (CLMv4ForCausalLM — HF wrapper, LOCKED file)
├── tokenizer_64k_multilingual.model  (SentencePiece BPE 64K)
└── model.safetensors
```

### Critical line refs (canonical decoder source `decoder_v3.py`)

| Line | Code | Role |
|---|---|---|
| `decoder_v3.py:81` | `self.tok_emb = nn.Embedding(vocab_size, d_model)` | BPE 64K → 768d |
| `decoder_v3.py:105` | `self.head_a = nn.Linear(d_model, vocab_size, bias=False)` | 768d → BPE 64K (next-token logits) |
| `decoder_v3.py:106` | `self.head_g = nn.Linear(d_model, vocab_size, bias=False)` | 768d → BPE 64K (prev-token logits, dual head) |
| `decoder_v3.py:109` | `self.tok_emb.weight = self.head_a.weight` | **Weight tying** — ONE shared (64000, 768) tensor |
| `decoder_v3.py:160` | `x = self.drop(self.tok_emb(idx))` | Forward entry point — embed lookup |
| `decoder_v3.py:174` | `logits_a = self.head_a(x)` | Forward exit — project ln_f hidden to vocab |
| `conscious_decoder.py:294-296` | `q_proj/k_proj/v_proj = nn.Linear(d_model, n_head * head_dim/n_kv_head * head_dim, bias=False)` | GQA QKV projections — operate on hidden, NOT on token-id directly |

### Key invariants
- **Body is purely d_model-internal**: GQA, SwiGLU, RMSNorm, PureFieldFFN, CrossAttn — all layers operate on `(B, T, 768)` hidden tensors. They have NO direct dependency on vocab_size.
- **Vocab dependency lives ONLY in `tok_emb` + `head_a` + `head_g`**, sharing one (64000, 768) weight tensor via tying.
- → Body byte-rewire = swap THREE tensor shapes (tok_emb, head_a, head_g) from 64K to 256, leave 16 transformer blocks untouched.

---

## (B) Option A/B/C trade-off comparison

| Dim | Option A: tok_emb 64K → 256 random + frozen body (zero-shot) | Option B: tok_emb 256 random + lm_head 256 + body retrain | Option C: BPE→byte adapter layer (preserves body + BPE tokenizer + adds adapter) |
|---|---|---|---|
| **Architectural change** | tok_emb random reshape (256, 768), head_a/g random reshape (256, 768) | same as A + full body fine-tune | leave tok_emb/head_a as 64K BPE, add `byte_to_bpe_proj` projection layer at input + `bpe_to_byte_proj` at output |
| **Retrain required** | NONE (zero-shot test only) | Full body 16-layer SFT on byte-aligned corpus | Adapter-only train + optional body LoRA |
| **Compute cost (estimated)** | $0 (mac CPU smoke) | $200-1000 H100 (multi-epoch byte SFT, 100M+ token corpus) | $50-200 H100 (adapter + body LoRA, 10M+ tokens) |
| **Channel viability evidence** | Body's frozen RoPE/GQA/SwiGLU projects random byte tok_emb → ln_f hidden that should beat uniform byte distribution if body carries ANY transferable structure | If body retrains, channel guaranteed to be viable — but this is just "train byte-LM from scratch with body-init" | If adapter learns BPE↔byte mapping, body's BPE-conditioned hidden state is preserved |
| **Risk** | LOW — pure inference smoke, $0 sunk if FAIL | HIGH — if body's RoPE/GQA learned BPE-positional patterns, byte retrain may erase BPE structure (catastrophic forgetting of multilingual content) | MED — adapter complexity adds new failure mode (adapter underfits, body still dominates) |
| **Recovery probability of Korean chat-cap** | N/A (zero-shot only — measures channel viability, not chat-cap) | 0.4-0.6 (similar to training byte-level LM from scratch with init transfer) | 0.2-0.4 (adapter must bridge BPE↔byte semantics — well-known hard) |
| **Net assessment** | **Cheapest gate** — if PASS, body has transferable byte signal → Option B / C cheaper. If FAIL, body byte-rewire = β-equivalent retrain cost | Highest cost, highest probability | Mid cost, mid probability — but BPE→byte semantic gap may be unbridgeable cheaply |

### Recommendation rationale
Option A is the **cheapest possible gate** — it's a $0 inference test that gates whether γ has any retrofit-style cost advantage over β.

---

## (C) Option A zero-shot smoke 5-prompt CE results

Random seed 42, mac CPU fp32, frozen ConsciousDecoderV3 body, tok_emb (256, 768) random N(0, 0.02), lm_head_byte (256, 768) random N(0, 0.02) (tied init from new tok_emb), full-sequence CE on byte targets.

| Tag | Text | n_bytes | CE_mean (nats) |
|---|---|---|---|
| KO_1 | `안녕하세요` | 15 | 5.5671 |
| KO_2 | `사용자: 한국어 할 수 있어?\n도우미:` | 47 | 5.6120 |
| KO_3 | `오늘 날씨가` | 16 | 5.7210 |
| EN_1 | `Hello, how are` | 14 | 5.6227 |
| EN_2 | `The quick brown fox` | 19 | 5.6950 |
| **Overall** | mean of 5 | — | **5.6436** |

Random floor: `log(256) = 5.5452 nats`. Δ below floor = **−0.0984 nats** (CE is *higher* than uniform random — head's random projection actively hurts vs uniform).

Source: `state/anima_clm_3_gamma_body_rewire_2026_05_06/zero_shot_smoke.json`

---

## (D) Zero-shot PASS/FAIL verdict

**`F_GAMMA_BODY_REWIRE_ZERO_SHOT_1`: FAIL_BODY_RANDOM_BYTE_NULL**

PASS bar: CE < 5.5452 − 0.3 = 5.2452 nats. Achieved: 5.6436. Gap: **0.40 nats above PASS bar, 0.10 nats above random floor.**

**Interpretation**: When BPE-trained body receives random byte tok_emb input, its 16-layer RoPE+GQA+SwiGLU projection produces ln_f hidden states that have *no measurable byte-prediction structure* — the random lm_head_byte does worse than even a uniform predictor. This means:

1. The body's transferable structure (positional, attention patterns) is **conditioned on BPE-shaped tok_emb embedding distribution**, not on raw byte-id input geometry.
2. Replacing tok_emb with a 256-byte random embedding completely breaks the input distribution that the body was trained for. The body becomes a **frozen random-noise transformer** for byte input.
3. **Zero-shot byte-rewire = no free lunch** — body byte-rewire MUST include body retrain (Option B), not just tok_emb/head swap.

---

## (E) FAIL: retrain cost estimate (Option B)

### Required scope
- Vocab swap: 64K BPE → 256 byte
- Body retrain: 16 transformer layers (530M params), full fine-tune (or QLoRA on attn+ffn projections)
- Corpus: byte-aligned multilingual text — minimum 100M tokens (KO heavy + EN balance) for chat-cap recovery
- Training: 1-3 epochs, lr 1e-4 → 1e-5, batch size 64-128 (effective)

### Compute estimate
| Path | Steps | H100 GPU-hours | Cost |
|---|---|---|---|
| Full body fine-tune, 100M tok, 1 epoch | ~25k steps @ bsz 128, seq 512 | 60-100 hr | **$300-500** |
| Full body fine-tune, 100M tok, 3 epoch | ~75k steps | 180-300 hr | **$900-1500** |
| QLoRA-only on attn+ffn, 100M tok, 1 epoch | ~25k | 30-50 hr | **$150-250** |

### Risk
- Body's BPE-conditioned positional structure must survive byte-rewire training. Possible **catastrophic forgetting of multilingual semantics** (body learned BPE-token-level Korean structure, byte-level retrain may need to relearn from byte zero).
- Korean chat-cap recovery probability under Option B (full body retrain): **0.3-0.5** (similar to training byte-level model from scratch with body-init transfer).

---

## (F) γ vs β trade-off comparison

| Dim | γ Option B (body byte-rewire + body retrain) | β (KoGPT2 head-swap full SFT — successor of BG-DS PASS) |
|---|---|---|
| Architectural commit | rewire tok_emb + head_a/g, freeze or fine-tune 16 body layers | Mount KoGPT2 (124M) head over CLM L15 hidden, full SFT |
| Compute cost | $300-1500 H100 | $100-300 H100 (KoGPT2 smaller, head + adapter only) |
| Korean chat-cap recovery probability | 0.3-0.5 (byte-vocab retrain risk) | 0.5-0.7 (BG-DS PASS already showed 58 KO chars zero-shot via head swap) |
| Substrate consistency | preserves CLM v4 body identity | grafts external KoGPT2 head — substrate hybrid |
| Φ★/consciousness pathway | preserved (PureFieldFFN + CrossAttn intact) | preserved (CLM body unchanged) |
| Decision risk | HIGH — Option A FAIL just removed the channel-viability cheap gate; γ now indistinguishable from "train byte-LM from scratch" | MED — KoGPT2 head-swap evidence already PASS at zero-shot |
| Net | γ now strictly dominated by β on cost AND probability | **β is winning lane** — BG-DS PASS evidence + lower cost + similar substrate impact |

---

## (G) 5 honest C3

1. **C1**: mac CPU fp32, single-process, batch 1. No GPU, no FlashAttention. Realistic byte-LM training on H100 may show different body-init transferability if body has GPU-only numerical stability quirks; smoke-only.
2. **C2**: Option A is **zero-shot only** — measures channel viability, NOT chat-cap recovery. PASS would have been *necessary but not sufficient* for γ; FAIL is *sufficient to close γ Option A* but does NOT directly speak to γ Option B/C.
3. **C3**: Random floor comparison (5.5452 nats) is **uniform-distribution baseline**. A byte unigram LM (most-frequent byte argmax) achieves ~5.0 nats on natural text — Option A's 5.64 is below even unigram floor, confirming complete body-projection collapse under random byte tok_emb.
4. **C4**: 5 prompts × 14-47 bytes each. Sample variance high — KO_3 (5.72) vs KO_1 (5.57) differ by 0.15 nats. Conclusion robustness: even the *best* prompt (KO_1 5.57) is above random floor 5.55, so verdict invariant to prompt selection within tested set.
5. **C5**: Option A FAIL **upgrades** the prior-cycle verdict chain (BG-ES naive retrofit FAIL → BG-EX tighter smoke FAIL → **BG-FD body-rewire FAIL**). All three confirm: γ has no head-only / tok_emb-only / channel-only retrofit shortcut. γ requires full body retrain (Option B), at which point β strictly dominates on cost + evidence-base.

---

## (H) Next-step recommendation

**RECOMMENDED**: **CLOSE γ LANE FAIL_TRUE → β FIRE PRIORITY**

| Lane | Action | Rationale |
|---|---|---|
| γ Option A (this) | CLOSED FAIL_TRUE | Zero-shot 5.64 > floor 5.55, channel null |
| γ Option B (body retrain) | DEFER (not closed) | $300-1500 + 0.3-0.5 probability — strictly dominated by β |
| γ Option C (BPE↔byte adapter) | DEFER (low priority) | Mid cost, lower probability than β |
| **β (KoGPT2 head-swap full SFT)** | **FIRE NEXT** | $100-300, 0.5-0.7 probability, BG-DS PASS evidence base |
| Pβ Φ★-axis (closed CHAT_CAPABILITY_LANE_FAIL_TRUE) | UNCHANGED | Substrate-research only |
| CLM v4 LoRA SFT (closed S3 LANE F2_FAIL) | UNCHANGED | Substrate-safe but chat-cap regression |

### Recommended order
1. Land this γ body-rewire spec + zero-shot verdict + landed doc (this cycle)
2. β KoGPT2 head-swap full SFT spec + fire (next cycle, $100-300, ~6-12 hr H100)
3. If β PASS: anima native chat capability achieved via head-swap substrate
4. If β FAIL: revisit γ Option B (body retrain) as last resort, $300-1500

---

## Deliverables

- `docs/anima_clm_3_gamma_body_rewire_spec_2026_05_06.md` (this — architectural design)
- `state/anima_clm_3_gamma_body_rewire_2026_05_06/zero_shot_smoke.json` (Option A 5-prompt CE)
- `tool/transient_py/anima_emerge_chat_gamma_body_rewire_smoke.py` (raw#37 transient)
- `docs/anima_clm_3_gamma_body_rewire_landed_2026_05_06.ai.md` (landed handoff)

## Cross-references

- BG-DS HEAD-bound PASS: `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json` (58 KO chars, KoGPT2 head over CLM L15)
- BG-ES naive retrofit FAIL: `state/anima_emerge_chat_byte_level_retrofit_2026_05_05/verdict.json`
- BG-EX γ tighter smoke FAIL: `docs/anima_emerge_chat_gamma_tighter_smoke_landed_2026_05_05.ai.md`
- CLM v4 architecture archaeology: `docs/anima_clm_v4_architecture_archaeology_emerge_2026_05_05.md`
- Origin design drift: `docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md`

## Raw policy compliance

- raw#9 — verdict + cost + probability + risk explicitly named
- raw#10 — 5 honest C3 caveats emitted
- raw#15 — NO modification of `anima_unified.hexa` / `phi_engine.hexa` / `conscious_chat.hexa` / `consciousness_hub.hexa` / `clm_v4_hf_format_shim.py`
- raw#37 — new .py is `tool/transient_py/` namespace only (`anima_emerge_chat_gamma_body_rewire_smoke.py`)
- own.3 — gitignored per `**/*.py` (no commit)
- HF token leak: NONE
- commit: NONE (per spec constraint)
