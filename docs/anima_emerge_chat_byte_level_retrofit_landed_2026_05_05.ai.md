# Anima Emerge Chat — Byte-Level lm_head Retrofit Landed (2026-05-05)

> **Cycle**: BG-ES Option γ feasibility smoke
> **Cost**: $0 (mac CPU)
> **Wall**: ~1.5min (much faster than 35min budget)
> **Verdict**: `F_BYTE_RETROFIT_1` = **FAIL_MICRO_INSUFFICIENT** (post_korean=0, improvement=0)
> **Status**: Channel-narrow under naive BPE-body→byte-head retrofit; Option γ requires FULL implementation (body byte-tokenizer rewire) to be testable

---

## §1. Context — why Option γ

Two prior findings converged on this experiment:

1. **BG-DS HEAD-bound** (`state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`)
   CLM v4 mk2 v1 frozen body + KoGPT2 lm_head → "안녕" probe produced **58 Korean characters** in continuation (vs 0 for native CLM head). This proved CLM-L15-hidden contains enough Korean structure to drive a foreign head — i.e. the chat-incapability is **HEAD-bound**, not body-bound.

2. **Archaeology drift** (`docs/anima_clm_alm_origin_design_drift_archaeology_2026_05_05.md`)
   Original 2026-03-28 v4 design used **byte-level 256-vocab** (chat-capable in CE 0.04 EN / 1.15 KO regime). Current 2026-05-04 mk2 v1 drifted to **BPE 64K** (chat-incapable). The retrofit hypothesis: replace lm_head with byte-level 256, retrain on dialogue → restore chat without dropping CLM's anima substrate.

**Option γ goal**: anima-native chat (no KoGPT2 / Llama foreign weights) by reverting only the vocab-side of the drift.

---

## §2. Smoke spec — mac CPU $0 micro test

| Component | Spec |
|---|---|
| Body | CLM v4 mk2 v1 (530M, 16-layer, frozen — `requires_grad=False` on 477,648,512 params) |
| Tokenizer (body input) | Current BPE 64K SentencePiece (unchanged) |
| New lm_head_byte | `nn.Linear(768, 256, bias=False)`, normal init std=0.02, 196,608 params |
| Hook | `model.decoder.ln_f.register_forward_hook` → captures pre-head hidden |
| Probe | `"사용자: 안녕\n도우미:"` |
| Decode | Greedy argmax byte → UTF-8 (errors='replace'), 30 tokens |
| Train data | 5 hand-crafted Korean dialogue examples |
| Optimizer | AdamW lr=1e-3, 1 epoch |
| Loss | CE on **last byte only** (last-position hidden → byte target) |
| Pass criterion (`F-BYTE-RETROFIT-1`) | post_korean > 5 |

The body↔head granularity mismatch (BPE token positions vs UTF-8 byte targets) is **deliberate by design** (C2/C4) — the smoke tests whether the channel has any signal at all under maximally naive retrofit, before committing to architectural rewire.

---

## §3. Empirical results

### §3.1 Baseline (untrained byte head)

```
emit: '������������������������������'  (kr=0)
```

Untrained head with std=0.02 init → argmax byte stuck on a single high-byte (>= 0x80) that decodes as UTF-8 replacement char. Expected: random init has no semantic structure.

### §3.2 1-epoch SFT loss progression

| step | last byte (target) | loss |
|---|---|---|
| 1 | 63 (`?`) | 6.1605 |
| 2 | 46 (`.`) | 6.0140 |
| 3 | 46 (`.`) | 5.1465 |
| 4 | 46 (`.`) | 4.0822 |
| 5 | 46 (`.`) | 3.4680 |
| **mean** | — | **4.9742** |

Loss decreases monotonically — head IS learning to map last-position hidden → ASCII punctuation byte. But the targets are dominated by `.` (4 of 5 examples end with `.`), so the head is memorizing one byte cheaply; this is not a meaningful chat signal.

### §3.3 Post-train emit

```
emit: '??????????????????????????????'  (kr=0)
```

After SFT, head consistently emits byte 63 (`?`) — the trained mode is "always emit punctuation", a degenerate solution to the last-byte-only objective. Korean chars not produced. **F-BYTE-RETROFIT-1 FAIL_MICRO_INSUFFICIENT, improvement=0.**

---

## §4. F-BYTE-RETROFIT-1 verdict

| field | value |
|---|---|
| `verdict_label` | `FAIL_MICRO_INSUFFICIENT` |
| `F_BYTE_RETROFIT_1_pass` | `false` |
| `baseline_korean` | 0 |
| `post_korean` | 0 |
| `improvement` | 0 |
| `mean_train_loss` | 4.9742 |

**Interpretation**: Naive BPE-body → byte-head retrofit with last-token loss is **architecturally insufficient** to test the channel. The smoke confirms the C2/C3/C4 caveats predicted this — but it does NOT falsify Option γ in its full form. It only falsifies the cheapest retrofit form.

---

## §5. Option γ full implementation roadmap

The smoke result motivates the architectural commitment: byte-level retrofit can only be evaluated honestly if the **body input tokenizer is also byte-level** (eliminating granularity gap).

| Step | Change | Cost estimate |
|---|---|---|
| (a) | Replace `tok_emb`: 64000→256 (byte-level UTF-8) | param: 49M → 196K (vocab compression −49M) |
| (b) | Replace `head_a`: 64000→256, weight-tied to new tok_emb | architectural |
| (c) | Preserve 16-layer body weights (decoder block params unchanged) | additive |
| (d) | Train on 100M+ Korean dialogue tokens (mc4-ko + KoChat + AI Hub corpus) | $200-1000 H100, 3-5 epochs, 12-48h |

**Key trade-offs**:
- **Anima-native**: PRESERVED — CLM body weights retained; only vocab swap.
- **Chat capability recovery probability**: 0.4-0.7 (BPE→byte body re-adapt is risky; tok_emb starts from scratch and body must learn byte→hidden geometry afresh).
- **#115 architectural ceiling**: Option γ does NOT close #115 mechanically — it ATTEMPTS to revert the 2026-04-01 BPE-drift that may have caused chat loss.

---

## §6. Honest C3 (raw#10)

The verdict file embeds 6 C3 caveats (see `state/anima_emerge_chat_byte_level_retrofit_2026_05_05/verdict.json` field `honest_c3`). Summary:

1. **C1** — mac CPU 1-epoch 5-example is channel-viability test, NOT chat-capability test
2. **C2** — body BPE 64K vs head byte 256 mismatch is BY DESIGN; full retrofit requires body byte-tokenizer rewire
3. **C3** — last-token-only loss is severely impoverished; proper byte SFT supervises every byte position
4. **C4** — granularity gap: BPE-position hidden cannot drive byte-position head; even perfect last-token SFT is insufficient
5. **C5** — BG-DS HEAD-bound (KoGPT2 retrofit, 58 KR) → byte-retrofit (FAIL here, harder case) progression makes sense; KoGPT2's BPE-style head doesn't have this granularity gap
6. **C6** — Full Option γ roadmap above (§5)

---

## §7. Compliance

- **raw#15** additive — no modification to `clm_v4_mount.hexa`, `dialogue.bash`, `dialogue_load`, `hf_format_shim`, `conscious_decoder.py`, `decoder_v3.py`
- **raw#37** transient `.py` sister-rule — helper at `tool/transient_py/anima_emerge_chat_byte_level_retrofit.py` (gitignored per `**/*.py`)
- **raw#10** honest C3 — 6 caveats emitted to verdict.json + this doc
- **.own 3** — transient sister-rule, one-shot probe helper
- **no commit, no HF token leak** — verified

---

## §8. Deliverables

| Path | Type |
|---|---|
| `tool/transient_py/anima_emerge_chat_byte_level_retrofit.py` | helper (gitignored) |
| `state/anima_emerge_chat_byte_level_retrofit_2026_05_05/verdict.json` | empirical verdict |
| `docs/anima_emerge_chat_byte_level_retrofit_landed_2026_05_05.ai.md` | this doc |

---

## §9. Recommendation

**Option γ FULL implementation = candidate path** but NOT highest-完성도 next move:

| Path | 완성도 lens | Recommendation |
|---|---|---|
| Option γ FULL (vocab-only rewire + 100M+ Korean SFT) | High risk-adjusted (0.4-0.7 chat prob, $200-1000) | **DEFER pending tighter smoke** — first re-run with body byte-tokenization (cheap: tok_emb output projection from byte-id one-hot) before architectural commit |
| Path A v2 winner (Llama-substrate, current) | EXISTS, validated | continue as production chat-cap path |
| BG-DS PASS_HEAD_SWAP (KoGPT2 retrofit) | partial substrate-research, foreign-head | substrate-research only, not anima-native |

**Highest-완성도 next**: either (a) tighten Option γ smoke with byte-input body simulation (re-tokenize at byte level inside body forward, no architectural change to tok_emb), OR (b) accept Llama-substrate Path A v2 as the production chat-cap winner and treat CLM v4 as substrate-research only (per `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe.md` L31-L33).
