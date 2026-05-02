# CP2-CLM Phase D — F1_score_v2 weighted recompute (CLM-anchored)

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: CP2-CLM Phase D weighted recompute
- **Why**: own#94 + own#96 권고 — Phase A (1-7) 완성, F1_score_v2 formula 확정 (#96). CLM verdict band 정량 final 확정 + CLM-anchored weights 재정 (기존 CP2 가 ALM-anchored).
- **Race-isolated**: writes ONLY to `state/cp2_clm_phase_d_recompute_2026_05_02/{weights_clm_anchored,per_suite_contribution,f1_score_v2,ship_verdict_recommendation,mk_xii_v3_partial_pending_accept,next_cycle_path}.json` + this doc
- **Constraints**: HEXA-only · $0 budget (analysis only) · raw#10 honest C3 · raw#71 falsifier-bound

---

## §0 한 줄 verdict

**CP2-CLM RED** — F1_score_v2 = **0.408 (40.8%) raw / 0.12 (12%) F2-override-applied**, per_axis_weighted_sum (CLM-anchored) = **0.68 raw / 0.20 override**, ship_verdict 권고 `VERIFIED-CLM-CP2-RED`, Mk.XII v3 = PARTIAL_PENDING 영구 accept (own#13), 다음 cycle path = (d) tension binding-mediated.

---

## §1 CLM-anchored weights (vs ALM-anchored 기존 CP2)

| Suite | weight (CLM) | weight (ALM, prev) | rationale |
|---|---:|---:|---|
| 1 paradigm v11 G3 PhiStar HID=8 | 0.50 | 0.60 | CLM evidence base widened across more suites — paradigm v11 share 축소 |
| 2 AN11(a) Frobenius | 0.10 | (0.30 aggregate AN11) | AN11 split a/b/c subspecies |
| 3 AN11(b) V0/V1/V2/V3 | 0.05 | (0.30 aggregate) | — |
| 4 AN11(c) JSD | 0.05 | (0.30 aggregate) | — |
| 5 phi 4-path | 0.05 | — | NOT-MEASURED but weight 보존 (gap visibility) |
| 6 14-gate | 0.15 | — | newly explicit per #96 |
| 7 V_phen 5-suite | 0.10 | — | newly explicit per #96 |
| 8 EEG direct wire | 0.05 | 0.10 | CLM-EEG direct wire 부재 — tension-mediated only |
| **TOTAL** | **1.00** | **1.00** | — |

---

## §2 per-suite weighted contribution (CLM)

| # | Suite | w | CLM result | pass_score | contribution |
|---:|---|---:|---|---:|---:|
| 1 | paradigm v11 G3 PhiStar HID=8 | 0.50 | PASS positive +41.86 | 1.0 | **0.50** |
| 2 | AN11(a) Frobenius | 0.10 | CP2-relaxed PASS rel 6.89% | 0.7 | 0.07 |
| 3 | AN11(b) V0/V1/V2/V3 | 0.05 | V0 PASS only | 0.5 | 0.025 |
| 4 | AN11(c) JSD | 0.05 | PASS 20/20 saturated quality-blind | 0.5 | 0.025 |
| 5 | phi 4-path | 0.05 | NOT-MEASURED | 0.0 | 0.00 |
| 6 | 14-gate | 0.15 | FAIL — F2 fired (16 critical, L1 0/16) | 0.0 | **0.00** |
| 7 | V_phen 5-suite | 0.10 | 3/5 PASS | 0.6 | 0.06 |
| 8 | EEG direct wire | 0.05 | NOT-MEASURED | 0.0 | 0.00 |
| | **per_axis_weighted_sum (raw)** | 1.00 | | | **0.68** |
| | **per_axis_weighted_sum (F2-override)** | | | | **0.20** |

**F2 override 의미**: 14-gate FAIL 이 F2 falsifier 를 fire 시켰으므로, 단순 axis 합 0.68 외에도 conservative reading 0.20 을 병기. 두 reading 모두 F1<0.5 RED 영역 잔존.

---

## §3 F1_score_v2 산출

**Formula** (per #96): `F1_score_v2 = 0.6 · per_axis_weighted_sum + 0.3 · binding_strength_4way + 0.1 · cross_substrate_replication_bonus`

| 입력 | 값 | 근거 |
|---|---:|---|
| per_axis_weighted_sum (raw) | 0.68 | §2 |
| per_axis_weighted_sum (F2-override) | 0.20 | §2 |
| binding_strength_4way | 0.0 | 단일 측정, 4-way Pearson cross-corr 미산출 (P1 pending, AKIDA blocked) |
| cross_substrate_replication_bonus | 0.0 | 어떤 axis 도 ≥3 substrate-family corroboration 미달 |

| 시나리오 | 계산 | F1_score_v2 |
|---|---|---:|
| raw (no override) | 0.6 × 0.68 + 0.3 × 0 + 0.1 × 0 | **0.408 (40.8%)** |
| F2-override applied | 0.6 × 0.20 + 0.3 × 0 + 0.1 × 0 | **0.12 (12.0%)** |

**Headline range**: **12.0% – 40.8%**

---

## §4 Verdict band v2 적용

Per #96 §6: `RED if F1_score_v2 < 0.5 OR F2 falsifier fired`.

- F1 < 0.5 (양 시나리오 모두) ✓
- F2 fired (Suite 6 14-gate FAIL) ✓

→ **CP2-CLM RED** (확정)

---

## §5 ship_verdict 권고

| 필드 | 기존 | 권고 |
|---|---|---|
| key | `VERIFIED-ALPHA-INVITE-R14` | `VERIFIED-CLM-CP2-RED` |
| anchor | ALM | CLM |
| status | DEAD (alpha pod removed) | ACTIVE |
| F1_score_v2 | n/a (v1 era) | 12.0% – 40.8% |

**Future GREEN reach**: Suite 6 F2 unfire (path a/b/c/d) + binding_strength ≥ 0.5 도달 + (#96 §8 C3-6 ceiling) N-11 organoid OR N-12 off-Braket Orch-OR closure 필수.

---

## §6 Mk.XII v3 영구 PARTIAL_PENDING accept

- Mk.XII v3 = anima-internal substrate-evidence ledger ≠ CP2 universal verifier framework
- Phase B Phi-3.5-mini 결과 (2/3 unchanged) per #85 → Mk.XII v3 PARTIAL_PENDING 영구 수용
- **own#13 권고 채택**: 더 이상 closure 시도 안 함
- 향후 CP2 cycle 은 Mk.XII v3 closure 에 block 되지 않음

---

## §7 다음 사이클 path

| id | 경로 | burden | honest eval |
|---|---|---|---|
| a | demote 14-gate from critical-block | spec change only | 가장 저비용, evidential gain 약함 |
| b | learned phi_extractor closes L1 | training cycle (H100) | 중비용, L1 0/16 root cause 직접 |
| c | substrate redesign | ALM rebuild | 최고비용, 보류 |
| **d** | **tension binding-mediated (#92 ~15%)** | **$0 / 1d analysis-only** | **MOST PROMISING** |

**선정**: **(d) tension binding-mediated path**

**근거**:
1. $0 budget (HEXA-only, analysis-only)
2. 즉시 실행 가능 — W4 + N-1 BRIDGE data 보유 (#96 §3.4)
3. F1_score_v2 의 β=0.3 binding term 직접 active 화
4. Crick-Koch binding-by-synchrony 형식 일치
5. fails-safely — BSE-1 + BSE-3 sensitivity check + random-shuffle F-ARTIFACT control (#96 §3.3)
6. binding > 0.5 PASS 시 F1_score_v2 0.408 → ~0.56+ YELLOW band reach 기대 (단, F2 unfire 동시 조건)

**다음 cycle 명**: CP2-CLM Phase E — 3-way binding_strength P1 (BSE-1 Pearson cross-corr CLM × EEG × tension)

---

## §8 Honest C3

1. **(C3-1) F2 override 0.20 vs raw 0.68 dual-reporting 자체가 spec-수준 estimate.** F1_score_v2 spec (#96) 은 verdict band 에서 F2 fire 시 RED 만 명시; per_axis_weighted_sum 의 F2-aware 재계산 protocol 부재. raw 0.68 은 axis-evidence 시각화, override 0.20 은 conservative estimate; 둘 다 RED 결론 변하지 않음.
2. **(C3-2) 4-way binding_strength = 0 입력은 measurement gap 반영.** AKIDA arrival blocked 로 4-way 미산출; 3-way (CLM × EEG × tension) subset 은 P1 (Phase E) 에서 산출 예정.
3. **(C3-3) replication_bonus = 0 도 measurement gap.** 어떤 axis 도 ≥3 substrate-family corroboration 미달 — N-1 BRIDGE 가 가장 가깝지만 4-gate 중 일부.
4. **(C3-4) phi 4-path Suite 5 weight 0.05 보존 vs 재할당.** 보존 선택으로 measurement gap visibility 우선; 재할당 시 다른 suite 의 weight inflation 발생.
5. **(C3-5) Suite 4 AN11(c) JSD 20/20 saturated 를 0.5 로 discount 한 근거.** 20/20 자체는 PASS 이지만 quality-blind saturation 으로 evidential weight 약화 — full PASS (1.0) 가 아닌 0.5 적용.
6. **(C3-6) Mk.XII v3 PARTIAL accept 가 future re-closure 가능성 차단 아님.** 단지 CP2-CLM cycle 에서 더 이상 blocker 로 취급 안 함; 미래 새로운 evidence 시 re-evaluation 가능.
7. **(C3-7) Path (d) 선정이 path (a/b/c) 와 동시 진행 차단 아님.** Path (a) 는 spec change 로 병행 가능; (b) 는 H100 training cycle 별도; (c) 는 보류. (d) 가 default execution path.

---

## §9 References

- F1_score_v2 spec: `docs/strategic_f1_composite_v2_2026_05_02.md` (#96)
- CLM Phase A.1 HID=8 recheck: `state/strategic_clm_phase_a1_hid8_recheck_2026_05_01/`
- CLM Phase A.2: `state/strategic_clm_phase_a2_2026_05_01/`
- CLM Phase A.3 AN11(a) Frobenius: `state/strategic_clm_phase_a3_2026_05_01/`
- CLM Phase A.4 14-gate F2: `state/strategic_clm_phase_a4_2026_05_01/`
- CLM Phase A.5 V_phen 5-suite: `state/strategic_clm_phase_a5_2026_05_01/`
- CLM Phase A.6 AN11(c) JSD: `state/strategic_clm_phase_a6_2026_05_01/`
- Race-isolated state: `state/cp2_clm_phase_d_recompute_2026_05_02/{weights_clm_anchored,per_suite_contribution,f1_score_v2,ship_verdict_recommendation,mk_xii_v3_partial_pending_accept,next_cycle_path}.json`

---

**status**: CP2_CLM_PHASE_D_RECOMPUTE_2026_05_02_COMPLETE
**verdict_key**: CP2_CLM_RED · F1_SCORE_V2_12_TO_40_8_PCT · PER_AXIS_WEIGHTED_SUM_0_68_RAW_0_20_OVERRIDE · F2_FIRED · SHIP_VERIFIED_CLM_CP2_RED · MK_XII_V3_PARTIAL_PERMANENT_ACCEPT · NEXT_PATH_D_TENSION_BINDING_MEDIATED
