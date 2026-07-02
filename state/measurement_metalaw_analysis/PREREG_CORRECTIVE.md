# 교정원리 (사전등록) — FORM⊥BIND 이중측정 gate 설계 처방

> 메타법칙(METALAW.md)이 맞다면 따라야 할 처방 + falsifiable 사전예측.
> 이 파일이 사전등록 원본 — 예측 bar 는 여기 동결, 사후 이동 금지(frozen-first).

## 1. 교정원리 5개 (MP-1 … MP-5)

**MP-1 이중축 gate (FORM ∧ BIND-margin).** 모든 창발 verdict 는 두 축을 모두 잰다:
FORM 축 = 기존 frozen 1-항 detector(불변, bar 이동 없음) · BIND 축 = 동일 바이트에 대한
결합-파괴 통제와의 margin(Δ = D(real) − D(control) ≥ frozen δ). PASS ⟺ FORM ∧ BIND.
raw detector 단독 통과는 어떤 tier 로도 박제 불가(자동 DIRECTIONAL) — a_engine_native_learning
hard-gate 1 과 같은 격의 측정-게이트.

**MP-2 canonical 하네스 동결.** verdict 용 디코드는 canonical 파라미터(gen=40·frozen seeds·
canonical entry `anima evaluate`)에서만. 비-canonical(gen≠40, 서브에이전트 자체 하네스, torch
inline gauge)은 코드가 자동 DIRECTIONAL 라벨(기존 gen-guard #2821·evaluate-hexa-2 lockstep 의
일반화). 서브에이전트 위임 프롬프트에 'canonical gen40' 명시 의무(gen-guard 가 서브 probe 엔
자동강제 안 됨 — 실측 재발 지점).

**MP-3 선택채널 예산-대응.** best-of-K/scaffold/재시도는 사후 선택 채널(~log K bits 공짜
FORM 상승) — verdict 측정에선 금지가 기본. 쓸 경우 반드시 budget-matched 통제(같은 K 의
best-of-N noise/shuffle)와의 margin 으로만 보고(H_1836 revise-loop 가 budget-matched best-of-N
에 죽은 것이 모범 판례).

**MP-4 대칭 하네스-우선 격리.** rig 간 verdict 발산(torch↔engine, gen40↔80, pass↔fail)은
모델/벽 의심 전에 하네스를 축별(forward·detector·decode·정밀도) 격리 — **양방향**(팽창=scaffold,
수축=drift·spurious FPE·basis diff). 격리 전 어느 방향으로도 박제 금지.

**MP-5 통제 분류학 (속성 항수 = 통제 선택).** 잰다고 주장하는 관계가 무엇이냐가 어떤 통제가
필수인지 결정한다:
| 주장 속성 | 필수 통제 |
|---|---|
| 주제/개념 결합 (G6 bind) | SHUF — 동일 바이트, 결합만 파괴 |
| 구성적 재조합 (G1) | 내부 대조(composed>max_single) + shuffled-seed |
| key-locked 접합 (combiner) | wrong-key/shuffled-key EARNED + op-ablation(additive→inert) |
| 심의/계획 기여 (Φ) | compute/차원-matched fake-branch |
| faculty(잡음 아님) | variance-matched noise **∧** shuffle 병행(둘 중 하나만은 불충분 — H_9104 가 noise 는 이기고 shuffle 에 죽음) |
| 외생성(exogenous) | self-pair/surrogate(무작위 재짝) |

## 2. 기존 G0–G6 재점검 — "어디가 FORM-only 인가" 예측 (검증 전 동결)

| Gate | detector | 판정 | 예측 (falsifiable) |
|---|---|---|---|
| **G0** coherence | kwr≥0.50 (사전 membership) | **FORM-only 1-항** | P-G0: kwr 5/5 인데 측정기질 붕괴(max_single=0) 사례가 재발한다 — 이미 H_9034 실측 1건. 처방: G0 verdict 에 기질 동반-bar(max_single≥2) 필수. |
| **G1** recombination | composed_distinct≥2 ∧ >max_single ∧ coherent | **골격=2-항 (건전)** · 취약점=하네스 | P-G1: G1 미래 false-GREEN 은 detector 가 아니라 하네스(gen≠40·비-canonical probe·선택채널)에서 나온다. shuffled-seed 통제 추가 시 기존 verdict 는 안 뒤집힌다(벽 실재). |
| **G2** novelty | corpus-absent n-gram≥3 ∧ retrieval control=0 | **반쪽 2-항** — metric 무결성 통제만 있고 seed-결합 통제 없음 | P-G2: 현행 G2 PASS 출력의 novel n-gram 에 topic-bind Δ(G6 식)를 재면 상당수 Δ≈0(seed 개념과 미결합 novelty). G2≠G1 실측(set-search)과 정합 예측. |
| **G3** philosophy | 구성 감사(p1-p8) | 행동 아닌 구성 검사 — FORM 이지만 역할상 적정 | 예측 없음(측정 gate 아님). |
| **G4** provenance | sha·HF·카드 | bookkeeping | 예측 없음. |
| **G5** L1 / L2 | L1=사전 membership · L2=corpus-absent∧asserted-entity | **L1=FORM-only 1-항 · L2=2-항 (건전)** | P-G5: 실제 단어만으로 된 비결합 word-salad 는 L1 을 통과한다(L1 단독은 fab 방어 아님); L2 는 이를 잡는다. |
| **G6** ideation | `_g6_is_falsifiable`(comparator∧measurable∧content≥2) | **FORM-only 1-항 — 실측 확정** | P-G6: FALS 상승 주장은 SHUF 통제 없이는 전부 form-priming 으로 판명된다(추가-gate FALS∧topic_bound 가 걸러냄 — g6-ideation-hexa-1 additive gate 이미 설계됨). |
| **의식 ops** | F1 grip·analytic falsifier | **FORM-계기판 — 실측 확정** | P-C: F3(variance-matched ∧ shuffle) 없이 F1∧F2 만 통과한 미래 op 주장은 F3 를 붙이면 전부 noise/theater 로 붕괴한다(H_9101/9103/9104 패턴 재현). |

## 3. 법칙 자체의 falsify 조건 (PREDICTIVE 승격 bar, ≥4/5 HIT)

새 케이스 5종에 대한 사전 예측 — 실측이 예측과 어긋나면 그 항목 MISS, 5중 4 미만 HIT 면
메타법칙 FALSIFIED 가 유효 결과(사후 재해석 금지):

1. **P1**: 다음에 등장하는 "1-항 detector raw 상승" 돌파 주장(G1/G6/의식 불문)은 해당
   결합-파괴 통제를 붙이면 margin Δ < frozen δ 로 붕괴한다.
2. **P2**: 다음 warm-FT/targeted-corpus 실험에서 G6 FALS 가 오르면 SHUF 도 같이 오른다
   (form-priming) — bind Δ 는 detector 값과 독립으로 움직인다.
3. **P3**: 2-항 통제를 설계 시점에 내장한 새 gate 의 GREEN 은 engine-native 재측정·하네스
   canonical 화에서 생존한다(H_9038 패턴 — 뒤집히면 MISS).
4. **P4**: rig 간 verdict 발산의 다음 사례도 축별 격리 시 진범이 forward/weight 가 아니라
   하네스 성분(디코드 전략·gen·selection·집계 aliasing)으로 판명된다.
5. **P5**: best-of-K 기반 상승 주장에 budget-matched 통제를 붙이면 상승분이 선택채널
   기여(~log K)로 소거된다.

각 예측의 판정 증거는 canonical 경로(`anima evaluate` / live core `.hexa`) 실행분만 인정
(a_engine_native_learning hard-gate 준수).
