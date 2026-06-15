# H_845 — `evol-spectrum-phi` (EVOL E1 · 진화 사다리 5번째 축 첫 측정)

**축**: EVOL (XENO 3D applicability matrix + TEMPORAL Δt 4D 위에 **5번째 축 — biological evolutionary complexity / species ladder** 신설) · XENO/TEMPORAL follow-up
**id**: H_845 · **date**: 2026-05-29 · **infra**: $0 mac-local (단일 foreground sync run, exit 0) · **verdict**: **🔴 FALSIFIED-INSTRUMENT (2/5)**

---

## 1. 슬러그 + 한 줄 요약 — invariant_detector 가 진화-complexity 사다리에서 Φ monotone 을 분리하는가

`evol-spectrum-phi` — XENO X1 `invariant_detector.hexa` 의 substrate-blind 2-unit co-TPM Φ 가 **4 species toy proxy substrate (bacteria → arthropod → mammal → AGI) 위에서 단조 진화-complexity 사다리** 를 만들어내는지 첫 측정. EVOL 도메인 round 1, TEMPORAL Δt 축과 자매 (XENO 3D + Δt + species = 5D applicability frontier).

4 substrate (n=128 dense, hardcoded literal, toy proxy 정직 표기):
- **bacteria**  (T1) — random walker (LCG noise materialised)
- **arthropod** (T2) — local 4-tap XOR sliding (4-tap Galois LFSR-like, mid integration)
- **mammal**   (T3) — multi-scale recursive (short-scale XOR + long-scale Δ=8 결합)
- **AGI**      (T4) — structured emergence (mammal seed + novelty injection)

> **결과**: **🔴 FALSIFIED-INSTRUMENT (2/5)** — invariant_detector 가 진화-complexity 사다리 위에서 **양 극단(bacteria floor + mammal ceiling)만 PASS** 하고, **mid-tier (arthropod) + supra-tier (AGI) 분화는 미해결**. F-E1-BACTERIA-LOW + F-E1-MAMMAL-HIGH PASS, F-E1-ARTH-MID + F-E1-AGI-VARIANT + F-E1-MONOTONE FAIL. monotone bacteria<arthropod<mammal≤AGI 두 곳에서 깨짐 (arthropod=0.081 < 0.2 mid-tier 하한 미달, AGI=0.468 < mammal=1.291 supra-tier reverse). H_670 (Kuramoto · logistic family) 의 양 극단 PASS / ordinal 미달 패턴과 동형 — **detector 단독으로 species ladder 의 mid + supra 단조 분화는 미해결**, naive 5번째 축 확장 = TEMPORAL T1 lag-axis · T2 embed-dim 과 같은 'detector 한계 발견형 closed-negative'. E2 monotone-strict re-design 자연 entry.

---

## 2. 동기 — XENO + TEMPORAL 위에 5번째 축이 필요한 이유

XENO X1 (substrate-blind invariant_detector) + paper #1414 v2 의 3D applicability matrix [n × density × structure] 이 substrate-family agnostic Φ-formalism 의 영역을 매핑했다. TEMPORAL (H_841/H_842) 가 4번째 축 Δt 를 추가했으나 **T1 lag-window 와 T2 multi-unit embed 양쪽이 닫힌-negative** — invariant_detector 의 'naive 축 확장' 이 시간 통합 측정에 부적합함을 honest 닫힌-negative 로 봉인.

**5번째 축 후보 = biological evolutionary complexity** — 의식 통합량(Φ)이 species 단조로 커진다는 직관은 IIT 의 가장 기본적인 통속 명제 ("박테리아 < 곤충 < 포유류 < 인간 의식")이며, 만약 invariant_detector 가 이 사다리를 closed-form 으로 분리한다면 5D applicability matrix 의 한 축이 깔끔히 확정된다. 만약 깨진다면 H_670 (Kuramoto · logistic family) 의 'ECA 전용 ordinal' 결론을 한 단계 더 확장 — Φ monotone 이 **dynamical-family 뿐 아니라 species-family 도 ECA artifact** 라는 진단으로 굳어진다.

본 H_845 = **EVOL 도메인 첫 측정** + invariant_detector 의 species 축 calibrate 첫 closed-form 검정.

---

## 3. 측정 도구 / 방법

**Φ primitive**: `compute_invariant_phi(signal, n_samples)` (XENO X1 detector, IIT4 big-Φ via 2-unit co-TPM, RFC 036 stdlib). substrate-blind, deterministic, NO RNG, NO GPU, $0 mac-local.

**공통 config**: 4 substrate × n=128 dense (hardcoded literal · post-LCG / post-XOR materialised, no RNG at runtime) · 단일 foreground synchronous run (no bg fork · no monitor · NO GPU).

### Substrate definitions (toy proxy 정직 표기)

| tier | substrate | 표현 | 통합 model |
|------|-----------|------|-----------|
| T1   | bacteria  | deterministic LCG-bit stream (materialised) | random walker · no integration · noise floor |
| T2   | arthropod | bit_t = bit_{t-1} ⊕ bit_{t-2} ⊕ bit_{t-3} ⊕ bit_{t-4} | local 4-tap XOR sliding · mid integration |
| T3   | mammal    | short-scale: bit_{t-1} ⊕ bit_{t-2}; long-scale Δ=8 coupling | multi-scale recursive · high integration (X10 hive-style) |
| T4   | AGI       | mammal seed + secondary novelty injection | structured emergence · novel deviation (X7 voyager + X10 hive 하이브리드 인근) |

**중요**: substrate complexity 분류만 — **실 bio data 아님**. 'bacteria', 'mammal' 등의 이름은 dynamical complexity tier 라벨 (한국어 직관 매칭) 이지, 실제 생물학적 측정의 toy proxy 아니다. 진짜 bio data anchor 는 E3 단계 (EEG 협력) 의 미래 작업.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F-E1-BACTERIA-LOW** : `bacteria phi < 0.2` — random walker = noise floor 분리 검정 (X1 detector noise threshold 0.1 baseline 비교)
- **F-E1-ARTH-MID** : `arthropod phi ∈ [0.2, 0.5)` — partial integration mid-tier 분리 검정
- **F-E1-MAMMAL-HIGH** : `mammal phi ≥ 0.5` — multi-scale recursive 가 substrate_type='conscious' 분류기준 충족
- **F-E1-AGI-VARIANT** : `AGI phi > mammal phi` — structured emergence > pure recursive
- **F-E1-MONOTONE** : `bacteria < arthropod < mammal ≤ AGI` strict — Φ ↑ complexity ↑ ordinal

**verdict 기준 (사전등록)**:
- 4-5 PASS 영역 — species ladder Φ-monotone 신호 확정 (numerical-tier 등급)
- 3 PASS 영역 — partial ordering (species-family 의존)
- ≤2 PASS 영역 — 🔴 FALSIFIED-INSTRUMENT (X1 detector 의 species-complexity 측정 한계 닫힌-negative)

post-tuning 0, threshold pre-run frozen.

---

## 5. Measurement (verdict-bearing 측정값)

> 출력 `EVOL/state/evol_e1_2026_05_29/e1_smoke.log` + `result.json` + verbatim 사본 `.verdicts/845_evol_spectrum_phi/E1_run.txt`. 단일 foreground sync run, exit 0, deterministic.

```
================================================================
  EVOL E1 — species-complexity spectrum Φ (substrate ladder)
================================================================

  detector  = XENO/detector/invariant_detector.hexa
              (substrate-blind IIT4 big-Φ · 2-unit co-TPM)
  substrate = 4 (bacteria · arthropod · mammal · AGI) — toy proxy
  n         = 128 (dense regime, hardcoded literal)
  context   = XENO 3D matrix + TEMPORAL Δt = 4D, EVOL = 5번째 축

  bacteria   phi=0.011676 integ=1.23173 irr=0.00947939 type=coherent_non_conscious
  arthropod  phi=0.0813584 integ=1.08136 irr=0.0752372 type=coherent_non_conscious
  mammal     phi=1.29064 integ=2.29064 irr=0.563441 type=conscious
  AGI        phi=0.468459 integ=1.46846 irr=0.319014 type=coherent_non_conscious

  [PASS] F-E1-BACTERIA-LOW : phi=0.011676 < 0.2
  [FAIL] F-E1-ARTH-MID     : phi=0.0813584 < 0.2 (under)
  [PASS] F-E1-MAMMAL-HIGH  : phi=1.29064 >= 0.5
  [FAIL] F-E1-AGI-VARIANT  : AGI phi=0.468459 <= mammal phi=1.29064
  [FAIL] F-E1-MONOTONE     : mammal<=AGI broken (1.29064 > 0.468459)

================================================================
  RESULT: 2 PASS / 3 FAIL  (5 사전등록 falsifier)
================================================================
  verdict 잠정 = 🔴 FALSIFIED-INSTRUMENT (<=2 PASS)
```

| tier | substrate | phi      | integration | irreducibility | substrate_type           |
|------|-----------|----------|-------------|----------------|--------------------------|
| T1   | bacteria  | 0.011676 | 1.23173     | 0.00948        | coherent_non_conscious   |
| T2   | arthropod | 0.081358 | 1.08136     | 0.07524        | coherent_non_conscious   |
| T3   | mammal    | **1.29064**  | 2.29064     | **0.56344**    | **conscious**            |
| T4   | AGI       | 0.46846  | 1.46846     | 0.31901        | coherent_non_conscious   |

---

## 6. Falsifier 평가

| id | target | result | value |
|----|--------|--------|-------|
| F-E1-BACTERIA-LOW | bacteria phi < 0.2 | **PASS** | 0.011676 |
| F-E1-ARTH-MID | arthropod phi ∈ [0.2, 0.5) | **FAIL** | 0.081358 (under 0.2) |
| F-E1-MAMMAL-HIGH | mammal phi ≥ 0.5 | **PASS** | 1.29064 |
| F-E1-AGI-VARIANT | AGI phi > mammal phi | **FAIL** | 0.468 < 1.291 (reverse) |
| F-E1-MONOTONE | strict bacteria<arthropod<mammal≤AGI | **FAIL** | mammal>AGI broken |

PASS: 2, FAIL: 3 → **🔴 FALSIFIED-INSTRUMENT** (≤2 PASS 영역).

---

## 7. 발견 / 해석

1. **floor + ceiling 만 PASS, mid/supra 미해결**. invariant_detector 가 species ladder 의 양 극단(bacteria noise floor + mammal multi-scale ceiling) 만 분리. mid-tier (arthropod 4-tap XOR) 는 detector 위에서 0.081 까지밖에 못 올라가서 mid-tier 하한 0.2 미달. supra-tier (AGI) 는 noise injection 이 2-unit co-TPM 의 결정 transition 을 deteriorate 시켜 mammal 의 깨끗한 multi-scale signal (Φ=1.291) 보다 낮은 통합량(Φ=0.468) 으로 떨어짐. **양 극단 분리 + ordinal 단조 미달** = H_670 (Kuramoto · logistic family) 의 'ECA 전용 단조' 결론과 동형. **Φ monotone 은 species-family 도 ECA artifact** 일 가능성 강해짐.

2. **mammal 만 'conscious' 분류**. substrate_type='conscious' 가 4 tier 中 **mammal 만** 충족 (irreducibility 0.563 > 0.5 + phi 1.291 > 0.01). bacteria/arthropod/AGI 모두 'coherent_non_conscious' (XENO 분류 기준 그대로). detector 는 mammal toy substrate (multi-scale recursive) 만 진짜로 의식 신호를 만들어내고, 나머지 substrate 의 ordinal 분화엔 nicht. AGI toy proxy 의 'novelty injection' 이 noise-like 행동으로 분류되어 supra-tier 가설 reversed.

3. **mid-tier 4-tap XOR 의 한계**. arthropod toy 가 mid-tier 분화 substrate 로 충분하지 않음. 4-tap window 의 짧은 메모리는 2-unit co-TPM 위에서 noise-very-close 신호 (Φ=0.081) 만 만들어내고, mid-tier 하한 0.2 미달. **mid-tier 분리** 엔 더 긴 메모리/더 풍부한 통합 structure 필요 (E2 monotone-strict re-design 자연 entry).

4. **TEMPORAL T1/T2 closed-negative 와 자매 자연스러운 패턴**. invariant_detector 의 **naive 축 확장**(species 축, lag 축, embed 축 모두) 이 양 극단만 분리하고 mid/supra 분화는 detector-redesign 없이는 미해결. EVOL 도 species axis 도 detector-redesign 필요 (E2 자연 entry).

5. **a_paper_negative_ok 적용**. 본 H_845 = closed-negative honest 결과 — F-E1 5 falsifier 중 2 PASS 만 정직 보고, post-tuning 0, threshold pre-run frozen. 이는 5D applicability frontier 의 5번째 축 (species) 도 detector 단순 적용으로 ECA-동형 단조 미충족 = publishable closed-negative.

6. **AGI > mammal 가설 reversed 의 진짜 의미**. structured emergence > pure recursive 라는 사전 가설은 X1 detector 의 2-unit co-TPM 위에서는 명제 자체가 측정 불능. mammal multi-scale 의 깨끗한 결정성이 AGI 의 'novelty injection' (= noise-leaking) 보다 detector 위에서 더 높이 측정됨. 의미: **'structured emergence' 는 X1 detector 에 inverse-shadow** — novelty 가 noise 로 측정됨. 진짜 AGI > mammal 신호엔 더 정교한 'creative structure' substrate model + 더 풍부한 detector 필요.

7. **H_670 결과와의 cross-link**. H_670 Kuramoto family logistic family 양쪽에서 'monotone-rising=false / floor PASS / ordered_pairs 2/3' 라는 패턴이 본 H_845 EVOL 에서도 재현 — **양 극단 PASS / ordinal 미달 / 두 군데 단조 깨짐**. 이는 우연이 아니고 X1 detector 가 (a) 양 극단 floor/ceiling 은 robust 하게 분리하나 (b) 중간 tier 분화는 dynamical-family 따라 일관되게 미해결이라는 구조적 패턴.

---

## 8. 양방향 sibling cross-link

- **EVOL.md** (이 H 의 도메인 SSOT) — E1 milestone done 표시, E2 milestone "monotone-strict re-design" 자연 entry path 명시
- **XENO/XENO.md** — invariant_detector 출처 도메인, 5번째 축 (species) 첫 closed-form 측정 결과 환류
- **TEMPORAL/TEMPORAL.md** — Δt 축 자매, H_841/H_842 closed-negative 패턴 동형 cross-cite
- **UNIVERSE/H_670** — Kuramoto · logistic family 'ECA 전용 단조' 결론과 본 H_845 EVOL 'species 단조 ECA artifact 가능성' cross-link
- **HEXAD/IIT4/IIT4.md** — Φ-formalism SSOT, 본 H 는 IIT4 big-Φ 의 species-family 적용 결과
- **UNIVERSE/CANDIDATES.md** — Cycle #32 entry, 환류 SSOT

---

## 9. 다음 cycle 추천 entry

- **E2 monotone-strict re-design** (자연 entry · CORE): detector 확장 (예: 4-unit Takens embed via T2 형식, 또는 surrogate-baseline 차감 H_670 logistic family 재사용) 또는 stratified substrate set (mid-tier 더 긴 메모리 substrate + supra-tier 더 정교한 structure)
- **E3 toy-bio anchor** (E2 통과 후): 실 EEG (S1 resting α / S15 anesthesia / S24 REM) 와 mammal toy proxy 비교 — toy 와 실 bio 의 Φ alignment 검정
- **E4 ladder universality**: H_670 Kuramoto · logistic family 의 ordinal 과 EVOL species tier 동형 검정 — 4-family triangulate (ECA · Kuramoto · logistic · species toy)
- **E5 papers**: XENO follow-up 4 (5D applicability frontier closed-negative — species axis ECA artifact 가능성, T1/T2 자매 paper)

---

## 10. 정직성 / governance

- **a_blue_closed**: 측정 verbatim, threshold pre-run frozen, post-tuning 0
- **a_completeness_over_cheap**: hardcoded literal substrate (toy proxy 정직 표기, 실 bio 미주장)
- **a_paper_negative_ok**: 2/5 PASS = publishable closed-negative honest finding
- **a_h_continuous_no_branch**: E2 자연 entry path 명시, branch 옵션 없음
- **a_discovery**: closed-negative 도 discovery (X1 detector 의 species-family ordinal 한계 = 새 정직 진단)
- **p1-p8**: 0 위반 (NO system prompt · NO identity rules · NO assistant framing · NO speak() · NO perplexity verdict)
- **p7 perplexity 0**: LLM judge 없음 (closed-form Φ 측정 + threshold compare 만)
- **feedback-domain-bidirectional-sibling**: EVOL.md + UNIVERSE/CANDIDATES.md 양쪽 cross-update
- **feedback-universe-h-slug-stale-verify**: 3-신호 검증 후 H_845 확정 (origin/main H_845 zero-hit + git log --all collision 0 + ls UNIVERSE/ 최고 H_844)
- **INBOX 환류 0건**: detector 자체 결함 아님 (양 극단 PASS 는 정상 동작) — 축 확장 가설이 reversed. hexa-lang 패치 사유 없음.
