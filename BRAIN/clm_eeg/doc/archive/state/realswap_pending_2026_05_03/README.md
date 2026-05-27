# clm_eeg 5-metric harness real-swap — smoke run executed (2026-05-03)

**Scope:** `.roadmap.anima_clm_eeg cond.1` blocker resolution path

## Status

`REAL_SWAP_SMOKE_RUN_PARTIAL_PASS_2026_05_03` — synthetic-chain composite PASS, real-fixture consumption blocked by harness aggregator semantics.

### Smoke run outcome (cycle N+1)

- Verdict: `state/clm_eeg_smoke_v6_real_2026_05_03/verdict.json`
- Sentinel emit: `verdict = HARNESS_OK` (Run A synthetic baseline)
- Harness exit code: `0`
- Composite tally: `pass_count=3 / required=2 / harness_ok=1` (synthetic dry-run aggregation)
- Chained fingerprint: `2804516380`
- Per-metric (harness scope is p1/p2/p3 only):
  - `p1_dry_run_pass=1` (synthetic-frozen LZ proxy)
  - `p2_dry_run_pass=1` (synthetic-frozen TLR proxy)
  - `p3_dry_run_pass=1` (synthetic-frozen GCG proxy)
- Dual-lock policy: PRESERVED — harness `chflags nouchg` → run → `chflags uchg` re-applied; byte count `10633` unchanged; no content modification.


The smoke harness `clm_eeg_harness_smoke.hexa` is a **pure aggregator**: it reads three pre-existing `state/clm_eeg_p{1,2,3}_*_pre_register.json` files (which are FROZEN synthetic dry-run manifests as of 2026-04-26) and emits a composite verdict. It does NOT consume `CLM_EEG_FIXTURE_PATH` directly. Setting that env (or `CLM_EEG_HARNESS_FIXTURE_MODE=real`) on the smoke harness has no effect on its computation — the synthetic-vs-real dimension lives upstream in the p1/p2/p3 pre-register tools, all of which are themselves uchg-locked under the same dual-lock contract.


### Cycle N transcoder context (preserved)

Scaffold landed (cycle N−1). Sibling-BG P1 output (`welch_clean.npz` +
`verdict.json`) landed cycle N. The schema mismatch (P2 scaffold expected
`welch_clean_summary.json`; P1 wrote `verdict.json` + `welch_clean.npz`) is
now bridged by:

```
                                                         gitignored)
```

The transcoder reads P1's verdict.json + a numpy-helper dump of the welch
PSD and emits a `synthetic_16ch_v1.json`-compatible JSON fixture at:

```
anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json
```

Sentinel emit (stderr): `__BANDPOWER_TRANSCODE__ PASS <fixture-path>`


- **tier:** `functional_analog`
- **NOT** full PASS
- **N=1** single-subject, single-session, single-montage (Cyton+Daisy 16ch)
- No population statistics, no test–retest, no cross-vendor validation yet

## Components

| File | Role |
|------|------|
| `anima-clm-eeg/tool/clm_eeg_harness_realswap.hexa` | Adapter — synthetic passthrough OR real-swap from sibling-BG P1 NPZ summary |
| `anima-clm-eeg/tool/welch_to_bandpower_transcoder.hexa` | **NEW (cycle N)** — bridges P1 npz/verdict → synthetic_16ch_v1 fixture schema |
| `anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json` | **NEW (cycle N)** — emitted real fixture (functional_analog tier, N=1) |
| `anima-clm-eeg/state/realswap_pending_2026_05_03/README.md` | This file — activation runbook |


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

## Activation path (cycle N — transcoder landed)

The real fixture is now generated. Two pre-steps + one optional swap:


The hexa stage1 runtime sandboxes shell `exec()`, so the numpy helper must
be invoked DIRECTLY by the caller before the transcoder runs:

```bash
python3 state/.welch_to_bandpower_helper.py \
    state/berger_v6_clean_reanalyze_2026_05_03/welch_clean.npz \
    state/.welch_to_bandpower_dump.txt
```

This produces a flat-text per-channel band-power dump (×1000 fixed-point).


```bash
HEXA_RESOLVER_NO_REROUTE=1 hexa run \
    anima-clm-eeg/tool/welch_to_bandpower_transcoder.hexa \
    --welch-npz state/berger_v6_clean_reanalyze_2026_05_03/welch_clean.npz \
    --verdict-json state/berger_v6_clean_reanalyze_2026_05_03/verdict.json \
    --clean-channels "2,3,4,7,9,10,11,12,13,14,15" \
    --output-fixture anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json
```

Sentinel: `__BANDPOWER_TRANSCODE__ PASS anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json`

The fixture carries verbatim P1 verdicts (`f1_status`, `f2_status`,
`p1_tier: analog`, `n_subjects: 1`, `rail_quarantined_rows_1idx: [1,5,6,8,16]`,
and `clean_channel_mask` for downstream auditors.

### Step 3 — EXECUTED (cycle N+1, 2026-05-03)

User-approved unlock + smoke run + re-lock executed. Outcome:

- harness exit code = 0
- sentinel emit = `verdict = HARNESS_OK`
- re-lock confirmed (`chflags uchg` restored; byte count 10633 unchanged)
- artifact: `state/clm_eeg_smoke_v6_real_2026_05_03/verdict.json`
- run log: `state/clm_eeg_smoke_v6_real_2026_05_03/run.log`
- AI ledger: `docs/ai-native/clm_eeg_smoke_v6_real_run_2026_05_03.ai.md`

```bash
# AS-EXECUTED (2026-05-03 23:51 KST)
chflags nouchg anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
CLM_EEG_FIXTURE_PATH=anima-clm-eeg/fixtures/real_v6_clean_2026_05_03.json \
CLM_EEG_HARNESS_FIXTURE_MODE=real \
    HEXA_RESOLVER_NO_REROUTE=1 hexa run \
    anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa --selftest
chflags uchg anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa
```

### Optional: legacy adapter (clm_eeg_harness_realswap.hexa)

The pre-existing `clm_eeg_harness_realswap.hexa` scaffold expected a
`welch_clean_summary.json` schema that P1 did not produce. With the
transcoder now landed, the adapter is functionally superseded for the
real fixture path. It still serves as a synthetic-mode passthrough; no
edits to it this cycle.


- **No metric threshold relaxation.** Frozen pre-register thresholds in
  `clm_eeg_p1_lz_pre_register.hexa` / `clm_eeg_p2_tlr_pre_register.hexa` /
  `clm_eeg_p3_gcg_pre_register.hexa` REMAIN unchanged. Any post-hoc
  retuning to force PASS = SSOT v2 bump (no silent edit).
- **No re-execution by this scaffold.** It only adapts the fixture path;
  metric computation lives in the existing `clm_eeg_*_real.hexa` tools.
- **No interpolation across rail-quarantined channels.** Zero-fill only.

## Open questions for next cycle

1. ~~Should the band-power transcoder be a separate `.hexa` tool…~~
   **RESOLVED cycle N**: separate `welch_to_bandpower_transcoder.hexa` —
   keeps `clm_eeg_harness_realswap.hexa` as pure synthetic passthrough.
2. ~~Sibling-BG P1 NPZ schema not yet frozen…~~
   **RESOLVED cycle N**: schema confirmed (keys `f`, `psd_ec`, `psd_eo`,
   `ap_ec`, `ap_eo`, `clean_channels`, `railed_rows`, `labels`); see
   helper.py docstring for verified types/shapes.
3. ~~**GATING DEPENDENCY (next cycle)** — `clm_eeg_harness_smoke.hexa` is
   `chflags uchg`...~~
   **RESOLVED cycle N+1 (2026-05-03)**: user-approved unlock + smoke run +
   re-lock executed. Honest finding: the smoke harness is a pure aggregator
   over upstream p{1,2,3} pre-register JSONs and does NOT consume
   `CLM_EEG_FIXTURE_PATH` directly. Composite HARNESS_OK reflects
   synthetic-frozen pre-register dry-runs (NOT real fixture evaluation).
   For a TRUE real-fixture composite, the upstream p{1,2,3} pre-register
   JSONs themselves must be re-emitted from real-side data — but those are
   also uchg-locked under the same dual-lock contract. Cascade-unlock
   a separate `clm_eeg_harness_real_smoke.hexa` that defaults to real-side
   p{1,2,3}_real.json paths (preserves dual-lock on synthetic harness), or
   (b) v2 SSOT freeze of the entire pre-register chain on real fixture
   (signed, not silent).
   global scalar (median-alpha → target 1542 ×1000 to land in synthetic
   fixture range). This preserves cross-channel variance ratios but does
   NOT preserve absolute physical units (µV²/Hz). Downstream metrics that
   rely only on relative band ratios (γ/θ ratio, etc.) are unaffected;
   metrics that key off absolute thresholds would need a re-calibration
   pass — not in scope this cycle.
