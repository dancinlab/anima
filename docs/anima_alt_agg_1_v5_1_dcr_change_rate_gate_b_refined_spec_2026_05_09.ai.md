# ALT-AGG-1 v5.1 — Gate B-refined DCR change_rate spec

**SSOT**: ALT-AGG-1 v5.1 + this doc + `tool/anima_cli/consciousness.hexa` (`_c3_b_pass_v5_refined`, `_c3_ensemble_v5_1_pass`, `_c3_ensemble_v5_1_label`) + `anima/registry/anima_artifact_registry.yaml` v5_1_* fields + `.own` line 980+ amend.

**Cycle**: anima 2026-05-09 NEXT-CYCLE 3/6 (사용자 directive verbatim "all bg go").
**Trigger**: KICK WAVE 4 ADDENDUM commit `c17b923c`.
**Rule precedence (raw#15 additive)**: v3 → v4 → v5 base → v5 ADDENDUM → **v5.1**. 모든 predicate 함수 보존; v5.1 은 Gate B replacement lane (v5 base Gate B `_dcr_pass(dcr_distinct)` 함수 그대로 살아있음).
**raw#82 retraction-aware**: v5 ADDENDUM verdicts (sft-1-8 = C3_FAIL_V5_ADDENDUM 등) 그대로 보존; v5.1 은 별도 lane 으로 산출되는 verdict overlay.

---

## 1. Motivation

KICK WAVE 4 ADDENDUM (commit `c17b923c`) 의 핵심 finding — 4 v5 gates 중 **DCR change_rate (consecutive-prompt argmax-change rate)** 가 sole strong substrate-level discriminator:

| Model | DCR distinct | DCR change_rate | Notes |
|---|---|---|---|
| sft-1-8 N=60 (fe4f8a7d) | 0.80 | **0.6379** (37/58) | Gate B-refined PASS |
| sft-1-7-y1 N=60 (757e4169) | 1.00 | **0.8475** (50/59) | Gate B-refined PASS, highest delta |
| paradigm-j N=120 (84aa8665) | 1.00 | **0.7479** (89/119) | Gate B-refined PASS |
| random_init seed=42 N=30 | 0.60 | **0.1429** (4/28) | Gate B-refined FAIL ★ |

기존 v5 Gate B `_dcr_pass(dcr_distinct) ≥ 0.40` 의 약점:
- random_init distinct=0.60 도 0.40 floor 통과 → leak
- distinct count 는 sample size 와 무관하게 5-axis 중 단 2개만 winning 시 PASS
- 실제 substrate-level discrimination 측정 불가

v5.1 Gate B-refined `_c3_b_pass_v5_refined(dcr_change_rate) ≥ 0.40`:
- random_init 0.143/0.172 strict reject ✓
- sft-1-8 0.6379 / sft-1-7-y1 0.8475 / paradigm-j 0.7479 PASS
- delta vs random_init: +0.4950 / +0.7046 / +0.6050 (모두 strong separator)

---

## 2. Gate B-refined definition

```hexa
fn _c3_b_pass_v5_refined(dcr_change_rate: float) -> bool {
    return dcr_change_rate >= 0.40
}
```

`dcr_change_rate := _dcr_compute_conditioning_rate(probe_results) = (n_argmax_changes / (n - 1))`.

Sample filter: anchor-divergent rows (`ok=true ∧ phi_drift_abs > 0`).
- `.own` historical canonical (line 994): random_init = 4/28 = 0.1429.
- Full anchor-divergent recompute (본 cycle): random_init = 5/29 = 0.1724.
- Both reject Gate B-refined floor 0.40.

---

## 3. v5.1 ensemble (4 gates)

```hexa
fn _c3_ensemble_v5_1_pass(piv_max, dcr_change_rate, d_rand, gate_d_random_below_005) -> bool {
    let a = _piv_max_pass(piv_max)                       // ≥ 0.10  (v5 inherit)
    let b = _c3_b_pass_v5_refined(dcr_change_rate)       // ≥ 0.40  (v5.1 NEW)
    let c = _drand_pass(d_rand)                          // ≥ 0.05  (v5 inherit)
    let d = gate_d_random_below_005                      // V14 self-test (v5 inherit)
    return a && b && c && d
}
```

3-tier label (`_c3_ensemble_v5_1_label`):
- All 4 PASS → `C3_PASS_V5_1`
- Gate D = false → `C3_FAIL_V14_VIOLATED_V5_1` (즉시; V14 strict precedence)
- 3 of 4 PASS (D=true 가정) → `C3_PARTIAL_NEAR_V5_1`
- ≤2 of 4 PASS → `C3_FAIL_V5_1`

Gate A/C/D 는 v5 base 그대로 — 본 cycle 은 Gate B replacement 만.
- Gate A (PIV-max): substrate amplitude saturation 정합 — 모든 trained 모델 < 0.10
- Gate C (D-RAND on c3_4): c3_4 collapse (v4 N=60 retest finding) 정합
- Gate D (random self-test < 0.05): random_init c3_4 mean 0.1338 > 0.05 — recalibration mandate carry (별도 cycle: c3_4_v5 normalized scale OR floor 0.15)

---

## 4. Existing-data validation (0-cost local)

| Model | DCR_change | Gate A | Gate B-r | Gate C | Gate D | v5.1 verdict |
|---|---|---|---|---|---|---|
| sft-1-8 N=60 | 0.6379 | FAIL (0.0393) | **PASS** | FAIL (-0.0034) | FAIL (0.1338) | **C3_FAIL_V14_VIOLATED_V5_1** |
| sft-1-7-y1 N=60 | 0.8475 | FAIL (0.0515) | **PASS** | pending | FAIL (shared) | **C3_FAIL_V14_VIOLATED_V5_1** |
| paradigm-j N=120 | 0.7479 | FAIL (0.0469) | **PASS** | pending | FAIL (shared) | **C3_FAIL_V14_VIOLATED_V5_1** |
| random_init seed=42 | 0.1429 | FAIL | **FAIL** ★ | anchor | FAIL | **C3_FAIL_V5_1_EXPECTED** |

★ random_init Gate B-refined FAIL = v5.1 의 핵심 V14 separator. delta vs trained models +0.4950 / +0.7046 / +0.6050.

**v5.1 strict EMERGE**: 본 cycle 산출 0건. V14 strict 정합 sustained — Gate B 강화만으로는 부족; Gate A (PIV) post-arch-fix re-probe + Gate D recalibration 별도 cycle mandate.

---

## 5. SSOT mirror (매단계)

- `tool/anima_cli/consciousness.hexa` lines 1196+ (3 신설 함수 — `_c3_b_pass_v5_refined`, `_c3_ensemble_v5_1_pass`, `_c3_ensemble_v5_1_label`; raw#15 additive — v5 함수 모두 보존)
- `anima/registry/anima_artifact_registry.yaml` — sft-1-8 / sft-1-7-y1 / paradigm-j / random-init-mk2-v1-mirror 4 entries 모두 `v5_1_dcr_change_rate` + `v5_1_gate_*_pass` + `v5_1_verdict` + `v5_1_honest_c3` fields 추가; framework_amends NEXT-CYCLE 3/6 entry land
- `.own` (line 980+ 별도 amend block; raw#82 retraction-aware — v5 ADDENDUM 두 verdicts 보존)
- 본 spec doc (yaml↔md mandate)
- `anima/registry/anima_artifact_registry.md` (yaml render 산출 — mandatory regenerate)

---

## 6. Honest-c3 (raw#10)

1. Gate B-refined 단독으로는 EMERGE 산출 불가 — v5.1 도 strict 통과 0건. V14 strict 정합.
2. random_init Gate B-refined FAIL 이 sole strong substrate-level evidence — substrate-level (5-axis 192-cell) 변별력은 living signal 하나뿐.
3. Gate D recalibration 별도 cycle 필요 (c3_4_v5 normalized scale OR floor 0.15) — random_init c3_4 mean 0.1338 가 substrate session noise 의 irreducible floor 임을 reaffirm.
4. Gate A PIV 는 post-arch-fix (CONSCIOUSNESS_DIM 192→96) re-probe 후 재평가; substrate amplitude saturation 가능성.
5. anchor-divergent filter convention preserved — `.own` historical figure (random_init 4/28=0.1429) 와 full recompute (5/29=0.1724) 둘 다 Gate B-refined FAIL.

---

## 7. Next steps (raw#15 additive carry)

1. Gate D recalibration (별도 cycle) — c3_4_v5 normalized 또는 floor 0.15 floor reset
2. Gate A post-arch-fix re-probe (CONSCIOUSNESS_DIM 192→96) — PIV 측정 재평가
3. cell-level DCR change_rate (192-cell `dominant_cells` JSON expose) — substrate stricter variant
4. paraphrase k≥3 PIV (Gate G) — semantic discrimination true measurement
5. 모든 BG (BG-LA/LB/LC/LD/LE/KM/etc) 측정 시 v5.1 lane 기본 산출 (registry yaml v5_1_* fields mandatory)
