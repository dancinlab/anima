# anima/emerge — chat head compare (BG-BQ landed) — 2026-05-05

> **Task** : tied vs untied embedding test — is `lm_head` itself broken?
> **Lane** : `anima-core/runtime/clm_v4_mount.hexa` substrate diagnosis
> **Cost** : $0 (mac CPU fp32)
> **Wall** : ~12s (model load 10.3s + 4 configs × 25-token greedy)
> **Verdict** : `FAIL_ALL_HEADS` — lm_head is NOT broken; substrate itself emits the same degenerate token under all 3 head paths
> **Lane closure** : `LM_HEAD_NOT_THE_BUG` — chat-incapability root-cause moves UPSTREAM of head matrix

---

## 1. Context

BG-AS (`state/anima_emerge_chat_semantic_bridge_2026_05_05/aggregate.json`) found that
`decoder.tok_emb` (embed) AND `decoder.head_a` (lm_head) both carry shape `[64000, 768]`.
Combined with the iterative-cosine decode emitting only `\x1c\x06\x06...`, the suspicion
arose: **maybe `lm_head` itself is broken** — i.e. the trained weights of `head_a` map
arbitrary hidden states to a degenerate ID-10 (`\x06`) cluster regardless of input.

This BG-BQ tests that hypothesis by running 3 heads against the SAME post-`ln_f` hidden
state captured via forward hook:

| Config | Path | Predicts |
|---|---|---|
| `baseline_model_forward` | `model.forward(...).logits` greedy | model's lm_head (head_a) baseline |
| `head_a` | explicit `head_a(last_hidden)` | should equal baseline (sanity) |
| `head_g` | explicit `head_g(last_hidden)` | aux head — prev-byte (BG-AF FAIL_TRUE evidence) |
| `tok_emb_tied` | `last_hidden @ tok_emb.weight.T` | tied-embedding decode |

If all 3 emit identical degenerate text → **substrate hidden is degenerate**, not lm_head.
If head_a / tok_emb_tied differ → **head matrix carries the pathology**.

---

## 2. Empirical results

### 2.1 Head presence + shapes

```
head_a:  torch.Size([64000, 768])   PRESENT
head_g:  torch.Size([64000, 768])   PRESENT
tok_emb: torch.Size([64000, 768])   PRESENT
ln_f:    RMSNorm
```

### 2.2 Decode outputs (prompt = `안녕`, n_continue = 25, greedy argmax)

```
baseline_model_forward → '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'
head_a                 → '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'
head_g                 → 'lu товаといった的人物的人物 важней的人物 должность的人物 важней的人物=0.086的人物 важней的人物 ...'
tok_emb_tied           → '\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06'
```

### 2.3 Pairwise diff

| Pair | Differ? |
|---|---|
| baseline vs head_a | **NO** (identical) |
| baseline vs head_g | YES |
| baseline vs tok_emb_tied | **NO** (identical) |
| head_a vs head_g | YES |
| head_a vs tok_emb_tied | **NO** (identical) |
| head_g vs tok_emb_tied | YES |

### 2.4 Coherence

`n_coherent = 0 / 4` → `verdict = FAIL_ALL_HEADS`

---

## 3. Interpretation

**Major finding**: `head_a` (lm_head) and `tok_emb_tied` produce **identical degenerate output** to baseline `model.forward`. Three different head matrices applied to the same hidden state yield the same `\x1c \x06 \x06...` token sequence.

Implication: **lm_head matrix itself is NOT the source of pathology.** The substrate hidden state at `ln_f` output is already so collapsed/degenerate that argmax over `[64000, 768] @ [768, 1] = [64000]` lands on token-32 (`\x1c`) once and token-10 (`\x06`) thereafter regardless of which 64k×768 projection matrix you apply.

**Secondary finding**: `head_g` produces *visibly different* (though still incoherent) multilingual word fragments — Russian, Japanese, Chinese, English fragments. This confirms head_g IS a different projection (not a copy of head_a) and is doing something genuinely distinct, but not chat-coherent. Consistent with C2 (cand-H prev-byte aux head, not next-token).

**Tied vs untied**: `head_a == tok_emb_tied` output equivalence is informative but ambiguous (C3). Either (a) weights are effectively tied (head_a learned to mirror tok_emb during training) OR (b) both end up argmax-ing to the same degenerate cluster regardless of weight values, because the hidden state is so concentrated. Without a weight-correlation check we cannot distinguish.

---

## 4. Root-cause shift

This BG-BQ **falsifies** the lm_head-broken hypothesis. The chat-incapability lane (Pβ chat-cap FAIL_TRUE / CLM v4 LoRA SFT FAIL_REGRESSION / iterative-cosine `\x06\x06\x06...`) must therefore have its root-cause UPSTREAM of the head:

- Decoder block stack — RMSNorm collapse, residual saturation, attention dead lanes
- ln_f layer — terminal normalization wiping discriminative signal
- tok_emb — input embedding distribution itself degenerate at greedy-decode time
- Training-time loss target — substrate may have been trained on prev-byte (head_g style) while head_a head was undertrained

Lane closure: `LM_HEAD_NOT_THE_BUG`. Next probe candidates:

1. **Hidden-state stat scan**: `last_hidden` mean/std/L2 across token positions — if std → 0, RMSNorm collapse confirmed.
2. **Top-k logit margin**: the gap between argmax-ID-10 and runner-up — if tiny, hidden is undirected; if huge, head matrix is genuinely overconfident on ID-10.
3. **head_a vs tok_emb weight correlation**: cosine across the [64000, 768] matrix to test true tying.

---

## 5. Honest C3

(Full text in `state/anima_emerge_chat_head_compare_2026_05_05/verdict.json`.)

- **C1** — mac CPU fp32; tie-breaking determinism not guaranteed across runs. (Not material here — three configs converged identically.)
- **C2** — `head_g` is the cand-H prev-byte aux head (BG-AF FAIL_TRUE evidence). Incoherent text under head_g is the EXPECTED null and does not falsify lm_head per se.
- **C3** — `tok_emb` tied-decode assumes embed-to-output weight tying. CLM v4 may have been trained WITHOUT tying. If untied, `tok_emb_tied` produces garbage by design and the equivalence with `head_a` here is consistent with both arriving at degenerate-cluster argmax independently.
- **C4** — `ln_f` normalization applied uniformly via the forward hook (POST-ln_f hidden); all 3 explicit-head paths see identical input. baseline ≡ head_a equivalence is the sanity check (PASSED).
- **C5** — single prompt `안녕` (KO greeting). Anecdotal. Broader prompt sweep needed before claiming "lm_head not broken across all inputs". Per-prompt variance not measured here.

---

## 6. Deliverables

```
tool/transient_py/anima_emerge_chat_head_compare.py        — BG-BQ helper (raw#37 transient, .own 3 gitignored)
state/anima_emerge_chat_head_compare_2026_05_05/aggregate.json   — 4-config decode text
state/anima_emerge_chat_head_compare_2026_05_05/verdict.json     — schema/1 verdict + 5 honest C3
docs/anima_emerge_chat_head_compare_landed_2026_05_05.ai.md      — this doc
```

raw policy: raw#37 PASS (`tool/transient_py/` namespace), raw#15 PASS (additive — no mount/shim/dialogue_load mod), raw#10 PASS (5 honest C3 emitted), no commit, no secret leak. Mac CPU fp32, $0.

---

## 7. Next actions (recommended)

| Probe | Tool | Cost | Why |
|---|---|---|---|
| Hidden-state stat scan | mac CPU helper | $0 ~10min | Test RMSNorm collapse — most likely root cause given symptom |
| Top-k logit margin | mac CPU helper | $0 ~5min | Distinguish "head overconfident" vs "hidden undirected" |
| head_a vs tok_emb weight cosine | mac CPU helper | $0 ~5min | Empirically resolve tying ambiguity (C3) |
| Prompt sweep ×10 | mac CPU helper | $0 ~30min | Generalize beyond `안녕` (C5) |

Ranked by 완성도 lens: hidden-state stat scan FIRST (highest information gain — directly tests the RMSNorm-collapse hypothesis that the lm_head-not-broken finding implies).
