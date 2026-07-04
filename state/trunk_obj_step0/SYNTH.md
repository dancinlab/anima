# trunk-objective STEP-0 3-후보 종합 (SYNTH)

> 2026-07-05 · mini numpy $0 · **전부 DIRECTIONAL (toy PASS ≠ 303M, a_toy_scale_recheck)** · pod 렌트 0 · commit/PR 없음.
> 배경: G1 재조합벽 = G6 반증벽 = 하나의 **trunk-objective 벽**으로 수렴 확정(real 303M engine-native). readout/lane/decode/consequence-lane 축(census a,b,c) 소진. 이번 라운드 = census (d) family = 유일 미검증 = trunk-objective 3 후보 STEP-0.
> 메타법칙: **DPI** — 결합 연산자는 target이 교환가능 bag/히스토그램일 때 by-construction INERT(합=교환가능→conjunction op도 additive 재표현). 레버 = readout 아니라 **target(비교환 상호작용항)**. **CE=echo** — next-byte CE는 합성 보상 안 함(재현만).

---

## 0. 스코어카드

| 후보 | verdict | REWARDS-RECOMB (A) | DPI-escape (B) | ablation 인과 (C) | not-refried (D) | by-constr 배제 (c) |
|---|---|---|---|---|---|---|
| ① γ trained-constructive-bind | **FAIL / REFRIED** | ✗ (c1 0/4: γ ≤ CE) | ✗ | ✗ (c3 0/4 trunk=readout) | ✗ (H_1602 재탕, γ→trunk 라우팅 measured-NULL) | ✓ clean |
| ② non-commutative target | **DIRECTIONAL** | ✗ (model-based earned OPTIMIZER-FRAGILE, 폐기) | ✓ (model-free cycle_frac 0.289 ≫ total-order 0.0) | ✓ (EXP-A ablation +0.008 / shuffle −0.009) | ✓ (실코퍼스 model-free, distinct 3근거) | ✓ (EXP-B clean; EXP-A는 by-constr 명시·존재증명 미사용) |
| ③ mitosis 성장+커리큘럼 | **DPI-FLOOR / REFRIED** | ✗ (C heldout 0.133 < chance 0.167) | ✗ | ✗ (D growthOFF가 오히려 최상, 성장=해로움) | ✗ (weight-level인데 H_1835 floor로 붕괴) | ✓ LOW (순열합성 intrinsic + split-guard + shuffle-drop) |

**단일 문장 결론: 세 후보 중 REWARDS-RECOMB ∧ DPI-escape ∧ not-falsified 3조건을 모두 만족한 후보는 없다.** ②만 DPI-escape(존재증명)+distinctness를 통과했으나 "objective가 held-out 재조합을 실제로 보상하나(A)"는 STEP-0에서 미증명 → 유일 생존자이자 조건부 top-1.

---

## (a) REWARDS-RECOMB ∧ DPI-escape ∧ not-falsified 를 STEP-0서 보인 후보?

**없음 (strict).** 각 조건별:

- **REWARDS-RECOMB (A) = 0/3.** ①은 c1 0/4로 γ가 CE보다 오히려 나쁨. ③은 C-arm heldout 0.133이 chance 0.167 미만(성장이 해로움). ②는 model-based earned=+0.24였으나 **OPTIMIZER-FRAGILE**(SGD→≈0, Adam→+0.24) + 반대칭 bilinear가 additive를 subsume해 conflated → 정직하게 폐기. 어느 후보도 "이 objective가 재조합을 보상한다"를 신뢰가능하게 못 보임.
- **DPI-escape (B) = ② 단독.** ②만 target 자체를 provably 비교환으로 만들고, **model-free cycle census**(실 한국어 2.6M어절, 삼각형 1266개 중 3-cycle 366개 = cycle_frac 0.2891, total-order-null 0.0 · SHUFFLE-null 0.5291)로 "additive가 원리적으로 못 덮는 29%"의 실재를 optimizer-무관하게 확인. ①·③은 additive를 이기는 것이 오직 order-capable 아키텍처(CE에도 이미 있음)이지 새 objective가 아님 → escape 아님.
- **not-falsified (D) = ② 단독.** ①은 H_1602(infonce/contrastive 이미 floored)의 유일 구별점(γ→trunk 라우팅)을 직접 isolate했더니 c3 0/4로 measured-NULL = 명시적 재탕. ③은 구성은 distinct(weight-level·성장·커리큘럼)하나 load-bearing 주장("weight-level이면 transfer 열림")이 반증되어 H_1835 floor로 붕괴 = 결과적 재탕.

⇒ **②가 (B)∧(D) 통과 유일 후보. 단 (A) 미충족.** 그래서 판정은 REWARDS-RECOMB(값) 아니라 **DPI-escape 존재증명 + distinct 축 확인**에 그친 **DIRECTIONAL**.

## (b) DPI-FLOOR / REFRIED (재탕)인 것?

- **① γ = REFRIED** (표면 결정) **위에 DPI-FLOOR** (근본 원인). 두 독립 kill: (1) c1 0/4 γ≤CE, (2) c3 0/4 trunk-routing = readout-routing. H_1602의 유일 구별점이 measured-NULL. H_1840(γ bind bilinear-bottleneck FAIR gate 0/3)과도 정합 — H_1840=OP-architecture축, ①=LOSS-form축, 둘 다 fail.
- **③ mitosis = DPI-FLOOR** (transfer 관점 REFRIED). weight-level MLP(B·D)가 train=1.0 완전암기해도 heldout은 chance(0.18/0.22, SE≈0.039) = H_1835 in-context transfer≈0과 동일 floor. 진단 arm **F(비교환 연산자 M_f∘M_g)만** heldout 1.0 + shuffle 0.40 급락 = DPI 예측 그대로(레버=비교환 operator, growth/optimization 아님).

## (c) by-construction artifact (L3 vi⊙vj 교훈) 배제됐나?

**3후보 모두 정직하게 처리.**
- **① clean** — 비교환성이 WORLD target(R 비대칭 / S_4 Cayley)에 있고 입력 feature v_a⊙v_b 아님; heldout이 train 1.0-exact에 도달 안 함(.68–.93) → table-leak 없음.
- **② 이원 처리 — 이게 핵심.** EXP-A는 저랭크 반대칭 R을 손으로 심음 = 명백한 by-construction, 코드/출력에 "interaction is HAND-PLANTED" 명시하고 **존재증명으로 쓰지 않음**(REFRIED alone). 존재증명은 오직 **EXP-B**(실 한국어 코퍼스, model-free 삼각형 count, SHUFFLE-null 0.529 통제)에서만 취함. L3 vi⊙vj 함정을 정확히 인식하고 회피.
- **③ LOW** — target 상호작용이 손심음 아니라 순열 함수합성 f(g(x))의 intrinsic 비교환성; split-guard(test triple ∉ train + 모든 primitive가 train 양슬롯 등장) assert 강제 + F가 shuffle서 0.40 급락 = earned order-sensitive 일반화이지 leak 아님 증명.

⇒ **by-construction artifact가 결론을 오염시킨 후보 없음.** ②의 EXP-A는 심었으나 그 사실을 명시하고 결론 근거에서 제외했으므로 clean.

## (d) top-1 후보 + STEP-1 승격 설계 (1문단)

**top-1 = ② non-commutative target** (유일하게 DPI-escape 존재증명 + H_1602/H_1835와 구조적 distinct + 실데이터 model-free 근거). **STEP-1 승격 설계**: 303M engine-native로 남은 미증명 조건은 (A) "비교환 target objective가 held-out 재조합을 실제 REWARD하나"이며, STEP-0의 model-based earned가 optimizer-fragile해 폐기됐으므로 STEP-1은 이 fragility를 소거하는 것이 핵심. 처방 = trunk에 **보조 방향성-예측 head**(관측 어순 a→b 의 BCE, 손실=CE + λ·L_dir)를 얹되, (1) L_dir target을 model-free cycle census로 고른 **intransitive(3-cycle) pair 부분집합**에만 걸어 additive가 원리적으로 못 덮는 신호만 보상하고, (2) 통제로 **total-order-only pair**(additive로 충분한 71%)에 같은 head를 건 arm과 **SHUFFLE(partner-scramble)** arm을 frozen 사전등록, (3) 판정은 perplexity 아니라(p7) `anima evaluate --py`의 G1 held-out composed_distinct + G6 falsifier로 engine-native, (4) ablation은 λ→0(objective OFF) → additive floor 복귀 인과. **frozen bar**: intransitive-arm G1 > (total-order-arm ∧ SHUFFLE-arm) + margin, λ-OFF서 붕괴. 단 **비용 경고**: 이는 objective-축 GPU 발사이며, 대안으로 memory `g1-coverage-density`(NL-byte held 0.95 vs 0.03, 조합-커버리지 코퍼스+충분 RF)가 GPU 발사 없이도 열릴 수 있는 저비용 레버이므로 STEP-1 발사 전 커버리지-밀도 축과 ROI 비교 권장. **정직**: STEP-0는 존재증명일 뿐, "인접 어순 방향성이 G1을 지배하는 그 조합속성인가"는 미증명(저수준 신호일 위험) — STEP-1의 첫 관문.

## (e) H_9130 bookkeep (1줄)

`H_9130` (신규 · H_9129 계열) — **trunk-objective STEP-0 3후보 종합: ①γ-constructive-bind REFRIED(c1 0/4 γ≤CE ∧ c3 0/4 trunk=readout, H_1602 재탕)·③mitosis-curriculum DPI-FLOOR(heldout chance, 성장 해로움, F-operator만 heldout 1.0)·②non-commutative-target DIRECTIONAL(실 한국어 model-free cycle_frac 0.289 ≫ total-order 0.0 = DPI 전제 붕괴점 존재증명 · 단 REWARDS-RECOMB는 optimizer-fragile로 미증명). 3조건 완전충족 후보 0. top-1=②, STEP-1 GPU는 커버리지-밀도 축과 ROI 비교 후 발사. 전부 mini DIRECTIONAL, toy≠303M.** 2 surfaces(HYPOTHESES.jsonl + card)는 main repo에서 등록, worktree commit/PR 없음.

---

## 종합 교훈 (다음 라운드용)

1. **레버 = 비교환 TARGET, readout/loss-form/growth 전부 아님.** ①(loss-form)·③(growth)·H_1602(readout aux)·H_1840(bind-OP)·h1816·exp3-bind 전수 floor. 오직 target을 provably 비교환으로 만들 때(②의 census, ③의 진단 F)만 additive floor 돌파. DPI 메타법칙 예측 그대로.
2. **방법론 2건 (②서 확립):** (i) model-based earned 결론은 optimizer에 민감(SGD 0 ↔ Adam +0.24) → **model-free 척도(intransitivity census)만 신뢰가능**. (ii) 반대칭 bilinear는 additive를 subsume(x=[w,1], S=[[0,1],[-1,0]]→w_a−w_b)하므로 "binding>additive" acc-gap은 non-additivity 증거로 **부적격**.
3. **distinctness는 측정으로 검증하라.** ①은 "γ→trunk 라우팅"이 H_1602와의 유일 구별점이라 주장했으나 G_trunk vs G_read isolate 결과 measured-NULL(c3 0/4). distinct 주장을 직접 isolate하는 arm이 재탕 여부를 가른다.
4. **비용:** ②만 STEP-1 후보. 그러나 objective-축 GPU 발사 전 `g1-coverage-density`(저비용, GPU 무관) 레버와 ROI 비교. ①·③ GPU 발사는 bar FAIL로 미인가(~각 1 H100-day 절약, p7).
