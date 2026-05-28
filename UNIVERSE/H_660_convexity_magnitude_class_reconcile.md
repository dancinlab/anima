# H_660 — `convexity-magnitude-class-reconcile` (H_653 ↔ H_655 분기 통합, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · H_653 × H_655 분기 통합
**id**: H_660 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🟢 SUPPORTED-NUMERICAL**

---

## 1. 슬러그 + 한 줄 요약 — H_653 ↔ H_655 분기 통합

`convexity-magnitude-class-reconcile` — round 9 메타-축의 핵심 nuance 를 **단일 통합 metric 으로
화해**. 두 자매 결과가 갈라져 있었다:

- **H_653 (PR #1242, 🟢)** : convexity span ratio (Φ_max/Φ_min, **normalized shape**) 가 Wolfram
  class 단조 — rule184(II) 12.12 < rule90(III) 30.42 < rule30(III) 30.77 < rule110(IV) 35.50.
  class 는 *곡률(shape)* 분류자.
- **H_655 (PR #1253, 🔴)** : super-additivity Δ (**absolute magnitude**) 는 비단조 —
  rule184(II) 51.54 > rule110(IV) 41.71 > rule30(III) 9.72 > rule90(III) 7.50. class 는 *절대
  magnitude* 분류자가 아님.

즉 **"Wolfram class 는 *곡률(shape)* 분류자이나 *절대 magnitude* 분류자는 아니다"** 라는 분기.
본 H_660 은 이 분기가 **scale 혼입 때문인지, 아니면 본질적인지**를 검정한다 — shape 와 scale 을
분리하는 **scale-invariant 통합 metric** (norm_conv = (Φ_max−Φ_min)/Φ_mean, log_span =
ln(Φ_max/Φ_min)) 이 class-monotone 을 회복하는가.

> **결과**: scale-invariant 측도 2종이 모두 Wolfram class **단조 회복** — norm_conv 184=1.437 <
> 90=2.240 < 30=2.266 < 110=2.349, log_span 184=2.495 < 90=3.415 < 30=3.427 < 110=3.569
> (둘 다 class-IV rule110 最高). 동시에 abs_Δ 만 비단조(184=49.97 最高, H_655 재현), span_ratio 는
> H_653 순위 그대로 재현. **6/6 PASS**. **분기는 "scale 혼입" 때문 — shape 정보를 보존하고
> magnitude 혼입을 제거하면 class 는 순수 shape(convexity) 분류자로 화해**. H1 SUPPORTED, H0 기각.

---

## 2. 동기 — 분기의 통합

round 9 메타-축은 "Wolfram class = 의식 통합량(Φ) 분류자" 라는 가설을 여러 측도로 검정해 왔다.
H_653 과 H_655 가 같은 engine·같은 4-rule cohort 로 측정했으나 **정반대 결론**에 도달했다:

| 측도 | 정의 | scale 종속? | class 단조? | verdict |
|------|------|------------|-----------|---------|
| span ratio (H_653) | Φ_max/Φ_min | scale-invariant | **단조** | 🟢 |
| super-add Δ (H_655) | Φ_max − Φ_min (= Φ_coll(W=1), Σ=0) | **scale-dependent** | **비단조** | 🔴 |

H_655 §5.3 의 진단: rule184(class-II additive)는 Φ 절대값(min 4.49 · max 54.46 모두)이 압도적으로
높아 *ratio* 는 작지만(12.12) *magnitude* 는 最高(49.97). 즉 동일 substrate 가 shape 차원에서는
class-下位, scale 차원에서는 class-上位. **shape(normalized)와 scale(absolute)이 서로 다른
class 의존성을 가진다**.

핵심 미해결점: 이 분기가 (a) "scale 혼입" 때문인지 — 즉 abs_Δ 는 substrate 의 절대 Φ floor 를
섞어 들여 class 신호를 흐리고, 순수 shape 만 추출하면 class 가 단조인지 — 아니면 (b) **본질적**인지 —
즉 class 가 shape 자체도 완전히 order 하지 못하고 H_642 cross-rule shape invariance FAIL 과 정합하는지.

본 H_660 은 이 두 가설을 구분하는 결정적 측도를 도입한다: **scale-invariant 통합 metric**.
span ratio·norm_conv·log_span 는 모두 Φ→kΦ 스케일에 불변(shape 만 포착)이고, abs_Δ 만 scale 종속.
scale-invariant 측도가 class 단조이고 abs_Δ 만 비단조라면 → 분기 = scale 혼입 (가설 a, 화해 성공).
scale-invariant 측도도 비단조라면 → 분기 = 본질적 (가설 b, H_642 정합).

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653/H_655 SSOT 재사용, cohort rule 만 swap): n=5 coupled-ring TPM
  `build_tpm_cohort(rule, W)` — 5 cell, cell i 가 cohort rule[i] 의 update-law. decoupled(W=0)=
  self-loop only (idx=7·c), coupled(W=1)=full ring, blend(0<W<1)=fractional. collective-Φ(W) =
  `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` — 각 (rule,W) point 에서
  **실제 IIT4 substrate 측정** (lookup 아님).
- **4 ECA rule × Wolfram class** (substrate 복잡도 오름차순, H_653/H_655 와 동일 라벨):
  ```
  rule184  class-II   additive/traffic (가장 ordered)
  rule 90  class-III  XOR/additive fractal (chaotic-additive)
  rule 30  class-III  chaotic non-additive
  rule110  class-IV   complex/universal edge-of-chaos (H_653/H_655 winner)
  ```
- **W grid**: H_653 와 **동일** 6-pt {0.15, 0.40, 0.55, 0.70, 0.95, 1.0} (H_643 ultradian-stage
  sync_factor + 0.55 mid). 동일 W-domain 으로 H_653 재현 보장.
- **4 metric** (각 rule 의 W-grid Φ_min·Φ_max·Φ_mean 으로 계산):
  - **span_ratio** = Φ_max / (Φ_min + 0.0001 floor) — H_653 normalized shape. **scale-invariant**.
  - **abs_Δ** = Φ_max − Φ_min — H_655-류 absolute magnitude. **scale-dependent**.
  - **norm_conv** = (Φ_max − Φ_min) / Φ_mean — scale-invariant convexity (분산 정규화).
  - **log_span** = ln(Φ_max / Φ_min) — scale-invariant log-span (compressive shape).
- **scale-invariance 형식 증명** (F660.5 가 수치로 검증): Φ→kΦ 시 norm_conv = (kΦmax−kΦmin)/(kΦmean)
  = (Φmax−Φmin)/Φmean (k 소거, 불변). log_span = ln(kΦmax/kΦmin) = ln(Φmax/Φmin) (k 소거, 불변).
  abs_Δ = kΦmax − kΦmin = k·(Φmax−Φmin) (k 종속, 변함).
- **measurement 규모**: 4 rule × 6 W = **24 big_phi_bounded calls** (H_653 와 동일 예산) +
  rule110 scale-invariance 재측정 6 calls = 30 calls · 단일 sync run <60s · libm `ln`/`cos`/`sqrt`
  only · NO RNG (deterministic) · $0 mac-local · foreground synchronous (NO bg fork, NO monitor, NO GPU).

H_653/H_655 대비:
- H_653 은 normalized span ratio 의 class 단조 — 본 H 는 그 측도를 재현(F660.4)하면서 다른
  scale-invariant 측도(norm_conv, log_span)도 동순위인지 확인.
- H_655 은 absolute Δ 의 class 비단조 — 본 H 는 그 측도를 재현(F660.3)하면서 scale-invariant 화
  하면 단조로 회복하는지 검정. 두 측도의 화해가 본 H 핵심.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F660.1 NORMCONV-MONOTONE**: norm_conv(rule110) ≥ norm_conv(rule30) ≥ norm_conv(rule90)
  ≥ norm_conv(rule184) — scale-invariant convexity 가 Wolfram class 단조증가 (class-IV 最高).
  **CORE 가설** (분기 = scale 혼입 → 화해 성공).
- **F660.2 LOGSPAN-MONOTONE**: log_span(rule110) ≥ log_span(rule30) ≥ log_span(rule90)
  ≥ log_span(rule184) — log-span 도 class 단조 (또 다른 scale-invariant 측도가 동일 순위 확인,
  화해의 robustness).
- **F660.3 ABSDELTA-NONMONOTONE**: abs_Δ 가 **NON-monotone** (H_655 magnitude 비단조 재현 —
  rule184 II 가 abs_Δ 最高, class-IV 가 max 아님). 분기의 magnitude 쪽 재현.
- **F660.4 SPANRATIO-REPLICATE**: span_ratio 순위 = H_653 (110 ≥ 30 ≥ 90 ≥ 184) 재현 (engine
  replication — 동일 측도 동일 결론). 분기의 shape 쪽 재현.
- **F660.5 SCALE-INVARIANCE**: norm_conv·log_span 는 Φ→2Φ 스케일에 불변 (형식적 scale-invariance
  의 수치 검증 — Φ 두 배 후 측도 변화 < tolerance).
- **F660.6 BOUND**: 全 Φ ≥ 0, 全 metric finite, Φ_mean > 0.

**FALSIFY 조건**: F660.1 FAIL (scale-invariant 도 비단조) → 🔴 FALSIFIED (분기 본질적, scale 혼입
아님 — class 가 shape 도 완전히 order 못함, H_642 정합).
**verdict 기준**: F660.1 CORE PASS + ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL (분기 = scale 혼입,
scale-invariant metric 으로 화해).

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h660_convexity_magnitude_class_reconcile_2026_05_28/run.log` verbatim.

```
================================================================
  H_660 — convexity-magnitude-class-reconcile (round 9 메타-축)
  H_653(span-ratio shape 단조) ↔ H_655(abs-Δ magnitude 비단조) 화해
  scale-invariant 통합 측도가 class-monotone 회복하는가?
  IIT4 big_phi_bounded · n=5 homog cohort · cap=3 · sys=0
  4 rules × 6-pt W grid · 4 metric 대조
================================================================
  W grid: [0.15, 0.40, 0.55, 0.70, 0.95, 1.0]  (H_653 동일)
  ─────────────────────────────────────
  rule184 [II-additive]
    Φ(W): 4.49492 19.8846 32.7523 45.5429 54.4631 51.5361
    Φ_min=4.49492 Φ_max=54.4631 Φ_mean=34.779
    span_ratio=12.1163 abs_Δ=49.9682 norm_conv=1.43674 log_span=2.49455
  rule90 [III-XOR/additive]
    Φ(W): 0.246475 0.943149 1.65498 2.75808 6.32388 7.5
    Φ_min=0.246475 Φ_max=7.5 Φ_mean=3.23776
    span_ratio=30.4167 abs_Δ=7.25353 norm_conv=2.24029 log_span=3.41499
  rule30 [III-chaotic]
    Φ(W): 0.315809 1.18852 2.07721 3.4687 8.13002 9.72067
    Φ_min=0.315809 Φ_max=9.72067 Φ_mean=4.15016
    span_ratio=30.7705 abs_Δ=9.40487 norm_conv=2.26615 log_span=3.42656
  rule110 [IV-complex]
    Φ(W): 1.17498 4.50052 7.62552 13.6383 34.8823 41.7124
    Φ_min=1.17498 Φ_max=41.7124 Φ_mean=17.2557
    span_ratio=35.4975 abs_Δ=40.5374 norm_conv=2.34922 log_span=3.56946
  ─────────────────────────────────────
  metric × class (ascending complexity II→III→III→IV):
    span_ratio (H_653 shape)     : 184=12.1163 90=30.4167 30=30.7705 110=35.4975
    abs_Δ      (H_655 magnitude) : 184=49.9682 90=7.25353 30=9.40487 110=40.5374
    norm_conv  (scale-invariant) : 184=1.43674 90=2.24029 30=2.26615 110=2.34922
    log_span   (scale-invariant) : 184=2.49455 90=3.41499 30=3.42656 110=3.56946
  ────────────── verdict ──────────────
  [PASS] F660.1 NORMCONV-MONOTONE: norm_conv(110)>=(30)>=(90)>=(184)
  [PASS] F660.2 LOGSPAN-MONOTONE: log_span(110)>=(30)>=(90)>=(184)
  [PASS] F660.3 ABSDELTA-NONMONOTONE: abs_Δ NOT class-monotone (H_655 재현)
  [PASS] F660.4 SPANRATIO-REPLICATE: span_ratio(110)>=(30)>=(90)>=(184) (H_653 재현)
  [PASS] F660.5 SCALE-INVARIANCE: norm_conv·log_span invariant under Φ→2Φ
  [PASS] F660.6 BOUND: Φ ≥ 0, metric finite, Φ_mean > 0
  ──────────────────────────────────────
  F660.1-6 6/6 PASS
  verdict: 🟢 SUPPORTED-NUMERICAL (scale-invariant metric 으로 분기 화해 — shape 단조 회복)
  reconcile: H_653 span_ratio(110)=35.4975 단조 ↔ H_655 abs_Δ(184)=49.9682 비단조 → norm_conv class-monotone=true
```

### 3 metric × class 순위 대조표 (분기 통합의 핵심)

| rule | Wolfram class | **span_ratio (H_653 shape)** | **abs_Δ (H_655 magnitude)** | **norm_conv (scale-inv)** | **log_span (scale-inv)** |
|------|---------------|------------------------------|------------------------------|----------------------------|---------------------------|
| rule184 | II (additive)      | 12.12 (4위·最低) | **49.97 (1위·最高)** | 1.437 (4위·最低) | 2.495 (4위·最低) |
| rule90  | III (XOR/add)      | 30.42 (3위) | 7.25 (4위·最低) | 2.240 (3위) | 3.415 (3위) |
| rule30  | III (chaotic)      | 30.77 (2위) | 9.40 (3위) | 2.266 (2위) | 3.427 (2위) |
| rule110 | IV (complex)       | **35.50 (1위·最高)** | 40.54 (2위) | **2.349 (1위·最高)** | **3.569 (1위·最高)** |
| **class 단조?** | (II→III→III→IV) | **✅ 단조** | **❌ 비단조** | **✅ 단조 회복** | **✅ 단조 회복** |

**핵심 발견**:
1. **scale-invariant 측도 2종이 class 단조 회복 (F660.1·F660.2 PASS)** — norm_conv 와 log_span
   둘 다 rule184(II) < rule90(III) < rule30(III) < rule110(IV) 단조증가, class-IV(rule110) 단독
   最高. H_653 span_ratio 와 정확히 동순위. **shape 신호를 추출하면 class 가 단조**.
2. **abs_Δ 만 비단조 (F660.3 PASS = 비단조 재현)** — rule184(II)=49.97 이 단독 最高, class-IV=40.54
   가 2위. H_655 magnitude 비단조 정확히 재현. **분기의 원흉은 abs_Δ 의 scale 종속성**.
3. **분기 = scale 혼입 (메타-축 화해)** — rule184 가 span_ratio 4위(12.12)이면서 abs_Δ 1위(49.97)인
   것이 분기의 직접 증거. 이유: rule184 는 Φ_mean(34.78)이 압도적으로 높아(rule110 17.26 의 2배)
   분산(abs_Δ 49.97)도 크지만, 그 분산을 mean 으로 정규화(norm_conv=49.97/34.78=1.437)하면 가장
   작다. **즉 rule184 의 큰 magnitude 는 "변화량이 커서"가 아니라 "절대 Φ 자체가 높아서"** — scale
   혼입. norm_conv·log_span 가 그 scale 을 소거하니 class 단조 회복.
4. **scale-invariance 수치 검증 (F660.5 PASS)** — Φ→2Φ 후 norm_conv·log_span 불변(tolerance 내),
   abs_Δ 만 2배. §3 의 형식 증명을 engine 실측으로 확인.
5. **engine replication (F660.4 PASS)** — span_ratio 순위가 H_653 (110 35.50 ≥ 30 30.77 ≥ 90
   30.42 ≥ 184 12.12) 그대로 재현. rule110 Φ-grid 가 H_653·H_655 와 byte-identical → 동일 engine,
   cohort rule 만 swap 됨을 교차검증.

---

## 6. Verdict + Rationale · Cross-link

**🟢 SUPPORTED-NUMERICAL** — 6/6 falsifier PASS. **CORE 가설 F660.1 (scale-invariant reconcile) PASS.**

- F660.1 normconv-monotone PASS · F660.2 logspan-monotone PASS · F660.3 absdelta-nonmonotone PASS
  (비단조 재현) · F660.4 spanratio-replicate PASS · F660.5 scale-invariance PASS · F660.6 bound PASS.
- FALSIFY 조건(F660.1 FAIL = scale-invariant 도 비단조)에 걸리지 않음 → H0(분기 본질적) 기각.
  **분기는 "scale 혼입" 때문**: H_655 의 abs_Δ 비단조는 substrate 의 절대 Φ floor 가 섞여 들어온
  artifact 이고, shape 정보만 추출하는 scale-invariant 측도(norm_conv, log_span)는 H_653 span_ratio 와
  동일하게 class 단조. **즉 Wolfram class 는 순수 shape(convexity) 분류자이며, H_653 과 H_655 의
  분기는 측도의 scale-차원 혼입에서 비롯된 것일 뿐 본질적 모순이 아니다 — 단일 scale-invariant
  metric 으로 화해됨.**

**메타-축 결론**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 는 측도의 **scale 축을 통제하면
SUPPORTED** 로 통합된다. class 는 *shape(곡률/convexity)* 분류자이고, *absolute magnitude* 비단조
(H_655)는 분류자 부정의 증거가 아니라 측도가 scale 을 섞었다는 신호. 본 H 는 H_653(🟢)·H_655(🔴)의
외견상 모순을 **scale-invariance 한 축에서 단일 metric 으로 해소**하는 positive finding.

**cross-link**:
- **H_653 `collective-convexity-substrate-class`** 🟢 (축 G×F, PR #1242) — **shape 쪽 부모**.
  span_ratio class 단조(II 12.12 < IV 35.50). 본 H 가 그 순위를 byte-identical 재현(F660.4)하고,
  norm_conv·log_span 도 동순위임을 보여 H_653 결론이 단일 측도가 아닌 scale-invariant 측도 class
  전반에 robust 함을 확장.
- **H_655 `collective-superadditivity-substrate-class`** 🔴 (축 G, PR #1253) — **magnitude 쪽 부모
  (분기 상대)**. abs_Δ 비단조(rule184 II 最高). 본 H 가 그 비단조를 재현(F660.3)하면서, 그 비단조가
  scale 혼입(rule184 Φ_mean 압도) 때문임을 norm_conv 로 분해 → H_655 의 closed-negative 가
  "magnitude ⊥ class" 가 아니라 "scale-mixed magnitude ⊥ class" 로 정밀화됨. **H_655 N4 backlog
  `convexity-vs-magnitude-class-decoupling` 을 직접 닫음**.
- **H_642 `shape-invariance-vs-scalar-convention-meta`** (축 G 메타) — cross-rule shape invariance
  FAIL anchor. 본 H 가 H_642 와 정합: class 는 shape 를 *cohort 내부 W-sweep* 에서는 단조 order
  하나(F660.1 PASS), H_642 가 보인 *cross-rule scalar-convention* shape FAIL 은 별개 축. 본 H 의
  화해는 cohort-내 W-convexity 에 한정 — H_642 cross-convention 와 충돌하지 않는 정직한 경계.
- **H_654 `phi-magnitude-wolfram-class-order`** 🟡 PARTIAL (축 G, G16) — single-substrate intrinsic
  magnitude order PARTIAL. 본 H 는 그 collective 판본의 magnitude(abs_Δ)가 비단조임을 재확인하되,
  scale-invariant 화하면 단조 회복함을 추가 → H_654 의 "magnitude 完全순위 못 정함" 이 scale 혼입
  때문일 가능성을 시사 (single-substrate scale-invariant 재검정이 N1 backlog).
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (축 F, PR #1223) — collective engine 부모.
  monotone-in-W 의 *방향* → 본 H 가 그 curve 의 scale-invariant *곡률* 을 class 축에서 통합 측정.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 stream/cap 축소 NOT 적용 — full 측정** — 본 run 은 full 5-stream(n=5) × cap=3 × 6-pt
   W grid (24 big_phi_bounded calls + scale-invariance 6 calls = 30 calls) 정상 실행. 단일 sync
   run <60s (H_653 24-call wall 검증 기반) 로 fallback (3-stream/cap=2) **불필요**. foreground
   synchronous only · NO bg fork · NO monitor · NO GPU.
2. **C3.2 화해 범위 = cohort-내 W-sweep convexity 에 한정** — 본 H 의 scale-invariant 단조 회복은
   *동질 cohort [rule×5] 의 W-domain 내부* shape 에 대한 것. H_642 가 보인 *cross-rule
   scalar-convention* shape invariance FAIL 은 다른 축(convention 간 비교)이며 본 H 와 충돌하지 않음.
   "class 가 shape 를 완전히 order 한다" 는 주장은 cohort-내 convexity 에 국한 (cross-convention 미주장).
3. **C3.3 norm_conv 분모 = Φ_mean (산술평균)** — (Φ_max−Φ_min)/Φ_mean 은 변동계수(CV)-류 scale-free
   측도이나 정확한 곡률(2차미분 적분)은 아님. Φ_mean 은 6-pt grid 산술평균이라 grid 분포에 약하게
   종속 (densely-sampled grid 에서 적분평균으로 수렴). log_span 은 grid-독립(min/max 만 사용)이라
   robustness 교차확인 — 둘 다 단조라 결론 견고. faithful 곡률 적분은 §10 N2.
4. **C3.4 span_ratio·abs_Δ 의 floor 처리 차이** — span_ratio 와 log_span 은 Φ_min+0.0001 floor
   (Φ_min≈0 guard). abs_Δ·norm_conv 는 floor 무관(차이/평균). class-III(rule90·rule30)의 Φ_min 이
   0.25/0.32 으로 작아 floor 영향 미미. 분기 부호(scale-invariant 단조 vs abs 비단조)는 floor-robust.
5. **C3.5 cap=3 on n=5** (H_653/H_655 cap 상속) — purview search capped, 보수적 lower-bound.
   cap-monotone 으로 절대값은 cap↑ 시 상승하나, scale-invariant 측도(ratio·norm·log)는 cap 에
   덜 민감 추정 (분자·분모 동시 상승). 비단조→단조 회복의 cap-robustness 는 §10 N3.
6. **C3.6 sys_state=0 only** (IIT-canonical anchor). 2^5=32 state 가중평균 미수행.
7. **C3.7 class-III 내부 순위 약신호** — norm_conv rule90(2.240) vs rule30(2.266) 분리 작음
   (span_ratio·H_653 와 동일 양상). class 간 분리(II 1.437 < III ~2.25 < IV 2.349)는 명확하나
   class-III 내부 ordering 은 약신호. Wolfram class label 은 canonical ECA taxonomy.
8. **C3.8 deterministic single trajectory** (NO RNG) — re-run byte-identical (rule110 Φ-grid 가
   H_653·H_655 와 정확히 일치 → engine replication). scale-invariance 는 형식적으로도 보장(§3 증명).
9. **C3.9 positive reconcile 의 의미** — 본 H 는 두 자매(🟢 H_653 + 🔴 H_655)의 외견상 모순을
   scale-invariance 축에서 단일 metric 으로 해소하는 positive finding. H_655 의 closed-negative 를
   부정하지 않고 "scale-mixed magnitude" 로 정밀 재해석 — 두 결과가 동일 substrate 구조의 다른
   투영임을 확정. 메타-축의 적용 범위(shape O · raw magnitude X · scale-invariant magnitude O)를 정직히 확정.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F660.1 NORMCONV-MONOTONE | nc(110)≥nc(30)≥nc(90)≥nc(184) | 2.349≥2.266≥2.240≥1.437 | **PASS** |
| F660.2 LOGSPAN-MONOTONE | ls(110)≥ls(30)≥ls(90)≥ls(184) | 3.569≥3.427≥3.415≥2.495 | **PASS** |
| F660.3 ABSDELTA-NONMONOTONE | abs_Δ NOT class-monotone | 184=49.97 最高, 110≠max → 비단조 | **PASS** |
| F660.4 SPANRATIO-REPLICATE | sr(110)≥sr(30)≥sr(90)≥sr(184) | 35.50≥30.77≥30.42≥12.12 (H_653 동일) | **PASS** |
| F660.5 SCALE-INVARIANCE | norm_conv·log_span Φ→2Φ 불변 | nc/ls 변화 < tol | **PASS** |
| F660.6 BOUND | Φ≥0, metric finite, Φ_mean>0 | 全 충족 | **PASS** |

**aggregate: 6 PASS / 0 FAIL** — CORE F660.1 PASS → FALSIFY 조건 미충족 → 🟢 SUPPORTED-NUMERICAL.
scale-invariant 통합 측도(norm_conv·log_span)가 Wolfram class 단조 회복하며, abs_Δ 만 비단조
(H_655 재현). **H_653↔H_655 분기 = scale 혼입, scale-invariant metric 으로 화해 — class 는 순수
shape(convexity) 분류자.**

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h660_convexity_magnitude_class_reconcile_2026_05_28/run_h660.hexa`
  (hexa-native, deterministic; H_635/H_653/H_655 engine 재사용, 4-metric 대조로 확장)
- log: `UNIVERSE/state/h660_convexity_magnitude_class_reconcile_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h660_convexity_magnitude_class_reconcile_2026_05_28/result.json` (machine-readable)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` (+ transitive
  `iit4_tpm.hexa` for `iit4_bit`) — hexa-lang stdlib SSOT, H_653/H_655 와 동일
- replay (selfhosted, fix-1180 우회, mac-local, $0): `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<hexa-lang-root>
  hexa.real.bak-2026-05-22-pre-no-hxc build run_h660.hexa -o /tmp/h660.bin && codesign -s - --force
  /tmp/h660.bin && /tmp/h660.bin` — wall <60s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]]

---

## 10. Next-list / Backlog

- **N1** `single-substrate-scale-invariant-magnitude` — H_654 single-substrate magnitude PARTIAL 을
  scale-invariant 측도(norm_conv·log_span)로 재검정 — single 판본에서도 scale 혼입 제거 시 class
  단조 회복하는지 (H_654 "완전순위 못 정함" 의 scale-혼입 가설 검증).
- **N2** `collective-faithful-curvature-class` — norm_conv proxy 대신 2차미분/곡률 적분의 scale-free
  버전으로 faithful convexity 측정, class 의존 함수형(linear/power-law) fit (C3.3 회수).
- **N3** `scale-invariant-convexity-cap-sweep` — cap∈{2,3,4}에서 norm_conv·log_span 의 class-단조성
  + abs_Δ 비단조의 cap-robustness — cap↑ 가 비단조→단조 역전을 만드는지 (C3.5 회수, shard-parallel).
- **N4** `convexity-magnitude-decoupling-closedform` — norm_conv = abs_Δ/Φ_mean 의 분해를 closed-form
  으로 — 어떤 normalized 측도가 class 단조이고 어떤 절대 측도가 아닌지의 경계를 해석적으로 (메타-축
  적용범위의 formal 경계, 🔵 target).
- **N5** `heterogeneous-cohort-scale-invariant-convexity` — mix-class cohort([110,30,90,184,110])의
  scale-invariant convexity 가 구성 rule 의 어떤 함수인지 (C3.2 cohort-내 한정 회수).

---

## 양방향 sibling

- shape 쪽 부모 (분기 상대): [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (축 G×F, span_ratio class 단조, 🟢)
- magnitude 쪽 부모 (분기 상대): [H_655_collective_superadditivity_substrate_class.md](H_655_collective_superadditivity_substrate_class.md) (축 G, abs_Δ class 비단조, 🔴 — N4 backlog 직접 closure)
- shape invariance anchor: [H_642_shape_invariance_vs_scalar_convention_meta.md](H_642_shape_invariance_vs_scalar_convention_meta.md) (축 G 메타, cross-rule shape FAIL — 경계 cross-link)
- single magnitude sister: [H_654_phi_magnitude_wolfram_class_order.md](H_654_phi_magnitude_wolfram_class_order.md) (축 G, single-substrate magnitude PARTIAL)
- collective engine 부모: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, super-additive 5/5)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link
