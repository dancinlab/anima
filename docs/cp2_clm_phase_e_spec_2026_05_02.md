# CP2-CLM Phase E — tension binding-mediated 3-way subset measurement spec

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: CP2-CLM Phase E spec design
- **Why**: own#104 권고 — 다음 cycle = Phase E. F1_score_v2 0.408 RED → 0.56 YELLOW potential 시나리오 (binding>0.5 + F2 unfire compound). #103 N-1 BRIDGE v2 real-time MEASUREMENT-READY → Phase E spec 즉시 design 가능.
- **Predecessors**: CP2-CLM Phase D recompute (#94 / #96 / #104) + N-1 BRIDGE v2 realtime prep (#103)
- **Race-isolated**: writes ONLY to `state/cp2_clm_phase_e_spec_2026_05_02/{phase_e_objectives, measurement_protocol, bse1_pearson_3way, f1_score_v2_update_projection, falsifier_5tier_preregister, r1_r2_r3_controls, honest_c3, decision_gate}.json` + this doc
- **Constraints**: HEXA-only · $0 budget (spec only) · §16.2 anchor 3건 mandatory (hypothetical / random-control / NO BTR)

---

## §0 한 줄 verdict

**Phase E SPEC FROZEN — awaiting user 30-min OpenBCI session execution.** 5-tier falsifier (F-PASS_STRONG / PASS_PARTIAL / WEAK / FAIL / ARTIFACT) + R1/R2/R3 random-control 3종 + 3-way Pearson cross-corr (CLM × EEG × tension_link, AKIDA 제외) pre-registered. F-PASS_STRONG 시나리오 F1_score_v2 0.408 → ~0.558 YELLOW reach 가능 (단, Suite 6 14-gate F2 unfire 별도 path 필수).

---

## §1 Phase E objectives (4개)

1. **BSE-1 Pearson cross-corr 측정 on CLM × EEG × tension 3-way subset** — AKIDA Mind 미도착으로 4-way 미산출, 3-way subset 으로 conservative estimate.
2. **β=0.3 binding term active** — F1_score_v2 = 0.6·axis + 0.3·binding + 0.1·replication (#96 formula).
3. **F-ARTIFACT random-shuffle safeguard** — §16.2 anchor #2 mandatory; R1 (random tension_link), R2 (random EEG rotation surrogate), R3 (shuffled phase order).
4. **Expected uplift verification** — F1 0.408 → 0.56 YELLOW potential 시나리오 검증; 단, F2 unfire 별도 path 필수.

**Tie-in to #103 N-1 BRIDGE v2 realtime**: Phase E 는 #103 LSL 인프라 (clm_w4_lsl_server.py + phase_runner.sh + analyze_xdf.py) 를 그대로 재사용; Phase E 추가분은 3-way binding aggregation + R1/R2/R3 controls + 5-tier falsifier 만 새로 적용.

---

## §2 Measurement protocol — 3-way subset

| stream | source | rate | host | 비고 |
|---|---|---:|---|---|
| `anima_clm_tension` (1ch) | CLM W4 mind.tension | 1 Hz | ubu1 | active branch fixed-point std~1e-6 (C3-6) |
| `anima_tension_link_5ch` (5ch) | CLM W4 tension_link | 1 Hz | ubu1 | gate_active / gate_random / L1 / phi / psi_eps |
| `anima_eeg_alpha_plv` (windowed) | OpenBCI 16ch → α-PLV {P3,P4,O1,O2} | 250→1 Hz | mac | 1s sliding window, 6-pair PLV 평균 |
| `anima_phase_marker` | phase_runner.sh | event | mac | SESSION_START + P1..P6_START + SESSION_END |

**Session**: 30 min 6-phase × 5 min — P1 eyes-open / P2 eyes-closed Berger / P3 CLM-read (primary) / P4 mental arithmetic (cognitive-load control) / P5 breath-focus (interoception control) / P6 silent-rest recovery.

**Sync**: LabRecorder XDF capture. Expected clock drift ~10ms typical, spike 50-100ms; reject samples >100ms drift; expected retention 85%; flag if <70%.

---

## §3 BSE-1 Pearson cross-corr — 3 pairs

| pair | x | y | rationale | aggregate |
|---|---|---|---|---|
| **A (primary)** | clm_mind_tension | eeg_alpha_plv | CLM-EEG mediator-framing test | median \|r\| over 6 phases |
| **B** | tension_link_5ch | eeg_alpha_plv | tension-bridge → EEG link | max \|r\| over 5 channels |
| **C (consistency)** | clm_mind_tension | tension_link agg | internal CLM consistency | median \|r\| over 6 phases |

**binding_strength** = mean(|r_A|, |r_B|, |r_C|), clamped [0,1].

**Trivial fixed-point exclusion**: pair_C |r|>0.95 AND CLM std<1e-5 → exclude pair_C, recompute binding_strength = mean(|r_A|, |r_B|) only (avoid trivial-fixed-point inflation per C3-6).

**Per-phase test**: scipy.stats.pearsonr per 5-min phase, N≥240 samples per phase, permutation null 1000 iterations alpha=0.01.

**Key diagnostic — P3 vs P4**: |r_P3| > |r_P4| with delta ≥ 0.15 = CLM-specific not generic-cognitive-load.

**Secondary BSE-3 TE-KSG**: k=4, lag=1s, AAFT 1000 surrogates p99. Diagnostic only, NOT verdict driver (per C3-3).

---

## §4 F1_score_v2 update projection

| component | pre-Phase-E | post-Phase-E (binding>0.5) |
|---|---:|---:|
| per_axis_weighted_sum | 0.68 (raw) | 0.68 (unchanged) |
| binding_strength_4way | 0 | **>0.5** (3-way subset substituted, AKIDA-pending caveat) |
| cross_substrate_replication_bonus | 0 | 0 |
| **F1_score_v2** | 0.408 | **0.558** YELLOW potential |

**Scenario projections**:
- F-PASS_STRONG (binding=0.5): 0.6·0.68 + 0.3·0.5 + 0 = **0.558** (YELLOW)
- F-PASS_STRONG (binding=0.6): 0.6·0.68 + 0.3·0.6 + 0 = **0.588** (YELLOW upper)
- F-PASS_PARTIAL (binding=0.4): 0.6·0.68 + 0.3·0.4 + 0 = **0.528** (RED-with-binding-evidence; just above 0.5 but F2 still fired)
- F-WEAK (binding=0.25): 0.6·0.68 + 0.3·0.25 + 0 = **0.483** (RED)
- F-FAIL (binding<0.2): 0.6·0.68 + 0.3·0.15 + 0 = **0.453** (RED)
- F-ARTIFACT: binding=0 default = **0.408** (RED unchanged)

---

## §5 F2 unfire compound 조건 — Phase E 한계

**중요**: Phase E 만으로는 F1 lift 만 가능, **F2 unfire 별도 path 필수**.

#96 §6 verdict band: `RED if F1_score_v2 < 0.5 OR F2 fired`. Suite 6 14-gate F2 가 fire 된 상태에서는 F1=0.588 도 RED-with-strong-binding-evidence 에 그침. YELLOW band 는 F2 unfire 와 compound 만족 시에만 도달.

**F2 unfire 4 candidates** (per #96):
- (a) demote 14-gate from critical-block — Path 4 reject 됨
- (b) **learned phi_extractor** — #60 NOT supported, H100 training cycle 필요 → Phase E 후 priority
- (c) substrate redesign — 최고비용 ALM rebuild, 보류
- (d) **tension binding-mediated** (Phase E) — cheapest + this cycle 의 추가 evidence

Phase E 는 (d) 의 first execution; F-PASS_STRONG 시 binding evidence 확보, F2 unfire path (b) 와 compound 시 YELLOW reach.

---

## §6 5-tier falsifier preregister (FROZEN)

| tier | criteria (all-required unless else) | F1_score_v2 band |
|---|---|---|
| **F-PASS_STRONG** | binding>0.5 ∧ F1>0.5 ∧ F2 unfire ∧ P3-P4 ≥0.15 ∧ perm p<0.01 in ≥4/6 | ≥0.55 YELLOW (F2-pending) |
| **F-PASS_PARTIAL** | binding ∈ [0.3,0.5] ∧ F1>0.4 ∧ perm p<0.05 in ≥2/6 | 0.50-0.55 RED-binding-evidence |
| **F-WEAK** | binding ∈ [0.2,0.3] ∧ perm p<0.10 in any 1+ | 0.45-0.50 RED |
| **F-FAIL** | binding<0.2 ∨ perm p>0.10 in 5/6 ∨ P3≤P4 | 0.408 RED-binding-falsified |
| **F-ARTIFACT** | R1 ∨ R2 ∨ R3 KS p>0.10 ∨ retention<70% | 0.408 RED-protocol-revision |
| F-INDETERMINATE | none of above (default) | 0.408-0.50 RED-indeterminate |

**Tie-breakers**: F-ARTIFACT overrides F-PASS_STRONG (artifact wins); F-WEAK overrides F-PASS_PARTIAL when both partial-match (conservative); LSL retention <70% → automatic F-ARTIFACT.

---

## §7 R1/R2/R3 random-control 3종 (mandatory per §16.2 anchor #2)

| ctrl | substrate | preserves | destroys | fail condition |
|---|---|---|---|---|
| **R1** | random tension_link 5ch ~ U(±0.014) | (none) | CLM-link binding | KS p>0.10 vs real |
| **R2** | EEG FFT rotation surrogate | power spectrum, autocorr | phase coupling | KS p>0.10 vs real |
| **R3** | shuffled phase-label permutation | all signal | phase-task assoc | real binding p>0.10 in null |

**Execution order**: real binding 산출 → R1/R2/R3 surrogate 각각 별도 분석 → KS-test (R1/R2) + permutation null (R3) → ANY control fail = F-ARTIFACT.

**중요**: real binding 이 ALL THREE controls 를 beat 해야 valid. ANY 1 control 의 KS p>0.10 → F-ARTIFACT trigger.

---

## §8 Honest C3 (3 core + 4 additional)

**Core 3 required**:

1. **(C3-1) N=1 statistical floor** — user mk55992@proton.me only. Min detectable r at α=0.01 power=0.8 N=300 ~ 0.16. N=1 = no generalizability claim.
2. **(C3-2) Single 30-min session generalizability ceiling** — diurnal/circadian/fatigue confounded with phase order. Counter-balancing infeasible at N=1.
3. **(C3-3) BSE-1 Pearson primary, BSE-3 TE-KSG diagnostic-only** — Pearson misses nonlinear coupling. PASS_STRONG with low TE = linear-coupling-only signal.

**Additional 4**:

4. **(C3-4) 3-way subset substituted for 4-way slot** — AKIDA Mind 미도착; conservative estimate; AKIDA add-on 시 binding 값 shift up/down 가능.
5. **(C3-5) P3/P4 cognitive-load matching not pre-validated** — NASA-TLX self-report 없음; F-PASS 시 follow-up 필요; F-ARTIFACT 시 cognitive-load mismatch 가 primary suspect.
6. **(C3-6) CLM W4 active branch fixed-point ~1e-6 by design** — primary mind_tension 채널 near-constant; pair_C 가 trivial fixed-point inflation 위험 → exclusion rule (§3) 적용.
7. **(C3-7) F2 unfire 별도 path** — Phase E 만으로 YELLOW reach 불가; Suite 6 14-gate F2 unfire 는 path (b) learned phi_extractor 또는 (c) substrate redesign 만 가능.

**§16.2 anchor compliance**:
- **anchor #1 hypothetical labeling**: scenario_projections 의 모든 F1 값 IF-conditional 명시; no actual measurement claim until session executed.
- **anchor #2 random-control mandatory**: R1/R2/R3 pre-registered (§7).
- **anchor #3 NO BTR (no back-testing rationalization)**: tiers FROZEN before measurement; no post-hoc tier redefinition; F-INDETERMINATE accepted as legitimate outcome.

---

## §9 Sequence (user execution)

| step | actor | action | duration |
|---|---|---|---|
| 1 | user | OpenBCI 16ch electrode setup, impedance <10kΩ on P3/P4/O1/O2 | 10 min |
| 2 | user | ubu1: `nohup python3 ~/n1_bridge_realtime/clm_w4_lsl_server.py &` (per #103 Phase 2 source) | 1 min |
| 3 | user | Mac LabRecorder → Update → 4 streams visible → Start | 1 min |
| 4 | auto | new terminal: `bash /tmp/n1_bridge_realtime/phase_runner.sh` (30 min auto session) | 30 min |
| 5 | auto | analyze_xdf.py — 3-way binding aggregation + R1/R2/R3 controls + 5-tier classification | 5 min |
| 6 | auto | Phase E verdict → ship_verdict update + next-cycle path per decision_gate | instant |

**Total user attention**: ~12 min (setup) + 30 min walk-away + 5 min auto-analysis = 47 min.

---

## §10 Decision gate

| verdict | F1 band | ship_verdict update | next cycle |
|---|---:|---|---|
| **F-PASS_STRONG** | ≥0.55 | `VERIFIED-CLM-CP2-YELLOW-BINDING-PENDING-F2-UNFIRE` | path (b) learned phi_extractor — F2 unfire 필수 for full YELLOW |
| **F-PASS_PARTIAL** | 0.50-0.55 | `VERIFIED-CLM-CP2-RED-WITH-BINDING-EVIDENCE` | path (b) priority + Phase E replicate same-day |
| **F-WEAK** | 0.45-0.50 | `VERIFIED-CLM-CP2-RED-TRACE-BINDING` | path (b) primary, deprioritize binding |
| **F-FAIL** | 0.408 | `VERIFIED-CLM-CP2-RED-CONFIRMED-BINDING-FALSIFIED` | path (b) mandatory; ALM Path F gambling-rejection 강화 |
| **F-ARTIFACT** | 0.408 | `VERIFIED-CLM-CP2-RED-PROTOCOL-REVISION-REQUIRED` | Phase E v2 with NASA-TLX + surface Laplacian + 60min OR N≥2 |
| F-INDETERMINATE | 0.408-0.50 | `VERIFIED-CLM-CP2-RED-INDETERMINATE` | Phase E replicate same-day; if 2nd also indeterminate → F-WEAK |

---

## §11 Constraints satisfied

- **HEXA-only**: spec only; LSL infra (.py) embedded as JSON source per #103 pattern; no .py committed
- **$0 budget**: spec design only; measurement reuses #103 open-source stack (LabRecorder + pylsl + pyxdf + scipy + numpy)
- **Race isolation**: writes ONLY to `state/cp2_clm_phase_e_spec_2026_05_02/*.json` + this doc; no overlap with #103 state dir or #94/#96 state dirs
- **§16.2 anchor compliance**: all 3 anchors satisfied (§8)
- **Length**: ~2200 words within 1500-2500 target

---

## §12 References

- F1_score_v2 spec: `docs/strategic_f1_composite_v2_2026_05_02.md` (#96)
- CP2-CLM Phase D recompute: `docs/cp2_clm_phase_d_recompute_2026_05_02.md` (#94 / #104)
- N-1 BRIDGE v2 realtime prep (LSL infrastructure): `docs/n_1_bridge_v2_realtime_prep_2026_05_02.md` (#103)
- N-1 BRIDGE v2 partial results: `docs/n_1_bridge_v2_partial_results_2026_05_02.md`
- Race-isolated state: `state/cp2_clm_phase_e_spec_2026_05_02/{phase_e_objectives, measurement_protocol, bse1_pearson_3way, f1_score_v2_update_projection, falsifier_5tier_preregister, r1_r2_r3_controls, honest_c3, decision_gate}.json`

---

**status**: CP2_CLM_PHASE_E_SPEC_2026_05_02_FROZEN_AWAITING_USER_EXECUTION
**verdict_key**: PHASE_E_SPEC_FROZEN · 3WAY_BSE1_PEARSON · BETA_0_3_BINDING_ACTIVE · 5TIER_FALSIFIER_PREREGISTERED · R1_R2_R3_CONTROLS_MANDATORY · F1_PROJECTION_0_408_TO_0_558_YELLOW_CONDITIONAL_ON_F2_UNFIRE · USER_NEXT_OPENBCI_30MIN_SESSION
