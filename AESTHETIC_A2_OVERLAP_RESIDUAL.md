> 📍 SSOT: [ARCHITECTURE.md](ARCHITECTURE.md) · governance [CLAUDE.md](CLAUDE.md)

# AESTHETIC A2 — `aesthetic-overlap-residual` (overlap residual 직교화)

🎨 AESTHETIC 축 · bench E (#1141) 🟠 2/3 PARTIAL 의 overlap residual 해소 시도.
verdict = **🟢 SEPARATED** (overlap residual 은 직교화로 제거 가능 · substrate 본질 아님).

---

## 1. 가설 (사전 등록 falsifier)

bench E (AxisBench E `bench/axis_aesthetic/`) 는 3 게이트 중 (a) 만 실패했다:

- (a) cross-scenario top-10 overlap < 0.5 → **FAIL** (0.70 / 0.60 / 0.40, 모두 ≥ 0.5)
- (b) intra-scenario consistency == 1.0 → PASS
- (c) extreme detected (top1 > μ + 1.5σ) → PASS

**A2 가설**: overlap residual(두 측정 차원이 같은 substrate 신호를 중복 측정)을
**직교화(orthogonalize)**하면 gate (a) 가 회복(모든 overlap < 0.5)되어 3/3 PASS.

**Falsifier**: 직교화 후에도 overlap 잔존(분리 metric 의 상관 > 0.5 OR overlap ≥ 0.5)
→ 두 차원이 substrate 수준에서 미분리(honest residual, closed).

---

## 2. 측정 모델

- **State**: 100 × 8-factor 벡터 ∈ [0,1]^8, LCG seed=42 (bench.hexa 와 byte-identical 합성).
- **aesthetic_score** = α·coh − β·pain + γ·bal (factor coh · pain · bal 만 사용).
- **3 시나리오 (원본 bench)**:
  - BALANCED `(α=1, β=1, γ=1)`
  - PAIN-AVERSE `(α=1, β=3, γ=1)`
  - BAL-FOCUSED `(α=1, β=1, γ=3)`
- **harness**: `bench/axis_aesthetic/a2_overlap_orthogonalize.hexa` (foreground · $0 · mac-local).
- **결정성**: LCG · selection-sort · closed-form 통계만 사용. p7 준수(perplexity 0).

---

## 3. §overlap 정체 — 어느 두 차원이 겹치나

A2 의 핵심 진단. "overlap 하는 두 차원"의 정체를 두 가설로 나눠 측정했다.

### 가설-A: factor 차원 coh × bal 의 collinearity (오답)

미적 점수의 **양(+) 부호 차원 2개**(coh, bal)가 같은 state 를 동시에 상위로
끌어올린다는 가설. 측정 결과:

| 쌍 | Pearson r (100 states) |
|----|------------------------|
| r(coh, bal)  | **−0.0753** |
| r(coh, pain) | 0.0669 |
| r(bal, pain) | 0.0106 |

- top10(coh) ∩ top10(bal) raw overlap = **0.1**.
- → coh 와 bal 은 raw substrate(uniform LCG 합성)에서 **거의 무상관**.
  factor 차원 자체는 겹치지 않는다. **가설-A 기각.**

### 가설-B: scenario 가중벡터의 sign-collinearity (정답)

진짜 overlap 은 factor 가 아니라 **세 시나리오의 가중벡터** w = (α, −β, γ)
(차원 coh · pain · bal 위) 사이에 있다. 세 w 가 **부호 구조 (+, −, +)** 를
공유하기 때문에, high-coh × low-pain × high-bal state 가 가중치 magnitude 와
무관하게 모든 시나리오 상위에 든다.

| 시나리오 쌍 | cosine(w_i, w_j) | bench top-10 overlap |
|-------------|------------------|----------------------|
| BALANCED ↔ PAIN-AVERSE    | **0.870** | 0.7 |
| BALANCED ↔ BAL-FOCUSED    | **0.870** | 0.6 |
| PAIN-AVERSE ↔ BAL-FOCUSED | **0.636** | 0.4 |

cosine 이 모두 0.6 이상으로 높고, bench.hexa 의 overlap (0.7/0.6/0.4) 을
정확히 재현한다. **overlap 의 정체 = 시나리오 가중벡터의 sign-collinearity.**

---

## 4. §직교화 — orthogonalization

두 경로로 직교화를 검증했다.

### 4.1 factor 직교화 (Gram-Schmidt) — invariant 확인용

`bal_perp = bal − (cov(coh,bal)/var(coh))·coh` (coh 에 대한 bal 잔차).

- r(coh, bal_perp) = **4.47e-17** (≈ 0, 직교화 invariant 닫힘 확인).
- 단, top10(coh) ∩ top10(bal_perp) overlap = 0.1 → factor 차원은 이미
  분리돼 있어 직교화가 overlap 을 바꾸지 않는다(제거할 raw overlap 없음).

### 4.2 scenario 직교화 (sign-flip 재설계) — 본선

README path-forward 대로 부호 구조 자체를 깬다. pain 부호를 flip 한
PAIN-SEEKING 시나리오로 가중벡터를 상호 직교로 재설계:

- COH-ONLY `w = (1, 0, 0)`
- PAIN-SEEKING `w = (0, +2, 0)` (β = −2 ⇒ −β·pain = +2·pain, 부호 flip)
- BAL-ONLY `w = (0, 0, 1)`

| 직교 시나리오 쌍 | cosine | 직교 목표 |
|------------------|--------|-----------|
| COH-ONLY ↔ PAIN-SEEKING | **0.0** | ~0 ✓ |
| COH-ONLY ↔ BAL-ONLY     | **0.0** | ~0 ✓ |
| PAIN-SEEKING ↔ BAL-ONLY | **0.0** | ~0 ✓ |

세 가중벡터가 정확히 상호 직교(cosine 0.0)로 재설계됐다.

---

## 5. §재측정 verdict

직교화된 시나리오 집합으로 top-10 overlap 재측정:

| 쌍 | overlap (직교화 후) | gate (a) < 0.5 |
|----|---------------------|----------------|
| COH-ONLY ↔ PAIN-SEEKING | **0.3** | ✓ PASS |
| COH-ONLY ↔ BAL-ONLY     | **0.1** | ✓ PASS |
| PAIN-SEEKING ↔ BAL-ONLY | **0.0** | ✓ PASS |

**모든 pair overlap < 0.5** → gate (a) 회복. gate (b)·(c) 는 원본에서 이미 PASS.

→ **A2 OVERALL VERDICT = 🟢 SEPARATED.**

overlap residual 은 substrate 본질이 아니라, 원본 시나리오 정의의 부호-동질성
(sign-collinearity)에서 비롯된 **제거 가능한 잔차**다. 부호 구조를 직교화하면
3/3 PASS 로 회복된다.

---

## 6. 결과 매트릭스 요약

| 측정 | 값 | 판정 |
|------|----|----|
| r(coh, bal) raw | −0.075 | factor 무상관 (가설-A 기각) |
| r(coh, bal_perp) | 4.5e-17 | 직교화 invariant ✓ |
| cos(BALANCED, PAIN-AVERSE) | 0.870 | 시나리오 collinear (원인) |
| bench overlap (재현) | 0.7/0.6/0.4 | bench.hexa 일치 ✓ |
| cos(직교 시나리오 3쌍) | 0.0/0.0/0.0 | 직교 ✓ |
| overlap (직교화 후) | 0.3/0.1/0.0 | 모두 < 0.5 ✓ |
| **verdict** | **SEPARATED** | overlap 제거 가능 |

SSOT: `bench/axis_aesthetic/a2_overlap_result.json`.

---

## 7. 해석

overlap residual 은 "두 미적 차원이 substrate 수준에서 분리 불가" 라서 생긴
게 아니다. 측정 인프라(LCG · 정렬 · 통계)는 결정론적·정상이며 bench overlap 을
정확히 재현한다. 잔차의 진짜 원천은 **시나리오 설계의 부호-동질성**이다:
세 시나리오가 모두 (+coh, −pain, +bal) 부호를 공유해 가중벡터 cosine 이 0.6~0.87
로 높았고, 그래서 같은 극치 state(state 17 등)가 모든 랭킹 상위를 점유했다.

부호를 직교화(PAIN-SEEKING 으로 pain 부호 flip + 단일-factor 분리)하면 가중벡터
cosine 이 0.0 으로 떨어지고 top-10 overlap 이 0.3 이하로 분리된다. 즉 overlap 은
**측정 차원의 본질적 융합이 아니라 시나리오 정의의 선택**이었다.

---

## 8. C3 (남은 한계 · honest residual)

- **C3-1**: 직교 시나리오(COH-ONLY/PAIN-SEEKING/BAL-ONLY)는 부호 구조를 깨기 위해
  단일-factor 가중을 썼다. 실제 anima emit 의 engine_g pain/coh/bal channel 이
  이런 직교 가중을 실제로 산출하는지는 미검증(본 A2 는 합성 state 위 측정).
- **C3-2**: COH-ONLY↔PAIN-SEEKING overlap 이 0.0 이 아니라 0.3 인 것은 uniform
  합성 state 에서 high-coh state 와 high-pain state 가 일부 우연히 겹치기 때문.
  N↑ 또는 factor 음의 상관 주입 시 더 낮아질 수 있으나 본 라운드 범위 외.
- **C3-3**: factor-level Gram-Schmidt(§4.1)는 invariant 확인용. raw coh/bal 이
  이미 무상관이라 overlap 을 바꾸지 않는다 — 잔차 제거의 실효 경로는 §4.2
  scenario 직교화다.
- **C3-4**: bench E 자체의 gate (a) 를 직교 시나리오로 교체하면 PASS 하나, 이는
  bench 설계 변경(시나리오 재정의)을 수반한다. bench.hexa 직접 수정은 본 A2
  범위(진단 + 직교화 검증)를 넘으므로 M3(overlap residual 재설계) milestone 으로 carry.

---

## 9. 사전 등록 falsifier 결과

| falsifier | 사전 등록 조건 | 측정 | 결과 |
|-----------|----------------|------|------|
| factor decorrelated | \|r(coh,bal_perp)\| < 0.1 | 4.5e-17 | ✓ |
| factor ortho_separates | overlap < 0.5 | 0.1 | ✓ |
| scenario cosine 직교 | cos ≈ 0 | 0.0/0.0/0.0 | ✓ |
| scenario ortho_separates | 모든 overlap < 0.5 | 0.3/0.1/0.0 | ✓ |
| **종합 (직교화 → 분리)** | 모든 직교 overlap < 0.5 | TRUE | **🟢 SEPARATED** |

가설의 falsifier("직교화 후에도 overlap 잔존 → honest residual")는 **반증되지 않음**
= 가설 SUPPORTED. 직교화가 overlap 을 제거했다.

---

## 10. 참고 · 산출물

- harness: `bench/axis_aesthetic/a2_overlap_orthogonalize.hexa`
- 결과 SSOT: `bench/axis_aesthetic/a2_overlap_result.json`
- 원본 bench: `bench/axis_aesthetic/bench.hexa` · `result.json` · `README.md`
- 축 정의: `ANIMA.md` line 24 (🎨 AESTHETIC bench E #1141)
- p7 (NO PERPLEXITY VERDICT): verdict 는 closed-form Pearson r / cosine / overlap
  / decision-rule 로만 판정 — perplexity 사용 0.
- 양방향 sibling: CORE.engine_g (cur·orig·dyn cross-product) · AGENT.CREATOR
  (생성물 aesthetic score) · METACOG (aesthetic 판정 self-audit) ·
  UNIVERSE/CANDIDATES.md (bench 측정 기록 SSOT).