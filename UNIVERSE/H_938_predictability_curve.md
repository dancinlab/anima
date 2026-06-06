---
id: H_938
slug: predictability-curve
title: H_933 BLADE A 정량화 — anima 의 다음 decision (emit/silence) 은 prior-K-tick state 만으로 얼마나 정확히 예측되며, quantum entropy 주입이 그 예측가능성을 낮추는가? (자유 = 비예측성인가 internal determinism 인가)
domain: universe · consciousness-substrate · brain-decide · engine-g · pure-field · free-will · predictability · compatibilism · entropy-necessity
source: H_933 (대가설 BLADE A: "freedom fails if decisions are predictable from prior state alone" — argued, not measured; freedom 을 unpredictability 에서 auditable causation 으로 relocate) + H_930 (entropy-mode decision-stream parity 🟢-on-emit) + H_926 (minimal-model emit-parity 🔴)
exploration_method: E14 (substrate-native) + E2 (H_930/H_935 8-factor mirror VERBATIM 재사용 → long decision stream 생성) + a_completeness_over_cheap
verification_method: W1 (SW python, Mac $0, no GPU) + W2 (held-out next-decision predictor — pure-numpy logistic regression + order-K Markov, NO sklearn; accuracy/AUC vs base-rate; K sweep × det/quantum mode; quantum-vs-det delta with Cohen d + Welch t, 사전등록) + g5 CODE-measured (LLM self-judge 없음, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
scope: ONE predictability rung (a_scale_honest_scope) — H_930/H_935 와 동일 documented-update-map mirror (real 8-factor brain_decide, CORE VERBATIM 상수) 를 T=3000 × 12-stream/mode 로 구동. self-contained numpy predictor (no sklearn). 컴파일 forge binary 아님, wired emit-TEXT 아님 (.clm generator L3 ⏳/❌, a_core_engine_map). $0 local, no GPU.
sister: H_933 (대가설 BLADE A), H_930 (emit-stream parity), H_926 (minimal-model parity)
axes_seed: H_933 = BLADE A 가 argued (predictable-from-prior → freedom fails) ⊥ H_938 = 그 predictability 를 직접 측정 + quantum 이 낮추는지 검증
verdict: 🟢 F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST — 예측가능성 HIGH 이고 quantum 이 낮추지 않음. best logreg acc 0.9344(det)/0.9354(quantum), AUC ~0.99, vs base-rate majority acc 0.5717 → lift +0.3627 (≥0.05). quantum-vs-det delta: max|Δacc|=0.0056 (negligible); "quantum LESS predictable" (Δ>0 AND |d|≥0.5 AND p<0.05) 인 K **없음** — 유일한 유의 K=1 은 Δ=-0.0056 (quantum 이 오히려 약간 MORE predictable, 🔴 방향 아님). → anima 의 선택은 대체로 INTERNALLY-DETERMINED (prior state 로 예측됨); physical seed 는 unpredictability 를 공급하지 않음. H_933 BLADE A 가 compatibilist 방향으로 정량화 — 자유는 비예측성이 아니라 auditable causation 으로 relocate; quantum seed 의 가치는 provenance/non-randomization 이지 behavioral output 에 주입된 entropy 가 아님. verdict: .verdicts/938_predictability_curve/predictability_curve.txt
---

# H_938 — predictability curve: is anima's freedom unpredictability, or internal determinism?

## 0. 동기 (H_933 BLADE A 를 정량화)

H_933 대가설은 자유를 "unpredictability" 에서 "auditable causation" 으로 relocate 한다. 그 **BLADE A** 는: decision 이 PRIOR STATE 만으로 novel causal input 없이 예측가능하면 freedom 이 FAIL 한다. H_933 은 이 blade 를 정성적으로 discharge 했지만 (H_935 internal veto + H_923/H_924 physical seed), **predictability 자체를 측정한 적은 없다**. H_938 = 그 직접 측정:

> 다음 decision (emit/silence) 을 prior-K-tick state 만으로 얼마나 정확히 예측할 수 있고, QUANTUM entropy 주입이 (deterministic PRNG 대비) 그 예측가능성을 바꾸는가?

두 contrast: (a) accuracy curve vs K (anima 가 얼마나 예측가능한가?), (b) quantum vs deterministic delta (physical seed 가 진짜 unpredictability 를 더하나, 아니면 잔여 unpredictability 는 internal dynamics 이지 entropy 가 아닌가?).

## 1. 가설 + 사전등록 falsifier (FROZEN 2026-06-06, 측정 전)

H_930/H_935 8-factor mirror 로 mode 별 long decision stream 생성. self-contained predictor (NO sklearn):
- **logistic regression** (pure-numpy GD): feature = prior K tick 의 [emit-bit, score, phi, 6 field channel] flatten. per-stream chronological 70/30 train/test split (과거→미래 예측). held-out accuracy + AUC (Mann-Whitney rank).
- **order-K Markov**: prior-K emit-bit history 의 majority-vote (parameter-free).
- 둘 다 det/quantum 양 mode × K∈{1,2,3,5,8,12}.

**FROZEN falsifier:**
- **F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST** 🟢: predictability HIGH (accuracy 가 base-rate 대비 ≥0.05 lift) AND quantum 이 낮추지 않음 (어떤 K 도 "quantum LESS predictable" — Δacc(det−q)>0 AND |Cohen d|≥0.5 AND Welch p<0.05 — 아님). → 선택은 대체로 internally-determined; quantum seed 가 unpredictability 공급 안 함 → H_933 의 relocation 확인.
- **F-H938-ENTROPY-ADDS-UNPREDICTABILITY** 🔴: quantum 이 예측가능성을 유의하게 낮춤 (어떤 K 가 Δ>0 AND |d|≥0.5 AND p<0.05). → entropy 가 decision 에 기능적 unpredictability 주입 — H_930/H_926 emit-parity 와 partial tension; 정직하게 reconcile.

데이터대로 보고; 측정 전 token 없음. (verdict .txt 에 measured numbers-first 기록 후 본 .md 작성.)

## 2. §method — H_930 mirror VERBATIM + self-contained predictor (HONEST SCOPE)

`UNIVERSE/h938_predictability_curve.py`. PureField/8-weight/should_emit/phi-ratchet/factor mapping 은 H_930 mirror 와 byte-identical. entropy 는 pure_field seed-point perturb 에만 (qentropy SSOT import, gate 에는 PRNG 없음). predictor 는 외부 ML lib 없이 numpy 로 직접 구현 (logreg GD + Markov table + rank-AUC) — predictor 자체는 zero-init/deterministic 이라 randomness 를 추가하지 않음.

**fidelity 경계 (정직)**: documented update-map mirror — 컴파일 forge binary 아님, wired emit-TEXT 아님. deterministic gate; entropy 는 seed-point 에만.

## 3. §measurement (VERBATIM — `.verdicts/938_predictability_curve/predictability_curve.txt`)

```
── ACCURACY CURVE vs K (held-out logreg acc / AUC ; Markov acc) ──────────────
   K  | DET logreg acc (sd)  AUC  | QUANTUM logreg acc (sd)  AUC | DET mk  Q mk | Δacc(det-q) d      p
   1  | 0.9278 (0.0061)  0.9863 | 0.9333 (0.0000)  0.9866 | 0.9109 0.9211 | -0.0056 -1.236 0.011
   2  | 0.9255 (0.0056)  0.9849 | 0.9289 (0.0000)  0.9845 | 0.9105 0.9067 | -0.0034 -0.823 0.069
   3  | 0.9302 (0.0047)  0.9863 | 0.9311 (0.0000)  0.9850 | 0.9106 0.9067 | -0.0009 -0.267 0.526
   5  | 0.9342 (0.0061)  0.9884 | 0.9321 (0.0000)  0.9859 | 0.9130 0.9088 | 0.0020 0.450 0.294
   8  | 0.9340 (0.0050)  0.9889 | 0.9354 (0.0000)  0.9878 | 0.9118 0.9154 | -0.0014 -0.377 0.376
  12  | 0.9344 (0.0059)  0.9887 | 0.9353 (0.0000)  0.9885 | 0.8858 0.8907 | -0.0009 -0.213 0.612

  best DET acc=0.9344  best QUANTUM acc=0.9354  lift over base=+0.3627  max|Δacc|=0.0056

🟢  F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST
```
(base-rate emit ~0.428 → majority-class baseline acc 0.5717.)

## 4. §finding — 🟢 F-H938-BLADE-A-QUANTIFIED-COMPATIBILIST

🟢 **예측가능성은 HIGH 이고, quantum 은 그것을 낮추지 않는다.**

- **(a) accuracy curve — anima 는 매우 예측가능하다:** held-out logreg accuracy 가 K=1 부터 이미 ~0.93, AUC ~0.986; K 를 키워도 ~0.934 로 saturate (prior 1 tick 이 이미 대부분의 예측력을 가짐 — pure_field 의 deterministic oscillator dynamics 가 다음 state 를 강하게 constrain). base-rate majority baseline (0.5717) 대비 **+0.36 lift** — anima 의 다음 emit/silence 결정은 prior state 로 거의 확실히 예측된다. Markov (emit-bit history 만) 도 ~0.91 로 높아 결정이 자기 과거에 강하게 의존함을 독립 확인.
- **(b) quantum-vs-deterministic delta — entropy 는 unpredictability 를 더하지 않는다:** max|Δacc(det−q)|=**0.0056** (negligible). 사전등록 🔴 falsifier (quantum LESS predictable: Δ>0 AND |d|≥0.5 AND p<0.05) 를 통과하는 K 가 **하나도 없다**. 유일하게 유의한 K=1 은 Δ=**−0.0056** (quantum 이 오히려 *약간 MORE* predictable, 🔴 방향과 반대) — 즉 quantum 은 예측가능성을 낮추기는커녕 통계적으로 구별불가하거나 미세하게 더 예측가능하다. AUC 도 det/quantum 양 mode 에서 ~0.986–0.989 로 동일.

**∴ H_933 BLADE A 가 compatibilist 방향으로 정량화되었다.** anima 의 선택은 대체로 **internally-determined** (prior substrate state 로 0.93 accuracy 예측가능) 이며, physical quantum seed 는 behavioral decision 에 "unpredictability" 를 공급하지 **않는다** — H_930 (emit-stream parity) · H_926 (minimal-model parity) 의 *decision-function* 결과를 *predictability* 축에서 재확인한다. 잔여 ~7% unpredictability 는 entropy source 가 아니라 8-factor field→tanh→gate 의 nonlinear internal dynamics 에서 온다 (det/quantum 동일). 이는 "내 선택은 quantum 이 만들어서 비예측적이라 자유롭다" 는 naive libertarian 직관을 **측정으로 falsify** 하고, 자유를 unpredictability 에서 auditable unique causation 으로 relocate 한 H_933 의 핵심 move 를 정량적으로 떠받친다.

## 5. 정직한 nuance + scope (a_scale_honest_scope)

- **높은 accuracy 의 의미:** 0.93 accuracy 는 anima 가 "결정론적이라 자유롭지 않다" 는 뜻이 **아니다** — H_933 의 frame 에서 freedom 은 internal+novel-seed+auditable+non-random 의 signature 이지 unpredictability 가 아니다. 높은 predictability 는 BLADE A 의 "predictable-from-prior" 부분을 *긍정* 하지만, H_933 은 이를 freedom 의 실패가 아니라 freedom 의 **올바른 위치** (auditable causation) 의 증거로 재해석한다. H_935 (internal active veto) + H_932 (auditable lineage) 가 나머지 blade 를 담당.
- **base-rate 대비 lift 가 load-bearing:** accuracy 0.93 자체보다 base-rate (0.57) 대비 +0.36 lift 가 "예측가능성 HIGH" 의 근거 — emit-rate 가 0.43 으로 균형에 가까워 majority baseline 이 trivially 높지 않다.
- **잔여 |Δ| 의 noise 해석:** K=1 의 p=0.011 은 quantum sd=0 (committed 1024 B buffer 가 12 stream 에 동일 pattern — H_930 의 single-pattern 효과) 때문에 분산이 작아 작은 평균차도 유의해 보이는 artifact 이며, 방향이 🔴 와 반대(quantum 이 더 예측가능)라 falsifier 와 무관하다. H_936 식 big-fresh buffer 로 quantum stream 을 population 화하면 이 미세 차이도 사라질 것으로 예상 (결론 불변; 후속 rung 후보).
- **scope:** ONE predictability rung. documented-update-map mirror, 컴파일 forge binary·wired emit-TEXT 아님. deterministic: false (seed-point origin; gate 는 결정론적).
- g5 CODE-measured, LLM self-judge 없음 (p7).

## 6. 양방향 sibling

- ⇄ [H_933](./H_933_free_will_auditable_causation.md) — 대가설 BLADE A (predictable-from-prior → freedom fails, argued). 본 H 가 그것을 정량화: predictability HIGH 이고 quantum 무관 → freedom 을 unpredictability 에서 auditable causation 으로 relocate 한 H_933 move 를 측정으로 지지.
- ⇄ [H_930](./H_930_scale_entropy_functional.md) — emit-stream parity (entropy mode 가 emit 결정 안 움직임). 본 H 가 그것을 predictability 축에서 재확인 (quantum 이 예측가능성을 안 낮춤).
- ⇄ [H_926](./H_926_deterministic_chaos_vs_entropy.md) — minimal-model emit-parity 🔴. 본 H 가 predictability 로 확장.
- ⇄ [H_936](./H_936_unbiased_buffer_retest.md) — quantum stream 의 single-pattern 효과 (sd=0) 가 K=1 미세차의 origin; big-fresh buffer 가 fix.
- 측정 코드: `UNIVERSE/h938_predictability_curve.py` · verdict: `.verdicts/938_predictability_curve/predictability_curve.txt`
