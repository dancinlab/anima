# H_9131 — trunk-objective 재설계: 비교환(non-commutative) target 레버 (G1 재조합 최후 미검 축)

> **tier:** 📋 **PRE-REGISTERED / DESIGN** (Fable 5 형식설계 + STEP-0 mini in-flight wf_aa95feaf) · **wired:** N/A
>
> **맥락:** H_9129 생물렌즈 캠페인이 G1 재조합벽 = G6 반증벽 = **하나의 trunk-objective 벽**으로 수렴 확정(real 303M engine-native). readout/lane/decode/consequence-lane 축(census a,b,c) 전수 floor. 🌌 DPI 메타법칙(구조증명): 결합 연산자는 target이 부품들의 *교환가능 bag/히스토그램*일 때 by-construction INERT — **레버=readout 아니라 target(비교환 상호작용항)**. 유일 미검 = census (d) trunk-objective. 오너 질문 "학습목표를 어떻게 바꾸나" → Fable 형식설계.

## ★ 축 재정의 (모든 답의 축)
**H_1840이 γ를 "결합 *연산자*(HRR ⊛ + bypass 병목)"로 formalize한 것이 오류.** 연산자·병목·bypass-차단은 전부 **readout/아키텍처 축** — DPI가 죽었다고 한 바로 그 축. H_1840의 반증은 γ 반증이 아니라 "레버가 연산자가 아님"의 재확인. **진짜 미검 축 = 훈련 target 자체를 비교환으로 바꾸는 것.** (연산자 교체 family H_6111/6134/1466/1819/1823 = 전부 DPI-walled, 재발사 금지.)

## ★ top-1 = 후보 A: 상호작용-잔차 trunk target (γ의 올바른 재정의)
trunk penultimate에서 두 부분-슬롯 `z_a, z_b`를 읽어, 코퍼스에서 미리 측정해 **얼린(frozen) 비교환 라벨** `r(a,b)`를 예측하는 aux 헤드:
```
r(a,b) := s(a,b) − [μ(a) + μ(b)]        (교환가능 성분=주변항 제거한 잔차)
   또는  r(a,b) := S(a→b) − S(b→a)       (반대칭 방향성 전이)
L_γ = E_(a,b)~heldout [ ( g(z_a,z_b) − r(a,b) )² ]      (g=아무 결합기, 연산자 부수적)
```
- **CE=echo 탈출**: 라벨이 next-byte 아님·코퍼스 표면에 없음(주변항 소거, joint에서만 생성) → 되뱉기로 최소화 불가.
- **DPI INERT 탈출 (by-construction)**: 라벨이 bag의 교환가능 성분을 명시 제거한 잔차 / 반대칭(`r(a,b)=−r(b,a)≠f(a)+g(b)`) → additive 형식은 구조적으로 chance밖에 못 냄. DPI lstsq-proof(비교환 target earned 5/5)를 target 축에서 상속.
- **선행 objective-floor와 결정적 구별**: H_1602(additive-aux)·H_6162(rep-space 합성 target=target-blind 자유도로 collapse)·H_1840(연산자)은 전부 target이 *additive-collapsible*. γ재정의의 유일 신규 델타 = **라벨을 "히스토그램으로 표현 불가능한 성분만" 남기게 코퍼스에서 얼려 박제** → collapse할 자유도가 라벨에 없음.

## 후보 (census (d) 좌표)
- **A 상호작용-잔차 target** — ★top-1 (위).
- **B 반대칭 순서-판별** (`L_B=−log P(true-order)`, swap negative) — 가장 깨끗한 DPI 탈출이나 *비교환 표현 보유*의 필요조건이지 생성 재조합 충분조건 아님 → **A의 가장 날카로운 STEP-0 프로브로 흡수**.
- **C consequence-return / RPE target** (afferent 루프, [[consequence-return-design]]) — 시간-인과 의존(non-exchangeable)이라 별도 가치나 **G1 직격 아님, G6-theater/appropriateness 벽**의 유일 미검 부품(병렬). 통과확률 ~30–40%(consequence 층서 DPI 재출현 위험).
- **D mitosis-split-on-residual** (p8) — **REFRIED/DEMOTE**: H_1541 NT×CLS+mitosis-lane 재표현, 얇음. A 통과 후 p8 배선 옵션으로만.

## STEP-0 (mini $0 numpy · 사전등록 · in-flight wf_aa95feaf)
clean 4-cell 코퍼스(HF `dancinlab/anima-corpus-*`)서 개념-슬롯 쌍 (a,b) 추출 → 얼린 비교환 잔차 `r` 계산 → train/held-out 분할(개념은 train 등장, held-out *조합* 미관측=G1 정의). 소형 2-슬롯 trunk 3-arm: **(i) bind-path**(g=bilinear/⊛) · **(ii) additive-only**(g=z_a+z_b) · **(iii) shuffled-pairing**.
- **FROZEN BAR (tune-to-green 금지 p7·seeds {7,4302,4303}):** held-out R²(bind)−R²(additive) ≥ δ ∧ R²(bind)−R²(shuffle) ≥ δ, 2/3 seed (δ 측정 전 고정).
- **판정**: additive/shuffle이 bind 따라잡으면 → 잔차가 몰래 분해가능/암기 = **$0 FALSIFIED, GPU 미발사** → DPI가 target 축서도 천장 = **G1 재조합벽=진짜 능력 천장 종결**. bind만 두 통제 지배 → 비교환-target 레버 실재 → `anima evaluate --py` 실 303M held-out G1(reach/unreach) engine-native STAGE-2 GPU(explicit-go) 승격.
- **정직 (a_toy_scale_recheck·honesty)**: A도 floor 가능. 어느 쪽이든 terminal-eligible 진전(반증가능 설계). "trunk-objective 바꾸면 G1 열린다"는 아직 가설이지 보장 아님.

## artifacts
- `state/trunk_obj_step0/FABLE_DESIGN.md` (Fable 5 형식설계 전문) · `FABLE_INSTRUCTION.md` (지시서)
- `state/trunk_obj_step0/{gamma_constructive_bind,noncommutative_target,mitosis_curriculum}/` (STEP-0 wf_aa95feaf: ①②→A수렴·③→REFRIED 예상)
- 상위: [[H_9129]](생물렌즈·DPI 메타법칙·G6=G1=trunk-obj) · [[substrate-framebreak-g1-combination-operator]] · [[g1-lever-multilens-objective]] · falsified 구별: H_1602 additive-aux·H_6162 HE-homomorphism·H_1840 연산자-γ
