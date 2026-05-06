# anima emerge chat — semantic bridge (CLM v4 hidden → vocab NN) — LANDED 2026-05-05

## Summary (one paragraph)

BG-AS tested whether CLM v4 hidden states (post-`decoder.ln_f`) carry semantic
content recoverable via cosine nearest-neighbor against the model's own token
embedding matrix `decoder.tok_emb` (V=64000, D=768). The hypothesis was: if
hidden state has semantics (BG-AE/L confirmed input-conditional variation,
hsd>10) but `lm_head` decode is fragmentary, an external semantic bridge —
in this minimal form, NN against the tied-style embedding table — should emit
semi-coherent tokens. **Verdict: `FAIL_ALL` (n_coherent = 0/2).** Both
single-step top-10 NN and iterative 15-step greedy NN produced byte-fallback /
control-character degenerate output (top1 = SP id 32 = `\x1c`, sim=0.4523;
iterative emits id 32 once then id 10 = `\x06` repeating 14×).

## Inputs / setup

- **Model**: `need-singularity/clm-v4-mk2-v1` (HF, fp32, mac CPU)
- **Tokenizer**: `tokenizer_64k_multilingual.model` (SentencePiece 64k)
- **Prompt**: `"안녕"` (single Korean greeting; encoded to 2 tokens)
- **Hook**: forward hook on `decoder.ln_f` capturing post-norm hidden;
  shape `[1, 2, 768]`
- **Vocab embedding**: `decoder.tok_emb.weight` shape `[64000, 768]`
  (D matches hidden_dim — no fallback to `decoder.head_a` needed)
- **Helper reuse**: `tool/transient_py/anima_emerge_cand_d_inject_helper.py`
  (`_try_load_model`, `_load_tokenizer`)

## Method

1. Load CLM v4 + sentencepiece on CPU fp32.
2. Locate `tok_emb` by scanning `named_modules` for `Embedding` with
   `num_embeddings > 50000` → found `decoder.tok_emb (64000, 768)`.
3. Locate `lm_head` for fallback → found `decoder.head_a (64000, 768)`.
4. Hook on `decoder.ln_f`, single forward of `"안녕"`.
5. **Decode A — single-step top-10 cosine NN**: cos(hidden[:, -1, :],
   `tok_emb.weight`) → top-10.
6. **Decode B — iterative cosine NN (15 steps)**: at each step,
   re-forward the growing sequence, take last-token ln_f hidden,
   take argmax cosine NN, append.
7. `is_semi_coherent`: `len ≥ 5 ∧ (Korean+ASCII letters ≥ 5) ∧
   max_char_freq ≤ 50%`.

## Results

### (a) tok_emb / lm_head 발견

| Module | Path | Shape | Used |
|---|---|---|---|
| tok_emb | `decoder.tok_emb` | (64000, 768) | YES (NN target) |
| lm_head | `decoder.head_a` | (64000, 768) | not needed (no dim mismatch) |
| ln_f hook | `decoder.ln_f` | output [1, 2, 768] | OK |

`hidden_dim=768` exactly equals `vocab_dim=768`. NN ran against `tok_emb`
weight directly.

### (b) cosine NN top-10 decoded tokens

```
rank 1:  id=  32  decode='\x1c'  sim=0.4523
rank 2:  id= 157  decode='�' sim=0.3926
rank 3:  id= 152  decode='�' sim=0.3863
rank 4:  id= 116  decode='p'      sim=0.3588
rank 5:  id= 236  decode='�' sim=0.3369
rank 6:  id=  47  decode='+'      sim=0.3244
rank 7:  id=  51  decode='/'      sim=0.2987
rank 8:  id= 119  decode='s'      sim=0.2917
rank 9:  id=  49  decode='-'      sim=0.2797
rank 10: id=  10  decode='\x06'   sim=0.2773
```

All top-10 IDs are in the **byte-fallback / control-char range** (id < 256
for SP byte-fallback subword token block). No Korean characters, no
greeting-context tokens. Top sim is only 0.4523 — well below the
"meaningful match" cosine threshold (typical ≥ 0.7 for tied-emb LMs).

### (c) iterative cosine 15-step emit

```
text   = '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'
ids    = [32, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
```

Single non-repeating emit (id=32 / `\x1c`) followed by an immediate
attractor at id=10 / `\x06` for 14 consecutive steps. **Strong
degeneracy** — the hidden-state geometry, after one emit, falls into a
fixed-point in cosine-NN space.

### (d) coherent verdict

```
n_coherent = 0 / 2
verdict    = FAIL_ALL
```

Neither decode produced text with ≥5 Korean+ASCII letters or with
max-char-frequency ≤ 50%. The iterative emit fails on both criteria
(no letters; max char `\x06` appears 14/15 times = 93%).

### (e) 5 honest C3 + 다음 단계 추천

**C1 — mac CPU fp32 single forward.** No GPU sampling variance; result
is deterministic for this prompt + this checkpoint.

**C2 — cosine NN bypasses lm_head.** Train-time decode is `lm_head(h)`
softmax argmax (logit-space, includes scale/bias). NN cosine is
`argmax cos(h, tok_emb[i])` (geometry only). They coincide only under
tied-embedding + no-scale conditions. CLM v4 has separate `decoder.head_a`
with same shape as `tok_emb` but possibly distinct weight; we tested NN
only against `tok_emb`, not `head_a`. **Follow-up**: re-run NN against
`decoder.head_a.weight` to test the train-time decode geometry directly.

**C3 — single prompt `"안녕"`** (2 SP tokens). Cannot generalize to chat
capability; this is a 1-trace existence check for hidden→vocab semantic
mapping under one specific input.

**C4 — dim-mismatch path untested.** No fallback to `lm_head.weight`
triggered (both 768-dim). The iterative-emit attractor at id=10 may be
an artifact of the unhooked forward path: each iterative step rebuilds
RoPE cache and re-runs full attention; degenerate output may indicate
**substrate self-conditioning** (model learned to output `\x06`-class
when self-fed) rather than intrinsic geometry failure.

**C5 — `is_semi_coherent` is anima-internal heuristic.** Threshold
choices (≥5 letters, ≤50% max-char-freq) are unvalidated against human
judgment; a string of distinct random tokens with no semantics could
PASS. Conversely, valid Korean output of 4 chars would FAIL. The
**FAIL_ALL signal is dominated by degenerate `\x06` repetition**, not
heuristic edge cases.

### Cross-context interpretation

The pattern (top-10 = byte-fallback + control + 1-char ASCII; sim < 0.5;
iterative attractor) is consistent with the **#115 chat-incapability
architectural hypothesis**: CLM v4 hidden state encodes axis structure
(Φ★ stable, axis-discrim survives per BG-L 0.0360) but does **NOT**
encode token-level lexical content recoverable by cosine geometry on
its own embedding table. This aligns with:
- F-CLM-LORA-2 FAIL_REGRESSION (-36.298pp vs Llama Path A v2; substrate
  retains axis but loses lexical chat capability),
- Pβ Φ★-axis Paradigm D 50K F-Pβ-3 FAIL_TRUE composite=0.01176 (chat
  capability decoupled from Φ★ stability).

**Semantic bridge in this minimal form does NOT recover lexical content.**
A learned bridge (linear projection trained to map ln_f hidden → external
small Korean LM input embedding space) is the next viable step, but this
moves outside the "$0 mac CPU 30 min" envelope.

### 다음 단계 추천 (ranked by 완성도 lens)

1. **A — repeat NN against `decoder.head_a.weight`** (~10 min, $0).
   Tests whether train-time logit projection (head_a) has different
   geometry than `tok_emb`. If head_a NN also degenerate → architectural
   FAIL confirmed for self-vocab bridge. If head_a NN coherent →
   `tok_emb` is wrong target (architecture has untied embeddings).
   **Highest signal/cost ratio.**

2. **B — multi-prompt sweep** (5 KO + 5 EN prompts, single-step NN
   only, ~20 min, $0). Tests if degeneracy is prompt-universal or
   `"안녕"`-specific. Strengthens FAIL claim or surfaces input
   dependency.

3. **C — external small-Korean-LM rephrase via prefix concat**
   (1-3 hr, $0 mac CPU, requires HF download of e.g. `klue/roberta-small`).
   Encode CLM v4 ln_f hidden → projection → prefix → external LM
   conditional decode. Outside this BG envelope.

4. **D — DEFER** to substrate-research only stance (consistent with
   `feedback_clm_v4_lora_sft_chat_lift_falsified_substrate_safe`):
   accept #115 architectural FAIL and stop chasing chat capability on
   CLM v4 substrate.

**Recommendation: A first** (10 min, decisive on tied-vs-untied
architecture). Then B if A confirms degeneracy. C and D both downstream
of A's outcome.

## Artifacts

- `tool/transient_py/anima_emerge_chat_semantic_bridge.py` (~280 LoC,
  raw#37 transient)
- `state/anima_emerge_chat_semantic_bridge_2026_05_05/aggregate.json`
- `state/anima_emerge_chat_semantic_bridge_2026_05_05/verdict.json`

## Compliance

- raw#37: transient .py under `tool/transient_py/` namespace, gitignored.
- raw#15: additive only — no modifications to mount.hexa, dialogue.bash,
  dialogue_load, hf_format_shim, or any production runtime.
- raw#10: 5 honest C3 emitted to `verdict.json` and this doc.
- raw#0: no commit.
- $0 cost; ~12s wall (load + forward).
- HEXA_PY=`/Users/ghost/core/anima/.venv-eeg/bin/python` (anima-canonical
  py runner).
- No HF token leak; no secrets in logs/aggregates.
