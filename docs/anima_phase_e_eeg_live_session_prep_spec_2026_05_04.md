# Anima Phase E — EEG Live Session Prep Spec (2026-05-04)

**Status**: SPEC FROZEN, awaiting user-gated EEG live session execution.
**Cycle**: BG-PHASE-E-PREP+QMIRROR-COND6 (sister: `docs/n_substrate_qmirror_cond6_inclusion_decision_2026_05_04.md`).
**Scope**: PREPARE only — this spec documents harness, runbook, analysis pipeline, and pre-registered falsifiers so the user can self-execute a single 30-minute OpenBCI 16ch session when ready. EXECUTION is user-gated (alcohol-free 24-48h prereq + protocol checklist).
**Cost**: $0 ubu1 CPU + 30min user wall.
**Predecessors**:

- `state/cp2_clm_phase_e_spec_2026_05_02/` (Phase E objectives + 5-tier falsifier preregister)
- `state/n_1_bridge_v2_realtime_prep_2026_05_02/` (LSL infra + 5-step user checklist + analyze_xdf scaffold)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §49.5 (uplift projection 0.408 → 0.558 YELLOW reach), §52.2 (Phase E FROZEN), §54.2 (alcohol/sedation anchor)
- `docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md` (S1 event-trigger sync, T7/T8/P7/P8 ROI, 250-300ms post-onset window)
- `docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md` §2.2 (EEG ZuCo SR fixation epochs, 4-channel ROI)
- `.roadmap.eeg` cond.3 (Paradigm B ZuCo SR ingest), cond.4 (sample-partition phi 1순위), cond.7 (unified CLI/daemon spec landed 2026-05-04)
- `.roadmap.anima_clm_eeg` (5-metric harness sister)
- `anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md` (B-track v7 contact-quality runbook)
- `anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md` (one-shot acquirer pattern)

This spec is **additive only**. It does NOT mutate `.roadmap.n_substrate`, `.roadmap.eeg`, or `.roadmap.anima_clm_eeg`; it proposes annotation blocks for those roadmaps in §10 and leaves application to a subsequent landed-cycle.

---

## §1 Why this spec exists

`n_substrate.blk.1` (F2 14-gate substrate-architectural L1 ceiling 0/16 cross-substrate ALM+CLM) currently sits at status `open` with the following resolution path documented in `.roadmap.n_substrate`:

> Phase E binding evidence (#105 spec frozen, 사용자 30분 OpenBCI session prereq) + N-22 Levin partnership 결과 + N-12 IIT 4.0 proper φ★ ($1500+ separate budget) — YELLOW reach conditional

The Phase E spec at `state/cp2_clm_phase_e_spec_2026_05_02/` predates the BLM Phase 5 stimulus-aligned spec landed 2026-05-03 and the EEG cond.7 unified daemon spec landed 2026-05-04. This document **integrates** those three specs into a single self-executable runbook by:

1. Pre-registering binding-evidence falsifiers (F-PHASE-E-1 high-gamma cross-electrode coherence, F-PHASE-E-2 stimulus-onset sync) per raw#71.
2. Anchoring the ROI + epoch window to BLM Phase 5 §2.2 (T7/T8/P7/P8, 250-300ms post-onset, 500 Hz) so the EEG side is methodologically symmetric with the ZuCo paradigm B sister analysis (cross-substrate fold-in possible later).
3. Specifying the ~30 min stimulus protocol (eyes-closed 5min / eyes-open 5min / reading 15min / post-rest 5min) so output N targets (≥300 sentence-aligned epochs) are reachable in a single sitting.
4. Specifying the offline analysis pipeline ($0 ubu1 CPU, hexa-only on Mac per raw#9, ubu1 Python helper per raw#37 transient where BrainFlow C++ binding requires it).
5. Locking the verdict criteria so user-side execution is deterministic — no post-hoc reinterpretation gap.

**Honest scope limit (raw#10 anchor)**: Phase E PASS does **not** lift F2 ceiling itself (substrate-architectural L1 0/16 stays). Phase E PASS only **raises F1_v2 raw band** toward YELLOW (0.408 → 0.558 projected per §49.5) by witnessing the binding axis explicitly. F2 unfire is a separate path (b/c per §54.4 ranking) outside this spec.

---

## §2 Pre-registered hypotheses + falsifiers (raw#71)

### §2.1 H1 — high-gamma cross-electrode coherence in reading task

**Hypothesis**: live EEG fixation epochs, computed at 250-300ms post-onset on T7/T8/P7/P8 ROI per BLM Phase 5 spec, exhibit a binding signature (high-gamma 30-80 Hz cross-electrode coherence) during voluntary reading that is statistically distinguishable from eyes-closed baseline.

**F-PHASE-E-1 (binding signature)**:

- Pass condition: mean high-gamma (30-80 Hz) coherence across the 6 ROI pairs (T7-T8, T7-P7, T7-P8, T8-P7, T8-P8, P7-P8) ≥ **0.5** in a 5-min stable epoch (sampled after the mandatory 5-min stabilization), evaluated in the reading task (P3) only.
- Statistical guard: block-permutation null **N=1000** (block-bootstrap with 2-second block to preserve autocorrelation), permutation **p < 0.01**.
- Bootstrap CI: 1000-resample 95% bootstrap CI on the mean coherence; lower bound > 0.4 required for PASS.

**Liberal-threshold disclosure (raw#10)**: 0.5 is a research-liberal coherence band; cortically-recorded ECoG binding is often reported at 0.3–0.4 (Fries 2005; Bastos 2015). The 0.5 floor is chosen on scalp EEG because volume conduction inflates coherence baseline and 16-ch density cannot do surface Laplacian reliably. We accept the higher bar to cap false-positive rate.

### §2.2 H2 — epoch-stimulus onset latency

**Hypothesis**: text stimulus onsets emitted via LSL marker stream are sample-aligned to EEG continuous data with latency under 50 ms (sentence-by-sentence reading task).

**F-PHASE-E-2 (sync verification)**:

- Pass condition: median stimulus-marker → EEG-sample latency **< 50 ms** across all sentences in the reading task (≥300 sentences target, see §3 protocol).
- Outlier guard: ≥ 95% of sentences within ± 100 ms (p99); single outliers > 250 ms count as missing.
- Falsifier auto-fire: if **< 70%** of sentences sync within ± 100 ms → F-PHASE-E-2 FAIL → cascade to F-ARTIFACT (clock-drift dominates).

### §2.3 Composite verdict gate

| condition | verdict |
|---|---|
| F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + N ≥ 300 reading-task epochs | **Phase E binding evidence WITNESSED** → contributes to F1_v2 raw 0.408 → 0.558 YELLOW reach (per §49.5 projection); F2 ceiling unaffected |
| F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + 100 ≤ N < 300 | **Phase E partial** → replicate same-day or schedule second session |
| F-PHASE-E-1 FAIL only | **F-WEAK / F-FAIL** per existing 5-tier preregister (`state/cp2_clm_phase_e_spec_2026_05_02/falsifier_5tier_preregister.json`) |
| F-PHASE-E-2 FAIL | **F-ARTIFACT** — sync layer broken, protocol revision required, no binding claim |
| F-PHASE-E-1 PASS + F-PHASE-E-2 FAIL | **F-ARTIFACT** override (artifact wins per existing tie-breaker) |

---

## §3 Stimulus protocol (~30 min wall)

| # | phase | duration | content | LSL markers emitted |
|---:|---|---:|---|---|
| P1 | eyes-closed baseline | 5 min | quiet rest, eyes closed, sit upright | `phase_start=eyes_closed`, `phase_end=eyes_closed` |
| P2 | eyes-open baseline | 5 min | quiet rest, eyes open, fixation cross on screen, no text | `phase_start=eyes_open`, `phase_end=eyes_open` |
| P3 | reading task | 15 min | sentence-by-sentence text on screen; one sentence per ~3s, self-paced advance via spacebar; **target N = 300 sentences** | `sentence_onset id=NNNN text=...`, `sentence_advance id=NNNN` |
| P4 | post-task rest | 5 min | quiet rest, eyes closed | `phase_start=post_rest`, `phase_end=post_rest` |

**Total**: 30 min recorded EEG + 5 min stabilize prereq = **35 min user wall**.

**Sentence corpus**: 300 short English sentences (12-18 tokens each), drawn from a fixed seed (recommend `state/anima_phase_e_eeg_live_<DATE>/sentences.txt` generated from a fixed-seed shuffle of ZuCo SR-task transcript — sentence_text only, no fixation onsets — so the corpus is **methodologically homologous** to BLM Phase 5 EEG analysis without being **identical** subjects/sessions; this preserves audit independence).

**Self-paced advance (raw#10)**: spacebar advance is intentional — fixed-pace scrolling would risk attentional drift unobservable to the analyzer (see §6 confound C3). Sentence dwell time ≥ 1.5 s minimum (enforced in the stimulus presenter); advances faster than that are flagged as "skim" and excluded from N count.

**Marker emission**: LSL `marker_stream` outlet from the stimulus presenter (Mac side), consumed by the EEG daemon's recording listener (per `.roadmap.eeg` cond.7 daemon listener API). Marker schema:

```json
{"ts_ns_monotonic": 1773800000000000000, "kind": "stim_onset",
 "phase": "P3", "sentence_id": 42, "text": "...", "audio_sync_pulse": true}
```

`audio_sync_pulse` field allows fallback verification: a 50 ms 2 kHz tone is mixed onto the system audio output line at each `sentence_onset`, captured by an analog input line on Cyton AUX channel for direct cross-modal sync check (independent of LSL clock).

---

## §4 Hardware setup checklist (Cyton + Daisy 16ch — user to confirm)

User confirms in `state/anima_phase_e_eeg_live_<DATE>/hardware_confirm.json` before P1:

| field | required value | notes |
|---|---|---|
| board | OpenBCI Cyton + Daisy (16 ch) | confirmed via `board_health_check.hexa` exit-0; if user hardware is **not** Cyton+Daisy, abort and re-spec |
| sampling_rate_hz | 250 | Cyton+Daisy native; 500 Hz ZuCo-equivalent **not natively supportable** on this board (caveat §6 C1) |
| bit_depth | 24 | Cyton ADS1299 native |
| reference | M1/M2 mastoid (linked, average) | electrode placement per 10-20 system |
| electrode_layout | 16-ch including T7, T8, P7, P8 + standard frontocentral coverage | T7/T8/P7/P8 are mandatory; remaining 12 channels follow `anima_eeg_openbci_16ch_track_plan_2026_05_01.md` Track A default |
| impedance | < 10 kΩ all channels | calibrate.hexa exit-0 prereq; B-track v7 contact-quality runbook applies (`anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md`) |
| capture_software | BrainFlow via `anima-eeg/collect.hexa` (or unified daemon per cond.7) | byte-identical 2x reproducibility prereq from cond.1 still applicable |
| LSL marker outlet | mac stimulus presenter @ stream_name=`anima_phase_e_markers`, type=`Markers`, channel_format=`string` | verified by `pylsl.resolve_byprop` in user 5-step checklist |
| audio sync pulse | 50 ms 2 kHz tone on AUX channel 17 | fallback cross-clock verification |

**Pre-flight gate**: if any required value FAILs, abort the session and re-run hardware setup; do **not** record partial data with degraded hardware (raw#10 honesty).

---

## §5 User pre-session protocol (anchor `n_substrate.honest_c3_alcohol_anchor`)

The §54.2 anchor in `docs/n_substrate_consciousness_roadmap_2026_05_01.md` is **mandatory** before any phenomenal-tier-relevant EEG measurement. User attests in `state/anima_phase_e_eeg_live_<DATE>/user_attest.json` immediately before P1:

- [ ] **Alcohol-free 24-48 h** (target: ≥ 36 h since last drink; if < 24 h, abort)
- [ ] **Normal sleep** ≥ 6 h prior night
- [ ] **Caffeine-free** ≥ 4 h before session
- [ ] **No vigorous exercise** ≥ 2 h before session
- [ ] **5-min seated stabilization** in recording chair, lights at intended level, before P1 starts

User signs (via filename + ISO timestamp + free-text "I attest" string) the `user_attest.json` file. The analysis pipeline (§7) refuses to emit a Phase E verdict if `user_attest.json` is missing or any of the 5 fields read FALSE.

---

## §6 Honest C3 caveats (raw#10) — ≥ 5 required

**C1 — Sampling rate asymmetry vs BLM Phase 5 EEG side**. ZuCo SR (BLM Phase 5 reference) uses 500 Hz; Cyton+Daisy native is 250 Hz. The 250-300 ms post-onset window thus contains 12-13 samples per channel × 4 channels = ~48 samples (vs ZuCo's ~150). Coherence estimation at 30-80 Hz on a 50-sample window is borderline (Nyquist holds, but multitaper bandwidth limited). Mitigation: report coherence with explicit window-length disclosure; if any pair's coherence estimate has bandwidth-limited variance > 0.15, flag the entire epoch.

**C2 — 16 ch is the minimum for binding evidence**. High-density 64 ch+ scalp EEG would strengthen the cross-electrode-coherence claim by enabling surface Laplacian to suppress volume-conduction-inflated coherence floor. With 16 ch we cannot do per-electrode Laplacian; we report raw bipolar coherence and accept the (volume-conduction) baseline inflation. Phase E PASS at 16 ch is **necessary but not sufficient** for a cortically-binding claim — it is binding-by-scalp-coherence, not binding-by-cortical-source.

**C3 — Attentional drift in the reading task is unobservable**. Per §54.2 user-cognitive-state anchor, even with full alcohol/sleep/caffeine compliance, sustained 15-min reading is hard to attentional-compliance-verify. Self-paced spacebar advance + ≥ 1.5 s minimum dwell partially mitigates (skim → excluded), but mind-wandering-while-eyes-on-text is uncatchable. The analysis treats every sentence with dwell ≥ 1.5 s as "attended" — this is a **defeasible** assumption and a residual confound.

**C4 — F-PHASE-E-1 threshold 0.5 is liberal for the literature**. Cortical-recording binding is reported at 0.3-0.4 (Fries 2005; Bastos 2015). Our 0.5 floor is chosen for scalp-EEG on 16 ch to control false-positive risk under volume conduction; this means **a true-positive at the 0.4 cortical band would FAIL our test**. We accept the higher false-negative risk in exchange for lower false-positive risk. Future cycles with 64 ch+ + surface Laplacian should re-band toward 0.35-0.40.

**C5 — N=300 sentence target may not be reachable in a single 30-min session**. BLM Phase 5 used N targets with **multi-session aggregation** (ZuCo subjects across SR1-8 sessions). A single 30-min session at 1.5 s minimum dwell and ~3 s mean dwell yields a hard ceiling of **300 sentences** (15 min × 60 s / 3 s/sent = 300). If the user advances slower than 3 s mean, N < 300 and verdict drops to "Phase E partial" requiring a same-day replicate. We pre-disclose this as a likely outcome rather than a surprise.

**C6 — Phase E PASS does NOT lift F2 ceiling itself**. The substrate-architectural L1 0/16 ceiling is **structural** (per `.roadmap.n_substrate.blk.1`); Phase E binding evidence raises F1_v2 raw band toward YELLOW but F2 override (`f2_override_score: 0.12`) remains canonical (per `f1_v2_band_thresholds_2026_05_04` in roadmap). Phase E + F2 unfire are independent paths; this spec only delivers Phase E.

**C7 — Single-subject (N=1 user)**. This is a within-subject design with no between-subject replication. Population-level binding claims are out of scope. The verdict applies only to "user-this-session" and is conditional on §5 protocol compliance.

**C8 — Sentence corpus methodological-homology vs identity tradeoff**. The corpus is drawn from ZuCo SR-task transcript text only (no fixation onsets, no subject overlap), so the EEG side is **methodologically homologous** to BLM Phase 5 ZuCo analysis but uses a different subject (the user). This is intentional — full identity would require the user to be a ZuCo subject (impossible). Methodological homology lets us cross-reference T7/T8/P7/P8 ROI rationale without claiming subject-level cross-substrate alignment.

---

## §7 Analysis pipeline (offline, $0 ubu1 CPU, hexa-on-Mac)

**Inputs**: `recordings/sessions/anima_phase_e_eeg_live_<DATE>/`

- `eeg_continuous.npy` — 16 ch × T samples float32 @ 250 Hz (from collect.hexa)
- `markers.jsonl` — LSL marker stream (sentence_onset, phase_start, etc.)
- `user_attest.json` — §5 attestation
- `hardware_confirm.json` — §4 hardware confirmation

**Pipeline (sequential)**:

```
P0: validate
  hexa run anima-eeg-core/tool/_metrics/_integration_test.hexa --session=<DATE>
  → checks user_attest + hardware_confirm + ROI present + sampling_rate=250

P1: preprocess
  bandpass 1-50 Hz (zero-phase, 4-pole Butterworth)
  notch 60 Hz
  ICA artifact removal (15 components, eye-blink + EMG auto-flag via correlation with FP1/FP2 + bandpower 50-100Hz floor)
  → eeg_clean.npy

P2: epoch extract
  for each sentence_onset in markers.jsonl (phase=P3 only):
    epoch = eeg_clean[T7,T8,P7,P8, t_onset+250ms : t_onset+550ms]  # ~75 samples per channel @ 250Hz
    metadata: sentence_id, dwell_ms (sentence_advance - sentence_onset), attended (dwell ≥ 1500ms)
    discard if any: dwell<1500ms / artifact-flagged / impedance >10kΩ at session-mid check
  → epochs.npz, kept_count

P3: high-gamma coherence per ROI pair
  for each pair in [T7-T8, T7-P7, T7-P8, T8-P7, T8-P8, P7-P8]:
    coherence_30_80hz = welch-coherence on epoch concatenation (per-sentence aggregation)
    bootstrap_95ci = 1000-resample bootstrap CI
  → coherence_per_pair.json

P4: F-PHASE-E-1 verdict
  mean_coh = mean over 6 pairs
  null_dist = block-permutation (2-sec block) × 1000 reshuffle of phase labels (P1 vs P3)
  permutation_p = (count of null_dist >= mean_coh) / 1000
  PASS = mean_coh >= 0.5 AND permutation_p < 0.01 AND lower_bootstrap_ci_5pct > 0.4

P5: F-PHASE-E-2 verdict
  for each sentence_onset:
    eeg_sample_idx = nearest sample by ts_ns_monotonic
    audio_sync_idx = aux_channel onset detector (50ms 2kHz envelope)
    latency_ms = abs(eeg_sample_idx_time - lsl_marker_time)  cross-checked with audio_sync_idx
  median_latency = median(latency_ms)
  pct_within_100ms = count(latency_ms < 100) / N
  PASS = median_latency < 50 AND pct_within_100ms >= 0.95

P6: composite verdict per §2.3 gate
  emit state/anima_phase_e_eeg_live_<DATE>/verdict.json
  emit state/anima_phase_e_eeg_live_<DATE>/per_sentence_coherence.json
  emit state/anima_phase_e_eeg_live_<DATE>/null_distribution.json
```

**Output schema** (`verdict.json`):

```json
{
  "session_date": "YYYY_MM_DD",
  "user_attest_verified": true,
  "hardware_confirm_verified": true,
  "n_sentences_target": 300,
  "n_sentences_kept": 287,
  "f_phase_e_1": {"verdict": "PASS|FAIL", "mean_coh": 0.52, "permutation_p": 0.003, "bootstrap_ci_lower": 0.43},
  "f_phase_e_2": {"verdict": "PASS|FAIL", "median_latency_ms": 18, "pct_within_100ms": 0.98},
  "composite": "PHASE_E_BINDING_WITNESSED|PHASE_E_PARTIAL|F-WEAK|F-FAIL|F-ARTIFACT",
  "f1_v2_projection": {"pre": 0.408, "post_if_pass": 0.558, "f2_state": "FIRES (unchanged)"},
  "honest_c3_compliance": ["C1_window_disclosed","C2_no_laplacian_disclosed","C3_attention_caveat","C4_band_liberal_disclosed","C5_N_ceiling_disclosed","C6_f2_unchanged","C7_n1_only","C8_corpus_homology"]
}
```

**Implementation note (raw#9 + raw#37)**: pipeline runs on Mac in hexa where possible (P0 validate, P5 sync verdict are pure hexa). P1 ICA + P3 welch coherence + P4 permutation null currently require numpy/scipy; per session memory `feedback_py_to_hexa_only`, these run **on ubu1** via SSH (BrainFlow-helper-style) — Mac side never writes new .py. Helper at `state/.phase_e_analysis_helper.py` (ubu1-only, raw#37 transient declared).

---

## §8 Verdict criteria (composite, locked)

| primary outcome | criteria | downstream effect |
|---|---|---|
| **PHASE_E_BINDING_WITNESSED** | F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + N ≥ 300 | F1_v2 raw 0.408 → 0.558 (YELLOW reach per §49.5); contributes to F1_v2 RED→YELLOW promotion path; F2 ceiling unchanged; **does NOT lift `n_substrate.blk.1`** structurally — only raises F1 raw component |
| **PHASE_E_PARTIAL** | F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + 100 ≤ N < 300 | replicate same-day (≥1 second 30-min session) before classifying further; do not commit verdict until N ≥ 300 cumulative |
| **F-WEAK** (existing 5-tier) | F-PHASE-E-1 in [0.3, 0.5] band, perm p < 0.05 | RED-with-trace-binding; insufficient for path-D justification alone |
| **F-FAIL** (existing 5-tier) | F-PHASE-E-1 < 0.3 OR perm p > 0.10 | RED-binding-falsified; pivot to path (b) learned phi_extractor (per existing falsifier preregister) |
| **F-ARTIFACT** | F-PHASE-E-2 FAIL OR R-control matches real (existing R1/R2/R3 from preregister) | INVALID-protocol-revision-required; no binding claim; do NOT count toward F1_v2 |
| **F-INDETERMINATE** | none of above match | replicate before classifying; honest report |

The existing 5-tier preregister at `state/cp2_clm_phase_e_spec_2026_05_02/falsifier_5tier_preregister.json` remains canonical for the ALM/CLM-side BSE-1 Pearson 3-way analysis. **This spec extends it** with F-PHASE-E-1 and F-PHASE-E-2 as **EEG-side gating falsifiers** — both must PASS before the BSE-1 binding_strength is computed (otherwise binding_strength is computed on artifact data, not signal).

---

## §9 Phase E does NOT lift F2 ceiling — explicit anchor

Per `n_substrate.cond.1.blocker_reason`:

> F2 falsifier FIRES on ALM/CLM 둘 다 (substrate-architectural L1 ceiling 0/16) — RED 유지, YELLOW 도달은 binding evidence (Phase E) + 사용자 EEG live session prerequisite

This means YELLOW reach **requires both** Phase E binding evidence AND F2 unfire. Phase E PASS alone keeps F1_v2 RED with strong binding evidence (per §49.5 projection 0.408 → 0.558 is **the F1_v2 raw band** — F2 override score 0.12 stays). The F1_v2 banding spec (`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md`) §11 explicitly lists `f2_override_canonical: true`, so the band reading after Phase E PASS is:

- **Raw F1_v2**: 0.558 (YELLOW band [0.50, 0.75])
- **F2-override F1_v2**: 0.12 (RED band [0, 0.50])
- **Canonical band emit**: RED (per `f2_override_canonical: true`)

The user authorization in `f1_v2_band_thresholds_2026_05_04` makes this canonical. Phase E PASS narrative reads: "Binding evidence WITNESSED + raw F1_v2 reaches YELLOW; canonical band remains RED until F2 unfire (separate path)." This is the honest answer.

---

## §10 Proposed annotation block — `.roadmap.n_substrate` + `.roadmap.eeg`

These are **proposed** additive-only annotations. This BG does **NOT** mutate the roadmap files; a follow-up landed-cycle should apply them. Both blocks honor `additive_only_mutation: true`, `semantics_preserved: true`, `historical_evidence_preserved: true`.

### §10.1 `.roadmap.n_substrate` cond.1 annotation (propose)

```json
"phase_e_eeg_live_session_prep_2026_05_04": {
  "ts_utc": "2026-05-04",
  "spec_doc": "docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md",
  "spec_landed_doc": "docs/anima_phase_e_eeg_live_session_prep_landed_2026_05_04.ai.md",
  "status": "SPEC_FROZEN_AWAITING_USER_30MIN_SESSION",
  "user_gating_step": "alcohol-free 24-48h + normal sleep + caffeine 4h free + exercise 2h free + 5min stabilize (per honest_c3_alcohol_anchor)",
  "user_wall_minutes": 30,
  "cost_usd": 0,
  "falsifiers_pre_registered": ["F-PHASE-E-1 high-gamma cross-electrode coherence >= 0.5 (perm p<0.01, bootstrap CI lower>0.4)","F-PHASE-E-2 stimulus-onset sync median <50ms + 95% within 100ms"],
  "verdict_criteria_locked": "PHASE_E_BINDING_WITNESSED requires F-PHASE-E-1 PASS + F-PHASE-E-2 PASS + N>=300 sentence-aligned reading-task epochs",
  "f1_v2_raw_projection_if_pass": 0.558,
  "f1_v2_canonical_band_if_pass": "RED (f2_override_canonical=true; F2 unfire is separate path)",
  "blk_1_lift": false,
  "blk_1_partial_relief": "raises F1_v2 raw band toward YELLOW only; structural L1 0/16 ceiling unchanged",
  "honest_c3_count": 8,
  "applies_to_blocker": "n_substrate.blk.1",
  "additive_only_mutation": true,
  "semantics_preserved": true,
  "historical_evidence_preserved": true
}
```

### §10.2 `.roadmap.eeg` cond.5 + cond.7 annotation (propose)

```json
"phase_e_live_session_prep_2026_05_04": {
  "ts_utc": "2026-05-04",
  "spec_doc": "docs/anima_phase_e_eeg_live_session_prep_spec_2026_05_04.md",
  "session_protocol": "P1 eyes-closed 5min + P2 eyes-open 5min + P3 reading 15min + P4 post-rest 5min, 30min total wall + 5min stabilize prereq",
  "lsl_marker_stream": "anima_phase_e_markers (Markers, string)",
  "audio_sync_aux_channel": 17,
  "roi_channels": ["T7","T8","P7","P8"],
  "epoch_window": "250-300ms post-onset (BLM Phase 5 §2.2 homology; 250Hz Cyton+Daisy native vs 500Hz ZuCo asymmetry disclosed in C1)",
  "n_sentence_target": 300,
  "user_gating_step": "alcohol-free 24-48h + protocol checklist (state/anima_phase_e_eeg_live_<DATE>/user_attest.json)",
  "contributes_to": ["eeg.cond.5","eeg.cond.7"],
  "cross_link": "n_substrate.cond.1 (binding evidence path)",
  "additive_only_mutation": true,
  "semantics_preserved": true
}
```

---

## §11 What this spec unblocks (and what it does NOT)

### §11.1 Unblocks

- **User self-execution path**: with this spec, a 30-min EEG session is fully specified (hardware checklist + protocol + analysis + verdict criteria); the user can self-execute when ready.
- **Phase E ↔ BLM Phase 5 cross-fold-in**: T7/T8/P7/P8 ROI + 250-300ms post-onset epoch is methodologically symmetric to ZuCo SR analysis — future cross-substrate phi proxy comparison (eeg.cond.4 sample-partition phi 1순위) becomes possible without re-protocoling.
- **F1_v2 raw band promotion path**: 0.408 → 0.558 YELLOW reach is now executable (conditional on PASS); previously this was a paper projection only.

### §11.2 Does NOT unblock

- **F2 14-gate substrate-architectural L1 0/16 ceiling**: structural; needs separate path (b/c learned phi_extractor + N-22 Levin + IIT 4.0 proper phi, $1500+ separate budget).
- **Population-level binding claim**: N=1 within-subject only.
- **Phenomenal-tier witness**: Phase E PASS emits `WITNESSED_ANALOG` or `WITNESSED_FUNCTIONAL` only; phenomenal tier reservation per `docs/n_substrate_putnam_cross_link_spec_2026_05_04.md` §5.3 stays.
- **EEG hardware arrival blocker (`eeg.blk.1`)**: spec assumes user has working OpenBCI Cyton+Daisy 16ch; if hardware is unavailable, this spec can't run. The spec is **runbook-ready** but **execution-gated** on hardware presence.

---

## §12 Cost + raw invariants

- **Cost**: $0 ubu1 CPU + 30 min user wall + 5 min user prep = **$0 + 35 min user wall**.
- **raw#9**: doc-only spec (md), pipeline implementations split hexa-on-Mac / py-on-ubu1 per session memory `feedback_py_to_hexa_only`; raw#37 transient declared for ubu1 helper.
- **raw#10**: 8 honest C3 caveats embedded (§6 C1-C8).
- **raw#15**: repo-relative paths only.
- **raw#71**: F-PHASE-E-1 + F-PHASE-E-2 pre-registered with locked thresholds before measurement; existing 5-tier preregister composes.
- **raw#91**: honesty-triad — F1_v2 raw vs F2-override band split disclosed (§9); Phase E PASS ≠ ceiling lift (§11.2).

---

## §13 Next-cycle handoff

After user executes the 30-min session and the analysis pipeline emits `verdict.json`:

1. Copy session state into `state/anima_phase_e_eeg_live_<DATE>/` (already pipeline default).
2. Apply the §10.1 + §10.2 proposed annotations to `.roadmap.n_substrate` + `.roadmap.eeg` (additive-only mutation cycle).
3. If `composite == PHASE_E_BINDING_WITNESSED`: update F1_v2 raw band ledger entry; F2 ceiling and `n_substrate.blk.1` open-status both unchanged (per §9).
4. If `composite == F-WEAK | F-FAIL`: pivot to path (b) learned phi_extractor per existing 5-tier preregister.
5. If `composite == F-ARTIFACT`: revise protocol (likely sync layer) and re-spec; do NOT count session toward F1_v2.
6. The `.ai.md` landed companion (`docs/anima_phase_e_eeg_live_session_prep_landed_2026_05_04.ai.md`) carries the 1-page summary for cross-cycle handoff.

End of spec.
