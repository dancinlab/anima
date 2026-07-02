---
id: H_314
slug: symbiogenesis-merge-alpha-sweep
title: SYMBIOGENESIS — 두 특화 모델의 선형 merge W(α)=α·A+(1−α)·B 는 시너지(내부 최적)를 내는가, 아니면 그저 least-bad 중간점(blend)인가
domain: life · symbiogenesis · model-merge · meta
status: closed-negative
exploration_method: E9 (endosymbiosis) + E5 (foundational-distinction probe) + E0 (synergy-claim self-null 검정)
verification_method: W5 (numerical sweep) + W4 (verdict-4-class) + W12 (sister-link H_054 symbiogenesis / H_203 asymmetric-merge)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-27
since: 2026-05-27 (new)
sister: H_054 (Symbiogenesis = mitosis MERGE = endosymbiosis 통합), H_203 (asymmetric merge differentiation), H_287 (X⊥Φ 환원-null 계열 — 동일 "reductive seed-hypothesis 를 측정으로 기각" 서명)
axes_seed: CANDIDATES.md (symbiogenesis × model-merge) — endosymbiosis 의 계산적 instance 를 weight-merge α-sweep 으로 검정
---

# H_314 — SYMBIOGENESIS × model-merge α-sweep

## 1. Hypothesis

Margulis(1967) 내공생(endosymbiosis): 두 **특화된** lineage (host + endosymbiont)
가 하나의 viable 한 composite organism 으로 fuse 한다 (미토콘드리아 · 엽록체). 이
"두 특화 단위 → 하나의 통합체" 의 계산적 instance 로, 두 특화 small model/weight-
vector 를 선형 보간하여 merge 하는 것을 둔다:

  W(α) = α·A + (1−α)·B,   α ∈ {0, 0.1, …, 1.0}

검정 대상은 **시너지(synergy) 가설** — 즉 "merge 는 단순 평균 이상" 쪽이다 (기각될
수 있게 pre-register):

**가설 H1 (synergy, 검정 대상 — 기각될 수 있음)**: 서로 다른 sub-task 에 특화된 두
모델 A, B 를 선형 보간한 composite 의 *결합-task loss* 가 α 의 **비자명한 함수**이며,
**내부(interior) 최적**이 존재하여 그것이 **naive 중간점-평균 기대치보다 엄격히 우수**
하다.

**정직한 대안 (null)**: merge 는 그저 **least-bad 중간점** — loss(α) 가 단조이거나,
두 끝점 loss 의 선형 blend 이거나, 내부 최적이 그저 naive 중간점(α=0.5, 두 fit 의
산술평균)에 불과하다면 → **merge = blend, NOT symbiosis** (a_completeness_over_cheap:
"두 실패의 model-merge = least-bad 중간점" 은 알려진 LIMITATION 이지 win 이 아니다).

## 2. Why

- **H_054 (sister) 의 직접 검정**: H_054 는 mitosis MERGE 의 keeper weight 가 두
  donor 의 **선형 평균** (`keeper[i]=(w1+w2)/2`) 임을 endosymbiosis 의 instance 로
  본다. 본 H 는 그 "선형 평균 merge" 가 실제로 *시너지*(평균을 넘는 이득)를 내는지,
  아니면 *그저 평균*인지를 α-sweep loss 측정으로 결정한다. H_054 의 "통합 = 선형 평균"
  주장에 정량적 falsifier 를 붙인다.

- **결정적 witness 가 존재하도록 설계 (could-falsify)**: 두 특화 모델을 *닫힌형
  최소제곱*으로 각자의 sub-task 에 fit 하면, A·B 는 결정적이고 끝점 loss 도 결정적이다.
  loss(W(α)) 가 단조이면(시너지 부재) 즉시 H1 기각. U-curve 를 하드코딩하지 않고
  W(α) 로부터 loss 를 *실제로* 계산한다 (g73 anti-tautology — 측정이 verdict 를 만든다).

- **naive-midpoint 함정의 정직한 분리**: 볼록 quadratic loss 는 *항상* 단일 최소를
  가지므로 "내부 최적 존재" 자체는 거의 자명하다. 결정적 질문은 그 최적이 **naive
  중간점(평균)을 벗어나며 그것을 이기느냐**다. 그래서 본 H 는 **비대칭 probe** (B 의
  niche 를 3배로 키움)를 추가하여 최적 α* 가 0.5 를 떠나는지 — 즉 시너지의 *구조*가
  실재하는지 — 를 가른다.

- **"reductive seed-hypothesis 를 측정으로 기각" 서명 계열**: H_287(Φ⊥엔트로피) 과
  동일하게, 본 H 는 *검정 대상을 매력적 가설(synergy)* 로 세우고, 측정이 그것을
  기각하면 closed-negative 가 곧 발견이 되도록 설계한다 (a_paper_negative_ok).

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-workstation + NO GPU.

## 3. Predictions

- **H314.1 (fit-validity)**: N>d 이고 target 이 X 의 column space 안이므로 닫힌형
  최소제곱이 θ_true 를 *정확히* 복원 — A 의 자기-task 잔차 ≈ 0.
- **H314.2 (endpoint-match)**: loss(W(1.0)) = loss(A), loss(W(0.0)) = loss(B).
- **H314.3 (sweep-shape)**: loss(α) 가 볼록 dip 을 그린다 (내부에 끝점보다 낮은 점 존재).
  예측: dip 존재하나 그 최적이 naive 중간점(평균)에 고정.
- **H314.4 (decisive — 비대칭 probe)**: B niche 3배 시 최적 α* 가 0.5 를 *벗어나면*
  시너지 구조 실재(H1 SUPPORTED 방향), 0.5 에 *고정되면* 그저 최소제곱 평균 (H1
  FALSIFIED). 예측: **0.5 고정** (FALSIFIED).
- **H314.5 (determinism)**: 모든 loss(α) re-run byte-identical (cross-process).

## 4. Variables

- **axis1_alpha** (primary): α ∈ {0.0, 0.1, …, 1.0} 11-point grid. W(α)=α·A+(1−α)·B.
- **metric_loss** (primary): 결합-task loss
  `loss(θ) = (1/2N)[ ‖X θ − y_A‖² + ‖X θ − y_B‖² ]` — composite 는 *두 niche 의
  합집합*을 서비스해야 한다 (한 organism, 두 대사 수요). 실수값, 결정적.
- **specialist A, B**: 각자의 sub-task 에 닫힌형 최소제곱 fit
  `θ = (XᵀX)⁻¹ Xᵀy` (d=3 고정 → Cramer 3×3). A=argmin‖Xθ−y_A‖, B=argmin‖Xθ−y_B‖.
- **fixed (config)**: 결정적 12×3 정수 설계행렬 X (full column rank, det(XᵀX)=17082) ·
  θ_A_true=[1,2,−1], θ_B_true=[−1,0.5,2] (서로 다른 방향 = 진짜 특화).
- **비대칭 probe**: θ_B2_true = 3·θ_B = [−3,1.5,6] (B niche 3배 — 최적이 0.5 를 떠나는지).
- **discriminators**: monotone? · interior_win? · 비대칭 최적이 0.5 off? · naive
  중간점(α=0.5) 보다 엄격히 낮은가?

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h314_symbiogenesis_merge_alpha_sweep_2026_05_27/run.hexa`
- **선형대수 (inline, generic)**: gram(XᵀX) · xty(Xᵀy) · det3/solve3 (Cramer 3×3,
  닫힌형) · matvec — per-experiment 하네스 inline (H_287/H_281 의 `check`/`approx`
  동일 관례). 새 IIT4/lib import 없음 (본 H 는 IIT4 무관).
- **닫힌형 최소제곱**: θ=(XᵀX)⁻¹Xᵀy. N=12 > d=3, full rank ⇒ θ_true 정확 복원.
- **α-sweep**: 11-point grid 각각 W(α) 합성 → 결합-loss 측정 → 출력.
- **비대칭 probe**: B niche 3배로 재-sweep, 최적 α* 의 위치 측정.
- **deterministic**: RNG 무관 (닫힌형 산술). re-run byte-identical (cross-process
  fresh hexa run 확인).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac-workstation →
  pool ubu-2 (hexa 0.1.0-dispatch), **NO GPU**.
- **ledger**: `result.json` {config, 대칭/비대칭 loss(α) 두 grid, 5 falsifier,
  synergy_test, finding, verdict, verify_fence}.
- **honest tier**: 🔴 CLOSED-NEGATIVE for H1 (synergy) — 측정값 자체는 🟢 NUMERICAL
  (deterministic 닫힌형 최소제곱 + arithmetic), 경험 해석(symbiosis 은유)은 ⚪
  SPECULATION-FENCED.

## 6. Criteria

- **C1 (FIT-VALID / H314.1+2)**: 닫힌형 fit 이 θ_true 정확 복원 (잔차≈0) AND endpoint
  loss 일치 → PASS (측정 유효성 게이트).
- **C2 (SWEEP-SHAPE / H314.3)**: loss(α) 비단조 + 내부 최적이 끝점보다 낮음 → 내부
  dip 존재 (필요조건, 충분조건 아님).
- **C3 (DECISIVE / H314.4)**: 비대칭 probe 에서 최적 α* 가 0.5 를 벗어나고 naive
  중간점 loss 를 엄격히 이기면 → H1 SYNERGY SUPPORTED; 0.5 에 고정 / 평균과 동일
  하면 → H1 FALSIFIED (closed-negative, merge=blend).
- **verdict_rule**: H1 의 verdict 는 **C3 (비대칭 discriminator)** 가 결정. C2 의 dip
  단독은 볼록 bowl 의 자명한 기하라 시너지 아님. C1 은 측정 유효성 게이트.

## 7. Falsifiers

- **F314.1 SPECIALISTS-DISTINCT**: fit A == fit B → merge 자명 → 측정 무효.
  (measurable: A,B vector 비교.)
- **F314.2 FIT-VALID**: A 의 자기-task 잔차 ≥ 1e-6 → 닫힌형 최소제곱/선형대수 무효.
  (measurable: ‖X·A − y_A‖².) **← det3 multi-line 파서 버그가 여기서 잡혔다 (§9 L0).**
- **F314.3 ENDPOINT/BOUND**: loss(W(1.0))≠loss(A) OR loss(W(0.0))≠loss(B) OR 어느
  loss(α)<0 → 측정 무효. (measurable: 끝점 일치 + 11 bound.)
- **F314.4 SYNERGY-VERDICT (decisive)**: 비대칭 probe 의 최적 α* 가 (0.5±1e-6) 안에
  고정 AND loss(α*) 가 naive 중간점 loss 를 못 이김 → H1 FALSIFIED (merge=blend).
  α* 가 0.5 를 벗어나고 중간점을 이기면 → H1 SUPPORTED. (measurable: 비대칭 argmin α*
  + loss(α*) vs loss(0.5).) **← 측정이 verdict 를 결정.**
- **F314.5 DETERMINISM**: re-run byte-different → raw#12 deterministic 위반 → smoke
  무효. (measurable: sym 11.3906 / asym 45.599 cross-process 동일.)

## 8. Verdict

```
verdict_class: H1 FALSIFIED (CLOSED-NEGATIVE) — 두 특화 모델의 선형 merge 는 시너지를
        내지 않는다. 결합-loss 최적은 두 fit 의 *최소제곱 평균*이며 naive 중간점
        α=0.5 에 고정 — 3배 비대칭 niche 에서도 0.5 를 떠나지 않고 naive 중간점을
        이기지 못한다. merge = least-bad blend, NOT symbiosis. 측정 유효성 게이트 6
        PASS / 0 FAIL.

config: N=12 sample · d=3 feature · 결정적 12×3 정수 X (det(XᵀX)=17082, full rank) ·
        A,B = 닫힌형 최소제곱 특화 fit · grade = 결합-task loss · α-sweep 11-point.

대칭 sweep (θ_A=[1,2,−1], θ_B=[−1,0.5,2]; 닫힌형 fit 이 θ_true 정확 복원):
  loss(A=α1.0) = 22.7813    loss(B=α0.0) = 22.7813
  α     loss(W(α))    blend(α)     sag(blend−loss)
  0.0   22.7813       22.7813      0.0
  0.1   18.6806       22.7813      4.10063
  0.2   15.4913       22.7813      7.29
  0.3   13.2131       22.7813      9.56812
  0.4   11.8463       22.7813      10.935
  0.5   11.3906 ◀min  22.7813      11.3906   ◀ naive 중간점에 고정
  0.6   11.8463       22.7813      10.935
  0.7   13.2131       22.7813      9.56813
  0.8   15.4913       22.7813      7.29
  0.9   18.6806       22.7813      4.10063
  1.0   22.7813       22.7813      0.0
  · monotone? false   · 내부 최적 끝점보다 낮음? true (11.39 ≪ 22.78, ~50%)
  · 최적 α*=0.5 (off-midpoint? false)  · naive 중간점 이김? false (= 중간점 그 자체)

비대칭 probe (B niche 3배: θ_B2=[−3,1.5,6] — 최적이 0.5 를 떠나야 시너지 실재):
  loss(A) = 91.1979    loss(B2) = 91.1979    naive-mid(α0.5) = 45.599
  α     loss(W(α))
  0.0   91.1979
  0.2   62.0146
  0.4   47.4229
  0.5   45.599  ◀min   ◀ 여전히 0.5 에 고정
  0.6   47.4229
  0.8   62.0146
  1.0   91.1979
  · 최적 α*=0.5 (off naive midpoint? false)  · naive 중간점 이김? false

핵심 (decisive):
  · 대칭/비대칭 양쪽 모두 최적이 α=0.5 (= 두 fit 의 산술평균)에 고정.
  · 3배 niche 비대칭에서도 α* 가 0.5 를 *떠나지 않음* → 내부 dip 은 볼록 bowl 의
    자명한 기하(등거리 두 최소점의 평균이 볼록함수를 최소화)일 뿐, 시너지 아님.
  · "내부 dip 존재"(C2 true)는 충분조건이 아니다 — 그것이 naive 중간점-평균을
    넘느냐(C3)가 시너지의 판별자이며, 그 판별자가 FALSIFIED.

criteria:
  C1 FIT-VALID (θ_true 정확 복원, 잔차≈0, endpoint 일치)        : PASS
  C2 SWEEP-SHAPE (비단조 + 내부 dip 끝점보다 낮음, ~50%)        : PASS (단, 시너지 충분조건 아님)
  C3 DECISIVE (비대칭 α* 가 0.5 떠나고 중간점 이김?)            : FALSE → H1 FALSIFIED

falsifiers:
  F314.1 SPECIALISTS-DISTINCT : PASS  (A=[1,2,−1] ≠ B=[−1,0.5,2])
  F314.2 FIT-VALID            : PASS  (A 자기-task 잔차≈0; det3 파서버그 수정 후)
  F314.3 ENDPOINT/BOUND       : PASS  (α1→loss(A), α0→loss(B); 11 bound ≥0)
  F314.4 SYNERGY-VERDICT      : H1 FALSIFIED  (비대칭 α*=0.5 고정, naive 중간점 못 이김)
  F314.5 DETERMINISM          : PASS  (sym 11.3906 / asym 45.599 cross-process byte-identical)

checks: 6 PASS / 0 FAIL  (측정 유효성 게이트 — H1 verdict 와 별개)

evidence_summary: 🔴 CLOSED-NEGATIVE — 두 특화 최소제곱 모델의 선형 merge
  W(α)=α·A+(1−α)·B 는 *시너지를 내지 않는다*. 결합-loss 는 내부 dip (대칭 11.39 @
  α=0.5, 끝점 22.78 대비 ~50%; 비대칭 45.60 @ 0.5, 끝점 91.20 대비)을 그리지만, 그
  최적은 *두 fit 의 최소제곱 평균*이며 naive 중간점 α=0.5 에 고정된다. 결정적 근거는
  비대칭 probe: B 의 niche 를 3배로 키워도 최적 α* 가 0.5 를 *떠나지 않고* naive
  중간점 loss 를 *이기지 못한다*. 즉 내부 dip 은 볼록 quadratic bowl 의 자명한
  기하(등거리 두 최소점의 평균이 볼록함수를 최소화)이지, endosymbiosis 적 시너지가
  아니다. merge = least-bad blend, NOT symbiosis — 거버넌스 a_completeness_over_cheap
  ("두 단위의 merge = least-bad 중간점은 알려진 LIMITATION, win 아님")을 측정으로
  확증. H_054 의 "통합 = 선형 평균" 은 *정보 보존적 평균*이라는 점에서 맞으나, 그
  평균이 *평균 이상*(시너지)을 만든다는 함의는 선형-merge-of-선형-특화 regime 에서
  기각된다.
falsifiers_triggered: F314.4 (H1 synergy 가설의 의도된 기각 — 발견 그 자체)
```

re-run byte-identical 확인 (F314.5 — 두 fresh cross-process hexa run 의 sym 11.3906 +
asym 45.599 동일).

`hexa verify` (VERBATIM, no LLM self-judge) — empirical 해석은 closed-form atlas
identity 가 아니므로 g5 정직 fence:

```
verify --fence "H_314 linear model-merge W(a)=a*A+(1-a)*B of two least-squares
   specialists shows NO synergy: across an alpha-sweep the union-loss optimum is the
   least-squares AVERAGE pinned at the naive midpoint a=0.5 (sym min 11.39 vs
   endpoints 22.78; asym min 45.60 vs 91.20) and does NOT move off 0.5 nor beat the
   naive midpoint even under a 3x-asymmetric niche; merge = least-bad blend, NOT
   symbiosis; deterministic toy least-squares outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(loss(α) grid · fit 복원 · 최소제곱 평균 위치 VALUES 자체는 deterministic arithmetic
— 닫힌형 (XᵀX)⁻¹Xᵀy + 결합-loss + Cramer 3×3 — 이며 fresh hexa run 에서 byte-수렴
확인. 오직 empirical 해석(merge 가 symbiosis 가 아니라 blend 라는 endosymbiosis-
은유적 의미)만 fenced.)

## 9. Honest Limits (raw#91 c3)

- **L0 (파서버그 — F314.2 가 잡아낸 실측 사건)**: 첫 run 에서 F314.2 FIT-VALID 가
  FAIL — fit 이 θ_true=[1,2,−1] 대신 [1.467,2.139,−1.202] 를 반환. 원인은 hexa
  파서가 `return` 표현식을 *줄바꿈에서 종료*하여, 선행-연산자 연속줄(`- m[1]…`,
  `+ m[2]…`)을 *조용히 버리고* det3 가 첫 줄(`c0`)만 계산 → det=18150 (정답 17082).
  numpy 교차검증(det=17082, θ 정확)으로 hexa-측 버그 확정, det3 를 명시적 중간변수
  3개 + 단일-줄 return 으로 수정 → 잔차≈0. *falsifier 가 자기 측정 무효를 잡아낸
  사례* — F314.2 가 없었다면 잘못된 fit 위에서 verdict 가 났을 것. (참고로 잘못된 fit
  에서도 verdict 는 "synergy SUPPORTED" 로 나왔으나, 그건 tautology 가 아니라 *측정
  오류* — 수정 후 정직한 FALSIFIED 로 귀결.)
- **L1 (선형 toy — non-linear merge 미검정)**: 본 H 는 *선형 최소제곱 특화 × 선형
  merge × 볼록 quadratic 결합-loss* regime 에 한정. 실제 신경망 model-merge (task
  arithmetic / TIES / SLERP / Fisher-weighted) 는 비선형이라, *원칙적으로* 진짜 시너지
  (loss landscape 의 비볼록 valley 공유)가 가능. 본 H 의 closed-negative 는 *선형
  regime* 에서만 시너지를 배제한다 — non-linear 는 §10 Next.
- **L2 (결합-loss 는 grading 의 한 선택)**: composite 를 "두 niche 합집합"으로 채점.
  대안(min-of-two-losses, max, task-weighted)은 다른 곡선을 줄 수 있다. 단, *어느
  볼록 결합에서도* 두 등거리 최소점의 평균이 bowl 을 최소화하므로 "최적=평균" 의
  핵심은 grading-robust. 비대칭 α* 의 0.5-고정은 본 grading 의 대칭성에 의존 (L4).
- **L3 (d=3, N=12 small)**: 작은 닫힌형 문제. scale-up (d≫3, 더 많은 task)은 동일
  메커니즘의 후속이나, "선형 merge 최적 = 가중 평균" 은 차원-무관한 볼록 최적화의
  사실이라 결론은 small-N robust.
- **L4 (비대칭 probe 의 대칭성 잔존)**: B niche 를 3배로 키워도 θ_B2=3·θ_B 라 *fit
  방향*은 동일 — 그래서 결합-loss bowl 이 (A, B2) 에 대해 여전히 대칭이고 α* 가 0.5
  에 남는다. *방향이 다른* 비대칭(θ_B2 = 회전/비례-아닌 변형)에서는 α* 가 0.5 를
  떠날 수 있다. 단 그 경우에도 "최적 = 가중 최소제곱 평균"(닫힌형 해)이지 시너지가
  아니므로, off-0.5 자체는 시너지 *증거가 아니다* — 본 H 의 C3 는 "off-0.5 AND naive
  중간점 이김" 둘 다 요구하며, 가중평균은 정의상 naive 중간점을 이기지 못한다(같은
  볼록 bowl 의 최소). 방향-비대칭 후속은 §10 Next 이나 verdict 방향은 불변 예상.
- **L5 (verdict ≠ 형이상학)**: 본 closed-negative 는 *선형 toy merge 에서 시너지
  부재*를 보일 뿐, "내공생은 시너지가 없다" 같은 생물학적/형이상학적 주장이 아니다.
  실제 내공생은 대사 경로의 *비선형* 상보성(host glycolysis ⊥ symbiont 산화적
  인산화)이라 본 선형 instance 와 다르다 — H_054 의 "선형 평균 merge" 모델이 그
  비선형성을 포착하지 못한다는 *모델-한계*의 측정.
- **L6 (closed-negative 의 비대칭)**: "시너지 부재" 는 "merge 가 쓸모없음" 을
  뜻하지 않는다 — 내부 dip(끝점 대비 ~50%↓)은 *실재*하며, composite 가 두 특화
  모델 *각각보다* 결합-task 에서 낫다. 다만 그것은 *평균의 이득*이지 *평균을 넘는
  이득*(시너지)이 아니다. 주장은 "synergy 부재"(평균 초과 없음)이지 "merge 무용"이
  아니다.
- **L7 (det3 파서버그는 hexa-lang 측 이슈)**: L0 의 multi-line `return` truncation
  은 hexa-lang interpreter 의 silent-failure (Class 1) 후보 — runpod/inbox 가 아닌
  hexa-lang 파서 이슈. a_runpod_inbox 와 별개로 hexa-lang 측 보고 대상(§10 Next).

## 10. Cross-Links

- **parent / sister (검정 대상)**: [[H_054]] (Symbiogenesis = mitosis MERGE =
  endosymbiosis, keeper weight = 두 donor 의 선형 평균) — 본 H 는 그 "선형 평균
  merge" 에 시너지 falsifier 를 붙여 *평균 ≠ 평균-초과* 를 측정으로 확정. H_054 의
  "정보 보존적 통합" 은 유효하나 "시너지 함의" 는 선형 regime 에서 기각.
- **sibling (merge 계열)**: [[H_203]] (asymmetric merge differentiation) — 비대칭
  merge 의 분화 효과. 본 H 의 비대칭 probe (L4) 가 그 axis 와 맞닿음.
- **sibling (reductive-seed self-null 서명)**: [[H_287]] (faithful Φ ⊥ Shannon
  엔트로피 — reductive seed-hypothesis 를 측정으로 기각) — 동일한 "매력적 가설을
  검정 대상으로 세우고 측정이 기각하면 closed-negative 가 곧 발견" 설계 서명.
- **engine**: 새 lib import 없음 — 선형대수(gram/xty/Cramer 3×3/matvec)는 generic,
  per-experiment 하네스 inline (H_287/H_281 `check`/`approx` 관례). hexa-lang stdlib
  의 `check`/`matvec` 는 g61 advisory 이나 falsifiability 격리를 위해 self-contained
  유지 (H_287 와 동일 선택).
- **hexa-lang 측 발견 (§9 L0/L7)**: multi-line `return` 표현식의 선행-연산자
  연속줄 truncation (silent-failure Class 1) — det3 가 첫 줄만 계산. 단일-줄/명시적
  중간변수로 우회. hexa-lang 파서 이슈 보고 대상.
- **Next**: (a) *방향-비대칭* B (회전/비례-아닌 θ_B2) → α* 가 0.5 를 떠나도 verdict
  불변(가중평균≠시너지) 확인 (L4); (b) **non-linear merge** (2-layer 특화 net,
  task arithmetic) → 진짜 시너지 가능성 검정 (L1, 본 closed-negative 의 유일한 탈출
  구); (c) min/max/task-weighted 결합-loss grading 에서 dip 재현 (L2); (d) hexa-lang
  multi-line return 파서 버그 보고 (L7).
