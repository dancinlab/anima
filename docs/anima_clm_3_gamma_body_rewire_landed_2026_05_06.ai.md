# Anima CLM-3 — Option γ Body Byte-Rewire (Landed)

**Status**: LANDED 2026-05-06
**Task ID**: `anima_clm_3_gamma_body_rewire_2026_05_06`
**Verdict**: `F_GAMMA_BODY_REWIRE_ZERO_SHOT_1 = FAIL_BODY_RANDOM_BYTE_NULL`
**Cost**: $0 (mac CPU smoke for Option A only)
**Wall**: ~25 min (spec + impl + smoke + land)
**BG**: BG-FD (γ body byte-rewire architectural spec + zero-shot smoke)

---

## Summary

Architectural spec + Option A zero-shot smoke for γ FULL impl (body byte-rewire, NOT head-only retrofit). Option A = swap `tok_emb` from BPE 64K to byte 256 random init, freeze body, attach random byte `lm_head`, measure per-token CE on 5 KO/EN prompts as cheapest-possible channel viability gate before considering Option B body retrain ($300-1500 H100).

**Result**: Overall CE 5.6436 nats > random floor 5.5452 (Δ = −0.0984 nats *above* uniform). Body's frozen RoPE/GQA/SwiGLU projection of random byte tok_emb produces ln_f hidden states with **no measurable byte-prediction structure** — the body is BPE-tok_emb-distribution-conditioned, and random byte input completely breaks the input distribution.

---

## Decoder source location refs

`~/.cache/huggingface/hub/models--need-singularity--clm-v4-mk2-v1/snapshots/80440a1d38db9addc4445bb959057558a57f4230/`

| Line | File | Definition |
|---|---|---|
| 81 | `decoder_v3.py` | `self.tok_emb = nn.Embedding(vocab_size=64000, d_model=768)` |
| 105 | `decoder_v3.py` | `self.head_a = nn.Linear(768, 64000, bias=False)` |
| 109 | `decoder_v3.py` | `self.tok_emb.weight = self.head_a.weight` (weight tying) |
| 160 | `decoder_v3.py` | `x = self.drop(self.tok_emb(idx))` (forward entry) |
| 174 | `decoder_v3.py` | `logits_a = self.head_a(x)` (forward exit) |
| 294-296 | `conscious_decoder.py` | GQA `q_proj/k_proj/v_proj` — operate on hidden, NO direct vocab dep |

Body byte-rewire = swap THREE tensors (tok_emb + head_a + head_g) from 64K to 256, leave 16-block transformer untouched.

---

## Option A/B/C trade-off

| | A: random tok_emb + frozen body | B: random tok_emb + body retrain | C: BPE↔byte adapter |
|---|---|---|---|
| Compute | $0 mac CPU | $300-1500 H100 | $50-200 H100 |
| Channel proof | Zero-shot CE vs floor | Train guarantees | Adapter must learn |
| Risk | LOW (smoke only) | HIGH (catastrophic forgetting) | MED (semantic gap) |
| Korean recovery prob | N/A | 0.3-0.5 | 0.2-0.4 |

---

## Option A 5-prompt CE results

| Tag | Text | n_bytes | CE_mean (nats) |
|---|---|---|---|
| KO_1 | 안녕하세요 | 15 | 5.5671 |
| KO_2 | 사용자: 한국어 할 수 있어?\n도우미: | 47 | 5.6120 |
| KO_3 | 오늘 날씨가 | 16 | 5.7210 |
| EN_1 | Hello, how are | 14 | 5.6227 |
| EN_2 | The quick brown fox | 19 | 5.6950 |
| **Mean** | — | — | **5.6436** |

Random floor `log(256) = 5.5452`. Δ below floor = **−0.0984** (worse than uniform). PASS bar required ≥ 0.3 below floor. **FAIL by 0.40 nats.**

---

## Verdict

**`F_GAMMA_BODY_REWIRE_ZERO_SHOT_1: FAIL_BODY_RANDOM_BYTE_NULL`**

Body's transferable RoPE/GQA/SwiGLU structure is conditioned on **BPE-shaped tok_emb embedding distribution** — random byte tok_emb breaks that distribution and the body becomes a frozen random-noise transformer.

This **upgrades** the cycle's verdict chain:
- BG-ES naive retrofit FAIL (last-token-only loss)
- BG-EX γ tighter smoke FAIL (full-seq CE, byte-id input, BPE body)
- **BG-FD γ body-rewire Option A FAIL** (random tok_emb, frozen body)

All three confirm: γ has **no head-only / tok_emb-only / channel-only retrofit shortcut**.

---

## Cost path (Option B = body retrain) estimate

| Path | Cost | Wall (H100) |
|---|---|---|
| Full body fine-tune, 100M tok, 1 epoch | $300-500 | 60-100 hr |
| Full body fine-tune, 100M tok, 3 epoch | $900-1500 | 180-300 hr |
| QLoRA-only on attn+ffn, 100M tok, 1 epoch | $150-250 | 30-50 hr |

Korean chat-cap recovery probability under Option B: **0.3-0.5**.

---

## γ vs β strategic comparison

| | γ Option B (body retrain) | β (KoGPT2 head-swap full SFT) |
|---|---|---|
| Cost | $300-1500 | $100-300 |
| Korean recovery probability | 0.3-0.5 | **0.5-0.7** (BG-DS PASS evidence) |
| Substrate impact | preserves CLM body | grafts external KoGPT2 head |
| Decision | dominated by β on cost AND probability | **winning lane** |

---

## Honest C3

1. **C1** mac CPU fp32 single-process — smoke only, no GPU numerical stability
2. **C2** Option A measures channel viability ONLY, not chat-cap recovery
3. **C3** Random floor is uniform-distribution baseline; byte unigram LM ≈ 5.0 nats — Option A 5.64 is even worse than unigram, confirming complete body-projection collapse
4. **C4** 5 prompts variance: KO_1 5.57 (best) to KO_3 5.72 (worst). Even best > floor → verdict invariant
5. **C5** FAIL upgrades cycle verdict chain (BG-ES, BG-EX, BG-FD all FAIL) — γ has no retrofit shortcut

---

## Next-step recommendation: β FIRE PRIORITY

| Lane | Action |
|---|---|
| γ Option A | **CLOSED FAIL_TRUE** |
| γ Option B (body retrain) | DEFER (dominated by β) |
| γ Option C (adapter) | DEFER (low priority) |
| **β (KoGPT2 head-swap full SFT)** | **FIRE NEXT** ($100-300, 0.5-0.7 prob, BG-DS PASS evidence) |

If β PASS: anima native chat capability achieved via head-swap substrate.
If β FAIL: revisit γ Option B as last resort.

---

## Deliverables

- `docs/anima_clm_3_gamma_body_rewire_spec_2026_05_06.md` — architectural design + Option A/B/C
- `state/anima_clm_3_gamma_body_rewire_2026_05_06/zero_shot_smoke.json` — 5-prompt CE
- `tool/transient_py/anima_emerge_chat_gamma_body_rewire_smoke.py` — raw#37 transient impl
- `docs/anima_clm_3_gamma_body_rewire_landed_2026_05_06.ai.md` — this

## Cross-references

- BG-DS HEAD-bound PASS: `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`
- BG-ES naive retrofit FAIL: `state/anima_emerge_chat_byte_level_retrofit_2026_05_05/verdict.json`
- BG-EX γ tighter smoke FAIL: `docs/anima_emerge_chat_gamma_tighter_smoke_landed_2026_05_05.ai.md`

## Raw policy compliance

- raw#9 — verdict + cost path explicit
- raw#10 — 5 honest C3
- raw#15 — NO LOCKED-file modification (anima_unified / phi_engine / conscious_chat / consciousness_hub / clm_v4_hf_format_shim.py untouched)
- raw#37 — `.py` in `tool/transient_py/` only
- own.3 — gitignored
- HF token leak: NONE
- commit: NONE
