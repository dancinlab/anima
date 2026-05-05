# anima-eeg EC/EO label-fix investigation — landed 2026-05-05

**Lane**: `EEG-EC-EO-LABEL-FIX`
**Cost**: $0 (local CPU reanalysis on Mac, no ubu1 round-trip needed — npy files already on Mac)
**Wall time**: ~30 sec actual analysis + verdict
**Inputs**:
- `state/anima_phase_e_eeg_live_2026_05_05/berger_{ec,eo}_60s.npy` (today)
- `anima-eeg/recordings/sessions/berger_{ec,eo}_60s_v6_2026_05_03.npy` (v6)
- existing sanity verdict at `state/phase_e_ec_eo_sanity_analysis_2026_05_05/verdict.json`

**Outputs**:
- `state/phase_e_ec_eo_label_fix_investigation_2026_05_05/verdict.json`
- `tool/transient_py/eeg_ec_eo_label_swap_investigation_2026_05_05.py` (raw#37 transient)

---

## Result summary

| hypothesis | today (2026-05-05) | v6 (2026-05-03) | overall |
|---|---|---|---|
| H1: EC/EO label swap at capture | passes after swap (O1 0.31→3.25, O2 0.02→50.8) | partial (O1 swap helps, O2 ratio ~1.0 either way) | **NOT confirmed jointly** |
| H2: O2/P4 floating/saturated | O2/P4 alpha 239x avg of other channels — saturated | all 16 channels share huge alpha (avg 43726 uV²) — different pathology | **confirmed for today**; v6 has *different* but related impedance issue |
| H3: EOG dominance on EO frontal | frontal RMS 13.6x occipital — severe blink contamination | frontal/occipital RMS ~1.5x — within normal range | confirmed for today only |

**Conclusion**: `H2+H3` — capture-quality hardware/contact problems, NOT a label swap.

**Berger classical replicated post-fix**: `false`
**Ready for Phase E main protocol**: `false`
**Next action**: `electrode_reseat_O2_P4_plus_new_capture` (and address EOG contamination via prep instructions or ICA).

---

## Why H1 is not the right fix

The H1 swap test for **today** alone looked compelling (both O1 and O2 ratios flip strongly above 1.0 when EC/EO files are swapped). But on closer inspection:

1. The post-swap O2 ratio of 50.8 is *too clean* — it is driven entirely by the saturation pattern of the floating O2 input. The "EC" file (when swapped, the original EO file) happens to have a smaller saturation amplitude. The result is a ratio of saturation noise, not cortical alpha.
2. For v6, swapping the labels does not produce a joint pass: O2 ratio stays at ~1.0 in both directions (O1 0.97 ↔ 1.03; O2 1.01 ↔ 0.99). v6 has a uniform contamination across all 16 channels (avg alpha 43726 uV² vs today's 3.6 uV²), suggesting reference-electrode failure or board-level coupling rather than per-channel floating.
3. If H1 were the true root cause, both captures would show classical Berger after swap. They don't.

So even though the H1 swap appears to "rescue" today's data, this is an artefact of how the saturation interacts with band-power integration — not real cortical signal.

## Why H2 is decisive for today

- 14 of 16 channels: alpha power 0.9–6.4 uV² (physiologically plausible scalp EEG resting alpha)
- O2: 869 uV² → 239× channel-set average
- P4: 869 uV² → 239× channel-set average (same magnitude as O2 → suggests shared reference floating, not per-channel artefact)
- These two channels' contribution dominates the "occipital sum" in F-BERGER-1 and F-BERGER-2, masking the actual cortical signal in O1.
- In fact O1 alone shows: alpha_O1_ec=4.29 vs alpha_O1_eo=13.94 — wrong direction (EC < EO). With ratio 0.31, O1 alone fails F-BERGER-1.

So H2 is real and decisive for today's capture quality, but H2 alone does not rescue Berger either.

## v6 has a separate pathology

v6 captures show *all 16 channels* with mean alpha ~43k uV² (~four orders of magnitude above today's clean channels). O2/P4 are still elevated (3.5x average) but not in the saturation regime that today's are. This pattern is consistent with reference-electrode contact failure (mains/EMI coupling raises floor on every channel uniformly).

## Recommendation for next capture

Hardware checks before any new capture:
1. Reseat O2 and P4 electrodes; verify impedance < 100 kΩ
2. Verify reference (Cyton SRB2/bias) connection — solid contact on earlobe/mastoid
3. Run a 30 s eyes-closed test before full Berger and confirm O1/O2 alpha sit in the 1–50 uV² range
4. EOG mitigation: ensure subject minimizes blinking during EO blocks; if persistent, plan ICA artefact-removal step
5. Audit the cue script to rule out user/operator EC/EO confusion at start; even though H1 didn't confirm, the protocol should be hardened (audible "EYES CLOSED" / "EYES OPEN" cue with a 3 s settle period before recording starts)

## Decision for current Phase E main protocol

**Do NOT use today's or v6 baselines for Phase E binding claims.** The Berger classical sanity check is a *capture quality gate*; both pre-existing baselines fail it for non-recoverable reasons (saturated channels and EOG dominance), and the label-swap hypothesis is not the explanation. A new capture is required after electrode reseat.

## Audit honest_c3 (≥5)

- C1: 60 s baseline only — no behavioural binding evidence (high-gamma coherence, theta-gamma PAC); label-swap test cannot validate task-locked phenomena.
- C2: hypothesis test compares between-condition power — does not exclude shared electrode-impedance pathology that produces same direction in both runs.
- C3: single subject, single electrode set, two sessions — no inter-subject control; if same user habitually reverses cue, label swap would be systematic and undetectable from data alone.
- C4: O2/P4 alpha 239× average strongly suggests floating-input saturation (50/60 Hz mains pickup) — alpha-band integral on saturated channel is meaningless.
- C5: filtfilt zero-phase 1–50 Hz bandpass does not remove EOG (eye-blink ~10 Hz transient) — frontal alpha in EO may be EOG, not cortical.
- C6: even if H1 had confirmed, swapping label files does not address WHY swap occurred at capture time — capture protocol/cue script audit needed regardless.
- C7: peak alpha freq ~8.5 Hz at O1 is on the low edge of alpha — could be theta leakage rather than classical 10 Hz Berger rhythm.

## Compliance

- raw#9: no model weights / large datasets created
- raw#37: analysis script lives at `tool/transient_py/eeg_ec_eo_label_swap_investigation_2026_05_05.py` (transient sister-rule, opt-out from py→hexa)
- raw#10: ≥5 honest_c3 entries (7 provided)
- raw#15: no git commit
- no new capture (existing data only)
