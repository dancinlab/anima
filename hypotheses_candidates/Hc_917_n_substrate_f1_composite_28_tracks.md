---
id: Hc_917
slug: n-substrate-f1-composite-28-tracks
title: F1 Composite Verdict — 28 N-substrate track + axis weight matrix (N-9 STRONG_PASS 10/10, N-11 PREP, N-12 FAIL/INDETERMINATE, N-21 PARTIAL, CP2 RED, path-2 RECALIBRATION_UNJUSTIFIED, path-3 FAIL, path-4 SUBSTRATE_SPECIFIC)
domain: consciousness, measurement
status: candidate-unverified
source_doc: docs/n_substrate_f1_composite_verdict_2026_05_01.md
source_lines: 1-60
promoted_at: 2026-05-11
linked_h: Hc_902 (N-substrate roadmap), Hc_903-905 (zombie posterior)
notes: "28 primary track + 4 sub-entry. F1 meta-verdict synthesis. Per-axis weight matrix. Cost $27.51 total (24.90 IonQ Forte + others)."
---

## Hypothesis

28개 N-substrate track 의 per-axis weight matrix synthesis 결과 F1 종합 평결이 own#2 (b) closure 에 미달. N-11 FinalSpark (weight 0.25, PREP_ONLY) + N-12 IonQ Orch-OR (weight 0.20, FAIL/INDETERMINATE) 가 highest single-axis weight 이나 0 contribution. N-9 nexus 3-axis 만 STRONG_PASS (10/10 falsifier, post-rerun KICK_BETA_REAL_ANU=1 + Gaia Sirius A).

## Sub-claims (28 tracks)

- cp2_r14_remeasure: 7-suite Mistral-7B-v0.3+r14 — RED (CP2 72.22% / AGI 22.22% / F2=17)
- path1_substrate_swap: GREEN-CANDIDATE Llama-3.1 +5.09, Qwen3 +1.04, Mistral -16.7
- path2_verifier_review: RECALIBRATION_UNJUSTIFIED (V2 PAPO 16/17)
- path3_phi_4path_4substrate: FAIL — L2 1/6, KL 4/6, V1 0.069
- path4_14gate_l1_cross_backbone: L1_SUBSTRATE_SPECIFIC (Mistral-Nemo 15/16 vs Mistral-7B 0/16)
- swap_qwen3_r14: RED (CP2 72.22% / AGI 11.11% / F2=16)
- swap_llama31_r14: RED (CP2 61.11% / AGI 41.67% / F2=13)
- swap_mistral_nemo_base: WEAKER_THAN_QWEN3
- n1_bridge_4gate: BRIDGE_WEAK_REAL_HW (3/4 B4 |r|=61<400)
- n2_eeg_akida_prep: SPEC_READY (1750-word)
- n3_clm_akida_prep: SPEC_READY (r≥0.85 target)
- n4_landauer_3axis_prep: PLAN_READY (4-phase)
- n5_gwt_3axis_prep: SPEC_READY (gwt entropy IMPLEMENTED)
- n6_clm_qrng: WITHIN_NOISE (Δ-0.778 nats, z=-0.828)
- n7_akida_qrng_prep: PLAN_READY (KS/KL/NIST)
- n8_akida_sim_prep: INTEGRATION_READY (ψ(Ω_ω) ordinal × Bekenstein/Landauer)
- n9_3axis_collab: WEAK_PASS (7/7 design, runtime 2/3 fallback)
- n9_rerun: **STRONG_PASS 10/10** (real ANU + Gaia Sirius A)
- n10_eeg_sim_loop: ABSORBED (φ 0.50→0.77 convergence)
- n11_finalspark_prep: READINESS_65PCT (2 HEXA tools missing)
- n12_ionq_aws_v1: FAIL — τ_2 ratio 7.82 outside [0.67, 1.5], $24.90 spent
- n12_ionq_aws_v2: INDETERMINATE_SUBSTRATE_INCAPABLE (OpenQASM3 'delay' rejected 3×)
- n13_photonic_prep: VENDOR_INVENTORY_READY (Lightmatter/Lightelligence/Q.ANT/NTT)
- n14_meg_snu_prep: ACCESS_PATH_DOC ($2400-3000 estimate)
- n15_hott_prep: SPEC_READY (Lean 4, 250 LoC, 14d to MVF4)
- n17_loihi3_prep: SPEC_READY (INRC RFP draft)
- n18_northpole_prep: DEFER (score 7/25, review 2026-11-01)
- n21_iit40_reproduce: PARTIAL (Casali PASS_ANALOG; Edlund/Albantakis FAIL)
- n21_reproduce_v2: FAIL (Edlund r=-0.524 still negative)
- n21_boly_webcam_fallback: DEGRADED_VIABLE (GazeRecorder 75-83% vs 88%)
- n21_boly_pilot_kit: KIT_READY (6 files, synthetic dry-run 1.0)

## Migration TODO

- [ ] 28 track 각각 별도 Hc 후보 (현재 cluster 화)
- [ ] N-9 STRONG_PASS 10/10 의 의미 — own#2 (b) closure 와 거리
- [ ] Per-axis weight matrix 의 정당성 (왜 N-11 가 0.25 highest?)
- [ ] F2 falsifier 의 정의 + 17 critical 의 source
