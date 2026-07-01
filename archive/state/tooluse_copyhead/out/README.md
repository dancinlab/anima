---
license: apache-2.0
base_model: dancinlab/anima-clm-chat-rung0-byte-18m
tags:
- anima
- byte-lm
- copy-head
- pointer-network
- tool-use
- agent
- lane-g
language:
- en
- fr
- de
- es
- ko
---

# anima-clm-chat-rung0-byte-18m-copyhead

**🟢 PASS-grade.** A byte-level (vocab256) CLM with a **gated pointer-attention copy head**
that closes the verbatim argument-copy residual surfaced by the #1833/#1835 tool-use fires.

- **Substrate**: GPU (Lane G; a_lane_akida_gpu_split — NOT AKIDA). Pool host aiden, RTX 5070.
- **Base**: `dancinlab/anima-clm-chat-rung0-byte-18m` (18.13M, ConsciousLMReconstructed, d384/6L/4H).
- **This model**: base trunk + A/G heads + a 49,665-param **copy head** (18.18M total).
- **Scope (a_scale_honest_scope)**: TOY 18M only — transfer to mid/7B UNVERIFIED.
- **p1..p8 clean**: the copy head is an architectural copy operator, not identity/persona/role
  injection; the `0xFE`/`0xFF` sentinels are learned grammar.

## The problem it fixes

The byte-LM mouth CALLS the tool (call_rate 0.83–1.0) but INVENTS a training-distribution-shaped
key instead of COPYING the asked held-out key → `correct_call = 0/36` (#1835 🔴 CLOSED-NEGATIVE).
A standard byte-LM at 18M has **no mechanism to copy a token from the prompt verbatim**.

## The copy head (gated pointer-attention)

At each output step the model produces, besides the standard A/G byte-LM logits:
- a copy query `q_c = W_q·h_t`, copy keys `k_i = W_k·h_i` over all context positions `i ≤ t`,
- causal copy attention `a = softmax(q_c·k_i / √d)`,
- a **copy distribution over the 256-byte vocab** = `scatter_add(a_i onto input_byte[i])`
  — "probability the next byte is a verbatim copy of the byte at the attended input position",
- a learned **gate** `g_t = sigmoid(W_g·h_t) ∈ [0,1]`.

Final next-byte distribution: `P = (1 − g_t)·softmax(lm_logits) + g_t·copy_dist`.
NLL is taken on that mixed distribution, so gate + pointer learn jointly with the LM.

This routes "the asked key in the prompt" → "the call arg" **structurally** (the pointer attends
the key's bytes and the gate opens to copy them) instead of the LM head sampling a plausible key.

### Byte-eq gate (HEXA-FUSION graph-off style)

`COPY_HEAD=0` → the head is fully bypassed and the forward is **byte-identical** to the original
arch: `max|Δ| forward = 0.0`, `max|Δ| forward_logprob(copy=off) = 0.0` (verified).

## Falsifier verdicts (verbatim, p7 script-checked — NO perplexity)

```
BYTE-EQ (head-OFF == original arch): forward max|Δ|=0.0 logprob(copy=off) max|Δ|=0.0 -> PASS
F-COPYHEAD-ARGCOPY         : with_copyhead correct_call=0.9722 (>= 0.5?) grounding=0.9722 (>= 0.5?)  [baseline #1835: correct_call=0.0 grounding=0.0]  -> PASS
F-COPYHEAD-OFF-MIRROR      : same ckpt, copy OFF correct_call=0.0 grounding=0.0 (MUST be < 0.5) -> PASS
F-COPYHEAD-RANDINIT-MIRROR : random_init grounding=0.0 (MUST be 0) -> PASS
F-COPYHEAD-NOTOOL-MIRROR   : with_copyhead+tool_disabled grounding=0.0 (MUST be 0) -> PASS
RULING: GREEN
```

**correct_call 0/36 → 35/36 (0.9722)** on the held-out PB01..PB36 keys (values in neither corpus).
The single miss is an over-copy (PB28 → PB288), an honest 1/36.

### Anti-Goodhart mirrors

- **head-OFF** (same ckpt, copy gate forced off) → correct_call 0.0: the **head** does the copy work,
  not the LM weights.
- **random-init + head** → grounding 0.0: learned capability, not a trivial/leaked copy.
- **tool-disabled** → grounding 0.0: the end-to-end win is REAL grounding, not cosmetic markers.

## Corpus note (the v1 → v2 fix)

The first fire (v1, fixed 3-char training keys) produced `correct_call=0.0` because the copy head
learned to copy exactly a 3-char span and TRUNCATED the 4-char probe (`PB01 → PB0`). The corpus was
regenerated with **variable-length keys (2–5 chars, including 4)** so the pointer learns
length-general copy. The head was correct all along; the corpus key-length had to match the probe.

## Files

- `tooluse_copyhead_with_copyhead_18m.pt` — the trained ckpt (state + config + copy_head flag).
- sha256: `7941a538755b896eb1e4dfcc0f3d5c2e4de277349e6d2e63ed58ef6b8f0461f7`

## Reproduce

`training/tooluse_copyhead_ab.py` (in the anima repo) — `--base-ckpt chat_rung0_18m.pt
--corpus argcopy_corpus_v2.txt --steps 2500 --batch 32`.

Lane G · a_lane_akida_gpu_split (GPU, NOT AKIDA) · a_paper_negative_ok lineage (#1835 🔴 → this 🟢).
