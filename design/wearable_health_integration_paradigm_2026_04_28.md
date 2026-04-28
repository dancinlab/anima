# Wearable Health × EEG Integration Paradigm — Design Doc (2026-04-28, C18)

## Purpose
Integrate consumer wearable physiological data (HRV, sleep stages, recovery /
readiness scores) with anima-eeg streams so that long-horizon EEG correlates
(engagement, drowsy_idx, LZ76 b(n), overnight T14 sleep classifier) can be
**cross-validated** against an independent physiological ground truth.

The system must run **without any cloud API call** for the EEG host
(raw#13 NO-API constraint). For Oura, the optional remote endpoint is invoked
only by an explicit user-loaded helper with the user's own personal access
token; the EEG / Claude CLI process never reaches the network on its own
(raw#37 transient helper, raw#65 idempotent re-run).

## Three supported wearable types

| # | Source | Ingestion path | Time precision | Notes |
|---|--------|----------------|----------------|-------|
| 1 | **Apple Watch** (via iPhone Health.app) | manual ZIP export → `export.xml` | 1 s | user must run Settings → Health → Export Health Data, then copy ZIP to repo |
| 2 | **Oura Ring** | (a) JSON export from app, OR (b) Personal Access Token + REST GET | 60 s (sleep), 1 s (HRV) | API key lives in `~/.oura_token` (chmod 600); never committed |
| 3 | **Whoop** | manual CSV export from app web dashboard | 60 s (recovery), 1 s (workout HR) | no public API for free tier |

All three converge into a **canonical row schema**
`anima/wearable_health/1`:
```
{ts: ISO-8601 UTC, source: "apple|oura|whoop",
  hrv_rmssd_ms: float, hr_bpm: int, spo2_pct: float,
  sleep_stage: "awake|rem|light|deep|null",
  recovery_x1000: int (0..1000), strain_x1000: int (0..1000),
  schema: "anima/wearable_health/1"}
```

## NO-API constraint reinforcement (raw#13)

- Apple Health: **strictly local** XML parse; no Apple ID / iCloud touched.
- Whoop: **strictly local** CSV parse.
- Oura: API path is **opt-in**; `--source oura --token-file ~/.oura_token`.
  Default mode is `--source oura --json <file>` (offline JSON export).
- The hexa tool itself never calls the network; only `/tmp/wearable_helper.py`
  does, and only when invoked with `--mode api-oura` and the token file
  present. Helper is regenerated each run (raw#37 transient).

## EEG correlation hypotheses (frozen — raw#12)

| H | Wearable signal | EEG signal | Window | Min Pearson r |
|---|-----------------|------------|--------|---------------|
| H1 | HRV RMSSD (ms) | engagement_index | 5-min sliding | +0.20 |
| H2 | HRV RMSSD (ms) | drowsy_idx | 5-min sliding | -0.20 (negative) |
| H3 | sleep_stage | overnight T14 classifier | 30-s epoch | accuracy ≥ 60% |
| H4 | recovery_x1000 (morning) | morning resting LZ76 b(n) | per-day | +0.20 |
| H5 | strain_x1000 (workout) | post-workout drowsy_idx delta | per-event | +0.20 |

Frozen criteria (raw#12):
- Time precision **1 s** (sub-window resolved to 1 s).
- N ≥ **14 days** to clear noise floor (rule of thumb for r≥0.20 at α=0.05).
- HRV-EEG paired window **5 min sliding**.
- Minimum meaningful correlation `|r| ≥ 0.20`; `|r| < 0.10` ⇒ negative finding.

## Time alignment

- All wearable rows are converted to **UTC ISO-8601** at ingest.
- EEG rows already carry UTC ts (anima-eeg recorder).
- Join: bucket both streams to **5-min aligned windows** (`ts // 300 * 300`).
- Tolerance: ≤ 5 s between paired ts inside the same bucket (F2 falsifier).
- Mismatch > 5 s → row dropped, logged as `align_drop` (not silently joined).

## Privacy invariants (raw#13)

| I | Statement |
|---|-----------|
| I1 | NO GPS / latitude / longitude fields ever stored |
| I2 | NO contacts / SMS / call / email metadata ever stored |
| I3 | NO photo / video bytes — Health export's photo metadata excluded |
| I4 | Apple Health `<MetadataEntry>` for `HKQuantityTypeIdentifierBloodGlucose` etc. medical PHI is filtered to the 7 fields in the canonical schema only |
| I5 | API tokens live in `~/.oura_token` (chmod 600); never echoed, never committed; regex `[A-Z0-9]{32}` masked in any log output |

Falsifier F5 below directly enforces I1–I3.

## Implementation sketch

- Hexa wrapper: `anima-eeg/tool/wearable_health_integrator.hexa` (~150 LoC,
  same pattern as B11 behavioral_correlates_logger).
- Python helper: `/tmp/wearable_helper.py` (transient — raw#37).
  - `--mode synth-apple` deterministic Apple Watch row
  - `--mode synth-oura` deterministic Oura row
  - `--mode synth-whoop` deterministic Whoop row
  - `--mode parse-apple --in <path-to-export.xml>` real Apple parse
  - `--mode parse-oura --in <path-to-oura.json>` real Oura JSON parse
  - `--mode parse-whoop --in <path-to-whoop.csv>` real Whoop CSV parse
  - `--mode api-oura --token-file ~/.oura_token --since YYYY-MM-DD` (opt-in)
- Output: append-only JSONL at
  `state/wearable_eeg_audit/<UTC-date>_wearable.jsonl`.
- Selftest harness (`--selftest`) writes 3 deterministic rows (one per source)
  to `state/anima_eeg_wearable_selftest.jsonl`, no real data needed.

## Five raw#71 falsifiers

| F | Statement | Sentinel value |
|---|-----------|----------------|
| F1 | User does NOT own the wearable → ingestion fails closed (no fabricated row) | parse-mode with missing `--in` returns exit 2, NOT exit 0 with synthetic row |
| F2 | time-align mismatch > 5 s → row tagged `align_drop`, NOT joined | helper join() with ts diff 6 s emits `align_drop:1` |
| F3 | N < 14 days → emit `insufficient_n` warning, refuse correlation report | `--correlate` over <14 distinct UTC dates returns exit 3 |
| F4 | `|r| < 0.10` over all 5 hypotheses → emit `null_finding` row, do NOT silently re-tune | bench harness with synthetic uncorrelated streams must yield `null_finding:1` |
| F5 | privacy field leak (lat/lon/contacts/title/url) → falsifier hard-fails | grep over emitted JSONL for `latitude\|longitude\|contact\|sms\|message_body\|photo` must return zero matches |

All five are exercised by `--falsifiers`; expected output `5 / 5 PASS`.

## raw refs (own-5 ≥ 2)

- raw#9 (cross-evidence) · raw#10 (proof-carrying) · raw#12 (frozen criteria)
- raw#13 (NO API) · raw#37 (transient helper) · raw#65 (idempotent)
- raw#71 (≥5 falsifiers) · raw#82 (privacy) · raw#91 (genus distinct)
- own-5 frameworks: Shaffer & Ginsberg 2017 HRV; Walker 2017 (sleep);
  Plews 2013 HRV training; Hjortskov 2004 (HRV-stress); Berry 2015 AASM.

## Genus (raw#106)

`wearable-physiology-eeg-cross-validation-integrator`

Distinct from B11 (behavioral inputs from the host machine: typing, mouse,
app switching) and from T2 (host context labeling). C18 reads exclusively
from external worn devices.

## User action plan

The user's responsibility (hardware-dependent — raw#10 honest C3):

1. **Apple Watch / iPhone**:
   `Settings → Health → Profile → Export All Health Data → ZIP`
   Copy `export.zip` to `state/wearable_inbox/apple_export_<YYYYMMDD>.zip`,
   unzip; the resulting `apple_health_export/export.xml` is the input.
   Run: `hexa anima-eeg/tool/wearable_health_integrator.hexa --ingest \
        --source apple --in state/wearable_inbox/apple_health_export/export.xml`
2. **Oura Ring**:
   App → Menu → Account → Export Data → email-zip OR
   https://cloud.ouraring.com/personal-access-tokens → save 32-char token
   to `~/.oura_token` then
   `hexa ... --ingest --source oura --token-file ~/.oura_token --since 2026-04-14`
3. **Whoop**:
   web dashboard → My Data → Export → CSV.
   `hexa ... --ingest --source whoop --in state/wearable_inbox/whoop_<date>.csv`

If the user does NOT own any of the three devices, the C18 pipeline remains
**dormant**; `--selftest` still passes (synthetic rows), but no real
correlation report is produced. This is the correct, falsifier-F1 honored
behavior.
