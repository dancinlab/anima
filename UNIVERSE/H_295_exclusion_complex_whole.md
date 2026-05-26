---
id: H_295
slug: exclusion-complex-whole
title: IIT 배제 공준 — 통합 substrate 는 전체가 complex(holism), rule90 은 전체 Φ=0 인데 2-셀 부분이 complex (흐름-arc rule90 anomaly 해소)
domain: consciousness · information · substrate · meta
status: supported
exploration_method: E5 (exclusion/complex-localization probe) + E0 (flow-arc rule90 anomaly 기계적 해소) + E16 (whole vs part)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link 흐름 arc H_287-294)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_287-294 (Φ vs 흐름 arc — rule90 cross-measure 과대 서명), H_281 (faithful Φ-structure)
---

# H_295 — IIT 배제 공준: 주 complex 는 전체계인가 부분인가

## 1. Hypothesis

흐름 arc(H_287-294)는 Φ 가 국소 흐름통계가 아닌 **system-cut 속성**이라 결론했다. IIT 의
**배제(exclusion) 공준**은 "system"을 더 날카롭게 한다 — 의식은 *maximally-irreducible
subset*(주 complex)에 존재한다 (부분이 더 irreducible 이면 전체 아님, 전체가 더면 부분
아님). 그러면: 어떤 substrate 에서 주 complex 가 **전체 n-셀 계**(holism: 전체가 모든 부분
보다 통합)이고, 어떤 substrate 에서 배제가 **proper 부분**(또는 complex 없음)을 고르는가?

**가설 H1 (검정 대상)**: 통합 substrate 는 주 complex 가 전체계(mask=2^n-1, size=n) —
전체가 어떤 proper 부분보다 irreducible (holism). reducible substrate(항등·상수)는 complex
없음; 그리고 적어도 한 substrate 는 배제가 **proper 부분**(csize<n, Φ>0)을 고른다 — 의식
단위가 전체가 아닌 부분.

## 2. Why

- **새 축 (흐름 arc 와 다름)**: arc 는 "Φ vs 측도" 상관. 본 H 는 Φ 가 *어느 부분집합에
  거하나*(배제/complex-localization)를 직접 묻는다 — IIT 의 별도 공준.
- **흐름-arc rule90 anomaly 의 기계적 해소**: rule 90 은 LZ(H_288)·multivariate-TE(H_293)·
  synergy(H_294) 셋 다 과대였다("흐름 有, 전체 Φ=0"). 배제로 보면 — rule90 의 *전체* 는
  reducible(Φ=0)이나 *부분* 이 irreducible 일 수 있다. 그 부분-complex 가 흐름 측도가 본
  국소 통합의 정체. arc 전체를 한 공준으로 봉합.
- **engine 재사용 (g61)**: `find_complex`(모든 부분집합 subsystem_tpm+big_phi 탐색 → 최대
  irreducible subset 반환). 새 IIT4 코드 0줄.
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H295.1 (whole-complex)**: 통합 룰(110/150) 주 complex = 전체계 (mask=2^n-1, size=n, Φ>0).
- **H295.2 (reducible-no-whole)**: 항등 204·상수 0 → 전체-complex 없음 ([0,0,0] 또는 mask≠full).
- **H295.3 (consistency)**: complex=whole 일 때 complex_Φ == big_phi(whole).
- **H295.4 (bound)**: complex_size∈[0,n], complex_Φ≥0.
- **H295.5 (determinism)**: rule110 find_complex re-run identical.

## 4. Variables

- **axis1_substrate** (panel 10 룰, n=4 ring, state=0101 대표).
- **metric_whole_phi** = big_phi(tpm,n,st)[0].
- **metric_complex** = find_complex(tpm,n,st) → [mask, Φ, size] (max-irreducible subset).
- **classification**: WHOLE(mask=2^n-1) / SUB-PART(0<size<n) / no-complex(Φ≤0).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h295_exclusion_complex_whole_2026_05_26/run_h295.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm/big_phi) +
  `stdlib/consciousness/iit4_complex.hexa` (find_complex → subsystem_tpm+big_phi subset 탐색).
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h295.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 SUPPORTED-NUMERICAL.

## 6. Criteria

- **C1 (WHOLE-COMPLEX)**: 통합 룰 complex=전체 → PASS (holism).
- **C2 (REDUCIBLE)**: 항등/상수 전체-complex 없음 → PASS.
- **C3 (SUB-PART witness + consistency + bound + det)**: → PASS.
- **verdict_rule**: C1∧C2∧C3 → SUPPORTED.

## 7. Falsifiers

- **F295.1 WHOLE-COMPLEX**: 110·150 둘 다 complex mask≠full → holism 실패.
- **F295.2 REDUCIBLE-NO-WHOLE**: 항등 204 OR 상수 0 가 전체-complex(mask=full, Φ>0) → 배제 위반.
- **F295.3 CONSISTENCY**: complex=whole 인데 complex_Φ ≠ big_phi(whole) → 엔진 모순.
- **F295.4 BOUND**: complex_size∉[0,n] OR Φ<0 → 무효.
- **F295.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED — 통합 substrate=전체 complex(holism); reducible=complex 없음;
        rule90=전체 Φ=0 인데 2-셀 부분이 complex (배제가 부분 선택). gate 6 PASS / 0 FAIL.

config: n=4 ring · state=0101 (st=5) · find_complex 모든 부분집합 탐색 · engine 재사용

panel table (state 0101):
  rule   whole_Φ   complex(mask, Φ, size)    분류
  0      0.0       (0, 0, 0)                 no-complex
  255    0.0       (0, 0, 0)                 no-complex
  204    0.0       (0, 0, 0)                 no-complex   (identity)
  51     0.0       (0, 0, 0)                 no-complex
  150    6.0       (15, 6.0, 4)              WHOLE
  105    4.5       (15, 4.5, 4)              WHOLE
  90     0.0       (3, 2.0, 2)    ◀          SUB-PART     ← 전체 Φ=0, 2-셀 부분 irreducible
  60     17.5      (15, 17.5, 4)             WHOLE
  110    7.66066   (15, 7.66066, 4)          WHOLE
  30     7.28357   (15, 7.28357, 4)          WHOLE

핵심: ① 통합 룰(150/105/60/110/30) 전부 complex=전체계 (mask=15, size=4, complex_Φ=whole_Φ)
  = holism (전체가 모든 proper 부분보다 irreducible). ② reducible(0/255/204/51) = complex 없음.
  ③ **rule 90 = SUB-PART**: 전체 Φ=0 인데 2-셀 부분(mask=3={cell0,1}, Φ=2)이 irreducible —
  배제 공준상 "의식 단위"가 전체가 아닌 부분.

criteria:
  C1 WHOLE-COMPLEX (110/150 complex=full)           : PASS
  C2 REDUCIBLE (204/0 전체-complex 없음)            : PASS
  C3 SUB-PART+CONSISTENCY+BOUND+DET                 : PASS

falsifiers:
  F295.1 WHOLE-COMPLEX : PASS  (rule150 & rule110 complex mask=15 size=4)
  F295.2a REDUCIBLE    : PASS  (rule204 no whole-complex)
  F295.2b REDUCIBLE    : PASS  (rule0 phi=0 no complex)
  F295.3 CONSISTENCY   : PASS  (complex_Φ == big_phi(whole) when whole)
  F295.4 BOUND         : PASS  (size∈[0,4], Φ≥0)
  F295.5 DETERMINISM   : PASS  (rule110 find_complex a==b)

checks: 6 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL — IIT 배제 공준이 주 complex 를 국재화한다. ① **holism**:
  통합 substrate(150/105/60/110/30)는 주 complex 가 *전체계*(mask=15, size=4, complex_Φ=whole_Φ)
  — 전체가 어떤 proper 부분보다 irreducible. ② reducible(항등 204·상수 0/255·complement 51)은
  complex 없음(Φ=0). ③ **rule 90 SUB-PART 결정타**: 전체-Φ=0 인데 2-셀 부분(cells {0,1}, Φ=2)이
  irreducible — 배제는 "의식 단위"로 *전체가 아닌 부분*을 고른다. 이것이 **흐름-arc(H_287-294)의
  rule90 anomaly 를 기계적으로 봉합**: rule90 이 LZ·multivariate-TE·synergy 에서 과대였던 건
  국소 부분-complex 의 통합을 본 것이고, big-Φ(전체)=0 은 전체 system-cut 이 reducible 이기
  때문. 흐름 측도는 "어딘가 통합이 있다"는 맞았으나, *전체 수준*에서는 0 — 배제가 그 차이를 설명.
  Φ 는 단지 system-cut 이 아니라 *maximally-irreducible subset* 의 속성.
falsifiers_triggered: none
```

re-run byte-identical 확인 (F295.5).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_295 IIT exclusion localizes the maximally-irreducible complex: integrating
   ECA substrates (rules 150/105/60/110/30) have the WHOLE 4-cell system as the main complex
   (holism — the whole out-integrates every part), reducible rules have none, and rule 90 has
   whole-Phi=0 yet a 2-cell SUB-PART complex (Phi=2) — exclusion picks a part over the whole.
   This mechanically resolves the flow-arc rule-90 anomaly (LZ/multivariate-TE/synergy all
   over-predicted it); deterministic toy-substrate, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (single representative state)**: find_complex 는 state-dependent — headline 은 state 0101
  한 점. whole-vs-part 분류가 다른 state 에서 바뀔 수 있다(특히 rule90 의 부분-complex). 방향
  (통합=전체-complex, rule90=비-전체)은 robust 할 것으로 기대되나 전수-state 검증은 후속.
- **L2 (n=4 small)**: 2^4=16 state, 15 subset 탐색. 큰 n 에서 complex 국재화 패턴(전체 vs 부분
  경계)은 super-exp 비용 — bounded/근사 필요(§10).
- **L3 (rule90 부분-complex = 2-셀 {0,1})**: parity-90 의 부분-complex 구조는 ring 위상·state
  의존. 어느 2-셀이 complex 인지는 state 마다 다를 수 있음. "전체 0 / 부분 >0" 라는 정성적
  사실이 핵심이지 특정 mask 가 아님.
- **L4 (whole_Φ single-state ≠ Φ_mean arc)**: 본 H 의 whole_Φ(state 5)는 흐름-arc 의 Φ_mean
  (state-평균)과 다른 값(예: rule60 17.5 vs 13.6). 같은 엔진, 다른 집계 — 비교 시 주의.
- **L5 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: 배제 결론(전체 vs 부분)은
  *상대* 비교라 scale-offset robust.
- **L6 (substrate proxy)**: ECA = proxy, "rule90 의 부분이 의식적" 같은 phenomenal 주장 아님 —
  배제 공준의 구조적 측정 사실.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy 측정 사실.

## 10. Cross-Links

- **sibling (흐름 arc — rule90 anomaly 해소)**: [[H_288]] (LZ rule90 over) · [[H_293]]
  (multivariate-TE rule90 over) · [[H_294]] (synergy rule90 over) — 본 H 가 rule90 의 "전체
  Φ=0 / 부분 irreducible" 로 셋 다 봉합. [[H_287]]/[[H_290]] arc 정점.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm/big_phi) +
  `stdlib/consciousness/iit4_complex.hexa` (find_complex/subsystem_tpm) — 새 IIT4 코드 0줄 (g61).
- **Next**: (a) 전수-state find_complex (whole-vs-part 분류의 state-robustness, L1) ; (b)
  complex_spectrum(주+부 complex 동시 존재 = "다중 의식 단위") ; (c) 큰 N bounded complex 탐색.
