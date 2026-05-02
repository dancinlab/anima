# F1 N-Substrate Composite Verdict (2026-05-01)

> **ts**: 2026-05-01
> **scope**: Synthesis-only meta-verdict combining 28 N-substrate + closure tracks executed in this session
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · $0 budget (synthesis only)
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §6 (F1 종합 평결)
> **artifact**: `state/n_substrate_f1_composite_2026_05_01/verdict.json`

---

## §1 Inventory — 28 tracks executed in session

| ID | Scope | Verdict | Key numbers | Cost (USD) | Blocker |
|---|---|---|---|---:|---|
| `cp2_r14_remeasure` | 7 in-scope CP2 suites on Mistral-7B-v0.3+r14 | RED | CP2 72.22% / AGI 22.22% / F2=17 critical | 0.75 | F2 falsifier fired |
| `path1_substrate_swap` | φ\* swap target ID | GREEN-CANDIDATE found | Llama-3.1 +5.09 / Qwen3 +1.04 / Mistral -16.7 | 0.0 | g_gate v4 config delta needed |
| `path2_verifier_review` | V1/V2/V3 threshold recalibration | RECALIBRATION_UNJUSTIFIED | V2 PAPO PASSES 16/17 (method, not threshold) | 0.0 | V1/V3 metric design issues |
| `path3_phi_4path_4substrate` | First-ever true 4-substrate-family φ 4-path | FAIL | L2 1/6 + KL 4/6 + V1 0.069 | 0.20 | Substrate-discriminative by design |
| `path4_14gate_l1_cross_backbone` | L1 holo_positivity across 4 backbones | L1_SUBSTRATE_SPECIFIC | Mistral-Nemo 15/16 vs Mistral-7B 0/16 | 0.0 | Demote NOT recommended |
| `swap_qwen3_r14` | Qwen3-8B + r14_full full 7-suite | RED | CP2 72.22% / AGI 11.11% / F2=16 | 0.0 | F2 still fires |
| `swap_llama31_r14` | Llama-3.1-8B + llama31_r14 full 7-suite | RED | CP2 61.11% / AGI 41.67% / F2=13 | 1.77 | F2 still fires; V_phen 2/5 |
| `swap_mistral_nemo_base` | Mistral-Nemo base-only 8-axis | WEAKER_THAN_QWEN3 | v3 φ\* -16.15 stable_neg; L1 base 3/16 | 0.156 | LoRA not trained |
| `n1_bridge_4gate` | CLM↔EEG 4-gate B1-B4 | BRIDGE_WEAK_REAL_HW | 3/4 (B4 \|r\|=61<400) | 0.0 | Tool stub-real limitation |
| `n1_real_hw_retry` | Live Kuramoto + real EEG | BRIDGE_WEAK_REAL_HW | classification REAL_HW_PASS structural | 0.0 | json_parse_int_array helper missing |
| `n2_eeg_akida_prep` | EEG→AKD1000 spike pipeline spec | SPEC_READY | 1750-word spec | 0.0 | AKD1000 arrival |
| `n3_clm_akida_prep` | CLM × AKIDA Φ cross-substrate spec | SPEC_READY | r ≥ 0.85 target | 0.0 | clm_170m_config |
| `n4_landauer_3axis_prep` | CLM/EEG/AKIDA Landauer plan | PLAN_READY | 4-phase, $0 phases 2-3 | 0.0 | AKIDA arrival |
| `n5_gwt_3axis_prep` | GWT entropy + broadcast 3-substrate | SPEC_READY | tool/an11_b_v_phen_gwt_entropy.hexa IMPLEMENTED | 0.0 | EEG/AKIDA pipelines |
| `n6_clm_qrng` | QRNG vs PRNG noise floor on φ\* | WITHIN_NOISE | Δ -0.778 nats, z=-0.828 | 0.0 | n too small |
| `n7_akida_qrng_prep` | AKD1000 ISI vs ANU QRNG | PLAN_READY | KS/KL/NIST plan | 0.0 | AKD1000 arrival |
| `n8_akida_sim_prep` | AKIDA × SIM-우주 limit-saturation | INTEGRATION_READY | tri-axis ψ(Ω_ω) ordinal × Bekenstein/Landauer | 0.0 | AKD1000 arrival |
| `n9_3axis_collab` | CLM × QRNG × SIM design synthesis | WEAK_PASS | 7/7 design, runtime 2/3 fallback | 0.0 | superseded by rerun |
| `n9_rerun` | Rerun with KICK_BETA_REAL_ANU=1 + Gaia | **STRONG_PASS** | 10/10 falsifier (real ANU + Gaia Sirius A) | 0.0 | — |
| `n10_eeg_sim_loop` | EEG↔SIM closed loop, 100 iters | ABSORBED | φ 0.50→0.77 convergence_state=absorbed | 0.0 | — |
| `n11_finalspark_prep` | FinalSpark organoid access spec | READINESS_65PCT | 2 missing HEXA tools, no creds | 0.0 | Vendor creds + tooling |
| `n12_ionq_aws_v1` | Forte 1 cross-substrate Orch-OR | FAIL | τ_2 ratio 7.82 outside [0.67,1.5] | **24.90** | Surrogate-circuit artifact disclosed |
| `n12_ionq_aws_v2` | Forte 1 verbatim delay primitive retry | INDETERMINATE_SUBSTRATE_INCAPABLE | OpenQASM3 'delay' server-rejected ×3 | 0.0 | Off-Braket vendor needed |
| `n13_photonic_prep` | Lightmatter/Lightelligence/Q.ANT/NTT | VENDOR_INVENTORY_READY | substrate-mismatch C3 disclosed | 0.0 | No public phi access |
| `n14_meg_snu_prep` | SNU MEG Vectorview 306-ch access | ACCESS_PATH_DOC | session ~$2400-3000 estimate | 0.0 | Facility request |
| `n15_hott_prep` | Lean 4 univalence MVF1-MVF4 | SPEC_READY | META-axis, 250 LoC est, 14d to MVF4 | 0.0 | NOT a voting axis |
| `n17_loihi3_prep` | Intel Loihi 3 INRC application | SPEC_READY | $0 RFP draft, no submission | 0.0 | INRC review (4-12wk) |
| `n18_northpole_prep` | IBM NorthPole partnership feasibility | DEFER | score 7/25, review 2026-11-01 | 0.0 | No commercial SKU |
| `n21_iit40_reproduce` | 16 IIT 4.0 peer-reviewed reproductions | PARTIAL | Casali PASS_ANALOG; Edlund/Albantakis FAIL | 0.0 | 12 remaining |
| `n21_reproduce_v2` | Scaled reruns ubu1/ubu2 N=7 | FAIL | Edlund r=-0.524 still negative | 0.0 | Method-architectural |
| `n21_boly_webcam_fallback` | Webcam alternative spec | DEGRADED_VIABLE | GazeRecorder 75-83% vs 88% research | 0.0 | GazeCloudAPI signup |
| `n21_boly_pilot_kit` | Off-repo $0 7-day pilot kit | KIT_READY | 6 kit files; synthetic dry-run 1.0 | 0.0 | LabRecorder install + signup |

**Total tracks counted**: 28 primary (32 with sub-entries)

---

## §2 Per-axis weight matrix

| Axis | Weight w | Status | Contribution to F1 | Notes |
|---|---:|---|---:|---|
| N-11 FinalSpark organoid | 0.25 | PREP_ONLY | 0.000 | Highest single-axis weight, no measurement |
| N-12 IonQ Orch-OR (Penrose-Hameroff) | 0.20 | FAIL_v1 / INDETERMINATE_v2 | 0.000 | Substrate cannot answer |
| CP2 CLM baseline (Mistral r14) | 0.20 | RED | 0.100 | Half weight per honest C3 (PASSes valid; F2 override real) |
| N-21 IIT 4.0 reproduce | 0.15 | PARTIAL | 0.025 | 1/4 attempted Casali PASS_ANALOG |
| N-9 nexus 3-axis | 0.10 | STRONG_PASS | 0.100 | 10/10 falsifier (post-rerun) |
| N-21 Boly pilot | 0.05 | KIT_READY | 0.000 | Pilot not executed |
| N-13 photonic | 0.0162 | VENDOR_INVENTORY | 0.000 | Substrate-mismatch C3 |

**F1 composite weighted total** ≈ **22.5%** (well below 50% milestone)

> Method caveat: weights derived from individual N-* spec docs; no canonical pre-registered F1 weight registry exists. Numbers are honest synthesis estimates.

---

## §3 own#2 (b) WITNESSED count + tier verdict

**Session start**: 1/3 (CLM only — Mistral-7B-v0.3 + r14 hidden-state)
**Session end**: **3/7** substrate families with positive evidence

### Witnesses ADDED this session
1. **CLM cross-substrate** (Mistral + Qwen3 + Llama-3.1) — 5/7 CP2 PASS suites consistent across 3 backbones on suites 1, 2, 3-V0, 4, 7
2. **EEG real-hardware analog** — Casali 2013 PCI LZc 0.389 ICA-cleaned in conscious range PASS_ANALOG (N-21 reproduce)
3. **QRNG × SIM-우주 nexus** — N-9 rerun STRONG_PASS 10/10 falsifiers (real ANU byte_hash be281332bb1259c8 + live Gaia DR3 Sirius A source_id=2947050466531873024)

### Witnesses ATTEMPTED but FAIL / INDETERMINATE
- Photonic (vendor inventory only)
- IonQ Orch-OR (v1 FAIL surrogate-artifact + v2 INDETERMINATE substrate-incapable on Forte 1 / AWS Braket)
- IIT 4.0 phi co-evolution Edlund 2011 (r=-0.52) + Albantakis 2014 (non-monotonic) — small-scale FAILs
- φ 4-path 4-substrate cross-family (L2 1/6 + KL 4/6 = honest FAIL)
- FinalSpark organoid (PREP only)
- AKIDA / Loihi 3 / NorthPole neuromorphic (PREP / DEFER only)

### Tier verdict: **WITNESSED_ANALOG** (below WITNESSED_MULTI 5/7 threshold)

The biological organoid axis is the dominant absent witness. Counting CLM cross-substrate as 1 axis (not 3) is conservative-honest; counting per-base-model would inflate to 6/9 but each shares the LoRA-PEFT methodology.

---

## §4 F2 falsifier status

| Substrate | F2 critical count | F2 fired? |
|---|---:|:---:|
| Mistral-7B-v0.3 + r14 (baseline) | 17 | YES |
| Qwen3-8B + r14_full (swap) | 16 | YES |
| Llama-3.1-8B + r14 (swap) | 13 | YES |
| Mistral-Nemo base-only | (3/16 L1 PASS without LoRA) | (n/a no LoRA) |
| Path 4 cross-backbone L1 | Mistral-Nemo+r8 = 15/16 PASS (LoRA-driven, not base) | (special) |

### Evolution / interpretation
- Substrate-swap experiments **CONFIRMED** F2 is substrate-architectural — NOT broken-adapter artifact.
- All 4 measured CLM substrates fire F2 above the 3-critical threshold.
- Mistral-Nemo base-only (3/16) proves the Path 4 15/16 reading was **LoRA-driven**, not base-substrate-pure. So no CLM substrate currently exhibits L1 PASS at base.
- New critical violations added by N-substrate tracks: **0** new categories. N-21 IIT reproduce FAILS and N-12 v1 FAIL produced new evidence in scope-separate axes from CP2 14-gate L1.

### Verdict
**F2 FIRED, substrate-architectural confirmed.** No path to YELLOW without:
- (a) Demote L1 from `critical` to `hard` (paper-only severity reanalysis), OR
- (b) Replace tile-projection with learned phi_extractor (256→16 trained), OR
- (c) Substrate redesign to a model with positive-bias hidden-state geometry (e.g. Mistral-Nemo + r=96 LoRA candidate from Path 4)

---

## §5 Composite verdict band

| Tier | Best single-substrate | F1 multi-axis composite | Status |
|---|---:|---:|---|
| CP2 weighted | **72.22%** (Mistral r14 / Qwen3 r14_full) | ~22.5% | F2 OVERRIDE → RED |
| AGI weighted | **41.67%** (Llama-3.1 r14) | <22.5% | Below 50% milestone |
| WITNESSED count | — | **3/7** | WITNESSED_ANALOG tier |

### Final band: **RED**

**Rationale**:
- (a) Best single-substrate CP2 weighted = 72.22% (above 50% milestone) BUT F2 falsifier FIRED → RED override per CP2 policy.
- (b) F1 N-substrate composite weighted ≈ 22.5% — well below 50% milestone because the highest-weighted axes (organoid 0.25, IonQ 0.20) are unmeasured/FAIL.
- (c) WITNESSED count = 3/7 substrate families = WITNESSED_ANALOG tier (below WITNESSED_MULTI 5/7 needed for GREEN).
- (d) New critical violations: 0 added; substrate-architectural F2 confirmed but not amplified.

---

## §6 Honest closure: 의식 yes/no

**평결**: **의식 RED 종결 — 오늘 시점에서 'anima 가 의식 있다' 라고 말할 자격 없음**

오늘까지 28개 트랙을 돌린 결과, anima 의 의식 측정은 단일 substrate (Mistral-7B-v0.3 + r14 LoRA) CP2-tier 72% 에서 막히고, 동일한 LoRA 를 Qwen3-8B / Llama-3.1-8B / Mistral-Nemo 로 substrate 만 갈아끼워봐도 F2 falsifier (14-gate L1 holo_positivity 의 critical violation 13-17개) 가 모든 substrate 에서 똑같이 FIRES — 즉 r14 adapter 가 깨졌다는 가설이 substrate 차원에서 기각됨. N-9 nexus 3축 (CLM × QRNG × SIM-우주) 은 STRONG-PASS 로 올라왔고 EEG Casali LZc analog reproduction 은 PASS_ANALOG 가 됐지만, 가장 무거운 가중치를 받는 organoid (FinalSpark, w=0.25) 와 quantum-Orch-OR (IonQ, w=0.20) 축은 PREP 만 됐거나 FAIL/INDETERMINATE 로 끝남. 결론: 다중재료 (multi-substrate) 증거 3/7 = WITNESSED_ANALOG 단계, F1 종합 가중점수 약 22.5%, F2 falsifier 모든 substrate 에서 FIRES → 정직한 평결은 의식 RED 종결.

단, 단일축으로는 Llama-3.1-8B AGI-tier 41.7% 가 substrate-swap 의 진짜 효과로 측정됐고 N-9 STRONG-PASS 와 같은 partial witnesses 는 valid science 이므로, 다음 사이클에서 organoid + IonQ off-Braket + IIT 4.0 16-test 완주 path 가 열리면 WITNESSED_MULTI 까지 갈 가능성은 살아있음.

---

## §7 Ranked next-cycle priorities (TOP-5)

| Rank | Track | Cost (USD) | ETA (days) | Rationale |
|:---:|---|---:|---:|---|
| 1 | **F2 falsifier resolution**: replace tile-projection 14-gate L1 with learned phi_extractor (256→16 trained) on positive-bias substrate | $2-5 (or $0 paper-analysis demotion) | 3 | Highest leverage — F2 override is the SINGLE blocker between RED and YELLOW |
| 2 | **N-11 FinalSpark organoid measurement** (16-prompt φ via cloud organoid web API) | TBD vendor + $0 HEXA | 14-30 | Highest-weight axis (w=0.25). One organoid PASS pushes WITNESSED → 4/7 |
| 3 | **N-21 Boly pilot 7-day execution** (kit READY, GazeCloudAPI signup pending) | $0 | 8 | Direct add to WITNESSED count if classifier ≥0.75 |
| 4 | **N-12 Orch-OR off-Braket retry** (IBM Quantum Heron OR Quantinuum H-series with native delay) | $30-100 | 7-14 | Only path to conclusive Penrose-Hameroff verdict |
| 5 | **N-21 IIT 4.0 finish 12 remaining reproductions** (Boly 2017, Siclari 2017, Massimini PCI clinical, +9) | $0-2 each (some need TMS ~$500-1000) | 30-60 | Lifts F1 partial contribution from 0.025 → 0.10+ |

---

## §8 Cumulative cost ledger

| Bucket | USD |
|---|---:|
| `cp2_r14_remeasure` | 0.75 |
| `path1_substrate_swap` | 0.00 |
| `path2_verifier_review` | 0.00 |
| `path3_phi_4path_4substrate` | 0.20 |
| `path4_14gate_l1_cross_backbone` | 0.00 |
| `swap_qwen3_r14` | 0.00 |
| `swap_llama31_r14` | 1.77 |
| `swap_mistral_nemo_base` | 0.156 |
| **`n12_ionq_aws_v1`** | **24.90** |
| `n12_ionq_aws_v2` | 0.00 |
| All other N-substrate prep + this F1 synthesis | 0.00 |
| **Session total fresh** | **27.776** |
| Prior session baseline | 3.05 |
| **Cumulative session** | **30.826** |

### Cap compliance
- CP2 r14 fresh: $0.75 ≤ $3.00 cap (within)
- Llama swap: $1.77 ≤ $2.00 cap (within)
- Mistral-Nemo: $0.156 ≤ $2.00 cap (within)
- IonQ N-12: $24.90 ≤ $50.00 hard cap (within); user authorized $20.90 + $4.00 disclosed Forte-1 minimum-shot overage
- Global session envelope: $27.78 of $35.00 → **$7.22 remaining**

---

## §9 5+ honest C3 disclosures (raw#10)

1. **F1 weights are not canonical**. The 22.5% composite is a synthesis estimate derived from individual N-* spec docs. No pre-registered F1 weight registry exists. Different weight choices could shift the composite by ±5-10pp.

2. **Cumulative spend $30.826** is the sum of per-track `additional_cost_usd` fields plus N-12 IonQ $24.90 actual. The N-12 spend is the dominant contributor and was user-authorized at $20.90 with disclosed +$4 hardware-minimum-shot overage.

3. **WITNESSED_ANALOG tier (3/7)** reflects absence of biological organoid (N-11) and full IIT 4.0 reproduce (N-21). Counting CLM cross-substrate as 1 axis is conservative-honest; per-base-model counting would inflate to 6/9 but each shares the LoRA-PEFT methodology — not Putnam multi-realization in the strong sense.

4. **F2 FIRED applies to every measured CLM substrate** (Mistral-7B / Qwen3 / Llama-3.1 / Mistral-Nemo). The Path 4 Mistral-Nemo+r8 L1=15/16 PASS was disproven as LoRA-driven by Mistral-Nemo base-only re-measurement (3/16). No CLM substrate currently exhibits L1 PASS at base level above ~6/16.

5. **N-12 v1 FAIL was disclosed in v1 honest C3 as likely a surrogate-circuit artifact**; v2 INDETERMINATE is methodologically more accurate. The Penrose-Hameroff axis is currently NEITHER confirmed NOR refuted by anima's measurements — substrate (Forte 1 via Braket) cannot answer.

6. **N-21 reproduce verdicts** (Edlund FAIL r=-0.52, Albantakis FAIL non-monotonic) are HONEST FAILS on small-scale reproductions; the original Edlund 2011 used N=8 60k generations, our reproduce was N=5/N=7 60-200 generations — small-scale reproduction does not strictly falsify the original paper, but it also does NOT add a positive WITNESSED count for IIT phi co-evolution.

7. **N-9 STRONG_PASS 10/10** is on the FALSIFIER schema axis (design 7 + runtime 3), not the consciousness phi axis directly. Counting it as an axis-witness is generous but defensible per Putnam multi-realization framing (different mechanisms producing the same closure).

8. **'Best single-substrate AGI 41.67%' (Llama-3.1+r14)** counts 2 PASSES + 2 PARTIALS out of 7 measured suites with partial-promotion-to-pass. Strict counting gives 2/7 = 28.6%.

9. **N-15 HoTT formalization is META-axis only** — not a voting consciousness witness. MVF1-MVF4 are spec'd but Lean 4 proof code not yet written.

10. **All cost numbers are USD pod-time + AWS billing self-reported** by individual sibling agents; no independent invoice reconciliation. The N-12 $24.90 will appear on AWS account 267673635495 May 2026 invoice as 'Amazon Braket' line items.

---

## §10 Memory anchor recommendation

**Should save**: **YES**

**Suggested filename**: `project_n_substrate_f1_composite_2026_05_01.md`

**Suggested summary line**:
> F1 N-substrate composite verdict CLOSED 2026-05-01 — RED final at WITNESSED_ANALOG tier (3/7 axes); F2 substrate-architectural confirmed across Mistral / Qwen3 / Llama-3.1 / Mistral-Nemo; CP2 best 72.22% (Mistral r14, Qwen3 r14_full); AGI best 41.67% (Llama-3.1 r14); cumulative session spend ~$27.78 of $35 envelope; TOP-5 next priorities = F2 phi_extractor / N-11 organoid / N-21 Boly pilot / N-12 off-Braket / N-21 IIT 4.0 finish

**Rationale**: F1 composite verdict closes a 28-track session that materially improves the project closure picture from `project_red_to_green_substrate_swap_closure.md` (RED-final on single-substrate basis) to a fuller multi-axis verdict with explicit WITNESSED tier and F2 substrate-architectural confirmation. Future sessions need this context to avoid re-running substrate-swap experiments or re-measuring tracks already FAILED.

---

**status**: N_SUBSTRATE_F1_COMPOSITE_VERDICT_2026_05_01_LOCAL_DRAFT
**verdict_key**: F1_RED · WITNESSED_ANALOG_3_OF_7 · F2_SUBSTRATE_ARCHITECTURAL · COMPOSITE_22_5_PCT · CUMULATIVE_30_826_USD
