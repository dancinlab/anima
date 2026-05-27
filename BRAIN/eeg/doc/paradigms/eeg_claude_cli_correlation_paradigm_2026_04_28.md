# anima-eeg ↔ Claude CLI Correlation Paradigm — Design (T1)

**Date**: 2026-04-28
**Author**: anima-eeg / design / T1
**Status**: NEW_PARADIGM_DISCOVERY (design + skeleton; no real paired sessions yet)
**Trigger**: User wants EEG state correlated with their Claude CLI conversation flow during normal coding/dialog use.
**Constraint**: **NO API** — direct Anthropic API calls forbidden (user cost). Only the Claude CLI's on-disk conversation `.jsonl` is consumed.
**Companions**:
  - `design/eeg_daily_life_paradigm_design_2026_04_28.md` (6-axis daily-life metrics — *eyes-open, task-engaged*; this paradigm IS daily-life)
  - `design/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md` (resting-axis Top-5)

---

## 0. Executive Summary

### Problem
The user already runs Claude CLI sessions for hours daily (coding/dialog). These sessions emit fully-detailed conversation `.jsonl` files at `~/.claude-claude7/projects/<encoded-cwd>/<session-uuid>.jsonl` with **per-message ISO-8601 timestamps**. If anima-eeg streams continuously during the same wall-clock window, every user prompt and every Claude response can be **time-aligned to an EEG segment** post-hoc — yielding *naturalistic* paired (cli_message, eeg_segment, metrics) data without forcing an artificial protocol.

### Solution: Two-Stream Wall-Clock Time-Align Verifier (Genus: `eeg-claude-cli-correlator`)

1. **Stream A** — anima-eeg long-duration (≥30 min) BrainFlow capture → CSV with `unix_ms` timestamps per sample (or windowed band-power/LZ76 emissions with window-start `unix_ms`).
2. **Stream B** — Claude CLI conversation `.jsonl` polled (or simply read post-session) for entries with `timestamp` + `type ∈ {user, assistant}` and `message.role ∈ {user, assistant}`.
3. **Time-align** — every CLI message gets two EEG windows:
   - **pre-window** (5s before user message timestamp): typing/thinking phase.
   - **peri-window** (10s after assistant reply timestamp): response-reading phase.
   - 6-axis daily-life metrics (re-use of `design/eeg_daily_life_paradigm_design_2026_04_28.md`):
     spectral-entropy-broadband · alpha-attenuation-index · sliding-LZ76-change-points ·
     sliding-LZ76-range · beta-alpha-ratio-engagement · drowsiness-index.
5. **Correlate**:
   - User-side: `len(user_msg)` × pre-window LZ76, alpha-attenuation, β/α engagement.
   - Claude-side: `len(assistant_msg)` + `code_block_count` + `latency_ms` × peri-window α-desync, P300-band proxy (250-500ms post-onset gamma transient), spectral-entropy.
6. **Emit** `state/eeg_claude_cli_audit/<date>_session.jsonl` — one row per (user_msg, assistant_msg) pair, including: `cli_msg_uuid`, `cli_ts_iso`, `cli_role`, `text_len`, `code_block_count`, `latency_ms`, `eeg_pre_window_metrics{6}`, `eeg_peri_window_metrics{6}`, `pair_verdict`.

### Privacy
- Only `text_len`, `code_block_count`, `latency_ms`, and metric scalars are emitted by default.
- Raw text is hashed (FNV-32) — original text never leaves the local audit log unless `EEG_CLI_INCLUDE_TEXT=1` (opt-in).

---

## 1. Time-Align Accuracy Estimate

| layer | accuracy | source |
|---|---|---|
| BrainFlow `unix_ms` per sample | ±1 ms | board-clock + host NTP (Cyton+Daisy 125 Hz native, sample interval 8 ms; jitter < 4 ms post-USB) |
| Claude CLI `.jsonl` `timestamp` (ISO-8601 ms) | ±50-200 ms | wall-clock at message-emit, dependent on host clock skew |
| Window edges (5s pre / 10s peri) | ±200 ms worst-case | dominated by CLI ts uncertainty |


---

## 2. Data Flow

```
Claude CLI (always running)            anima-eeg (BrainFlow streamer)
        │                                       │
        ▼                                       ▼
~/.claude-claude7/projects/             /tmp/anima_eeg_stream_<ts>.csv
   <encoded-cwd>/<uuid>.jsonl              (or band_power / LZ76 windowed JSON)
        │                                       │
        └──────────────┬────────────────────────┘
                       ▼
    - parses CLI .jsonl → list[(uuid, role, ts_unix_ms, text_len, code_blocks)]
    - parses EEG CSV/JSON → time-indexed metric series
    - for each user/assistant msg, slices pre/peri window, computes 6 metrics
    - emits paired_session.jsonl
                       │
                       ▼
  anima-clm-eeg/tool/eeg_claude_cli_correlator.hexa
    - per-message verdict: ≥4 of 6 daily-life axes pass → PAIR_OK
```


---


```jsonl
{"genus":"eeg-claude-cli-correlator","raw_rank":9,"deterministic":true,
 "session_id":"<uuid>","cli_jsonl":"<path>","eeg_csv":"<path>",
 "n_pairs":N,"pair_ok_count":K,"pair_ok_rate":K/N,
 "session_verdict":"SESSION_OK|SESSION_FAIL",
 "pairs":[{"pair_idx":i,"user_uuid":"...","assistant_uuid":"...",
           "user_ts_iso":"...","assistant_ts_iso":"...",
           "latency_ms":..., "user_text_len":..., "assistant_text_len":...,
           "code_block_count":...,
           "eeg_pre":{"sp_entropy":..,"alpha_atten":..,"lz76_cp":..,"lz76_range":..,"beta_alpha":..,"drowsy":..},
           "eeg_peri":{"sp_entropy":..,"alpha_atten":..,"lz76_cp":..,"lz76_range":..,"beta_alpha":..,"drowsy":..},
           "pair_axes_pass":k_of_6, "pair_verdict":"PAIR_OK|PAIR_FAIL"}, ...]}
```

`PAIR_OK` = ≥4 of 6 axes pass on the **peri-window** (response-reading is the cleanest-aligned phase).

---


1. **Time-align inversion** — randomly shuffle CLI timestamps; pair_ok_rate must collapse from baseline ≥ 0.60 to ≤ chance (~0.30). If shuffled rate ≥ baseline ⇒ paradigm refuted (no real coupling).
2. **Empty-EEG falsifier** — feed all-zero EEG; every axis must FAIL ⇒ pair_ok_rate = 0 (catches false-positive on flat input).
3. **Cross-session swap** — pair user A's CLI log against user B's EEG (different session) ⇒ pair_ok_rate must collapse below 0.45.
4. **Pre-window ≡ peri-window null** — if metrics are identical between pre and peri window for every pair, the helper is degenerate (no temporal differentiation) ⇒ FAIL_DEGENERATE.
6. **Drowsiness escape valve** — late-night session with `drowsy > 3.0` on > 50 % pairs but `pair_ok_rate ≥ 0.60` is internally contradictory ⇒ FAIL (high-vigilance criteria can't co-exist with high drowsiness).
7. **Latency-only confound** — if `latency_ms` alone (no EEG) predicts `pair_verdict` at AUC ≥ 0.90, the EEG is contributing nothing ⇒ FAIL_NO_EEG_VALUE.

(7 falsifiers; ≥ 5 required.)

---


| paradigm | expected pair_ok_rate | mechanism |
|---|---|---|
| User actively coding (this paradigm) | ≥ 0.60 | engaged daily-life signature |
| User asleep with CLI replaying old log | ≤ 0.20 | drowsy > 3.0, β/α < 0.3, no engagement |
| Synthetic flat EEG ↔ real CLI | = 0.00 | empty-EEG falsifier #2 |
| Real EEG ↔ synthetic random CLI ts | ≤ 0.30 | shuffled-ts falsifier #1 |
| Anesthesia-cohort EEG ↔ real CLI | ≤ 0.10 | LZ76 < 0.3 collapses sliding-cp/range |

---

## 6. Implementation Skeleton

  - reads paired_session.jsonl (line-by-line FNV-checked)
  - per-line: extract `pair_axes_pass`, count `PAIR_OK`
  - emits aggregate `state/eeg_claude_cli_audit/<date>_session.jsonl` (last line = session summary)
  - synthetic selftest: 10 paired rows hardcoded with deterministic axes_pass; expected pair_ok_rate ≥ 0.6.
  - argparse: `--cli-jsonl <path> --eeg-csv <path> --out <path>`
  - parse CLI jsonl → user/assistant rows with `timestamp` ISO-8601 → unix_ms.
  - parse EEG CSV → time-indexed band-power / LZ76 series.
  - for each (user_msg, next_assistant_msg) pair, slice pre/peri windows → 6 metrics → pair verdict.
  - emit JSONL.
- **No new state schema**: re-uses `state/eeg_claude_cli_audit/<date>_session.jsonl` (date-bucketed).

---

## 7. Roadmap

- **T1 (this design + skeleton)** — paradigm + verifier scaffolded; selftest synthetic.
- **T2** — first real paired session: 30-min anima-eeg stream + concurrent Claude CLI dialog → emit live audit row, hand-inspect.

---


- **Time-align ±200-300 ms**: adequate for slow metrics (4-10 s windows) but **insufficient for ERP-grade analysis**. Schema labels `eeg_peri.p300_band_proxy` as NON_AUTHORITATIVE.
- **No real paired session yet**: T1 is design + skeleton only. All metrics in selftest are SYNTHETIC.
- **Privacy**: text-content emission is opt-in; default emits only scalars + FNV hash of text.
- **NO API**: zero outbound HTTP; the verifier reads only on-disk `.jsonl` (already on user's disk by virtue of having run Claude CLI).
- **Raw#46 honest**: 6 axes, supermajority verdict, no single dominant axis allowed (falsifier #5 catches reverse-engineering).
