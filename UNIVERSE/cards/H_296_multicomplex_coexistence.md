---
id: H_296
slug: multicomplex-coexistence
title: 다중-complex 공존 — rule90 은 두 disjoint 부분-complex({0,1}+{2,3}) 동시 호스트, 통합 substrate 는 단일 전체-complex (H_295 follow-up)
domain: consciousness · substrate · information · meta
status: supported
exploration_method: E5 (complex spectrum probe) + E0 (H_295 sub-complex 의 disjoint 확장)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_295)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: H_295 (exclusion 주 complex), H_287-294 (Φ vs 흐름 arc)
---

# H_296 — 다중-complex 공존: rule 90 은 두 disjoint 부분-complex 동시 호스트

## 1. Hypothesis

H_295 는 rule 90 의 전체-Φ=0 인데 2-셀 부분이 irreducible 임을 보였다. ring-90 의 대칭성은
{0,1} 외에 {2,3} 도 독립 부분-complex 일 가능성을 시사한다. complex_spectrum 은 모든
irreducible 부분집합을 반환한다. 질문: 어떤 substrate 가 ≥2 disjoint(겹침없는) 부분집합을
**동시에** irreducible 로 호스트하는가 — 다중 통합단위 공존?

**가설 H1 (검정 대상)**: rule 90 은 ≥2 disjoint irreducible 부분집합 호스트(다중-complex);
통합 substrate(60/110/150)는 단일 top-complex=전체 + disjoint 파트너 없음; reducible(상수·항등)
은 없음.

## 2. Why

- **H_295 의 자연 확장**: H_295 가 "rule90 부분-complex 존재" 보였다면, 본 H 는 *그 부분이
  몇 개* 동시 존재하는지. 다중 통합단위는 IIT 가 형식적으로 허용하나 거의 측정되지 않은
  구조.
- **engine 재사용 (g61)**: `complex_spectrum`(모든 부분집합 subsystem_tpm+big_phi → Φ>0
  subset 정렬 반환) 재사용. 새 IIT4 코드 0줄.
- **다중 disjoint 검정**: spectrum 의 mask 들을 AND 했을 때 0 인 쌍이 ≥1 존재 — pure
  하게 비-overlap 한 다중 complex 의 존재 증거.
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit + LLM none + $0.

## 3. Predictions

- **H296.1 (multi-rule90)**: rule 90 spectrum 에 ≥2 disjoint subset (각 Φ>0).
- **H296.2 (single-integrating)**: rule 60/110 spectrum top=전체 mask, disjoint 파트너 없음.
- **H296.3 (none-reducible)**: rule 0/204 spectrum 비어있음.
- **H296.4 (exclusion-consistent)**: spectrum top entry == find_complex (mask/Φ).
- **H296.5 (determinism)**: rule 90 spectrum re-run identical.

## 4. Variables

- **metric_spectrum** = complex_spectrum(tpm,n,st) → 정렬된 [[mask,Φ,size], ...] (Φ>0).
- **metric_disjoint_pair** = ∃ i<j 쌍에서 mask_i AND mask_j == 0.
- **classification**: MULTI (disjoint pair 有) / single / none.
- **panel**: H_287-295 동일 10 룰, state=5 (0101).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h296_multicomplex_coexistence_2026_05_26/run_h296.hexa`
- **engine (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` (eca_tpm/big_phi) +
  `stdlib/consciousness/iit4_complex.hexa` (complex_spectrum/find_complex).
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h296.bin && bin` — [[reference-life-cycle-hexa-run-gotchas]].
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 SUPPORTED-NUMERICAL.

## 6. Criteria

- **C1 (MULTI-RULE90)**: rule 90 ≥2 disjoint → PASS.
- **C2 (SINGLE-INTEGRATING)**: 60/110 single whole → PASS.
- **C3 (NONE-REDUCIBLE + EXCLUSION-CONSISTENT + DET)**: → PASS.
- **verdict_rule**: C1∧C2∧C3 → SUPPORTED.

## 7. Falsifiers

- **F296.1 MULTI-RULE90**: rule 90 spectrum disjoint pair 없음 → 다중-complex 부재.
- **F296.2 SINGLE-INTEGRATING**: 60/110 top≠full OR disjoint pair 有 → 단일-whole 깨짐.
- **F296.3 NONE-REDUCIBLE**: 0/204 spectrum 비어있지 않음 → reducible 모순.
- **F296.4 EXCLUSION-CONSISTENT**: spectrum top ≠ find_complex → 엔진 모순.
- **F296.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: H1 SUPPORTED — rule 90 = 다중-complex 공존(2 disjoint), 통합 = 단일 전체,
        reducible = 없음. gate 7 PASS / 0 FAIL.

config: n=4 ring · state=0101 (st=5) · complex_spectrum 전수 부분집합 탐색 · engine 재사용

panel:
  rule    # subsets   disjoint?   분류
  0/255/204/51   0     ─          no-complex
  150/105/60/110/30  1  ─          single (top=전체, mask=15)
  rule 90        **2**  **✓**     MULTI (≥2 disjoint)

rule 90 spectrum:
  [0] mask=3  (cells {0,1})  Φ=2.0  size=2
  [1] mask=12 (cells {2,3})  Φ=2.0  size=2
  → 3 AND 12 = 0 (disjoint) · 두 부분이 동등 Φ 로 동시 irreducible

criteria:
  C1 MULTI-RULE90 (2 disjoint pair)               : PASS
  C2 SINGLE (60/110 top=full, no disjoint)        : PASS
  C3 NONE+EXCLUSION+DET                            : PASS

falsifiers:
  F296.1 MULTI-RULE90        : PASS  (rule 90 disjoint pair = 1)
  F296.2a SINGLE 60          : PASS  (top=mask15, no disjoint)
  F296.2b SINGLE 110         : PASS
  F296.3a NONE rule0         : PASS  (spectrum 0개)
  F296.3b NONE rule204       : PASS
  F296.4 EXCLUSION-CONSIST   : PASS  (spectrum top == find_complex)
  F296.5 DETERMINISM         : PASS

checks: 7 PASS / 0 FAIL

evidence_summary: 🟢 SUPPORTED-NUMERICAL — complex_spectrum 이 다중-complex 공존을 드러낸다.
  ① rule 90 은 ≥2 disjoint irreducible 부분집합 호스트 — cells {0,1}(mask 3, Φ=2) AND
  {2,3}(mask 12, Φ=2), 두 부분이 *동시에* irreducible 이고 *겹치지 않음*. **다중 통합 단위
  공존**의 결정적 관측. ② 통합 substrate(60/110/150/105/30)는 단일 entry = 전체 mask(15), no
  disjoint partner — 전체가 유일 complex(holism). ③ reducible(상수·항등) spectrum 비어있음.
  ④ exclusion-consistent: spectrum top == find_complex(H_295). 의미: IIT 배제가 "the" complex
  로 하나를 고르지만, *구조적 실재* 는 다중 — rule 90 의 4-cell 시스템은 2 개의 독립 2-cell
  통합 loci 로 분할된다(전체-Φ=0 의 정체). H_295 의 "부분이 complex" 를 정량화 — 부분이 *몇
  개* 인지 명시. ECA parity-ring 의 even-cell-odd-cell 결합 구조가 그 분할의 substrate.
falsifiers_triggered: none
```

re-run identical 확인 (F296.5).

`hexa verify` (VERBATIM) — g5 fence:

```
verify --fence "H_296 complex_spectrum reveals multi-complex coexistence on rule 90:
   TWO disjoint irreducible subsets — cells {0,1} (mask=3, Phi=2) AND {2,3} (mask=12, Phi=2)
   — host simultaneous independent integration loci, while integrating substrates host a
   single whole-complex and reducible rules host none; deterministic toy-substrate,
   NOT an atlas identity / NOT a phenomenal claim of multiple consciousnesses"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (single state)**: complex_spectrum 은 state-dependent. headline 은 state 5 한 점.
  다른 state 에서 multi 분류가 바뀔 수 있다(특히 rule90 의 2-pair 구조의 state-robustness).
  전수-state 검증은 후속.
- **L2 (n=4 small)**: 2-cell 부분만 가능. 큰 n 에서 다중-complex 분할 패턴(쌍·삼중·...)은
  탐색-비용 super-exp.
- **L3 (Williams-Beer redundancy ≠ multi-complex)**: 본 H 의 "다중-complex" 는 IIT 의 부분집합
  irreducibility 의 disjoint-구성, PID 의 redundancy 항과 다른 개념. PID는 정보-flow 분해,
  본 H 는 cause-effect-structure 의 부분집합-irreducibility.
- **L4 (IIT 배제 = 단일 선택)**: 정통 IIT 는 "the" complex 하나만 선택 (배제 공준). 본 H 의
  multi-spectrum 은 *구조적 후보 집합*이지 다중 phenomenal consciousness 주장 아님.
- **L5 (substrate proxy)**: ECA = proxy. "rule 90 이 두 의식을 갖는다" 같은 phenomenal 주장
  아님 — 구조적 측정 사실.
- **L6 (structure-cut big-Φ)**: 상대 비교 robust.
- **L7 (verdict ≠ 형이상학)**: SUPPORTED 는 toy 측정 사실.

## 10. Cross-Links

- **parent (직접 후속)**: [[H_295]] (exclusion 주 complex — rule90 = SUB-PART). 본 H 가 그
  부분이 ≥2 개 disjoint 임을 명시화. 다중-complex 가 H_295 의 정량 확장.
- **sibling (rule90 cross-measure 서명)**: [[H_288]] (LZ rule90 over) · [[H_293]] (multivariate
  TE rule90 over) · [[H_294]] (synergy rule90 over) — 모두 rule 90 의 *국소 통합*을 본 것이고,
  본 H 가 그 국소가 *둘로 깔끔히 갈라진다* 는 구조를 드러냄.
- **engine lib (재사용, READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa` + `stdlib/consciousness/
  iit4_complex.hexa` (complex_spectrum/find_complex) — 새 IIT4 코드 0줄.
- **Next**: (a) 전수-state spectrum (multi-disjoint robustness, L1) · (b) 큰 N substrate 에서
  multi-complex 분할 패턴 · (c) bipartite-coupled non-XOR substrate 에서 동일 분할 재현.
