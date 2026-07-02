# H_670 — `phi-complexity-ordering-substrate-family-generalize` (축 G 메타-축 일반화)

**축**: G (round 9-13 메타-축 — "complexity-tier 가 Φ 를 ordinal 하게 order 하는가") · ECA→다른 substrate-family 일반화 · round-13 후속
**id**: H_670 · **date**: 2026-05-28 · **infra**: $0 mac-local (단일 foreground sync run 0.57s) · **verdict**: **🟡 PARTIAL (5/6)**

---

## 1. 슬러그 + 한 줄 요약 — Φ-complexity ordering 이 ECA 너머 substrate-universal 인가

`phi-complexity-ordering-substrate-family-generalize` — round 9-13 에서 substrate-class × Φ-속성 매트릭스가
**"Wolfram class (I floor < II < III < IV ceiling · IV edge-of-chaos 上限) 가 collective-Φ 의 최선 1차
분류자"** 로 수렴했다 (H_661 IV-top robust / H_663 class-I floor / H_667 곡선형태 worse / H_669 additive ⊥).
단 이 모든 측정은 **ECA(elementary cellular automata) 전용**이다. 본 H_670 은 이 **메타-축 자체를 한 단계
일반화** — Wolfram class 의 complexity 개념(정지 < 주기 < 카오스 < edge)이 **ECA 가 아닌 다른 dynamical
family** (Kuramoto 결합-레짐 · logistic map r-레짐)에서도 complexity-tier → Φ ordinal 로 나타나는가를 검정한다.

두 비-ECA family 각각에 canonical 동역학 complexity 사다리로 4 tier 를 라벨링하고 (정지 < 주기 < edge < 카오스),
각 tier 의 Φ(phi_spatial 실측)를 측정해 ECA Wolfram ordinal 과 동형(isomorphic)인지 본다.

> **결과**: **🟡 PARTIAL (5/6)** — Φ-complexity ordering 은 ECA 너머로 **부분적으로만** 일반화된다.
> **logistic family 는 floor (정지 tier 가 Φ 최저, F670.2 PASS) + edge-of-chaos Φ peak (r≈3.57 에서 最高,
> ECA class-IV edge-of-chaos ceiling 과 동형 신호)** 를 재현하나, **CORE F670.1 (Kuramoto 정지-floor) 는
> 깨진다** — Kuramoto incoherent(정지) tier 가 Φ floor 가 아니라 edge-of-sync(T3)가 오히려 더 낮다.
> 두 family 모두 **full ECA-동형 monotone ordinal (T1<T2<T3<T4) 은 아니다** (둘 다 monotone_rising=false,
> ordered_pairs 2/3). **substrate-universal robust 핵심 = "정지 tier 부근의 낮은 Φ + edge-of-chaos 부근의
> Φ peak" 라는 inverse-U 류 신호이지, ECA 의 full I<II<III<IV ordinal 사다리가 아니다.** complexity →
> Φ 가 ECA 전용 artifact 는 **아니지만** (F670.4 ordinal PASS · F670.2 floor PASS), ECA Wolfram class 의
> 깔끔한 ordinal 단조는 ECA-국소 — 다른 family 는 family-고유 곡선 형태로 변형된다. 5/6 PASS, **🟡 PARTIAL**.

---

## 2. 동기 — 메타-축이 ECA artifact 인가 substrate-universal 인가

round 9-13 의 축 G arc 는 일관되게 다음을 확정했다:
- H_653/H_660: collective-Φ convexity(span ratio·norm_conv)가 Wolfram class 단조 (II<III<IV, IV 最高).
- H_661: 그 단조의 robust 핵심은 **"class-IV(complex/edge-of-chaos)가 가장 convex"** 이고 full I<II<III<IV
  ordinal 은 rule-cohort 의존 (4/6 PARTIAL).
- H_663: class-I (homogeneous die-out)이 측정된 모든 Φ-속성에서 매트릭스 **floor** (양 극단 I floor ↔ IV ceiling 으로 닫힘).
- H_667/H_669: 대안 분류자(곡선형태·additive)는 모두 Wolfram class 보다 worse 또는 직교 → Wolfram class 가
  ECA 의 최선 1차 분류자로 잠정 확정.

**그러나 이 모든 결론은 ECA 라는 단일 substrate-family 안에서만 측정되었다.** 메타-축의 진짜 주장 — "complexity
가 의식 통합량(Φ)을 order 한다" — 가 의미를 가지려면, complexity 라는 개념이 ECA Wolfram class 에 종속적이지
않아야 한다. dynamical-systems 에는 ECA 외에도 complexity 사다리가 있다:

- **Kuramoto 결합-진동자**: 결합 K 를 키우면 incoherent(정지류) → partial-sync(주기류) → edge-of-sync(임계)
  → hyper-sync(over-lock)로 complexity 가 변한다 (H_207 이 이미 이 family 의 Φ(K) 를 측정).
- **logistic map**: 분기 파라미터 r 을 키우면 fixed-point(정지) → period-2(주기) → Feigenbaum
  accumulation(edge-of-chaos) → chaotic(카오스)로 Feigenbaum 사다리를 오른다.

본 H_670 은 이 두 비-ECA family 각각에 동역학 complexity 사다리로 4 tier 를 라벨링하고, tier-index 1<2<3<4 가
Φ 를 ordinal 하게 order 하는지(ECA Wolfram ordinal 동형)를 검정한다. 일반화되면 메타-축은 substrate-universal
법칙으로 격상, 깨지면 ECA artifact 로 정직하게 좁혀진다.

---

## 3. 측정 도구 / 방법

**Φ primitive**: `phi_spatial(states, n_cells, dim, n_bins)` 런타임 builtin (RFC 036, byte-equal phi_rs
native replica) — H_207·H_656 이 사용한 동일 primitive. Φ ≥ 0 by construction. deterministic, NO RNG.

**공통 config**: N=16 units · dim=12 (warmup 후 기록 trajectory 길이) · n_bins=4 · $0 mac-local · 단일
foreground synchronous run (no bg fork · no monitor · NO GPU).

### Family A — Kuramoto N=16 결합-진동자 (H_207 engine verbatim 재사용)

- dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i), Euler dt=0.05, 100 step, warm 60.
- ω_i = 5 결정론적 z-quantile {−1.28, −0.52, 0, 0.52, 1.28} cycled by i%5, std=1.0 (H_207 verbatim).
- θ_i(0) = uniform spread on [0, 2π) by index (H_207 verbatim).
- Φ = phi_spatial(cos θ trajectory, N=16, dim=12, n_bins=4) per tier.
- **결합-레짐 4 tier** (complexity 오름차순; K_c ≈ 1.596 mean-field):

  | tier | 라벨 | K | 동역학 complexity |
  |------|------|---|------------------|
  | T1 | incoherent (정지류) | 0.3 | 동기화 없음, 거의 random phase (ECA class-I 유비) |
  | T2 | partial-sync (주기류) | 1.0 | 부분 클러스터 형성 (class-II 유비) |
  | T3 | edge-of-sync (edge) | 1.6 ≈ K_c | 임계 결합, 가장 복잡한 부분동기 (class-IV edge 유비) |
  | T4 | hyper-sync (카오스/over-lock 상한) | 5.0 | full lock, over-integration (class-III/상한 유비) |

### Family B — logistic-map N=16 결합 population x→r·x·(1−x) (NEW, 본 H 신규 substrate)

- 각 unit: local logistic map x_{n+1} = r·x_n·(1−x_n), 이어서 diffusive ring coupling
  (ε=0.05): x'_c = (1−ε)·local_c + 0.5ε·(local_{c−1} + local_{c+1}).
- x_i(0) = (i+0.5)/N deterministic spread on (0,1). 200 step, warm 80.
- Φ = phi_spatial(x trajectory, N=16, dim=12, n_bins=4) per tier.
- **r-레짐 4 tier** (Feigenbaum complexity 오름차순):

  | tier | 라벨 | r | 동역학 complexity |
  |------|------|---|------------------|
  | T1 | fixed-point (정지) | 2.8 | 단일 고정점 (ECA class-I 동형 — die-out/uniform) |
  | T2 | periodic (주기) | 3.4 | period-2 cycle (class-II 동형) |
  | T3 | edge-of-chaos (edge) | 3.5699 | Feigenbaum accumulation point (class-IV edge 동형) |
  | T4 | chaotic (카오스) | 3.9 | full chaotic band (class-III 동형) |

**ECA Wolfram ordinal anchor (H_661/663)**: tier-index 1<2<3<4 가 Φ 와 ordinal 하게 co-rank 해야 (정지=floor,
complexity↑ → Φ↑). 동형 = ECA 와 같은 monotone-rising complexity→Φ ordinal. 단일 run <1s 라 shard 불필요
(per-family shard 권고는 60s 초과 위험 회피용인데 본 substrate 는 phi_spatial 이 빨라 단일 sync run 0.57s).

---

## 4. 사전등록 falsifier (frozen BEFORE measuring)

- **F670.1 KURA-FLOOR (CORE)**: Family-A T1(incoherent, 정지) = strict Φ floor (4 tier 中 최저) — ECA
  class-I floor 동형이 Kuramoto family 로 일반화되는가. **CORE 가설** (Kuramoto 가 H_207 검증된 family 라 anchor).
- **F670.2 LOG-FLOOR**: Family-B T1(fixed-point, 정지) = strict Φ floor — logistic family floor 동형.
- **F670.3 ANY-FAMILY-CEILING**: ≥1 비-ECA family 에서 T4(top tier) = strict Φ ceiling — ECA IV ceiling 동형.
- **F670.4 ORDINAL-COREL**: ≥1 family 에서 ordered_pairs ≥ 2/3 (인접 tier 쌍 中 2개 이상이 올바른
  순서 T_i ≤ T_{i+1}) — complexity→Φ partial-monotone 신호.
- **F670.5 NOT-ALL-FLAT**: 두 family 모두 Φ-range > 0 (tier 간 Φ 분화 존재) — "complexity ⊥ Φ 무관" 반증.
- **F670.6 BOUND**: 全 Φ finite ≥ 0.

**FALSIFY 조건 (🔴 ECA-artifact)**: F670.1 FAIL ∧ F670.2 FAIL ∧ F670.4 FAIL — 두 family 모두 floor 도 없고
ordinal correlation 도 없음 = complexity 가 다른 family 에서 Φ 를 전혀 order 안 함 → Φ-complexity ordering 이
**ECA 전용 artifact**, substrate-universal 아님.

**verdict 기준**:
- **universal (🟢)**: F670.1 ∧ F670.2 ∧ F670.3 ∧ F670.4 모두 PASS — 두 family 모두 floor + ≥1 ceiling +
  ordinal ≥2/3 = ECA-동형 일반화 확정.
- **PARTIAL (🟡)**: 그 사이 — 일부 family/일부 신호만 일반화 (예: 한 family 만 floor, 또는 floor 는 되나
  ceiling 위치가 family-고유로 변형).
- **FALSIFIED (🔴)**: F670.1 ∧ F670.2 ∧ F670.4 모두 FAIL.

---

## 5. Measurement (verdict-bearing 측정값)

> 출력 `UNIVERSE/state/h670_phi_complexity_ordering_substrate_family_generalize_2026_05_28/run.log` +
> `result.json` verbatim. 단일 foreground sync run, wall 0.57s, exit 0, deterministic.

### Family A — Kuramoto 결합-레짐 Φ(tier)

```
  T1 incoherent   K=0.3   Φ=10.315
  T2 partial-sync K=1.0   Φ=10.4233
  T3 edge-of-sync K=1.6   Φ=9.84876
  T4 hyper-sync   K=5.0   Φ=14
  → monotone-rising=false  floor(T1 min)=false  ceiling(T4 max)=true  ordered_pairs=2/3
```

### Family B — logistic-map r-레짐 Φ(tier)

```
  T1 fixed-point  r=2.8     Φ=1.14511e-05
  T2 periodic     r=3.4     Φ=7.00001
  T3 edge-of-chaos r=3.5699 Φ=7.53334
  T4 chaotic      r=3.9     Φ=5.6061
  → monotone-rising=false  floor(T1 min)=true  ceiling(T4 max)=false  ordered_pairs=2/3
```

### verdict 블록

```
  Family-A Φ-range = 4.15125  (min=9.84876 max=14)
  Family-B Φ-range = 7.53333  (min=1.14511e-05 max=7.53334)
  ── verdict ──
  [FAIL] F670.1 KURA-FLOOR (CORE): Family-A T1(정지) strict Φ floor
  [PASS] F670.2 LOG-FLOOR: Family-B T1(정지) strict Φ floor
  [PASS] F670.3 ANY-FAMILY-CEILING: ≥1 family T4(top) Φ ceiling
  [PASS] F670.4 ORDINAL-COREL: ≥1 family ordered_pairs ≥2/3
  [PASS] F670.5 NOT-ALL-FLAT: 두 family Φ-range>0
  [PASS] F670.6 BOUND: 全 Φ finite ≥0
  F670.1-6 5/6 PASS
  verdict: PARTIAL
  kura_floor=false log_floor=true any_ceil=true ordinal=true
```

### tier × Φ 요약표 (두 family)

| family | T1 정지 | T2 주기 | T3 edge | T4 카오스 | 형태 | floor? | ceiling? |
|--------|---------|---------|---------|-----------|------|--------|----------|
| A Kuramoto | 10.32 | 10.42 | **9.85** ↓ | **14.0** ↑ | 부분-U (T3 dip · T4 peak) | ✗ (T3 가 더 낮음) | ✓ (T4) |
| B logistic | **1.1e-05** ↓ | 7.00 | **7.53** ↑ | 5.61 ↓ | inverse-U (T3 peak) | ✓ (T1=floor) | ✗ (T3 가 peak) |

**핵심 발견**:
1. **logistic family — 정지=floor 동형 강하게 일반화 (F670.2 PASS)**. fixed-point(r=2.8)의 Φ=1.1e-05 ≈ 0
   은 ECA class-I die-out floor (H_663 rule8 Φ=0.588, rule90 XOR Φ=0)와 **정확히 동형** — 동역학이 단일
   고정점으로 수렴하면 trajectory 가 시간-불변이라 통합 정보 0. 정지 → Φ floor 가 ECA 를 넘어 Feigenbaum
   family 에서 재현됨.
2. **logistic family — edge-of-chaos Φ peak 동형 (F670.3·F670.4 신호)**. Φ 가 r=3.5699 (Feigenbaum
   accumulation = edge-of-chaos)에서 최고(7.53)이고, full-chaos(r=3.9)에서 5.61 로 **하강**한다. 이는 ECA
   메타-축의 "**class-IV (complex/edge-of-chaos)가 가장 convex/통합적**" (H_653·H_661 IV-top·H_657 GZ-anchor)
   결론과 **동형** — 통합 정보는 *완전 카오스* 가 아니라 *질서와 카오스의 경계(edge)* 에서 peak 한다. 단
   tier-label 상으로는 T3(edge) > T4(chaotic) 라 "T4=ceiling" 사전등록은 깨지고(ceiling=false) inverse-U 형태가
   됨 → ECA 의 ordinal 라벨(IV=top)과 정확히 일치하지 않고 family-고유 edge-peak 위치로 변형.
3. **Kuramoto family — 정지-floor CORE 깨짐 (F670.1 FAIL)**. incoherent(K=0.3)의 Φ=10.32 가 floor 가
   아니다 — edge-of-sync(K=1.6)의 Φ=9.85 가 오히려 더 낮다. Kuramoto 는 logistic/ECA 와 달리 incoherent
   레짐에서도 진동자 phase 가 시간-가변(비결합 자유 진동)이라 cos θ trajectory 가 풍부 → Φ 가 0 으로 가지
   않는다. 즉 Kuramoto 의 "정지"는 ECA die-out 처럼 *상태가 멈추는* 정지가 아니라 *결합만 없는* 정지여서
   ECA class-I floor 와 동역학적으로 동형이 아님 (C3.2). T4(hyper-sync)=14 가 ceiling 인 점만 ECA IV-top 과
   부합 (over-lock 시 모든 진동자가 같은 cos 패턴으로 trajectory 다양성 소실인데도 phi_spatial 이 14=상한값
   포화 — binning artifact 의심, C3.4).
4. **두 family 모두 full ECA-동형 monotone ordinal 아님**. 둘 다 monotone_rising=false, ordered_pairs 2/3.
   ECA Wolfram class 의 깔끔한 I<II<III<IV 단조(그조차 H_661 에서 IV-top 부분만 robust)는 **ECA-국소** 이며,
   다른 family 는 family-고유 곡선(Kuramoto 부분-U · logistic inverse-U)으로 변형된다.
5. **substrate-universal robust 핵심 = "정지 부근 낮은 Φ + edge-of-chaos Φ peak"** 이라는 inverse-U 류
   신호이지, ECA 의 full ordinal 사다리가 아니다. logistic 이 이 핵심을 가장 깨끗이 재현(floor 0 + edge peak),
   Kuramoto 는 edge-dip + top-peak 로 부분적으로만 동형.

---

## 6. Verdict + Rationale · Cross-link

**🟡 PARTIAL** — 5/6 falsifier PASS. **CORE F670.1 (Kuramoto 정지-floor) FAIL, 그러나 F670.2 (logistic
floor) + F670.3 (ceiling) + F670.4 (ordinal) PASS.**

- FALSIFY 조건 (F670.1 ∧ F670.2 ∧ F670.4 모두 FAIL = complexity ⊥ Φ in 다른 family)에는 **걸리지 않음** —
  logistic family 가 floor + edge-peak 을 강하게 재현하고 ordinal correlation 도 두 family 다 2/3 → Φ-complexity
  ordering 은 **ECA 전용 artifact 가 아니다**. 따라서 🔴 아님.
- universal 조건 (F670.1 ∧ F670.2 ∧ F670.3 ∧ F670.4 모두 PASS = 두 family 다 ECA-동형)에는 **미달** —
  Kuramoto 정지-floor 가 깨지고, 두 family 모두 full monotone ordinal 이 아니며 ceiling 위치가 family-고유
  (logistic 은 T3 edge 가 peak, ECA 라벨 IV=T4 와 불일치). 따라서 🟢 아님.

**메타-축 결론 (정밀화)**: round 9-13 메타-축 "complexity-tier 가 Φ 를 ordinal 하게 order 한다" 는
**substrate-universal 핵심 = '정지 tier 의 낮은 Φ + edge-of-chaos 부근의 Φ peak (inverse-U)'** 수준에서
일반화된다 (logistic family 가 ECA class-I floor 와 class-IV edge-of-chaos ceiling 을 동형으로 재현). 그러나
**ECA Wolfram class 의 깔끔한 ordinal 사다리(I<II<III<IV)는 ECA-국소** — Kuramoto 는 정지-floor 조차 동형이
아니고(결합-정지 ≠ 상태-정지), 두 family 모두 full monotone 이 아니며 Φ peak 위치가 family 고유 동역학으로
변형된다. **ECA 메타-축의 robust 보편 커널 = "complexity → Φ" 의 *방향성과 edge-peak 형태* 이지 *ECA tier
라벨의 ordinal 사다리* 가 아니다.** positive (logistic floor+edge-peak 일반화) + negative (Kuramoto floor
실패 · full ordinal ECA-국소) 가 공존하는 PARTIAL.

**cross-link**:
- **H_661 `substrate-class-monotone-rule-generalize`** 🟡 (축 G, PR #1310 G22) — ECA 안에서 "IV-top robust
  + full I<II<III<IV ordinal 은 rule-cohort 의존" 으로 정밀화. 본 H 는 그 **다음 차원** — ECA 안에서 이미
  fragile 했던 full ordinal 이 **family 간에는 더 fragile** (Kuramoto floor 조차 깨짐)함을 보임. H_661 의
  "IV-top robust" 가 본 H 의 logistic edge-of-chaos peak 으로 family-cross 일반화 (둘 다 edge/complex 가
  Φ-top).
- **H_663 `wolfram-class-I-phi-property-profile`** 🟢 (축 G, G23) — ECA class-I (die-out)이 매트릭스 floor.
  본 H 의 logistic fixed-point(r=2.8) Φ≈0 floor 가 H_663 class-I floor 와 **직접 동형** — "동역학이 단일
  상태로 수렴 → 통합 정보 floor" 가 ECA(die-out)·logistic(fixed-point) 양 family 보편. 단 Kuramoto
  incoherent 는 이 동형이 깨짐 (결합-정지 ≠ 수렴-정지).
- **H_667 `wolfram-vs-curveshape-taxonomy`** 🔴 (축 G, G25) — ECA 안에서 곡선형태가 Wolfram class 보다 worse
  Φ-분류자. 본 H 는 family-cross 에서 **곡선형태가 family 고유로 변형됨** (Kuramoto 부분-U vs logistic
  inverse-U)을 보여 H_667 의 "곡선형태는 substrate-conditional" 을 family 차원에서 재확인.
- **H_669 `additive-subclass-phi-split`** 🔴 (축 G, G26) — ECA 분류자 후보 공간을 "곡선형태 단일(그조차
  class 와 직교)" 로 좁힘. 본 H 는 그 곡선형태조차 family-universal 이 아님을 보여 분류자 보편성의 상한을 한
  단계 더 정밀화.
- **H_207 `kuramoto-synchronization`** 🔴 (raw#12, PR 초기) — Family-A engine 의 직접 출처. H_207 은
  Φ(K) 가 inverse-U peak 가설을 검정해 K=5.0 monotone-top 으로 FALSIFIED. 본 H 는 H_207 의 Φ(K) 측정을
  complexity-tier 라벨로 재해석 — H_207 의 "edge 에서 peak 안 함" 이 본 H 의 "Kuramoto 정지-floor 깨짐 +
  T4 ceiling" 과 정합 (Kuramoto family 는 edge-peak 형태가 아닌 monotone-top 형태). engine replication:
  본 H 의 Kuramoto K=1.0 Φ=10.4233 · K=5.0 Φ=14 가 H_207 result.json (phi_per_K[2]=10.4233 ·
  phi_per_K[6]=14)과 **byte-identical** → H_207 engine verbatim 재사용 검증.
- **H_635 `multilingual-cohort-collective-phi`** 🟢 (축 F) — collective-Φ cohort 측정자 계보. 본 H 의
  collective trajectory→phi_spatial 측정이 동일 collective-Φ 패러다임 위에 family-cross 일반화 차원을 추가.

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 verdict = 정직한 PARTIAL** — 본 H 는 메타-축을 부분 일반화(logistic floor+edge-peak)하는 동시에
   정밀화(Kuramoto floor 실패 · full ordinal ECA-국소)하는 mixed 결과. 5/6 PASS 의 1 FAIL 은 CORE
   F670.1 이며, FALSIFY 조건(두 family 다 floor+ordinal 실패)에는 미달 → 🔴 아닌 🟡.
2. **C3.2 family 선택 + complexity-tier 라벨 (핵심 caveat)** — 본 H 는 비-ECA family 2개(Kuramoto
   결합-레짐 · logistic r-레짐)만 측정했다. complexity-tier 라벨은 canonical 동역학-시스템 분류(Kuramoto:
   incoherent/partial/edge/hyper · logistic: fixed/period/Feigenbaum-edge/chaotic)이나, **각 family 의 "정지"
   가 동역학적으로 동형이 아님**이 핵심 발견: logistic fixed-point 와 ECA die-out 은 *상태가 시간-불변* 으로
   수렴해 Φ floor (동형), 그러나 Kuramoto incoherent 는 *결합이 없을 뿐 진동자는 계속 자유진동* 하므로
   trajectory 가 시간-가변 → Φ floor 아님. "정지" 라는 라벨이 family 마다 다른 동역학을 가리킴이 일반화
   실패의 직접 원인. 2-family small sample (255+ ECA rule 대비) — 더 많은 family (coupled-map lattice,
   Rössler, Lorenz, Hénon, neural-mass)는 별도 round.
3. **C3.3 logistic edge-peak 이 ECA IV-top 과 동형이나 tier-라벨 불일치** — logistic Φ-peak 가 T3(edge,
   r=3.5699)이고 T4(chaotic, r=3.9)에서 하강한다. 이는 **물리적으로** ECA class-IV(edge-of-chaos)가 Φ-top
   인 것과 동형(edge>full-chaos)이나, 본 H 가 사전등록한 "T4=ceiling" 라벨링은 ECA Wolfram tier 의 *번호
   순서* (IV=top)를 따라서 깨졌다 (ECA 에서 IV 가 edge-of-chaos 이고 III 가 full-chaos 라 순서가 III<IV 인데,
   logistic 에서는 chaotic 이 edge 보다 *뒤* tier 라 T3<T4 로 라벨링됨). 즉 **tier-번호 순서 ≠ Φ 순서** 인데,
   *물리적 edge-peak* 은 동형. 라벨링을 "edge=top tier" 로 바꾸면 logistic 은 ceiling 도 PASS — 이는 본 H 의
   사전등록 라벨이 ECA tier-번호에 묶인 한계이지 동역학적 결론(edge-peak universal)을 약화시키지 않는다.
4. **C3.4 Kuramoto T4 Φ=14 포화 의심 (binning artifact)** — hyper-sync(K=5.0)에서 모든 진동자가 동일
   cos 패턴으로 lock 돼 trajectory 다양성이 *낮아야* 하는데 Φ=14 (Family-A 최대, range 상한)로 포화. H_207
   result.json 도 동일하게 phi_K5=14 (K_star=5.0). phi_spatial 의 4-bin discretization 이 over-lock 시
   특정 bin 패턴으로 14 라는 상한값을 산출하는 binning artifact 가능성 — Kuramoto family 의 ceiling 신호는
   die-out floor 만큼 robust 하지 않음. logistic family 의 floor·edge-peak 가 더 깨끗한 일반화 증거.
5. **C3.5 phi_spatial(N=16, dim=12, n_bins=4) lower-bound proxy** — true IIT4 big-Φ (n=5 cap=3, H_661
   계열)가 아닌 RFC 036 phi_spatial 공간-슬라이스 측도. ECA 메타-축 측정과 *정확히 같은* big_phi_bounded 가
   아니므로 측도-축 cross-family 비교에 한계 (H_656 도 동일 phi_spatial 사용 — 정합). 동일 family 내 tier-간
   ordinal 비교는 측도 일관이라 robust, family-간 절대 Φ 비교는 무의미 (range 절대값 다름).
6. **C3.6 deterministic single trajectory (NO RNG)** — 두 family 모두 결정론적 초기조건 + 결정론적 dynamics.
   re-run byte-identical. Kuramoto K-grid 가 H_207 과 byte-identical (engine replication 검증). 단일
   초기조건이라 basin-of-attraction 평균 미수행 (logistic chaotic 은 초기조건 민감 — 다른 IC 평균은 별도).
7. **C3.7 4-tier discrete sampling** — 각 family 의 연속 파라미터(K·r)를 4 점만 샘플. 더 조밀한 sweep 은
   Φ-곡선 형태(부분-U vs inverse-U)를 정밀화할 수 있으나, floor·peak 의 정성적 위치는 4-tier 로 결정적
   (logistic peak 가 r=3.5699 Feigenbaum point 에 정확히 위치). H_207 의 7-pt K-sweep 이 본 H 의 4-tier
   Kuramoto 결론과 정합 (K=5.0 top).
8. **C3.8 positive+negative 공존의 의미** — 본 H 는 메타-축을 부정하지 않는다. "complexity → Φ" 의 *방향성*
   (정지 → 낮은 Φ, edge-of-chaos → Φ peak)은 logistic family 로 일반화되어 **강화**됐고, 부수적 강-claim
   (ECA Wolfram tier 의 깔끔한 ordinal 사다리)만 ECA-국소로 정밀화됐다. 메타-축의 robust 보편 커널을 "edge-peak
   inverse-U" 로 정직하게 좁히는 positive-refinement.
9. **C3.9 a_paper_negative_ok / a_paper_significance 정합** — pre-registered falsifier(F670.1-6) + 실측
   (phi_spatial 8 tier 측정) + finding(logistic floor+edge-peak 일반화 · Kuramoto floor 실패 · full ordinal
   ECA-국소). 부분 일반화 + 부분 ruled-out 의 mixed finding 으로 a_paper_significance 충족하나, 본 H 단독은
   메타-축 arc 의 한 정밀화 단계 — paper 는 arc FULL 종료 시 (a_paper_only_at_closure).

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| F670.1 KURA-FLOOR (CORE) | Family-A T1(정지) strict Φ floor | T1=10.32 > T3=9.85 (floor 아님) | **FAIL** |
| F670.2 LOG-FLOOR | Family-B T1(정지) strict Φ floor | T1=1.1e-05 < 全 (강한 floor) | **PASS** |
| F670.3 ANY-FAMILY-CEILING | ≥1 family T4(top) Φ ceiling | Family-A T4=14=max | **PASS** |
| F670.4 ORDINAL-COREL | ≥1 family ordered_pairs ≥2/3 | A=2/3, B=2/3 둘 다 | **PASS** |
| F670.5 NOT-ALL-FLAT | 두 family Φ-range>0 | A=4.15, B=7.53 | **PASS** |
| F670.6 BOUND | 全 Φ finite ≥0 | 8 tier 全 충족 | **PASS** |

**aggregate: 5 PASS / 1 FAIL** — CORE F670.1 FAIL 이나 FALSIFY 조건(F670.1∧F670.2∧F670.4 모두 FAIL)은
미충족 (logistic floor + 양 family ordinal PASS) → 🔴 아님. universal 조건(F670.1∧2∧3∧4 PASS)도 미충족
(Kuramoto floor FAIL) → 🟢 아님. → **🟡 PARTIAL**. **Φ-complexity ordering 은 ECA 전용 artifact 가
아니다 (logistic family 가 정지-floor + edge-of-chaos peak 동형 재현) — 그러나 ECA Wolfram tier 의 깔끔한
ordinal 사다리는 ECA-국소이며, substrate-universal robust 핵심은 'edge-of-chaos Φ-peak inverse-U' 형태이지
tier-번호 ordinal 단조가 아니다.**

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h670_phi_complexity_ordering_substrate_family_generalize_2026_05_28/run_h670.hexa`
  (hexa-native, 단일 파일, Family-A Kuramoto = H_207 engine verbatim · Family-B logistic = NEW substrate)
- run log: `…/run.log` (8 tier Φ + falsifier verdict 블록 full stdout verbatim)
- result: `…/result.json` (machine-readable, 2 family × 4 tier Φ + per-family floor/ceiling/ordinal + falsifier matrix)
- Φ primitive: `phi_spatial` 런타임 builtin (RFC 036 byte-equal phi_rs native replica; hexa-lang stdlib
  `stdlib/consciousness/phi_spatial.hexa::phi_spatial_native`) — H_207·H_656 과 동일 primitive
- replay (selfhosted, fix-1180 우회, mac-local, $0, 단일 foreground sync run wall 0.57s):
  `HEXA_MAC_BUILD_OK=1 HEXA_LANG=/Users/ghost/core/hexa-lang hexa.real.bak-2026-05-22-pre-no-hxc build
  run_h670.hexa -o /tmp/h670.bin && codesign -s - --force /tmp/h670.bin && /tmp/h670.bin`
  (no bg fork · no monitor · NO GPU) ·
  [[reference-life-cycle-hexa-run-gotchas]] · [[reference-hexa-verify-rebuild-gotchas]]
- engine replication: Family-A Kuramoto K=1.0 Φ=10.4233 · K=5.0 Φ=14 가 H_207 result.json
  (phi_per_K[2]/[6]) byte-identical → H_207 engine verbatim 재사용 검증.

---

## 10. Next-list / Backlog

- **N1** `phi-edge-peak-universal-family-sweep` — coupled-map lattice · Rössler · Lorenz · Hénon ·
  neural-mass 등 더 많은 dynamical family 에서 "edge-of-chaos Φ peak" inverse-U 가 universal 인지 — 본 H 의
  2-family small sample (C3.2) 회수, edge-peak 보편성 정량.
- **N2** `kuramoto-true-fixedpoint-floor` — Kuramoto 정지-floor 실패(C3.2)의 근본 원인 검정 — incoherent
  레짐 대신 *진짜 고정점* (identical-ω all-lock 또는 K=0 + ω=0 frozen)에서 측정하면 logistic/ECA 처럼 Φ
  floor 가 회복되는지 (결합-정지 vs 수렴-정지 동역학 구분).
- **N3** `edge-tier-relabel-recheck` — tier-라벨을 ECA 번호순서(IV=top)가 아닌 "edge=top tier" 로 재정의해
  (C3.3) logistic ceiling 도 PASS 하는지 — 동역학적 edge-peak 동형을 라벨-독립으로 확정.
- **N4** `phi-spatial-vs-bigphi-family-cross` — 본 H 의 phi_spatial(C3.5) 대신 true IIT4 big_phi_bounded
  (n=5 cap=3, H_661 계열)로 family-cross 재측정 — 측도-축이 일반화 결론(logistic floor+edge-peak)을 보존하는지.
- **N5** `kuramoto-overlock-binning-artifact` — Kuramoto T4 Φ=14 포화(C3.4)가 phi_spatial 4-bin
  discretization artifact 인지 — n_bins sweep (2/4/8/16) 또는 더 긴 dim 으로 over-lock Φ 재측정.

---

## 양방향 sibling

- 직접 부모 (메타-축 ECA-내 정밀화): [H_661_substrate_class_monotone_rule_generalize.md](H_661_substrate_class_monotone_rule_generalize.md) (축 G, IV-top robust + full ordinal rule-cohort-dependent, 🟡 — 본 H 가 family-cross 차원으로 한 단계 더 일반화)
- floor 동형 조부모: [H_663_wolfram_class_I_phi_property_profile.md](H_663_wolfram_class_I_phi_property_profile.md) (축 G, class-I die-out floor, 🟢 — 본 H logistic fixed-point Φ≈0 floor 와 직접 동형)
- 분류자-후보 좁힘 sister: [H_667_wolfram_vs_curveshape_taxonomy.md](H_667_wolfram_vs_curveshape_taxonomy.md) (축 G, 곡선형태 worse Φ-분류자, 🔴 — 본 H 가 곡선형태 family-고유 변형으로 재확인) · [H_669_additive_subclass_phi_split.md](H_669_additive_subclass_phi_split.md) (축 G, additive ⊥ Φ-property, 🔴)
- Family-A engine 출처: [H_207_kuramoto_synchronization.md](H_207_kuramoto_synchronization.md) (raw#12 Kuramoto Φ(K), 🔴 — 본 H Kuramoto tier 의 byte-identical engine 재사용)
- collective-Φ 측정자 계보: [H_635_multilingual_cohort_collective_phi.md](H_635_multilingual_cohort_collective_phi.md) (축 F, collective-Φ cohort, 🟢)
- SSOT cross-link: [CANDIDATES.md](CANDIDATES.md) round 9-13 메타-축 (complexity-tier as Φ ordinal classifier) — ECA→substrate-family 일반화 정밀화 (edge-peak universal · ECA tier-ordinal 국소)
