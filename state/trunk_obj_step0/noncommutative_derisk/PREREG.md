# PREREG — H_9131 ② non-commutative target · STEP-0.5 de-risk (frozen-residual R²)

> 2026-07-05 · mini numpy $0 · CPU-local · pod/GPU 렌트 0 · commit/PR 없음.
> **이 문서는 R² 관측 전에 고정. 1바이트도 사후 변경 금지 (tune-to-green 금지, c2·p7).**

## 목적
STEP-0가 남긴 유일 크랙: ②의 REWARDS-RECOMB(비교환 objective가 held-out 재조합을 REWARD하나)가
model-based earned에서 optimizer-fragile(SGD 0 ↔ Adam +0.24)해 미증명. → optimizer 원천차단한
**closed-form lstsq R² 회귀**로 $0에 가른다. 라벨은 코퍼스서 **얼림**(학습 자유도 0).

## 데이터 (frozen, model-free)
- 코퍼스: archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt (2.33M어절)
- precedence 행렬 P[i,j]=count(i가 같은 줄서 j에 선행), top-400 어절 vocab (census.py 산출 P.npy).
- census 확인: full-triangle 중 3-cycle_frac = **0.0920** (≫ total-order-null 0.0) = 비교환 구조 실재 (DPI-escape 전제).

## 얼린 라벨 (form: 반대칭 잔차, 교환성분 제거)
- 개념쌍(a,b) mincount MINC_TGT=40 (tot=P[a→b]+P[b→a]≥40).
- y(a,b) = (P[a→b] − P[b→a]) / (P[a→b]+P[b→a]) ∈ [−1,1], y(b,a)=−y(a,b). **코퍼스 통계로 얼림, 학습 DOF 0.**

## 얼린 특징 (per-concept, leak-safe)
- 앵커 A = degree 상위 K=32 개념, **개념-쌍 유니버스서 DISJOINT 배제** (앵커는 target pair에 안 나옴 → feature leak 차단).
- z_c[k] = (P[c→A_k] − P[A_k→c]) / (P[c→A_k]+P[A_k→c]+1) ∈ [−1,1]. c의 앵커-상대 방향 프로파일 (단일개념 파생, a-vs-b 직접값 미포함).

## 3-arm (전부 np.linalg.lstsq closed-form, optimizer 무관, ridge 없음)
- **(ii) additive/total-order (강한 보수 baseline)**: ŷ = f(a)−f(b), f(c)=θ·z_c. design row = (z_a−z_b).
  ★ 순수 z_a+z_b(대칭)이 아니라 f(a)−f(b) 사용 = **total-order/rank 로 additive가 덮는 71%를 온전히 준다** (bar를 더 어렵게 = 보수적, tune-to-green 반대방향). 순수 z_a+z_b 대칭 arm은 참고로만 보고(반대칭 target서 ≈0 예상).
- **(i) bind**: ŷ = w·[ (z_a−z_b) , antisym-bilinear ], antisym-bilinear = upper-tri of (z_a⊗z_b − z_b⊗z_a), dim K(K−1)/2=496. bind ⊇ additive (nested) → gap = 순수 상호작용 기여.
- **(iii) shuffle**: bind 모델을 partner-scramble(각 쌍의 b를 무작위 b'로 치환, 라벨 y(a,b) 유지)한 train서 적합·held-out(동일 scramble)서 평가. 실 페어링 구조 사용여부 통제.

## train/held-out split (G1 정의 = 미관측 조합)
- 모든 개념은 train pair에 ≥1회 등장(marginal/feature 관측). held-out = 쌍의 20%, **조합(a,b)이 train에 부재**, 단 a·b 각각은 train 개념집합에 존재. seed가 split·shuffle 결정 (앵커·라벨·특징은 seed 무관 = 진짜 얼림).

## R²
held-out R² = 1 − SS_res/SS_tot (SS_tot = held-out y 분산 기준). seed별 verbatim 보고.

## FROZEN BAR (δ=0.10, seeds {7,4302,4303}, 2/3)
- **REWARDS-RECOMB-signal** IFF ≥2/3 seed서 **둘 다**:
  (1) held R²(bind) − held R²(additive) ≥ 0.10  ∧  (2) held R²(bind) − held R²(shuffle) ≥ 0.10.
- **FALSIFIED-DPI-ceiling** IFF bind가 위를 못 넘음(additive 또는 shuffle이 δ 안으로 따라잡음) = 잔차가 몰래 분해가능/암기 = DPI가 target축서도 천장.
- **DIRECTIONAL** = 경계(1/3 seed만, 또는 한 gap만 통과).
- ★ leak 플래그: held R²(bind) = 1.0 exact 이거나 shuffle held R² ≫ 0 이면 leak 의심 → 결과 무효.

## 정직 (사전 명시)
- mini numpy = 303M engine-native 아님 → **어떤 PASS도 DIRECTIONAL** (a_toy_scale_recheck). PASS = "STEP-1 GPU 정당화 신호"지 GREEN closure 아님.
- by-construction 금지: 상호작용을 world/input feature에 심지 않음 — 라벨은 코퍼스서 얼려 추출, feature는 앵커-상대 단일개념 프로파일(a-vs-b 직접값 없음).
- additive를 약하게(z_a+z_b) 만들어 bind를 이기게 하는 함정 회피 = additive를 f(a)−f(b) total-order로 강하게 고정.
