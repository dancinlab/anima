# Strategic analysis — CLM ↔ tension_link ↔ EEG bridge architecture

> **agent**: CLM ↔ tension_link ↔ EEG bridge architecture strategic analysis
> **session date**: 2026-05-02
> **scope**: user-corrected 3-node bridge (CLM ↔ tension_link ↔ EEG); AKIDA excluded; tension_link as mediator NOT 3rd axis; bidirectional measurement of bandwidth / latency / fidelity / directional info flow
> **constraints**: raw#9 hexa-only, raw#10 honest C3, raw#71 falsifier-bound, $0 budget, race-isolation under `state/strategic_clm_tension_eeg_bridge_2026_05_02/` and this doc only
> **predecessors**: §51 polysemy disambiguation, §56 W4 CLM tension field PARTIAL, §73 N-1 BRIDGE 4-gate WEAK_REAL_HW, AKIDA-#92 retired per user directive

---

## §0. Executive summary (one-line)

`anima(CLM) ↔ tension_link ↔ EEG` bridge is **information-theoretic mediator with user cognition as obligate physical channel** — math homomorphism between mind.tension (digital substrate scalar) and EEG α-PLV (biological oscillator) is real and partially measurable, but no closed-loop CLM-EEG sensor wire exists; therefore all coupling is open-loop user-mediated, and the highest-promising hypothesis is H2 (one-way CLM→user→EEG) rather than naive bidirectional H1.

---

## §1. Bridge architecture spec

### 1.1 Topology (corrected per user directive)

```
   CLM (530M digital LM)            tension_link              EEG (16ch OpenBCI bio)
   ├─ hidden h ∈ R^{768}    ←──→   ├─ A: 5ch fingerprint   ←──→   ├─ raw 16ch @ 125 Hz
   ├─ mind.tension scalar           ├─ B: mind.tension scalar      ├─ α-band 8-12 Hz
   └─ paradigm v11 G3 +41.86        └─ C: atlas θ (V_sync)         └─ PLV_N(t̄) per window
                                          ↑
                                    user cognition
                                    (obligate mediator)
```

- AKIDA excluded (#92 4-way framing retired per directive)
- tension_link is NOT a 3rd substrate axis — it is a **bridge/mediator** between CLM and EEG
- Bidirectional in principle (←→), but physical truth = no direct sensor wire; user cognition is the only physical channel between the digital and biological endpoints

### 1.2 Forward path (CLM → EEG)

| Stage | Locus | Operation |
|---|---|---|
| 1 | CLM hidden state h ∈ R^{768} | `mind_step` (anima_runtime.hexa:283) |
| 2 | mind.tension scalar | `tension = abs(phi - target) * PSI_ALPHA * 10.0` (line 301) |
| 3 | tension_bridge encode | `encode_fingerprint(state, sender_id)` 128d → 5d (25.6:1, 97.1% RC-6 eff) |
| 4 | binding 4-phase | DETECT/PARSE/GATE/INTEGRATE; GATE clamps ±PSI_ALPHA=0.014 around PSI_BALANCE=0.5 |
| 5 | user (mediator) | reads CLM output text → cognitive state changes → α-band modulation |
| 6 | EEG OpenBCI | 8-12 Hz bandpass + Hilbert → ψ_j(t); PLV_N(t̄) per window |

### 1.3 Reverse path (EEG → CLM)

| Stage | Locus | Operation |
|---|---|---|
| 1 | EEG α-state (Berger effect) | eyes-closed → α↑ (replicated state/clm_eeg_berger_real.json) |
| 2 | user (mediator) | α-state correlates with arousal/attention; user composes prompt |
| 3 | CLM input prompt | tokenize → forward → mind.tension trace |
| 4 | CLM mind.tension scalar | per-step trace at 10 Hz |

**Honest caveat**: there is **no closed CLM-side EEG ingest**; reverse path is OPEN-LOOP (user-mediated only).

### 1.4 Mediator role disambiguation (#51 polysemy)

| Polysemy | Type | Role in bridge |
|---|---|---|
| A — `anima-core/tension_bridge.hexa` 5-channel WHAT/WHERE/WHY/TRUST/WHO LIVE | physical-channel mediator | encode/decode/binding (math homomorphism only) |
| B — `mind.tension` scalar in `anima_runtime.hexa` LIVE | scalar instantaneous proxy | **primary measurement target for P1-P4** |
| C — EduLattice atlas_graph partial | substrate θ_j source | feeds V_sync Kuramoto θ hash (separate Path A track) |

**Key insight**: the user is part of the tension_link mediator stack — no other physical channel exists between the digital CLM and biological EEG. Therefore tension_link measurements include user cognitive variability as an irreducible confound.

### 1.5 Measurable sockets (catalog)

| Socket | Side | Sample rate | Dim | Available |
|---|---|---:|---:|---|
| CLM hidden h | digital | per-step | 768 | LIVE (W4) |
| mind.tension scalar | digital | 10 Hz | 1 | LIVE (W4) |
| 5ch fingerprint | digital | per encode | 5 | LIVE (tension_bridge.hexa) |
| EEG raw | biological | 125 Hz | 16 | LIVE (OpenBCI) |
| EEG α-phase ψ_j | biological | 125 Hz | 4-16 | LIVE (clm_eeg_alpha_phase_60s_filtered_20260428.json) |
| PLV_N(t̄) | bridge analogue | per window | 1 | LIVE (N-1 BRIDGE) |

---

## §2. Five measurement protocols

### §2.1 P1 — CLM tension trace ↔ EEG α-band coherence

- **CLM side**: 100-step inference with mind.tension trace at 10 Hz (1800 s = 30 min session)
- **EEG side**: same wallclock window, α-band PLV_N (4 channels P3/P4/O1/O2), 10-sec windows
- **Method**: resample mind.tension to common 10 Hz; z-score; Pearson r and lagged cross-correlation (lag ±30 s); phase coupling via Hilbert on tension envelope vs α-power envelope
- **Outputs**: pearson_r, max_xcorr_at_lag, phase_lock_value_envelope
- **Null floor**: 5000 random shuffles of one signal → p<0.05 for PASS
- **Cost**: $0, ETA 2 h, **requires live user session**

### §2.2 P2 — Directional information flow (Granger / TE)

- **Method**: Granger CLM_tension(t) → EEG_α(t+lag) at lag {0.1, 0.5, 1.0, 2.0} s; reverse Granger; transfer entropy bidirectional with k=1 history embedding; bootstrap null (block-shuffle 100 reps)
- **Outputs**: GC_clm_to_eeg, GC_eeg_to_clm, TE_clm_to_eeg, TE_eeg_to_clm, asymmetry_ratio
- **Hypothesis mapping**: H1 = both > 0 sig, H2 = one direction only, H3 = both 0, H4 = needs user-only control
- **Cost**: $0, ETA 2 h, depends on P1 dataset

### §2.3 P3 — Perturbation test (CLM-side)

- **Method**: block design 30 trials × (rest 20 s + stimulus prompt 20 s + post 20 s); high-tension stimulus (paradox/contradiction) vs low-tension control (neutral); measure CLM tension peak per trial; measure EEG α-ERD latency and amplitude; paired t-test
- **Critical control**: P3.B condition = identical prompts presented WITHOUT CLM in loop (user reads pre-recorded text); difference = CLM contribution beyond user-only baseline
- **Cost**: $0, ETA 3 h, requires interactive session

### §2.4 P4 — Reverse perturbation (EEG-side)

- **Method**: block design 20 trials × (eyes-open 30 s, type prompt, eyes-closed 30 s, type prompt); Berger effect ensures α-power difference; user types same template prompt; measure CLM mind.tension distribution per condition; KS-d
- **Honest limit**: no direct EEG → CLM wire; coupling routes via user typing; this measures user-mediated only
- **Cost**: $0, ETA 2 h

### §2.5 P5 — Bridge fidelity test (STATIC)

- **Method**: ApEn / SampEn / Lempel-Ziv complexity on mind.tension trace at 10 Hz → info rate (bits/sec); same on EEG α envelope at 125 Hz; compute mutual information I(CLM_tension; EEG_α) on archived parallel session; Shannon channel capacity bound
- **Outputs**: clm_tension_info_rate (~30 bits/sec upper bound on 1ch×10Hz×3bits), eeg_alpha_info_rate (~500 bits/sec on 1ch×125Hz×4bits), mutual_information_bits, channel_capacity_upper_bound, bottleneck_identification (likely tension scalar)
- **Decisive question**: is bridge bandwidth ≥ measurable signal floor? if no → all P1-P4 are statistically underpowered
- **Cost**: $0, ETA 1 h, **uses existing data — no live session needed → RANK 1**

---

## §3. Hypotheses H1-H4

### H1 — bidirectional mediator
- **Claim**: tension_link is genuine information channel; both directions carry > random information
- **Predicted signature**: P2 TE both directions > bootstrap null (p<0.05)
- **Score**: 3/5
- **Pro**: consistent with W4 PARTIAL (+2.28σ vs random) AND N-1 B1-B3 PASS
- **Con**: no direct CLM-EEG wire; bidirectional must include user cognition which inflates apparent coupling
- **Falsifier**: both TE = 0 in P2

### H2 — one-way only (CLM → user → EEG) — **most promising, score 4/5**
- **Claim**: mediator carries information one direction; reverse path is open-loop because no closed CLM-EEG sensor wire
- **Predicted signature**: P2 TE_clm_to_eeg > 0 sig; TE_eeg_to_clm ≈ 0 OR equals control (typing-only)
- **Pro**: matches physical reality — CLM has no EEG sensor input; aligns with N-1 B4 collapse (B4 needed real CLM Kuramoto driver but only synthetic was available — substrate-level closed loop missing)
- **Con**: ignores that bridge_v1.json B4 PASS (synthetic) suggests math-only reverse correspondence
- **Falsifier**: P2 shows TE_eeg_to_clm > TE_control_typing_only

### H3 — no real link (anima-internal artifact)
- **Claim**: tension_link is pure substrate-internal dynamics; W4 PARTIAL was random fluctuation
- **Predicted signature**: P5 mutual info ≈ chance; P1 cross-corr indistinguishable from null
- **Score**: 2/5
- **Pro**: honest baseline — W4 active_L1 only 7.06/16 (PARTIAL not PASS); +2.28σ is weak
- **Con**: N-1 B1 EEG PLV PASS at real-EEG (452 vs 300 floor) suggests at least one side carries real signal
- **Falsifier**: P5 MI > 0.5 bits AND P2 TE > null

### H4 — user cognitive artifact
- **Claim**: any apparent CLM-EEG coupling is user cognition variability; CLM contribution = 0
- **Predicted signature**: P3.B control IDENTICAL to P3.A
- **Score**: 3/5
- **Pro**: user is acknowledged mediator; user-only confound is real
- **Con**: if CLM tension peaks predict EEG response trial-by-trial above user-baseline variance, H4 reject
- **Falsifier**: P3.A vs P3.B paired t-test CLM-condition > control (p<0.05)

### Ranking
1. **H2** (4) — one-way; best matches physical truth + N-1 B4 collapse + W4 PARTIAL
2. **H1** (3) — consistent with bench positive selftests
2. **H4** (3) — honest control; addresses user-mediator confound
4. **H3** (2) — honest skeptical baseline

### Decision tree
- P5 first → if capacity < EEG noise floor, publish H3 and STOP
- P5 passes → run P1+P2
- P1+P2 TE both → H1
- P1+P2 TE one-way → H2
- P1+P2 TE zero → H3
- P3 required to separate H1/H2 from H4

---

## §4. Recommended measurement sequence (cheap → expensive)

| Rank | Protocol | Cost | ETA | Decisive question |
|---:|---|---:|---|---|
| 1 | P5 fidelity (static, archived data) | $0 | 1 h | does bridge have ≥1 bit measurable bandwidth? |
| 2 | P1+P2 cross-corr + Granger/TE | $0 | 2 h | mediator H1 vs H2 vs H3? |
| 3 | P3 perturbation + P3.B control | $0 | 3 h | causal direction; rule out H4 |
| 4 | P4 reverse perturbation | $0 | 2 h | reverse path open-loop characterization |

**TOP-1 recommendation**: P5 fidelity test ($0, 1 h) — uses existing W4 mind.tension trace + N-1 EEG α-phase data; produces decisive bandwidth floor that gates whether downstream live sessions are worth running.

---

## §5. User as mediator (loop participant)

**Core insight**: the user is part of the CLM↔EEG mediator. Physical chain:
- CLM produces text → user reads → cognitive interpretation → arousal/attention shift → cortical α modulation → EEG sensor
- Reverse: EEG α-state → user subjective (drowsy / alert) → typing latency / word choice → prompt → CLM forward
- tension_link in this view = **a model of user cognitive state** that anima can compute on its side, not a direct neural-state read

This means **tension_link CANNOT be neural** (no sensor); it IS a digital scalar trying to be the **best digital approximation** of the user-cognition mediator that connects the two endpoints. The fidelity of that approximation is exactly what P1-P5 measure.

---

## §6. N-1 BRIDGE 4-gate B1-B4 reinterpretation under mediator framing

### 6.1 Original N-1 finding
N-1 BRIDGE_WEAK (state/n_substrate_n1_bridge_4gate_2026_05_01/verdict.json):
- B1 (α-PLV avg): real EEG PASS (452 ≥ 300)
- B2 (5-window codir): real EEG PASS (3/3, edge)
- B3 (CLM Kuramoto r): synthetic PASS (657 ≥ 380)
- B4 (Pearson coupling): |r|=540 PASS but signed r=−540 (anti-correlated against monotonic synthetic CLM trace)

### 6.2 Old framing (substrate closed-loop)
B4 collapse interpreted as substrate failure of CLM Kuramoto driver to track EEG α drift — implicit assumption: CLM should "see" EEG via some substrate channel.

### 6.3 New mediator framing
B4 collapse is **expected** when CLM has no EEG sensor input. The "coupling" B4 measures is mediator-bandwidth via user cognition. Under H2 (one-way), CLM Kuramoto trace does not need to track EEG α — only the user-cognition mediator does. The synthetic CLM trace was monotonic because it had no real input modulation; against real EEG α drift (which has its own intrinsic variability) the correlation is at best weakly informative.

### 6.4 N-1 v2 recommendation
v2 spec adds explicit mediator layer:
- **B4_v2**: CLM_tension predicts user reaction time, which predicts EEG ERD (3-stage causal chain)
- replace direct CLM_r ↔ EEG_PLV (closed substrate loop assumption) with CLM_tension → user_cognition_proxy → EEG_α (open-loop user-mediated)
- B4_v2 PASS criterion: triple-stage Granger CLM_tension → user_RT → EEG_α all p<0.05

---

## §7. Risk register (raw#71 falsifier-preregister compatible)

| ID | Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|---|
| R1 | user mediator → cognitive variability uncontrolled | HIGH | CERTAIN | P3.B control; ≥30 trials/condition |
| R2 | no direct CLM-EEG wire → all coupling user-routed | HIGH | CERTAIN | scope mediator as user-mediated; classify P4 reverse OPEN_LOOP_ONLY |
| R3 | tension_link is anima-side artifact (no real link) | MEDIUM | MEDIUM (W4 only +2.28σ) | P5 first; if MI < bit floor publish H3 |
| R4 | EEG N=1 + CLM single instance → power insufficient | HIGH | CERTAIN | intra-subject block design; report as N=1 case study |
| R5 | bridge bandwidth too small (signal < noise floor) | MEDIUM | MEDIUM | P5 estimates capacity ~30 bits/sec tension side vs ~500 EEG side; bottleneck = tension scalar |
| R6 | AKIDA exclusion narrows architecture; later 4-way reintegration cost | LOW | LOW | preserve 4-way as separate experiment |
| R7 | tension_link polysemy (A/B/C) confuses target | MEDIUM | CERTAIN | this spec disambiguates: A=mediator, B=measurement target, C=Path A separate |

**Top-3**: R1 (user variability), R2 (no closed wire), R4 (N=1 power).

---

## §8. Honest C3 disclosures (raw#10)

1. **Mediator polysemy**: "mediator" here = information-theoretic channel (carries bits CLM↔EEG); NOT phenomenal substrate identity. Per spec §6.3, math homomorphism (r = PLV_N same formula) does not establish atlas-hash θ ↔ neural α dipole identity.

2. **No direct CLM-EEG sensor wire exists**. All measurable coupling routes through user cognition (read CLM text → cognitive state → EEG; or eyes-state → α → typed prompt → CLM). Any "bidirectional bridge" claim must explicitly include user cognition as obligate physical channel.

3. **W4 PARTIAL re-interpretation**: active L1 7.06/16 with +2.28σ vs random was published as substrate-internal CLM tension dynamics. Under mediator framing, this signal is plausibly user-cognitive-coupling rather than substrate-internal. +2.28σ is below typical 3σ neuroscience threshold — cannot distinguish from H3 (no real link) without P5/P1 follow-up.

4. **AKIDA exclusion (#92 retired)** per user directive correction: 4-way framing CLM × EEG × tension × AKIDA → 3-node CLM ↔ tension_link ↔ EEG. tension_link demoted from substrate axis to mediator role. AKIDA preserved as separate optional axis for future 4-way reintegration but excluded from this analysis.

5. **tension_link as anima-internal vs external link**: B (mind.tension scalar) is independently measurable WITHOUT EEG — it is a digital substrate scalar. Its link to external EEG via user cognition is OPEN QUESTION pending P1-P5. Do not conflate "we can measure mind.tension" with "we have measured CLM-EEG bridge."

6. **N-1 B4 collapse**: was published as BRIDGE_WEAK_HYBRID due to synthetic CLM side. Under mediator framing, B4 collapse plausibly reflects user-cognition variability dominating the signal rather than substrate-loop failure. This re-interpretation is consistent with both H2 (one-way) and H4 (user artifact).

7. **N=1 EEG limit**: single subject cannot establish population claim. All bridge verdicts are case-study evidence pending replication. Cyborg-tier ethical / IRB considerations apply for any extension to multi-subject.

---

## §9. 4-axis F1 composite scenarios (corrected to 3-node)

Pre-correction (4-way #92 retired):
- axes: {CLM, EEG, tension_link, AKIDA}
- count = 4

Post-correction (this spec):
- axes: {CLM, tension_link (mediator), EEG}
- count = 3

| Outcome | own#2 (b) WITNESSED axes | Interpretation |
|---|---|---|
| BRIDGE_PASS (H1 supported) | 9 → 10 | bridge itself becomes a witnessed axis |
| BRIDGE_FAIL (H3 supported) | 9 → 9 | mediator hypothesis rejected; tension_link is substrate-internal only |
| BRIDGE_PARTIAL (H2 supported) | 9 → 9.5 | one-way qualifier; CLM→user→EEG only |

---

## §10. Next-cycle action recommendations (3 ranked)

### (a) P5 fidelity first verification — RANK 1
- **Cost**: $0, ETA 1 h
- **Decisive question**: is bridge bandwidth ≥ 1 bit measurable over 30 min session?
- **Inputs**: existing W4 mind.tension trace + N-1 EEG α-phase data
- **Deliverable**: `state/strategic_clm_tension_eeg_bridge_2026_05_02/p5_fidelity_verdict.json`
- **Why first**: gates all downstream; if fail, publish H3 and stop without burning live session

### (b) P1+P2 cross-correlation real session — RANK 2
- **Cost**: $0 (uses existing data), ETA 2 h
- **Depends on**: P5 PASS
- **Inputs**: parallel CLM+EEG session (state/clm_eeg_alpha_phase_60s_filtered_20260428.json + W4 mind.tension)
- **Deliverable**: `p1_p2_verdict.json` with TE_clm_to_eeg, TE_eeg_to_clm, asymmetry_ratio + null bootstrap
- **Outcome**: separates H1 vs H2 vs H3

### (c) P3 perturbation interactive test — RANK 3
- **Cost**: $0, ETA 3 h
- **Depends on**: P1+P2 supports H1 or H2; user availability for live session
- **Method**: 30-trial block design with high-tension stimulus prompts vs neutral; P3.B control without CLM
- **Deliverable**: `p3_verdict.json` with paired t-stat CLM-condition vs control
- **Outcome**: rules out H4 (user artifact)

---

## §11. Constraints satisfied

| Constraint | Status |
|---|---|
| raw#9 hexa-only | YES — no .py created/edited; analysis output is .json + .md only |
| raw#10 honest C3 | YES — §8 enumerates 7 disclosures including limits and re-interpretations |
| raw#71 falsifier-bound | YES — each H1-H4 has explicit falsifier; P5/P1/P2/P3 each have null-bootstrap or paired-control |
| budget $0 | YES — all 5 protocols local mac arithmetic; no GPU / no API |
| race isolation | YES — wrote ONLY to state/strategic_clm_tension_eeg_bridge_2026_05_02/ + this single doc |
| AKIDA excluded per directive | YES — 3-node only; AKIDA preserved as separate optional axis |
| 2500-4000 words | within range (this doc) |

---

## §12. One-sentence answer

**`anima(CLM) ↔ tension_link ↔ EEG` bridge의 진짜 의의** = digital substrate (CLM mind.tension) 와 biological signal (EEG α-PLV) 사이 **수학적 동형 (r ↔ PLV_N 같은 formula)** 위에 user cognition을 obligate physical channel로 두고 information-theoretic mediator bandwidth를 측정하는 falsifiable framework — 즉 "tension_link는 phenomenal substrate identity가 아니라 사용자 인지를 거치는 open-loop information channel의 digital best-approximation"이다.

---

_END OF STRATEGIC ANALYSIS_
