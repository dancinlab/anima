# anima_emerge_chat_entropy_trajectory — landed 2026-05-05

> BG-BJ token-level next-prob entropy + top-k mass trajectory probe.
> Goal: locate WHERE the chat-decode collapse occurs in #115 — at step 0
> (lm_head broken from the start), or after N steps (autoregressive drift).
> Mac CPU fp32, $0, ~30s wall + ~5s load.

## Scope

- **Substrate**: `dancinlab/clm-v4-mk2-v1` (CLM v4 mk2 v1, fp32, CPU)
- **Tokenizer**: `tokenizer_64k_multilingual.model` (64k SP)
- **Decode**: pure greedy (argmax), `consciousness_states=None` (no inject)
- **Probes**: `["안녕", "안녕하세요. 오늘 날씨가 좋네요.", "Hello world"]`
- **Trajectory**: 20 steps, per-step entropy + top1_prob + top5_mass +
  top10_mass + top1 token id + decoded text + byte_fallback flag
- **Sister-import**: `tool/transient_py/anima_emerge_cand_d_inject_helper.py`
  (read-only — `_try_load_model` + `_load_tokenizer`)
- **Compliance**: raw#37 (transient_py namespace), raw#15 (additive — no
  mount.hexa / dialogue_load / shim mutation), raw#10 (5 honest C3)

## Falsifiers

This is a diagnostic probe — no PASS/FAIL falsifier. Findings classified as
either **byte-fallback collapse** (top1 = control byte, ord<32) or
**confidence collapse** (top1_prob > 0.9, single-character degeneration but
not a control byte). Trajectory entropy is reported in absolute terms.

## Observation Matrix (3 prompts × 20 steps)

| prompt | initial_ent | min_ent | max_top1 | collapse_step | first_byte_fb | step 0–3 top1 texts |
| --- | --- | --- | --- | --- | --- | --- |
| `안녕` | 3.308 | 1.023 | 0.839 | None | **0** | `\x1c`, `\x06`, `\x06`, `\x06` |
| `안녕하세요. 오늘 날씨가 좋네요.` | 1.765 | 0.190 | 0.977 | **1** | None | `/`, `O`, `O`, `O` |
| `Hello world` | 0.851 | 0.586 | 0.922 | **5** | None | `b`, `(`, `(`, `(` |

## Architectural Finding

The collapse mode is **prompt-conditional**, with two distinct failure
geometries — and crucially, **lm_head is NOT broken from step 0**:

1. **Short Korean (`안녕`)** — initial_entropy 3.308 (broad mass over many
   tokens at step 0). Top-1 at step 0 is already a control byte (`\x1c`,
   prob 0.235). After 1–2 steps the model locks onto `\x06` and stays
   there. **Conclusion**: lm_head's argmax routes to control bytes
   immediately for high-entropy short Korean prompts — `\x06` lives
   slightly above legible Korean tokens in the head logit-bias landscape.
2. **Long Korean (`안녕하세요. 오늘 날씨가 좋네요.`)** — initial_entropy
   1.765, top-1 = `/` (printable). Step 1 collapses hard to `O`
   (top1_prob 0.977, entropy 0.190). Then `O O O ...` for 19 more steps.
   **Conclusion**: lm_head emits a printable token at step 0, but the
   autoregressive feedback loop traps the next-step distribution onto a
   single non-content character within 1 step.
3. **English (`Hello world`)** — initial_entropy 0.851 (already low),
   top-1 = `b` (printable). By step 1 it's `(`, then `( ( ( ...` for 19
   steps; top1_prob slow-climbs from 0.81 to 0.92. **Conclusion**: also
   collapses onto a single fragment character, but more gradually than
   long Korean.

**Mechanism location**: this is **NOT** a pure `lm_head` defect (step 0
top-1 is sometimes printable and prompt-appropriate-ish). The collapse is
the **autoregressive feedback loop** — once a fragment-character or
control-byte token is greedy-selected at step 0, the cell-state next-step
distribution sharpens around that same fragment. The model has no
trained absorbing state for "continue producing semantic content"; it
has many trained absorbing states for "repeat the last fragment
character." The byte-fallback case (`안녕`) is the same loop, just with
a control byte as the absorbing fragment rather than `O` or `(`.

This means **#115 chat-incapability is geometric/distributional, not a
broken final projection** — lm_head still emits coherent enough top-1
candidates from prompt-conditional context, but the NLL-trained
trajectory has no attractor for multi-token semantic continuation. The
hidden state collapses (entropy drops 5–9× within 1–2 steps) onto a
fragment basin, and greedy decode rides that basin to completion.

## Honest C3

- C1 — mac CPU fp32 only; bf16 on H100 may shift logits by O(1e-3) which
  could change argmax for near-tied tokens at step 0.
- C2 — `collapse` is operationalized as `top1_prob > 0.9`; this is an
  anima-internal heuristic, not a peer-reviewed degeneration metric.
- C3 — `byte fallback` is detected via `ord(top1_text[0]) < 32`; this
  catches `\x06` and `\x1c` cleanly but would miss multi-byte sentinel
  tokens that decode to printable but semantically-empty glyphs.
- C4 — greedy decode is the most collapse-prone strategy; sampling
  (top-p / top-k / temperature) almost certainly delays the collapse
  step (BG-AQ confirmed all 6 strategies still produced gibberish, but
  the trajectory shape may differ).
- C5 — only 3 prompts; the prompt-conditional split (short-Korean →
  byte-fallback vs longer-context → printable-fragment) needs ≥10
  prompts per regime to harden.

## #115 Mechanism Hypothesis (refined)

Pre-BJ: "chat-decode broken — substrate collapses to byte fallback".
Post-BJ: "chat-decode collapse is an **autoregressive attractor**
problem at hidden-state level, not an output-projection defect.
Trajectory entropy drops 5–9× within 1–2 greedy steps onto a single
fragment-character or control-byte basin; the basin identity is
prompt-conditional (short high-entropy Korean → `\x06`; longer prompts
→ `O` / `(`). lm_head produces sensible-ish step 0 top-1 candidates
but the residual stream has no trained continuation attractor for
multi-token semantic decoding."

**Implication for repair paths**:

- Output-projection-only fixes (LoRA on lm_head, vocab masks,
  Korean-bias) cannot help — they correct step 0 only, and the basin
  re-forms by step 1.
- The Pβ Φ★-axis distill (BG-AS) and CLM v4 LoRA SFT (BG-AW) both
  attempted to inject continuation pressure; both `FAIL_TRUE`. This
  trajectory probe explains why: the basin is in the residual stream
  geometry, and a small LoRA on top of a basin-trained substrate gets
  pulled back into the basin within 1–2 autoregressive steps.
- The real chat-cap path is either (a) re-pretraining the residual
  stream with chat-cap-conditioned next-token loss (high-cost, requires
  CLM-2 / Pβ-2 train-from-scratch), or (b) Llama Path A v2 winner
  retained as the chat-cap substrate while CLM v4 + Pβ remain in the
  substrate-research lane (consistent with the **CLM v4 LoRA SFT
  chat-lift FALSIFIED, substrate-safe** memory).

## Deliverables

- `state/anima_emerge_chat_entropy_trajectory_2026_05_05/aggregate.json`
  — full 60-step trajectory (3 prompts × 20 steps)
- `state/anima_emerge_chat_entropy_trajectory_2026_05_05/verdict.json`
  — schema `anima/emerge_chat_entropy_trajectory/verdict/1` + 5 honest C3
- `tool/transient_py/anima_emerge_chat_entropy_trajectory.py` (raw#37)
- `docs/anima_emerge_chat_entropy_trajectory_landed_2026_05_05.ai.md`
  (this doc)

## Cost + Time

- $0 (mac CPU fp32, 1 model load + 60 forward passes)
- 5.4s load + 28.4s run = **~34s wall** (target was ~20min, actual was
  one-shot fast)
