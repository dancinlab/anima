---
schema: anima-eeg-core/_gates/ai-native/1
last_updated: 2026-05-02
ssot:
  composite:    anima-eeg-core/tool/modules/_gates/composite_gate.hexa
  berger_alpha: anima-eeg-core/tool/modules/_gates/berger_alpha.hexa
  rms_band:     anima-eeg-core/tool/modules/_gates/rms_band.hexa
  pe_saturation: anima-eeg-core/tool/modules/_gates/pe_saturation.hexa
  hjorth_band:  anima-eeg-core/tool/modules/_gates/hjorth_band.hexa
status: live — Phase 2 validity gates; 4 atomic + 1 composite; AND-rule (all_pass = berger ∧ rms ∧ pe ∧ hjorth)
roadmap_entry: 270
raws:
  - raw#9 hexa-only
  - raw#10 honest (1+ FAIL → downstream metrics meaningless)
  - raw#65 gate
  - raw#82 venv-eeg
  - raw#91 honest
  - own5
---

# anima-eeg-core gate modules (AI-native)

Phase 2 validity gates — 4 atomic gates + 1 composite. Each gate emits PASS/FAIL on a `.npy` input or selftest preset. Composite returns `all_pass = berger ∧ rms ∧ pe ∧ hjorth`. raw#10 honest: any single FAIL invalidates downstream metric interpretation.

## TL;DR for an agent reading this cold

- **5 files**: 4 atomic gates + 1 composite. ~150-280 LOC each.
- **AND-rule** composite — atomic gates are independently necessary for valid downstream metric computation.
- Each gate has selftest preset (pass / fail synthetic fixtures) + real-input mode (`--input <npy>`).
- Output is **key=value text** + JSON cert. `composite_gate.hexa` aggregates 4 atomic verdicts into one composite cert.
- @resolver-bypass(reason="darwin-native: .venv-eeg/bin/python BrainFlow venv on host").

## Architecture map

```
anima-eeg-core/tool/modules/_gates/
├── composite_gate.hexa     AND-aggregator over 4 atomic gates
├── berger_alpha.hexa       α-band dominance (8-12 Hz, eyes-closed Berger 1929)
├── rms_band.hexa           RMS within band — saturation/silence detector
├── pe_saturation.hexa      Permutation entropy ceiling — flat-line detector
└── hjorth_band.hexa        Hjorth activity / mobility / complexity range
```

## API contract

```hexa
// Per atomic gate:
fn run_<gate>(npy_path: string, fs: int) -> GateResult
// GateResult { passed: bool, reasons: [string], metric_value: float, threshold: float }

// composite_gate.hexa
fn run_all_gates(npy_path: string, fs: int) -> CompositeResult
// → CompositeResult {
//     berger:       GateResult,
//     rms:          GateResult,
//     pe:           GateResult,
//     hjorth:       GateResult,
//     all_pass:     bool,    // AND of 4 gates
//     dominant_fail: string  // first failed gate name (for triage)
// }
```

Output text format:

```
__GATE_BERGER_ALPHA__ PASS metric=0.523 threshold=0.30 ...
__GATE_RMS_BAND__     PASS rms=12.4 band=(0.5,5.0)
__GATE_PE_SATURATION__ PASS pe=0.78 threshold>=0.60
__GATE_HJORTH_BAND__   PASS activity=23.1 mobility=0.87 complexity=2.3
__COMPOSITE_GATE__     PASS all_pass=true (4/4)
```

JSON cert (composite):

```json
{
  "schema": "anima-eeg-core/_gates/composite/1",
  "all_pass": true,
  "atomics": {"berger": {...}, "rms": {...}, "pe": {...}, "hjorth": {...}},
  "input_sha256": "...",
  "fs_hz": 250
}
```

## Invocation patterns

```bash
# Composite gate on real input
hexa run anima-eeg-core/tool/modules/_gates/composite_gate.hexa \
  --input data/recorded.npy --fs 250

# Single atomic gate
hexa run anima-eeg-core/tool/modules/_gates/berger_alpha.hexa --selftest

# Selftest all 4
for g in berger_alpha rms_band pe_saturation hjorth_band; do
  hexa run anima-eeg-core/tool/modules/_gates/${g}.hexa --selftest
done
```

## Failure cascade

```
composite_gate.run_all_gates()
  ├── berger_alpha → PASS (α 8-12 Hz dominance ≥ 0.30)
  ├── rms_band     → FAIL (silence: rms < 1.0 µV)
  └── early-out OR continue (raw#10 honest: continue, surface ALL fails)
```

When `all_pass=false`:
- Downstream metrics (Φ, LZ76, Hjorth, coherence) are flagged invalid.
- `dominant_fail` field lets pipeline_suggester re-route (e.g. RMS_FAIL → suggest higher gain).
- Audit row emits `gates_passed=N/4, dominant_fail=<name>` for triage.

## raw#10 caveats

1. **AND-rule strict.** No partial-credit. 1 atomic FAIL → all_pass=false. raw#10 honest: ambiguous data is worse than no data for consciousness inference.
2. **Berger threshold 0.30** assumes occipital channel selection. Frontal channels need lower threshold (~0.15) — currently hardcoded; future raw#10 debt is per-channel threshold table.
3. **PE saturation assumes 250 Hz fs.** Other fs need m, τ recalibration (`pe_saturation.hexa --fs 500 --m 4 --tau 2`).
4. **Hjorth complexity is sensitive to filter.** Run `composite_gate` AFTER `_core/filter_pipeline.hexa` (notch+bandpass), never on raw.
5. **Composite cert lacks prev-cert chain hash.** Tampering detectable per-cert but not at sequence level.
6. **No streaming gate.** Each gate is whole-file; real-time gating requires sliding-window driver (Phase 5+).

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `composite_gate.hexa` | `12f50e50f91eb64b1bcb31d7a5a5b0d2dcea6913ca6eefee34dad7b9a458138d` | 152 |
| `berger_alpha.hexa` | `1a84e3d8e5847563a3c3a5918ade07cd75417a44f42b8643dae42c7e532ad8ef` | 280 |
| `rms_band.hexa` | `3e5b0961f7b0ade470755822098a70d59eb1b0378a6f9db13f6e3b0fd4e07339` | 231 |
| `pe_saturation.hexa` | `fa461626946797cca258c8cca09c88c3ac163ece46cfe0da1ecc2702939af854` | 261 |
| `hjorth_band.hexa` | `b0e2b049bf5f9a6582d470a2bd8545a2a29e98c29913139cca42ed32d311a459` | 243 |

shas pinned 2026-05-02.
