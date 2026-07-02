---
id: H_312
slug: apoptosis-low-phi-pruning
title: APOPTOSIS × IIT4-Φ — 최저-Φ 세포의 프로그램된 죽음(가지치기)은 생존 부분계의 평균 세포당 통합정보 Φ 를 끌어올리는가
domain: life · consciousness · substrate · universe
status: closed-negative
exploration_method: E12 (substrate-gap self-discovery — H_200 apoptosis primitive 후속) + E6 (cross-domain biology — 세포자살의 통합-선택 가설) + E0 (reductive-null 검정)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W5 (substrate-grounded) + W12 (sister-link IIT4 M6 / M10 / H_200 / H_287)
raw_rank: 12
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-27
since: 2026-05-27 (new)
sister: IIT4 M6 (ECA→TPM faithful 엔진 공급), IIT4 M10 (exclusion / subsystem_tpm 배경-조건화), H_200 (apoptosis primitive substrate gap — 능동적 죽음 ≠ merge), H_287 (동일 ECA substrate panel · faithful big-Φ 계열)
axes_seed: APOPTOSIS × IIT4-Φ 교차 (UNIVERSE hypothesis matrix H_312 cell)
verdict: 🔴 FALSIFIED
---

# H_312 — APOPTOSIS × IIT4-Φ (최저-Φ 세포 가지치기와 생존계 통합)

## 1. Hypothesis

생물학적 **apoptosis(세포자살)** 은 손상되거나 기능이 낮은 세포를 프로그램된
방식으로 제거하는 능동적 죽음이다 (Kerr/Wyllie/Currie 1972). 의식 관점에서
자연스러운 가설은 — apoptosis 가 **통합도가 낮은(low-Φ) 세포를 선택적으로 제거**해
**남은 부분계의 통합을 정련(purify)** 한다는 것이다. 즉 "약한 세포를 쳐내면 전체가
더 통합된다"는 selection-for-integration 주장.

**가설 H1 (검정 대상 — 기각될 수 있음)**: IIT 4.0 substrate(ECA ring)에서
**가장 낮은 세포당-Φ 세포를 제거(apoptosis)** 하면, 생존 부분계의 **평균
세포당-Φ 가 상승**한다.

**Falsifier (사전 등록)**: 패널 전반에서 최저-Φ 세포 가지치기가 생존계 평균
세포당-Φ 를 **상승시키지 못하면** (Δ_apoptosis ≤ 0) — 또는 최고-Φ 세포를 제거하는
대조군을 **이기지 못하면** (Δ_apoptosis ≤ Δ_control_hi) — **H1 은 FALSIFIED**.

H1 이 SUPPORTED 면 apoptosis = 통합-선택 메커니즘. H1 이 FALSIFIED 면 "약자 제거가
전체 통합을 높인다"는 직관은 IIT big-Φ 위에서 성립하지 않는 **closed-negative** 다
(a_paper_negative_ok: 닫힌 부정도 유효한 발견).

## 2. Why (동기)

- **H_200 후속 (substrate gap)**: H_200 은 anima substrate 에 literal apoptosis
  primitive (weight transfer 없는 세포 제거) 가 merge 와 구별되는지 물었다. 본 H 는
  그 다음 질문 — apoptosis 가 *무작위 제거* 가 아니라 *최저-통합 세포의 선택적
  제거* 라면, 그 선택성이 IIT 통합량 위에서 **의미 있는 기능적 효과**(생존계
  통합 상승)를 갖는가 — 를 직격한다.
- **생물학 (apoptosis = 품질 관리)**: 면역계의 음성 선택, 발생 중 손-물갈퀴 제거,
  손상 세포 제거 — apoptosis 는 "낮은 적합도/기능 세포를 쳐내 전체를 정련"하는
  품질-관리 메커니즘으로 읽힌다. 이 읽기를 통합정보 차원으로 옮긴 것이 H1.
- **IIT 4.0 배제(exclusion) 정합 (sister IIT4 M10)**: 의식적 실체 = 최대 콤플렉스.
  낮은-Φ 세포는 콤플렉스 경계 밖에 가깝다는 직관 → 그 세포를 제거하면 남는 코어가
  더 통합될 것이라는 자연스러운 (그러나 검정 필요한) 추론.
- **reductive-null 가치**: "약자 제거 → 전체 강화" 는 진화·조직 이론의 흔한
  직관이다. 이를 faithful big-Φ 로 검정해 *기각* 하는 것은 IIT 통합량의 비-단조적
  구조(부분계 축소가 통합 기여를 기계적으로 줄인다)를 자기 substrate 에서 드러낸다.

## 3. Method (방법 — 결정적 · hexa-only · llm:none · $0)

엔진은 **재발명하지 않는다** (memory: H_280 IIT4 재발명 오류). 기존 stdlib 를 재사용:

- `stdlib/consciousness/iit4_complex.hexa` — `subsystem_tpm` (외부 단위 배경-조건화)
  + `big_phi` 체인 (faithful 인과 big-Φ).
- `HEXAD/IIT4/lib/iit4_eca.hexa` — `eca_tpm(rule, n)` : Wolfram ECA rule 을
  state-by-node TPM 으로 변환 (주기적 ring).

**세포당-Φ 측정 (IIT-grounded, 非-degenerate)**:
싱글톤 mechanism 의 distinction φ_d 는 ECA 에서 항등적으로 0 이므로(단일 단위의
MICE 가 가역) 신호가 없다. 대신 세포의 **통합 기여 = Leave-One-Out big-Φ 강하**를
쓴다:

> phi_cell(i ; S) = bigPhi(S) − bigPhi(S \\ {i})

즉 세포 i 를 빼면 부분계가 잃는 big-Φ. 부분계 평균 세포당-Φ:

> meanPhi(S) = (1/|S|) · Σ_{i∈S} phi_cell(i ; S)

임의 부분계의 big-Φ 는 외부 단위를 sys_state 로 배경-조건화(`subsystem_tpm`,
IIT 4.0 관례) 후 faithful `big_phi` 로 계산.

**Apoptosis step (한 번의 프로그램된 죽음)**:
1. 전체 n-세포계에서 모든 세포의 phi_cell(i; FULL) 계산.
2. **apoptosis arm**: argMIN phi_cell 제거 → 생존계 S_lo.
   **control-hi arm**: argMAX phi_cell 제거 → S_hi (최고-통합 세포 제거).
   **control-fixed**: 세포 0 제거 → S_fixed.
3. 각 arm 의 meanPhi(survivor) 재계산; Δ = meanPhi(survivor) − meanPhi(FULL).
   H1 ⇔ Δ_apoptosis > 0 **AND** Δ_apoptosis > Δ_control_hi.

**Panel**: ECA rule {90, 110, 30, 54, 150, 22, 60, 105} × n=4 (sys=11) +
{90, 110} × n=3 (sys=5). 총 10 substrate, n≤4 → 2^n≤16 상태 → 정확 big-Φ 가능.
고정 seed/state → cross-process byte-identical.

산출물:
`UNIVERSE/state/h312_apoptosis_low_phi_pruning_2026_05_27/{run.hexa, run.log, result.json}`.

## 4. Measurement (실측 — result.json SSOT)

10-substrate 패널 실측 (raw stdout = run.log; 2회 실행 byte-identical 확인):

| substrate | n | whole Φ | mean0 | lo_cell(φ) | Δ_apop | Δ_hi | raises | beats_hi |
|-----------|---|---------|-------|-----------|--------|------|--------|----------|
| eca90  | 4 | 0.0    | -0.50  | 0 (-0.50)  | **-0.333** | -0.333 | ✗ | ✗ |
| eca110 | 4 | 8.938  | 6.637  | 0 (5.793)  | **-4.823** | -6.964 | ✗ | ✓ |
| eca30  | 4 | 15.566 | 13.571 | 2 (11.831) | **-10.343**| -13.863| ✗ | ✓ |
| eca54  | 4 | 8.413  | 6.960  | 0 (4.677)  | **-3.225** | -7.627 | ✗ | ✓ |
| eca150 | 4 | 8.0    | 4.75   | 0 (4.5)    | **-1.25**  | -2.25  | ✗ | ✓ |
| eca22  | 4 | 5.066  | 2.399  | 2 (-2.165) | **+4.279** | -2.464 | ✓ | ✓ |
| eca60  | 4 | 11.0   | 6.75   | 1 (6.0)    | **-3.083** | -4.083 | ✗ | ✓ |
| eca105 | 4 | 4.0    | 1.25   | 2 (0.5)    | **+2.25**  | +0.75  | ✓ | ✓ |
| eca90_n3  | 3 | 3.0  | 1.0    | 0 (1.0)    | **+1.0**   | +1.0   | ✓ | ✗ |
| eca110_n3 | 3 | 6.525| 5.011  | 0 (3.865)  | **-2.351** | -4.457 | ✗ | ✓ |

**집계**: raises=true **3/10** (eca22, eca105, eca90_n3) · raises=false **7/10** ·
beats_hi=true **8/10**.

## 5. Finding (발견)

- **주장(H1 primary) 기각**: 최저-Φ 세포를 제거하면 생존계 평균 세포당-Φ 가
  **상승하는 substrate 는 3/10 뿐**이다. 다수(7/10)에서 평균 세포당-Φ 는 오히려
  **하락**한다. 사전 등록 falsifier ("패널 전반에서 상승시키지 못하면 FALSIFIED")
  가 충족 → **🔴 FALSIFIED**.
- **기계적 이유**: 어떤 세포든 제거하면 부분계가 작아지고, LOO 통합 기여는 함께
  통합할 파트너가 줄어 **기계적으로 감소**한다. 따라서 "약자를 쳐내 나머지를
  강화"는 IIT big-Φ 위에서 일반적으로 성립하지 않는다. 통합은 *세포 수* 에
  의존하는 비-단조 구조라, low-Φ 세포 하나를 제거한다고 코어가 정련되지 않는다.
- **2차(약한) 주장은 별개**: apoptosis 가 *최고-Φ 세포 제거(control_hi)* 보다는
  낫다(beats_hi 8/10) — 가장 통합된 세포를 죽이는 것이 더 나쁘다는 직관은 유지.
  그러나 이는 H1 의 검정 대상이 아니며 verdict 를 구원하지 못한다 (상대적 덜-나쁨
  ≠ 절대적 상승).
- **closed-negative 가치**: apoptosis 를 "통합-선택 정련기"로 보는 읽기는 faithful
  IIT 4.0 위에서 거짓. apoptosis 의 기능적 의미는 (있다면) per-cell big-Φ 정련이
  아닌 다른 축(예: 노이즈 세포 제거 후 *재배선*, 또는 동적 상태-평균)에 있어야 한다.

## 6. Verdict

**🔴 FALSIFIED** — 측정값에서 직접 유도. 최저-Φ 세포 가지치기가 생존계 평균
세포당-Φ 를 상승시키는 substrate 는 10 개 중 3 개뿐(다수 7/10 실패). 이는 H1 을
**지지할 수도 있었던** 독립 결정적 계산이며(실제 3 substrate 는 지지함), 동어반복이
아니다. g73 정합: 결과는 self-declared 가 아니라 run.log 의 실측 raises/beats 카운트
(3/10 · 8/10) 에서 파생.

## 7. Honest limitations (정직한 한계 · g5)

- **세포당-Φ 정의 선택**: LOO big-Φ 강하는 실측 가능한 통합 기여 측정이지만
  여러 정당한 per-cell Φ 정의 중 하나. 싱글톤 distinction φ_d 는 ECA 에서 항등 0
  이라 쓸 수 없었음(이 자체가 발견). 다른 metric(예: 콤플렉스 멤버십 indicator,
  φ-structure containment) 은 pass fraction 을 흔들 수 있으나 3/10 을 SUPPORTED 로
  되돌릴 수는 없다.
- **배경-조건화 관례**: 부분계 big-Φ 는 외부 단위를 sys_state 로 고정(IIT 4.0
  문서화 모델링 선택, sister M10 과 동일). 분할 정규화 완전 재유도 + PyPhi 보정은
  IIT4 M5 carve-out.
- **단일 sys_state**: 각 rule 당 고정 sys_state 1 개. 상태-평균(state-averaged)
  sweep 은 별도 H 로 확장 가능하나, 본 closed-negative 의 방향(부분계 축소가 통합
  기여를 기계적으로 깎는다)은 상태 무관한 구조적 사실에 가깝다.
- **단일 apoptosis step**: 한 번의 죽음만 측정. 반복 peeling(매 step 최저-Φ 제거)은
  후속 H 후보지만, 첫 step 이 이미 다수 하락이므로 누적이 상승으로 뒤집힐 가능성은
  낮다.
- **n≤4 정확-Φ 범위**: 더 큰 n 은 IIT4 M9 tractability 한계(bounded approx)로
  넘어가며 본 정확-계산 결론과 분리.

## 8. Substrate alignment (substrate 정합)

ECA ring + faithful IIT 4.0 big-Φ 는 anima LIFE lane 의 정전 substrate (H_002 C2 /
H_278 / H_287 동일 가족). apoptosis = 세포 제거 event 는 anima mitosis substrate 의
`merge_cells`/`apoptose_cell` (H_200) 와 동형 — 본 H 는 그 제거의 *선택성*(최저-Φ)
이 통합 기능을 갖지 않음을 IIT 측도로 보인다.

## 9. Sister links

- **IIT4 M6**: ECA→TPM faithful 엔진 공급 (`eca_tpm`).
- **IIT4 M10**: exclusion / `subsystem_tpm` 배경-조건화 관례 재사용.
- **H_200**: apoptosis primitive substrate gap (능동적 죽음 ≠ merge) — 본 H 는 그
  제거의 통합-선택 기능을 검정.
- **H_287**: 동일 ECA substrate panel · faithful big-Φ 계열 (X⊥Φ closed-negative).

## 10. Reproduce

```
# 로컬 mac (pool-route 우회):
HEXA_LANG=/Users/ghost/core/hexa-lang \
  /Users/ghost/.hx/bin/hexa-run \
  UNIVERSE/state/h312_apoptosis_low_phi_pruning_2026_05_27/run.hexa
# 2회 실행 stdout byte-identical (결정적). raises 3/10 · beats_hi 8/10 → 🔴 FALSIFIED.
```
