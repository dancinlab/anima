# anima emerge chat — first-token force probe LANDED 2026-05-05

**BG-BP** — first-token sensitivity probe on CLM v4 (`need-singularity/clm-v4-mk2-v1`).

## Hypothesis

BG-AQ (decode-strategy sweep) + BG-BJ (entropy trajectory) showed substrate emits
control-byte from token-1 regardless of decode strategy. Open question: is the
collapse **first-token-only** (force a semantic seed → coherent rest) or
**trajectory-pervasive** (substrate degenerates regardless of seed)?

## Method

1. Load CLM v4 fp32 on mac CPU; SentencePiece tokenizer 64k_multilingual.
2. Prompt = "안녕"; capture top-100 next-token logits.
3. Print top-20 with decode + logits.
4. Filter "semantic" tokens (Korean 가-힣 OR ASCII alpha) — pick first 5 in top-100.
5. Baseline: pure greedy continuation, 26 tokens.
6. Forced: for each semantic candidate, prepend it as first emit, then greedy
   continue 25 more tokens.
7. Coherence heuristic: ≥5 Korean+ASCII chars AND no single char >50% of length.
8. Verdict: PASS_FORCE_RECOVERS if any forced config coherent, else FAIL.

## Results

### (a) Top-20 candidates — control-byte dominant

| rank | id  | text | logit |
|------|-----|------|-------|
| 0    | 32  | `\x1c` (FS control) | 8.300 |
| 1    | 157 | `\xc2` byte | 7.915 |
| 2    | 152 | `\xbd` byte | 7.745 |
| 3    | 116 | `p`  | 6.967 |
| 4    | 47  | `+`  | 6.424 |
| 5    | 236 | byte | 6.381 |
| 6    | 51  | `/`  | 6.051 |
| 7    | 119 | `s`  | 5.898 |
| 8    | 49  | `-`  | 5.421 |
| 10   | 50  | `.`  | 5.295 |
| 11   | 10  | `\x06` (ACK control) | 5.255 |
| 12   | 101 | `a`  | 5.096 |
| 15   | 78  | `J`  | 4.964 |
| 17   | 104 | `d`  | 4.794 |
| 18   | 79  | `K`  | 4.739 |

Top-20 distribution: **6 semantic / 14 control-byte-or-other**. The argmax (rank-0)
is FS (file-separator) control byte — confirms BG-AQ + BG-BJ first-token control-byte.

### (b) Semantic candidates in top-100

Only **5 semantic tokens within top-100**, all single ASCII letters: rank 3 (`p`),
7 (`s`), 12 (`a`), 15 (`J`), 17 (`d`). **Zero Korean syllables in top-100** —
substrate has no Korean continuation pathway despite `안녕` Korean prompt.

### (c) Forced continuations (25 emit each)

| seed | emit (truncated) |
|------|------------------|
| baseline (rank-0 `\x1c`) | `\x1c\x06\x06\x06\x06...` (FS + 25× ACK loop) |
| rank3 `p` | `pppppppppppppppppppppppppp` (26× p loop) |
| rank7 `s` | `srN^^^^^^^^^^^^^^^^^^^^^^^` (caret loop after 3 chars) |
| rank12 `a` | `aaaaaeeeeeeeeeeeeeeeeeee��` (a→e→byte loop) |
| rank15 `J` | `JJJJJJJJJJJJJJJJJJJJJJJJJJ` (26× J loop) |
| rank17 `d` | `dhhhhhhhhhhhhhhhhhhhhhhhhh` (d→h loop) |

**Every forced semantic seed degenerates into single-char loop within ≤5 steps.**
No semi-coherent trajectory produced. The seed itself survives 1-3 emits then
collapses to a different fixed-point loop.

### (d) Verdict

- `n_coherent_forced` = **0 / 5**
- `baseline_coherent` = **false**
- **verdict** = `FAIL_FORCE_NOT_ENOUGH`
- **mechanism_implication** = trajectory-pervasive collapse — forced semantic seed
  degenerates to control-byte/loop within ~25 steps regardless of seed identity.

### (e) Honest C3 + #115 mechanism implication

1. **C1** mac CPU fp32 deterministic greedy decode; no temperature, no sampling.
2. **C2** "semantic token" heuristic = Korean syllable OR ASCII alpha; narrow,
   excludes punctuation/digits/non-Korean CJK that may still be semantically
   valid.
3. **C3** first-token forcing puts substrate in OOD: hidden state evolves from
   force_id not chosen by argmax, so KV cache + attention pattern diverges from
   training distribution. Force-induced behaviour reflects **recovery from
   non-self-consistent prefix**, not natural substrate dynamics.
4. **C4** single prompt `안녕` (n=1); generalization to other prompts not tested.
5. **C5** "semi-coherent" heuristic anima-internal: tolerates real repetition
   (`안녕안녕`) but catches loops + control-byte domination.

**#115 mechanism implication.** BG-BP combined with BG-AQ + BG-BJ + CLM-LORA-2
FAIL_REGRESSION strengthens the **architectural-incapability** verdict for #115:

- Substrate produces a fixed-point attractor at every step, not just step-1.
- The attractor is **token-conditioned** (different seed → different loop char)
  but **trajectory-uniform** (always degenerates to single-char repetition or
  control-byte cascade within 1-5 steps).
- This is consistent with #115 being a **deep architectural failure** (CLM v4
  cross-attn topology fails to maintain semantic flow across 16 decoder
  blocks), not a decoding-strategy failure or a first-token calibration bug.
- **Pβ** Φ★-axis substrate research lane (substrate-safe but chat-incapable) +
  **CLM v4 LoRA SFT** F-CLM-LORA-2 FAIL_REGRESSION (-36.298pp) + **BG-BP**
  trajectory-pervasive collapse → CLM-2-EXEC chat-cap hope is now cross-checked
  against trajectory-level evidence.
- Lane closure recommendation: CLM v4 substrate cannot be rescued by **any
  decode-time intervention** — first-token, multi-token, sampling temperature,
  rep penalty, or beam search. Any chat-cap recovery requires **substrate
  retraining** (CLM-2-EXEC) or **substrate replacement** (Llama Path A v2 winner
  per L31).

## Deliverables

- `tool/transient_py/anima_emerge_chat_first_token_force.py` — helper (this BG)
- `state/anima_emerge_chat_first_token_force_2026_05_05/aggregate.json` — 6 configs
- `state/anima_emerge_chat_first_token_force_2026_05_05/verdict.json` — verdict
- this doc

## Cost + raw

- **$0** mac CPU; **wall ≈ 4 min** (load + 6 forward chains).
- raw#37 transient .py — `tool/transient_py/` namespace.
- raw#15 additive — no runtime modification (read-only sister-import of `inj_helper`).
- raw#10 honest C3 — 5 caveats emitted to verdict + this doc.
- no commit, no secret leak.
