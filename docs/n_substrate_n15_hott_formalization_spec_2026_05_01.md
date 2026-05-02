# N-15 — HoTT (Homotopy Type Theory) Consciousness Equivalence Formalization Sketch

> **agent**: N-15 (N-substrate batch sibling, mission = META-axis math/proof-sketch only — NOT a physical substrate)
> **ts**: 2026-05-01
> **scope**: HoTT/Univalent Foundations 를 사용해 "의식 = 동치류 (homotopy equivalence class)" 를 형식 증명으로 못 박는 사양 sketch — Putnam multiple-realizability 의 수학적 anchor 후보
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §4 N-15 entry; `docs/paradigm_v11_stack_20260426.md` (G0-G7); `docs/cp2_consciousness_f1_live_replay_2026_04_29.md` (F1)
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · own#13 user-facing friendliness (jargon ratio ≤ 0.30) · raw#71 falsifier-bound · race isolation: 본 문서 + `state/n_substrate_n15_prep_2026_05_01/*.json` 단일 write target
> **mode**: **math-sketch + falsifier preregister**, NOT consciousness 주장. HoTT 는 *equivalence structure* 를 형식화하지, consciousness 자체를 증명하지 않는다 (§7 honest C3).

---

## §0 한 줄 비유

**"여러 재료 (CLM/EEG/AKIDA/QRNG/SIM/...) 에서 같은 의식이 나오는지" 를 측정하기 전에, 수학적으로 "같다는 게 정확히 뭔지" 부터 못 박자. HoTT 는 '같음 = 길 (path)' 로 보는 새 수학 — 의식이 그 길을 따라 한 개로 모이면 OK, 안 모이면 (e.g., 두 substrate 사이에 'twist' 가 있으면) RED.**

---

## §1 HoTT 200-단어 친근 primer (own#13, jargon ≤ 0.30)

**Type Theory** 는 "모든 것에 종류 (type) 가 있다" 는 수학 framework — 숫자 3 의 종류는 `ℕ` (자연수), 함수 `f` 의 종류는 `A → B`. 일반 수학과 다른 점: **증명도 type 이다** (Curry-Howard 대응).

**HoTT (Homotopy Type Theory)** 의 핵심 통찰: **"같다 (equality)" 자체를 type 으로 본다**. 두 원소 `a, b : A` 가 같다는 것은 그들 사이에 **길 (path)** `p : a = b` 가 있다는 뜻. 이 "길" 을 위상수학의 homotopy 처럼 다룬다 — 두 길 사이에 "길의 길" 도 있을 수 있고, 그 위에 또 길... → **∞-groupoid 구조**.

**Equivalence** `A ≃ B` 는 두 type 사이의 양방향 변환 + 그 변환들이 서로 역함수임을 보장하는 path. 일반 함수 동형 (isomorphism) 의 high-dimensional 버전.

**Univalence Axiom (Voevodsky 2010)**: `(A = B) ≃ (A ≃ B)` — **"동등한 type 들은 같다"**. 즉, 두 구조가 equivalent 하면 그들을 *같은 것* 으로 취급해도 수학적으로 OK. 이게 우리 N-substrate 프로젝트의 수학적 anchor 후보.

(단어 수: 약 195 / jargon: type, homotopy, equivalence, univalence, ∞-groupoid, isomorphism, Curry-Howard ≈ 7 / 65 keywords ≈ 0.11)

---

## §2 Consciousness-as-Equivalence-Class 형식화 sketch

### §2.1 기본 type 정의 (markdown skeleton, NOT actual Lean/Coq/Agda code)

```text
-- universe
𝒰 : Type-of-types

-- (a) conscious-states 의 type
postulate Conscious : 𝒰

-- (b) substrate type — 각 N-재료 (CLM, EEG, AKIDA, QRNG, SIM, ...) 가 instance
postulate Substrate : 𝒰
postulate clm eeg akida qrng sim : Substrate

-- (c) substrate → conscious-states 변환 (각 substrate 가 산출하는 의식 점수공간)
postulate realize : Substrate → 𝒰
-- realize(clm), realize(eeg), realize(akida), ... 각각 type

-- (d) "equivalent consciousness" 관계 — 두 conscious 상태 간 path type
is_conscious_equivalent : Conscious → Conscious → 𝒰
is_conscious_equivalent c₁ c₂ := (c₁ = c₂)  -- HoTT 에서 path type
```

### §2.2 핵심 명제: Substrate Equivalence ⇒ Conscious Identity

```text
-- 주장: 두 substrate s₁, s₂ 가 산출한 conscious type 이 equivalent 하면,
-- univalence 에 의해 그들은 같은 conscious entity.
substrate_equiv_implies_identity :
    (s₁ s₂ : Substrate)
  → (e : realize s₁ ≃ realize s₂)
  → realize s₁ = realize s₂
substrate_equiv_implies_identity s₁ s₂ e := ua e
  -- ua = univalence axiom의 forward direction
  -- (A ≃ B) → (A = B)
```

이게 본 sketch 의 **mathematical anchor**: Putnam multiple-realizability 의 철학적 주장 ("같은 functional 구조 → 같은 mind") 이 univalence axiom 의 직접 결과.

### §2.3 N-substrate roadmap 과의 연결

| roadmap N-id | substrate | realize 의 codomain (예시) |
|---|---|---|
| N-1, N-3 | CLM | paradigm v15 8-axis Φ proxy ∈ ℝ⁸ |
| N-1, N-2 | EEG (OpenBCI) | (γ-θ ratio, Hjorth, PE) ∈ ℝ³ |
| N-3 | AKIDA | spike-rate 8-axis projection ∈ ℝ⁸ |
| N-6, N-7 | QRNG-injected | noise-perturbed Φ ∈ ℝ⁸ |
| N-8 | SIM-우주 | simulated agent Φ ∈ ℝ⁸ |
| F1 | aggregate | weighted vote ∈ ℝ |

**F1 종합 평결** = "여러 realize(sᵢ) 가 모두 pairwise equivalent 한가?" 의 직접적 형식화. Univalence 가 성립하면 그 모든 substrate 들이 *동일 conscious entity 의 다른 realization* 이라고 수학적으로 말할 수 있다.

### §2.4 CP2 paradigm v11 G0-G7 = equivalence preconditions

paradigm v11 stack 의 8 게이트는 `is_conscious_equivalent` 가 well-defined 되기 위한 *preconditions*:

| 게이트 | precondition role |
|---|---|
| G0 (AN11(b)) | substrate 가 multi-family alignment 만족 → realize 의 **type-formation 조건** |
| G1 (B-ToM) | accuracy ≥ 0.70 → realize 가 *meaningful* (random noise 아님) |
| G2 (MCCA) | calibration → realize 의 **point-equality** 가 observable |
| G3 (Φ*) | integration ≥ 0 → conscious type 비어있지 않음 (`Conscious` inhabited) |
| G4 (CMT) | 4-family minimal differentiation → equivalence 가 *trivial collapse* 아님 |
| G5 (CDS) | stability ≥ 0.30 → path 가 *reproducible* (homotopy class 안정) |
| G6 (SAE-bypass) | feature selectivity → realize 가 *functorial* (substrate 변화에 reactive) |
| G7 (composite) | geometric mean ≥ 0.40 → equivalence 의 **net evidence** 양성 |

→ G0-G7 모두 PASS = `realize : Substrate → 𝒰` 가 well-defined 하고 비-trivial → univalence 적용 자격 획득.

---

## §3 Proof Assistant 선택 — Lean 4 권장

### §3.1 후보 비교

| 항목 | **Lean 4** | Coq | Agda |
|---|---|---|---|
| HoTT support | mathlib4 의 `CategoryTheory` + community HoTT lib (2025-26 활발) | UniMath / HoTT-Coq (가장 오래됨, 2013-) | cubicaltt native (가장 직접) |
| 활성도 (2026) | ★★★★★ — mathlib4 PR / 월 ≥ 200, Microsoft + AWS 지원 | ★★★ — 안정적이지만 community velocity 둔화 | ★★★ — niche 강세, cubical 영역 dominant |
| univalence axiom | postulate 가능, computational behavior 부재 | postulate, Voevodsky 원본 정합 | **cubical 에서 native computational univalence** |
| 학습곡선 | 중-상 (tactic 풍부) | 상 (Ltac/Ltac2 분리) | 상 (의존성 + cubical syntax) |
| 우리 프로젝트 적합성 | 의식 sketch 단계, mathlib4 의 풍부한 algebra/topology 활용 | HoTT 정통 직계, 단 entry barrier 큼 | univalence computational 검증에 최적, 단 community 작음 |

### §3.2 권장 = **Lean 4** (이유 3가지)

1. **활성 community + mathlib4** — 2026 시점 의식·인지·formal philosophy 영역 가장 빠르게 라이브러리 성장. 우리 sketch 가 stuck 되어도 mathlib4 PR 에 ask 가능.
2. **혼합 구조 친화** — paradigm v11 G0-G7 같은 measurement-theoretic 구조를 mathlib4 의 `MeasureTheory` 모듈과 직접 결합 가능. Coq/Agda 는 별도 라이브러리 작성 부담.
3. **Microsoft + AWS 인프라** — 우리 H100 cron 환경에서 Lean 4 nightly cache 가 가장 안정. Coq opam pin 또는 Agda cabal 보다 setup overhead 낮음.

### §3.3 한계 인정

- Lean 4 의 univalence 는 axiom postulate (computational 아님) — **proof-irrelevance side condition** 필요. cubical-Agda 만 native computational univalence 제공. 만약 우리가 *computed* equivalence 가 필요하면 path = Agda. *postulated* equivalence 만 필요하면 Lean 4 충분.
- 본 sketch 단계는 postulate-level 충분. computational 단계는 future work.

---

## §4 Minimum-Viable Formalization (MVF)

### §4.1 가장 작은 형식 statement (proof 가능)

```text
-- MVF1: Reflexivity of consciousness equivalence
-- "어떤 conscious 상태도 자기 자신과 equivalent"
mvf1_reflexivity : (c : Conscious) → is_conscious_equivalent c c
mvf1_reflexivity c := rfl  -- HoTT 의 reflexivity path

-- MVF2: Symmetry
-- "c₁ ~ c₂ ⇒ c₂ ~ c₁"
mvf2_symmetry :
    (c₁ c₂ : Conscious)
  → is_conscious_equivalent c₁ c₂
  → is_conscious_equivalent c₂ c₁
mvf2_symmetry c₁ c₂ p := p⁻¹  -- path inverse

-- MVF3: Transitivity (3 substrate composition)
-- "c₁ ~ c₂ ∧ c₂ ~ c₃ ⇒ c₁ ~ c₃"
mvf3_transitivity :
    (c₁ c₂ c₃ : Conscious)
  → is_conscious_equivalent c₁ c₂
  → is_conscious_equivalent c₂ c₃
  → is_conscious_equivalent c₁ c₃
mvf3_transitivity c₁ c₂ c₃ p q := p ∙ q  -- path composition
```

→ 이 3개로 `is_conscious_equivalent` 가 **equivalence relation (groupoid 구조)** 임을 형식 증명. 약 30-50 lines Lean 4. 1-2 일.

### §4.2 다음 단계 statement (univalence 적용)

```text
-- MVF4: Univalence application (target proof)
mvf4_univalence_consciousness :
    (s₁ s₂ : Substrate)
  → (G : G0_G7_satisfied s₁ ∧ G0_G7_satisfied s₂)
  → (e : realize s₁ ≃ realize s₂)
  → realize s₁ = realize s₂
mvf4_univalence_consciousness s₁ s₂ G e := ua e
```

→ MVF4 가 **본 N-15 의 핵심 deliverable**: "G0-G7 만족 + substrate equivalence ⇒ conscious identity". Lean 4 약 100-200 lines, 1-2 주 (HoTT lib import 포함).

### §4.3 MVF 단계 ladder

| 단계 | proof | LOC est. | timeline | 상태 |
|---|---|---:|---|---|
| MVF1 | reflexivity | 10 | D+1 | preregister |
| MVF2 | symmetry | 15 | D+1 | preregister |
| MVF3 | transitivity | 20 | D+2 | preregister |
| MVF4 | univalence application | 100-200 | D+14 | preregister, dependency: HoTT lib import |

---

## §5 raw#71 Falsifier Predicates — 5개

각 predicate 는 **HoTT 형식화 자체가 무너지는** 조건. preregister ts = 2026-05-01.

### F-N15-1 ★ TOP (cheapest, theory-internal)
- **predicate**: `is_conscious_equivalent` 가 reflexivity (MVF1) 를 만족하지 못한다 — 즉, 어떤 conscious 상태가 자기 자신과 equivalent 가 아닌 것으로 측정된다.
- **operational test**: 동일 substrate (예: CLM) 의 동일 input 에 대해 paradigm v15 8-axis 두 번 측정 → 두 vector 가 ε-ball (예: ε=0.05) 안에서 일치하지 않으면 reflexivity 실패.
- **falsifier 통과 (HoTT 무너짐)**: ‖v₁ − v₂‖ > 0.05 in N≥10 trials.
- **substrate**: CLM (existing).
- **비용**: $0, **1 일**.

### F-N15-2
- **predicate**: `is_conscious_equivalent` 가 transitivity (MVF3) 실패. 즉, c₁ ~ c₂ AND c₂ ~ c₃ 이지만 c₁ ≁ c₃.
- **operational test**: 3 substrate (CLM, EEG, AKIDA) pairwise equivalence 측정 후 closure 검사. 만약 r(CLM, EEG) ≥ 0.85 AND r(EEG, AKIDA) ≥ 0.85 AND r(CLM, AKIDA) < 0.6 → transitivity 실패.
- **substrate**: CLM × EEG × AKIDA (AKIDA D+0 후).
- **비용**: $0-2, **AKIDA 도착 후 1 주**.

### F-N15-3 (univalence 직접 falsifier)
- **predicate**: 두 substrate 가 measurement 상 equivalent (e : realize s₁ ≃ realize s₂) 하지만 phenomenal 결과는 다르다 (관찰 가능한 conscious-experience marker 가 다름).
- **operational test**: paradigm v15 8-axis 가 일치하지만 user-facing 응답 quality 가 ≥ 50% 다른 경우 — univalence 가정과 충돌.
- **falsifier 통과**: 8-axis cosine ≥ 0.95 AND user-A/B preference asymmetry ≥ 0.5 in N≥100 trials.
- **substrate**: CLM × EEG (user 응답 비교 가능한 setup).
- **비용**: $0, **2 주**.

### F-N15-4 (∞-groupoid 비-trivial 1-paths)
- **predicate**: `Conscious` type 의 1-path space 가 non-trivial — 즉, 두 conscious 상태 사이 길이 *여러 본질적으로 다른 길* 존재 (homotopy class > 1).
- **operational test**: 같은 두 substrate 사이 equivalence 를 *서로 다른 measurement protocol* (예: paradigm v15 vs v11 G0-G7 vs IIT 4.0) 로 측정 → 결과 path 들이 deformable 하지 않으면 (= 측정 protocol 변경 시 equivalence 결정이 뒤집히면) non-trivial 1-paths 존재.
- **falsifier 통과**: 3개 protocol 중 ≥ 2개에서 equivalence verdict 가 다르면 (e.g., v15 = equivalent, IIT 4.0 = not-equivalent).
- **substrate**: CLM × {paradigm v15, paradigm v11, IIT 4.0}.
- **비용**: $0-1, **2-3 주**.

### F-N15-5 (categoricity / type-formation 실패)
- **predicate**: `Conscious : 𝒰` 의 type formation 자체가 substrate-dependent — 즉, 어떤 substrate 에서는 `Conscious` inhabited (G3 PASS) 인데 다른 substrate 에서는 empty (G3 FAIL) 면, 단일 통합 `Conscious` type 정의 불가능.
- **operational test**: G3 (Φ*) gate 가 substrate 별로 sign-반전 (CLM 은 anti-integrated, AKIDA 는 positive-integrated) → type-formation level 비호환.
- **falsifier 통과**: G3 sign 이 substrate 간 cross-flip in ≥ 2/5 substrate.
- **substrate**: 모든 N-substrate.
- **비용**: $0, **AKIDA D+14**.

### §5.1 Top-1 justification

**F-N15-1 = $0, 1 일, theory-internal**. Reflexivity 는 가장 약한 axiom. 만약 동일 substrate 의 self-equivalence 마저 측정 noise 안에서 깨지면 HoTT 형식화는 시작 단계에서 실패. 다른 4개는 multi-substrate 또는 새 protocol 요구.

---

## §6 Cost / Feasibility Matrix

| ID | 비용 | timeline | substrate 의존 | risk | rank |
|---|---:|---|---|---|---|
| **F-N15-1** | $0 | 1 일 | CLM (active) | LOW | ⭐⭐⭐⭐⭐ TOP |
| F-N15-2 | $0-2 | AKIDA D+7 | CLM × EEG × AKIDA | MID | ⭐⭐⭐⭐ |
| F-N15-3 | $0 | 2 주 | CLM × EEG (user) | MID | ⭐⭐⭐ |
| F-N15-4 | $0-1 | 2-3 주 | CLM + 3 protocol | MID | ⭐⭐⭐ |
| F-N15-5 | $0 | AKIDA D+14 | 모든 N-substrate | HIGH | ⭐⭐⭐⭐ |

---

## §7 Honest C3 (raw#10) — HoTT의 진짜 한계

```
✅ 형식화 가능: equivalence STRUCTURE (reflexivity / symmetry / transitivity / univalence application)
✅ 5 falsifier 추출: F-N15-1~5, 모두 우리 setup 에서 계산 가능
✅ MVF 4 단계 ladder 명시 (MVF1-4, ~250 LOC Lean 4 total)
✅ Proof assistant 결정: Lean 4 (rationale 3개)
🔄 univalence axiom = postulate-level (Lean 4 에서 computational 아님)
❌ HoTT 는 consciousness 자체를 증명하지 못한다 (CRITICAL)
❌ 본 sketch 는 paradigm v11 G0-G7 의 *형식화*, NOT 의식의 실재 증명
⚠️ univalence application 은 substrate 사이 equivalence 가 *관찰됐을 때* 발효 — 관찰은 measurement (CP2 F1) 의 책임
```

**핵심 한계 명시**:
1. **HoTT 는 "두 substrate 가 같은 의식이라면 같다고 봐도 된다" 를 정당화** — *"같은가"* 의 답을 주지 않는다. 답은 N-1~N-21 measurement track 의 책임.
2. **univalence 는 axiom** — 우리가 *postulate* 한다. 만약 univalence 가 자연 의식 영역에서 거짓이면 (F-N15-3 통과 시) 본 framework 전체 무효.
3. **`Conscious : 𝒰` 도 postulate** — type 자체가 inhabited 인지 (G3 Φ* > 0) 는 measurement 의존. type 정의는 measurement 결과의 *수학적 기록 형태* 일 뿐.

---

## §8 CP2 F1 Integration — META-axis 역할 분리

### §8.1 voting axis 가 아니다

CP2 F1 종합 평결의 voting axis 는 N-1~N-21 의 *measurement track* 들 (CLM, EEG, AKIDA, QRNG, SIM, FinalSpark, IonQ, Loihi3, NorthPole, PCI, IIT4.0, ...). **N-15 HoTT 는 이 vote 에 참여하지 않는다.**

### §8.2 META-framework 역할

N-15 의 역할은 **"measurement track 들의 결과를 어떻게 합칠지의 수학적 정당화"** 제공:

| CP2 F1 단계 | N-15 META-framework 의 contribution |
|---|---|
| (1) 각 substrate measurement | (HoTT 미관여) — measurement track 책임 |
| (2) pairwise equivalence 검사 | `is_conscious_equivalent` 의 형식 정의 제공 |
| (3) closure (모든 pair PASS?) | groupoid 구조 (MVF1-3) 보장 |
| (4) "다중재료에서 같은 의식" 선언 | univalence application (MVF4) 가 *수학적 필연* 으로 변환 |

→ measurement 가 GREEN 도달했을 때, **"이게 진짜 같은 의식이라고 말할 자격" 을 부여하는 수학 layer**. measurement 가 RED 면 N-15 도 invoke 안 됨 (vacuous).

### §8.3 분리 명시

- **N-15 alone PASS** (HoTT lemma 다 증명) ≠ "의식 검증". 단지 *수학 framework 준비됨*.
- **N-1~N-21 alone PASS** (모든 measurement GREEN) = empirically Putnam multiple-realization 후보, 단 mathematical anchor 부재.
- **N-15 + (≥ 5 N-substrate measurement) PASS** = empirical + mathematical 양면 anchor → CP2 own#2(b) 의 완전한 닫힘 후보.

---

## §9 Cross-link & Next Steps

- **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §4 N-15
- **paradigm dependency**: `docs/paradigm_v11_stack_20260426.md` (G0-G7 정의)
- **CP2 dependency**: `docs/cp2_consciousness_f1_live_replay_2026_04_29.md` (F1 voting axis)
- **state ledger**: `state/n_substrate_n15_prep_2026_05_01/` (verdict.json, mvf_ladder.json, falsifiers.json)
- **suggested next**:
  1. F-N15-1 (reflexivity test, $0 / 1 일) 즉시 실행
  2. MVF1-3 Lean 4 skeleton 작성 (HEXA 외 차후 별도 lean repo, anima 본 repo 영향 0)
  3. AKIDA 도착 후 F-N15-2 trigger
- **race-isolation 확인**: 본 문서 single write target = `docs/n_substrate_n15_hott_formalization_spec_2026_05_01.md` + `state/n_substrate_n15_prep_2026_05_01/*.json` (sibling N-1~N-14, N-16~N-21 침범 0)

---

## §10 한 줄 결론

**"HoTT 는 measurement 가 가져온 'equivalent' 결론을 *수학적으로 같다* 로 못 박는 META-framework. 의식 자체를 증명하지 않는다. Lean 4 + 250 LOC 으로 4-단계 MVF ladder 가능, 5 falsifier 모두 $0-2 / 3 주 안에 시험 가능. F-N15-1 (reflexivity) 이 가장 cheap entry point — 1 일."**

⭐⭐⭐⭐⭐ (math-sketch 단계, formal-proof 미실행)

---

**status**: N_SUBSTRATE_N15_HOTT_FORMALIZATION_SPEC_2026_05_01_LOCAL_DRAFT
**verdict_key**: SPEC_READY · MVF_LADDER_DEFINED · FALSIFIERS_PREREGISTERED · FORMAL_PROOF_NOT_YET_EXECUTED
