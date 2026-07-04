# VERDICT — H_9131 ② non-commutative target · STEP-0.5 de-risk

> 2026-07-05 · mini numpy $0 · CPU-local · pod/GPU 0 · commit/PR 없음 · PREREG.md frozen bar 불변 적용.

## 판정: **FALSIFIED-DPI-ceiling** (optimizer-robust)

STEP-0의 유일 크랙("비교환 objective가 held-out 재조합을 REWARD하나"가 model-based earned에서
optimizer-fragile로 미증명)을 closed-form lstsq R²(optimizer 원천차단)로 가른 결과:
**비교환 target objective는 held-out 재조합을 additive-decomposable(total-order) 이상으로 REWARD하지 않는다.**
n_pass(2/3, δ=0.10) = **0**. leak 없음.

## 3-arm held-out R² (verbatim, frozen bar K=32)

| seed | bind | additive(total-order) | shuffle | sym_ref(z_a+z_b) | gap b−add | gap b−sf | pass_both |
|---|---|---|---|---|---|---|---|
| 7 | 0.2726 | **0.4844** | 0.0567 | 0.0677 | **−0.2118** | +0.2159 | ✗ |
| 4302 | 0.3047 | **0.4935** | −0.0599 | 0.0504 | **−0.1888** | +0.3646 | ✗ |
| 4303 | 0.1843 | **0.5178** | −0.0409 | 0.0607 | **−0.3334** | +0.2252 | ✗ |

- train_bind ≈ 0.647 ≫ held_bind ≈ 0.25 = bind는 496 상호작용 차원을 **overfit(암기)만**.
- additive train 0.498 ≈ held 0.49 = total-order는 held-out서 깨끗이 일반화.
- **gap_bind−additive 3 seed 전부 음수** → bind가 강한 additive baseline을 **못 이김**.
- gap_bind−shuffle 전부 양수(+0.22~+0.36) → bind가 실 페어링은 쓰지만, 그 상호작용이 additive 너머로 일반화 안 됨.

## 왜 STEP-0의 model-based +0.24가 착시였나 (크랙 해소)
sym_ref(z_a+z_b 대칭 additive) held-out R² ≈ 0.06. bind(0.27) − sym(0.06) = **+0.21** → 약한 대칭 baseline
쓰면 가짜 PASS. 강한 total-order baseline f(a)−f(b)(held 0.48)를 쓰면 bind가 **−0.24로 오히려 짐**.
= STEP-0 note 2(ii) "반대칭 bilinear가 additive를 subsume" 함정 그대로. 정직한 baseline이 +0.24를 소거.

## 강건성 부록 (SENSITIVITY.json · 앵커/bilinear 용량 스윕, bar 불변)
| K | n_bilinear | held_add | held_bind | gap b−add |
|---|---|---|---|---|
| 4 | 6 | 0.290 | 0.299 | **+0.009** |
| 8 | 28 | 0.439 | 0.441 | **+0.002** |
| 16 | 120 | 0.472 | 0.442 | −0.030 |
| 32 | 496 | 0.499 | 0.254 | −0.245 |
**모든 용량서 bind의 held-out 우위 최대 +0.009 (≪ δ=0.10).** 저용량=bilinear 기여≈0, 고용량=overfit.
→ FALSIFIED는 용량 artifact 아님. 비교환 잔차의 held-out-일반화 성분은 **total-order가 전부 덮고**,
진짜 intransitive(cycle_frac 0.092) 성분은 **암기(idiosyncratic)이지 재조합 아님**.

## leak-check (전부 통과)
- 조합-disjoint: held-out pair ∩ train pair = ∅ (assert 통과).
- 개념 존재: held-out a·b 모두 train 개념집합에 존재 (G1 정의).
- feature-disjoint: 앵커 32개 ∩ 개념쌍 유니버스 = ∅ (a-vs-b 직접값 feature 미포함).
- held R²(bind) exact 1.0 아님 (0.18~0.30) · shuffle held R² 저값 → leak 플래그 0.

## engine-native? / next
- **engine-native = NO** — mini numpy toy, 303M engine-native 아님 → 판정 DIRECTIONAL wrt 303M (a_toy_scale_recheck).
  단 이는 **negative(보수)** 방향이라: REWARDS-RECOMB가 성립할 때만 STEP-1 escalate가 정당했는데,
  optimizer-robust로 REWARDS-RECOMB이 **꺼짐** → escalate 정당성 소멸.
- **STEP-1 GPU 정당화되나? = NO.** ②의 objective-축 GPU 발사는 REWARDS-RECOMB 신호에 의존했고, 그 신호가
  optimizer-fragility 제거 후 사라짐. DPI 메타법칙이 **target 축서도 유지** = G1 벽은 진짜 능력천장 방향.
  저비용 대안(`g1-coverage-density`, GPU 무관 조합-커버리지 코퍼스)만 남음.

## 산출물
- PREREG.md (관측 전 고정 bar) · census.py + P.npy/vocab.json/census.json (precedence·cycle census)
- derisk.py + RESULT.json (frozen bar 3-arm) · sensitivity.py + SENSITIVITY.json (용량 스윕) · VERDICT.md
