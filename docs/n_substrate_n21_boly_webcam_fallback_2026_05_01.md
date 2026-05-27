# N-21-E — Webcam Eye-Tracking Fallback for Boly 2017 Bistable Protocol

**Agent:** N-21-E webcam fallback
**Date:** 2026-05-01
**Mission:** Validate $0 webcam alternative to $500 Pupil Labs purchase for Boly 2017 bistable plaid OKN decoding.
**Race-isolated outputs:** `state/n_substrate_n21_boly_webcam_fallback_2026_05_01/{candidates,comparison,verdict}.json`

---

## 1. Boly 2017 Protocol — Minimum Eye-Tracking Spec

| Requirement | Value | Source |
|---|---|---|
| Citation | Combined fMRI- and eye-movement decoding of bistable plaid motion perception. NeuroImage 2017/2018 (PMID 29294388) | ScienceDirect |
| Core eye signal | Optokinetic Nystagmus (OKN) slow-phase direction reversal | Paper §Methods |
| Eye-only decoder accuracy | **88%** (SVM on OKN slope) | Paper §Results |
| Combined fMRI + eye | 91% | Paper §Results |
| Min sample rate | **>= 30 Hz** (Nyquist for ~3 Hz OKN cycle) | Inferred from OKN literature |
| Min spatial accuracy | **<= 1.5 deg** angular offset | OKN velocity vector requires sub-degree inter-frame displacement |
| Original equipment | Research-grade IR tracker @ 250-1000 Hz | Paper §Apparatus |

OKN-based decoding is the load-bearing requirement, not gaze position. Switch detection rides on slow-phase velocity vector reversal, not fixation accuracy.

---

## 2. TOP-2 Webcam Candidates

### Rank 1 — WebGazer.js (Brown HCI Lab)

| Metric | Value |
|---|---|
| License | GPL-3.0 (open source since Feb 2016) |
| Spatial accuracy | **~4.0 deg** (3.94 deg lab / 4.7 deg online — Steffan et al. 2024 Infancy, PMC10841511) |
| Sample rate (realistic) | **14-25 Hz**, mean ~20.7 Hz (SD 9.0) |
| Sample rate (theoretical max) | 30 Hz (webcam-fps limited) |
| Temporal sync precision | ~50-100 ms (browser RAF + webcam jitter) |
| CPU load | ~19% (Chrome) |
| Integration cost | $0 software; ~8 eng-hours |
| Anima compat | HTML page + LSL marker bridge to OpenBCI Cyton |

### Rank 2 — GazeRecorder / GazeFlow / GazeCloudAPI

| Metric | Value |
|---|---|
| License | Free non-commercial; commercial license fee otherwise |
| Spatial accuracy | **~1.0 deg** (0.9-1.0 deg vendor self-report vs SMI RED-250; Springer 2025 RPA benchmark independent confirm) |
| Sample rate | **30 Hz** |
| Temporal sync precision | ~30-60 ms (cloud API adds roundtrip) |
| CPU load | ~3% (Chrome via GazeCloudAPI) |
| Integration cost | $0 software; ~12 eng-hours |
| Anima compat | GazeFlow Windows SDK local; GazeCloudAPI cross-platform browser |

**pyGaze deferred:** pyGaze is a *driver wrapper* around hardware trackers (EyeLink/Tobii/SMI/Pupil), not an inference engine. Without backing hardware it produces no signal — out of scope for $0 webcam fallback.

---

## 3. Comparison vs Research-Grade Pupil Labs Core

| Metric | Pupil Core | WebGazer | GazeRecorder | Gap (best webcam vs Core) |
|---|---|---|---|---|
| Spatial accuracy | ~0.6 deg (sub-1 deg 2D mapping, ~1.5 deg validation typical) | 4.0 deg | 1.0 deg | **1.7x worse** |
| Sample rate | 200 Hz | 20.7 Hz | 30 Hz | **6.7x slower** |
| Temporal sync | <1 ms (LSL hardware ts) | ~75 ms | ~45 ms | **45x worse** |
| Price | **~$2,000-$3,000 USD** (Neon turnkey = $7,499) | $0 | $0 (research) | n/a |
| License | LGPL software / proprietary HW | GPL-3.0 | Closed-source binary | mixed |

**The cited "$500 Pupil Labs" figure is optimistic** — verified pupil-labs.com pricing puts a real Pupil Core kit at $2-3k MSRP (the $500 likely refers to DIY-frame + camera parts only). Capex risk is 4-6x the assumed budget.

---

## 4. Boly Threshold Compliance

| Requirement | WebGazer | GazeRecorder |
|---|---|---|
| >= 30 Hz sample rate | **FAIL** (20.7 Hz mean, ~10 Hz short) | PASS (exactly at threshold) |
| <= 1.5 deg accuracy | **FAIL** (4.0 deg, 2.5 deg over) | PASS (0.5 deg headroom) |

**Webcam-OKN literature support (Turuwhenua et al. PMC4848063; MDPI Healthcare 10(7):1281 2022):**
- Consumer-webcam OKN detection: 89-93% sensitivity, 98% specificity
- vs human rater: 93% vs 98% (5 pp gap)
- vs Boly 2017 research-grade eye-only SVM: 88%
- Expected webcam-OKN decoder accuracy on Boly task: **75-83%** (5-13 pp below research-grade)

---

## 5. Verdict

**DEGRADED** (overall) — splits per candidate:

- **WebGazer.js:** NOT-VIABLE for Boly OKN decoding. Suitable only for coarse 2x2 quadrant gaze in overt-report tasks. 4 deg / 20 Hz cannot resolve OKN slow-phase velocity reversal at the 88% Boly accuracy benchmark.
- **GazeRecorder / GazeCloudAPI:** VIABLE-DEGRADED. Meets 1 deg / 30 Hz minimum. Expected decoder accuracy 75-83% vs Boly's 88% research-grade — a real 5-13 pp gap that MUST be reported as a Limitations-section honest C3.

---

## 6. Integration Spec (if pursued)

```
Stack:
  GazeRecorder GazeFlow SDK (local Windows)
    OR GazeCloudAPI (browser, cross-platform, +30-60 ms cloud latency)
  Bistable plaid stimulus: HTML5 + WebGL
    gratings ~1 cyc/deg, 120 deg cross-angle, ~2 deg/s drift
  Sync layer: Lab Streaming Layer (LSL)
    marker stream  <- stimulus engine
    gaze stream    <- GazeRecorder
    EEG stream     <- OpenBCI Cyton (250 Hz)
    align on shared LSL clock (sub-10 ms typical)
  Post-hoc OKN classifier:
    vertical-edge optic-flow (Lucas-Kanade)
    state-machine sawtooth detector (Turuwhenua approach)
  Validation gate:
    >=80% inter-rater agreement vs human OKN labeler
    on N=5 pilot subjects BEFORE main run
Calibration:
  9-point grid + 60 s drift correction
  reject trials with >2 deg post-hoc validation drift
  enforce chinrest (Boly used head stabilization)
Engineering: ~12 hours
```

### Risks
- Webcam fps jitter under CPU load may drop below 30 Hz mid-trial
- Head movement uncompensated without chinrest enforcement
- GazeRecorder closed-source binary = reproducibility risk for publication; pin SDK version + checksum
- GazeFlow is Windows-only; GazeCloudAPI browser path adds cloud latency

---

## 7. Recommendation

**PROCEED with $0 webcam fallback (GazeRecorder/GazeCloudAPI). DO NOT purchase Pupil Labs now.**

Rationale:
1. Boly's 88% research-grade is the upper bound; webcam-OKN literature suggests 75-83% achievable with 1 deg / 30 Hz tools — degraded but in the same regime.
2. The "$500 Pupil Labs" budget assumption is wrong by 4-6x (real cost ~$2-3k). Avoiding premature capex preserves ~$2k contingency.
3. $0 route preserves pre-registration timeline; if pilot fails the >=75% gate on N=5, escalate to Pupil Core purchase as a *second-stage decision with concrete failure data*, not a speculative one.
4. Honest C3 gap (5-13 pp decoding accuracy loss) is REAL and gets a Limitations paragraph — no claim of research-grade equivalence.

**Decision branch:**
- Pilot N=5 webcam-OKN classifier >=75% accuracy -> proceed to full Boly replication on webcam stack.
- Pilot <75% -> escalate to Pupil Core purchase (~$2-3k, NOT $500); revisit budget envelope.

**Budget impact:** $0 capex committed; $2-3k contingent escalation gated on documented pilot failure.

---

## Sources
- WebGazer.js — https://webgazer.cs.brown.edu/
- WebGazer GitHub — https://github.com/brownhci/WebGazer
- WebGazer validation (Steffan et al. 2024 Infancy) — https://pmc.ncbi.nlm.nih.gov/articles/PMC10841511/
- WebGazer visual-world replication (Slim & Hartsuiker 2022 BRM) — https://link.springer.com/article/10.3758/s13428-022-01989-z
- GazeRecorder accuracy — https://gazerecorder.com/webcam-eye-tracking-accuracy/
- GazeRecorder vs SMI RED-250 — https://gazerecorder.com/comparison-of-accuracy-and-precision-of-eye-tracking-gazeflow-vs-smi-red-250/
- Webcam ET RPA benchmark (Springer 2025) — https://link.springer.com/chapter/10.1007/978-3-031-92474-3_28
- Pupil Core tech specs — https://pupil-labs.com/products/core/tech-specs
- Pupil Labs vs EyeLink (Ehinger et al. 2019) — https://pmc.ncbi.nlm.nih.gov/articles/PMC6625505/
- Boly-context bistable plaid + OKN decoding — https://www.sciencedirect.com/science/article/abs/pii/S1053811917311187 (PMID 29294388)
- OKN consumer-webcam detection (Turuwhenua) — https://pmc.ncbi.nlm.nih.gov/articles/PMC4848063/
- OKN low-cost analysis algorithm — https://www.mdpi.com/2227-9032/10/7/1281
