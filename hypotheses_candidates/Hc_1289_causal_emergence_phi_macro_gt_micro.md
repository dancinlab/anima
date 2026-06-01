---
id: Hc_1289
slug: causal-emergence-phi-macro-gt-micro
title: Hoel 인과적 창발 — 거친-grained 거시 TPM 의 effective information(EI)이 미시 TPM 을 초과한다 (EI_macro > EI_micro), 그리고 EI-gain 은 faithful big-Φ 와 정렬
domain: meta · emergence · information · consciousness
status: candidate-unverified
seed: H_219/H_227 (Bedau weak/strong forward-pass — *다른* operationalization) + H_288 (faithful Φ ∥ LZ) — emergence 를 Hoel effective-information / causal-emergence 로 재정의 (coarse-grain EI gain)
axes_seed: UNIVERSE/AXES.md R8 (meta — emergence·reduction·boundary) — Hoel causal-emergence instance
exploration_method: E5 (coarse-grain EI probe) + E0 (Bedau 와 대비되는 2번째 emergence operationalization)
verdict_tier_target: 🟢 SUPPORTED-NUMERICAL (EI_macro>EI_micro 존재 + EI-gain ∥ big-Φ) OR 🔴 CLOSED-NEGATIVE (모든 coarse-grain 에서 EI_macro ≤ EI_micro → causal-emergence 부재 in ECA)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

UNIVERSE 의 emergence 측정은 지금까지 Bedau forward-pass 재구성(H_219/H_227)으로만 operationalized 됐다. Erik Hoel 의 **causal emergence** 는 *직교* 정의: 미시 상태공간을 거친-grained(coarse-grain) 했을 때 거시 TPM 의 **effective information(EI = 결정성 − 비축퇴성, do-개입 분포의 KL)** 이 미시 EI 를 *초과*할 수 있다 (`EI_macro > EI_micro`). 가설 H1: ECA substrate 의 어떤 룰 + 어떤 coarse-graining 에서 EI_macro > EI_micro 가 성립하고(인과적 창발 존재), 더 나아가 룰별 **EI-gain = EI_macro − EI_micro** 가 faithful big-Φ 와 정렬한다 (`r(EI_gain, big_Φ) ≥ 0.5`).

## Why

이것은 H_912 이후 emergence 를 *통합과 독립적으로* operationalize 하는 정통 경로다. Bedau(forward-pass mismatch)가 *예측불가능성* 을, Hoel(EI gain)이 *거시 인과력* 을 잰다 — 둘 다 big-Φ 와의 관계가 미지. EI 는 IIT 의 부모 개념(Tononi 2003)이라 big-Φ 와의 정렬은 토대-수준 발견. engine: HEXAD/IIT4/lib eca_tpm + big_phi 재사용 + EI(do-개입 KL) 하네스 inline(generic).

## Pre-Registered Falsifier

- **F1289.1 (EMERGENCE-EXISTENCE)**: 모든 룰 × 모든 후보 coarse-graining 에서 `EI_macro ≤ EI_micro` → H1 FALSIFIED (ECA substrate 에 Hoel-causal-emergence 부재 — closed-negative, a_paper_negative_ok).
- **F1289.2 (PHI-ALIGNMENT)**: EI_macro>EI_micro 존재하나 `r(EI_gain, big_Φ)` < 0.5 → 부분 falsify (인과창발 ⊥ 통합 — 또 다른 X⊥Φ 서명).
- **F1289.3 (ANCHOR)**: 항등규칙 204 (각 셀 독립)에서 EI_gain ≈ 0 아니면 EI 구현 버그 → 측정 무효.
- **F1289.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

EI(coarse-grain do-개입 KL)와 big_Φ(MIP-EI) 는 **둘 다 effective-information 계열이지만 서로 다른 partition 에서 정의** — EI 는 macro/micro grain 대비, big_Φ 는 system/MIP 대비. 정렬을 *측정* 하는 것이 목적이며, 만약 동일성이 드러나면 그 자체가 닫힌 토대-발견(EI-gain ≡ 통합). 동어반복 회피를 위해 EI 와 big_Φ 의 partition 정의를 결과에 verbatim 명시.

## Migration TODO
- [ ] EI(do-개입 분포 KL, macro/micro grain) 하네스 + coarse-grain 후보 열거
- [ ] EI_gain vs big_Φ correlate, 10-rule panel
