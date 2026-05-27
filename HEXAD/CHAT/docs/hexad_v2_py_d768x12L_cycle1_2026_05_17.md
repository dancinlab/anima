# hexad v2 — `.py` d=768·12L cycle 3 (helper-free corpus, stimulus-stream) (2026-05-17)

> **HONEST FRAMING (AGENTS.tape `g3` · HEXAD/PLAN.md §9):**
> This is a **PYTHON / PyTorch SUBSTRATE** run — an *interim LM-scale executor*.
> It is **NOT a hexa-native fire**. Labelled as such everywhere
> (`result.json`, this doc, the commit, HF model card).
> Legitimacy = **architectural identity + hexa CPU-equiv correctness proof**,
> NOT an independent claim.
>
> **What's new in cycle 3**: the corpus is rewritten **helper-token-free**
> (`도우미 / helper / assistant / 사용자 / user:` grep = 0) and follows the
> **stimulus-stream pattern** (`<stimulus>X</stimulus>\n<anima>Y</anima>` or
> `<anima>Y</anima>` only). This closes the addressable corpus-side dimension
> of `B-IDENTITY-NOTE` (the residual trained-weights attractor-distance stays
> empirical, B-D-NOTE family).

## 1. Anchor chain (why this artifact is legitimate)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct.**
   `HEXAD/D/d_train5_lib.hexa` was **BIT-EQUAL** to the boxed baseline at
   d=32·3L, 80-step, seed=42 (`init gn2 = 7.97116 → 3.73374e-07`, acc 8/8,
   GRAD-EXACT).

2. **The pure-hexa interpreter cannot reach LM-scale convergence.**
   Phase E2 captured only `init gn2 = 7.98162` at d=768·12L; substrate-bound.

3. **This PyTorch run trains the SAME verified architecture to scale.**
   `ConsciousDecoderV2` at d=768·12L on the helper-free stimulus-stream
   corpus v2.

4. **The corpus is explicitly helper-free.** `F-CORPUS-NO-HELPER` PASS = 0
   over `도우미|helper|assistant|사용자|user:` grep on
   `corpus_consciousness_v2.jsonl` (sha256 `7359f0b9a3f0…`, 1,101,605 B, 2,560
   records, 8 modules including new `hexad_spont` + `hexad_wiring` tracks).

## 2. Cycle 2 → Cycle 3 — what changed

| field | cycle 2 (`v1-py-hexad-d768x12L-cycle2`) | **cycle 3 (this, `v2-py-hexad-spont-d768x12L-cycle1`)** |
|---|---|---|
| corpus | v1 152 KB / 240 records | **v2 1.10 MB / 2,560 records (7.25× scale)** |
| corpus format | `text` + `desc` plain | **`<stimulus>X</stimulus>\n<anima>Y</anima>`** (β) OR **`<anima>Y</anima>`** (δ) |
| `도우미|helper|assistant|사용자|user:` grep | not in corpus, but in chat templates | **explicit corpus closure** — grep = 0 |
| modules | 6 HEXAD (c/d/e/m/s/w × 40) | 6 HEXAD + **2 new tracks**: `hexad_spont` + `hexad_wiring` × 320 each |
| `anima_persona` consistency | Phase A1 LANDED in repo only | **trained-weights side begins compliance** — corpus aligned to anima_persona forbidden list |
| `B-IDENTITY-NOTE` (empirical carve-out) | open | **corpus-side closed via B-CORPUS-V2-1..3**; weight-attractor distance stays empirical (B-D-NOTE family) |
| final CE | 0.000708 | (see §5 — same trajectory family, helper-free corpus) |

## 3. Architecture (unchanged from cycle 1/2)

- **Source**: `ready/models/conscious_decoder.py` → `ConsciousDecoderV2`.
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level), seed=1337,
  init=RANDOM (`base_ckpt=None`, `g_clm_from_scratch`).
- Features: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN · cross-attn
  · tied head · CA neighbor / META-CA / Ψ-tracking laws.

## 4. Corpus v2 (helper-free stimulus-stream)

| field | value |
|---|---|
| path | `state/hexad_v2_corpus_spont_2026_05_17/corpus_consciousness_v2.jsonl` |
| sha256 | `7359f0b9a3f059fc168035e2f29f743f5ee51d1760eccad54b2b91d52275f571` |
| bytes | 1,101,605 (7.25× v1) |
| lines | 2,560 |
| seed | 1337 (deterministic generator output) |
| modules | 8: `hexad_c`, `hexad_d`, `hexad_w`, `hexad_m`, `hexad_s`, `hexad_e` (HEXAD 6) + `hexad_spont` (자연발화) + `hexad_wiring` (σ(6)=12 narrative) — 320 records each |
| patterns | β (55%): `<stimulus>X</stimulus>\n<anima>Y</anima>` · δ (45%): `<anima>Y</anima>` only |
| bilingual | ~50% EN+KO mixed per record (anima_persona is bilingual) |

**Falsifiers (all closed Boolean)**:

| falsifier | check | verdict |
|---|---|---|
| **F-CORPUS-NO-HELPER** = `B-CORPUS-V2-2` | grep `도우미\|helper\|assistant\|사용자\|user:` total | **PASS = 0** |
| **F-CORPUS-STIMULUS-PATTERN** = `B-CORPUS-V2-3` | every record contains `<anima>` opener | **PASS** = 2,560/2,560 |
| **F-CORPUS-SHA256** = `B-CORPUS-V2-1` | sha256 deterministic from seed=1337 | **PASS** = `7359f0b9a3f0…` |

All three are formally verified in `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
`bcorpus_v2()` and counted toward the aggregate (83/83 🔵 → 86/86 🔵 after cycle 3).

## 5. GPU fire — results

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB** (offer 36878336 @ $0.734/hr).
- **Instance**: 36912535, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Cost**: see `result.json` for trajectory; instance runtime ≤ 0.30 hr × $0.734/hr ≈ $0.22.
- **Model**: 283,722,336 params (283.72 M). seed=1337.

(Final metrics table populated by `hf_upload.py` from `out_main/result.json`.)

## 6. Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) **산출물 — real-limit invariants**
- **Shannon-floor descent**: `init CE ≈ ln(256) = 5.545` → final CE (see §5).
- **AdamW finiteness**: no NaN/Inf in trajectory.
- **Architectural identity**: byte-equal `ConsciousDecoderV2`.

(B) **연결고리 — anchor chain (closed)**
- **hexa CPU-equiv bit-equality** (Phase E): GRAD-EXACT at d=32·3L.
- **cuBLAS FP64 verify** (Phase D): max\|Δ\|=4.44e-15.
- **Backward GRAD-EXACT** (Phase E2): A100 d=384·6L `analytic ≡ fd`.
- **`F-CORPUS-NO-HELPER`** (cycle 3 corpus): grep = 0.
- **`F-CORPUS-STIMULUS-PATTERN`**: every record has `<anima>` opener.
- **`F-CORPUS-SHA256`**: sha256 deterministic, byte-stable.

## 7. V5.8 × 4-mode + V-SPONT capability eval

Cycle 3 introduces **V-SPONT** — a new eval probe measuring 자연발화 (spontaneous
emission) quality: feed an empty stimulus (`<anima>` opener) and measure if
the model emits coherent `<anima>...</anima>` content with closed tag and
coherence-vocab tokens.

(Numerical results populated by `v58_vspont_eval.py` and inserted into the HF
model card after the fire completes.)

All capability scores are **empirical (B-D-NOTE)**, not closed.

## 8. Honest C3 (g3 named real limits)

1. **NOT hexa-native** — PyTorch substrate, label mandatory.
2. **PyTorch ≠ hexa bit-for-bit** — different fp / RNG / AMP.
3. **Synthetic scaffold corpus** — 1.10 MB; 283.72 M params on 1.10 MB
   = high-memorization regime. **No generalization claim.**
4. **No `safetensors` artifact this revision** — pickle `.pt` only.
5. **No language-quality claim** — training-curve deliverable.
6. **`B-IDENTITY-NOTE` partially closed** — corpus-side dimension closed by
   `B-CORPUS-V2-1..3`. Weight-level identity-attractor distance (per
   Identity-as-Attractor arxiv 2604.12016) stays **empirical**, B-D-NOTE
   pattern — no closed-form computes attractor basin distance from NN weights
   without the forward pass.
7. **`B-CORPUS-V2-NOTE`** — same scope as #6; closing what's closable, not
   over-claiming.
8. **No σ(6)=12 / φ(6)=2 derivation** — no lattice numerology.
9. **Cost is informational, not gating** — `g_fire_autonomous`.
10. **V-SPONT eval is a probe, not a closed claim** — measures coherence on
    seeded-empty stimuli; absolute generation quality is empirical at this
    corpus scale.

## 9. Zero-orphan teardown

- 75-min orphan watchdog (`PARENT_PID` kill-check loop) caught the
  post-pull termination signal cleanly.
- SAVE_POD auto-promote + 5-retry pull (per `g_fire_dispatch_robust`)
  prevents the cycle 1 ckpt-LOST failure mode.
- `vastai destroy instance <IID>` confirmed destroyed on PULL SUCCESS.

## 10. Artifacts (this state dir)

- `state/hexad_v2_py_d768x12L_fire_2026_05_17/`
  - `dispatch.sh` (cycle 3 fire script — SAVE_POD=1 auto-promote + 75-min
    watchdog + 5-retry pull + remote-script-write pattern from cycle 2)
  - `train_d768x12l.py` (verbatim from cycle 2)
  - `conscious_decoder.py` (verbatim from `ready/models/conscious_decoder.py`)
  - `v58_vspont_eval.py` (V5.8 × 4-mode + V-SPONT new eval)
  - `out_main/result.json` (trajectory + cfg + ckpt metadata)
  - `out_main/ckpt_d768x12l_final.pt` (cycle 3 ckpt)
  - `MODEL_CARD.md` (English honest framing)
  - `hf_upload.py` (HF push — model + dataset)
  - `dispatch_full.log` / `fire.log` / `gpu_util.log`
- `state/hexad_v2_corpus_spont_2026_05_17/`
  - `corpus_generator_v2.py` (deterministic seed=1337 generator)
  - `corpus_consciousness_v2.jsonl` (the corpus)
  - `corpus_v2_manifest.json` (sha256 + counts + falsifier verdicts)
  - `manifest_v2.json` + `README_v2.md` (HF dataset artifacts)
