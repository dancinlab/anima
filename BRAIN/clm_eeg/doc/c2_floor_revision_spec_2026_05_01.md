# C2 Floor Revision Spec — P2 TLR Coupling Threshold Reformulation

- **Date**: 2026-05-01
- **Document type**: **decision spec only — no source/state/criteria mutation**
- **Scope**: P2 TLR `C2_clm_r_min_x1000` (currently `380`, ≡ floor 0.38) revision candidates + falsifier preregister + decision protocol

---

## §0. Executive Summary


- `raw_no_ica` / `filtered_narrowband`: 0.372 (F_PLVP_01 ref-short 위반, 0.38 floor 미달)
- `ica_cleaned_narrowband` / `amica_fallback`: 0.993 / 0.999 (F_PLVP_02 collapse — volume conduction 의심)

P3 GCG (commit `f27d6363f`) 도 real FALSIFIED, P1 LZ b=351 (frozen lo 650 미달). composite ≥2/3 PASS NOT met. **즉, frozen criteria v1.1 surface 가 real EEG 입력에 대해 falsify 됨**.


권장: **후보 B (PLI/wPLI)** — post-hoc threshold relax 회피, volume conduction immunity 직교 lever, falsifier 명시 가능. fallback 으로 후보 A (downward 0.38→0.30) 를 *공식 v2 bump* 절차 안에서만 검토.

---


v1.1 frozen P2 TLR criteria (`state/clm_eeg_pre_register_v1_1.json` §criteria.P2_TLR):

| key | value | 의미 |
|---|---|---|
| `C1_alpha_coh_min_x1000` | **450** | alpha-band coherence 최소 0.450 |
| `C2_clm_r_min_x1000` | **380** | CLM coupling r 최소 **0.380** ← 본 spec 의 revision 대상 |
| `verdict_rule` | `"P2.PASS = (alpha_coh >= C1) AND (clm_r >= C2)"` | conjunction |

v1.1 changelog §5 negative falsifier #5: `criteria.P2_TLR.C2_clm_r_min_x1000 ≠ 380` → **v2 bump 필수**.

**본 spec 은 위 380 floor 를 변경하지 않는다.** 본 doc 은 (a) 변경이 정당화되는 조건, (b) 후보 reformulation 3 종, (c) 각 후보의 falsifier preregister, (d) 결정 protocol 만 명시한다.

---

## §2. 3 후보 대안

### 2.1 후보 A — Downward Revision (380 → 300)

- **변경**: `C2_clm_r_min_x1000`: 380 → **300** (0.30 floor)
- **장점**: 수정 minimal, v2 bump 1 line, hexa toolchain 변경 없음.
  1. **post-hoc threshold change** — falsified 후 threshold 를 측정값에 맞게 내리는 행위 = data dredging / HARKing 의 전형.
  2. 0.30 의 *생리학적/이론적 근거 없음* — 380 도 근거 부족했지만, 300 은 더 약함.
  3. ica_cleaned 0.993 / amica 0.999 collapse (F_PLVP_02) 는 **threshold 와 무관**하게 여전히 falsifier triggered → P2_PASS 달성해도 **volume conduction 의심 미해소**.
- **결론**: **post-hoc relax 회피 원칙 위반**. 단독 채택 권장하지 않음. 만약 채택한다면 **공식 pre-register v2 bump + rationale doc + new falsifier set** 패키지로만.

### 2.2 후보 B — PLI / wPLI 도입 (volume conduction immune)

- **변경**: P2 TLR coupling metric 을 amplitude-correlation/PLV 계열 → **PLI (Phase Lag Index)** 또는 **wPLI (weighted PLI)** 로 교체.
- **threshold 신규 산정**: PLI/wPLI 는 [0, 1] range 이지만 분포가 PLV/r 과 다름 — synthetic fixture 재 emit 필요. 잠정 floor 후보 = **wPLI 0.10** (Vinck et al. 2011 신뢰 lower bound).
- **rationale**: 
  - PLI = `|<sign(Δφ)>|` (zero-lag 0-처리), wPLI = imaginary-cross-spectrum 가중. 둘 다 **volume conduction** (zero-lag synchrony) 에 immune.
  - F_PLVP_02 collapse (ica 0.993 / amica 0.999) 가 *volume conduction* 으로 의심되는 한, PLI/wPLI 는 그 구체적 의심 source 를 **직교 lever 로** 제거.
  - F_PLVP_01 ref-short 0.372 는 PLI/wPLI 에서 다른 값으로 mapping → real signal vs leak 분리 검증 가능.
- **단점**: hexa toolchain rewrite 필요 (`clm_eeg_p2_tlr_pre_register.hexa` 의 coupling 계산 logic 교체), synthetic fixture v2 emit, baseline (human PLI/wPLI 분포) 신규 reference 필요. 비용 ↑, 그러나 **honest reformulation**.
- **결론**: **권장 path** (§8 참조).

### 2.3 후보 C — Alternative Coupling Metric (PSI / MI / TE 중 택일)

P2 coupling 을 다음 중 하나로 교체:

- **C-1 PSI (Phase Slope Index)**: Nolte et al. 2008. directional, volume conduction immune. range ≈ [-1, 1]. floor 후보 = **|PSI| ≥ 0.05**.
- **C-2 MI (Mutual Information, Gaussian copula)**: nonlinear 일반화, range bits. floor 후보 = **MI ≥ 0.10 bits**.
- **C-3 TE (Transfer Entropy)**: directional + nonlinear, MI 의 lagged 확장. floor 후보 = **TE ≥ 0.05 bits**, **bias-correction 필수**.
- **장점**: post-hoc relax 아님, nonlinear/directional 정보 추가. P3 GCG (Granger causality) 와 부분 redundancy 발생 가능 → P2/P3 직교성 재검토 필요.
- **단점**: PLI/wPLI 보다 estimator variance 高 (특히 짧은 segment), surrogate testing 필수. hexa toolchain rewrite cost 가 후보 B 보다 큼. baseline 신뢰 reference 부족 (literature 분산 大).
- **결론**: 후보 B 가 부적합/불충분 시 fallback. C-1 PSI 가 가장 enticing (volume conduction immune + directional) 이나 P3 GCG 와 redundancy 검사 선결.

---


### 3.1 후보 A (downward 380→300) — falsifiers

- **F_A_01 ref-short stage**: ref-short real .npy 측정값 < **300** → fail (honest: 0.372 보고 0.30 으로 floor 내리는 것 자체가 의심).
- **F_A_02 ica/amica collapse**: ica_cleaned 또는 amica_fallback ≥ **0.95** → fail (volume conduction proxy, threshold 무관 적용).
- **F_A_03 synth/real divergence**: synthetic_16ch_v1 fixture clm_r ≥ 0.70 AND real ref-short clm_r < 0.45 → "fixture-only PASS" 판정 → fail.
  1. 0.30 의 *근거 없음* (어떤 cohort/baseline 에서 0.30 이 의미 있나?).
  2. ica_cleaned 0.993 collapse 는 floor relax 와 무관 — F_A_02 가 항상 trigger 될 가능성 高.
  3. 본 후보 채택 = "측정값에 맞춰 threshold 내림" — Popperian falsifiability 약화.

### 3.2 후보 B (PLI / wPLI) — falsifiers

- **F_B_01 wPLI ref-short**: ref-short real .npy 의 wPLI < **0.10** → fail.
- **F_B_02 wPLI ceiling collapse**: ica_cleaned 또는 amica_fallback wPLI ≥ **0.95** → fail (PLI/wPLI 도 ceiling collapse 가능 — saturated 시 의심).
- **F_B_03 PLI vs PLV divergence**: 동일 segment 에서 PLV ≥ 0.95 AND wPLI ≤ 0.05 → "volume conduction artifact identified" 판정 (F_B_03 trigger = 후보 B 의 *positive* validation, not failure).
  1. wPLI 0.10 floor 도 *post-hoc 적이지 않다는 보장 없음* — Vinck 2011 lower bound 인용 강제, otherwise 후보 A 와 동일 함정.
  2. Synthetic fixture (alpha-coupled gaussian) 에서 PLI/wPLI baseline 분포 사전 검증 필수 — 미검증 시 floor 무근거.
  3. PLI 는 짧은 segment (n < 256 sample) 에서 bias 大 — segment length 별 power analysis 필수.

### 3.3 후보 C (PSI/MI/TE) — falsifiers

- **F_C_01 PSI ref-short**: |PSI(ref-short)| < **0.05** → fail.
- **F_C_02 P3 redundancy**: corr(PSI, GCG) ≥ **0.85** across 16ch → "P2/P3 직교성 위반" → fail (후보 C 자체 reject, P2 와 P3 가 사실상 같은 측정).
- **F_C_03 surrogate test**: 50 IAAFT surrogate 의 PSI 분포 95-percentile ≤ real PSI 미달 → "PSI not above chance" → fail.
  1. PSI 의 0.05 floor 도 baseline 미정.
  2. P3 GCG 와 redundancy — 둘 다 directional → 같은 정보 측정 가능성 高 (F_C_02 가 trigger 되면 P2/P3 분리 의미 상실).
  3. MI/TE 는 estimator 선택 (Gaussian copula vs k-NN vs binning) 에 결과 의존 — estimator 미고정 시 reproducibility ↓.

---

## §4. Frozen Criteria 변경 Protocol (v1.1 → v2 bump)


본 spec 의 어느 후보든 채택 시 다음 sequence:

1. **decision lock-in**: 본 spec §5 결정 기준 통과 → 후보 X 확정. doc-level lock (이 doc 는 그대로 보존, 결정 결과는 별도 *decision marker* 로 emit).
2. **별도 file 발행**: `state/clm_eeg_pre_register_v2.json` (NOT in-place edit of `v1.json` or `v1_1.json`).
3. **hexa toolchain 갱신** (후보 B/C 시): `tool/clm_eeg_p2_tlr_pre_register.hexa` v2 — 후보 A 시 threshold 1 line만, 후보 B/C 시 coupling fn 재작성.
4. **synthetic fixture v2 emit** (후보 B/C 시): `fixtures/synthetic_16ch_v2.json` — 후보 B 의 PLI/wPLI baseline 분포 establish.
5. **falsifier set v2 emit**: §3 의 후보별 F_*_01~03 을 `state/clm_eeg_p2_tlr_pre_register_v2.json` 의 `falsifiers` array 로 명시.
6. **chain_sha256 재계산**: v2 의 (hexa + fixture + emitted JSON) 새 chain. v1.1 chain 과 별개로 보존.
7. **changelog md**: `docs/clm_eeg_pre_register_v1_1_to_v2_changelog.md` 발행 — 본 spec doc 을 §1 source 로 cite.
8. **chflags uchg + git commit dual-lock**: v1.1 patch 와 동일 protocol.
9. **D-day verify rerun**: real .npy 4 stage 에 대해 v2 falsifier set rerun. PASS/FAIL 결과를 honest 보고.

**위 9 step 중 하나라도 skip 시 v2 bump 무효 → spec 위반.**

---

## §5. 결정 기준 (post-hoc threshold change 회피 vs honest reformulation)

후보 채택 결정은 다음 5 기준 모두 통과 시에만:

1. **Popperian falsifiability 보존**: 후보의 floor 가 *측정값에 맞춰 내려진* 것이면 reject. 외부 reference (literature, prior cohort baseline) 인용 강제.
3. **P2/P3 직교성**: 후보 metric 이 P3 GCG 와 redundant 하면 reject (후보 C-1 PSI 의 F_C_02 risk).
4. **Reproducibility**: estimator 명시 + segment length / surrogate test protocol 명시. 미명시 시 reject.
5. **Cost-justified**: hexa rewrite + fixture v2 emit 비용이 결과 신뢰성 향상에 비례. 후보 A 는 cost 낮으나 (1) 위반, 후보 B 는 cost 中 + (1)(2) 통과, 후보 C 는 cost 高 + (3) risk.


---


본 spec doc 자체에 대한 falsifier (이 doc 가 잘못 작성되었을 가능성):

- **F_SPEC_01 — 후보 누락**: 후보 D (e.g., Cross-Frequency Coupling, Phase-Amplitude Coupling) 가 P2 TLR 의 alpha-band scope 안에서 더 적절함이 입증되면 본 spec 미흡 → revise.
- **F_SPEC_03 — 권장 path 의 cost over-estimate**: 후보 B (PLI/wPLI) 가 hexa toolchain 1 함수 교체로 충분함에도 본 spec 이 "rewrite cost 大" 로 부풀려 후보 A 를 fallback 으로 격상시키면 → bias 의심 → revise.

---

## §7. Trade-off Matrix

| 기준 | 후보 A (380→300) | 후보 B (PLI/wPLI) | 후보 C (PSI/MI/TE) |
|---|---|---|---|
| post-hoc 회피 (§5.1) | **fail** | pass | pass |
| volume cond 의심 해소 (§5.2) | fail | **pass** | pass (PSI/TE) |
| P2/P3 직교성 (§5.3) | pass | pass | risk (C-1 PSI) |
| Reproducibility (§5.4) | pass (trivial) | pass (Vinck protocol) | risk (estimator 분산) |
| Cost (hexa rewrite) | **low** | mid | high |
| F3 F_PLVP_01 대응 | partial (relax 만) | **direct** (다른 metric) | direct |
| F3 F_PLVP_02 대응 | none | **direct** (volume cond immune) | direct |
| 외부 reference 강도 | weak | **strong** (Vinck 2011) | medium-mixed |
| v2 bump 정당성 | data-dredging risk | **honest reformulation** | honest reformulation |
| 종합 | **reject 단독** | **권장** | fallback |

---

## §8. 권장 Path + 사유

### 8.1 권장 — 후보 B (PLI / wPLI)

**사유**:

2. **F3 두 falsifier 모두 직접 대응**: F_PLVP_01 (0.372 ref-short) → wPLI 로 다른 값 mapping. F_PLVP_02 (ica 0.993 / amica 0.999) → PLI/wPLI 는 zero-lag synchrony immune → volume conduction collapse 자동 식별.
3. **외부 reference**: Vinck et al. 2011 (NeuroImage) "An improved index of phase-synchronization" — wPLI 의 0.10 lower bound 신뢰 가능. 후보 A 의 "0.30 무근거" 와 대조.
4. **Cost-justified**: hexa toolchain `clm_eeg_p2_tlr_pre_register.hexa` 의 coupling 함수 1개 교체 (PLV → wPLI 의 imaginary cross-spectrum). 후보 C 보다 비용 낮음.
5. **P2/P3 직교성 보존**: PLI/wPLI 는 phase-only, P3 GCG 는 prediction-based → 직교.

### 8.2 Fallback — 후보 C-1 PSI (단, F_C_02 P2/P3 redundancy 사전 검증 통과 시)

후보 B 채택 후 D-day rerun 결과 wPLI 도 두 falsifier triggered 면, PSI (directional + volume cond immune) 로 escalate. 단 F_C_02 redundancy check 사전 필수.

### 8.3 후보 A 사용 조건

후보 B/C 모두 §5 결정 기준에 fail 입증 시에만, 그것도 *공식 v2 bump + 외부 reference + new falsifier set* 패키지 안에서만. 단독 채택 절대 금지.

### 8.4 다음 cycle (별도 작업)

- 본 spec 의 권장 (후보 B) 을 수신한 후, **별도 cycle** 에서 v2 bump §4 9-step protocol 실행.
- D+1 P1 LZ verify (별도 cycle) 와 조정 — composite ≥2/3 PASS 재 시도 시점.


본 spec 자체의 미입증 의심 (§9 항목 참조) 을 인정. 권장 path = 후보 B 는 *정당화 가능* 하나 *완전 입증 아님* — Vinck 2011 인용 1편 단독 의존, wPLI 0.10 floor 도 cohort-specific 검증 미수행, F_C_02 같은 redundancy 가 후보 B 에 존재할 가능성 (PLI vs PLV 가 동일 phase 정보 sub-set) 미배제.

---


1. **wPLI 0.10 floor 가 cohort-specific 검증 없이 외부 1 reference (Vinck 2011) 에 의존** — anima EEG hardware (OpenBCI Cyton 16ch) + d-day session conditions 에 대한 prior baseline 부재.
2. **후보 B 가 F_PLVP_02 (volume conduction) 를 "해소" 한다는 주장은 이론적** — 실제 ica_cleaned 0.993 collapse 가 PLI/wPLI 에서 어느 값으로 mapping 될지 *측정 전엔 미확인*. 권장의 (2) 사유는 inference 이지 observation 아님.
3. **본 spec 의 후보 enumeration (A/B/C) 이 exhaustive 하다는 보장 없음** — Cross-Frequency Coupling, Cross-Spectral Density, Granger Spectral, Phase-Amplitude Coupling 등 검토 미수행 (F_SPEC_01 risk).

---

## §10. Refs

- frozen v1.1: `anima-clm-eeg/state/clm_eeg_pre_register_v1_1.json`
- v1.1 changelog: `anima-clm-eeg/docs/clm_eeg_pre_register_v1_to_v1_1_changelog.md`
- P3 GCG falsified commit: `f27d6363f`
- Vinck M et al. (2011) "An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias", NeuroImage 55(4):1548-1565.
- Nolte G et al. (2008) "Robustly estimating the flow direction of information in complex physical systems", PRL 100:234101.
