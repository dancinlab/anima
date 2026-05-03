# clm_eeg 5-metric harness real-swap — pending state (2026-05-03)

**Scope:** `.roadmap.anima_clm_eeg cond.1` blocker resolution path

## Status

Scaffold landed. Fixture swap **pending** — awaiting sibling-BG P1
output at:

```
state/berger_v6_clean_reanalyze_2026_05_03/welch_clean.npz
state/berger_v6_clean_reanalyze_2026_05_03/welch_clean_summary.json
```

Once that JSON sidecar lands, this scaffold consumes it.

## Tier (raw#10 honest C3)

- **tier:** `functional_analog`
- **NOT** full PASS
- **N=1** single-subject, single-session, single-montage (Cyton+Daisy 16ch)
- No population statistics, no test–retest, no cross-vendor validation yet

## Components

| File | Role |
|------|------|
| `anima-clm-eeg/tool/clm_eeg_harness_realswap.hexa` | Adapter — synthetic passthrough OR real-swap from sibling-BG P1 NPZ summary |
| `anima-clm-eeg/state/realswap_pending_2026_05_03/README.md` | This file — activation runbook |

## Channel quarantine (raw#10 honest)

v6 paired-symmetric Berger PHENOMENAL: **5 of 16 channels rail-saturated**.

| 1-idx | 0-idx | Name | Status |
|------:|------:|------|--------|
| 1 | 0 | Fp1 | rail-quarantined |
| 5 | 4 | P7 | rail-quarantined |
| 6 | 5 | P8 | rail-quarantined |
| 8 | 7 | O2 | rail-quarantined |
| 16 | 15 | P4 | rail-quarantined |

Clean channels (1-indexed in source): `[2, 3, 4, 7, 9, 10, 11, 12, 13, 14, 15]`
→ **11 channels usable**

**Quarantine policy:** zero-fill (NOT interpolation).
Rationale — preserves loss visibility for downstream auditors instead
of fabricating signal where none was recorded.

## Activation path

Once sibling-BG P1 lands `welch_clean_summary.json`:

1. Run the adapter in real mode:

   ```bash
   HEXA_RESOLVER_NO_REROUTE=1 hexa run anima-clm-eeg/tool/clm_eeg_harness_realswap.hexa \
       --fixture-mode real \
       --real-summary-json state/berger_v6_clean_reanalyze_2026_05_03/welch_clean_summary.json \
       --clean-channels "2,3,4,7,9,10,11,12,13,14,15" \
       --output anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json
   ```

2. Re-run the 5-metric pre-register chain pointing `CLM_EEG_FIXTURE_PATH`
   at the new fixture:

   ```bash
   CLM_EEG_FIXTURE_PATH=anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json \
       hexa run anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa
   # ... and p2 / p3 likewise
   ```

3. Re-run the harness aggregator:

   ```bash
   HEXA_RESOLVER_NO_REROUTE=1 hexa run anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa --selftest
   ```

## Honest constraints (raw#71 falsifier-bound)

- **No metric threshold relaxation.** Frozen pre-register thresholds in
  `clm_eeg_p1_lz_pre_register.hexa` / `clm_eeg_p2_tlr_pre_register.hexa` /
  `clm_eeg_p3_gcg_pre_register.hexa` REMAIN unchanged. Any post-hoc
  retuning to force PASS = SSOT v2 bump (no silent edit).
- **No re-execution by this scaffold.** It only adapts the fixture path;
  metric computation lives in the existing `clm_eeg_*_real.hexa` tools.
- **No interpolation across rail-quarantined channels.** Zero-fill only.

## Open questions for next cycle

1. Should the band-power transcoder be a separate `.hexa` tool or stay
   inlined inside `clm_eeg_harness_realswap.hexa`? (Lean toward separate
   to keep adapter pure-bridge.)
2. The sibling-BG P1 NPZ summary schema is not yet frozen — once it lands,
   confirm field names (`per_channel_band_powers_x1000`?) before
   activating real-mode transcoding.
3. Existing `clm_eeg_harness_smoke.hexa` aggregates p1/p2/p3 pre-register
   verdicts — its output JSON does not yet carry a `fixture_mode` tag.
   The file is currently `chflags uchg` (immutable, dual-lock protected
   — see `anima-clm-eeg/tool/silent_edit_dual_lock.sh.txt`), so this
   cycle did **not** modify it. Next cycle: unlock + add
   `CLM_EEG_HARNESS_FIXTURE_MODE` env propagation into the cert (annotation
   only — aggregation logic unchanged) so post-real-swap auditors can
   distinguish synthetic vs functional-analog runs in the marker chain.
