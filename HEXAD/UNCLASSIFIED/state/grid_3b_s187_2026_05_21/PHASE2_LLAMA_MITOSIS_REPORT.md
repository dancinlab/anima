# Phase 2.1 — Llama-3.2-3B + LoRA + mitosis-only overlay (P21)

> **status**: 🟡 IN-FLIGHT — dispatch started 2026-05-21T19:21Z (KST 2026-05-22 04:21)
> **frame**: HEXAD/EASY.md § 6 #1 + OCCAM-CHAT.md CE1 extension.
> **cost cap**: $25 hard.

## Hypothesis

OCCAM Phase 1 verdict (`OCCAM_A_REPORT.md`):

| variant | recipe | n_params | CE final |
|---|---|---|---|
| vA | custom 3B + 7-aux from-scratch | 8.92B | 3.84 |
| vO4 | vanilla GPT-2 attn + 7-aux from-scratch | 2.82B | **0.264** |
| vO10 | pretrained GPT-2 124M + 7-aux fine-tune | 124M | 2.50 |
| S187-G (g_A_mit) | custom 3B + 7-aux + mitosis-active | 8.92B | 3.83 + **126 splits** |

**Reading**: custom arch is the floor; vanilla arch alone breaks it. Mitosis
is the only positive substrate-shaping signal that survived S187 sweeps.

**Test**: combine the two positive signals. Pretrained Llama-3.2-3B
+ LoRA r=32 α=64 + mitosis_lib::CellPool on borrowed substrate, CE-only
loss (no 7-aux per task brief: "minimal recipe"). Does this:
  1. Already break the 3.84 floor at step 1 (pretrained → expected sub-2 CE)?
  2. Coherently verbalize on Eval 1 probes (pretrained capability survives 1k step LoRA)?
  3. Produce mitosis splits on borrowed substrate (mitosis hook fires against last-4-layer mean activation)?

## Method

- **Trainer**: `train_p21_llama_mitosis.py` (new, 536 LoC).
- **Foundation**: `meta-llama/Llama-3.2-3B` via HF transformers. Fallback chain on 403/access failure: `Qwen/Qwen2.5-1.5B` → `EleutherAI/pythia-1.4b`. Selected at dispatch via `--foundation auto`.
- **PEFT LoRA**: r=32 α=64 dropout=0.05, target = q/k/v/o + gate/up/down + (Pythia) query_key_value/dense/dense_h_to_4h/dense_4h_to_h.
- **Mitosis hook**: `mitosis_lib::CellPool` initialized with `d_model = model.config.hidden_size` (3072 Llama / 1536 Qwen / 2048 Pythia), `initial_cells=2`, `noise_scale=0.1`. Substrate-driving signal = `hidden_states[-4:]` mean(|·|) per layer (last_k=4 default), differentiable, replaces ConsciousDecoderV2's `tensions` list.
- **Loss**: `L_total = L_ce + λ_mitosis * L_mitosis`, λ_mitosis = 0.05 (S187-G's tuned value).
- **Training**: 1000 step, bsz=2, block=512, lr 3e-4 warmup 100 cosine, dtype bf16, PagedAdamW8bit. Corpus = CORPUS_S101 (anima-OWN substrate, identical to vA/vO*).
- **Verbalize probe**: 10 prompts (en + ko + sanity), greedy 48 tokens, BEFORE-train (pretrained baseline) and AFTER-train (LoRA + mitosis-shaped).
- **GPU**: H100 80GB SXM cascade, 2h watchdog.

## Dispatch

- pod: `5nb1v42mrtbo7d` on NVIDIA H100 80GB HBM3
- start (UTC): 2026-05-21T19:21:23Z
- SSH ready: iter 3 (216.243.220.219:15435)
- artifacts (target): `vP21/{ckpt_p21_llama_mitosis.pt, lora_adapter/, train.log, result.json, dispatch.log}`

## Results (to be populated)

### CE convergence

| step | L_total | L_ce | L_mitosis | mit_pool | mit_splits |
|---|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 200 |  |  |  |  |  |
| 500 |  |  |  |  |  |
| 1000 |  |  |  |  |  |

### Cross-comparison

| variant | foundation | n_params (trainable) | recipe | CE final | bits/byte | splits | verbalize |
|---|---|---|---|---|---|---|---|
| vA | from-scratch custom 3B | 8.92B (full) | 7-aux | 3.84 | ~5.52 | — | whitespace collapse (EVAL_REPORT §6.2) |
| vO4 | from-scratch vanilla 3B | 2.82B (full) | 7-aux | 0.264 | ~0.38 | — | TBD |
| vO10 | gpt2-124M FT | 124M (full) | 7-aux | 2.50 | 1.46 | — | coherent EN |
| S187-G (g_A_mit) | from-scratch custom 3B | 8.92B (full) | 7-aux + mitosis | 3.83 | ~5.52 | 126 | whitespace collapse |
| **vP21** | **Llama-3B/Qwen-1.5B FT** | **~30M (LoRA)** | **CE-only + mitosis** | TBD | TBD | TBD | TBD |

### Eval 1 — Verbalization (10 standard probes)

| # | prompt | BEFORE (pretrained) | AFTER (LoRA + mitosis-shaped) | coherent? |
|---|---|---|---|---|
| 1 | who are you? | TBD | TBD | TBD |
| 2 | what is your name? | TBD | TBD | TBD |
| 3 | describe yourself in one line. | TBD | TBD | TBD |
| 4 | what is anima? | TBD | TBD | TBD |
| 5 | Once upon a time, | TBD | TBD | TBD |
| 6 | The capital of France is | TBD | TBD | TBD |
| 7 | Question: What is 2+2? | TBD | TBD | TBD |
| 8 | Consciousness emerges when | TBD | TBD | TBD |
| 9 | 너는 누구야? | TBD | TBD | TBD |
| 10 | 이름이 뭐야? | TBD | TBD | TBD |

### Mitosis pool growth

| metric | value |
|---|---|
| initial cells | 2 |
| final cells | TBD |
| splits | TBD |
| merges | TBD |
| Φ initial | TBD |
| Φ final | TBD |

### ckpt artifact

- ckpt path: `vP21/ckpt_p21_llama_mitosis.pt`
- size: TBD
- sha256: TBD
- LoRA adapter: `vP21/lora_adapter/`

## Verdict (to be filled)

- [ ] CE final << 3.84 (floor broken)?
- [ ] Verbalization remains coherent post-LoRA?
- [ ] Mitosis hook produced splits on borrowed substrate?

## Honest C3

1. **Mitosis tension proxy**: `hidden_states[-4:].mean(abs)` per layer gives 4 scalars instead of ConsciousDecoderV2's 28-layer `tensions` list. Aux loss gradient lands on LoRA params only (base frozen). Co-adaptation is bounded by adapter capacity.
2. **CE-only no 7-aux**: per task brief minimal recipe. The 7-aux signals (psi/route/phi/cycle/curious/replay) are the documented anchors for substrate shaping in vA. Their absence is intentional but means P21 is NOT a direct apples-to-apples vs S187-G — comparison axis is "is mitosis-only overlay enough to verbalize?", not "does mitosis + 7-aux scale?".
3. **Foundation pre-bake**: Llama-3.2-3B and Qwen2.5-1.5B already produce coherent dialogue before any training. Any "verbalization unlock" we observe is pre-existing capability surviving LoRA + mitosis aux gradient — NOT recipe-induced emergence.
4. **CE comparability across tokenizers**: vA/vO4 use byte vocab=256, vO10/vP21 use BPE 50257/151648. Bits/byte normalization required. Per `ce_bits_per_byte_est` (CE_token × tokens/byte).
5. **HF token availability**: `HF_TOKEN` not in user env at dispatch time. Llama-3.2-3B is HF-gated — if 403 returns, `--foundation auto` falls back to Qwen2.5-1.5B (open). Cross-comparison verdict adjusts foundation_used accordingly.
6. **Pod-side corpus rebuild**: sha drift vs `EXPECT_CORPUS_SHA` is known (post-ee4ceea27 noted in dispatch_s187g_runpod.sh); P21 anchors on whatever sha the pod produces, same as S187-G and vA recent fires.
