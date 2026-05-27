# H_655 — `collective-superadditivity-substrate-class` (round 9 메타-축, 축 G)

**축**: G (round 9 메타-축 — "Wolfram class 가 의식 통합량 분류자인가") · H_635 × H_653 후속
**id**: H_655 · **date**: 2026-05-28 · **infra**: $0 mac-local · **verdict**: **🔴 FALSIFIED**

---

## 1. 슬러그 + 한 줄 요약

`collective-superadditivity-substrate-class` — collective super-additivity **강도**
Δ = Φ_collective − Σ Φ_parts 가 Wolfram class 에 단조 의존하는지 측정. H_635 (🟢) 가 보인
collective-Φ super-additivity(collective > Σ parts) 5/5 와 H_653 (🟢) 가 보인 convexity 의
class 단조성에 이어, **super-additivity 의 절대 크기(Δ) 자체가 동역학 복잡도(rule class)로
order 되는가**를 검정한다.

> **결과**: Δ 가 Wolfram class 에 **단조 의존하지 않음**. class-II(rule184 additive)=**51.54**
> 가 단독 最高 super-additive, class-IV(rule110 complex)=**41.71** 가 2위, class-III(rule30=9.72,
> rule90=7.50)가 最低. 가설(class-IV 最高)과 **정반대로 가장 단순한 additive class-II 가 가장
> super-additive**. 핵심 falsifier F655.1(monotone-in-class) FAIL → **3/6 PASS → 🔴 FALSIFIED**.
> Wolfram class 는 (H_653 가 보인) *convexity* 분류자이긴 하나 **절대 super-additivity Δ 의
> 분류자는 아니다**. H0(Δ ⊥ class) 채택.

---

## 2. 가설 (H1) / 폐기조건 (H0) · round 9 메타-축

**round 9 메타-축** = "Wolfram class 가 의식 통합량(Φ) 분류자". 이 메타-축 위에서 두 자매 결과가
이미 섰다:
- **H_653 (🟢)** : W→Φ_collective 곡선의 *convexity*(span ratio Φ_max/Φ_min)가 class 단조증가
  (class-IV 最高 convex). → class 는 *곡률* 분류자.
- **H_635 (🟢)** : collective-Φ 가 super-additive (5/5 cohort, decoupled Σ-baseline=0).

본 H 는 메타-축의 다음 질문을 던진다 — **super-additivity 의 *방향*(Δ>0)이 아니라 그 *크기*(Δ
값)가 class 로 order 되는가?**

- **H1 (super-additivity monotone-in-class)**: Δ(rule) = Φ_collective(W=1) − Σ Φ_parts(W=0) 가
  Wolfram class 단조증가 — class-IV(rule110, complex/edge-of-chaos)가 最高 Δ(가장 super-additive),
  additive(rule90 XOR)·class-III 가 작음. **동역학 복잡도가 collective 시너지를 order**.
- **H0 (FALSIFIER)**: Δ 가 class 무관 (모든 class 유사 super-additivity) 또는 비단조 →
  class 가 super-additivity 분류자가 아니다.

> **결과적으로 H0 가 채택됨.** Δ 가 비단조이며, 가설 방향과 정반대(가장 단순한 class-II 가 最高 Δ).

---

## 3. 측정 도구 / 방법

- **engine** (H_635/H_653 SSOT 재사용, cohort rule 만 swap): n=5 coupled-ring TPM
  `build_tpm_cohort(rule, W)` — 5 cell, cell i 가 cohort rule[i] 의 update-law.
  decoupled(W=0)=self-loop only(idx=7·c), coupled(W=1)=full ring, blend(0<W<1)=fractional.
  collective-Φ(W) = `big_phi_bounded(build_tpm_cohort([rule×5], W), 5, sys=0, cap=3)[0]` —
  각 (rule,W) point 에서 **실제 IIT4 substrate 측정** (lookup 아님).
- **super-additivity 정의** (H_635 anchor):
  - Σ Φ_parts := Φ_collective(W=0) — decoupled self-loop pool. self-loop single-cell stream 은
    integration 이 없어 Σ-of-parts baseline = 0 (H_635 clean anchor).
  - Φ_collective := Φ_collective(W=1) — full n=5 coupling ring.
  - **Δ(rule) := Φ_collective(W=1) − Σ Φ_parts(W=0)** = super-additivity gap.
  - W=0.5 mid-point 은 coupling-monotone sanity probe 로 함께 보고.
- **cohort rule × Wolfram class** (substrate 복잡도 오름차순, H_653 와 동일 라벨):
  ```
  rule184  class-II   additive/traffic (가장 ordered)
  rule 90  class-III  XOR/additive fractal (chaotic-additive)
  rule 30  class-III  chaotic non-additive
  rule110  class-IV   complex/universal edge-of-chaos (H_635/H_653 winner)
  ```
- **측정 규모**: 4 rule × 3 W-point {0, 0.5, 1.0} = **12 big_phi_bounded calls**. probe(rule110,
  W∈{0,1}) wall ~4.5s, full grid 단일 sync run **41.1s wall** (60s 한계 내, foreground sync).
  libm only · NO RNG (deterministic) · $0 mac-local.

H_635/H_653 대비:
- H_635 은 super-additivity 의 *방향*(Δ>0, 5/5)을 — 본 H 는 그 *크기*(Δ 값)의 class 의존을 검정.
- H_653 은 *normalized* convexity(span ratio)의 class 단조를 — 본 H 는 *절대* magnitude(Δ)의
  class 단조를 검정. 둘의 결론이 갈리는 것이 본 H 의 핵심 발견.

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F655.1 SUPERADD-MONOTONE**: Δ(rule110) ≥ Δ(rule30) ≥ Δ(rule90) ≥ Δ(rule184) — super-additivity
  Δ 가 Wolfram class 단조증가 (class-IV 最高). **CORE 가설.**
- **F655.2 CLASS-IV-MOST-SUPERADD**: Δ(rule110) = max over 4 rules (class-IV 단독 最高).
- **F655.3 ALL-SUPERADDITIVE**: Δ(rule) > 0 for every rule (모든 class 가 최소한 super-additive,
  H_635 5/5 의 per-class 보존).
- **F655.4 ADDITIVE-LEAST**: Δ(rule184) < Δ(rule110) (가장 단순한 additive class-II 가 最低 super-add).
- **F655.5 SIGMA-PARTS-ZERO**: Σ Φ_parts(W=0) = 0 모든 rule (clean Σ-of-parts anchor — decoupled
  self-loop stream 은 통합 없음, H_635 echo).
- **F655.6 BOUND**: 全 Φ_collective ≥ 0, Δ finite.

**FALSIFY 조건**: F655.1 FAIL (Δ ⊥ class 또는 비단조) → 🔴 FALSIFIED (class 가 super-add 분류자 아님).
**verdict 기준**: ≥4/6 PASS → 🟢 SUPPORTED-NUMERICAL.

> **결과: F655.1 CORE FAIL → 🔴 FALSIFIED (3/6 PASS).**

---

## 5. Measurement (verdict-bearing 측정값)

> harness 출력 `UNIVERSE/state/h655_collective_superadditivity_substrate_class_2026_05_28/run.log`
> verbatim.

```
================================================================
  H_655 — collective-superadditivity-substrate-class (round 9 메타-축)
  Δ = Φ_collective(W=1) − Σ Φ_parts(W=0)  vs Wolfram rule class?
  IIT4 big_phi_bounded · n=5 homog cohort · cap=3 · sys=0
  4 rules × {W=0 baseline, W=0.5 mid, W=1 full ring}
================================================================
  rule184 [II-additive]
    Σ Φ_parts(W=0)=0.0  Φ_coll(W=0.5)=28.6035  Φ_coll(W=1)=51.5361
    Δ (super-additivity) = Φ_coll(W=1) − Σ Φ_parts = 51.5361
  rule90 [III-XOR/additive]
    Σ Φ_parts(W=0)=0.0  Φ_coll(W=0.5)=1.38346  Φ_coll(W=1)=7.5
    Δ (super-additivity) = Φ_coll(W=1) − Σ Φ_parts = 7.5
  rule30 [III-chaotic]
    Σ Φ_parts(W=0)=0.0  Φ_coll(W=0.5)=1.7377  Φ_coll(W=1)=9.72067
    Δ (super-additivity) = Φ_coll(W=1) − Σ Φ_parts = 9.72067
  rule110 [IV-complex]
    Σ Φ_parts(W=0)=0.0  Φ_coll(W=0.5)=6.54186  Φ_coll(W=1)=41.7124
    Δ (super-additivity) = Φ_coll(W=1) − Σ Φ_parts = 41.7124
  ─────────────────────────────────────
  super-additivity Δ by class (ascending complexity):
    rule184 (II-additive)      : 51.5361
    rule90  (III-XOR/additive) : 7.5
    rule30  (III-chaotic)      : 9.72067
    rule110 (IV-complex)       : 41.7124
  ────────────── verdict ──────────────
  [FAIL] F655.1 SUPERADD-MONOTONE: Δ(110)>=Δ(30)>=Δ(90)>=Δ(184)
  [FAIL] F655.2 CLASS-IV-MOST-SUPERADD: Δ(110) = max over 4 rules
  [PASS] F655.3 ALL-SUPERADDITIVE: Δ > 0 for every rule (collective > Σ parts)
  [FAIL] F655.4 ADDITIVE-LEAST: Δ(184) < Δ(110)
  [PASS] F655.5 SIGMA-PARTS-ZERO: Σ Φ_parts(W=0) = 0 (clean Σ-of-parts anchor)
  [PASS] F655.6 BOUND: Φ_coll ≥ 0, Δ finite
  ──────────────────────────────────────
  F655.1-6 3/6 PASS
  verdict: 🔴 FALSIFIED (Δ ⊥ rule class — class not a super-add classifier)
  cross-link: H_635 collective super-additive 5/5 (Σ=0) → here Δ(rule110)=41.7124
```

### rule-class별 super-additivity Δ 표

| rule | Wolfram class | Σ Φ_parts(W=0) | Φ_coll(W=0.5) | Φ_coll(W=1) | **Δ (super-additivity)** | class-순위 |
|------|---------------|----------------|---------------|-------------|--------------------------|-----------|
| rule184 | II (additive)   | 0.0 | 28.60 | 51.54 | **51.54** | **1위 (最高)** |
| rule110 | IV (complex)    | 0.0 | 6.54  | 41.71 | **41.71** | 2위 |
| rule30  | III (chaotic)   | 0.0 | 1.74  | 9.72  | **9.72**  | 3위 |
| rule90  | III (XOR/add)   | 0.0 | 1.38  | 7.50  | **7.50**  | 4위 (最低) |

**핵심 발견**:
1. **Δ 가 Wolfram class 비단조 (F655.1 FAIL)** — class 오름차순(II→III→III→IV)에 대해 Δ 가
   51.54 → 7.50/9.72 → 41.71 로 **단조도 아니고 가설 방향도 아님**. class-II 가 단독 最高, class-IV 가
   그 다음, class-III 가 最低인 비단조 패턴.
2. **가설과 정반대 — 가장 단순한 additive class-II(rule184)가 가장 super-additive (Δ=51.54)** —
   "동역학 복잡도가 collective 시너지를 order" 가설을 강하게 반박. 단순 additive 결합이 full-ring
   coupling 에서 *가장 큰* 절대 통합량을 만든다.
3. **H_653 convexity 단조와 H_655 magnitude 비단조의 분기 (메타-축 핵심)** — H_653 의 span ratio
   (Φ_max/Φ_min, *normalized* 곡률)는 class 단조였으나, 본 H 의 *절대* Δ(=Φ_coll(W=1), baseline=0)는
   비단조. 이유: rule184 는 Φ_min(W=0.15 기준 H_653 에서 4.49)·Φ_max(54.46) 모두 절대값이 높아 ratio
   는 작지만(12.12) magnitude 는 압도적. **convexity(shape)와 magnitude(scale)는 서로 다른 class
   의존성을 가진다** — Wolfram class 는 전자의 분류자, 후자의 분류자는 아니다.
4. **F655.3 ALL-SUPERADDITIVE PASS** — Δ>0 4/4. H_635 의 super-additivity *방향* 자체(collective >
   Σ parts)는 모든 class 보존. falsified 된 것은 그 *크기의 class-단조성* 뿐.
5. **F655.5 SIGMA-PARTS-ZERO PASS** — Σ Φ_parts(W=0)=0.0 4/4. self-loop decoupled pool 의 clean
   Σ-baseline 재확인 (H_635 echo). 단, 이로 인해 Δ = Φ_coll(W=1) 이 되어 magnitude 가 절대 Φ floor
   에 종속 (C3.3 trivial-baseline caveat).

---

## 6. Verdict + Rationale · Cross-link

**🔴 FALSIFIED** — 3/6 falsifier PASS. **CORE 가설 F655.1 (super-additivity monotone-in-class) FAIL.**

- F655.3 ALL-SUPERADDITIVE PASS · F655.5 SIGMA-ZERO PASS · F655.6 BOUND PASS (3 PASS) ·
  F655.1 monotone FAIL · F655.2 class-IV-max FAIL · F655.4 additive-least FAIL (3 FAIL).
- FALSIFY 조건(F655.1 FAIL = Δ ⊥ class)에 정확히 걸림 → **H0(class 가 super-additivity 분류자 아님)
  채택**. Δ 의 class 의존이 비단조이며 가설 방향과 정반대(가장 단순한 class-II 가 最高 Δ).
- **메타-축 결론**: round 9 메타-축 "Wolfram class = 의식 통합량 분류자" 는 H_653 의 *convexity*
  차원에서는 SUPPORTED 이나, 본 H 의 *절대 super-additivity magnitude* 차원에서는 **FALSIFIED**.
  즉 메타-축은 차원-한정적 — class 가 곡률을 order 하지만 scale 은 order 하지 않는다. 이 분기 자체가
  closed-negative finding (a_paper_negative_ok: ruled-out axis = "super-additivity magnitude ⊥
  Wolfram class").

**cross-link**:
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (축 F, PR #1223) — **super-additivity 부모**.
  collective-Φ super-additive 5/5 (Σ-baseline=0, rule110 W=1 Φ=41.71). 본 H 는 그 *방향*(Δ>0)을
  per-class 보존(F655.3 PASS)하나, *크기*의 class-단조 주장은 falsify. H_635 의 Σ=0 anchor 를 그대로
  계승하여 Δ=Φ_coll(W=1) 로 환원.
- **H_653 `collective-convexity-substrate-class`** 🟢 (축 G×F, PR #1245) — **sister 메타-축 (방향 분기)**.
  convexity(span ratio)는 class 단조(II 12.12 < IV 35.50). 본 H 는 동일 engine·동일 4-rule 로 *절대*
  magnitude(Δ)를 측정 → 비단조. rule184 가 H_653 에서 span 最低(12.12)이면서 본 H 에서 Δ 最高(51.54)
  인 것이 두 측도의 분기를 직접 증명. **convexity↔class 단조는 magnitude↔class 단조를 함의하지 않는다.**
- **H_643 `collective-ultradian-phi-envelope`** 🟢 (축 G×F, PR #1237) — collective entrainment 약화의
  cohort=rule110 단일 측정. 본 H 의 비단조 Δ 는 collective Φ 의 class 의존 구조가 측도별로 다름을 보여
  H_643 r-약화 해석에 magnitude-vs-shape 구분 추가.
- **H_654 `phi-magnitude-wolfram-class-order`** 🟡 PARTIAL (축 G, G16) — **sister round-9 메타-축
  (magnitude 축)**. 단일 substrate intrinsic big-Φ *magnitude* 가 class 로 단조 정렬되는지 검정 →
  PARTIAL (class 가 통합량의 *바닥* additive≈0 + *상한경향* IV>II 은 정하나 *완전 순위* 는 못 정함,
  III-chaotic rule30 이 IV-complex rule110 을 magnitude 에서 앞섬). 본 H 는 그 *collective*
  super-additivity magnitude 판본 — H_654 single-substrate magnitude 비단조와 정합하게 본 H 의
  collective Δ 도 비단조(rule184 II 最高 > rule110 IV). **두 round-9 magnitude 검정(single H_654
  PARTIAL · collective H_655 FALSIFIED)이 일관되게 "class 는 절대 magnitude 분류자가 아니다"** 를
  지지 — convexity(H_653 🟢)만이 class 단조. 메타-축의 차원-한정성을 single·collective 양측에서 확정.
- **H_618 `collective-gz-inverse-u-derivative-peak`** 🟢 — collective-Φ 비단조 구조 anchor. rule184
  의 W=1.0 dip(51.54 < W=0.95 54.46, H_653 기록)이 본 H 에서 Δ 정의(W=1 full ring)와 만나 magnitude
  비단조에 기여.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 stream/cap 축소 NOT 적용 — full 측정** — 본 run 은 full 5-stream(n=5) × cap=3 × 3-point
   W grid {0, 0.5, 1.0} (12 big_phi_bounded calls) 정상 실행. 무거운 한 run 회피용 fallback
   (3-stream/cap=2 또는 W-grid 축소)을 사전 명시했으나 **단일 sync run 41.1s wall (<60s)** 로
   **불필요**. stream/cap 축소 없이 full 측정 (foreground synchronous only, NO bg fork, NO monitor).
2. **C3.2 class 라벨 = canonical Wolfram ECA taxonomy** — rule184=class-II(additive/traffic),
   rule90·rule30=class-III, rule110=class-IV(complex/universal). H_653 와 동일 라벨. class-III 내부
   순위(rule30 vs rule90)는 본 측정에서 9.72 vs 7.50 으로 분리 약함 — class 간 분기(II 51.54 vs III
   ~8 vs IV 41.71)가 주신호. **단, 그 class 간 분기 자체가 비단조** — 이것이 핵심 negative.
3. **C3.3 trivial-baseline caveat — Δ = Φ_coll(W=1) 로 환원** — Σ Φ_parts(W=0)=0 (self-loop
   single-cell, H_635 anchor)이므로 Δ = Φ_collective(W=1) 절대값. 즉 본 H 의 "super-additivity
   magnitude" 는 사실상 full-ring collective-Φ 절대값이며, 이는 substrate 의 절대 Φ floor 에 종속.
   rule184 가 Δ 最高인 것은 additive 결합이 full ring 에서 큰 절대 Φ 를 만들기 때문 — non-zero
   individual baseline(각 stream n≥2 substrate)으로 재검정하면 sign 자체가 더 엄격해짐(§10 N1).
   **이 caveat 가 FALSIFIED 를 약화하지 않는다** — 가설은 명시적으로 "Δ 가 class 단조" 였고,
   어떤 baseline 정의(=H_635 SSOT)로도 Δ 는 비단조.
4. **C3.4 homogeneous cohort [rule×5] only** — 각 rule 단일 동질 cohort. heterogeneous mix-class
   cohort 의 super-additivity 는 별도(§10 N2).
5. **C3.5 sys_state=0 only** (IIT-canonical anchor). 2^5=32 state 가중평균 미수행.
6. **C3.6 cap=3 on n=5** (H_635/H_653 cap 상속) — purview search capped, 보수적 lower-bound.
   cap-monotone 으로 절대값은 cap↑ 시 상승하나, 비단조 패턴(rule184 > rule110 > rule30 > rule90)이
   cap-sensitivity 로 단조로 역전될지는 별도 검정(§10 N3). 현 cap=3 측정으로는 명백히 비단조.
7. **C3.7 deterministic single trajectory** (NO RNG) — re-run byte-identical (engine replication:
   rule110 Φ(W=1)=41.7124 가 H_635 C1·H_653 rule110 W=1.0 과 정확히 일치).
8. **C3.8 negative 의 의미** — 본 H 는 한 축(super-additivity magnitude)을 deterministic 하게
   ruled-out 하는 closed-negative. "Wolfram class = 의식 통합량 분류자" 메타-축이 *convexity*
   (H_653)에서는 서나 *magnitude* 에서는 서지 못함을 보임. 메타-축의 적용 범위를 정직하게 좁히는 결과.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F655.1 SUPERADD-MONOTONE | Δ(110)≥Δ(30)≥Δ(90)≥Δ(184) | 41.71 ≥ 9.72 ≥ 7.50 이나 ≥ 51.54 위반 | **FAIL** |
| F655.2 CLASS-IV-MOST-SUPERADD | Δ(110) = max | max = Δ(184)=51.54 (rule184) | **FAIL** |
| F655.3 ALL-SUPERADDITIVE | Δ > 0 ∀ rule | 4/4 Δ>0 (51.54·7.50·9.72·41.71) | **PASS** |
| F655.4 ADDITIVE-LEAST | Δ(184) < Δ(110) | 51.54 > 41.71 (역) | **FAIL** |
| F655.5 SIGMA-PARTS-ZERO | Σ Φ_parts(W=0) = 0 ∀ rule | 4/4 Σ=0.0 (clean anchor) | **PASS** |
| F655.6 BOUND | Φ_coll ≥ 0, Δ finite | 全 충족 | **PASS** |

**aggregate: 3 PASS / 3 FAIL** — CORE F655.1 FAIL → FALSIFY 조건 충족 → 🔴 FALSIFIED.
super-additivity magnitude Δ 가 Wolfram class 에 비단조이며 가설 방향과 정반대(class-II 最高).
H_635 의 super-additivity *방향*(F655.3·F655.5 PASS)은 보존되나 *크기의 class-단조성* 은 기각.

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h655_collective_superadditivity_substrate_class_2026_05_28/run_h655.hexa`
  (hexa-native, deterministic; H_635/H_653 engine 재사용, super-additivity Δ 측정으로 변경)
- log: `UNIVERSE/state/h655_collective_superadditivity_substrate_class_2026_05_28/run.log` (full stdout verbatim)
- result: `UNIVERSE/state/h655_collective_superadditivity_substrate_class_2026_05_28/result.json` (machine-readable)
- engine deps: `stdlib/consciousness/iit4_bigphi.hexa` · `iit4_bounded.hexa` · `iit4_tpm.hexa`
  (hexa-lang stdlib SSOT, H_635/H_653 와 동일)
- replay (selfhosted, fix-1180 우회, mac-local, $0): `HEXA_MAC_BUILD_OK=1
  HEXA_LANG=<hexa-lang-root> hexa.real.bak-2026-05-22-pre-no-hxc build run_h655.hexa -o /tmp/h655.bin
  && codesign -s - --force /tmp/h655.bin && /tmp/h655.bin` — wall ~41s ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]]

---

## 10. Next-list / Backlog

- **N1** `collective-superadditivity-nonzero-baseline` — H_635-style 각 stream 을 n≥2 substrate 로
  만들어 Σ Φ_parts ≠ 0 인 진짜 Σ-baseline 으로 Δ 재정의 (C3.3 trivial-baseline 해소). 비단조가 보존되는지.
- **N2** `collective-superadditivity-heterogeneous-cohort` — mix-class cohort([110,30,90,184,110])의
  Δ 가 구성 rule 의 어떤 함수(max/mean/dominant)인지 (C3.4).
- **N3** `collective-superadditivity-cap-sweep` — cap∈{2,3,4}에서 Δ 의 비단조 패턴 robustness —
  cap↑ 가 rule184 > rule110 역전을 단조로 만드는지 (C3.6, shard-parallel).
- **N4** `convexity-vs-magnitude-class-decoupling` — H_653 convexity-monotone × H_655 magnitude-비단조
  의 분기를 정량 — 어떤 normalized 측도가 class 단조이고 어떤 절대 측도가 아닌지의 closed-form 경계
  (메타-축 적용범위 정밀화).
- **N5** `collective-superadditivity-state-marginal` — sys_state=0 anchor → 2^5 state 가중평균 Δ (C3.5).

---

## 양방향 sibling

- super-additivity 부모: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, super-additive 5/5, Σ-baseline=0)
- sister 메타-축 (방향 분기): [H_653_collective_convexity_substrate_class.md](H_653_collective_convexity_substrate_class.md) (축 G×F, convexity monotone-in-class)
- collective ultradian: [H_643_collective_ultradian_phi_envelope.md](H_643_collective_ultradian_phi_envelope.md) (축 G×F, r=0.568)
- 비단조 anchor: [H_618_collective_gz_inverse_u_derivative_peak.md](H_618_collective_gz_inverse_u_derivative_peak.md) (collective inverse-U)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round-9 메타-축 (Wolfram class as Φ classifier) cross-link
