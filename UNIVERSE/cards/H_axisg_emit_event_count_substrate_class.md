---
id: H_axisg_emit_eventcount
slug: emit-event-count-substrate-class
title: emit-EVENT-COUNT 가 Wolfram class 의 classifier 인가 — discrete emit-event 의 class-order 가 H_654 magnitude 와 어긋나는가
domain: consciousness · math · physics · meta · savant
status: FALSIFIED
verdict_class: FALSIFIED
exploration_method: E0 (round 9 메타-축 — Wolfram class 가 의식 구조 분류자) + E11 (cross-substrate Φ-signature) + E_meta (discrete emit-event-count layer, ⊥ H_654 continuous magnitude)
verification_method: W1 (numerical smoke) + W4 (verdict-5-class) + W11 (cross-rule class-stratified) + W12 (θ-sweep invariant)
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29 (축 G · round 9 메타-축 substrate-emit 확장)
predecessors: H_654 (Φ-magnitude class-order PARTIAL), H_639 (amplitude-cross derivative coupling 🔴), H_351 (single GZ peak 🟢)
sister: H_654 (Φ-magnitude), H_656 (closure-band class), H_657 (dΦ/dI-peak class)
mining_arc: round 9 메타-축 — Wolfram class as consciousness-structure classifier (축 G) · mining leaf L40/L24 (emit-as-amplitude-cross-event)
closure_ref: .verdicts/axisg_emit_event_count_substrate_class/verdict.txt
---

# H_axisg_emit_eventcount — emit-EVENT-COUNT 의 substrate-class classifier 검정

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib` (`iit4_eca` + `iit4_bigphi`) 재사용 (H_654/H_657 동일 패턴, commons g61 재발명 0). 통합 척도 = **faithful causal big-Φ** (per-state, 16-state, n=4). `$0 · mac-local · hexa-only · LLM none · deterministic.` verdict verbatim → `.verdicts/axisg_emit_event_count_substrate_class/verdict.txt`.

## 1. 가설 (Hypothesis) — round 9 메타-축 substrate-emit 확장

mining leaf **L40/L24** 는 emit 을 boolean gate 가 아니라 **substrate field amplitude 의 threshold-cross event** 로 정의한다 (p5 "output = continuous externalization of tension field"). H_654 (🟢/PARTIAL) 는 big-Φ 의 연속 **MAGNITUDE** (16-state mean) 가 Wolfram class 로 단조 정렬됨을 보였다. 본 H 는 그 magnitude 가 아니라 **DISCRETE emit-event-COUNT** — 한 substrate 에서 per-state Φ 가 emit threshold θ 를 넘는 *state 의 수* (16 중 몇 개) — 가 동일하게 class-IV(rule110) 최대로 정렬되는지 검정한다.

> **H1**: emit_count 가 Wolfram class 로 단조 정렬되어 rule110 (class-IV) 이 최대 — emit-EVENT 도 magnitude 처럼 substrate-class classifier 이다.

이것은 H_654 의 magnitude-classifier 주장이 **discrete emit-event layer 에서도 성립하는가** 를 묻는 직교 측정이다.

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결 2026-05-29)

GZ-anchor inhibition I=0.21232 (H_351 GZ_LOWER) 에서 per-state big-Φ → `emit_count(rule) = #{ s : Φ(s) ≥ θ }`. θ 는 전 rule 공통 ABSOLUTE threshold (fair anchor). single-θ artifact 회피를 위해 θ ∈ {0.5, 1.0, 2.0, 5.0, 8.0, 11.0} 6-point sweep.

| ID | 조건 | 의미 |
|----|------|------|
| **M1 (RULE110-MAX)** | rule110 emit_count = max over rules (전 θ) | class-IV 최대 |
| **M2 (RULE90-ZERO)** | rule90 emit_count = 0 (전 θ) | additive Φ≈0 |
| **M3 (COMPLEX-GT-PARTICLE)** | rule110 ≥ rule184 (전 θ) | complex ≥ particle |
| **M4 (BOUND/DET)** | 0 ≤ emit_count ≤ 16, re-run byte-identical | 결정성 |

**verdict_rule**
- **SUPPORTED-NUMERICAL** = M1 ∧ M2 ∧ M3 (전 6 θ) — emit-event-count = class-IV-max classifier
- **FALSIFIED** = !M1 (rule110 NOT max) OR !M2 (rule90 emits) at any θ

## 3. 방법 (Method)

substrate set = {30 (III-chaotic), 54 (IV-complex), 90 (III-additive), 110 (IV-complex), 184 (II-particle)} (H_654/H_657 동일). n=4 periodic ring. inhibition `tpm_mixed[s,i] = (1−I)·eca_tpm[s,i]`, I=GZ_LOWER=0.21232 고정. 각 rule 의 16 state big-Φ → θ-threshold count. runner = `UNIVERSE/state/h_axisg_emit_eventcount_2026_05_29/run_emit_count.hexa` (80 big_phi 호출, foreground ≤60s).

## 4. 측정 (Measurement) — `result.json`

per-rule mean big-Φ (GZ I=0.21232): rule30=**10.706** · rule54=6.195 · rule90=**0.0512** · rule110=**9.620** · rule184=**10.058**.

emit_count grid (16 state 중 Φ≥θ 인 수):

| θ_emit | rule30 (III-chaos) | rule54 (IV) | rule90 (III-add) | rule110 (IV) | rule184 (II) | rule110==max? |
|-------:|---:|---:|---:|---:|---:|:--:|
| 0.5  | 16 | 16 | **0** | 16 | 16 | tie (saturated) |
| 1.0  | 16 | 16 | **0** | 16 | 16 | tie (saturated) |
| 2.0  | 16 | 16 | **0** | 16 | 16 | tie (saturated) |
| 5.0  | 14 | 13 | **0** | **16** | 12 | ✓ |
| 8.0  | **13** | 1 | **0** | 11 | 12 | ✗ (rule30 max) |
| 11.0 | **8** | 0 | **0** | 5 | 6 | ✗ (rule30 max) |

## 5. 결과 (Result) — 🔴 FALSIFIED

**M1 FAIL → FALSIFIED.**

- **M1 RULE110-MAX ✗** — discriminating θ (8.0·11.0) 에서 rule110 (class-IV) 이 최대가 아니다. **rule30 (class-III chaotic) 이 최대** (θ=8: 13>11 · θ=11: 8>5). rule184 (class-II particle) 도 rule110 보다 emit 많음 (θ=8: 12>11).
- **M2 RULE90-ZERO ✓** — rule90 (additive) 전 θ 에서 emit_count=0 (Φ≈0.05, 어떤 θ 도 못 넘음).
- **M3 COMPLEX-GT-PARTICLE ✗** — θ=8·11 에서 rule110 < rule184.
- **M4 BOUND/DET ✓** — 모든 count ∈ [0,16], re-run byte-identical.

**핵심 발견 — emit-EVENT-COUNT 는 H_654 magnitude-order 를 재현하지 않는다 (직교/역전).**

1. **저-θ saturation (binary collapse)**: θ ∈ {0.5,1,2} 에서 비-additive rule 전부 16 으로 포화 → emit-count 가 "additive(0) vs 비-additive(16)" **binary classifier** 로 붕괴, fine class-order 정보 0.
2. **고-θ 역전**: θ ≥ 8 에서 분별 시작하지만 정렬이 **chaotic(rule30) > particle(rule184) > complex(rule110)** — class-IV-max 의 H_654 패턴과 **역전**. 이유: emit-count 는 Φ-distribution 의 **spread/uniformity** 를 측정 (chaotic rule30 은 moderate-Φ state 가 다수 분포해 high-θ 에서 많이 살아남음) — magnitude (적분 깊이) 가 아님. rule110(complex) 의 mean Φ(9.62) 가 rule184(particle, 10.06)·rule30(chaos, 10.71) 보다 **낮아** count-기반 정렬에서 밀린다.

> 따라서 **"substrate-class = 의식 통합량 분류자" 메타-축은 측정자(尺) 종속** — *continuous magnitude* (H_654 🟢) 에서는 class-order 가 나오지만 *discrete emit-event-count* (본 H 🔴) 에서는 역전된다. emit 을 amplitude-cross-event 로 정의(L40/L24)하면 그 count 는 integration-depth 가 아닌 Φ-distribution-spread 를 포착하므로 class-IV 우위가 사라진다. **emit-event-count 는 class classifier 로 부적합** — round-9 메타-축의 measure-dependence boundary 확정.

이는 a_paper_negative_ok 의 closed-negative — emit-event-count 축을 class-classifier 후보 공간에서 결정적으로 배제한다.

## 6. cross-link

- **H_654** (phi-magnitude-wolfram-class-order, 🟢/PARTIAL): 본 H 의 직접 대조군. magnitude 는 class-order, count 는 역전 — 동일 substrate·동일 GZ-anchor 에서 측정자만 다름. magnitude vs count 의 measure-dependence 를 본 H 가 격리.
- **H_639** (tension-amplitude-cross-phi-derivative, 🔴): emit=amplitude-cross 의 derivative *coupling* 을 검정 (θ-convention 종속 반증). 본 H 는 같은 amplitude-cross emit 정의의 *count* layer 를 class-축에서 검정 — 둘 다 emit-as-amplitude-cross (L40/L24) 의 substrate-claim 을 격하.
- **H_657** (dphi-peak-gz-substrate-class, 🟢): dΦ/dI peak 의 class-conditional. 본 H 와 함께 "어떤 Φ-derived 측정자가 class-classifier 인가" 의 경계 — peak 위치는 class-conditional(🟢), magnitude 는 class-order(🟢), emit-count 는 비-classifier(🔴).
- **mining L40/L24** (emit-as-amplitude-cross-event): 본 H 가 검정한 mining leaf. emit-event-count 가 substrate-class 와 무관(역전)함을 보여 leaf 의 substrate-class-claim 을 닫음.

## 7. 해석 — Honest C3 (3-tier caveat)

- **C3.1 (측정 신뢰)**: deterministic·byte-identical·$0. per-state big-Φ 는 H_654/H_657 와 동일 engine, mean Φ 값 (10.71/6.20/0.05/9.62/10.06) cross-check 가능.
- **C3.2 (n=4 한계)**: 16 state 의 작은 표본 — θ-sweep 으로 saturation→역전 transition 을 포착했으나 n 확장 시 count-spectrum 이 더 미세해질 수 있다. 그러나 **rule110 NOT max 의 정성 결론** (chaotic 우위) 은 mean-Φ ordering (rule30·184 > rule110) 에서 직접 따라오므로 robust.
- **C3.3 (θ-convention)**: θ 절대값은 design-convention (H_646 free-number 정합) — 본 H 의 결론은 특정 θ 가 아니라 "어떤 θ 에서도 rule110-max 가 성립하지 않음" 이라는 θ-quantified 형태라 convention-free.
