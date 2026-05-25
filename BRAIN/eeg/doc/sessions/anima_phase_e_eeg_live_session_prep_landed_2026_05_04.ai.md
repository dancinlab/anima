# Phase E EEG Live Session Prep — landed 2026-05-04 (1-page handoff)

**Spec**: `docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md`
**Cycle**: BG-PHASE-E-PREP+QMIRROR-COND6 (sister: qmirror cond.6 inclusion decision)
**Status**: SPEC FROZEN, awaiting user-gated 30-min OpenBCI EEG session.
**Cost**: $0 ubu1 CPU + 30 min user wall + 5 min stabilize prereq.

## What landed

A self-executable runbook for a single 30-min OpenBCI Cyton+Daisy 16ch EEG session that delivers Phase E binding-evidence verdict. Integrates:

- BLM Phase 5 ROI (T7/T8/P7/P8 + 250-300 ms post-onset epoch) for methodological homology with ZuCo SR analysis.
- Existing Phase E 5-tier falsifier preregister (`state/cp2_clm_phase_e_spec_2026_05_02/`) extended with two **EEG-side gating falsifiers**: F-PHASE-E-1 (high-gamma 30-80 Hz cross-electrode coherence ≥ 0.5, perm p < 0.01, bootstrap 95% CI lower > 0.4) and F-PHASE-E-2 (LSL marker → EEG sample sync median latency < 50 ms, ≥ 95% within ± 100 ms).
- Stimulus protocol P1-P4 (eyes-closed 5min / eyes-open 5min / reading 15min / post-rest 5min) with self-paced spacebar advance, 1.5 s minimum dwell, target N = 300 sentences, audio-sync pulse on Cyton AUX channel 17 for cross-clock verification.
- Hardware checklist (Cyton+Daisy 16ch, 250 Hz, < 10 kΩ impedance, 10-20 placement with mandatory T7/T8/P7/P8) and user pre-session attestation per §54.2 alcohol/sleep/caffeine anchor.

## Verdict criteria (locked)

- **PHASE_E_BINDING_WITNESSED** = F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + N ≥ 300 → F1_v2 **raw** 0.408 → 0.558 (YELLOW reach per §49.5 projection); F1_v2 **canonical band** stays RED because `f2_override_canonical: true` (per `f1_v2_band_thresholds_2026_05_04`); `n_substrate.blk.1` structural F2 ceiling **NOT** lifted, only F1 raw component raised.
- **PHASE_E_PARTIAL** if N in [100, 300) — same-day replicate before classifying.
- **F-WEAK / F-FAIL** per existing 5-tier preregister; pivot to path (b) learned phi_extractor.
- **F-ARTIFACT** override if F-PHASE-E-2 FAILs OR R-control matches real (existing R1/R2/R3).

## What this enables

- User can self-execute a single 30-min session when ready (alcohol-free 24-48h + sleep + caffeine/exercise compliance + 5-min stabilization).
- Output `state/anima_phase_e_eeg_live_<DATE>/verdict.json` is deterministic vs the locked criteria — no post-hoc reinterpretation gap.
- Post-session annotations to `.roadmap.n_substrate` cond.1 + `.roadmap.eeg` cond.5/cond.7 are pre-drafted in §10.1/§10.2 of the spec for an additive-only mutation cycle.

## What this does NOT enable

- F2 14-gate substrate-architectural L1 0/16 ceiling unaffected (separate path: learned phi_extractor + N-22 Levin + IIT 4.0 proper phi, $1500+ separate budget).
- Population-level binding claim out of scope (N=1 within-subject).
- Phenomenal tier reservation per `n_substrate_putnam_cross_link_spec_2026_05_04` §5.3 unchanged — Phase E PASS emits `WITNESSED_ANALOG` only.

## Honest C3 (8 caveats)

C1 sampling rate asymmetry (Cyton+Daisy 250 Hz vs ZuCo 500 Hz; ~50-sample epoch borderline for multitaper). C2 16 ch precludes surface Laplacian; binding-by-scalp-coherence not binding-by-cortical-source. C3 attentional drift in reading task unobservable beyond dwell-time gating. C4 0.5 coherence threshold liberal vs cortical 0.3-0.4 literature; chosen for FP-rate control on scalp + volume conduction. C5 N = 300 ceiling tight in single 30-min session at 3 s mean dwell. C6 Phase E PASS does NOT lift F2 ceiling. C7 N=1 within-subject. C8 corpus is methodologically homologous (ZuCo SR-task transcript text) but not subject-identical.

## Raw invariant compliance


## Sister landings this cycle

- `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md` — qmirror cond.6 N_witnessed inclusion + concordance pair denominator exclusion locked per Putnam spec §4.4 informative-substrates filter.
- `docs/n_substrate_qmirror_cond6_inclusion_landed_2026_05_04.ai.md` — sister 1-page handoff.
