<!-- @no-lineage-citation-exempt-file -->
# anima emerge chat — lm_head row-norm survey LANDED 2026-05-05

**Lane**: emerge / chat-capability / substrate-research
**BG**: BG-DC (mac CPU $0, ~5min wall)
**Spec source**: BG-CF verdict 권고 1순위 (lnf_scale_ablate honest_c3 follow-up)
**Sister context**: BG-CA korean_rank_survey (best_korean_rank=197, KOREAN_TRAIN_ABSENT)

## Why

BG-CF (lnf_scale_ablate) → FAIL_LNF_NOT_THE_BUG. ln_f gain-ablation across
{0.1, 0.5, 1.5, 2.0, 5.0, 10.0, unit, random} produced zero diff vs baseline.
Root cause is *not* the final RMSNorm gain. Verdict honest_c3 권고 1순위 =
lm_head.weight row-norm distribution survey. Hypothesis: Korean token rows
have systematically smaller L2 norms than basin (byte-fallback +
replacement-char) rows, so Korean logits never enter top-k cone — explaining
BG-CA Korean rank 197 finding.

This lane is **substrate-research only**. Chat-capability path lives in
Llama Path A v2. Architectural-issue diagnosis lane.

## Method

`tool/transient_py/anima_emerge_chat_lm_head_row_norm.py` (transient sister
helper, opt-out class three):

1. Load `need-singularity/clm-v4-mk2-v1` fp32 CPU via
   `inj_helper._try_load_model`.
2. Walk SentencePiece vocab (64000), classify each token id by clean piece
   text:
   - **korean**: contains any 가-힣 (Hangul Syllables block)
   - **basin**: starts with byte-fallback prefix and ends with `>` OR
     contains U+FFFD
   - **ascii**: all-ASCII alphabetic
   - **cjk**: Han 一-鿿 OR Kana ぀-ヿ
3. `W = model.decoder.head_a.weight.data` shape (64000, 768).
4. Per-category row L2 norm via `W[ids].norm(dim=-1)`.
5. Cross-check: forward "안녕" once, slice logits per category for sanity.

## Result

### (a) Category counts

| category | count | % vocab |
|----------|-------|---------|
| korean   | 5701  | 8.91 %  |
| basin    | 256   | 0.40 %  |
| ascii    | 11004 | 17.19 % |
| cjk      | 29851 | 46.64 % |

256 basin = exact byte-fallback set (one entry per byte 0x00-0xFF). CJK
dominates ~47%.

### (b) Row-norm distribution

| category | mean   | std    | min    | max    |
|----------|--------|--------|--------|--------|
| korean   | 0.6419 | 0.0188 | 0.5748 | 0.7041 |
| basin    | 0.6832 | 0.0398 | 0.5534 | 0.7618 |
| ascii    | 0.6418 | 0.0190 | n/a    | n/a    |
| cjk      | 0.6418 | 0.0188 | n/a    | n/a    |

Korean / ascii / cjk row norms statistically indistinguishable
(mean ~0.642, std ~0.019). Basin rows mean=0.683 — slightly higher
(1.064x ratio), but basin min 0.5534 < korean max 0.7041 < basin max 0.7618.
No bias term (`head_a.bias is None`).

### (c) Logit at "안녕" prompt

| category | mean    | max    |
|----------|---------|--------|
| korean   | -5.858  | -3.051 |
| basin    | +0.586  | +8.300 |

**logit_gap = 6.444** (basin_mean - korean_mean). basin_max = 8.300 vs
korean_max = -3.051 — basin tokens dominate by ~11.3 logit units even
though row-norm ratio is only 1.064.

### (d) Verdict

`basin_to_korean_ratio = 1.0642` → **NORMS_COMPARABLE** (threshold 1.2 / 0.8).
Row norm hypothesis **FALSIFIED** as primary cause.

The 6.4-logit basin-dominance gap is not explained by row-norm magnitude.
The cause must lie in **direction** of basin row vectors aligning with the
post-ln_f hidden state — i.e. cosine alignment in 768-D, not vector
magnitude. Row-norm survey eliminates magnitude-bias hypothesis; remaining
suspects:

1. **Direction-axis hypothesis** — basin rows cluster along the dominant
   principal-component direction of typical hidden states (substrate's
   "default attractor").
2. **Hidden-state hypothesis** — pre-ln_f hidden vectors at the prompt-final
   position project predominantly onto basin row directions regardless of
   input language.
3. **Embed-side hypothesis** — input `tok_emb` for Korean produces hidden
   trajectory that lands in basin-aligned region (not Korean-aligned region).

### (e) Honest C3 + architectural-root-cause refinement

- **C1** mac CPU fp32 — numerical precision floor low; row-norm differences
  <1% within fp32 noise.
- **C2** row norm != logit dominance — `logit = h dot W_row + b`. With h
  fixed, logit is rank-1 in W_row, but cosine-similarity (direction)
  governs the inner product up to ‖W_row‖. Row-norm equality plus 6.4-logit
  gap = direction asymmetry.
- **C3** single prompt 안녕 — broader Korean / multilingual prompt sweep
  needed to confirm direction-asymmetry generality.
- **C4** 'basin' = byte-fallback + replacement-char heuristic. The 256 byte
  tokens are **architectural** (BPE byte-fallback), not learned. Their
  dominance suggests training-time signal collapse to fallback distribution.
- **C5** mean comparison ignores distribution shape — basin std=0.0398
  (2x korean std=0.0188); some basin rows may have outlier-large norms
  driving mean.

**Architectural-root-cause refinement**: Korean-incapability is **not a
magnitude problem** in lm_head — it is a **direction problem**. The
next-most-informative probe is cosine-similarity of `h_final` (post-ln_f)
against (basin row mean, korean row mean, ascii row mean) on Korean
prompts. If `cos(h_final, basin_mean) >> cos(h_final, korean_mean)` we have
direction-collapse; remediation = re-orient hidden trajectory (LoRA on
attention or pre-ln_f) rather than scale heads.

## Recommendations

1. **Next BG (suggested BG-DD)**: cosine-alignment survey
   `cos(h_final, W_row)` per category at multiple Korean prompts (>=10),
   aggregate per-position over generation, $0 mac CPU.
2. **L34 candidate**: "Korean-incapability is direction-collapse, not
   magnitude-collapse" — promote to memory after BG-DD confirms.
3. **Architectural path**: substrate's pre-ln_f hidden trajectory does not
   visit Korean-aligned region of head space regardless of input. Path =
   **input-conditioning intervention** (KV-injection / prefix tuning), not
   output-rescaling intervention.

## Artifacts

- `tool/transient_py/anima_emerge_chat_lm_head_row_norm.py` — sister-rule helper
- `state/anima_emerge_chat_lm_head_row_norm_2026_05_05/aggregate.json` — full stats
- `state/anima_emerge_chat_lm_head_row_norm_2026_05_05/verdict.json` — schema verdict

## Compliance

- transient sister-rule (importlib + torch attribute walk; hexa cannot
  inspect tensors)
- additive only — no anima runtime touched
- honest C3 — five caveats emitted to verdict + landing doc
- transient sister-rule, one-shot probe (opt-out class three)
- $0 mac CPU, ~5min wall (load 4.9s + survey instant)
- HF token leak free (model_id only, no auth header in code)
- Commit deferred per session policy
