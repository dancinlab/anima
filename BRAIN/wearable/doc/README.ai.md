# wearable/ — wearable physiology axis

Status: design-only (2026-05-06). Specs absorbed from `anima/design/`. No implementations yet.

## Scope
Consumer wearable physiological data (HRV / sleep stages / recovery / readiness / cardiac rhythm) used as cross-validation ground truth for hexa-brain EEG streams. Distinct axis from `eeg/` (PPG/HRV vs scalp EEG); paired analysis happens at integration layer.

## Sources
- **Oura Ring** — JSON export OR opt-in REST GET with personal access token (`~/.oura_token`, chmod 600, never committed).
- **Whoop** — manual CSV export from app web dashboard (no public API for free tier).
- **Cardiac (ECG/PPG)** — OpenBCI Cyton auxiliary analog GPIO (D11, D12, A6, A7) for in-helmet R-peak detection (Pan-Tompkins 1985), HR/HRV (Task Force 1996), heart-brain coherence (McCraty 2014).

## Canonical row schema `anima/wearable_health/1`
```
{ts: ISO-8601 UTC, source: "apple|oura|whoop",
 hrv_rmssd_ms: float, hr_bpm: int, spo2_pct: float,
 sleep_stage: "awake|rem|light|deep|null",
 recovery_x1000: int (0..1000), strain_x1000: int (0..1000),
 schema: "anima/wearable_health/1"}
```

## Provenance
- `doc/wearable_health_integration_paradigm_2026_04_28.md` — Apple Watch + Oura + Whoop spec (canonical row schema, NO-API constraint, opt-in API path)
- `doc/cardiac_eeg_integration_paradigm_2026_04_28.md` — Cyton aux GPIO ECG/PPG ↔ EEG cross-modal paradigm (heart-brain coherence)

Migrated from `anima/design/` on 2026-05-06 alongside the broader EEG → hexa-brain absorption.


## Reactivation
When implementation begins, follow the canonical hive mk2 layout:
```
wearable/{core,module,doc}/
  core/    wearable_unify.hexa (multi-source row converger)
  module/
    apple_health/{core,module,doc}/   xml_parse + health_export_decoder
    oura/{core,module,doc}/           json_decode + (opt-in) rest_client
    whoop/{core,module,doc}/          csv_decode
    cardiac/{core,module,doc}/        pan_tompkins + hrv_rmssd
  doc/     this README + paradigm specs
```
