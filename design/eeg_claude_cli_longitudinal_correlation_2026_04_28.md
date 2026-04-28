# anima-eeg ↔ Claude CLI Longitudinal Correlation Paradigm — Design (B9)

**Date**: 2026-04-28
**Author**: anima-clm-eeg / design / B9
**Status**: NEW_PARADIGM_DISCOVERY (design + skeleton + selftest synthetic; **NO real 1-2 week measurement yet**)
**Trigger**: B9 long-term version of T1 paired (cli, eeg) correlation. T1 = single session; B9 = 1-2 week aggregate (N>=100 paired messages) → longitudinal correlation matrix.
**Constraint**: **NO API** — direct Anthropic API calls forbidden. Only the Claude CLI's on-disk conversation `.jsonl` is consumed.
**Companions**:
  - `design/eeg_claude_cli_correlation_paradigm_2026_04_28.md` (T1 — single session)
  - `design/eeg_daily_life_paradigm_design_2026_04_28.md` (6-axis daily-life metrics)
**Compliance**: raw#9 hexa-only · raw#10 honest C3 · raw#12 frozen criteria · raw#37 transient `/tmp` helper · raw#65 idempotent FNV · raw#71 ≥5 falsifiers · raw#82 darwin-native · raw#91 high-variance honest · own 5 completeness-first.

---

## 0. Differentiation from T1

| dimension | T1 (paradigm) | B9 (this design) |
|---|---|---|
| timescale | single session (≥30 min) | 1-2 weeks accumulated |
| N | per-pair verdict, 5-50 pairs | aggregate N≥100 paired messages |
| analysis | per-pair PASS/FAIL via 6-axis daily-life verdict | **correlation matrix** 6 features × 5 metrics, Bonferroni-corrected p<0.05 |
| output | session summary line (PAIR_OK rate) | longitudinal correlation matrix + significance + ASCII heatmap |
| dependency | post-hoc, single .jsonl + single EEG csv | polling daemon (cron) over 1-2 weeks |
| privacy | text len + FNV hash | **same** (msg body NEVER persisted) |

T1 verifies *that* a paired session produces 6-axis verdicts. B9 verifies *whether* per-message features systematically correlate with EEG metrics across many days — i.e., is there a stable individual signature.

---

## 1. Per-Message Features (6) × EEG Metrics (5)

**Per-message features (raw#46 multi-feature; columns of correlation matrix):**
1. `user_msg_len`     — char length of user message
2. `user_code_blocks` — count of triple-backtick blocks in user message
3. `user_topic_specificity` — vague (≤30 chars, no code) = 0; specific (≥50 chars OR code) = 1; binarized
4. `assistant_msg_len`  — char length of assistant response
5. `assistant_latency_ms` — ts(assistant) − ts(user) in ms
6. `assistant_tool_uses` — count of tool_use blocks (parsed from `.jsonl`)

**EEG metrics (5; rows of correlation matrix):**
1. `lz76_b_x1000` — frozen Kaspar-Schuster 1987 LZ76 normalized (raw#12)
2. `engagement_x1000` — β/α ratio, daily-life axis
3. `drowsy_x1000` — α+θ over β proxy
4. `alpha_atten_x1000` — α attenuation index (eyes-open marker)
5. `sp_entropy_x1000` — broadband spectral entropy

EEG segment per message: 5s pre-message + 10s post-message (T1 schema reused).

---

## 2. Correlation + Significance

For each (feature, metric) cell:
- **Spearman rank correlation r_s** (robust, no normality assumption).
- **Two-tailed p-value** via tabulated t-distribution lookup (n≥100, df=n−2).
- **Bonferroni correction** for 30 hypotheses (6×5 cells) → α' = 0.05/30 ≈ 0.00167.

A cell is "significant" iff |r_s| ≥ 0.2 AND p_corrected < 0.05 (i.e., raw p < 0.00167).

---

## 3. Frozen Criteria (raw#12, frozen 2026-04-28)

| ID | criterion | threshold |
|---|---|---|
| C1 | N paired messages | N ≥ 100 |
| C2 | EEG segment availability | ≥ 80% of messages have non-empty 15 s window |
| C3 | minimum effect size | \|r_s\| ≥ 0.20 |
| C4 | Bonferroni-corrected significance | p_raw < 0.05/30 = 0.00167 |
| C5 | at-least-one significant cell | sum(significant) ≥ 1 |
| C6 | privacy invariant | message body NEVER persisted; only FNV-32 hash |

`B9.PASS = C1 ∧ C2 ∧ C5 ∧ C6` (C3, C4 are per-cell qualifiers, not session-level gates).

---

## 4. Falsifiers (raw#71, ≥5 required)

1. **F1: N<100 paired** — sample-size insufficient → ABSTAIN, not PASS. (Avoids underpowered claims.)
2. **F2: EEG-CLI ts mismatch** — if >10% of messages have EEG ts mismatch >5 s, reject. (Hardware drift / clock skew confound.)
3. **F3: Zero significant after Bonferroni** — no cell survives correction → "no longitudinal correlation found" (NEGATIVE finding, still publishable per raw#52 negative oracle).
4. **F4: r ≥ 0.5 over-interpretation** — any cell with \|r_s\| ≥ 0.5 raises overinterpretation flag (suspicious for confound — e.g. day-of-week, time-of-day, or single-session dominance). Manual inspection required before claiming.
5. **F5: privacy violation** — emitted JSONL contains literal CLI message text (regex search for any 80+ char text run that is not a hash, hex, or numeric). Auto-FAIL.
6. **F6: single-session dominance** — if removing the single most-massive day collapses any "significant" cell to non-significant, that cell is rejected (not robust).
7. **F7: time-shuffle null** — randomly shuffle EEG-segment-to-message assignment; the shuffled correlation matrix MUST have ≥10× fewer significant cells than the real assignment. If parity, the original is noise.

(7 falsifiers; ≥5 required.)

---

## 5. Privacy Architecture (raw#9 / own 5 completeness)

- The `.jsonl` polling daemon ONLY reads `timestamp`, `type`, `message.role`, `len(message.content)`, count of triple-backticks, count of tool_use blocks.
- Message text → FNV-32 hash (single 8-hex-digit string), persisted as `msg_hash` field.
- Original text never written to any anima file. Original `.jsonl` files in `~/.claude-claude7/projects/` are owned by Claude CLI, untouched.
- raw#9 hexa-only: `/tmp/claude_cli_eeg_corr_helper.py` is transient (re-emitted each run, deleted after).

---

## 6. Implementation

### `anima-clm-eeg/tool/eeg_claude_cli_longitudinal_correlator.hexa` (~180 LoC)
Pure aggregator — reads paired-message JSONL (one row per message with feature columns + EEG-window metric columns), computes 6×5 Spearman correlation matrix via integer-only rank algorithm, evaluates Bonferroni significance, emits ASCII heatmap.

Selftest mode: synthesizes 100 paired messages with deterministic FNV seed; injects 2 known correlations (user_msg_len ↔ lz76 with r≈+0.4, assistant_latency ↔ drowsy with r≈+0.3). Selftest passes if both injected correlations are recovered as significant after Bonferroni.

### `/tmp/claude_cli_eeg_corr_helper.py` (raw#37 transient)
- argparse: `--cli-glob '~/.claude-claude7/projects/*/*.jsonl'  --eeg-csv-glob '<dir>/*.csv'  --out <jsonl>  --window-pre 5  --window-peri 10`
- For each .jsonl line of type=user/assistant, parse ts → unix_ms.
- For each EEG csv, build time-indexed (unix_ms → metric_dict) lookup.
- For each user message, find nearest assistant response (next message with role=assistant); emit row with features + pre-window metrics + peri-window metrics.
- Output: `state/eeg_claude_cli_longitudinal/<date>_paired.jsonl`.

### State paths
- `state/eeg_claude_cli_longitudinal/<date>_paired.jsonl` — per-message paired rows (helper output).
- `state/eeg_claude_cli_longitudinal/<date>_corr.jsonl` — verifier output (correlation matrix + verdict).

---

## 7. User Action Plan (1-2 week measurement protocol)

1. **Day 0 (today)**: Land design + skeleton + selftest. Confirm hexa selftest PASS.
2. **Days 1-14**: User wears anima-eeg helmet during normal Claude CLI sessions whenever comfortable. No protocol — just naturalistic use. Each session: start anima-eeg recorder before opening Claude CLI, stop when ending.
3. **Daily housekeeping**: nightly cron `eeg_claude_cli_longitudinal_correlator.hexa --build-paired` aggregates that day's `.jsonl` + EEG into the paired JSONL.
4. **Day 14**: run `--analyze` to compute the 6×5 correlation matrix over all paired rows. Expected outcome (honest C3, raw#10): UNKNOWN — this is exploratory; PASS, FAIL, or ABSTAIN are all acceptable.
5. **Reporting**: emit `state/eeg_claude_cli_longitudinal/2026-05-12_corr.jsonl` with the matrix and ASCII heatmap. Manual review for F4 over-interpretation.

---

## 8. Honest C3 (raw#10, raw#91)

- **No real 1-2 week data yet** — this design lands the scaffold + selftest synthetic. Real correlation values are UNKNOWN.
- **Time-align ±200-300 ms** (T1 carry-over) — adequate for slow metrics over 5-10 s windows; **insufficient for ERP-grade <100 ms tasks**.
- **N≥100 may take >2 weeks** of normal use; the threshold is pre-registered. If the user falls short (e.g., light usage), the verdict is ABSTAIN, not FAIL.
- **Bonferroni is conservative**; FDR (Benjamini-Hochberg) could be added in a v2 but is NOT in B9 frozen criteria.
- **Privacy is structural, not aspirational**: the helper opens .jsonl read-only and only extracts scalar features + 8-digit hash; even with full code review, it is impossible to reconstruct message text from the audit trail.
