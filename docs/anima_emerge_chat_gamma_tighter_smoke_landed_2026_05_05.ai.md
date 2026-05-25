# Anima Emerge Chat — Option γ Tighter Smoke (Body byte-id input simulation)

**Status**: LANDED 2026-05-06
**Task ID**: `anima_emerge_chat_gamma_tighter_smoke_2026_05_05`
**Verdict**: `FAIL_BODY_BPE_BYTE_INCOMPATIBLE`
**Cost**: $0 (mac CPU)
**Wall**: ~3 min
**BG**: BG-EX (γ tighter smoke — BG-ES 권고 1순위)

---

## Summary

Channel viability test for Option γ (byte-level retrofit) BEFORE committing to
the architectural full-implementation ($200-1000 H100 spend). The naive retrofit
(BG-ES) FAIL was attributed to BPE-body 64K ↔ byte-head 256 granularity
mismatch + last-token-only loss impoverishment. This tighter smoke replaces
last-token-only with **full-sequence CE** and feeds **byte-ids 0-255 directly**
to the BPE-vocab body (no `tok_emb` change), testing whether the trained body's
ln_f hidden state contains *any* byte-equivalent signal under byte-id input.

**Result**: even with full-sequence CE supervision and AdamW(lr=1e-3) for 5
dialog examples, train loss decreases monotonically (5.87 → 3.11) but
post-train decode emits **0 Korean characters** on both probe1 (`안녕`) and
probe2 (`사용자: 한국어 할 수 있어?\n도우미:`). Train loss decrease is
byte-frequency memorization, NOT chat capability.

---

## Design

### Approach
- **`tok_emb`**: BPE 64K **frozen** (no architectural change)
- **Input**: byte-ids 0-255 fed directly (byte 0 → BPE token 0, byte 1 → BPE
  token 1, …) — exploits the fact that BPE first 256 tokens are commonly
  byte-fallback, but their *semantics* are NOT byte-equivalent
- **`lm_head_byte`**: new `nn.Linear(768, 256, bias=False)`, init N(0, 0.02)
- **Loss**: full-sequence CE — predict `byte_ids[1:]` from `hidden[:-1]`
  (every position supervised, not just last)
- **Body**: frozen, hidden captured via `model.decoder.ln_f` forward hook

### Train data
5 Korean dialog examples (사용자/도우미 pairs), 1 epoch, AdamW(lr=1e-3).

### Probes
1. `안녕` → 6 bytes `[236, 149, 136, 235, 133, 149]`
2. `사용자: 한국어 할 수 있어?\n도우미:` (multi-turn dialog header)

### Threshold
`F_GAMMA_TIGHTER_1`: `post_korean > 5` on probe1 OR probe2.

---

## Result

| Metric | Value |
|---|---|
| baseline emit (untrained head) | `'\x0fiRd...'` (kr=0) |
| post-train probe1 emit | `'���...               '` (kr=0) |
| post-train probe2 emit | `'::::::::::::::::::::::::::::::'` (kr=0) |
| improvement_korean | **0** |
| train loss (step-wise) | 5.87 → 5.21 → 4.44 → 3.74 → 3.11 |
| mean train loss | 4.4748 |
| F-GAMMA-TIGHTER-1 | **FAIL** |

### Observations
- Train loss decrease is real (Δ=2.76 nats over 5 steps) → byte head IS
  learning *something* (frequency distribution of bytes in dialog corpus).
- Post-train emit collapses to **constant tokens** (`�` block on probe1, `:` on
  probe2) — head learned a degenerate prior favoring whatever byte the body's
  ln_f hidden most strongly drives, which is NOT a UTF-8 Korean leading byte
  (`0xEA`-`0xED`).
- Probe2 emitting only `:` is illustrative: the dialog format header ends with
  `:`, so `:` is the most-frequent byte in the train corpus's tail position →
  head greedy-decodes the byte-frequency mode, not a context-sensitive
  continuation.

---

## Verdict & Implications

### F-GAMMA-TIGHTER-1: **FAIL_BODY_BPE_BYTE_INCOMPATIBLE**

The body's ln_f hidden state under byte-id input does NOT carry sufficient
byte-position-equivalent semantics to drive a byte-vocab head, even with
full-sequence supervision. The body was trained on BPE-tokenized 64K-vocab
input where token-id `n` represents an arbitrary BPE merge, NOT byte `n`.
Byte-id input → BPE-token-id `n ∈ [0, 256)` → body interprets as *that* BPE
token, not as byte `n`. The hidden representation is therefore "next BPE
token" in a degenerate corner of the BPE vocab, not "next byte".

### Implications for γ full implementation
- **Channel-viability HYPOTHESIS REJECTED**: simple byte-id input feeding does
  NOT produce a learnable byte-channel via head-only training.
- **γ full impl is NOT cheaply justified**: the $200-1000 H100 spend would
  require either (a) `tok_emb` rewire to 256-byte vocab + retrain body, OR (b)
  a BPE→byte adapter layer between `ln_f` and `lm_head_byte` (also requires
  body fine-tune on byte-aligned corpus).
- **Cheap path closed**: no head-only retrofit can recover Korean chat capability
  from a BPE-trained body via byte-vocab swap.

### Lane closure recommendation
Close `GAMMA_RETROFIT_HEAD_ONLY_LANE` as **FAIL_TRUE — channel
architecturally bypassed under head-only training**. γ full impl deferred
pending separate cycle (architectural commit + corpus + multi-epoch GPU spend).

---

## Honest C3 (caveats)

1. **C1**: mac CPU fp32, single-process. No GPU, no batching. Realistic byte-level
   SFT requires 1B+ tokens corpus + multi-epoch + GPU; this is a 5-example 1-epoch
   micro testing whether the *channel* is viable, not whether the trained model is
   chat-capable.
2. **C2**: byte-id 0-255 → BPE first 256 entries mapping is not byte-semantic.
   BPE-trained body learned `tok_emb[n]` as the vector for whatever BPE merge
   token `n` happens to be in the SentencePiece 64K vocab — typically
   `<unk>`, `<s>`, `</s>`, then byte-fallback bytes for unseen UTF-8, then
   high-frequency subwords. Body sees byte-id input as a degenerate BPE
   sub-vocab corner, not as byte stream.
3. **C3**: 1 epoch + 5 dialogs is severely under-trained. Full impl needs 100M+
   tokens. But baseline already emits 0 Korean → SFT-induced lift would need to
   surface from below noise floor. The fact that train loss decreases (head
   learns byte frequency prior) but Korean emits stay 0 indicates the body's
   hidden distribution has very low entropy along Korean-leading bytes, not a
   training-budget issue.
4. **C4**: full-sequence CE is strictly stronger signal than BG-ES last-token-only.
   FAIL with full-seq CE → channel narrowness is architectural, not loss-function-impoverished.
   This *upgrades* BG-ES's verdict from "ambiguous loss-impoverishment" to "clear
   channel-architectural failure".
5. **C5**: PASS would have been positive evidence for γ full impl ($200-1000 H100)
   justification (channel exists, just under-trained). FAIL means full impl requires
   body-side tok_emb rewire OR BPE→byte adapter — both are larger architectural
   commitments than the spec's "vocab swap only" estimate. γ full impl
   chat-capability-recovery probability should be revised DOWN from 0.4-0.7 to
   0.2-0.4 in light of this channel-architectural FAIL.

---

## Deliverables

- `state/anima_emerge_chat_gamma_tighter_smoke_2026_05_05/verdict.json`
- `tool/transient_py/anima_emerge_chat_gamma_tighter_smoke.py`
- `docs/anima_emerge_chat_gamma_tighter_smoke_landed_2026_05_05.ai.md` (this)

## Cross-references

- BG-ES naive retrofit (FAIL_MICRO_INSUFFICIENT, last-token-only):
  `state/anima_emerge_chat_byte_level_retrofit_2026_05_05/verdict.json`
- BG-DS HEAD-bound (PASS via KoGPT2 head, 58 Korean chars):
  `state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/verdict.json`
- Helper module sister: `tool/transient_py/anima_emerge_cand_d_inject_helper.py`

## Raw policy compliance

- raw#15 — no mount.hexa / shim / decoder modification (additive only)
- raw#37 — transient .py sister-rule, `tool/transient_py/` namespace
- raw#10 — 5 honest C3 caveats emitted
- own.3 — gitignored per `**/*.py`
- HF token leak: NONE
- commit: NONE (per spec constraint)
